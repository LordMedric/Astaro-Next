<template>
  <div class="space-y-6">
    <!-- Standardized Page Header -->
    <div class="bg-white border border-slate-200 rounded-xl p-5 shadow-xs flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
      <div>
        <div class="flex items-center gap-2.5">
          <span class="w-1.5 h-6 bg-[#ee7f00] rounded-xs inline-block"></span>
          <h1 class="text-xl font-bold text-slate-900 tracking-tight">Definitions &amp; Objects</h1>
          <span class="text-[11px] bg-blue-50 text-[#0072ce] font-medium font-mono px-2 py-0.5 rounded border border-blue-200">
            UTM Object Store
          </span>
        </div>
        <p class="text-xs text-slate-500 mt-1 pl-4">
          Manage reusable Hosts, Networks, Ranges, DNS Hosts, Network Groups, and Service Groups across all firewall, WAF, and NAT policies.
        </p>
      </div>

      <div class="flex items-center gap-2.5 flex-wrap">
        <button
          type="button"
          @click="fetchDefinitions"
          :disabled="isLoading"
          class="px-3.5 py-2 text-xs font-semibold bg-white hover:bg-slate-50 text-slate-700 rounded-lg border border-slate-300 transition-colors flex items-center gap-1.5 shadow-xs cursor-pointer active:bg-slate-100"
          title="Reload definitions from database"
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
          <span>+ New {{ activeTab === 'networks' ? 'Network Definition' : (activeTab === 'services' ? 'Service Definition' : 'Time Period') }}...</span>
        </button>
      </div>
    </div>

    <!-- Standardized Flat Tab Navigation Strip (UTM 9 Style) -->
    <div class="flex border-b border-slate-200 gap-1 bg-[#f4f6f9] p-1.5 rounded-t-xl overflow-x-auto text-xs font-bold">
      <button
        type="button"
        @click="activeTab = 'networks'"
        :class="[
          'px-4 py-2 rounded-lg transition-all flex items-center gap-2 cursor-pointer whitespace-nowrap',
          activeTab === 'networks'
            ? 'bg-white text-slate-900 shadow-xs border-b-2 border-[#ee7f00]'
            : 'text-slate-600 hover:text-slate-900 hover:bg-white/60'
        ]"
      >
        <svg class="w-4 h-4 text-[#0072ce]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
        </svg>
        <span>Network Definitions &amp; Groups</span>
        <span
          class="px-1.5 py-0.2 rounded-full text-[10px] font-mono"
          :class="activeTab === 'networks' ? 'bg-[#0072ce] text-white' : 'bg-slate-200 text-slate-700'"
        >
          {{ networkObjects.length }}
        </span>
      </button>

      <button
        type="button"
        @click="activeTab = 'services'"
        :class="[
          'px-4 py-2 rounded-lg transition-all flex items-center gap-2 cursor-pointer whitespace-nowrap',
          activeTab === 'services'
            ? 'bg-white text-slate-900 shadow-xs border-b-2 border-[#ee7f00]'
            : 'text-slate-600 hover:text-slate-900 hover:bg-white/60'
        ]"
      >
        <svg class="w-4 h-4 text-[#ee7f00]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
        </svg>
        <span>Service Definitions &amp; Groups</span>
        <span
          class="px-1.5 py-0.2 rounded-full text-[10px] font-mono"
          :class="activeTab === 'services' ? 'bg-[#0072ce] text-white' : 'bg-slate-200 text-slate-700'"
        >
          {{ serviceObjects.length }}
        </span>
      </button>

      <button
        type="button"
        @click="activeTab = 'times'"
        :class="[
          'px-4 py-2 rounded-lg transition-all flex items-center gap-2 cursor-pointer whitespace-nowrap',
          activeTab === 'times'
            ? 'bg-white text-slate-900 shadow-xs border-b-2 border-[#ee7f00]'
            : 'text-slate-600 hover:text-slate-900 hover:bg-white/60'
        ]"
      >
        <svg class="w-4 h-4 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <span>Time Periods &amp; Schedules</span>
        <span
          class="px-1.5 py-0.2 rounded-full text-[10px] font-mono"
          :class="activeTab === 'times' ? 'bg-[#0072ce] text-white' : 'bg-slate-200 text-slate-700'"
        >
          {{ timeObjects.length }}
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
            :placeholder="activeTab === 'networks' ? 'Search network objects, IPs, groups...' : 'Search services, ports, groups...'"
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
            <option value="type">Type / Protocol</option>
          </select>
        </div>

        <span class="font-mono text-slate-600 font-bold">
          Showing {{ filteredItemsCount }} objects
        </span>
      </div>
    </div>

    <!-- TAB 1: NETWORK DEFINITIONS TABLE -->
    <div v-if="activeTab === 'networks'" class="bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden">
      <div v-if="filteredNetworkObjects.length === 0" class="p-12 text-center text-slate-400 text-xs">
        No network objects match your search criteria. Click "+ New Network Definition..." to create one.
      </div>
      <table v-else class="w-full text-left text-xs border-collapse">
        <thead class="bg-[#f4f6f9] text-slate-700 font-bold border-b border-slate-200">
          <tr>
            <th class="p-3 pl-4">Name</th>
            <th class="p-3">Type</th>
            <th class="p-3 font-mono">IPv4 Address / Group Members</th>
            <th class="p-3">Interface Binding</th>
            <th class="p-3">Comment</th>
            <th class="p-3 text-right pr-4">Actions</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-100 font-medium text-slate-700">
          <tr
            v-for="(net, idx) in filteredNetworkObjects"
            :key="net.id"
            :class="idx % 2 === 0 ? 'bg-white' : 'bg-[#f7f7f7]'"
            class="hover:bg-blue-50/40 transition-colors"
          >
            <td class="p-3 pl-4 font-bold text-slate-900 flex items-center gap-2">
              <span class="w-2 h-2 rounded-full" :class="net.type === 'Network group' || net.type === 'Network Group' ? 'bg-purple-600' : 'bg-[#0072ce]'"></span>
              {{ net.name }}
            </td>

            <td class="p-3">
              <span
                :class="[
                  'px-2 py-0.5 rounded text-[10px] font-bold uppercase border',
                  net.type === 'Network group' || net.type === 'Network Group'
                    ? 'bg-purple-50 text-purple-700 border-purple-200 font-black'
                    : 'bg-blue-50 text-[#0072ce] border-blue-200'
                ]"
              >
                {{ net.type }}
              </span>
            </td>

            <!-- Address / Group Members rendering -->
            <td class="p-3 font-mono">
              <div v-if="net.type === 'Network group' || net.type === 'Network Group'" class="flex items-center gap-1.5 flex-wrap">
                <span
                  v-for="(member, mIdx) in getGroupMembers(net)"
                  :key="mIdx"
                  class="px-2 py-0.5 rounded text-[10px] font-bold bg-purple-100 text-purple-800 border border-purple-200"
                >
                  {{ member }}
                </span>
                <span v-if="!getGroupMembers(net).length" class="text-slate-600 font-semibold">{{ net.address }}</span>
              </div>
              <div v-else class="text-slate-800 font-semibold">
                {{ net.address }}
              </div>
            </td>

            <td class="p-3 text-slate-600">
              <span class="px-2 py-0.5 rounded text-[10px] font-semibold bg-slate-100 text-slate-700">
                {{ net.interface || 'Any' }}
              </span>
            </td>

            <td class="p-3 text-slate-500 text-[11px] truncate max-w-xs">
              {{ net.comment || '—' }}
            </td>

            <!-- Standard Action Triplet: Edit | Clone | Delete -->
            <td class="p-3 text-right pr-4 space-x-1.5 whitespace-nowrap">
              <button
                type="button"
                @click="editNetObject(net)"
                class="px-2 py-1 bg-white hover:bg-slate-50 text-slate-700 border border-slate-300 rounded text-[11px] font-bold shadow-2xs cursor-pointer"
              >
                Edit
              </button>
              <button
                type="button"
                @click="cloneNetObject(net)"
                class="px-2 py-1 bg-white hover:bg-slate-50 text-amber-700 border border-slate-300 rounded text-[11px] font-bold shadow-2xs cursor-pointer"
              >
                Clone
              </button>
              <button
                type="button"
                @click="deleteNetworkObject(net.id)"
                class="px-2 py-1 bg-white hover:bg-rose-50 text-rose-600 border border-rose-200 rounded text-[11px] font-bold shadow-2xs cursor-pointer"
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
      <div v-if="filteredServiceObjects.length === 0" class="p-12 text-center text-slate-400 text-xs">
        No service objects match your search criteria. Click "+ New Service Definition..." to create one.
      </div>
      <table v-else class="w-full text-left text-xs border-collapse">
        <thead class="bg-[#f4f6f9] text-slate-700 font-bold border-b border-slate-200">
          <tr>
            <th class="p-3 pl-4">Service Name</th>
            <th class="p-3">Protocol / Type</th>
            <th class="p-3 font-mono">Destination Port / Members</th>
            <th class="p-3 font-mono">Source Port</th>
            <th class="p-3">Comment</th>
            <th class="p-3 text-right pr-4">Actions</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-100 font-medium text-slate-700">
          <tr
            v-for="(srv, idx) in filteredServiceObjects"
            :key="srv.id"
            :class="idx % 2 === 0 ? 'bg-white' : 'bg-[#f7f7f7]'"
            class="hover:bg-blue-50/40 transition-colors"
          >
            <td class="p-3 pl-4 font-bold text-slate-900 flex items-center gap-2">
              <span class="w-2 h-2 rounded-full" :class="srv.protocol === 'Group' || srv.type === 'Service Group' ? 'bg-purple-600' : 'bg-[#ee7f00]'"></span>
              {{ srv.name }}
            </td>

            <td class="p-3">
              <span
                :class="[
                  'px-2 py-0.5 rounded text-[10px] font-bold uppercase border',
                  srv.protocol === 'Group' || srv.type === 'Service Group'
                    ? 'bg-purple-50 text-purple-700 border-purple-200 font-black'
                    : 'bg-amber-50 text-amber-800 border-amber-200'
                ]"
              >
                {{ srv.protocol === 'Group' || srv.type === 'Service Group' ? 'SERVICE GROUP' : srv.protocol }}
              </span>
            </td>

            <td class="p-3 font-mono font-bold text-slate-900">
              <div v-if="srv.protocol === 'Group' || srv.type === 'Service Group'" class="flex items-center gap-1.5 flex-wrap">
                <span
                  v-for="(member, mIdx) in getServiceGroupMembers(srv)"
                  :key="mIdx"
                  class="px-2 py-0.5 rounded text-[10px] font-bold bg-amber-100 text-amber-900 border border-amber-200"
                >
                  {{ member }}
                </span>
                <span v-if="!getServiceGroupMembers(srv).length" class="text-slate-700">{{ srv.dst_port }}</span>
              </div>
              <div v-else>
                {{ srv.dst_port }}
              </div>
            </td>

            <td class="p-3 font-mono text-slate-500">
              {{ srv.src_port || '1:65535' }}
            </td>

            <td class="p-3 text-slate-500 text-[11px] truncate max-w-xs">
              {{ srv.comment || '—' }}
            </td>

            <!-- Standard Action Triplet: Edit | Clone | Delete -->
            <td class="p-3 text-right pr-4 space-x-1.5 whitespace-nowrap">
              <button
                type="button"
                @click="editSrvObject(srv)"
                class="px-2 py-1 bg-white hover:bg-slate-50 text-slate-700 border border-slate-300 rounded text-[11px] font-bold shadow-2xs cursor-pointer"
              >
                Edit
              </button>
              <button
                type="button"
                @click="cloneSrvObject(srv)"
                class="px-2 py-1 bg-white hover:bg-slate-50 text-amber-700 border border-slate-300 rounded text-[11px] font-bold shadow-2xs cursor-pointer"
              >
                Clone
              </button>
              <button
                type="button"
                @click="deleteServiceObject(srv.id)"
                class="px-2 py-1 bg-white hover:bg-rose-50 text-rose-600 border border-rose-200 rounded text-[11px] font-bold shadow-2xs cursor-pointer"
              >
                Delete
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- TIME PERIOD DEFINITIONS TABLE (Sophos UTM 9 Parity) -->
    <div v-if="activeTab === 'times'" class="bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden">
      <table class="w-full text-left text-xs border-collapse">
        <thead class="bg-slate-50 text-slate-700 border-b border-slate-200 font-semibold">
          <tr>
            <th class="p-3 w-8">#</th>
            <th class="p-3">Name</th>
            <th class="p-3">Schedule Type</th>
            <th class="p-3">Active Days / Date Range</th>
            <th class="p-3">Time Window</th>
            <th class="p-3">Comment</th>
            <th class="p-3 text-right">Actions</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-100 font-normal text-slate-800">
          <tr v-for="(time, idx) in filteredTimeObjects" :key="time.id" class="hover:bg-slate-50 transition-colors">
            <td class="p-3 text-slate-400 font-mono">{{ idx + 1 }}</td>
            <td class="p-3">
              <div class="font-bold text-slate-900 flex items-center gap-2">
                <span class="w-2 h-2 rounded-full bg-emerald-500"></span>
                <span>{{ time.name }}</span>
              </div>
            </td>
            <td class="p-3">
              <span class="px-2 py-0.5 rounded text-[10px] font-bold uppercase font-mono" :class="time.type === 'Recurring' ? 'bg-emerald-50 text-emerald-800 border border-emerald-200' : 'bg-amber-50 text-amber-800 border border-amber-200'">
                {{ time.type }}
              </span>
            </td>
            <td class="p-3 font-mono text-slate-700">
              <span v-if="time.type === 'Recurring'">
                {{ (time.days || []).map(d => d.toUpperCase()).join(', ') || 'All Days' }}
              </span>
              <span v-else>
                {{ time.start_date }} &rarr; {{ time.end_date }}
              </span>
            </td>
            <td class="p-3 font-mono text-slate-900 font-bold">
              {{ time.start_time }} &ndash; {{ time.end_time }}
            </td>
            <td class="p-3 text-slate-500 italic max-w-xs truncate">{{ time.comment || '—' }}</td>
            <td class="p-3 text-right space-x-1.5 whitespace-nowrap">
              <button type="button" @click="editTimeObject(time)" class="px-2 py-1 bg-white hover:bg-slate-50 text-blue-700 border border-slate-300 rounded text-[11px] font-bold shadow-2xs cursor-pointer">Edit</button>
              <button type="button" @click="cloneTimeObject(time)" class="px-2 py-1 bg-white hover:bg-slate-50 text-amber-700 border border-slate-300 rounded text-[11px] font-bold shadow-2xs cursor-pointer">Clone</button>
              <button type="button" @click="deleteTimeObject(time.id)" class="px-2 py-1 bg-white hover:bg-rose-50 text-rose-600 border border-rose-200 rounded text-[11px] font-bold shadow-2xs cursor-pointer">Delete</button>
            </td>
          </tr>
          <tr v-if="filteredTimeObjects.length === 0">
            <td colspan="7" class="p-8 text-center text-slate-400">
              No time period definitions found matching your filter criteria.
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- CREATE / EDIT MODAL DIALOG -->
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
        <div class="bg-white rounded-2xl shadow-2xl border border-slate-200 max-w-2xl w-full overflow-hidden flex flex-col my-6">
          <!-- Modal Header -->
          <div class="px-5 py-3.5 bg-slate-900 text-white flex items-center justify-between border-b border-slate-800">
            <div class="flex items-center gap-2.5">
              <div class="w-8 h-8 rounded-lg bg-[#ee7f00] flex items-center justify-center text-white font-bold text-xs shadow-md">
                OBJ
              </div>
              <div>
                <h3 class="text-xs font-bold uppercase tracking-wider text-white">
                  {{ editingId ? 'Edit Object' : 'Create New' }} ({{ activeTab === 'networks' ? 'Network' : 'Service' }})
                </h3>
                <p class="text-[10px] text-slate-400">Sophos UTM Reusable Definition &amp; Object Store</p>
              </div>
            </div>
            <button @click="isModalOpen = false" class="text-slate-400 hover:text-white font-bold cursor-pointer text-base leading-none">&times;</button>
          </div>

          <!-- Network Object Form -->
          <form v-if="activeTab === 'networks'" @submit.prevent="saveNetworkObject" class="p-5 space-y-4 text-xs max-h-[80vh] overflow-y-auto">
            <div>
              <label class="block font-bold text-slate-700 mb-1">Name *</label>
              <input
                v-model="newNet.name"
                type="text"
                required
                placeholder="e.g. DMZ Subnet, Web Servers Group, Gateway IP"
                class="w-full p-2 border border-slate-300 rounded-lg focus:border-[#0072ce] focus:outline-none"
              />
            </div>

            <div class="grid grid-cols-2 gap-3">
              <div>
                <label class="block font-bold text-slate-700 mb-1">Type</label>
                <select
                  v-model="newNet.type"
                  class="w-full p-2 border border-slate-300 rounded-lg focus:border-[#0072ce] focus:outline-none bg-white font-medium"
                >
                  <option value="Host">Host (Single IP / FQDN)</option>
                  <option value="Network">Network (CIDR Subnet)</option>
                  <option value="Range">IP Range (From - To)</option>
                  <option value="DNS host">DNS host (Dynamic IP)</option>
                  <option value="DNS group">DNS group (Resolved IPs)</option>
                  <option value="Network group">Network group (Multiple Members)</option>
                  <option value="Multicast group">Multicast group</option>
                  <option value="Availability Group">Availability Group (Failover)</option>
                </select>
              </div>
              <div>
                <label class="block font-bold text-slate-700 mb-1">Interface Binding</label>
                <select
                  v-model="newNet.interface"
                  class="w-full p-2 border border-slate-300 rounded-lg focus:border-[#0072ce] focus:outline-none bg-white font-medium"
                >
                  <option value="<< Any >>">&lt;&lt; Any &gt;&gt;</option>
                  <option value="eth0 (WAN)">eth0 (WAN)</option>
                  <option value="eth1 (LAN)">eth1 (LAN)</option>
                  <option value="eth2 (DMZ)">eth2 (DMZ)</option>
                </select>
              </div>
            </div>

            <!-- NETWORK GROUP MEMBERSHIP & INLINE OBJECT CREATION -->
            <div v-if="newNet.type === 'Network group' || newNet.type === 'Network Group'" class="space-y-3 pt-1">
              <!-- Selected Group Members Container -->
              <div class="p-3.5 bg-purple-50/60 rounded-xl border border-purple-200 space-y-2.5">
                <div class="flex items-center justify-between">
                  <div class="flex items-center gap-2">
                    <span class="w-2 h-2 rounded-full bg-purple-600"></span>
                    <span class="font-bold text-purple-950 text-xs">Selected Group Members ({{ selectedGroupMembers.length }})</span>
                  </div>
                  <button
                    v-if="selectedGroupMembers.length > 0"
                    type="button"
                    @click="selectedGroupMembers = []"
                    class="text-[10px] text-purple-700 hover:text-rose-600 font-bold cursor-pointer"
                  >
                    Clear All
                  </button>
                </div>

                <!-- Members Pills -->
                <div class="flex flex-wrap gap-1.5 min-h-8 p-2 bg-white rounded-lg border border-purple-200">
                  <span
                    v-for="(member, mIdx) in selectedGroupMembers"
                    :key="mIdx"
                    class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md text-[11px] font-bold bg-purple-100 text-purple-900 border border-purple-300 shadow-2xs"
                  >
                    <span>{{ getObjectIcon(member) }}</span>
                    <span>{{ member }}</span>
                    <button
                      type="button"
                      @click="removeGroupMember(mIdx)"
                      class="text-purple-500 hover:text-rose-600 font-bold ml-0.5 cursor-pointer leading-none"
                      title="Remove member"
                    >
                      ✕
                    </button>
                  </span>
                  <span v-if="selectedGroupMembers.length === 0" class="text-slate-400 text-[11px] italic py-0.5">
                    No members selected yet. Choose from existing objects below or create a new one.
                  </span>
                </div>
              </div>

              <!-- Available Objects Selector & Inline Creator Bar -->
              <div class="border border-slate-200 rounded-xl p-3.5 bg-white space-y-3 shadow-2xs">
                <div class="flex items-center justify-between gap-2 flex-wrap">
                  <span class="font-bold text-slate-800 text-xs flex items-center gap-1.5">
                    <span>📚</span>
                    <span>Choose Existing Network Objects</span>
                  </span>
                  <button
                    type="button"
                    @click="isInlineNetOpen = !isInlineNetOpen"
                    class="px-2.5 py-1 bg-emerald-50 hover:bg-emerald-100 text-emerald-700 border border-emerald-300 rounded-md font-bold text-[11px] flex items-center gap-1 shadow-2xs cursor-pointer transition-colors"
                  >
                    <span>{{ isInlineNetOpen ? '▲ Close Creator' : '+ Create New Network Object...' }}</span>
                  </button>
                </div>

                <!-- INLINE NEW OBJECT CREATION FORM (EMBEDDED IN SAME WINDOW) -->
                <div v-if="isInlineNetOpen" class="p-3.5 bg-emerald-50/50 rounded-xl border border-emerald-200 space-y-3">
                  <div class="flex items-center justify-between border-b border-emerald-200/60 pb-1.5">
                    <span class="font-bold text-emerald-900 text-xs flex items-center gap-1.5">
                      <span>✨</span>
                      <span>New Network Object Definition (Created &amp; Added to Group)</span>
                    </span>
                    <button type="button" @click="isInlineNetOpen = false" class="text-slate-400 hover:text-slate-600 text-xs font-bold">✕</button>
                  </div>

                  <div class="grid grid-cols-1 sm:grid-cols-3 gap-2.5">
                    <div>
                      <label class="block font-bold text-slate-700 mb-1">Object Name *</label>
                      <input
                        v-model="inlineNet.name"
                        type="text"
                        placeholder="e.g. DMZ_DB_01"
                        class="w-full p-1.5 border border-slate-300 rounded-md bg-white font-medium focus:border-emerald-600 focus:outline-none text-xs"
                      />
                    </div>
                    <div>
                      <label class="block font-bold text-slate-700 mb-1">Type</label>
                      <select
                        v-model="inlineNet.type"
                        class="w-full p-1.5 border border-slate-300 rounded-md bg-white font-medium focus:border-emerald-600 focus:outline-none text-xs"
                      >
                        <option value="Host">Host (Single IP)</option>
                        <option value="Network">Network (CIDR Subnet)</option>
                        <option value="Range">IP Range</option>
                        <option value="DNS host">DNS host (FQDN)</option>
                      </select>
                    </div>
                    <div>
                      <label class="block font-bold text-slate-700 mb-1">IPv4 / Subnet / FQDN *</label>
                      <input
                        v-model="inlineNet.address"
                        type="text"
                        :placeholder="inlineNet.type === 'Host' ? '192.168.1.50' : (inlineNet.type === 'Network' ? '192.168.1.0/24' : '192.168.1.10 - 192.168.1.50')"
                        class="w-full p-1.5 border border-slate-300 rounded-md bg-white font-mono focus:border-emerald-600 focus:outline-none text-xs"
                      />
                    </div>
                  </div>

                  <div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
                    <div>
                      <label class="block font-bold text-slate-700 mb-1">Interface Binding</label>
                      <select
                        v-model="inlineNet.interface"
                        class="w-full p-1.5 border border-slate-300 rounded-md bg-white font-medium focus:border-emerald-600 focus:outline-none text-xs"
                      >
                        <option value="<< Any >>">&lt;&lt; Any &gt;&gt;</option>
                        <option value="eth0 (WAN)">eth0 (WAN)</option>
                        <option value="eth1 (LAN)">eth1 (LAN)</option>
                        <option value="eth2 (DMZ)">eth2 (DMZ)</option>
                      </select>
                    </div>
                    <div>
                      <label class="block font-bold text-slate-700 mb-1">Comment</label>
                      <input
                        v-model="inlineNet.comment"
                        type="text"
                        placeholder="Optional notes"
                        class="w-full p-1.5 border border-slate-300 rounded-md bg-white font-medium focus:border-emerald-600 focus:outline-none text-xs"
                      />
                    </div>
                  </div>

                  <div class="flex justify-end gap-2 pt-1">
                    <button
                      type="button"
                      @click="isInlineNetOpen = false"
                      class="px-3 py-1 rounded border border-slate-300 bg-white text-slate-700 text-[11px] font-bold hover:bg-slate-50 cursor-pointer"
                    >
                      Cancel
                    </button>
                    <button
                      type="button"
                      @click="createInlineNetworkObject"
                      class="px-3.5 py-1 rounded bg-emerald-600 hover:bg-emerald-700 text-white text-[11px] font-bold shadow-xs cursor-pointer"
                    >
                      ✔ Save &amp; Add to Group
                    </button>
                  </div>
                </div>

                <!-- Search & Filter Controls -->
                <div class="flex items-center gap-2">
                  <div class="relative flex-1">
                    <input
                      v-model="existingNetSearch"
                      type="text"
                      placeholder="Search existing objects by name, IP, or type..."
                      class="w-full pl-7 pr-3 py-1.5 text-xs bg-slate-50 border border-slate-200 rounded-lg focus:bg-white focus:border-[#0072ce] focus:outline-none"
                    />
                    <svg class="w-3.5 h-3.5 text-slate-400 absolute left-2 top-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                    </svg>
                  </div>
                  <select v-model="existingNetTypeFilter" class="p-1.5 text-xs bg-slate-50 border border-slate-200 rounded-lg font-bold">
                    <option value="ALL">All Types</option>
                    <option value="Host">Hosts</option>
                    <option value="Network">Networks</option>
                    <option value="Range">Ranges</option>
                    <option value="DNS host">DNS Hosts</option>
                  </select>
                </div>

                <!-- Existing Objects Selectable Grid -->
                <div class="border border-slate-200 rounded-lg max-h-44 overflow-y-auto divide-y divide-slate-100 bg-[#fbfcfd]">
                  <div
                    v-for="obj in filteredAvailableNetObjects"
                    :key="obj.id || obj.name"
                    @click="toggleGroupMember(obj.name)"
                    class="p-2 flex items-center justify-between hover:bg-blue-50/60 cursor-pointer transition-colors"
                    :class="selectedGroupMembers.includes(obj.name) ? 'bg-purple-50/70' : ''"
                  >
                    <div class="flex items-center gap-2.5">
                      <input
                        type="checkbox"
                        :checked="selectedGroupMembers.includes(obj.name)"
                        @click.stop="toggleGroupMember(obj.name)"
                        class="w-3.5 h-3.5 rounded text-purple-600 focus:ring-purple-500 cursor-pointer"
                      />
                      <div>
                        <div class="font-bold text-slate-900 flex items-center gap-1.5 text-[11px]">
                          <span>{{ getObjectIcon(obj.name, obj.type) }}</span>
                          <span>{{ obj.name }}</span>
                        </div>
                        <div class="text-[10px] font-mono text-slate-500">{{ obj.address }}</div>
                      </div>
                    </div>
                    <span class="px-1.5 py-0.2 rounded text-[9px] font-bold uppercase font-mono bg-slate-100 text-slate-700 border border-slate-200">
                      {{ obj.type }}
                    </span>
                  </div>

                  <div v-if="filteredAvailableNetObjects.length === 0" class="p-4 text-center text-slate-400 text-[11px]">
                    No network objects found. Use the creator above to add one on the fly.
                  </div>
                </div>
              </div>
            </div>

            <!-- Standard Address Field for Non-Group Objects -->
            <div v-else>
              <label class="block font-bold text-slate-700 mb-1">IPv4 / IPv6 Address *</label>
              <input
                v-model="newNet.address"
                type="text"
                required
                :placeholder="newNet.type === 'Host' ? '192.168.1.50' : (newNet.type === 'Network' ? '192.168.1.0/24' : '192.168.1.10 - 192.168.1.50')"
                class="w-full p-2 border border-slate-300 rounded-lg font-mono focus:border-[#0072ce] focus:outline-none"
              />
            </div>

            <div>
              <label class="block font-bold text-slate-700 mb-1">Comment</label>
              <input
                v-model="newNet.comment"
                type="text"
                placeholder="Optional notes"
                class="w-full p-2 border border-slate-300 rounded-lg focus:border-[#0072ce] focus:outline-none"
              />
            </div>

            <div class="pt-3 border-t border-slate-200 flex items-center justify-between">
              <button
                type="button"
                @click="isModalOpen = false"
                class="px-4 py-2 rounded-lg border border-slate-300 bg-white text-slate-700 text-xs font-bold hover:bg-slate-50 cursor-pointer"
              >
                Cancel
              </button>
              <button
                type="submit"
                class="px-5 py-2 rounded-lg bg-[#0072ce] hover:bg-blue-700 text-white text-xs font-bold shadow-xs cursor-pointer"
              >
                {{ editingId ? 'Update Definition' : 'Save Definition' }}
              </button>
            </div>
          </form>

          <!-- Service Object Form -->
          <form v-else @submit.prevent="saveServiceObject" class="p-5 space-y-4 text-xs max-h-[80vh] overflow-y-auto">
            <div>
              <label class="block font-bold text-slate-700 mb-1">Service Name *</label>
              <input
                v-model="newSrv.name"
                type="text"
                required
                placeholder="e.g. HTTPS, Web Services Group, Custom App 8080"
                class="w-full p-2 border border-slate-300 rounded-lg focus:border-[#0072ce] focus:outline-none"
              />
            </div>

            <div class="grid grid-cols-2 gap-3">
              <div>
                <label class="block font-bold text-slate-700 mb-1">Protocol / Type</label>
                <select
                  v-model="newSrv.type"
                  class="w-full p-2 border border-slate-300 rounded-lg focus:border-[#0072ce] focus:outline-none bg-white font-medium"
                >
                  <option value="TCP">TCP</option>
                  <option value="UDP">UDP</option>
                  <option value="TCP/UDP">TCP/UDP</option>
                  <option value="ICMP">ICMP</option>
                  <option value="IP Protocol">IP Protocol</option>
                  <option value="Service Group">Service Group</option>
                </select>
              </div>
              <div v-if="newSrv.type !== 'Service Group'">
                <label class="block font-bold text-slate-700 mb-1">Destination Port *</label>
                <input
                  v-model="newSrv.dst_port"
                  type="text"
                  required
                  placeholder="e.g. 443, 80:90, or HTTP, HTTPS"
                  class="w-full p-2 border border-slate-300 rounded-lg font-mono focus:border-[#0072ce] focus:outline-none"
                />
              </div>
              <div v-else>
                <label class="block font-bold text-slate-700 mb-1">Group Type</label>
                <div class="p-2 bg-amber-50 rounded-lg border border-amber-200 font-bold text-amber-900">
                  Multiple Services
                </div>
              </div>
            </div>

            <!-- SERVICE GROUP MEMBERSHIP & INLINE SERVICE CREATION -->
            <div v-if="newSrv.type === 'Service Group'" class="space-y-3 pt-1">
              <!-- Selected Service Group Members Container -->
              <div class="p-3.5 bg-amber-50/60 rounded-xl border border-amber-200 space-y-2.5">
                <div class="flex items-center justify-between">
                  <div class="flex items-center gap-2">
                    <span class="w-2 h-2 rounded-full bg-[#ee7f00]"></span>
                    <span class="font-bold text-amber-950 text-xs">Selected Service Members ({{ selectedSrvGroupMembers.length }})</span>
                  </div>
                  <button
                    v-if="selectedSrvGroupMembers.length > 0"
                    type="button"
                    @click="selectedSrvGroupMembers = []"
                    class="text-[10px] text-amber-800 hover:text-rose-600 font-bold cursor-pointer"
                  >
                    Clear All
                  </button>
                </div>

                <!-- Service Members Pills -->
                <div class="flex flex-wrap gap-1.5 min-h-8 p-2 bg-white rounded-lg border border-amber-200">
                  <span
                    v-for="(member, mIdx) in selectedSrvGroupMembers"
                    :key="mIdx"
                    class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md text-[11px] font-bold bg-amber-100 text-amber-900 border border-amber-300 shadow-2xs"
                  >
                    <span>⚡</span>
                    <span>{{ member }}</span>
                    <button
                      type="button"
                      @click="removeSrvGroupMember(mIdx)"
                      class="text-amber-600 hover:text-rose-600 font-bold ml-0.5 cursor-pointer leading-none"
                      title="Remove member"
                    >
                      ✕
                    </button>
                  </span>
                  <span v-if="selectedSrvGroupMembers.length === 0" class="text-slate-400 text-[11px] italic py-0.5">
                    No services selected yet. Choose from existing definitions below or create a new one.
                  </span>
                </div>
              </div>

              <!-- Available Services Selector & Inline Creator Bar -->
              <div class="border border-slate-200 rounded-xl p-3.5 bg-white space-y-3 shadow-2xs">
                <div class="flex items-center justify-between gap-2 flex-wrap">
                  <span class="font-bold text-slate-800 text-xs flex items-center gap-1.5">
                    <span>🔌</span>
                    <span>Choose Existing Service Definitions</span>
                  </span>
                  <button
                    type="button"
                    @click="isInlineSrvOpen = !isInlineSrvOpen"
                    class="px-2.5 py-1 bg-amber-50 hover:bg-amber-100 text-amber-800 border border-amber-300 rounded-md font-bold text-[11px] flex items-center gap-1 shadow-2xs cursor-pointer transition-colors"
                  >
                    <span>{{ isInlineSrvOpen ? '▲ Close Creator' : '+ Create New Service Definition...' }}</span>
                  </button>
                </div>

                <!-- INLINE NEW SERVICE CREATION FORM -->
                <div v-if="isInlineSrvOpen" class="p-3.5 bg-amber-50/50 rounded-xl border border-amber-200 space-y-3">
                  <div class="flex items-center justify-between border-b border-amber-200/60 pb-1.5">
                    <span class="font-bold text-amber-900 text-xs flex items-center gap-1.5">
                      <span>✨</span>
                      <span>New Service Definition (Created &amp; Added to Group)</span>
                    </span>
                    <button type="button" @click="isInlineSrvOpen = false" class="text-slate-400 hover:text-slate-600 text-xs font-bold">✕</button>
                  </div>

                  <div class="grid grid-cols-1 sm:grid-cols-3 gap-2.5">
                    <div>
                      <label class="block font-bold text-slate-700 mb-1">Service Name *</label>
                      <input
                        v-model="inlineSrv.name"
                        type="text"
                        placeholder="e.g. MySQL Port 3306"
                        class="w-full p-1.5 border border-slate-300 rounded-md bg-white font-medium focus:border-amber-600 focus:outline-none text-xs"
                      />
                    </div>
                    <div>
                      <label class="block font-bold text-slate-700 mb-1">Protocol</label>
                      <select
                        v-model="inlineSrv.type"
                        class="w-full p-1.5 border border-slate-300 rounded-md bg-white font-medium focus:border-amber-600 focus:outline-none text-xs"
                      >
                        <option value="TCP">TCP</option>
                        <option value="UDP">UDP</option>
                        <option value="TCP/UDP">TCP/UDP</option>
                        <option value="ICMP">ICMP</option>
                      </select>
                    </div>
                    <div>
                      <label class="block font-bold text-slate-700 mb-1">Destination Port *</label>
                      <input
                        v-model="inlineSrv.dst_port"
                        type="text"
                        placeholder="e.g. 3306 or 8080:8090"
                        class="w-full p-1.5 border border-slate-300 rounded-md bg-white font-mono focus:border-amber-600 focus:outline-none text-xs"
                      />
                    </div>
                  </div>

                  <div class="flex justify-end gap-2 pt-1">
                    <button
                      type="button"
                      @click="isInlineSrvOpen = false"
                      class="px-3 py-1 rounded border border-slate-300 bg-white text-slate-700 text-[11px] font-bold hover:bg-slate-50 cursor-pointer"
                    >
                      Cancel
                    </button>
                    <button
                      type="button"
                      @click="createInlineServiceObject"
                      class="px-3.5 py-1 rounded bg-[#ee7f00] hover:bg-amber-600 text-white text-[11px] font-bold shadow-xs cursor-pointer"
                    >
                      ✔ Save &amp; Add to Group
                    </button>
                  </div>
                </div>

                <!-- Search & Filter Controls -->
                <div class="flex items-center gap-2">
                  <div class="relative flex-1">
                    <input
                      v-model="existingSrvSearch"
                      type="text"
                      placeholder="Search existing services by name, port, or protocol..."
                      class="w-full pl-7 pr-3 py-1.5 text-xs bg-slate-50 border border-slate-200 rounded-lg focus:bg-white focus:border-[#0072ce] focus:outline-none"
                    />
                    <svg class="w-3.5 h-3.5 text-slate-400 absolute left-2 top-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                    </svg>
                  </div>
                </div>

                <!-- Existing Services Selectable Grid -->
                <div class="border border-slate-200 rounded-lg max-h-44 overflow-y-auto divide-y divide-slate-100 bg-[#fbfcfd]">
                  <div
                    v-for="srv in filteredAvailableSrvObjects"
                    :key="srv.id || srv.name"
                    @click="toggleSrvGroupMember(srv.name)"
                    class="p-2 flex items-center justify-between hover:bg-amber-50/60 cursor-pointer transition-colors"
                    :class="selectedSrvGroupMembers.includes(srv.name) ? 'bg-amber-50/80' : ''"
                  >
                    <div class="flex items-center gap-2.5">
                      <input
                        type="checkbox"
                        :checked="selectedSrvGroupMembers.includes(srv.name)"
                        @click.stop="toggleSrvGroupMember(srv.name)"
                        class="w-3.5 h-3.5 rounded text-amber-600 focus:ring-amber-500 cursor-pointer"
                      />
                      <div>
                        <div class="font-bold text-slate-900 text-[11px]">
                          {{ srv.name }}
                        </div>
                        <div class="text-[10px] font-mono text-slate-500">Port: {{ srv.dst_port }}</div>
                      </div>
                    </div>
                    <span class="px-1.5 py-0.2 rounded text-[9px] font-bold uppercase font-mono bg-slate-100 text-slate-700 border border-slate-200">
                      {{ srv.protocol || srv.type }}
                    </span>
                  </div>

                  <div v-if="filteredAvailableSrvObjects.length === 0" class="p-4 text-center text-slate-400 text-[11px]">
                    No service definitions found. Use the creator above to add one on the fly.
                  </div>
                </div>
              </div>
            </div>

            <div v-if="newSrv.type !== 'Service Group'">
              <label class="block font-bold text-slate-700 mb-1">Source Port Range</label>
              <input
                v-model="newSrv.src_port"
                type="text"
                placeholder="1:65535 (Default)"
                class="w-full p-2 border border-slate-300 rounded-lg font-mono focus:border-[#0072ce] focus:outline-none"
              />
            </div>

            <div>
              <label class="block font-bold text-slate-700 mb-1">Comment</label>
              <input
                v-model="newSrv.comment"
                type="text"
                placeholder="Optional notes"
                class="w-full p-2 border border-slate-300 rounded-lg focus:border-[#0072ce] focus:outline-none"
              />
            </div>

            <div class="pt-3 border-t border-slate-200 flex items-center justify-between">
              <button
                type="button"
                @click="isModalOpen = false"
                class="px-4 py-2 rounded-lg border border-slate-300 bg-white text-slate-700 text-xs font-bold hover:bg-slate-50 cursor-pointer"
              >
                Cancel
              </button>
              <button
                type="submit"
                class="px-5 py-2 rounded-lg bg-[#0072ce] hover:bg-blue-700 text-white text-xs font-bold shadow-xs cursor-pointer"
              >
                {{ editingId ? 'Update Service' : 'Save Service' }}
              </button>
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

