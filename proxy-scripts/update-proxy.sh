#!/bin/bash
set -e

echo "🔄 Updating and restarting honeypot proxy"
echo "=========================================="

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check if Go file exists
if [ ! -f "honeypot-proxy.go" ]; then
    echo -e "${RED}Error: honeypot-proxy.go not found!${NC}"
    exit 1
fi

echo -e "${YELLOW}Stopping service...${NC}"
sudo systemctl stop honeypot-proxy

echo -e "${YELLOW}Backing up old binary...${NC}"
if [ -f /opt/honeypot-proxy/bin/honeypot-proxy ]; then
    sudo cp /opt/honeypot-proxy/bin/honeypot-proxy /opt/honeypot-proxy/bin/honeypot-proxy.bak
fi

echo -e "${YELLOW}Building new binary...${NC}"
go build -o honeypot-proxy honeypot-proxy.go
sudo mv honeypot-proxy /opt/honeypot-proxy/bin/
sudo chmod 755 /opt/honeypot-proxy/bin/honeypot-proxy

echo -e "${YELLOW}Starting service...${NC}"
sudo systemctl start honeypot-proxy

sleep 2
if sudo systemctl is-active --quiet honeypot-proxy; then
    echo -e "${GREEN}✓ Service restarted successfully${NC}"
    echo ""
    echo "Recent logs:"
    sudo journalctl -u honeypot-proxy -n 10 --no-pager
else
    echo -e "${RED}✗ Service failed to start. Rolling back...${NC}"
    if [ -f /opt/honeypot-proxy/bin/honeypot-proxy.bak ]; then
        sudo mv /opt/honeypot-proxy/bin/honeypot-proxy.bak /opt/honeypot-proxy/bin/honeypot-proxy
        sudo systemctl start honeypot-proxy
        echo -e "${YELLOW}Rollback complete${NC}"
    fi
    exit 1
fi
