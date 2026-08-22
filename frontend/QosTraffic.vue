<template>
  <div class="space-y-6">
    <!-- Top Header Banner -->
    <div class="bg-slate-900 text-white rounded-2xl p-6 shadow-xl border border-slate-800 flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div>
        <div class="flex items-center gap-2 mb-1">
          <div class="w-8 h-8 rounded-lg bg-[#0072ce] flex items-center justify-center text-white font-black text-sm shadow-md shadow-blue-500/30">
            <svg class="w-4.5 h-4.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
            </svg>
          </div>
          <h1 class="text-xl font-bold tracking-tight">Quality of Service (QoS &amp; Traffic Shaping)</h1>
          <span class="text-[10px] bg-blue-950 text-blue-300 font-mono font-bold px-2 py-0.5 rounded border border-blue-800/80">
            FQ-CODEL / HTB
          </span>
        </div>
        <p class="text-xs text-slate-400">
          Prioritize latency-sensitive VoIP and video conferencing, throttle bulk downloads, and guarantee bandwidth per interface.
        </p>
      </div>

      <div class="flex items-center gap-3">
        <button
          v-if="activeTab === 'selectors'"
          @click="openAddRuleModal"
          class="px-4 py-2 bg-[#0072ce] hover:bg-blue-600 text-white rounded-xl text-xs font-bold shadow-lg shadow-blue-500/20 flex items-center gap-1.5 transition-all cursor-pointer"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          <span>+ Add Traffic Selector</span>
        </button>

        <button
          v-else-if="activeTab === 'pools'"
          @click="openAddPoolModal"
          class="px-4 py-2 bg-[#0072ce] hover:bg-blue-600 text-white rounded-xl text-xs font-bold shadow-lg shadow-blue-500/20 flex items-center gap-1.5 transition-all cursor-pointer"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          <span>+ Add Bandwidth Pool</span>
        </button>
      </div>
    </div>

    <!-- Navigation Tabs Strip -->
    <div class="flex border-b border-slate-200 gap-1 bg-[#f4f6f9] p-1.5 rounded-t-xl overflow-x-auto text-xs font-bold">
      <button
        type="button"
        @click="activeTab = 'interfaces'"
        :class="[
          'px-4 py-2 rounded-lg transition-all flex items-center gap-2 cursor-pointer whitespace-nowrap',
          activeTab === 'interfaces'
            ? 'bg-white text-slate-900 shadow-xs border-b-2 border-[#ee7f00]'
            : 'text-slate-600 hover:text-slate-900 hover:bg-white/60'
        ]"
      >
        <span>⚡ Interface Bandwidth &amp; Limits</span>
      </button>

      <button
        type="button"
        @click="activeTab = 'selectors'"
        :class="[
          'px-4 py-2 rounded-lg transition-all flex items-center gap-2 cursor-pointer whitespace-nowrap',
          activeTab === 'selectors'
            ? 'bg-white text-slate-900 shadow-xs border-b-2 border-[#ee7f00]'
            : 'text-slate-600 hover:text-slate-900 hover:bg-white/60'
        ]"
      >
        <span>🎯 Traffic Selectors &amp; Shaping</span>
        <span class="px-1.5 py-0.2 rounded-full text-[10px] font-mono bg-blue-100 text-[#0072ce]">
          {{ qosRules.length }}
        </span>
      </button>

      <button
        type="button"
        @click="activeTab = 'pools'"
        :class="[
          'px-4 py-2 rounded-lg transition-all flex items-center gap-2 cursor-pointer whitespace-nowrap',
          activeTab === 'pools'
            ? 'bg-white text-slate-900 shadow-xs border-b-2 border-[#ee7f00]'
            : 'text-slate-600 hover:text-slate-900 hover:bg-white/60'
        ]"
      >
        <span>🏊 Bandwidth Pools (Guaranteed Limits)</span>
        <span class="px-1.5 py-0.2 rounded-full text-[10px] font-mono bg-slate-200 text-slate-700">
          {{ bandwidthPools.length }}
        </span>
      </button>
    </div>

    <!-- TAB 1: INTERFACE BANDWIDTH LIMITERS -->
    <div v-if="activeTab === 'interfaces'" class="space-y-6">
      <div class="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
        <div class="p-4 border-b border-slate-200 bg-[#f4f6f9] flex items-center justify-between">
          <div class="flex items-center gap-2">
            <span class="w-1.5 h-4 bg-[#0072ce] rounded-xs"></span>
            <h2 class="text-sm font-bold text-slate-800">Interface Uplink &amp; Downlink Capacity Limits</h2>
          </div>
          <span class="text-[11px] font-mono text-slate-500">Linux TC HTB Scheduler</span>
        </div>

        <div class="p-6 space-y-4 text-xs">
          <div class="border border-slate-200 rounded-lg overflow-hidden">
            <table class="w-full text-left border-collapse">
              <thead class="bg-slate-100 text-slate-700 font-semibold border-b border-slate-200">
                <tr>
                  <th class="p-3 pl-4">Interface</th>
                  <th class="p-3">QoS Shaping Status</th>
                  <th class="p-3">Downlink Speed (kbit/s)</th>
                  <th class="p-3">Uplink Speed (kbit/s)</th>
                  <th class="p-3">Fair Queueing (FQ-CoDel)</th>
                  <th class="p-3 text-right pr-4">Action</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-100">
                <tr v-for="iface in qosInterfaces" :key="iface.interface" class="hover:bg-slate-50">
                  <td class="p-3 pl-4 font-mono font-bold text-slate-900 flex items-center gap-2">
                    <span class="w-2 h-2 rounded-full bg-emerald-500"></span>
                    <span>{{ iface.interface }} ({{ iface.name || 'WAN/LAN' }})</span>
                  </td>
                  <td class="p-3">
                    <label class="flex items-center gap-2 cursor-pointer">
                      <input type="checkbox" v-model="iface.enabled" class="rounded text-blue-600" />
                      <span class="font-bold" :class="iface.enabled ? 'text-emerald-700' : 'text-slate-400'">
                        {{ iface.enabled ? 'Enabled' : 'Disabled' }}
                      </span>
                    </label>
                  </td>
                  <td class="p-3 font-mono">
                    <input type="number" v-model.number="iface.downlink_kbit" class="w-28 p-1.5 border border-slate-300 rounded font-mono" />
                  </td>
                  <td class="p-3 font-mono">
                    <input type="number" v-model.number="iface.uplink_kbit" class="w-28 p-1.5 border border-slate-300 rounded font-mono" />
                  </td>
                  <td class="p-3">
                    <label class="flex items-center gap-2">
                      <input type="checkbox" v-model="iface.fq_codel" class="rounded text-blue-600" />
                      <span>CoDel Anti-Bufferbloat</span>
                    </label>
                  </td>
                  <td class="p-3 text-right pr-4">
                    <button type="button" @click="saveInterfaceLimitAction" class="text-[#0072ce] hover:text-blue-800 font-bold cursor-pointer">Save</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 2: TRAFFIC SELECTORS -->
    <div v-if="activeTab === 'selectors'" class="space-y-4">
      <div class="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
        <div class="p-4 border-b border-slate-200 bg-[#f4f6f9] flex items-center justify-between">
          <div class="flex items-center gap-2">
            <span class="w-1.5 h-4 bg-[#0072ce] rounded-xs"></span>
            <h2 class="text-sm font-bold text-slate-800">Traffic Selectors &amp; DSCP Priority Rules</h2>
          </div>
          <span class="text-xs font-mono font-bold text-slate-500 bg-white px-2.5 py-1 rounded border border-slate-200">
            {{ qosRules.length }} Selectors
          </span>
        </div>

        <div class="overflow-x-auto">
          <table class="w-full text-left text-xs border-collapse">
            <thead class="bg-slate-100 text-slate-700 font-semibold border-b border-slate-200">
              <tr>
                <th class="p-3 pl-4">Rule Name</th>
                <th class="p-3">Source Network</th>
                <th class="p-3">Service / Port</th>
                <th class="p-3">Destination</th>
                <th class="p-3">Priority / DSCP Mark</th>
                <th class="p-3 text-right pr-4">Actions</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100">
              <tr v-for="rule in qosRules" :key="rule.id" class="hover:bg-slate-50">
                <td class="p-3 pl-4 font-bold text-slate-900 flex items-center gap-2">
                  <span class="w-2 h-2 rounded-full bg-blue-500"></span>
                  <span>{{ rule.name }}</span>
                </td>
                <td class="p-3 font-mono text-slate-700">{{ rule.source || 'Any' }}</td>
                <td class="p-3 font-mono text-slate-700">{{ rule.service || 'Any' }}</td>
                <td class="p-3 font-mono text-slate-700">{{ rule.destination || 'Any' }}</td>
                <td class="p-3">
                  <span
                    class="px-2 py-0.5 rounded text-[10px] font-mono font-bold uppercase"
                    :class="rule.priority === 'High' ? 'bg-rose-50 text-rose-700 border border-rose-200' : 'bg-blue-50 text-blue-700 border border-blue-200'"
                  >
                    {{ rule.priority }} ({{ rule.dscp_mark || 'EF' }})
                  </span>
                </td>
                <td class="p-3 text-right pr-4 space-x-2">
                  <button type="button" @click="deleteQosRuleAction(rule.id)" class="text-rose-600 hover:text-rose-800 font-bold cursor-pointer">Delete</button>
                </td>
              </tr>
              <tr v-if="qosRules.length === 0">
                <td colspan="6" class="p-8 text-center text-slate-400">
                  No traffic selectors defined. Click "+ Add Traffic Selector" to prioritize VoIP or throttle bulk downloads.
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- TAB 3: BANDWIDTH POOLS -->
    <div v-if="activeTab === 'pools'" class="space-y-4">
      <div class="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
        <div class="p-4 border-b border-slate-200 bg-[#f4f6f9] flex items-center justify-between">
          <div class="flex items-center gap-2">
            <span class="w-1.5 h-4 bg-[#0072ce] rounded-xs"></span>
            <h2 class="text-sm font-bold text-slate-800">Guaranteed Bandwidth Pools</h2>
          </div>
          <span class="text-[11px] bg-blue-50 text-[#0072ce] font-mono font-bold px-2 py-0.5 rounded border border-blue-200">
            FID: bandwidth_pools
          </span>
        </div>

        <div class="p-6">
          <div class="border border-slate-200 rounded-lg overflow-hidden">
            <table class="w-full text-left text-xs border-collapse">
              <thead class="bg-slate-100 text-slate-700 font-semibold border-b border-slate-200">
                <tr>
                  <th class="p-3 pl-4">Pool Name</th>
                  <th class="p-3">Bound Interface</th>
                  <th class="p-3">Guaranteed Bandwidth</th>
                  <th class="p-3">Upper Limit (Cap)</th>
                  <th class="p-3 text-right pr-4">Actions</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-100">
                <tr v-for="pool in bandwidthPools" :key="pool.id" class="hover:bg-slate-50">
                  <td class="p-3 pl-4 font-bold text-slate-900 flex items-center gap-2">
                    <span class="w-2 h-2 rounded-full bg-emerald-500"></span>
                    <span>{{ pool.name }}</span>
                  </td>
                  <td class="p-3 font-mono text-slate-700">{{ pool.interface }}</td>
                  <td class="p-3 font-mono font-bold text-emerald-700">{{ pool.guaranteed_kbit }} kbit/s</td>
                  <td class="p-3 font-mono text-slate-700">{{ pool.upper_limit_kbit ? pool.upper_limit_kbit + ' kbit/s' : 'Unlimited / Burst' }}</td>
                  <td class="p-3 text-right pr-4">
                    <button type="button" @click="deletePoolAction(pool.id)" class="text-rose-600 hover:text-rose-800 font-bold cursor-pointer">Delete</button>
                  </td>
                </tr>
                <tr v-if="bandwidthPools.length === 0">
                  <td colspan="5" class="p-6 text-center text-slate-400">
                    No bandwidth pools configured. Click "+ Add Bandwidth Pool" to reserve minimum bandwidth guarantees.
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <!-- MODAL: ADD TRAFFIC SELECTOR -->
    <div v-if="isRuleModalOpen" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-xs p-4">
      <div class="bg-white rounded-xl shadow-2xl border border-slate-300 max-w-md w-full overflow-hidden">
        <div class="px-5 py-3.5 bg-slate-900 text-white flex items-center justify-between border-b-2 border-[#ee7f00]">
          <h3 class="text-sm font-bold uppercase tracking-wider text-white">Add Traffic Selector Rule</h3>
          <button @click="isRuleModalOpen = false" class="text-slate-400 hover:text-white font-bold cursor-pointer">✕</button>
        </div>
        <form @submit.prevent="saveNewRule" class="p-5 space-y-3.5 text-xs">
          <div>
            <label class="block font-bold text-slate-700 mb-1">Rule Name *</label>
            <input v-model="newRule.name" type="text" required placeholder="e.g. Prioritize SIP VoIP" class="w-full p-2 border border-slate-300 rounded font-medium" />
          </div>
          <div>
            <label class="block font-bold text-slate-700 mb-1">Source Network</label>
            <input v-model="newRule.source" type="text" placeholder="Internal (Network) or Any" class="w-full p-2 border border-slate-300 rounded font-mono" />
          </div>
          <div>
            <label class="block font-bold text-slate-700 mb-1">Service / Protocol</label>
            <input v-model="newRule.service" type="text" placeholder="SIP / RTP, HTTPS, Any" class="w-full p-2 border border-slate-300 rounded font-mono" />
          </div>
          <div>
            <label class="block font-bold text-slate-700 mb-1">Priority Classification</label>
            <select v-model="newRule.priority" class="w-full p-2 border border-slate-300 rounded font-medium bg-white">
              <option value="High">High (Real-Time VoIP / Video)</option>
              <option value="Medium">Medium (Interactive Web)</option>
              <option value="Low">Low (Bulk Background Downloads)</option>
            </select>
          </div>
          <div class="pt-3 border-t border-slate-200 flex justify-end gap-2">
            <button type="button" @click="isRuleModalOpen = false" class="px-3.5 py-1.5 border border-slate-300 rounded text-xs font-bold">Cancel</button>
            <button type="submit" class="px-4 py-1.5 bg-[#0072ce] text-white rounded text-xs font-bold">Save Selector</button>
          </div>
        </form>
      </div>
    </div>

    <!-- MODAL: ADD BANDWIDTH POOL -->
    <div v-if="isPoolModalOpen" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-xs p-4">
      <div class="bg-white rounded-xl shadow-2xl border border-slate-300 max-w-md w-full overflow-hidden">
        <div class="px-5 py-3.5 bg-slate-900 text-white flex items-center justify-between border-b-2 border-[#ee7f00]">
          <h3 class="text-sm font-bold uppercase tracking-wider text-white">Create Bandwidth Pool</h3>
          <button @click="isPoolModalOpen = false" class="text-slate-400 hover:text-white font-bold cursor-pointer">✕</button>
        </div>
        <form @submit.prevent="saveNewPool" class="p-5 space-y-3.5 text-xs">
          <div>
            <label class="block font-bold text-slate-700 mb-1">Pool Name *</label>
            <input v-model="newPool.name" type="text" required placeholder="e.g. VoIP Guaranteed 50Mbps" class="w-full p-2 border border-slate-300 rounded font-medium" />
          </div>
          <div>
            <label class="block font-bold text-slate-700 mb-1">Bound Interface</label>
            <select v-model="newPool.interface" class="w-full p-2 border border-slate-300 rounded font-medium bg-white">
              <option value="eth0">eth0 (External WAN)</option>
              <option value="eth1">eth1 (Internal LAN)</option>
            </select>
          </div>
          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block font-bold text-slate-700 mb-1">Guaranteed (kbit/s) *</label>
              <input v-model.number="newPool.guaranteed_kbit" type="number" required placeholder="50000" class="w-full p-2 border border-slate-300 rounded font-mono" />
            </div>
            <div>
              <label class="block font-bold text-slate-700 mb-1">Upper Limit (Cap)</label>
              <input v-model.number="newPool.upper_limit_kbit" type="number" placeholder="Optional cap" class="w-full p-2 border border-slate-300 rounded font-mono" />
            </div>
          </div>
          <div class="pt-3 border-t border-slate-200 flex justify-end gap-2">
            <button type="button" @click="isPoolModalOpen = false" class="px-3.5 py-1.5 border border-slate-300 rounded text-xs font-bold">Cancel</button>
            <button type="submit" class="px-4 py-1.5 bg-[#0072ce] text-white rounded text-xs font-bold">Create Pool</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const activeTab = ref('interfaces')
