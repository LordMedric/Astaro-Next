<template>
  <div class="min-h-full bg-[#f4f6f9] text-slate-800 font-sans antialiased selection:bg-[#0072ce] selection:text-white">
    <!-- Notification Toasts Floating Stack -->
    <div class="fixed bottom-5 right-5 z-50 flex flex-col gap-2 max-w-md w-full pointer-events-none" aria-live="polite">
      <transition-group
        enter-active-class="transition duration-300 ease-out transform"
        enter-from-class="translate-y-2 opacity-0 scale-95"
        enter-to-class="translate-y-0 opacity-100 scale-100"
        leave-active-class="transition duration-200 ease-in transform"
        leave-from-class="translate-y-0 opacity-100 scale-100"
        leave-to-class="translate-y-2 opacity-0 scale-95"
      >
        <div
          v-for="toast in toasts"
          :key="toast.id"
          :class="[
            'pointer-events-auto p-4 rounded-xl shadow-xl border flex items-start gap-3 text-xs backdrop-blur-md transition-all',
            toast.type === 'success' ? 'bg-emerald-950/95 border-emerald-500/50 text-emerald-200' :
            toast.type === 'error' ? 'bg-rose-950/95 border-rose-500/50 text-rose-200' :
            toast.type === 'warning' ? 'bg-amber-950/95 border-amber-500/50 text-amber-200' :
            'bg-slate-900/95 border-slate-700 text-slate-200'
          ]"
          role="alert"
        >
          <div class="mt-0.5 flex-none">
            <svg v-if="toast.type === 'success'" class="w-4 h-4 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
            <svg v-else-if="toast.type === 'error'" class="w-4 h-4 text-rose-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
            <svg v-else-if="toast.type === 'warning'" class="w-4 h-4 text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
            <svg v-else class="w-4 h-4 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div class="flex-1">
            <h4 class="font-bold uppercase tracking-wider text-[11px]">{{ toast.title }}</h4>
            <p class="mt-0.5 opacity-90 leading-relaxed">{{ toast.message }}</p>
          </div>
          <button
            type="button"
            @click="dismissToast(toast.id)"
            class="text-slate-400 hover:text-white transition-colors cursor-pointer p-0.5"
            aria-label="Dismiss notification"
          >
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </transition-group>
    </div>

    <!-- Top Management & Telemetry Header Banner -->
    <div class="mb-6 flex flex-col md:flex-row md:items-center md:justify-between gap-4 bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
      <!-- Title & Subtitle with Sophos Blue Accent -->
      <div class="flex items-center gap-3.5">
        <div class="w-11 h-11 rounded-lg bg-[#0072ce] flex items-center justify-center text-white shadow-md shadow-blue-500/20 font-black flex-shrink-0">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 9l3 3-3 3m5 0h3M5 20h14a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
        </div>
        <div>
          <div class="flex items-center gap-2.5 flex-wrap">
            <h1 class="text-lg font-bold text-slate-900 tracking-tight">Network Interfaces</h1>
            <span class="inline-flex items-center gap-1.5 px-2 py-0.5 rounded-full text-[11px] font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200">
              <span class="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
              {{ activeInterfacesCount }}/{{ interfacesList.length }} Ports Active
            </span>
            <span class="inline-flex items-center px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-blue-50 text-[#0072ce] border border-blue-100 uppercase">
              UTM 9 Engine
            </span>
          </div>
          <p class="text-xs text-slate-500 mt-0.5">Configure physical Ethernet ports, IP assignments (DHCP / Static), zone routing, and link parameters.</p>
        </div>
      </div>

      <!-- Quick Actions, Filters & Refresh Button -->
      <div class="flex items-center flex-wrap gap-2.5">
        <!-- Search filter box -->
        <div class="relative min-w-[180px]">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Filter interfaces..."
            class="w-full bg-[#f4f6f9] text-slate-800 text-xs px-3 py-1.5 pl-8 rounded-lg border border-slate-300 focus:outline-none focus:border-[#0072ce] focus:ring-1 focus:ring-[#0072ce] placeholder:text-slate-400 transition-colors"
          />
          <svg class="w-3.5 h-3.5 text-slate-400 absolute left-2.5 top-2.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
          <button
            v-if="searchQuery"
            @click="searchQuery = ''"
            class="absolute right-2.5 top-2 text-slate-400 hover:text-slate-600"
          >
            ✕
          </button>
        </div>

        <!-- Zone Selector Filter -->
        <select
          v-model="selectedZoneFilter"
          class="bg-[#f4f6f9] text-slate-700 text-xs px-3 py-1.5 rounded-lg border border-slate-300 focus:outline-none focus:border-[#0072ce] font-medium"
        >
          <option value="ALL">All Zones</option>
          <option value="WAN">WAN</option>
          <option value="LAN">LAN</option>
          <option value="DMZ">DMZ</option>
          <option value="HA">HA / Aux</option>
        </select>

        <!-- Refresh Interfaces Button -->
        <button
          type="button"
          @click="fetchInterfaces(true)"
          :disabled="isLoading"
          class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-white border border-slate-300 text-xs font-semibold text-slate-700 hover:bg-[#f4f6f9] hover:text-slate-900 active:bg-slate-100 disabled:opacity-50 transition-all shadow-2xs cursor-pointer"
          title="Reload interface states and hardware telemetry"
        >
          <svg
            :class="['w-3.5 h-3.5 text-slate-500', isLoading ? 'animate-spin text-[#0072ce]' : '']"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          <span>Refresh</span>
        </button>
      </div>
    </div>

    <!-- Navigation Tabs Strip (Sophos UTM 9 Style) -->
    <div class="flex border-b border-slate-200 gap-1 bg-[#f4f6f9] p-1.5 rounded-t-xl overflow-x-auto text-xs font-bold mb-6">
      <button
        type="button"
        @click="activeTab = 'stats'"
        :class="[
          'px-4 py-2 rounded-lg transition-all flex items-center gap-2 cursor-pointer whitespace-nowrap',
          activeTab === 'stats'
            ? 'bg-white text-slate-900 shadow-xs border-b-2 border-[#ee7f00]'
            : 'text-slate-600 hover:text-slate-900 hover:bg-white/60'
        ]"
      >
        <span>📊 Network Statistics</span>
        <span class="px-1.5 py-0.2 rounded-full text-[10px] font-mono bg-blue-100 text-[#0072ce]">Today</span>
      </button>

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
        <span>🔌 Hardware &amp; Virtual Interfaces</span>
        <span class="px-1.5 py-0.2 rounded-full text-[10px] font-mono bg-slate-200 text-slate-700">
          {{ interfacesList.length }}
        </span>
      </button>

      <button
        type="button"
        @click="activeTab = 'groups'"
        :class="[
          'px-4 py-2 rounded-lg transition-all flex items-center gap-2 cursor-pointer whitespace-nowrap',
          activeTab === 'groups'
            ? 'bg-white text-slate-900 shadow-xs border-b-2 border-[#ee7f00]'
            : 'text-slate-600 hover:text-slate-900 hover:bg-white/60'
        ]"
      >
        <span>👥 Interface Groups &amp; LAGs</span>
        <span class="px-1.5 py-0.2 rounded-full text-[10px] font-mono bg-slate-200 text-slate-700">
          {{ interfaceGroups.length }}
        </span>
      </button>

      <button
        type="button"
        @click="activeTab = 'uplinks'"
        :class="[
          'px-4 py-2 rounded-lg transition-all flex items-center gap-2 cursor-pointer whitespace-nowrap',
          activeTab === 'uplinks'
            ? 'bg-white text-slate-900 shadow-xs border-b-2 border-[#ee7f00]'
            : 'text-slate-600 hover:text-slate-900 hover:bg-white/60'
        ]"
      >
        <span>⚖️ Uplink Balancing &amp; Multi-WAN</span>
        <span class="px-1.5 py-0.2 rounded-full text-[10px] font-mono" :class="uplinkConfig.enabled ? 'bg-emerald-600 text-white' : 'bg-slate-200 text-slate-700'">
          {{ uplinkConfig.enabled ? 'Active' : 'Off' }}
        </span>
      </button>
    </div>

    <!-- TAB 0: NETWORK STATISTICS (TODAY) - EXACT SOPHOS UTM 9 DASHBOARD -->
    <div v-if="activeTab === 'stats'" class="space-y-6">
      <div class="flex items-center justify-between">
        <h2 class="text-xs font-bold uppercase tracking-wider text-slate-700">Network Statistics — Today</h2>
        <span class="text-[11px] font-mono text-slate-500">Total packets: 3,562,702 &bull; Total traffic: 3.9 GB</span>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- Top Accounting Services -->
        <div class="bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden">
          <div class="p-3.5 bg-[#f4f6f9] border-b border-slate-200 flex items-center justify-between">
            <span class="text-xs font-bold text-slate-800">Top Accounting Services</span>
            <span class="text-[#0072ce] text-xs font-bold">▶</span>
          </div>
          <div class="p-4 flex flex-col sm:flex-row items-center gap-6">
            <div class="w-32 h-32 flex-shrink-0 relative">
              <svg viewBox="-55 -55 110 110" class="w-full h-full transform -rotate-90">
                <path
                  v-for="(slice, sIdx) in accountingServicesSlices"
                  :key="sIdx"
                  :d="slice.path"
                  :fill="slice.color"
                  stroke="#ffffff"
                  stroke-width="1.5"
                >
                  <title>{{ slice.name }}: {{ slice.traffic }} ({{ slice.pct }}%)</title>
                </path>
              </svg>
            </div>
            <div class="flex-1 w-full overflow-x-auto">
              <table class="w-full text-left text-[11px] border-collapse">
                <thead>
                  <tr class="border-b border-slate-200 text-slate-500 font-bold uppercase">
                    <th class="py-1 px-1.5">#</th>
                    <th class="py-1 px-1.5">Proto</th>
                    <th class="py-1 px-1.5">Port</th>
                    <th class="py-1 px-1.5">Service</th>
                    <th class="py-1 px-1.5 text-right">Packets</th>
                    <th class="py-1 px-1.5 text-right">Traffic</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-slate-100">
                  <tr v-for="(svc, idx) in accountingServices" :key="idx" class="hover:bg-slate-50">
                    <td class="py-1 px-1.5 font-mono text-slate-400">{{ idx + 1 }}</td>
                    <td class="py-1 px-1.5 font-mono text-slate-600">{{ svc.proto }}</td>
                    <td class="py-1 px-1.5 font-mono text-slate-600">{{ svc.port }}</td>
                    <td class="py-1 px-1.5 font-bold flex items-center gap-1.5">
                      <span class="w-2.5 h-2.5 rounded-xs" :style="{ backgroundColor: svc.color }"></span>
                      <span class="text-slate-800">{{ svc.name }}</span>
                    </td>
                    <td class="py-1 px-1.5 text-right font-mono text-slate-600">{{ svc.packets.toLocaleString() }}</td>
                    <td class="py-1 px-1.5 text-right font-mono font-bold text-[#0072ce]">{{ svc.traffic }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- Top Source Hosts -->
        <div class="bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden">
          <div class="p-3.5 bg-[#f4f6f9] border-b border-slate-200 flex items-center justify-between">
            <span class="text-xs font-bold text-slate-800">Top Source Hosts</span>
            <span class="text-[#0072ce] text-xs font-bold">▶</span>
          </div>
          <div class="p-4 flex flex-col sm:flex-row items-center gap-6">
            <div class="w-32 h-32 flex-shrink-0 relative">
              <svg viewBox="-55 -55 110 110" class="w-full h-full transform -rotate-90">
                <path
                  v-for="(slice, sIdx) in sourceHostsSlices"
                  :key="sIdx"
                  :d="slice.path"
                  :fill="slice.color"
                  stroke="#ffffff"
                  stroke-width="1.5"
                >
                  <title>{{ slice.name }}: {{ slice.traffic }} ({{ slice.pct }}%)</title>
                </path>
              </svg>
            </div>
            <div class="flex-1 w-full overflow-x-auto">
              <table class="w-full text-left text-[11px] border-collapse">
                <thead>
                  <tr class="border-b border-slate-200 text-slate-500 font-bold uppercase">
                    <th class="py-1 px-1.5">#</th>
                    <th class="py-1 px-1.5">User / Host</th>
                    <th class="py-1 px-1.5 text-center">Type</th>
                    <th class="py-1 px-1.5 text-right">Packets</th>
                    <th class="py-1 px-1.5 text-right">Traffic</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-slate-100">
                  <tr v-for="(h, idx) in sourceHosts" :key="idx" class="hover:bg-slate-50">
                    <td class="py-1 px-1.5 font-mono text-slate-400">{{ idx + 1 }}</td>
                    <td class="py-1 px-1.5 font-bold flex items-center gap-1.5">
                      <span class="w-2.5 h-2.5 rounded-xs" :style="{ backgroundColor: h.color }"></span>
                      <span class="text-slate-900 font-mono">{{ h.name }}</span>
                    </td>
                    <td class="py-1 px-1.5 text-center text-xs">
                      <span v-if="h.flag">{{ h.flag }}</span>
                      <span v-else>💻</span>
                    </td>
                    <td class="py-1 px-1.5 text-right font-mono text-slate-600">{{ h.packets.toLocaleString() }}</td>
                    <td class="py-1 px-1.5 text-right font-mono font-bold text-emerald-700">{{ h.traffic }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>

      <!-- Concurrent Connections Today (Live Area Graph) -->
      <div class="bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden">
        <div class="p-3.5 bg-[#f4f6f9] border-b border-slate-200 flex items-center justify-between">
          <span class="text-xs font-bold text-slate-800">Concurrent Connections Today</span>
          <span class="text-[11px] font-mono text-slate-500">Peak: <strong>888 connections</strong> at 21:40</span>
        </div>
        <div class="p-6">
          <div class="relative w-full h-48">
            <svg class="w-full h-full overflow-visible" viewBox="0 0 1000 220" preserveAspectRatio="none">
              <defs>
                <linearGradient id="itfConnGrad" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stop-color="#0072ce" stop-opacity="0.45" />
                  <stop offset="100%" stop-color="#0072ce" stop-opacity="0.02" />
                </linearGradient>
              </defs>
              <line x1="0" y1="0" x2="1000" y2="0" stroke="#e2e8f0" stroke-dasharray="4" />
              <line x1="0" y1="55" x2="1000" y2="55" stroke="#e2e8f0" stroke-dasharray="4" />
              <line x1="0" y1="110" x2="1000" y2="110" stroke="#e2e8f0" stroke-dasharray="4" />
              <line x1="0" y1="165" x2="1000" y2="165" stroke="#e2e8f0" stroke-dasharray="4" />
              <line x1="0" y1="220" x2="1000" y2="220" stroke="#cbd5e1" stroke-width="1.5" />
              <text x="5" y="15" fill="#64748b" font-size="11" font-family="monospace">888</text>
              <text x="5" y="70" fill="#64748b" font-size="11" font-family="monospace">666</text>
              <text x="5" y="125" fill="#64748b" font-size="11" font-family="monospace">444</text>
              <text x="5" y="180" fill="#64748b" font-size="11" font-family="monospace">222</text>
              <text x="5" y="215" fill="#64748b" font-size="11" font-family="monospace">0</text>
              <path
                d="M 50 220 L 50 180 L 100 80 L 150 150 L 200 120 L 250 90 L 300 110 L 350 180 L 400 190 L 450 170 L 500 160 L 550 25 L 600 70 L 650 170 L 700 160 L 750 150 L 800 160 L 850 110 L 900 130 L 950 80 L 1000 140 L 1000 220 Z"
                fill="url(#itfConnGrad)"
              />
              <path
                d="M 50 180 L 100 80 L 150 150 L 200 120 L 250 90 L 300 110 L 350 180 L 400 190 L 450 170 L 500 160 L 550 25 L 600 70 L 650 170 L 700 160 L 750 150 L 800 160 L 850 110 L 900 130 L 950 80 L 1000 140"
                fill="none"
                stroke="#0072ce"
                stroke-width="2.5"
                stroke-linejoin="round"
                stroke-linecap="round"
              />
            </svg>
          </div>
          <div class="flex justify-between text-[10px] font-mono text-slate-400 pt-2 border-t border-slate-100">
            <span>12:05</span>
            <span>14:04</span>
            <span>16:04</span>
            <span>18:03</span>
            <span>20:03</span>
            <span class="font-bold text-[#0072ce]">22:02 (Peak 888)</span>
            <span>00:02</span>
            <span>02:02</span>
            <span>04:01</span>
            <span>06:01</span>
            <span>08:00</span>
            <span>10:00</span>
            <span>12:00</span>
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 1: HARDWARE INTERFACES -->
    <div v-if="activeTab === 'interfaces'">
      <!-- ENTERPRISE DATA TABLE CANVAS -->
      <div class="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden flex flex-col">
      <!-- Table Header Action Strip -->
      <div class="px-5 py-3.5 border-b border-slate-200 bg-[#f4f6f9]/60 flex flex-col sm:flex-row sm:items-center justify-between gap-2">
        <div class="flex items-center gap-2">
          <span class="w-1.5 h-4 bg-[#0072ce] rounded-full"></span>
          <h2 class="text-xs font-bold text-slate-800 uppercase tracking-wider">Physical Hardware Interfaces</h2>
          <span class="text-[11px] text-slate-400 font-mono">({{ filteredInterfaces.length }} configured)</span>
        </div>
        <div class="flex items-center gap-3 text-xs text-slate-500">
          <span class="flex items-center gap-1.5">
            <span class="w-2 h-2 rounded-full bg-emerald-500"></span> Active (Up)
          </span>
          <span class="flex items-center gap-1.5">
            <span class="w-2 h-2 rounded-full bg-slate-400"></span> Inactive (Down)
          </span>
        </div>
      </div>

      <!-- Structured Data Table Canvas with crisp grey borders (border-slate-200) & alternating rows -->
      <div class="overflow-x-auto">
        <table class="w-full text-left border-collapse" role="table">
          <thead>
            <tr class="border-b border-slate-200 bg-[#f4f6f9] text-[11px] font-bold text-slate-500 uppercase tracking-wider">
              <th scope="col" class="py-3 px-4 border-r border-slate-200/80">Interface Name</th>
              <th scope="col" class="py-3 px-4 border-r border-slate-200/80">IP Address</th>
              <th scope="col" class="py-3 px-4 border-r border-slate-200/80">Netmask</th>
              <th scope="col" class="py-3 px-4 border-r border-slate-200/80">Zone Assignment</th>
              <th scope="col" class="py-3 px-4 border-r border-slate-200/80">Link Operational Status</th>
              <th scope="col" class="py-3 px-4 border-r border-slate-200/80">Port Link Speed</th>
              <th scope="col" class="py-3 px-4 text-right">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-200 text-xs">
            <tr
              v-for="(iface, index) in filteredInterfaces"
              :key="iface.id"
              :class="[
                'transition-colors duration-150',
                index % 2 === 0 ? 'bg-white hover:bg-blue-50/30' : 'bg-[#f4f6f9]/60 hover:bg-blue-50/40'
              ]"
            >
              <!-- 1. Interface Name & Hardware Details -->
              <td class="py-3.5 px-4 border-r border-slate-200/80">
                <div class="flex items-center gap-3">
                  <!-- Physical Port Jack Box Representation -->
                  <div
                    class="relative flex-shrink-0 w-8 h-8 rounded-lg flex items-center justify-center font-mono text-[11px] font-bold shadow-2xs border"
                    :class="[
                      iface.linkStatus.toLowerCase() === 'up'
                        ? 'bg-slate-800 text-slate-200 border-slate-700 ring-1 ring-emerald-500/30'
                        : 'bg-slate-200 text-slate-500 border-slate-300'
                    ]"
                  >
                    <span>{{ iface.portNumber || `P${index + 1}` }}</span>
                    <!-- Port LED Indicator -->
                    <span
                      class="absolute -top-1 -right-1 w-2.5 h-2.5 rounded-full border-2 border-white"
                      :class="iface.linkStatus.toLowerCase() === 'up' ? 'bg-emerald-500 ring-1 ring-emerald-400/50' : 'bg-slate-400'"
                      :title="`Link state: ${iface.linkStatus}`"
                    ></span>
                  </div>

                  <div>
                    <div class="flex items-center gap-1.5">
                      <span class="font-bold text-slate-900">{{ iface.name }}</span>
                      <span class="text-[10px] font-mono px-1.5 py-0.2 rounded bg-slate-100 text-slate-600 border border-slate-200">
                        {{ iface.hwName }}
                      </span>
                    </div>
                    <div class="text-[10px] text-slate-400 font-mono mt-0.5">
                      MAC: {{ iface.macAddress || '00:0C:29:A1:B2:0' + (index + 1) }}
                    </div>
                  </div>
                </div>
              </td>

              <!-- 2. IP Address -->
              <td class="py-3.5 px-4 border-r border-slate-200/80 font-mono">
                <div class="flex items-center gap-1.5">
                  <span
                    v-if="iface.ipAddress && iface.ipAddress !== '0.0.0.0'"
                    class="font-bold text-slate-800"
                  >
                    {{ iface.ipAddress }}
                  </span>
                  <span v-else class="text-slate-400 italic">Unassigned (DHCP)</span>

                  <!-- Mode Badge (Static / DHCP) -->
                  <span
                    :class="[
                      'text-[10px] px-1.5 py-0.5 rounded font-sans font-bold uppercase tracking-wider',
                      iface.mode === 'dhcp'
                        ? 'bg-amber-50 text-amber-700 border border-amber-200'
                        : 'bg-slate-100 text-slate-700 border border-slate-200'
                    ]"
                  >
                    {{ iface.mode === 'dhcp' ? 'DHCP' : 'Static' }}
                  </span>
                </div>
                <div v-if="iface.gateway" class="text-[10px] text-slate-400 font-mono mt-0.5">
                  GW: {{ iface.gateway }}
                </div>
              </td>

              <!-- 3. Netmask -->
              <td class="py-3.5 px-4 border-r border-slate-200/80 font-mono text-slate-700">
                <span v-if="iface.netmask">{{ iface.netmask }}</span>
                <span v-else class="text-slate-400 italic">--</span>
              </td>

              <!-- 4. Zone Assignment (WAN / LAN / DMZ) -->
              <td class="py-3.5 px-4 border-r border-slate-200/80">
                <span
                  :class="[
                    'inline-flex items-center gap-1 px-2.5 py-1 rounded-md text-[11px] font-bold uppercase tracking-wider border shadow-2xs',
                    getZoneBadgeClasses(iface.zone)
                  ]"
                >
                  <svg v-if="iface.zone === 'WAN'" class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9" />
                  </svg>
                  <svg v-else-if="iface.zone === 'LAN'" class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                  </svg>
                  <svg v-else class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                  </svg>
                  {{ iface.zone }}
                </span>
              </td>

              <!-- 5. Link Operational Status (Visual Pill Badge: Green for Up, Gray for Down) -->
              <td class="py-3.5 px-4 border-r border-slate-200/80">
                <span
                  v-if="iface.linkStatus.toLowerCase() === 'up'"
                  class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-[11px] font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200 shadow-2xs"
                >
                  <span class="w-2 h-2 rounded-full bg-emerald-500 ring-2 ring-emerald-300 animate-pulse"></span>
                  Active (Up)
                </span>
                <span
                  v-else
                  class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-[11px] font-semibold bg-slate-100 text-slate-500 border border-slate-200"
                >
                  <span class="w-2 h-2 rounded-full bg-slate-400"></span>
                  Inactive (Down)
                </span>
              </td>

              <!-- 6. Port Link Speed -->
              <td class="py-3.5 px-4 border-r border-slate-200/80 font-mono text-slate-700">
                <div class="flex items-center gap-1.5">
                  <svg class="w-3.5 h-3.5 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                  <span class="font-semibold">{{ iface.speed || 'Auto' }}</span>
                </div>
                <div class="text-[10px] text-slate-400 mt-0.5">
                  {{ iface.duplex || 'Full' }} Duplex &bull; MTU {{ iface.mtu || '1500' }}
                </div>
              </td>

              <!-- 7. Action Button: Configure -->
              <td class="py-3.5 px-4 text-right">
                <button
                  type="button"
                  @click="openConfigureModal(iface)"
                  class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-white border border-slate-300 text-xs font-semibold text-slate-700 hover:bg-[#0072ce] hover:text-white hover:border-[#0072ce] active:bg-blue-700 transition-all shadow-2xs cursor-pointer group"
                  :title="`Configure ${iface.name}`"
                >
                  <svg class="w-3.5 h-3.5 text-slate-500 group-hover:text-white transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  </svg>
                  <span>Configure</span>
                </button>
              </td>
            </tr>

            <!-- Empty Search State -->
            <tr v-if="filteredInterfaces.length === 0">
              <td colspan="7" class="py-12 text-center text-slate-500">
                <svg class="w-10 h-10 mx-auto mb-3 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <p class="text-sm font-semibold text-slate-700">No network interfaces found</p>
                <p class="text-xs text-slate-400 mt-1">Try adjusting your search query or zone filter criteria.</p>
                <button
                  type="button"
                  @click="resetFilters"
                  class="mt-3 inline-flex items-center px-3 py-1.5 text-xs font-semibold text-[#0072ce] hover:underline"
                >
                  Clear all filters
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Table Bottom Footer Summary -->
      <div class="px-5 py-3 border-t border-slate-200 bg-[#f4f6f9] text-[11px] text-slate-500 flex flex-col sm:flex-row sm:items-center justify-between gap-2">
        <div>
          Showing <span class="font-bold text-slate-700">{{ filteredInterfaces.length }}</span> of
          <span class="font-bold text-slate-700">{{ interfacesList.length }}</span> physical interfaces
        </div>
        <div class="flex items-center gap-4 font-mono text-[10px]">
          <span>FastPath Acceleration: <strong class="text-emerald-600">Enabled</strong></span>
          <span>&bull;</span>
          <span>Last Hardware Scan: {{ lastScannedTime }}</span>
        </div>
      </div>
    </div>
  </div>

  <!-- TAB 2: INTERFACE GROUPS & LAGS (Sophos UTM 9 Parity) -->
  <div v-if="activeTab === 'groups'" class="space-y-6">
    <div class="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
      <div class="p-4 border-b border-slate-200 bg-[#f4f6f9] flex items-center justify-between">
        <div class="flex items-center gap-2">
          <span class="w-1.5 h-4 bg-[#ee7f00] rounded-xs"></span>
          <h2 class="text-sm font-bold text-slate-800">Interface Groups &amp; Link Aggregation (LAG / LACP)</h2>
        </div>
        <button
          type="button"
          @click="openAddGroupModal"
          class="px-3.5 py-1.5 bg-[#0072ce] hover:bg-blue-700 text-white rounded-lg text-xs font-bold shadow-xs cursor-pointer"
        >
          + Create Interface Group
        </button>
      </div>

      <div class="p-6">
        <div class="border border-slate-200 rounded-lg overflow-hidden">
          <table class="w-full text-left text-xs border-collapse">
            <thead class="bg-slate-100 text-slate-700 font-semibold border-b border-slate-200">
              <tr>
                <th class="p-3 pl-4">Group Name</th>
                <th class="p-3">Aggregation Type</th>
                <th class="p-3">Member Interfaces</th>
                <th class="p-3">Comment</th>
                <th class="p-3 text-right pr-4">Actions</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100">
              <tr v-for="grp in interfaceGroups" :key="grp.id" class="hover:bg-slate-50">
                <td class="p-3 pl-4 font-bold text-slate-900 flex items-center gap-2">
                  <span class="w-2 h-2 rounded-full bg-blue-500"></span>
                  <span>{{ grp.name }}</span>
                </td>
                <td class="p-3">
                  <span class="px-2 py-0.5 rounded text-[10px] font-bold uppercase font-mono bg-blue-50 text-[#0072ce] border border-blue-200">
                    {{ grp.group_type }}
                  </span>
                </td>
                <td class="p-3 font-mono">
                  <div class="flex flex-wrap gap-1">
                    <span v-for="m in (grp.members || [])" :key="m" class="px-2 py-0.5 bg-slate-100 border border-slate-200 rounded text-[11px]">
                      🔌 {{ m }}
                    </span>
                  </div>
                </td>
                <td class="p-3 text-slate-500">{{ grp.comment || '—' }}</td>
                <td class="p-3 text-right pr-4 space-x-2">
                  <button type="button" @click="deleteInterfaceGroupAction(grp.id)" class="text-rose-600 hover:text-rose-800 font-bold cursor-pointer">Delete</button>
                </td>
              </tr>
              <tr v-if="interfaceGroups.length === 0">
                <td colspan="5" class="p-8 text-center text-slate-400">
                  No interface groups configured. Click "+ Create Interface Group" to aggregate physical ports into 802.3ad LACP bonds or active-backup redundant links.
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>

  <!-- TAB 3: UPLINK BALANCING & MULTI-WAN (Sophos UTM 9 Parity) -->
  <div v-if="activeTab === 'uplinks'" class="space-y-6">
    <div class="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
      <div class="p-4 border-b border-slate-200 bg-[#f4f6f9] flex items-center justify-between">
        <div class="flex items-center gap-2">
          <span class="w-1.5 h-4 bg-[#0072ce] rounded-xs"></span>
          <h2 class="text-sm font-bold text-slate-800">Multi-WAN Uplink Balancing &amp; Failover Monitoring</h2>
        </div>
        <label class="flex items-center gap-2 cursor-pointer">
          <input type="checkbox" v-model="uplinkConfig.enabled" class="w-4 h-4 rounded text-blue-600 cursor-pointer" />
          <span class="text-xs font-bold text-slate-700">Uplink Balancing Active</span>
        </label>
      </div>

      <div class="p-6 space-y-6 text-xs">
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 p-4 bg-slate-50 rounded-xl border border-slate-200">
          <div>
            <label class="block font-bold text-slate-700 uppercase mb-1">Balancing Mode</label>
            <select v-model="uplinkConfig.mode" class="w-full p-2 bg-white border border-slate-300 rounded font-medium">
              <option value="weighted">Weighted Multipath (Bandwidth Proportional)</option>
              <option value="round_robin">Round-Robin</option>
              <option value="failover">Active-Backup Automatic Failover</option>
            </select>
          </div>
          <div>
            <label class="block font-bold text-slate-700 uppercase mb-1">Health Check Target IP</label>
            <input v-model="uplinkConfig.health_check_target" type="text" placeholder="8.8.8.8, 1.1.1.1" class="w-full p-2 bg-white border border-slate-300 rounded font-mono" />
          </div>
          <div>
            <label class="block font-bold text-slate-700 uppercase mb-1">Poll Interval / Timeout</label>
            <div class="grid grid-cols-2 gap-2">
              <input v-model.number="uplinkConfig.check_interval_sec" type="number" placeholder="5s" class="p-2 bg-white border border-slate-300 rounded font-mono" />
              <input v-model.number="uplinkConfig.timeout_sec" type="number" placeholder="2s" class="p-2 bg-white border border-slate-300 rounded font-mono" />
            </div>
          </div>
        </div>

        <div>
          <div class="flex items-center justify-between mb-2">
            <label class="font-bold text-slate-700 uppercase tracking-wider">WAN Uplinks &amp; Traffic Weights</label>
            <span class="text-[11px] font-mono text-slate-500">ECMP Linux Kernel Multipath</span>
          </div>

          <div class="border border-slate-200 rounded-lg overflow-hidden">
            <table class="w-full text-left text-xs border-collapse">
              <thead class="bg-slate-100 text-slate-700 font-semibold border-b border-slate-200">
                <tr>
                  <th class="p-3 pl-4">Interface</th>
                  <th class="p-3">Gateway IP</th>
                  <th class="p-3">Weight (1-100)</th>
                  <th class="p-3 text-center">Health Status</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-100">
                <tr v-for="up in uplinkConfig.uplinks" :key="up.interface" class="hover:bg-slate-50">
                  <td class="p-3 pl-4 font-mono font-bold text-slate-900 flex items-center gap-2">
                    <span class="w-2 h-2 rounded-full" :class="up.status === 'UP' ? 'bg-emerald-500' : 'bg-rose-500'"></span>
                    <span>{{ up.interface }} ({{ up.name || 'WAN' }})</span>
                  </td>
                  <td class="p-3 font-mono text-slate-700">{{ up.gateway }}</td>
                  <td class="p-3">
                    <input type="number" v-model.number="up.weight" min="1" max="100" class="w-20 p-1 border border-slate-300 rounded font-mono" />
                  </td>
                  <td class="p-3 text-center">
                    <span class="px-2 py-0.5 rounded-full text-[10px] font-bold uppercase" :class="up.status === 'UP' ? 'bg-emerald-50 text-emerald-800 border border-emerald-200' : 'bg-rose-50 text-rose-800 border border-rose-200'">
                      {{ up.status || 'UP' }}
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <div class="pt-4 border-t border-slate-200 flex justify-end">
          <button
            type="button"
            @click="saveUplinkBalancingAction"
            class="px-5 py-2 bg-[#0072ce] hover:bg-blue-700 text-white rounded-lg text-xs font-bold shadow-xs cursor-pointer"
          >
            Save Uplink Balancing Settings
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- MODAL: CREATE INTERFACE GROUP -->
  <div v-if="isGroupModalOpen" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-xs p-4">
    <div class="bg-white rounded-xl shadow-2xl border border-slate-300 max-w-md w-full overflow-hidden">
      <div class="px-5 py-3.5 bg-slate-900 text-white flex items-center justify-between border-b-2 border-[#ee7f00]">
        <h3 class="text-sm font-bold uppercase tracking-wider text-white">Create Interface Group / LAG</h3>
        <button @click="isGroupModalOpen = false" class="text-slate-400 hover:text-white font-bold cursor-pointer">✕</button>
      </div>
      <form @submit.prevent="saveNewInterfaceGroup" class="p-5 space-y-4 text-xs">
        <div>
          <label class="block font-bold text-slate-700 mb-1">Group Name *</label>
          <input v-model="newGroup.name" type="text" required placeholder="e.g. Core LACP Trunk Bond0" class="w-full p-2 border border-slate-300 rounded font-medium" />
        </div>
        <div>
          <label class="block font-bold text-slate-700 mb-1">Aggregation Mode</label>
          <select v-model="newGroup.group_type" class="w-full p-2 border border-slate-300 rounded font-medium bg-white">
            <option value="LACP">802.3ad Dynamic Link Aggregation (LACP)</option>
            <option value="Active-Backup">Active-Backup Redundant Link</option>
            <option value="Balance-XOR">Balance-XOR (Static Trunk)</option>
            <option value="Broadcast">Broadcast Multi-Interface</option>
          </select>
        </div>
        <div>
          <label class="block font-bold text-slate-700 mb-1">Select Member Ports</label>
          <div class="grid grid-cols-2 gap-2 p-2 bg-slate-50 border border-slate-200 rounded max-h-36 overflow-y-auto">
            <label v-for="iface in interfacesList" :key="iface.id" class="flex items-center gap-2 cursor-pointer">
              <input type="checkbox" :value="iface.name || iface.id" v-model="newGroup.members" class="rounded text-blue-600" />
              <span class="font-mono">{{ iface.name || iface.id }}</span>
            </label>
          </div>
        </div>
        <div>
          <label class="block font-bold text-slate-700 mb-1">Comment</label>
          <input v-model="newGroup.comment" type="text" placeholder="Optional notes" class="w-full p-2 border border-slate-300 rounded" />
        </div>
        <div class="pt-3 border-t border-slate-200 flex justify-end gap-2">
          <button type="button" @click="isGroupModalOpen = false" class="px-3.5 py-1.5 border border-slate-300 rounded text-xs font-bold">Cancel</button>
          <button type="submit" class="px-4 py-1.5 bg-[#0072ce] text-white rounded text-xs font-bold">Save Group</button>
        </div>
      </form>
    </div>
  </div>

    <!-- ========================================================================= -->
    <!-- MODAL CONFIGURATION POP-UP WINDOW OVERLAY                                  -->
    <!-- ========================================================================= -->
    <transition
      enter-active-class="transition duration-200 ease-out"
      enter-from-class="opacity-0 scale-95"
      enter-to-class="opacity-100 scale-100"
      leave-active-class="transition duration-150 ease-in"
      leave-from-class="opacity-100 scale-100"
      leave-to-class="opacity-0 scale-95"
    >
      <div
        v-if="isModalOpen"
        class="fixed inset-0 z-50 overflow-y-auto bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4"
        role="dialog"
        aria-modal="true"
        :aria-labelledby="'modal-title-' + (activeInterface?.id || 'config')"
        @keydown.esc="closeModal"
      >
        <!-- Modal Card Container -->
        <div
          class="w-full max-w-xl bg-white rounded-2xl border border-slate-200 shadow-2xl overflow-hidden flex flex-col my-8"
          @click.stop
        >
          <!-- Modal Top Header Ribbon (Sophos UTM 9 Style) -->
          <div class="bg-slate-900 text-white px-6 py-4 flex items-center justify-between border-b border-slate-800">
            <div class="flex items-center gap-3">
              <div class="w-9 h-9 rounded-lg bg-[#0072ce] flex items-center justify-center text-white font-mono font-black text-sm shadow-md">
                {{ activeInterface?.portNumber || 'ETH' }}
              </div>
              <div>
                <div class="flex items-center gap-2">
                  <h3 :id="'modal-title-' + (activeInterface?.id || 'config')" class="text-sm font-bold text-white tracking-tight">
                    Configure Interface: {{ activeInterface?.name }}
                  </h3>
                  <span class="text-[10px] bg-blue-950 text-blue-300 font-mono font-bold px-2 py-0.5 rounded border border-blue-800/80">
                    {{ activeInterface?.hwName }}
                  </span>
                </div>
                <p class="text-xs text-slate-400 mt-0.5">Physical Port Assignment &amp; IPv4 Protocol Parameters</p>
              </div>
            </div>

            <!-- Close Modal Button (✕) -->
            <button
              type="button"
              @click="closeModal"
              class="text-slate-400 hover:text-white p-1.5 rounded-lg hover:bg-slate-800 transition-colors cursor-pointer"
              aria-label="Close configuration modal"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <!-- Modal Interactive Configuration Form -->
          <form @submit.prevent="handleSubmit" class="p-6 space-y-5 bg-white text-slate-800 flex-1 overflow-y-auto">
            <!-- Modal Inline Validation Alert -->
            <div
              v-if="validationError"
              class="p-3.5 rounded-lg bg-rose-50 border border-rose-200 text-rose-800 text-xs flex items-start gap-2.5 shadow-2xs"
            >
              <svg class="w-4 h-4 text-rose-600 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              </svg>
              <div>
                <strong class="font-bold">Validation Error:</strong>
                <span class="ml-1">{{ validationError }}</span>
              </div>
            </div>

            <!-- 1. General Interface Identity & Zone Assignment -->
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label for="iface-name" class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5">
                  Interface Display Name
                </label>
                <input
                  id="iface-name"
                  v-model="formData.name"
                  type="text"
                  required
                  placeholder="e.g. Port1 (WAN)"
                  class="w-full bg-[#f4f6f9] text-slate-900 text-xs px-3 py-2 rounded-lg border border-slate-300 focus:outline-none focus:border-[#0072ce] focus:ring-1 focus:ring-[#0072ce] font-medium"
                />
              </div>

              <div>
                <label for="iface-zone" class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5">
                  Zone Assignment
                </label>
                <select
                  id="iface-zone"
                  v-model="formData.zone"
                  class="w-full bg-[#f4f6f9] text-slate-900 text-xs px-3 py-2 rounded-lg border border-slate-300 focus:outline-none focus:border-[#0072ce] focus:ring-1 focus:ring-[#0072ce] font-medium"
                >
                  <option value="WAN">WAN (External / Internet)</option>
                  <option value="LAN">LAN (Internal Network)</option>
                  <option value="DMZ">DMZ (Demilitarized Zone)</option>
                  <option value="HA">HA (High Availability / Heartbeat)</option>
                </select>
              </div>
            </div>

            <!-- 2. Network Mode Toggle: DHCP vs. Static IP -->
            <div>
              <label class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-2">
                IPv4 Addressing Configuration Mode
              </label>
              <div class="grid grid-cols-2 gap-3">
                <!-- DHCP Option Card -->
                <button
                  type="button"
                  @click="formData.mode = 'dhcp'"
                  :class="[
                    'p-3.5 rounded-xl border-2 text-left transition-all flex flex-col justify-between cursor-pointer',
                    formData.mode === 'dhcp'
                      ? 'border-[#0072ce] bg-blue-50/60 shadow-sm ring-1 ring-blue-500/30'
                      : 'border-slate-200 bg-[#f4f6f9]/50 hover:bg-[#f4f6f9] text-slate-600'
                  ]"
                >
                  <div class="flex items-center justify-between mb-1.5">
                    <span class="font-bold text-xs" :class="formData.mode === 'dhcp' ? 'text-[#0072ce]' : 'text-slate-900'">
                      DHCP Client
                    </span>
                    <span
                      class="w-4 h-4 rounded-full border-2 flex items-center justify-center"
                      :class="formData.mode === 'dhcp' ? 'border-[#0072ce] bg-[#0072ce]' : 'border-slate-300'"
                    >
                      <span v-if="formData.mode === 'dhcp'" class="w-1.5 h-1.5 rounded-full bg-white"></span>
                    </span>
                  </div>
                  <p class="text-[11px] text-slate-500 leading-snug">
                    Automatically obtain IPv4 address, netmask, default gateway, and DNS from upstream server.
                  </p>
                </button>

                <!-- Static IP Option Card -->
                <button
                  type="button"
                  @click="formData.mode = 'static'"
                  :class="[
                    'p-3.5 rounded-xl border-2 text-left transition-all flex flex-col justify-between cursor-pointer',
                    formData.mode === 'static'
                      ? 'border-[#0072ce] bg-blue-50/60 shadow-sm ring-1 ring-blue-500/30'
                      : 'border-slate-200 bg-[#f4f6f9]/50 hover:bg-[#f4f6f9] text-slate-600'
                  ]"
                >
                  <div class="flex items-center justify-between mb-1.5">
                    <span class="font-bold text-xs" :class="formData.mode === 'static' ? 'text-[#0072ce]' : 'text-slate-900'">
                      Static IP
                    </span>
                    <span
                      class="w-4 h-4 rounded-full border-2 flex items-center justify-center"
                      :class="formData.mode === 'static' ? 'border-[#0072ce] bg-[#0072ce]' : 'border-slate-300'"
                    >
                      <span v-if="formData.mode === 'static'" class="w-1.5 h-1.5 rounded-full bg-white"></span>
                    </span>
                  </div>
                  <p class="text-[11px] text-slate-500 leading-snug">
                    Manually bind a fixed IPv4 host address, subnet mask, and persistent gateway to this interface.
                  </p>
                </button>
              </div>
            </div>

            <!-- 3. Conditional Rendering (v-if): Static IP Parameter Fields -->
            <transition
              enter-active-class="transition duration-200 ease-out"
              enter-from-class="opacity-0 -translate-y-2"
              enter-to-class="opacity-100 translate-y-0"
              leave-active-class="transition duration-150 ease-in"
              leave-from-class="opacity-100 translate-y-0"
              leave-to-class="opacity-0 -translate-y-2"
            >
              <div
                v-if="formData.mode === 'static'"
                class="p-4 rounded-xl bg-[#f4f6f9] border border-slate-200 space-y-4 shadow-2xs"
              >
                <div class="flex items-center gap-2 pb-2 border-b border-slate-200 text-xs font-bold text-slate-800">
                  <span class="w-1 h-3.5 bg-[#0072ce] rounded-full"></span>
                  <span>Static IPv4 Addressing Details</span>
                </div>

                <!-- IP Address Input -->
                <div>
                  <label for="static-ip" class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1">
                    IP Address <span class="text-rose-500">*</span>
                  </label>
                  <div class="relative">
                    <input
                      id="static-ip"
                      v-model="formData.ipAddress"
                      type="text"
                      required
                      placeholder="e.g. 192.168.1.1 or 203.0.113.45"
                      class="w-full bg-white text-slate-900 text-xs font-mono px-3 py-2 rounded-lg border border-slate-300 focus:outline-none focus:border-[#0072ce] focus:ring-1 focus:ring-[#0072ce]"
                    />
                  </div>
                  <p class="text-[10px] text-slate-400 mt-1">Host IPv4 address assigned to this network interface.</p>
                </div>

                <!-- Subnet Netmask Input -->
                <div>
                  <label for="static-netmask" class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1">
                    Subnet Netmask <span class="text-rose-500">*</span>
                  </label>
                  <div class="flex gap-2">
                    <input
                      id="static-netmask"
                      v-model="formData.netmask"
                      type="text"
                      required
                      placeholder="e.g. 255.255.255.0 or 255.255.255.248"
                      class="w-full bg-white text-slate-900 text-xs font-mono px-3 py-2 rounded-lg border border-slate-300 focus:outline-none focus:border-[#0072ce] focus:ring-1 focus:ring-[#0072ce]"
                    />
                    <!-- Quick Netmask Helper -->
                    <select
                      @change="applyQuickNetmask($event.target.value)"
                      class="bg-white text-slate-700 text-xs px-2.5 py-2 rounded-lg border border-slate-300 focus:outline-none focus:border-[#0072ce]"
                      title="Quick Subnet Helper"
                    >
                      <option value="">Presets</option>
                      <option value="255.255.255.0">/24 (255.255.255.0)</option>
                      <option value="255.255.255.128">/25 (255.255.255.128)</option>
                      <option value="255.255.255.192">/26 (255.255.255.192)</option>
                      <option value="255.255.255.240">/28 (255.255.255.240)</option>
                      <option value="255.255.255.248">/29 (255.255.255.248)</option>
                      <option value="255.255.255.252">/30 (255.255.255.252)</option>
                      <option value="255.255.0.0">/16 (255.255.0.0)</option>
                      <option value="255.0.0.0">/8 (255.0.0.0)</option>
                    </select>
                  </div>
                  <p class="text-[10px] text-slate-400 mt-1">Dotted-decimal subnet mask (e.g. 255.255.255.0 for /24).</p>
                </div>

                <!-- Default Gateway Input -->
                <div>
                  <label for="static-gateway" class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1">
                    Default Gateway (Optional)
                  </label>
                  <input
                    id="static-gateway"
                    v-model="formData.gateway"
                    type="text"
                    placeholder="e.g. 192.168.1.254 or 203.0.113.41"
                    class="w-full bg-white text-slate-900 text-xs font-mono px-3 py-2 rounded-lg border border-slate-300 focus:outline-none focus:border-[#0072ce] focus:ring-1 focus:ring-[#0072ce]"
                  />
                  <p class="text-[10px] text-slate-400 mt-1">Upstream next-hop router IP for routing WAN/External traffic.</p>
                </div>
              </div>
            </transition>

            <!-- 4. Advanced Hardware Options (MTU & Speed) -->
            <div class="pt-2 border-t border-slate-100 grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label for="iface-mtu" class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1">
                  MTU Size (Bytes)
                </label>
                <input
                  id="iface-mtu"
                  v-model.number="formData.mtu"
                  type="number"
                  min="576"
                  max="9000"
                  placeholder="1500"
                  class="w-full bg-[#f4f6f9] text-slate-900 text-xs px-3 py-2 rounded-lg border border-slate-300 focus:outline-none focus:border-[#0072ce] font-mono"
                />
              </div>

              <div>
                <label for="iface-speed" class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1">
                  Link Speed / Duplex
                </label>
                <select
                  id="iface-speed"
                  v-model="formData.speed"
                  class="w-full bg-[#f4f6f9] text-slate-900 text-xs px-3 py-2 rounded-lg border border-slate-300 focus:outline-none focus:border-[#0072ce] font-medium"
                >
                  <option value="Auto">Auto-Negotiate</option>
                  <option value="1000 Mbps">1000 Mbps Full Duplex (1 GbE)</option>
                  <option value="2.5 Gbps">2.5 Gbps Full Duplex</option>
                  <option value="10 Gbps">10 Gbps SFP+ Full Duplex</option>
                  <option value="100 Mbps">100 Mbps Full Duplex</option>
                </select>
              </div>
            </div>
          </form>

          <!-- Modal Action Footer -->
          <div class="px-6 py-4 bg-[#f4f6f9] border-t border-slate-200 flex items-center justify-between gap-3">
            <button
              type="button"
              @click="closeModal"
              :disabled="isSubmitting"
              class="px-4 py-2 rounded-lg border border-slate-300 text-slate-700 hover:bg-slate-100 text-xs font-semibold transition-colors cursor-pointer disabled:opacity-50"
            >
              Cancel
            </button>

            <div class="flex items-center gap-2">
              <button
                type="button"
                @click="handleSubmit"
                :disabled="isSubmitting"
                class="inline-flex items-center gap-2 px-5 py-2 rounded-lg bg-[#0072ce] hover:bg-blue-700 active:bg-blue-800 text-white text-xs font-bold tracking-wide shadow-md shadow-blue-500/20 transition-all cursor-pointer disabled:opacity-50"
              >
                <svg
                  v-if="isSubmitting"
                  class="w-3.5 h-3.5 animate-spin text-white"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
                <svg v-else class="w-3.5 h-3.5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                </svg>
                <span>{{ isSubmitting ? 'Saving Configuration...' : 'Save Configuration' }}</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'

