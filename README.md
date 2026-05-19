# TLS MitM Honeypot

TU Delft Hacking Lab — Project #12. A TLS-terminating proxy that decrypts attacker traffic and forwards it to a fake HTTP service we control, so we can observe what attackers actually do over TLS.

## Goal

Set up a TLS proxy between a client and a target service. The proxy terminates TLS, logs the decrypted traffic (request + response + handshake metadata), and forwards plaintext to a backend honeypot — so we can observe what attackers do over otherwise-encrypted channels.

## Architecture

Two Go programs, separate binaries, talking over the network:

```
attacker ──TLS──▶  proxy  ──plaintext──▶  honeypot
                  :8443                    :8080
              (terminates TLS,           (fake admin login,
               logs traffic)              logs requests)
```

- **`src/proxy/`** — TLS-terminating reverse proxy. Accepts HTTPS, logs full request + response (with TLS handshake metadata) as JSON to `./logs/`, forwards plaintext to the honeypot.
- **`src/honeypot/`** — Fake HTTP service that returns a believable admin login page and logs every request as JSON lines.
- **`deployments/`** — Dockerfiles, firewall script for production.

## References

- https://github.com/Nirusu/how-to-setup-a-honeypot
- https://www.mitmproxy.org/

## Responsible Professor

Harm Griffioen

---

## Quick start

```bash
# 1. Generate dev cert (one-time)
openssl req -x509 -newkey rsa:2048 -nodes \
  -keyout testdata/key.pem -out testdata/cert.pem \
  -days 365 -subj "/CN=localhost"

# 2. Bring up the stack (Docker)
docker compose up -d

# 3. Test
curl -k https://localhost:8443/admin
docker compose logs honeypot                # honeypot JSON
cat logs/traffic-$(date +%F).jsonl          # proxy traffic

# 4. Tear down
docker compose down
```

---

## Local development

Two ways to run: native Go binaries (fastest iteration) or Docker (matches production).

### Option A: Native binaries

Three terminals, no Docker required:

```bash
# Terminal 1 — honeypot on :8080
go run ./src/honeypot

# Terminal 2 — proxy on :8443 (or :18443 on Windows if Docker held :8443)
go run ./src/proxy

# Terminal 3 — test
curl -k https://localhost:8443/admin
```

> **Windows port-conflict gotcha:** if you see `bind: An attempt was made to access a socket in a way forbidden by its access permissions`, port `:8443` is in the Hyper-V reserved range (residue from Docker Desktop). Run the proxy with `--listen :18443` instead, or reboot to release the reservation.

### Option B: Docker compose

```bash
docker compose build
docker compose up -d
curl -k https://localhost:8443/admin
docker compose down
```

What `docker compose up` gives you:

- **Proxy** at host `:8443` (forwards to container `honeypot:8080` on the internal `honeynet` network)
- **Honeypot** at internal `:8080` only — *not* reachable from the host or the internet
- **Cert files** mounted read-only from `./testdata/` into the proxy
- **Proxy logs** persist on the host in `./logs/` (gitignored)
- **Restart policy** `unless-stopped` so containers come back after reboot

### Flags

Both binaries accept `--help`.

| Flag | Proxy default | Honeypot default | Notes |
|---|---|---|---|
| `--listen` | `:8443` | `:8080` | Use `:443` for proxy in production |
| `--target` | `localhost:8080` | — | Proxy upstream |
| `--cert` / `--key` | `testdata/cert.pem` / `testdata/key.pem` | — | TLS material for proxy |
| `--log-dir` | `./logs` | — | Where proxy writes JSON logs |
| `--log-file` | — | (stdout) | Honeypot log destination |
| `--forward-https` | `false` | — | Forward to honeypot over HTTPS instead of HTTP |
| `--verbose` | `false` | — | Echo each request/response to stdout |

---

## Testing

### Smoke test (1 request)

```bash
curl -k https://localhost:8443/admin
```

Expected: HTTP 200, fake login HTML returned, one new entry in both the honeypot log and `logs/traffic-*.jsonl`.

### Probe battery (representative attacker traffic)

