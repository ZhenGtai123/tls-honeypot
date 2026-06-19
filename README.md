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

| Stack | Cert CN | WordPress | PHP | Character | Port |
|---|---|---|---|---|---|
| **Vulnerable** | `sys-admin.internal` | 5.9 | 7.4 EOL | Debug on, 512 MB uploads, no security headers | 8443 | 
| **Hardened** | `fge-integration-test.internal.coralset.com` | 6.7 | 8.3 | Debug off, 8 MB uploads, security headers | 8444 |

---

## Prerequisites

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

## Generate the nginx backend certificate

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

### Create log directories

```bash
mkdir -p logs/vuln logs/hardened
```

### Start the full stack

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

### Verify the MitM is transparent

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

### Test attacker behaviour

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

### Inspect the logs

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

###  Stop

```bash
docker compose down          # keep WordPress data volumes
docker compose down -v       # also wipe DB + WP volumes (full reset)
```

---

# VM deployment — proxies on host, WordPress in Docker (`compose.split.yaml`)

Use this on the VM. WordPress and its databases stay sandboxed in Docker. The Go proxy binaries run directly on the host to bind to the real public network interfaces before Docker's NAT layer intercepts traffic.

```
internet
  ├─ 145.220.231.96–103  :443 ──iptables──▶ host :8443 (proxy-vuln)     ──TLS──▶ 127.0.0.1:8081 (nginx-vuln  in Docker)
  └─ 145.220.231.104–111 :443 ──iptables──▶ host :8444 (proxy-hardened) ──TLS──▶ 127.0.0.1:8082 (nginx-hardened in Docker)
```

### VM prerequisites

On a fresh Ubuntu 22.04 VM, install everything needed before touching the project:

```bash
# Docker engine + Compose plugin
sudo apt update
sudo apt install -y docker.io docker-compose-plugin

# Add your user to the docker group so you don't need sudo
sudo usermod -aG docker $USER
newgrp docker

# Go 1.21+ (needed to compile the proxy on the host)
wget -q https://go.dev/dl/go1.23.0.linux-amd64.tar.gz
sudo rm -rf /usr/local/go && sudo tar -C /usr/local -xzf go1.23.0.linux-amd64.tar.gz
echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.bashrc && source ~/.bashrc
go version   # should print go1.23.x

# Firewall tools
sudo apt install -y ufw iptables-persistent openssl jq
```

### Clone the repository

```bash
ssh <user>@<vpn-ip>
git clone https://github.com/<org>/tls-honeypot
cd tls-honeypot
```

### Generate the nginx backend certificate

This cert is used for the internal proxy→nginx TLS leg (TLS B). Attackers never see it.

```bash
mkdir -p testdata logs/vuln logs/hardened

openssl req -x509 -newkey rsa:2048 -nodes \
  -keyout testdata/key.pem \
  -out    testdata/cert.pem \
  -days   3650 \
  -subj   "/CN=honeypot-backend"
```

> Do **not** commit `testdata/key.pem` — it is in `.gitignore`. The public `cert.pem` can be committed.

### Start the WordPress Docker stack

```bash
docker compose -f compose.split.yaml up -d
```

Wait ~20 seconds for MySQL and WordPress to finish initialising, then check every container is `Up` with no `Restarting`:

```bash
docker compose -f compose.split.yaml ps
```

Expected output:

```
NAME                     IMAGE                         STATUS
...-db-hardened-1        mysql:8.4                     Up X seconds
...-db-vuln-1            mysql:8.0                     Up X seconds
...-nginx-hardened-1     nginx:latest                  Up X seconds
...-nginx-vuln-1         nginx:latest                  Up X seconds
...-wp-hardened-1        wordpress:6.7-php8.3-apache   Up X seconds
...-wp-vuln-1            wordpress:5.9-php7.4-apache   Up X seconds
```

Smoke-test the nginx containers directly (proxies not started yet):

```bash
curl -sk -o /dev/null -w "%{http_code}\n" https://localhost:8081/   # expect 200 or 302
curl -sk -o /dev/null -w "%{http_code}\n" https://localhost:8082/   # expect 200 or 302
```