const activeTab = ref('networks') // 'networks' | 'services'
const isModalOpen = ref(false)
const searchQuery = ref('')
const sortBy = ref('name_asc')
const isLoading = ref(false)
const editingId = ref(null)

const networkObjects = ref([])
const serviceObjects = ref([])

// Group Members selections
const selectedGroupMembers = ref([])
const selectedSrvGroupMembers = ref([])

// Inline Network Object Creator State (Embedded in Same Window)
const isInlineNetOpen = ref(false)
const inlineNet = ref({
  name: '',
  type: 'Host',
  address: '',
  interface: '<< Any >>',
  comment: ''
})
const existingNetSearch = ref('')
const existingNetTypeFilter = ref('ALL')

// Inline Service Definition Creator State (Embedded in Same Window)
const isInlineSrvOpen = ref(false)
const inlineSrv = ref({
  name: '',
  type: 'TCP',
  dst_port: '',
  src_port: '1:65535',
  comment: ''
})
const existingSrvSearch = ref('')

const newNet = ref({
  id: null,
  name: '',
  type: 'Host',
  address: '',
  interface: '<< Any >>',
  comment: ''
})

const newSrv = ref({
  id: null,
  name: '',
  type: 'TCP',
  protocol: 'TCP',
  dst_port: '',
  src_port: '1:65535',
  comment: ''
})

