#!/usr/bin/env python3
"""Generate summary, classification detail, and CVE detail reports in one run."""

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import List, Optional, Tuple

from classify_request import CLASSIFICATION_LABELS, classify_request
from log_loader import (
    filter_operator_traffic,
    find_latest_log_pair,
    load_merged_logs,
    load_requests,
    load_traffic,
)
from map_cve import get_cve_catalog, identify_cves, request_matches_cve
from parse_attacks import (
    build_classification_detail,
    build_cve_detail,
    build_report,
    default_cve_detail_paths,
    default_detail_paths,
    default_report_paths,
    format_cve_detail_report,
    format_detail_report,
    format_text_report,
)


def load_log_data(
    log_dir: Path,
    requests_path: Optional[Path],
    traffic_path: Optional[Path],
    aggregated: bool,
) -> Tuple[List[dict], List[dict], Optional[List[dict]], Optional[Path]]:
    source_files = None
    req_path = requests_path

    if aggregated:
        if requests_path or traffic_path:
            print(
                "Error: --all cannot be combined with --requests or --traffic.",
                file=sys.stderr,
            )
            sys.exit(1)
        requests, traffic, source_files = load_merged_logs(log_dir)
        if not requests:
            print("Error: no log file pairs found in directory.", file=sys.stderr)
            sys.exit(1)
        return requests, traffic, source_files, None

    req_path = requests_path
    traf_path = traffic_path
    if not req_path or not traf_path:
        auto_req, auto_traf = find_latest_log_pair(log_dir)
        req_path = req_path or auto_req
        traf_path = traf_path or auto_traf

    if not req_path or not req_path.exists():
        print("Error: requests file not found.", file=sys.stderr)
        sys.exit(1)
    if not traf_path or not traf_path.exists():
        print("Error: traffic file not found.", file=sys.stderr)
        sys.exit(1)

    requests = load_requests(req_path)
    traffic = load_traffic(traf_path)
    return requests, traffic, source_files, req_path


def discover_report_targets(requests: List[dict]) -> Tuple[Counter, Counter]:
    """Return classification and CVE counts present in the loaded requests."""
    classifications = Counter()
    cves = Counter()

    for req in requests:
        classifications[classify_request(req)] += 1
        for match in identify_cves(req):
            cves[match["cve_id"]] += 1

    return classifications, cves


def write_report(text: str, data: dict, text_path: Path, json_path: Path) -> None:
    text_path.parent.mkdir(parents=True, exist_ok=True)
    text_path.write_text(text)
    json_path.write_text(json.dumps(data, indent=2))


def generate_all_reports(
    requests: List[dict],
    traffic: List[dict],
    output_dir: Path,
    req_path: Optional[Path],
    aggregated: bool,
    source_files: Optional[List[dict]] = None,
    *,
    skip_summary: bool = False,
    skip_classifications: bool = False,
    skip_cves: bool = False,
    include_empty: bool = False,
    all_catalog_cves: bool = False,
) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated = {
        "summary": None,
        "classifications": [],
        "cves": [],
        "skipped": {"classifications": [], "cves": []},
    }

    summary = build_report(requests, traffic, source_files)
    classification_counts, cve_counts = discover_report_targets(requests)

    if not skip_summary:
        text_path, json_path = default_report_paths(output_dir, req_path, aggregated)
        write_report(format_text_report(summary), summary, text_path, json_path)
        generated["summary"] = {"text": str(text_path), "json": str(json_path)}
        print(f"Summary report: {text_path}")

    if not skip_classifications:
        for classification in CLASSIFICATION_LABELS:
            count = classification_counts.get(classification, 0)
            if count == 0 and not include_empty:
                generated["skipped"]["classifications"].append(classification)
                continue

            detail = build_classification_detail(requests, traffic, classification)
            text_path, json_path = default_detail_paths(
                output_dir, classification, req_path, aggregated
            )
            write_report(format_detail_report(detail), detail, text_path, json_path)
            generated["classifications"].append(
                {
                    "classification": classification,
                    "count": count,
                    "text": str(text_path),
                    "json": str(json_path),
                }
            )
            print(f"Classification detail ({classification}, {count:,}): {text_path}")

    if not skip_cves:
        cve_ids = [entry["cve_id"] for entry in get_cve_catalog()] if all_catalog_cves else sorted(
            cve_counts,
            key=lambda cve_id: (-cve_counts[cve_id], cve_id),
        )

        for cve_id in cve_ids:
            count = sum(1 for req in requests if request_matches_cve(req, cve_id))
            if count == 0 and not include_empty:
                generated["skipped"]["cves"].append(cve_id)
                continue

            detail = build_cve_detail(requests, traffic, cve_id)
            text_path, json_path = default_cve_detail_paths(
                output_dir, cve_id, req_path, aggregated
            )
            write_report(format_cve_detail_report(detail), detail, text_path, json_path)
            generated["cves"].append(
                {
                    "cve_id": cve_id,
                    "count": count,
                    "text": str(text_path),
                    "json": str(json_path),
                }
            )
            print(f"CVE detail ({cve_id}, {count:,}): {text_path}")

    manifest_path = output_dir / "report-manifest.json"
    manifest = {
        "output_dir": str(output_dir),
        "aggregated": aggregated,
        "total_requests": len(requests),
        "classification_counts": dict(classification_counts.most_common()),
        "cve_counts": dict(cve_counts.most_common()),
        "generated": generated,
    }
    manifest_path.write_text(json.dumps(manifest, indent=2))
    print(f"Manifest: {manifest_path}")

    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Generate the attack summary report plus detail reports for every "
            "attack classification and CVE seen in the logs."
        )
    )
    parser.add_argument(
        "--dir",
        type=Path,
        default=Path("."),
        help="Directory to search for log files (default: current directory)",
    )
    parser.add_argument(
        "--requests",
        type=Path,
        help="Path to a specific requests JSONL file",
    )
    parser.add_argument(
        "--traffic",
        type=Path,
        help="Path to a specific traffic JSONL file",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("reports"),
        help="Directory for generated reports (default: reports)",
    )
    parser.add_argument(
        "--latest",
        action="store_true",
        help="Use only the latest log pair instead of aggregating all days",
    )
    parser.add_argument(
        "--skip-summary",
        action="store_true",
        help="Skip the main attack summary report",
    )
    parser.add_argument(
        "--skip-classifications",
        action="store_true",
        help="Skip per-classification detail reports",
    )
    parser.add_argument(
        "--skip-cves",
        action="store_true",
        help="Skip per-CVE detail reports",
    )
    parser.add_argument(
        "--include-empty",
        action="store_true",
        help="Also write detail reports for classifications/CVEs with zero matches",
    )
    parser.add_argument(
        "--all-catalog-cves",
        action="store_true",
        help="Iterate the full CVE catalog instead of only CVEs seen in the logs",
    )
    args = parser.parse_args()

    aggregated = not args.latest

    requests, traffic, source_files, req_path = load_log_data(
        args.dir, args.requests, args.traffic, aggregated
    )
    requests, traffic = filter_operator_traffic(requests, traffic)

    generate_all_reports(
        requests,
        traffic,
        args.output_dir,
        req_path,
        aggregated,
        source_files,
        skip_summary=args.skip_summary,
        skip_classifications=args.skip_classifications,
        skip_cves=args.skip_cves,
        include_empty=args.include_empty,
        all_catalog_cves=args.all_catalog_cves,
    )


if __name__ == "__main__":
    main()
