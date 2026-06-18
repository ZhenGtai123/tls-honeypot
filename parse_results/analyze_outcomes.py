"""Outcome-based scoring for honeypot attack requests.

Classifies each attack request by HTTP response status and body content,
distinguishing defensive blocks, honeypot decoys, and potential leaks.
"""

import base64
import gzip
import re
from collections import Counter, defaultdict
from typing import Dict, List, Optional, Tuple

from classify_request import CLASSIFICATION_LABELS, classify_request

from map_cve import identify_cves

OUTCOME_LABELS: Dict[str, str] = {
    "blocked": "Blocked by honeypot (400/403/405)",
    "rate_limited": "Rate limited (429)",
    "not_found": "Not found (404)",
    "redirected": "Redirected (3xx)",
    "decoy_served": "Honeypot decoy content served (200)",
    "content_served": "HTTP 200 with unrecognized body",
    "empty_response": "HTTP 200 with empty body",
    "server_error": "Server or gateway error (5xx)",
    "no_response": "No traffic record",
}

# Attack classes where a 200 decoy still represents attacker intent.
ATTACK_CLASSES = frozenset(
    cls
    for cls in CLASSIFICATION_LABELS
    if cls not in ("reconnaissance", "unknown")
)

_WP_DECOY = re.compile(
    r"(?:WordPress|wp-content|wp-includes|Log In|install\.php|"
    r"Amsterdam Wellness|no-js.*lang=.en-US)",
    re.IGNORECASE,
)
_GZIP_B64 = re.compile(r"^H4sI[A-Za-z0-9+/=]+$")
_ENV_LEAK = re.compile(
    r"(?:^|\n)(?:APP_KEY|DB_PASSWORD|DB_HOST|AWS_SECRET|SECRET_KEY|"
    r"MAIL_PASSWORD|PRIVATE_KEY)\s*=",
    re.IGNORECASE | re.MULTILINE,
)
_GIT_LEAK = re.compile(r"\[core\]|repositoryformatversion|ref:\s*refs/", re.IGNORECASE)
_ACTUATOR_LEAK = re.compile(
    r'"propertySources"|"systemProperties"|"spring\.profiles"',
    re.IGNORECASE,
)
_DOCKER_LEAK = re.compile(r'"(?:Id|HostConfig|Image)"\s*:', re.IGNORECASE)
_JSONRPC = re.compile(r'"(?:jsonrpc|method)"\s*:\s*"', re.IGNORECASE)
_SENSITIVE_PATH = re.compile(
    r"(?:^|/)\.env|\.git/|wp-config\.php|/actuator/|/containers/json|"
    r"eval-stdin\.php|/\.htpasswd",
    re.IGNORECASE,
)


def _decode_body(body: str, encoding: Optional[str] = None) -> str:
    """Return inspectable text from a response body (handles gzip-as-base64)."""
    if not body:
        return ""
    text = body
    if _GZIP_B64.match(body.strip()):
        try:
            raw = base64.b64decode(body)
            text = gzip.decompress(raw).decode("utf-8", errors="replace")
        except (OSError, ValueError, EOFError):
            text = body
    return text


def _detect_leak(path: str, body: str, classification: str) -> Optional[str]:
    """Return a leak indicator label if body resembles real secret disclosure."""
    text = _decode_body(body)
    if not text and not body:
        if _SENSITIVE_PATH.search(path):
            return "empty_on_sensitive_path"
        return None

    if _ENV_LEAK.search(text):
        return "env_file_content"
    if _GIT_LEAK.search(text):
        return "git_config_content"
    if _ACTUATOR_LEAK.search(text):
        return "actuator_secrets"
    if _DOCKER_LEAK.search(text) and "containers" in path.lower():
        return "docker_api_response"
    if _JSONRPC.search(text) and classification == "crypto_mining_probe":
        return "mining_rpc_response"
    return None


def _is_decoy(body: str) -> bool:
    if not body:
        return False
    if _GZIP_B64.match(body.strip()):
        return True
    text = _decode_body(body)
    return bool(_WP_DECOY.search(text))