const filteredNetworkObjects = computed(() => {
  let list = [...networkObjects.value]
  if (searchQuery.value.trim()) {
    const q = searchQuery.value.toLowerCase()
    list = list.filter(n =>
      (n.name && n.name.toLowerCase().includes(q)) ||
      (n.address && n.address.toLowerCase().includes(q)) ||
      (n.type && n.type.toLowerCase().includes(q)) ||
      (n.comment && n.comment.toLowerCase().includes(q))
    )
  }
  if (sortBy.value === 'name_asc') list.sort((a, b) => (a.name || '').localeCompare(b.name || ''))
  else if (sortBy.value === 'name_desc') list.sort((a, b) => (b.name || '').localeCompare(a.name || ''))
  else if (sortBy.value === 'type') list.sort((a, b) => (a.type || '').localeCompare(b.type || ''))
  return list
})

const filteredServiceObjects = computed(() => {
  let list = [...serviceObjects.value]
  if (searchQuery.value.trim()) {
    const q = searchQuery.value.toLowerCase()
    list = list.filter(s =>
      (s.name && s.name.toLowerCase().includes(q)) ||
      (s.dst_port && s.dst_port.toLowerCase().includes(q)) ||
      (s.protocol && s.protocol.toLowerCase().includes(q)) ||
      (s.comment && s.comment.toLowerCase().includes(q))
    )
  }
  if (sortBy.value === 'name_asc') list.sort((a, b) => (a.name || '').localeCompare(b.name || ''))
  else if (sortBy.value === 'name_desc') list.sort((a, b) => (b.name || '').localeCompare(a.name || ''))
  else if (sortBy.value === 'type') list.sort((a, b) => (a.protocol || a.type || '').localeCompare(b.protocol || b.type || ''))
  return list
})

