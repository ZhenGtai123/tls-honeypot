# Honeypot Log Report Tools

Two Python scripts parse honeypot request and traffic logs and produce human-readable text reports plus structured JSON.

| Script | Purpose |
|--------|---------|
| `parse_attacks.py` | Cybersecurity attack report: classifications, severity, CVE mapping, top attackers, drill-down detail reports |
| `parse_traffic.py` | General traffic report: HTTP methods, status codes, TLS, response times, experiment groups |

Shared modules:

| Module | Purpose |
|--------|---------|
| `log_loader.py` | Load and merge paired `requests-*.jsonl` / `traffic-*.jsonl` files |
| `classify_request.py` | Heuristic attack classification (RCE, login attempts, sensitive file probes, etc.) |
| `map_cve.py` | CVE and exploit-signature mapping from request paths, queries, and bodies |

No third-party packages are required — Python 3.7+ with the standard library is enough.

## Log files

Place paired JSONL files in a directory (e.g. `logs/`):

```
logs/
  requests-2026-06-11.jsonl
  traffic-2026-06-11.jsonl
  requests-2026-06-12.jsonl
  traffic-2026-06-12.jsonl
```

Each line in a file is one JSON object. `requests-*.jsonl` holds incoming request metadata; `traffic-*.jsonl` holds matched request/response pairs. Filenames must follow the pattern `requests-YYYY-MM-DD.jsonl` and `traffic-YYYY-MM-DD.jsonl` so the scripts can pair them by date.

When you do not pass explicit file paths, the scripts pick the **latest date pair** in `--dir`. Use `--all` to merge every matching pair into one report.

---

## parse_attacks.py

`parse_attacks.py` can produce three kinds of report:

| Mode | Flag | Output files (with `--all`) |
|------|------|-----------------------------|
| **Summary** | *(default)* | `attack-report-all.txt`, `attack-report-all.json` |
| **Classification detail** | `--detail CLASSIFICATION` | `detail-<classification>-all.txt`, `detail-<classification>-all.json` |
| **CVE detail** | `--cve CVE_ID` | `cve-<CVE_ID>-all.txt`, `cve-<CVE_ID>-all.json` |

Without `--all`, the date from the log filename is used instead of `-all` (e.g. `attack-report-2026-06-12.txt`).

`--detail` and `--cve` are mutually exclusive. Both produce a full per-event breakdown with request headers, bodies, and responses where available.

### Basic usage

From the project root, using the latest log pair in `logs/` and writing output to `reports/`:

```bash
python3 parse_attacks.py --dir logs --output-dir reports
```

Output (date taken from the log filename):

- `reports/attack-report-2026-06-12.txt`
- `reports/attack-report-2026-06-12.json`

### Aggregate all days

```bash
python3 parse_attacks.py --dir logs --output-dir reports --all
```

Output:

- `reports/attack-report-all.txt`
- `reports/attack-report-all.json`

The summary report includes a **LIKELY CVE / EXPLOIT SIGNATURES** section with counts and top paths for each matched CVE or technique.

### Explicit input files

```bash
python3 parse_attacks.py \
  --requests logs/requests-2026-06-11.jsonl \
  --traffic logs/traffic-2026-06-11.jsonl \
  --output-dir reports
```

### CVE mapping

Attack reports include a `cve_summary` section (JSON) and a matching text section that links request signatures to likely CVEs. Mappings are heuristic: a match means the traffic *resembles* a known exploit, not that your server is vulnerable.

List all supported CVE and technique rules:

```bash
python3 parse_attacks.py --list-cves
```

Example mappings:

| Request signature | Likely CVE |
|-------------------|------------|
| `/vendor/phpunit/.../eval-stdin.php` | CVE-2017-9841 (PHPUnit RCE) |
| POST body with `__proto__` + `child_process` | CVE-2025-55182 (React2Shell) |
| `/developmentserver/metadatauploader` | CVE-2024-34102 (Magento CosmicSting) |
| `/cgi-bin/../../bin/sh` | CVE-2021-41773 (Apache path traversal) |
| `/_ignition/execute-solution` | CVE-2021-3129 (Laravel Ignition) |
| `/webui/` | CVE-2024-3400 (Palo Alto PAN-OS) |
| `/.env` | TECH-ENV-EXPOSURE (exposed config file) |
| `/.git/config` | TECH-GIT-EXPOSURE (exposed repository) |

Technique IDs (prefixed `TECH-`) cover common exploit patterns that are not tied to a single CVE.

### Per-CVE detail report

Drill into every request that matches a specific CVE or technique signature:

