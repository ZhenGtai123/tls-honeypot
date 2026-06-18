#!/usr/bin/env python3
"""Parse honeypot request/traffic logs and generate a general traffic report."""

import argparse
import json
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Tuple

from classify_request import CLASSIFICATION_LABELS, classify_request
from log_loader import (
    extract_date_from_filename,
    find_latest_log_pair,
    load_merged_logs,
    load_requests,
    load_traffic,
)


def parse_timestamp(ts: str) -> datetime:
    ts = ts.replace("Z", "+00:00")
    if "." in ts:
        base, rest = ts.split(".", 1)
        frac, tz = rest.split("+", 1) if "+" in rest else (rest, "00:00")
        frac = (frac + "000000")[:6]
        ts = f"{base}.{frac}+{tz}"
    return datetime.fromisoformat(ts)


def percentile(values: List[float], pct: float) -> float:
    if not values:
        return 0
    sorted_vals = sorted(values)
    idx = int(len(sorted_vals) * pct / 100)
    idx = min(idx, len(sorted_vals) - 1)
    return sorted_vals[idx]


def build_traffic_report(
    requests: List[dict],
    traffic: List[dict],
    source_files: Optional[List[dict]] = None,
) -> dict:
    traffic_by_id = {t["request"]["request_id"]: t for t in traffic}

    methods = Counter()
    paths = Counter()
    urls = Counter()
    client_ips = Counter()
    user_agents = Counter()
    hosts = Counter()
    classifications = Counter()
    experiment_groups = Counter()
    protos = Counter()
    content_types = Counter()
    hourly = Counter()
    daily = Counter()
    tls_versions = Counter()
    cipher_suites = Counter()
    destination_ports = Counter()
    forwarded_to = Counter()
    requests_with_body = 0

    status_codes = Counter()
    response_durations = []
    response_body_sizes = []
    truncated_bodies = 0
    status_by_method = defaultdict(Counter)
    status_by_classification = defaultdict(Counter)

    timestamps = []
    responded_ids = set()

    for req in requests:
        rid = req["request_id"]
        cls = classify_request(req)
        method = req.get("method", "")
        path = req.get("path", req.get("url", ""))

        methods[method] += 1
        paths[path] += 1
        urls[req.get("url", "")] += 1
        client_ips[req.get("client_ip", "")] += 1
        user_agents[req.get("user_agent", "")] += 1
        hosts[req.get("host", "")] += 1
        classifications[cls] += 1
        experiment_groups[req.get("experiment_group", "")] += 1
        protos[req.get("proto", "")] += 1
        destination_ports[req.get("destination_port", "")] += 1
        forwarded_to[req.get("forwarded_to", "")] += 1

        ct = req.get("headers", {}).get("Content-Type", req.get("headers", {}).get("content-type", ""))
        if ct:
            content_types[ct.split(";")[0].strip()] += 1

        if req.get("body"):
            requests_with_body += 1

        tls = req.get("tls", {})
        if tls.get("version"):
            tls_versions[tls["version"]] += 1
        if tls.get("cipher_suite"):
            cipher_suites[tls["cipher_suite"]] += 1

        ts = parse_timestamp(req["timestamp"])
        timestamps.append(ts)
        hourly[ts.strftime("%H:00 UTC")] += 1
        daily[ts.strftime("%Y-%m-%d")] += 1

        if rid in traffic_by_id:
            responded_ids.add(rid)

    for t in traffic:
        req = t["request"]
        resp = t["response"]
        method = req.get("method", "")
        cls = classify_request(req)
        code = resp.get("status_code")

        status_codes[code] += 1
        status_by_method[method][code] += 1
        status_by_classification[cls][code] += 1

        if resp.get("duration_ms") is not None:
            response_durations.append(resp["duration_ms"])
        if resp.get("body"):
            response_body_sizes.append(len(resp["body"]))
        if resp.get("body_truncated"):
            truncated_bodies += 1

    timestamps.sort()
    time_range = {
        "start": timestamps[0].isoformat() if timestamps else None,
        "end": timestamps[-1].isoformat() if timestamps else None,
        "duration_hours": round((timestamps[-1] - timestamps[0]).total_seconds() / 3600, 1)
        if len(timestamps) >= 2
        else 0,
    }

    return {
        "summary": {
            "total_requests": len(requests),
            "total_responses": len(traffic),
            "requests_without_response": len(requests) - len(responded_ids),
            "response_rate_pct": round(100 * len(responded_ids) / len(requests), 1) if requests else 0,
            "unique_client_ips": len(client_ips),
            "unique_paths": len(paths),
            "unique_hosts": len(hosts),
            "unique_user_agents": len(user_agents),
            "requests_with_body": requests_with_body,
            "time_range": time_range,
            "source_files": source_files or [],
            "days_covered": len(daily),
        },
        "classifications": {
            cls: {
                "label": CLASSIFICATION_LABELS.get(cls, cls),
                "count": count,
                "pct": round(100 * count / len(requests), 1) if requests else 0,
            }
            for cls, count in classifications.most_common()
        },
        "experiment_groups": dict(experiment_groups.most_common()),
        "http_methods": dict(methods.most_common()),
        "protocols": dict(protos.most_common()),
        "status_codes": dict(status_codes.most_common()),
        "status_by_method": {m: dict(c.most_common()) for m, c in status_by_method.items()},
        "status_by_classification": {c: dict(s.most_common()) for c, s in status_by_classification.items()},
        "top_paths": [{"path": p, "count": c} for p, c in paths.most_common(30)],
        "top_urls": [{"url": u, "count": c} for u, c in urls.most_common(20)],
        "top_client_ips": [{"ip": ip, "count": c} for ip, c in client_ips.most_common(20)],
        "top_user_agents": [{"user_agent": ua, "count": c} for ua, c in user_agents.most_common(15)],
        "top_hosts": [{"host": h, "count": c} for h, c in hosts.most_common(15)],
        "content_types": dict(content_types.most_common(15)),
        "tls_versions": dict(tls_versions.most_common()),
        "cipher_suites": dict(cipher_suites.most_common(10)),
        "destination_ports": dict(destination_ports.most_common()),
        "forwarded_to": dict(forwarded_to.most_common()),
        "hourly_activity": dict(sorted(hourly.items())),
        "daily_activity": dict(sorted(daily.items())),
        "response_stats": {
            "count": len(response_durations),
            "avg_duration_ms": round(sum(response_durations) / len(response_durations), 1)
            if response_durations
            else 0,
            "min_duration_ms": min(response_durations) if response_durations else 0,
            "max_duration_ms": max(response_durations) if response_durations else 0,
            "p50_duration_ms": round(percentile(response_durations, 50), 1),
            "p95_duration_ms": round(percentile(response_durations, 95), 1),
            "avg_body_size": round(sum(response_body_sizes) / len(response_body_sizes))
            if response_body_sizes
            else 0,
            "max_body_size": max(response_body_sizes) if response_body_sizes else 0,
            "truncated_bodies": truncated_bodies,
        },
    }


