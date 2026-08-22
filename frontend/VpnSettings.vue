<template>
  <div class="space-y-6">
    <!-- Standardized Page Header -->
    <div class="bg-white border border-slate-200 rounded-xl p-5 shadow-xs flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
      <div>
        <div class="flex items-center gap-2.5">
          <span class="w-1.5 h-6 bg-[#ee7f00] rounded-xs inline-block"></span>
          <h1 class="text-xl font-bold text-slate-900 tracking-tight">Site-to-Site &amp; Remote Access VPN</h1>
          <span class="text-[11px] bg-blue-50 text-[#0072ce] font-medium font-mono px-2 py-0.5 rounded border border-blue-200">
            SSL / IPsec / AWS VPC / WireGuard
          </span>
        </div>
        <p class="text-xs text-slate-500 mt-1 pl-4">
          Connect as an SSL client to external servers, establish IPsec &amp; Amazon VPC interconnects, route cross-premises subnets, and provision remote user tunnels.
        </p>
      </div>

      <div class="flex items-center gap-2.5 flex-wrap">
        <button
          type="button"
          @click="fetchData(true)"
          :disabled="isLoading"
          class="px-3.5 py-2 text-xs font-semibold bg-white hover:bg-slate-50 text-slate-700 rounded-lg border border-slate-300 transition-colors flex items-center gap-1.5 shadow-xs cursor-pointer active:bg-slate-100"
          title="Reload active tunnels from kernel daemon"
        >
          <svg :class="['w-3.5 h-3.5 text-slate-500', isLoading ? 'animate-spin text-[#0072ce]' : '']" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          <span>Refresh</span>
        </button>

        <button
          v-if="activeTab === 'remote_users'"
          type="button"
          @click="openAddUserModal"
          class="px-4 py-2 bg-[#0072ce] hover:bg-blue-700 text-white rounded-lg text-xs font-bold shadow-sm flex items-center gap-2 transition-all cursor-pointer"
        >
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
          </svg>
          <span>+ Add Remote User...</span>
        </button>

        <button
          v-else
          type="button"
          @click="openAddTunnelModal(activeTab)"
          class="px-4 py-2 bg-[#0072ce] hover:bg-blue-700 text-white rounded-lg text-xs font-bold shadow-sm flex items-center gap-2 transition-all cursor-pointer"
        >
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          <span>+ New {{ activeTabLabel }}...</span>
        </button>
      </div>
    </div>

    <!-- Telemetry Statistics Strip -->
    <div class="grid grid-cols-2 sm:grid-cols-4 gap-3.5">
      <div class="bg-white p-3.5 rounded-xl border border-slate-200 shadow-xs flex items-center gap-3">
        <div class="w-9 h-9 rounded-lg bg-blue-50 text-[#0072ce] flex items-center justify-center font-bold">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
          </svg>
        </div>
        <div>
          <div class="text-[10px] uppercase font-bold text-slate-400">Site Tunnels</div>
          <div class="text-base font-bold text-slate-900">{{ tunnelsList.length }} Configured</div>
        </div>
      </div>

      <div class="bg-white p-3.5 rounded-xl border border-slate-200 shadow-xs flex items-center gap-3">
        <div class="w-9 h-9 rounded-lg bg-emerald-50 text-emerald-600 flex items-center justify-center font-bold">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <div>
          <div class="text-[10px] uppercase font-bold text-slate-400">Connected Peers</div>
          <div class="text-base font-bold text-emerald-600">{{ activePeersCount }} Active</div>
        </div>
      </div>

      <div class="bg-white p-3.5 rounded-xl border border-slate-200 shadow-xs flex items-center gap-3">
        <div class="w-9 h-9 rounded-lg bg-indigo-50 text-indigo-600 flex items-center justify-center font-bold">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M9 19l3 3m0 0l3-3m-3 3V10" />
          </svg>
        </div>
        <div>
          <div class="text-[10px] uppercase font-bold text-slate-400">Total Data Transfer</div>
          <div class="text-base font-bold text-indigo-700 font-mono">{{ aggregateTransferFormatted }}</div>
        </div>
      </div>

      <div class="bg-white p-3.5 rounded-xl border border-slate-200 shadow-xs flex items-center gap-3">
        <div class="w-9 h-9 rounded-lg bg-purple-50 text-purple-600 flex items-center justify-center font-bold">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
          </svg>
        </div>
        <div>
          <div class="text-[10px] uppercase font-bold text-slate-400">Crypto Engine</div>
          <div class="text-xs font-mono font-bold text-purple-700">TLS 1.3 / AES-GCM / IKEv2</div>
        </div>
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
            placeholder="Search tunnels, gateways, subnets, clients..."
            class="w-full pl-8 pr-3 py-1.5 bg-slate-50 border border-slate-200 rounded-lg text-xs focus:bg-white focus:border-[#0072ce] focus:outline-none"
          />
          <svg class="w-4 h-4 text-slate-400 absolute left-2.5 top-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </div>
      </div>

      <div class="flex items-center gap-4 text-slate-500 font-medium">
        <div class="flex items-center gap-2">
          <span>Filter:</span>
          <select v-model="statusFilter" class="bg-slate-50 border border-slate-200 rounded-lg px-2 py-1 text-xs text-slate-700 font-bold">
            <option value="ALL">All Items</option>
            <option value="ACTIVE">Connected / Active Only</option>
            <option value="INACTIVE">Disabled / Inactive Only</option>
          </select>
        </div>

        <span class="font-mono text-slate-600 font-bold">
          Showing {{ currentFilteredItemsCount }} items
        </span>
      </div>
    </div>

    <!-- TAB 1, 3, 4, 5: SITE-TO-SITE & CLIENT TUNNELS MATRIX -->
    <div v-if="activeTab !== 'remote_users'" class="bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden">
      <div v-if="filteredTunnels.length === 0" class="p-12 text-center text-slate-400 text-xs">
        No VPN tunnels found matching your filter criteria. Click "+ New {{ activeTabLabel }}..." to establish a connection.
      </div>
      <table v-else class="w-full text-left text-xs border-collapse">
        <thead class="bg-[#f4f6f9] text-slate-700 font-bold border-b border-slate-200">
          <tr>
            <th class="p-3 pl-4 w-12 text-center">Status</th>
            <th class="p-3">Tunnel Name</th>
            <th class="p-3">Type / Mode</th>
            <th class="p-3 font-mono">Remote Endpoint / Server</th>
            <th class="p-3 font-mono">Local Network</th>
            <th class="p-3 font-mono">Routed Remote Subnets</th>
            <th class="p-3">Firewall Policy</th>
            <th class="p-3 text-right pr-4">Actions</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-100 font-medium text-slate-700">
          <tr
            v-for="(tun, idx) in filteredTunnels"
            :key="tun.id || tun.tunnel_name || idx"
            :class="idx % 2 === 0 ? 'bg-white' : 'bg-[#f7f7f7]'"
            class="hover:bg-blue-50/40 transition-colors"
          >
            <!-- Status Toggle -->
            <td class="p-3 pl-4 text-center">
              <button
                type="button"
                @click="toggleTunnel(tun)"
                class="relative inline-flex h-4 w-8 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none"
                :class="tun.enabled !== false ? 'bg-emerald-500' : 'bg-slate-300'"
                title="Toggle tunnel status"
              >
                <span
                  class="pointer-events-none inline-block h-3 w-3 transform rounded-full bg-white shadow-xs ring-0 transition duration-200 ease-in-out"
                  :class="tun.enabled !== false ? 'translate-x-4' : 'translate-x-0'"
                ></span>
              </button>
            </td>

            <td class="p-3 font-bold text-slate-900 flex items-center gap-2">
              <span class="w-2 h-2 rounded-full" :class="tun.enabled !== false ? 'bg-emerald-500' : 'bg-slate-400'"></span>
              <span>{{ tun.name || tun.tunnel_name }}</span>
            </td>

            <td class="p-3">
              <span
                :class="[
                  'px-2 py-0.5 rounded text-[10px] font-bold uppercase border',
                  getTunnelTypeBadgeClasses(tun.type || tun.tunnel_type)
                ]"
              >
                {{ formatTunnelType(tun.type || tun.tunnel_type) }}
              </span>
            </td>

            <td class="p-3 font-mono font-semibold text-slate-800">
              {{ tun.remote_gateway || tun.remote_endpoint || 'Any' }}
            </td>

            <td class="p-3 font-mono text-slate-600">
              {{ tun.local_network || tun.local_virtual_ip || '192.168.1.0/24' }}
            </td>

            <td class="p-3 font-mono">
              <div v-if="Array.isArray(tun.remote_subnets)" class="flex items-center gap-1 flex-wrap">
                <span v-for="sub in tun.remote_subnets" :key="sub" class="px-1.5 py-0.2 rounded bg-slate-100 text-slate-700 border border-slate-200 text-[10px]">
                  {{ sub }}
                </span>
              </div>
              <div v-else class="text-blue-700 font-bold">
                {{ tun.remote_network || '10.0.0.0/16' }}
              </div>
            </td>

            <td class="p-3">
              <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-50 text-emerald-700 border border-emerald-200">
                Auto-Permit (Accept)
              </span>
            </td>

            <!-- Standard Action Triplet: Edit | Clone | Delete -->
            <td class="p-3 text-right pr-4 space-x-1.5 whitespace-nowrap">
              <button
                type="button"
                @click="editTunnel(tun)"
                class="px-2 py-1 bg-white hover:bg-slate-50 text-slate-700 border border-slate-300 rounded text-[11px] font-bold shadow-2xs cursor-pointer"
              >
                Edit
              </button>
              <button
                type="button"
                @click="cloneTunnel(tun)"
                class="px-2 py-1 bg-white hover:bg-slate-50 text-amber-700 border border-slate-300 rounded text-[11px] font-bold shadow-2xs cursor-pointer"
              >
                Clone
              </button>
              <button
                type="button"
                @click="deleteTunnel(tun.id || tun.name || tun.tunnel_name)"
                class="px-2 py-1 bg-white hover:bg-rose-50 text-rose-600 border border-rose-200 rounded text-[11px] font-bold shadow-2xs cursor-pointer"
              >
                Delete
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- TAB 2: REMOTE ACCESS VPN (WIREGUARD PEERS) -->
    <div v-else class="bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden">
      <div v-if="filteredPeers.length === 0" class="p-12 text-center text-slate-400 text-xs">
        No remote access user clients configured. Click "+ Add Remote User..." to provision a client profile.
      </div>
      <table v-else class="w-full text-left text-xs border-collapse">
        <thead class="bg-[#f4f6f9] text-slate-700 font-bold border-b border-slate-200">
          <tr>
            <th class="p-3 pl-4">Client User / Hostname</th>
            <th class="p-3 font-mono">Assigned Virtual IP</th>
            <th class="p-3 font-mono">Public Crypto Key</th>
            <th class="p-3">Status</th>
            <th class="p-3 font-mono">Data Transferred</th>
            <th class="p-3 text-right pr-4">Actions</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-100 font-medium text-slate-700">
          <tr
            v-for="(peer, idx) in filteredPeers"
            :key="peer.id || idx"
            :class="idx % 2 === 0 ? 'bg-white' : 'bg-[#f7f7f7]'"
            class="hover:bg-blue-50/40 transition-colors"
          >
            <td class="p-3 pl-4 font-bold text-slate-900 flex items-center gap-2">
              <span class="w-2 h-2 rounded-full" :class="peer.status === 'active' || peer.is_active ? 'bg-emerald-500' : 'bg-slate-400'"></span>
              <span>{{ peer.client_name }}</span>
            </td>

            <td class="p-3 font-mono font-bold text-blue-700">
              {{ peer.virtual_ip }}
            </td>

            <td class="p-3 font-mono text-slate-500 text-[11px] truncate max-w-xs" :title="peer.public_key">
              {{ peer.public_key }}
            </td>

            <td class="p-3">
              <span
                :class="[
                  'px-2 py-0.5 rounded text-[10px] font-bold uppercase border',
                  peer.status === 'active' || peer.is_active
                    ? 'bg-emerald-50 text-emerald-700 border-emerald-200'
                    : 'bg-slate-100 text-slate-600 border-slate-200'
                ]"
              >
                {{ peer.status === 'active' || peer.is_active ? 'Connected' : 'Disconnected' }}
              </span>
            </td>

            <td class="p-3 font-mono text-slate-600">
              {{ formatBytes((peer.transfer_rx || 0) + (peer.transfer_tx || 0)) }}
            </td>

            <td class="p-3 text-right pr-4 space-x-1.5 whitespace-nowrap">
              <button
                type="button"
                @click="downloadPeerConfig(peer)"
                class="px-2 py-1 bg-blue-50 hover:bg-blue-100 text-[#0072ce] border border-blue-200 rounded text-[11px] font-bold shadow-2xs cursor-pointer"
              >
                Download .conf
              </button>
              <button
                type="button"
                @click="deletePeer(peer.id || peer.public_key)"
                class="px-2 py-1 bg-white hover:bg-rose-50 text-rose-600 border border-rose-200 rounded text-[11px] font-bold shadow-2xs cursor-pointer"
              >
                Delete
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- MODAL: ADD / EDIT SITE-TO-SITE & CLIENT VPN TUNNEL -->
    <transition
      enter-active-class="transition duration-150 ease-out"
      enter-from-class="opacity-0 scale-95"
      enter-to-class="opacity-100 scale-100"
      leave-active-class="transition duration-100 ease-in"
      leave-from-class="opacity-100 scale-100"
      leave-to-class="opacity-0 scale-95"
    >
      <div
        v-if="isTunnelModalOpen"
        class="fixed inset-0 z-40 overflow-y-auto bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4"
        @keydown.esc="isTunnelModalOpen = false"
      >
        <div class="bg-white rounded-2xl shadow-2xl border border-slate-200 max-w-xl w-full overflow-hidden flex flex-col my-6 max-h-[90vh]">
          <!-- Modal Header -->
          <div class="px-5 py-3.5 bg-slate-900 text-white flex items-center justify-between border-b border-slate-800">
            <div class="flex items-center gap-2.5">
              <div class="w-8 h-8 rounded-lg bg-[#ee7f00] flex items-center justify-center text-white font-bold text-xs shadow-md">
                VPN
              </div>
              <div>
                <h3 class="text-xs font-bold uppercase tracking-wider text-white">
                  {{ editingTunnelId ? 'Edit VPN Tunnel' : 'Establish Client / Site-to-Site VPN Tunnel' }}
                </h3>
                <p class="text-[10px] text-slate-400">SSL Client, IPsec IKEv2, Amazon VPC, and WireGuard</p>
              </div>
            </div>
            <button @click="isTunnelModalOpen = false" class="text-slate-400 hover:text-white font-bold cursor-pointer text-base leading-none">&times;</button>
          </div>

          <!-- Form Fields -->
          <form @submit.prevent="saveTunnel" class="p-5 space-y-4 text-xs flex-1 overflow-y-auto">
            <div>
              <label class="block font-bold text-slate-700 mb-1">Tunnel Name *</label>
              <input
                v-model="formTunnel.tunnel_name"
                type="text"
                required
                placeholder="e.g. Branch Office SSL Client, AWS Production VPC, HQ Datacenter"
                class="w-full p-2 border border-slate-300 rounded focus:border-[#0072ce] focus:outline-none"
              />
            </div>

            <div class="grid grid-cols-2 gap-3">
              <div>
                <label class="block font-bold text-slate-700 mb-1">Tunnel Type / Protocol</label>
                <select
                  v-model="formTunnel.tunnel_type"
                  class="w-full p-2 border border-slate-300 rounded focus:border-[#0072ce] focus:outline-none bg-white font-medium"
                >
                  <option value="ssl_client">SSL VPN (Client Mode - Connect Outward)</option>
                  <option value="ssl_server">SSL VPN (Server Mode - Accept Inbound)</option>
                  <option value="ipsec">IPsec / IKEv2 (Site-to-Site Gateway)</option>
                  <option value="amazon_vpc">Amazon VPC (AWS Cloud Interconnect)</option>
                  <option value="wireguard">WireGuard (Site-to-Site Peer)</option>
                </select>
              </div>

              <div>
                <label class="block font-bold text-slate-700 mb-1">Initial State</label>
                <select
                  v-model="formTunnel.enabled"
                  class="w-full p-2 border border-slate-300 rounded focus:border-[#0072ce] focus:outline-none bg-white font-medium"
                >
                  <option :value="true">Enabled (Connected)</option>
                  <option :value="false">Disabled</option>
                </select>
              </div>
            </div>

            <!-- TYPE 1: SSL CLIENT MODE (Firewall connects to external SSL/OpenVPN server) -->
            <div v-if="formTunnel.tunnel_type === 'ssl_client'" class="space-y-3 p-3.5 bg-blue-50/50 rounded-xl border border-blue-200">
              <div class="text-[11px] font-bold text-[#0072ce] flex items-center gap-1.5">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                </svg>
                <span>SSL VPN Client Configuration (Outbound Connection)</span>
              </div>

              <div class="grid grid-cols-3 gap-3">
                <div class="col-span-2">
                  <label class="block font-bold text-slate-700 mb-1">Remote Server FQDN / IP *</label>
                  <input
                    v-model="formTunnel.remote_endpoint"
                    type="text"
                    required
                    placeholder="e.g. vpn.remotebranch.com or 198.51.100.10"
                    class="w-full p-2 border border-slate-300 rounded bg-white font-mono"
                  />
                </div>
                <div>
                  <label class="block font-bold text-slate-700 mb-1">Port</label>
                  <input
                    v-model.number="formTunnel.remote_port"
                    type="number"
                    placeholder="1194"
                    class="w-full p-2 border border-slate-300 rounded bg-white font-mono"
                  />
                </div>
              </div>

              <div class="grid grid-cols-2 gap-3">
                <div>
                  <label class="block font-bold text-slate-700 mb-1">Authentication Mode</label>
                  <select v-model="formTunnel.auth_mode" class="w-full p-2 border border-slate-300 rounded bg-white font-medium">
                    <option value="password">Username &amp; Password</option>
                    <option value="certificate">X.509 Certificate (PKI / TLS)</option>
                    <option value="psk">Static Pre-Shared Key</option>
                  </select>
                </div>
                <div>
                  <label class="block font-bold text-slate-700 mb-1">Transport Protocol</label>
                  <select v-model="formTunnel.protocol" class="w-full p-2 border border-slate-300 rounded bg-white font-medium">
                    <option value="UDP">UDP (Fast &amp; Low Latency)</option>
                    <option value="TCP">TCP (Port 443 Firewall Bypass)</option>
                  </select>
                </div>
              </div>

              <div v-if="formTunnel.auth_mode === 'password'" class="grid grid-cols-2 gap-3">
                <div>
                  <label class="block font-bold text-slate-700 mb-1">Client Username *</label>
                  <input v-model="formTunnel.username" type="text" placeholder="astaro-client" class="w-full p-2 border border-slate-300 rounded bg-white" />
                </div>
                <div>
                  <label class="block font-bold text-slate-700 mb-1">Client Password *</label>
                  <input v-model="formTunnel.password" type="password" placeholder="••••••••••••" class="w-full p-2 border border-slate-300 rounded bg-white font-mono" />
                </div>
              </div>

              <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <div>
                  <div class="flex items-center justify-between mb-1">
                    <label class="block font-bold text-slate-700">Local Network (Advertised)</label>
                    <button
                      type="button"
                      @click="openInlineNetModal('local')"
                      class="text-[10px] text-[#0072ce] hover:underline font-bold cursor-pointer"
                    >
                      + New Network Object
                    </button>
                  </div>
                  <div class="space-y-1.5">
                    <select
                      v-if="networkDefs.length > 0"
                      @change="e => { if (e.target.value) formTunnel.local_networks_text = e.target.value }"
                      class="w-full p-1.5 border border-slate-300 rounded bg-white text-xs font-mono"
                    >
                      <option value="">-- Choose Local Definition --</option>
                      <option v-for="net in networkDefs" :key="'loc-' + net.id" :value="net.address || net.name">
                        🌐 {{ net.name }} ({{ net.address }})
                      </option>
                    </select>
                    <input v-model="formTunnel.local_networks_text" type="text" placeholder="192.168.1.0/24" class="w-full p-2 border border-slate-300 rounded bg-white font-mono text-xs" />
                  </div>
                </div>

                <div>
                  <div class="flex items-center justify-between mb-1">
                    <label class="block font-bold text-slate-700">Remote Subnets *</label>
                    <button
                      type="button"
                      @click="openInlineNetModal('remote')"
                      class="text-[10px] text-[#0072ce] hover:underline font-bold cursor-pointer"
                    >
                      + New Network Object
                    </button>
                  </div>
                  <div class="space-y-1.5">
                    <select
                      v-if="networkDefs.length > 0"
                      @change="e => { if (e.target.value) formTunnel.remote_subnets_text = e.target.value }"
                      class="w-full p-1.5 border border-slate-300 rounded bg-white text-xs font-mono"
                    >
                      <option value="">-- Choose Remote Definition --</option>
                      <option v-for="net in networkDefs" :key="'rem-' + net.id" :value="net.address || net.name">
                        🌐 {{ net.name }} ({{ net.address }})
                      </option>
                    </select>
                    <input v-model="formTunnel.remote_subnets_text" type="text" required placeholder="10.50.0.0/16, 172.16.0.0/24" class="w-full p-2 border border-slate-300 rounded bg-white font-mono text-xs" />
                  </div>
                </div>
              </div>

              <div class="space-y-2 pt-1">
                <div class="flex items-center gap-2">
                  <input id="auto_fw_ssl" v-model="formTunnel.auto_firewall_rule" type="checkbox" class="rounded text-[#0072ce] focus:ring-[#0072ce] h-4 w-4 cursor-pointer" />
                  <label for="auto_fw_ssl" class="text-slate-700 font-bold cursor-pointer">
                    Automatic Firewall Rule (Permit bi-directional traffic to &amp; from remote subnets)
                  </label>
                </div>
                <div class="flex items-center gap-2">
                  <input id="default_gw_ssl" v-model="formTunnel.use_default_gateway" type="checkbox" class="rounded text-[#0072ce] focus:ring-[#0072ce] h-4 w-4 cursor-pointer" />
                  <label for="default_gw_ssl" class="text-slate-700 font-bold cursor-pointer">
                    Use as Default Gateway (Route all outbound Internet traffic through remote SSL VPN)
                  </label>
                </div>
              </div>
            </div>

            <!-- TYPE 2: IPSEC IKEV2 -->
            <div v-else-if="formTunnel.tunnel_type === 'ipsec'" class="space-y-3 p-3.5 bg-slate-50 rounded-xl border border-slate-200">
              <div class="text-[11px] font-bold text-slate-800 flex items-center gap-1.5">
                <span>IPsec / IKEv2 Gateway Settings</span>
              </div>
              <div class="grid grid-cols-2 gap-3">
                <div>
                  <label class="block font-bold text-slate-700 mb-1">Remote Gateway IP / Hostname *</label>
                  <input v-model="formTunnel.remote_endpoint" type="text" required placeholder="203.0.113.1" class="w-full p-2 border border-slate-300 rounded bg-white font-mono" />
                </div>
                <div>
                  <label class="block font-bold text-slate-700 mb-1">Pre-Shared Key (PSK) *</label>
                  <input v-model="formTunnel.preshared_key" type="password" required placeholder="SecretKey123!#" class="w-full p-2 border border-slate-300 rounded bg-white font-mono" />
                </div>
              </div>
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <div>
                  <div class="flex items-center justify-between mb-1">
                    <label class="block font-bold text-slate-700">Local Subnets</label>
                    <button
                      type="button"
                      @click="openInlineNetModal('local')"
                      class="text-[10px] text-[#0072ce] hover:underline font-bold cursor-pointer"
                    >
                      + New Network Object
                    </button>
                  </div>
                  <div class="space-y-1.5">
                    <select
                      v-if="networkDefs.length > 0"
                      @change="e => { if (e.target.value) formTunnel.local_networks_text = e.target.value }"
                      class="w-full p-1.5 border border-slate-300 rounded bg-white text-xs font-mono"
                    >
                      <option value="">-- Choose Local Definition --</option>
                      <option v-for="net in networkDefs" :key="'loc-ipsec-' + net.id" :value="net.address || net.name">
                        🌐 {{ net.name }} ({{ net.address }})
                      </option>
                    </select>
                    <input v-model="formTunnel.local_networks_text" type="text" placeholder="192.168.1.0/24" class="w-full p-2 border border-slate-300 rounded bg-white font-mono text-xs" />
                  </div>
                </div>
                <div>
                  <div class="flex items-center justify-between mb-1">
                    <label class="block font-bold text-slate-700">Remote Subnets *</label>
                    <button
                      type="button"
                      @click="openInlineNetModal('remote')"
                      class="text-[10px] text-[#0072ce] hover:underline font-bold cursor-pointer"
                    >
                      + New Network Object
                    </button>
                  </div>
                  <div class="space-y-1.5">
                    <select
                      v-if="networkDefs.length > 0"
                      @change="e => { if (e.target.value) formTunnel.remote_subnets_text = e.target.value }"
                      class="w-full p-1.5 border border-slate-300 rounded bg-white text-xs font-mono"
                    >
                      <option value="">-- Choose Remote Definition --</option>
                      <option v-for="net in networkDefs" :key="'rem-ipsec-' + net.id" :value="net.address || net.name">
                        🌐 {{ net.name }} ({{ net.address }})
                      </option>
                    </select>
                    <input v-model="formTunnel.remote_subnets_text" type="text" required placeholder="10.100.0.0/16" class="w-full p-2 border border-slate-300 rounded bg-white font-mono text-xs" />
                  </div>
                </div>
              </div>
            </div>

            <!-- TYPE 3: AMAZON VPC -->
            <div v-else-if="formTunnel.tunnel_type === 'amazon_vpc'" class="space-y-3 p-3.5 bg-amber-50/50 rounded-xl border border-amber-200">
              <div class="text-[11px] font-bold text-amber-900 flex items-center gap-1.5">
                <span>Amazon AWS VPC Cloud Gateway</span>
              </div>
              <div class="grid grid-cols-2 gap-3">
                <div>
                  <label class="block font-bold text-slate-700 mb-1">AWS Region</label>
                  <select v-model="formTunnel.aws_region" class="w-full p-2 border border-slate-300 rounded bg-white font-medium">
                    <option value="us-east-1">us-east-1 (N. Virginia)</option>
                    <option value="us-east-2">us-east-2 (Ohio)</option>
                    <option value="us-west-2">us-west-2 (Oregon)</option>
                    <option value="eu-west-1">eu-west-1 (Ireland)</option>
                    <option value="eu-central-1">eu-central-1 (Frankfurt)</option>
                  </select>
                </div>
                <div>
                  <label class="block font-bold text-slate-700 mb-1">AWS VPC ID</label>
                  <input v-model="formTunnel.aws_vpc_id" type="text" placeholder="vpc-0a1b2c3d4e5f" class="w-full p-2 border border-slate-300 rounded bg-white font-mono" />
                </div>
              </div>
              <div class="grid grid-cols-2 gap-3">
                <div>
                  <label class="block font-bold text-slate-700 mb-1">AWS VGW / Tunnel IP *</label>
                  <input v-model="formTunnel.remote_endpoint" type="text" required placeholder="52.95.120.45" class="w-full p-2 border border-slate-300 rounded bg-white font-mono" />
                </div>
                <div>
                  <label class="block font-bold text-slate-700 mb-1">AWS VPC CIDR Subnet *</label>
                  <input v-model="formTunnel.remote_subnets_text" type="text" required placeholder="172.31.0.0/16" class="w-full p-2 border border-slate-300 rounded bg-white font-mono" />
                </div>
              </div>
            </div>

            <!-- TYPE 4: WIREGUARD -->
            <div v-else class="space-y-3 p-3.5 bg-purple-50/50 rounded-xl border border-purple-200">
              <div class="text-[11px] font-bold text-purple-900 flex items-center gap-1.5">
                <span>WireGuard Site-to-Site Configuration</span>
              </div>
              <div class="grid grid-cols-2 gap-3">
                <div>
                  <label class="block font-bold text-slate-700 mb-1">Remote Endpoint &amp; Port *</label>
                  <input v-model="formTunnel.remote_endpoint" type="text" required placeholder="vpn.corp.company.com:51820" class="w-full p-2 border border-slate-300 rounded bg-white font-mono" />
                </div>
                <div>
                  <label class="block font-bold text-slate-700 mb-1">Remote Peer Public Key *</label>
                  <input v-model="formTunnel.remote_public_key" type="text" required placeholder="xK8b3s90j12LmOP947vbcKqLmNwz458vBnmQ123aA=" class="w-full p-2 border border-slate-300 rounded bg-white font-mono" />
                </div>
              </div>
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <div>
                  <label class="block font-bold text-slate-700 mb-1">Local Tunnel IP</label>
                  <input v-model="formTunnel.local_virtual_ip" type="text" placeholder="10.250.0.2/30" class="w-full p-2 border border-slate-300 rounded bg-white font-mono text-xs" />
                </div>
                <div>
                  <div class="flex items-center justify-between mb-1">
                    <label class="block font-bold text-slate-700">Allowed Remote Subnets *</label>
                  </div>
                  <div class="space-y-1.5">
                    <select
                      v-if="networkDefs.length > 0"
                      @change="e => { if (e.target.value) formTunnel.remote_subnets_text = e.target.value }"
                      class="w-full p-1.5 border border-slate-300 rounded bg-white text-xs font-mono"
                    >
                      <option value="">-- Choose Remote Definition --</option>
                      <option v-for="net in networkDefs" :key="'rem-wg-' + net.id" :value="net.address || net.name">
                        🌐 {{ net.name }} ({{ net.address }})
                      </option>
                    </select>
                    <input v-model="formTunnel.remote_subnets_text" type="text" required placeholder="10.100.0.0/16, 172.16.0.0/16" class="w-full p-2 border border-slate-300 rounded bg-white font-mono text-xs" />
                  </div>
                </div>
              </div>
            </div>

            <div>
              <label class="block font-bold text-slate-700 mb-1">Comment / Notes</label>
              <input
                v-model="formTunnel.comment"
                type="text"
                placeholder="Optional notes or documentation"
                class="w-full p-2 border border-slate-300 rounded focus:border-[#0072ce] focus:outline-none"
              />
            </div>

            <!-- Modal Footer -->
            <div class="pt-3 border-t border-slate-200 flex items-center justify-between">
              <button
                type="button"
                @click="isTunnelModalOpen = false"
                class="px-3.5 py-1.5 rounded border border-slate-300 bg-white text-slate-700 text-xs font-bold hover:bg-slate-50 cursor-pointer"
              >
                Cancel
              </button>
              <button
                type="submit"
                class="px-4 py-1.5 rounded bg-[#0072ce] hover:bg-blue-700 text-white text-xs font-bold shadow-xs cursor-pointer"
              >
                {{ editingTunnelId ? 'Update Tunnel' : 'Save &amp; Establish Tunnel' }}
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
              <h3 class="text-xs font-bold uppercase tracking-wider text-white">Add Network Definition</h3>
            </div>
            <button @click="isInlineNetModalOpen = false" class="text-slate-400 hover:text-white cursor-pointer font-bold text-base">&times;</button>
          </div>
          <form @submit.prevent="saveInlineNet" class="p-5 space-y-3.5 text-xs text-slate-800">
            <div>
              <label class="block font-bold text-slate-700 mb-1">Name *</label>
              <input type="text" required v-model="newInlineNet.name" placeholder="e.g. Remote Office Subnet" class="w-full p-2 border border-slate-300 rounded font-medium focus:border-[#0072ce] focus:outline-none" />
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
              <input type="text" required v-model="newInlineNet.address" placeholder="e.g. 10.50.0.0/16 or 192.168.1.50" class="w-full p-2 border border-slate-300 rounded font-mono focus:border-[#0072ce] focus:outline-none" />
            </div>
            <div class="pt-3 border-t border-slate-200 flex justify-between">
              <button type="button" @click="isInlineNetModalOpen = false" class="px-3.5 py-1.5 border border-slate-300 rounded text-slate-700 hover:bg-slate-50 cursor-pointer">Cancel</button>
              <button type="submit" class="px-4 py-1.5 bg-[#0072ce] text-white font-bold rounded shadow-xs cursor-pointer">Save &amp; Use</button>
            </div>
          </form>
        </div>
      </div>
    </transition>

    <!-- MODAL: ADD REMOTE USER CLIENT -->
    <transition
      enter-active-class="transition duration-150 ease-out"
      enter-from-class="opacity-0 scale-95"
      enter-to-class="opacity-100 scale-100"
      leave-active-class="transition duration-100 ease-in"
      leave-from-class="opacity-100 scale-100"
      leave-to-class="opacity-0 scale-95"
    >
      <div
        v-if="isUserModalOpen"
        class="fixed inset-0 z-40 overflow-y-auto bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4"
        @keydown.esc="isUserModalOpen = false"
      >
        <div class="bg-white rounded-2xl shadow-2xl border border-slate-200 max-w-md w-full overflow-hidden flex flex-col my-6">
          <div class="px-5 py-3.5 bg-slate-900 text-white flex items-center justify-between border-b border-slate-800">
            <h3 class="text-xs font-bold uppercase tracking-wider text-white">Provision Remote Access VPN User</h3>
            <button @click="isUserModalOpen = false" class="text-slate-400 hover:text-white font-bold cursor-pointer">&times;</button>
          </div>
          <form @submit.prevent="saveRemoteUser" class="p-5 space-y-3 text-xs">
            <div>
              <label class="block font-bold text-slate-700 mb-1">User / Device Identifier *</label>
              <input type="text" required v-model="formUser.client_name" placeholder="e.g. alex-macbook-pro" class="w-full p-2 border border-slate-300 rounded" />
            </div>
            <div>
              <label class="block font-bold text-slate-700 mb-1">Assigned Virtual IP *</label>
              <input type="text" required v-model="formUser.virtual_ip" placeholder="10.8.0.10/32" class="w-full p-2 border border-slate-300 rounded font-mono" />
            </div>
            <div>
              <label class="block font-bold text-slate-700 mb-1">Client Device Type</label>
              <select v-model="formUser.device_type" class="w-full p-2 border border-slate-300 rounded bg-white font-medium">
                <option value="macOS">macOS</option>
                <option value="Windows">Windows 11 / 10</option>
                <option value="Linux">Linux Desktop</option>
                <option value="iOS">iOS (iPhone / iPad)</option>
                <option value="Android">Android</option>
              </select>
            </div>
            <div class="pt-3 border-t border-slate-200 flex justify-between">
              <button type="button" @click="isUserModalOpen = false" class="px-3.5 py-1.5 border rounded text-slate-700 cursor-pointer">Cancel</button>
              <button type="submit" class="px-4 py-1.5 bg-[#0072ce] text-white font-bold rounded shadow-xs cursor-pointer">Generate &amp; Download Profile</button>
            </div>
          </form>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, h } from 'vue'

