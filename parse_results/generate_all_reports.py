#!/usr/bin/env python3
"""Generate the full honeypot report set in one run.

Produces attack summary, per-classification detail, per-CVE detail, extended
analysis (outcomes, concern events, campaigns), optional config comparison,
and a report manifest listing every generated file.
"""

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import List, Optional, Tuple

from analyze_campaigns import build_campaign_analysis, format_campaign_report
from analyze_outcomes import (
    build_concern_detail,
    build_outcome_analysis,
    format_concern_report,
    format_outcome_report,
)
from classify_request import CLASSIFICATION_LABELS, classify_request
from compare_configs import build_config_comparison, format_comparison_report
from log_loader import (
    extract_date_from_filename,
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

EPILOG = """
Output files (aggregated run, suffix -all):
  attack-report-all.txt/json          Main attack summary
  detail-<classification>-all.txt/json Per-classification event detail
  cve-<CVE_ID>-all.txt/json           Per-CVE event detail
  analysis-outcomes-all.txt/json      Outcome scoring (blocked/decoy/concern)
  analysis-concerns-all.txt/json      Full detail for concern events only
  analysis-campaigns-all.txt/json     IP campaigns and attack sequences
  compare-<A>-vs-<B>.txt/json         Config comparison (with --compare-with)
  report-manifest.json                Index of all generated files

Examples:
  python3 generate_all_reports.py --dir logs/vuln --output-dir reports/vuln
  python3 generate_all_reports.py --dir logs/vuln --output-dir reports/vuln \\
    --compare-with logs/hardened
  python3 generate_all_reports.py --dir logs/vuln --output-dir reports/vuln \\
    --skip-classifications --skip-cves
"""


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
                "Error: --latest cannot be combined with --requests or --traffic.",
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


def report_suffix(req_path: Optional[Path], aggregated: bool) -> str:
    """Return filename suffix (-all or -YYYY-MM-DD)."""
    if aggregated:
        return "-all"
    if req_path:
        date = extract_date_from_filename(req_path, "requests")
        if date:
            return f"-{date}"
    return ""


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
    log_dir: Optional[Path] = None,
    *,
    skip_summary: bool = False,
    skip_classifications: bool = False,
    skip_cves: bool = False,
    skip_extended: bool = False,
    include_empty: bool = False,
    all_catalog_cves: bool = False,
    compare_with: Optional[Path] = None,
    compare_baseline_label: Optional[str] = None,
    compare_label: Optional[str] = None,
) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated = {
        "summary": None,
        "classifications": [],
        "cves": [],
        "extended": {},
        "comparison": None,
        "skipped": {"classifications": [], "cves": []},
    }

    summary = build_report(requests, traffic, source_files)
    classification_counts, cve_counts = discover_report_targets(requests)
    suffix = report_suffix(req_path, aggregated)

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

    outcome_summary = None
    concern_summary = None
    campaign_summary = None

    if not skip_extended:
        outcome = build_outcome_analysis(requests, traffic)
        outcome_summary = outcome["summary"]
        outcome_text = output_dir / f"analysis-outcomes{suffix}.txt"
        outcome_json = output_dir / f"analysis-outcomes{suffix}.json"
        write_report(format_outcome_report(outcome), outcome, outcome_text, outcome_json)
        generated["extended"]["outcomes"] = {
            "text": str(outcome_text),
            "json": str(outcome_json),
        }
        print(f"Outcome analysis: {outcome_text}")

        concern = build_concern_detail(requests, traffic)
        concern_summary = concern["summary"]
        concern_text = output_dir / f"analysis-concerns{suffix}.txt"
        concern_json = output_dir / f"analysis-concerns{suffix}.json"
        write_report(format_concern_report(concern), concern, concern_text, concern_json)
        generated["extended"]["concerns"] = {
            "text": str(concern_text),
            "json": str(concern_json),
            "count": concern_summary["total_events"],
        }
        print(
            f"Concern events ({concern_summary['total_events']:,}): {concern_text}"
        )

        campaigns = build_campaign_analysis(requests)
        campaign_summary = campaigns["summary"]
        campaign_text = output_dir / f"analysis-campaigns{suffix}.txt"
        campaign_json = output_dir / f"analysis-campaigns{suffix}.json"
        write_report(format_campaign_report(campaigns), campaigns, campaign_text, campaign_json)
        generated["extended"]["campaigns"] = {
            "text": str(campaign_text),
            "json": str(campaign_json),
        }
        print(f"Campaign analysis: {campaign_text}")

    if compare_with and compare_with.exists() and log_dir:
        comparison = build_config_comparison(
            compare_with,
            log_dir,
            baseline_label=compare_baseline_label or compare_with.name,
            comparison_label=compare_label or log_dir.name,
        )
        cmp_name = (
            f"compare-{comparison['baseline']['label']}-vs-"
            f"{comparison['comparison']['label']}"
        )
        cmp_text = output_dir / f"{cmp_name}.txt"
        cmp_json = output_dir / f"{cmp_name}.json"
        write_report(format_comparison_report(comparison), comparison, cmp_text, cmp_json)
        generated["comparison"] = {"text": str(cmp_text), "json": str(cmp_json)}
        print(f"Config comparison: {cmp_text}")
    elif compare_with and not compare_with.exists():
        print(f"Warning: --compare-with path not found: {compare_with}", file=sys.stderr)

    manifest_path = output_dir / "report-manifest.json"
    manifest = {
        "output_dir": str(output_dir),
        "log_dir": str(log_dir) if log_dir else None,
        "aggregated": aggregated,
        "total_requests": len(requests),
        "classification_counts": dict(classification_counts.most_common()),
        "cve_counts": dict(cve_counts.most_common()),
        "outcome_summary": outcome_summary,
        "concern_summary": concern_summary,
        "campaign_summary": campaign_summary,
        "generated": generated,
    }
    manifest_path.write_text(json.dumps(manifest, indent=2))
    print(f"Manifest: {manifest_path}")

    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Generate the full honeypot report set: attack summary, classification "
            "and CVE detail reports, extended analysis, and optional config comparison."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=EPILOG,
    )
    parser.add_argument(
        "--dir",
        type=Path,
        default=Path("."),
        help="Directory containing requests-*.jsonl and traffic-*.jsonl (default: .)",
    )
    parser.add_argument(
        "--requests",
        type=Path,
        help="Path to a specific requests JSONL file (implies --latest)",
    )
    parser.add_argument(
        "--traffic",
        type=Path,
        help="Path to a specific traffic JSONL file (implies --latest)",
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
        help="Use only the latest log pair instead of aggregating all days (default: aggregate all)",
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
        "--skip-extended",
        action="store_true",
        help="Skip extended analysis (outcomes, concerns, campaigns)",
    )
    parser.add_argument(
        "--include-empty",
        action="store_true",
        help="Also write detail reports for classifications/CVEs with zero matches",
    )
    parser.add_argument(
        "--all-catalog-cves",
        action="store_true",
        help="Write CVE detail reports for the full catalog, not just matches in logs",
    )
    parser.add_argument(
        "--compare-with",
        type=Path,
        metavar="LOG_DIR",
        help="Compare --dir logs against another config (e.g. logs/hardened)",
    )
    parser.add_argument(
        "--compare-baseline-label",
        help="Display label for the --compare-with (baseline) config",
    )
    parser.add_argument(
        "--compare-label",
        help="Display label for the --dir (comparison) config",
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
        log_dir=args.dir,
        skip_summary=args.skip_summary,
        skip_classifications=args.skip_classifications,
        skip_cves=args.skip_cves,
        skip_extended=args.skip_extended,
        include_empty=args.include_empty,
        all_catalog_cves=args.all_catalog_cves,
        compare_with=args.compare_with,
        compare_baseline_label=args.compare_baseline_label,
        compare_label=args.compare_label,
    )


if __name__ == "__main__":
    main()