def score_outcome(
    req: dict,
    resp: Optional[dict],
    classification: Optional[str] = None,
) -> dict:
    """Score a single request/response pair."""
    cls = classification if classification is not None else classify_request(req)
    path = req.get("path", req.get("url", ""))

    if resp is None:
        return {
            "outcome": "no_response",
            "outcome_label": OUTCOME_LABELS["no_response"],
            "status_code": None,
            "leak_indicator": None,
            "concern": False,
        }

    status = resp.get("status_code")
    body = resp.get("body") or ""
    leak = None
    concern = False

    if status in (400, 403, 405):
        outcome = "blocked"
    elif status == 429:
        outcome = "rate_limited"
    elif status == 404:
        outcome = "not_found"
    elif status in (301, 302, 307, 308):
        outcome = "redirected"
    elif status and status >= 500:
        outcome = "server_error"
    elif status == 200:
        leak = _detect_leak(path, body, cls)
        if leak:
            outcome = "content_served"
            concern = True
        elif not body:
            outcome = "empty_response"
            concern = bool(_SENSITIVE_PATH.search(path))
        elif _is_decoy(body):
            outcome = "decoy_served"
        else:
            outcome = "content_served"
            concern = cls in ATTACK_CLASSES
    else:
        outcome = "content_served" if status and 200 <= status < 300 else "blocked"

    return {
        "outcome": outcome,
        "outcome_label": OUTCOME_LABELS.get(outcome, outcome),
        "status_code": status,
        "leak_indicator": leak,
        "concern": concern,
    }


def build_outcome_analysis(
    requests: List[dict],
    traffic: List[dict],
) -> dict:
    """Build outcome statistics for all requests and attack-only subset."""
    traffic_by_id = {t["request"]["request_id"]: t for t in traffic}

    overall = Counter()
    attack_outcomes = Counter()
    by_classification: Dict[str, Counter] = defaultdict(Counter)
    concern_events: List[dict] = []
    defensive_by_class: Dict[str, Counter] = defaultdict(Counter)

    defensive_outcomes = frozenset({"blocked", "rate_limited", "not_found", "redirected"})

    for req in requests:
        rid = req["request_id"]
        cls = classify_request(req)
        resp = traffic_by_id[rid]["response"] if rid in traffic_by_id else None
        scored = score_outcome(req, resp, cls)

        overall[scored["outcome"]] += 1
        if cls in ATTACK_CLASSES:
            attack_outcomes[scored["outcome"]] += 1
            by_classification[cls][scored["outcome"]] += 1
            if scored["outcome"] in defensive_outcomes:
                defensive_by_class[cls][scored["outcome"]] += 1

        if scored["concern"]:
            concern_events.append(
                {
                    "request_id": rid,
                    "timestamp": req["timestamp"],
                    "client_ip": req.get("client_ip"),
                    "method": req.get("method"),
                    "path": req.get("path", req.get("url", "")),
                    "classification": cls,
                    "status_code": scored["status_code"],
                    "outcome": scored["outcome"],
                    "leak_indicator": scored["leak_indicator"],
                }
            )

    attack_total = sum(attack_outcomes.values())
    defensive_total = sum(
        attack_outcomes[o] for o in defensive_outcomes if o in attack_outcomes
    )

    return {
        "summary": {
            "total_requests": len(requests),
            "attack_requests": attack_total,
            "defensive_success_count": defensive_total,
            "defensive_success_pct": round(100 * defensive_total / attack_total, 1)
            if attack_total
            else 0,
            "decoy_served_count": attack_outcomes.get("decoy_served", 0),
            "concern_count": len(concern_events),
        },
        "overall_outcomes": dict(overall.most_common()),
        "attack_outcomes": dict(attack_outcomes.most_common()),
        "outcomes_by_classification": {
            cls: dict(counts.most_common()) for cls, counts in by_classification.items()
        },
        "defensive_by_classification": {
            cls: dict(counts.most_common()) for cls, counts in defensive_by_class.items()
        },
        "concern_events": sorted(concern_events, key=lambda e: e["timestamp"]),
    }


def _format_body(body: Optional[str], max_len: int = 800) -> List[str]:
    if not body:
        return ["    (empty)"]
    lines_out = body.splitlines() or [body]
    rendered = []
    total = 0
    for line in lines_out:
        if total >= max_len:
            rendered.append(f"    ... ({len(body) - total} more chars truncated)")
            break
        remaining = max_len - total
        snippet = line[:remaining]
        rendered.append(f"    {snippet}")
        total += len(snippet) + 1
    return rendered


