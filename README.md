# TLS MitM Honeypot

TU Delft Hacking Lab — Project #12. A TLS proxy that decrypts attacker traffic and forwards it to a fake HTTP service we control.

**Responsible professor:** Harm Griffioen
**References:** [Nirusu/how-to-setup-a-honeypot](https://github.com/Nirusu/how-to-setup-a-honeypot), [mitmproxy.org](https://www.mitmproxy.org/)

## How it works

```
attacker ──TLS──▶  proxy  ──plaintext──▶  honeypot
                  :8443                    :8080
```

- **`src/proxy/`** — terminates TLS, logs each request + response (including TLS handshake metadata) to `./logs/`, forwards plaintext.
- **`src/honeypot/`** — fake admin login page; logs every request as JSON to stdout.

## Run it locally

With Docker (cert rotation generates the cert automatically — no openssl needed):

```bash
docker compose up -d
curl -k https://localhost:8443/admin
docker compose down
```

Or natively (no Docker, faster iteration). You can use cert rotation here too:

```bash
# terminal 1
go run ./src/honeypot
# terminal 2
go run ./src/proxy --rotate-cert-interval=24h
# terminal 3
curl -k https://localhost:8443/admin
```

If you prefer a static cert for local testing, generate one first:

```bash
openssl req -x509 -newkey rsa:2048 -nodes \
  -keyout testdata/key.pem -out testdata/cert.pem \
  -days 365 -subj "/CN=localhost"
# then run without --rotate-cert-interval
go run ./src/proxy
```

> Windows gotcha: if `:8443` fails to bind, it's reserved by Hyper-V. Run `go run ./src/proxy --listen :18443` and `curl ... :18443/...`.

## Test it

A few representative probes:

```bash
URL=https://localhost:8443
curl -ksS -A "CensysInspect/1.1" $URL/                                # scanner UA
curl -ksS $URL/.env                                                   # config-leak probe
curl -ksS -X POST -d "log=admin&pwd=hunter2" $URL/wp-login.php        # credential stuffing
printf 'binary\xff\xfe\x80data' | curl -ksS $URL/upload -X POST --data-binary @-   # binary body
```

Then inspect:

```bash
docker compose logs honeypot | tail -5            # honeypot JSON
tail -5 logs/traffic-$(date +%F).jsonl            # proxy: full request + response
```

Each day `./logs/` gets three files:
- `requests-YYYY-MM-DD.jsonl` — proxy, request only
- `traffic-YYYY-MM-DD.jsonl` — proxy, request + response (including 502s and other proxy errors)
- `honeypot-YYYY-MM-DD.jsonl` — honeypot view of the same requests (also echoed to stdout)

Notable fields: `tls.{version,cipher_suite,server_name,negotiated_protocol}` for the negotiated handshake, `tls.client_*` (cipher suites, curves, sig schemes, ALPN, versions) for the client's ClientHello offer — a JA3-style fingerprint for identifying scanning tools; `client_ip` is the authoritative peer while the spoofable `forwarded_for` holds any attacker `X-Forwarded-For`; `experiment_group` tags vuln vs hardened; `body_encoding="base64"` when the body isn't valid UTF-8, `body_truncated=true` when it exceeded the cap. The Go structs in `src/proxy/main.go` and `src/honeypot/main.go` are the authoritative schema.

## Deploy the experiment to the VM

Two WordPress variants — vulnerable vs hardened — each behind its own TLS-logging proxy bound to 8 of the VM's 16 public IPs. Each proxy tags its traffic `experiment_group=vuln|hardened`. Inbound is locked to `:443` upstream; the WordPress/DB containers run on `internal` networks with no outbound route, so a compromised vulnerable WordPress can't attack third parties.

```
attacker ──TLS──▶ proxy(:443) ──TLS──▶ nginx ──HTTP──▶ wordpress ──▶ db
                  .96–.103 → vuln stack   /   .104–.111 → hardened stack
```

```bash
ssh hackinglab-...@<vpn-ip>          # SSH only over the VPN
cd tls-honeypot && git pull
mkdir -p logs/vuln logs/hardened
docker compose -f compose.split.yaml up -d --build
```

Verify from off-VPN (phone hotspot, *not* the VM):

```bash
curl -k https://145.220.231.96/                       # a vuln IP
curl -k https://145.220.231.104/                      # a hardened IP
tail -1 logs/vuln/traffic-$(date -u +%F).jsonl        # check experiment_group + client_cipher_suites
```

`compose.split.yaml` only runs on the VM (the per-IP bindings need those addresses on the host). For local single-stack dev, use `docker compose up -d` (`compose.yaml`) instead.

## Flags

`go run ./src/proxy --help` and `go run ./src/honeypot --help`. Most useful:

| | Proxy | Honeypot |
|---|---|---|
| `--listen` | `:8443` (use `:443` in prod) | `:8080` |
| `--target` | `localhost:8080` | — |
| `--cert` / `--key` | `testdata/cert.pem` / `testdata/key.pem` (ignored when rotating) | — |
| `--rotate-cert-interval` | `0` (disabled; use `24h` in prod) | — |
| `--experiment-group` | `default` (set `vuln`/`hardened`, one proxy per group) | — |
| `--log-dir` | `./logs` | `./logs` |
| `--log-file` | — | (overrides `--log-dir` with a single file) |
| `--quiet` | — | suppress stdout request logs |

## Troubleshooting

- **`bind: socket access permission`** on Windows → use `--listen :18443` (Hyper-V holds `:8443`).
- **Docker errors about `dockerDesktopLinuxEngine` pipe** → Docker Desktop is stopped; restart it.
- **`openssl: Can't open openssl.cnf`** (Miniconda Windows) → `$env:OPENSSL_CONF = "C:\Program Files\Git\usr\ssl\openssl.cnf"` first.
- **Log filenames dated wrong** → containers run in UTC; expected.

## Project status

- [x] Proxy + honeypot end-to-end (TLS termination, JSON logs, TLS handshake metadata, base64 fallback for non-UTF-8 bodies, error responses logged)
- [x] Docker compose stack with firewall script
- [ ] More fake endpoints (per-app responses, not one generic login)
- [ ] GitHub Actions CI
- [ ] `docs/architecture.md`
- [ ] Real-VM deployment + log shipping
- [ ] Data analysis + project report