const filteredAvailableNetObjects = computed(() => {
  let list = networkObjects.value.filter(n =>
    n.type !== 'Network group' &&
    n.type !== 'Network Group' &&
    n.id !== editingId.value &&
    n.name !== newNet.value.name
  )
  if (existingNetTypeFilter.value !== 'ALL') {
    list = list.filter(n => n.type.toLowerCase() === existingNetTypeFilter.value.toLowerCase())
  }
  if (existingNetSearch.value.trim()) {
    const q = existingNetSearch.value.toLowerCase()
    list = list.filter(n =>
      n.name.toLowerCase().includes(q) ||
      (n.address && n.address.toLowerCase().includes(q)) ||
      (n.type && n.type.toLowerCase().includes(q))
    )
  }
  return list
})

const filteredAvailableSrvObjects = computed(() => {
  let list = serviceObjects.value.filter(s =>
    s.protocol !== 'Group' &&
    s.type !== 'Service Group' &&
    s.id !== editingId.value &&
    s.name !== newSrv.value.name
  )
  if (existingSrvSearch.value.trim()) {
    const q = existingSrvSearch.value.toLowerCase()
    list = list.filter(s =>
      s.name.toLowerCase().includes(q) ||
      (s.dst_port && s.dst_port.toLowerCase().includes(q)) ||
      (s.protocol && s.protocol.toLowerCase().includes(q))
    )
  }
  return list
})

