"""Compare honeypot configurations (e.g. vuln vs hardened)."""

from collections import Counter
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from analyze_campaigns import build_campaign_analysis
from analyze_outcomes import build_outcome_analysis
from classify_request import CLASSIFICATION_LABELS, classify_request
from log_loader import filter_operator_traffic, load_merged_logs


def _classification_counts(requests: List[dict]) -> Dict[str, int]:
    counts = Counter(classify_request(r) for r in requests)
    return {cls: counts.get(cls, 0) for cls in CLASSIFICATION_LABELS}


def _delta_pct(a: int, b: int) -> Optional[float]:
    if a == 0:
        return None if b == 0 else 100.0
    return round(100 * (b - a) / a, 1)


def load_config_logs(log_dir: Path) -> Tuple[List[dict], List[dict], str]:
    requests, traffic, _ = load_merged_logs(log_dir)
    requests, traffic = filter_operator_traffic(requests, traffic)
    name = log_dir.name or str(log_dir)
    return requests, traffic, name


def build_config_comparison(
    baseline_dir: Path,
    comparison_dir: Path,
    baseline_label: Optional[str] = None,
    comparison_label: Optional[str] = None,
) -> dict:
    """Compare two honeypot log directories."""
    base_req, base_traf, base_name = load_config_logs(baseline_dir)
    cmp_req, cmp_traf, cmp_name = load_config_logs(comparison_dir)

    base_label = baseline_label or base_name
    cmp_label = comparison_label or cmp_name

    base_cls = _classification_counts(base_req)
    cmp_cls = _classification_counts(cmp_req)

    base_outcomes = build_outcome_analysis(base_req, base_traf)
    cmp_outcomes = build_outcome_analysis(cmp_req, cmp_traf)

    base_campaigns = build_campaign_analysis(base_req)
    cmp_campaigns = build_campaign_analysis(cmp_req)

    classification_diff = []
    all_keys = set(base_cls) | set(cmp_cls)
    for cls in sorted(all_keys, key=lambda c: -(base_cls.get(c, 0) + cmp_cls.get(c, 0))):
        b = base_cls.get(cls, 0)
        c = cmp_cls.get(cls, 0)
        classification_diff.append(
            {
                "classification": cls,
                "label": CLASSIFICATION_LABELS.get(cls, cls),
                base_label: b,
                cmp_label: c,
                "delta": c - b,
                "delta_pct": _delta_pct(b, c),
            }
        )

    def outcome_rates(outcomes: dict) -> dict:
        attack = outcomes["summary"]["attack_requests"]
        ao = outcomes["attack_outcomes"]
        if not attack:
            return {}
        return {
            k: round(100 * v / attack, 1) for k, v in ao.items()
        }

    base_rates = outcome_rates(base_outcomes)
    cmp_rates = outcome_rates(cmp_outcomes)

    outcome_diff = []
    for outcome in sorted(set(base_rates) | set(cmp_rates)):
        outcome_diff.append(
            {
                "outcome": outcome,
                base_label: base_rates.get(outcome, 0),
                cmp_label: cmp_rates.get(outcome, 0),
                "delta_pct_points": round(
                    cmp_rates.get(outcome, 0) - base_rates.get(outcome, 0), 1
                ),
            }
        )

    return {
        "baseline": {
            "label": base_label,
            "dir": str(baseline_dir),
            "total_requests": len(base_req),
            "unique_ips": base_campaigns["summary"]["unique_client_ips"],
            "classifications": base_cls,
            "outcomes": base_outcomes["summary"],
            "defensive_pct": base_outcomes["summary"]["defensive_success_pct"],
        },
        "comparison": {
            "label": cmp_label,
            "dir": str(comparison_dir),
            "total_requests": len(cmp_req),
            "unique_ips": cmp_campaigns["summary"]["unique_client_ips"],
            "classifications": cmp_cls,
            "outcomes": cmp_outcomes["summary"],
            "defensive_pct": cmp_outcomes["summary"]["defensive_success_pct"],
        },
        "classification_diff": classification_diff,
        "outcome_rate_diff": outcome_diff,
        "defensive_improvement_pct_points": round(
            cmp_outcomes["summary"]["defensive_success_pct"]
            - base_outcomes["summary"]["defensive_success_pct"],
            1,
        ),
    }


