#!/bin/bash
set -e

echo "⚠️  COMPLETE RESET SCRIPT"
echo "========================"
echo -e "\n${RED}This will remove ALL honeypot proxy files, logs, and configurations.${NC}"
echo -e "${YELLOW}Are you sure? Type 'yes' to continue:${NC}"
read -r confirmation

if [ "$confirmation" != "yes" ]; then
    echo "Aborted."
    exit 0
fi

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}Stopping services...${NC}"
sudo systemctl stop honeypot-proxy 2>/dev/null || true
sudo systemctl disable honeypot-proxy 2>/dev/null || true

echo -e "${YELLOW}Removing systemd service...${NC}"
sudo rm -f /etc/systemd/system/honeypot-proxy.service
sudo systemctl daemon-reload

echo -e "${YELLOW}Killing any running proxy processes...${NC}"
sudo pkill -f honeypot-proxy 2>/dev/null || true

echo -e "${YELLOW}Removing application files...${NC}"
sudo rm -rf /opt/honeypot-proxy

echo -e "${YELLOW}Removing log files...${NC}"
sudo rm -rf /var/log/honeypot-proxy

echo -e "${YELLOW}Removing configuration...${NC}"
sudo rm -rf /etc/honeypot-proxy
sudo rm -f /etc/logrotate.d/honeypot-proxy

echo -e "${YELLOW}Removing user...${NC}"
sudo userdel honeypot-proxy 2>/dev/null || true

echo -e "${YELLOW}Cleaning up certificates in current directory...${NC}"
rm -f server.crt server.key server.csr san.conf 2>/dev/null || true

echo -e "${GREEN}✅ Reset complete!${NC}"
echo ""
echo "The following have been removed:"
echo "  - /opt/honeypot-proxy/ (application)"
echo "  - /var/log/honeypot-proxy/ (logs)"
echo "  - /etc/honeypot-proxy/ (config)"
echo "  - systemd service"
echo "  - honeypot-proxy user"
echo "  - Local certificates"
echo ""
echo "You can now run complete-setup.sh again for a fresh installation."
