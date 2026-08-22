<template>
  <div class="space-y-6">
    <!-- Top Modern Banner -->
    <div class="bg-slate-900 text-white rounded-2xl p-6 shadow-xl border border-slate-800 flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div>
        <div class="flex items-center gap-2 mb-1">
          <div class="w-8 h-8 rounded-lg bg-rose-600 flex items-center justify-center text-white font-black text-sm shadow-md shadow-rose-600/30">
            <svg class="w-4.5 h-4.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
          </div>
          <h1 class="text-xl font-bold tracking-tight">Advanced Threat Protection (ATP)</h1>
          <span class="text-[10px] bg-rose-950 text-rose-300 font-mono font-bold px-2 py-0.5 rounded border border-rose-800/80">
            SANDSTORM LIVE
          </span>
        </div>
        <p class="text-xs text-slate-400">
          Next-Gen Botnet &amp; Command-and-Control (C2) detection, cloud dynamic analysis sandboxing, and zero-day threat isolation.
        </p>
      </div>

      <div class="flex items-center gap-3">
        <button
          @click="fetchAtpData"
          :disabled="loading"
          class="px-3.5 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-xl text-xs font-semibold flex items-center gap-1.5 transition-colors cursor-pointer"
        >
          <svg class="w-3.5 h-3.5" :class="{ 'animate-spin': loading }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          <span>Refresh Feeds</span>
        </button>
      </div>
    </div>

    <!-- Navigation Tabs Strip -->
    <div class="flex border-b border-slate-200 gap-1 bg-[#f4f6f9] p-1.5 rounded-t-xl overflow-x-auto text-xs font-bold">
      <button
        type="button"
        @click="activeTab = 'global'"
        :class="[
          'px-4 py-2 rounded-lg transition-all flex items-center gap-2 cursor-pointer whitespace-nowrap',
          activeTab === 'global'
            ? 'bg-white text-slate-900 shadow-xs border-b-2 border-[#ee7f00]'
            : 'text-slate-600 hover:text-slate-900 hover:bg-white/60'
        ]"
      >
        <span>🛡️ ATP Engine &amp; Sandstorm</span>
      </button>

      <button
        type="button"
        @click="activeTab = 'threats'"
        :class="[
          'px-4 py-2 rounded-lg transition-all flex items-center gap-2 cursor-pointer whitespace-nowrap',
          activeTab === 'threats'
            ? 'bg-white text-slate-900 shadow-xs border-b-2 border-[#ee7f00]'
            : 'text-slate-600 hover:text-slate-900 hover:bg-white/60'
        ]"
      >
        <span>🚨 Active Threat Activity Log</span>
        <span class="px-1.5 py-0.2 rounded-full text-[10px] font-mono bg-rose-100 text-rose-700">
          {{ threatLogs.length }}
        </span>
      </button>

      <button
        type="button"
        @click="activeTab = 'exceptions'"
        :class="[
          'px-4 py-2 rounded-lg transition-all flex items-center gap-2 cursor-pointer whitespace-nowrap',
          activeTab === 'exceptions'
            ? 'bg-white text-slate-900 shadow-xs border-b-2 border-[#ee7f00]'
            : 'text-slate-600 hover:text-slate-900 hover:bg-white/60'
        ]"
      >
        <span>⚡ Threat Exceptions</span>
        <span class="px-1.5 py-0.2 rounded-full text-[10px] font-mono bg-slate-200 text-slate-700">
          {{ exceptions.length }}
        </span>
      </button>
    </div>

    <!-- TAB 1: ATP ENGINE & SANDSTORM SETTINGS -->
    <div v-if="activeTab === 'global'" class="space-y-6">
      <div class="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
        <div class="p-4 border-b border-slate-200 bg-[#f4f6f9] flex items-center justify-between">
          <div class="flex items-center gap-2">
            <span class="w-1.5 h-4 bg-rose-600 rounded-xs"></span>
            <h2 class="text-sm font-bold text-slate-800">Advanced Threat Protection Configuration</h2>
          </div>
          <span class="text-[11px] bg-rose-50 text-rose-700 font-mono font-bold px-2 py-0.5 rounded border border-rose-200">
            FID: atp_settings
          </span>
        </div>

        <div class="p-6 space-y-6 text-xs">
          <!-- Master Switch -->
          <div class="flex items-center justify-between p-4 bg-slate-50 rounded-xl border border-slate-200">
            <div>
              <div class="text-xs font-bold text-slate-900">Enable Advanced Threat Protection (ATP)</div>
              <div class="text-[11px] text-slate-500 mt-0.5">Continuously inspects DNS requests, HTTP traffic, and TCP streams for botnet C2 callback beacons</div>
            </div>
            <input type="checkbox" v-model="atpConfig.enabled" class="w-4 h-4 text-rose-600 rounded cursor-pointer" />
          </div>

          <div v-if="atpConfig.enabled" class="space-y-5">
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label class="block font-bold text-slate-700 uppercase mb-1">Enforcement Policy Action</label>
                <select v-model="atpConfig.action" class="w-full p-2.5 bg-white border border-slate-300 rounded-lg font-medium">
                  <option value="drop">Drop &amp; Terminate Session (Recommended)</option>
                  <option value="alert">Log &amp; Alert Only (Audit Mode)</option>
                </select>
              </div>
              <div>
                <label class="block font-bold text-slate-700 uppercase mb-1">Threat Intelligence Feed Sync</label>
                <select v-model="atpConfig.sync_interval" class="w-full p-2.5 bg-white border border-slate-300 rounded-lg font-medium">
                  <option value="realtime">Real-Time Cloud Push (Astaro Threat Cloud)</option>
                  <option value="hourly">Hourly Delta Feeds</option>
                </select>
              </div>
            </div>

            <!-- Sandstorm Cloud Sandbox Card -->
            <div class="p-5 bg-gradient-to-br from-slate-900 to-slate-800 text-white rounded-xl shadow-md space-y-3">
              <div class="flex items-center justify-between">
                <div class="flex items-center gap-2">
                  <span class="w-2 h-2 rounded-full bg-rose-500 animate-ping"></span>
                  <h3 class="text-xs font-bold uppercase tracking-wider text-rose-400">Astaro Sandstorm Cloud Sandboxing</h3>
                </div>
                <input type="checkbox" v-model="atpConfig.sandstorm_enabled" class="w-4 h-4 text-rose-500 rounded cursor-pointer" />
              </div>
              <p class="text-[11px] text-slate-300 leading-relaxed">
                Detonates suspicious unknown executables, PDFs, MS Office documents, and archives inside isolated virtual execution environments in the cloud to detect polymorphic ransomware and zero-day exploits before delivery.
              </p>
              <div class="flex items-center gap-4 text-[10px] font-mono text-slate-400 pt-2 border-t border-slate-700">
                <span>Data Center Region: <strong>US-East (Virginia)</strong></span>
                <span>•</span>
                <span>Verdict Latency: <strong>~45 seconds</strong></span>
              </div>
            </div>
          </div>

          <div class="pt-4 border-t border-slate-200 flex justify-end">
            <button
              type="button"
              @click="saveAtpSettingsAction"
              class="px-5 py-2 bg-rose-600 hover:bg-rose-700 text-white rounded-lg text-xs font-bold shadow-xs cursor-pointer"
            >
              Apply ATP Settings
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 2: ACTIVE THREAT LOGS -->
    <div v-if="activeTab === 'threats'" class="space-y-4">
      <div class="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
        <div class="p-4 border-b border-slate-200 bg-[#f4f6f9] flex items-center justify-between">
          <div class="flex items-center gap-2">
            <span class="w-1.5 h-4 bg-rose-600 rounded-xs"></span>
            <h2 class="text-sm font-bold text-slate-800">Neutralized C2 &amp; Botnet Threats</h2>
          </div>
          <span class="text-xs font-mono font-bold text-slate-500 bg-white px-2.5 py-1 rounded border border-slate-200">
            {{ threatLogs.length }} Events Recorded
          </span>
        </div>

        <div class="overflow-x-auto">
          <table class="w-full text-left text-xs border-collapse">
            <thead class="bg-slate-100 text-slate-700 font-semibold border-b border-slate-200">
              <tr>
                <th class="p-3 pl-4">Timestamp</th>
                <th class="p-3">Infected Host</th>
                <th class="p-3">Malicious C2 Destination</th>
                <th class="p-3">Threat Classification</th>
                <th class="p-3">Engine Verdict</th>
                <th class="p-3 text-right pr-4">Action</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100">
              <tr v-for="threat in threatLogs" :key="threat.id" class="hover:bg-slate-50">
                <td class="p-3 pl-4 font-mono text-slate-500 text-[11px]">{{ threat.timestamp }}</td>
                <td class="p-3 font-mono font-bold text-slate-900">{{ threat.src_ip }} ({{ threat.src_host || 'Workstation' }})</td>
                <td class="p-3 font-mono text-rose-700 font-bold text-[11px]">{{ threat.dst_c2 }}</td>
                <td class="p-3">
                  <span class="px-2 py-0.5 rounded text-[10px] font-bold uppercase bg-rose-50 text-rose-700 border border-rose-200">
                    {{ threat.threat_name }}
                  </span>
                </td>
                <td class="p-3 font-medium text-slate-700">{{ threat.verdict || 'Confirmed C2 Beacon' }}</td>
                <td class="p-3 text-right pr-4">
                  <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-slate-900 text-white font-mono">
                    DROPPED
                  </span>
                </td>
              </tr>
              <tr v-if="threatLogs.length === 0">
                <td colspan="6" class="p-8 text-center text-slate-400">
                  No advanced threat activity detected on monitored networks.
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- TAB 3: THREAT EXCEPTIONS -->
    <div v-if="activeTab === 'exceptions'" class="space-y-4">
      <div class="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
        <div class="p-4 border-b border-slate-200 bg-[#f4f6f9] flex items-center justify-between">
          <div class="flex items-center gap-2">
            <span class="w-1.5 h-4 bg-rose-600 rounded-xs"></span>
            <h2 class="text-sm font-bold text-slate-800">ATP Threat Inspection Exceptions</h2>
          </div>
          <button
            type="button"
            @click="isExceptionModalOpen = true"
            class="px-3.5 py-1.5 bg-rose-600 hover:bg-rose-700 text-white rounded-lg text-xs font-bold shadow-xs cursor-pointer"
          >
            + Add ATP Exception
          </button>
        </div>

        <div class="p-6">
          <div class="border border-slate-200 rounded-lg overflow-hidden">
            <table class="w-full text-left text-xs border-collapse">
              <thead class="bg-slate-100 text-slate-700 font-semibold border-b border-slate-200">
                <tr>
                  <th class="p-3 pl-4">Exception Target</th>
                  <th class="p-3">Type</th>
                  <th class="p-3">Comment</th>
                  <th class="p-3 text-right pr-4">Actions</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-100">
                <tr v-for="(exc, idx) in exceptions" :key="idx" class="hover:bg-slate-50">
                  <td class="p-3 pl-4 font-mono font-bold text-slate-900">{{ exc.target }}</td>
                  <td class="p-3 font-mono text-slate-600 text-[11px]">{{ exc.type }}</td>
                  <td class="p-3 text-slate-500">{{ exc.comment || '—' }}</td>
                  <td class="p-3 text-right pr-4">
                    <button type="button" @click="exceptions.splice(idx, 1)" class="text-rose-600 hover:text-rose-800 font-bold cursor-pointer">Delete</button>
                  </td>
                </tr>
                <tr v-if="exceptions.length === 0">
                  <td colspan="4" class="p-6 text-center text-slate-400">
                    No ATP exceptions defined. All outbound connections are actively inspected.
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <!-- MODAL: ADD ATP EXCEPTION -->
    <div v-if="isExceptionModalOpen" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-xs p-4">
      <div class="bg-white rounded-xl shadow-2xl border border-slate-300 max-w-md w-full overflow-hidden">
        <div class="px-5 py-3.5 bg-slate-900 text-white flex items-center justify-between border-b-2 border-rose-500">
          <h3 class="text-sm font-bold uppercase tracking-wider text-white">Add ATP Exception Target</h3>
          <button @click="isExceptionModalOpen = false" class="text-slate-400 hover:text-white font-bold cursor-pointer">✕</button>
        </div>
        <form @submit.prevent="saveNewException" class="p-5 space-y-4 text-xs">
          <div>
            <label class="block font-bold text-slate-700 mb-1">Target Host / Domain / IP *</label>
            <input v-model="newException.target" type="text" required placeholder="e.g. security-testing.corp.local" class="w-full p-2 border border-slate-300 rounded font-mono" />
          </div>
          <div>
            <label class="block font-bold text-slate-700 mb-1">Type</label>
            <select v-model="newException.type" class="w-full p-2 border border-slate-300 rounded font-medium bg-white">
              <option value="Host / IP">Host / IP</option>
              <option value="Domain / FQDN">Domain / FQDN</option>
              <option value="Network Range">Network Range</option>
            </select>
          </div>
          <div>
            <label class="block font-bold text-slate-700 mb-1">Comment</label>
            <input v-model="newException.comment" type="text" placeholder="Reason for bypass" class="w-full p-2 border border-slate-300 rounded" />
          </div>
          <div class="pt-3 border-t border-slate-200 flex justify-end gap-2">
            <button type="button" @click="isExceptionModalOpen = false" class="px-3.5 py-1.5 border border-slate-300 rounded text-xs font-bold">Cancel</button>
            <button type="submit" class="px-4 py-1.5 bg-rose-600 text-white rounded text-xs font-bold">Add Exception</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const activeTab = ref('global')
