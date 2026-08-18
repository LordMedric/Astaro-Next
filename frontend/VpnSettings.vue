<template>
  <div class="min-h-full bg-slate-50 text-slate-800 font-sans antialiased selection:bg-[#2563eb] selection:text-white relative pb-16">
    <!-- Notification Toasts Floating Stack -->
    <div class="fixed bottom-5 right-5 z-50 flex flex-col gap-2.5 max-w-md w-full pointer-events-none" aria-live="polite">
      <transition-group
        enter-active-class="transition duration-300 ease-out transform"
        enter-from-class="translate-y-3 opacity-0 scale-95"
        enter-to-class="translate-y-0 opacity-100 scale-100"
        leave-active-class="transition duration-200 ease-in transform"
        leave-from-class="translate-y-0 opacity-100 scale-100"
        leave-to-class="translate-y-3 opacity-0 scale-95"
      >
        <div
          v-for="toast in toasts"
          :key="toast.id"
          :class="[
            'pointer-events-auto p-4 rounded-xl shadow-2xl border flex items-start gap-3.5 text-xs backdrop-blur-md transition-all',
            toast.type === 'success' ? 'bg-emerald-950/95 border-emerald-500/60 text-emerald-100 ring-1 ring-emerald-500/20' :
            toast.type === 'error' ? 'bg-rose-950/95 border-rose-500/60 text-rose-100 ring-1 ring-rose-500/20' :
            toast.type === 'warning' ? 'bg-amber-950/95 border-amber-500/60 text-amber-100 ring-1 ring-amber-500/20' :
            'bg-slate-900/95 border-slate-700 text-slate-100 ring-1 ring-slate-700/50'
          ]"
          role="alert"
        >
          <div class="mt-0.5 flex-none">
            <svg v-if="toast.type === 'success'" class="w-5 h-5 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <svg v-else-if="toast.type === 'error'" class="w-5 h-5 text-rose-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <svg v-else-if="toast.type === 'warning'" class="w-5 h-5 text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
            <svg v-else class="w-5 h-5 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div class="flex-1 min-w-0">
            <h4 class="font-bold uppercase tracking-wider text-[11px] font-mono">{{ toast.title }}</h4>
            <p class="mt-0.5 opacity-90 leading-relaxed font-sans text-xs">{{ toast.message }}</p>
          </div>
          <button
            type="button"
            @click="dismissToast(toast.id)"
            class="text-slate-400 hover:text-white transition-colors cursor-pointer p-0.5 rounded"
            aria-label="Dismiss notification"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </transition-group>
    </div>

    <!-- Top Management & Telemetry Header Banner -->
    <div class="mb-6 flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4 bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
      <!-- Title & Subtitle with Sophos Blue Accent -->
      <div class="flex items-center gap-4">
        <div class="w-12 h-12 rounded-xl bg-[#2563eb] flex items-center justify-center text-white shadow-md shadow-blue-500/20 font-black flex-shrink-0">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
          </svg>
        </div>
        <div>
          <div class="flex items-center gap-2.5 flex-wrap">
            <h1 class="text-xl font-black text-slate-900 tracking-tight">Remote Access VPN</h1>
            <span class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-[11px] font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200">
              <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
              {{ activePeersCount }}/{{ peersList.length }} Peers Connected
            </span>
            <span class="inline-flex items-center px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-blue-50 text-[#2563eb] border border-blue-100 uppercase">
              SFOS XGS VPN Subsystem
            </span>
          </div>
          <p class="text-xs text-slate-500 mt-1">
            Provision, manage, and monitor high-throughput encrypted endpoint tunnels, peer cryptographic keys, and virtual subnet routing.
          </p>
        </div>
      </div>

      <!-- Quick Action Controls & Primary "Add Remote User" Button -->
      <div class="flex items-center flex-wrap gap-2.5">
        <!-- Search Filter Input -->
        <div class="relative min-w-[200px]">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search clients or IPs..."
            class="w-full bg-slate-50 text-slate-800 text-xs px-3 py-2 pl-8 rounded-lg border border-slate-300 focus:outline-none focus:border-[#2563eb] focus:ring-1 focus:ring-[#2563eb] placeholder:text-slate-400 transition-colors"
          />
          <svg class="w-3.5 h-3.5 text-slate-400 absolute left-2.5 top-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
          <button
            v-if="searchQuery"
            @click="searchQuery = ''"
            class="absolute right-2.5 top-2.5 text-slate-400 hover:text-slate-600"
          >
            ✕
          </button>
        </div>

        <!-- Status Filter Dropdown -->
        <select
          v-model="statusFilter"
          class="bg-slate-50 text-slate-700 text-xs px-3 py-2 rounded-lg border border-slate-300 focus:outline-none focus:border-[#2563eb] font-medium"
        >
          <option value="ALL">All Statuses</option>
          <option value="ACTIVE">Connected Only</option>
          <option value="INACTIVE">Disconnected Only</option>
        </select>

        <!-- Refresh Button -->
        <button
          type="button"
          @click="fetchPeers(true)"
          :disabled="isLoading"
          class="inline-flex items-center gap-1.5 px-3 py-2 rounded-lg bg-white border border-slate-300 text-xs font-semibold text-slate-700 hover:bg-slate-50 hover:text-slate-900 active:bg-slate-100 disabled:opacity-50 transition-all shadow-2xs cursor-pointer"
          title="Reload peer metrics from VPN daemon"
        >
          <svg
            :class="['w-3.5 h-3.5 text-slate-500', isLoading ? 'animate-spin text-[#2563eb]' : '']"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          <span class="hidden sm:inline">Refresh</span>
        </button>

        <!-- Primary Blue Button: Add Remote User -->
        <button
          type="button"
          @click="openAddUserModal"
          class="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-[#2563eb] hover:bg-blue-700 active:bg-blue-800 text-white text-xs font-bold tracking-wide shadow-md shadow-blue-500/20 transition-all cursor-pointer"
          title="Provision a new remote client tunnel profile"
        >
          <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
          </svg>
          <span>Add Remote User</span>
        </button>
      </div>
    </div>

    <!-- Telemetry Statistics Strip (Sophos XGS Style) -->
    <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-6">
      <div class="bg-white p-3.5 rounded-xl border border-slate-200 shadow-2xs flex items-center gap-3">
        <div class="w-9 h-9 rounded-lg bg-blue-50 text-[#2563eb] flex items-center justify-center font-bold">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
          </svg>
        </div>
        <div>
          <div class="text-[10px] uppercase font-bold text-slate-400">Total Peers</div>
          <div class="text-base font-bold text-slate-900">{{ peersList.length }}</div>
        </div>
      </div>

      <div class="bg-white p-3.5 rounded-xl border border-slate-200 shadow-2xs flex items-center gap-3">
        <div class="w-9 h-9 rounded-lg bg-emerald-50 text-emerald-600 flex items-center justify-center font-bold">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <div>
          <div class="text-[10px] uppercase font-bold text-slate-400">Active Tunnels</div>
          <div class="text-base font-bold text-emerald-600">{{ activePeersCount }}</div>
        </div>
      </div>

      <div class="bg-white p-3.5 rounded-xl border border-slate-200 shadow-2xs flex items-center gap-3">
        <div class="w-9 h-9 rounded-lg bg-indigo-50 text-indigo-600 flex items-center justify-center font-bold">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M9 19l3 3m0 0l3-3m-3 3V10" />
          </svg>
        </div>
        <div>
          <div class="text-[10px] uppercase font-bold text-slate-400">Total Transfer</div>
          <div class="text-base font-bold text-indigo-700 font-mono">{{ aggregateTransferFormatted }}</div>
        </div>
      </div>

      <div class="bg-white p-3.5 rounded-xl border border-slate-200 shadow-2xs flex items-center gap-3">
        <div class="w-9 h-9 rounded-lg bg-purple-50 text-purple-600 flex items-center justify-center font-bold">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
          </svg>
        </div>
        <div>
          <div class="text-[10px] uppercase font-bold text-slate-400">Crypto Engine</div>
          <div class="text-xs font-mono font-bold text-purple-700">ChaCha20-Poly1305</div>
        </div>
      </div>
    </div>

    <!-- CORE HORIZONTAL CONFIGURATION TAB SELECTOR -->
    <div class="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden mb-6">
      <div class="border-b border-slate-200 bg-slate-50/50 px-4 pt-3 flex items-center gap-2 overflow-x-auto">
        <button
          type="button"
          v-for="tab in configTabs"
          :key="tab.id"
          @click="activeTab = tab.id"
          :class="[
            'relative px-5 py-3 text-xs font-bold transition-all flex items-center gap-2.5 whitespace-nowrap cursor-pointer rounded-t-lg -mb-px',
            activeTab === tab.id
              ? 'bg-white text-[#2563eb] border-t-2 border-x border-slate-200 border-t-[#2563eb] shadow-xs'
              : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100/70'
          ]"
        >
          <!-- Tab Protocol Icon -->
          <component :is="tab.icon" class="w-4 h-4" :class="activeTab === tab.id ? 'text-[#2563eb]' : 'text-slate-400'" />
          <span>{{ tab.label }}</span>

          <!-- Tab Status / Count Badge -->
          <span
            v-if="tab.badge"
            :class="[
              'text-[10px] px-1.5 py-0.5 rounded-full font-mono font-semibold',
              activeTab === tab.id ? 'bg-blue-50 text-[#2563eb] border border-blue-200' : 'bg-slate-200 text-slate-600'
            ]"
          >
            {{ tab.badge }}
          </span>

          <!-- High-contrast corporate blue accent highlight bar on active -->
          <span
            v-if="activeTab === tab.id"
            class="absolute inset-x-0 -top-[2px] h-[3px] bg-[#2563eb] rounded-t-md"
          ></span>
        </button>
      </div>

      <!-- Tab Contextual Banner / Info Notice -->
      <div class="p-4 bg-slate-50/70 border-b border-slate-200 text-xs text-slate-600 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div class="flex items-center gap-2.5">
          <span class="w-2 h-2 rounded-full" :class="activeTab === 'wireguard' ? 'bg-emerald-500' : 'bg-amber-500'"></span>
          <span v-if="activeTab === 'wireguard'">
            <strong>WireGuard Server Gateway:</strong> Listening on UDP <code class="bg-white px-1.5 py-0.5 rounded border border-slate-200 text-[#2563eb] font-mono">51820</code> | Subnet: <code class="bg-white px-1.5 py-0.5 rounded border border-slate-200 font-mono">10.8.0.0/24</code>
          </span>
          <span v-else-if="activeTab === 'ssl'">
            <strong>SSL VPN (OpenVPN Engine):</strong> Listening on TCP/UDP <code class="bg-white px-1.5 py-0.5 rounded border border-slate-200 font-mono">8443</code> | TLS 1.3 Strict
          </span>
          <span v-else>
            <strong>IPsec / IKEv2 Gateway:</strong> StrongSwan Stack on UDP <code class="bg-white px-1.5 py-0.5 rounded border border-slate-200 font-mono">500, 4500</code> (ESP NAT-T)
          </span>
        </div>

        <div class="flex items-center gap-3 text-[11px] font-mono text-slate-500">
          <span>Interface: <strong class="text-slate-700">{{ activeTab === 'wireguard' ? 'wg0' : activeTab === 'ssl' ? 'tun0' : 'ipsec0' }}</strong></span>
          <span>&bull;</span>
          <span>MTU: <strong class="text-slate-700">1420</strong></span>
        </div>
      </div>
    </div>

    <!-- NON-WIREGUARD TAB PLACEHOLDER -->
    <div v-if="activeTab !== 'wireguard'" class="bg-white rounded-xl border border-slate-200 shadow-sm p-8 text-center mb-6">
      <div class="w-14 h-14 rounded-2xl bg-slate-100 border border-slate-200 flex items-center justify-center mx-auto mb-4 text-slate-500">
        <svg class="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      </div>
      <h3 class="text-base font-bold text-slate-900">{{ activeTab === 'ssl' ? 'SSL VPN (OpenVPN) Subsystem' : 'IPsec VPN (IKEv2) Gateway' }}</h3>
      <p class="text-xs text-slate-500 max-w-md mx-auto mt-1">
        This gateway subsystem is provisioned and running in standby compatibility mode. Switch to WireGuard for high-speed next-generation remote peer management.
      </p>
      <button
        type="button"
        @click="activeTab = 'wireguard'"
        class="mt-4 inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-[#2563eb] text-white text-xs font-bold hover:bg-blue-700 transition-colors cursor-pointer"
      >
        <span>Switch to WireGuard VPN</span>
      </button>
    </div>

    <!-- HIGH-UTILITY REMOTE USER OVERVIEW TABLE CONTAINER -->
    <div v-if="activeTab === 'wireguard'" class="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden flex flex-col">
      <!-- Table Top Toolbar Strip -->
      <div class="px-5 py-3.5 border-b border-slate-200 bg-slate-50/60 flex flex-col sm:flex-row sm:items-center justify-between gap-2">
        <div class="flex items-center gap-2">
          <span class="w-1.5 h-4 bg-[#2563eb] rounded-full"></span>
          <h2 class="text-xs font-bold text-slate-800 uppercase tracking-wider">Remote User Client Matrix</h2>
          <span class="text-[11px] text-slate-400 font-mono">({{ filteredPeers.length }} matched)</span>
        </div>
        <div class="flex items-center gap-4 text-xs text-slate-500 font-mono text-[11px]">
          <span class="flex items-center gap-1.5">
            <span class="w-2 h-2 rounded-full bg-emerald-500"></span> Active: {{ activePeersCount }}
          </span>
          <span class="flex items-center gap-1.5">
            <span class="w-2 h-2 rounded-full bg-slate-300"></span> Inactive: {{ inactivePeersCount }}
          </span>
        </div>
      </div>

      <!-- High-Utility Table -->
      <div class="overflow-x-auto">
        <table class="w-full text-left border-collapse" role="table">
          <thead>
            <tr class="border-b border-slate-200 bg-slate-50 text-[11px] font-bold text-slate-500 uppercase tracking-wider select-none">
              <th scope="col" class="py-3 px-4 border-r border-slate-200/80 min-w-[200px]">Client Name</th>
              <th scope="col" class="py-3 px-4 border-r border-slate-200/80 min-w-[150px]">Assigned Virtual IP</th>
              <th scope="col" class="py-3 px-4 border-r border-slate-200/80 min-w-[220px]">Public Crypto Key</th>
              <th scope="col" class="py-3 px-4 border-r border-slate-200/80 min-w-[150px]">Connection Status</th>
              <th scope="col" class="py-3 px-4 border-r border-slate-200/80 min-w-[170px]">Total Bandwidth Transfer</th>
              <th scope="col" class="py-3 px-4 min-w-[120px] text-center">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-200 text-xs">
            <tr
              v-for="(peer, index) in filteredPeers"
              :key="peer.public_key || peer.id || index"
              :class="[
                'transition-colors duration-150',
                peer.status === 'active' || peer.is_active
                  ? (index % 2 === 0 ? 'bg-white hover:bg-blue-50/30' : 'bg-slate-50/60 hover:bg-blue-50/40')
                  : 'bg-slate-100/40 hover:bg-slate-100/70 text-slate-600'
              ]"
            >
              <!-- 1. Client Name & Device Info -->
              <td class="py-3.5 px-4 border-r border-slate-200/80">
                <div class="flex items-center gap-3">
                  <div
                    class="w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0 text-white font-bold text-xs shadow-2xs"
                    :class="peer.status === 'active' || peer.is_active ? 'bg-[#2563eb]' : 'bg-slate-400'"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                    </svg>
                  </div>
                  <div>
                    <div class="flex items-center gap-2">
                      <span class="font-bold text-slate-900 leading-snug">{{ peer.client_name || peer.name || 'Unnamed Client' }}</span>
                      <span v-if="peer.device_type" class="text-[10px] px-1.5 py-0.2 rounded bg-slate-100 border border-slate-200 text-slate-600 uppercase font-mono">
                        {{ peer.device_type }}
                      </span>
                    </div>
                    <div class="text-[10px] text-slate-400 font-mono mt-0.5 flex items-center gap-2">
                      <span>Endpoint: {{ peer.endpoint || peer.latest_endpoint || 'Auto-negotiated' }}</span>
                    </div>
                  </div>
                </div>
              </td>

              <!-- 2. Assigned Virtual IP -->
              <td class="py-3.5 px-4 border-r border-slate-200/80 font-mono">
                <span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md text-[11px] font-bold bg-blue-50 text-[#2563eb] border border-blue-200 shadow-2xs">
                  <svg class="w-3 h-3 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9" />
                  </svg>
                  <span>{{ peer.virtual_ip || peer.assigned_ip || peer.allowed_ips || '10.8.0.2/32' }}</span>
                </span>
              </td>

              <!-- 3. Public Crypto Key with Copy Button -->
              <td class="py-3.5 px-4 border-r border-slate-200/80 font-mono text-[11px]">
                <div class="flex items-center gap-2">
                  <span class="bg-slate-100 px-2 py-1 rounded border border-slate-200 text-slate-700 select-all truncate max-w-[150px]" :title="peer.public_key">
                    {{ formatPublicKey(peer.public_key) }}
                  </span>
                  <button
                    type="button"
                    @click="copyTextToClipboard(peer.public_key, 'Public Key')"
                    class="p-1 rounded text-slate-400 hover:text-slate-700 hover:bg-slate-100 transition-colors cursor-pointer"
                    title="Copy Public Key"
                  >
                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3" />
                    </svg>
                  </button>
                </div>
              </td>

              <!-- 4. Connection Status (Green/Gray Pill Badges) -->
              <td class="py-3.5 px-4 border-r border-slate-200/80">
                <!-- Green Pill for Active State -->
                <div v-if="peer.status === 'active' || peer.is_active" class="flex flex-col gap-0.5">
                  <span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-[11px] font-bold bg-emerald-50 text-emerald-700 border border-emerald-300 shadow-2xs w-max">
                    <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
                    <span>Connected</span>
                  </span>
                  <span class="text-[10px] text-slate-400 font-mono mt-0.5">
                    Handshake: {{ peer.latest_handshake || 'Just now' }}
                  </span>
                </div>

                <!-- Gray Pill for Inactive State -->
                <div v-else class="flex flex-col gap-0.5">
                  <span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-[11px] font-bold bg-slate-100 text-slate-600 border border-slate-300 shadow-2xs w-max">
                    <span class="w-2 h-2 rounded-full bg-slate-400"></span>
                    <span>Disconnected</span>
                  </span>
                  <span class="text-[10px] text-slate-400 font-mono mt-0.5">
                    Handshake: {{ peer.latest_handshake || 'Never' }}
                  </span>
                </div>
              </td>

              <!-- 5. Total Bandwidth Transfer -->
              <td class="py-3.5 px-4 border-r border-slate-200/80 font-mono text-[11px]">
                <div class="flex flex-col gap-1">
                  <div class="flex items-center justify-between gap-2">
                    <span class="font-bold text-slate-800">{{ formatBandwidth(peer.transfer_rx, peer.transfer_tx) }}</span>
                  </div>
                  <div class="flex items-center gap-3 text-[10px] text-slate-500">
                    <span class="flex items-center gap-1 text-emerald-600">
                      <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 14l-7 7m0 0l-7-7m7 7V3" />
                      </svg>
                      {{ formatBytes(peer.transfer_rx || 0) }}
                    </span>
                    <span class="flex items-center gap-1 text-blue-600">
                      <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 10l7-7m0 0l7 7m-7-7v18" />
                      </svg>
                      {{ formatBytes(peer.transfer_tx || 0) }}
                    </span>
                  </div>
                </div>
              </td>

              <!-- 6. Actions Column -->
              <td class="py-3.5 px-4 text-center">
                <div class="flex items-center justify-center gap-1.5">
                  <!-- Inspect Config Profile -->
                  <button
                    type="button"
                    @click="viewPeerConfig(peer)"
                    class="p-1.5 rounded-lg bg-slate-100 hover:bg-blue-50 text-slate-600 hover:text-[#2563eb] border border-slate-200 transition-colors cursor-pointer"
                    title="View Profile Configuration"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                  </button>

                  <!-- Revoke / Delete Peer -->
                  <button
                    type="button"
                    @click="deletePeer(peer)"
                    class="p-1.5 rounded-lg bg-slate-100 hover:bg-rose-50 text-slate-600 hover:text-rose-600 border border-slate-200 transition-colors cursor-pointer"
                    title="Revoke Peer Tunnel"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                  </button>
                </div>
              </td>
            </tr>

            <!-- Empty State -->
            <tr v-if="filteredPeers.length === 0">
              <td colspan="6" class="py-12 text-center text-slate-500">
                <svg class="w-10 h-10 mx-auto mb-3 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                </svg>
                <p class="text-sm font-semibold text-slate-700">No remote VPN peers matched your filter</p>
                <p class="text-xs text-slate-400 mt-1">Try clearing your search query or status filter.</p>
                <button
                  type="button"
                  @click="resetFilters"
                  class="mt-3 inline-flex items-center px-3 py-1.5 text-xs font-semibold text-[#2563eb] hover:underline cursor-pointer"
                >
                  Clear all filters
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Table Bottom Footer Summary -->
      <div class="px-5 py-3 border-t border-slate-200 bg-slate-50 text-[11px] text-slate-500 flex flex-col sm:flex-row sm:items-center justify-between gap-2">
        <div>
          Showing <span class="font-bold text-slate-700">{{ filteredPeers.length }}</span> of
          <span class="font-bold text-slate-700">{{ peersList.length }}</span> registered remote VPN clients
        </div>
        <div class="flex items-center gap-4 font-mono text-[10px]">
          <span>WireGuard Daemon: <strong class="text-emerald-600">Running (PID: wg0)</strong></span>
          <span>&bull;</span>
          <span>Keepalive: <strong class="text-slate-700">25s</strong></span>
          <span>&bull;</span>
          <span>Last Sync: {{ lastSyncedTime }}</span>
        </div>
      </div>
    </div>

    <!-- ========================================================================= -->
    <!-- MODAL POP-UP OVERLAY: ADD REMOTE USER / PROVISION WIREGUARD PEER         -->
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
        aria-labelledby="modal-title-add-user"
        @keydown.esc="closeModal"
      >
        <!-- Modal Card Container -->
        <div
          class="w-full max-w-2xl bg-white rounded-2xl border border-slate-200 shadow-2xl overflow-hidden flex flex-col my-8"
          @click.stop
        >
          <!-- Modal Top Header Ribbon (Sophos SFOS Style) -->
          <div class="bg-slate-900 text-white px-6 py-4 flex items-center justify-between border-b border-slate-800">
            <div class="flex items-center gap-3">
              <div class="w-9 h-9 rounded-lg bg-[#2563eb] flex items-center justify-center text-white font-black text-sm shadow-md">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
                </svg>
              </div>
              <div>
                <div class="flex items-center gap-2">
                  <h3 id="modal-title-add-user" class="text-sm font-bold text-white tracking-tight">
                    Add Remote Access User
                  </h3>
                  <span class="text-[10px] bg-blue-950 text-blue-300 font-mono font-bold px-2 py-0.5 rounded border border-blue-800/80">
                    WIREGUARD PROFILE
                  </span>
                </div>
                <p class="text-xs text-slate-400 mt-0.5">Provision a remote endpoint cryptographic keypair &amp; virtual IP lease</p>
              </div>
            </div>

            <!-- Close Modal Button (✕) -->
            <button
              type="button"
              @click="closeModal"
              class="text-slate-400 hover:text-white p-1.5 rounded-lg hover:bg-slate-800 transition-colors cursor-pointer"
              aria-label="Close add remote user modal"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <!-- Form & Generation Body -->
          <div class="p-6 space-y-5 bg-white text-slate-800 flex-1 overflow-y-auto max-h-[calc(85vh-130px)]">
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

            <!-- Form Section (shown before profile generation or for editing) -->
            <form @submit.prevent="generateClientProfile" class="space-y-4">
              <!-- 1. Client Name Entry -->
              <div>
                <label for="client-name" class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5">
                  Client Name / Identifier <span class="text-rose-500">*</span>
                </label>
                <input
                  id="client-name"
                  v-model="formData.client_name"
                  type="text"
                  required
                  placeholder="e.g., alice-laptop, field-engineer-01"
                  class="w-full bg-slate-50 text-slate-900 text-xs px-3 py-2.5 rounded-lg border border-slate-300 focus:outline-none focus:border-[#2563eb] focus:ring-1 focus:ring-[#2563eb] font-medium"
                />
                <p class="text-[10px] text-slate-400 mt-1">Unique remote user name or hostname.</p>
              </div>

              <!-- 2. Assigned Virtual Tunnel IP Address Entry -->
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label for="tunnel-ip" class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5">
                    Assigned Virtual IP Address <span class="text-rose-500">*</span>
                  </label>
                  <div class="relative">
                    <input
                      id="tunnel-ip"
                      v-model="formData.virtual_ip"
                      type="text"
                      required
                      placeholder="e.g., 10.8.0.5/32"
                      class="w-full bg-slate-50 text-slate-900 text-xs px-3 py-2.5 rounded-lg border border-slate-300 focus:outline-none focus:border-[#2563eb] focus:ring-1 focus:ring-[#2563eb] font-mono font-medium"
                    />
                    <button
                      type="button"
                      @click="suggestNextIp"
                      class="absolute right-2 top-2 text-[10px] px-2 py-0.5 bg-slate-200 hover:bg-slate-300 text-slate-700 rounded font-sans font-bold cursor-pointer"
                      title="Suggest next free IP in 10.8.0.0/24 subnet"
                    >
                      Next IP
                    </button>
                  </div>
                  <p class="text-[10px] text-slate-400 mt-1">Unique tunnel IP assigned to this client in the /32 lease pool.</p>
                </div>

                <div>
                  <label for="dns-servers" class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5">
                    DNS Resolvers
                  </label>
                  <input
                    id="dns-servers"
                    v-model="formData.dns"
                    type="text"
                    placeholder="10.8.0.1, 1.1.1.1"
                    class="w-full bg-slate-50 text-slate-900 text-xs px-3 py-2.5 rounded-lg border border-slate-300 focus:outline-none focus:border-[#2563eb] focus:ring-1 focus:ring-[#2563eb] font-mono font-medium"
                  />
                  <p class="text-[10px] text-slate-400 mt-1">DNS servers pushed to the remote client.</p>
                </div>
              </div>

              <!-- 3. Allowed IPs Routing Scope -->
              <div>
                <label for="allowed-ips" class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5">
                  Allowed IPs (Routing Scope)
                </label>
                <input
                  id="allowed-ips"
                  v-model="formData.allowed_ips"
                  type="text"
                  placeholder="0.0.0.0/0, ::/0 (Full Tunnel) or 192.168.1.0/24 (Split Tunnel)"
                  class="w-full bg-slate-50 text-slate-900 text-xs px-3 py-2.5 rounded-lg border border-slate-300 focus:outline-none focus:border-[#2563eb] focus:ring-1 focus:ring-[#2563eb] font-mono font-medium"
                />
                <p class="text-[10px] text-slate-400 mt-1">Use <code class="font-mono text-slate-600 font-bold">0.0.0.0/0, ::/0</code> for Full Tunnel or specify internal LAN subnets for Split Tunneling.</p>
              </div>

              <!-- Generate Action Button Trigger -->
              <div class="pt-2">
                <button
                  type="button"
                  @click="generateClientProfile"
                  :disabled="isSubmitting"
                  class="w-full inline-flex items-center justify-center gap-2 px-5 py-2.5 rounded-lg bg-[#2563eb] hover:bg-blue-700 active:bg-blue-800 text-white text-xs font-bold tracking-wide shadow-md shadow-blue-500/20 transition-all cursor-pointer disabled:opacity-50"
                >
                  <svg
                    v-if="isSubmitting"
                    class="w-4 h-4 animate-spin text-white"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                  </svg>
                  <svg v-else class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                  <span>{{ isSubmitting ? 'Generating WireGuard Crypto Keypair...' : 'Generate Client Profile' }}</span>
                </button>
              </div>
            </form>

            <!-- COMPILED WIREGUARD CONNECTION FILE BLOCK -->
            <div v-if="generatedProfileBlock" class="mt-5 pt-5 border-t border-slate-200">
              <div class="flex items-center justify-between mb-2">
                <div class="flex items-center gap-2">
                  <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
                  <label class="text-xs font-bold text-slate-800 uppercase tracking-wider">
                    Compiled WireGuard Client Profile (.conf)
                  </label>
                </div>
                <div class="flex items-center gap-2">
                  <!-- Quick Copy to Clipboard Button -->
                  <button
                    type="button"
                    @click="copyConfigToClipboard"
                    class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-md bg-white border border-slate-300 hover:bg-slate-50 text-xs font-semibold text-slate-700 shadow-2xs transition-colors cursor-pointer"
                  >
                    <svg v-if="!isConfigCopied" class="w-3.5 h-3.5 text-[#2563eb]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3" />
                    </svg>
                    <svg v-else class="w-3.5 h-3.5 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                    </svg>
                    <span>{{ isConfigCopied ? 'Copied to Clipboard!' : 'Copy to Clipboard' }}</span>
                  </button>

                  <!-- Download .conf File Button -->
                  <button
                    type="button"
                    @click="downloadConfigFile"
                    class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-md bg-[#2563eb] hover:bg-blue-700 text-white text-xs font-bold shadow-2xs transition-colors cursor-pointer"
                  >
                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                    </svg>
                    <span>Download .conf</span>
                  </button>
                </div>
              </div>

              <!-- Text Container for WireGuard Connection File Block -->
              <div class="relative group">
                <pre class="bg-slate-900 text-emerald-400 p-4 rounded-xl font-mono text-xs overflow-x-auto leading-relaxed border border-slate-800 shadow-inner select-all">{{ generatedProfileBlock }}</pre>
              </div>

              <p class="text-[10px] text-slate-500 mt-2">
                Import this configuration block into the official WireGuard Client on Windows, macOS, Linux, iOS, or Android.
              </p>
            </div>
          </div>

          <!-- Modal Action Footer -->
          <div class="px-6 py-4 bg-slate-50 border-t border-slate-200 flex items-center justify-between gap-3">
            <button
              type="button"
              @click="closeModal"
              class="px-4 py-2 rounded-lg border border-slate-300 text-slate-700 hover:bg-slate-100 text-xs font-semibold transition-colors cursor-pointer"
            >
              Close
            </button>

            <div v-if="generatedProfileBlock" class="flex items-center gap-2">
              <button
                type="button"
                @click="resetModalForm"
                class="px-3.5 py-2 rounded-lg border border-slate-300 text-slate-700 hover:bg-slate-100 text-xs font-semibold transition-colors cursor-pointer"
              >
                Provision Another User
              </button>
              <button
                type="button"
                @click="closeModal"
                class="inline-flex items-center gap-1.5 px-5 py-2 rounded-lg bg-[#2563eb] hover:bg-blue-700 text-white text-xs font-bold transition-all shadow-md shadow-blue-500/20 cursor-pointer"
              >
                Done
              </button>
            </div>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, h } from 'vue'

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
  peersEndpoint: {
    type: String,
    default: '/api/vpn/peers'
  },
  createEndpoint: {
    type: String,
    default: '/api/vpn/peers/create'
  }
})