def format_traffic_report(report: dict) -> str:
    lines = []
    s = report["summary"]
    tr = s["time_range"]
    rs = report["response_stats"]

    lines.append("=" * 72)
    lines.append("TRAFFIC REPORT")
    lines.append("=" * 72)
    lines.append("")
    lines.append("OVERVIEW")
    lines.append("-" * 40)
    lines.append(f"  Period:                  {tr['start']} → {tr['end']}")
    lines.append(f"  Duration:                {tr['duration_hours']} hours")
    lines.append(f"  Total requests:          {s['total_requests']:,}")
    lines.append(f"  Requests with response:  {s['total_responses']:,} ({s['response_rate_pct']}%)")
    lines.append(f"  Requests without response: {s['requests_without_response']:,}")
    lines.append(f"  Requests with body:      {s['requests_with_body']:,}")
    lines.append(f"  Unique client IPs:       {s['unique_client_ips']:,}")
    lines.append(f"  Unique paths:            {s['unique_paths']:,}")
    lines.append(f"  Unique hosts:            {s['unique_hosts']:,}")
    lines.append(f"  Unique user-agents:      {s['unique_user_agents']:,}")
    if s.get("days_covered", 1) > 1:
        lines.append(f"  Days covered:            {s['days_covered']}")
    lines.append("")

    if s.get("source_files"):
        lines.append("SOURCE FILES")
        lines.append("-" * 40)
        for src in s["source_files"]:
            lines.append(
                f"  {src['date']}  {src['request_count']:5,} requests  "
                f"{src['traffic_count']:5,} responses  ({src['requests_file']})"
            )
        lines.append("")

    if report["experiment_groups"]:
        lines.append("EXPERIMENT GROUPS")
        lines.append("-" * 40)
        for group, count in report["experiment_groups"].items():
            lines.append(f"  {group:20s}  {count:5,}")
        lines.append("")

    lines.append("REQUEST CLASSIFICATIONS")
    lines.append("-" * 40)
    for cls, info in report["classifications"].items():
        lines.append(f"  {info['count']:5,} ({info['pct']:5.1f}%)  {info['label']}")
    lines.append("")

    lines.append("HTTP METHODS")
    lines.append("-" * 40)
    for method, count in report["http_methods"].items():
        lines.append(f"  {method:12s}  {count:5,}")
    lines.append("")

    if report["protocols"]:
        lines.append("PROTOCOLS")
        lines.append("-" * 40)
        for proto, count in report["protocols"].items():
            lines.append(f"  {proto:12s}  {count:5,}")
        lines.append("")

    lines.append("RESPONSE STATUS CODES")
    lines.append("-" * 40)
    for code, count in report["status_codes"].items():
        lines.append(f"  {code}  {count:5,}")
    lines.append("")

    lines.append("STATUS BY HTTP METHOD")
    lines.append("-" * 40)
    for method, codes in sorted(report["status_by_method"].items()):
        code_str = ", ".join(f"{c}({n})" for c, n in codes.items())
        lines.append(f"  {method:12s}  {code_str}")
    lines.append("")

    lines.append("TOP TARGETED PATHS")
    lines.append("-" * 40)
    for item in report["top_paths"][:25]:
        lines.append(f"  {item['count']:5,}  {item['path']}")
    lines.append("")

    lines.append("TOP HOSTS")
    lines.append("-" * 40)
    for item in report["top_hosts"][:15]:
        lines.append(f"  {item['count']:5,}  {item['host']}")
    lines.append("")

    lines.append("TOP CLIENT IPs")
    lines.append("-" * 40)
    for item in report["top_client_ips"][:15]:
        lines.append(f"  {item['ip']:20s}  {item['count']:5,}")
    lines.append("")

    lines.append("TOP USER-AGENTS")
    lines.append("-" * 40)
    for item in report["top_user_agents"][:12]:
        ua = item["user_agent"][:65]
        lines.append(f"  {item['count']:5,}  {ua}")
    lines.append("")

    if report["content_types"]:
        lines.append("REQUEST CONTENT-TYPES")
        lines.append("-" * 40)
        for ct, count in report["content_types"].items():
            lines.append(f"  {count:5,}  {ct}")
        lines.append("")

    if report["tls_versions"]:
        lines.append("TLS VERSIONS")
        lines.append("-" * 40)
        for version, count in report["tls_versions"].items():
            lines.append(f"  {version:20s}  {count:5,}")
        lines.append("")

    if report["cipher_suites"]:
        lines.append("TOP TLS CIPHER SUITES")
        lines.append("-" * 40)
        for cipher, count in report["cipher_suites"].items():
            lines.append(f"  {count:5,}  {cipher}")
        lines.append("")

    if report["destination_ports"]:
        lines.append("DESTINATION PORTS")
        lines.append("-" * 40)
        for port, count in report["destination_ports"].items():
            lines.append(f"  {port:12s}  {count:5,}")
        lines.append("")

    if report.get("daily_activity") and s.get("days_covered", 1) > 1:
        lines.append("DAILY ACTIVITY")
        lines.append("-" * 40)
        max_d = max(report["daily_activity"].values())
        for day, count in report["daily_activity"].items():
            bar = "█" * max(1, int(30 * count / max_d))
            lines.append(f"  {day}  {count:5,}  {bar}")
        lines.append("")

    lines.append("HOURLY ACTIVITY (UTC" + (", aggregated)" if s.get("days_covered", 1) > 1 else ")"))
    lines.append("-" * 40)
    max_h = max(report["hourly_activity"].values()) if report["hourly_activity"] else 1
    for hour, count in report["hourly_activity"].items():
        bar = "█" * max(1, int(30 * count / max_h))
        lines.append(f"  {hour}  {count:5,}  {bar}")
    lines.append("")

    lines.append("RESPONSE TIMING & SIZE")
    lines.append("-" * 40)
    lines.append(f"  Responses measured:  {rs['count']:,}")
    lines.append(f"  Average duration:    {rs['avg_duration_ms']} ms")
    lines.append(f"  Median (p50):        {rs['p50_duration_ms']} ms")
    lines.append(f"  p95 duration:        {rs['p95_duration_ms']} ms")
    lines.append(f"  Min / Max duration:  {rs['min_duration_ms']} / {rs['max_duration_ms']} ms")
    lines.append(f"  Average body size:   {rs['avg_body_size']:,} bytes")
    lines.append(f"  Max body size:       {rs['max_body_size']:,} bytes")
    lines.append(f"  Truncated bodies:    {rs['truncated_bodies']:,}")
    lines.append("")
    lines.append("=" * 72)

    return "\n".join(lines)


