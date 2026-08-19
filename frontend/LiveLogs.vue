<template>
  <div class="space-y-6">
    <!-- Header Section -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-slate-200 pb-4">
      <div>
        <div class="flex items-center gap-2">
          <span class="w-1.5 h-5 bg-[#ee7f00] rounded-full"></span>
          <h1 class="text-xl font-bold text-slate-900">Live Logs & Connection State Table</h1>
        </div>
        <p class="text-xs text-slate-500 mt-1">
          Real-time packet filter firewall log stream and active Linux netfilter stateful connection tracking (conntrack).
        </p>
      </div>

      <!-- Controls -->
      <div class="flex items-center gap-2">
        <button
          type="button"
          @click="isStreaming = !isStreaming"
          :class="[
            'inline-flex items-center gap-1.5 px-3 py-1.5 rounded text-xs font-bold shadow-xs transition-colors cursor-pointer',
            isStreaming
              ? 'bg-emerald-600 hover:bg-emerald-700 text-white'
              : 'bg-amber-600 hover:bg-amber-700 text-white'
          ]"
        >
          <span class="w-2 h-2 rounded-full" :class="isStreaming ? 'bg-white animate-pulse' : 'bg-white/60'"></span>
          <span>{{ isStreaming ? 'Live Stream: Active' : 'Stream: Paused' }}</span>
        </button>

        <button
          type="button"
          @click="fetchData"
          class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded bg-white hover:bg-slate-50 text-slate-700 border border-slate-300 text-xs font-bold shadow-xs cursor-pointer"
        >
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          <span>Refresh</span>
        </button>
      </div>
    </div>

    <!-- Tab Navigation Strip -->
    <div class="flex border-b border-slate-200 gap-1 bg-[#f4f6f9] p-1.5 rounded-t-lg">
      <button
        type="button"
        @click="activeTab = 'logs'"
        :class="[
          'px-4 py-2 text-xs font-bold rounded-md transition-all flex items-center gap-2 cursor-pointer',
          activeTab === 'logs'
            ? 'bg-white text-slate-900 shadow-xs border-b-2 border-[#ee7f00]'
            : 'text-slate-600 hover:text-slate-900 hover:bg-white/60'
        ]"
      >
        <svg class="w-4 h-4 text-[#005299]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
        <span>Live Packet Filter Log ({{ logs.length }})</span>
      </button>

      <button
        type="button"
        @click="activeTab = 'conntrack'"
        :class="[
          'px-4 py-2 text-xs font-bold rounded-md transition-all flex items-center gap-2 cursor-pointer',
          activeTab === 'conntrack'
            ? 'bg-white text-slate-900 shadow-xs border-b-2 border-[#ee7f00]'
            : 'text-slate-600 hover:text-slate-900 hover:bg-white/60'
        ]"
      >
        <svg class="w-4 h-4 text-[#005299]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
        </svg>
        <span>Active Connection Table ({{ connections.length }})</span>
      </button>
    </div>

    <!-- Filter Bar -->
    <div class="flex items-center justify-between gap-3">
      <div class="flex items-center gap-3">
        <div class="relative w-72">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Filter by IP, Port, Protocol, Action..."
            class="w-full text-xs px-3 py-1.5 pl-8 rounded border border-slate-300 bg-white focus:outline-none focus:border-[#005299] focus:ring-1 focus:ring-[#005299]"
          />
          <svg class="w-3.5 h-3.5 text-slate-400 absolute left-2.5 top-2.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </div>

        <div v-if="activeTab === 'logs'" class="flex items-center gap-1.5">
          <button
            type="button"
            @click="actionFilter = 'ALL'"
            :class="['px-2.5 py-1 rounded text-[11px] font-bold border cursor-pointer', actionFilter === 'ALL' ? 'bg-[#005299] text-white border-[#005299]' : 'bg-white text-slate-600 border-slate-300']"
          >
            All Actions
          </button>
          <button
            type="button"
            @click="actionFilter = 'DROP'"
            :class="['px-2.5 py-1 rounded text-[11px] font-bold border cursor-pointer', actionFilter === 'DROP' ? 'bg-rose-600 text-white border-rose-600' : 'bg-white text-rose-700 border-rose-200']"
          >
            DROP Only
          </button>
          <button
            type="button"
            @click="actionFilter = 'ACCEPT'"
            :class="['px-2.5 py-1 rounded text-[11px] font-bold border cursor-pointer', actionFilter === 'ACCEPT' ? 'bg-emerald-600 text-white border-emerald-600' : 'bg-white text-emerald-700 border-emerald-200']"
          >
            ACCEPT Only
          </button>
        </div>
      </div>

      <span class="text-xs text-slate-400 font-mono">
        Auto-refresh: 3s
      </span>
    </div>

    <!-- TAB 1: LIVE PACKET FILTER LOG STREAM -->
    <div v-if="activeTab === 'logs'" class="bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full text-left text-xs border-collapse font-mono">
          <thead class="bg-[#1b232e] text-slate-200 font-bold border-b border-slate-700">
            <tr>
              <th class="p-2.5 pl-4 w-20">Time</th>
              <th class="p-2.5 w-20">Action</th>
              <th class="p-2.5">Interface</th>
              <th class="p-2.5">Protocol</th>
              <th class="p-2.5">Source</th>
              <th class="p-2.5">Destination</th>
              <th class="p-2.5">Rule #</th>
              <th class="p-2.5 pr-4 text-right">Length</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100">
            <tr
              v-for="(log, idx) in filteredLogs"
              :key="log.id"
              :class="idx % 2 === 0 ? 'bg-white' : 'bg-[#f7f7f7]'"
              class="hover:bg-blue-50/50 transition-colors"
            >
              <td class="p-2.5 pl-4 text-slate-500 font-semibold">{{ log.timestamp }}</td>
              <td class="p-2.5">
                <span
                  :class="[
                    'px-2 py-0.5 rounded text-[10px] font-bold',
                    log.action === 'DROP'
                      ? 'bg-rose-100 text-rose-800 border border-rose-200'
                      : log.action === 'ACCEPT'
                      ? 'bg-emerald-100 text-emerald-800 border border-emerald-200'
                      : 'bg-amber-100 text-amber-800 border border-amber-200'
                  ]"
                >
                  {{ log.action }}
                </span>
              </td>
              <td class="p-2.5 text-slate-700 font-bold">
                {{ log.in_interface }} <span v-if="log.out_interface !== '-'"> &rarr; {{ log.out_interface }}</span>
              </td>
              <td class="p-2.5 text-slate-900 font-bold">
                {{ log.protocol }} <span v-if="log.tcp_flags" class="text-[10px] text-slate-400">[{{ log.tcp_flags }}]</span>
              </td>
              <td class="p-2.5 text-slate-800">
                {{ log.src_ip }}:<span class="text-slate-500">{{ log.src_port }}</span>
              </td>
              <td class="p-2.5 text-slate-800">
                {{ log.dst_ip }}:<span class="text-[#005299] font-bold">{{ log.dst_port }}</span>
              </td>
              <td class="p-2.5 text-slate-600 font-sans text-[11px] font-semibold">
                {{ log.rule_name }}
              </td>
              <td class="p-2.5 pr-4 text-right text-slate-400">
                {{ log.packet_length }} B
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- TAB 2: ACTIVE CONNECTION STATE TABLE (CONNTRACK) -->
    <div v-if="activeTab === 'conntrack'" class="bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full text-left text-xs border-collapse font-mono">
          <thead class="bg-[#1b232e] text-slate-200 font-bold border-b border-slate-700">
            <tr>
              <th class="p-2.5 pl-4">Protocol</th>
              <th class="p-2.5">State</th>
              <th class="p-2.5">Source Address</th>
              <th class="p-2.5">Destination Address</th>
              <th class="p-2.5">Service</th>
              <th class="p-2.5">Data Transferred</th>
              <th class="p-2.5">TTL</th>
              <th class="p-2.5 pr-4 text-right">Action</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100">
            <tr
              v-for="(conn, idx) in filteredConnections"
              :key="conn.id"
              :class="idx % 2 === 0 ? 'bg-white' : 'bg-[#f7f7f7]'"
              class="hover:bg-blue-50/50 transition-colors"
            >
              <td class="p-2.5 pl-4 text-slate-900 font-bold">{{ conn.protocol }}</td>
              <td class="p-2.5">
                <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-blue-50 text-[#005299] border border-blue-200">
                  {{ conn.state }}
                </span>
              </td>
              <td class="p-2.5 text-slate-800">{{ conn.src_ip }}:<span class="text-slate-500">{{ conn.src_port }}</span></td>
              <td class="p-2.5 text-slate-800">{{ conn.dst_ip }}:<span class="text-[#005299] font-bold">{{ conn.dst_port }}</span></td>
              <td class="p-2.5 text-slate-700 font-sans font-bold">{{ conn.service || conn.dst_port }}</td>
              <td class="p-2.5 text-slate-600">{{ conn.bytes_formatted || conn.bytes + ' B' }}</td>
              <td class="p-2.5 text-slate-400">{{ conn.ttl }}s</td>
              <td class="p-2.5 pr-4 text-right">
                <button
                  type="button"
                  @click="killConn(conn.id)"
                  class="px-2 py-0.5 rounded bg-rose-50 text-rose-700 hover:bg-rose-600 hover:text-white border border-rose-200 text-[10px] font-sans font-bold transition-colors cursor-pointer"
                >
                  Terminate
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  authToken: {
    type: String,
    default: ''
  }
})