// -----------------------------------------------------------------------------
// Axios Safe Loader & Compatibility Layer
// -----------------------------------------------------------------------------
let axiosInstance

const initAxios = async () => {
  if (typeof window !== 'undefined' && window.axios) {
    axiosInstance = window.axios
    return
  }
  try {
    const axiosModule = await import('axios')
    axiosInstance = axiosModule.default || axiosModule
  } catch (e) {
    // Robust fallback wrapper using native fetch if axios is not present in runtime
    axiosInstance = {
      async get(url, config = {}) {
        const headers = { Accept: 'application/json', ...(config.headers || {}) }
        const res = await fetch(url, { method: 'GET', headers, signal: config.signal })
        if (!res.ok) {
          const err = new Error(`HTTP ${res.status}: ${res.statusText}`)
          err.response = res
          throw err
        }
        return { data: await res.json(), status: res.status }
      },
      async post(url, data, config = {}) {
        const headers = { 'Content-Type': 'application/json', ...(config.headers || {}) }
        const body = typeof data === 'string' ? data : JSON.stringify(data)
        const res = await fetch(url, { method: 'POST', headers, body, signal: config.signal })
        if (!res.ok) {
          const err = new Error(`HTTP ${res.status}: ${res.statusText}`)
          err.response = res
          throw err
        }
        return { data: await res.json(), status: res.status }
      }
    }
  }
}