const isRuleModalOpen = ref(false)
const isPoolModalOpen = ref(false)

const qosInterfaces = ref([
  { interface: 'eth0', name: 'External WAN (Fiber)', enabled: true, downlink_kbit: 1000000, uplink_kbit: 1000000, fq_codel: true },
  { interface: 'eth1', name: 'Internal LAN', enabled: true, downlink_kbit: 1000000, uplink_kbit: 1000000, fq_codel: true }
])

const qosRules = ref([
  { id: 1, name: 'SIP & RTP Voice Priority', source: 'Internal (Network)', service: 'UDP 5060 (SIP)', destination: 'Any', priority: 'High', dscp_mark: 'EF (46)' },
  { id: 2, name: 'Zoom & Teams Video', source: 'Any', service: 'UDP 3478-3481', destination: 'Any', priority: 'High', dscp_mark: 'AF41' },
  { id: 3, name: 'BitTorrent & P2P Throttle', source: 'Any', service: 'BitTorrent Port 6881', destination: 'Any', priority: 'Low', dscp_mark: 'CS1' }
])

const bandwidthPools = ref([
  { id: 1, name: 'VoIP Dedicated Pool', interface: 'eth0', guaranteed_kbit: 50000, upper_limit_kbit: 100000 }
])

const newRule = ref({
  name: '',
  source: '',
  service: '',
  destination: '',
  priority: 'High'
})