const filteredItemsCount = computed(() => {
  return activeTab.value === 'networks' ? filteredNetworkObjects.value.length : filteredServiceObjects.value.length
})

const getObjectIcon = (name, type = '') => {
  const match = networkObjects.value.find(n => n.name === name)
  const t = (type || (match ? match.type : '')).toLowerCase()
  if (t.includes('host')) return '🖥️'
  if (t.includes('network')) return '🌐'
  if (t.includes('range')) return '🔀'
  if (t.includes('dns')) return '📡'
  return '📦'
}

const getGroupMembers = (net) => {
  if (Array.isArray(net.members) && net.members.length > 0) return net.members
  if (typeof net.address === 'string' && net.address.includes(',')) {
    return net.address.split(',').map(s => s.trim()).filter(Boolean)
  }
  return []
}

const getServiceGroupMembers = (srv) => {
  if (Array.isArray(srv.members) && srv.members.length > 0) return srv.members
  if (typeof srv.dst_port === 'string' && srv.dst_port.includes(',')) {
    return srv.dst_port.split(',').map(s => s.trim()).filter(Boolean)
  }
  return []
}

const toggleGroupMember = (name) => {
  const idx = selectedGroupMembers.value.indexOf(name)
  if (idx > -1) {
    selectedGroupMembers.value.splice(idx, 1)
  } else {
    selectedGroupMembers.value.push(name)
  }
}