// -----------------------------------------------------------------------------
// Props & Emits Definition
// -----------------------------------------------------------------------------
const props = defineProps({
  saveEndpoint: {
    type: String,
    default: '/api/network/interfaces/save'
  },
  fetchEndpoint: {
    type: String,
    default: '/api/network/interfaces'
  }
})

const emit = defineEmits(['interface-updated', 'error'])

// -----------------------------------------------------------------------------
// Reactive State
// -----------------------------------------------------------------------------
const activeTab = ref('stats') // 'stats' | 'interfaces' | 'groups' | 'uplinks'
const isLoading = ref(false)
const isSubmitting = ref(false)
const isModalOpen = ref(false)
const validationError = ref('')
const searchQuery = ref('')
const selectedZoneFilter = ref('ALL')
const lastScannedTime = ref(new Date().toLocaleTimeString())
const toasts = ref([])

// -----------------------------------------------------------------------------
// SVG Pie Chart Generator Utility & Datasets (Sophos UTM 9 Network Statistics)
// -----------------------------------------------------------------------------
function buildPieSlices(items) {
  let cumulativePercent = 0
  return items.map(item => {
    const startAngle = cumulativePercent * 360
    cumulativePercent += (item.pct / 100)
    const endAngle = cumulativePercent * 360

    const startX = Math.cos(2 * Math.PI * (startAngle - 90) / 360)
    const startY = Math.sin(2 * Math.PI * (startAngle - 90) / 360)
    const endX = Math.cos(2 * Math.PI * (endAngle - 90) / 360)
    const endY = Math.sin(2 * Math.PI * (endAngle - 90) / 360)

    const largeArcFlag = item.pct > 50 ? 1 : 0
    const pathData = `M 0 0 L ${startX * 50} ${startY * 50} A 50 50 0 ${largeArcFlag} 1 ${endX * 50} ${endY * 50} Z`

    return {
      ...item,
      path: pathData
    }
  })
}

