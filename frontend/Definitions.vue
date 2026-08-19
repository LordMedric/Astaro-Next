<template>
  <div class="space-y-6">
    <!-- Header Section -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-slate-200 pb-4">
      <div>
        <div class="flex items-center gap-2">
          <span class="w-1.5 h-5 bg-[#ee7f00] rounded-full"></span>
          <h1 class="text-xl font-bold text-slate-900">Definitions & Objects</h1>
        </div>
        <p class="text-xs text-slate-500 mt-1">
          Manage reusable network hosts, subnets, IP ranges, and TCP/UDP service objects across all firewall, NAT, and routing policies.
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
          <span>New {{ activeTab === 'networks' ? 'Network Definition' : 'Service Definition' }}</span>
        </button>
      </div>
    </div>

    <!-- Tab Navigation Strip (Sophos UTM Style with Orange Active Underline) -->
    <div class="flex border-b border-slate-200 gap-1 bg-[#f4f6f9] p-1.5 rounded-t-lg">
      <button
        type="button"
        @click="activeTab = 'networks'"
        :class="[
          'px-4 py-2 text-xs font-bold rounded-md transition-all flex items-center gap-2 cursor-pointer',
          activeTab === 'networks'
            ? 'bg-white text-slate-900 shadow-xs border-b-2 border-[#ee7f00]'
            : 'text-slate-600 hover:text-slate-900 hover:bg-white/60'
        ]"
      >
        <svg class="w-4 h-4 text-[#005299]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
        </svg>
        <span>Network Definitions ({{ networkObjects.length }})</span>
      </button>

      <button
        type="button"
        @click="activeTab = 'services'"
        :class="[
          'px-4 py-2 text-xs font-bold rounded-md transition-all flex items-center gap-2 cursor-pointer',
          activeTab === 'services'
            ? 'bg-white text-slate-900 shadow-xs border-b-2 border-[#ee7f00]'
            : 'text-slate-600 hover:text-slate-900 hover:bg-white/60'
        ]"
      >
        <svg class="w-4 h-4 text-[#005299]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
        </svg>
        <span>Service Definitions ({{ serviceObjects.length }})</span>
      </button>
    </div>

    <!-- Search & Filter Bar -->
    <div class="flex items-center justify-between gap-3">
      <div class="relative w-72">
        <input
          v-model="searchQuery"
          type="text"
          :placeholder="activeTab === 'networks' ? 'Search network objects, IPs...' : 'Search services, ports...'"
          class="w-full text-xs px-3 py-1.5 pl-8 rounded border border-slate-300 bg-white focus:outline-none focus:border-[#005299] focus:ring-1 focus:ring-[#005299]"
        />
        <svg class="w-3.5 h-3.5 text-slate-400 absolute left-2.5 top-2.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
      </div>
      <span class="text-xs text-slate-400 font-mono">
        Showing {{ filteredItems.length }} objects
      </span>
    </div>

    <!-- TAB 1: NETWORK DEFINITIONS TABLE -->
    <div v-if="activeTab === 'networks'" class="bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden">
      <table class="w-full text-left text-xs border-collapse">
        <thead class="bg-[#f4f6f9] text-slate-700 font-bold border-b border-slate-200">
          <tr>
            <th class="p-3 pl-4">Name</th>
            <th class="p-3">Type</th>
            <th class="p-3 font-mono">IPv4 Address / Subnet</th>
            <th class="p-3">Interface Binding</th>
            <th class="p-3">Comment</th>
            <th class="p-3 text-right pr-4">Actions</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-100">
          <tr
            v-for="(net, idx) in filteredNetworkObjects"
            :key="net.id"
            :class="idx % 2 === 0 ? 'bg-white' : 'bg-[#f7f7f7]'"
            class="hover:bg-blue-50/50 transition-colors"
          >
            <td class="p-3 pl-4 font-bold text-slate-900 flex items-center gap-2">
              <span class="w-2 h-2 rounded-full bg-[#005299]"></span>
              {{ net.name }}
            </td>
            <td class="p-3">
              <span class="px-2 py-0.5 rounded text-[10px] font-bold uppercase bg-blue-50 text-[#005299] border border-blue-200">
                {{ net.type }}
              </span>
            </td>
            <td class="p-3 font-mono text-slate-800 font-semibold">
              {{ net.address }}
            </td>
            <td class="p-3 text-slate-600">
              <span class="px-2 py-0.5 rounded text-[10px] font-semibold bg-slate-100 text-slate-700">
                {{ net.interface || 'Any' }}
              </span>
            </td>
            <td class="p-3 text-slate-500 text-[11px] truncate max-w-xs">
              {{ net.comment || '—' }}
            </td>
            <td class="p-3 text-right pr-4">
              <button
                type="button"
                @click="deleteNetworkObject(net.id)"
                class="text-rose-600 hover:text-rose-800 text-[11px] font-bold cursor-pointer"
              >
                Delete
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- TAB 2: SERVICE DEFINITIONS TABLE -->
    <div v-if="activeTab === 'services'" class="bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden">
      <table class="w-full text-left text-xs border-collapse">
        <thead class="bg-[#f4f6f9] text-slate-700 font-bold border-b border-slate-200">
          <tr>
            <th class="p-3 pl-4">Service Name</th>
            <th class="p-3">Protocol</th>
            <th class="p-3 font-mono">Destination Port</th>
            <th class="p-3 font-mono">Source Port</th>
            <th class="p-3">Comment</th>
            <th class="p-3 text-right pr-4">Actions</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-100">
          <tr
            v-for="(srv, idx) in filteredServiceObjects"
            :key="srv.id"
            :class="idx % 2 === 0 ? 'bg-white' : 'bg-[#f7f7f7]'"
            class="hover:bg-blue-50/50 transition-colors"
          >
            <td class="p-3 pl-4 font-bold text-slate-900 flex items-center gap-2">
              <span class="w-2 h-2 rounded-full bg-[#ee7f00]"></span>
              {{ srv.name }}
            </td>
            <td class="p-3">
              <span class="px-2 py-0.5 rounded text-[10px] font-bold uppercase bg-amber-50 text-amber-800 border border-amber-200">
                {{ srv.protocol }}
              </span>
            </td>
            <td class="p-3 font-mono text-slate-900 font-bold">
              {{ srv.dst_port }}
            </td>
            <td class="p-3 font-mono text-slate-500">
              {{ srv.src_port || '1:65535' }}
            </td>
            <td class="p-3 text-slate-500 text-[11px] truncate max-w-xs">
              {{ srv.comment || '—' }}
            </td>
            <td class="p-3 text-right pr-4">
              <button
                type="button"
                @click="deleteServiceObject(srv.id)"
                class="text-rose-600 hover:text-rose-800 text-[11px] font-bold cursor-pointer"
              >
                Delete
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- CREATE MODAL DIALOG -->
    <div
      v-if="isModalOpen"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-xs p-4"
    >
      <div class="bg-white rounded-xl shadow-2xl border border-slate-300 max-w-lg w-full overflow-hidden">
        <!-- Modal Header -->
        <div class="px-5 py-3.5 bg-[#1b232e] text-white flex items-center justify-between border-b-2 border-[#ee7f00]">
          <h3 class="text-sm font-bold uppercase tracking-wider">
            Create {{ activeTab === 'networks' ? 'Network Definition' : 'Service Definition' }}
          </h3>
          <button @click="isModalOpen = false" class="text-slate-400 hover:text-white font-bold cursor-pointer">✕</button>
        </div>

        <!-- Network Modal Form -->
        <div v-if="activeTab === 'networks'" class="p-5 space-y-4 text-xs">
          <div>
            <label class="block font-bold text-slate-700 mb-1">Definition Name</label>
            <input
              v-model="newNet.name"
              type="text"
              placeholder="e.g. Finance Subnet, MailServer Host"
              class="w-full p-2 border border-slate-300 rounded focus:border-[#005299] focus:outline-none"
            />
          </div>

          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block font-bold text-slate-700 mb-1">Type</label>
              <select
                v-model="newNet.type"
                class="w-full p-2 border border-slate-300 rounded focus:border-[#005299] focus:outline-none bg-white"
              >
                <option value="Host">Host (Single IP)</option>
                <option value="Network">Network (Subnet CIDR)</option>
                <option value="Range">IP Range</option>
                <option value="DNS Host">DNS Host (FQDN)</option>
                <option value="Network Group">Network Group</option>
              </select>
            </div>
            <div>
              <label class="block font-bold text-slate-700 mb-1">Interface Binding</label>
              <select
                v-model="newNet.interface"
                class="w-full p-2 border border-slate-300 rounded focus:border-[#005299] focus:outline-none bg-white"
              >
                <option value="Any">&lt;&lt; Any &gt;&gt;</option>
                <option value="LAN">Internal (LAN)</option>
                <option value="WAN">External (WAN)</option>
                <option value="DMZ">DMZ</option>
              </select>
            </div>
          </div>

          <div>
            <label class="block font-bold text-slate-700 mb-1">IPv4 Address / Netmask / FQDN</label>
            <input
              v-model="newNet.address"
              type="text"
              placeholder="e.g. 192.168.1.100 or 10.0.0.0/24"
              class="w-full p-2 border border-slate-300 rounded font-mono focus:border-[#005299] focus:outline-none"
            />
          </div>

          <div>
            <label class="block font-bold text-slate-700 mb-1">Comment</label>
            <input
              v-model="newNet.comment"
              type="text"
              placeholder="Optional notes or documentation"
              class="w-full p-2 border border-slate-300 rounded focus:border-[#005299] focus:outline-none"
            />
          </div>
        </div>

        <!-- Service Modal Form -->
        <div v-else class="p-5 space-y-4 text-xs">
          <div>
            <label class="block font-bold text-slate-700 mb-1">Service Name</label>
            <input
              v-model="newSrv.name"
              type="text"
              placeholder="e.g. HTTPS Alternative, Custom DB Port"
              class="w-full p-2 border border-slate-300 rounded focus:border-[#005299] focus:outline-none"
            />
          </div>

          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block font-bold text-slate-700 mb-1">Protocol</label>
              <select
                v-model="newSrv.protocol"
                class="w-full p-2 border border-slate-300 rounded focus:border-[#005299] focus:outline-none bg-white"
              >
                <option value="TCP">TCP</option>
                <option value="UDP">UDP</option>
                <option value="TCP/UDP">TCP/UDP</option>
                <option value="ICMP">ICMP</option>
                <option value="IP">IP Protocol</option>
              </select>
            </div>
            <div>
              <label class="block font-bold text-slate-700 mb-1">Destination Port(s)</label>
              <input
                v-model="newSrv.dst_port"
                type="text"
                placeholder="e.g. 8443 or 8000:8080"
                class="w-full p-2 border border-slate-300 rounded font-mono focus:border-[#005299] focus:outline-none"
              />
            </div>
          </div>

          <div>
            <label class="block font-bold text-slate-700 mb-1">Source Port Range</label>
            <input
              v-model="newSrv.src_port"
              type="text"
              placeholder="Default: 1:65535"
              class="w-full p-2 border border-slate-300 rounded font-mono focus:border-[#005299] focus:outline-none"
            />
          </div>

          <div>
            <label class="block font-bold text-slate-700 mb-1">Comment</label>
            <input
              v-model="newSrv.comment"
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
            @click="saveDefinition"
            class="px-4 py-1.5 rounded bg-[#005299] hover:bg-[#003d73] text-white text-xs font-bold shadow-xs cursor-pointer"
          >
            Save Definition
          </button>
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

