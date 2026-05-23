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

One-time, generate a dev cert:

```bash
openssl req -x509 -newkey rsa:2048 -nodes \
  -keyout testdata/key.pem -out testdata/cert.pem \
  -days 365 -subj "/CN=localhost"
```

Then with Docker:

```bash
docker compose up -d
curl -k https://localhost:8443/admin
docker compose down
```

Or natively (no Docker, faster iteration):

```bash
# terminal 1
go run ./src/honeypot
# terminal 2
go run ./src/proxy
# terminal 3
curl -k https://localhost:8443/admin
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

Notable fields: `tls.{version,cipher_suite,server_name,negotiated_protocol}` for handshake metadata, `body_encoding="base64"` when the body isn't valid UTF-8, `body_truncated=true` when it exceeded the size cap. The Go structs in `src/proxy/main.go` and `src/honeypot/main.go` are the authoritative schema.

## Deploy to a VM

When the professor gives you one:

```bash
# On the VM:
ssh user@<vm-ip>
sudo apt install -y docker.io docker-compose-plugin ufw git
git clone https://github.com/ZhenGtai123/tls-honeypot.git
cd tls-honeypot && git checkout main

# Generate a cert (or set up Let's Encrypt for a real domain)
mkdir -p testdata && openssl req -x509 -newkey rsa:2048 -nodes \
  -keyout testdata/key.pem -out testdata/cert.pem \
  -days 365 -subj "/CN=$(hostname -f)"

# Publish on :443 instead of :8443
sed -i 's/"8443:8443"/"443:8443"/' compose.yaml

# Lock down the host — edit SSH_ALLOW_FROM in the script first, then:
sudo bash deployments/firewall.sh

# Bring it up
docker compose up -d
```

Verify from outside (your phone hotspot, *not* the VM):

```bash
curl -k https://<vm-public-ip>/admin
```

You should get the fake login HTML, and the request lands in `logs/traffic-*.jsonl` on the VM within seconds.

To update after merges: `git pull && docker compose up -d`.

## Flags

`go run ./src/proxy --help` and `go run ./src/honeypot --help`. Most useful:

| | Proxy | Honeypot |
|---|---|---|
| `--listen` | `:8443` (use `:443` in prod) | `:8080` |
| `--target` | `localhost:8080` | — |
| `--cert` / `--key` | `testdata/cert.pem` / `testdata/key.pem` | — |
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