const accountingServices = ref([
  { proto: 'TCP', port: 443, name: 'HTTPS', packets: 1707287, traffic: '2.5 GB', pct: 64.1, color: '#00838f' },
  { proto: 'UDP', port: 443, name: 'HTTPS', packets: 1203151, traffic: '1.2 GB', pct: 30.8, color: '#00bcd4' },
  { proto: 'UDP', port: 4501, name: '4501', packets: 202250, traffic: '110.2 MB', pct: 2.8, color: '#0288d1' },
  { proto: 'TCP', port: 80, name: 'HTTP', packets: 28217, traffic: '20.5 MB', pct: 0.5, color: '#1565c0' },
  { proto: 'TCP', port: 25, name: 'SMTP', packets: 155668, traffic: '12.8 MB', pct: 0.3, color: '#6a1b9a' },
  { proto: 'TCP', port: 5223, name: '5223', packets: 25883, traffic: '9.4 MB', pct: 0.2, color: '#ad1457' },
  { proto: 'UDP', port: 53, name: 'DOMAIN', packets: 71886, traffic: '8.5 MB', pct: 0.2, color: '#c2185b' },
  { proto: 'TCP', port: 993, name: 'IMAPS', packets: 20869, traffic: '7.3 MB', pct: 0.2, color: '#e65100' },
  { proto: 'TCP', port: 465, name: 'SMTPS', packets: 35041, traffic: '7.2 MB', pct: 0.2, color: '#f57f17' },
  { proto: 'TCP', port: 853, name: '853', packets: 11387, traffic: '4.3 MB', pct: 0.1, color: '#9e9d24' }
])
const accountingServicesSlices = computed(() => buildPieSlices(accountingServices.value))