const removeGroupMember = (idx) => {
  selectedGroupMembers.value.splice(idx, 1)
}

const toggleSrvGroupMember = (name) => {
  const idx = selectedSrvGroupMembers.value.indexOf(name)
  if (idx > -1) {
    selectedSrvGroupMembers.value.splice(idx, 1)
  } else {
    selectedSrvGroupMembers.value.push(name)
  }
}

const removeSrvGroupMember = (idx) => {
  selectedSrvGroupMembers.value.splice(idx, 1)
}

const createInlineNetworkObject = async () => {
  if (!inlineNet.value.name.trim() || !inlineNet.value.address.trim()) {
    alert('Please provide an Object Name and Address/Subnet.')
    return
  }

  const payload = {
    name: inlineNet.value.name.trim(),
    type: inlineNet.value.type,
    address: inlineNet.value.address.trim(),
    interface: inlineNet.value.interface || '<< Any >>',
    comment: inlineNet.value.comment ? `${inlineNet.value.comment} (Created in Group)` : 'Created in Group Modal'
  }

  try {
    const axiosLib = (typeof window !== 'undefined' && window.axios) ? window.axios : null
    if (axiosLib) {
      const res = await axiosLib.post('/api/definitions/networks', payload)
      if (res.data && res.data.object) {
        networkObjects.value.push(res.data.object)
      } else {
        networkObjects.value.push({ id: `net-${Date.now()}`, ...payload })
      }
    } else {
      networkObjects.value.push({ id: `net-${Date.now()}`, ...payload })
    }

    // Automatically select the newly created object into the group!
    if (!selectedGroupMembers.value.includes(payload.name)) {
      selectedGroupMembers.value.push(payload.name)
    }

    // Reset inline form and close
    inlineNet.value = { name: '', type: 'Host', address: '', interface: '<< Any >>', comment: '' }
    isInlineNetOpen.value = false
  } catch (err) {
    console.error('Failed to create inline network object:', err)
  }
}

