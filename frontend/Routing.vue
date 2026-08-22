<template>
  <div class="space-y-6">
    <!-- Top Header Banner -->
    <div class="bg-slate-900 text-white rounded-2xl p-6 shadow-xl border border-slate-800 flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div>
        <div class="flex items-center gap-2 mb-1">
          <div class="w-8 h-8 rounded-lg bg-[#0072ce] flex items-center justify-center text-white font-black text-sm">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7" />
            </svg>
          </div>
          <h1 class="text-xl font-bold tracking-tight">Routing &amp; Gateways</h1>
          <span class="text-[10px] bg-blue-950 text-blue-300 font-mono font-bold px-2 py-0.5 rounded border border-blue-800/80">
            KERNEL FIB
          </span>
        </div>
        <p class="text-xs text-slate-400">
          Configure static routing tables, policy-based gateway steering (PBR), and dynamic BGP/OSPF protocol daemons.
        </p>
      </div>

      <div class="flex items-center gap-3">
        <button
          @click="fetchRoutes"
          :disabled="loading"
          class="px-3.5 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-xl text-xs font-semibold flex items-center gap-1.5 transition-colors cursor-pointer"
        >
          <svg class="w-3.5 h-3.5" :class="{ 'animate-spin': loading }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          <span>Refresh FIB</span>
        </button>
        <button
          v-if="activeTab === 'static'"
          @click="openAddModal"
          class="px-4 py-2 bg-[#0072ce] hover:bg-blue-600 text-white rounded-xl text-xs font-bold shadow-lg shadow-blue-500/20 flex items-center gap-1.5 transition-all cursor-pointer"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          <span>+ Add Route</span>
        </button>

        <button
          v-else-if="activeTab === 'pbr'"
          @click="openAddPbrModal"
          class="px-4 py-2 bg-[#0072ce] hover:bg-blue-600 text-white rounded-xl text-xs font-bold shadow-lg shadow-blue-500/20 flex items-center gap-1.5 transition-all cursor-pointer"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          <span>+ Add Policy Route</span>
        </button>
      </div>
    </div>

    <!-- Navigation Sub-Tabs -->
    <div class="flex border-b border-slate-200 gap-2">
      <button
        v-for="tab in tabs"
        :key="tab.id"
        @click="activeTab = tab.id"
        :class="[
          'px-4 py-2.5 text-xs font-bold transition-all border-b-2 flex items-center gap-2 cursor-pointer',
          activeTab === tab.id
            ? 'border-[#0072ce] text-[#0072ce] bg-blue-50/50 rounded-t-lg'
            : 'border-transparent text-slate-500 hover:text-slate-800'
        ]"
      >
        <span>{{ tab.label }}</span>
        <span
          v-if="tab.badge"
          class="px-1.5 py-0.5 text-[10px] rounded-full font-mono font-bold"
          :class="activeTab === tab.id ? 'bg-[#0072ce] text-white' : 'bg-slate-200 text-slate-600'"
        >
          {{ tab.badge }}
        </span>
      </button>
    </div>

    <!-- TAB 1: Static Routes Table -->
    <div v-if="activeTab === 'static'" class="space-y-4">
      <div class="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
        <div class="px-5 py-4 bg-slate-50 border-b border-slate-200 flex items-center justify-between">
          <div>
            <h3 class="text-xs font-bold text-slate-800 uppercase tracking-wider">IPv4 &amp; IPv6 Static Routing Table</h3>
            <p class="text-[11px] text-slate-500 mt-0.5">Direct packet forwarding paths assigned to next-hop IP gateways and physical interfaces</p>
          </div>
          <span class="text-xs font-mono font-bold text-slate-500 bg-white px-2.5 py-1 rounded border border-slate-200">
            {{ routes.length }} Route(s)
          </span>
        </div>

        <div class="overflow-x-auto">
          <table class="w-full text-left text-xs">
            <thead class="bg-[#f4f6f9] text-slate-600 font-bold border-b border-slate-200">
              <tr>
                <th class="p-3 pl-5">Status</th>
                <th class="p-3">Destination Subnet</th>
                <th class="p-3">Gateway IP</th>
                <th class="p-3">Interface</th>
                <th class="p-3">Metric</th>
                <th class="p-3">Type</th>
                <th class="p-3">Comment</th>
                <th class="p-3 pr-5 text-right">Actions</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100 font-medium text-slate-700">
              <tr v-if="loading" class="text-center">
                <td colspan="8" class="p-8 text-slate-400">Loading kernel routing entries...</td>
              </tr>
              <tr v-else-if="routes.length === 0" class="text-center">
                <td colspan="8" class="p-8 text-slate-400">No static routes configured. Click "+ Add Route" to create one.</td>
              </tr>
              <tr
                v-for="route in routes"
                :key="route.id"
                class="hover:bg-slate-50/80 transition-colors"
              >
                <td class="p-3 pl-5">
                  <span
                    class="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-bold font-mono"
                    :class="route.enabled ? 'bg-emerald-100 text-emerald-800' : 'bg-slate-200 text-slate-600'"
                  >
                    <span class="w-1.5 h-1.5 rounded-full" :class="route.enabled ? 'bg-emerald-500' : 'bg-slate-400'"></span>
                    {{ route.enabled ? 'ACTIVE' : 'DISABLED' }}
                  </span>
                </td>
                <td class="p-3 font-mono font-bold text-slate-900">{{ route.destination }}</td>
                <td class="p-3 font-mono text-slate-700">{{ route.gateway || 'Directly Connected' }}</td>
                <td class="p-3">
                  <span class="px-2 py-0.5 rounded bg-blue-50 text-[#0072ce] border border-blue-200 font-mono text-[11px] font-bold">
                    {{ route.interface }}
                  </span>
                </td>
                <td class="p-3 font-mono font-bold text-slate-600">{{ route.metric }}</td>
                <td class="p-3">
                  <span class="px-2 py-0.5 rounded text-[11px] font-bold" :class="route.route_type === 'Default Gateway' ? 'bg-amber-100 text-amber-800' : 'bg-slate-100 text-slate-700'">
                    {{ route.route_type }}
                  </span>
                </td>
                <td class="p-3 text-slate-500 text-[11px] max-w-xs truncate">{{ route.comment || '—' }}</td>
                <td class="p-3 pr-5 text-right">
                  <div class="flex items-center justify-end gap-2">
                    <button
                      @click="editRoute(route)"
                      class="text-blue-600 hover:text-blue-800 font-bold text-[11px] cursor-pointer"
                    >
                      Edit
                    </button>
                    <button
                      @click="deleteRoute(route.id)"
                      class="text-rose-600 hover:text-rose-800 font-bold text-[11px] cursor-pointer"
                    >
                      Delete
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- TAB 2: Policy-Based Routing (PBR) (Sophos UTM 9 Parity) -->
    <div v-else-if="activeTab === 'pbr'" class="space-y-4">
      <div class="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
        <div class="px-5 py-4 bg-slate-50 border-b border-slate-200 flex items-center justify-between">
          <div>
            <h3 class="text-xs font-bold text-slate-800 uppercase tracking-wider">Policy-Based Routing (PBR) Rules</h3>
            <p class="text-[11px] text-slate-500 mt-0.5">Route traffic through specific WAN interfaces based on source IP, protocol port, or destination service</p>
          </div>
          <span class="text-xs font-mono font-bold text-slate-500 bg-white px-2.5 py-1 rounded border border-slate-200">
            {{ pbrRoutes.length }} Rule(s)
          </span>
        </div>

        <div class="overflow-x-auto">
          <table class="w-full text-left text-xs">
            <thead class="bg-[#f4f6f9] text-slate-600 font-bold border-b border-slate-200">
              <tr>
                <th class="p-3 pl-5">Status</th>
                <th class="p-3">Rule Name</th>
                <th class="p-3">Source Network</th>
                <th class="p-3">Destination Network</th>
                <th class="p-3">Service / Port</th>
                <th class="p-3">Target Gateway / Interface</th>
                <th class="p-3">Comment</th>
                <th class="p-3 pr-5 text-right">Actions</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100 font-medium text-slate-700">
              <tr v-if="pbrRoutes.length === 0" class="text-center">
                <td colspan="8" class="p-8 text-slate-400">No policy-based routes configured. Click "+ Add Policy Route" to steer application traffic.</td>
              </tr>
              <tr v-for="pbr in pbrRoutes" :key="pbr.id" class="hover:bg-slate-50/80 transition-colors">
                <td class="p-3 pl-5">
                  <span
                    class="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-bold font-mono"
                    :class="pbr.enabled ? 'bg-emerald-100 text-emerald-800' : 'bg-slate-200 text-slate-600'"
                  >
                    <span class="w-1.5 h-1.5 rounded-full" :class="pbr.enabled ? 'bg-emerald-500' : 'bg-slate-400'"></span>
                    {{ pbr.enabled ? 'ACTIVE' : 'DISABLED' }}
                  </span>
                </td>
                <td class="p-3 font-bold text-slate-900">{{ pbr.name }}</td>
                <td class="p-3 font-mono text-slate-700">{{ pbr.source || 'Any' }}</td>
                <td class="p-3 font-mono text-slate-700">{{ pbr.destination || 'Any' }}</td>
                <td class="p-3">
                  <span class="px-2 py-0.5 rounded bg-purple-50 text-purple-700 border border-purple-200 font-mono text-[10px] font-bold">
                    {{ pbr.service || 'Any' }}
                  </span>
                </td>
                <td class="p-3 font-mono font-bold text-[#0072ce]">{{ pbr.target_gateway || pbr.interface }}</td>
                <td class="p-3 text-slate-500 max-w-xs truncate">{{ pbr.comment || '—' }}</td>
                <td class="p-3 pr-5 text-right space-x-2">
                  <button @click="deletePbrAction(pbr.id)" class="text-rose-600 hover:text-rose-800 font-bold cursor-pointer">Delete</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- TAB 3: Dynamic Routing (BGP / OSPF) -->
    <div v-else-if="activeTab === 'dynamic'" class="space-y-4">
      <div class="bg-white rounded-2xl border border-slate-200 shadow-sm p-6 space-y-5">
        <div>
          <h3 class="text-xs font-bold text-slate-800 uppercase tracking-wider">Dynamic Routing Protocol Engine (FRRouting)</h3>
          <p class="text-[11px] text-slate-500 mt-0.5">Autonomous System Number (ASN) peering and dynamic area route advertisements</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
          <!-- BGP Section -->
          <div class="p-4 rounded-xl border border-slate-200 space-y-3 bg-slate-50/50">
            <div class="flex items-center justify-between">
              <span class="text-xs font-bold text-slate-800">Border Gateway Protocol (BGP)</span>
              <span class="text-[10px] bg-slate-200 text-slate-600 px-2 py-0.5 rounded font-mono font-bold">ASN 65001</span>
            </div>
            <div class="space-y-2 text-xs">
              <div>
                <label class="block text-[11px] font-bold text-slate-600 mb-1">Local BGP Router ID</label>
                <input type="text" value="192.168.1.1" disabled class="w-full p-2 bg-white border border-slate-300 rounded font-mono text-xs" />
              </div>
              <div>
                <label class="block text-[11px] font-bold text-slate-600 mb-1">Peer Neighbor ASN</label>
                <input type="text" placeholder="e.g. 64512 (AWS Direct Connect)" class="w-full p-2 bg-white border border-slate-300 rounded text-xs" />
              </div>
            </div>
          </div>

          <!-- OSPF Section -->
          <div class="p-4 rounded-xl border border-slate-200 space-y-3 bg-slate-50/50">
            <div class="flex items-center justify-between">
              <span class="text-xs font-bold text-slate-800">Open Shortest Path First (OSPF v2/v3)</span>
              <span class="text-[10px] bg-slate-200 text-slate-600 px-2 py-0.5 rounded font-mono font-bold">Area 0.0.0.0</span>
            </div>
            <div class="space-y-2 text-xs">
              <div>
                <label class="block text-[11px] font-bold text-slate-600 mb-1">OSPF Backbone Area</label>
                <input type="text" value="0.0.0.0 (Backbone Area)" disabled class="w-full p-2 bg-white border border-slate-300 rounded font-mono text-xs" />
              </div>
              <div>
                <label class="block text-[11px] font-bold text-slate-600 mb-1">Redistribute Connected Subnets</label>
                <select class="w-full p-2 bg-white border border-slate-300 rounded text-xs">
                  <option value="enabled">Enabled (Advertise LAN + DMZ)</option>
                  <option value="disabled">Disabled</option>
                </select>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 4: Live Kernel FIB Table -->
    <div v-else-if="activeTab === 'fib'" class="space-y-4">
      <div class="bg-slate-900 rounded-2xl border border-slate-800 p-5 shadow-xl text-white space-y-3">
        <div class="flex items-center justify-between border-b border-slate-800 pb-3">
          <div class="flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            <h3 class="text-xs font-bold tracking-wider uppercase text-emerald-400">Live Linux Kernel Forwarding Information Base (FIB)</h3>
          </div>
          <span class="text-[10px] font-mono text-slate-400">ip route show</span>
        </div>
        <pre class="bg-slate-950 p-4 rounded-xl font-mono text-xs text-slate-300 overflow-x-auto leading-relaxed border border-slate-800/80">{{ kernelFIB }}</pre>
      </div>
    </div>

    <!-- ADD / EDIT ROUTE MODAL -->
    <transition
      enter-active-class="transition duration-150 ease-out"
      enter-from-class="opacity-0 scale-95"
      enter-to-class="opacity-100 scale-100"
      leave-active-class="transition duration-100 ease-in"
      leave-from-class="opacity-100 scale-100"
      leave-to-class="opacity-0 scale-95"
    >
      <div
        v-if="isModalOpen"
        class="fixed inset-0 z-50 overflow-y-auto bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4"
        @keydown.esc="isModalOpen = false"
      >
        <div class="w-full max-w-md bg-white rounded-2xl border border-slate-200 shadow-2xl overflow-hidden flex flex-col my-6">
          <div class="bg-slate-900 text-white px-5 py-3.5 flex items-center justify-between border-b border-slate-800">
            <div class="flex items-center gap-2">
              <div class="w-7 h-7 rounded bg-[#0072ce] flex items-center justify-center text-white font-bold text-xs">
                RT
              </div>
              <h3 class="text-xs font-bold uppercase tracking-wider text-white">
                {{ form.id ? 'Edit Route' : 'Add Static Route' }}
              </h3>
            </div>
            <button @click="isModalOpen = false" class="text-slate-400 hover:text-white cursor-pointer font-bold text-base">&times;</button>
          </div>

          <form @submit.prevent="saveRoute" class="p-5 space-y-3.5 text-xs text-slate-800">
            <div>
              <div class="flex items-center justify-between mb-1">
                <label class="block font-bold text-slate-700">Destination Subnet (CIDR) *</label>
                <button
                  type="button"
                  @click="openInlineNetModal('destination')"
                  class="text-[10px] text-[#0072ce] hover:underline font-bold cursor-pointer"
                >
                  + New Network Object
                </button>
              </div>
              <div class="space-y-1.5">
                <select
                  v-if="networkDefs.length > 0"
                  @change="e => { if (e.target.value) form.destination = e.target.value }"
                  class="w-full p-2 border border-slate-300 rounded font-mono bg-white text-xs"
                >
                  <option value="">-- Choose from Network Definitions --</option>
                  <option v-for="net in networkDefs" :key="'dst-rt-' + net.id" :value="net.address || net.name">
                    🌐 {{ net.name }} ({{ net.address }})
                  </option>
                </select>
                <input
                  v-model="form.destination"
                  type="text"
                  required
                  placeholder="e.g. 10.200.0.0/16 or 0.0.0.0/0"
                  class="w-full p-2 border border-slate-300 rounded font-mono focus:border-[#0072ce] focus:outline-none"
                />
              </div>
            </div>

            <div>
              <div class="flex items-center justify-between mb-1">
                <label class="block font-bold text-slate-700">Gateway Next-Hop IP *</label>
                <button
                  type="button"
                  @click="openInlineNetModal('gateway')"
                  class="text-[10px] text-[#0072ce] hover:underline font-bold cursor-pointer"
                >
                  + New Gateway Host
                </button>
              </div>
              <div class="space-y-1.5">
                <select
                  v-if="networkDefs.length > 0"
                  @change="e => { if (e.target.value) form.gateway = e.target.value }"
                  class="w-full p-2 border border-slate-300 rounded font-mono bg-white text-xs"
                >
                  <option value="">-- Choose from Host Definitions --</option>
                  <option v-for="net in networkDefs" :key="'gw-rt-' + net.id" :value="net.address || net.name">
                    🖥️ {{ net.name }} ({{ net.address }})
                  </option>
                </select>
                <input
                  v-model="form.gateway"
                  type="text"
                  required
                  placeholder="e.g. 192.168.1.254"
                  class="w-full p-2 border border-slate-300 rounded font-mono focus:border-[#0072ce] focus:outline-none"
                />
              </div>
            </div>

            <div class="grid grid-cols-2 gap-3">
              <div>
                <label class="block font-bold text-slate-700 mb-1">Outbound Interface</label>
                <select v-model="form.interface" class="w-full p-2 border border-slate-300 rounded bg-white font-medium">
                  <option value="Any">Any Interface</option>
                  <option value="ens33 (WAN)">ens33 (WAN)</option>
                  <option value="ens34 (LAN)">ens34 (LAN)</option>
                  <option value="wg0 (VPN)">wg0 (WireGuard)</option>
                </select>
              </div>
              <div>
                <label class="block font-bold text-slate-700 mb-1">Metric / Priority</label>
                <input
                  v-model.number="form.metric"
                  type="number"
                  min="1"
                  max="1000"
                  class="w-full p-2 border border-slate-300 rounded font-mono focus:border-[#0072ce] focus:outline-none"
                />
              </div>
            </div>

            <div>
              <label class="block font-bold text-slate-700 mb-1">Route Type</label>
              <select v-model="form.route_type" class="w-full p-2 border border-slate-300 rounded bg-white font-medium">
                <option value="Static">Static Route</option>
                <option value="Default Gateway">Default Gateway</option>
                <option value="Blackhole / Null">Blackhole (Null Route)</option>
              </select>
            </div>

            <div>
              <label class="block font-bold text-slate-700 mb-1">Comment</label>
              <input
                v-model="form.comment"
                type="text"
                placeholder="e.g. Branch Office datacenter interconnect"
                class="w-full p-2 border border-slate-300 rounded focus:border-[#0072ce] focus:outline-none"
              />
            </div>

            <div class="flex items-center gap-2 pt-1">
              <input
                id="rt-enable"
                v-model="form.enabled"
                type="checkbox"
                class="w-4 h-4 rounded border-slate-300 text-[#0072ce] focus:ring-[#0072ce]"
              />
              <label for="rt-enable" class="font-bold text-slate-700 cursor-pointer">
                Enable Route immediately in kernel table
              </label>
            </div>

            <div class="pt-3 border-t border-slate-200 flex justify-between">
              <button
                type="button"
                @click="isModalOpen = false"
                class="px-3.5 py-1.5 border border-slate-300 rounded text-xs font-semibold text-slate-700 hover:bg-slate-50 cursor-pointer"
              >
                Cancel
              </button>
              <button
                type="submit"
                class="px-4 py-1.5 bg-[#0072ce] hover:bg-blue-700 text-white rounded text-xs font-bold shadow-xs cursor-pointer"
              >
                Save Route
              </button>
            </div>
          </form>
        </div>
      </div>
    </transition>

    <!-- INLINE SUB-MODAL: CREATE NEW NETWORK / HOST OBJECT ON THE FLY -->
    <transition
      enter-active-class="transition duration-150 ease-out"
      enter-from-class="opacity-0 scale-95"
      enter-to-class="opacity-100 scale-100"
      leave-active-class="transition duration-100 ease-in"
      leave-from-class="opacity-100 scale-100"
      leave-to-class="opacity-0 scale-95"
    >
      <div
        v-if="isInlineNetModalOpen"
        class="fixed inset-0 z-[100] bg-slate-950/70 backdrop-blur-xs flex items-center justify-center p-4"
        @keydown.esc="isInlineNetModalOpen = false"
      >
        <div class="w-full max-w-md bg-white rounded-2xl border border-slate-200 shadow-2xl overflow-hidden flex flex-col">
          <div class="bg-slate-900 text-white px-5 py-3.5 flex items-center justify-between border-b border-slate-800">
            <div class="flex items-center gap-2">
              <span class="w-2.5 h-2.5 rounded-full bg-[#ee7f00]"></span>
              <h3 class="text-xs font-bold uppercase tracking-wider text-white">Add Network / Host Definition</h3>
            </div>
            <button @click="isInlineNetModalOpen = false" class="text-slate-400 hover:text-white cursor-pointer font-bold text-base">&times;</button>
          </div>
          <form @submit.prevent="saveInlineNet" class="p-5 space-y-3.5 text-xs text-slate-800">
            <div>
              <label class="block font-bold text-slate-700 mb-1">Name *</label>
              <input type="text" required v-model="newInlineNet.name" placeholder="e.g. Branch Subnet or Next-Hop Gateway" class="w-full p-2 border border-slate-300 rounded font-medium focus:border-[#0072ce] focus:outline-none" />
            </div>
            <div>
              <label class="block font-bold text-slate-700 mb-1">Type</label>
              <select v-model="newInlineNet.type" class="w-full p-2 border border-slate-300 rounded bg-white font-bold text-slate-800">
                <option value="Network">Network (CIDR)</option>
                <option value="Host">Host (Single IP)</option>
                <option value="Range">IP Range</option>
                <option value="DNS host">DNS host (FQDN)</option>
                <option value="Network group">Network group</option>
              </select>
            </div>
            <div>
              <label class="block font-bold text-slate-700 mb-1">IPv4 Address / Subnet *</label>
              <input type="text" required v-model="newInlineNet.address" placeholder="e.g. 10.200.0.0/16 or 192.168.1.254" class="w-full p-2 border border-slate-300 rounded font-mono focus:border-[#0072ce] focus:outline-none" />
            </div>
            <div class="pt-3 border-t border-slate-200 flex justify-between">
              <button type="button" @click="isInlineNetModalOpen = false" class="px-3.5 py-1.5 border border-slate-300 rounded text-slate-700 hover:bg-slate-50 cursor-pointer">Cancel</button>
              <button type="submit" class="px-4 py-1.5 bg-[#0072ce] text-white font-bold rounded shadow-xs cursor-pointer">Save &amp; Use</button>
            </div>
          </form>
        </div>
      </div>
    </transition>

    <!-- MODAL: CREATE POLICY ROUTE (PBR) -->
    <div v-if="isPbrModalOpen" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-xs p-4">
      <div class="bg-white rounded-xl shadow-2xl border border-slate-300 max-w-lg w-full overflow-hidden">
        <div class="px-5 py-3.5 bg-slate-900 text-white flex items-center justify-between border-b-2 border-[#ee7f00]">
          <h3 class="text-sm font-bold uppercase tracking-wider text-white">Create Policy-Based Routing Rule</h3>
          <button @click="isPbrModalOpen = false" class="text-slate-400 hover:text-white font-bold cursor-pointer">✕</button>
        </div>
        <form @submit.prevent="savePbrRoute" class="p-5 space-y-3.5 text-xs">
          <div>
            <label class="block font-bold text-slate-700 mb-1">Rule Name *</label>
            <input v-model="pbrForm.name" type="text" required placeholder="e.g. VoIP SIP Gateway Steering" class="w-full p-2 border border-slate-300 rounded font-medium" />
          </div>
          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block font-bold text-slate-700 mb-1">Source Network</label>
              <input v-model="pbrForm.source" type="text" placeholder="192.168.1.0/24 or Any" class="w-full p-2 border border-slate-300 rounded font-mono" />
            </div>
            <div>
              <label class="block font-bold text-slate-700 mb-1">Destination Network</label>
              <input v-model="pbrForm.destination" type="text" placeholder="0.0.0.0/0 or Any" class="w-full p-2 border border-slate-300 rounded font-mono" />
            </div>
          </div>
          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block font-bold text-slate-700 mb-1">Service / Protocol</label>
              <input v-model="pbrForm.service" type="text" placeholder="UDP 5060, HTTPS, Any" class="w-full p-2 border border-slate-300 rounded font-mono" />
            </div>
            <div>
              <label class="block font-bold text-slate-700 mb-1">Target Gateway / Interface *</label>
              <input v-model="pbrForm.target_gateway" type="text" required placeholder="192.168.1.254 (Fiber WAN)" class="w-full p-2 border border-slate-300 rounded font-mono font-bold" />
            </div>
          </div>
          <div>
            <label class="block font-bold text-slate-700 mb-1">Comment</label>
            <input v-model="pbrForm.comment" type="text" placeholder="Optional notes" class="w-full p-2 border border-slate-300 rounded" />
          </div>
          <div class="pt-3 border-t border-slate-200 flex justify-end gap-2">
            <button type="button" @click="isPbrModalOpen = false" class="px-3.5 py-1.5 border border-slate-300 rounded text-xs font-bold">Cancel</button>
            <button type="submit" class="px-4 py-1.5 bg-[#0072ce] text-white rounded text-xs font-bold">Save Policy Route</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const activeTab = ref('static')
