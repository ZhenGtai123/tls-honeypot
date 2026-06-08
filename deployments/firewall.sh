#!/usr/bin/env bash
# Host firewall + port routing for the honeypot VM.  Run with sudo.
#
# What this script does:
#   1. ufw deny-by-default, allow SSH (your IP only), allow public :443.
#   2. iptables REDIRECT: steers traffic from each public IP's :443 into the
#      correct host-side proxy port (8443 for vuln, 8444 for hardened).
#      The proxies listen on 0.0.0.0:8443 / 0.0.0.0:8444 — they are not
#      exposed externally (ufw blocks direct access to those ports).
#
# EDIT SSH_ALLOW_FROM below before running or you will lock yourself out.

set -euo pipefail

SSH_ALLOW_FROM="1.2.3.4"   # your static/home IP — CHANGE THIS
SSH_PORT=22
TLS_PORT=443

VULN_IPS=(
  145.220.231.96  145.220.231.97  145.220.231.98  145.220.231.99
  145.220.231.100 145.220.231.101 145.220.231.102 145.220.231.103
)
HARDENED_IPS=(
  145.220.231.104 145.220.231.105 145.220.231.106 145.220.231.107
  145.220.231.108 145.220.231.109 145.220.231.110 145.220.231.111
)
PROXY_VULN_PORT=8443
PROXY_HARDENED_PORT=8444

# ── Pre-flight checks ────────────────────────────────────────────────────────

if [[ $EUID -ne 0 ]]; then
  echo "Run as root (sudo bash deployments/firewall.sh)" >&2
  exit 1
fi

if [[ "$SSH_ALLOW_FROM" == "1.2.3.4" ]]; then
  echo "ERROR: edit SSH_ALLOW_FROM in this script to your real IP first." >&2
  echo "       Otherwise you will lock yourself out." >&2
  exit 1
fi

command -v ufw      >/dev/null || { echo "ufw not installed: apt install -y ufw"      >&2; exit 1; }
command -v iptables >/dev/null || { echo "iptables not found"                         >&2; exit 1; }

# ── ufw: inbound/outbound policy ────────────────────────────────────────────

echo "[firewall.sh] Resetting ufw rules ..."
ufw --force reset

ufw default deny incoming
ufw default deny outgoing

# Inbound: SSH (you only) + HTTPS (what attackers reach; iptables routes it below)
ufw allow from "$SSH_ALLOW_FROM" to any port "$SSH_PORT" proto tcp comment "ssh from home"
ufw allow "$TLS_PORT"/tcp                                             comment "public TLS"

# Outbound: bare minimum — deliberately NOT allowing SMTP/IRC so a compromised
# WordPress (sandboxed in Docker) cannot be weaponised even if Docker bypasses ufw.
ufw allow out 53      comment "DNS"
ufw allow out 443/tcp comment "HTTPS - apt/updates"
ufw allow out 80/tcp  comment "HTTP  - apt"
ufw allow out 123/udp comment "NTP"

ufw --force enable
ufw status verbose

# ── iptables: steer :443 traffic into the correct proxy port ─────────────────
# REDIRECT rewrites the destination port on packets arriving at the host.
# The proxy running on 0.0.0.0:PROXY_PORT picks them up.
# ufw does not manage the nat table, so we add these rules directly.

echo "[firewall.sh] Installing iptables REDIRECT rules ..."

# Flush only the PREROUTING chain in nat so we start clean.
iptables -t nat -F PREROUTING

for ip in "${VULN_IPS[@]}"; do
  iptables -t nat -A PREROUTING \
    -d "$ip" -p tcp --dport "$TLS_PORT" \
    -j REDIRECT --to-port "$PROXY_VULN_PORT"
  echo "  $ip:$TLS_PORT  →  :$PROXY_VULN_PORT (vuln)"
done

for ip in "${HARDENED_IPS[@]}"; do
  iptables -t nat -A PREROUTING \
    -d "$ip" -p tcp --dport "$TLS_PORT" \
    -j REDIRECT --to-port "$PROXY_HARDENED_PORT"
  echo "  $ip:$TLS_PORT  →  :$PROXY_HARDENED_PORT (hardened)"
done

# Persist across reboots (requires iptables-persistent).
if command -v netfilter-persistent >/dev/null 2>&1; then
  netfilter-persistent save
  echo "[firewall.sh] iptables rules saved (netfilter-persistent)."
else
  echo "[firewall.sh] WARNING: netfilter-persistent not installed."
  echo "             Rules will be lost on reboot."
  echo "             Install with: apt install -y iptables-persistent"
fi

echo
echo "Done. Sanity-check SSH from another shell before closing this one."
echo "If locked out, use your cloud console to run: sudo ufw disable"