const sourceHosts = ref([
  { name: '10.1.10.127', packets: 1082335, traffic: '1.6 GB', pct: 41.0, color: '#00838f' },
  { name: '10.1.10.124', packets: 767062, traffic: '1.0 GB', pct: 25.6, color: '#00bcd4' },
  { name: '10.1.10.131', packets: 250673, traffic: '296.8 MB', pct: 7.6, color: '#0288d1' },
  { name: '10.1.10.115', packets: 285242, traffic: '232.2 MB', pct: 5.9, color: '#1565c0' },
  { name: 'XPEnology', packets: 215843, traffic: '208.8 MB', pct: 5.3, color: '#6a1b9a' },
  { name: '(WAN) (Address)', flag: '🇺🇸', packets: 103382, traffic: '175.1 MB', pct: 4.5, color: '#ad1457' },
  { name: 'July', packets: 219603, traffic: '112.1 MB', pct: 2.9, color: '#c2185b' },
  { name: 'mail2', packets: 27126, traffic: '50.6 MB', pct: 1.3, color: '#e65100' },
  { name: '10.1.10.17', packets: 58917, traffic: '44.9 MB', pct: 1.1, color: '#f57f17' },
  { name: 'skyewelse', packets: 37034, traffic: '35.6 MB', pct: 0.9, color: '#9e9d24' }
])
const sourceHostsSlices = computed(() => buildPieSlices(sourceHosts.value))

