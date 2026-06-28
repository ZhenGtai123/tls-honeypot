#!/usr/bin/env python3
"""
ip_country_breakdown.py
-----------------------
Extracts unique attacker IPs from the .txt report files and looks up their
country of origin using the MaxMind GeoLite2 offline database — the standard
geolocation database used in academic security and network measurement research.

Produces three separate breakdowns: vulnerable, hardened, and combined.

Setup (one-time):
    1. Sign up free at https://www.maxmind.com/en/geolite2/signup
    2. Download GeoLite2-Country.mmdb from your MaxMind account
    3. pip install geoip2 --break-system-packages

Usage:
    python3 python3 parse_results/ip_country_breakdown.py \
        --reports reports \
        --db path/to/GeoLite2-Country.mmdb

Expected folder layout:
    <reports>/
        vuln/
            attacks/  *.txt
        hardened/
            attacks/  *.txt

Output:
    - Prints all three tables to the terminal
    - Saves country_breakdown.txt to the reports folder
"""

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

try:
    import geoip2.database
    import geoip2.errors
except ImportError:
    sys.exit("geoip2 not installed. Run: pip3 install geoip2 --break-system-packages")

# Config
SKIP_IPS   = {"127.0.0.1", "::1", "localhost"}
IP_PATTERN = re.compile(r'Client IP:\s+(\S+)')
SKIP_DIRS  = {"__MACOSX", ".git", ".DS_Store"}

def is_hidden(path: Path) -> bool:
    return any(part.startswith(".") or part in SKIP_DIRS for part in path.parts)


def extract_unique_ips(folder: Path) -> set[str]:
    # Return the set of unique attacker IPs found in all .txt files under folder.
    ips: set[str] = set()
    for txt_file in folder.rglob("*.txt"):
        if is_hidden(txt_file):
            continue
        for line in txt_file.read_text(errors="replace").splitlines():
            m = IP_PATTERN.search(line)
            if m:
                ip = m.group(1).strip()
                if ip not in SKIP_IPS:
                    ips.add(ip)
    return ips


def lookup_country(ip: str, reader: geoip2.database.Reader) -> str:
    # Return the ISO country code for an IP, or 'Unknown'.
    try:
        response = reader.country(ip)
        return response.country.iso_code or "Unknown"
    except geoip2.errors.AddressNotFoundError:
        return "Unknown"
    except Exception:
        return "Unknown"


def count_countries(ip_set: set[str], reader: geoip2.database.Reader) -> Counter:
    # Return a Counter of {country_code: unique_ip_count} for a set of IPs.
    country_ips: Counter = Counter()
    for ip in ip_set:
        country_ips[lookup_country(ip, reader)] += 1
    return country_ips


def build_table(label: str, country_ips: Counter) -> str:
    # Build a formatted country breakdown table.
    total = sum(country_ips.values())
    lines = []
    lines.append("=" * 52)
    lines.append(f"  {label}  ({total:,} unique IPs)")
    lines.append("=" * 52)
    lines.append(f"  {'Country':<14} {'Unique IPs':>10}  {'%':>6}")
    lines.append(f"  {'-' * 14} {'-' * 10}  {'-' * 6}")
    for country, count in country_ips.most_common():
        pct = count / total * 100
        lines.append(f"  {country:<14} {count:>10,}  {pct:>5.1f}%")
    lines.append("=" * 52)
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="IP → Country breakdown from attack reports")
    parser.add_argument("--reports", required=True,
                        help="Path to the reports folder (contains vuln/ and hardened/ subdirs)")
    parser.add_argument("--db", required=True,
                        help="Path to GeoLite2-Country.mmdb (download free from maxmind.com)")
    args = parser.parse_args()

    reports_root = Path(args.reports)
    db_path      = Path(args.db)

    if not reports_root.exists():
        sys.exit(f"Reports folder not found: {reports_root}")
    if not db_path.exists():
        sys.exit(f"GeoLite2 database not found: {db_path}")

    vuln_dir     = reports_root / "vuln"
    hardened_dir = reports_root / "hardened"
    for d in (vuln_dir, hardened_dir):
        if not d.exists():
            sys.exit(f"Expected subfolder not found: {d}")

    print("Extracting unique IPs from report files...")
    vuln_ips     = extract_unique_ips(vuln_dir)
    hardened_ips = extract_unique_ips(hardened_dir)
    combined_ips = vuln_ips | hardened_ips

    print(f"   Vulnerable : {len(vuln_ips):,} unique IPs")
    print(f"   Hardened   : {len(hardened_ips):,} unique IPs")
    print(f"   Combined   : {len(combined_ips):,} unique IPs "
          f"({len(vuln_ips & hardened_ips):,} overlap both)\n")

    print("Looking up countries using MaxMind GeoLite2...")
    with geoip2.database.Reader(str(db_path)) as reader:
        vuln_counts     = count_countries(vuln_ips,     reader)
        hardened_counts = count_countries(hardened_ips, reader)
        combined_counts = count_countries(combined_ips, reader)

    vuln_table     = build_table("VULNERABLE", vuln_counts)
    hardened_table = build_table("HARDENED",   hardened_counts)
    combined_table = build_table("COMBINED",   combined_counts)

    full_report = "\n\n".join([vuln_table, hardened_table, combined_table])
    print(full_report)

    out_file = reports_root / "country_breakdown.txt"
    out_file.write_text(full_report)
    print(f"\nSaved → {out_file}")


if __name__ == "__main__":
    main()