def format_comparison_report(comparison: dict) -> str:
    base = comparison["baseline"]
    cmp = comparison["comparison"]
    lines = []

    lines.append("=" * 72)
    lines.append(f"CONFIG COMPARISON: {base['label']} vs {cmp['label']}")
    lines.append("=" * 72)
    lines.append("")
    lines.append("OVERVIEW")
    lines.append("-" * 40)
    lines.append(f"  {'':20s}  {base['label']:>12s}  {cmp['label']:>12s}  {'delta':>8s}")
    lines.append(
        f"  {'Total requests':20s}  {base['total_requests']:12,}  "
        f"{cmp['total_requests']:12,}  {cmp['total_requests'] - base['total_requests']:+8,}"
    )
    lines.append(
        f"  {'Unique IPs':20s}  {base['unique_ips']:12,}  "
        f"{cmp['unique_ips']:12,}  {cmp['unique_ips'] - base['unique_ips']:+8,}"
    )
    lines.append(
        f"  {'Defensive outcome %':20s}  {base['defensive_pct']:11.1f}%  "
        f"{cmp['defensive_pct']:11.1f}%  "
        f"{comparison['defensive_improvement_pct_points']:+7.1f}pp"
    )
    lines.append(
        f"  {'Concern events':20s}  {base['outcomes']['concern_count']:12,}  "
        f"{cmp['outcomes']['concern_count']:12,}  "
        f"{cmp['outcomes']['concern_count'] - base['outcomes']['concern_count']:+8,}"
    )
    lines.append("")

    lines.append("CLASSIFICATION CHANGES")
    lines.append("-" * 40)
    for row in comparison["classification_diff"]:
        if row["delta"] == 0:
            continue
        delta_pct = row["delta_pct"]
        pct_str = f"{delta_pct:+.1f}%" if delta_pct is not None else "n/a"
        lines.append(
            f"  {row['classification']:28s}  {row[base['label']]:6,} → "
            f"{row[cmp['label']]:6,}  ({row['delta']:+,} / {pct_str})"
        )
    lines.append("")

    lines.append("ATTACK OUTCOME RATE CHANGES (percentage points)")
    lines.append("-" * 40)
    for row in comparison["outcome_rate_diff"]:
        d = row["delta_pct_points"]
        if d == 0:
            continue
        lines.append(
            f"  {row['outcome']:18s}  {row[base['label']]:5.1f}% → "
            f"{row[cmp['label']]:5.1f}%  ({d:+.1f}pp)"
        )
    lines.append("")
    lines.append("=" * 72)
    return "\n".join(lines)


def main() -> None:
    import argparse
    import json

    parser = argparse.ArgumentParser(description="Compare two honeypot log configurations.")
    parser.add_argument("baseline", type=Path, help="Baseline log directory")
    parser.add_argument("comparison", type=Path, help="Comparison log directory")
    parser.add_argument("--baseline-label", help="Label for baseline config")
    parser.add_argument("--comparison-label", help="Label for comparison config")
    parser.add_argument("--output-dir", type=Path, default=Path("reports"))
    parser.add_argument("--print", action="store_true", dest="print_report")
    args = parser.parse_args()

    comparison = build_config_comparison(
        args.baseline,
        args.comparison,
        baseline_label=args.baseline_label,
        comparison_label=args.comparison_label,
    )
    text = format_comparison_report(comparison)
    if args.print_report:
        print(text)
    else:
        args.output_dir.mkdir(parents=True, exist_ok=True)
        name = f"compare-{comparison['baseline']['label']}-vs-{comparison['comparison']['label']}"
        (args.output_dir / f"{name}.txt").write_text(text)
        (args.output_dir / f"{name}.json").write_text(json.dumps(comparison, indent=2))
        print(f"Wrote {args.output_dir / f'{name}.txt'}")


if __name__ == "__main__":
    main()