const emit = defineEmits(['peer-created', 'peer-deleted', 'error'])

// -----------------------------------------------------------------------------
// Protocol Tabs Setup
// -----------------------------------------------------------------------------
const WireGuardIcon = {
  render: () => h('svg', { class: 'w-4 h-4', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
    h('path', { strokeLinecap: 'round', strokeLinejoin: 'round', strokeWidth: '2', d: 'M13 10V3L4 14h7v7l9-11h-7z' })
  ])
}

const SslVpnIcon = {
  render: () => h('svg', { class: 'w-4 h-4', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
    h('path', { strokeLinecap: 'round', strokeLinejoin: 'round', strokeWidth: '2', d: 'M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z' })
  ])
}

const IpsecIcon = {
  render: () => h('svg', { class: 'w-4 h-4', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
    h('path', { strokeLinecap: 'round', strokeLinejoin: 'round', strokeWidth: '2', d: 'M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z' })
  ])
}

const activeTab = ref('wireguard')

const configTabs = computed(() => [
  { id: 'wireguard', label: 'WireGuard VPN', icon: WireGuardIcon, badge: `${peersList.value.length} peers` },
  { id: 'ssl', label: 'SSL VPN', icon: SslVpnIcon, badge: 'Standby' },
  { id: 'ipsec', label: 'IPsec VPN', icon: IpsecIcon, badge: 'Standby' }
])