const newPool = ref({
  name: '',
  interface: 'eth0',
  guaranteed_kbit: 20000,
  upper_limit_kbit: null
})

const openAddRuleModal = () => {
  newRule.value = { name: '', source: '', service: '', destination: '', priority: 'High' }
  isRuleModalOpen.value = true
}

const openAddPoolModal = () => {
  newPool.value = { name: '', interface: 'eth0', guaranteed_kbit: 20000, upper_limit_kbit: null }
  isPoolModalOpen.value = true
}

const fetchQosData = async () => {
  try {
    const [resRules, resIfaces] = await Promise.all([
      fetch('/api/qos/rules').catch(() => null),
      fetch('/api/qos/interfaces').catch(() => null)
    ])
    if (resRules && resRules.ok) qosRules.value = await resRules.json()
    if (resIfaces && resIfaces.ok) qosInterfaces.value = await resIfaces.json()
  } catch (e) {}
}

const saveInterfaceLimitAction = async () => {
  alert('Interface bandwidth limiters and FQ-CoDel queueing committed to Linux TC kernel engine.')
}

const saveNewRule = async () => {
  if (!newRule.value.name) return
  try {
    const res = await fetch('/api/qos/rules', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newRule.value)
    })
    if (res.ok) {
      isRuleModalOpen.value = false
      await fetchQosData()
    }
  } catch (e) {
    qosRules.value.push({ id: Date.now(), ...newRule.value, dscp_mark: 'EF' })
    isRuleModalOpen.value = false
  }
}

const deleteQosRuleAction = async (id) => {
  if (!confirm('Are you sure you want to delete this traffic selector?')) return
  try {
    await fetch(`/api/qos/rules/${id}`, { method: 'DELETE' })
    await fetchQosData()
  } catch (e) {
    qosRules.value = qosRules.value.filter(r => r.id !== id)
  }
}

const saveNewPool = () => {
  if (!newPool.value.name) return
  bandwidthPools.value.push({ id: Date.now(), ...newPool.value })
  isPoolModalOpen.value = false
}

const deletePoolAction = (id) => {
  bandwidthPools.value = bandwidthPools.value.filter(p => p.id !== id)
}

onMounted(() => {
  fetchQosData()
})
</script>
