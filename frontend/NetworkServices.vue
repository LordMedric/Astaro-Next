<template>
  <div class="space-y-6">
    <!-- Standardized Page Header -->
    <div class="bg-white border border-slate-200 rounded-xl p-5 shadow-xs flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
      <div>
        <div class="flex items-center gap-2.5">
          <span class="w-1.5 h-6 bg-[#ee7f00] rounded-xs inline-block"></span>
          <h1 class="text-xl font-bold text-slate-900 tracking-tight">Network Services (DHCP &amp; DNS)</h1>
          <span class="text-[11px] bg-blue-50 text-[#0072ce] font-medium font-mono px-2 py-0.5 rounded border border-blue-200">
            Dnsmasq / CoreDNS Engine
          </span>
        </div>
        <p class="text-xs text-slate-500 mt-1 pl-4">
          Manage local DHCP subnets, static IP reservations, upstream DNS forwarders, Static DNS records, DynDNS, and NTP.
        </p>
      </div>

      <div class="flex items-center gap-2.5 flex-wrap">
        <button
          type="button"
          @click="refreshCurrentTab"
          :disabled="isLoading"
          class="px-3.5 py-2 text-xs font-semibold bg-white hover:bg-slate-50 text-slate-700 rounded-lg border border-slate-300 transition-colors flex items-center gap-1.5 shadow-xs cursor-pointer active:bg-slate-100"
          title="Refresh active services"
        >
          <svg :class="['w-3.5 h-3.5 text-slate-500', isLoading ? 'animate-spin text-[#0072ce]' : '']" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          <span>Refresh</span>
        </button>

        <button
          v-if="activeTab === 'reservations'"
          type="button"
          @click="openAddReservationModal"
          class="px-4 py-2 bg-[#0072ce] hover:bg-blue-700 text-white rounded-lg text-xs font-bold shadow-sm flex items-center gap-2 transition-all cursor-pointer"
        >
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          <span>+ Add Reservation...</span>
        </button>

        <button
          v-else-if="activeTab === 'static_dns'"
          type="button"
          @click="openAddDnsModal"
          class="px-4 py-2 bg-[#0072ce] hover:bg-blue-700 text-white rounded-lg text-xs font-bold shadow-sm flex items-center gap-2 transition-all cursor-pointer"
        >
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          <span>+ Add DNS Record...</span>
        </button>

        <button
          v-else-if="activeTab === 'dhcp'"
          type="button"
          @click="saveDhcpSettings"
          :disabled="isSaving"
          class="px-4 py-2 bg-[#0072ce] hover:bg-blue-700 text-white rounded-lg text-xs font-bold shadow-sm flex items-center gap-2 transition-all cursor-pointer"
        >
          <span v-if="isSaving" class="w-3.5 h-3.5 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
          <span>Apply DHCP Settings</span>
        </button>

        <button
          v-else-if="activeTab === 'dns'"
          type="button"
          @click="saveDnsSettings"
          class="px-4 py-2 bg-[#0072ce] hover:bg-blue-700 text-white rounded-lg text-xs font-bold shadow-sm flex items-center gap-2 transition-all cursor-pointer"
        >
          <span>Save DNS Settings</span>
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
        <component :is="tab.icon" class="w-4 h-4 text-[#0072ce]" />
        <span>{{ tab.label }}</span>
        <span
          v-if="tab.badge"
          class="px-1.5 py-0.2 rounded-full text-[10px] font-mono"
          :class="activeTab === tab.id ? 'bg-[#0072ce] text-white' : 'bg-slate-200 text-slate-700'"
        >
          {{ tab.badge }}
        </span>
      </button>
    </div>

    <!-- TAB 1: DHCP SERVER CONFIGURATION -->
    <div v-if="activeTab === 'dhcp'" class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Left 2 Cols: Main DHCP Server Settings -->
      <div class="lg:col-span-2 space-y-6">
        <div class="bg-white border border-slate-200 rounded-xl shadow-xs overflow-hidden">
          <div class="p-4 border-b border-slate-200 bg-slate-50 flex items-center justify-between">
            <div class="flex items-center gap-2">
              <span class="w-1.5 h-4 bg-[#0072ce] rounded-xs"></span>
              <h2 class="text-sm font-bold text-slate-800">DHCP Server Global Settings</h2>
            </div>
            <!-- Global DHCP Switch -->
            <label class="relative inline-flex items-center cursor-pointer">
              <input type="checkbox" v-model="dhcpConfig.enabled" @change="saveDhcpSettings" class="sr-only peer" />
              <div class="w-11 h-6 bg-slate-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-slate-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-[#0072ce]"></div>
              <span class="ml-2 text-xs font-bold" :class="dhcpConfig.enabled ? 'text-emerald-600' : 'text-slate-400'">
                {{ dhcpConfig.enabled ? 'Enabled' : 'Disabled' }}
              </span>
            </label>
          </div>

          <div class="p-6 space-y-5 text-xs">
            <!-- Listening Interface & Subnet -->
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1">Serving Interface</label>
                <select v-model="dhcpConfig.interface" class="w-full bg-white border border-slate-300 rounded-lg px-3 py-2 text-xs text-slate-800 focus:ring-2 focus:ring-blue-500 focus:outline-none font-medium">
                  <option value="eth0">eth0 (Internal LAN - 192.168.1.1/24)</option>
                  <option value="eth1">eth1 (DMZ - 10.0.10.1/24)</option>
                  <option value="eth2">eth2 (Guest WiFi - 172.16.20.1/24)</option>
                  <option value="br0">br0 (Bridge Interface - 192.168.2.1/24)</option>
                </select>
              </div>

              <div>
                <label class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1">Domain Name</label>
                <input type="text" v-model="dhcpConfig.domain_name" placeholder="internal.medric.net" class="w-full bg-white border border-slate-300 rounded-lg px-3 py-2 text-xs text-slate-800 focus:ring-2 focus:ring-blue-500 focus:outline-none" />
              </div>
            </div>

            <!-- IP Range Pool -->
            <div class="p-4 bg-slate-50 border border-slate-200 rounded-lg space-y-3">
              <div class="text-xs font-bold text-slate-700 flex items-center gap-1.5">
                <svg class="w-4 h-4 text-[#0072ce]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                </svg>
                <span>Dynamic IPv4 Lease Range</span>
              </div>
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label class="block text-[11px] font-semibold text-slate-600 mb-1">Range Start IP</label>
                  <input type="text" v-model="dhcpConfig.range_start" class="w-full bg-white border border-slate-300 rounded-md px-3 py-1.5 text-xs font-mono text-slate-800 focus:ring-2 focus:ring-blue-500 focus:outline-none" />
                </div>
                <div>
                  <label class="block text-[11px] font-semibold text-slate-600 mb-1">Range End IP</label>
                  <input type="text" v-model="dhcpConfig.range_end" class="w-full bg-white border border-slate-300 rounded-md px-3 py-1.5 text-xs font-mono text-slate-800 focus:ring-2 focus:ring-blue-500 focus:outline-none" />
                </div>
              </div>
            </div>

            <!-- Gateway & DNS Options -->
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <div>
                <label class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1">Default Gateway (Router)</label>
                <input type="text" v-model="dhcpConfig.gateway" class="w-full bg-white border border-slate-300 rounded-lg px-3 py-2 text-xs font-mono text-slate-800 focus:ring-2 focus:ring-blue-500 focus:outline-none" />
              </div>
              <div>
                <label class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1">Primary DNS</label>
                <input type="text" v-model="dhcpConfig.dns_primary" class="w-full bg-white border border-slate-300 rounded-lg px-3 py-2 text-xs font-mono text-slate-800 focus:ring-2 focus:ring-blue-500 focus:outline-none" />
              </div>
              <div>
                <label class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1">Secondary DNS</label>
                <input type="text" v-model="dhcpConfig.dns_secondary" class="w-full bg-white border border-slate-300 rounded-lg px-3 py-2 text-xs font-mono text-slate-800 focus:ring-2 focus:ring-blue-500 focus:outline-none" />
              </div>
            </div>

            <!-- Lease Time & IPv6 Support -->
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 items-center">
              <div>
                <label class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1">Default Lease Duration (Hours)</label>
                <div class="flex items-center gap-2">
                  <input type="number" v-model.number="dhcpConfig.lease_time_hours" min="1" max="720" class="w-28 bg-white border border-slate-300 rounded-lg px-3 py-2 text-xs font-mono text-slate-800 focus:ring-2 focus:ring-blue-500 focus:outline-none" />
                  <span class="text-xs text-slate-500">hours (Default: 24h)</span>
                </div>
              </div>

              <div class="flex items-center gap-3 pt-4">
                <input type="checkbox" id="ipv6_stateful" v-model="dhcpConfig.ipv6_enabled" class="rounded text-[#0072ce] focus:ring-blue-500 h-4 w-4" />
                <label for="ipv6_stateful" class="text-xs font-bold text-slate-700 cursor-pointer">
                  Enable DHCPv6 Stateful Addressing &amp; SLAAC RA
                </label>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Right 1 Col: Quick Status & DHCP Relay Option -->
      <div class="space-y-6">
        <!-- Live Pool Utilization Card -->
        <div class="bg-white border border-slate-200 rounded-xl p-5 shadow-xs space-y-4">
          <h3 class="text-xs font-bold text-slate-800 uppercase tracking-wider flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-emerald-500"></span>
            <span>DHCP Pool Status</span>
          </h3>

          <div class="space-y-2">
            <div class="flex justify-between text-xs font-medium">
              <span class="text-slate-600">Active Leases:</span>
              <span class="font-bold text-slate-900">{{ activeLeasesCount }} / {{ totalPoolSize }}</span>
            </div>
            <div class="w-full bg-slate-100 rounded-full h-2.5 overflow-hidden">
              <div class="bg-[#0072ce] h-2.5 rounded-full transition-all duration-500" :style="{ width: `${poolUtilizationPct}%` }"></div>
            </div>
            <div class="text-[11px] text-right text-slate-500 font-mono">{{ poolUtilizationPct }}% Allocated</div>
          </div>

          <div class="pt-3 border-t border-slate-100 space-y-1.5 text-[11px] text-slate-600">
            <div class="flex justify-between">
              <span>Static Reservations:</span>
              <span class="font-bold text-slate-800">{{ staticReservations.length }}</span>
            </div>
            <div class="flex justify-between">
              <span>Subnet Mask:</span>
              <span class="font-mono text-slate-800">255.255.255.0 (/24)</span>
            </div>
            <div class="flex justify-between">
              <span>Broadcast:</span>
              <span class="font-mono text-slate-800">192.168.1.255</span>
            </div>
          </div>
        </div>

        <!-- DHCP Relay Mode Card -->
        <div class="bg-white border border-slate-200 rounded-xl p-5 shadow-xs space-y-3">
          <div class="flex items-center justify-between">
            <h3 class="text-xs font-bold text-slate-800 uppercase tracking-wider">DHCP Relay Agent</h3>
            <input type="checkbox" v-model="dhcpRelay.enabled" class="rounded text-[#0072ce] h-4 w-4" />
          </div>
          <p class="text-[11px] text-slate-500">Forward broadcast DHCP requests to an external enterprise DHCP Server (e.g. Windows Server DHCP).</p>
          <div v-if="dhcpRelay.enabled" class="space-y-2 pt-2">
            <label class="block text-[11px] font-bold text-slate-700">Target DHCP Server IP</label>
            <input type="text" v-model="dhcpRelay.server_ip" placeholder="10.0.0.50" class="w-full bg-white border border-slate-300 rounded-md px-3 py-1.5 text-xs font-mono text-slate-800 focus:ring-2 focus:ring-blue-500 focus:outline-none" />
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 2: STATIC IP RESERVATIONS -->
    <div v-if="activeTab === 'reservations'" class="space-y-4">
      <!-- Search toolbar -->
      <div class="flex items-center justify-between bg-white p-3.5 rounded-xl border border-slate-200 shadow-xs text-xs">
        <div class="relative w-72">
          <input
            v-model="resSearchQuery"
            type="text"
            placeholder="Search hostnames, MACs, reserved IPs..."
            class="w-full pl-8 pr-3 py-1.5 bg-slate-50 border border-slate-200 rounded-lg text-xs focus:bg-white focus:border-[#0072ce] focus:outline-none"
          />
          <svg class="w-4 h-4 text-slate-400 absolute left-2.5 top-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </div>
        <span class="font-mono text-slate-500 font-bold">Showing {{ filteredReservations.length }} of {{ staticReservations.length }}</span>
      </div>

      <div class="bg-white border border-slate-200 rounded-xl shadow-xs overflow-hidden">
        <div class="overflow-x-auto">
          <table class="w-full text-left text-xs text-slate-700">
            <thead class="bg-slate-100/75 border-b border-slate-200 text-[11px] font-bold text-slate-600 uppercase tracking-wider">
              <tr>
                <th class="py-3 px-4">Hostname / Device</th>
                <th class="py-3 px-4 font-mono">MAC Address</th>
                <th class="py-3 px-4 font-mono">Reserved IP Address</th>
                <th class="py-3 px-4">Comment</th>
                <th class="py-3 px-4">Status</th>
                <th class="py-3 px-4 text-right pr-4">Actions</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100 font-medium">
              <tr v-for="res in filteredReservations" :key="res.id" class="hover:bg-slate-50/80 transition-colors">
                <td class="py-3 px-4 font-bold text-slate-900 flex items-center gap-2">
                  <span class="w-2 h-2 rounded-full bg-[#0072ce]"></span>
                  <span>{{ res.hostname }}</span>
                </td>
                <td class="py-3 px-4 font-mono text-slate-600">{{ res.mac }}</td>
                <td class="py-3 px-4 font-mono font-bold text-blue-700">{{ res.ip }}</td>
                <td class="py-3 px-4 text-slate-500">{{ res.comment || '—' }}</td>
                <td class="py-3 px-4">
                  <span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-100 text-emerald-800">
                    Active
                  </span>
                </td>
                <td class="py-3 px-4 text-right pr-4 space-x-1.5 whitespace-nowrap">
                  <button @click="editReservation(res)" class="px-2 py-1 bg-white hover:bg-slate-50 text-slate-700 border border-slate-300 rounded text-[11px] font-bold shadow-2xs cursor-pointer">Edit</button>
                  <button @click="cloneReservation(res)" class="px-2 py-1 bg-white hover:bg-slate-50 text-amber-700 border border-slate-300 rounded text-[11px] font-bold shadow-2xs cursor-pointer">Clone</button>
                  <button @click="deleteReservation(res.id)" class="px-2 py-1 bg-white hover:bg-rose-50 text-rose-600 border border-rose-200 rounded text-[11px] font-bold shadow-2xs cursor-pointer">Delete</button>
                </td>
              </tr>
              <tr v-if="filteredReservations.length === 0">
                <td colspan="6" class="py-8 text-center text-slate-400">No static reservations configured. Click '+ Add Reservation...' to map a MAC to an IP.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- TAB 3: LIVE DHCP LEASES -->
    <div v-if="activeTab === 'leases'" class="space-y-4">
      <div class="bg-white border border-slate-200 rounded-xl shadow-xs overflow-hidden">
        <div class="overflow-x-auto">
          <table class="w-full text-left text-xs text-slate-700">
            <thead class="bg-slate-100/75 border-b border-slate-200 text-[11px] font-bold text-slate-600 uppercase tracking-wider">
              <tr>
                <th class="py-3 px-4">Client Hostname</th>
                <th class="py-3 px-4 font-mono">Assigned IP</th>
                <th class="py-3 px-4 font-mono">MAC Address</th>
                <th class="py-3 px-4">Vendor / Device</th>
                <th class="py-3 px-4 font-mono">Lease Expiration</th>
                <th class="py-3 px-4 text-right pr-4">Quick Action</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100 font-medium">
              <tr v-for="lease in activeLeases" :key="lease.mac" class="hover:bg-slate-50/80 transition-colors">
                <td class="py-3 px-4 font-bold text-slate-900">{{ lease.hostname || '(Unknown Host)' }}</td>
                <td class="py-3 px-4 font-mono font-bold text-blue-700">{{ lease.ip }}</td>
                <td class="py-3 px-4 font-mono text-slate-600">{{ lease.mac }}</td>
                <td class="py-3 px-4">
                  <span class="px-2 py-0.5 rounded text-[10px] font-mono bg-slate-100 text-slate-700 border border-slate-200">
                    {{ lease.vendor || 'Generic Device' }}
                  </span>
                </td>
                <td class="py-3 px-4 text-slate-500 font-mono text-[11px]">{{ lease.expires }}</td>
                <td class="py-3 px-4 text-right pr-4 space-x-1.5">
                  <button
                    @click="convertLeaseToStatic(lease)"
                    class="px-2.5 py-1 bg-blue-50 text-[#0072ce] hover:bg-blue-100 rounded border border-blue-200 text-[11px] font-bold cursor-pointer"
                  >
                    Make Static
                  </button>
                  <button
                    @click="releaseLease(lease.ip)"
                    class="px-2 py-1 bg-white text-rose-600 hover:bg-rose-50 rounded border border-rose-200 text-[11px] font-bold cursor-pointer ml-1"
                  >
                    Release
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- TAB 4: DNS RESOLVER & FORWARDERS -->
    <div v-if="activeTab === 'dns'" class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <div class="lg:col-span-2 space-y-6">
        <div class="bg-white border border-slate-200 rounded-xl shadow-xs overflow-hidden">
          <div class="p-4 border-b border-slate-200 bg-slate-50 flex items-center justify-between">
            <div class="flex items-center gap-2">
              <span class="w-1.5 h-4 bg-[#0072ce] rounded-xs"></span>
              <h2 class="text-sm font-bold text-slate-800">Upstream DNS Forwarders &amp; Cache</h2>
            </div>
            <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-100 text-emerald-800">
              DNSSEC Active
            </span>
          </div>

          <div class="p-6 space-y-5 text-xs">
            <!-- Upstream DNS Forwarders List -->
            <div>
              <label class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-2">Upstream DNS Server IPs</label>
              <div class="space-y-2">
                <div v-for="(fw, idx) in dnsConfig.forwarders" :key="idx" class="flex items-center gap-2">
                  <input type="text" v-model="dnsConfig.forwarders[idx]" class="w-full bg-white border border-slate-300 rounded-lg px-3 py-2 text-xs font-mono text-slate-800 focus:ring-2 focus:ring-blue-500 focus:outline-none" />
                  <button @click="removeDnsForwarder(idx)" type="button" class="p-2 text-slate-400 hover:text-rose-600 cursor-pointer">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                  </button>
                </div>
              </div>
              <button
                type="button"
                @click="addDnsForwarder"
                class="mt-2 text-xs font-bold text-[#0072ce] hover:underline flex items-center gap-1 cursor-pointer"
              >
                + Add Forwarder IP
              </button>
            </div>

            <!-- DNSSEC & Caching Options -->
            <div class="p-4 bg-slate-50 border border-slate-200 rounded-lg space-y-3">
              <div class="flex items-center justify-between">
                <div>
                  <div class="text-xs font-bold text-slate-800">DNSSEC Validation</div>
                  <div class="text-[11px] text-slate-500">Cryptographically validate upstream DNS responses to prevent DNS spoofing.</div>
                </div>
                <input type="checkbox" v-model="dnsConfig.dnssec" class="rounded text-[#0072ce] h-4 w-4" />
              </div>

              <div class="flex items-center justify-between pt-2 border-t border-slate-200">
                <div>
                  <div class="text-xs font-bold text-slate-800">DNS Query Logging</div>
                  <div class="text-[11px] text-slate-500">Log all incoming LAN client DNS queries for reporting and security analytics.</div>
                </div>
                <input type="checkbox" v-model="dnsConfig.query_logging" class="rounded text-[#0072ce] h-4 w-4" />
              </div>

              <div class="pt-2 border-t border-slate-200 grid grid-cols-2 gap-4">
                <div>
                  <label class="block text-[11px] font-bold text-slate-700 mb-1">Cache Size (Entries)</label>
                  <input type="number" v-model.number="dnsConfig.cache_size" class="w-full bg-white border border-slate-300 rounded-md px-3 py-1.5 text-xs font-mono text-slate-800" />
                </div>
                <div>
                  <label class="block text-[11px] font-bold text-slate-700 mb-1">Max TTL (Seconds)</label>
                  <input type="number" v-model.number="dnsConfig.max_ttl" class="w-full bg-white border border-slate-300 rounded-md px-3 py-1.5 text-xs font-mono text-slate-800" />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Right Col: DNS Quick Providers Preset -->
      <div class="space-y-4">
        <div class="bg-white border border-slate-200 rounded-xl p-5 shadow-xs space-y-3">
          <h3 class="text-xs font-bold text-slate-800 uppercase tracking-wider">Fast Presets</h3>
          <div class="space-y-2">
            <button
              type="button"
              @click="applyDnsPreset(['1.1.1.1', '1.0.0.1'])"
              class="w-full text-left p-2.5 rounded-lg border border-slate-200 hover:border-blue-300 hover:bg-blue-50/50 text-xs transition-colors cursor-pointer"
            >
              <div class="font-bold text-slate-800">Cloudflare DNS (Fast &amp; Private)</div>
              <div class="text-[10px] font-mono text-slate-500">1.1.1.1, 1.0.0.1</div>
            </button>
            <button
              type="button"
              @click="applyDnsPreset(['8.8.8.8', '8.8.4.4'])"
              class="w-full text-left p-2.5 rounded-lg border border-slate-200 hover:border-blue-300 hover:bg-blue-50/50 text-xs transition-colors cursor-pointer"
            >
              <div class="font-bold text-slate-800">Google Public DNS</div>
              <div class="text-[10px] font-mono text-slate-500">8.8.8.8, 8.8.4.4</div>
            </button>
            <button
              type="button"
              @click="applyDnsPreset(['9.9.9.9', '149.112.112.112'])"
              class="w-full text-left p-2.5 rounded-lg border border-slate-200 hover:border-blue-300 hover:bg-blue-50/50 text-xs transition-colors cursor-pointer"
            >
              <div class="font-bold text-slate-800">Quad9 (Malware Blocking)</div>
              <div class="text-[10px] font-mono text-slate-500">9.9.9.9, 149.112.112.112</div>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 5: STATIC DNS RECORDS -->
    <div v-if="activeTab === 'static_dns'" class="space-y-4">
      <div class="bg-white border border-slate-200 rounded-xl shadow-xs overflow-hidden">
        <div class="overflow-x-auto">
          <table class="w-full text-left text-xs text-slate-700">
            <thead class="bg-slate-100/75 border-b border-slate-200 text-[11px] font-bold text-slate-600 uppercase tracking-wider">
              <tr>
                <th class="py-3 px-4">FQDN / Hostname</th>
                <th class="py-3 px-4 font-mono">Target IP Address</th>
                <th class="py-3 px-4">Type</th>
                <th class="py-3 px-4">Description</th>
                <th class="py-3 px-4 text-right pr-4">Actions</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100 font-medium">
              <tr v-for="rec in staticDnsRecords" :key="rec.id" class="hover:bg-slate-50/80 transition-colors">
                <td class="py-3 px-4 font-bold text-slate-900">{{ rec.hostname }}</td>
                <td class="py-3 px-4 font-mono font-bold text-blue-700">{{ rec.ip }}</td>
                <td class="py-3 px-4"><span class="px-2 py-0.5 bg-slate-100 rounded text-[10px] font-bold font-mono">A Record</span></td>
                <td class="py-3 px-4 text-slate-500">{{ rec.description || '—' }}</td>
                <td class="py-3 px-4 text-right pr-4 space-x-1.5 whitespace-nowrap">
                  <button @click="editDnsRecord(rec)" class="px-2 py-1 bg-white hover:bg-slate-50 text-slate-700 border border-slate-300 rounded text-[11px] font-bold shadow-2xs cursor-pointer">Edit</button>
                  <button @click="cloneDnsRecord(rec)" class="px-2 py-1 bg-white hover:bg-slate-50 text-amber-700 border border-slate-300 rounded text-[11px] font-bold shadow-2xs cursor-pointer">Clone</button>
                  <button @click="deleteDnsRecord(rec.id)" class="px-2 py-1 bg-white hover:bg-rose-50 text-rose-600 border border-rose-200 rounded text-[11px] font-bold shadow-2xs cursor-pointer">Delete</button>
                </td>
              </tr>
              <tr v-if="staticDnsRecords.length === 0">
                <td colspan="5" class="py-8 text-center text-slate-400">No static local DNS records configured.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- TAB 6: DYNAMIC DNS (DYNDNS) -->
    <div v-if="activeTab === 'dyndns'" class="space-y-6">
      <div class="bg-white border border-slate-200 rounded-xl shadow-xs overflow-hidden">
        <div class="p-4 border-b border-slate-200 bg-slate-50 flex items-center justify-between">
          <div>
            <h2 class="text-sm font-bold text-slate-800">Dynamic DNS (DynDNS) Client</h2>
            <p class="text-xs text-slate-500">Automatically update external domain A records when your WAN IP changes.</p>
          </div>
          <label class="relative inline-flex items-center cursor-pointer">
            <input type="checkbox" v-model="dyndnsConfig.enabled" class="sr-only peer" />
            <div class="w-11 h-6 bg-slate-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-slate-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-[#0072ce]"></div>
          </label>
        </div>

        <div class="p-6 space-y-4 text-xs">
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1">Service Provider</label>
              <select v-model="dyndnsConfig.provider" class="w-full bg-white border border-slate-300 rounded-lg px-3 py-2 text-xs font-medium text-slate-800 focus:ring-2 focus:ring-blue-500 focus:outline-none">
                <option value="cloudflare">Cloudflare API</option>
                <option value="noip">No-IP.com</option>
                <option value="dyndns">DynDNS.org</option>
                <option value="duckdns">DuckDNS</option>
                <option value="namecheap">Namecheap</option>
                <option value="custom">Custom HTTP Update URL</option>
              </select>
            </div>
            <div>
              <label class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1">Domain / Hostname to Update</label>
              <input type="text" v-model="dyndnsConfig.hostname" placeholder="home.medric.net" class="w-full bg-white border border-slate-300 rounded-lg px-3 py-2 text-xs font-mono text-slate-800 focus:ring-2 focus:ring-blue-500 focus:outline-none" />
            </div>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1">Username / Account Email</label>
              <input type="text" v-model="dyndnsConfig.username" class="w-full bg-white border border-slate-300 rounded-lg px-3 py-2 text-xs text-slate-800 focus:ring-2 focus:ring-blue-500 focus:outline-none" />
            </div>
            <div>
              <label class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1">Password / API Secret Token</label>
              <input type="password" v-model="dyndnsConfig.password" class="w-full bg-white border border-slate-300 rounded-lg px-3 py-2 text-xs font-mono text-slate-800 focus:ring-2 focus:ring-blue-500 focus:outline-none" />
            </div>
          </div>

          <div class="pt-4 border-t border-slate-200 flex justify-end gap-3">
            <button
              type="button"
              @click="forceDyndnsUpdate"
              class="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-lg text-xs font-bold cursor-pointer"
            >
              Force DynDNS Sync Now
            </button>
            <button
              type="button"
              @click="saveDyndnsSettings"
              class="px-5 py-2 bg-[#0072ce] hover:bg-blue-700 text-white rounded-lg text-xs font-bold shadow-xs cursor-pointer"
            >
              Save DynDNS Settings
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 7: NTP TIME SYNCHRONIZATION -->
    <div v-if="activeTab === 'ntp'" class="space-y-6">
      <div class="bg-white border border-slate-200 rounded-xl shadow-xs overflow-hidden">
        <div class="p-4 border-b border-slate-200 bg-slate-50 flex items-center justify-between">
          <div class="flex items-center gap-2">
            <span class="w-1.5 h-4 bg-[#0072ce] rounded-xs"></span>
            <h2 class="text-sm font-bold text-slate-800">Network Time Protocol (NTP) Time Daemon</h2>
          </div>
          <span class="text-xs font-mono font-bold text-slate-600 bg-slate-100 px-2 py-1 rounded">
            UTC-4 (Eastern Time)
          </span>
        </div>

        <div class="p-6 space-y-4 text-xs">
          <div>
            <label class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1">Upstream NTP Servers (1 per line)</label>
            <textarea
              v-model="ntpConfig.servers"
              rows="3"
              class="w-full bg-white border border-slate-300 rounded-lg p-3 text-xs font-mono text-slate-800 focus:ring-2 focus:ring-blue-500 focus:outline-none leading-relaxed"
            ></textarea>
          </div>

          <div class="flex items-center justify-between pt-2">
            <div class="flex items-center gap-2">
              <input type="checkbox" id="serve_ntp" v-model="ntpConfig.serve_clients" class="rounded text-[#0072ce] h-4 w-4" />
              <label for="serve_ntp" class="text-xs font-bold text-slate-700 cursor-pointer">
                Serve NTP time synchronization to local LAN clients (Port 123)
              </label>
            </div>
            <button
              type="button"
              @click="syncNtpNow"
              class="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-lg text-xs font-bold cursor-pointer"
            >
              Sync System Clock Now
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- MODAL: ADD / EDIT STATIC RESERVATION -->
    <transition
      enter-active-class="transition duration-150 ease-out"
      enter-from-class="opacity-0 scale-95"
      enter-to-class="opacity-100 scale-100"
      leave-active-class="transition duration-100 ease-in"
      leave-from-class="opacity-100 scale-100"
      leave-to-class="opacity-0 scale-95"
    >
      <div
        v-if="isReservationModalOpen"
        class="fixed inset-0 z-40 overflow-y-auto bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4"
        @keydown.esc="isReservationModalOpen = false"
      >
        <div class="bg-white rounded-2xl shadow-2xl border border-slate-200 max-w-md w-full overflow-hidden flex flex-col my-6">
          <div class="px-5 py-3.5 bg-slate-900 text-white flex items-center justify-between border-b border-slate-800">
            <h3 class="text-xs font-bold uppercase tracking-wider text-white">
              {{ editingResId ? 'Edit Static Reservation' : 'Add Static DHCP Reservation' }}
            </h3>
            <button @click="isReservationModalOpen = false" class="text-slate-400 hover:text-white font-bold cursor-pointer">&times;</button>
          </div>
          <form @submit.prevent="saveReservation" class="p-5 space-y-3.5 text-xs">
            <!-- Host Definition Quick Picker -->
            <div v-if="networkDefs.length > 0" class="p-2.5 bg-blue-50/60 rounded-xl border border-blue-200/80 space-y-1.5">
              <div class="flex items-center justify-between">
                <span class="font-bold text-slate-800 text-[11px]">Choose from Existing Host Definitions</span>
                <button
                  type="button"
                  @click="openInlineHostModal('reservation')"
                  class="text-[10px] text-[#0072ce] hover:underline font-bold cursor-pointer"
                >
                  + New Host Object...
                </button>
              </div>
              <select
                @change="onSelectHostForReservation"
                class="w-full p-1.5 border border-slate-300 rounded bg-white text-xs font-mono"
              >
                <option value="">-- Autofill from Host Object --</option>
                <option v-for="net in networkDefs" :key="'res-net-' + net.id" :value="net.address + '|' + net.name">
                  🖥️ {{ net.name }} ({{ net.address }})
                </option>
              </select>
            </div>

            <div>
              <label class="block font-bold text-slate-700 mb-1">Hostname / Device Name *</label>
              <input type="text" required v-model="formRes.hostname" placeholder="e.g. synology-nas" class="w-full p-2 border border-slate-300 rounded focus:border-[#0072ce] focus:outline-none" />
            </div>
            <div>
              <label class="block font-bold text-slate-700 mb-1">MAC Address *</label>
              <input type="text" required v-model="formRes.mac" placeholder="e.g. 00:11:32:4A:BC:88" class="w-full p-2 border border-slate-300 rounded font-mono focus:border-[#0072ce] focus:outline-none" />
            </div>
            <div>
              <label class="block font-bold text-slate-700 mb-1">Reserved IPv4 Address *</label>
              <input type="text" required v-model="formRes.ip" placeholder="e.g. 192.168.1.10" class="w-full p-2 border border-slate-300 rounded font-mono focus:border-[#0072ce] focus:outline-none" />
            </div>
            <div>
              <label class="block font-bold text-slate-700 mb-1">Comment</label>
              <input type="text" v-model="formRes.comment" placeholder="Optional notes" class="w-full p-2 border border-slate-300 rounded focus:border-[#0072ce] focus:outline-none" />
            </div>
            <div class="pt-3 border-t border-slate-200 flex justify-between">
              <button type="button" @click="isReservationModalOpen = false" class="px-3.5 py-1.5 border border-slate-300 rounded text-slate-700 hover:bg-slate-50 cursor-pointer">Cancel</button>
              <button type="submit" class="px-4 py-1.5 bg-[#0072ce] hover:bg-blue-700 text-white font-bold rounded shadow-xs cursor-pointer">Save Reservation</button>
            </div>
          </form>
        </div>
      </div>
    </transition>

    <!-- MODAL: ADD / EDIT STATIC DNS RECORD -->
    <transition
      enter-active-class="transition duration-150 ease-out"
      enter-from-class="opacity-0 scale-95"
      enter-to-class="opacity-100 scale-100"
      leave-active-class="transition duration-100 ease-in"
      leave-from-class="opacity-100 scale-100"
      leave-to-class="opacity-0 scale-95"
    >
      <div
        v-if="isDnsModalOpen"
        class="fixed inset-0 z-40 overflow-y-auto bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4"
        @keydown.esc="isDnsModalOpen = false"
      >
        <div class="bg-white rounded-2xl shadow-2xl border border-slate-200 max-w-md w-full overflow-hidden flex flex-col my-6">
          <div class="px-5 py-3.5 bg-slate-900 text-white flex items-center justify-between border-b border-slate-800">
            <h3 class="text-xs font-bold uppercase tracking-wider text-white">
              {{ editingDnsId ? 'Edit DNS Record' : 'Add Static DNS Host' }}
            </h3>
            <button @click="isDnsModalOpen = false" class="text-slate-400 hover:text-white font-bold cursor-pointer">&times;</button>
          </div>
          <form @submit.prevent="saveDnsRecord" class="p-5 space-y-3.5 text-xs">
            <!-- Host Definition Quick Picker -->
            <div v-if="networkDefs.length > 0" class="p-2.5 bg-blue-50/60 rounded-xl border border-blue-200/80 space-y-1.5">
              <div class="flex items-center justify-between">
                <span class="font-bold text-slate-800 text-[11px]">Choose from Existing Host Definitions</span>
                <button
                  type="button"
                  @click="openInlineHostModal('dns')"
                  class="text-[10px] text-[#0072ce] hover:underline font-bold cursor-pointer"
                >
                  + New Host Object...
                </button>
              </div>
              <select
                @change="onSelectHostForDns"
                class="w-full p-1.5 border border-slate-300 rounded bg-white text-xs font-mono"
              >
                <option value="">-- Autofill from Host Object --</option>
                <option v-for="net in networkDefs" :key="'dns-net-' + net.id" :value="net.address">
                  🖥️ {{ net.name }} ({{ net.address }})
                </option>
              </select>
            </div>

            <div>
              <label class="block font-bold text-slate-700 mb-1">FQDN / Hostname *</label>
              <input type="text" required v-model="formDns.hostname" placeholder="e.g. app.internal.medric.net" class="w-full p-2 border border-slate-300 rounded font-mono focus:border-[#0072ce] focus:outline-none" />
            </div>
            <div>
              <label class="block font-bold text-slate-700 mb-1">Target IP Address *</label>
              <input type="text" required v-model="formDns.ip" placeholder="e.g. 192.168.1.50" class="w-full p-2 border border-slate-300 rounded font-mono focus:border-[#0072ce] focus:outline-none" />
            </div>
            <div>
              <label class="block font-bold text-slate-700 mb-1">Description</label>
              <input type="text" v-model="formDns.description" placeholder="Optional notes" class="w-full p-2 border border-slate-300 rounded focus:border-[#0072ce] focus:outline-none" />
            </div>
            <div class="pt-3 border-t border-slate-200 flex justify-between">
              <button type="button" @click="isDnsModalOpen = false" class="px-3.5 py-1.5 border border-slate-300 rounded text-slate-700 hover:bg-slate-50 cursor-pointer">Cancel</button>
              <button type="submit" class="px-4 py-1.5 bg-[#0072ce] hover:bg-blue-700 text-white font-bold rounded shadow-xs cursor-pointer">Save Record</button>
            </div>
          </form>
        </div>
      </div>
    </transition>

    <!-- INLINE SUB-MODAL: CREATE NEW HOST DEFINITION -->
    <transition
      enter-active-class="transition duration-150 ease-out"
      enter-from-class="opacity-0 scale-95"
      enter-to-class="opacity-100 scale-100"
      leave-active-class="transition duration-100 ease-in"
      leave-from-class="opacity-100 scale-100"
      leave-to-class="opacity-0 scale-95"
    >
      <div
        v-if="isInlineHostModalOpen"
        class="fixed inset-0 z-[100] bg-slate-950/70 backdrop-blur-xs flex items-center justify-center p-4"
        @keydown.esc="isInlineHostModalOpen = false"
      >
        <div class="w-full max-w-md bg-white rounded-2xl border border-slate-200 shadow-2xl overflow-hidden flex flex-col">
          <div class="bg-slate-900 text-white px-5 py-3.5 flex items-center justify-between border-b border-slate-800">
            <div class="flex items-center gap-2">
              <span class="w-2.5 h-2.5 rounded-full bg-[#ee7f00]"></span>
              <h3 class="text-xs font-bold uppercase tracking-wider text-white">Add Host Definition</h3>
            </div>
            <button @click="isInlineHostModalOpen = false" class="text-slate-400 hover:text-white cursor-pointer font-bold text-base">&times;</button>
          </div>
          <form @submit.prevent="saveInlineHost" class="p-5 space-y-3.5 text-xs text-slate-800">
            <div>
              <label class="block font-bold text-slate-700 mb-1">Host Name *</label>
              <input type="text" required v-model="newInlineHost.name" placeholder="e.g. synology-nas" class="w-full p-2 border border-slate-300 rounded font-medium focus:border-[#0072ce] focus:outline-none" />
            </div>
            <div>
              <label class="block font-bold text-slate-700 mb-1">IPv4 Address *</label>
              <input type="text" required v-model="newInlineHost.address" placeholder="e.g. 192.168.1.10" class="w-full p-2 border border-slate-300 rounded font-mono focus:border-[#0072ce] focus:outline-none" />
            </div>
            <div class="pt-3 border-t border-slate-200 flex justify-between">
              <button type="button" @click="isInlineHostModalOpen = false" class="px-3.5 py-1.5 border border-slate-300 rounded text-slate-700 hover:bg-slate-50 cursor-pointer">Cancel</button>
              <button type="submit" class="px-4 py-1.5 bg-[#0072ce] text-white font-bold rounded shadow-xs cursor-pointer">Save &amp; Use</button>
            </div>
          </form>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, h } from 'vue'