const props = defineProps({
  authToken: {
    type: String,
    default: ''
  }
})

const activeTab = ref('all_tunnels') // 'all_tunnels' | 'ssl' | 'ipsec' | 'amazon_vpc' | 'remote_users'
const isLoading = ref(false)
const searchQuery = ref('')
const statusFilter = ref('ALL')
const isTunnelModalOpen = ref(false)
const isUserModalOpen = ref(false)
const editingTunnelId = ref(null)

// Tab icons
const TunnelIcon = {
  render: () => h('svg', { class: 'w-4 h-4', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
    h('path', { strokeLinecap: 'round', strokeLinejoin: 'round', strokeWidth: '2', d: 'M13 10V3L4 14h7v7l9-11h-7z' })
  ])
}

const SslIcon = {
  render: () => h('svg', { class: 'w-4 h-4', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
    h('path', { strokeLinecap: 'round', strokeLinejoin: 'round', strokeWidth: '2', d: 'M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z' })
  ])
}

const IpsecIcon = {
  render: () => h('svg', { class: 'w-4 h-4', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
    h('path', { strokeLinecap: 'round', strokeLinejoin: 'round', strokeWidth: '2', d: 'M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z' })
  ])
}

const AwsIcon = {
  render: () => h('svg', { class: 'w-4 h-4', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
    h('path', { strokeLinecap: 'round', strokeLinejoin: 'round', strokeWidth: '2', d: 'M3 15a4 4 0 004 4h9a5 5 0 10-.1-9.999 5.002 5.002 0 00-9.78 2.096A4.001 4.001 0 003 15z' })
  ])
}