const loading = ref(false)
const routes = ref([])
const networkDefs = ref([])
const isInlineNetModalOpen = ref(false)
const inlineNetTarget = ref('destination')
const newInlineNet = ref({ name: '', type: 'Network', address: '' })

function openInlineNetModal(target = 'destination') {
  inlineNetTarget.value = target
  newInlineNet.value = {
    name: '',
    type: target === 'gateway' ? 'Host' : 'Network',
    address: ''
  }
  isInlineNetModalOpen.value = true
}

async function saveInlineNet() {
  if (!newInlineNet.value.name || !newInlineNet.value.address) return
  try {
    const res = await fetch('/api/definitions/networks', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newInlineNet.value)
    })
    if (res.ok) {
      await fetchRoutes()
    }
  } catch (err) {
    console.error('Failed to create network definition in Routing:', err)
  }

  const selectedVal = newInlineNet.value.address || newInlineNet.value.name
  if (inlineNetTarget.value === 'destination') {
    form.value.destination = selectedVal
  } else if (inlineNetTarget.value === 'gateway') {
    form.value.gateway = selectedVal
  }

  isInlineNetModalOpen.value = false
}

const kernelFIB = ref('')
const isModalOpen = ref(false)

const tabs = [
  { id: 'static', label: 'Static Routes', badge: '' },
  { id: 'pbr', label: 'Policy Routing (PBR)', badge: 'SD-WAN' },
  { id: 'dynamic', label: 'Dynamic Routing (BGP/OSPF)', badge: null },
  { id: 'fib', label: 'Live Kernel FIB Table', badge: 'Live' }
]

