<template>
  <div class="space-y-6">
    <!-- Header Section -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-slate-200 pb-4">
      <div>
        <div class="flex items-center gap-2">
          <span class="w-1.5 h-5 bg-[#ee7f00] rounded-full"></span>
          <h1 class="text-xl font-bold text-slate-900">NAT & Masquerading Rules</h1>
        </div>
        <p class="text-xs text-slate-500 mt-1">
          Configure Outbound Masquerading (Source NAT) and Inbound Port Forwarding (Destination NAT) with real-time NFTables synchronization.
        </p>
      </div>
      <div class="flex items-center gap-2">
        <button
          type="button"
          @click="openCreateModal"
          class="inline-flex items-center gap-2 px-3.5 py-1.5 rounded bg-[#005299] hover:bg-[#003d73] text-white text-xs font-bold shadow-xs transition-colors cursor-pointer"
        >
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          <span>New NAT Rule</span>
        </button>
      </div>
    </div>

    <!-- Tab Navigation Strip (Sophos UTM Style) -->
    <div class="flex border-b border-slate-200 gap-1 bg-[#f4f6f9] p-1.5 rounded-t-lg">
      <button
        type="button"
        @click="activeTab = 'all'"
        :class="[
          'px-4 py-2 text-xs font-bold rounded-md transition-all flex items-center gap-2 cursor-pointer',
          activeTab === 'all'
            ? 'bg-white text-slate-900 shadow-xs border-b-2 border-[#ee7f00]'
            : 'text-slate-600 hover:text-slate-900 hover:bg-white/60'
        ]"
      >
        <span>All Rules ({{ natRules.length }})</span>
      </button>

      <button
        type="button"
        @click="activeTab = 'masquerading'"
        :class="[
          'px-4 py-2 text-xs font-bold rounded-md transition-all flex items-center gap-2 cursor-pointer',
          activeTab === 'masquerading'
            ? 'bg-white text-slate-900 shadow-xs border-b-2 border-[#ee7f00]'
            : 'text-slate-600 hover:text-slate-900 hover:bg-white/60'
        ]"
      >
        <span>Masquerading (SNAT)</span>
      </button>

      <button
        type="button"
        @click="activeTab = 'dnat'"
        :class="[
          'px-4 py-2 text-xs font-bold rounded-md transition-all flex items-center gap-2 cursor-pointer',
          activeTab === 'dnat'
            ? 'bg-white text-slate-900 shadow-xs border-b-2 border-[#ee7f00]'
            : 'text-slate-600 hover:text-slate-900 hover:bg-white/60'
        ]"
      >
        <span>DNAT (Port Forwarding)</span>
      </button>
    </div>

    <!-- Status Banner: NFTables Kernel Sync Indicator -->
    <div class="p-3 bg-emerald-50 border border-emerald-200 rounded-lg text-emerald-800 text-xs flex items-center justify-between">
      <div class="flex items-center gap-2">
        <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
        <span class="font-bold">NFTables Kernel NAT Acceleration Active:</span>
        <span>Outbound Masquerade & Inbound DNAT hooks synchronized.</span>
      </div>
      <span class="text-[11px] font-mono font-bold bg-emerald-100 px-2 py-0.5 rounded text-emerald-900">
        table ip astaro_nat
      </span>
    </div>

    <!-- NAT Rules Table -->
    <div class="bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden">
      <table class="w-full text-left text-xs border-collapse">
        <thead class="bg-[#f4f6f9] text-slate-700 font-bold border-b border-slate-200">
          <tr>
            <th class="p-3 pl-4 w-12 text-center">Status</th>
            <th class="p-3">Rule Name</th>
            <th class="p-3">Type</th>
            <th class="p-3">Traffic Source</th>
            <th class="p-3">Service / Port</th>
            <th class="p-3">Destination / Target</th>
            <th class="p-3">Comment</th>
            <th class="p-3 text-right pr-4">Actions</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-100">
          <tr
            v-for="(rule, idx) in filteredRules"
            :key="rule.id"
            :class="idx % 2 === 0 ? 'bg-white' : 'bg-[#f7f7f7]'"
            class="hover:bg-blue-50/50 transition-colors"
          >
            <!-- Toggle Slider -->
            <td class="p-3 pl-4 text-center">
              <button
                type="button"
                @click="toggleRule(rule)"
                class="relative inline-flex h-4 w-8 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none"
                :class="rule.enabled ? 'bg-[#005299]' : 'bg-slate-300'"
              >
                <span
                  class="pointer-events-none inline-block h-3 w-3 transform rounded-full bg-white shadow-sm ring-0 transition duration-200 ease-in-out"
                  :class="rule.enabled ? 'translate-x-4' : 'translate-x-0'"
                ></span>
              </button>
            </td>

            <td class="p-3 font-bold text-slate-900">
              {{ rule.name }}
            </td>

            <td class="p-3">
              <span
                :class="[
                  'px-2 py-0.5 rounded text-[10px] font-bold uppercase border',
                  rule.type === 'Masquerading'
                    ? 'bg-blue-50 text-[#005299] border-blue-200'
                    : 'bg-amber-50 text-amber-800 border-amber-200'
                ]"
              >
                {{ rule.type }}
              </span>
            </td>

            <td class="p-3 font-mono font-semibold text-slate-700">
              {{ rule.source_network || rule.traffic_source || 'Any' }}
            </td>

            <td class="p-3 font-mono text-slate-900 font-bold">
              {{ rule.traffic_service || 'Any' }}
            </td>

            <td class="p-3 font-mono">
              <div v-if="rule.type === 'Masquerading'" class="text-slate-600">
                &rarr; {{ rule.outbound_interface }}
              </div>
              <div v-else class="text-emerald-700 font-bold">
                &rarr; {{ rule.destination_nat_target }}:{{ rule.service_translation || 'Same' }}
              </div>
            </td>

            <td class="p-3 text-slate-500 text-[11px] truncate max-w-xs">
              {{ rule.comment || '—' }}
            </td>

            <td class="p-3 text-right pr-4 space-x-2">
              <button
                type="button"
                @click="deleteRule(rule.id)"
                class="text-rose-600 hover:text-rose-800 text-[11px] font-bold cursor-pointer"
              >
                Delete
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>    <!-- CREATE NAT RULE COMPACT MODAL -->
    <div
      v-if="isModalOpen"
      class="fixed inset-0 z-40 overflow-y-auto bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4"
    >
      <div class="bg-white rounded-2xl shadow-2xl border border-slate-200 max-w-lg w-full overflow-hidden flex flex-col my-6 max-h-[90vh]">
        <!-- Modal Header -->
        <div class="px-5 py-3.5 bg-slate-900 text-white flex items-center justify-between border-b border-slate-800">
          <div class="flex items-center gap-2.5">
            <div class="w-8 h-8 rounded-lg bg-[#005299] flex items-center justify-center text-white font-bold text-xs shadow-md">
              NAT
            </div>
            <div>
              <h3 class="text-xs font-bold uppercase tracking-wider text-white">Create New NAT Rule</h3>
              <p class="text-[10px] text-slate-400">Configure address and port translation</p>
            </div>
          </div>
          <button @click="isModalOpen = false" class="text-slate-400 hover:text-white font-bold cursor-pointer text-base leading-none">&times;</button>
        </div>

        <!-- Form Fields -->
        <div class="p-5 space-y-4 text-xs flex-1 overflow-y-auto">
          <div>
            <label class="block font-bold text-slate-700 mb-1">Rule Name *</label>
            <input
              v-model="newRule.name"
              type="text"
              placeholder="e.g. Masquerade LAN to WAN, Forward Web Port 443"
              class="w-full p-2 border border-slate-300 rounded focus:border-[#005299] focus:outline-none"
            />
          </div>

          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block font-bold text-slate-700 mb-1">Rule Type</label>
              <select
                v-model="newRule.type"
                class="w-full p-2 border border-slate-300 rounded focus:border-[#005299] focus:outline-none bg-white font-medium"
              >
                <option value="Masquerading">Masquerading (Outbound SNAT)</option>
                <option value="DNAT">DNAT (Port Forwarding)</option>
                <option value="SNAT">Source NAT (SNAT)</option>
                <option value="1:1 NAT">1:1 Full Cone NAT</option>
              </select>
            </div>
            <div>
              <label class="block font-bold text-slate-700 mb-1">Initial State</label>
              <select
                v-model="newRule.enabled"
                class="w-full p-2 border border-slate-300 rounded focus:border-[#005299] focus:outline-none bg-white font-medium"
              >
                <option :value="true">Enabled (Active)</option>
                <option :value="false">Disabled</option>
              </select>
            </div>
          </div>

          <!-- Masquerading specific -->
          <div v-if="newRule.type === 'Masquerading'" class="space-y-3 p-3 bg-[#f4f6f9] rounded-lg border border-slate-200">
            <div>
              <div class="flex items-center justify-between mb-1">
                <label class="block font-bold text-slate-700">Source Network / Group</label>
                <button
                  type="button"
                  @click="openInlineNetModal"
                  class="text-[11px] font-bold text-[#005299] hover:text-blue-800 flex items-center gap-1.5 bg-white px-2.5 py-1 rounded border border-slate-300 shadow-2xs cursor-pointer"
                >
                  <svg class="w-3.5 h-3.5 text-amber-500" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M2 6a2 2 0 012-2h5l2 2h5a2 2 0 012 2v6a2 2 0 01-2 2H4a2 2 0 01-2-2V6z" />
                  </svg>
                  <span>Add Network Definition / Group</span>
                </button>
              </div>
              <select
                v-model="newRule.source_network"
                class="w-full p-2 border border-slate-300 rounded bg-white font-mono"
              >
                <option v-for="net in networkDefs" :key="net.id" :value="net.name">
                  {{ net.name }} ({{ net.address }})
                </option>
                <option value="Internal (Network)">Internal (Network) [192.168.1.0/24]</option>
              </select>
            </div>
            <div>
              <label class="block font-bold text-slate-700 mb-1">Outbound Interface</label>
              <select
                v-model="newRule.outbound_interface"
                class="w-full p-2 border border-slate-300 rounded bg-white"
              >
                <option value="Uplink Interfaces (WAN)">Uplink Interfaces (WAN / External)</option>
                <option value="ens33">ens33 (WAN)</option>
                <option value="eth0">eth0 (WAN)</option>
              </select>
            </div>
          </div>

          <!-- DNAT specific -->
          <div v-else class="space-y-3 p-3 bg-amber-50/50 rounded-lg border border-amber-200">
            <div class="grid grid-cols-2 gap-3">
              <div>
                <div class="flex items-center justify-between mb-1">
                  <label class="block font-bold text-slate-700">Incoming Service</label>
                  <button
                    type="button"
                    @click="openInlineSrvModal"
                    class="text-[10px] font-bold text-[#005299] hover:text-blue-800 bg-white px-2 py-0.5 rounded border border-slate-300 cursor-pointer"
                  >
                    + New Service
                  </button>
                </div>
                <select
                  v-model="newRule.traffic_service"
                  class="w-full p-2 border border-slate-300 rounded bg-white"
                >
                  <option v-for="srv in serviceDefs" :key="srv.id" :value="srv.name">
                    {{ srv.name }} ({{ srv.protocol }}:{{ srv.dst_port }})
                  </option>
                  <option value="HTTPS">HTTPS (TCP:443)</option>
                  <option value="HTTP">HTTP (TCP:80)</option>
                  <option value="SSH">SSH (TCP:22)</option>
                </select>
              </div>
              <div>
                <label class="block font-bold text-slate-700 mb-1">Original Destination</label>
                <input
                  v-model="newRule.traffic_destination"
                  type="text"
                  placeholder="e.g. Uplink (WAN IP)"
                  class="w-full p-2 border border-slate-300 rounded bg-white"
                />
              </div>
            </div>

            <div class="grid grid-cols-2 gap-3">
              <div>
                <label class="block font-bold text-slate-700 mb-1">Target Host / IP</label>
                <input
                  v-model="newRule.destination_nat_target"
                  type="text"
                  placeholder="e.g. 192.168.1.100"
                  class="w-full p-2 border border-slate-300 rounded font-mono bg-white"
                />
              </div>
              <div>
                <label class="block font-bold text-slate-700 mb-1">Translated Port</label>
                <input
                  v-model="newRule.service_translation"
                  type="text"
                  placeholder="e.g. 443 (Leave blank for same)"
                  class="w-full p-2 border border-slate-300 rounded font-mono bg-white"
                />
              </div>
            </div>

            <div class="flex items-center gap-2 pt-1">
              <input
                id="auto-fw"
                v-model="newRule.auto_firewall_rule"
                type="checkbox"
                class="w-4 h-4 rounded border-slate-300 text-[#005299] focus:ring-[#005299]"
              />
              <label for="auto-fw" class="text-slate-700 font-bold">
                Automatic Firewall rule (Permit translated traffic)
              </label>
            </div>
          </div>

          <div>
            <label class="block font-bold text-slate-700 mb-1">Comment</label>
            <input
              v-model="newRule.comment"
              type="text"
              placeholder="Optional notes or documentation"
              class="w-full p-2 border border-slate-300 rounded focus:border-[#005299] focus:outline-none"
            />
          </div>
        </div>

        <!-- Modal Footer -->
        <div class="p-4 bg-[#f4f6f9] border-t border-slate-200 flex items-center justify-end gap-2">
          <button
            type="button"
            @click="isModalOpen = false"
            class="px-3.5 py-1.5 rounded border border-slate-300 bg-white text-slate-700 text-xs font-bold hover:bg-slate-50 cursor-pointer"
          >
            Cancel
          </button>
          <button
            type="button"
            @click="saveRule"
            class="px-4 py-1.5 rounded bg-[#005299] hover:bg-[#003d73] text-white text-xs font-bold shadow-xs cursor-pointer"
          >
            Save Rule
          </button>
        </div>
      </div>
    </div>

    <!-- INLINE NETWORK OBJECT / GROUP MODAL -->
    <div
      v-if="isInlineNetModalOpen"
      class="fixed inset-0 z-[100] bg-slate-950/70 backdrop-blur-xs flex items-center justify-center p-4"
    >
      <div class="w-full max-w-md bg-white rounded-xl border border-slate-200 shadow-2xl overflow-hidden">
        <div class="bg-[#005299] text-white px-4 py-3 flex items-center justify-between">
          <h3 class="text-xs font-bold uppercase tracking-wider">Add Network Definition</h3>
          <button @click="isInlineNetModalOpen = false" class="text-white/80 hover:text-white cursor-pointer font-bold">&times;</button>
        </div>
        <div class="p-4 space-y-3 text-xs">
          <div>
            <label class="block font-bold text-slate-700 mb-1">Name *</label>
            <input type="text" v-model="newInlineNet.name" placeholder="e.g. DMZ Servers" class="w-full p-2 border border-slate-300 rounded" />
          </div>
          <div>
            <label class="block font-bold text-slate-700 mb-1">Type</label>
            <select v-model="newInlineNet.type" class="w-full p-2 border border-slate-300 rounded bg-white">
              <option value="Host">Host</option>
              <option value="DNS host">DNS host</option>
              <option value="DNS group">DNS group</option>
              <option value="Network">Network</option>
              <option value="Range">Range</option>
              <option value="Multicast group">Multicast group</option>
              <option value="Network group">Network group</option>
              <option value="Availability Group">Availability Group</option>
            </select>
          </div>
          <div>
            <label class="block font-bold text-slate-700 mb-1">Address / Members *</label>
            <input type="text" v-model="newInlineNet.address" placeholder="192.168.1.50 or 10.0.0.0/24" class="w-full p-2 border border-slate-300 rounded font-mono" />
          </div>
        </div>
        <div class="px-4 py-2.5 bg-slate-50 border-t border-slate-200 flex justify-between">
          <button @click="isInlineNetModalOpen = false" class="px-3 py-1 text-xs border rounded text-slate-700 cursor-pointer">Cancel</button>
          <button @click="saveInlineNet" class="px-4 py-1 text-xs font-bold bg-[#005299] text-white rounded shadow-xs cursor-pointer">Save &amp; Use</button>
        </div>
      </div>
    </div>

    <!-- INLINE SERVICE DEFINITION MODAL -->
    <div
      v-if="isInlineSrvModalOpen"
      class="fixed inset-0 z-[100] bg-slate-950/70 backdrop-blur-xs flex items-center justify-center p-4"
    >
      <div class="w-full max-w-md bg-white rounded-xl border border-slate-200 shadow-2xl overflow-hidden">
        <div class="bg-[#005299] text-white px-4 py-3 flex items-center justify-between">
          <h3 class="text-xs font-bold uppercase tracking-wider">New Service Definition / Group</h3>
          <button @click="isInlineSrvModalOpen = false" class="text-white/80 hover:text-white cursor-pointer font-bold">&times;</button>
        </div>
        <div class="p-4 space-y-3 text-xs">
          <div>
            <label class="block font-bold text-slate-700 mb-1">Service Name *</label>
            <input type="text" v-model="newInlineSrv.name" placeholder="e.g. Minecraft Server" class="w-full p-2 border border-slate-300 rounded" />
          </div>
          <div>
            <label class="block font-bold text-slate-700 mb-1">Protocol / Type</label>
            <select v-model="newInlineSrv.type" class="w-full p-2 border border-slate-300 rounded bg-white">
              <option value="TCP">TCP</option>
              <option value="UDP">UDP</option>
              <option value="TCP/UDP">TCP/UDP</option>
              <option value="Service Group">Service Group</option>
            </select>
          </div>
          <div>
            <label class="block font-bold text-slate-700 mb-1">Destination Port *</label>
            <input type="text" v-model="newInlineSrv.dst_port" placeholder="e.g. 25565 or 8080:8090" class="w-full p-2 border border-slate-300 rounded font-mono" />
          </div>
        </div>
        <div class="px-4 py-2.5 bg-slate-50 border-t border-slate-200 flex justify-between">
          <button @click="isInlineSrvModalOpen = false" class="px-3 py-1 text-xs border rounded text-slate-700">Cancel</button>
          <button @click="saveInlineSrv" class="px-4 py-1 text-xs font-bold bg-[#005299] text-white rounded shadow-xs">Save &amp; Use</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const props = defineProps({
  authToken: {
    type: String,
    default: ''
  }
})