const activeTab = ref('networks') // 'networks' | 'services'
const searchQuery = ref('')
const isModalOpen = ref(false)

const networkObjects = ref([])
const serviceObjects = ref([])

const newNet = ref({
  name: '',
  type: 'Host',
  address: '',
  interface: 'Any',
  comment: ''
})

const newSrv = ref({
  name: '',
  protocol: 'TCP',
  dst_port: '',
  src_port: '1:65535',
  comment: ''
})

const filteredNetworkObjects = computed(() => {
  const q = searchQuery.value.toLowerCase()
  if (!q) return networkObjects.value
  return networkObjects.value.filter(n =>
    n.name.toLowerCase().includes(q) ||
    n.address.toLowerCase().includes(q) ||
    (n.comment && n.comment.toLowerCase().includes(q))
  )
})

const filteredServiceObjects = computed(() => {
  const q = searchQuery.value.toLowerCase()
  if (!q) return serviceObjects.value
  return serviceObjects.value.filter(s =>
    s.name.toLowerCase().includes(q) ||
    s.dst_port.toLowerCase().includes(q) ||
    s.protocol.toLowerCase().includes(q)
  )
})

const filteredItems = computed(() => {
  return activeTab.value === 'networks' ? filteredNetworkObjects.value : filteredServiceObjects.value
})

