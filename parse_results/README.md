# Honeypot Log Report Tools

Two Python scripts parse honeypot request and traffic logs and produce human-readable text reports plus structured JSON.

| Script | Purpose |
|--------|---------|
| `parse_attacks.py` | Cybersecurity attack report: classifications, severity, top attackers, successful probes |
| `parse_traffic.py` | General traffic report: HTTP methods, status codes, TLS, response times, experiment groups |

Both scripts depend on `log_loader.py` (log loading) and `classify_request.py` (request classification). No third-party packages are required — Python 3.7+ with the standard library is enough.

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

Generates an attack-focused report with classification counts, severity breakdown, top targeted paths, hourly/daily activity, and samples of attack traffic.

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

### Explicit input files

```bash
python3 parse_attacks.py \
  --requests logs/requests-2026-06-11.jsonl \
  --traffic logs/traffic-2026-06-11.jsonl \
  --output-dir reports
```

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
| `--list-classifications` | List classifications and counts, then exit |
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
# 1. Attack summary across all collected logs
python3 parse_attacks.py --dir logs --output-dir reports --all

# 2. General traffic stats for the same period
python3 parse_traffic.py --dir logs --output-dir reports --all

# 3. Drill into a specific attack type
python3 parse_attacks.py --dir logs --output-dir reports --all --detail login_attempt
```

## Help

```bash
python3 parse_attacks.py --help
python3 parse_traffic.py --help
```