const UsersIcon = {
  render: () => h('svg', { class: 'w-4 h-4', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
    h('path', { strokeLinecap: 'round', strokeLinejoin: 'round', strokeWidth: '2', d: 'M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z' })
  ])
}

const tunnelsList = ref([
  {
    id: 'tun-branch-ssl-client',
    name: 'Branch Office SSL Client',
    tunnel_name: 'Branch Office SSL Client',
    type: 'ssl_client',
    tunnel_type: 'ssl_client',
    remote_gateway: 'vpn.remotebranch.com:1194',
    remote_endpoint: 'vpn.remotebranch.com:1194',
    local_network: '192.168.1.0/24',
    remote_network: '10.50.0.0/16',
    remote_subnets: ['10.50.0.0/16'],
    status: 'Connected',
    latency_ms: 19,
    enabled: true
  },
  {
    id: 'tun-hq-wireguard',
    name: 'HQ-Datacenter-Tunnel',
    tunnel_name: 'HQ-Datacenter-Tunnel',
    type: 'wireguard',
    tunnel_type: 'wireguard',
    remote_gateway: 'vpn.corp.company.com:51820',
    remote_endpoint: 'vpn.corp.company.com:51820',
    local_network: '10.250.0.2/30',
    remote_network: '10.100.0.0/16',
    remote_subnets: ['10.100.0.0/16', '172.16.0.0/16'],
    status: 'Connected',
    latency_ms: 14,
    enabled: true
  },
  {
    id: 'tun-aws-vpc-link',
    name: 'Cloud-AWS-VPC-Link',
    tunnel_name: 'Cloud-AWS-VPC-Link',
    type: 'amazon_vpc',
    tunnel_type: 'amazon_vpc',
    remote_gateway: '52.95.120.45:4500',
    remote_endpoint: '52.95.120.45:4500',
    local_network: '169.254.10.1/30',
    remote_network: '172.31.0.0/16',
    remote_subnets: ['172.31.0.0/16'],
    status: 'Connected',
    latency_ms: 28,
    enabled: true
  }
])