const props = defineProps({
  authToken: {
    type: String,
    default: ''
  }
})

const activeTab = ref('dhcp')
const isSaving = ref(false)
const isLoading = ref(false)
const resSearchQuery = ref('')
const isReservationModalOpen = ref(false)
const isDnsModalOpen = ref(false)
const editingResId = ref(null)
const editingDnsId = ref(null)

const networkDefs = ref([])
const isInlineHostModalOpen = ref(false)
const inlineHostTarget = ref('reservation')
const newInlineHost = ref({ name: '', address: '' })

const formRes = ref({ hostname: '', mac: '', ip: '', comment: '' })
const formDns = ref({ hostname: '', ip: '', description: '' })

const loadNetworkDefs = async () => {
  try {
    const axiosLib = (typeof window !== 'undefined' && window.axios) ? window.axios : null
    if (axiosLib) {
      const res = await axiosLib.get('/api/definitions/networks').catch(() => null)
      if (res && res.data) {
        networkDefs.value = res.data
      }
    }
  } catch (e) {
    console.error('Failed to load network definitions in NetworkServices:', e)
  }
}

const openInlineHostModal = (target = 'reservation') => {
  inlineHostTarget.value = target
  newInlineHost.value = { name: '', address: '' }
  isInlineHostModalOpen.value = true
}