const activeTab = ref('all') // 'all' | 'masquerading' | 'dnat'
const isModalOpen = ref(false)
const isInlineNetModalOpen = ref(false)
const isInlineSrvModalOpen = ref(false)

const newInlineNet = ref({ name: '', type: 'Host', address: '' })
const newInlineSrv = ref({ name: '', type: 'TCP', dst_port: '' })

const natRules = ref([])
const networkDefs = ref([])
const serviceDefs = ref([])

const newRule = ref({
  name: '',
  type: 'Masquerading',
  enabled: true,
  source_network: 'Internal (Network)',
  outbound_interface: 'Uplink Interfaces (WAN)',
  traffic_source: 'Any',
  traffic_service: 'HTTPS',
  traffic_destination: 'Uplink (WAN IP)',
  destination_nat_target: '192.168.1.100',
  service_translation: '',
  auto_firewall_rule: true,
  comment: ''
})

const openInlineNetModal = () => {
  newInlineNet.value = { name: '', type: 'Host', address: '' }
  isInlineNetModalOpen.value = true
}

const openInlineSrvModal = () => {
  newInlineSrv.value = { name: '', type: 'TCP', dst_port: '' }
  isInlineSrvModalOpen.value = true
}

const saveInlineNet = async () => {
  if (!newInlineNet.value.name || !newInlineNet.value.address) return
  const axiosLib = (typeof window !== 'undefined' && window.axios) ? window.axios : null
  if (axiosLib) {
    try {
      await axiosLib.post('/api/definitions/networks', newInlineNet.value)
      await fetchNatRules()
    } catch (e) {
      console.error(e)
    }
  }
  newRule.value.source_network = newInlineNet.value.name
  isInlineNetModalOpen.value = false
}