const peersList = ref([
  {
    id: 'wg-01',
    client_name: 'alex-macbook-pro',
    virtual_ip: '10.8.0.2/32',
    public_key: 'xK9vR8kM2tQ0pW4jL8nB7yC5zX1mN3vK6rT9uP2wE4=',
    status: 'active',
    is_active: true,
    transfer_rx: 1845493760,
    transfer_tx: 489230450
  },
  {
    id: 'wg-02',
    client_name: 'sarah-thinkpad-x1',
    virtual_ip: '10.8.0.3/32',
    public_key: 'hP7qZ3mK9vR8tW2jL5nB1yC4zX0mN8vK3rT6uP9wQ1=',
    status: 'active',
    is_active: true,
    transfer_rx: 924857600,
    transfer_tx: 154230450
  },
  {
    id: 'wg-03',
    client_name: 'devops-staging-bastion',
    virtual_ip: '10.8.0.4/32',
    public_key: 'yM4vK9tQ0pW2jL7nB5yC1zX8mN3vK6rT0uP4wE9rT2=',
    status: 'inactive',
    is_active: false,
    transfer_rx: 34500000,
    transfer_tx: 12000000
  }
])

const tabs = computed(() => [
  { id: 'all_tunnels', label: 'All Site-to-Site Tunnels', icon: TunnelIcon, count: tunnelsList.value.length },
  { id: 'ssl', label: 'SSL VPN (Client & Server)', icon: SslIcon, count: tunnelsList.value.filter(t => (t.type || t.tunnel_type)?.includes('ssl')).length },
  { id: 'ipsec', label: 'IPsec / IKEv2 Gateway', icon: IpsecIcon, count: tunnelsList.value.filter(t => (t.type || t.tunnel_type) === 'ipsec').length },
  { id: 'amazon_vpc', label: 'Amazon VPC Interconnect', icon: AwsIcon, count: tunnelsList.value.filter(t => (t.type || t.tunnel_type) === 'amazon_vpc').length },
  { id: 'remote_users', label: 'Remote Access Users (WireGuard)', icon: UsersIcon, count: peersList.value.length }
])