const fetchDefinitions = async () => {
  try {
    const axiosLib = (typeof window !== 'undefined' && window.axios) ? window.axios : null
    if (!axiosLib) return

    const [netRes, srvRes] = await Promise.all([
      axiosLib.get('/api/definitions/networks'),
      axiosLib.get('/api/definitions/services')
    ])
    if (netRes.data) networkObjects.value = netRes.data
    if (srvRes.data) serviceObjects.value = srvRes.data
  } catch (err) {
    console.error('Failed to fetch definitions:', err)
  }
}

const openCreateModal = () => {
  if (activeTab.value === 'networks') {
    newNet.value = { name: '', type: 'Host', address: '', interface: 'Any', comment: '' }
  } else {
    newSrv.value = { name: '', protocol: 'TCP', dst_port: '', src_port: '1:65535', comment: '' }
  }
  isModalOpen.value = true
}

const saveDefinition = async () => {
  const axiosLib = (typeof window !== 'undefined' && window.axios) ? window.axios : null
  if (!axiosLib) return

  try {
    if (activeTab.value === 'networks') {
      if (!newNet.value.name || !newNet.value.address) return
      await axiosLib.post('/api/definitions/networks', newNet.value)
    } else {
      if (!newSrv.value.name || !newSrv.value.dst_port) return
      await axiosLib.post('/api/definitions/services', newSrv.value)
    }
    isModalOpen.value = false
    await fetchDefinitions()
  } catch (err) {
    console.error('Failed to save definition:', err)
  }
}

const deleteNetworkObject = async (id) => {
  const axiosLib = (typeof window !== 'undefined' && window.axios) ? window.axios : null
  if (!axiosLib) return
  try {
    await axiosLib.delete(`/api/definitions/networks/${id}`)
    await fetchDefinitions()
  } catch (err) {
    console.error('Failed to delete network object:', err)
  }
}

const deleteServiceObject = async (id) => {
  const axiosLib = (typeof window !== 'undefined' && window.axios) ? window.axios : null
  if (!axiosLib) return
  try {
    await axiosLib.delete(`/api/definitions/services/${id}`)
    await fetchDefinitions()
  } catch (err) {
    console.error('Failed to delete service object:', err)
  }
}

onMounted(() => {
  fetchDefinitions()
})
</script>
