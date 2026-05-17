#!/bin/bash

echo "Generating browser-compatible certificate..."

cd /opt/honeypot-proxy/certs

# Remove old files
sudo rm -f server.key server.crt server.csr

# Generate private key
sudo openssl genrsa -out server.key 2048

# Create certificate config
sudo tee cert.conf > /dev/null <<EOF
[req]
default_bits = 2048
prompt = no
default_md = sha256
distinguished_name = dn
req_extensions = v3_req

[dn]
CN = 192.168.100.20

[v3_req]
keyUsage = keyEncipherment, dataEncipherment, digitalSignature
extendedKeyUsage = serverAuth
subjectAltName = @alt_names

[alt_names]
IP.1 = 192.168.100.20
IP.2 = 127.0.0.1
DNS.1 = localhost
EOF

# Generate CSR
sudo openssl req -new -key server.key -out server.csr -config cert.conf

# Generate self-signed certificate
sudo openssl x509 -req -in server.csr -signkey server.key -out server.crt -days 365 -extensions v3_req -extfile cert.conf

# Set permissions
sudo chmod 600 server.key
sudo chmod 644 server.crt

# Clean up
sudo rm -f cert.conf server.csr

echo "✅ Certificate generated"
openssl x509 -in server.crt -text -noout | grep -E "Subject:|DNS:|IP Address:"