const saveInlineHost = async () => {
  if (!newInlineHost.value.name || !newInlineHost.value.address) return
  const axiosLib = (typeof window !== 'undefined' && window.axios) ? window.axios : null
  if (axiosLib) {
    try {
      await axiosLib.post('/api/definitions/networks', {
        name: newInlineHost.value.name,
        type: 'Host',
        address: newInlineHost.value.address
      })
      await loadNetworkDefs()
    } catch (e) {
      console.error('Failed to create host definition:', e)
    }
  }

  if (inlineHostTarget.value === 'reservation') {
    formRes.value.hostname = newInlineHost.value.name
    formRes.value.ip = newInlineHost.value.address
  } else if (inlineHostTarget.value === 'dns') {
    formDns.value.hostname = `${newInlineHost.value.name}.internal.medric.net`
    formDns.value.ip = newInlineHost.value.address
  }

  isInlineHostModalOpen.value = false
}

const onSelectHostForReservation = (e) => {
  const val = e.target.value
  if (val) {
    const [ip, name] = val.split('|')
    formRes.value.ip = ip || ''
    formRes.value.hostname = name || ''
  }
  e.target.value = ''
}

const onSelectHostForDns = (e) => {
  const val = e.target.value
  if (val) {
    formDns.value.ip = val
  }
  e.target.value = ''
}

