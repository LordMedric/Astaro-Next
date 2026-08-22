# Astaro-Next Next-Generation Firewall OS

A modern, enterprise-grade Next-Generation Firewall (NGFW) & Unified Threat Management (UTM) platform built entirely on **100% open-source Linux technologies**. Astaro-Next delivers the legendary clarity and power of Astaro / UTM with a modernized, lightning-fast web experience inspired by modern enterprise NGFW appliances.

---

## 🛠️ Open-Source Engine & Technology Architecture

| Firewall & UTM Capability | Open-Source Engine / Technology | Description & Role |
|---|---|---|
| **Packet Filtering, Stateful Firewall & NAT** | **Linux `nftables` + `conntrack`** | High-performance atomic kernel packet filtering, SNAT/DNAT, stateful connection tracking, and geo-ip filtering via native sets. |
| **Intrusion Prevention (IPS/IDS) & Anti-DoS** | **Suricata + `fail2ban`** | Multi-threaded Next-Gen IDS/IPS engine with ET Open rulesets, protocol decoders, JA3 TLS fingerprinting, and automated anti-portscan rate-limiting. |
| **Advanced Threat Protection (ATP)** | **CAPE Sandbox + Suricata C2 Feeds** | Config And Payload Extraction (CAPE) automated dynamic malware detonation in isolated VMs, zero-day isolation, and botnet C2 DNS sinkholing. |
| **Web Protection & Content Filtering** | **Squid Proxy + Zenarmor + ClamAV** | High-throughput HTTP/HTTPS caching proxy, category-based URL filtering, SSL Bump/Inspection, and streaming anti-virus analysis. |
| **Email Protection & Anti-Spam** | **Postfix + Rspamd + ClamAV + Fetchmail** | Enterprise Mail Transfer Agent (MTA) with statistical neural anti-spam (Rspamd), DKIM/SPF/DMARC validation, POP3 proxy, and S/MIME encryption. |
| **Web Application Firewall (WAF)** | **NGINX + OWASP ModSecurity Core Rule Set (CRS)** | Reverse proxy with Layer 7 WAF inspection, SQLi / XSS protection, SNI routing, and automated Let's Encrypt TLS certificates. |
| **Virtual Private Networks (VPN)** | **WireGuard + StrongSwan (IPsec) + OpenVPN** | Kernel WireGuard for blazing speed site-to-site & roadwarrior tunnels, StrongSwan for enterprise IKEv2, and OpenVPN SSL tunnels. |
| **DNS, DHCP & Time Services** | **Unbound + `dnsmasq` + `chrony`** | Validating recursive DNSSEC resolver (Unbound), persistent stateful DHCP server with IP lease tracking, and high-precision NTP. |
| **Routing & Bandwidth Management (QoS)** | **FRRouting (FRR) + Linux `tc` (CAKE / FQ_CoDel)** | Policy-Based Routing (PBR), BGP/OSPF dynamic routing, Uplink Balancing, and Bufferbloat-free Traffic Shaping. |
| **Directory Authentication & 2FA** | **OpenLDAP + FreeRADIUS + RFC 6238 TOTP (PyOTP)** | Multi-backend user authentication with Active Directory / LDAP SSO, RADIUS, and Time-based One-Time Password 2FA tokens. |
| **Management API & WebAdmin UI** | **FastAPI + Uvicorn + Vue 3 (SFC) + Tailwind CSS** | Ultra-responsive asynchronous Python 3.11 middleware with zero-build browser-side Vue 3 compilation and SQLite persistence. |

---

## 📁 Repository Structure

- **`backend/`**: FastAPI-based firewall configuration daemon (`main.py`) and persistent SQLite database (`database.py`). Directly controls Linux kernel subsystems (`nftables`, WireGuard, interfaces, Postfix, Rspamd, Squid, Suricata).
- **`frontend/`**: Vue 3 management single-page application with Tailwind CSS styling and interactive SVG telemetry dashboards.
- **`install.sh`**: One-line turnkey appliance provisioner for Debian 12 (Bookworm) and Debian 13 (Trixie).
- **`build-utm-iso.sh`**: Automated bootable ISO builder for bare-metal and hypervisor appliances (Proxmox, VMware, Hyper-V, KVM).

---

## 🚀 Installation & Deployment

### Turnkey Automated Install (Debian 12 / 13)
```bash
curl -sSL https://raw.githubusercontent.com/LordMedric/Astaro-Next/main/install.sh | bash
```

### Accessing the WebAdmin Console
Once installed, open your browser and navigate to:
```
https://<YOUR_FIREWALL_IP>:4444
```
- **Default Authentication Token**: `astaro-admin-sec-key-9982441`
- **Swagger REST API Documentation**: `https://<YOUR_FIREWALL_IP>:4444/api/docs`

