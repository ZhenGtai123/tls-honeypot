#!/usr/bin/env bash
# Host-level firewall rules for the TLS honeypot VM, applied via ufw (a
# friendly frontend over iptables). Run with sudo on the production VM
# after you've SSH'd in and confirmed your SSH session works.
#
# Defense in depth:
#   1. Cloud provider's security group / firewall (configured in their web UI)
#   2. This ufw config — host-level
#   3. Docker's own iptables rules — managed by Docker, container scope
#
# Containment goal: a compromised honeypot can't be weaponized for spam,
# DDoS, scanning, or pivoting. Inbound is restricted to SSH (from you) and
# HTTPS (public). Outbound is restricted to the minimum we need for
# operations.
#
# IMPORTANT: edit SSH_ALLOW_FROM below to your real home IP before running,
# or you will lock yourself out and have to use the cloud console to recover.

set -euo pipefail

# === EDIT BEFORE RUNNING ===========================================
SSH_ALLOW_FROM="1.2.3.4"   # your home/static IP — CHANGE THIS
SSH_PORT=22
TLS_PORT=443
# ===================================================================

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

# Outbound: only the bare minimum
ufw allow out 53        comment "DNS"
ufw allow out 443/tcp   comment "HTTPS - apt updates, log shipping"
ufw allow out 80/tcp    comment "HTTP - apt sources"
ufw allow out 123/udp   comment "NTP - clock sync"
# Deliberately NOT allowed: SMTP (25, 465, 587), IRC (6667), Tor (9050),
# arbitrary high ports. A compromised container can't reach the broader
# internet for spam or C2.

ufw --force enable
ufw status verbose

cat <<EOM

[firewall.sh] Done. Sanity-check from another shell that you can still SSH:
  ssh user@<this-vm-ip>

If SSH no longer works, use your cloud provider's web console (out-of-band)
to disable ufw: 'sudo ufw disable'.
EOM