```bash
URL=https://localhost:8443

# Scanner UAs
curl -ksS -A "Mozilla/5.0 (compatible; CensysInspect/1.1)" $URL/
curl -ksS -A "masscan/1.3.2" $URL/
curl -ksS -A "Mozilla/5.00 (Nikto/2.1.6)" $URL/robots.txt
curl -ksS -A "sqlmap/1.7.2#stable" -X POST -d "username=admin'--&password=" $URL/admin

# Common CVE-probe paths
curl -ksS $URL/.git/HEAD
curl -ksS $URL/.env
curl -ksS $URL/server-status
curl -ksS $URL/actuator/health
curl -ksS $URL/manager/html

# Credential stuffing
curl -ksS -X POST -d "log=admin&pwd=hunter2" $URL/wp-login.php

# Unusual methods (expect 405)
curl -ksS -X PUT  $URL/upload
curl -ksS -X TRACE $URL/

# Binary body (verifies base64 encoding)
printf 'binary\xff\xfe\x80\x81data' | curl -ksS $URL/upload -X POST --data-binary @-
```

### Inspecting the logs

```bash
# Last 5 proxy traffic entries (request + response + TLS)
tail -5 logs/traffic-$(date +%F).jsonl | python -m json.tool

# Last 5 honeypot entries
docker compose logs honeypot --no-log-prefix | tail -5

# Count requests by status code (proxy)
cat logs/traffic-*.jsonl | python -c "
import json, sys, collections
c = collections.Counter(json.loads(l)['response']['status_code'] for l in sys.stdin)
for k, v in sorted(c.items()): print(f'{k}: {v}')"

# Top User-Agents
cat logs/traffic-*.jsonl | python -c "
import json, sys, collections
c = collections.Counter(json.loads(l)['request']['headers'].get('User-Agent','') for l in sys.stdin)
for ua, n in c.most_common(10): print(f'{n:4d}  {ua[:80]}')"
```

PowerShell equivalents:

```powershell
Get-Content logs\traffic-2026-05-19.jsonl -Tail 5
Get-Content logs\traffic-2026-05-19.jsonl -Tail 1 | python -m json.tool
```

---

## Log schema

### `logs/requests-YYYY-MM-DD.jsonl` (proxy, one line per request)

| Field | Type | Notes |
|---|---|---|
| `timestamp` | RFC3339 | When the request arrived at the proxy |
| `method` | string | GET / POST / etc. |
| `url` | string | Path + query |
| `proto` | string | `HTTP/1.1` or `HTTP/2.0` (from ALPN negotiation) |
| `host` | string | Host header value |
| `headers` | map | All request headers as a flat map |
| `body` | string | Request body, UTF-8 or base64 (see `body_encoding`) |
| `body_encoding` | string | Omitted = UTF-8; `"base64"` = raw bytes weren't valid UTF-8 |
| `body_truncated` | bool | True if body exceeded 10 KB and was cut |
| `client_ip` | string | IP of the connecting client (no port) |
| `forwarded_to` | string | Backend URL the proxy forwarded to |
| `tls.version` | string | `TLS 1.2` / `TLS 1.3` |
| `tls.cipher_suite` | string | e.g. `TLS_AES_128_GCM_SHA256` |
| `tls.server_name` | string | SNI from ClientHello |
| `tls.negotiated_protocol` | string | ALPN result: `h2` or `http/1.1` |

### `logs/traffic-YYYY-MM-DD.jsonl` (proxy, one line per request+response pair)

Same `request` block as above, plus a `response` block with `status_code`, `status`, `headers`, `body`, `body_encoding`, `body_truncated`, `duration_ms`. **Error responses (502 when backend is down, etc.) are recorded here too** with `response.body` containing the error reason.

### Honeypot stdout (one line per request)

| Field | Notes |
|---|---|
| `timestamp` | UTC |
| `method`, `path`, `query`, `proto`, `host` | Standard request fields |
| `headers` | All headers, including `X-Forwarded-For` from the proxy |
| `body`, `body_encoding`, `body_truncated` | Same convention as proxy |
| `client_ip` | Real attacker IP (pulled from `X-Forwarded-For`, falls back to `RemoteAddr`) |
| `user_agent` | Convenience copy of the UA header |

---

## Deploy to a remote VM

The professor will provide a VM. Once you have SSH access:

### 1. Prepare the VM (once per VM)

```bash
ssh user@<vm-ip>

# Install Docker + ufw
sudo apt update
sudo apt install -y docker.io docker-compose-plugin ufw git

# Clone the repo
git clone https://github.com/ZhenGtai123/tls-honeypot.git
cd tls-honeypot
git checkout main   # or whichever branch is canonical at deploy time
```

