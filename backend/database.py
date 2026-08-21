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

# Initialize schema immediately on import
init_database()
