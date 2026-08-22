<template>
  <div class="space-y-6">
    <!-- Standardized Page Header -->
    <div class="bg-white border border-slate-200 rounded-xl p-5 shadow-xs flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
      <div>
        <div class="flex items-center gap-2.5">
          <span class="w-1.5 h-6 bg-[#ee7f00] rounded-xs inline-block"></span>
          <h1 class="text-xl font-bold text-slate-900 tracking-tight">NAT &amp; Masquerading Rules</h1>
          <span class="text-[11px] bg-blue-50 text-[#0072ce] font-medium font-mono px-2 py-0.5 rounded border border-blue-200">
            NFTables NAT Engine
          </span>
        </div>
        <p class="text-xs text-slate-500 mt-1 pl-4">
          Configure Outbound Masquerading (Source NAT), Inbound Port Forwarding (Destination NAT), and 1:1 Server Mapping.
        </p>
      </div>

      <div class="flex items-center gap-2.5 flex-wrap">
        <button
          type="button"
          @click="fetchNatRules"
          :disabled="isLoading"
          class="px-3.5 py-2 text-xs font-semibold bg-white hover:bg-slate-50 text-slate-700 rounded-lg border border-slate-300 transition-colors flex items-center gap-1.5 shadow-xs cursor-pointer active:bg-slate-100"
          title="Reload NAT rules from kernel datastore"
        >
          <svg :class="['w-3.5 h-3.5 text-slate-500', isLoading ? 'animate-spin text-[#0072ce]' : '']" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          <span>Refresh</span>
        </button>

        <button
          type="button"
          @click="openCreateModal"
          class="px-4 py-2 bg-[#0072ce] hover:bg-blue-700 text-white rounded-lg text-xs font-bold shadow-sm flex items-center gap-2 transition-all cursor-pointer"
        >
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          <span>+ New NAT Rule...</span>
        </button>
      </div>
    </div>

    <!-- Standardized Flat Tab Navigation Strip (UTM 9 Style) -->
    <div class="flex border-b border-slate-200 gap-1 bg-[#f4f6f9] p-1.5 rounded-t-xl overflow-x-auto text-xs font-bold">
      <button
        v-for="tab in tabs"
        :key="tab.id"
        type="button"
        @click="activeTab = tab.id"
        :class="[
          'px-4 py-2 rounded-lg transition-all flex items-center gap-2 cursor-pointer whitespace-nowrap',
          activeTab === tab.id
            ? 'bg-white text-slate-900 shadow-xs border-b-2 border-[#ee7f00]'
            : 'text-slate-600 hover:text-slate-900 hover:bg-white/60'
        ]"
      >
        <span>{{ tab.label }}</span>
        <span
          class="px-1.5 py-0.2 rounded-full text-[10px] font-mono"
          :class="activeTab === tab.id ? 'bg-[#0072ce] text-white' : 'bg-slate-200 text-slate-700'"
        >
          {{ tab.count }}
        </span>
      </button>
    </div>

    <!-- Standardized Search & Filter Toolbar -->
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 bg-white p-3.5 rounded-xl border border-slate-200 shadow-xs text-xs">
      <div class="flex items-center gap-2 w-full sm:w-80">
        <div class="relative w-full">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search NAT rules, sources, targets, ports..."
            class="w-full pl-8 pr-3 py-1.5 bg-slate-50 border border-slate-200 rounded-lg text-xs focus:bg-white focus:border-[#0072ce] focus:outline-none"
          />
          <svg class="w-4 h-4 text-slate-400 absolute left-2.5 top-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </div>
      </div>

      <div class="flex items-center gap-4 text-slate-500 font-medium">
        <div class="flex items-center gap-2">
          <span>Sort by:</span>
          <select v-model="sortBy" class="bg-slate-50 border border-slate-200 rounded-lg px-2 py-1 text-xs text-slate-700 font-bold">
            <option value="name_asc">Name asc</option>
            <option value="name_desc">Name desc</option>
            <option value="type">Type</option>
            <option value="status">Status</option>
          </select>
        </div>

        <span class="font-mono text-slate-600 font-bold">
          Showing {{ filteredRules.length }} of {{ natRules.length }} rules
        </span>
      </div>
    </div>

    <!-- NAT Rules Table -->
    <div class="bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden">
      <div v-if="filteredRules.length === 0" class="p-12 text-center text-slate-400 text-xs">
        No NAT rules found matching your filter criteria. Click "+ New NAT Rule..." to create one.
      </div>
      <table v-else class="w-full text-left text-xs border-collapse">
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
        <tbody class="divide-y divide-slate-100 font-medium text-slate-700">
          <tr
            v-for="(rule, idx) in filteredRules"
            :key="rule.id"
            :class="idx % 2 === 0 ? 'bg-white' : 'bg-[#f7f7f7]'"
            class="hover:bg-blue-50/40 transition-colors"
          >
            <!-- Status Toggle -->
            <td class="p-3 pl-4 text-center">
              <button
                type="button"
                @click="toggleRule(rule)"
                class="relative inline-flex h-4 w-8 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none"
                :class="rule.enabled ? 'bg-emerald-500' : 'bg-slate-300'"
                title="Toggle NAT Rule status"
              >
                <span
                  class="pointer-events-none inline-block h-3 w-3 transform rounded-full bg-white shadow-xs ring-0 transition duration-200 ease-in-out"
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
                    ? 'bg-blue-50 text-[#0072ce] border-blue-200'
                    : rule.type === '1:1 NAT'
                    ? 'bg-purple-50 text-purple-700 border-purple-200'
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
                &rarr; {{ rule.outbound_interface || 'Uplink Interfaces (WAN)' }}
              </div>
              <div v-else class="text-emerald-700 font-bold">
                &rarr; {{ rule.destination_nat_target || '192.168.1.100' }}<span v-if="rule.service_translation">:{{ rule.service_translation }}</span>
              </div>
            </td>

            <td class="p-3 text-slate-500 text-[11px] truncate max-w-xs">
              {{ rule.comment || '—' }}
            </td>

            <!-- Standardized Action Triplet: Edit | Clone | Delete -->
            <td class="p-3 text-right pr-4 space-x-1.5 whitespace-nowrap">
              <button
                type="button"
                @click="editRule(rule)"
                class="px-2 py-1 bg-white hover:bg-slate-50 text-slate-700 border border-slate-300 rounded text-[11px] font-bold shadow-2xs cursor-pointer"
              >
                Edit
              </button>
              <button
                type="button"
                @click="cloneRule(rule)"
                class="px-2 py-1 bg-white hover:bg-slate-50 text-amber-700 border border-slate-300 rounded text-[11px] font-bold shadow-2xs cursor-pointer"
              >
                Clone
              </button>
              <button
                type="button"
                @click="deleteRule(rule.id)"
                class="px-2 py-1 bg-white hover:bg-rose-50 text-rose-600 border border-rose-200 rounded text-[11px] font-bold shadow-2xs cursor-pointer"
              >
                Delete
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- CREATE / EDIT NAT RULE COMPACT MODAL -->
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
        class="fixed inset-0 z-40 overflow-y-auto bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4"
        @keydown.esc="isModalOpen = false"
      >
        <div class="bg-white rounded-2xl shadow-2xl border border-slate-200 max-w-lg w-full overflow-hidden flex flex-col my-6 max-h-[90vh]">
          <!-- Modal Header -->
          <div class="px-5 py-3.5 bg-slate-900 text-white flex items-center justify-between border-b border-slate-800">
            <div class="flex items-center gap-2.5">
              <div class="w-8 h-8 rounded-lg bg-[#ee7f00] flex items-center justify-center text-white font-bold text-xs shadow-md">
                NAT
              </div>
              <div>
                <h3 class="text-xs font-bold uppercase tracking-wider text-white">
                  {{ editingId ? 'Edit NAT Rule' : 'Create New NAT Rule' }}
                </h3>
                <p class="text-[10px] text-slate-400">Configure address and port translation</p>
              </div>
            </div>
            <button @click="isModalOpen = false" class="text-slate-400 hover:text-white font-bold cursor-pointer text-base leading-none">&times;</button>
          </div>

          <!-- Form Fields -->
          <form @submit.prevent="saveRule" class="p-5 space-y-4 text-xs flex-1 overflow-y-auto">
            <div>
              <label class="block font-bold text-slate-700 mb-1">Rule Name *</label>
              <input
                v-model="formRule.name"
                type="text"
                required
                placeholder="e.g. Masquerade LAN to WAN, Forward Web Port 443"
                class="w-full p-2 border border-slate-300 rounded focus:border-[#0072ce] focus:outline-none"
              />
            </div>

            <div class="grid grid-cols-2 gap-3">
              <div>
                <label class="block font-bold text-slate-700 mb-1">Rule Type</label>
                <select
                  v-model="formRule.type"
                  class="w-full p-2 border border-slate-300 rounded focus:border-[#0072ce] focus:outline-none bg-white font-medium"
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
                  v-model="formRule.enabled"
                  class="w-full p-2 border border-slate-300 rounded focus:border-[#0072ce] focus:outline-none bg-white font-medium"
                >
                  <option :value="true">Enabled (Active)</option>
                  <option :value="false">Disabled</option>
                </select>
              </div>
            </div>

            <!-- Masquerading specific -->
            <div v-if="formRule.type === 'Masquerading'" class="space-y-3 p-3 bg-[#f4f6f9] rounded-lg border border-slate-200">
              <div>
                <div class="flex items-center justify-between mb-1">
                  <label class="block font-bold text-slate-700">Source Network / Group</label>
                  <button
                    type="button"
                    @click="openInlineNetModal"
                    class="text-[11px] font-bold text-[#0072ce] hover:underline flex items-center gap-1 cursor-pointer"
                  >
                    <span>+ Add Network Definition</span>
                  </button>
                </div>
                <select
                  v-model="formRule.source_network"
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
                  v-model="formRule.outbound_interface"
                  class="w-full p-2 border border-slate-300 rounded bg-white font-medium"
                >
                  <option value="Uplink Interfaces (WAN)">Uplink Interfaces (WAN / External)</option>
                  <option value="ens33">ens33 (WAN)</option>
                  <option value="eth0">eth0 (WAN)</option>
                </select>
              </div>
            </div>

            <!-- DNAT / SNAT / 1:1 NAT specific -->
            <div v-else class="space-y-3 p-3.5 bg-amber-50/40 rounded-xl border border-amber-200">
              <!-- Traffic Source -->
              <div>
                <div class="flex items-center justify-between mb-1">
                  <label class="block font-bold text-slate-700">Traffic Source</label>
                  <button
                    type="button"
                    @click="openInlineNetModal('traffic_source')"
                    class="text-[10px] font-bold text-[#0072ce] hover:underline cursor-pointer"
                  >
                    + Add Network Definition
                  </button>
                </div>
                <select
                  v-model="formRule.traffic_source"
                  class="w-full p-2 border border-slate-300 rounded-lg bg-white font-mono text-xs"
                >
                  <option value="Any">Any (Internet / 0.0.0.0/0)</option>
                  <option value="Internet IPv4">Internet IPv4</option>
                  <option v-for="net in networkDefs" :key="'src-' + net.id" :value="net.name">
                    {{ net.name }} ({{ net.address }})
                  </option>
                </select>
              </div>

              <!-- Service & Original Destination Grid -->
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <div>
                  <div class="flex items-center justify-between mb-1">
                    <label class="block font-bold text-slate-700">Incoming Traffic Service</label>
                    <button
                      type="button"
                      @click="openInlineSrvModal('traffic_service')"
                      class="text-[10px] font-bold text-[#0072ce] hover:underline cursor-pointer"
                    >
                      + New Service
                    </button>
                  </div>
                  <select
                    v-model="formRule.traffic_service"
                    class="w-full p-2 border border-slate-300 rounded-lg bg-white font-medium text-xs"
                  >
                    <option value="Any">Any Service</option>
                    <option v-for="srv in serviceDefs" :key="'srv-' + srv.id" :value="srv.name">
                      {{ srv.name }} ({{ srv.protocol }}:{{ srv.dst_port }})
                    </option>
                    <option value="HTTPS">HTTPS (TCP:443)</option>
                    <option value="HTTP">HTTP (TCP:80)</option>
                    <option value="SSH">SSH (TCP:22)</option>
                    <option value="RDP">RDP (TCP:3389)</option>
                    <option value="OpenVPN">OpenVPN (UDP:1194)</option>
                  </select>
                </div>

                <div>
                  <div class="flex items-center justify-between mb-1">
                    <label class="block font-bold text-slate-700">Original Destination</label>
                    <button
                      type="button"
                      @click="openInlineNetModal('traffic_destination')"
                      class="text-[10px] font-bold text-[#0072ce] hover:underline cursor-pointer"
                    >
                      + Add Object
                    </button>
                  </div>
                  <select
                    v-model="formRule.traffic_destination"
                    class="w-full p-2 border border-slate-300 rounded-lg bg-white font-mono text-xs"
                  >
                    <option value="Uplink (WAN IP)">Uplink Interfaces (WAN IP)</option>
                    <option value="External (WAN) (Address)">External (WAN) (Address)</option>
                    <option v-for="net in networkDefs" :key="'dst-' + net.id" :value="net.name">
                      {{ net.name }} ({{ net.address }})
                    </option>
                  </select>
                </div>
              </div>

              <!-- Target Host & Service Translation Grid -->
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <div>
                  <div class="flex items-center justify-between mb-1">
                    <label class="block font-bold text-slate-700">Destination NAT Target Host *</label>
                    <button
                      type="button"
                      @click="openInlineNetModal('destination_nat_target')"
                      class="text-[10px] font-bold text-[#0072ce] hover:underline cursor-pointer"
                    >
                      + Add Host
                    </button>
                  </div>
                  <select
                    v-model="formRule.destination_nat_target"
                    required
                    class="w-full p-2 border border-slate-300 rounded-lg font-mono bg-white text-xs"
                  >
                    <option v-for="net in networkDefs" :key="'tgt-' + net.id" :value="net.address || net.name">
                      {{ net.name }} ({{ net.address }})
                    </option>
                    <option value="192.168.1.100">192.168.1.100</option>
                    <option value="192.168.1.50">192.168.1.50</option>
                  </select>
                </div>

                <div>
                  <div class="flex items-center justify-between mb-1">
                    <label class="block font-bold text-slate-700">Translated Port / Service</label>
                    <button
                      type="button"
                      @click="openInlineSrvModal('service_translation')"
                      class="text-[10px] font-bold text-[#0072ce] hover:underline cursor-pointer"
                    >
                      + New Service
                    </button>
                  </div>
                  <input
                    v-model="formRule.service_translation"
                    type="text"
                    placeholder="e.g. 443, 8080 (blank = keep original)"
                    class="w-full p-2 border border-slate-300 rounded-lg font-mono bg-white text-xs focus:border-[#0072ce] focus:outline-none"
                  />
                </div>
              </div>

              <div class="flex items-center gap-2 pt-1">
                <input
                  id="auto-fw"
                  v-model="formRule.auto_firewall_rule"
                  type="checkbox"
                  class="w-4 h-4 rounded border-slate-300 text-[#0072ce] focus:ring-[#0072ce]"
                />
                <label for="auto-fw" class="text-slate-700 font-bold cursor-pointer">
                  Automatic Firewall rule (Permit translated traffic)
                </label>
              </div>
            </div>

            <div>
              <label class="block font-bold text-slate-700 mb-1">Comment</label>
              <input
                v-model="formRule.comment"
                type="text"
                placeholder="Optional notes or documentation"
                class="w-full p-2 border border-slate-300 rounded focus:border-[#0072ce] focus:outline-none"
              />
            </div>

            <!-- Modal Footer -->
            <div class="pt-3 border-t border-slate-200 flex items-center justify-between">
              <button
                type="button"
                @click="isModalOpen = false"
                class="px-3.5 py-1.5 rounded border border-slate-300 bg-white text-slate-700 text-xs font-bold hover:bg-slate-50 cursor-pointer"
              >
                Cancel
              </button>
              <button
                type="submit"
                class="px-4 py-1.5 rounded bg-[#0072ce] hover:bg-blue-700 text-white text-xs font-bold shadow-xs cursor-pointer"
              >
                {{ editingId ? 'Update Rule' : 'Save Rule' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </transition>

    <!-- INLINE NETWORK OBJECT / GROUP MODAL (Z-[100]) -->
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
        <div class="w-full max-w-md bg-white rounded-2xl border border-slate-200 shadow-2xl overflow-hidden">
          <div class="bg-slate-900 text-white px-4 py-3 flex items-center justify-between border-b border-slate-800">
            <h3 class="text-xs font-bold uppercase tracking-wider text-white">Add Network Definition / Group</h3>
            <button @click="isInlineNetModalOpen = false" class="text-slate-400 hover:text-white cursor-pointer font-bold">&times;</button>
          </div>
          <form @submit.prevent="saveInlineNet" class="p-4 space-y-3 text-xs">
            <div>
              <label class="block font-bold text-slate-700 mb-1">Name *</label>
              <input type="text" required v-model="newInlineNet.name" placeholder="e.g. DMZ Servers" class="w-full p-2 border border-slate-300 rounded" />
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
              <input type="text" required v-model="newInlineNet.address" placeholder="192.168.1.50 or 10.0.0.0/24" class="w-full p-2 border border-slate-300 rounded font-mono" />
            </div>
            <div class="pt-2 border-t border-slate-200 flex justify-between">
              <button type="button" @click="isInlineNetModalOpen = false" class="px-3 py-1 text-xs border rounded text-slate-700 cursor-pointer">Cancel</button>
              <button type="submit" class="px-4 py-1 text-xs font-bold bg-[#0072ce] text-white rounded shadow-xs cursor-pointer">Save &amp; Use</button>
            </div>
          </form>
        </div>
      </div>
    </transition>

    <!-- INLINE SERVICE DEFINITION MODAL (Z-[100]) -->
    <transition
      enter-active-class="transition duration-150 ease-out"
      enter-from-class="opacity-0 scale-95"
      enter-to-class="opacity-100 scale-100"
      leave-active-class="transition duration-100 ease-in"
      leave-from-class="opacity-100 scale-100"
      leave-to-class="opacity-0 scale-95"
    >
      <div
        v-if="isInlineSrvModalOpen"
        class="fixed inset-0 z-[100] bg-slate-950/70 backdrop-blur-xs flex items-center justify-center p-4"
        @keydown.esc="isInlineSrvModalOpen = false"
      >
        <div class="w-full max-w-md bg-white rounded-2xl border border-slate-200 shadow-2xl overflow-hidden">
          <div class="bg-slate-900 text-white px-4 py-3 flex items-center justify-between border-b border-slate-800">
            <h3 class="text-xs font-bold uppercase tracking-wider text-white">New Service Definition / Group</h3>
            <button @click="isInlineSrvModalOpen = false" class="text-slate-400 hover:text-white cursor-pointer font-bold">&times;</button>
          </div>
          <form @submit.prevent="saveInlineSrv" class="p-4 space-y-3 text-xs">
            <div>
              <label class="block font-bold text-slate-700 mb-1">Service Name *</label>
              <input type="text" required v-model="newInlineSrv.name" placeholder="e.g. Minecraft Server" class="w-full p-2 border border-slate-300 rounded" />
            </div>
            <div>
              <label class="block font-bold text-slate-700 mb-1">Protocol / Type</label>
              <select v-model="newInlineSrv.type" class="w-full p-2 border border-slate-300 rounded bg-white font-medium">
                <option value="TCP">TCP</option>
                <option value="UDP">UDP</option>
                <option value="TCP/UDP">TCP/UDP</option>
                <option value="Service Group">Service Group</option>
              </select>
            </div>
            <div>
              <label class="block font-bold text-slate-700 mb-1">Destination Port *</label>
              <input type="text" required v-model="newInlineSrv.dst_port" placeholder="e.g. 25565 or 8080:8090" class="w-full p-2 border border-slate-300 rounded font-mono" />
            </div>
            <div class="pt-2 border-t border-slate-200 flex justify-between">
              <button type="button" @click="isInlineSrvModalOpen = false" class="px-3 py-1 text-xs border rounded text-slate-700 cursor-pointer">Cancel</button>
              <button type="submit" class="px-4 py-1 text-xs font-bold bg-[#0072ce] text-white rounded shadow-xs cursor-pointer">Save &amp; Use</button>
            </div>
          </form>
        </div>
      </div>
    </transition>
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

const activeTab = ref('all') // 'all' | 'masquerading' | 'dnat' | 'onenat'
const searchQuery = ref('')
const sortBy = ref('name_asc')
const isLoading = ref(false)
const isModalOpen = ref(false)
const isInlineNetModalOpen = ref(false)
const isInlineSrvModalOpen = ref(false)
const editingId = ref(null)

const newInlineNet = ref({ name: '', type: 'Host', address: '' })
const newInlineSrv = ref({ name: '', type: 'TCP', dst_port: '' })

const natRules = ref([])
const networkDefs = ref([])
const serviceDefs = ref([])

const formRule = ref({
  id: null,
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

const tabs = computed(() => [
  { id: 'all', label: 'All Rules', count: natRules.value.length },
  { id: 'masquerading', label: 'Masquerading (SNAT)', count: natRules.value.filter(r => r.type === 'Masquerading' || r.type === 'SNAT').length },
  { id: 'dnat', label: 'DNAT (Port Forwarding)', count: natRules.value.filter(r => r.type === 'DNAT').length },
  { id: 'onenat', label: '1:1 NAT', count: natRules.value.filter(r => r.type === '1:1 NAT').length }
])

const filteredRules = computed(() => {
  let list = [...natRules.value]

  // Tab filter
  if (activeTab.value === 'masquerading') {
    list = list.filter(r => r.type === 'Masquerading' || r.type === 'SNAT')
  } else if (activeTab.value === 'dnat') {
    list = list.filter(r => r.type === 'DNAT')
  } else if (activeTab.value === 'onenat') {
    list = list.filter(r => r.type === '1:1 NAT')
  }

  // Search filter
  if (searchQuery.value.trim()) {
    const q = searchQuery.value.toLowerCase()
    list = list.filter(r =>
      (r.name && r.name.toLowerCase().includes(q)) ||
      (r.source_network && r.source_network.toLowerCase().includes(q)) ||
      (r.destination_nat_target && r.destination_nat_target.toLowerCase().includes(q)) ||
      (r.traffic_service && r.traffic_service.toLowerCase().includes(q)) ||
      (r.comment && r.comment.toLowerCase().includes(q))
    )
  }

  // Sorting
  if (sortBy.value === 'name_asc') list.sort((a, b) => (a.name || '').localeCompare(b.name || ''))
  else if (sortBy.value === 'name_desc') list.sort((a, b) => (b.name || '').localeCompare(a.name || ''))
  else if (sortBy.value === 'type') list.sort((a, b) => (a.type || '').localeCompare(b.type || ''))
  else if (sortBy.value === 'status') list.sort((a, b) => (b.enabled ? 1 : 0) - (a.enabled ? 1 : 0))

  return list
})

const inlineNetTarget = ref('source_network')
const inlineSrvTarget = ref('traffic_service')

const openInlineNetModal = (target = 'source_network') => {
  inlineNetTarget.value = target
  newInlineNet.value = { name: '', type: 'Host', address: '' }
  isInlineNetModalOpen.value = true
}

const openInlineSrvModal = (target = 'traffic_service') => {
  inlineSrvTarget.value = target
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

  // Assign newly created object to target field
  if (inlineNetTarget.value === 'destination_nat_target') {
    formRule.value.destination_nat_target = newInlineNet.value.address || newInlineNet.value.name
  } else if (inlineNetTarget.value === 'traffic_source') {
    formRule.value.traffic_source = newInlineNet.value.name
  } else if (inlineNetTarget.value === 'traffic_destination') {
    formRule.value.traffic_destination = newInlineNet.value.name
  } else {
    formRule.value.source_network = newInlineNet.value.name
  }

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

  if (inlineSrvTarget.value === 'service_translation') {
    formRule.value.service_translation = newInlineSrv.value.dst_port || newInlineSrv.value.name
  } else {
    formRule.value.traffic_service = newInlineSrv.value.name
  }

  isInlineSrvModalOpen.value = false
}

const fetchNatRules = async () => {
  isLoading.value = true
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
  } finally {
    isLoading.value = false
  }
}

const openCreateModal = () => {
  editingId.value = null
  formRule.value = {
    id: null,
    name: '',
    type: activeTab.value === 'dnat' ? 'DNAT' : (activeTab.value === 'onenat' ? '1:1 NAT' : 'Masquerading'),
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

const editRule = (rule) => {
  editingId.value = rule.id
  formRule.value = JSON.parse(JSON.stringify(rule))
  isModalOpen.value = true
}

const cloneRule = (rule) => {
  editingId.value = null
  formRule.value = {
    ...JSON.parse(JSON.stringify(rule)),
    id: null,
    name: `${rule.name} (Clone)`
  }
  isModalOpen.value = true
}

const saveRule = async () => {
  const axiosLib = (typeof window !== 'undefined' && window.axios) ? window.axios : null
  if (!axiosLib) return

  try {
    const payload = {
      ...formRule.value,
      id: editingId.value || formRule.value.id
    }
    await axiosLib.post('/api/nat/rules', payload)
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
  const item = natRules.value.find(r => r.id === id)
  if (!confirm(`Are you sure you want to delete NAT rule '${item ? item.name : id}'?`)) return

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
