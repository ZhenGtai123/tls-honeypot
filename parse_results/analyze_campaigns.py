"""IP-level campaign analysis for honeypot traffic.

Groups requests by source IP into sessions, profiles scanner behavior,
and surfaces multi-step attack sequences.
"""

from collections import Counter, defaultdict
from datetime import datetime, timedelta
from typing import Dict, List, Optional

from classify_request import CLASSIFICATION_LABELS, classify_request

SESSION_GAP = timedelta(minutes=30)
BULK_SCANNER_REQUESTS = 500
BULK_SCANNER_PATHS = 100
ATTACK_CLASSES = frozenset(
    cls for cls in CLASSIFICATION_LABELS if cls not in ("reconnaissance", "unknown")
)


def _parse_ts(ts: str) -> datetime:
    ts = ts.replace("Z", "+00:00")
    if "." in ts:
        base, rest = ts.split(".", 1)
        frac, tz = rest.split("+", 1) if "+" in rest else (rest, "00:00")
        frac = (frac + "000000")[:6]
        ts = f"{base}.{frac}+{tz}"
    return datetime.fromisoformat(ts)


def _profile_ip(total: int, unique_paths: int, attack_count: int) -> str:
    if total >= BULK_SCANNER_REQUESTS or unique_paths >= BULK_SCANNER_PATHS:
        return "bulk_scanner"
    if attack_count >= 10 and unique_paths <= 20:
        return "targeted"
    if unique_paths >= 50:
        return "active_attacker"
    if total <= 5:
        return "drive_by"
    return "moderate"


def _split_sessions(events: List[dict]) -> List[List[dict]]:
    if not events:
        return []
    sessions: List[List[dict]] = [[events[0]]]
    for ev in events[1:]:
        gap = ev["_ts"] - sessions[-1][-1]["_ts"]
        if gap > SESSION_GAP:
            sessions.append([ev])
        else:
            sessions[-1].append(ev)
    return sessions


def build_campaign_analysis(requests: List[dict]) -> dict:
    """Analyze per-IP campaigns, deduplication, and attack sequences."""
    by_ip: Dict[str, List[dict]] = defaultdict(list)

    for req in requests:
        ip = req.get("client_ip") or "unknown"
        cls = classify_request(req)
        path = req.get("path", req.get("url", ""))
        method = req.get("method", "")
        by_ip[ip].append(
            {
                "_ts": _parse_ts(req["timestamp"]),
                "timestamp": req["timestamp"],
                "request_id": req["request_id"],
                "method": method,
                "path": path,
                "classification": cls,
                "dedup_key": (method, path),
            }
        )

    total_requests = len(requests)
    unique_probes = len({(r.get("client_ip"), r.get("method"), r.get("path", r.get("url", ""))) for r in requests})
    profile_counts = Counter()
    campaigns: List[dict] = []

    for ip, events in by_ip.items():
        events.sort(key=lambda e: e["_ts"])
        classifications = Counter(e["classification"] for e in events)
        paths = {e["path"] for e in events}
        dedup_keys = {e["dedup_key"] for e in events}
        attack_count = sum(classifications[c] for c in ATTACK_CLASSES if c in classifications)

        sessions = _split_sessions(events)
        session_summaries = []
        for i, sess in enumerate(sessions, 1):
            sess_cls = Counter(e["classification"] for e in sess)
            seq = []
            prev = None
            for e in sess:
                c = e["classification"]
                if c != prev:
                    seq.append(c)
                    prev = c
            session_summaries.append(
                {
                    "session": i,
                    "requests": len(sess),
                    "start": sess[0]["timestamp"],
                    "end": sess[-1]["timestamp"],
                    "classifications": dict(sess_cls.most_common()),
                    "sequence": seq,
                }
            )

        profile = _profile_ip(len(events), len(paths), attack_count)
        profile_counts[profile] += 1

        repeat_ratio = round(100 * (1 - len(dedup_keys) / len(events)), 1) if events else 0

        campaigns.append(
            {
                "ip": ip,
                "total_requests": len(events),
                "unique_paths": len(paths),
                "unique_probes": len(dedup_keys),
                "repeat_ratio_pct": repeat_ratio,
                "attack_requests": attack_count,
                "profile": profile,
                "classifications": dict(classifications.most_common()),
                "primary_activity": classifications.most_common(1)[0][0],
                "sessions": len(sessions),
                "first_seen": events[0]["timestamp"],
                "last_seen": events[-1]["timestamp"],
                "session_details": session_summaries[:10],
                "top_paths": dict(Counter(e["path"] for e in events).most_common(5)),
            }
        )

    campaigns.sort(key=lambda c: (-c["total_requests"], c["ip"]))

    # Multi-step sequences worth highlighting (3+ distinct attack classes in one session)
    notable_sequences: List[dict] = []
    for camp in campaigns:
        for sess in camp.get("session_details", []):
            attack_steps = [s for s in sess["sequence"] if s in ATTACK_CLASSES]
            seen = set()
            first_order: List[str] = []
            for step in attack_steps:
                if step not in seen:
                    seen.add(step)
                    first_order.append(step)
            if len(first_order) >= 2:
                notable_sequences.append(
                    {
                        "ip": camp["ip"],
                        "session": sess["session"],
                        "start": sess["start"],
                        "sequence": first_order,
                        "attack_types": len(first_order),
                        "requests": sess["requests"],
                    }
                )

    notable_sequences.sort(
        key=lambda s: (-s["attack_types"], -s["requests"], s["start"])
    )

    return {
        "summary": {
            "total_requests": total_requests,
            "unique_client_ips": len(by_ip),
            "unique_probes": unique_probes,
            "dedup_savings_pct": round(100 * (1 - unique_probes / total_requests), 1)
            if total_requests
            else 0,
            "ip_profiles": dict(profile_counts.most_common()),
        },
        "top_campaigns": campaigns[:25],
        "notable_sequences": notable_sequences[:30],
    }


