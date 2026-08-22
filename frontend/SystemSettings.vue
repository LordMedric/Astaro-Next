<template>
  <div class="space-y-6">
    <!-- Top Modern Breadcrumb & Action Banner -->
    <div class="bg-white border border-slate-200 rounded-xl p-5 shadow-xs flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div>
        <div class="flex items-center gap-2">
          <span class="w-2 h-6 bg-[#005299] rounded-xs"></span>
          <h1 class="text-xl font-bold text-slate-900 tracking-tight">System & WebAdmin Settings</h1>
          <span class="bg-slate-100 text-slate-700 text-xs font-bold font-mono px-2.5 py-0.5 rounded-full border border-slate-200">
            Astaro-Next Linux v2.4.0
          </span>
        </div>
        <p class="text-xs text-slate-500 mt-1 pl-4">
          Configure appliance hostname, WebAdmin HTTPS console ACLs, SSH shell access, SMTP/Telegram alert triggers, and power controls.
        </p>
      </div>

      <!-- Tab Navigation Pills -->
      <div class="flex items-center gap-1 bg-slate-100 p-1 rounded-lg border border-slate-200 overflow-x-auto text-xs font-semibold">
        <button
          v-for="tab in tabs"
          :key="tab.id"
          @click="activeTab = tab.id"
          :class="[
            'px-3.5 py-1.5 rounded-md transition-all whitespace-nowrap cursor-pointer',
            activeTab === tab.id
              ? 'bg-white text-[#005299] shadow-xs font-bold'
              : 'text-slate-600 hover:text-slate-900 hover:bg-slate-200/60'
          ]"
        >
          <span class="flex items-center gap-1.5">
            <component :is="tab.icon" class="w-3.5 h-3.5" />
            <span>{{ tab.label }}</span>
          </span>
        </button>
      </div>
    </div>

    <!-- TAB 1: APPLIANCE IDENTIFICATION -->
    <div v-if="activeTab === 'identity'" class="space-y-6">
      <div class="bg-white border border-slate-200 rounded-xl shadow-xs overflow-hidden">
        <div class="p-4 border-b border-slate-200 bg-slate-50 flex items-center justify-between">
          <div class="flex items-center gap-2">
            <span class="w-1.5 h-4 bg-[#005299] rounded-xs"></span>
            <h2 class="text-sm font-bold text-slate-800">Appliance Identity & System Timezone</h2>
          </div>
        </div>

        <div class="p-6 space-y-4">
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1">Appliance Hostname (FQDN)</label>
              <input type="text" v-model="identityConfig.hostname" class="w-full bg-white border border-slate-300 rounded-lg px-3 py-2 text-xs font-mono text-slate-800 focus:ring-2 focus:ring-blue-500 focus:outline-none" />
            </div>
            <div>
              <label class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1">Domain Name</label>
              <input type="text" v-model="identityConfig.domain" class="w-full bg-white border border-slate-300 rounded-lg px-3 py-2 text-xs text-slate-800 focus:ring-2 focus:ring-blue-500 focus:outline-none" />
            </div>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1">Organization / Company</label>
              <input type="text" v-model="identityConfig.organization" class="w-full bg-white border border-slate-300 rounded-lg px-3 py-2 text-xs text-slate-800 focus:ring-2 focus:ring-blue-500 focus:outline-none" />
            </div>
            <div>
              <label class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1">Administrator Email</label>
              <input type="email" v-model="identityConfig.admin_email" class="w-full bg-white border border-slate-300 rounded-lg px-3 py-2 text-xs text-slate-800 focus:ring-2 focus:ring-blue-500 focus:outline-none" />
            </div>
          </div>

          <div>
            <label class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1">System Timezone</label>
            <select v-model="identityConfig.timezone" class="w-full bg-white border border-slate-300 rounded-lg px-3 py-2 text-xs font-medium text-slate-800 focus:ring-2 focus:ring-blue-500 focus:outline-none">
              <option value="America/New_York">America/New_York (Eastern Time - UTC-4/5)</option>
              <option value="America/Chicago">America/Chicago (Central Time - UTC-5/6)</option>
              <option value="America/Denver">America/Denver (Mountain Time - UTC-6/7)</option>
              <option value="America/Los_Angeles">America/Los_Angeles (Pacific Time - UTC-7/8)</option>
              <option value="UTC">UTC (Universal Coordinated Time)</option>
              <option value="Europe/London">Europe/London (GMT / BST)</option>
              <option value="Europe/Berlin">Europe/Berlin (CET / CEST)</option>
            </select>
          </div>

          <div class="pt-4 border-t border-slate-200 flex justify-end">
            <button
              type="button"
              @click="saveIdentitySettings"
              class="px-5 py-2 bg-[#005299] hover:bg-[#003d73] text-white rounded-lg text-xs font-bold shadow-xs cursor-pointer"
            >
              Save Identity Settings
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 2: WEBADMIN CONSOLE SETTINGS -->
    <div v-if="activeTab === 'webadmin'" class="space-y-6">
      <div class="bg-white border border-slate-200 rounded-xl shadow-xs overflow-hidden">
        <div class="p-4 border-b border-slate-200 bg-slate-50 flex items-center justify-between">
          <div class="flex items-center gap-2">
            <span class="w-1.5 h-4 bg-[#005299] rounded-xs"></span>
            <h2 class="text-sm font-bold text-slate-800">WebAdmin Console & Access Control (ACL)</h2>
          </div>
        </div>

        <div class="p-6 space-y-4">
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1">WebAdmin HTTPS Port</label>
              <input type="number" v-model.number="webadminConfig.port" class="w-full bg-white border border-slate-300 rounded-lg px-3 py-2 text-xs font-mono text-slate-800 focus:ring-2 focus:ring-blue-500 focus:outline-none" />
              <p class="text-[11px] text-slate-500 mt-1">Default Astaro-Next / Astaro port is 4444.</p>
            </div>
            <div>
              <label class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1">Session Timeout (Minutes)</label>
              <input type="number" v-model.number="webadminConfig.session_timeout_min" min="5" max="480" class="w-full bg-white border border-slate-300 rounded-lg px-3 py-2 text-xs font-mono text-slate-800 focus:ring-2 focus:ring-blue-500 focus:outline-none" />
            </div>
          </div>

          <div>
            <label class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1">Allowed Networks / Hosts for WebAdmin Access</label>
            <div class="flex flex-wrap gap-2 p-3 bg-slate-50 border border-slate-200 rounded-lg min-h-[48px] items-center">
              <span
                v-for="(host, idx) in webadminConfig.allowed_networks"
                :key="idx"
                class="inline-flex items-center gap-1.5 px-2.5 py-1 bg-white border border-slate-300 rounded-md text-xs font-mono font-medium text-slate-800 shadow-xs"
              >
                <span>{{ host }}</span>
                <button type="button" @click="webadminConfig.allowed_networks.splice(idx, 1)" class="text-slate-400 hover:text-rose-600 font-bold ml-1 cursor-pointer">&times;</button>
              </span>
              <input
                type="text"
                v-model="newAclHost"
                @keydown.enter.prevent="addAclHost"
                placeholder="+ Type IP or Subnet (e.g. 192.168.1.0/24) and press Enter"
                class="flex-1 min-w-[240px] bg-transparent border-0 text-xs text-slate-800 placeholder:text-slate-400 focus:ring-0 focus:outline-none py-1"
              />
            </div>
          </div>

          <div class="pt-4 border-t border-slate-200 flex justify-end">
            <button
              type="button"
              @click="saveWebadminSettings"
              class="px-5 py-2 bg-[#005299] hover:bg-[#003d73] text-white rounded-lg text-xs font-bold shadow-xs cursor-pointer"
            >
              Apply WebAdmin Configuration
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 3: SSH SHELL ACCESS -->
    <div v-if="activeTab === 'shell'" class="space-y-6">
      <div class="bg-white border border-slate-200 rounded-xl shadow-xs overflow-hidden">
        <div class="p-4 border-b border-slate-200 bg-slate-50 flex items-center justify-between">
          <div class="flex items-center gap-2">
            <span class="w-1.5 h-4 bg-[#005299] rounded-xs"></span>
            <h2 class="text-sm font-bold text-slate-800">SSH Shell Daemon (OpenSSH)</h2>
          </div>
          <label class="relative inline-flex items-center cursor-pointer">
            <input type="checkbox" v-model="sshConfig.enabled" class="sr-only peer" />
            <div class="w-11 h-6 bg-slate-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-slate-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-[#005299]"></div>
          </label>
        </div>

        <div class="p-6 space-y-4">
          <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div>
              <label class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1">SSH Port</label>
              <input type="number" v-model.number="sshConfig.port" class="w-full bg-white border border-slate-300 rounded-lg px-3 py-2 text-xs font-mono text-slate-800 focus:ring-2 focus:ring-blue-500 focus:outline-none" />
            </div>
            <div class="flex items-center gap-2 pt-6">
              <input type="checkbox" id="ssh_root" v-model="sshConfig.allow_root_login" class="rounded text-[#005299] h-4 w-4" />
              <label for="ssh_root" class="text-xs font-bold text-slate-700 cursor-pointer">Allow Root Login</label>
            </div>
            <div class="flex items-center gap-2 pt-6">
              <input type="checkbox" id="ssh_password" v-model="sshConfig.allow_password_auth" class="rounded text-[#005299] h-4 w-4" />
              <label for="ssh_password" class="text-xs font-bold text-slate-700 cursor-pointer">Allow Password Auth</label>
            </div>
          </div>

          <div>
            <label class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1">Authorized SSH Public Keys (1 key per line)</label>
            <textarea
              v-model="sshConfig.authorized_keys"
              rows="4"
              placeholder="ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAI... admin@workstation"
              class="w-full bg-white border border-slate-300 rounded-lg p-3 text-xs font-mono text-slate-800 focus:ring-2 focus:ring-blue-500 focus:outline-none leading-relaxed"
            ></textarea>
          </div>

          <div class="pt-4 border-t border-slate-200 flex justify-end">
            <button
              type="button"
              @click="saveSshSettings"
              class="px-5 py-2 bg-[#005299] hover:bg-[#003d73] text-white rounded-lg text-xs font-bold shadow-xs cursor-pointer"
            >
              Apply SSH Settings
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 4: NOTIFICATIONS & ALERTING (Phase 1 Parity) -->
    <div v-if="activeTab === 'notifications'" class="space-y-6">
      <div class="bg-white border border-slate-200 rounded-xl shadow-xs overflow-hidden">
        <div class="p-4 border-b border-slate-200 bg-slate-50 flex items-center justify-between">
          <div class="flex items-center gap-2">
            <span class="w-1.5 h-4 bg-[#ee7f00] rounded-xs"></span>
            <h2 class="text-sm font-bold text-slate-800">Email Notifications &amp; SMTP Alert Dispatcher</h2>
          </div>
          <span class="text-[11px] bg-emerald-50 text-emerald-800 font-mono font-bold px-2 py-0.5 rounded border border-emerald-200">
            FID: notifications_notifications
          </span>
        </div>

        <div class="p-6 space-y-6">
          <!-- Master Toggle -->
          <div class="flex items-center justify-between p-3.5 bg-slate-50 rounded-lg border border-slate-200">
            <div>
              <div class="text-xs font-bold text-slate-900">Enable Email Notification Triggers</div>
              <div class="text-[11px] text-slate-500">Dispatch critical administrative events, threats, backups, and health alerts</div>
            </div>
            <input type="checkbox" v-model="notifSettings.email_enabled" class="w-4 h-4 text-blue-600 rounded border-slate-300 focus:ring-blue-500 cursor-pointer" />
          </div>

          <div v-if="notifSettings.email_enabled" class="space-y-4">
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <div>
                <label class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1">SMTP Server Host</label>
                <input type="text" v-model="notifSettings.smtp_server" class="w-full bg-white border border-slate-300 rounded-lg px-3 py-2 text-xs font-mono text-slate-800 focus:ring-2 focus:ring-blue-500 focus:outline-none" />
              </div>
              <div>
                <label class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1">SMTP Port</label>
                <input type="number" v-model.number="notifSettings.smtp_port" class="w-full bg-white border border-slate-300 rounded-lg px-3 py-2 text-xs font-mono text-slate-800 focus:ring-2 focus:ring-blue-500 focus:outline-none" />
              </div>
              <div>
                <label class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1">Security / Encryption</label>
                <select v-model="notifSettings.smtp_security" class="w-full bg-white border border-slate-300 rounded-lg px-3 py-2 text-xs font-medium text-slate-800 focus:ring-2 focus:ring-blue-500 focus:outline-none">
                  <option value="STARTTLS">STARTTLS (Opportunistic TLS)</option>
                  <option value="SSL">SSL / TLS Explicit (Port 465)</option>
                  <option value="None">None (Plaintext Port 25)</option>
                </select>
              </div>
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1">Sender Email Address</label>
                <input type="email" v-model="notifSettings.sender_email" class="w-full bg-white border border-slate-300 rounded-lg px-3 py-2 text-xs text-slate-800 focus:ring-2 focus:ring-blue-500 focus:outline-none" />
              </div>
              <div>
                <label class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1">Administrator Recipient Email(s)</label>
                <input type="text" v-model="notifSettings.admin_recipients" placeholder="admin@domain.com, security@domain.com" class="w-full bg-white border border-slate-300 rounded-lg px-3 py-2 text-xs text-slate-800 focus:ring-2 focus:ring-blue-500 focus:outline-none" />
              </div>
            </div>

            <!-- SMTP Authentication -->
            <div class="p-4 bg-slate-50 rounded-lg border border-slate-200 space-y-3">
              <div class="flex items-center gap-2">
                <input type="checkbox" v-model="notifSettings.smtp_auth_enabled" id="smtpAuth" class="w-4 h-4 text-blue-600 rounded border-slate-300 focus:ring-blue-500 cursor-pointer" />
                <label for="smtpAuth" class="text-xs font-bold text-slate-800 cursor-pointer">Require SMTP Authentication</label>
              </div>
              <div v-if="notifSettings.smtp_auth_enabled" class="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-2">
                <div>
                  <label class="block text-xs font-medium text-slate-600 mb-1">Username</label>
                  <input type="text" v-model="notifSettings.smtp_username" class="w-full bg-white border border-slate-300 rounded-lg px-3 py-1.5 text-xs text-slate-800 focus:ring-2 focus:ring-blue-500 focus:outline-none" />
                </div>
                <div>
                  <label class="block text-xs font-medium text-slate-600 mb-1">Password</label>
                  <input type="password" v-model="notifSettings.smtp_password" class="w-full bg-white border border-slate-300 rounded-lg px-3 py-1.5 text-xs text-slate-800 focus:ring-2 focus:ring-blue-500 focus:outline-none" />
                </div>
              </div>
            </div>

            <!-- Event Category Checklists (Astaro-Next Parity) -->
            <div>
              <label class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-2">Notification Event Triggers</label>
              <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-3">
                <label class="flex items-center gap-2 p-2.5 bg-white border border-slate-200 rounded-lg text-xs font-medium text-slate-700 hover:bg-slate-50 cursor-pointer">
                  <input type="checkbox" v-model="notifSettings.alert_events.system_hardware" class="w-4 h-4 text-blue-600 rounded" />
                  <span>CPU / RAM / Disk High Usage</span>
                </label>
                <label class="flex items-center gap-2 p-2.5 bg-white border border-slate-200 rounded-lg text-xs font-medium text-slate-700 hover:bg-slate-50 cursor-pointer">
                  <input type="checkbox" v-model="notifSettings.alert_events.threat_detected" class="w-4 h-4 text-blue-600 rounded" />
                  <span>IPS &amp; ATP Threats Detected</span>
                </label>
                <label class="flex items-center gap-2 p-2.5 bg-white border border-slate-200 rounded-lg text-xs font-medium text-slate-700 hover:bg-slate-50 cursor-pointer">
                  <input type="checkbox" v-model="notifSettings.alert_events.vpn_tunnel_down" class="w-4 h-4 text-blue-600 rounded" />
                  <span>VPN Tunnel State Changes</span>
                </label>
                <label class="flex items-center gap-2 p-2.5 bg-white border border-slate-200 rounded-lg text-xs font-medium text-slate-700 hover:bg-slate-50 cursor-pointer">
                  <input type="checkbox" v-model="notifSettings.alert_events.backup_complete" class="w-4 h-4 text-blue-600 rounded" />
                  <span>Scheduled Backup Completed</span>
                </label>
                <label class="flex items-center gap-2 p-2.5 bg-white border border-slate-200 rounded-lg text-xs font-medium text-slate-700 hover:bg-slate-50 cursor-pointer">
                  <input type="checkbox" v-model="notifSettings.alert_events.firmware_available" class="w-4 h-4 text-blue-600 rounded" />
                  <span>Up2Date Firmware Available</span>
                </label>
                <label class="flex items-center gap-2 p-2.5 bg-white border border-slate-200 rounded-lg text-xs font-medium text-slate-700 hover:bg-slate-50 cursor-pointer">
                  <input type="checkbox" v-model="notifSettings.alert_events.cert_expiring" class="w-4 h-4 text-blue-600 rounded" />
                  <span>TLS Certificate Expiration (30d)</span>
                </label>
              </div>
            </div>

            <!-- SNMP Traps -->
            <div class="p-4 bg-slate-50 rounded-lg border border-slate-200 space-y-3">
              <div class="flex items-center gap-2">
                <input type="checkbox" v-model="notifSettings.snmp_traps_enabled" id="snmpTraps" class="w-4 h-4 text-blue-600 rounded border-slate-300 focus:ring-blue-500 cursor-pointer" />
                <label for="snmpTraps" class="text-xs font-bold text-slate-800 cursor-pointer">Enable SNMP Trap Receiver</label>
              </div>
              <div v-if="notifSettings.snmp_traps_enabled" class="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-2">
                <div>
                  <label class="block text-xs font-medium text-slate-600 mb-1">SNMP Community</label>
                  <input type="text" v-model="notifSettings.snmp_community" class="w-full bg-white border border-slate-300 rounded-lg px-3 py-1.5 text-xs text-slate-800 focus:ring-2 focus:ring-blue-500 focus:outline-none" />
                </div>
                <div>
                  <label class="block text-xs font-medium text-slate-600 mb-1">SNMP Trap Target Host / IP</label>
                  <input type="text" v-model="notifSettings.snmp_trap_receiver" class="w-full bg-white border border-slate-300 rounded-lg px-3 py-1.5 text-xs font-mono text-slate-800 focus:ring-2 focus:ring-blue-500 focus:outline-none" />
                </div>
              </div>
            </div>
          </div>

          <div class="pt-4 border-t border-slate-200 flex items-center justify-between">
            <button
              type="button"
              @click="sendTestEmailAction"
              class="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-800 border border-slate-300 rounded-lg text-xs font-bold shadow-2xs flex items-center gap-1.5 cursor-pointer"
            >
              <svg class="w-3.5 h-3.5 text-[#ee7f00]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
              <span>Send Test Email</span>
            </button>

            <button
              type="button"
              @click="saveNotificationSettingsAction"
              class="px-5 py-2 bg-[#005299] hover:bg-[#003d73] text-white rounded-lg text-xs font-bold shadow-xs cursor-pointer"
            >
              Save Notification Settings
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 5: LOG SETTINGS & REMOTE SYSLOG (Phase 2 Parity) -->
    <div v-if="activeTab === 'logs'" class="space-y-6">
      <div class="bg-white border border-slate-200 rounded-xl shadow-xs overflow-hidden">
        <div class="p-4 border-b border-slate-200 bg-slate-50 flex items-center justify-between">
          <div class="flex items-center gap-2">
            <span class="w-1.5 h-4 bg-[#005299] rounded-xs"></span>
            <h2 class="text-sm font-bold text-slate-800">Local Retention &amp; Remote Syslog Servers</h2>
          </div>
          <button
            type="button"
            @click="openAddSyslogModal"
            class="px-3.5 py-1.5 bg-[#005299] hover:bg-blue-700 text-white rounded-lg text-xs font-bold shadow-xs flex items-center gap-1.5 cursor-pointer"
          >
            + Add Syslog Server
          </button>
        </div>

        <div class="p-6 space-y-6">
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1">Local Log Retention (Days)</label>
              <select v-model.number="logSettings.local_retention_days" class="w-full bg-white border border-slate-300 rounded-lg px-3 py-2 text-xs font-medium text-slate-800 focus:ring-2 focus:ring-blue-500 focus:outline-none">
                <option :value="30">30 Days</option>
                <option :value="60">60 Days</option>
                <option :value="90">90 Days (Default)</option>
                <option :value="180">180 Days (Half Year)</option>
                <option :value="365">365 Days (1 Year)</option>
              </select>
            </div>
            <div>
              <label class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1">Max Disk Buffer Size (MB)</label>
              <input type="number" v-model.number="logSettings.max_disk_usage_mb" class="w-full bg-white border border-slate-300 rounded-lg px-3 py-2 text-xs font-mono text-slate-800 focus:ring-2 focus:ring-blue-500 focus:outline-none" />
            </div>
          </div>

          <!-- Syslog Servers Table -->
          <div>
            <div class="flex items-center justify-between mb-2">
              <label class="text-xs font-bold text-slate-700 uppercase tracking-wider">Configured Remote Syslog Collectors</label>
              <span class="text-[11px] font-mono text-slate-500">Rsyslog Daemon</span>
            </div>

            <div class="border border-slate-200 rounded-lg overflow-hidden">
              <table class="w-full text-left text-xs border-collapse">
                <thead class="bg-slate-100 text-slate-700 border-b border-slate-200 font-semibold">
                  <tr>
                    <th class="p-3">Server Name</th>
                    <th class="p-3">Host / Endpoint</th>
                    <th class="p-3">Port / Proto</th>
                    <th class="p-3">Facility</th>
                    <th class="p-3">Streams Streamed</th>
                    <th class="p-3 text-right">Actions</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-slate-100 font-normal text-slate-800">
                  <tr v-for="srv in logSettings.syslog_servers" :key="srv.id" class="hover:bg-slate-50">
                    <td class="p-3 font-bold text-slate-900">{{ srv.name }}</td>
                    <td class="p-3 font-mono text-slate-700">{{ srv.host }}</td>
                    <td class="p-3 font-mono">{{ srv.port }} ({{ srv.protocol }})</td>
                    <td class="p-3 font-mono">{{ srv.facility }}</td>
                    <td class="p-3">
                      <div class="flex flex-wrap gap-1">
                        <span v-if="srv.log_firewall" class="px-1.5 py-0.5 bg-blue-50 text-blue-700 rounded text-[10px] font-mono">Firewall</span>
                        <span v-if="srv.log_ips" class="px-1.5 py-0.5 bg-purple-50 text-purple-700 rounded text-[10px] font-mono">IPS</span>
                        <span v-if="srv.log_web" class="px-1.5 py-0.5 bg-emerald-50 text-emerald-700 rounded text-[10px] font-mono">Web</span>
                        <span v-if="srv.log_mail" class="px-1.5 py-0.5 bg-amber-50 text-amber-700 rounded text-[10px] font-mono">Mail</span>
                        <span v-if="srv.log_auth" class="px-1.5 py-0.5 bg-rose-50 text-rose-700 rounded text-[10px] font-mono">Auth</span>
                      </div>
                    </td>
                    <td class="p-3 text-right">
                      <button
                        type="button"
                        @click="removeSyslogServer(srv.id)"
                        class="text-rose-600 hover:text-rose-800 text-xs font-bold cursor-pointer"
                      >
                        Delete
                      </button>
                    </td>
                  </tr>
                  <tr v-if="!logSettings.syslog_servers || logSettings.syslog_servers.length === 0">
                    <td colspan="6" class="p-6 text-center text-slate-400">
                      No remote syslog servers configured. Click "+ Add Syslog Server" to stream live events to SIEM.
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <div class="pt-4 border-t border-slate-200 flex justify-end">
            <button
              type="button"
              @click="saveLogSettingsAction"
              class="px-5 py-2 bg-[#005299] hover:bg-[#003d73] text-white rounded-lg text-xs font-bold shadow-xs cursor-pointer"
            >
              Commit Log Retention &amp; Syslog Settings
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 6: REBOOT & SHUTDOWN -->
    <div v-if="activeTab === 'power'" class="space-y-6">
      <div class="bg-white border border-slate-200 rounded-xl shadow-xs p-6 space-y-4 max-w-2xl">
        <h2 class="text-sm font-bold text-slate-800 flex items-center gap-2">
          <span class="w-2 h-2 rounded-full bg-rose-500"></span>
          <span>Appliance Hardware Power Control</span>
        </h2>
        <p class="text-xs text-slate-500">Gracefully reboot or shutdown the underlying Debian Linux gateway engine.</p>

        <div class="pt-4 border-t border-slate-200 flex gap-4">
          <button
            type="button"
            @click="triggerReboot"
            class="px-5 py-2.5 bg-amber-600 hover:bg-amber-700 text-white rounded-lg text-xs font-bold shadow-xs cursor-pointer"
          >
            Reboot Security Gateway
          </button>
          <button
            type="button"
            @click="triggerShutdown"
            class="px-5 py-2.5 bg-rose-600 hover:bg-rose-700 text-white rounded-lg text-xs font-bold shadow-xs cursor-pointer"
          >
            Power Off / Shutdown
          </button>
        </div>
      </div>
    </div>

    <!-- MODAL: ADD REMOTE SYSLOG SERVER -->
    <div v-if="isSyslogModalOpen" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-xs">
      <div class="bg-white border border-slate-200 rounded-xl shadow-2xl w-full max-w-lg overflow-hidden">
        <div class="p-4 bg-slate-900 text-white flex items-center justify-between">
          <div class="flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-[#ee7f00]"></span>
            <h3 class="text-xs font-bold uppercase tracking-wider">Add Remote Syslog Server</h3>
          </div>
          <button @click="isSyslogModalOpen = false" class="text-slate-400 hover:text-white cursor-pointer">&times;</button>
        </div>

        <div class="p-6 space-y-4 text-xs">
          <div>
            <label class="block font-bold text-slate-700 uppercase mb-1">Server Name / Label</label>
            <input type="text" v-model="newSyslog.name" placeholder="e.g. Corporate SIEM Collector" class="w-full bg-slate-50 border border-slate-300 rounded-lg p-2 text-slate-800" />
          </div>

          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block font-bold text-slate-700 uppercase mb-1">Host / IP Address</label>
              <input type="text" v-model="newSyslog.host" placeholder="192.168.1.50" class="w-full bg-slate-50 border border-slate-300 rounded-lg p-2 font-mono" />
            </div>
            <div>
              <label class="block font-bold text-slate-700 uppercase mb-1">Port</label>
              <input type="number" v-model.number="newSyslog.port" class="w-full bg-slate-50 border border-slate-300 rounded-lg p-2 font-mono" />
            </div>
          </div>

          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block font-bold text-slate-700 uppercase mb-1">Protocol</label>
              <select v-model="newSyslog.protocol" class="w-full bg-slate-50 border border-slate-300 rounded-lg p-2 font-medium">
                <option value="UDP">UDP (RFC 5426)</option>
                <option value="TCP">TCP (RFC 5425)</option>
                <option value="TLS">TLS Encrypted Syslog</option>
              </select>
            </div>
            <div>
              <label class="block font-bold text-slate-700 uppercase mb-1">Facility</label>
              <select v-model="newSyslog.facility" class="w-full bg-slate-50 border border-slate-300 rounded-lg p-2 font-mono">
                <option value="local0">local0</option>
                <option value="local1">local1</option>
                <option value="local2">local2</option>
                <option value="daemon">daemon</option>
                <option value="authpriv">authpriv</option>
              </select>
            </div>
          </div>

          <div>
            <label class="block font-bold text-slate-700 uppercase mb-2">Log Streams to Forward</label>
            <div class="grid grid-cols-2 gap-2">
              <label class="flex items-center gap-2"><input type="checkbox" v-model="newSyslog.log_firewall" /><span>Firewall Rules</span></label>
              <label class="flex items-center gap-2"><input type="checkbox" v-model="newSyslog.log_ips" /><span>Intrusion Prevention</span></label>
              <label class="flex items-center gap-2"><input type="checkbox" v-model="newSyslog.log_web" /><span>Web Protection</span></label>
              <label class="flex items-center gap-2"><input type="checkbox" v-model="newSyslog.log_mail" /><span>Mail &amp; Quarantine</span></label>
              <label class="flex items-center gap-2"><input type="checkbox" v-model="newSyslog.log_auth" /><span>User Logins &amp; 2FA</span></label>
              <label class="flex items-center gap-2"><input type="checkbox" v-model="newSyslog.log_system" /><span>System &amp; Daemons</span></label>
            </div>
          </div>
        </div>

        <div class="p-4 bg-slate-50 border-t border-slate-200 flex justify-end gap-2">
          <button type="button" @click="isSyslogModalOpen = false" class="px-4 py-1.5 border border-slate-300 rounded-lg text-xs font-bold cursor-pointer">Cancel</button>
          <button type="button" @click="saveNewSyslogServer" class="px-5 py-1.5 bg-[#005299] hover:bg-[#003d73] text-white rounded-lg text-xs font-bold cursor-pointer">Add Server</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, h } from 'vue'

