#!/usr/bin/env bash
# ==============================================================================
# Astaro-Next Firewall OS - Astaro-Next Style Automated Installer ISO Builder
# ==============================================================================
# Target: Debian 12 (Bookworm) / Debian 13 (Trixie) 64-bit amd64
# Output: dist/astaro-next-installer-amd64.iso (Hybrid BIOS & UEFI Bootable)
# ==============================================================================

set -e

if [ "$EUID" -ne 0 ]; then
  echo "[-] Please run as root (e.g. sudo bash build-utm-iso.sh)"
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUTPUT_DIR="${SCRIPT_DIR}/dist"
ISO_NAME="astaro-next-installer-amd64.iso"
WORK_DIR="/root/astaro-iso-workspace"
DEBIAN_ISO_URL="https://cdimage.debian.org/debian-cd/current/amd64/iso-cd/debian-12.9.0-amd64-netinst.iso"
LOCAL_SOURCE_ISO=""

# Check if local debian ISO exists in workspace
if [ -f "${SCRIPT_DIR}/debian-13.iso" ]; then
  LOCAL_SOURCE_ISO="${SCRIPT_DIR}/debian-13.iso"
elif [ -f "${SCRIPT_DIR}/debian-12.iso" ]; then
  LOCAL_SOURCE_ISO="${SCRIPT_DIR}/debian-12.iso"
fi

echo "===================================================================="
echo "    Astaro-Next Firewall OS - Automated Appliance ISO Builder       "
echo "===================================================================="