const activeTab = ref('logs') // 'logs' | 'conntrack'
const isStreaming = ref(true)
const searchQuery = ref('')
const actionFilter = ref('ALL') // 'ALL' | 'DROP' | 'ACCEPT'

const logs = ref([])
const connections = ref([])
let streamTimer = null

const filteredLogs = computed(() => {
  let list = logs.value
  if (actionFilter.value !== 'ALL') {
    list = list.filter(l => l.action === actionFilter.value)
  }
  const q = searchQuery.value.toLowerCase()
  if (!q) return list
  return list.filter(l =>
    l.src_ip.toLowerCase().includes(q) ||
    l.dst_ip.toLowerCase().includes(q) ||
    String(l.dst_port).includes(q) ||
    l.protocol.toLowerCase().includes(q) ||
    l.rule_name.toLowerCase().includes(q)
  )
})

const filteredConnections = computed(() => {
  const q = searchQuery.value.toLowerCase()
  if (!q) return connections.value
  return connections.value.filter(c =>
    c.src_ip.toLowerCase().includes(q) ||
    c.dst_ip.toLowerCase().includes(q) ||
    String(c.dst_port).includes(q) ||
    c.protocol.toLowerCase().includes(q) ||
    c.state.toLowerCase().includes(q)
  )
})

const fetchData = async () => {
  const axiosLib = (typeof window !== 'undefined' && window.axios) ? window.axios : null
  if (!axiosLib) return

  try {
    const [logsRes, connRes] = await Promise.all([
      axiosLib.get('/api/logs/firewall'),
      axiosLib.get('/api/system/connections')
    ])
    if (logsRes.data && logsRes.data.logs) {
      logs.value = logsRes.data.logs
    }
    if (connRes.data && connRes.data.connections) {
      connections.value = connRes.data.connections
    }
  } catch (err) {
    // Retain previous logs
  }
}

const killConn = async (connId) => {
  const axiosLib = (typeof window !== 'undefined' && window.axios) ? window.axios : null
  if (!axiosLib) return
  try {
    await axiosLib.delete(`/api/system/connections/${connId}`)
    await fetchData()
  } catch (err) {
    console.error('Failed to kill connection:', err)
  }
}

onMounted(() => {
  fetchData()
  streamTimer = setInterval(() => {
    if (isStreaming.value) {
      fetchData()
    }
  }, 3000)
})

onUnmounted(() => {
  if (streamTimer) {
    clearInterval(streamTimer)
  }
})
</script>