const createInlineServiceObject = async () => {
  if (!inlineSrv.value.name.trim() || !inlineSrv.value.dst_port.trim()) {
    alert('Please provide a Service Name and Destination Port.')
    return
  }

  const payload = {
    name: inlineSrv.value.name.trim(),
    type: inlineSrv.value.type,
    protocol: inlineSrv.value.type,
    dst_port: inlineSrv.value.dst_port.trim(),
    src_port: inlineSrv.value.src_port || '1:65535',
    comment: inlineSrv.value.comment ? `${inlineSrv.value.comment} (Created in Group)` : 'Created in Group Modal'
  }

  try {
    const axiosLib = (typeof window !== 'undefined' && window.axios) ? window.axios : null
    if (axiosLib) {
      const res = await axiosLib.post('/api/definitions/services', payload)
      if (res.data && res.data.object) {
        serviceObjects.value.push(res.data.object)
      } else {
        serviceObjects.value.push({ id: `srv-${Date.now()}`, ...payload })
      }
    } else {
      serviceObjects.value.push({ id: `srv-${Date.now()}`, ...payload })
    }

    // Automatically select the newly created service into the group!
    if (!selectedSrvGroupMembers.value.includes(payload.name)) {
      selectedSrvGroupMembers.value.push(payload.name)
    }

    // Reset inline form and close
    inlineSrv.value = { name: '', type: 'TCP', dst_port: '', src_port: '1:65535', comment: '' }
    isInlineSrvOpen.value = false
  } catch (err) {
    console.error('Failed to create inline service object:', err)
  }
}

