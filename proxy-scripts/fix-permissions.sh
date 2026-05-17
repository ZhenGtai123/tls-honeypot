#!/bin/bash

echo "🔧 Fixing permissions and ownership..."

# Fix binary permissions
sudo chown root:root /opt/honeypot-proxy/bin/honeypot-proxy
sudo chmod 755 /opt/honeypot-proxy/bin/honeypot-proxy

# Fix certs permissions
sudo chown root:root /opt/honeypot-proxy/certs/*
sudo chmod 644 /opt/honeypot-proxy/certs/*.crt
sudo chmod 600 /opt/honeypot-proxy/certs/*.key

# Fix log directory
sudo chown -R honeypot-proxy:honeypot-proxy /var/log/honeypot-proxy
sudo chmod 755 /var/log/honeypot-proxy

# Test binary
echo "Testing binary execution..."
sudo /opt/honeypot-proxy/bin/honeypot-proxy -h
if [ $? -eq 0 ]; then
    echo "✓ Binary works correctly"
else
    echo "✗ Binary still has issues"
    exit 1
fi

# Restart service
echo "Restarting service..."
sudo systemctl daemon-reload
sudo systemctl restart honeypot-proxy

# Check status
sleep 2
sudo systemctl status honeypot-proxy --no-pager

# Show logs if still failing
if ! sudo systemctl is-active --quiet honeypot-proxy; then
    echo "Service still failing. Checking logs..."
    sudo journalctl -u honeypot-proxy -n 20 --no-pager
fi