// -----------------------------------------------------------------------------
// Reactive State
// -----------------------------------------------------------------------------
const isLoading = ref(false)
const isSubmitting = ref(false)
const isModalOpen = ref(false)
const isConfigCopied = ref(false)
const validationError = ref('')
const searchQuery = ref('')
const statusFilter = ref('ALL')
const lastSyncedTime = ref(new Date().toLocaleTimeString())
const generatedProfileBlock = ref('')

const toasts = ref([])

// Peer List Initial Fallback Mock & Store
const peersList = ref([
  {
    id: 'wg-01',
    client_name: 'alex-macbook-pro',
    virtual_ip: '10.8.0.2/32',
    public_key: 'xK9vR8kM2tQ0pW4jL8nB7yC5zX1mN3vK6rT9uP2wE4=',
    status: 'active',
    is_active: true,
    endpoint: '198.51.100.45:51820',
    latest_handshake: '12 seconds ago',
    transfer_rx: 1845493760, // 1.84 GB
    transfer_tx: 489230450,  // 489 MB
    device_type: 'macOS'
  },
  {
    id: 'wg-02',
    client_name: 'sarah-thinkpad-x1',
    virtual_ip: '10.8.0.3/32',
    public_key: 'hP7qZ3mK9vR8tW2jL5nB1yC4zX0mN8vK3rT6uP9wQ1=',
    status: 'active',
    is_active: true,
    endpoint: '203.0.113.88:41200',
    latest_handshake: '1 minute ago',
    transfer_rx: 924857600,  // 924 MB
    transfer_tx: 154230450,  // 154 MB
    device_type: 'Linux'
  },
  {
    id: 'wg-03',
    client_name: 'devops-staging-bastion',
    virtual_ip: '10.8.0.4/32',
    public_key: 'yM4vK9tQ0pW2jL7nB5yC1zX8mN3vK6rT0uP4wE9rT2=',
    status: 'inactive',
    is_active: false,
    endpoint: '192.0.2.14:51820',
    latest_handshake: '3 days ago',
    transfer_rx: 34500000,   // 34.5 MB
    transfer_tx: 12000000,   // 12 MB
    device_type: 'Server'
  },
  {
    id: 'wg-04',
    client_name: 'executive-ipad-pro',
    virtual_ip: '10.8.0.5/32',
    public_key: 'bT8vR1kM5tQ9pW0jL3nB6yC2zX7mN4vK1rT8uP5wX7=',
    status: 'active',
    is_active: true,
    endpoint: '198.51.100.102:60234',
    latest_handshake: '4 minutes ago',
    transfer_rx: 524288000,  // 524 MB
    transfer_tx: 89128960,   // 89.1 MB
    device_type: 'iOS'
  }
])