If either nginx container keeps restarting, check:

```bash
docker logs <container-name>
```

### Configure the firewall and IP routing

```bash
sudo bash deployments/firewall.sh
```

What it does:
1. **ufw** — default deny, allow SSH from any IP (key-based auth), allow public port 443
2. **iptables PREROUTING REDIRECT** — steers each IP range's port 443 to the correct proxy port on the host:

```
145.220.231.96–103  :443  →  :8443   (vuln proxy)
145.220.231.104–111 :443  →  :8444   (hardened proxy)
```

Rules survive reboots because `iptables-persistent` saves them automatically.

Verify the rules are in place:

```bash
sudo iptables -t nat -L PREROUTING -n --line-numbers
```

### Build and start the host proxies

```bash
bash deployments/proxy-start.sh
```

This compiles the Go proxy binary and starts both instances as background daemons:

| Proxy | Listens | Forwards to | Certificate CN |
|---|---|---|---|
| `proxy-vuln` | `:8443` | `localhost:8081` | `sys-admin.internal` |
| `proxy-hardened` | `:8444` | `localhost:8082` | `fge-integration-test.internal.coralset.com` |

PIDs are written to `/tmp/proxy-vuln.pid` and `/tmp/proxy-hardened.pid`.

Confirm both are running:

```bash
ps aux | grep honeypot-proxy
tail -20 logs/vuln/proxy.log
tail -20 logs/hardened/proxy.log
```

### Verify end-to-end from off-VPN

Use a phone hotspot or any machine that is **not** the VM (on-VM curl bypasses the iptables redirect):

```bash
# Each proxy must show a different certificate CN
echo | openssl s_client -connect 145.220.231.96:443  2>/dev/null | openssl x509 -noout -subject
# expected: subject=CN=sys-admin.internal

echo | openssl s_client -connect 145.220.231.104:443 2>/dev/null | openssl x509 -noout -subject
# expected: subject=CN=fge-integration-test.internal.coralset.com

# WordPress must load through both paths
curl -k -o /dev/null -w "%{http_code}\n" https://145.220.231.96/
curl -k -o /dev/null -w "%{http_code}\n" https://145.220.231.104/

# Confirm traffic is being logged
tail -1 logs/vuln/traffic-$(date -u +%F).jsonl     | jq '{group: .request.experiment_group, ip: .request.client_ip}'
tail -1 logs/hardened/traffic-$(date -u +%F).jsonl | jq '{group: .request.experiment_group, ip: .request.client_ip}'
```

### Tuning rate limits

Rate limits live in `compose.split.yaml` under each nginx service and take effect after a container restart — no image rebuild needed:

```yaml
nginx-vuln:
  environment:
    NGINX_RATE_LIMIT: "30r/s"   # sustained requests/sec per client IP
    NGINX_RATE_BURST: "60"      # burst queue depth before HTTP 429

nginx-hardened:
  environment:
    NGINX_RATE_LIMIT: "10r/s"
    NGINX_RATE_BURST: "20"
```

| Variable | Description |
|---|---|
| `NGINX_RATE_LIMIT` | Token refill rate — how many requests/sec each IP is allowed to sustain |
| `NGINX_RATE_BURST` | Queue depth — excess requests are held here before being rejected with 429 |

Apply without touching the WordPress or DB containers:

```bash
# Edit compose.split.yaml, then:
docker compose -f compose.split.yaml up -d --no-deps nginx-vuln
docker compose -f compose.split.yaml up -d --no-deps nginx-hardened
```

### Container hardening reference

All six containers in `compose.split.yaml` are hardened assuming an attacker achieves code execution inside one:

| Measure | Applied to | What it prevents |
|---|---|---|
| `cap_drop: ALL` + minimum `cap_add` | all | Removes all Linux capabilities; only the minimum are re-granted (e.g. `NET_BIND_SERVICE`+`CHOWN` for nginx, `SETUID`/`DAC_OVERRIDE`/`FOWNER` for Apache and MySQL) |
| `security_opt: no-new-privileges:true` | all | Blocks privilege escalation via setuid-bit executables inside the container |
| `deploy.resources.limits.pids` | all | Caps total processes — prevents fork-bomb DoS from inside a compromised container |
| `deploy.resources.limits` (memory + CPU) | all | Prevents one container from exhausting VM resources |
| `read_only: true` + tmpfs | nginx only | Root FS is read-only; only `/tmp`, `/var/cache/nginx`, `/var/run`, `/etc/nginx/conf.d` are writable in-memory mounts |

