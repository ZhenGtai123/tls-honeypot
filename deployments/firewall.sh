#!/usr/bin/env bash
# Host firewall for the honeypot VM. Run with sudo on the VM.
# Deny-by-default inbound and outbound; only SSH (from you), public 443,
# and essential outbound (DNS, HTTP/S, NTP) are allowed.
# EDIT SSH_ALLOW_FROM below before running or you'll lock yourself out.

set -euo pipefail

SSH_ALLOW_FROM="1.2.3.4"   # your home/static IP — CHANGE THIS
SSH_PORT=22
TLS_PORT=443

if [[ $EUID -ne 0 ]]; then
  echo "Run as root (sudo bash deployments/firewall.sh)" >&2
  exit 1
fi

if [[ "$SSH_ALLOW_FROM" == "1.2.3.4" ]]; then
  echo "ERROR: edit SSH_ALLOW_FROM in this script to your real IP first." >&2
  echo "       Otherwise you will lock yourself out." >&2
  exit 1
fi

command -v ufw >/dev/null || { echo "ufw not installed: apt install -y ufw" >&2; exit 1; }

echo "[firewall.sh] Resetting ufw rules ..."
ufw --force reset

# Defaults
ufw default deny incoming
ufw default deny outgoing

# Inbound: SSH (you only) + HTTPS (public, what attackers reach)
ufw allow from "$SSH_ALLOW_FROM" to any port "$SSH_PORT" proto tcp comment "ssh from home"
ufw allow "$TLS_PORT"/tcp comment "public TLS - the proxy"

# Outbound: bare minimum. Deliberately NOT allowing SMTP/IRC/etc. so a
# compromised honeypot can't be weaponized.
ufw allow out 53        comment "DNS"
ufw allow out 443/tcp   comment "HTTPS - apt, log shipping"
ufw allow out 80/tcp    comment "HTTP - apt"
ufw allow out 123/udp   comment "NTP"

ufw --force enable
ufw status verbose

echo
echo "Done. Sanity-check SSH from another shell before closing this one."
echo "If locked out, use your cloud console to run: sudo ufw disable"