const activeTabLabel = computed(() => {
  if (activeTab.value === 'ssl') return 'SSL VPN Tunnel'
  if (activeTab.value === 'ipsec') return 'IPsec Connection'
  if (activeTab.value === 'amazon_vpc') return 'Amazon VPC Link'
  if (activeTab.value === 'remote_users') return 'Remote User'
  return 'Site-to-Site Tunnel'
})

const networkDefs = ref([])
const isInlineNetModalOpen = ref(false)
const inlineNetTarget = ref('local')
const newInlineNet = ref({ name: '', type: 'Network', address: '' })

const openInlineNetModal = (target = 'local') => {
  inlineNetTarget.value = target
  newInlineNet.value = {
    name: '',
    type: target === 'remote_endpoint' ? 'Host' : 'Network',
    address: ''
  }
  isInlineNetModalOpen.value = true
}

const saveInlineNet = async () => {
  if (!newInlineNet.value.name || !newInlineNet.value.address) return
  const axiosLib = (typeof window !== 'undefined' && window.axios) ? window.axios : null
  if (axiosLib) {
    try {
      await axiosLib.post('/api/definitions/networks', newInlineNet.value)
      await fetchData()
    } catch (e) {
      console.error('Failed to create network definition in VPN:', e)
    }
  }

  const selectedVal = newInlineNet.value.address || newInlineNet.value.name
  if (inlineNetTarget.value === 'local') {
    formTunnel.value.local_networks_text = selectedVal
  } else if (inlineNetTarget.value === 'remote') {
    formTunnel.value.remote_subnets_text = selectedVal
  } else if (inlineNetTarget.value === 'remote_endpoint') {
    formTunnel.value.remote_endpoint = selectedVal
  }

  isInlineNetModalOpen.value = false
}