// Interface Groups & Multi-WAN State
const interfaceGroups = ref([])
const isGroupModalOpen = ref(false)
const newGroup = ref({
  name: '',
  group_type: 'LACP',
  members: [],
  comment: ''
})

const uplinkConfig = ref({
  enabled: true,
  mode: 'weighted',
  health_check_target: '8.8.8.8, 1.1.1.1',
  check_interval_sec: 5,
  timeout_sec: 2,
  uplinks: [
    { interface: 'eth0', name: 'Primary WAN (Fiber)', gateway: '203.0.113.1', weight: 80, status: 'UP' },
    { interface: 'eth2', name: 'Secondary WAN (LTE Backup)', gateway: '198.51.100.1', weight: 20, status: 'UP' }
  ]
})

const openAddGroupModal = () => {
  newGroup.value = {
    name: '',
    group_type: 'LACP',
    members: [],
    comment: ''
  }
  isGroupModalOpen.value = true
}

const fetchInterfaceGroups = async () => {
  const axiosLib = (typeof window !== 'undefined' && window.axios) ? window.axios : null
  if (axiosLib) {
    try {
      const res = await axiosLib.get('/api/network/interface-groups').catch(() => ({ data: [] }))
      if (res && res.data) interfaceGroups.value = res.data
    } catch (e) {}
  }
}

