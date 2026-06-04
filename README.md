# TLS MitM Honeypot

TU Delft Hacking Lab — Project #12.  
**Responsible professor:** Harm Griffioen

---

## How it works

```
attacker ──[TLS A]──▶ proxy (MitM) ──[TLS B]──▶ nginx ──[HTTP]──▶ wordpress ──▶ db
```

The proxy sits invisibly in the middle of two independent TLS sessions:

- **TLS A** — the attacker's session. The proxy presents a rotating self-signed certificate. The attacker sees a normal HTTPS server.
- **TLS B** — the proxy's connection to nginx. Uses a static self-signed cert from `testdata/`. The proxy skips cert verification (it trusts its own backend).

The attacker never knows a proxy exists. All traffic — including the full TLS ClientHello fingerprint — is logged to JSON before being forwarded unchanged.

Two stacks run in parallel. Each has its own proxy with a different certificate identity:

| Stack | Cert CN | WordPress | PHP | Character |
|---|---|---|---|---|
| **Vulnerable** | `sys-admin.internal` | 5.9 | 7.4 EOL | Debug on, 512 MB uploads, no security headers |
| **Hardened** | `fge-integration-test.internal.coralset.com` | 6.7 | 8.3 | Debug off, 8 MB uploads, security headers |

---

## A — Prerequisites