const formTunnel = ref({
  tunnel_name: '',
  tunnel_type: 'ssl_client',
  remote_endpoint: '',
  remote_port: 1194,
  protocol: 'UDP',
  auth_mode: 'password',
  username: '',
  password: '',
  local_networks_text: '192.168.1.0/24',
  remote_subnets_text: '10.50.0.0/16',
  local_virtual_ip: '10.250.0.2/30',
  remote_public_key: '',
  preshared_key: '',
  auto_firewall_rule: true,
  use_default_gateway: false,
  aws_region: 'us-east-1',
  aws_vpc_id: '',
  comment: '',
  enabled: true
})

const formUser = ref({
  client_name: '',
  virtual_ip: '10.8.0.10/32',
  device_type: 'macOS'
})

const activePeersCount = computed(() => peersList.value.filter(p => p.status === 'active' || p.is_active).length)
const aggregateTransferFormatted = computed(() => {
  const total = peersList.value.reduce((acc, p) => acc + (p.transfer_rx || 0) + (p.transfer_tx || 0), 0)
  return formatBytes(total)
})

const filteredTunnels = computed(() => {
  let list = [...tunnelsList.value]

  if (activeTab.value === 'ssl') {
    list = list.filter(t => (t.type || t.tunnel_type)?.includes('ssl'))
  } else if (activeTab.value === 'ipsec') {
    list = list.filter(t => (t.type || t.tunnel_type) === 'ipsec')
  } else if (activeTab.value === 'amazon_vpc') {
    list = list.filter(t => (t.type || t.tunnel_type) === 'amazon_vpc')
  }

  if (statusFilter.value === 'ACTIVE') {
    list = list.filter(t => t.enabled !== false)
  } else if (statusFilter.value === 'INACTIVE') {
    list = list.filter(t => t.enabled === false)
  }

  if (searchQuery.value.trim()) {
    const q = searchQuery.value.toLowerCase()
    list = list.filter(t =>
      (t.name && t.name.toLowerCase().includes(q)) ||
      (t.tunnel_name && t.tunnel_name.toLowerCase().includes(q)) ||
      (t.remote_gateway && t.remote_gateway.toLowerCase().includes(q)) ||
      (t.remote_endpoint && t.remote_endpoint.toLowerCase().includes(q)) ||
      (t.remote_network && t.remote_network.toLowerCase().includes(q))
    )
  }

  return list
})