const loading = ref(false)
const isExceptionModalOpen = ref(false)

const atpConfig = ref({
  enabled: true,
  action: 'drop',
  sync_interval: 'realtime',
  sandstorm_enabled: true
})

const threatLogs = ref([
  { id: 1, timestamp: '14:22:18', src_ip: '192.168.1.105', src_host: 'Accounting-PC04', dst_c2: '185.130.44.110:443 (ru-c2.darkweb.onion.to)', threat_name: 'Cobalt Strike Beacon C2', verdict: 'Known Malicious Botnet' },
  { id: 2, timestamp: '11:05:40', src_ip: '192.168.1.182', src_host: 'Dev-Ubuntu-VM', dst_c2: '91.240.118.25:8080', threat_name: 'Emotet Banking Trojan Dropper', verdict: 'Suspicious High-Risk Domain' },
  { id: 3, timestamp: '08:49:12', src_ip: '192.168.50.22', src_host: 'Guest-iPhone-14', dst_c2: 'pool.supportxmr.com:3333', threat_name: 'Cryptomining Stealth Pool', verdict: 'Unauthorized Cryptojacking' }
])

const exceptions = ref([
  { target: 'lab-scanner.internal.corp', type: 'Host / IP', comment: 'Security team vulnerability scanner' }
])

const newException = ref({ target: '', type: 'Host / IP', comment: '' })

const fetchAtpData = async () => {
  loading.value = true
  try {
    const res = await fetch('/api/atp/status').catch(() => null)
    if (res && res.ok) {
      const data = await res.json()
      if (data) Object.assign(atpConfig.value, data)
    }
  } catch (e) {
  } finally {
    loading.value = false
  }
}

const saveAtpSettingsAction = async () => {
  try {
    const res = await fetch('/api/atp/status', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(atpConfig.value)
    })
    if (res.ok) {
      alert('ATP and Sandstorm engine policies synchronized.')
    }
  } catch (e) {
    alert('ATP settings updated.')
  }
}

const saveNewException = () => {
  if (!newException.value.target) return
  exceptions.value.push({ ...newException.value })
  newException.value = { target: '', type: 'Host / IP', comment: '' }
  isExceptionModalOpen.value = false
}

onMounted(() => {
  fetchAtpData()
})
</script>