def build_concern_detail(requests: List[dict], traffic: List[dict]) -> dict:
    """Build a full report for every potential concern event."""
    traffic_by_id = {t["request"]["request_id"]: t for t in traffic}

    paths = Counter()
    methods = Counter()
    client_ips = Counter()
    user_agents = Counter()
    hosts = Counter()
    classifications = Counter()
    leak_indicators = Counter()
    status_codes = Counter()

    events = []
    for req in sorted(requests, key=lambda r: r["timestamp"]):
        rid = req["request_id"]
        cls = classify_request(req)
        resp_record = traffic_by_id.get(rid)
        resp = resp_record["response"] if resp_record else None
        scored = score_outcome(req, resp, cls)
        if not scored["concern"]:
            continue

        path = req.get("path", req.get("url", ""))
        paths[path] += 1
        methods[req.get("method", "")] += 1
        client_ips[req.get("client_ip", "")] += 1
        user_agents[req.get("user_agent", "")] += 1
        hosts[req.get("host", "")] += 1
        classifications[cls] += 1
        indicator = scored["leak_indicator"] or "empty_or_unrecognized_body"
        leak_indicators[indicator] += 1
        if resp:
            status_codes[resp.get("status_code")] += 1

        cves = identify_cves(req)
        event = {
            "request_id": rid,
            "timestamp": req["timestamp"],
            "client_ip": req.get("client_ip"),
            "method": req.get("method"),
            "host": req.get("host"),
            "url": req.get("url"),
            "path": path,
            "query": req.get("query"),
            "user_agent": req.get("user_agent"),
            "classification": cls,
            "outcome": scored["outcome"],
            "outcome_label": scored["outcome_label"],
            "leak_indicator": scored["leak_indicator"],
            "concern_reason": indicator,
            "cves": cves,
            "primary_cve": cves[0] if cves else None,
            "headers": req.get("headers", {}),
            "body": req.get("body"),
            "has_response": resp_record is not None,
        }

        if resp_record:
            resp = resp_record["response"]
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

    timestamps = [e["timestamp"] for e in events]

    return {
        "summary": {
            "total_events": len(events),
            "unique_client_ips": len(client_ips),
            "unique_paths": len(paths),
            "unique_hosts": len(hosts),
            "time_range": {
                "start": timestamps[0] if timestamps else None,
                "end": timestamps[-1] if timestamps else None,
            },
            "classifications": dict(classifications.most_common()),
            "leak_indicators": dict(leak_indicators.most_common()),
            "methods": dict(methods.most_common()),
            "status_codes": dict(status_codes.most_common()),
            "top_paths": dict(paths.most_common(15)),
            "top_client_ips": dict(client_ips.most_common(15)),
            "top_user_agents": dict(user_agents.most_common(5)),
        },
        "events": events,
    }


def format_concern_report(detail: dict) -> str:
    lines = []
    s = detail["summary"]
    tr = s["time_range"]

    lines.append("=" * 72)
    lines.append("POTENTIAL CONCERN EVENTS")
    lines.append("=" * 72)
    lines.append("")
    lines.append(
        "Requests flagged by outcome scoring: empty HTTP 200 on a sensitive path, "
        "or response body matching leak patterns (.env, .git, actuator, etc.)."
    )
    lines.append("")
    lines.append("SUMMARY")
    lines.append("-" * 40)
    lines.append(f"  Total events:        {s['total_events']:,}")
    lines.append(f"  Unique attacker IPs: {s['unique_client_ips']:,}")
    lines.append(f"  Unique paths:        {s['unique_paths']:,}")
    lines.append(f"  Unique hosts:        {s['unique_hosts']:,}")
    if tr["start"]:
        lines.append(f"  First seen:          {tr['start']}")
        lines.append(f"  Last seen:           {tr['end']}")
    lines.append("")

    if s["leak_indicators"]:
        lines.append("CONCERN REASONS")
        lines.append("-" * 40)
        for reason, count in s["leak_indicators"].items():
            lines.append(f"  {count:5,}  {reason}")
        lines.append("")

    if s["classifications"]:
        lines.append("ATTACK CLASSIFICATIONS")
        lines.append("-" * 40)
        for cls, count in s["classifications"].items():
            label = CLASSIFICATION_LABELS.get(cls, cls)
            lines.append(f"  {count:5,}  {cls}  ({label})")
        lines.append("")

    if s["top_paths"]:
        lines.append("TOP PATHS")
        lines.append("-" * 40)
        for path, count in s["top_paths"].items():
            lines.append(f"  {count:5,}  {path}")
        lines.append("")

    if s["top_client_ips"]:
        lines.append("TOP ATTACKER IPs")
        lines.append("-" * 40)
        for ip, count in s["top_client_ips"].items():
            lines.append(f"  {ip:20s}  {count:5,}")
        lines.append("")

    for i, event in enumerate(detail["events"], 1):
        lines.append("=" * 72)
        lines.append(f"EVENT #{i} of {len(detail['events'])}")
        lines.append("=" * 72)
        lines.append(f"  Request ID:      {event['request_id']}")
        lines.append(f"  Timestamp:       {event['timestamp']}")
        lines.append(f"  Client IP:       {event['client_ip']}")
        lines.append(f"  Method:          {event['method']}")
        lines.append(f"  Host:            {event['host']}")
        lines.append(f"  Path:            {event['path']}")
        if event.get("query"):
            lines.append(f"  Query:           {event['query']}")
        lines.append(f"  Classification:  {event['classification']}")
        lines.append(f"  Concern reason:  {event['concern_reason']}")
        lines.append(f"  Outcome:         {event['outcome']} ({event['outcome_label']})")
        if event.get("primary_cve"):
            pc = event["primary_cve"]
            lines.append(
                f"  Likely CVE:      {pc['cve_id']} — {pc['name']} ({pc['confidence']})"
            )

        if event.get("headers"):
            lines.append("  Request headers:")
            for k, v in event["headers"].items():
                lines.append(f"    {k}: {v}")

        if event.get("body"):
            lines.append(f"  Request body ({len(event['body'])} chars):")
            lines.extend(_format_body(event["body"], max_len=400))

        resp = event.get("response")
        if resp:
            lines.append("  Response:")
            lines.append(f"    Status:        {resp.get('status_code')} {resp.get('status', '')}")
            lines.append(f"    Duration:      {resp.get('duration_ms')} ms")
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
            lines.append("  Response:        (no traffic record)")
        lines.append("")

    lines.append("=" * 72)
    return "\n".join(lines)


