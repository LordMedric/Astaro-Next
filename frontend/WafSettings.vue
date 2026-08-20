<template>
  <div class="space-y-6">
    <!-- Header Section -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-slate-200 pb-4">
      <div>
        <div class="flex items-center gap-2">
          <span class="w-1.5 h-5 bg-[#ee7f00] rounded-full"></span>
          <h1 class="text-xl font-bold text-slate-900">Webserver Protection (WAF)</h1>
        </div>
        <p class="text-xs text-slate-500 mt-1">
          Publish web applications with SSL offloading, Reverse Proxy load balancing, and Layer 7 Web Application Firewall threat protection.
        </p>
      </div>

      <!-- Action Buttons -->
      <div class="flex items-center gap-2">
        <button
          type="button"
          @click="openNginxPreview"
          class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded bg-white hover:bg-slate-50 text-slate-700 border border-slate-300 text-xs font-bold shadow-xs cursor-pointer"
          title="Inspect generated Nginx & NAXSI configuration"
        >
          <svg class="w-3.5 h-3.5 text-[#005299]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
          </svg>
          <span>nginx.conf</span>
        </button>

        <button
          type="button"
          @click="openCreateModal"
          class="inline-flex items-center gap-2 px-3.5 py-1.5 rounded bg-[#005299] hover:bg-[#003d73] text-white text-xs font-bold shadow-xs transition-colors cursor-pointer"
        >
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          <span>New {{ activeTab === 'virtual' ? 'Virtual Webserver' : (activeTab === 'real' ? 'Real Webserver' : 'Protection Profile') }}</span>
        </button>
      </div>
    </div>

    <!-- Tab Navigation Strip (Sophos UTM Style) -->
    <div class="flex border-b border-slate-200 gap-1 bg-[#f4f6f9] p-1.5 rounded-t-lg">
      <button
        type="button"
        @click="activeTab = 'virtual'"
        :class="[
          'px-4 py-2 text-xs font-bold rounded-md transition-all flex items-center gap-2 cursor-pointer',
          activeTab === 'virtual'
            ? 'bg-white text-slate-900 shadow-xs border-b-2 border-[#ee7f00]'
            : 'text-slate-600 hover:text-slate-900 hover:bg-white/60'
        ]"
      >
        <svg class="w-4 h-4 text-[#005299]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9" />
        </svg>
        <span>Virtual Webservers ({{ virtualServers.length }})</span>
      </button>

      <button
        type="button"
        @click="activeTab = 'real'"
        :class="[
          'px-4 py-2 text-xs font-bold rounded-md transition-all flex items-center gap-2 cursor-pointer',
          activeTab === 'real'
            ? 'bg-white text-slate-900 shadow-xs border-b-2 border-[#ee7f00]'
            : 'text-slate-600 hover:text-slate-900 hover:bg-white/60'
        ]"
      >
        <svg class="w-4 h-4 text-[#005299]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 12h14M5 12a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v4a2 2 0 01-2 2M5 12a2 2 0 00-2 2v4a2 2 0 002 2h14a2 2 0 002-2v-4a2 2 0 00-2-2m-2-4h.01M17 16h.01" />
        </svg>
        <span>Real Webservers ({{ realServers.length }})</span>
      </button>

      <button
        type="button"
        @click="activeTab = 'profiles'"
        :class="[
          'px-4 py-2 text-xs font-bold rounded-md transition-all flex items-center gap-2 cursor-pointer',
          activeTab === 'profiles'
            ? 'bg-white text-slate-900 shadow-xs border-b-2 border-[#ee7f00]'
            : 'text-slate-600 hover:text-slate-900 hover:bg-white/60'
        ]"
      >
        <svg class="w-4 h-4 text-[#005299]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
        </svg>
        <span>Protection Profiles ({{ protectionProfiles.length }})</span>
      </button>
    </div>

    <!-- Status Banner: Nginx WAF Engine -->
    <div class="p-3 bg-emerald-50 border border-emerald-200 rounded-lg text-emerald-800 text-xs flex items-center justify-between">
      <div class="flex items-center gap-2">
        <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
        <span class="font-bold">Nginx Reverse Proxy & NAXSI WAF Engine:</span>
        <span>Active &amp; enforcing Layer 7 inspection on HTTP/HTTPS virtual hosts.</span>
      </div>
      <span class="text-[11px] font-mono font-bold bg-emerald-100 px-2 py-0.5 rounded text-emerald-900">
        Engine: Nginx 1.22 + NAXSI L7
      </span>
    </div>

    <!-- TAB 1: VIRTUAL WEBSERVERS (FRONTENDS) -->
    <div v-if="activeTab === 'virtual'" class="bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden">
      <table class="w-full text-left text-xs border-collapse">
        <thead class="bg-[#f4f6f9] text-slate-700 font-bold border-b border-slate-200">
          <tr>
            <th class="p-3 pl-4 w-12 text-center">Status</th>
            <th class="p-3">Virtual Host Name</th>
            <th class="p-3">Domains (FQDN)</th>
            <th class="p-3">Interface / Port</th>
            <th class="p-3">SSL/TLS Certificate</th>
            <th class="p-3">Real Webservers</th>
            <th class="p-3">Protection Profile</th>
            <th class="p-3 text-right pr-4">Actions</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-100">
          <tr
            v-for="(vs, idx) in virtualServers"
            :key="vs.id"
            :class="idx % 2 === 0 ? 'bg-white' : 'bg-[#f7f7f7]'"
            class="hover:bg-blue-50/50 transition-colors"
          >
            <td class="p-3 pl-4 text-center">
              <button
                type="button"
                @click="toggleVirtualServer(vs)"
                class="relative inline-flex h-4 w-8 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out"
                :class="vs.enabled ? 'bg-[#005299]' : 'bg-slate-300'"
              >
                <span
                  class="inline-block h-3 w-3 transform rounded-full bg-white shadow-sm transition duration-200"
                  :class="vs.enabled ? 'translate-x-4' : 'translate-x-0'"
                ></span>
              </button>
            </td>

            <td class="p-3 font-bold text-slate-900">
              {{ vs.name }}
            </td>

            <td class="p-3 font-mono font-bold text-[#005299]">
              {{ vs.domain }}
            </td>

            <td class="p-3 font-mono text-slate-700 font-semibold">
              {{ vs.interface || 'Uplink (WAN)' }}:<span class="font-bold text-slate-900">{{ vs.port || 443 }}</span>
            </td>

            <td class="p-3">
              <span v-if="vs.ssl" class="inline-flex items-center gap-1 px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-50 text-emerald-700 border border-emerald-200">
                <span>🔒</span> {{ vs.cert_name || 'Let\'s Encrypt / Custom SSL' }}
              </span>
              <span v-else class="text-slate-400 font-mono text-[11px]">Plain HTTP</span>
            </td>

            <td class="p-3 font-mono text-slate-800">
              <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-blue-50 text-[#005299] border border-blue-200">
                &rarr; {{ vs.upstream }}
              </span>
            </td>

            <td class="p-3">
              <span class="px-2 py-0.5 rounded text-[10px] font-bold uppercase bg-amber-50 text-amber-800 border border-amber-200">
                {{ vs.profile || 'Standard WAF Profile' }}
              </span>
            </td>

            <td class="p-3 text-right pr-4 space-x-2">
              <button
                type="button"
                @click="deleteVirtualServer(vs.id)"
                class="text-rose-600 hover:text-rose-800 text-[11px] font-bold cursor-pointer"
              >
                Delete
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- TAB 2: REAL WEBSERVERS (BACKENDS) -->
    <div v-if="activeTab === 'real'" class="bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden">
      <table class="w-full text-left text-xs border-collapse">
        <thead class="bg-[#f4f6f9] text-slate-700 font-bold border-b border-slate-200">
          <tr>
            <th class="p-3 pl-4">Backend Name</th>
            <th class="p-3 font-mono">Host / IP Address</th>
            <th class="p-3">Protocol</th>
            <th class="p-3 font-mono">Port</th>
            <th class="p-3">Keepalive</th>
            <th class="p-3">Comment</th>
            <th class="p-3 text-right pr-4">Actions</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-100">
          <tr
            v-for="(rs, idx) in realServers"
            :key="rs.id"
            :class="idx % 2 === 0 ? 'bg-white' : 'bg-[#f7f7f7]'"
            class="hover:bg-blue-50/50 transition-colors"
          >
            <td class="p-3 pl-4 font-bold text-slate-900 flex items-center gap-2">
              <span class="w-2 h-2 rounded-full bg-emerald-500"></span>
              {{ rs.name }}
            </td>
            <td class="p-3 font-mono font-bold text-slate-800">{{ rs.host }}</td>
            <td class="p-3">
              <span class="px-2 py-0.5 rounded text-[10px] font-bold uppercase bg-blue-50 text-[#005299] border border-blue-200">
                {{ rs.protocol }}
              </span>
            </td>
            <td class="p-3 font-mono font-bold text-slate-900">{{ rs.port }}</td>
            <td class="p-3 text-slate-600">{{ rs.keepalive ? 'Enabled' : 'Disabled' }}</td>
            <td class="p-3 text-slate-500 text-[11px] truncate max-w-xs">{{ rs.comment || '—' }}</td>
            <td class="p-3 text-right pr-4">
              <button
                type="button"
                @click="deleteRealServer(rs.id)"
                class="text-rose-600 hover:text-rose-800 text-[11px] font-bold cursor-pointer"
              >
                Delete
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- TAB 3: PROTECTION PROFILES -->
    <div v-if="activeTab === 'profiles'" class="bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden">
      <table class="w-full text-left text-xs border-collapse">
        <thead class="bg-[#f4f6f9] text-slate-700 font-bold border-b border-slate-200">
          <tr>
            <th class="p-3 pl-4">Profile Name</th>
            <th class="p-3 text-center">SQLi Defense</th>
            <th class="p-3 text-center">XSS Defense</th>
            <th class="p-3 text-center">Form Hardening</th>
            <th class="p-3 text-center">Cookie Signing</th>
            <th class="p-3 text-center">SlowHTTP / Rate Limit</th>
            <th class="p-3 text-center">Antivirus Scan</th>
            <th class="p-3 text-right pr-4">Actions</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-100">
          <tr
            v-for="(prof, idx) in protectionProfiles"
            :key="prof.id"
            :class="idx % 2 === 0 ? 'bg-white' : 'bg-[#f7f7f7]'"
            class="hover:bg-blue-50/50 transition-colors"
          >
            <td class="p-3 pl-4 font-bold text-slate-900 flex items-center gap-2">
              <span class="w-2 h-2 rounded-full bg-[#ee7f00]"></span>
              {{ prof.name }}
            </td>
            <td class="p-3 text-center"><span class="text-emerald-600 font-bold">✓ Active</span></td>
            <td class="p-3 text-center"><span class="text-emerald-600 font-bold">✓ Active</span></td>
            <td class="p-3 text-center">
              <span v-if="prof.form_hardening" class="text-blue-600 font-bold">✓ Enabled</span>
              <span v-else class="text-slate-400">—</span>
            </td>
            <td class="p-3 text-center">
              <span v-if="prof.cookie_signing" class="text-purple-600 font-bold">✓ Signed</span>
              <span v-else class="text-slate-400">—</span>
            </td>
            <td class="p-3 text-center">
              <span v-if="prof.rate_limit" class="px-2 py-0.5 rounded text-[10px] font-bold bg-amber-50 text-amber-800 border border-amber-200">
                {{ prof.rate_limit }} req/s
              </span>
              <span v-else class="text-slate-400">—</span>
            </td>
            <td class="p-3 text-center">
              <span v-if="prof.av_scan" class="text-emerald-600 font-bold">✓ ClamAV</span>
              <span v-else class="text-slate-400">—</span>
            </td>
            <td class="p-3 text-right pr-4">
              <button
                type="button"
                @click="deleteProfile(prof.id)"
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
        <div class="px-5 py-3.5 bg-[#1b232e] text-white flex items-center justify-between border-b-2 border-[#ee7f00]">
          <h3 class="text-sm font-bold uppercase tracking-wider">
            Create {{ activeTab === 'virtual' ? 'Virtual Webserver' : (activeTab === 'real' ? 'Real Webserver' : 'Protection Profile') }}
          </h3>
          <button @click="isModalOpen = false" class="text-slate-400 hover:text-white font-bold cursor-pointer">✕</button>
        </div>

        <!-- Virtual Server Form -->
        <div v-if="activeTab === 'virtual'" class="p-5 space-y-4 text-xs">
          <div>
            <label class="block font-bold text-slate-700 mb-1">Virtual Server Name</label>
            <input
              v-model="newVS.name"
              type="text"
              placeholder="e.g. Nextcloud Cloud Portal, Corporate OWA"
              class="w-full p-2 border border-slate-300 rounded focus:border-[#005299] focus:outline-none"
            />
          </div>

          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block font-bold text-slate-700 mb-1">Domain / FQDN</label>
              <input
                v-model="newVS.domain"
                type="text"
                placeholder="e.g. cloud.company.com"
                class="w-full p-2 border border-slate-300 rounded font-mono focus:border-[#005299] focus:outline-none"
              />
            </div>
            <div>
              <label class="block font-bold text-slate-700 mb-1">Listening Port</label>
              <input
                v-model="newVS.port"
                type="number"
                placeholder="443"
                class="w-full p-2 border border-slate-300 rounded font-mono focus:border-[#005299] focus:outline-none"
              />
            </div>
          </div>

          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block font-bold text-slate-700 mb-1">Target Real Webserver</label>
              <select
                v-model="newVS.upstream"
                class="w-full p-2 border border-slate-300 rounded bg-white font-mono"
              >
                <option v-for="rs in realServers" :key="rs.id" :value="rs.host + ':' + rs.port">
                  {{ rs.name }} ({{ rs.host }}:{{ rs.port }})
                </option>
                <option value="192.168.1.100:8080">192.168.1.100:8080 (Custom)</option>
              </select>
            </div>
            <div>
              <label class="block font-bold text-slate-700 mb-1">Protection Profile</label>
              <select
                v-model="newVS.profile"
                class="w-full p-2 border border-slate-300 rounded bg-white"
              >
                <option v-for="p in protectionProfiles" :key="p.id" :value="p.name">
                  {{ p.name }}
                </option>
              </select>
            </div>
          </div>

          <div class="pt-2 border-t border-slate-100 space-y-2">
            <div class="flex items-center gap-2">
              <input id="vs-ssl" v-model="newVS.ssl" type="checkbox" class="rounded text-[#005299]" />
              <label for="vs-ssl" class="text-slate-700 font-semibold cursor-pointer">Enable SSL/TLS Encryption &amp; HTTPS Offloading</label>
            </div>
            <div class="flex items-center gap-2">
              <input id="vs-ws" v-model="newVS.websocket" type="checkbox" class="rounded text-[#005299]" />
              <label for="vs-ws" class="text-slate-700 font-semibold cursor-pointer">WebSocket Passthrough Support</label>
            </div>
          </div>
        </div>

        <!-- Real Server Form -->
        <div v-else-if="activeTab === 'real'" class="p-5 space-y-4 text-xs">
          <div>
            <label class="block font-bold text-slate-700 mb-1">Real Server Name</label>
            <input
              v-model="newRS.name"
              type="text"
              placeholder="e.g. Backend Web Node 01"
              class="w-full p-2 border border-slate-300 rounded focus:border-[#005299] focus:outline-none"
            />
          </div>

          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block font-bold text-slate-700 mb-1">Host / IP Address</label>
              <input
                v-model="newRS.host"
                type="text"
                placeholder="e.g. 192.168.1.50"
                class="w-full p-2 border border-slate-300 rounded font-mono focus:border-[#005299] focus:outline-none"
              />
            </div>
            <div>
              <label class="block font-bold text-slate-700 mb-1">Port</label>
              <input
                v-model="newRS.port"
                type="number"
                placeholder="8080"
                class="w-full p-2 border border-slate-300 rounded font-mono focus:border-[#005299] focus:outline-none"
              />
            </div>
          </div>

          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block font-bold text-slate-700 mb-1">Protocol</label>
              <select v-model="newRS.protocol" class="w-full p-2 border border-slate-300 rounded bg-white font-bold">
                <option value="HTTP">HTTP (Plain)</option>
                <option value="HTTPS">HTTPS (Encrypted Backend)</option>
              </select>
            </div>
            <div>
              <label class="block font-bold text-slate-700 mb-1">Keepalive</label>
              <select v-model="newRS.keepalive" class="w-full p-2 border border-slate-300 rounded bg-white">
                <option :value="true">Enabled</option>
                <option :value="false">Disabled</option>
              </select>
            </div>
          </div>
        </div>

        <!-- Protection Profile Form -->
        <div v-else class="p-5 space-y-4 text-xs">
          <div>
            <label class="block font-bold text-slate-700 mb-1">Profile Name</label>
            <input
              v-model="newProfile.name"
              type="text"
              placeholder="e.g. Strict Enterprise WAF Profile"
              class="w-full p-2 border border-slate-300 rounded focus:border-[#005299] focus:outline-none"
            />
          </div>

          <div class="space-y-2 pt-2 border-t border-slate-100">
            <div class="flex items-center gap-2">
              <input id="prof-sqli" v-model="newProfile.sqli" type="checkbox" class="rounded text-[#005299]" />
              <label for="prof-sqli" class="text-slate-700 font-semibold cursor-pointer">SQL Injection (SQLi) Defense</label>
            </div>
            <div class="flex items-center gap-2">
              <input id="prof-xss" v-model="newProfile.xss" type="checkbox" class="rounded text-[#005299]" />
              <label for="prof-xss" class="text-slate-700 font-semibold cursor-pointer">Cross-Site Scripting (XSS) Filter</label>
            </div>
            <div class="flex items-center gap-2">
              <input id="prof-form" v-model="newProfile.form_hardening" type="checkbox" class="rounded text-[#005299]" />
              <label for="prof-form" class="text-slate-700 font-semibold cursor-pointer">Form Hardening (Tamper Protection)</label>
            </div>
            <div class="flex items-center gap-2">
              <input id="prof-cookie" v-model="newProfile.cookie_signing" type="checkbox" class="rounded text-[#005299]" />
              <label for="prof-cookie" class="text-slate-700 font-semibold cursor-pointer">Cookie Signing (Anti-Session Hijacking)</label>
            </div>
            <div class="flex items-center gap-2">
              <input id="prof-av" v-model="newProfile.av_scan" type="checkbox" class="rounded text-[#005299]" />
              <label for="prof-av" class="text-slate-700 font-semibold cursor-pointer">HTTP File Upload Antivirus Scanning (ClamAV)</label>
            </div>
          </div>
        </div>

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
            @click="saveItem"
            class="px-4 py-1.5 rounded bg-[#005299] hover:bg-[#003d73] text-white text-xs font-bold shadow-xs cursor-pointer"
          >
            Save
          </button>
        </div>
      </div>
    </div>

    <!-- NGINX CONF PREVIEW MODAL -->
    <div
      v-if="isNginxPreviewOpen"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-xs p-4"
    >
      <div class="bg-white rounded-xl shadow-2xl border border-slate-300 max-w-2xl w-full overflow-hidden">
        <div class="px-5 py-3.5 bg-[#1b232e] text-white flex items-center justify-between border-b-2 border-[#ee7f00]">
          <h3 class="text-sm font-bold uppercase tracking-wider">Generated nginx.conf Preview</h3>
          <button @click="isNginxPreviewOpen = false" class="text-slate-400 hover:text-white font-bold cursor-pointer">✕</button>
        </div>
        <div class="p-4 bg-slate-950 text-slate-200 font-mono text-xs overflow-x-auto max-h-96">
          <pre>{{ nginxConfPreview }}</pre>
        </div>
        <div class="p-3 bg-[#f4f6f9] border-t border-slate-200 flex justify-end">
          <button
            type="button"
            @click="isNginxPreviewOpen = false"
            class="px-4 py-1.5 rounded bg-[#005299] text-white text-xs font-bold cursor-pointer"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const props = defineProps({
  authToken: {
    type: String,
    default: ''
  }
})

const activeTab = ref('virtual') // 'virtual' | 'real' | 'profiles'
const isModalOpen = ref(false)
const isNginxPreviewOpen = ref(false)
const nginxConfPreview = ref('')

const virtualServers = ref([
  { id: 1, name: 'Cloud File Portal', domain: 'cloud.company.com', port: 443, ssl: true, cert_name: 'Let\'s Encrypt (cloud.company.com)', upstream: '192.168.1.100:8080', profile: 'Strict WAF Profile', enabled: true },
  { id: 2, name: 'Corporate Webmail (OWA)', domain: 'mail.company.com', port: 443, ssl: true, cert_name: 'Wildcard SSL (*.company.com)', upstream: '192.168.1.50:443', profile: 'Exchange Protection Profile', enabled: true },
  { id: 3, name: 'Documentation Hub', domain: 'docs.internal', port: 80, ssl: false, cert_name: '', upstream: '192.168.2.20:80', profile: 'Standard WAF Profile', enabled: false }
])

const realServers = ref([
  { id: 1, name: 'Nextcloud Backend 01', host: '192.168.1.100', port: 8080, protocol: 'HTTP', keepalive: true, comment: 'Primary Nextcloud app container' },
  { id: 2, name: 'Exchange Mail Server', host: '192.168.1.50', port: 443, protocol: 'HTTPS', keepalive: true, comment: 'On-premise Microsoft Exchange node' },
  { id: 3, name: 'Docs Wiki Cluster', host: '192.168.2.20', port: 80, protocol: 'HTTP', keepalive: false, comment: 'Internal MkDocs documentation webserver' }
])

const protectionProfiles = ref([
  { id: 1, name: 'Strict WAF Profile', sqli: true, xss: true, form_hardening: true, cookie_signing: true, rate_limit: 50, av_scan: true },
  { id: 2, name: 'Exchange Protection Profile', sqli: true, xss: true, form_hardening: false, cookie_signing: true, rate_limit: 100, av_scan: true },
  { id: 3, name: 'Standard WAF Profile', sqli: true, xss: true, form_hardening: false, cookie_signing: false, rate_limit: 200, av_scan: false }
])

const newVS = ref({
  name: '',
  domain: '',
  port: 443,
  ssl: true,
  upstream: '192.168.1.100:8080',
  profile: 'Strict WAF Profile',
  websocket: true
})

const newRS = ref({
  name: '',
  host: '',
  port: 8080,
  protocol: 'HTTP',
  keepalive: true
})

const newProfile = ref({
  name: '',
  sqli: true,
  xss: true,
  form_hardening: true,
  cookie_signing: true,
  av_scan: true
})

const openCreateModal = () => {
  isModalOpen.value = true
}

const toggleVirtualServer = (vs) => {
  vs.enabled = !vs.enabled
}

const deleteVirtualServer = (id) => {
  virtualServers.value = virtualServers.value.filter(v => v.id !== id)
}

const deleteRealServer = (id) => {
  realServers.value = realServers.value.filter(r => r.id !== id)
}

const deleteProfile = (id) => {
  protectionProfiles.value = protectionProfiles.value.filter(p => p.id !== id)
}

const saveItem = () => {
  if (activeTab.value === 'virtual') {
    if (!newVS.value.name || !newVS.value.domain) return
    virtualServers.value.push({
      id: virtualServers.value.length + 1,
      ...newVS.value,
      enabled: true
    })
  } else if (activeTab.value === 'real') {
    if (!newRS.value.name || !newRS.value.host) return
    realServers.value.push({
      id: realServers.value.length + 1,
      ...newRS.value
    })
  } else {
    if (!newProfile.value.name) return
    protectionProfiles.value.push({
      id: protectionProfiles.value.length + 1,
      ...newProfile.value,
      rate_limit: 100
    })
  }
  isModalOpen.value = false
}

const openNginxPreview = () => {
  let conf = `# =========================================================================\n# NGINX REVERSE PROXY & NAXSI WAF AUTOGENERATED CONFIGURATION\n# Astaro-Next Appliance\n# =========================================================================\n\n`
  virtualServers.value.filter(v => v.enabled).forEach(v => {
    conf += `server {\n`
    conf += `    listen ${v.port}${v.ssl ? ' ssl http2' : ''};\n`
    conf += `    server_name ${v.domain};\n`
    if (v.ssl) {
      conf += `    ssl_certificate /etc/astaro/ssl/${v.domain}.crt;\n`
      conf += `    ssl_certificate_key /etc/astaro/ssl/${v.domain}.key;\n`
      conf += `    ssl_protocols TLSv1.2 TLSv1.3;\n`
    }
    conf += `    location / {\n`
    conf += `        proxy_pass http://${v.upstream};\n`
    conf += `        proxy_set_header Host $host;\n`
    conf += `        proxy_set_header X-Real-IP $remote_addr;\n`
    conf += `        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;\n`
    conf += `        proxy_set_header X-Forwarded-Proto $scheme;\n`
    conf += `        # NAXSI WAF Rules\n`
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