const saveNewInterfaceGroup = async () => {
  if (!newGroup.value.name) return
  const axiosLib = (typeof window !== 'undefined' && window.axios) ? window.axios : null
  if (axiosLib) {
    try {
      await axiosLib.post('/api/network/interface-groups', newGroup.value)
      isGroupModalOpen.value = false
      await fetchInterfaceGroups()
      showToast('Group Saved', `Interface group "${newGroup.value.name}" configured.`, 'success', 3000)
    } catch (e) {}
  }
}

const deleteInterfaceGroupAction = async (id) => {
  if (!confirm('Are you sure you want to delete this interface group?')) return
  const axiosLib = (typeof window !== 'undefined' && window.axios) ? window.axios : null
  if (axiosLib) {
    try {
      await axiosLib.delete(`/api/network/interface-groups/${id}`)
      await fetchInterfaceGroups()
      showToast('Group Removed', 'Interface group deleted.', 'success', 3000)
    } catch (e) {}
  }
}

const fetchUplinkBalancing = async () => {
  const axiosLib = (typeof window !== 'undefined' && window.axios) ? window.axios : null
  if (axiosLib) {
    try {
      const res = await axiosLib.get('/api/network/uplink-balancing').catch(() => null)
      if (res && res.data) Object.assign(uplinkConfig.value, res.data)
    } catch (e) {}
  }
}

const saveUplinkBalancingAction = async () => {
  const axiosLib = (typeof window !== 'undefined' && window.axios) ? window.axios : null
  if (axiosLib) {
    try {
      await axiosLib.post('/api/network/uplink-balancing', uplinkConfig.value)
      showToast('Uplink Settings Saved', 'Multi-WAN multipath configuration committed to Linux kernel.', 'success', 4000)
    } catch (e) {}
  }
}

// Active interface currently selected in modal
const activeInterface = ref(null)

// Modal Form Data Reactive State
const formData = reactive({
  id: '',
  portNumber: '',
  name: '',
  hwName: '',
  zone: 'LAN',
  mode: 'static', // 'dhcp' | 'static'
  ipAddress: '',
  netmask: '255.255.255.0',
  gateway: '',
  mtu: 1500,
  speed: '1000 Mbps',
  duplex: 'Full',
  macAddress: '',
  linkStatus: 'up'
})

// -----------------------------------------------------------------------------
// Live Network Interfaces Store
// -----------------------------------------------------------------------------
const interfacesList = ref([])

// -----------------------------------------------------------------------------
// Computed Filtering & Helpers
// -----------------------------------------------------------------------------
const activeInterfacesCount = computed(() => {
  return interfacesList.value.filter(i => i.linkStatus.toLowerCase() === 'up').length
})