const form = ref({
  id: null,
  destination: '',
  gateway: '',
  interface: 'Any',
  metric: 10,
  route_type: 'Static',
  comment: '',
  enabled: true
})

async function fetchRoutes() {
  loading.value = true
  try {
    const [res, fibRes, netRes] = await Promise.all([
      fetch('/api/routing/routes').catch(() => null),
      fetch('/api/routing/status').catch(() => null),
      fetch('/api/definitions/networks').catch(() => null)
    ])
    if (res && res.ok) {
      routes.value = await res.json()
      tabs[0].badge = String(routes.value.length)
    }
    if (fibRes && fibRes.ok) {
      const data = await fibRes.json()
      kernelFIB.value = data.kernel_routes || 'default via 192.168.1.254 dev ens33'
    }
    if (netRes && netRes.ok) {
      networkDefs.value = await netRes.json()
    }
  } catch (err) {
    console.error('Failed to fetch routes:', err)
  } finally {
    loading.value = false
  }
}

function openAddModal() {
  form.value = {
    id: null,
    destination: '',
    gateway: '',
    interface: 'Any',
    metric: 10,
    route_type: 'Static',
    comment: '',
    enabled: true
  }
  isModalOpen.value = true
}

function editRoute(route) {
  form.value = { ...route }
  isModalOpen.value = true
}