// Tab icons
const DhcpIcon = {
  render: () => h('svg', { class: 'w-4 h-4', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
    h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M5 12h14M5 12a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v4a2 2 0 01-2 2M5 12a2 2 0 00-2 2v4a2 2 0 002 2h14a2 2 0 002-2v-4a2 2 0 00-2-2m-2-4h.01M17 16h.01' })
  ])
}

const StaticIcon = {
  render: () => h('svg', { class: 'w-4 h-4', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
    h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z' })
  ])
}

const LeasesIcon = {
  render: () => h('svg', { class: 'w-4 h-4', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
    h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M13 10V3L4 14h7v7l9-11h-7z' })
  ])
}

const DnsIcon = {
  render: () => h('svg', { class: 'w-4 h-4', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
    h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9' })
  ])
}

const DynDnsIcon = {
  render: () => h('svg', { class: 'w-4 h-4', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
    h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15' })
  ])
}

const NtpIcon = {
  render: () => h('svg', { class: 'w-4 h-4', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
    h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z' })
  ])
}

const staticReservations = ref([
  { id: 1, hostname: 'medric-nas', mac: '00:11:32:4A:BC:88', ip: '192.168.1.10', comment: 'Synology Core Storage' },
  { id: 2, hostname: 'hp-laserjet', mac: 'A4:5D:36:7E:11:22', ip: '192.168.1.20', comment: 'Office Printer' },
  { id: 3, hostname: 'proxmox-pve-01', mac: 'BC:24:11:88:99:AA', ip: '192.168.1.50', comment: 'Hypervisor Node 1' },
  { id: 4, hostname: 'unifi-ap-hd', mac: '74:83:C2:10:44:90', ip: '192.168.1.5', comment: 'Main Floor Access Point' },
  { id: 5, hostname: 'home-assistant-vm', mac: '52:54:00:12:34:56', ip: '192.168.1.30', comment: 'Home Automation Bridge' }
])