const filteredPeers = computed(() => {
  let list = [...peersList.value]
  if (statusFilter.value === 'ACTIVE') list = list.filter(p => p.status === 'active' || p.is_active)
  else if (statusFilter.value === 'INACTIVE') list = list.filter(p => p.status !== 'active' && !p.is_active)

  if (searchQuery.value.trim()) {
    const q = searchQuery.value.toLowerCase()
    list = list.filter(p =>
      p.client_name.toLowerCase().includes(q) ||
      p.virtual_ip.toLowerCase().includes(q)
    )
  }
  return list
})

const currentFilteredItemsCount = computed(() => {
  return activeTab.value === 'remote_users' ? filteredPeers.value.length : filteredTunnels.value.length
})

const formatBytes = (bytes) => {
  if (!bytes || bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB', 'TB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i]
}

const formatTunnelType = (type) => {
  if (!type) return 'TUNNEL'
  if (type === 'ssl_client') return 'SSL Client Mode'
  if (type === 'ssl_server') return 'SSL Server Mode'
  if (type === 'amazon_vpc') return 'AWS Cloud VPC'
  if (type === 'ipsec') return 'IPsec IKEv2'
  if (type === 'wireguard') return 'WireGuard'
  return type.toUpperCase()
}

const getTunnelTypeBadgeClasses = (type) => {
  if (type === 'ssl_client') return 'bg-blue-50 text-[#0072ce] border-blue-200'
  if (type === 'ssl_server') return 'bg-cyan-50 text-cyan-800 border-cyan-200'
  if (type === 'amazon_vpc') return 'bg-amber-50 text-amber-900 border-amber-200'
  if (type === 'ipsec') return 'bg-indigo-50 text-indigo-800 border-indigo-200'
  return 'bg-purple-50 text-purple-700 border-purple-200'
}

const fetchData = async (isManual = false) => {
  isLoading.value = true
  try {
    const axiosLib = (typeof window !== 'undefined' && window.axios) ? window.axios : null
    if (axiosLib) {
      const [tunRes, peerRes, netRes] = await Promise.all([
        axiosLib.get('/api/vpn/tunnels').catch(() => null),
        axiosLib.get('/api/vpn/peers').catch(() => null),
        axiosLib.get('/api/definitions/networks').catch(() => null)
      ])
      if (tunRes && tunRes.data && tunRes.data.tunnels) {
        tunnelsList.value = tunRes.data.tunnels
      }
      if (peerRes && peerRes.data && peerRes.data.peers) {
        peersList.value = peerRes.data.peers
      }
      if (netRes && netRes.data) {
        networkDefs.value = netRes.data
      }
    }
  } catch (e) {
    console.error('Failed to fetch VPN data:', e)
  } finally {
    isLoading.value = false
  }
}

const openAddTunnelModal = (type = 'ssl_client') => {
  editingTunnelId.value = null
  let defaultType = 'ssl_client'
  if (type === 'ssl') defaultType = 'ssl_client'
  else if (type === 'ipsec') defaultType = 'ipsec'
  else if (type === 'amazon_vpc') defaultType = 'amazon_vpc'

  formTunnel.value = {
    tunnel_name: '',
    tunnel_type: defaultType,
    remote_endpoint: '',
    remote_port: 1194,
    protocol: 'UDP',
    auth_mode: 'password',
    username: '',
    password: '',
    local_networks_text: '192.168.1.0/24',
    remote_subnets_text: '10.50.0.0/16',
    local_virtual_ip: '10.250.0.2/30',
    remote_public_key: '',
    preshared_key: '',
    auto_firewall_rule: true,
    use_default_gateway: false,
    aws_region: 'us-east-1',
    aws_vpc_id: '',
    comment: '',
    enabled: true
  }
  isTunnelModalOpen.value = true
}