# 1. Install prerequisites
echo "[+] Step 1/6: Installing ISO mastering tools..."
export DEBIAN_FRONTEND=noninteractive
sed -i '/cdrom:/d' /etc/apt/sources.list /etc/apt/sources.list.d/* 2>/dev/null || true
apt-get update -y
apt-get install -y --no-install-recommends \
  xorriso \
  isolinux \
  syslinux-utils \
  cpio \
  gzip \
  p7zip-full \
  wget \
  curl \
  ca-certificates

# 2. Setup workspace
echo "[+] Step 2/6: Setting up build directories..."
rm -rf "${WORK_DIR}"
mkdir -p "${WORK_DIR}/iso_root" "${WORK_DIR}/initrd_temp" "${OUTPUT_DIR}"

# 3. Obtain base Debian installer ISO
if [ -n "${LOCAL_SOURCE_ISO}" ] && [ -f "${LOCAL_SOURCE_ISO}" ]; then
  echo "[+] Step 3/6: Extracting local Debian installer ISO (${LOCAL_SOURCE_ISO})..."
  7z x -o"${WORK_DIR}/iso_root" "${LOCAL_SOURCE_ISO}" > /dev/null
else
  echo "[+] Step 3/6: Downloading official Debian minimal netinst base..."
  wget -q --show-progress -O "${WORK_DIR}/debian-base.iso" "${DEBIAN_ISO_URL}" || {
    echo "[-] Fallback: downloading mirror netinst..."
    wget -q --show-progress -O "${WORK_DIR}/debian-base.iso" "https://cdimage.debian.org/cdimage/archive/12.8.0/amd64/iso-cd/debian-12.8.0-amd64-netinst.iso"
  }
  echo "    Extracting ISO filesystem..."
  7z x -o"${WORK_DIR}/iso_root" "${WORK_DIR}/debian-base.iso" > /dev/null
fi

# 4. Inject Preseed Configuration & Payload into Installer Initrd
echo "[+] Step 4/6: Embedding Astaro-Next preseed & automated provisioning payload..."

# Create the preseed configuration
cat << 'EOF' > "${WORK_DIR}/preseed.cfg"
# ==============================================================================
# Astaro-Next Firewall OS - Unattended Automated Installer Preseed
# ==============================================================================
d-i debian-installer/locale string en_US.UTF-8
d-i keyboard-configuration/xkb-keymap select us

# Network Configuration (DHCP fallback)
d-i netcfg/choose_interface select auto
d-i netcfg/get_hostname string astaro-next
d-i netcfg/get_domain string internal

# Mirror Settings
d-i mirror/country string manual
d-i mirror/http/hostname string deb.debian.org
d-i mirror/http/directory string /debian
d-i mirror/http/proxy string

# Root Account (password: astaro)
d-i passwd/root-login boolean true
d-i passwd/make-user boolean false
d-i passwd/root-password password astaro
d-i passwd/root-password-again password astaro

# Clock and Timezone (UTC standard)
d-i clock-setup/utc boolean true
d-i time/zone string UTC
d-i clock-setup/ntp boolean true

# Automated Partitioning (Guided - Entire Disk)
d-i partman-auto/method string regular
d-i partman-auto/choose_recipe select atomic
d-i partman-partitioning/confirm_write_new_label boolean true
d-i partman/choose_partition select finish
d-i partman/confirm boolean true
d-i partman/confirm_nooverwrite boolean true

# Base Packages to Install
tasksel tasksel/first multiselect ssh-server, standard
d-i pkgsel/include string python3 python3-venv python3-pip nftables wireguard wireguard-tools nginx postfix rspamd curl openssl ca-certificates iproute2 net-tools sudo
d-i pkgsel/upgrade select full-upgrade
popularity-contest popularity-contest/participate boolean false

# GRUB Bootloader Installation (Automatic to primary drive)
d-i grub-installer/only_debian boolean true
d-i grub-installer/with_other_os boolean true
d-i grub-installer/bootdev string default

# Late Command: Inject Astaro-Next Codebase, Certificates & Enable Middleware Service
d-i preseed/late_command string \
  mkdir -p /target/opt/astaro; \
  cp -r /cdrom/astaro_payload/* /target/opt/astaro/; \
  in-target python3 -m venv /opt/astaro/backend/venv; \
  in-target /opt/astaro/backend/venv/bin/pip install --upgrade pip; \
  in-target /opt/astaro/backend/venv/bin/pip install -r /opt/astaro/backend/requirements.txt; \
  mkdir -p /target/etc/astaro/ssl; \
  openssl req -x509 -newkey rsa:2048 -keyout /target/etc/astaro/ssl/middleware.key -out /target/etc/astaro/ssl/middleware.crt -days 3650 -nodes -subj "/CN=astaro-next.internal/O=Astaro NextGen Firewall/OU=Middleware"; \
  chmod 600 /target/etc/astaro/ssl/middleware.key; \
  chmod 644 /target/etc/astaro/ssl/middleware.crt; \
  echo "astaro-admin-sec-key-9982441" > /target/etc/astaro/middleware.token; \
  chmod 600 /target/etc/astaro/middleware.token; \
  cp /target/opt/astaro/backend/astaro-middleware.service /target/etc/systemd/system/; \
  in-target systemctl daemon-reload; \
  in-target systemctl enable astaro-middleware.service; \
  in-target systemctl enable ssh.service; \
  mkdir -p /target/etc/nftables.d /target/etc/wireguard /target/etc/network/interfaces.d; \
  sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /target/etc/ssh/sshd_config;

# Finish without prompt and reboot
d-i finish-install/reboot_in_progress note
EOF

# Copy codebase payload directly into ISO tree
mkdir -p "${WORK_DIR}/iso_root/astaro_payload"
cp -r "${SCRIPT_DIR}/backend" "${WORK_DIR}/iso_root/astaro_payload/"
cp -r "${SCRIPT_DIR}/frontend" "${WORK_DIR}/iso_root/astaro_payload/"

# Repack initrd.gz with preseed.cfg included at the root
INITRD_PATH=""
for p in "${WORK_DIR}/iso_root/install.amd/initrd.gz" "${WORK_DIR}/iso_root/install/initrd.gz"; do
  if [ -f "$p" ]; then
    INITRD_PATH="$p"
    break
  fi
done

if [ -n "${INITRD_PATH}" ]; then
  echo "    Injecting preseed into ${INITRD_PATH}..."
  cd "${WORK_DIR}/initrd_temp"
  zcat "${INITRD_PATH}" | cpio -idmv > /dev/null 2>&1 || true
  cp "${WORK_DIR}/preseed.cfg" preseed.cfg
  find . | cpio -o -H newc | gzip -9 > "${INITRD_PATH}"
  cd "${WORK_DIR}"
  rm -rf "${WORK_DIR}/initrd_temp"
fi

# Also place preseed.cfg in ISO root
cp "${WORK_DIR}/preseed.cfg" "${WORK_DIR}/iso_root/preseed.cfg"

# 5. Customize Boot Menu Branding
echo "[+] Step 5/6: Customizing bootloader branding & timeout (Astaro-Next Style)..."

# ISOLINUX Menu (BIOS)
if [ -f "${WORK_DIR}/iso_root/isolinux/isolinux.cfg" ]; then
  cat << 'EOF' > "${WORK_DIR}/iso_root/isolinux/isolinux.cfg"
default astaro-install
timeout 30
prompt 0

label astaro-install
  menu label ^Install Astaro-Next Firewall OS (Automated)
  kernel /install.amd/vmlinuz
  append vga=788 initrd=/install.amd/initrd.gz auto=true priority=critical preseed/file=/cdrom/preseed.cfg --- quiet
EOF
fi

# GRUB Menu (UEFI)
if [ -f "${WORK_DIR}/iso_root/boot/grub/grub.cfg" ]; then
  cat << 'EOF' > "${WORK_DIR}/iso_root/boot/grub/grub.cfg"
set default="0"
set timeout=3

set menu_color_normal=white/black
set menu_color_highlight=black/light-gray

menuentry "Install Astaro-Next Firewall OS (Automated)" {
    set background_color=black
    linux /install.amd/vmlinuz vga=788 auto=true priority=critical preseed/file=/cdrom/preseed.cfg --- quiet
    initrd /install.amd/initrd.gz
}
EOF
fi

# Regenerate md5sums
cd "${WORK_DIR}/iso_root"
if [ -f "md5sum.txt" ]; then
  md5sum $(find . -type f ! -name "md5sum.txt" ! -path "./isolinux/*" ! -path "./boot/*") > md5sum.txt 2>/dev/null || true
fi

# 6. Master Hybrid Bootable ISO with xorriso
echo "[+] Step 6/6: Mastering hybrid bootable ISO with xorriso..."
cd "${WORK_DIR}"

xorriso -as mkisofs \
  -r -V "ASTARO_NEXT" \
  -o "${OUTPUT_DIR}/${ISO_NAME}" \
  -J -joliet-long \
  -b isolinux/isolinux.bin \
  -c isolinux/boot.cat \
  -no-emul-boot -boot-load-size 4 -boot-info-table \
  -isohybrid-mbr /usr/lib/ISOLINUX/isohdpfx.bin \
  -eltorito-alt-boot \
  -e boot/grub/efi.img \
  -no-emul-boot -isohybrid-gpt-basdat \
  "${WORK_DIR}/iso_root" 2>/dev/null || \
xorriso -as mkisofs \
  -r -V "ASTARO_NEXT" \
  -o "${OUTPUT_DIR}/${ISO_NAME}" \
  -J -joliet-long \
  -b isolinux/isolinux.bin \
  -c isolinux/boot.cat \
  -no-emul-boot -boot-load-size 4 -boot-info-table \
  "${WORK_DIR}/iso_root"

echo ""
echo "===================================================================="
echo "    🎉 Astaro-Next Installer ISO Built Successfully!"
echo "===================================================================="
echo "  ISO Path:    ${OUTPUT_DIR}/${ISO_NAME}"
echo "  Format:      Hybrid BIOS (MBR) + UEFI Bootable"
echo "  Installer:   Automated (Astaro-Next / ASG Style)"
echo "  Default Web: https://<device-ip>:4444"
echo "  Root Login:  root / astaro"
echo "===================================================================="