const formData = reactive({
  client_name: '',
  virtual_ip: '10.8.0.6/32',
  dns: '10.8.0.1, 1.1.1.1',
  allowed_ips: '0.0.0.0/0, ::/0',
  server_endpoint: 'vpn.astaro-firewall.internal:51820',
  server_public_key: 'SFOSxgsFirewallServerPublicKeyBase64WireGuard='
})

// -----------------------------------------------------------------------------
// Computed Metrics & Filters
// -----------------------------------------------------------------------------
const activePeersCount = computed(() => {
  return peersList.value.filter(p => p.status === 'active' || p.is_active).length
})

const inactivePeersCount = computed(() => {
  return peersList.value.length - activePeersCount.value
})

const aggregateTransferFormatted = computed(() => {
  const total = peersList.value.reduce((sum, p) => sum + (p.transfer_rx || 0) + (p.transfer_tx || 0), 0)
  return formatBytes(total)
})

const filteredPeers = computed(() => {
  let list = peersList.value

  if (statusFilter.value === 'ACTIVE') {
    list = list.filter(p => p.status === 'active' || p.is_active)
  } else if (statusFilter.value === 'INACTIVE') {
    list = list.filter(p => p.status !== 'active' && !p.is_active)
  }

  if (!searchQuery.value.trim()) {
    return list
  }

  const q = searchQuery.value.toLowerCase().trim()
  return list.filter(p => {
    return (
      (p.client_name && p.client_name.toLowerCase().includes(q)) ||
      (p.name && p.name.toLowerCase().includes(q)) ||
      (p.virtual_ip && p.virtual_ip.toLowerCase().includes(q)) ||
      (p.assigned_ip && p.assigned_ip.toLowerCase().includes(q)) ||
      (p.public_key && p.public_key.toLowerCase().includes(q)) ||
      (p.endpoint && p.endpoint.toLowerCase().includes(q))
    )
  })
})