const activeLeases = ref([
  { hostname: 'MacBook-Pro-M3', ip: '192.168.1.105', mac: 'F0:18:98:33:44:55', vendor: 'Apple, Inc.', expires: '21h 14m' },
  { hostname: 'iPhone-15-Pro', ip: '192.168.1.106', mac: '3C:06:30:11:22:33', vendor: 'Apple, Inc.', expires: '18h 05m' },
  { hostname: 'workstation-dev', ip: '192.168.1.110', mac: 'D8:BB:C1:44:55:66', vendor: 'Intel Corp', expires: '23h 59m' },
  { hostname: 'smart-tv-livingroom', ip: '192.168.1.115', mac: '64:16:66:77:88:99', vendor: 'LG Electronics', expires: '12h 30m' },
  { hostname: 'sonos-soundbar', ip: '192.168.1.120', mac: '48:A6:B8:99:AA:BB', vendor: 'Sonos, Inc.', expires: '19h 40m' }
])

const staticDnsRecords = ref([
  { id: 1, hostname: 'router.home.medric.net', ip: '192.168.1.1', description: 'Astaro Next Gateway' },
  { id: 2, hostname: 'nas.internal.medric.net', ip: '192.168.1.10', description: 'Main Storage Cluster' },
  { id: 3, hostname: 'pve.internal.medric.net', ip: '192.168.1.50', description: 'Proxmox VE Web Console' }
])