const saveInlineSrv = async () => {
  if (!newInlineSrv.value.name || !newInlineSrv.value.dst_port) return
  const axiosLib = (typeof window !== 'undefined' && window.axios) ? window.axios : null
  if (axiosLib) {
    try {
      await axiosLib.post('/api/definitions/services', {
        name: newInlineSrv.value.name,
        type: newInlineSrv.value.type,
        protocol: newInlineSrv.value.type.includes('UDP') ? 'UDP' : 'TCP',
        dst_port: newInlineSrv.value.dst_port
      })
      await fetchNatRules()
    } catch (e) {
      console.error(e)
    }
  }
  newRule.value.traffic_service = newInlineSrv.value.name
  isInlineSrvModalOpen.value = false
}

const filteredRules = computed(() => {
  if (activeTab.value === 'masquerading') {
    return natRules.value.filter(r => r.type === 'Masquerading' || r.type === 'SNAT')
  }
  if (activeTab.value === 'dnat') {
    return natRules.value.filter(r => r.type === 'DNAT' || r.type === '1:1 NAT')
  }
  return natRules.value
})

const fetchNatRules = async () => {
  try {
    const axiosLib = (typeof window !== 'undefined' && window.axios) ? window.axios : null
    if (!axiosLib) return

    const [natRes, netRes, srvRes] = await Promise.all([
      axiosLib.get('/api/nat/rules'),
      axiosLib.get('/api/definitions/networks'),
      axiosLib.get('/api/definitions/services')
    ])
    if (natRes.data) natRules.value = natRes.data
    if (netRes.data) networkDefs.value = netRes.data
    if (srvRes.data) serviceDefs.value = srvRes.data
  } catch (err) {
    console.error('Failed to fetch NAT rules:', err)
  }
}