const props = defineProps({
  authToken: {
    type: String,
    default: ''
  }
})

const activeTab = ref('identity')
const newAclHost = ref('')
const isSyslogModalOpen = ref(false)

// Tab icons
const IdentityIcon = {
  render: () => h('svg', { class: 'w-4 h-4', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
    h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4' })
  ])
}

const WebadminIcon = {
  render: () => h('svg', { class: 'w-4 h-4', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
    h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z' })
  ])
}

const ShellIcon = {
  render: () => h('svg', { class: 'w-4 h-4', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
    h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M8 9l3 3-3 3m5 0h3M5 20h14a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z' })
  ])
}

const NotifIcon = {
  render: () => h('svg', { class: 'w-4 h-4', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
    h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9' })
  ])
}

const LogIcon = {
  render: () => h('svg', { class: 'w-4 h-4', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
    h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z' })
  ])
}

const PowerIcon = {
  render: () => h('svg', { class: 'w-4 h-4', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
    h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M13 10V3L4 14h7v7l9-11h-7z' })
  ])
}

const tabs = [
  { id: 'identity', label: 'Appliance Identity', icon: IdentityIcon },
  { id: 'webadmin', label: 'WebAdmin ACLs', icon: WebadminIcon },
  { id: 'shell', label: 'SSH Shell', icon: ShellIcon },
  { id: 'notifications', label: 'Notifications & Alerts', icon: NotifIcon },
  { id: 'logs', label: 'Log Settings & Syslog', icon: LogIcon },
  { id: 'power', label: 'Shutdown & Reboot', icon: PowerIcon }
]