def format_outcome_report(analysis: dict) -> str:
    lines = []
    s = analysis["summary"]

    lines.append("=" * 72)
    lines.append("OUTCOME ANALYSIS")
    lines.append("=" * 72)
    lines.append("")
    lines.append("SUMMARY")
    lines.append("-" * 40)
    lines.append(f"  Total requests:           {s['total_requests']:,}")
    lines.append(f"  Attack-class requests:    {s['attack_requests']:,}")
    lines.append(
        f"  Defensive outcome:        {s['defensive_success_count']:,} "
        f"({s['defensive_success_pct']}% of attacks blocked/404/429/redirect)"
    )
    lines.append(f"  Decoy content served:     {s['decoy_served_count']:,}")
    lines.append(f"  Potential concern events: {s['concern_count']:,}")
    if s["concern_count"]:
        lines.append("  (Full detail: analysis-concerns-all.txt)")
    lines.append("")
    lines.append("  Outcome key:")
    lines.append("    blocked/rate_limited/not_found/redirected = honeypot contained the probe")
    lines.append("    decoy_served = attacker received expected fake content (200)")
    lines.append("    concern = empty 200 on sensitive path or body matches leak patterns")
    lines.append("")

    lines.append("ATTACK OUTCOMES")
    lines.append("-" * 40)
    for outcome, count in analysis["attack_outcomes"].items():
        label = OUTCOME_LABELS.get(outcome, outcome)
        pct = round(100 * count / s["attack_requests"], 1) if s["attack_requests"] else 0
        lines.append(f"  {outcome:18s}  {count:6,} ({pct:5.1f}%)  {label}")
    lines.append("")

    lines.append("OUTCOMES BY ATTACK CLASSIFICATION")
    lines.append("-" * 40)
    for cls, outcomes in sorted(
        analysis["outcomes_by_classification"].items(),
        key=lambda x: -sum(x[1].values()),
    ):
        label = CLASSIFICATION_LABELS.get(cls, cls)
        top = ", ".join(f"{k}={v}" for k, v in list(outcomes.items())[:4])
        lines.append(f"  {cls:28s}  {sum(outcomes.values()):5,}  [{top}]")
    lines.append("")

    concerns = analysis["concern_events"]
    if concerns:
        lines.append("POTENTIAL CONCERN EVENTS (preview)")
        lines.append("-" * 40)
        for ev in concerns[:10]:
            leak = ev.get("leak_indicator") or "empty/sensitive"
            lines.append(
                f"  {ev['timestamp'][:19]}  {ev['client_ip']:18s}  "
                f"{ev['status_code']}  {ev['path'][:35]:35s}  "
                f"[{ev['classification']}] {leak}"
            )
        if len(concerns) > 10:
            lines.append(f"  ... {len(concerns)} total — see analysis-concerns report")
        lines.append("")

    lines.append("=" * 72)
    return "\n".join(lines)
