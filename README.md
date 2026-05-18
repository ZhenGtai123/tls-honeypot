# TLS MitM Honeypot

TU Delft Hacking Lab — Project #12.

## Goal

Set up a TLS proxy between a client and a target service. The proxy terminates TLS, decrypts the traffic, logs it, and forwards plaintext to a backend honeypot — so we can observe what attackers do over otherwise-encrypted channels.

## Architecture

Two Go programs, separate binaries, talking over the network:

```
attacker ──TLS──▶  proxy  ──plaintext──▶  honeypot
                  :8443                    :8080
              (terminates TLS,           (fake admin login,
               logs traffic)              logs requests)
```

- **`src/proxy/`** — TLS-terminating reverse proxy. Loads a cert, accepts HTTPS, logs request/response JSON to `./logs/`, forwards over plaintext HTTP to the honeypot.
- **`src/honeypot/`** — Fake HTTP service that returns a believable admin login page and logs every request as JSON lines.

## Stack

- Go 1.23+

## References

- https://github.com/Nirusu/how-to-setup-a-honeypot
- https://www.mitmproxy.org/

## Responsible Professor

Harm Griffioen

## Local development

No VM or Docker needed. Both binaries run on your laptop in two terminals.

### One-time setup: generate a self-signed dev cert

```
mkdir -p testdata
openssl req -x509 -newkey rsa:2048 -nodes \
  -keyout testdata/key.pem -out testdata/cert.pem \
  -days 365 -subj "/CN=localhost"
```

Cert files are gitignored (see `.gitignore` — anything matching `*.pem`, `*.key`, `*.crt`).

### Run both binaries

Three terminals:

```
# Terminal 1 — honeypot (plain HTTP on :8080)
go run ./src/honeypot

# Terminal 2 — proxy (TLS on :8443, forwards to honeypot)
go run ./src/proxy

# Terminal 3 — test it
curl -k https://localhost:8443/admin
```

What you should see:

- `curl` returns the fake admin login HTML.
- The honeypot prints a JSON log line to stdout describing the request (method, path, headers, source IP).
- The proxy writes `./logs/requests-YYYY-MM-DD.jsonl` and `./logs/traffic-YYYY-MM-DD.jsonl`.

### Flags

Both binaries accept `--help` for the full list.

| Flag | Proxy default | Honeypot default | Notes |
|---|---|---|---|
| `--listen` | `:8443` | `:8080` | Use `:443` for proxy in production |
| `--target` | `localhost:8080` | — | Proxy upstream |
| `--cert` / `--key` | `testdata/cert.pem` / `testdata/key.pem` | — | TLS material for proxy |
| `--log-dir` | `./logs` | — | Where proxy writes JSON logs |
| `--log-file` | — | (stdout) | Honeypot log destination |

## Deploy locally with Docker

Same setup we'll run on the professor's VM later — practice it locally first.

```
# One-time: generate the dev cert if you haven't already (see above)

docker compose build         # build proxy + honeypot images
docker compose up -d         # start both, detached
curl -k https://localhost:8443/admin

# View logs
docker compose logs honeypot          # honeypot JSON logs (stdout)
cat logs/traffic-$(date +%F).jsonl    # proxy traffic log on the host

docker compose down          # tear down
```

What this gets you:

- **Proxy** at host `:8443` (forwards to container `honeypot:8080` on the internal `honeynet` bridge network)
- **Honeypot** at internal `:8080` only — not reachable from the host or the internet
- **Cert files** mounted read-only from `./testdata/` into the proxy
- **Proxy logs** persist on the host in `./logs/` (gitignored)
- **Restart policy** `unless-stopped` so containers come back after reboot

When deploying to a real VM later, the only change is in `compose.yaml`: switch `"8443:8443"` to `"443:8443"` so the proxy is exposed on the standard HTTPS port. Everything else stays the same.

## Project status

- [x] Initial scaffold (`go.mod`, `.gitignore`, README)
- [x] Proxy: TLS termination + reverse proxy + JSON request/response logs *(QS832 on `vibe-coded`)*
- [x] Honeypot: fake admin login + JSON request logs
- [x] TLS handshake metadata in proxy logs (SNI, ALPN, cipher, TLS version)
- [x] Dockerfiles + `compose.yaml` for local deployment
- [ ] More fake endpoints (`/wp-login.php`, `/.env`, `/phpmyadmin/`, etc.)
- [ ] GitHub Actions CI (`go build`, `go vet`, `go test`)
- [ ] `docs/architecture.md` capturing design decisions
- [ ] Deployment to a public VM
- [ ] Log shipping pipeline
- [ ] Data analysis + project report