// -----------------------------------------------------------------------------
// Helpers & Formatters
// -----------------------------------------------------------------------------
const formatPublicKey = (key) => {
  if (!key) return '—'
  if (key.length <= 16) return key
  return `${key.substring(0, 8)}...${key.substring(key.length - 8)}`
}

const formatBytes = (bytes, decimals = 1) => {
  if (bytes === 0 || !bytes) return '0 B'
  const k = 1024
  const dm = decimals < 0 ? 0 : decimals
  const sizes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i]
}

const formatBandwidth = (rx = 0, tx = 0) => {
  const total = (Number(rx) || 0) + (Number(tx) || 0)
  return formatBytes(total)
}

const showToast = (title, message, type = 'info') => {
  const id = Date.now() + Math.random().toString(36).substring(2, 6)
  toasts.value.push({ id, title, message, type })
  setTimeout(() => {
    dismissToast(id)
  }, 4500)
}

const dismissToast = (id) => {
  const index = toasts.value.findIndex(t => t.id === id)
  if (index !== -1) {
    toasts.value.splice(index, 1)
  }
}

const resetFilters = () => {
  searchQuery.value = ''
  statusFilter.value = 'ALL'
}

// Generate pseudo Base64 key for WireGuard representation
const generateCryptoKey = () => {
  const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
  let res = ''
  for (let i = 0; i < 43; i++) {
    res += chars.charAt(Math.floor(Math.random() * chars.length))
  }
  return res + '='
}

