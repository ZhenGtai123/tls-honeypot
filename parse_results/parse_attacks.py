#!/usr/bin/env python3
"""Parse honeypot request/traffic logs and generate a cybersecurity attack report."""

import argparse
import json
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Tuple

from classify_request import (
    CLASSIFICATION_DESCRIPTIONS,
    CLASSIFICATION_LABELS,
    SEVERITY,
    classify_request,
    resolve_classification,
)
from log_loader import (
    extract_date_from_filename,
    find_all_log_pairs,
    find_latest_log_pair,
    load_merged_logs,
    load_requests,
    load_traffic,
)


def parse_timestamp(ts: str) -> datetime:
    """Parse ISO timestamps with optional nanosecond precision."""
    ts = ts.replace("Z", "+00:00")
    if "." in ts:
        base, rest = ts.split(".", 1)
        frac, tz = rest.split("+", 1) if "+" in rest else (rest, "00:00")
        frac = (frac + "000000")[:6]
        ts = f"{base}.{frac}+{tz}"
    return datetime.fromisoformat(ts)


def build_report(
    requests: List[dict],
    traffic: List[dict],
    source_files: Optional[List[dict]] = None,
) -> dict:
    traffic_by_id = {t["request"]["request_id"]: t for t in traffic}

    classifications = Counter()
    methods = Counter()
    paths = Counter()
    client_ips = Counter()
    user_agents = Counter()
    hourly = Counter()
    daily = Counter()
    hosts = Counter()
    severity_counts = Counter()

    attack_details = defaultdict(list)
    ip_classifications = defaultdict(Counter)
    successful_attacks = []

    timestamps = []

    for req in requests:
        rid = req["request_id"]
        cls = classify_request(req)
        log_cls = req.get("classification", "unknown")
        ip = req.get("client_ip", "unknown")
        path = req.get("path", req.get("url", ""))
        method = req.get("method", "")
        ua = req.get("user_agent", "")

        classifications[cls] += 1
        methods[method] += 1
        paths[path] += 1
        client_ips[ip] += 1
        user_agents[ua] += 1
        hosts[req.get("host", "")] += 1
        severity_counts[SEVERITY.get(cls, "LOW")] += 1
        ip_classifications[ip][cls] += 1

        ts = parse_timestamp(req["timestamp"])
        timestamps.append(ts)
        hourly[ts.strftime("%H:00 UTC")] += 1
        daily[ts.strftime("%Y-%m-%d")] += 1

        entry = {
            "request_id": rid,
            "timestamp": req["timestamp"],
            "client_ip": ip,
            "method": method,
            "path": path,
            "classification": cls,
            "log_classification": log_cls,
            "severity": SEVERITY.get(cls, "LOW"),
            "user_agent": ua,
        }

        if rid in traffic_by_id:
            resp = traffic_by_id[rid]["response"]
            entry["status_code"] = resp.get("status_code")
            entry["duration_ms"] = resp.get("duration_ms")
            if resp.get("status_code") == 200 and cls not in ("reconnaissance", "unknown"):
                successful_attacks.append(entry)
        else:
            entry["status_code"] = None

        if cls not in ("reconnaissance", "unknown"):
            attack_details[cls].append(entry)

    status_by_class = defaultdict(Counter)
    response_times = []
    status_codes = Counter()
    for t in traffic:
        req = t["request"]
        resp = t["response"]
        cls = classify_request(req)
        status_by_class[cls][resp.get("status_code")] += 1
        status_codes[resp.get("status_code")] += 1
        if resp.get("duration_ms") is not None:
            response_times.append(resp["duration_ms"])

    timestamps.sort()
    time_range = {
        "start": timestamps[0].isoformat() if timestamps else None,
        "end": timestamps[-1].isoformat() if timestamps else None,
        "duration_hours": round((timestamps[-1] - timestamps[0]).total_seconds() / 3600, 1)
        if len(timestamps) >= 2
        else 0,
    }

    top_attackers = []
    for ip, count in client_ips.most_common(20):
        top_attackers.append(
            {
                "ip": ip,
                "total_requests": count,
                "classifications": dict(ip_classifications[ip].most_common()),
                "primary_activity": ip_classifications[ip].most_common(1)[0][0]
                if ip_classifications[ip]
                else "unknown",
            }
        )

    return {
        "summary": {
            "total_requests": len(requests),
            "total_with_response": len(traffic),
            "requests_without_response": len(requests) - len(traffic),
            "unique_client_ips": len(client_ips),
            "unique_paths": len(paths),
            "time_range": time_range,
            "severity_breakdown": dict(severity_counts),
            "source_files": source_files or [],
            "days_covered": len(daily),
        },
        "attack_classifications": {
            cls: {
                "label": CLASSIFICATION_LABELS.get(cls, cls),
                "count": count,
                "severity": SEVERITY.get(cls, "LOW"),
                "pct": round(100 * count / len(requests), 1) if requests else 0,
            }
            for cls, count in classifications.most_common()
        },
        "http_methods": dict(methods.most_common()),
        "status_codes": dict(status_codes.most_common()),
        "status_by_classification": {
            cls: dict(codes.most_common()) for cls, codes in status_by_class.items()
        },
        "top_targeted_paths": [{"path": p, "count": c} for p, c in paths.most_common(30)],
        "top_user_agents": [{"user_agent": ua, "count": c} for ua, c in user_agents.most_common(15)],
        "top_attackers": top_attackers,
        "hourly_activity": dict(sorted(hourly.items())),
        "daily_activity": dict(sorted(daily.items())),
        "targeted_hosts": dict(hosts.most_common(10)),
        "successful_exploitation_probes": successful_attacks[:50],
        "attack_samples": {
            cls: sorted(entries, key=lambda e: e["timestamp"])[:10]
            for cls, entries in attack_details.items()
        },
        "response_stats": {
            "avg_duration_ms": round(sum(response_times) / len(response_times), 1)
            if response_times
            else 0,
            "max_duration_ms": max(response_times) if response_times else 0,
        },
    }


