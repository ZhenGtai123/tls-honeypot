#!/bin/bash
set -e

echo "🔧 Complete Honeypot Proxy Setup"
echo "================================="

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Check if running as root - we need sudo for many commands
if [ "$EUID" -eq 0 ]; then 
    echo -e "${RED}Please don't run as root directly. Run as normal user with sudo in the script.${NC}"
    exit 1
fi

step_skip() {
    echo -e "${YELLOW}→${NC} $1"
}

echo -e "${BLUE}Step 1: Creating directory structure...${NC}"
sudo mkdir -p /opt/honeypot-proxy/{bin,certs,data}
sudo mkdir -p /var/log/honeypot-proxy
sudo mkdir -p /etc/honeypot-proxy
sudo mkdir -p /var/log/suricata
sudo mkdir -p /var/log/captures

if [ ! -L /opt/honeypot-proxy/logs ]; then
    sudo ln -sf /var/log/honeypot-proxy /opt/honeypot-proxy/logs
    step_skip "Created symlink"
fi

echo -e "${BLUE}Step 2: Creating system user...${NC}"
if ! id -u honeypot-proxy &>/dev/null; then
    sudo useradd -r -s /bin/false honeypot-proxy
    step_skip "Created user"
fi

echo -e "${BLUE}Step 3: Setting permissions...${NC}"
sudo chown -R root:root /opt/honeypot-proxy
sudo chown -R honeypot-proxy:honeypot-proxy /var/log/honeypot-proxy
sudo chmod 755 /opt/honeypot-proxy
sudo mkdir -p /opt/honeypot-proxy/{bin,certs,data}
sudo chmod 755 /opt/honeypot-proxy/bin
sudo chmod 755 /opt/honeypot-proxy/certs
sudo chmod 755 /opt/honeypot-proxy/data
sudo chmod 755 /var/log/honeypot-proxy

echo -e "${BLUE}Step 4: Generating certificates...${NC}"
# Generate certificates directly in /opt/honeypot-proxy/certs/
sudo bash -c 'cd /opt/honeypot-proxy/certs/ && \
    openssl genrsa -out server.key 2048 && \
    cat > san.conf <<EOF
[req]
distinguished_name = req_distinguished_name
req_extensions = v3_req
prompt = no

[req_distinguished_name]
CN = 192.168.100.20
O = HoneypotProxy
C = US

[v3_req]
keyUsage = keyEncipherment, dataEncipherment
extendedKeyUsage = serverAuth
subjectAltName = @alt_names

[alt_names]
IP.1 = 192.168.100.20
IP.2 = 127.0.0.1
DNS.1 = honeypot-proxy.local
EOF
    openssl req -new -x509 -days 365 -key server.key -out server.crt \
      -config san.conf -extensions v3_req && \
    chmod 600 server.key && \
    chmod 644 server.crt && \
    rm -f san.conf'

step_skip "Generated fresh certificates"

echo -e "${BLUE}Step 5: Stopping any running proxy process...${NC}"
sudo pkill -f honeypot-proxy 2>/dev/null || true
sudo systemctl stop honeypot-proxy 2>/dev/null || true

echo -e "${BLUE}Step 6: Building Go binary...${NC}"
if [ ! -f "honeypot-proxy.go" ]; then
    echo -e "${RED}Error: honeypot-proxy.go not found in current directory!${NC}"
    exit 1
fi

# Build fresh
go build -o honeypot-proxy honeypot-proxy.go
sudo mv honeypot-proxy /opt/honeypot-proxy/bin/
sudo chmod 755 /opt/honeypot-proxy/bin/honeypot-proxy
echo -e "${GREEN}✓${NC} Binary built and installed"

# Test binary
if sudo /opt/honeypot-proxy/bin/honeypot-proxy -h &>/dev/null; then
    echo -e "${GREEN}✓${NC} Binary works correctly"
else
    echo -e "${RED}✗ Binary test failed${NC}"
    exit 1
fi

echo -e "${BLUE}Step 7: Creating systemd service (running as root)...${NC}"
sudo tee /etc/systemd/system/honeypot-proxy.service > /dev/null <<'EOF'
[Unit]
Description=Honeypot HTTPS Proxy
After=network.target

[Service]
Type=simple
User=root
Group=root
WorkingDirectory=/opt/honeypot-proxy

ExecStart=/opt/honeypot-proxy/bin/honeypot-proxy -listen="192.168.100.20:443" -target="192.168.100.10:80" -cert="/opt/honeypot-proxy/certs/server.crt" -key="/opt/honeypot-proxy/certs/server.key" -log-dir="/var/log/honeypot-proxy" -verbose

Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
echo -e "${GREEN}✓${NC} Service created"

echo -e "${BLUE}Step 8: Setting up logrotate...${NC}"
sudo tee /etc/logrotate.d/honeypot-proxy > /dev/null <<EOF
/var/log/honeypot-proxy/*.jsonl {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
    create 0640 root root
}
EOF

echo -e "${BLUE}Step 9: Starting service...${NC}"
sudo systemctl start honeypot-proxy
sudo systemctl enable honeypot-proxy

echo -e "${BLUE}Step 10: Checking service status...${NC}"
sleep 2
if sudo systemctl is-active --quiet honeypot-proxy; then
    echo -e "${GREEN}✓ Service is running${NC}"
    sudo systemctl status honeypot-proxy --no-pager
else
    echo -e "${RED}✗ Service failed to start${NC}"
    sudo journalctl -u honeypot-proxy -n 20 --no-pager
    exit 1
fi

echo -e "\n${GREEN}✅ Setup Complete!${NC}"
echo "========================================="
echo -e "${BLUE}Proxy is running:${NC}"
echo "  HTTPS → Proxy (192.168.100.20:443) → Honeypot (192.168.100.10:80)"
echo ""
echo -e "${BLUE}Useful commands:${NC}"
echo "  View service logs:  sudo journalctl -u honeypot-proxy -f"
echo "  View proxy logs:    tail -f /var/log/honeypot-proxy/traffic-*.jsonl | jq '.'"
echo "  Restart proxy:      sudo systemctl restart honeypot-proxy"
echo "  Stop proxy:         sudo systemctl stop honeypot-proxy"
echo ""
echo -e "${BLUE}Test the proxy:${NC}"
echo "  curl -k https://192.168.100.20/wordpress"
