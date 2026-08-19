#!/usr/bin/env bash
# ==============================================================================
# Astaro-Next Firewall OS - Bootable Appliance ISO Image Builder
# ==============================================================================
# Target Platform: Debian 12 (Bookworm) / Debian 13 (Trixie) 64-bit (amd64)
# Output: astaro-next-appliance.iso (Hybrid BIOS & UEFI Bootable)
# ==============================================================================

set -e

if [ "$EUID" -ne 0 ]; then
  echo "[-] Please run as root (e.g., sudo bash build-iso.sh)"
  exit 1
fi

BUILD_DIR="${SCRIPT_DIR}/.build-workspace"
OUTPUT_DIR="${SCRIPT_DIR}/dist"
ISO_NAME="astaro-next-v2.4-amd64.iso"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "===================================================================="
echo "          Astaro-Next Firewall OS ISO Builder                      "
echo "===================================================================="

# 1. Install ISO building prerequisites
echo "[+] Step 1/6: Cleaning apt sources and installing ISO mastering tools..."
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

chmod 666 /dev/null 2>/dev/null || true
chmod 1777 /tmp 2>/dev/null || true

apt-get update -y
apt-get install -y --no-install-recommends \
  live-build \
  debootstrap \
  debian-archive-keyring \
  debian-keyring \
  gpgv \
  gnupg \
  xorriso \
  isolinux \
  syslinux-utils \
  syslinux-efi \
  grub-pc-bin \
  grub-efi-amd64-bin \
  mtools \
  dosfstools \
  squashfs-tools \
  git \
  curl \
  ca-certificates

# 2. Prepare workspace
echo "[+] Step 2/6: Setting up build workspace in ${BUILD_DIR}..."
rm -rf "${BUILD_DIR}"
mkdir -p "${BUILD_DIR}" "${OUTPUT_DIR}"
cd "${BUILD_DIR}"

# 3. Configure Debian Live system
echo "[+] Step 3/6: Configuring live-build parameters (Hybrid BIOS/UEFI)..."
lb config \
  --distribution bookworm \
  --architectures amd64 \
  --linux-flavours amd64 \
  --archive-areas "main contrib non-free non-free-firmware" \
  --apt-indices false \
  --apt-recommends false \
  --bootloaders "syslinux,grub-efi" \
  --binary-images iso-hybrid \
  --image-name "astaro-next" \
  --iso-application "Astaro-Next Firewall OS" \
  --iso-publisher "Astaro-Next Security Team" \
  --iso-volume "ASTARO_NEXT" \
  --memtest none

# 4. Define Package Inclusions
echo "[+] Step 4/6: Defining firewall & networking package list..."
mkdir -p config/package-lists
cat << 'EOF' > config/package-lists/astaro.list.chroot
# Essential Live Boot Hooks & System
live-boot
live-config
live-config-systemd
live-tools
linux-image-amd64
systemd
systemd-sysv
dbus
iproute2
net-tools
nftables
wireguard
wireguard-tools
nginx
postfix
rspamd
openssl
curl
wget
ca-certificates
openssh-server
python3
python3-pip
python3-venv
psmisc
pciutils
usbutils
sudo
locales
tzdata
EOF

# 5. Inject Astaro-Next Codebase and Services into Rootfs
echo "[+] Step 5/6: Injecting Astaro-Next codebase & services into ISO rootfs..."
ROOTFS_DIR="config/includes.chroot"
mkdir -p "${ROOTFS_DIR}/opt/astaro"
mkdir -p "${ROOTFS_DIR}/etc/astaro/ssl"
mkdir -p "${ROOTFS_DIR}/etc/systemd/system"
mkdir -p "${ROOTFS_DIR}/etc/nftables.d"
mkdir -p "${ROOTFS_DIR}/etc/network/interfaces.d"
mkdir -p "${ROOTFS_DIR}/etc/wireguard"

# Copy repository files into the image rootfs
cp -r "${SCRIPT_DIR}/backend" "${ROOTFS_DIR}/opt/astaro/"
cp -r "${SCRIPT_DIR}/frontend" "${ROOTFS_DIR}/opt/astaro/"

# Pre-generate self-signed TLS certificates
openssl req -x509 -newkey rsa:2048 \
  -keyout "${ROOTFS_DIR}/etc/astaro/ssl/middleware.key" \
  -out "${ROOTFS_DIR}/etc/astaro/ssl/middleware.crt" \
  -days 3650 -nodes \
  -subj "/CN=astaro-next.internal/O=Astaro NextGen Firewall/OU=Middleware" 2>/dev/null
chmod 600 "${ROOTFS_DIR}/etc/astaro/ssl/middleware.key"
chmod 644 "${ROOTFS_DIR}/etc/astaro/ssl/middleware.crt"

# Set default API token
echo "astaro-admin-sec-key-9982441" > "${ROOTFS_DIR}/etc/astaro/middleware.token"
chmod 600 "${ROOTFS_DIR}/etc/astaro/middleware.token"

# Systemd Service Unit
cat << 'EOF' > "${ROOTFS_DIR}/etc/systemd/system/astaro-middleware.service"
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

# Chroot Post-Installation Hook (Virtualenv & Systemd Enablement)
mkdir -p config/hooks/normal
cat << 'EOF' > config/hooks/normal/0990-astaro-setup.hook.chroot
#!/bin/sh
set -e

# Create Python virtual environment and install dependencies
cd /opt/astaro/backend
python3 -m venv venv
./venv/bin/pip install --upgrade pip
./venv/bin/pip install -r requirements.txt

# Enable systemd services
systemctl enable astaro-middleware.service
systemctl enable ssh.service
systemctl enable nftables.service 2>/dev/null || true

# Set default root password to 'astaro' for console access if desired
echo "root:astaro" | chpasswd
EOF
chmod +x config/hooks/normal/0990-astaro-setup.hook.chroot

# 6. Execute Live Build
echo "[+] Step 6/6: Compiling and mastering the ISO image (this may take 3-5 minutes)..."
lb build

# Move generated ISO to dist/
if [ -f "live-image-amd64.hybrid.iso" ]; then
  mv "live-image-amd64.hybrid.iso" "${OUTPUT_DIR}/${ISO_NAME}"
elif [ -f "astaro-next-amd64.hybrid.iso" ]; then
  mv "astaro-next-amd64.hybrid.iso" "${OUTPUT_DIR}/${ISO_NAME}"
else
  # Catch any .iso file produced
  ISO_PRODUCED=$(find . -maxdepth 1 -name "*.iso" | head -n1)
  if [ -n "${ISO_PRODUCED}" ]; then
    mv "${ISO_PRODUCED}" "${OUTPUT_DIR}/${ISO_NAME}"
  fi
fi

echo ""
echo "===================================================================="
echo "    🎉 Bootable Astaro-Next ISO Created Successfully!"
echo "===================================================================="
echo "  ISO Path:    ${OUTPUT_DIR}/${ISO_NAME}"
echo "  Architecture: 64-bit x86_64 (BIOS & UEFI Hybrid)"
echo "  Default Web: https://<device-ip>:4444"
echo "  Root Login:  root / astaro"
echo "===================================================================="