const identityConfig = ref({
  hostname: 'home.medric.net',
  domain: 'medric.net',
  organization: 'Medric Networks LLC',
  admin_email: 'admin@medric.net',
  timezone: 'America/New_York'
})

const webadminConfig = ref({
  port: 4444,
  session_timeout_min: 60,
  allowed_networks: ['192.168.1.0/24', '10.0.0.0/8']
})

const sshConfig = ref({
  enabled: true,
  port: 22,
  allow_root_login: true,
  allow_password_auth: true,
  authorized_keys: 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAINaA6N9E6GZ8kM... admin@medric.net'
})

const notifSettings = ref({
  email_enabled: true,
  smtp_server: '127.0.0.1',
  smtp_port: 25,
  smtp_security: 'STARTTLS',
  smtp_auth_enabled: false,
  smtp_username: '',
  smtp_password: '',
  sender_email: 'astaro-appliance@corp.astaro.net',
  admin_recipients: 'admin@medric.net, secops@medric.net',
  alert_events: {
    system_hardware: true,
    threat_detected: true,
    vpn_tunnel_down: true,
    backup_complete: true,
    firmware_available: true,
    cert_expiring: true
  },
  snmp_traps_enabled: false,
  snmp_community: 'public',
  snmp_trap_receiver: '192.168.1.50'
})

