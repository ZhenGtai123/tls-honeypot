# Honeypot Log Report Tools

Python scripts that parse honeypot request and traffic logs and produce human-readable text reports plus structured JSON. No third-party packages are required — Python 3.7+ with the standard library is enough.

## Scripts

| Script | Purpose |
|--------|---------|
| `generate_all_reports.py` | **Recommended.** Generates the full report set in one run |
| `parse_attacks.py` | Attack summary and individual classification/CVE drill-down reports |
| `parse_traffic.py` | General traffic overview (TLS, latency, experiment groups) |
| `compare_configs.py` | Standalone comparison of two honeypot configurations |

## Shared modules

| Module | Purpose |
|--------|---------|
| `log_loader.py` | Load and merge paired `requests-*.jsonl` / `traffic-*.jsonl` files |
| `classify_request.py` | Heuristic attack classification (RCE, login attempts, sensitive file probes, etc.) |
| `map_cve.py` | CVE and exploit-signature mapping from request paths, queries, and bodies |
| `analyze_outcomes.py` | Outcome scoring by HTTP status and response body (blocked, decoy, concern) |
| `analyze_campaigns.py` | IP profiles, sessions, and multi-step attack sequences |
| `compare_configs.py` | Side-by-side comparison of two log directories |

## Log files

Place paired JSONL files in a directory (e.g. `logs/vuln/`):

```
logs/vuln/
  requests-2026-06-11.jsonl
  traffic-2026-06-11.jsonl
  requests-2026-06-12.jsonl
  traffic-2026-06-12.jsonl
```

Each line in a file is one JSON object. `requests-*.jsonl` holds incoming request metadata; `traffic-*.jsonl` holds matched request/response pairs. Filenames must follow `requests-YYYY-MM-DD.jsonl` and `traffic-YYYY-MM-DD.jsonl` so the scripts can pair them by date.

By default, `generate_all_reports.py` merges **all** matching pairs. Use `--latest` to process only the most recent date pair.

---

## generate_all_reports.py

The primary entry point. Generates every report type and writes a manifest listing all output files.

### Basic usage

```bash
# Full report set for vuln logs (aggregates all days)
python3 generate_all_reports.py --dir logs/vuln --output-dir reports/vuln

# Compare vuln against hardened config
python3 generate_all_reports.py --dir logs/vuln --output-dir reports/vuln \
  --compare-with logs/hardened

# Summary + extended analysis only (skip large detail reports)
python3 generate_all_reports.py --dir logs/vuln --output-dir reports/vuln \
  --skip-classifications --skip-cves

# Single day only
python3 generate_all_reports.py --dir logs/vuln --output-dir reports/vuln --latest
```

### Output files

Aggregated runs use the `-all` suffix. Single-day runs use `-YYYY-MM-DD`.

| File | Content |
|------|---------|
| `attack-report-all.txt/json` | Main attack summary with CVE counts, outcome/campaign sections |
| `detail-<classification>-all.txt/json` | Full per-event detail for each attack classification |
| `cve-<CVE_ID>-all.txt/json` | Full per-event detail for each matched CVE/technique |
| `analysis-outcomes-all.txt/json` | Outcome scoring: blocked, rate-limited, decoy, concern rates |
| `analysis-concerns-all.txt/json` | Full per-event detail for potential concern events only |
| `analysis-campaigns-all.txt/json` | IP profiles, sessions, multi-step attack sequences |
| `compare-<A>-vs-<B>.txt/json` | Config comparison (when `--compare-with` is set) |
| `report-manifest.json` | Index of all generated files with counts and summary stats |

### Options

| Flag | Description |
|------|-------------|
| `--dir DIR` | Directory containing log files (default: `.`) |
| `--requests PATH` | Specific requests JSONL file (implies `--latest`) |
| `--traffic PATH` | Specific traffic JSONL file (implies `--latest`) |
| `--output-dir DIR` | Output directory (default: `reports`) |
| `--latest` | Process only the latest log pair (default: aggregate all days) |
| `--skip-summary` | Skip the main attack summary report |
| `--skip-classifications` | Skip per-classification detail reports |
| `--skip-cves` | Skip per-CVE detail reports |
| `--skip-extended` | Skip outcome, concern, and campaign analysis |
| `--include-empty` | Write detail reports even for zero-match classifications/CVEs |
| `--all-catalog-cves` | Write CVE detail for the full catalog, not just matches in logs |
| `--compare-with DIR` | Compare `--dir` logs against another config directory |
| `--compare-baseline-label` | Display label for the baseline (`--compare-with`) config |
| `--compare-label` | Display label for the current (`--dir`) config |