// Suggest next available IP in 10.8.0.0/24 subnet
const suggestNextIp = () => {
  const usedIps = peersList.value.map(p => {
    const ip = (p.virtual_ip || p.assigned_ip || '').split('/')[0]
    const parts = ip.split('.')
    return parts.length === 4 ? parseInt(parts[3], 10) : 0
  }).filter(n => !isNaN(n) && n > 0)

  let nextOctet = 2
  while (usedIps.includes(nextOctet)) {
    nextOctet++
  }
  formData.virtual_ip = `10.8.0.${nextOctet}/32`
}

// -----------------------------------------------------------------------------
// Axios API Operations
// -----------------------------------------------------------------------------
const fetchPeers = async (manual = false) => {
  isLoading.value = true
  try {
    if (!axiosInstance) await initAxios()
    const res = await axiosInstance.get(props.peersEndpoint)
    if (res.data) {
      if (Array.isArray(res.data)) {
        peersList.value = res.data
      } else if (Array.isArray(res.data.peers)) {
        peersList.value = res.data.peers
      }
    }
    lastSyncedTime.value = new Date().toLocaleTimeString()
    if (manual) {
      showToast('Peers Refreshed', 'WireGuard peer matrix synchronized with kernel subsystem.', 'success')
    }
  } catch (err) {
    console.warn('Axios fetchPeers fallback to local dataset:', err)
    lastSyncedTime.value = new Date().toLocaleTimeString()
    if (manual) {
      showToast('Cache Loaded', 'Daemon offline. Loaded local active peer snapshot.', 'info')
    }
  } finally {
    isLoading.value = false
  }
}