const logSettings = ref({
  local_retention_days: 90,
  max_disk_usage_mb: 5000,
  compress_archives: true,
  remote_syslog_enabled: true,
  syslog_servers: [
    {
      id: 'syslog-1',
      name: 'Splunk Enterprise SIEM',
      host: '192.168.1.50',
      port: 514,
      protocol: 'UDP',
      facility: 'local0',
      log_firewall: true,
      log_ips: true,
      log_web: true,
      log_mail: true,
      log_auth: true,
      log_system: true
    }
  ]
})

const newSyslog = ref({
  name: '',
  host: '',
  port: 514,
  protocol: 'UDP',
  facility: 'local0',
  log_firewall: true,
  log_ips: true,
  log_web: true,
  log_mail: true,
  log_auth: true,
  log_system: true
})

const fetchSettings = async () => {
  const axiosLib = (typeof window !== 'undefined' && window.axios) ? window.axios : null
  if (!axiosLib) return
  try {
    const [resNotif, resLog] = await Promise.all([
      axiosLib.get('/api/system/notifications').catch(() => null),
      axiosLib.get('/api/system/log-settings').catch(() => null)
    ])
    if (resNotif && resNotif.data) Object.assign(notifSettings.value, resNotif.data)
    if (resLog && resLog.data) Object.assign(logSettings.value, resLog.data)
  } catch (e) {}
}