### Extended analysis

**Outcome analysis** scores each attack request by HTTP response:

- `blocked` / `rate_limited` / `not_found` / `redirected` — honeypot contained the probe
- `decoy_served` — attacker received expected fake content (HTTP 200)
- Concern events — empty HTTP 200 on a sensitive path, or body matching leak patterns

**Concern report** (`analysis-concerns-all.txt`) lists every flagged event with full request/response detail.

**Campaign analysis** groups traffic by source IP: profiles (`bulk_scanner`, `targeted`, etc.), sessions (30-minute gap), deduplication stats, and multi-step attack sequences.

**Config comparison** (`--compare-with`) shows classification and outcome-rate deltas between two honeypot configurations.

Standalone comparison:

```bash
python3 compare_configs.py logs/hardened logs/vuln --output-dir reports
```

---

## parse_attacks.py

Generates individual reports. Useful for ad-hoc drill-down; prefer `generate_all_reports.py` for batch runs.

| Mode | Flag | Output files (aggregated) |
|------|------|---------------------------|
| **Summary** | *(default)* | `attack-report-all.txt/json` |
| **Classification detail** | `--detail CLASSIFICATION` | `detail-<classification>-all.txt/json` |
| **CVE detail** | `--cve CVE_ID` | `cve-<CVE_ID>-all.txt/json` |

```bash
python3 parse_attacks.py --dir logs/vuln --output-dir reports/vuln --all
python3 parse_attacks.py --dir logs/vuln --output-dir reports/vuln --all --detail rce_attempt
python3 parse_attacks.py --dir logs/vuln --output-dir reports/vuln --all --cve CVE-2017-9841
python3 parse_attacks.py --list-classifications
python3 parse_attacks.py --list-cves
```

The summary report includes outcome and campaign sections. CVE mappings are heuristic — a match means the traffic *resembles* a known exploit, not that the target is vulnerable.

Example CVE mappings:

| Request signature | Likely CVE |
|-------------------|------------|
| `/vendor/phpunit/.../eval-stdin.php` | CVE-2017-9841 (PHPUnit RCE) |
| POST body with `__proto__` + `child_process` | CVE-2025-55182 (React2Shell) |
| `/developmentserver/metadatauploader` | CVE-2024-34102 (Magento CosmicSting) |
| `/.env` | TECH-ENV-EXPOSURE |
| `/.git/config` | TECH-GIT-EXPOSURE |

### Options

| Flag | Description |
|------|-------------|
| `--dir DIR` | Directory to search for log files |
| `--requests PATH` | Path to a specific requests JSONL file |
| `--traffic PATH` | Path to a specific traffic JSONL file |
| `--output-dir DIR` | Directory for output files |
| `--all` | Merge all log pairs |
| `--detail CLASSIFICATION` | Per-event detail for one attack type |
| `--cve CVE_ID` | Per-event detail for one CVE or technique |
| `--list-classifications` | List classifications and counts, then exit |
| `--list-cves` | List CVE rules and exit |
| `--print` | Print text report to stdout |

---

## parse_traffic.py

Broader traffic overview: request/response coverage, HTTP methods, status codes, top paths and hosts, TLS versions, response latency percentiles, and experiment groups.

```bash
python3 parse_traffic.py --dir logs/vuln --output-dir reports/vuln --all
```

Output: `traffic-report-all.txt/json`

---

## Typical workflow

```bash
# 1. Full report set (summary + details + extended analysis)
python3 generate_all_reports.py --dir logs/vuln --output-dir reports/vuln \
  --compare-with logs/hardened

# 2. General traffic stats
python3 parse_traffic.py --dir logs/vuln --output-dir reports/vuln --all

# 3. Review concern events
less reports/vuln/analysis-concerns-all.txt

# 4. Ad-hoc drill-down (if needed)
python3 parse_attacks.py --dir logs/vuln --output-dir reports/vuln --all --detail rce_attempt
python3 parse_attacks.py --dir logs/vuln --output-dir reports/vuln --all --cve CVE-2017-9841
```

## Help

```bash
python3 generate_all_reports.py --help
python3 parse_attacks.py --help
python3 parse_traffic.py --help
python3 compare_configs.py --help
```