The primary containment is the `internal: true` Docker networks — even with a full shell inside a container there is no outbound internet route. The measures above add depth-in-defence.

### Updating a running deployment

```bash
ssh <user>@<vpn-ip>
cd tls-honeypot && git pull

# Restart WordPress + nginx containers (picks up compose changes)
docker compose -f compose.split.yaml up -d

# Rebuild and restart host proxies (picks up proxy source changes)
kill $(cat /tmp/proxy-vuln.pid /tmp/proxy-hardened.pid) 2>/dev/null || true
bash deployments/proxy-start.sh
```

To restart only one service without touching the others:

```bash
docker compose -f compose.split.yaml up -d --no-deps <service-name>
# e.g.: nginx-vuln, wp-hardened, db-vuln ...
```

### Stopping the deployment

```bash
# Stop host proxies
kill $(cat /tmp/proxy-vuln.pid /tmp/proxy-hardened.pid) 2>/dev/null || true

# Stop Docker stack (keeps data volumes)
docker compose -f compose.split.yaml down

# Full reset — also wipes DB and WordPress data volumes
docker compose -f compose.split.yaml down -v
```

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| `bind: address already in use` on port 8443/8444 | Another process or Docker container holds the port — `docker compose down` first |
| `bind: socket access permission` on Windows | Hyper-V owns the port — change `--listen` to `:18443` and update `WP_HOME` in compose.yaml |
| SSH locked out after running `firewall.sh` | Should not happen — SSH is open to all IPs. If ufw was pre-configured differently, use the cloud console to run `sudo ufw allow ssh` |
| nginx container keeps restarting | Check `docker logs <container>` — most likely a missing cert (`testdata/`) or a tmpfs/cap issue |
| nginx logs `chown ... Operation not permitted` | `CHOWN` cap is missing from nginx `cap_add` — verify `compose.split.yaml` has `CHOWN` listed |
| `502 Bad Gateway` from proxy | nginx or WP not ready — wait 20 s and retry; check `docker compose -f compose.split.yaml ps` |
| Clients get HTTP 429 unexpectedly | Rate limit too tight — raise `NGINX_RATE_BURST` in `compose.split.yaml` and restart nginx |
| iptables rules lost after reboot | Run `sudo netfilter-persistent save` or `apt install -y iptables-persistent` then re-run `firewall.sh` |
| Proxies not receiving traffic after reboot | iptables PREROUTING rules are gone — re-run `sudo bash deployments/firewall.sh` |
| Logs dated one day off | Containers run UTC — expected |
| Both proxies show the same cert CN | Check `--cert-cn` flag is set differently in `proxy-start.sh` per proxy instance |
| `WP_DEBUG already defined` PHP warning | Pre-existing: `wp-config.php` defines it before `WORDPRESS_CONFIG_EXTRA` is injected — harmless on the vuln stack, doesn't affect logging |

---

## Project status

- [x] Transparent MitM proxy — TLS termination + re-encryption, attacker sees nothing
- [x] TLS ClientHello fingerprinting (JA3-style: cipher suites, curves, sig schemes, ALPN)
- [x] Certificate rotation — random key/serial per interval, pinned CN per proxy identity
- [x] Two-stack setup: vulnerable (WP 5.9 / PHP 7.4 EOL) vs hardened (WP 6.7 / PHP 8.3)
- [x] Network isolation — WordPress/DB on `internal: true` Docker networks
- [x] Container hardening — `cap_drop`, `no-new-privileges`, `pids_limit`, resource limits, read-only nginx filesystem
- [x] Rate limiting — per-IP `limit_req` in nginx, configurable via env vars in `compose.split.yaml`
- [x] Firewall + iptables routing for 16-IP VM deployment
- [X] Vulnerable plugin installation
- [X] Data analysis + report