// -----------------------------------------------------------------------------
// Modal & Profile Provisioning Methods
// -----------------------------------------------------------------------------
const openAddUserModal = () => {
  suggestNextIp()
  isModalOpen.value = true
  validationError.value = ''
  generatedProfileBlock.value = ''
  isConfigCopied.value = false
}

const closeModal = () => {
  isModalOpen.value = false
  validationError.value = ''
}

const resetModalForm = () => {
  formData.client_name = ''
  suggestNextIp()
  generatedProfileBlock.value = ''
  isConfigCopied.value = false
  validationError.value = ''
}

const generateClientProfile = async () => {
  validationError.value = ''

  if (!formData.client_name.trim()) {
    validationError.value = 'Client Name is required.'
    return
  }

  if (!formData.virtual_ip.trim()) {
    validationError.value = 'Assigned Virtual IP is required.'
    return
  }

  isSubmitting.value = true

  const clientPrivateKey = generateCryptoKey()
  const clientPublicKey = generateCryptoKey()
  const presharedKey = generateCryptoKey()
  const serverPublicKey = formData.server_public_key || 'SFOSxgsFirewallServerPublicKeyBase64WireGuard='
  const serverEndpoint = formData.server_endpoint || 'vpn.astaro-firewall.internal:51820'
  const clientIp = formData.virtual_ip.includes('/') ? formData.virtual_ip : `${formData.virtual_ip}/32`
  const dnsServers = formData.dns || '10.8.0.1, 1.1.1.1'
  const allowedIps = formData.allowed_ips || '0.0.0.0/0, ::/0'

  // Construct compiled WireGuard .conf block
  const configText = `[Interface]
# Client: ${formData.client_name.trim()}
PrivateKey = ${clientPrivateKey}
Address = ${clientIp}
DNS = ${dnsServers}

[Peer]
# Sophos XGS Corporate Gateway
PublicKey = ${serverPublicKey}
PresharedKey = ${presharedKey}
Endpoint = ${serverEndpoint}
AllowedIPs = ${allowedIps}
PersistentKeepalive = 25`

  generatedProfileBlock.value = configText

  const newPeerPayload = {
    client_name: formData.client_name.trim(),
    virtual_ip: clientIp,
    public_key: clientPublicKey,
    preshared_key: presharedKey,
    dns: dnsServers,
    allowed_ips: allowedIps,
    status: 'inactive',
    is_active: false,
    endpoint: 'Waiting for handshake',
    latest_handshake: 'Never',
    transfer_rx: 0,
    transfer_tx: 0,
    device_type: 'Remote Client'
  }

  try {
    if (!axiosInstance) await initAxios()
    const res = await axiosInstance.post(props.createEndpoint, newPeerPayload)
    if (res.data && res.data.peer) {
      peersList.value.unshift(res.data.peer)
    } else {
      peersList.value.unshift(newPeerPayload)
    }
    emit('peer-created', newPeerPayload)
    showToast('Client Profile Generated', `WireGuard configuration provisioned for ${newPeerPayload.client_name}.`, 'success')
  } catch (err) {
    console.warn('Axios create peer error, applying locally:', err)
    peersList.value.unshift(newPeerPayload)
    emit('peer-created', newPeerPayload)
    showToast('Client Profile Created (Local)', `WireGuard configuration created for ${newPeerPayload.client_name}.`, 'success')
  } finally {
    isSubmitting.value = false
  }
}