def format_campaign_report(analysis: dict) -> str:
    lines = []
    s = analysis["summary"]

    lines.append("=" * 72)
    lines.append("CAMPAIGN ANALYSIS")
    lines.append("=" * 72)
    lines.append("")
    lines.append("SUMMARY")
    lines.append("-" * 40)
    lines.append(f"  Total requests:       {s['total_requests']:,}")
    lines.append(f"  Unique client IPs:    {s['unique_client_ips']:,}")
    lines.append(f"  Unique probes:        {s['unique_probes']:,}  (method + path + IP)")
    lines.append(
        f"  Repetitive traffic:   {s['dedup_savings_pct']}% of requests are repeats"
    )
    lines.append("")
    lines.append("IP PROFILES")
    lines.append("-" * 40)
    profile_desc = {
        "bulk_scanner": "High volume or wide path sweep (automated scanner)",
        "targeted": "Few paths, multiple attack attempts (focused)",
        "active_attacker": "Sustained attack activity",
        "drive_by": "Single-digit requests",
        "moderate": "Typical background probing",
    }
    for profile, count in s["ip_profiles"].items():
        lines.append(f"  {profile:18s}  {count:5,}  {profile_desc.get(profile, '')}")
    lines.append("")

    lines.append("TOP CAMPAIGNS BY VOLUME")
    lines.append("-" * 40)
    for camp in analysis["top_campaigns"][:15]:
        classes = ", ".join(
            f"{k}({v})" for k, v in list(camp["classifications"].items())[:3]
        )
        lines.append(
            f"  {camp['ip']:20s}  {camp['total_requests']:5,} reqs  "
            f"{camp['unique_paths']:4,} paths  {camp['sessions']} sessions  "
            f"[{camp['profile']}]"
        )
        lines.append(
            f"    repeat {camp['repeat_ratio_pct']}%  attacks {camp['attack_requests']}  "
            f"classes: {classes}"
        )
    lines.append("")

    sequences = analysis["notable_sequences"]
    if sequences:
        lines.append("MULTI-STEP ATTACK SEQUENCES")
        lines.append("-" * 40)
        lines.append("  IPs with 2+ attack types in a single session (first-seen order):")
        lines.append("")
        for seq in sequences[:15]:
            flow = " → ".join(seq["sequence"])
            lines.append(
                f"  {seq['ip']:20s}  session {seq['session']}  "
                f"{seq['requests']:4,} reqs  {seq['start'][:19]}"
            )
            lines.append(f"    {flow}")
        lines.append("")

    lines.append("=" * 72)
    return "\n".join(lines)