const editTunnel = (tun) => {
  editingTunnelId.value = tun.id || tun.name || tun.tunnel_name
  formTunnel.value = {
    tunnel_name: tun.name || tun.tunnel_name || '',
    tunnel_type: tun.type || tun.tunnel_type || 'ssl_client',
    remote_endpoint: tun.remote_gateway || tun.remote_endpoint || '',
    remote_port: 1194,
    protocol: 'UDP',
    auth_mode: tun.auth_type || 'password',
    username: '',
    password: '',
    local_networks_text: tun.local_network || tun.local_virtual_ip || '192.168.1.0/24',
    remote_subnets_text: Array.isArray(tun.remote_subnets) ? tun.remote_subnets.join(', ') : (tun.remote_network || '10.50.0.0/16'),
    local_virtual_ip: tun.local_virtual_ip || '10.250.0.2/30',
    remote_public_key: tun.remote_public_key || '',
    preshared_key: '',
    auto_firewall_rule: true,
    use_default_gateway: false,
    aws_region: 'us-east-1',
    aws_vpc_id: '',
    comment: '',
    enabled: tun.enabled !== false
  }
  isTunnelModalOpen.value = true
}

const cloneTunnel = (tun) => {
  editingTunnelId.value = null
  formTunnel.value = {
    tunnel_name: `${tun.name || tun.tunnel_name} (Clone)`,
    tunnel_type: tun.type || tun.tunnel_type || 'ssl_client',
    remote_endpoint: tun.remote_gateway || tun.remote_endpoint || '',
    remote_port: 1194,
    protocol: 'UDP',
    auth_mode: tun.auth_type || 'password',
    username: '',
    password: '',
    local_networks_text: tun.local_network || tun.local_virtual_ip || '192.168.1.0/24',
    remote_subnets_text: Array.isArray(tun.remote_subnets) ? tun.remote_subnets.join(', ') : (tun.remote_network || '10.50.0.0/16'),
    local_virtual_ip: tun.local_virtual_ip || '10.250.0.2/30',
    remote_public_key: tun.remote_public_key || '',
    preshared_key: '',
    auto_firewall_rule: true,
    use_default_gateway: false,
    aws_region: 'us-east-1',
    aws_vpc_id: '',
    comment: '',
    enabled: true
  }
  isTunnelModalOpen.value = true
}

const saveTunnel = async () => {
  const remoteSubnets = formTunnel.value.remote_subnets_text
    .split(',')
    .map(s => s.trim())
    .filter(Boolean)

  const localNetworks = formTunnel.value.local_networks_text
    .split(',')
    .map(s => s.trim())
    .filter(Boolean)

  const payload = {
    tunnel_name: formTunnel.value.tunnel_name,
    tunnel_type: formTunnel.value.tunnel_type,
    remote_endpoint: formTunnel.value.remote_endpoint,
    remote_port: formTunnel.value.remote_port,
    protocol: formTunnel.value.protocol,
    auth_mode: formTunnel.value.auth_mode,
    username: formTunnel.value.username,
    password: formTunnel.value.password,
    local_virtual_ip: formTunnel.value.local_virtual_ip,
    local_networks: localNetworks,
    remote_subnets: remoteSubnets,
    remote_public_key: formTunnel.value.remote_public_key,
    preshared_key: formTunnel.value.preshared_key,
    route_mode: formTunnel.value.use_default_gateway ? 'full_gateway' : 'split_tunnel',
    auto_firewall_rule: formTunnel.value.auto_firewall_rule,
    aws_region: formTunnel.value.aws_region,
    aws_vpc_id: formTunnel.value.aws_vpc_id,
    comment: formTunnel.value.comment,
    enabled: formTunnel.value.enabled
  }

  try {
    const axiosLib = (typeof window !== 'undefined' && window.axios) ? window.axios : null
    if (axiosLib) {
      await axiosLib.post('/api/vpn/tunnels/save', payload)
      await fetchData()
    }
  } catch (e) {
    console.error('Failed to save tunnel:', e)
  }

  isTunnelModalOpen.value = false
}

const toggleTunnel = async (tun) => {
  tun.enabled = !tun.enabled
  const axiosLib = (typeof window !== 'undefined' && window.axios) ? window.axios : null
  if (axiosLib) {
    try {
      await axiosLib.post('/api/vpn/tunnels/save', {
        tunnel_name: tun.name || tun.tunnel_name,
        tunnel_type: tun.type || tun.tunnel_type,
        remote_endpoint: tun.remote_gateway || tun.remote_endpoint,
        local_virtual_ip: tun.local_network || tun.local_virtual_ip || '10.250.0.2/30',
        remote_subnets: Array.isArray(tun.remote_subnets) ? tun.remote_subnets : [tun.remote_network || '10.0.0.0/16'],
        enabled: tun.enabled
      })
    } catch (e) {
      console.error(e)
    }
  }
}

const deleteTunnel = async (id) => {
  if (!confirm(`Are you sure you want to delete VPN tunnel '${id}'?`)) return
  try {
    const axiosLib = (typeof window !== 'undefined' && window.axios) ? window.axios : null
    if (axiosLib) {
      await axiosLib.delete(`/api/vpn/tunnels/${id}`)
      await fetchData()
    }
  } catch (e) {
    console.error('Failed to delete tunnel:', e)
  }
}

const openAddUserModal = () => {
  formUser.value = {
    client_name: '',
    virtual_ip: `10.8.0.${peersList.value.length + 2}/32`,
    device_type: 'macOS'
  }
  isUserModalOpen.value = true
}

const saveRemoteUser = async () => {
  try {
    const axiosLib = (typeof window !== 'undefined' && window.axios) ? window.axios : null
    if (axiosLib) {
      await axiosLib.post('/api/vpn/peers/create', {
        client_name: formUser.value.client_name,
        virtual_ip: formUser.value.virtual_ip
      })
      await fetchData()
    }
  } catch (e) {
    console.error(e)
  }
  isUserModalOpen.value = false
}

const downloadPeerConfig = (peer) => {
  const confContent = `[Interface]
PrivateKey = (ClientGeneratedPrivateKeyBase64==)
Address = ${peer.virtual_ip}
DNS = 1.1.1.1, 8.8.8.8

[Peer]
PublicKey = Astaro-NextxgsFirewallServerPublicKeyBase64WireGuard=
Endpoint = vpn.astaro-gateway.internal:51820
AllowedIPs = 0.0.0.0/0, ::/0
PersistentKeepalive = 25`

  const blob = new Blob([confContent], { type: 'text/plain;charset=utf-8' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `${peer.client_name || 'astaro-vpn'}.conf`
  a.click()
  URL.revokeObjectURL(url)
}

const deletePeer = async (id) => {
  if (!confirm(`Are you sure you want to delete remote user client '${id}'?`)) return
  try {
    const axiosLib = (typeof window !== 'undefined' && window.axios) ? window.axios : null
    if (axiosLib) {
      await axiosLib.delete(`/api/vpn/wireguard/peer/${id}`)
      await fetchData()
    }
  } catch (e) {
    console.error(e)
  }
}

onMounted(() => {
  fetchData()
})
</script>