```bash
python3 parse_attacks.py --dir logs --output-dir reports --all --cve CVE-2017-9841
```

Output:

- `reports/cve-CVE-2017-9841-all.txt`
- `reports/cve-CVE-2017-9841-all.json`

Technique IDs work the same way:

```bash
python3 parse_attacks.py --dir logs --output-dir reports --all --cve TECH-ENV-EXPOSURE
```

CVE detail reports include:

- CVE metadata (name, product, severity, confidence, notes)
- Summary stats (primary vs secondary signature matches, IPs, paths, time range)
- Attack classification breakdown for matching requests
- Full per-event details (headers, body, response, match role)

A request counts as a **primary** match when the CVE is its highest-confidence signature; otherwise it is **secondary** (the CVE matched but another signature ranked higher).

### Per-classification detail report

List classifications found in the logs:

```bash
python3 parse_attacks.py --dir logs --list-classifications
```

Generate a full event-by-event breakdown for one classification:

```bash
python3 parse_attacks.py --dir logs --output-dir reports --all --detail rce_attempt
```

Output:

- `reports/detail-rce_attempt-all.txt`
- `reports/detail-rce_attempt-all.json`

Aliases work too (e.g. `command_injection`, `rce`, `webdav`).

Detail reports include a **Likely CVE** field per event when the request matches a known exploit signature (e.g. `eval-stdin.php` → CVE-2017-9841).

### Print to terminal

```bash
python3 parse_attacks.py --dir logs --all --print
```

With `--print`, the text report goes to stdout. Use `--output-json` to still write JSON to disk.

### Options

| Flag | Description |
|------|-------------|
| `--dir DIR` | Directory to search for log files (default: `.`) |
| `--requests PATH` | Path to a specific requests JSONL file |
| `--traffic PATH` | Path to a specific traffic JSONL file |
| `--output-dir DIR` | Directory for default output filenames (default: `.`) |
| `--output-text PATH` | Override text report path |
| `--output-json PATH` | Override JSON report path |
| `--all` | Merge all `requests-*.jsonl` / `traffic-*.jsonl` pairs (cannot combine with `--requests` / `--traffic`) |
| `--detail CLASSIFICATION` | Per-event detail report for one attack type |
| `--cve CVE_ID` | Per-event detail report for one CVE or technique signature |
| `--list-classifications` | List classifications and counts, then exit |
| `--list-cves` | List CVE / exploit signature rules and exit |
| `--print` | Print text report to stdout instead of writing a file |

---

## parse_traffic.py

Generates a broader traffic overview: request/response coverage, HTTP methods, status codes, top paths and hosts, TLS versions, response latency percentiles, and experiment groups.

### Basic usage

```bash
python3 parse_traffic.py --dir logs --output-dir reports
```

Output:

- `reports/traffic-report-2026-06-12.txt`
- `reports/traffic-report-2026-06-12.json`

### Aggregate all days

```bash
python3 parse_traffic.py --dir logs --output-dir reports --all
```

Output:

- `reports/traffic-report-all.txt`
- `reports/traffic-report-all.json`

### Explicit input files

```bash
python3 parse_traffic.py \
  --requests logs/requests-2026-06-11.jsonl \
  --traffic logs/traffic-2026-06-11.jsonl \
  --output-dir reports
```

### Print to terminal

```bash
python3 parse_traffic.py --dir logs --all --print
```

### Options

| Flag | Description |
|------|-------------|
| `--dir DIR` | Directory to search for log files (default: `.`) |
| `--requests PATH` | Path to a specific requests JSONL file |
| `--traffic PATH` | Path to a specific traffic JSONL file |
| `--output-dir DIR` | Directory for default output filenames (default: `.`) |
| `--output-text PATH` | Override text report path |
| `--output-json PATH` | Override JSON report path |
| `--all` | Merge all log pairs (cannot combine with `--requests` / `--traffic`) |
| `--print` | Print text report to stdout instead of writing a file |

---

## Typical workflow

```bash
# 1. Attack summary across all collected logs (includes CVE counts)
python3 parse_attacks.py --dir logs --output-dir reports --all

# 2. General traffic stats for the same period
python3 parse_traffic.py --dir logs --output-dir reports --all

# 3. Drill into a specific attack type
python3 parse_attacks.py --dir logs --output-dir reports --all --detail login_attempt

# 4. Drill into a specific CVE seen in the summary report
python3 parse_attacks.py --dir logs --output-dir reports --all --cve CVE-2017-9841
```

## Help

```bash
python3 parse_attacks.py --help
python3 parse_traffic.py --help
```