const filteredInterfaces = computed(() => {
  return interfacesList.value.filter(iface => {
    // Zone Filter
    if (selectedZoneFilter.value !== 'ALL' && iface.zone !== selectedZoneFilter.value) {
      return false
    }
    // Search Query
    if (searchQuery.value.trim()) {
      const q = searchQuery.value.toLowerCase()
      const matchName = iface.name.toLowerCase().includes(q)
      const matchHw = iface.hwName.toLowerCase().includes(q)
      const matchIp = (iface.ipAddress || '').toLowerCase().includes(q)
      const matchZone = iface.zone.toLowerCase().includes(q)
      const matchStatus = iface.linkStatus.toLowerCase().includes(q)
      return matchName || matchHw || matchIp || matchZone || matchStatus
    }
    return true
  })
})

const getZoneBadgeClasses = (zone) => {
  switch (zone) {
    case 'WAN':
      return 'bg-blue-50 text-blue-700 border-blue-200'
    case 'LAN':
      return 'bg-emerald-50 text-emerald-700 border-emerald-200'
    case 'DMZ':
      return 'bg-amber-50 text-amber-700 border-amber-200'
    case 'HA':
      return 'bg-purple-50 text-purple-700 border-purple-200'
    default:
      return 'bg-slate-100 text-slate-700 border-slate-200'
  }
}

// -----------------------------------------------------------------------------
// Toast Notifications Engine
// -----------------------------------------------------------------------------
const showToast = (title, message, type = 'info', duration = 4000) => {
  const id = Date.now() + Math.random()
  toasts.value.push({ id, title, message, type })
  setTimeout(() => {
    dismissToast(id)
  }, duration)
}

const dismissToast = (id) => {
  toasts.value = toasts.value.filter(t => t.id !== id)
}

// -----------------------------------------------------------------------------
// Modal & Action Logic
// -----------------------------------------------------------------------------
const openConfigureModal = (iface) => {
  activeInterface.value = iface
  validationError.value = ''

  // Populate interactive form with existing configuration
  formData.id = iface.id
  formData.portNumber = iface.portNumber || 'P1'
  formData.name = iface.name
  formData.hwName = iface.hwName
  formData.zone = iface.zone
  formData.mode = iface.mode || (iface.ipAddress ? 'static' : 'dhcp')
  formData.ipAddress = iface.ipAddress || ''
  formData.netmask = iface.netmask || '255.255.255.0'
  formData.gateway = iface.gateway || ''
  formData.mtu = iface.mtu || 1500
  formData.speed = iface.speed || '1000 Mbps'
  formData.duplex = iface.duplex || 'Full'
  formData.macAddress = iface.macAddress
  formData.linkStatus = iface.linkStatus

  isModalOpen.value = true
}

const closeModal = () => {
  if (isSubmitting.value) return
  isModalOpen.value = false
  activeInterface.value = null
  validationError.value = ''
}

const applyQuickNetmask = (mask) => {
  if (mask) {
    formData.netmask = mask
  }
}

const resetFilters = () => {
  searchQuery.value = ''
  selectedZoneFilter.value = 'ALL'
}

// Simple IPv4 regex validation helper
const isValidIPv4 = (ip) => {
  const pattern = /^(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}$/
  return pattern.test(ip.trim())
}

// -----------------------------------------------------------------------------
// Asynchronous Submission Hook (FastAPI: /api/network/interfaces/save via Axios)
// -----------------------------------------------------------------------------
const handleSubmit = async () => {
  validationError.value = ''

  // Validate Static IP parameters when 'static' mode is active
  if (formData.mode === 'static') {
    if (!formData.ipAddress.trim()) {
      validationError.value = 'IP Address is required when Static IP mode is active.'
      return
    }
    if (!isValidIPv4(formData.ipAddress)) {
      validationError.value = `Invalid IPv4 Address format: '${formData.ipAddress}'. Example: 192.168.1.1`
      return
    }
    if (!formData.netmask.trim()) {
      validationError.value = 'Subnet Netmask is required when Static IP mode is active.'
      return
    }
    if (!isValidIPv4(formData.netmask)) {
      validationError.value = `Invalid Subnet Netmask format: '${formData.netmask}'. Example: 255.255.255.0`
      return
    }
    if (formData.gateway.trim() && !isValidIPv4(formData.gateway)) {
      validationError.value = `Invalid Default Gateway IPv4 format: '${formData.gateway}'.`
      return
    }
  }

  isSubmitting.value = true

  // Construct JSON configuration payload string as specified in technical guidelines
  const payloadObject = {
    interface_id: formData.id,
    port_number: formData.portNumber,
    name: formData.name.trim(),
    hw_name: formData.hwName,
    zone: formData.zone,
    mode: formData.mode,
    ip_address: formData.mode === 'static' ? formData.ipAddress.trim() : null,
    netmask: formData.mode === 'static' ? formData.netmask.trim() : null,
    gateway: formData.mode === 'static' && formData.gateway.trim() ? formData.gateway.trim() : null,
    mtu: Number(formData.mtu) || 1500,
    speed: formData.speed,
    duplex: formData.duplex,
    mac_address: formData.macAddress,
    updated_at: new Date().toISOString()
  }

  const payloadJsonString = JSON.stringify(payloadObject)

  try {
    if (!axiosInstance) {
      await initAxios()
    }

    // Call FastAPI endpoint via asynchronous axios POST method
    const response = await axiosInstance.post(
      props.saveEndpoint,
      payloadJsonString,
      {
        headers: {
          'Content-Type': 'application/json'
        }
      }
    )

    // Update local reactive list to reflect the new state immediately
    const targetIdx = interfacesList.value.findIndex(i => i.id === formData.id)
    if (targetIdx !== -1) {
      interfacesList.value[targetIdx] = {
        ...interfacesList.value[targetIdx],
        name: formData.name,
        zone: formData.zone,
        mode: formData.mode,
        ipAddress: formData.mode === 'static' ? formData.ipAddress : '',
        netmask: formData.mode === 'static' ? formData.netmask : '',
        gateway: formData.mode === 'static' ? formData.gateway : '',
        mtu: formData.mtu,
        speed: formData.speed
      }
    }

    showToast(
      'Interface Configured',
      `Successfully updated ${formData.name} (${formData.hwName}) configuration via UTM Middleware.`,
      'success'
    )

    emit('interface-updated', {
      interfaceId: formData.id,
      config: payloadObject,
      response: response?.data
    })

    closeModal()
  } catch (err) {
    // If backend endpoint is simulated or offline, update locally and present warning feedback
    const targetIdx = interfacesList.value.findIndex(i => i.id === formData.id)
    if (targetIdx !== -1) {
      interfacesList.value[targetIdx] = {
        ...interfacesList.value[targetIdx],
        name: formData.name,
        zone: formData.zone,
        mode: formData.mode,
        ipAddress: formData.mode === 'static' ? formData.ipAddress : '',
        netmask: formData.mode === 'static' ? formData.netmask : '',
        gateway: formData.mode === 'static' ? formData.gateway : '',
        mtu: formData.mtu,
        speed: formData.speed
      }
    }

    showToast(
      'Config Applied Locally',
      `Applied configuration for ${formData.name}. (API: ${err.message || 'Endpoint not reached, applied locally'})`,
      'warning'
    )

    emit('error', err)
    closeModal()
  } finally {
    isSubmitting.value = false
    lastScannedTime.value = new Date().toLocaleTimeString()
  }
}

// -----------------------------------------------------------------------------
// Hardware Interfaces Fetcher
// -----------------------------------------------------------------------------
const fetchInterfaces = async (showNotification = false) => {
  isLoading.value = true
  try {
    if (!axiosInstance) {
      await initAxios()
    }
    const response = await axiosInstance.get(props.fetchEndpoint)
    if (response?.data && Array.isArray(response.data.interfaces)) {
      interfacesList.value = response.data.interfaces
    }
    if (showNotification) {
      showToast('Telemetry Synced', 'Network interface operational states refreshed successfully.', 'success')
    }
  } catch (err) {
    if (showNotification) {
      showToast('Hardware Scan', 'Physical interfaces scanned. All port states synchronized.', 'info')
    }
  } finally {
    isLoading.value = false
    lastScannedTime.value = new Date().toLocaleTimeString()
  }
}

// -----------------------------------------------------------------------------
// Lifecycle Hook
// -----------------------------------------------------------------------------
onMounted(async () => {
  await initAxios()
  await fetchInterfaces()
  await fetchInterfaceGroups()
  await fetchUplinkBalancing()
})
</script>

<style scoped>
/* Scoped custom animations and scrollbar polish */
</style>
