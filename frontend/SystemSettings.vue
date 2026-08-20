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
              <p class="text-[11px] text-slate-500 mt-1">Default Sophos UTM / Astaro port is 4444.</p>
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

    <!-- TAB 4: NOTIFICATIONS & ALERTS -->
    <div v-if="activeTab === 'notifications'" class="space-y-6">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- Email Alerting Card -->
        <div class="bg-white border border-slate-200 rounded-xl shadow-xs overflow-hidden">
          <div class="p-4 border-b border-slate-200 bg-slate-50 flex items-center justify-between">
            <h2 class="text-sm font-bold text-slate-800">Email Notification Sender (SMTP)</h2>
            <input type="checkbox" v-model="notifConfig.email_enabled" class="rounded text-[#005299] h-4 w-4" />
          </div>
          <div class="p-5 space-y-3">
            <div>
              <label class="block text-[11px] font-bold text-slate-700 mb-1">Recipient Alert Email</label>
              <input type="email" v-model="notifConfig.recipient_email" class="w-full bg-white border border-slate-300 rounded-md px-3 py-1.5 text-xs text-slate-800" />
            </div>
            <div>
              <label class="block text-[11px] font-bold text-slate-700 mb-1">SMTP Smarthost & Port</label>
              <div class="grid grid-cols-3 gap-2">
                <input type="text" v-model="notifConfig.smtp_host" placeholder="smtp.mailgun.org" class="col-span-2 bg-white border border-slate-300 rounded-md px-3 py-1.5 text-xs font-mono text-slate-800" />
                <input type="number" v-model.number="notifConfig.smtp_port" placeholder="587" class="bg-white border border-slate-300 rounded-md px-3 py-1.5 text-xs font-mono text-slate-800" />
              </div>
            </div>
            <button
              type="button"
              @click="sendTestEmail"
              class="w-full py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-bold rounded-lg cursor-pointer transition-colors"
            >
              Send Test Email Alert
            </button>
          </div>
        </div>

        <!-- Telegram Webhook Alerting Card -->
        <div class="bg-white border border-slate-200 rounded-xl shadow-xs overflow-hidden">
          <div class="p-4 border-b border-slate-200 bg-slate-50 flex items-center justify-between">
            <h2 class="text-sm font-bold text-slate-800">Telegram Bot Instant Alerts</h2>
            <input type="checkbox" v-model="notifConfig.telegram_enabled" class="rounded text-[#005299] h-4 w-4" />
          </div>
          <div class="p-5 space-y-3">
            <div>
              <label class="block text-[11px] font-bold text-slate-700 mb-1">Telegram Bot API Token</label>
              <input type="password" v-model="notifConfig.telegram_bot_token" placeholder="123456789:ABCdefGhIJKlmNoPQRstuVWXyz" class="w-full bg-white border border-slate-300 rounded-md px-3 py-1.5 text-xs font-mono text-slate-800" />
            </div>
            <div>
              <label class="block text-[11px] font-bold text-slate-700 mb-1">Telegram Chat ID</label>
              <input type="text" v-model="notifConfig.telegram_chat_id" placeholder="-100123456789" class="w-full bg-white border border-slate-300 rounded-md px-3 py-1.5 text-xs font-mono text-slate-800" />
            </div>
            <button
              type="button"
              @click="sendTestTelegram"
              class="w-full py-2 bg-blue-50 hover:bg-blue-100 text-[#005299] text-xs font-bold rounded-lg cursor-pointer transition-colors"
            >
              Send Test Telegram Push Notification
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 5: REBOOT & SHUTDOWN -->
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
  </div>
</template>

<script setup>
import { ref, h } from 'vue'

const props = defineProps({
  authToken: {
    type: String,
    default: ''
  }
})

const activeTab = ref('identity')
const newAclHost = ref('')

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

const PowerIcon = {
  render: () => h('svg', { class: 'w-4 h-4', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
    h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M13 10V3L4 14h7v7l9-11h-7z' })
  ])
}

const tabs = [
  { id: 'identity', label: 'Appliance Identity', icon: IdentityIcon },
  { id: 'webadmin', label: 'WebAdmin ACLs', icon: WebadminIcon },
  { id: 'shell', label: 'SSH Shell', icon: ShellIcon },
  { id: 'notifications', label: 'Alerts & Webhooks', icon: NotifIcon },
  { id: 'power', label: 'Shutdown & Reboot', icon: PowerIcon }
]

const identityConfig = ref({
  hostname: 'home.medric.net',
  domain: 'medric.net',
  organization: 'Medric Networks',
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

const notifConfig = ref({
  email_enabled: true,
  recipient_email: 'alerts@medric.net',
  smtp_host: 'smtp.sendgrid.net',
  smtp_port: 587,
  telegram_enabled: false,
  telegram_bot_token: '',
  telegram_chat_id: ''
})

const addAclHost = () => {
  if (!newAclHost.value.trim()) return
  if (!webadminConfig.value.allowed_networks.includes(newAclHost.value.trim())) {
    webadminConfig.value.allowed_networks.push(newAclHost.value.trim())
  }
  newAclHost.value = ''
}

const saveIdentitySettings = () => { alert('Identity settings updated.') }
const saveWebadminSettings = () => { alert('WebAdmin access configuration applied.') }
const saveSshSettings = () => { alert('SSH daemon configuration synced.') }
const sendTestEmail = () => { alert('Dispatched test alert email to ' + notifConfig.value.recipient_email) }
const sendTestTelegram = () => { alert('Dispatched test notification payload to Telegram Webhook.') }
const triggerReboot = () => { if (confirm('Are you sure you want to reboot Astaro-Next gateway?')) alert('Reboot sequence initiated.') }
const triggerShutdown = () => { if (confirm('Are you sure you want to shut down the appliance?')) alert('Shutdown sequence initiated.') }
</script>
