#!/usr/bin/env python3
"""
===============================================================================
Astaro-Next Firewall OS - SQLite Persistent Datastore Engine
===============================================================================
Provides zero-external-dependency SQLite persistence for:
  - Zone-Based Firewall Rules & Sequencing
  - NAT / Masquerading / DNAT Rules
  - Network & Service Definitions (8 UTM Types)
  - Static & Policy Routes
  - System Settings, Admin ACLs & Notifications
  - Network Services (DHCP, DNS Forwarders, DynDNS, NTP)
  - WAF Profiles & Virtual Servers
  - WireGuard / IPsec VPN Peers & Tunnels
  - User Accounts & Roles
  - Backup & Configuration Snapshots
===============================================================================
"""

import os
import json
import sqlite3
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional

logger = logging.getLogger("astaro-database")

# Preferred system directory on Debian/Enterprise appliances, fallback to local directory
DB_SYSTEM_DIR = Path(os.getenv("ASTARO_DB_DIR", "/var/lib/astaro"))
try:
    DB_SYSTEM_DIR.mkdir(parents=True, exist_ok=True)
    DB_PATH = DB_SYSTEM_DIR / "astaro_config.db"
except Exception:
    DB_PATH = Path("astaro_config.db")

def get_db_connection() -> sqlite3.Connection:
    """Create and return a thread-safe connection with row_factory set to sqlite3.Row."""
    conn = sqlite3.connect(str(DB_PATH), timeout=10.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    return conn

def init_database():
    """Create all required tables and populate initial defaults if empty."""
    with get_db_connection() as conn:
        cursor = conn.cursor()

        # 1. Firewall Rules
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS firewall_rules (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                src_zone TEXT DEFAULT 'LAN',
                source_type TEXT DEFAULT 'Any',
                source_value TEXT DEFAULT 'Any',
                dest_zone TEXT DEFAULT 'WAN',
                dest_type TEXT DEFAULT 'Any',
                dest_value TEXT DEFAULT 'Any',
                services TEXT DEFAULT 'Any',
                action TEXT DEFAULT 'accept',
                enabled INTEGER DEFAULT 1,
                comment TEXT DEFAULT '',
                seq_order INTEGER DEFAULT 0
            )
        """)

        # 2. NAT Rules
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS nat_rules (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                type TEXT DEFAULT 'Masquerading',
                enabled INTEGER DEFAULT 1,
                source_network TEXT DEFAULT 'Internal (Network)',
                outbound_interface TEXT DEFAULT 'Uplink Interfaces (WAN)',
                traffic_service TEXT DEFAULT 'HTTPS',
                traffic_destination TEXT DEFAULT 'Uplink (WAN IP)',
                destination_nat_target TEXT DEFAULT '',
                service_translation TEXT DEFAULT '',
                auto_firewall_rule INTEGER DEFAULT 1,
                comment TEXT DEFAULT ''
            )
        """)

        # 3. Network Definitions (8 Sophos UTM Types)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS network_objects (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                type TEXT DEFAULT 'Host',
                address TEXT DEFAULT '',
                netmask TEXT DEFAULT '/24 (255.255.255.0)',
                from_ip TEXT DEFAULT '',
                to_ip TEXT DEFAULT '',
                comment TEXT DEFAULT '',
                interface TEXT DEFAULT '<< Any >>'
            )
        """)

        # 4. Service Definitions
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS service_objects (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                type TEXT DEFAULT 'TCP',
                protocol TEXT DEFAULT 'TCP',
                dst_port TEXT DEFAULT '',
                src_port TEXT DEFAULT '1:65535',
                comment TEXT DEFAULT ''
            )
        """)

        # 5. Users & Auth
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                username TEXT NOT NULL UNIQUE,
                real_name TEXT DEFAULT '',
                email TEXT DEFAULT '',
                role TEXT DEFAULT 'Administrator',
                status TEXT DEFAULT 'Active',
                auth_backend TEXT DEFAULT 'Local Database',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 6. Static & Policy Routes
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS routes (
                id TEXT PRIMARY KEY,
                destination TEXT NOT NULL,
                gateway TEXT NOT NULL,
                interface TEXT DEFAULT 'Any',
                metric INTEGER DEFAULT 10,
                route_type TEXT DEFAULT 'Static',
                comment TEXT DEFAULT '',
                enabled INTEGER DEFAULT 1
            )
        """)

        # 7. WAF Published Web Applications
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS waf_rules (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL UNIQUE,
                domain TEXT NOT NULL,
                upstream TEXT NOT NULL,
                ssl_enabled INTEGER DEFAULT 1,
                certificate_id TEXT DEFAULT 'cert_webadmin_default',
                certificate_name TEXT DEFAULT 'Appliance Default SSL',
                enable_sni INTEGER DEFAULT 1,
                waf_mode TEXT DEFAULT 'blocking',
                rule_packs TEXT DEFAULT 'SQLi, XSS, RCE, Protocol Violations',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        # Safe column migrations for existing databases
        for col_def in [
            "ALTER TABLE waf_rules ADD COLUMN certificate_id TEXT DEFAULT 'cert_webadmin_default'",
            "ALTER TABLE waf_rules ADD COLUMN certificate_name TEXT DEFAULT 'Appliance Default SSL'",
            "ALTER TABLE waf_rules ADD COLUMN enable_sni INTEGER DEFAULT 1"
        ]:
            try:
                cursor.execute(col_def)
            except sqlite3.OperationalError:
                pass

        # 8. VPN Tunnels (Site-to-Site)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vpn_tunnels (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                type TEXT DEFAULT 'WireGuard',
                remote_gateway TEXT DEFAULT '',
                local_network TEXT DEFAULT '192.168.1.0/24',
                remote_network TEXT DEFAULT '10.0.0.0/24',
                auth_type TEXT DEFAULT 'Pre-Shared Key (PSK)',
                status TEXT DEFAULT 'Connected',
                uptime TEXT DEFAULT '4d 18h',
                tx_bytes TEXT DEFAULT '4.2 GB',
                rx_bytes TEXT DEFAULT '8.7 GB'
            )
        """)

        # 9. Generic Key-Value Settings (System, IPS, DHCP, DNS, etc.)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS key_value_store (
                section TEXT NOT NULL,
                key TEXT NOT NULL,
                value_json TEXT NOT NULL,
                PRIMARY KEY (section, key)
            )
        """)

        # 10. Backups & Firmware Snapshots
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS backups (
                id TEXT PRIMARY KEY,
                filename TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                size_bytes INTEGER DEFAULT 0,
                version TEXT DEFAULT '2.4.0',
                notes TEXT DEFAULT ''
            )
        """)

        # 11. SMTP Profiles (Email Protection Multi-Domain SNI)
        # 11. SMTP Profiles (Email Protection Multi-Domain SNI)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS smtp_profiles (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL UNIQUE,
                domains_json TEXT NOT NULL,
                target_host TEXT NOT NULL,
                target_port INTEGER DEFAULT 25,
                certificate_id TEXT DEFAULT 'cert_webadmin_default',
                certificate_name TEXT DEFAULT 'Appliance Default SSL',
                enable_sni INTEGER DEFAULT 1,
                recipient_verification TEXT DEFAULT 'Callout / ActiveSync',
                spam_action TEXT DEFAULT 'Quarantine',
                spx_enabled INTEGER DEFAULT 0,
                enabled INTEGER DEFAULT 1,
                config_json TEXT DEFAULT '{}',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 12. Time Period Definitions (Recurring / Single)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS time_objects (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL UNIQUE,
                type TEXT DEFAULT 'Recurring',
                days_json TEXT DEFAULT '["mon","tue","wed","thu","fri"]',
                start_time TEXT DEFAULT '08:00',
                end_time TEXT DEFAULT '17:00',
                start_date TEXT DEFAULT '',
                end_date TEXT DEFAULT '',
                comment TEXT DEFAULT '',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 13. Authentication Servers (AD / LDAP / RADIUS / TACACS+)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS auth_servers (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL UNIQUE,
                type TEXT DEFAULT 'Active Directory',
                host TEXT NOT NULL,
                port INTEGER DEFAULT 389,
                ssl_enabled INTEGER DEFAULT 0,
                base_dn TEXT DEFAULT '',
                bind_dn TEXT DEFAULT '',
                bind_pw TEXT DEFAULT '',
                timeout INTEGER DEFAULT 10,
                comment TEXT DEFAULT '',
                status TEXT DEFAULT 'Online',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 14. OTP / 2FA Tokens
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS otp_tokens (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                username TEXT NOT NULL,
                secret_key TEXT NOT NULL,
                algorithm TEXT DEFAULT 'sha1',
                timestep INTEGER DEFAULT 30,
                status TEXT DEFAULT 'Active',
                scratch_codes_json TEXT DEFAULT '[]',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 15. Real Webservers (WAF Upstream Nodes)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS real_webservers (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL UNIQUE,
                host TEXT NOT NULL,
                port INTEGER DEFAULT 80,
                ssl_enabled INTEGER DEFAULT 0,
                keepalive INTEGER DEFAULT 1,
                timeout INTEGER DEFAULT 60,
                health_check_url TEXT DEFAULT '/',
                comment TEXT DEFAULT '',
                status TEXT DEFAULT 'Healthy',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 16. Interface Groups
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS interface_groups (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL UNIQUE,
                members_json TEXT NOT NULL DEFAULT '[]',
                comment TEXT DEFAULT '',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 17. QoS & Traffic Shaping Rules
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS qos_rules (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                interface TEXT DEFAULT 'eth0 (WAN Uplink)',
                traffic_selector TEXT DEFAULT 'Web Traffic (HTTP/HTTPS)',
                guaranteed_bandwidth TEXT DEFAULT '50 Mbps',
                max_bandwidth TEXT DEFAULT '100 Mbps',
                priority INTEGER DEFAULT 5,
                enabled INTEGER DEFAULT 1,
                comment TEXT DEFAULT '',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 18. Policy-Based Routes (PBR)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS policy_routes (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                source_network TEXT DEFAULT 'Any',
                destination_network TEXT DEFAULT 'Any',
                service TEXT DEFAULT 'Any',
                gateway TEXT NOT NULL,
                interface TEXT DEFAULT 'eth0 (WAN)',
                metric INTEGER DEFAULT 10,
                enabled INTEGER DEFAULT 1,
                comment TEXT DEFAULT '',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 19. Email Encryption & User Certificates (S/MIME / OpenPGP)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS email_certificates (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                user_id TEXT DEFAULT '',
                email TEXT NOT NULL,
                type TEXT DEFAULT 'S/MIME',
                fingerprint TEXT DEFAULT '',
                expires_at TEXT DEFAULT '',
                has_private_key INTEGER DEFAULT 0,
                comment TEXT DEFAULT '',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()
        _seed_initial_defaults(conn)

def _seed_initial_defaults(conn: sqlite3.Connection):
    """Seed initial defaults if tables are empty."""
    cursor = conn.cursor()

    # Seed Firewall Rules
    cursor.execute("SELECT COUNT(*) FROM firewall_rules")
    if cursor.fetchone()[0] == 0:
        default_fw = [
            ("1", "Allow Internal Web Traffic", "LAN", "Network", "192.168.1.0/24", "WAN", "Any", "Any", "Web Services (HTTP/HTTPS)", "accept", 1, "Permits internal LAN outbound internet web surfing", 1),
            ("2", "Allow Internal DNS Resolution", "LAN", "Network", "192.168.1.0/24", "WAN", "Any", "Any", "DNS (UDP/TCP 53)", "accept", 1, "Forward internal DNS lookups to public root resolvers", 2),
            ("3", "Allow Secure Admin SSH Access", "LAN", "Host", "192.168.1.50", "LAN", "Host", "192.168.1.1", "SSH", "accept", 1, "Administrative console SSH terminal access", 3),
            ("4", "Allow WireGuard Teleworker Mesh", "WAN", "Any", "Any", "LAN", "Host", "192.168.1.1", "WireGuard", "accept", 1, "WireGuard VPN site-to-site and mobile tunnels", 4),
            ("5", "Drop Inbound Unsolicited WAN", "WAN", "Any", "Any", "LAN", "Any", "Any", "Any", "drop", 1, "Default drop for unsolicited inbound external traffic", 5)
        ]
        cursor.executemany("""
            INSERT INTO firewall_rules (id, name, src_zone, source_type, source_value, dest_zone, dest_type, dest_value, services, action, enabled, comment, seq_order)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, default_fw)

    # Seed NAT Rules
    cursor.execute("SELECT COUNT(*) FROM nat_rules")
    if cursor.fetchone()[0] == 0:
        default_nat = [
            ("nat-1", "Default Masquerading (LAN to WAN)", "Masquerading", 1, "Internal (Network)", "Uplink Interfaces (WAN)", "Any", "Uplink (WAN IP)", "", "", 1, "Outbound SNAT for all internal clients"),
            ("nat-2", "Port Forward HTTPS to Webserver", "DNAT", 1, "Any", "ens33", "HTTPS", "Uplink (WAN IP)", "192.168.1.100", "443", 1, "Forwards external HTTPS requests to internal DMZ server"),
            ("nat-3", "Port Forward SSH to Jumpbox", "DNAT", 1, "Any", "ens33", "SSH", "Uplink (WAN IP)", "192.168.1.10", "22", 1, "External SSH access to internal jumpbox")
        ]
        cursor.executemany("""
            INSERT INTO nat_rules (id, name, type, enabled, source_network, outbound_interface, traffic_service, traffic_destination, destination_nat_target, service_translation, auto_firewall_rule, comment)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, default_nat)

    # Seed Network Objects
    cursor.execute("SELECT COUNT(*) FROM network_objects")
    if cursor.fetchone()[0] == 0:
        default_nets = [
            ("net-1", "Internal (Network)", "Network", "192.168.1.0", "/24 (255.255.255.0)", "", "", "Internal LAN client subnet", "LAN"),
            ("net-2", "DMZ Network", "Network", "192.168.10.0", "/24 (255.255.255.0)", "", "", "Public facing server DMZ zone", "DMZ"),
            ("net-3", "Branch Office Subnet", "Network", "10.0.0.0", "/16 (255.255.0.0)", "", "", "Remote Site-to-Site VPN subnet", "<< Any >>"),
            ("net-4", "Primary Domain Controller", "Host", "192.168.1.10", "", "", "", "Active Directory & DNS Server", "LAN"),
            ("net-5", "Public DNS Resolvers", "Network group", "1.1.1.1, 8.8.8.8, 9.9.9.9", "", "", "", "Trusted public DNS resolvers", "<< Any >>"),
            ("net-6", "DHCP Reservation Range", "Range", "", "", "192.168.1.100", "192.168.1.200", "Dynamic client IP pool", "LAN"),
            ("net-7", "Cloud Gateway FQDN", "DNS host", "gateway.cloud.astaro.net", "", "", "", "Dynamic cloud tunnel endpoint", "<< Any >>")
        ]
        cursor.executemany("""
            INSERT INTO network_objects (id, name, type, address, netmask, from_ip, to_ip, comment, interface)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, default_nets)

    # Seed Service Objects
    cursor.execute("SELECT COUNT(*) FROM service_objects")
    if cursor.fetchone()[0] == 0:
        default_srvs = [
            ("srv-1", "HTTP", "TCP", "TCP", "80", "1:65535", "Standard Web HTTP traffic"),
            ("srv-2", "HTTPS", "TCP", "TCP", "443", "1:65535", "Secure TLS/SSL Web traffic"),
            ("srv-3", "DNS", "UDP", "UDP", "53", "1:65535", "Domain Name System resolution"),
            ("srv-4", "SSH", "TCP", "TCP", "22", "1:65535", "Secure Shell remote terminal access"),
            ("srv-5", "WireGuard", "UDP", "UDP", "51820", "1:65535", "WireGuard VPN tunnel protocol"),
            ("srv-6", "WebAdmin HTTPS", "TCP", "TCP", "4444", "1:65535", "Astaro-Next WebAdmin management console"),
            ("srv-7", "SMTP", "TCP", "TCP", "25", "1:65535", "Simple Mail Transfer Protocol")
        ]
        cursor.executemany("""
            INSERT INTO service_objects (id, name, type, protocol, dst_port, src_port, comment)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, default_srvs)

    # Seed Users
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        default_users = [
            ("usr-1", "admin", "Administrator", "admin@astaro.local", "Administrator", "Active", "Local Database", "2026-08-01 00:00:00"),
            ("usr-2", "sec-auditor", "Security Auditor", "auditor@astaro.local", "Read-Only Auditor", "Active", "Local Database", "2026-08-10 12:00:00"),
            ("usr-3", "vpn-user1", "Remote Engineer", "engineer@astaro.local", "VPN User", "Active", "Local Database", "2026-08-15 08:30:00")
        ]
        cursor.executemany("""
            INSERT INTO users (id, username, real_name, email, role, status, auth_backend, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, default_users)

    # Seed Static Routes
    cursor.execute("SELECT COUNT(*) FROM routes")
    if cursor.fetchone()[0] == 0:
        default_routes = [
            ("rt-1", "0.0.0.0/0", "192.168.1.254", "ens33 (WAN)", 1, "Default Gateway", "Default outbound default route via WAN ISP uplink", 1),
            ("rt-2", "10.100.0.0/16", "192.168.1.2", "ens34 (LAN)", 10, "Static", "Branch Office interconnect via internal core switch", 1),
            ("rt-3", "172.16.0.0/12", "192.168.1.3", "ens34 (LAN)", 20, "Static", "Corporate Datacenter trunk route", 1)
        ]
        cursor.executemany("""
            INSERT INTO routes (id, destination, gateway, interface, metric, route_type, comment, enabled)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, default_routes)

    # Seed WAF Rules
    cursor.execute("SELECT COUNT(*) FROM waf_rules")
    if cursor.fetchone()[0] == 0:
        default_waf = [
            ("waf-1", "Main Corporate Portal", "portal.company.com", "http://192.168.1.100:80", 1, "blocking", "SQLi, XSS, RCE, Protocol Violations", "2026-08-01 10:00:00"),
            ("waf-2", "Customer API Gateway", "api.company.com", "http://192.168.1.105:8080", 1, "blocking", "SQLi, XSS, RCE, Rate-Limiting", "2026-08-05 14:20:00")
        ]
        cursor.executemany("""
            INSERT INTO waf_rules (id, name, domain, upstream, ssl_enabled, waf_mode, rule_packs, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, default_waf)

    # Seed VPN Tunnels
    cursor.execute("SELECT COUNT(*) FROM vpn_tunnels")
    if cursor.fetchone()[0] == 0:
        default_tunnels = [
            ("tun-1", "HQ to Branch Office Tunnel", "WireGuard", "203.0.113.50:51820", "192.168.1.0/24", "10.0.0.0/24", "Pre-Shared Key (PSK)", "Connected", "4d 18h", "4.2 GB", "8.7 GB"),
            ("tun-2", "AWS VPC Direct Link", "IPsec (IKEv2)", "198.51.100.25", "192.168.1.0/24", "172.31.0.0/16", "X.509 Certificate", "Connected", "12d 4h", "18.5 GB", "31.2 GB")
        ]
        cursor.executemany("""
            INSERT INTO vpn_tunnels (id, name, type, remote_gateway, local_network, remote_network, auth_type, status, uptime, tx_bytes, rx_bytes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, default_tunnels)

    # Seed System Settings
    cursor.execute("SELECT COUNT(*) FROM key_value_store WHERE section = 'system_settings'")
    if cursor.fetchone()[0] == 0:
        sys_settings = {
            "hostname": "astaro-gateway.local",
            "domain": "astaro.local",
            "webadmin_port": 4444,
            "webadmin_allowed_networks": "192.168.1.0/24, 10.0.0.0/8",
            "ssh_enabled": True,
            "ssh_port": 22,
            "ssh_password_auth": False,
            "email_alerts_enabled": True,
            "alert_recipient": "admin@astaro.local",
            "smtp_server": "127.0.0.1",
            "telegram_alerts_enabled": False,
            "telegram_bot_token": "",
            "telegram_chat_id": ""
        }
        for k, v in sys_settings.items():
            cursor.execute("INSERT OR REPLACE INTO key_value_store (section, key, value_json) VALUES ('system_settings', ?, ?)", (k, json.dumps(v)))

    # Seed DHCP Server Settings (State preserved across updates/rebuilds)
    cursor.execute("SELECT COUNT(*) FROM key_value_store WHERE section = 'dhcp_settings'")
    if cursor.fetchone()[0] == 0:
        dhcp_defaults = {
            "enabled": True,
            "interface": "eth0",
            "range_start": "192.168.1.100",
            "range_end": "192.168.1.200",
            "gateway": "192.168.1.1",
            "dns_primary": "192.168.1.1",
            "dns_secondary": "1.1.1.1",
            "domain_name": "internal.medric.net",
            "lease_time_hours": 24,
            "ipv6_enabled": False
        }
        for k, v in dhcp_defaults.items():
            cursor.execute("INSERT OR REPLACE INTO key_value_store (section, key, value_json) VALUES ('dhcp_settings', ?, ?)", (k, json.dumps(v)))

    # Seed Backups Catalog
    cursor.execute("SELECT COUNT(*) FROM backups")
    if cursor.fetchone()[0] == 0:
        default_backups = [
            ("bk-1", "astaro-backup-factory-initial.tar.gz", "2026-08-01 00:00:00", 1482000, "2.4.0", "Factory default installation snapshot"),
            ("bk-2", "astaro-backup-pre-update-v2.3.tar.gz", "2026-08-15 18:30:00", 2154000, "2.3.9", "Pre-upgrade system state backup")
        ]
        cursor.executemany("""
            INSERT INTO backups (id, filename, created_at, size_bytes, version, notes)
            VALUES (?, ?, ?, ?, ?, ?)
        """, default_backups)

    # Seed Time Objects
    cursor.execute("SELECT COUNT(*) FROM time_objects")
    if cursor.fetchone()[0] == 0:
        default_times = [
            ("time-1", "Working Hours", "Recurring", '["mon","tue","wed","thu","fri"]', "08:00", "17:00", "", "", "Standard business working hours (Mon-Fri 8am-5pm)"),
            ("time-2", "Weekend Off-Peak", "Recurring", '["sat","sun"]', "00:00", "23:59", "", "", "Weekend maintenance and off-peak window"),
            ("time-3", "Annual Maintenance Window", "Single", '[]', "22:00", "04:00", "2026-12-24", "2026-12-25", "Scheduled emergency holiday maintenance window")
        ]
        cursor.executemany("""
            INSERT INTO time_objects (id, name, type, days_json, start_time, end_time, start_date, end_date, comment)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, default_times)

    # Seed Auth Servers
    cursor.execute("SELECT COUNT(*) FROM auth_servers")
    if cursor.fetchone()[0] == 0:
        default_auth = [
            ("auth-1", "HQ Active Directory", "Active Directory", "192.168.1.10", 389, 0, "dc=corp,dc=astaro,dc=net", "cn=Administrator,cn=Users,dc=corp,dc=astaro,dc=net", "", 10, "Primary enterprise domain controller for SSO & User Portal", "Online"),
            ("auth-2", "Radius MFA Server", "RADIUS", "192.168.1.25", 1812, 0, "", "", "", 5, "Secondary RADIUS authentication server for VPN tunnels", "Online")
        ]
        cursor.executemany("""
            INSERT INTO auth_servers (id, name, type, host, port, ssl_enabled, base_dn, bind_dn, bind_pw, timeout, comment, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, default_auth)

    # Seed Real Webservers
    cursor.execute("SELECT COUNT(*) FROM real_webservers")
    if cursor.fetchone()[0] == 0:
        default_reals = [
            ("real-1", "Internal Intranet App", "192.168.1.100", 8080, 0, 1, 60, "/health", "Production backend microservice cluster", "Healthy"),
            ("real-2", "Nextcloud Storage Node", "192.168.1.105", 443, 1, 1, 120, "/status.php", "Enterprise file sharing backend", "Healthy")
        ]
        cursor.executemany("""
            INSERT INTO real_webservers (id, name, host, port, ssl_enabled, keepalive, timeout, health_check_url, comment, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, default_reals)

    # Seed Interface Groups
    cursor.execute("SELECT COUNT(*) FROM interface_groups")
    if cursor.fetchone()[0] == 0:
        default_if_groups = [
            ("ifg-1", "Internal Interfaces", '["eth1 (LAN)", "vlan10 (VoIP)"]', "Aggregate group of internal trusted network interfaces"),
            ("ifg-2", "Uplink Interfaces", '["eth0 (WAN Uplink)"]', "All public-facing Internet gateway interfaces")
        ]
        cursor.executemany("""
            INSERT INTO interface_groups (id, name, members_json, comment)
            VALUES (?, ?, ?, ?)
        """, default_if_groups)

    # Seed QoS Rules
    cursor.execute("SELECT COUNT(*) FROM qos_rules")
    if cursor.fetchone()[0] == 0:
        default_qos = [
            ("qos-1", "Prioritize VoIP & Telephony", "eth0 (WAN Uplink)", "VoIP SIP / RTP (UDP 5060, 10000-20000)", "20 Mbps", "50 Mbps", 8, 1, "Guarantees low latency and jitter for voice calls"),
            ("qos-2", "Throttle Bulk File Transfers & P2P", "eth0 (WAN Uplink)", "P2P / Torrent Traffic", "1 Mbps", "5 Mbps", 1, 1, "Caps non-essential bulk bandwidth consumption")
        ]
        cursor.executemany("""
            INSERT INTO qos_rules (id, name, interface, traffic_selector, guaranteed_bandwidth, max_bandwidth, priority, enabled, comment)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, default_qos)

    # Seed Policy Routes
    cursor.execute("SELECT COUNT(*) FROM policy_routes")
    if cursor.fetchone()[0] == 0:
        default_pbr = [
            ("pbr-1", "Route Guest Wi-Fi via Secondary WAN", "Guest Wi-Fi Subnet (192.168.20.0/24)", "Any", "Any", "198.51.100.1", "eth2 (WAN Backup)", 5, 1, "Directs non-critical guest traffic away from primary business fiber"),
            ("pbr-2", "Direct Corporate VPN via MPLS Gateway", "Internal (Network)", "Branch Office Subnet", "Any", "10.254.0.1", "eth1 (LAN)", 10, 1, "Forces inter-branch corporate traffic over dedicated private circuit")
        ]
        cursor.executemany("""
            INSERT INTO policy_routes (id, name, source_network, destination_network, service, gateway, interface, metric, enabled, comment)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, default_pbr)

    # Seed Email Certificates
    cursor.execute("SELECT COUNT(*) FROM email_certificates")
    if cursor.fetchone()[0] == 0:
        default_email_certs = [
            ("cert-em-1", "Admin Corporate S/MIME Key", "usr-1", "admin@astaro.local", "S/MIME", "9A:8B:7C:6D:5E:4F:3A:2B:1C:0D", "2027-12-31", 1, "Master administrative certificate for email signing and decryption"),
            ("cert-em-2", "SecOps OpenPGP Public Key", "usr-2", "secops@corp.astaro.net", "OpenPGP", "E4:5A:23:BC:78:90:12:34:56:78", "2028-06-30", 0, "Public key for automated security advisory distribution")
        ]
        cursor.executemany("""
            INSERT INTO email_certificates (id, name, user_id, email, type, fingerprint, expires_at, has_private_key, comment)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, default_email_certs)

    conn.commit()

# =============================================================================
# Helper Query Methods for REST Endpoints
# =============================================================================

# --- Firewall Rules ---
def db_get_firewall_rules() -> List[Dict[str, Any]]:
    with get_db_connection() as conn:
        rows = conn.execute("SELECT * FROM firewall_rules ORDER BY seq_order ASC, id ASC").fetchall()
        return [dict(r) for r in rows]

def db_save_firewall_rule(rule_dict: Dict[str, Any]) -> Dict[str, Any]:
    with get_db_connection() as conn:
        rid = str(rule_dict.get("id") or "")
        if not rid:
            # Auto-generate next numeric ID
            max_id = conn.execute("SELECT MAX(CAST(id AS INTEGER)) FROM firewall_rules").fetchone()[0] or 0
            rid = str(max_id + 1)
            rule_dict["id"] = rid

        seq = rule_dict.get("seq_order", 0)
        conn.execute("""
            INSERT OR REPLACE INTO firewall_rules (id, name, src_zone, source_type, source_value, dest_zone, dest_type, dest_value, services, action, enabled, comment, seq_order)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            rid,
            rule_dict.get("name", "Unnamed Rule"),
            rule_dict.get("src_zone", "LAN"),
            rule_dict.get("source_type", "Any"),
            rule_dict.get("source_value", "Any"),
            rule_dict.get("dest_zone", "WAN"),
            rule_dict.get("dest_type", "Any"),
            rule_dict.get("dest_value", "Any"),
            rule_dict.get("services", "Any"),
            rule_dict.get("action", "accept"),
            1 if rule_dict.get("enabled", True) else 0,
            rule_dict.get("comment", ""),
            seq
        ))
        conn.commit()
        return rule_dict

def db_delete_firewall_rule(rule_id: str) -> bool:
    with get_db_connection() as conn:
        cur = conn.execute("DELETE FROM firewall_rules WHERE id = ?", (str(rule_id),))
        conn.commit()
        return cur.rowcount > 0

def db_reorder_firewall_rules(ordered_ids: List[str]):
    with get_db_connection() as conn:
        for idx, rid in enumerate(ordered_ids, start=1):
            conn.execute("UPDATE firewall_rules SET seq_order = ? WHERE id = ?", (idx, str(rid)))
        conn.commit()

# --- NAT Rules ---
def db_get_nat_rules() -> List[Dict[str, Any]]:
    with get_db_connection() as conn:
        rows = conn.execute("SELECT * FROM nat_rules ORDER BY id ASC").fetchall()
        return [dict(r) for r in rows]

def db_save_nat_rule(rule_dict: Dict[str, Any]) -> Dict[str, Any]:
    with get_db_connection() as conn:
        rid = str(rule_dict.get("id") or "")
        if not rid:
            max_id = conn.execute("SELECT COUNT(*) FROM nat_rules").fetchone()[0] or 0
            rid = f"nat-{max_id + 1}"
            rule_dict["id"] = rid

        conn.execute("""
            INSERT OR REPLACE INTO nat_rules (id, name, type, enabled, source_network, outbound_interface, traffic_service, traffic_destination, destination_nat_target, service_translation, auto_firewall_rule, comment)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            rid,
            rule_dict.get("name", "Unnamed NAT"),
            rule_dict.get("type", "Masquerading"),
            1 if rule_dict.get("enabled", True) else 0,
            rule_dict.get("source_network", "Internal (Network)"),
            rule_dict.get("outbound_interface", "Uplink Interfaces (WAN)"),
            rule_dict.get("traffic_service", "HTTPS"),
            rule_dict.get("traffic_destination", "Uplink (WAN IP)"),
            rule_dict.get("destination_nat_target", ""),
            rule_dict.get("service_translation", ""),
            1 if rule_dict.get("auto_firewall_rule", True) else 0,
            rule_dict.get("comment", "")
        ))
        conn.commit()
        return rule_dict

def db_delete_nat_rule(rule_id: str) -> bool:
    with get_db_connection() as conn:
        cur = conn.execute("DELETE FROM nat_rules WHERE id = ?", (str(rule_id),))
        conn.commit()
        return cur.rowcount > 0

# --- Network Objects ---
def db_get_network_objects() -> List[Dict[str, Any]]:
    with get_db_connection() as conn:
        rows = conn.execute("SELECT * FROM network_objects ORDER BY name ASC").fetchall()
        return [dict(r) for r in rows]

def db_save_network_object(obj_dict: Dict[str, Any]) -> Dict[str, Any]:
    with get_db_connection() as conn:
        oid = str(obj_dict.get("id") or "")
        if not oid:
            count = conn.execute("SELECT COUNT(*) FROM network_objects").fetchone()[0] or 0
            oid = f"net-{count + 1}"
            obj_dict["id"] = oid

        conn.execute("""
            INSERT OR REPLACE INTO network_objects (id, name, type, address, netmask, from_ip, to_ip, comment, interface)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            oid,
            obj_dict.get("name", ""),
            obj_dict.get("type", "Host"),
            obj_dict.get("address", ""),
            obj_dict.get("netmask", "/24 (255.255.255.0)"),
            obj_dict.get("from_ip", ""),
            obj_dict.get("to_ip", ""),
            obj_dict.get("comment", ""),
            obj_dict.get("interface", "<< Any >>")
        ))
        conn.commit()
        return obj_dict

def db_delete_network_object(net_id: str) -> bool:
    with get_db_connection() as conn:
        cur = conn.execute("DELETE FROM network_objects WHERE id = ?", (str(net_id),))
        conn.commit()
        return cur.rowcount > 0

# --- Service Objects ---
def db_get_service_objects() -> List[Dict[str, Any]]:
    with get_db_connection() as conn:
        rows = conn.execute("SELECT * FROM service_objects ORDER BY name ASC").fetchall()
        return [dict(r) for r in rows]

def db_save_service_object(obj_dict: Dict[str, Any]) -> Dict[str, Any]:
    with get_db_connection() as conn:
        sid = str(obj_dict.get("id") or "")
        if not sid:
            count = conn.execute("SELECT COUNT(*) FROM service_objects").fetchone()[0] or 0
            sid = f"srv-{count + 1}"
            obj_dict["id"] = sid

        conn.execute("""
            INSERT OR REPLACE INTO service_objects (id, name, type, protocol, dst_port, src_port, comment)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            sid,
            obj_dict.get("name", ""),
            obj_dict.get("type", "TCP"),
            obj_dict.get("protocol", "TCP"),
            obj_dict.get("dst_port", ""),
            obj_dict.get("src_port", "1:65535"),
            obj_dict.get("comment", "")
        ))
        conn.commit()
        return obj_dict

def db_delete_service_object(srv_id: str) -> bool:
    with get_db_connection() as conn:
        cur = conn.execute("DELETE FROM service_objects WHERE id = ?", (str(srv_id),))
        conn.commit()
        return cur.rowcount > 0

# --- Routes (Static & Policy) ---
def db_get_routes() -> List[Dict[str, Any]]:
    with get_db_connection() as conn:
        rows = conn.execute("SELECT * FROM routes ORDER BY metric ASC, destination ASC").fetchall()
        return [dict(r) for r in rows]

def db_save_route(route_dict: Dict[str, Any]) -> Dict[str, Any]:
    with get_db_connection() as conn:
        rid = str(route_dict.get("id") or "")
        if not rid:
            count = conn.execute("SELECT COUNT(*) FROM routes").fetchone()[0] or 0
            rid = f"rt-{count + 1}"
            route_dict["id"] = rid

        conn.execute("""
            INSERT OR REPLACE INTO routes (id, destination, gateway, interface, metric, route_type, comment, enabled)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            rid,
            route_dict.get("destination", "0.0.0.0/0"),
            route_dict.get("gateway", ""),
            route_dict.get("interface", "Any"),
            int(route_dict.get("metric", 10)),
            route_dict.get("route_type", "Static"),
            route_dict.get("comment", ""),
            1 if route_dict.get("enabled", True) else 0
        ))
        conn.commit()
        return route_dict

def db_delete_route(route_id: str) -> bool:
    with get_db_connection() as conn:
        cur = conn.execute("DELETE FROM routes WHERE id = ?", (str(route_id),))
        conn.commit()
        return cur.rowcount > 0

# --- WAF Rules ---
def db_get_waf_rules() -> List[Dict[str, Any]]:
    with get_db_connection() as conn:
        rows = conn.execute("SELECT * FROM waf_rules ORDER BY name ASC").fetchall()
        return [dict(r) for r in rows]

def db_save_waf_rule(rule_dict: Dict[str, Any]) -> Dict[str, Any]:
    with get_db_connection() as conn:
        rid = str(rule_dict.get("id") or f"waf-{rule_dict.get('name', 'unnamed')}")
        conn.execute("""
            INSERT OR REPLACE INTO waf_rules (id, name, domain, upstream, ssl_enabled, certificate_id, certificate_name, enable_sni, waf_mode, rule_packs)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            rid,
            rule_dict.get("name", "Unnamed App"),
            rule_dict.get("domain", "app.local"),
            rule_dict.get("upstream", "http://127.0.0.1:8080"),
            1 if rule_dict.get("ssl_enabled", True) else 0,
            rule_dict.get("certificate_id", "cert_webadmin_default"),
            rule_dict.get("certificate_name", "Appliance Default SSL"),
            1 if rule_dict.get("enable_sni", True) else 0,
            rule_dict.get("waf_mode", "blocking"),
            rule_dict.get("rule_packs", "SQLi, XSS, RCE")
        ))
        conn.commit()
        return rule_dict

def db_delete_waf_rule(rule_name: str) -> bool:
    with get_db_connection() as conn:
        cur = conn.execute("DELETE FROM waf_rules WHERE name = ? OR id = ?", (str(rule_name), str(rule_name)))
        conn.commit()
        return cur.rowcount > 0

# --- VPN Tunnels ---
def db_get_vpn_tunnels() -> List[Dict[str, Any]]:
    with get_db_connection() as conn:
        rows = conn.execute("SELECT * FROM vpn_tunnels ORDER BY name ASC").fetchall()
        return [dict(r) for r in rows]

def db_save_vpn_tunnel(tun_dict: Dict[str, Any]) -> Dict[str, Any]:
    with get_db_connection() as conn:
        tid = str(tun_dict.get("id") or f"tun-{tun_dict.get('name', 'site')}")
        conn.execute("""
            INSERT OR REPLACE INTO vpn_tunnels (id, name, type, remote_gateway, local_network, remote_network, auth_type, status, uptime, tx_bytes, rx_bytes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            tid,
            tun_dict.get("name", "Site-to-Site"),
            tun_dict.get("type", "WireGuard"),
            tun_dict.get("remote_gateway", ""),
            tun_dict.get("local_network", "192.168.1.0/24"),
            tun_dict.get("remote_network", "10.0.0.0/24"),
            tun_dict.get("auth_type", "Pre-Shared Key (PSK)"),
            tun_dict.get("status", "Connected"),
            tun_dict.get("uptime", "Just now"),
            tun_dict.get("tx_bytes", "0 B"),
            tun_dict.get("rx_bytes", "0 B")
        ))
        
        # If auto_firewall_rule is requested, automatically provision bi-directional firewall rule
        if tun_dict.get("auto_firewall_rule", True):
            fw_id = f"fw-vpn-{tid}"
            tun_name = tun_dict.get("name", "VPN Tunnel")
            conn.execute("""
                INSERT OR REPLACE INTO firewall_rules (id, name, src_zone, source_type, source_value, dest_zone, dest_type, dest_value, services, action, enabled, comment)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                fw_id,
                f"VPN: {tun_name} (Auto-Permit)",
                "VPN",
                "Network",
                tun_dict.get("remote_network", "Any"),
                "LAN",
                "Network",
                tun_dict.get("local_network", "192.168.1.0/24"),
                "Any",
                "accept",
                1,
                f"Automatically generated rule for Site-to-Site VPN '{tun_name}'"
            ))

        # If remote_network is provided, also register policy route in routes table
        rem_net = tun_dict.get("remote_network", "")
        if rem_net and rem_net != "Any":
            route_id = f"route-vpn-{tid}"
            conn.execute("""
                INSERT OR REPLACE INTO routes (id, destination, gateway, interface, metric, route_type, comment, enabled)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                route_id,
                rem_net,
                tun_dict.get("remote_gateway") or "VPN Gateway",
                f"vpn-{tun_dict.get('type', 'tun').lower()}",
                10,
                "VPN Tunnel Route",
                f"Dynamic route via {tun_dict.get('name', 'VPN')}",
                1
            ))

        conn.commit()
        return tun_dict

def db_delete_vpn_tunnel(tunnel_id: str) -> bool:
    with get_db_connection() as conn:
        cur = conn.execute("DELETE FROM vpn_tunnels WHERE id = ? OR name = ?", (str(tunnel_id), str(tunnel_id)))
        conn.commit()
        return cur.rowcount > 0

# --- Users ---
def db_get_users() -> List[Dict[str, Any]]:
    with get_db_connection() as conn:
        rows = conn.execute("SELECT * FROM users ORDER BY username ASC").fetchall()
        return [dict(r) for r in rows]

def db_save_user(user_dict: Dict[str, Any]) -> Dict[str, Any]:
    with get_db_connection() as conn:
        uid = str(user_dict.get("id") or "")
        if not uid:
            count = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0] or 0
            uid = f"usr-{count + 1}"
            user_dict["id"] = uid

        conn.execute("""
            INSERT OR REPLACE INTO users (id, username, real_name, email, role, status, auth_backend)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            uid,
            user_dict.get("username", "user"),
            user_dict.get("real_name", ""),
            user_dict.get("email", ""),
            user_dict.get("role", "User"),
            user_dict.get("status", "Active"),
            user_dict.get("auth_backend", "Local Database")
        ))
        conn.commit()
        return user_dict

def db_delete_user(user_id: str) -> bool:
    with get_db_connection() as conn:
        cur = conn.execute("DELETE FROM users WHERE id = ? OR username = ?", (str(user_id), str(user_id)))
        conn.commit()
        return cur.rowcount > 0

# --- Key-Value Config (System Settings, Network Services, etc.) ---
def db_get_section(section: str) -> Dict[str, Any]:
    with get_db_connection() as conn:
        rows = conn.execute("SELECT key, value_json FROM key_value_store WHERE section = ?", (section,)).fetchall()
        result = {}
        for r in rows:
            try:
                result[r["key"]] = json.loads(r["value_json"])
            except Exception:
                result[r["key"]] = r["value_json"]
        return result

def db_save_section(section: str, data: Dict[str, Any]):
    with get_db_connection() as conn:
        for k, v in data.items():
            val_str = json.dumps(v)
            conn.execute("INSERT OR REPLACE INTO key_value_store (section, key, value_json) VALUES (?, ?, ?)", (section, k, val_str))
        conn.commit()

# --- Backups Catalog ---
def db_get_backups() -> List[Dict[str, Any]]:
    with get_db_connection() as conn:
        rows = conn.execute("SELECT * FROM backups ORDER BY created_at DESC").fetchall()
        return [dict(r) for r in rows]

def db_create_backup_entry(filename: str, size_bytes: int, version: str, notes: str) -> Dict[str, Any]:
    with get_db_connection() as conn:
        count = conn.execute("SELECT COUNT(*) FROM backups").fetchone()[0] or 0
        bid = f"bk-{count + 1}"
        conn.execute("""
            INSERT INTO backups (id, filename, size_bytes, version, notes)
            VALUES (?, ?, ?, ?, ?)
        """, (bid, filename, size_bytes, version, notes))
        conn.commit()
        return {"id": bid, "filename": filename, "size_bytes": size_bytes, "version": version, "notes": notes}

def db_delete_backup(backup_id: str) -> bool:
    with get_db_connection() as conn:
        cur = conn.execute("DELETE FROM backups WHERE id = ?", (str(backup_id),))
        conn.commit()
        return cur.rowcount > 0

# --- SMTP Profiles (Email Protection Multi-Domain SNI) ---
def db_get_smtp_profiles() -> List[Dict[str, Any]]:
    with get_db_connection() as conn:
        rows = conn.execute("SELECT * FROM smtp_profiles ORDER BY name ASC").fetchall()
        results = []
        for r in rows:
            d = dict(r)
            try:
                d["domains"] = json.loads(d.get("domains_json") or "[]")
            except Exception:
                d["domains"] = []
            try:
                d["config"] = json.loads(d.get("config_json") or "{}")
            except Exception:
                d["config"] = {}
            results.append(d)
        return results

def db_save_smtp_profile(prof_dict: Dict[str, Any]) -> Dict[str, Any]:
    with get_db_connection() as conn:
        pid = str(prof_dict.get("id") or f"prof-{prof_dict.get('name', 'unnamed').lower().replace(' ', '-')}")
        domains_json = json.dumps(prof_dict.get("domains", []))
        config_json = json.dumps(prof_dict.get("config", {}))
        conn.execute("""
            INSERT OR REPLACE INTO smtp_profiles (
                id, name, domains_json, target_host, target_port,
                certificate_id, certificate_name, enable_sni,
                recipient_verification, spam_action, spx_enabled, enabled, config_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            pid,
            prof_dict.get("name", "Unnamed Profile"),
            domains_json,
            prof_dict.get("target_host", "192.168.1.50"),
            prof_dict.get("target_port", 25),
            prof_dict.get("certificate_id", "cert_webadmin_default"),
            prof_dict.get("certificate_name", "Appliance Default SSL"),
            1 if prof_dict.get("enable_sni", True) else 0,
            prof_dict.get("recipient_verification", "Callout / ActiveSync"),
            prof_dict.get("spam_action", "Quarantine"),
            1 if prof_dict.get("spx_enabled", False) else 0,
            1 if prof_dict.get("enabled", True) else 0,
            config_json
        ))
        conn.commit()
        return prof_dict

def db_delete_smtp_profile(profile_id: str) -> bool:
    with get_db_connection() as conn:
        cur = conn.execute("DELETE FROM smtp_profiles WHERE id = ? OR name = ?", (str(profile_id), str(profile_id)))
        conn.commit()
        return cur.rowcount > 0

# --- Time Period Objects ---
def db_get_time_objects() -> List[Dict[str, Any]]:
    with get_db_connection() as conn:
        rows = conn.execute("SELECT * FROM time_objects ORDER BY name ASC").fetchall()
        results = []
        for r in rows:
            d = dict(r)
            try:
                d["days"] = json.loads(d.get("days_json") or "[]")
            except Exception:
                d["days"] = []
            results.append(d)
        return results

def db_save_time_object(time_dict: Dict[str, Any]) -> Dict[str, Any]:
    with get_db_connection() as conn:
        tid = str(time_dict.get("id") or f"time-{time_dict.get('name', 'unnamed').lower().replace(' ', '-')}")
        days_json = json.dumps(time_dict.get("days", ["mon","tue","wed","thu","fri"]))
        conn.execute("""
            INSERT OR REPLACE INTO time_objects (id, name, type, days_json, start_time, end_time, start_date, end_date, comment)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            tid,
            time_dict.get("name", "Unnamed Time Period"),
            time_dict.get("type", "Recurring"),
            days_json,
            time_dict.get("start_time", "08:00"),
            time_dict.get("end_time", "17:00"),
            time_dict.get("start_date", ""),
            time_dict.get("end_date", ""),
            time_dict.get("comment", "")
        ))
        conn.commit()
        return time_dict

def db_delete_time_object(time_id: str) -> bool:
    with get_db_connection() as conn:
        cur = conn.execute("DELETE FROM time_objects WHERE id = ? OR name = ?", (str(time_id), str(time_id)))
        conn.commit()
        return cur.rowcount > 0

# --- Authentication Servers ---
def db_get_auth_servers() -> List[Dict[str, Any]]:
    with get_db_connection() as conn:
        rows = conn.execute("SELECT * FROM auth_servers ORDER BY name ASC").fetchall()
        return [dict(r) for r in rows]

def db_save_auth_server(server_dict: Dict[str, Any]) -> Dict[str, Any]:
    with get_db_connection() as conn:
        sid = str(server_dict.get("id") or f"auth-{server_dict.get('name', 'srv').lower().replace(' ', '-')}")
        conn.execute("""
            INSERT OR REPLACE INTO auth_servers (id, name, type, host, port, ssl_enabled, base_dn, bind_dn, bind_pw, timeout, comment, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            sid,
            server_dict.get("name", "Auth Server"),
            server_dict.get("type", "Active Directory"),
            server_dict.get("host", "127.0.0.1"),
            int(server_dict.get("port") or 389),
            1 if server_dict.get("ssl_enabled", False) else 0,
            server_dict.get("base_dn", ""),
            server_dict.get("bind_dn", ""),
            server_dict.get("bind_pw", ""),
            int(server_dict.get("timeout") or 10),
            server_dict.get("comment", ""),
            server_dict.get("status", "Online")
        ))
        conn.commit()
        return server_dict

def db_delete_auth_server(server_id: str) -> bool:
    with get_db_connection() as conn:
        cur = conn.execute("DELETE FROM auth_servers WHERE id = ? OR name = ?", (str(server_id), str(server_id)))
        conn.commit()
        return cur.rowcount > 0

# --- OTP / 2FA Tokens ---
def db_get_otp_tokens() -> List[Dict[str, Any]]:
    with get_db_connection() as conn:
        rows = conn.execute("SELECT * FROM otp_tokens ORDER BY username ASC").fetchall()
        results = []
        for r in rows:
            d = dict(r)
            try:
                d["scratch_codes"] = json.loads(d.get("scratch_codes_json") or "[]")
            except Exception:
                d["scratch_codes"] = []
            results.append(d)
        return results

def db_save_otp_token(otp_dict: Dict[str, Any]) -> Dict[str, Any]:
    with get_db_connection() as conn:
        oid = str(otp_dict.get("id") or f"otp-{otp_dict.get('username', 'user').lower()}")
        scratch_json = json.dumps(otp_dict.get("scratch_codes", []))
        conn.execute("""
            INSERT OR REPLACE INTO otp_tokens (id, user_id, username, secret_key, algorithm, timestep, status, scratch_codes_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            oid,
            str(otp_dict.get("user_id", "")),
            otp_dict.get("username", "admin"),
            otp_dict.get("secret_key", ""),
            otp_dict.get("algorithm", "sha1"),
            int(otp_dict.get("timestep") or 30),
            otp_dict.get("status", "Active"),
            scratch_json
        ))
        conn.commit()
        return otp_dict

def db_delete_otp_token(token_id: str) -> bool:
    with get_db_connection() as conn:
        cur = conn.execute("DELETE FROM otp_tokens WHERE id = ? OR username = ?", (str(token_id), str(token_id)))
        conn.commit()
        return cur.rowcount > 0

# --- Real Webservers ---
def db_get_real_webservers() -> List[Dict[str, Any]]:
    with get_db_connection() as conn:
        rows = conn.execute("SELECT * FROM real_webservers ORDER BY name ASC").fetchall()
        return [dict(r) for r in rows]

def db_save_real_webserver(server_dict: Dict[str, Any]) -> Dict[str, Any]:
    with get_db_connection() as conn:
        rid = str(server_dict.get("id") or f"real-{server_dict.get('name', 'srv').lower().replace(' ', '-')}")
        conn.execute("""
            INSERT OR REPLACE INTO real_webservers (id, name, host, port, ssl_enabled, keepalive, timeout, health_check_url, comment, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            rid,
            server_dict.get("name", "Real Webserver"),
            server_dict.get("host", "127.0.0.1"),
            int(server_dict.get("port") or 80),
            1 if server_dict.get("ssl_enabled", False) else 0,
            1 if server_dict.get("keepalive", True) else 0,
            int(server_dict.get("timeout") or 60),
            server_dict.get("health_check_url", "/"),
            server_dict.get("comment", ""),
            server_dict.get("status", "Healthy")
        ))
        conn.commit()
        return server_dict

def db_delete_real_webserver(server_id: str) -> bool:
    with get_db_connection() as conn:
        cur = conn.execute("DELETE FROM real_webservers WHERE id = ? OR name = ?", (str(server_id), str(server_id)))
        conn.commit()
        return cur.rowcount > 0

# --- Interface Groups ---
def db_get_interface_groups() -> List[Dict[str, Any]]:
    with get_db_connection() as conn:
        rows = conn.execute("SELECT * FROM interface_groups ORDER BY name ASC").fetchall()
        results = []
        for r in rows:
            d = dict(r)
            try:
                d["members"] = json.loads(d.get("members_json") or "[]")
            except Exception:
                d["members"] = []
            results.append(d)
        return results

def db_save_interface_group(group_dict: Dict[str, Any]) -> Dict[str, Any]:
    with get_db_connection() as conn:
        gid = str(group_dict.get("id") or f"ifg-{group_dict.get('name', 'grp').lower().replace(' ', '-')}")
        members_json = json.dumps(group_dict.get("members", []))
        conn.execute("""
            INSERT OR REPLACE INTO interface_groups (id, name, members_json, comment)
            VALUES (?, ?, ?, ?)
        """, (
            gid,
            group_dict.get("name", "Interface Group"),
            members_json,
            group_dict.get("comment", "")
        ))
        conn.commit()
        return group_dict

def db_delete_interface_group(group_id: str) -> bool:
    with get_db_connection() as conn:
        cur = conn.execute("DELETE FROM interface_groups WHERE id = ? OR name = ?", (str(group_id), str(group_id)))
        conn.commit()
        return cur.rowcount > 0

# --- QoS Rules ---
def db_get_qos_rules() -> List[Dict[str, Any]]:
    with get_db_connection() as conn:
        rows = conn.execute("SELECT * FROM qos_rules ORDER BY priority DESC, name ASC").fetchall()
        return [dict(r) for r in rows]

def db_save_qos_rule(rule_dict: Dict[str, Any]) -> Dict[str, Any]:
    with get_db_connection() as conn:
        qid = str(rule_dict.get("id") or f"qos-{rule_dict.get('name', 'rule').lower().replace(' ', '-')}")
        conn.execute("""
            INSERT OR REPLACE INTO qos_rules (id, name, interface, traffic_selector, guaranteed_bandwidth, max_bandwidth, priority, enabled, comment)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            qid,
            rule_dict.get("name", "QoS Rule"),
            rule_dict.get("interface", "eth0 (WAN Uplink)"),
            rule_dict.get("traffic_selector", "Any"),
            rule_dict.get("guaranteed_bandwidth", "10 Mbps"),
            rule_dict.get("max_bandwidth", "50 Mbps"),
            int(rule_dict.get("priority") or 5),
            1 if rule_dict.get("enabled", True) else 0,
            rule_dict.get("comment", "")
        ))
        conn.commit()
        return rule_dict

def db_delete_qos_rule(rule_id: str) -> bool:
    with get_db_connection() as conn:
        cur = conn.execute("DELETE FROM qos_rules WHERE id = ? OR name = ?", (str(rule_id), str(rule_id)))
        conn.commit()
        return cur.rowcount > 0

# --- Policy Routes (PBR) ---
def db_get_policy_routes() -> List[Dict[str, Any]]:
    with get_db_connection() as conn:
        rows = conn.execute("SELECT * FROM policy_routes ORDER BY metric ASC, name ASC").fetchall()
        return [dict(r) for r in rows]

def db_save_policy_route(pbr_dict: Dict[str, Any]) -> Dict[str, Any]:
    with get_db_connection() as conn:
        pid = str(pbr_dict.get("id") or f"pbr-{pbr_dict.get('name', 'rule').lower().replace(' ', '-')}")
        conn.execute("""
            INSERT OR REPLACE INTO policy_routes (id, name, source_network, destination_network, service, gateway, interface, metric, enabled, comment)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            pid,
            pbr_dict.get("name", "Policy Route"),
            pbr_dict.get("source_network", "Any"),
            pbr_dict.get("destination_network", "Any"),
            pbr_dict.get("service", "Any"),
            pbr_dict.get("gateway", "192.168.1.1"),
            pbr_dict.get("interface", "eth0 (WAN)"),
            int(pbr_dict.get("metric") or 10),
            1 if pbr_dict.get("enabled", True) else 0,
            pbr_dict.get("comment", "")
        ))
        conn.commit()
        return pbr_dict

def db_delete_policy_route(route_id: str) -> bool:
    with get_db_connection() as conn:
        cur = conn.execute("DELETE FROM policy_routes WHERE id = ? OR name = ?", (str(route_id), str(route_id)))
        conn.commit()
        return cur.rowcount > 0

# --- Email Encryption Certificates ---
def db_get_email_certificates() -> List[Dict[str, Any]]:
    with get_db_connection() as conn:
        rows = conn.execute("SELECT * FROM email_certificates ORDER BY email ASC").fetchall()
        return [dict(r) for r in rows]

def db_save_email_certificate(cert_dict: Dict[str, Any]) -> Dict[str, Any]:
    with get_db_connection() as conn:
        cid = str(cert_dict.get("id") or f"cert-em-{cert_dict.get('email', 'user').replace('@', '-').replace('.', '-')}")
        conn.execute("""
            INSERT OR REPLACE INTO email_certificates (id, name, user_id, email, type, fingerprint, expires_at, has_private_key, comment)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            cid,
            cert_dict.get("name", "Certificate"),
            str(cert_dict.get("user_id", "")),
            cert_dict.get("email", ""),
            cert_dict.get("type", "S/MIME"),
            cert_dict.get("fingerprint", ""),
            cert_dict.get("expires_at", "2027-12-31"),
            1 if cert_dict.get("has_private_key", False) else 0,
            cert_dict.get("comment", "")
        ))
        conn.commit()
        return cert_dict

def db_delete_email_certificate(cert_id: str) -> bool:
    with get_db_connection() as conn:
        cur = conn.execute("DELETE FROM email_certificates WHERE id = ? OR email = ?", (str(cert_id), str(cert_id)))
        conn.commit()
        return cur.rowcount > 0

# Initialize schema immediately on import
init_database()