### Local machine (dev/testing)

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) running
- [Go 1.21+](https://go.dev/dl/) installed (only needed if running proxies natively)

### VM (production deployment)

- Ubuntu 22.04 LTS
- Docker + Docker Compose v2: `apt install -y docker.io docker-compose-plugin`
- Go 1.21+: see https://go.dev/dl/ or run the installer script
- iptables-persistent: `apt install -y iptables-persistent`
- openssl: `apt install -y openssl`

---

## B — Generate the nginx backend certificate

nginx needs a TLS certificate for **TLS B** (the proxy→nginx leg). This cert is never seen by attackers; it just encrypts the internal connection. Generate it once and commit the public cert (not the key).

```bash
# Run from the project root
mkdir -p testdata

openssl req -x509 -newkey rsa:2048 -nodes \
  -keyout testdata/key.pem \
  -out  testdata/cert.pem \
  -days 3650 \
  -subj "/CN=honeypot-backend"
```

> Do **not** commit `testdata/key.pem`. It is already in `.gitignore`.  
> `testdata/cert.pem` (public cert only) can be committed.

The proxy connects to nginx with `--forward-https` and skips cert verification, so any self-signed cert works.

---

## Local testing — everything in Docker (`compose.yaml`)

Use this for development. Both proxies and both WordPress stacks run as containers.

### C — Create log directories

```bash
mkdir -p logs/vuln logs/hardened
```

### D — Start the full stack

```bash
docker compose up -d --build
```

This starts 8 containers:

```
proxy-vuln      → nginx-vuln      → wp-vuln      → db-vuln
proxy-hardened  → nginx-hardened  → wp-hardened  → db-hardened
```

Wait ~15 seconds for WordPress to finish initialising. Check all containers are healthy:

```bash
docker compose ps
```

Expected output — all containers `Up`, no `Restarting`:

```
tls-honeypot-proxy-vuln-1       Up   0.0.0.0:8443->8443/tcp
tls-honeypot-proxy-hardened-1   Up   0.0.0.0:8444->8443/tcp
tls-honeypot-nginx-vuln-1       Up
tls-honeypot-nginx-hardened-1   Up
tls-honeypot-wp-vuln-1          Up
tls-honeypot-wp-hardened-1      Up
tls-honeypot-db-vuln-1          Up
tls-honeypot-db-hardened-1      Up
```

### E — Verify the MitM is transparent

Check that each proxy presents a different certificate (the attacker sees two unrelated servers):

```bash
# Vulnerable proxy — should show CN=sys-admin.internal
echo | openssl s_client -connect localhost:8443 2>/dev/null | openssl x509 -noout -subject

# Hardened proxy — should show CN=fge-integration-test.internal.coralset.com
echo | openssl s_client -connect localhost:8444 2>/dev/null | openssl x509 -noout -subject
```

Hit both stacks:

```bash
curl -k https://localhost:8443/          # vulnerable WordPress home
curl -k https://localhost:8444/          # hardened WordPress home
```

### F — Test attacker behaviour

```bash
# Credential stuffing — captured by both stacks
curl -k -X POST \
  -d "log=admin&pwd=hunter2&wp-submit=Log+In&redirect_to=%2Fwp-admin%2F&testcookie=1" \
  https://localhost:8443/wp-login.php

# Config-leak probe — vuln serves it, hardened WordPress handles it differently
curl -k https://localhost:8443/.env
curl -k https://localhost:8444/.env

# XML-RPC probe
curl -k https://localhost:8443/xmlrpc.php
curl -k https://localhost:8444/xmlrpc.php

# Path traversal attempt
curl -k "https://localhost:8443/wp-content/../../../../etc/passwd"

# Scanner user-agent
curl -k -A "Expanse, a Palo Alto Networks company" https://localhost:8443/
```

### G — Inspect the logs

```bash
# Latest traffic entry from the vulnerable proxy
tail -1 logs/vuln/traffic-$(date +%F).jsonl | jq '{
  group:    .request.experiment_group,
  class:    .request.classification,
  client:   .request.client_ip,
  tls_ver:  .request.tls.version,
  ja3:      .request.tls.client_cipher_suites,
  status:   .response.status_code
}'

# Compare with hardened
tail -1 logs/hardened/traffic-$(date +%F).jsonl | jq '.request.classification'
```

Key log fields:

| Field | Description |
|---|---|
| `experiment_group` | `vuln` or `hardened` |
| `classification` | `login_attempt`, `sensitive_file_probe`, `xmlrpc_probe`, … |
| `client_ip` | Attacker's real IP (from `RemoteAddr`, not spoofable) |
| `tls.version` | Negotiated TLS version |
| `tls.client_cipher_suites` | Attacker's offered cipher list (JA3 input) |
| `tls.client_curves` | Attacker's supported curves |
| `tls.server_name` | SNI the attacker sent |
| `body_encoding` | `base64` when body is binary |
| `body_truncated` | `true` when body exceeded 1 MiB cap |

### H — Stop

```bash
docker compose down          # keep WordPress data volumes
docker compose down -v       # also wipe DB + WP volumes (full reset)
```

---

## VM deployment — proxies on host, WordPress in Docker (`compose.split.yaml`)

Use this on the VM. WordPress stays sandboxed in Docker. The proxy binaries run directly on the host so they can bind to real network interfaces before Docker's NAT layer.

```
internet
  ├─ 145.220.231.96–103  :443 ──iptables──▶ host :8443 (proxy-vuln)     ──TLS──▶ 127.0.0.1:8081 (nginx-vuln  in Docker)
  └─ 145.220.231.104–111 :443 ──iptables──▶ host :8444 (proxy-hardened) ──TLS──▶ 127.0.0.1:8082 (nginx-hardened in Docker)
```

### I — First-time setup on the VM

```bash
ssh <user>@<vpn-ip>
git clone https://github.com/<org>/tls-honeypot
cd tls-honeypot
```

### J — Generate backend cert (same as step B)

```bash
mkdir -p testdata logs/vuln logs/hardened

openssl req -x509 -newkey rsa:2048 -nodes \
  -keyout testdata/key.pem \
  -out  testdata/cert.pem \
  -days 3650 \
  -subj "/CN=honeypot-backend"
```

### K — Start the WordPress Docker stack

```bash
docker compose -f compose.split.yaml up -d
```

Verify nginx containers are up and listening on localhost:

```bash
docker compose -f compose.split.yaml ps
curl -k https://localhost:8081/   # nginx-vuln  (no proxy in front yet)
curl -k https://localhost:8082/   # nginx-hardened
```

### L — Configure the firewall and IP routing

Edit `SSH_ALLOW_FROM` in `deployments/firewall.sh` to your own IP first — otherwise you will lock yourself out.

```bash
nano deployments/firewall.sh   # set SSH_ALLOW_FROM="your.ip.here"
sudo bash deployments/firewall.sh
```

This applies two things:
1. **ufw** — deny-by-default, allow SSH (your IP only) + public port 443
2. **iptables PREROUTING REDIRECT** — steers traffic from each public IP's `:443` into the correct host proxy port

```
145.220.231.96–103  :443  →  :8443   (vuln proxy)
145.220.231.104–111 :443  →  :8444   (hardened proxy)
```

### M — Build and start the host proxies

```bash
bash deployments/proxy-start.sh
```

This compiles the proxy binary and starts both instances as background processes:

- `proxy-vuln` on `:8443` → `localhost:8081` (nginx-vuln), CN=`sys-admin.internal`
- `proxy-hardened` on `:8444` → `localhost:8082` (nginx-hardened), CN=`fge-integration-test.internal.coralset.com`

Tail the proxy logs:

```bash
tail -f logs/vuln/proxy.log
tail -f logs/hardened/proxy.log
```

### N — Verify from off-VPN

Use a phone hotspot or any machine that is **not** the VM itself.

```bash
# Each proxy presents a different certificate — attacker sees two unrelated servers
echo | openssl s_client -connect 145.220.231.96:443  2>/dev/null | openssl x509 -noout -subject
echo | openssl s_client -connect 145.220.231.104:443 2>/dev/null | openssl x509 -noout -subject

# WordPress should load through the proxy
curl -k https://145.220.231.96/
curl -k https://145.220.231.104/

# Check experiment_group tag in logs
tail -1 logs/vuln/traffic-$(date -u +%F).jsonl     | jq .request.experiment_group
tail -1 logs/hardened/traffic-$(date -u +%F).jsonl | jq .request.experiment_group
```

### O — Update the running deployment

```bash
ssh <user>@<vpn-ip>
cd tls-honeypot && git pull

# Restart WordPress containers
docker compose -f compose.split.yaml up -d

# Rebuild and restart host proxies
kill $(cat /tmp/proxy-vuln.pid /tmp/proxy-hardened.pid) 2>/dev/null || true
bash deployments/proxy-start.sh
```

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| `bind: address already in use` on port 8443/8444 | Another process or Docker container holds the port — `docker compose down` first |
| `bind: socket access permission` on Windows | Hyper-V owns the port — change `--listen` to `:18443` and update `WP_HOME` in compose.yaml |
| nginx container keeps restarting | Config syntax error or missing cert — `docker logs <container>` |
| `502 Bad Gateway` from proxy | nginx or WP not ready — wait 15 s and retry |
| iptables rules lost after reboot | `apt install -y iptables-persistent` then re-run `firewall.sh` |
| Logs dated one day off | Containers run UTC — expected |
| Both proxies show the same cert CN | Check `--cert-cn` flag is set differently per proxy instance |

---

## Project status

- [x] Transparent MitM proxy — TLS termination + re-encryption, attacker sees nothing
- [x] TLS ClientHello fingerprinting (JA3-style: cipher suites, curves, sig schemes, ALPN)
- [x] Certificate rotation — random key/serial per interval, pinned CN per proxy identity
- [x] Two-stack setup: vulnerable (WP 5.9 / PHP 7.4 EOL) vs hardened (WP 6.7 / PHP 8.3)
- [x] Network isolation — WordPress/DB on `internal: true` Docker networks
- [x] Firewall + iptables routing for 16-IP VM deployment
- [ ] Vulnerable plugin installation
- [ ] GitHub Actions CI
- [ ] Data analysis + report
