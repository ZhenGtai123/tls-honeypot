"""Shared utilities for loading honeypot request/traffic log files."""

import json
from pathlib import Path
from typing import List, Optional, Tuple


def load_requests(path: Path) -> List[dict]:
    records = []
    with path.open() as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def load_traffic(path: Path) -> List[dict]:
    records = []
    with path.open() as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def extract_date_from_filename(path: Path, prefix: str) -> Optional[str]:
    """Extract YYYY-MM-DD date from e.g. requests-2026-06-11.jsonl."""
    stem = path.stem
    parts = stem.rsplit("-", 3)
    if len(parts) >= 4 and parts[0] == prefix:
        return "-".join(parts[1:])
    return None


def find_all_log_pairs(directory: Path) -> List[Tuple[str, Path, Path]]:
    """Find all matching requests/traffic file pairs sorted by date."""
    pairs = []
    for req_path in sorted(directory.glob("requests-*.jsonl")):
        date = extract_date_from_filename(req_path, "requests")
        if not date:
            continue
        traf_path = directory / f"traffic-{date}.jsonl"
        if traf_path.exists():
            pairs.append((date, req_path, traf_path))
    return pairs


def find_latest_log_pair(directory: Path) -> Tuple[Optional[Path], Optional[Path]]:
    pairs = find_all_log_pairs(directory)
    if not pairs:
        return None, None
    _, req_path, traf_path = pairs[-1]
    return req_path, traf_path


def load_merged_logs(directory: Path) -> Tuple[List[dict], List[dict], List[dict]]:
    """Load and merge all log pairs. Returns (requests, traffic, source_files)."""
    pairs = find_all_log_pairs(directory)
    if not pairs:
        return [], [], []

    all_requests = []
    all_traffic = []
    source_files = []

    for date, req_path, traf_path in pairs:
        requests = load_requests(req_path)
        traffic = load_traffic(traf_path)
        all_requests.extend(requests)
        all_traffic.extend(traffic)
        source_files.append(
            {
                "date": date,
                "requests_file": req_path.name,
                "traffic_file": traf_path.name,
                "request_count": len(requests),
                "traffic_count": len(traffic),
            }
        )

    return all_requests, all_traffic, source_files