async function saveRoute() {
  try {
    const res = await fetch('/api/routing/routes', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form.value)
    })
    if (res.ok) {
      isModalOpen.value = false
      await fetchRoutes()
    }
  } catch (err) {
    console.error('Failed to save route:', err)
  }
}

async function deleteRoute(routeId) {
  if (!confirm(`Are you sure you want to delete route ${routeId}?`)) return
  try {
    const res = await fetch(`/api/routing/routes/${routeId}`, { method: 'DELETE' })
    if (res.ok) {
      await fetchRoutes()
    }
  } catch (err) {
    console.error('Failed to delete route:', err)
  }
}

const pbrRoutes = ref([])
const isPbrModalOpen = ref(false)
const pbrForm = ref({
  name: '',
  source: '',
  destination: '',
  service: '',
  target_gateway: '',
  interface: 'eth0',
  comment: '',
  enabled: true
})

function openAddPbrModal() {
  pbrForm.value = {
    name: '',
    source: '',
    destination: '',
    service: '',
    target_gateway: '',
    interface: 'eth0',
    comment: '',
    enabled: true
  }
  isPbrModalOpen.value = true
}

async function fetchPbrRoutes() {
  try {
    const res = await fetch('/api/routing/policy-routes')
    if (res.ok) {
      pbrRoutes.value = await res.json()
      tabs[1].badge = `${pbrRoutes.value.length} Rules`
    }
  } catch (err) {}
}

async function savePbrRoute() {
  if (!pbrForm.value.name || !pbrForm.value.target_gateway) return
  try {
    const res = await fetch('/api/routing/policy-routes', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(pbrForm.value)
    })
    if (res.ok) {
      isPbrModalOpen.value = false
      await fetchPbrRoutes()
    }
  } catch (err) {
    console.error('Failed to save policy route:', err)
  }
}

async function deletePbrAction(id) {
  if (!confirm('Are you sure you want to delete this policy-based route?')) return
  try {
    const res = await fetch(`/api/routing/policy-routes/${id}`, { method: 'DELETE' })
    if (res.ok) {
      await fetchPbrRoutes()
    }
  } catch (err) {
    console.error('Failed to delete policy route:', err)
  }
}

onMounted(() => {
  fetchRoutes()
  fetchPbrRoutes()
})
</script>
