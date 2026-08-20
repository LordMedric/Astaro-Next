<template>
  <div class="space-y-6">
    <!-- Top Header Banner (Astaro-Next Slate-900 / Modernized Style) -->
    <div class="bg-slate-900 text-white rounded-2xl p-6 shadow-xl border border-slate-800 flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div>
        <div class="flex items-center gap-2 mb-1">
          <div class="w-8 h-8 rounded-lg bg-[#ee7f00] flex items-center justify-center text-white font-black text-sm">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9" />
            </svg>
          </div>
          <h1 class="text-xl font-bold tracking-tight">Webserver Protection (WAF)</h1>
          <span class="text-[10px] bg-orange-950 text-orange-300 font-mono font-bold px-2 py-0.5 rounded border border-orange-800/80">
            NGINX &amp; NAXSI L7
          </span>
        </div>
        <p class="text-xs text-slate-400">
          Publish web applications with SSL offloading, Reverse Proxy load balancing, Site Path routing, and Layer 7 Web Application Firewall threat protection.
        </p>
      </div>

      <div class="flex items-center gap-2">
        <button
          type="button"
          @click="isLiveLogOpen = true"
          class="px-3.5 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-xl text-xs font-semibold flex items-center gap-1.5 transition-colors cursor-pointer"
        >
          <svg class="w-3.5 h-3.5 text-[#0072ce]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          <span>Open Live Log</span>
        </button>

        <button
          type="button"
          @click="openNginxPreview"
          class="px-3 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-xl text-xs font-semibold flex items-center gap-1.5 transition-colors cursor-pointer"
          title="Inspect generated Nginx & NAXSI configuration"
        >
          <svg class="w-3.5 h-3.5 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
          </svg>
          <span>nginx.conf</span>
        </button>

        <button
          type="button"
          @click="openCreateModal"
          class="px-4 py-2 bg-[#0072ce] hover:bg-blue-600 text-white rounded-xl text-xs font-bold shadow-lg shadow-blue-500/20 flex items-center gap-1.5 transition-all cursor-pointer"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          <span>+ New {{ activeTabLabel }}...</span>
        </button>
      </div>
    </div>

    <!-- Tab Navigation Strip (All 5 Sophos UTM 9 Tabs) -->
    <div class="flex border-b border-slate-200 gap-1 bg-[#f4f6f9] p-1.5 rounded-t-xl overflow-x-auto">
      <button
        v-for="tab in tabs"
        :key="tab.id"
        type="button"
        @click="activeTab = tab.id"
        :class="[
          'px-4 py-2 text-xs font-bold rounded-lg transition-all flex items-center gap-2 cursor-pointer whitespace-nowrap',
          activeTab === tab.id
            ? 'bg-white text-slate-900 shadow-xs border-b-2 border-[#ee7f00]'
            : 'text-slate-600 hover:text-slate-900 hover:bg-white/60'
        ]"
      >
        <span>{{ tab.label }}</span>
        <span
          v-if="tab.badge !== undefined"
          class="px-1.5 py-0.2 rounded-full text-[10px] font-mono font-bold"
          :class="activeTab === tab.id ? 'bg-[#0072ce] text-white' : 'bg-slate-200 text-slate-700'"
        >
          {{ tab.badge }}
        </span>
      </button>
    </div>

    <!-- Search & Filter Controls Toolbar -->
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 bg-white p-3.5 rounded-xl border border-slate-200 shadow-2xs text-xs">
      <div class="flex items-center gap-2 w-full sm:w-80">
        <div class="relative w-full">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search virtual servers, domains, real backends..."
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
            <option value="status">Status</option>
            <option value="port">Port</option>
          </select>
        </div>

        <div class="flex items-center gap-2">
          <span>Display:</span>
          <select class="bg-slate-50 border border-slate-200 rounded-lg px-2 py-1 text-xs text-slate-700 font-bold">
            <option>100</option>
            <option>50</option>
            <option>20</option>
          </select>
        </div>

        <span class="font-mono text-slate-600 font-bold">
          1-{{ filteredVirtualServers.length }} of {{ virtualServers.length }}
        </span>
      </div>
    </div>

    <!-- TAB 1: VIRTUAL WEBSERVERS (CARD LIST - MATCHING SOPHOS UTM 9 LAYOUT) -->
    <div v-if="activeTab === 'virtual'" class="space-y-4">
      <div v-if="filteredVirtualServers.length === 0" class="p-12 text-center bg-white rounded-2xl border border-slate-200 text-slate-400 text-xs">
        No virtual webservers match your search criteria. Click "+ New Virtual Webserver..." to create one.
      </div>

      <div
        v-for="vs in filteredVirtualServers"
        :key="vs.id"
        class="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden hover:border-slate-300 transition-all"
      >
        <div class="p-5 flex flex-col lg:flex-row lg:items-center justify-between gap-4 border-b border-slate-100 bg-slate-50/50">
          <div class="flex items-start sm:items-center gap-3.5">
            <!-- Toggle Switch (Sophos UTM Green / Grey Style) -->
            <button
              type="button"
              @click="toggleVirtualServer(vs)"
              class="relative inline-flex h-5 w-10 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none"
              :class="vs.enabled ? 'bg-emerald-500' : 'bg-slate-300'"
              title="Toggle Virtual Webserver state"
            >
              <span
                class="inline-block h-4 w-4 transform rounded-full bg-white shadow-xs transition duration-200"
                :class="vs.enabled ? 'translate-x-5' : 'translate-x-0'"
              ></span>
            </button>

            <div>
              <div class="flex items-center gap-2">
                <h3 class="text-sm font-bold text-slate-900 tracking-tight">{{ vs.name }}</h3>
                <span v-if="vs.ssl" class="px-2 py-0.2 rounded text-[10px] font-bold bg-emerald-100 text-emerald-800 border border-emerald-200 font-mono">
                  HTTPS :{{ vs.port || 443 }}
                </span>
                <span v-else class="px-2 py-0.2 rounded text-[10px] font-bold bg-slate-100 text-slate-700 border border-slate-200 font-mono">
                  HTTP :{{ vs.port || 80 }}
                </span>
              </div>
              <p v-if="vs.comment" class="text-[11px] text-slate-500 mt-0.5">{{ vs.comment }}</p>
            </div>
          </div>

          <!-- Action Buttons: Edit / Delete / Clone (UTM 9 Parity) -->
          <div class="flex items-center gap-2 self-end lg:self-center">
            <button
              type="button"
              @click="editVirtualServer(vs)"
              class="px-2.5 py-1 bg-white hover:bg-slate-50 text-slate-700 border border-slate-300 rounded text-xs font-bold shadow-2xs flex items-center gap-1 cursor-pointer"
            >
              <svg class="w-3.5 h-3.5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
              </svg>
              <span>Edit</span>
            </button>

            <button
              type="button"
              @click="cloneVirtualServer(vs)"
              class="px-2.5 py-1 bg-white hover:bg-slate-50 text-slate-700 border border-slate-300 rounded text-xs font-bold shadow-2xs flex items-center gap-1 cursor-pointer"
            >
              <svg class="w-3.5 h-3.5 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
              </svg>
              <span>Clone</span>
            </button>

            <button
              type="button"
              @click="deleteVirtualServer(vs.id)"
              class="px-2.5 py-1 bg-white hover:bg-rose-50 text-rose-700 border border-rose-200 rounded text-xs font-bold shadow-2xs flex items-center gap-1 cursor-pointer"
            >
              <svg class="w-3.5 h-3.5 text-rose-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
              <span>Delete</span>
            </button>
          </div>
        </div>

        <!-- Card Metadata Grid (Exact Sophos UTM Structure) -->
        <div class="p-5 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 text-xs">
          <!-- Type Column -->
          <div class="space-y-1">
            <span class="text-slate-400 font-bold uppercase tracking-wider text-[10px]">Type:</span>
            <div class="font-medium text-slate-800">
              {{ vs.type || (vs.ssl ? 'Encrypted (HTTPS), Redirection enabled' : 'Plaintext (HTTP)') }}
            </div>
            <div class="text-[11px] text-slate-500 font-mono">
              Interface: {{ vs.interface || 'Uplink Interfaces (WAN)' }}
            </div>
          </div>

          <!-- Domains Column -->
          <div class="space-y-1">
            <span class="text-slate-400 font-bold uppercase tracking-wider text-[10px]">Domains:</span>
            <div class="space-y-0.5">
              <div
                v-for="d in getDomainsList(vs)"
                :key="d"
                class="font-mono font-bold text-[#0072ce] text-[11px] flex items-center gap-1"
              >
                <span>{{ d }}</span>
              </div>
            </div>
          </div>

          <!-- Site Path Routes & Real Webservers Column -->
          <div class="space-y-1">
            <span class="text-slate-400 font-bold uppercase tracking-wider text-[10px]">Site Path Routes:</span>
            <div class="flex items-center gap-2">
              <span class="font-mono font-bold text-slate-700 bg-slate-100 px-1.5 py-0.5 rounded text-[11px]">/</span>
              <div class="flex items-center gap-1.5 font-semibold text-slate-800 text-[11px]">
                <svg class="w-3.5 h-3.5 text-emerald-500" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                </svg>
                <span>{{ vs.real_servers && vs.real_servers.length ? vs.real_servers.join(', ') : vs.upstream }}</span>
              </div>
            </div>
          </div>

          <!-- Firewall Profile & Advanced Flags Column -->
          <div class="space-y-1">
            <span class="text-slate-400 font-bold uppercase tracking-wider text-[10px]">Firewall Profile:</span>
            <div>
              <span class="inline-block px-2 py-0.5 rounded bg-amber-50 text-amber-800 border border-amber-200 font-bold text-[10px]">
                {{ vs.profile || '*OWA & Exchange ActiveSync' }}
              </span>
            </div>
            <div class="text-[11px] text-slate-500 flex items-center gap-1 pt-1">
              <span class="font-semibold text-slate-600">Advanced:</span>
              <span>{{ vs.pass_host_header !== false ? 'Pass host header' : 'None' }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 2: REAL WEBSERVERS (BACKENDS) -->
    <div v-else-if="activeTab === 'real'" class="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
      <div class="px-5 py-4 bg-slate-50 border-b border-slate-200 flex items-center justify-between">
        <div>
          <h3 class="text-xs font-bold text-slate-800 uppercase tracking-wider">Backend Real Webservers Catalog</h3>
          <p class="text-[11px] text-slate-500 mt-0.5">Physical host nodes, internal application containers, and DMZ endpoints</p>
        </div>
        <span class="text-xs font-mono font-bold text-slate-500 bg-white px-2.5 py-1 rounded border border-slate-200">
          {{ realServers.length }} Backend(s)
        </span>
      </div>

      <div class="overflow-x-auto">
        <table class="w-full text-left text-xs border-collapse">
          <thead class="bg-[#f4f6f9] text-slate-700 font-bold border-b border-slate-200">
            <tr>
              <th class="p-3 pl-5">Status</th>
              <th class="p-3">Backend Name</th>
              <th class="p-3 font-mono">Host / IP Address</th>
              <th class="p-3">Protocol</th>
              <th class="p-3 font-mono">Port</th>
              <th class="p-3">Keepalive</th>
              <th class="p-3">Comment</th>
              <th class="p-3 pr-5 text-right">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100 font-medium text-slate-700">
            <tr
              v-for="rs in realServers"
              :key="rs.id"
              class="hover:bg-slate-50/80 transition-colors"
            >
              <td class="p-3 pl-5">
                <span
                  class="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-bold font-mono"
                  :class="rs.enabled !== false ? 'bg-emerald-100 text-emerald-800' : 'bg-slate-200 text-slate-600'"
                >
                  <span class="w-1.5 h-1.5 rounded-full" :class="rs.enabled !== false ? 'bg-emerald-500' : 'bg-slate-400'"></span>
                  {{ rs.enabled !== false ? 'ENABLED' : 'DISABLED' }}
                </span>
              </td>
              <td class="p-3 font-bold text-slate-900">{{ rs.name }}</td>
              <td class="p-3 font-mono font-bold text-[#0072ce]">{{ rs.host }}</td>
              <td class="p-3">
                <span class="px-2 py-0.5 rounded text-[10px] font-bold uppercase bg-blue-50 text-[#0072ce] border border-blue-200">
                  {{ rs.protocol }}
                </span>
              </td>
              <td class="p-3 font-mono font-bold text-slate-900">{{ rs.port }}</td>
              <td class="p-3 text-slate-600">{{ rs.keepalive ? 'Enabled' : 'Disabled' }}</td>
              <td class="p-3 text-slate-500 text-[11px] truncate max-w-xs">{{ rs.comment || '—' }}</td>
              <td class="p-3 pr-5 text-right">
                <div class="flex items-center justify-end gap-2">
                  <button
                    type="button"
                    @click="deleteRealServer(rs.id)"
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

    <!-- TAB 3: SITE PATH ROUTING -->
    <div v-else-if="activeTab === 'site_path'" class="bg-white rounded-2xl border border-slate-200 shadow-sm p-6 space-y-4">
      <div class="flex items-center justify-between border-b border-slate-100 pb-3">
        <div>
          <h3 class="text-xs font-bold text-slate-800 uppercase tracking-wider">Site Path Routing Rules</h3>
          <p class="text-[11px] text-slate-500 mt-0.5">Route specific HTTP URL subpaths (e.g. /owa, /autodiscover, /api) to dedicated real server pools</p>
        </div>
        <span class="text-[10px] bg-purple-100 text-purple-800 font-mono font-bold px-2 py-1 rounded">
          L7 PATH ROUTER
        </span>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div class="p-4 rounded-xl bg-slate-50 border border-slate-200 space-y-2">
          <div class="flex items-center justify-between">
            <span class="font-bold text-slate-800 text-xs">/owa (Outlook Web Access)</span>
            <span class="text-[10px] bg-emerald-100 text-emerald-800 font-mono font-bold px-1.5 py-0.5 rounded">Active</span>
          </div>
          <p class="text-[11px] text-slate-600">Routes to Microsoft Exchange backend node with Form-Based Authentication.</p>
          <div class="text-[10px] font-mono text-slate-500 bg-white p-2 rounded border border-slate-200">
            Path: /owa/* &rarr; Real Servers: Mail Medric Net (192.168.1.50:443)
          </div>
        </div>

        <div class="p-4 rounded-xl bg-slate-50 border border-slate-200 space-y-2">
          <div class="flex items-center justify-between">
            <span class="font-bold text-slate-800 text-xs">/autodiscover (Exchange AutoDiscover)</span>
            <span class="text-[10px] bg-emerald-100 text-emerald-800 font-mono font-bold px-1.5 py-0.5 rounded">Active</span>
          </div>
          <p class="text-[11px] text-slate-600">Directs mobile ActiveSync client probes to AutoDiscover XML handler.</p>
          <div class="text-[10px] font-mono text-slate-500 bg-white p-2 rounded border border-slate-200">
            Path: /autodiscover/* &rarr; Real Servers: Medric Networks (192.168.1.50:443)
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 4: REQUEST REDIRECTION -->
    <div v-else-if="activeTab === 'redirection'" class="bg-white rounded-2xl border border-slate-200 shadow-sm p-6 space-y-4">
      <div class="flex items-center justify-between border-b border-slate-100 pb-3">
        <div>
          <h3 class="text-xs font-bold text-slate-800 uppercase tracking-wider">Request Redirections</h3>
          <p class="text-[11px] text-slate-500 mt-0.5">Automated HTTP-to-HTTPS upgrades and URI alias rewrites</p>
        </div>
        <span class="text-[10px] bg-blue-100 text-blue-800 font-mono font-bold px-2 py-1 rounded">
          HTTP 301 / 302
        </span>
      </div>

      <div class="p-4 rounded-xl bg-slate-50 border border-slate-200 space-y-2">
        <div class="flex items-center justify-between">
          <span class="font-bold text-slate-800 text-xs">HTTP to HTTPS Global Upgrade</span>
          <span class="text-[10px] bg-emerald-100 text-emerald-800 font-mono font-bold px-1.5 py-0.5 rounded">HTTP 301</span>
        </div>
        <p class="text-[11px] text-slate-600">Automatically redirects all plaintext port 80 traffic to TLS/SSL port 443 preserving query parameters.</p>
      </div>
    </div>

    <!-- TAB 5: ADVANCED & GLOBAL BUFFER SETTINGS -->
    <div v-else-if="activeTab === 'advanced'" class="bg-white rounded-2xl border border-slate-200 shadow-sm p-6 space-y-5">
      <div class="flex items-center justify-between border-b border-slate-100 pb-3">
        <div>
          <h3 class="text-xs font-bold text-slate-800 uppercase tracking-wider">WAF Engine Advanced Parameters</h3>
          <p class="text-[11px] text-slate-500 mt-0.5">Nginx proxy buffers, SlowHTTP mitigation, and NAXSI learning rules</p>
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-5 text-xs">
        <div class="p-4 rounded-xl border border-slate-200 space-y-3 bg-slate-50/50">
          <span class="font-bold text-slate-800">Buffer Limits &amp; Upload Sizes</span>
          <div class="space-y-2">
            <div>
              <label class="block text-[11px] font-bold text-slate-600 mb-1">Max Client Request Body (MB)</label>
              <input type="number" value="128" class="w-full p-2 bg-white border border-slate-300 rounded text-xs font-mono" />
            </div>
            <div>
              <label class="block text-[11px] font-bold text-slate-600 mb-1">Proxy Read Timeout (Seconds)</label>
              <input type="number" value="60" class="w-full p-2 bg-white border border-slate-300 rounded text-xs font-mono" />
            </div>
          </div>
        </div>

        <div class="p-4 rounded-xl border border-slate-200 space-y-3 bg-slate-50/50">
          <span class="font-bold text-slate-800">NAXSI WAF Operation Mode</span>
          <div class="space-y-2">
            <label class="flex items-center gap-2 p-2 bg-white rounded border border-slate-200 cursor-pointer">
              <input type="radio" name="naxsi_mode" checked class="text-[#0072ce]" />
              <span class="font-bold text-slate-800">Blocking Mode (Drop SQLi / XSS immediately)</span>
            </label>
            <label class="flex items-center gap-2 p-2 bg-white rounded border border-slate-200 cursor-pointer">
              <input type="radio" name="naxsi_mode" class="text-[#0072ce]" />
              <span class="font-bold text-slate-800">Learning Mode (Generate whitelist suggestions without blocking)</span>
            </label>
          </div>
        </div>
      </div>
    </div>

    <!-- ADD / EDIT VIRTUAL WEBSERVER MODAL (MATCHING SOPHOS UTM 9 FORM EXACTLY) -->
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
        <div class="w-full max-w-lg bg-white rounded-2xl border border-slate-200 shadow-2xl overflow-hidden flex flex-col my-6">
          <div class="bg-slate-900 text-white px-5 py-3.5 flex items-center justify-between border-b border-slate-800">
            <div class="flex items-center gap-2">
              <div class="w-7 h-7 rounded bg-[#ee7f00] flex items-center justify-center text-white font-bold text-xs">
                VS
              </div>
              <h3 class="text-xs font-bold uppercase tracking-wider text-white">
                {{ editingId ? 'Edit Virtual Webserver' : 'Add Virtual Webserver' }}
              </h3>
            </div>
            <button @click="isModalOpen = false" class="text-slate-400 hover:text-white cursor-pointer font-bold text-base">&times;</button>
          </div>

          <form @submit.prevent="saveVirtualServer" class="p-5 space-y-3.5 text-xs text-slate-800 max-h-[80vh] overflow-y-auto">
            <!-- Name -->
            <div>
              <label class="block font-bold text-slate-700 mb-1">Name *</label>
              <input
                v-model="formVS.name"
                type="text"
                required
                placeholder="e.g. ActiveSync Medric Networks LLC"
                class="w-full p-2 border border-slate-300 rounded focus:border-[#0072ce] focus:outline-none"
              />
            </div>

            <!-- Interface -->
            <div>
              <label class="block font-bold text-slate-700 mb-1">Interface</label>
              <select v-model="formVS.interface" class="w-full p-2 border border-slate-300 rounded bg-white font-medium">
                <option value="Uplink Interfaces (WAN)">:: Uplink Interfaces (WAN) ::</option>
                <option value="ens33 (WAN)">ens33 (WAN)</option>
                <option value="ens34 (LAN)">ens34 (LAN)</option>
                <option value="<< Any >>">&lt;&lt; Any &gt;&gt;</option>
              </select>
            </div>

            <!-- Type & Port -->
            <div class="grid grid-cols-2 gap-3">
              <div>
                <label class="block font-bold text-slate-700 mb-1">Type</label>
                <select v-model="formVS.type" class="w-full p-2 border border-slate-300 rounded bg-white font-medium">
                  <option value="Encrypted (HTTPS), Redirection enabled">Encrypted (HTTPS) &amp; redirect</option>
                  <option value="Encrypted (HTTPS)">Encrypted (HTTPS)</option>
                  <option value="Plaintext (HTTP)">Plaintext (HTTP)</option>
                </select>
              </div>
              <div>
                <label class="block font-bold text-slate-700 mb-1">Port</label>
                <input
                  v-model.number="formVS.port"
                  type="number"
                  placeholder="443"
                  class="w-full p-2 border border-slate-300 rounded font-mono focus:border-[#0072ce] focus:outline-none"
                />
              </div>
            </div>

            <!-- Domains Box with inline add -->
            <div>
              <div class="flex items-center justify-between mb-1">
                <label class="font-bold text-slate-700">Domains (FQDN)</label>
                <button
                  type="button"
                  @click="addDomainPrompt"
                  class="text-[11px] font-bold text-[#0072ce] hover:underline flex items-center gap-1 cursor-pointer"
                >
                  <span class="w-4 h-4 rounded bg-blue-50 border border-blue-200 flex items-center justify-center text-xs font-bold">+</span>
                  <span>Add Domain</span>
                </button>
              </div>
              <div class="p-2 border border-slate-300 rounded bg-slate-50 min-h-16 max-h-28 overflow-y-auto space-y-1">
                <div
                  v-for="(dom, dIdx) in formVS.domains"
                  :key="dIdx"
                  class="flex items-center justify-between bg-white px-2.5 py-1 rounded border border-slate-200 font-mono text-[11px]"
                >
                  <span class="font-bold text-slate-900">{{ dom }}</span>
                  <button type="button" @click="removeDomain(dIdx)" class="text-rose-600 hover:text-rose-800 font-bold">&times;</button>
                </div>
                <div v-if="formVS.domains.length === 0" class="text-slate-400 text-center py-2 text-[11px]">
                  No domains added yet. Click "+ Add Domain".
                </div>
              </div>
            </div>

            <!-- Real Webservers for path '/' with inline add button -->
            <div>
              <div class="flex items-center justify-between mb-1">
                <label class="font-bold text-slate-700">Real Webservers for path '/'</label>
                <button
                  type="button"
                  @click="openInlineRealServerModal"
                  class="text-[11px] font-bold text-emerald-700 hover:underline flex items-center gap-1 cursor-pointer"
                >
                  <span class="w-4 h-4 rounded bg-emerald-50 border border-emerald-200 flex items-center justify-center text-xs font-bold text-emerald-700">+</span>
                  <span>New Real Webserver</span>
                </button>
              </div>
              <div class="p-2 border border-slate-300 rounded bg-slate-50 max-h-32 overflow-y-auto space-y-1">
                <label
                  v-for="rs in realServers"
                  :key="rs.id"
                  class="flex items-center justify-between p-1.5 bg-white rounded border border-slate-200 cursor-pointer hover:bg-blue-50/50"
                >
                  <div class="flex items-center gap-2">
                    <input
                      type="checkbox"
                      :value="rs.name"
                      v-model="formVS.real_servers"
                      class="w-4 h-4 rounded text-[#0072ce]"
                    />
                    <span class="font-bold text-slate-800">{{ rs.name }}</span>
                  </div>
                  <span
                    class="text-[10px] font-mono font-bold"
                    :class="rs.enabled !== false ? 'text-emerald-700' : 'text-slate-400'"
                  >
                    {{ rs.enabled !== false ? 'enabled' : 'disabled' }}
                  </span>
                </label>
              </div>
            </div>

            <!-- Firewall profile -->
            <div>
              <label class="block font-bold text-slate-700 mb-1">Firewall Profile</label>
              <select v-model="formVS.profile" class="w-full p-2 border border-slate-300 rounded bg-white font-medium">
                <option value=":: No Profile ::">:: No Profile ::</option>
                <option value="*OWA & Exchange ActiveSync">*OWA &amp; Exchange ActiveSync</option>
                <option value="Exchange AutoDiscover">Exchange AutoDiscover</option>
                <option value="Strict WAF Profile">Strict WAF Profile</option>
                <option value="Standard WAF Profile">Standard WAF Profile</option>
              </select>
            </div>

            <!-- Theme / Customization -->
            <div>
              <label class="block font-bold text-slate-700 mb-1">Theme / Customization</label>
              <select v-model="formVS.theme" class="w-full p-2 border border-slate-300 rounded bg-white font-medium">
                <option value=":: No Customization ::">:: No Customization ::</option>
                <option value="Corporate Modern">Corporate Modern</option>
                <option value="Sophos UTM Classic">Sophos UTM Classic</option>
              </select>
            </div>

            <!-- Comment -->
            <div>
              <label class="block font-bold text-slate-700 mb-1">Comment</label>
              <input
                v-model="formVS.comment"
                type="text"
                placeholder="e.g. ActiveSync exchange mobile sync"
                class="w-full p-2 border border-slate-300 rounded focus:border-[#0072ce] focus:outline-none"
              />
            </div>

            <!-- Advanced (Collapsible) -->
            <div class="border border-slate-200 rounded-xl overflow-hidden">
              <button
                type="button"
                @click="showAdvanced = !showAdvanced"
                class="w-full px-3 py-2 bg-slate-100 flex items-center justify-between font-bold text-slate-700 cursor-pointer"
              >
                <span>Advanced</span>
                <span>{{ showAdvanced ? '▲' : '▼' }}</span>
              </button>
              <div v-if="showAdvanced" class="p-3 bg-white space-y-2">
                <label class="flex items-center gap-2 font-medium text-slate-700 cursor-pointer">
                  <input type="checkbox" v-model="formVS.disable_compression" class="rounded text-[#0072ce]" />
                  <span>Disable compression support</span>
                </label>
                <label class="flex items-center gap-2 font-medium text-slate-700 cursor-pointer">
                  <input type="checkbox" v-model="formVS.rewrite_html" class="rounded text-[#0072ce]" />
                  <span>Rewrite HTML</span>
                </label>
                <label class="flex items-center gap-2 font-medium text-slate-700 cursor-pointer">
                  <input type="checkbox" v-model="formVS.pass_host_header" class="rounded text-[#0072ce]" />
                  <span>Pass host header</span>
                </label>
              </div>
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
                Save
              </button>
            </div>
          </form>
        </div>
      </div>
    </transition>

    <!-- INLINE ADD REAL SERVER SUB-MODAL (Z-[100] SO IT OPENS CLEANLY ON TOP) -->
    <transition
      enter-active-class="transition duration-150 ease-out"
      enter-from-class="opacity-0 scale-95"
      enter-to-class="opacity-100 scale-100"
      leave-active-class="transition duration-100 ease-in"
      leave-from-class="opacity-100 scale-100"
      leave-to-class="opacity-0 scale-95"
    >
      <div
        v-if="isInlineRSModalOpen"
        class="fixed inset-0 z-[100] overflow-y-auto bg-slate-900/70 backdrop-blur-xs flex items-center justify-center p-4"
        @keydown.esc="isInlineRSModalOpen = false"
      >
        <div class="w-full max-w-md bg-white rounded-2xl border border-slate-200 shadow-2xl overflow-hidden flex flex-col my-6">
          <div class="bg-slate-900 text-white px-5 py-3 flex items-center justify-between border-b border-slate-800">
            <div class="flex items-center gap-2">
              <div class="w-6 h-6 rounded bg-emerald-600 flex items-center justify-center text-white font-bold text-xs">
                RS
              </div>
              <h3 class="text-xs font-bold uppercase tracking-wider text-white">Add Real Webserver</h3>
            </div>
            <button @click="isInlineRSModalOpen = false" class="text-slate-400 hover:text-white cursor-pointer font-bold text-base">&times;</button>
          </div>

          <form @submit.prevent="saveInlineRealServer" class="p-5 space-y-3 text-xs text-slate-800">
            <div>
              <label class="block font-bold text-slate-700 mb-1">Name *</label>
              <input
                v-model="newInlineRS.name"
                type="text"
                required
                placeholder="e.g. Medric Networks"
                class="w-full p-2 border border-slate-300 rounded focus:border-[#0072ce] focus:outline-none"
              />
            </div>

            <div class="grid grid-cols-2 gap-3">
              <div>
                <label class="block font-bold text-slate-700 mb-1">Host / IP *</label>
                <input
                  v-model="newInlineRS.host"
                  type="text"
                  required
                  placeholder="e.g. 192.168.1.50"
                  class="w-full p-2 border border-slate-300 rounded font-mono focus:border-[#0072ce] focus:outline-none"
                />
              </div>
              <div>
                <label class="block font-bold text-slate-700 mb-1">Port *</label>
                <input
                  v-model.number="newInlineRS.port"
                  type="number"
                  required
                  placeholder="443"
                  class="w-full p-2 border border-slate-300 rounded font-mono focus:border-[#0072ce] focus:outline-none"
                />
              </div>
            </div>

            <div>
              <label class="block font-bold text-slate-700 mb-1">Protocol</label>
              <select v-model="newInlineRS.protocol" class="w-full p-2 border border-slate-300 rounded bg-white font-bold">
                <option value="HTTPS">HTTPS (Encrypted Backend)</option>
                <option value="HTTP">HTTP (Plaintext Backend)</option>
              </select>
            </div>

            <div class="pt-3 border-t border-slate-200 flex justify-between">
              <button
                type="button"
                @click="isInlineRSModalOpen = false"
                class="px-3.5 py-1.5 border border-slate-300 rounded text-xs font-semibold text-slate-700 hover:bg-slate-50 cursor-pointer"
              >
                Cancel
              </button>
              <button
                type="submit"
                class="px-4 py-1.5 bg-emerald-600 hover:bg-emerald-700 text-white rounded text-xs font-bold shadow-xs cursor-pointer"
              >
                Add Real Webserver
              </button>
            </div>
          </form>
        </div>
      </div>
    </transition>

    <!-- LIVE LOG MODAL -->
    <div
      v-if="isLiveLogOpen"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-xs p-4"
    >
      <div class="bg-slate-900 text-white rounded-2xl shadow-2xl border border-slate-800 max-w-3xl w-full overflow-hidden">
        <div class="px-5 py-3.5 bg-slate-950 flex items-center justify-between border-b border-slate-800">
          <div class="flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            <h3 class="text-xs font-bold uppercase tracking-wider text-emerald-400">Live Web Application Firewall (WAF) Log</h3>
          </div>
          <button @click="isLiveLogOpen = false" class="text-slate-400 hover:text-white font-bold cursor-pointer">&times;</button>
        </div>
        <div class="p-4 bg-black font-mono text-xs text-slate-300 overflow-x-auto max-h-96 space-y-1">
          <div class="text-emerald-400">[WAF-PASS] 2026-08-20 16:30:12 192.168.1.50 GET outlook.medricnetworks.com/owa/ 200 OK (0.012s)</div>
          <div class="text-emerald-400">[WAF-PASS] 2026-08-20 16:30:18 192.168.1.52 POST eas.medricnetworks.com/Microsoft-Server-ActiveSync 200 OK (0.024s)</div>
          <div class="text-rose-400">[WAF-BLOCK] 2026-08-20 16:31:02 194.26.29.112 POST autodiscover.medricnetworks.com/autodiscover.xml NAXSI_SQLI_RULE_8 (403 Forbidden)</div>
        </div>
        <div class="p-3 bg-slate-950 border-t border-slate-800 flex justify-end">
          <button
            type="button"
            @click="isLiveLogOpen = false"
            class="px-4 py-1.5 bg-[#0072ce] text-white text-xs font-bold rounded cursor-pointer"
          >
            Close Log
          </button>
        </div>
      </div>
    </div>

    <!-- NGINX CONF PREVIEW MODAL -->
    <div
      v-if="isNginxPreviewOpen"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-xs p-4"
    >
      <div class="bg-white rounded-2xl shadow-2xl border border-slate-300 max-w-2xl w-full overflow-hidden">
        <div class="px-5 py-3.5 bg-slate-900 text-white flex items-center justify-between border-b-2 border-[#ee7f00]">
          <h3 class="text-xs font-bold uppercase tracking-wider">Generated nginx.conf Preview</h3>
          <button @click="isNginxPreviewOpen = false" class="text-slate-400 hover:text-white font-bold cursor-pointer">&times;</button>
        </div>
        <div class="p-4 bg-slate-950 text-slate-200 font-mono text-xs overflow-x-auto max-h-96">
          <pre>{{ nginxConfPreview }}</pre>
        </div>
        <div class="p-3 bg-slate-100 border-t border-slate-200 flex justify-end">
          <button
            type="button"
            @click="isNginxPreviewOpen = false"
            class="px-4 py-1.5 rounded bg-[#0072ce] text-white text-xs font-bold cursor-pointer"
          >
            Close
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

const activeTab = ref('virtual') // 'virtual' | 'real' | 'site_path' | 'redirection' | 'advanced'
const isModalOpen = ref(false)
const isInlineRSModalOpen = ref(false)
const isLiveLogOpen = ref(false)
const isNginxPreviewOpen = ref(false)
const nginxConfPreview = ref('')
const searchQuery = ref('')
const sortBy = ref('name_asc')
const showAdvanced = ref(true)
const editingId = ref(null)

const tabs = computed(() => [
  { id: 'virtual', label: 'Virtual Webservers', badge: virtualServers.value.length },
  { id: 'real', label: 'Real Webservers', badge: realServers.value.length },
  { id: 'site_path', label: 'Site Path Routing', badge: null },
  { id: 'redirection', label: 'Request Redirection', badge: null },
  { id: 'advanced', label: 'Advanced', badge: null }
])

const activeTabLabel = computed(() => {
  if (activeTab.value === 'virtual') return 'Virtual Webserver'
  if (activeTab.value === 'real') return 'Real Webserver'
  if (activeTab.value === 'site_path') return 'Site Path Route'
  if (activeTab.value === 'redirection') return 'Request Redirection'
  return 'WAF Setting'
})

// Sophos UTM 9 matching Virtual Webservers
const virtualServers = ref([
  {
    id: 'vs-1',
    name: 'ActiveSync Medric Networks LLC',
    interface: 'Uplink Interfaces (WAN)',
    type: 'Encrypted (HTTPS), Redirection enabled',
    port: 443,
    ssl: true,
    domains: ['outlook.medricnetworks.com', 'eas.medricnetworks.com'],
    real_servers: ['Medric Networks'],
    upstream: '192.168.1.50:443',
    profile: '*OWA & Exchange ActiveSync',
    theme: ':: No Customization ::',
    comment: 'Primary Exchange ActiveSync synchronization tunnel',
    pass_host_header: true,
    enabled: true
  },
  {
    id: 'vs-2',
    name: 'AutoDisco Medric Networks LLC',
    interface: 'Uplink Interfaces (WAN)',
    type: 'Encrypted (HTTPS), Redirection enabled',
    port: 443,
    ssl: true,
    domains: ['autodiscover.medricnetworks.com'],
    real_servers: ['Medric Networks'],
    upstream: '192.168.1.50:443',
    profile: 'Exchange AutoDiscover',
    theme: ':: No Customization ::',
    comment: 'Exchange AutoDiscover discovery service',
    pass_host_header: true,
    enabled: true
  },
  {
    id: 'vs-3',
    name: 'CastleTruBlue Webmail',
    interface: 'Uplink Interfaces (WAN)',
    type: 'Encrypted (HTTPS), Redirection enabled',
    port: 443,
    ssl: true,
    domains: ['mail.castletrublue.com'],
    real_servers: ['Mail CastleTruBlue Com'],
    upstream: '192.168.1.55:443',
    profile: '*OWA & Exchange ActiveSync',
    theme: ':: No Customization ::',
    comment: 'CastleTruBlue corporate webmail portal',
    pass_host_header: true,
    enabled: true
  },
  {
    id: 'vs-4',
    name: 'Medric 3CX VoIP Webclient',
    interface: 'Uplink Interfaces (WAN)',
    type: 'Encrypted (HTTPS)',
    port: 5001,
    ssl: true,
    domains: ['pbx.medricnetworks.com'],
    real_servers: ['3CX'],
    upstream: '192.168.1.80:5001',
    profile: 'Strict WAF Profile',
    theme: ':: No Customization ::',
    comment: '3CX PBX WebClient endpoint',
    pass_host_header: true,
    enabled: false
  }
])

// Real Webservers Catalog (matching screenshot)
const realServers = ref([
  { id: 'rs-1', name: '3CX', host: '192.168.1.80', port: 5001, protocol: 'HTTPS', keepalive: true, enabled: false, comment: '3CX VoIP PBX Server' },
  { id: 'rs-2', name: 'Mail CastleTruBlue Com', host: '192.168.1.55', port: 443, protocol: 'HTTPS', keepalive: true, enabled: true, comment: 'CastleTruBlue Exchange Backend' },
  { id: 'rs-3', name: 'Mail Medric Net', host: '192.168.1.50', port: 443, protocol: 'HTTPS', keepalive: true, enabled: true, comment: 'Medric Net primary Exchange Node' },
  { id: 'rs-4', name: 'Medric Networks', host: '192.168.1.50', port: 443, protocol: 'HTTPS', keepalive: true, enabled: true, comment: 'ActiveSync Exchange cluster' },
  { id: 'rs-5', name: 'Summer', host: '192.168.1.90', port: 8080, protocol: 'HTTP', keepalive: true, enabled: true, comment: 'Summer Portal web app' }
])

const formVS = ref({
  id: null,
  name: '',
  interface: 'Uplink Interfaces (WAN)',
  type: 'Encrypted (HTTPS), Redirection enabled',
  port: 443,
  ssl: true,
  domains: [],
  real_servers: ['Medric Networks'],
  upstream: '192.168.1.50:443',
  profile: '*OWA & Exchange ActiveSync',
  theme: ':: No Customization ::',
  comment: '',
  disable_compression: false,
  rewrite_html: false,
  pass_host_header: true,
  enabled: true
})

const newInlineRS = ref({
  name: '',
  host: '',
  port: 443,
  protocol: 'HTTPS'
})

const filteredVirtualServers = computed(() => {
  let list = [...virtualServers.value]
  if (searchQuery.value.trim()) {
    const q = searchQuery.value.toLowerCase()
    list = list.filter(v =>
      v.name.toLowerCase().includes(q) ||
      (v.domains && v.domains.some(d => d.toLowerCase().includes(q))) ||
      (v.real_servers && v.real_servers.some(r => r.toLowerCase().includes(q)))
    )
  }
  if (sortBy.value === 'name_asc') list.sort((a, b) => a.name.localeCompare(b.name))
  else if (sortBy.value === 'name_desc') list.sort((a, b) => b.name.localeCompare(a.name))
  else if (sortBy.value === 'status') list.sort((a, b) => (b.enabled ? 1 : 0) - (a.enabled ? 1 : 0))
  else if (sortBy.value === 'port') list.sort((a, b) => a.port - b.port)
  return list
})

function getDomainsList(vs) {
  if (Array.isArray(vs.domains)) return vs.domains
  if (vs.domain) return [vs.domain]
  return ['app.local']
}

function openCreateModal() {
  editingId.value = null
  formVS.value = {
    id: null,
    name: '',
    interface: 'Uplink Interfaces (WAN)',
    type: 'Encrypted (HTTPS), Redirection enabled',
    port: 443,
    ssl: true,
    domains: [],
    real_servers: ['Medric Networks'],
    upstream: '192.168.1.50:443',
    profile: '*OWA & Exchange ActiveSync',
    theme: ':: No Customization ::',
    comment: '',
    disable_compression: false,
    rewrite_html: false,
    pass_host_header: true,
    enabled: true
  }
  isModalOpen.value = true
}

function editVirtualServer(vs) {
  editingId.value = vs.id
  formVS.value = {
    ...vs,
    domains: Array.isArray(vs.domains) ? [...vs.domains] : (vs.domain ? [vs.domain] : []),
    real_servers: Array.isArray(vs.real_servers) ? [...vs.real_servers] : []
  }
  isModalOpen.value = true
}

function cloneVirtualServer(vs) {
  const clone = {
    ...vs,
    id: `vs-${Date.now()}`,
    name: `${vs.name} (Clone)`,
    domains: Array.isArray(vs.domains) ? [...vs.domains] : [vs.domain]
  }
  virtualServers.value.push(clone)
}

function addDomainPrompt() {
  const domain = prompt('Enter Fully Qualified Domain Name (FQDN):', 'app.medricnetworks.com')
  if (domain && domain.trim()) {
    formVS.value.domains.push(domain.trim())
  }
}

function removeDomain(idx) {
  formVS.value.domains.splice(idx, 1)
}

function openInlineRealServerModal() {
  newInlineRS.value = {
    name: '',
    host: '',
    port: 443,
    protocol: 'HTTPS'
  }
  isInlineRSModalOpen.value = true
}

function saveInlineRealServer() {
  if (!newInlineRS.value.name || !newInlineRS.value.host) return
  const newObj = {
    id: `rs-${Date.now()}`,
    name: newInlineRS.value.name,
    host: newInlineRS.value.host,
    port: newInlineRS.value.port,
    protocol: newInlineRS.value.protocol,
    keepalive: true,
    enabled: true,
    comment: 'Created inline from Virtual Webserver editor'
  }
  realServers.value.push(newObj)
  if (!formVS.value.real_servers.includes(newObj.name)) {
    formVS.value.real_servers.push(newObj.name)
  }
  isInlineRSModalOpen.value = false
}

async function saveVirtualServer() {
  if (!formVS.value.name) return
  const payload = {
    ...formVS.value,
    id: editingId.value || `vs-${Date.now()}`,
    domain: formVS.value.domains[0] || 'app.local',
    ssl: formVS.value.type.includes('HTTPS')
  }

  if (editingId.value) {
    const idx = virtualServers.value.findIndex(v => v.id === editingId.value)
    if (idx >= 0) virtualServers.value[idx] = payload
  } else {
    virtualServers.value.push(payload)
  }

  // Persist to backend API
  try {
    await fetch('/api/waf/rules/save', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        rule_name: payload.name,
        hosted_domain: payload.domains[0] || 'app.local',
        real_server_ip: '192.168.1.50',
        real_server_port: payload.port || 443,
        enable_ssl: payload.ssl,
        enable_naxsi_waf: true
      })
    })
  } catch (err) {
    console.error('Failed to persist WAF rule to backend:', err)
  }

  isModalOpen.value = false
}

const toggleVirtualServer = (vs) => {
  vs.enabled = !vs.enabled
}

const deleteVirtualServer = async (id) => {
  const item = virtualServers.value.find(v => v.id === id)
  if (!confirm(`Are you sure you want to delete virtual webserver '${item ? item.name : id}'?`)) return
  virtualServers.value = virtualServers.value.filter(v => v.id !== id)
  try {
    if (item) {
      await fetch(`/api/waf/rules/${item.name}`, { method: 'DELETE' })
    }
  } catch (e) {
    console.error(e)
  }
}

const deleteRealServer = (id) => {
  if (!confirm('Are you sure you want to delete this real webserver?')) return
  realServers.value = realServers.value.filter(r => r.id !== id)
}

const openNginxPreview = () => {
  let conf = `# =========================================================================\n# NGINX REVERSE PROXY & NAXSI WAF AUTOGENERATED CONFIGURATION\n# Astaro-Next Appliance (Sophos UTM 9 Parity)\n# =========================================================================\n\n`
  virtualServers.value.filter(v => v.enabled).forEach(v => {
    const doms = getDomainsList(v).join(' ')
    conf += `server {\n`
    conf += `    listen ${v.port}${v.ssl ? ' ssl http2' : ''};\n`
    conf += `    server_name ${doms};\n`
    if (v.ssl) {
      conf += `    ssl_certificate /etc/astaro/ssl/wildcard.crt;\n`
      conf += `    ssl_certificate_key /etc/astaro/ssl/wildcard.key;\n`
      conf += `    ssl_protocols TLSv1.2 TLSv1.3;\n`
    }
    conf += `    location / {\n`
    conf += `        proxy_pass https://${v.upstream};\n`
    conf += `        proxy_set_header Host $host;\n`
    conf += `        proxy_set_header X-Real-IP $remote_addr;\n`
    conf += `        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;\n`
    conf += `        proxy_set_header X-Forwarded-Proto $scheme;\n`
    conf += `        # NAXSI WAF L7 Profile: ${v.profile}\n`
    conf += `        SecRulesEnabled;\n`
    conf += `        DeniedUrl "/waf-denied";\n`
    conf += `        CheckRule "$SQL >= 8" BLOCK;\n`
    conf += `        CheckRule "$XSS >= 8" BLOCK;\n`
    conf += `    }\n`
    conf += `}\n\n`
  })
  nginxConfPreview.value = conf
  isNginxPreviewOpen.value = true
}

onMounted(() => {})
</script>