const tabs = computed(() => [
  { id: 'dhcp', label: 'DHCP Server', icon: DhcpIcon },
  { id: 'reservations', label: 'Static Reservations', icon: StaticIcon, badge: staticReservations.value.length },
  { id: 'leases', label: 'Live Leases', icon: LeasesIcon, badge: activeLeases.value.length },
  { id: 'dns', label: 'DNS Forwarders', icon: DnsIcon },
  { id: 'static_dns', label: 'Static DNS', icon: DnsIcon, badge: staticDnsRecords.value.length },
  { id: 'dyndns', label: 'Dynamic DNS', icon: DynDnsIcon },
  { id: 'ntp', label: 'NTP Time', icon: NtpIcon }
])

const dhcpConfig = ref({
  enabled: true,
  interface: 'eth0',
  range_start: '192.168.1.100',
  range_end: '192.168.1.200',
  gateway: '192.168.1.1',
  dns_primary: '192.168.1.1',
  dns_secondary: '1.1.1.1',
  domain_name: 'internal.medric.net',
  lease_time_hours: 24,
  ipv6_enabled: false
})

const dhcpRelay = ref({
  enabled: false,
  server_ip: ''
})

const dnsConfig = ref({
  forwarders: ['1.1.1.1', '8.8.8.8'],
  dnssec: true,
  query_logging: true,
  cache_size: 10000,
  max_ttl: 86400
})