def find_log_files(directory: Path) -> Tuple[Optional[Path], Optional[Path]]:
    return find_latest_log_pair(directory)


def default_report_paths(output_dir: Path, requests_path: Optional[Path], aggregated: bool) -> Tuple[Path, Path]:
    if aggregated:
        return output_dir / "traffic-report-all.txt", output_dir / "traffic-report-all.json"
    date = extract_date_from_filename(requests_path, "requests") if requests_path else None
    suffix = f"-{date}" if date else ""
    return (
        output_dir / f"traffic-report{suffix}.txt",
        output_dir / f"traffic-report{suffix}.json",
    )


def write_outputs(text: str, data: dict, text_path: Path, json_path: Path, print_to_console: bool) -> None:
    text_path.write_text(text)
    json_path.write_text(json.dumps(data, indent=2))
    if print_to_console:
        print(text)
    else:
        print(f"Text report written to {text_path}")
        print(f"JSON report written to {json_path}")


def main():
    parser = argparse.ArgumentParser(description="Generate a general traffic report from honeypot logs.")
    parser.add_argument("--requests", type=Path, help="Path to requests JSONL file")
    parser.add_argument("--traffic", type=Path, help="Path to traffic JSONL file")
    parser.add_argument("--dir", type=Path, default=Path("."), help="Directory to search for log files")
    parser.add_argument("--output-json", type=Path, help="JSON output path (default: traffic-report-<date>.json)")
    parser.add_argument("--output-text", type=Path, help="Text output path (default: traffic-report-<date>.txt)")
    parser.add_argument("--output-dir", type=Path, default=Path("."), help="Directory for default output files")
    parser.add_argument("--all", action="store_true", help="Aggregate all log files into one report")
    parser.add_argument("--print", action="store_true", help="Print report to stdout instead of writing files")
    args = parser.parse_args()

    req_path = args.requests
    traf_path = args.traffic
    source_files = None
    aggregated = args.all

    if aggregated:
        if args.requests or args.traffic:
            print("Error: --all cannot be combined with --requests or --traffic.", file=sys.stderr)
            sys.exit(1)
        requests, traffic, source_files = load_merged_logs(args.dir)
        if not requests:
            print("Error: no log file pairs found in directory.", file=sys.stderr)
            sys.exit(1)
        req_path = None
    else:
        if not req_path or not traf_path:
            auto_req, auto_traf = find_log_files(args.dir)
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

    report = build_traffic_report(requests, traffic, source_files)
    text = format_traffic_report(report)

    default_text, default_json = default_report_paths(args.output_dir, req_path, aggregated)
    text_path = args.output_text or default_text
    json_path = args.output_json or default_json

    if args.print:
        print(text)
        if args.output_json:
            json_path.write_text(json.dumps(report, indent=2))
            print(f"JSON report written to {json_path}", file=sys.stderr)
    else:
        write_outputs(text, report, text_path, json_path, print_to_console=False)


if __name__ == "__main__":
    main()
