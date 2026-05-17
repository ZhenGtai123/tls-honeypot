# Complete Honeypot Proxy Setup Guide

This guide walks through setting up two Ubuntu VMs on VirtualBox to run a TLS-decrypting honeypot with your own Go proxy, following the architecture from [Nirusu’s honeypot guide](https://github.com/Nirusu/how-to-setup-a-honeypot) but using a custom Go proxy instead of PolarProxy.

## Architecture

- **Proxy VM** (192.168.100.20) – runs the Go proxy, iptables forwarding, Suricata IDS, and packet capture.
- **Honeypot VM** (192.168.100.10) – runs a vulnerable web application (WordPress).
- Both VMs communicate over a **VirtualBox Host-Only network** (192.168.100.0/24). Your Windows host also has an IP on this network (e.g., 192.168.100.1) for SSH access.

```
Windows Host (VSCode)
      │ SSH (192.168.100.1)
      ▼
┌──────────────────────┐          ┌─────────────────────┐
│   Proxy VM           │   HTTP   │  Honeypot VM        │
│   192.168.100.20     │─────────▶│  192.168.100.10     │
│   (Go proxy :443)    │          │  (WordPress :80)    │
│   iptables + Suricata│          │                     │
└──────────────────────┘          └─────────────────────┘
        Host-Only network 192.168.100.0/24
```

---

## 1. VirtualBox & VM Preparation

### 1.1 Create the Host-Only Network

1. Open VirtualBox → **File** → **Host Network Manager**.
2. Click **Create** to add a new host-only network.
3. Select the new adapter and click **Properties**.
   - **Adapter** tab: set IPv4 address to `192.168.100.1`, mask `255.255.255.0`.
   - **DHCP Server** tab: **uncheck** “Enable Server” (we will use static IPs).
4. Click **Apply** → **Close**.

### 1.2 Create Two VMs

Create two Ubuntu 20.04 (or 22.04) VMs with the following settings:

| Setting               | Proxy VM           | Honeypot VM        |
|-----------------------|--------------------|--------------------|
| Memory                | 2 GB               | 2 GB               |
| Disk                  | 20 GB              | 20 GB              |
| Network Adapter 1     | NAT (for internet) | NAT (for internet) |
| Network Adapter 2     | Host-Only (vboxnet0) | Host-Only (vboxnet0) |

> **Why two adapters?**  
> - NAT allows the VMs to download packages (apt, go, etc.).  
> - Host-Only gives them static IPs on `192.168.100.0/24` and allows them to talk to each other and to your Windows host.

### 1.3 Install Ubuntu on Both VMs

Use the default installation. Create a regular user (e.g., `ubuntu`) with sudo privileges.

After installation, shut down the VMs and ensure both have the two network adapters as above.

---

## 2. Static IP Configuration (Netplan)

Start each VM and open a terminal (or use the VM console). We will assign static IPs on the Host-Only interface.

### 2.1 On Proxy VM

Find interface names:
```bash
ip a
```
You’ll likely see `enp0s3` (NAT) and `enp0s8` (Host-Only). Edit netplan:
```bash
sudo nano /etc/netplan/00-installer-config.yaml
```
Replace with:
```yaml
network:
  version: 2
  ethernets:
    enp0s3:                # NAT interface – gets DHCP
      dhcp4: true
    enp0s8:                # Host-Only interface – static
      dhcp4: no
      addresses:
        - 192.168.100.20/24
      nameservers:
        addresses: [8.8.8.8, 8.8.4.4]
```
Apply:
```bash
sudo netplan apply
```

### 2.2 On Honeypot VM

Similarly, edit netplan:
```yaml
network:
  version: 2
  ethernets:
    enp0s3:
      dhcp4: true
    enp0s8:
      dhcp4: no
      addresses:
        - 192.168.100.10/24
      nameservers:
        addresses: [8.8.8.8, 8.8.4.4]
```
Apply:
```bash
sudo netplan apply
```

### 2.3 Verify Connectivity

- On each VM, `ip a` should show the correct IPs.
- From Proxy VM, ping the honeypot: `ping 192.168.100.10`.
- From Windows host, ping both VMs: `ping 192.168.100.20` and `ping 192.168.100.10`.

---

## 3. SSH Access & VSCode Setup

### 3.1 Install and Enable SSH on Both VMs

Run on each VM:
```bash
sudo apt update
sudo apt install -y openssh-server
sudo systemctl enable --now ssh
```

### 3.2 (Optional) Set Up SSH Keys for Passwordless Login

From Windows PowerShell (as admin):
```powershell
# Generate key pair (if not already)
ssh-keygen -t ed25519

# Copy public key to each VM
type $env:USERPROFILE\.ssh\id_ed25519.pub | ssh ubuntu@192.168.100.20 "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"
type $env:USERPROFILE\.ssh\id_ed25519.pub | ssh ubuntu@192.168.100.10 "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"
```

### 3.3 Connect with VSCode

1. Install the **Remote – SSH** extension.
2. Press `Ctrl+Shift+P` → **Remote-SSH: Open SSH Configuration File** → select your user config.
3. Add:
   ```ssh-config
   Host proxy-vm
       HostName 192.168.100.20
       User ubuntu
       IdentityFile ~/.ssh/id_ed25519

   Host honeypot-vm
       HostName 192.168.100.10
       User ubuntu
       IdentityFile ~/.ssh/id_ed25519
   ```
4. Connect: `Ctrl+Shift+P` → **Remote-SSH: Connect to Host** → `proxy-vm`.

Now you can open terminals and edit files directly on both VMs from VSCode.

---

## 4. Install WordPress on Honeypot VM

Run these commands on the honeypot VM (`192.168.100.10`):

```bash
# Install LAMP stack
sudo apt update
sudo apt install -y apache2 mysql-server php php-mysql libapache2-mod-php php-curl php-gd php-mbstring php-xml php-xmlrpc

# Download WordPress
cd /tmp
wget https://wordpress.org/latest.tar.gz
tar -xzf latest.tar.gz
sudo mv wordpress /var/www/html/

# Set permissions
sudo chown -R www-data:www-data /var/www/html/wordpress
sudo chmod -R 755 /var/www/html/wordpress

# Create MySQL database
sudo mysql -u root <<EOF
CREATE DATABASE wordpress;
CREATE USER 'wpuser'@'localhost' IDENTIFIED BY 'StrongPassword123!';
GRANT ALL ON wordpress.* TO 'wpuser'@'localhost';
FLUSH PRIVILEGES;
EOF

# Restart Apache
sudo systemctl restart apache2
```

WordPress will be available at `http://192.168.100.10/wordpress`. You can complete the setup wizard later.

> **Test**: On proxy VM, run `curl http://192.168.100.10/wordpress` – you should see the WordPress page.

---

## 5. Build and Deploy the Go Proxy (on Proxy VM)

The proxy will:
- Listen on `192.168.100.20:443` with a TLS certificate.
- Decrypt each request, log details (JSONL format), and forward plain HTTP to `192.168.100.10:80`.
- Send the response back to the client.

### 5.1 Install Go

On proxy VM:
```bash
wget https://go.dev/dl/go1.22.3.linux-amd64.tar.gz
sudo rm -rf /usr/local/go
sudo tar -C /usr/local -xzf go1.22.3.linux-amd64.tar.gz
echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.bashrc
source ~/.bashrc
go version
```

### 5.2 Prepare the Go Source Code

Create a file named `honeypot-proxy.go` in your home directory on the proxy VM. (You must provide this file; the content is not included here but should implement TLS termination, logging, and forwarding as described.)

### 5.3 Use the Provided Setup Scripts

The user has provided several bash scripts. Save them on the proxy VM (e.g., in `~/scripts/`) and make them executable.

**Script 1: `complete-setup.sh`** – installs the proxy as a systemd service.  
**Script 2: `gen-cert.sh`** – generates TLS certificate.  
**Script 3: `reset-proxy.sh`** – removes everything.  
**Script 4: `update-proxy.sh`** – rebuilds and restarts.  
**Script 5: `fix-permissions.sh`** – fixes ownership.

#### 5.3.1 Generate the Certificate

Run the certificate generation script:
```bash
chmod +x gen-cert.sh
./gen-cert.sh
```
This creates `server.key` and `server.crt` inside `/opt/honeypot-proxy/certs/`.

#### 5.3.2 Run the Complete Setup

Make sure `honeypot-proxy.go` is in the same directory as `complete-setup.sh`, then:
```bash
chmod +x complete-setup.sh
./complete-setup.sh
```

The script will:
- Create directories, user, log rotation.
- Build the Go binary.
- Install systemd service (runs as root, listening on `192.168.100.20:443`, forwarding to `192.168.100.10:80`).
- Start the service.

Check status:
```bash
sudo systemctl status honeypot-proxy
```

#### 5.3.3 View Logs

Proxy logs (JSONL) are written to `/var/log/honeypot-proxy/`. View with:
```bash
tail -f /var/log/honeypot-proxy/traffic-*.jsonl | jq '.'
```
Service logs: `sudo journalctl -u honeypot-proxy -f`

---

## 6. Iptables Forwarding & Firewall (Proxy VM)

Now we configure iptables so that incoming traffic to the proxy’s public IP is handled correctly.

### 6.1 Enable IP Forwarding

```bash
sudo sysctl -w net.ipv4.ip_forward=1
echo "net.ipv4.ip_forward=1" | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```

### 6.2 Set Up iptables Rules

We will:
- Allow loopback and established connections.
- Allow SSH from the 192.168.100.0/24 network.
- Forward **port 80** (HTTP) directly to the honeypot (for unencrypted traffic).
- Let **port 443** go to the Go proxy (which listens on the proxy VM itself, not forwarded).
- Masquerade traffic from the honeypot so replies go back through the proxy.

Run these commands on the proxy VM:

```bash
# Flush existing rules (optional)
sudo iptables -F
sudo iptables -t nat -F
sudo iptables -P INPUT DROP
sudo iptables -P FORWARD DROP
sudo iptables -P OUTPUT ACCEPT

# Allow loopback and established connections
sudo iptables -A INPUT -i lo -j ACCEPT
sudo iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
sudo iptables -A FORWARD -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT

# Allow SSH from the host-only network
sudo iptables -A INPUT -s 192.168.100.0/24 -p tcp --dport 22 -j ACCEPT

# Allow the Go proxy to receive connections on port 443
sudo iptables -A INPUT -p tcp --dport 443 -j ACCEPT

# --- HTTP (port 80) : forward directly to honeypot ---
sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j DNAT --to-destination 192.168.100.10:80
sudo iptables -A FORWARD -d 192.168.100.10 -p tcp --dport 80 -j ACCEPT

# --- HTTPS (port 443) : NOT forwarded; Go proxy handles it locally ---
# No DNAT rule for 443

# Allow forwarding to/from honeypot VM
sudo iptables -A FORWARD -s 192.168.100.10 -j ACCEPT
sudo iptables -A FORWARD -d 192.168.100.10 -j ACCEPT

# Masquerade so honeypot replies appear from the proxy's IP
sudo iptables -t nat -A POSTROUTING -s 192.168.100.10 -j MASQUERADE
```

### 6.3 Save iptables Rules

```bash
sudo apt install -y iptables-persistent
sudo netfilter-persistent save
```

During installation, answer “Yes” to save current IPv4 rules.

---

## 7. Optional: Suricata IDS & Packet Capture (Proxy VM)

### 7.1 Install Suricata

```bash
sudo add-apt-repository ppa:oisf/suricata-stable -y
sudo apt update
sudo apt install -y suricata
sudo suricata-update
```

### 7.2 Configure Suricata

Edit `/etc/suricata/suricata.yaml`:
- Set `HOME_NET: "[192.168.100.0/24]"`
- Under `af-packet:`, set `interface: enp0s8` (or your host-only interface).

Start Suricata:
```bash
sudo systemctl enable suricata
sudo systemctl start suricata
```

### 7.3 Install TShark for Packet Capture

```bash
sudo apt install -y tshark
sudo mkdir -p /var/log/captures
```

Capture all traffic on the host-only interface, excluding port 443 (already logged by the proxy):
```bash
sudo tshark -i enp0s8 -b filesize:500000 -w /var/log/captures/honeypot.pcap -f "not (tcp port 443)" &
```
To make it persistent, create a systemd service or add to crontab.

---

## 8. Testing the Setup

From your Windows host (or any machine on the 192.168.100.0/24 network):

### 8.1 Test HTTP (direct to honeypot)
```bash
curl http://192.168.100.20/wordpress
```
You should see the WordPress page (because port 80 is forwarded to the honeypot).

### 8.2 Test HTTPS (through Go proxy)
```bash
curl -k https://192.168.100.20/wordpress
```
The `-k` ignores self-signed certificate errors. You should again see the WordPress page, but this time the request passed through the Go proxy, which logged the decrypted traffic.

### 8.3 Check Proxy Logs

On the proxy VM:
```bash
sudo journalctl -u honeypot-proxy -f
```
You’ll see each request logged with method, path, headers, and POST body (if any).

### 8.4 Simulate an Attack

Try a path traversal:
```bash
curl -k "https://192.168.100.20/wordpress/../../../../etc/passwd"
```
The proxy’s log should show the malicious path.

---

## 9. Useful Commands & Scripts

| Action | Command |
|--------|---------|
| Restart proxy | `sudo systemctl restart honeypot-proxy` |
| View live proxy logs | `sudo journalctl -u honeypot-proxy -f` |
| View JSON logs | `tail -f /var/log/honeypot-proxy/traffic-*.jsonl \| jq '.'` |
| Reset everything | `./reset-proxy.sh` (run on proxy VM) |
| Update proxy code | Copy new `honeypot-proxy.go`, then `./update-proxy.sh` |
| Reload iptables | `sudo netfilter-persistent reload` |
| Check Suricata alerts | `sudo tail -f /var/log/suricata/fast.log` |

---

## 10. Next Steps

- Complete the WordPress setup wizard by visiting `http://192.168.100.10/wordpress` from your browser.
- Harden the honeypot with more vulnerable plugins or a custom application.
- Integrate the proxy logs with ELK (Elasticsearch, Logstash, Kibana) for analysis.
- Set up Falco on the honeypot VM to detect post‑exploit behaviour.