### 2. Get a TLS cert

Two options:

- **Self-signed** (fast, attackers see warnings):
  ```bash
  mkdir -p testdata
  openssl req -x509 -newkey rsa:2048 -nodes \
    -keyout testdata/key.pem -out testdata/cert.pem \
    -days 365 -subj "/CN=$(hostname -f)"
  ```
- **Let's Encrypt** (requires a real domain pointing at the VM): set up Caddy or certbot, then mount the result into `testdata/`.

### 3. Switch the proxy to port 443

Edit `compose.yaml` one line:

```yaml
ports:
  - "443:8443"   # was "8443:8443" for local dev
```

### 4. Lock down the host

The repo ships a firewall script. **Edit it first** to put your home IP in the SSH allow rule, then run:

```bash
sudo bash deployments/firewall.sh
```

What this does (in plain English):

- Drops every inbound packet by default
- Allows SSH (port 22) only from your home IP
- Allows public TLS (port 443)
- Drops every outbound packet by default
- Allows only DNS, HTTPS-out (for `apt update` + log shipping), and NTP (clock sync)
- Notably blocks outbound SMTP/IRC/etc. so a compromised honeypot can't be weaponized for spam or DDoS

### 5. Bring it up

```bash
docker compose up -d
docker compose ps          # both containers should be Up
docker compose logs proxy --tail 5
```

### 6. Verify from outside

From your phone's hotspot (or any non-VM network):

```bash
curl -k https://<vm-public-ip>/admin
```

You should get the fake login HTML, and within seconds you'll start seeing the request in `logs/traffic-*.jsonl` on the VM.

### 7. Updating after a merge

```bash
ssh user@<vm-ip>
cd tls-honeypot
git pull
docker compose build
docker compose up -d        # rolling restart, picks up new images
```

---

## Operations

### Where logs land

- `logs/requests-YYYY-MM-DD.jsonl` and `logs/traffic-YYYY-MM-DD.jsonl` — rotated daily by the proxy
- `docker compose logs honeypot` — honeypot stdout (rotated by Docker)

### Shipping logs off the VM

Run from your laptop periodically:

```bash
rsync -avz user@<vm-ip>:tls-honeypot/logs/ ./vm-logs/
```

### Healthcheck

Set up Uptime Robot (free) or similar to ping `https://<vm-public-ip>/` every 5 minutes and alert you if it goes down.

### Stopping

```bash
docker compose down
```

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Proxy fails to bind `:8443` on Windows with "socket access permission" | Hyper-V reserved port range | Run with `--listen :18443`, or reboot to release |
| `docker compose` fails with `open //./pipe/dockerDesktopLinuxEngine` | Docker Desktop is stopped | Start Docker Desktop |
| `openssl` fails with "Can't open openssl.cnf" | Miniconda's OpenSSL doesn't ship a config | `$env:OPENSSL_CONF = "C:\Program Files\Git\usr\ssl\openssl.cnf"` before running |
| Requests return 502 immediately | Honeypot container isn't up | `docker compose ps`, then `docker compose up -d honeypot` |
| `body` field in logs has `�` characters | Should never happen since the base64 fix; if it does, file a bug | Check `body_encoding`; non-UTF-8 should be `"base64"` |
| Log files dated wrong | Container runs in UTC; your laptop is local time | Expected — filenames use UTC |

---

## Project status

- [x] Initial scaffold (`go.mod`, `.gitignore`, README)
- [x] Proxy: TLS termination + reverse proxy + JSON request/response logs *(QS832 on `vibe-coded`)*
- [x] Honeypot: fake admin login + JSON request logs
- [x] TLS handshake metadata in proxy logs (SNI, ALPN, cipher, TLS version)
- [x] Dockerfiles + `compose.yaml` for local deployment
- [x] Non-UTF-8 body safety (base64 fallback) — no byte-level data loss
- [x] Proxy error responses logged to traffic file (502s no longer invisible)
- [x] `deployments/firewall.sh` — ufw rules for the production VM
- [ ] More fake endpoints (`/wp-login.php`, `/.env`, `/phpmyadmin/`, etc. returning believable per-app responses instead of one generic login page)
- [ ] GitHub Actions CI (`go build`, `go vet`, `go test`)
- [ ] `docs/architecture.md` capturing design decisions
- [ ] Deployment to a public VM
- [ ] Log shipping pipeline (cron `rsync`)
- [ ] Data analysis + project report