def format_text_report(report: dict) -> str:
    lines = []
    s = report["summary"]
    tr = s["time_range"]

    lines.append("=" * 72)
    lines.append("CYBERSECURITY ATTACK REPORT")
    lines.append("=" * 72)
    lines.append("")
    lines.append("OVERVIEW")
    lines.append("-" * 40)
    lines.append(f"  Period:              {tr['start']} → {tr['end']}")
    lines.append(f"  Duration:            {tr['duration_hours']} hours")
    lines.append(f"  Total requests:      {s['total_requests']:,}")
    lines.append(f"  With response:       {s['total_with_response']:,}")
    lines.append(f"  No response logged:  {s['requests_without_response']:,}")
    lines.append(f"  Unique attacker IPs: {s['unique_client_ips']:,}")
    lines.append(f"  Unique paths hit:    {s['unique_paths']:,}")
    if s.get("days_covered", 1) > 1:
        lines.append(f"  Days covered:        {s['days_covered']}")
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

    lines.append("SEVERITY BREAKDOWN")
    lines.append("-" * 40)
    for sev in ("HIGH", "MEDIUM", "LOW"):
        count = s["severity_breakdown"].get(sev, 0)
        bar = "█" * min(count // 50, 40)
        lines.append(f"  {sev:8s}  {count:5,}  {bar}")
    lines.append("")

    lines.append("ATTACK CLASSIFICATIONS")
    lines.append("-" * 40)
    for cls, info in report["attack_classifications"].items():
        label = info["label"]
        lines.append(
            f"  [{info['severity']:6s}] {info['count']:5,} ({info['pct']:5.1f}%)  {label}"
        )
    lines.append("")

    lines.append("HTTP METHODS")
    lines.append("-" * 40)
    for method, count in report["http_methods"].items():
        lines.append(f"  {method:12s}  {count:5,}")
    lines.append("")

    lines.append("RESPONSE STATUS CODES")
    lines.append("-" * 40)
    for code, count in report["status_codes"].items():
        meaning = {
            200: "OK (content served)",
            404: "Not Found",
            429: "Rate Limited",
            400: "Bad Request (blocked?)",
            403: "Forbidden",
            502: "Bad Gateway",
        }.get(code, "")
        lines.append(f"  {code}  {count:5,}  {meaning}")
    lines.append("")

    lines.append("TOP TARGETED PATHS")
    lines.append("-" * 40)
    for item in report["top_targeted_paths"][:20]:
        lines.append(f"  {item['count']:5,}  {item['path']}")
    lines.append("")

    lines.append("TOP ATTACKER IPs")
    lines.append("-" * 40)
    for atk in report["top_attackers"][:15]:
        classes = ", ".join(f"{k}({v})" for k, v in list(atk["classifications"].items())[:3])
        lines.append(f"  {atk['ip']:20s}  {atk['total_requests']:5,}  [{classes}]")
    lines.append("")

    lines.append("SCANNER / BOT USER-AGENTS")
    lines.append("-" * 40)
    for item in report["top_user_agents"][:10]:
        ua = item["user_agent"][:65]
        lines.append(f"  {item['count']:5,}  {ua}")
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

    probes = report["successful_exploitation_probes"]
    if probes:
        lines.append("PROBES THAT RECEIVED HTTP 200 (potential exposure)")
        lines.append("-" * 40)
        for p in probes[:20]:
            lines.append(
                f"  {p['timestamp'][:19]}  {p['client_ip']:18s}  "
                f"{p['method']:6s}  {p['path'][:40]:40s}  [{p['classification']}]"
            )
        lines.append("")

    for cls, samples in report["attack_samples"].items():
        if cls in ("reconnaissance", "unknown") or not samples:
            continue
        label = CLASSIFICATION_LABELS.get(cls, cls)
        lines.append(f"SAMPLE: {label.upper()}")
        lines.append("-" * 40)
        for sample in samples[:5]:
            status = sample.get("status_code", "—")
            lines.append(
                f"  {sample['timestamp'][:19]}  {sample['client_ip']:18s}  "
                f"{sample['method']:6s}  {status}  {sample['path'][:45]}"
            )
        lines.append("")

    rs = report["response_stats"]
    lines.append("RESPONSE TIMING")
    lines.append("-" * 40)
    lines.append(f"  Average: {rs['avg_duration_ms']} ms")
    lines.append(f"  Max:     {rs['max_duration_ms']} ms")
    lines.append("")
    lines.append("=" * 72)

    return "\n".join(lines)


def build_classification_detail(
    requests: List[dict], traffic: List[dict], classification: str
) -> dict:
    traffic_by_id = {t["request"]["request_id"]: t for t in traffic}
    matched = [r for r in requests if classify_request(r) == classification]

    paths = Counter()
    methods = Counter()
    client_ips = Counter()
    user_agents = Counter()
    hosts = Counter()
    status_codes = Counter()
    queries = Counter()

    events = []
    for req in sorted(matched, key=lambda r: r["timestamp"]):
        rid = req["request_id"]
        paths[req.get("path", "")] += 1
        methods[req.get("method", "")] += 1
        client_ips[req.get("client_ip", "")] += 1
        user_agents[req.get("user_agent", "")] += 1
        hosts[req.get("host", "")] += 1
        if req.get("query"):
            queries[req["query"]] += 1

        event = {
            "request_id": rid,
            "timestamp": req["timestamp"],
            "client_ip": req.get("client_ip"),
            "method": req.get("method"),
            "host": req.get("host"),
            "url": req.get("url"),
            "path": req.get("path"),
            "query": req.get("query"),
            "proto": req.get("proto"),
            "user_agent": req.get("user_agent"),
            "forwarded_to": req.get("forwarded_to"),
            "experiment_group": req.get("experiment_group"),
            "classification": classify_request(req),
            "log_classification": req.get("classification", "unknown"),
            "headers": req.get("headers", {}),
            "body": req.get("body"),
            "body_encoding": req.get("body_encoding"),
            "tls": req.get("tls", {}),
            "has_response": rid in traffic_by_id,
        }

        if rid in traffic_by_id:
            resp = traffic_by_id[rid]["response"]
            status_codes[resp.get("status_code")] += 1
            event["response"] = {
                "timestamp": resp.get("timestamp"),
                "status_code": resp.get("status_code"),
                "status": resp.get("status"),
                "duration_ms": resp.get("duration_ms"),
                "headers": resp.get("headers", {}),
                "body": resp.get("body"),
                "body_truncated": resp.get("body_truncated"),
                "body_encoding": resp.get("body_encoding"),
            }
        else:
            event["response"] = None

        events.append(event)

    timestamps = [parse_timestamp(r["timestamp"]) for r in matched]
    timestamps.sort()

    return {
        "classification": classification,
        "label": CLASSIFICATION_LABELS.get(classification, classification),
        "description": CLASSIFICATION_DESCRIPTIONS.get(classification, ""),
        "severity": SEVERITY.get(classification, "LOW"),
        "summary": {
            "total_events": len(matched),
            "with_response": sum(1 for e in events if e["has_response"]),
            "without_response": sum(1 for e in events if not e["has_response"]),
            "unique_client_ips": len(client_ips),
            "unique_paths": len(paths),
            "unique_hosts": len(hosts),
            "time_range": {
                "start": timestamps[0].isoformat() if timestamps else None,
                "end": timestamps[-1].isoformat() if timestamps else None,
            },
            "methods": dict(methods.most_common()),
            "status_codes": dict(status_codes.most_common()),
            "top_paths": dict(paths.most_common(10)),
            "top_client_ips": dict(client_ips.most_common(10)),
            "top_user_agents": dict(user_agents.most_common(5)),
            "top_hosts": dict(hosts.most_common(10)),
            "top_queries": dict(queries.most_common(10)),
        },
        "events": events,
    }


def _format_body(body: Optional[str], max_len: int = 800) -> List[str]:
    if not body:
        return ["    (empty)"]
    lines = body.splitlines() or [body]
    rendered = []
    total = 0
    for line in lines:
        if total >= max_len:
            rendered.append(f"    ... ({len(body) - total} more chars truncated)")
            break
        remaining = max_len - total
        snippet = line[:remaining]
        rendered.append(f"    {snippet}")
        total += len(snippet) + 1
    return rendered


def format_detail_report(detail: dict) -> str:
    lines = []
    s = detail["summary"]
    tr = s["time_range"]

    lines.append("=" * 72)
    lines.append(f"DETAIL REPORT: {detail['label'].upper()}")
    lines.append("=" * 72)
    lines.append("")
    lines.append(f"Classification:  {detail['classification']}")
    lines.append(f"Severity:        {detail['severity']}")
    if detail["description"]:
        lines.append(f"Description:     {detail['description']}")
    lines.append("")
    lines.append("SUMMARY")
    lines.append("-" * 40)
    lines.append(f"  Total events:        {s['total_events']:,}")
    lines.append(f"  With response:       {s['with_response']:,}")
    lines.append(f"  Without response:    {s['without_response']:,}")
    lines.append(f"  Unique attacker IPs: {s['unique_client_ips']:,}")
    lines.append(f"  Unique paths:        {s['unique_paths']:,}")
    lines.append(f"  Unique hosts:        {s['unique_hosts']:,}")
    if tr["start"]:
        lines.append(f"  First seen:          {tr['start']}")
        lines.append(f"  Last seen:           {tr['end']}")
    lines.append("")

    if s["methods"]:
        lines.append("HTTP METHODS")
        lines.append("-" * 40)
        for method, count in s["methods"].items():
            lines.append(f"  {method:12s}  {count:5,}")
        lines.append("")

    if s["status_codes"]:
        lines.append("RESPONSE STATUS CODES")
        lines.append("-" * 40)
        for code, count in s["status_codes"].items():
            lines.append(f"  {code}  {count:5,}")
        lines.append("")

    if s["top_paths"]:
        lines.append("TOP PATHS")
        lines.append("-" * 40)
        for path, count in s["top_paths"].items():
            lines.append(f"  {count:5,}  {path}")
        lines.append("")

    if s["top_queries"]:
        lines.append("TOP QUERY STRINGS")
        lines.append("-" * 40)
        for query, count in s["top_queries"].items():
            lines.append(f"  {count:5,}  {query}")
        lines.append("")

    if s["top_client_ips"]:
        lines.append("TOP ATTACKER IPs")
        lines.append("-" * 40)
        for ip, count in s["top_client_ips"].items():
            lines.append(f"  {ip:20s}  {count:5,}")
        lines.append("")

    if s["top_user_agents"]:
        lines.append("USER-AGENTS")
        lines.append("-" * 40)
        for ua, count in s["top_user_agents"].items():
            lines.append(f"  {count:5,}  {ua[:65]}")
        lines.append("")

    for i, event in enumerate(detail["events"], 1):
        lines.append("=" * 72)
        lines.append(f"EVENT #{i} of {len(detail['events'])}")
        lines.append("=" * 72)
        lines.append(f"  Request ID:     {event['request_id']}")
        lines.append(f"  Timestamp:      {event['timestamp']}")
        lines.append(f"  Client IP:      {event['client_ip']}")
        lines.append(f"  Method:         {event['method']}")
        lines.append(f"  Host:           {event['host']}")
        lines.append(f"  URL:            {event['url']}")
        lines.append(f"  Path:           {event['path']}")
        if event.get("query"):
            lines.append(f"  Query:          {event['query']}")
        lines.append(f"  User-Agent:     {event['user_agent']}")
        lines.append(f"  Forwarded to:   {event.get('forwarded_to', '')}")
        lines.append(f"  Experiment:     {event.get('experiment_group', '')}")

        if event.get("headers"):
            lines.append("  Request headers:")
            for k, v in event["headers"].items():
                lines.append(f"    {k}: {v}")

        if event.get("body"):
            lines.append(f"  Request body ({len(event['body'])} chars):")
            lines.extend(_format_body(event["body"], max_len=400))

        tls = event.get("tls", {})
        if tls:
            lines.append(f"  TLS version:    {tls.get('version', '')}")
            lines.append(f"  Cipher suite:   {tls.get('cipher_suite', '')}")

        resp = event.get("response")
        if resp:
            lines.append("  Response:")
            lines.append(f"    Status:       {resp.get('status_code')} {resp.get('status', '')}")
            lines.append(f"    Duration:     {resp.get('duration_ms')} ms")
            if resp.get("headers"):
                lines.append("    Headers:")
                for k, v in resp["headers"].items():
                    lines.append(f"      {k}: {v}")
            body = resp.get("body") or ""
            truncated = resp.get("body_truncated")
            suffix = " (truncated in log)" if truncated else ""
            lines.append(f"    Body ({len(body)} chars{suffix}):")
            lines.extend(_format_body(body))
        else:
            lines.append("  Response:       (no traffic record)")
        lines.append("")

    lines.append("=" * 72)
    return "\n".join(lines)


def list_classifications(requests: List[dict]) -> str:
    counts = Counter(classify_request(r) for r in requests)
    lines = ["Available classifications:", ""]
    for cls, count in counts.most_common():
        label = CLASSIFICATION_LABELS.get(cls, cls)
        sev = SEVERITY.get(cls, "LOW")
        lines.append(f"  {cls:30s}  [{sev:6s}]  {count:5,}  {label}")
    lines.append("")
    lines.append("Usage: python3 parse_attacks.py --detail <classification>")
    lines.append("  e.g. python3 parse_attacks.py --detail rce_attempt")
    return "\n".join(lines)


def find_log_files(directory: Path) -> Tuple[Optional[Path], Optional[Path]]:
    return find_latest_log_pair(directory)


def extract_log_date(path: Path) -> Optional[str]:
    return extract_date_from_filename(path, "requests")


def default_report_paths(output_dir: Path, requests_path: Optional[Path], aggregated: bool) -> Tuple[Path, Path]:
    if aggregated:
        return output_dir / "attack-report-all.txt", output_dir / "attack-report-all.json"
    date = extract_log_date(requests_path) if requests_path else None
    suffix = f"-{date}" if date else ""
    return (
        output_dir / f"attack-report{suffix}.txt",
        output_dir / f"attack-report{suffix}.json",
    )


def default_detail_paths(
    output_dir: Path, classification: str, requests_path: Optional[Path], aggregated: bool
) -> Tuple[Path, Path]:
    if aggregated:
        return (
            output_dir / f"detail-{classification}-all.txt",
            output_dir / f"detail-{classification}-all.json",
        )
    date = extract_log_date(requests_path) if requests_path else None
    suffix = f"-{date}" if date else ""
    return (
        output_dir / f"detail-{classification}{suffix}.txt",
        output_dir / f"detail-{classification}{suffix}.json",
    )


def write_outputs(
    text: str,
    data: dict,
    text_path: Path,
    json_path: Path,
    print_to_console: bool,
) -> None:
    text_path.write_text(text)
    json_path.write_text(json.dumps(data, indent=2))
    if print_to_console:
        print(text)
    else:
        print(f"Text report written to {text_path}")
        print(f"JSON report written to {json_path}")


def main():
    parser = argparse.ArgumentParser(description="Generate a cybersecurity attack report from honeypot logs.")
    parser.add_argument(
        "--requests",
        type=Path,
        help="Path to requests JSONL file (default: auto-detect in directory)",
    )
    parser.add_argument(
        "--traffic",
        type=Path,
        help="Path to traffic JSONL file (default: auto-detect in directory)",
    )
    parser.add_argument(
        "--dir",
        type=Path,
        default=Path("."),
        help="Directory to search for log files (default: current directory)",
    )
    parser.add_argument(
        "--output-json",
        type=Path,
        help="Write structured report as JSON to this path (default: attack-report-<date>.json)",
    )
    parser.add_argument(
        "--output-text",
        type=Path,
        help="Write text report to this path (default: attack-report-<date>.txt)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("."),
        help="Directory for default output files (default: current directory)",
    )
    parser.add_argument(
        "--print",
        action="store_true",
        help="Print report to stdout instead of writing to files",
    )
    parser.add_argument(
        "--detail",
        metavar="CLASSIFICATION",
        help="Show full per-event breakdown for a classification (e.g. rce_attempt)",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Aggregate all requests-*.jsonl and traffic-*.jsonl files into one report",
    )
    parser.add_argument(
        "--list-classifications",
        action="store_true",
        help="List available attack classifications and exit",
    )
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
            print("Error: requests file not found. Use --requests or place requests-*.jsonl in --dir.", file=sys.stderr)
            sys.exit(1)
        if not traf_path or not traf_path.exists():
            print("Error: traffic file not found. Use --traffic or place traffic-*.jsonl in --dir.", file=sys.stderr)
            sys.exit(1)

        requests = load_requests(req_path)
        traffic = load_traffic(traf_path)

    if args.list_classifications:
        print(list_classifications(requests))
        return

    if args.detail:
        classification = resolve_classification(args.detail)
        if not classification:
            print(f"Error: unknown classification '{args.detail}'.\n", file=sys.stderr)
            print(list_classifications(requests), file=sys.stderr)
            sys.exit(1)

        detail = build_classification_detail(requests, traffic, classification)
        text = format_detail_report(detail)

        default_text, default_json = default_detail_paths(args.output_dir, classification, req_path, aggregated)
        text_path = args.output_text or default_text
        json_path = args.output_json or default_json

        if args.print:
            print(text)
            if args.output_json:
                json_path.write_text(json.dumps(detail, indent=2))
                print(f"JSON detail written to {json_path}", file=sys.stderr)
        else:
            write_outputs(text, detail, text_path, json_path, print_to_console=False)
        return

    report = build_report(requests, traffic, source_files)
    text = format_text_report(report)

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