const dyndnsConfig = ref({
  enabled: true,
  provider: 'cloudflare',
  hostname: 'home.medric.net',
  username: 'admin@medric.net',
  password: '••••••••••••••••'
})

const ntpConfig = ref({
  servers: '0.pool.ntp.org\n1.pool.ntp.org\ntime.cloudflare.com',
  serve_clients: true
})

const totalPoolSize = computed(() => 101)
const activeLeasesCount = computed(() => activeLeases.value.length)
const poolUtilizationPct = computed(() => Math.round((activeLeasesCount.value / totalPoolSize.value) * 100))

const filteredReservations = computed(() => {
  if (!resSearchQuery.value.trim()) return staticReservations.value
  const q = resSearchQuery.value.toLowerCase()
  return staticReservations.value.filter(r =>
    r.hostname.toLowerCase().includes(q) ||
    r.mac.toLowerCase().includes(q) ||
    r.ip.toLowerCase().includes(q) ||
    (r.comment && r.comment.toLowerCase().includes(q))
  )
})

const refreshCurrentTab = () => {
  isLoading.value = true
  setTimeout(() => { isLoading.value = false }, 300)
}

const openAddReservationModal = () => {
  editingResId.value = null
  formRes.value = { hostname: '', mac: '', ip: '', comment: '' }
  isReservationModalOpen.value = true
}