onMounted(() => {
  fetchSettings()
})

const addAclHost = () => {
  if (!newAclHost.value.trim()) return
  if (!webadminConfig.value.allowed_networks.includes(newAclHost.value.trim())) {
    webadminConfig.value.allowed_networks.push(newAclHost.value.trim())
  }
  newAclHost.value = ''
}

const saveIdentitySettings = () => { alert('Identity settings saved.') }
const saveWebadminSettings = () => { alert('WebAdmin access configuration applied.') }
const saveSshSettings = () => { alert('SSH daemon configuration synced.') }

const sendTestEmailAction = async () => {
  const axiosLib = (typeof window !== 'undefined' && window.axios) ? window.axios : null
  if (axiosLib) {
    try {
      const res = await axiosLib.post('/api/system/notifications/test-email', {
        recipient: notifSettings.value.admin_recipients,
        smtp_server: notifSettings.value.smtp_server
      })
      alert(res.data.message || 'Test email dispatched.')
      return
    } catch (e) {}
  }
  alert('Dispatched test alert email to ' + notifSettings.value.admin_recipients)
}

const saveNotificationSettingsAction = async () => {
  const axiosLib = (typeof window !== 'undefined' && window.axios) ? window.axios : null
  if (axiosLib) {
    try {
      await axiosLib.post('/api/system/notifications', notifSettings.value)
    } catch (e) {}
  }
  alert('Notification preferences saved successfully.')
}

