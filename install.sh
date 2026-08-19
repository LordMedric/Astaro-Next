#!/usr/bin/env bash
# ==============================================================================
# Astaro-Next Firewall OS - Turnkey Appliance Setup & Provisioning Script
# ==============================================================================
# Target: Debian 12 (Bookworm) / Debian 13 (Trixie)
# Description: Fully automates dependencies, middleware daemon, and systemd service.
# ==============================================================================

set -e

# Ensure running as root
if [ "$EUID" -ne 0 ]; then
  echo "[-] Please run as root (e.g. sudo bash install.sh)"
  exit 1
fi

echo "===================================================================="
echo "          Astaro-Next Next-Gen Firewall OS Installer               "
echo "===================================================================="

# 1. Update and install system dependencies
echo "[+] Step 1/5: Cleaning apt sources and installing Linux packages..."
export DEBIAN_FRONTEND=noninteractive

# Automatically purge any cdrom sources leftover from offline installer ISO
sed -i 's/^[[:space:]]*deb[[:space:]]*cdrom/# deb cdrom/g' /etc/apt/sources.list 2>/dev/null || true
sed -i '/cdrom:/d' /etc/apt/sources.list 2>/dev/null || true

if [ -d /etc/apt/sources.list.d ]; then
  for f in /etc/apt/sources.list.d/*.sources /etc/apt/sources.list.d/*.list; do
    if [ -f "$f" ]; then
      sed -i '/cdrom:/d' "$f" 2>/dev/null || true
      sed -i '/URIs:.*cdrom/d' "$f" 2>/dev/null || true
      sed -i 's/^[[:space:]]*deb[[:space:]]*cdrom/# deb cdrom/g' "$f" 2>/dev/null || true
    fi
  done
fi

apt-get update -y
apt-get install -y --no-install-recommends \
  curl \
  wget \
  git \
  openssl \
  python3 \
  python3-pip \
  python3-venv \
  nftables \
  wireguard \
  wireguard-tools \
  nginx \
  postfix \
  rspamd \
  iproute2 \
  net-tools \
  ca-certificates

# 2. Deploy repository to /opt/astaro
INSTALL_DIR="/opt/astaro"
echo "[+] Step 2/5: Deploying Astaro-Next codebase to ${INSTALL_DIR}..."

# Ensure we are in a safe directory outside of INSTALL_DIR
cd /root 2>/dev/null || cd /tmp

if [ -d "${INSTALL_DIR}/.git" ]; then
  echo "    Existing repository found, pulling latest main branch..."
  cd "${INSTALL_DIR}"
  git fetch --all
  git reset --hard origin/main
else
  echo "    Cloning Astaro-Next from GitHub into ${INSTALL_DIR}..."
  rm -rf "${INSTALL_DIR}"
  git clone https://github.com/LordMedric/Astaro-Next.git "${INSTALL_DIR}"
fi

# 3. Setup Python Virtual Environment
echo "[+] Step 3/5: Setting up Python virtual environment & dependencies..."
cd "${INSTALL_DIR}/backend"
python3 -m venv venv
./venv/bin/pip install --upgrade pip
./venv/bin/pip install -r requirements.txt

# 4. Generate SSL Certificates if not present
echo "[+] Step 4/5: Generating TLS certificates for WebAdmin HTTPS..."
mkdir -p /etc/astaro/ssl
if [ ! -f /etc/astaro/ssl/middleware.key ] || [ ! -f /etc/astaro/ssl/middleware.crt ]; then
  openssl req -x509 -newkey rsa:2048 \
    -keyout /etc/astaro/ssl/middleware.key \
    -out /etc/astaro/ssl/middleware.crt \
    -days 3650 -nodes \
    -subj "/CN=astaro-next.internal/O=Astaro NextGen Firewall/OU=Middleware"
  chmod 600 /etc/astaro/ssl/middleware.key
  chmod 644 /etc/astaro/ssl/middleware.crt
fi

# Set default API token file
if [ ! -f /etc/astaro/middleware.token ]; then
  echo "astaro-admin-sec-key-9982441" > /etc/astaro/middleware.token
  chmod 600 /etc/astaro/middleware.token
fi

# 5. Register and start systemd service
echo "[+] Step 5/5: Registering & starting astaro-middleware systemd service..."
cat << 'EOF' > /etc/systemd/system/astaro-middleware.service
[Unit]
Description=Astaro-Next Appliance Configuration Middleware Daemon
After=network.target local-fs.target
Wants=nftables.service

[Service]
Type=simple
User=root
WorkingDirectory=/opt/astaro/backend
ExecStart=/opt/astaro/backend/venv/bin/python main.py
Restart=always
RestartSec=3
KillMode=process
LimitNOFILE=65536
AmbientCapabilities=CAP_NET_ADMIN CAP_NET_RAW CAP_DAC_OVERRIDE

# Environment Variables
Environment="ASTARO_LISTEN_HOST=0.0.0.0"
Environment="ASTARO_LISTEN_PORT=4444"
Environment="ASTARO_FRONTEND_DIR=/opt/astaro/frontend"
Environment="ASTARO_NFTABLES_CONF=/etc/nftables.conf"
Environment="ASTARO_WIREGUARD_DIR=/etc/wireguard"
Environment="ASTARO_AUTH_TOKEN_FILE=/etc/astaro/middleware.token"

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable astaro-middleware
systemctl restart astaro-middleware

# Ensure nftables and wireguard directories exist
mkdir -p /etc/nftables.d /etc/wireguard /etc/network/interfaces.d

# Get Primary IP
PRIMARY_IP=$(ip -4 addr show scope global | grep inet | awk '{print $2}' | cut -d/ -f1 | head -n1 || echo "YOUR_SERVER_IP")

echo ""
echo "===================================================================="
echo "    🎉 Astaro-Next Firewall OS Installation Complete!"
echo "===================================================================="
echo "  WebAdmin Console:  https://${PRIMARY_IP}:4444"
echo "  REST API Swagger:  https://${PRIMARY_IP}:4444/api/docs"
echo "  Service Status:    systemctl status astaro-middleware"
echo "===================================================================="