const editReservation = (res) => {
  editingResId.value = res.id
  formRes.value = JSON.parse(JSON.stringify(res))
  isReservationModalOpen.value = true
}

const cloneReservation = (res) => {
  editingResId.value = null
  formRes.value = {
    ...JSON.parse(JSON.stringify(res)),
    id: null,
    hostname: `${res.hostname}-clone`
  }
  isReservationModalOpen.value = true
}

const saveReservation = () => {
  if (editingResId.value) {
    const idx = staticReservations.value.findIndex(r => r.id === editingResId.value)
    if (idx >= 0) staticReservations.value[idx] = { ...formRes.value, id: editingResId.value }
  } else {
    staticReservations.value.push({
      id: Date.now(),
      ...formRes.value
    })
  }
  isReservationModalOpen.value = false
}

const openAddDnsModal = () => {
  editingDnsId.value = null
  formDns.value = { hostname: '', ip: '', description: '' }
  isDnsModalOpen.value = true
}

const editDnsRecord = (rec) => {
  editingDnsId.value = rec.id
  formDns.value = JSON.parse(JSON.stringify(rec))
  isDnsModalOpen.value = true
}

const cloneDnsRecord = (rec) => {
  editingDnsId.value = null
  formDns.value = {
    ...JSON.parse(JSON.stringify(rec)),
    id: null,
    hostname: `clone.${rec.hostname}`
  }
  isDnsModalOpen.value = true
}

const saveDnsRecord = () => {
  if (editingDnsId.value) {
    const idx = staticDnsRecords.value.findIndex(d => d.id === editingDnsId.value)
    if (idx >= 0) staticDnsRecords.value[idx] = { ...formDns.value, id: editingDnsId.value }
  } else {
    staticDnsRecords.value.push({
      id: Date.now(),
      ...formDns.value
    })
  }
  isDnsModalOpen.value = false
}

const fetchDhcpSettings = async () => {
  const axiosLib = (typeof window !== 'undefined' && window.axios) ? window.axios : null
  if (axiosLib) {
    try {
      const res = await axiosLib.get('/api/network-services/dhcp').catch(() => null)
      if (res && res.data) {
        Object.assign(dhcpConfig.value, res.data)
      }
    } catch (e) {
      console.error('Failed to fetch DHCP config:', e)
    }
  } else {
    try {
      const res = await fetch('/api/network-services/dhcp').catch(() => null)
      if (res && res.ok) {
        const data = await res.json()
        if (data) Object.assign(dhcpConfig.value, data)
      }
    } catch (e) {}
  }
}

const fetchDnsSettings = async () => {
  const axiosLib = (typeof window !== 'undefined' && window.axios) ? window.axios : null
  if (axiosLib) {
    try {
      const res = await axiosLib.get('/api/network-services/dns').catch(() => null)
      if (res && res.data) {
        Object.assign(dnsConfig.value, res.data)
      }
    } catch (e) {
      console.error('Failed to fetch DNS config:', e)
    }
  } else {
    try {
      const res = await fetch('/api/network-services/dns').catch(() => null)
      if (res && res.ok) {
        const data = await res.json()
        if (data) Object.assign(dnsConfig.value, data)
      }
    } catch (e) {}
  }
}

const saveDhcpSettings = async () => {
  isSaving.value = true
  try {
    const axiosLib = (typeof window !== 'undefined' && window.axios) ? window.axios : null
    if (axiosLib) {
      await axiosLib.post('/api/network-services/dhcp', dhcpConfig.value)
    } else {
      await fetch('/api/network-services/dhcp', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(dhcpConfig.value)
      })
    }
  } catch (e) {
    console.error('Failed to save DHCP config:', e)
  } finally {
    setTimeout(() => { isSaving.value = false }, 400)
  }
}

const addDnsForwarder = () => {
  dnsConfig.value.forwarders.push('')
}

const removeDnsForwarder = (idx) => {
  dnsConfig.value.forwarders.splice(idx, 1)
}

const applyDnsPreset = (ips) => {
  dnsConfig.value.forwarders = [...ips]
}

const saveDnsSettings = async () => {
  try {
    const axiosLib = (typeof window !== 'undefined' && window.axios) ? window.axios : null
    if (axiosLib) {
      await axiosLib.post('/api/network-services/dns', dnsConfig.value)
    } else {
      await fetch('/api/network-services/dns', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(dnsConfig.value)
      })
    }
  } catch (e) {
    console.error('Failed to save DNS config:', e)
  }
}

const convertLeaseToStatic = (lease) => {
  if (!staticReservations.value.some(r => r.mac.toLowerCase() === lease.mac.toLowerCase())) {
    staticReservations.value.push({
      id: Date.now(),
      hostname: lease.hostname || 'Device',
      mac: lease.mac,
      ip: lease.ip,
      comment: `Converted from lease (${lease.vendor || 'Auto'})`
    })
    activeTab.value = 'reservations'
  }
}

const releaseLease = (ip) => {
  activeLeases.value = activeLeases.value.filter(l => l.ip !== ip)
}

const deleteReservation = (id) => {
  staticReservations.value = staticReservations.value.filter(r => r.id !== id)
}

const deleteDnsRecord = (id) => {
  staticDnsRecords.value = staticDnsRecords.value.filter(d => d.id !== id)
}

const saveDyndnsSettings = async () => {
  alert('DynDNS settings saved.')
}

const forceDyndnsUpdate = () => {
  alert('Forced Dynamic DNS IP synchronization check.')
}

const syncNtpNow = () => {
  alert('Synchronized hardware RTC and system clock with NTP pool.')
}

onMounted(() => {
  loadNetworkDefs()
  fetchDhcpSettings()
  fetchDnsSettings()
})
</script>