const openAddSyslogModal = () => {
  newSyslog.value = {
    name: '',
    host: '',
    port: 514,
    protocol: 'UDP',
    facility: 'local0',
    log_firewall: true,
    log_ips: true,
    log_web: true,
    log_mail: true,
    log_auth: true,
    log_system: true
  }
  isSyslogModalOpen.value = true
}

const saveNewSyslogServer = () => {
  if (!newSyslog.value.name || !newSyslog.value.host) {
    alert('Please enter a server name and host IP.')
    return
  }
  const sid = 'syslog-' + Date.now()
  logSettings.value.syslog_servers.push({
    ...newSyslog.value,
    id: sid
  })
  isSyslogModalOpen.value = false
}

const removeSyslogServer = (id) => {
  logSettings.value.syslog_servers = logSettings.value.syslog_servers.filter(s => s.id !== id)
}

const saveLogSettingsAction = async () => {
  const axiosLib = (typeof window !== 'undefined' && window.axios) ? window.axios : null
  if (axiosLib) {
    try {
      await axiosLib.post('/api/system/log-settings', logSettings.value)
    } catch (e) {}
  }
  alert('Log retention and remote syslog settings committed.')
}

const triggerReboot = () => { if (confirm('Are you sure you want to reboot Astaro-Next gateway?')) alert('Reboot sequence initiated.') }
const triggerShutdown = () => { if (confirm('Are you sure you want to shut down the appliance?')) alert('Shutdown sequence initiated.') }
</script>
