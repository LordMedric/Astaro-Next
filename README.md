# Astaro-Next Firewall OS

A modern Next-Generation Firewall (NGFW) management dashboard and backend middleware inspired by Sophos XGS / SFOS architecture, targeting Debian GNU/Linux systems.

## Project Structure

- **`backend/`**: FastAPI-based firewall configuration daemon and middleware service (`port 4444`). Interacts directly with Linux subsystems (nftables, WireGuard, network interfaces, Postfix, Squid, etc.).
- **`frontend/`**: Vue 3 single-page web management application with Tailwind CSS styling modeled after Sophos SFOS appliances.

## Subsystems & Features

- **Control Center & Setup Wizard**: Real-time system telemetry (CPU, RAM, Disk, Services, Interfaces) and first-run configuration.
- **Network Interfaces**: Physical and virtual interface configuration, IP assignment, and persistence (`/etc/network/interfaces.d/`).
- **Firewall & NFTables**: Zone-based policy management with atomic compilation and live inspection.
- **WireGuard VPN**: Tunnel management, keypair generation, and client profile provisioning.
- **Mail Security & Manager**: Postfix mail queue monitoring, message inspection, and spam quarantine.
- **Web Protection & WAF**: Squid proxy integration and Web Application Firewall rulesets.

## Getting Started

### Backend Setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

### Frontend Setup

Open `frontend/index.html` in your browser or serve via a lightweight HTTP server:

```bash
cd frontend
python -m http.server 8080
```