const fetchDefinitions = async () => {
  isLoading.value = true
  try {
    const axiosLib = (typeof window !== 'undefined' && window.axios) ? window.axios : null
    if (axiosLib) {
      const [netRes, srvRes, timeRes] = await Promise.all([
        axiosLib.get('/api/definitions/networks').catch(() => ({ data: [] })),
        axiosLib.get('/api/definitions/services').catch(() => ({ data: [] })),
        axiosLib.get('/api/definitions/time-periods').catch(() => ({ data: [] }))
      ])
      if (netRes && netRes.data) networkObjects.value = netRes.data
      if (srvRes && srvRes.data) serviceObjects.value = srvRes.data
      if (timeRes && timeRes.data) timeObjects.value = timeRes.data
    }
  } catch (err) {
    console.error('Failed to fetch definitions:', err)
  } finally {
    isLoading.value = false
  }
}

const filteredNetworkObjects = computed(() => {
  let list = [...networkObjects.value]
  if (searchQuery.value.trim()) {
    const q = searchQuery.value.toLowerCase()
    list = list.filter(n => n.name.toLowerCase().includes(q) || (n.address && n.address.toLowerCase().includes(q)) || (n.comment && n.comment.toLowerCase().includes(q)))
  }
  return list
})

const filteredServiceObjects = computed(() => {
  let list = [...serviceObjects.value]
  if (searchQuery.value.trim()) {
    const q = searchQuery.value.toLowerCase()
    list = list.filter(s => s.name.toLowerCase().includes(q) || (s.dst_port && s.dst_port.toLowerCase().includes(q)) || (s.comment && s.comment.toLowerCase().includes(q)))
  }
  return list
})

const openCreateModal = () => {
  editingId.value = null
  if (activeTab.value === 'networks') {
    newNet.value = { id: null, name: '', type: 'Host', address: '', netmask: '/24 (255.255.255.0)', from_ip: '', to_ip: '', comment: '', interface: '<< Any >>' }
    selectedGroupMembers.value = []
  } else if (activeTab.value === 'services') {
    newSrv.value = { id: null, name: '', type: 'TCP', protocol: 'TCP', dst_port: '', src_port: '1:65535', comment: '' }
    selectedSrvGroupMembers.value = []
  } else {
    newTime.value = { id: null, name: '', type: 'Recurring', days: ['mon', 'tue', 'wed', 'thu', 'fri'], start_time: '08:00', end_time: '17:00', start_date: '', end_date: '', comment: '' }
  }
  isModalOpen.value = true
}

const editNetObject = (net) => {
  editingId.value = net.id
  newNet.value = JSON.parse(JSON.stringify(net))
  selectedGroupMembers.value = getGroupMembers(net)
  isModalOpen.value = true
}

const cloneNetObject = (net) => {
  editingId.value = null
  newNet.value = { ...JSON.parse(JSON.stringify(net)), id: null, name: `${net.name} (Clone)` }
  selectedGroupMembers.value = getGroupMembers(net)
  isModalOpen.value = true
}

const editSrvObject = (srv) => {
  editingId.value = srv.id
  newSrv.value = { ...JSON.parse(JSON.stringify(srv)), type: srv.protocol === 'Group' ? 'Service Group' : (srv.type || srv.protocol) }
  selectedSrvGroupMembers.value = getServiceGroupMembers(srv)
  isModalOpen.value = true
}

const cloneSrvObject = (srv) => {
  editingId.value = null
  newSrv.value = { ...JSON.parse(JSON.stringify(srv)), id: null, name: `${srv.name} (Clone)`, type: srv.protocol === 'Group' ? 'Service Group' : (srv.type || srv.protocol) }
  selectedSrvGroupMembers.value = getServiceGroupMembers(srv)
  isModalOpen.value = true
}

const saveNetworkObject = async () => {
  if (!newNet.value.name) return
  const isGroup = newNet.value.type === 'Network group' || newNet.value.type === 'Network Group'
  if (!isGroup && !newNet.value.address) return
  const axiosLib = (typeof window !== 'undefined' && window.axios) ? window.axios : null
  try {
    const formattedAddress = isGroup ? selectedGroupMembers.value.join(', ') : newNet.value.address
    const payload = { ...newNet.value, id: editingId.value || newNet.value.id, address: formattedAddress, members: isGroup ? selectedGroupMembers.value : [] }
    if (axiosLib) await axiosLib.post('/api/definitions/networks', payload)
    else await fetch('/api/definitions/networks', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) })
    isModalOpen.value = false
    await fetchDefinitions()
  } catch (err) {
    console.error('Failed to save network definition:', err)
  }
}

const saveServiceObject = async () => {
  if (!newSrv.value.name) return
  const isGroup = newSrv.value.type === 'Service Group'
  if (!isGroup && !newSrv.value.dst_port) return
  const axiosLib = (typeof window !== 'undefined' && window.axios) ? window.axios : null
  try {
    const formattedDstPort = isGroup ? selectedSrvGroupMembers.value.join(', ') : newSrv.value.dst_port
    const payload = { ...newSrv.value, id: editingId.value || newSrv.value.id, protocol: isGroup ? 'Group' : (newSrv.value.type.includes('UDP') ? 'UDP' : 'TCP'), dst_port: formattedDstPort, members: isGroup ? selectedSrvGroupMembers.value : [] }
    if (axiosLib) await axiosLib.post('/api/definitions/services', payload)
    else await fetch('/api/definitions/services', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) })
    isModalOpen.value = false
    await fetchDefinitions()
  } catch (err) {
    console.error('Failed to save service definition:', err)
  }
}

const deleteNetworkObject = async (id) => {
  const item = networkObjects.value.find(n => n.id === id)
  if (!confirm(`Are you sure you want to delete network definition '${item ? item.name : id}'?`)) return
  const axiosLib = (typeof window !== 'undefined' && window.axios) ? window.axios : null
  try {
    if (axiosLib) await axiosLib.delete(`/api/definitions/networks/${id}`)
    else await fetch(`/api/definitions/networks/${id}`, { method: 'DELETE' })
    await fetchDefinitions()
  } catch (err) {
    console.error('Failed to delete network object:', err)
  }
}

const deleteServiceObject = async (id) => {
  const item = serviceObjects.value.find(s => s.id === id)
  if (!confirm(`Are you sure you want to delete service definition '${item ? item.name : id}'?`)) return
  const axiosLib = (typeof window !== 'undefined' && window.axios) ? window.axios : null
  try {
    if (axiosLib) await axiosLib.delete(`/api/definitions/services/${id}`)
    else await fetch(`/api/definitions/services/${id}`, { method: 'DELETE' })
    await fetchDefinitions()
  } catch (err) {
    console.error('Failed to delete service object:', err)
  }
}

onMounted(() => {
  fetchDefinitions()
})
</script>
