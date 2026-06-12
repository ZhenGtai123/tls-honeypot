#!/usr/bin/env bash
# Build and start both host proxies (vuln + hardened) as background processes.
# Run from the project root:  bash deployments/proxy-start.sh
#
# Logs: logs/vuln/   logs/hardened/
# PIDs: /tmp/proxy-vuln.pid   /tmp/proxy-hardened.pid
#
# Stop:  kill $(cat /tmp/proxy-vuln.pid) $(cat /tmp/proxy-hardened.pid)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$ROOT"

# ── Build ─────────────────────────────────────────────────────────────────────

echo "[proxy-start] Building proxy binary ..."
CGO_ENABLED=0 go build -trimpath -ldflags="-s -w" -o /tmp/honeypot-proxy ./src/proxy
echo "[proxy-start] Built: /tmp/honeypot-proxy"

# ── Log dirs ──────────────────────────────────────────────────────────────────

mkdir -p logs/vuln logs/hardened

# ── Start vuln proxy ──────────────────────────────────────────────────────────

if [[ -f /tmp/proxy-vuln.pid ]] && kill -0 "$(cat /tmp/proxy-vuln.pid)" 2>/dev/null; then
  echo "[proxy-start] proxy-vuln already running (PID $(cat /tmp/proxy-vuln.pid)), skipping."
else
  /tmp/honeypot-proxy \
    --listen :8443 \
    --target localhost:8081 \
    --forward-https \
    --rotate-cert-interval=24h \
    --cert-cn=sys-admin.internal \
    --experiment-group=vuln \
    --min-tls-version=1.0 \
    --log-dir="$ROOT/logs/vuln" \
    >> "$ROOT/logs/vuln/proxy.log" 2>&1 &
  echo $! > /tmp/proxy-vuln.pid
  echo "[proxy-start] proxy-vuln started (PID $!, :8443 → localhost:8081)"
fi

# ── Start hardened proxy ──────────────────────────────────────────────────────

if [[ -f /tmp/proxy-hardened.pid ]] && kill -0 "$(cat /tmp/proxy-hardened.pid)" 2>/dev/null; then
  echo "[proxy-start] proxy-hardened already running (PID $(cat /tmp/proxy-hardened.pid)), skipping."
else
  /tmp/honeypot-proxy \
    --listen :8444 \
    --target localhost:8082 \
    --forward-https \
    --rotate-cert-interval=24h \
    --cert-cn=fge-integration-test.internal.coralset.com \
    --experiment-group=hardened \
    --min-tls-version=1.2 \
    --log-dir="$ROOT/logs/hardened" \
    >> "$ROOT/logs/hardened/proxy.log" 2>&1 &
  echo $! > /tmp/proxy-hardened.pid
  echo "[proxy-start] proxy-hardened started (PID $!, :8444 → localhost:8082)"
fi

echo
echo "Proxies running. Tail logs with:"
echo "  tail -f logs/vuln/proxy.log"
echo "  tail -f logs/hardened/proxy.log"
echo
echo "Stop with:"
echo "  kill \$(cat /tmp/proxy-vuln.pid) \$(cat /tmp/proxy-hardened.pid)"
