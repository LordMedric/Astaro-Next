<template>
  <div class="space-y-6">
    <!-- Top Modern Breadcrumb & Action Banner -->
    <div class="bg-white border border-slate-200 rounded-xl p-5 shadow-xs flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div>
        <div class="flex items-center gap-2">
          <span class="w-2 h-6 bg-[#005299] rounded-xs"></span>
          <h1 class="text-xl font-bold text-slate-900 tracking-tight">Executive & Security Reports</h1>
          <span class="bg-emerald-50 text-emerald-700 text-xs font-bold px-2.5 py-0.5 rounded-full border border-emerald-200">
            Real-Time Analytics Engine
          </span>
        </div>
        <p class="text-xs text-slate-500 mt-1 pl-4">
          High-level executive security summaries, bandwidth utilization accounting, threat telemetry, and scheduled automated PDF reporting.
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

    <!-- TAB 1: EXECUTIVE SUMMARY -->
    <div v-if="activeTab === 'executive'" class="space-y-6">
      <!-- 4 Top Big Stat Metric Cards -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div class="bg-white border border-slate-200 rounded-xl p-4 shadow-xs">
          <div class="text-[11px] font-bold text-slate-500 uppercase tracking-wider">Total Threats Blocked</div>
          <div class="text-2xl font-black text-rose-600 mt-1">14,892</div>
          <div class="text-[10px] text-emerald-600 font-semibold mt-1 flex items-center gap-1">
            <span>&uarr; 12%</span> vs last week
          </div>
        </div>

        <div class="bg-white border border-slate-200 rounded-xl p-4 shadow-xs">
          <div class="text-[11px] font-bold text-slate-500 uppercase tracking-wider">Network Traffic Inspected</div>
          <div class="text-2xl font-black text-blue-700 mt-1">1.48 TB</div>
          <div class="text-[10px] text-slate-500 mt-1">WAN throughput (eth0)</div>
        </div>

        <div class="bg-white border border-slate-200 rounded-xl p-4 shadow-xs">
          <div class="text-[11px] font-bold text-slate-500 uppercase tracking-wider">Spam & Phishing Filtered</div>
          <div class="text-2xl font-black text-amber-600 mt-1">3,410</div>
          <div class="text-[10px] text-slate-500 mt-1">99.4% Spam Catch Rate</div>
        </div>

        <div class="bg-white border border-slate-200 rounded-xl p-4 shadow-xs">
          <div class="text-[11px] font-bold text-slate-500 uppercase tracking-wider">Gateway Uptime</div>
          <div class="text-2xl font-black text-emerald-600 mt-1">99.98%</div>
          <div class="text-[10px] text-slate-500 mt-1">No unscheduled outages</div>
        </div>
      </div>

      <!-- Action: Generate Executive Report PDF -->
      <div class="bg-gradient-to-r from-[#005299] to-[#003366] rounded-xl p-6 text-white shadow-xs flex flex-col sm:flex-row items-center justify-between gap-4">
        <div>
          <h2 class="text-base font-bold">Generate Comprehensive Executive Report (PDF)</h2>
          <p class="text-xs text-blue-100 mt-1">Compile full network accounting, top threats, web protection logs, and mail activity into a branded report.</p>
        </div>
        <button
          type="button"
          @click="generatePdfReport"
          class="px-5 py-2.5 bg-white hover:bg-slate-100 text-[#005299] rounded-lg text-xs font-bold shadow-xs cursor-pointer flex items-center gap-2 whitespace-nowrap"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          <span>Download Executive PDF</span>
        </button>
      </div>
    </div>

    <!-- TAB 2: NETWORK & BANDWIDTH USAGE -->
    <div v-if="activeTab === 'bandwidth'" class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div class="bg-white border border-slate-200 rounded-xl p-5 shadow-xs space-y-4">
        <h2 class="text-xs font-bold text-slate-800 uppercase tracking-wider flex items-center gap-2">
          <span class="w-2 h-2 rounded-full bg-blue-500"></span>
          <span>Top Bandwidth Consumers (Internal Hosts)</span>
        </h2>
        <div class="space-y-3">
          <div v-for="host in topTalkers" :key="host.ip" class="space-y-1">
            <div class="flex justify-between text-xs font-medium">
              <span class="font-bold text-slate-900">{{ host.hostname }} <span class="font-mono text-slate-500 font-normal">({{ host.ip }})</span></span>
              <span class="font-mono text-blue-700 font-bold">{{ host.traffic }}</span>
            </div>
            <div class="w-full bg-slate-100 rounded-full h-2 overflow-hidden">
              <div class="bg-[#005299] h-2 rounded-full" :style="{ width: `${host.pct}%` }"></div>
            </div>
          </div>
        </div>
      </div>

      <div class="bg-white border border-slate-200 rounded-xl p-5 shadow-xs space-y-4">
        <h2 class="text-xs font-bold text-slate-800 uppercase tracking-wider flex items-center gap-2">
          <span class="w-2 h-2 rounded-full bg-emerald-500"></span>
          <span>Top Protocols & Applications</span>
        </h2>
        <div class="space-y-3">
          <div v-for="proto in topProtocols" :key="proto.name" class="space-y-1">
            <div class="flex justify-between text-xs font-medium">
              <span class="font-bold text-slate-900">{{ proto.name }} <span class="text-slate-400 font-normal">({{ proto.port }})</span></span>
              <span class="font-mono text-slate-700 font-bold">{{ proto.volume }}</span>
            </div>
            <div class="w-full bg-slate-100 rounded-full h-2 overflow-hidden">
              <div class="bg-emerald-600 h-2 rounded-full" :style="{ width: `${proto.pct}%` }"></div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 3: THREAT INTELLIGENCE -->
    <div v-if="activeTab === 'threats'" class="space-y-6">
      <div class="bg-white border border-slate-200 rounded-xl shadow-xs overflow-hidden">
        <div class="p-4 border-b border-slate-200 bg-slate-50">
          <h2 class="text-sm font-bold text-slate-800">Top Threat Vectors Blocked (Last 7 Days)</h2>
        </div>
        <table class="w-full text-left text-xs text-slate-700">
          <thead class="bg-slate-100/75 border-b border-slate-200 text-[11px] font-bold text-slate-600 uppercase tracking-wider">
            <tr>
              <th class="py-3 px-4">Threat Category</th>
              <th class="py-3 px-4">Blocked Attacks</th>
              <th class="py-3 px-4">Primary Defense Subsystem</th>
              <th class="py-3 px-4">Threat Severity</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100 font-medium">
            <tr v-for="t in threatVectors" :key="t.name" class="hover:bg-slate-50/80">
              <td class="py-3 px-4 font-bold text-slate-900">{{ t.name }}</td>
              <td class="py-3 px-4 font-mono font-bold text-rose-600">{{ t.count.toLocaleString() }}</td>
              <td class="py-3 px-4"><span class="px-2 py-0.5 rounded text-[10px] font-mono bg-slate-100 text-slate-700">{{ t.subsystem }}</span></td>
              <td class="py-3 px-4">
                <span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-rose-100 text-rose-800 uppercase">
                  {{ t.severity }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
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

const activeTab = ref('executive')

// Tab icons
const ExecIcon = {
  render: () => h('svg', { class: 'w-4 h-4', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
    h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z' })
  ])
}

const BandwidthIcon = {
  render: () => h('svg', { class: 'w-4 h-4', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
    h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M13 7h8m0 0v8m0-8l-8 8-4-4-6 6' })
  ])
}

const ThreatIcon = {
  render: () => h('svg', { class: 'w-4 h-4', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
    h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z' })
  ])
}

const tabs = [
  { id: 'executive', label: 'Executive Summary', icon: ExecIcon },
  { id: 'bandwidth', label: 'Bandwidth Accounting', icon: BandwidthIcon },
  { id: 'threats', label: 'Threat Intelligence', icon: ThreatIcon }
]

const topTalkers = ref([
  { hostname: 'medric-nas', ip: '192.168.1.10', traffic: '680 GB', pct: 85 },
  { hostname: 'workstation-dev', ip: '192.168.1.110', traffic: '340 GB', pct: 45 },
  { hostname: 'proxmox-pve-01', ip: '192.168.1.50', traffic: '220 GB', pct: 30 },
  { hostname: 'smart-tv-livingroom', ip: '192.168.1.115', traffic: '95 GB', pct: 15 }
])

const topProtocols = ref([
  { name: 'HTTPS Web Traffic', port: 'TCP/443', volume: '920 GB', pct: 75 },
  { name: 'WireGuard VPN Tunnel', port: 'UDP/51820', volume: '310 GB', pct: 35 },
  { name: 'SMTP Mail Delivery', port: 'TCP/25,587', volume: '140 GB', pct: 18 },
  { name: 'SSH Remote Access', port: 'TCP/22', volume: '25 GB', pct: 5 }
])

const threatVectors = ref([
  { name: 'Apache Log4j & Spring4Shell RCE', count: 4820, subsystem: 'Suricata IPS Engine', severity: 'Critical' },
  { name: 'Web Application SQL Injection (SQLi)', count: 3410, subsystem: 'Nginx ModSecurity WAF', severity: 'High' },
  { name: 'SSH & RDP Brute Force Scans', count: 5290, subsystem: 'NFTables Anti-Portscan', severity: 'Medium' },
  { name: 'Spamhaus Zen RBL Blocked Senders', count: 1372, subsystem: 'Postfix SMTP Relay', severity: 'Low' }
])

const generatePdfReport = () => {
  alert('Generated Astaro-Next Weekly Executive Security Report (PDF).')
}
</script>