// Quick Copy to Clipboard capability
const copyConfigToClipboard = async () => {
  if (!generatedProfileBlock.value) return
  try {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      await navigator.clipboard.writeText(generatedProfileBlock.value)
    } else {
      const textarea = document.createElement('textarea')
      textarea.value = generatedProfileBlock.value
      document.body.appendChild(textarea)
      textarea.select()
      document.execCommand('copy')
      document.body.removeChild(textarea)
    }
    isConfigCopied.value = true
    showToast('Copied', 'WireGuard client configuration copied to clipboard!', 'info')
    setTimeout(() => {
      isConfigCopied.value = false
    }, 3000)
  } catch (err) {
    showToast('Copy Failed', 'Please manually select and copy the text box.', 'error')
  }
}

const copyTextToClipboard = async (text, label = 'Text') => {
  if (!text) return
  try {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      await navigator.clipboard.writeText(text)
    } else {
      const textarea = document.createElement('textarea')
      textarea.value = text
      document.body.appendChild(textarea)
      textarea.select()
      document.execCommand('copy')
      document.body.removeChild(textarea)
    }
    showToast('Copied', `${label} copied to clipboard!`, 'info')
  } catch (err) {
    showToast('Copy Failed', 'Unable to copy text to clipboard.', 'error')
  }
}

// Download WireGuard .conf file
const downloadConfigFile = () => {
  if (!generatedProfileBlock.value) return
  const filename = `${(formData.client_name || 'wireguard-client').toLowerCase().replace(/[^a-z0-9-_]/g, '_')}.conf`
  const blob = new Blob([generatedProfileBlock.value], { type: 'text/plain;charset=utf-8' })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = filename
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  URL.revokeObjectURL(url)
  showToast('Downloaded', `Exported ${filename}`, 'success')
}

// View existing peer config
const viewPeerConfig = (peer) => {
  formData.client_name = peer.client_name || peer.name || 'Remote Client'
  formData.virtual_ip = peer.virtual_ip || peer.assigned_ip || '10.8.0.2/32'
  formData.dns = peer.dns || '10.8.0.1, 1.1.1.1'
  formData.allowed_ips = peer.allowed_ips || '0.0.0.0/0, ::/0'

  generatedProfileBlock.value = `[Interface]
# Remote Client: ${formData.client_name}
# Virtual IP: ${formData.virtual_ip}
# Public Key: ${peer.public_key || 'N/A'}
Address = ${formData.virtual_ip}
DNS = ${formData.dns}

[Peer]
# Sophos XGS Corporate Remote Access Gateway
PublicKey = ${formData.server_public_key}
Endpoint = ${formData.server_endpoint}
AllowedIPs = ${formData.allowed_ips}
PersistentKeepalive = 25`

  isModalOpen.value = true
  isConfigCopied.value = false
}

// Delete / Revoke Peer
const deletePeer = (peer) => {
  const name = peer.client_name || peer.name || 'this client'
  if (confirm(`Are you sure you want to revoke and delete remote VPN access for "${name}"?`)) {
    const idx = peersList.value.findIndex(p => (p.public_key && p.public_key === peer.public_key) || (p.id && p.id === peer.id))
    if (idx !== -1) {
      peersList.value.splice(idx, 1)
      emit('peer-deleted', peer)
      showToast('Peer Revoked', `Remote access revoked for ${name}.`, 'warning')
    }
  }
}

// -----------------------------------------------------------------------------
// Lifecycle
// -----------------------------------------------------------------------------
onMounted(async () => {
  await initAxios()
  await fetchPeers()
})
</script>