const openCreateModal = () => {
  newRule.value = {
    name: '',
    type: activeTab.value === 'dnat' ? 'DNAT' : 'Masquerading',
    enabled: true,
    source_network: 'Internal (Network)',
    outbound_interface: 'Uplink Interfaces (WAN)',
    traffic_source: 'Any',
    traffic_service: 'HTTPS',
    traffic_destination: 'Uplink (WAN IP)',
    destination_nat_target: '192.168.1.100',
    service_translation: '',
    auto_firewall_rule: true,
    comment: ''
  }
  isModalOpen.value = true
}

const saveRule = async () => {
  const axiosLib = (typeof window !== 'undefined' && window.axios) ? window.axios : null
  if (!axiosLib) return

  try {
    await axiosLib.post('/api/nat/rules', newRule.value)
    isModalOpen.value = false
    await fetchNatRules()
  } catch (err) {
    console.error('Failed to save NAT rule:', err)
  }
}

const toggleRule = async (rule) => {
  rule.enabled = !rule.enabled
  const axiosLib = (typeof window !== 'undefined' && window.axios) ? window.axios : null
  if (!axiosLib) return
  try {
    await axiosLib.post('/api/nat/rules', rule)
  } catch (err) {
    console.error('Failed to toggle NAT rule:', err)
  }
}

const deleteRule = async (id) => {
  const axiosLib = (typeof window !== 'undefined' && window.axios) ? window.axios : null
  if (!axiosLib) return
  try {
    await axiosLib.delete(`/api/nat/rules/${id}`)
    await fetchNatRules()
  } catch (err) {
    console.error('Failed to delete NAT rule:', err)
  }
}

onMounted(() => {
  fetchNatRules()
})
</script>
