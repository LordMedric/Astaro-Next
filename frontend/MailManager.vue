<template>
  <div class="space-y-6">
    <!-- Header Section -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-slate-200 pb-4">
      <div>
        <div class="flex items-center gap-2">
          <span class="w-1.5 h-5 bg-[#ee7f00] rounded-full"></span>
          <h1 class="text-xl font-bold text-slate-900">Email Protection</h1>
        </div>
        <p class="text-xs text-slate-500 mt-1">
          Configure SMTP/POP3 Proxy, Simple Mode or multi-domain SMTP Profiles, Postfix routing, Smart Host relaying, Anti-Spam, and Quarantine.
        </p>
      </div>

      <!-- Action Buttons -->
      <div class="flex items-center gap-2">
        <button
          type="button"
          @click="fetchQuarantine(true)"
          :disabled="isLoading"
          class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded bg-white hover:bg-slate-50 text-slate-700 border border-slate-300 text-xs font-bold shadow-xs cursor-pointer"
        >
          <svg
            :class="['w-3.5 h-3.5 text-slate-500', isLoading ? 'animate-spin text-[#005299]' : '']"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          <span>Refresh</span>
        </button>

        <button
          v-if="activeTab === 'profiles'"
          type="button"
          @click="openCreateProfileModal"
          class="inline-flex items-center gap-2 px-3.5 py-1.5 rounded bg-[#005299] hover:bg-[#003d73] text-white text-xs font-bold shadow-xs transition-colors cursor-pointer"
        >
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          <span>New SMTP Profile</span>
        </button>
      </div>
    </div>

    <!-- Tab Navigation Strip (Sophos UTM Style with Orange Active Underline) -->
    <div class="flex border-b border-slate-200 gap-1 bg-[#f4f6f9] p-1.5 rounded-t-lg overflow-x-auto">
      <button
        type="button"
        @click="activeTab = 'general'"
        :class="[
          'px-4 py-2 text-xs font-bold rounded-md transition-all flex items-center gap-2 cursor-pointer whitespace-nowrap',
          activeTab === 'general'
            ? 'bg-white text-slate-900 shadow-xs border-b-2 border-[#ee7f00]'
            : 'text-slate-600 hover:text-slate-900 hover:bg-white/60'
        ]"
      >
        <svg class="w-4 h-4 text-[#005299]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
        </svg>
        <span>Global &amp; Mode</span>
      </button>

      <button
        type="button"
        @click="activeTab = 'profiles'"
        :class="[
          'px-4 py-2 text-xs font-bold rounded-md transition-all flex items-center gap-2 cursor-pointer whitespace-nowrap',
          activeTab === 'profiles'
            ? 'bg-white text-slate-900 shadow-xs border-b-2 border-[#ee7f00]'
            : 'text-slate-600 hover:text-slate-900 hover:bg-white/60'
        ]"
      >
        <svg class="w-4 h-4 text-[#005299]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
        </svg>
        <span>SMTP Profiles ({{ smtpProfiles.length }})</span>
      </button>

      <button
        type="button"
        @click="activeTab = 'routing'"
        :class="[
          'px-4 py-2 text-xs font-bold rounded-md transition-all flex items-center gap-2 cursor-pointer whitespace-nowrap',
          activeTab === 'routing'
            ? 'bg-white text-slate-900 shadow-xs border-b-2 border-[#ee7f00]'
            : 'text-slate-600 hover:text-slate-900 hover:bg-white/60'
        ]"
      >
        <svg class="w-4 h-4 text-[#005299]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4" />
        </svg>
        <span>Routing &amp; Relaying</span>
      </button>

      <button
        type="button"
        @click="activeTab = 'antispam'"
        :class="[
          'px-4 py-2 text-xs font-bold rounded-md transition-all flex items-center gap-2 cursor-pointer whitespace-nowrap',
          activeTab === 'antispam'
            ? 'bg-white text-slate-900 shadow-xs border-b-2 border-[#ee7f00]'
            : 'text-slate-600 hover:text-slate-900 hover:bg-white/60'
        ]"
      >
        <svg class="w-4 h-4 text-[#005299]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
        </svg>
        <span>Anti-Spam &amp; Antivirus</span>
      </button>

      <button
        type="button"
        @click="activeTab = 'quarantine'"
        :class="[
          'px-4 py-2 text-xs font-bold rounded-md transition-all flex items-center gap-2 cursor-pointer whitespace-nowrap',
          activeTab === 'quarantine'
            ? 'bg-white text-slate-900 shadow-xs border-b-2 border-[#ee7f00]'
            : 'text-slate-600 hover:text-slate-900 hover:bg-white/60'
        ]"
      >
        <svg class="w-4 h-4 text-[#005299]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
        </svg>
        <span>Quarantine ({{ quarantineItems.length }})</span>
      </button>

      <button
        type="button"
        @click="activeTab = 'spool'"
        :class="[
          'px-4 py-2 text-xs font-bold rounded-md transition-all flex items-center gap-2 cursor-pointer whitespace-nowrap',
          activeTab === 'spool'
            ? 'bg-white text-slate-900 shadow-xs border-b-2 border-[#ee7f00]'
            : 'text-slate-600 hover:text-slate-900 hover:bg-white/60'
        ]"
      >
        <svg class="w-4 h-4 text-[#005299]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 10h16M4 14h16M4 18h16" />
        </svg>
        <span>Mail Spool / Queue ({{ spoolItems.length }})</span>
      </button>
    </div>

    <!-- TAB 1: GLOBAL & OPERATION MODE (Simple Mode vs Profile Mode) -->
    <div v-if="activeTab === 'general'" class="space-y-6">
      <!-- Operation Mode Selector Card -->
      <div class="bg-white rounded-xl border border-slate-200 shadow-xs p-5 space-y-4">
        <div class="flex items-center justify-between border-b border-slate-100 pb-3">
          <div>
            <h3 class="font-bold text-sm text-slate-900">SMTP Operation Mode</h3>
            <p class="text-xs text-slate-500 mt-0.5">
              Choose between simple single-domain relaying or multi-domain SMTP Profile isolation.
            </p>
          </div>
          <span
            :class="[
              'px-2.5 py-1 rounded text-xs font-bold font-mono border',
              operationMode === 'profile'
                ? 'bg-purple-50 text-purple-700 border-purple-200'
                : 'bg-blue-50 text-[#005299] border-blue-200'
            ]"
          >
            {{ operationMode === 'profile' ? 'PROFILE MODE ACTIVE' : 'SIMPLE MODE ACTIVE' }}
          </span>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 pt-2">
          <!-- Simple Mode Option Card -->
          <div
            @click="operationMode = 'simple'"
            :class="[
              'p-4 rounded-xl border-2 transition-all cursor-pointer flex items-start gap-3',
              operationMode === 'simple'
                ? 'border-[#005299] bg-blue-50/50 shadow-xs ring-1 ring-[#005299]/30'
                : 'border-slate-200 bg-white hover:bg-slate-50'
            ]"
          >
            <input
              type="radio"
              name="op-mode"
              :checked="operationMode === 'simple'"
              class="mt-1 text-[#005299]"
            />
            <div>
              <div class="font-bold text-slate-900 text-xs flex items-center gap-2">
                <span>Simple Mode</span>
                <span class="text-[10px] bg-slate-100 px-1.5 py-0.5 rounded text-slate-600">Standard</span>
              </div>
              <p class="text-[11px] text-slate-500 mt-1 leading-relaxed">
                Applies one unified set of antispam, antivirus, and upstream routing policies across all inbound and outbound email domains.
              </p>
            </div>
          </div>

          <!-- Profile Mode Option Card -->
          <div
            @click="operationMode = 'profile'"
            :class="[
              'p-4 rounded-xl border-2 transition-all cursor-pointer flex items-start gap-3',
              operationMode === 'profile'
                ? 'border-purple-600 bg-purple-50/50 shadow-xs ring-1 ring-purple-500/30'
                : 'border-slate-200 bg-white hover:bg-slate-50'
            ]"
          >
            <input
              type="radio"
              name="op-mode"
              :checked="operationMode === 'profile'"
              class="mt-1 text-purple-600"
            />
            <div>
              <div class="font-bold text-slate-900 text-xs flex items-center gap-2">
                <span>Profile Mode (Multiple SMTP Profiles)</span>
                <span class="text-[10px] bg-purple-100 px-1.5 py-0.5 rounded text-purple-800 font-bold">Sophos UTM Advanced</span>
              </div>
              <p class="text-[11px] text-slate-500 mt-1 leading-relaxed">
                Define distinct domain profiles with independent target Exchange/Postfix hosts, recipient verification callouts, SPX encryption, and quarantine actions per domain.
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- Global SMTP Switch & Listening Ports -->
      <div class="bg-white rounded-xl border border-slate-200 shadow-xs p-5 space-y-4">
        <div class="flex items-center justify-between border-b border-slate-100 pb-3">
          <div class="flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
            <h3 class="font-bold text-sm text-slate-900">Postfix SMTP Proxy Engine</h3>
          </div>
          <button
            type="button"
            @click="smtpProxyEnabled = !smtpProxyEnabled"
            class="relative inline-flex h-5 w-10 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out"
            :class="smtpProxyEnabled ? 'bg-[#005299]' : 'bg-slate-300'"
          >
            <span
              class="inline-block h-4 w-4 transform rounded-full bg-white shadow-sm transition duration-200"
              :class="smtpProxyEnabled ? 'translate-x-5' : 'translate-x-0'"
            ></span>
          </button>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 text-xs">
          <div class="p-3 bg-[#f4f6f9] rounded-lg border border-slate-200">
            <div class="text-slate-500 text-[10px] uppercase font-bold">Inbound Listener</div>
            <div class="text-slate-900 font-mono font-bold text-sm mt-1">Port 25 (ESMTP)</div>
          </div>
          <div class="p-3 bg-[#f4f6f9] rounded-lg border border-slate-200">
            <div class="text-slate-500 text-[10px] uppercase font-bold">Submission Port</div>
            <div class="text-slate-900 font-mono font-bold text-sm mt-1">Port 587 (STARTTLS)</div>
          </div>
          <div class="p-3 bg-[#f4f6f9] rounded-lg border border-slate-200">
            <div class="text-slate-500 text-[10px] uppercase font-bold">Max Message Size</div>
            <div class="text-slate-900 font-mono font-bold text-sm mt-1">50 MB</div>
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 2: SMTP PROFILES (Multi-Domain Profiles) -->
    <div v-if="activeTab === 'profiles'" class="space-y-4">
      <div v-if="operationMode === 'simple'" class="p-4 bg-amber-50 border border-amber-200 rounded-xl text-amber-900 text-xs flex items-center justify-between">
        <div class="flex items-center gap-2">
          <span>ℹ️</span>
          <span>SMTP Profiles are active when <strong>Profile Mode</strong> is enabled in Global &amp; Mode settings.</span>
        </div>
        <button
          type="button"
          @click="operationMode = 'profile'"
          class="px-3 py-1 bg-amber-600 hover:bg-amber-700 text-white rounded font-bold cursor-pointer"
        >
          Switch to Profile Mode
        </button>
      </div>

      <div class="bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden">
        <table class="w-full text-left text-xs border-collapse">
          <thead class="bg-[#f4f6f9] text-slate-700 font-bold border-b border-slate-200">
            <tr>
              <th class="p-3 pl-4 w-12 text-center">Status</th>
              <th class="p-3">Profile Name</th>
              <th class="p-3">Protected Domains</th>
              <th class="p-3">Target Mail Host</th>
              <th class="p-3">Recipient Verification</th>
              <th class="p-3">Spam Action</th>
              <th class="p-3 text-center">SPX Encryption</th>
              <th class="p-3 text-right pr-4">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100">
            <tr
              v-for="(prof, idx) in smtpProfiles"
              :key="prof.id"
              :class="idx % 2 === 0 ? 'bg-white' : 'bg-[#f7f7f7]'"
              class="hover:bg-blue-50/50 transition-colors"
            >
              <td class="p-3 pl-4 text-center">
                <button
                  type="button"
                  @click="prof.enabled = !prof.enabled"
                  class="relative inline-flex h-4 w-8 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out"
                  :class="prof.enabled ? 'bg-[#005299]' : 'bg-slate-300'"
                >
                  <span
                    class="inline-block h-3 w-3 transform rounded-full bg-white shadow-sm transition duration-200"
                    :class="prof.enabled ? 'translate-x-4' : 'translate-x-0'"
                  ></span>
                </button>
              </td>

              <td class="p-3 font-bold text-slate-900">
                {{ prof.name }}
              </td>

              <td class="p-3 font-mono font-bold text-[#005299]">
                <div class="flex items-center gap-1 flex-wrap">
                  <span v-for="(dom, dIdx) in prof.domains" :key="dIdx" class="px-2 py-0.5 rounded text-[10px] bg-blue-50 text-[#005299] border border-blue-200">
                    {{ dom }}
                  </span>
                </div>
              </td>

              <td class="p-3 font-mono font-bold text-slate-800">
                &rarr; {{ prof.target_host }}
              </td>

              <td class="p-3">
                <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-slate-100 text-slate-700">
                  {{ prof.recipient_verification }}
                </span>
              </td>

              <td class="p-3">
                <span
                  :class="[
                    'px-2 py-0.5 rounded text-[10px] font-bold uppercase border',
                    prof.spam_action === 'Quarantine' ? 'bg-amber-50 text-amber-800 border-amber-200' :
                    prof.spam_action === 'Reject' ? 'bg-rose-50 text-rose-800 border-rose-200' :
                    'bg-slate-100 text-slate-700 border-slate-200'
                  ]"
                >
                  {{ prof.spam_action }}
                </span>
              </td>

              <td class="p-3 text-center">
                <span v-if="prof.spx_enabled" class="text-purple-600 font-bold">🔒 Active</span>
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
    </div>

    <!-- TAB 3: ROUTING & RELAYING (Smart Host) -->
    <div v-if="activeTab === 'routing'" class="space-y-6">
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- Upstream Smarthost Configuration -->
        <div class="bg-white rounded-xl border border-slate-200 shadow-xs p-5 space-y-4">
          <div class="border-b border-slate-100 pb-3">
            <h3 class="font-bold text-sm text-slate-900">Upstream Smart Host (Outbound Relay)</h3>
            <p class="text-xs text-slate-500 mt-0.5">Route outbound messages through authenticated external relay provider.</p>
          </div>

          <div class="space-y-3 text-xs">
            <div>
              <label class="block font-bold text-slate-700 mb-1">Smart Host FQDN / IP</label>
              <input
                v-model="smarthost.host"
                type="text"
                placeholder="e.g. smtp.sendgrid.net or smtp.office365.com"
                class="w-full p-2 border border-slate-300 rounded font-mono focus:border-[#005299] focus:outline-none"
              />
            </div>
            <div class="grid grid-cols-2 gap-3">
              <div>
                <label class="block font-bold text-slate-700 mb-1">Port</label>
                <input
                  v-model="smarthost.port"
                  type="number"
                  placeholder="587"
                  class="w-full p-2 border border-slate-300 rounded font-mono focus:border-[#005299] focus:outline-none"
                />
              </div>
              <div>
                <label class="block font-bold text-slate-700 mb-1">Authentication</label>
                <select v-model="smarthost.auth" class="w-full p-2 border border-slate-300 rounded bg-white">
                  <option :value="true">Username / Password (TLS)</option>
                  <option :value="false">No Authentication (IP Whitelist)</option>
                </select>
              </div>
            </div>
            <div v-if="smarthost.auth" class="grid grid-cols-2 gap-3">
              <div>
                <label class="block font-bold text-slate-700 mb-1">Username</label>
                <input
                  v-model="smarthost.username"
                  type="text"
                  placeholder="apikey or user@company.com"
                  class="w-full p-2 border border-slate-300 rounded focus:border-[#005299] focus:outline-none"
                />
              </div>
              <div>
                <label class="block font-bold text-slate-700 mb-1">Password</label>
                <input
                  v-model="smarthost.password"
                  type="password"
                  placeholder="••••••••••••"
                  class="w-full p-2 border border-slate-300 rounded focus:border-[#005299] focus:outline-none"
                />
              </div>
            </div>
          </div>
        </div>

        <!-- Allowed Relay Networks -->
        <div class="bg-white rounded-xl border border-slate-200 shadow-xs p-5 space-y-4">
          <div class="border-b border-slate-100 pb-3">
            <h3 class="font-bold text-sm text-slate-900">Allowed Relaying Networks</h3>
            <p class="text-xs text-slate-500 mt-0.5">Internal networks permitted to relay unauthenticated outbound mail.</p>
          </div>

          <div class="space-y-3 text-xs">
            <div class="p-3 bg-[#f4f6f9] rounded-lg border border-slate-200 space-y-2 font-mono">
              <div class="flex items-center gap-2">
                <span class="w-2 h-2 rounded-full bg-[#005299]"></span>
                <span class="font-bold text-slate-900">Internal (Network) [192.168.1.0/24]</span>
              </div>
              <div class="flex items-center gap-2">
                <span class="w-2 h-2 rounded-full bg-[#005299]"></span>
                <span class="font-bold text-slate-900">DMZ (Network) [192.168.2.0/24]</span>
              </div>
            </div>
            <p class="text-[11px] text-slate-400">
              Manage these networks in <strong>Configure &rarr; Definitions &amp; Objects</strong>.
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 4: ANTI-SPAM & ANTIVIRUS -->
    <div v-if="activeTab === 'antispam'" class="space-y-6">
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- Anti-Spam Engine -->
        <div class="bg-white rounded-xl border border-slate-200 shadow-xs p-5 space-y-4 text-xs">
          <div class="border-b border-slate-100 pb-3">
            <h3 class="font-bold text-sm text-slate-900">Anti-Spam Engine (Rspamd / SpamAssassin)</h3>
            <p class="text-slate-500 mt-0.5">Heuristic score thresholds, Greylisting, and RBL blacklists.</p>
          </div>

          <div class="space-y-3">
            <div class="grid grid-cols-2 gap-3">
              <div>
                <label class="block font-bold text-slate-700 mb-1">Spam Threshold Score</label>
                <input
                  v-model="spamSettings.threshold"
                  type="number"
                  step="0.5"
                  class="w-full p-2 border border-slate-300 rounded font-mono focus:border-[#005299] focus:outline-none"
                />
              </div>
              <div>
                <label class="block font-bold text-slate-700 mb-1">Blackhole Threshold</label>
                <input
                  v-model="spamSettings.blackhole_threshold"
                  type="number"
                  step="0.5"
                  class="w-full p-2 border border-slate-300 rounded font-mono focus:border-[#005299] focus:outline-none"
                />
              </div>
            </div>

            <div class="space-y-2 pt-2 border-t border-slate-100">
              <div class="flex items-center gap-2">
                <input id="chk-grey" v-model="spamSettings.greylisting" type="checkbox" class="rounded text-[#005299]" />
                <label for="chk-grey" class="text-slate-700 font-semibold cursor-pointer">Greylisting (Temporarily reject unknown senders)</label>
              </div>
              <div class="flex items-center gap-2">
                <input id="chk-spf" v-model="spamSettings.spf" type="checkbox" class="rounded text-[#005299]" />
                <label for="chk-spf" class="text-slate-700 font-semibold cursor-pointer">SPF Verification (Sender Policy Framework)</label>
              </div>
              <div class="flex items-center gap-2">
                <input id="chk-dkim" v-model="spamSettings.dkim" type="checkbox" class="rounded text-[#005299]" />
                <label for="chk-dkim" class="text-slate-700 font-semibold cursor-pointer">DKIM Verification &amp; Inbound Signing</label>
              </div>
            </div>
          </div>
        </div>

        <!-- Antivirus & Attachment Quarantine -->
        <div class="bg-white rounded-xl border border-slate-200 shadow-xs p-5 space-y-4 text-xs">
          <div class="border-b border-slate-100 pb-3">
            <h3 class="font-bold text-sm text-slate-900">Antivirus &amp; Attachment Blocker</h3>
            <p class="text-slate-500 mt-0.5">Dual-engine malware scanning and dangerous file extension filtering.</p>
          </div>

          <div class="space-y-3">
            <div class="flex items-center justify-between p-3 bg-emerald-50 rounded-lg border border-emerald-200 text-emerald-900">
              <div>
                <div class="font-bold">ClamAV Scanning Engine Active</div>
                <div class="text-[11px] text-emerald-700">Real-time MIME attachment disassembly</div>
              </div>
              <span class="text-xs font-bold font-mono">100% ONLINE</span>
            </div>

            <div>
              <label class="block font-bold text-slate-700 mb-1">Blocked Attachment File Types</label>
              <input
                v-model="blockedExtensions"
                type="text"
                placeholder=".exe, .scr, .bat, .vbs, .js, .pif"
                class="w-full p-2 border border-slate-300 rounded font-mono focus:border-[#005299] focus:outline-none"
              />
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 5: QUARANTINE MANAGER -->
    <div v-if="activeTab === 'quarantine'" class="bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden">
      <table class="w-full text-left text-xs border-collapse">
        <thead class="bg-[#f4f6f9] text-slate-700 font-bold border-b border-slate-200">
          <tr>
            <th class="p-3 pl-4">Timestamp</th>
            <th class="p-3">Sender</th>
            <th class="p-3">Recipient</th>
            <th class="p-3">Subject</th>
            <th class="p-3">Threat Reason</th>
            <th class="p-3 text-right pr-4">Actions</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-100">
          <tr
            v-for="(item, idx) in quarantineItems"
            :key="item.id"
            :class="idx % 2 === 0 ? 'bg-white' : 'bg-[#f7f7f7]'"
            class="hover:bg-blue-50/50 transition-colors"
          >
            <td class="p-3 pl-4 text-slate-500 font-mono">{{ item.time }}</td>
            <td class="p-3 font-mono font-bold text-slate-800">{{ item.sender }}</td>
            <td class="p-3 font-mono text-slate-600">{{ item.recipient }}</td>
            <td class="p-3 font-semibold text-slate-900 truncate max-w-xs">{{ item.subject }}</td>
            <td class="p-3">
              <span
                :class="[
                  'px-2 py-0.5 rounded text-[10px] font-bold uppercase border',
                  item.reason === 'Malware' ? 'bg-rose-50 text-rose-700 border-rose-200' : 'bg-amber-50 text-amber-700 border-amber-200'
                ]"
              >
                {{ item.reason }} ({{ item.score }})
              </span>
            </td>
            <td class="p-3 text-right pr-4 space-x-2">
              <button
                type="button"
                @click="releaseQuarantine(item.id)"
                class="text-emerald-600 hover:text-emerald-800 font-bold cursor-pointer"
              >
                Release
              </button>
              <button
                type="button"
                @click="deleteQuarantine(item.id)"
                class="text-rose-600 hover:text-rose-800 font-bold cursor-pointer"
              >
                Delete
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- TAB 6: MAIL SPOOL / QUEUE -->
    <div v-if="activeTab === 'spool'" class="bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden">
      <div class="p-3 bg-[#f4f6f9] border-b border-slate-200 flex items-center justify-between">
        <span class="text-xs font-bold text-slate-700">Postfix Active &amp; Deferred Spool Queue</span>
        <button
          type="button"
          @click="flushQueue"
          class="px-3 py-1 rounded bg-[#005299] hover:bg-[#003d73] text-white text-xs font-bold shadow-xs cursor-pointer"
        >
          Flush Mail Queue
        </button>
      </div>

      <table class="w-full text-left text-xs border-collapse">
        <thead class="bg-[#f4f6f9] text-slate-700 font-bold border-b border-slate-200">
          <tr>
            <th class="p-3 pl-4">Queue ID</th>
            <th class="p-3">Sender</th>
            <th class="p-3">Recipient</th>
            <th class="p-3">Size</th>
            <th class="p-3">Status</th>
            <th class="p-3 text-right pr-4">Actions</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-100">
          <tr
            v-for="(item, idx) in spoolItems"
            :key="item.id"
            :class="idx % 2 === 0 ? 'bg-white' : 'bg-[#f7f7f7]'"
            class="hover:bg-blue-50/50 transition-colors"
          >
            <td class="p-3 pl-4 font-mono font-bold text-[#005299]">{{ item.queue_id }}</td>
            <td class="p-3 font-mono text-slate-700">{{ item.sender }}</td>
            <td class="p-3 font-mono text-slate-700">{{ item.recipient }}</td>
            <td class="p-3 text-slate-500 font-mono">{{ item.size }}</td>
            <td class="p-3">
              <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-amber-50 text-amber-800 border border-amber-200">
                {{ item.status }}
              </span>
            </td>
            <td class="p-3 text-right pr-4 space-x-2">
              <button
                type="button"
                @click="retrySpool(item.id)"
                class="text-blue-600 hover:text-blue-800 font-bold cursor-pointer"
              >
                Retry
              </button>
              <button
                type="button"
                @click="deleteSpool(item.id)"
                class="text-rose-600 hover:text-rose-800 font-bold cursor-pointer"
              >
                Delete
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- CREATE SMTP PROFILE MODAL -->
    <div
      v-if="isModalOpen"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-xs p-4"
    >
      <div class="bg-white rounded-xl shadow-2xl border border-slate-300 max-w-lg w-full overflow-hidden">
        <div class="px-5 py-3.5 bg-[#1b232e] text-white flex items-center justify-between border-b-2 border-[#ee7f00]">
          <h3 class="text-sm font-bold uppercase tracking-wider">Create SMTP Profile</h3>
          <button @click="isModalOpen = false" class="text-slate-400 hover:text-white font-bold cursor-pointer">✕</button>
        </div>

        <div class="p-5 space-y-4 text-xs">
          <div>
            <label class="block font-bold text-slate-700 mb-1">Profile Name</label>
            <input
              v-model="newProfile.name"
              type="text"
              placeholder="e.g. Primary Corporate Exchange Profile"
              class="w-full p-2 border border-slate-300 rounded focus:border-[#005299] focus:outline-none"
            />
          </div>

          <div>
            <label class="block font-bold text-slate-700 mb-1">Protected Domains (Comma-separated)</label>
            <input
              v-model="newProfile.domains_input"
              type="text"
              placeholder="e.g. company.com, sales.company.com"
              class="w-full p-2 border border-slate-300 rounded font-mono focus:border-[#005299] focus:outline-none"
            />
          </div>

          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block font-bold text-slate-700 mb-1">Target Host / IP</label>
              <input
                v-model="newProfile.target_host"
                type="text"
                placeholder="e.g. 192.168.1.50"
                class="w-full p-2 border border-slate-300 rounded font-mono focus:border-[#005299] focus:outline-none"
              />
            </div>
            <div>
              <label class="block font-bold text-slate-700 mb-1">Recipient Verification</label>
              <select v-model="newProfile.recipient_verification" class="w-full p-2 border border-slate-300 rounded bg-white">
                <option value="Active Directory (LDAP)">Active Directory (LDAP)</option>
                <option value="SMTP Callout">SMTP Callout</option>
                <option value="Disabled">Disabled</option>
              </select>
            </div>
          </div>

          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block font-bold text-slate-700 mb-1">Action on Spam</label>
              <select v-model="newProfile.spam_action" class="w-full p-2 border border-slate-300 rounded bg-white font-bold">
                <option value="Quarantine">Quarantine</option>
                <option value="Tag [SPAM]">Tag Subject [SPAM]</option>
                <option value="Reject">Reject (550)</option>
                <option value="Blackhole">Blackhole (Silently Drop)</option>
              </select>
            </div>
            <div>
              <label class="block font-bold text-slate-700 mb-1">Action on Malware</label>
              <select v-model="newProfile.malware_action" class="w-full p-2 border border-slate-300 rounded bg-white font-bold">
                <option value="Quarantine">Quarantine</option>
                <option value="Drop">Drop Attachment</option>
              </select>
            </div>
          </div>

          <div class="pt-2 border-t border-slate-100 space-y-2">
            <div class="flex items-center gap-2">
              <input id="spx-chk" v-model="newProfile.spx_enabled" type="checkbox" class="rounded text-[#005299]" />
              <label for="spx-chk" class="text-slate-700 font-semibold cursor-pointer">Enable SPX PDF Encryption for Outbound Sensitive Mail</label>
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
            @click="saveProfile"
            class="px-4 py-1.5 rounded bg-[#005299] hover:bg-[#003d73] text-white text-xs font-bold shadow-xs cursor-pointer"
          >
            Save Profile
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

const activeTab = ref('general') // 'general' | 'profiles' | 'routing' | 'antispam' | 'quarantine' | 'spool'
const operationMode = ref('profile') // 'simple' | 'profile'
const smtpProxyEnabled = ref(true)
const isLoading = ref(false)
const isModalOpen = ref(false)

const smarthost = ref({
  host: 'smtp.sendgrid.net',
  port: 587,
  auth: true,
  username: 'apikey',
  password: '••••••••••••'
})

const spamSettings = ref({
  threshold: 5.0,
  blackhole_threshold: 12.0,
  greylisting: true,
  spf: true,
  dkim: true
})

const blockedExtensions = ref('.exe, .scr, .bat, .vbs, .js, .pif, .hta, .cmd')

const smtpProfiles = ref([
  {
    id: 1,
    name: 'Corporate Exchange Mail Profile',
    domains: ['company.com', 'mail.company.com'],
    target_host: '192.168.1.50:25',
    recipient_verification: 'Active Directory (LDAP)',
    spam_action: 'Quarantine',
    malware_action: 'Quarantine',
    spx_enabled: true,
    enabled: true
  },
  {
    id: 2,
    name: 'Subsidiary & Marketing Domain Profile',
    domains: ['marketing-branch.com'],
    target_host: '192.168.2.30:25',
    recipient_verification: 'SMTP Callout',
    spam_action: 'Tag [SPAM]',
    malware_action: 'Quarantine',
    spx_enabled: false,
    enabled: true
  }
])

const quarantineItems = ref([
  { id: 1, time: '14:22:10', sender: 'phish@fake-invoice.com', recipient: 'finance@company.com', subject: 'Urgent Wire Transfer Request', reason: 'Spam', score: 9.8 },
  { id: 2, time: '12:05:41', sender: 'promo@freelotto.xyz', recipient: 'admin@company.com', subject: 'Claim Your $5,000 Voucher', reason: 'Spam', score: 8.2 },
  { id: 3, time: '09:14:22', sender: 'attacker@bad-domain.ru', recipient: 'it@company.com', subject: 'Invoice_Attachment.zip', reason: 'Malware', score: 10.0 }
])

const spoolItems = ref([
  { id: 1, queue_id: '4F89A1201B', sender: 'billing@company.com', recipient: 'client@remote-server.org', size: '42.1 KB', status: 'Deferred (Connection timeout)' },
  { id: 2, queue_id: '7A11C9088D', sender: 'noreply@company.com', recipient: 'user@yahoo.com', size: '18.4 KB', status: 'Active (Connecting)' }
])

const newProfile = ref({
  name: '',
  domains_input: '',
  target_host: '192.168.1.50',
  recipient_verification: 'Active Directory (LDAP)',
  spam_action: 'Quarantine',
  malware_action: 'Quarantine',
  spx_enabled: false
})

const openCreateProfileModal = () => {
  newProfile.value = {
    name: '',
    domains_input: '',
    target_host: '192.168.1.50',
    recipient_verification: 'Active Directory (LDAP)',
    spam_action: 'Quarantine',
    malware_action: 'Quarantine',
    spx_enabled: false
  }
  isModalOpen.value = true
}

const saveProfile = () => {
  if (!newProfile.value.name || !newProfile.value.domains_input) return
  const doms = newProfile.value.domains_input.split(',').map(d => d.trim()).filter(Boolean)
  smtpProfiles.value.push({
    id: smtpProfiles.value.length + 1,
    name: newProfile.value.name,
    domains: doms,
    target_host: newProfile.value.target_host,
    recipient_verification: newProfile.value.recipient_verification,
    spam_action: newProfile.value.spam_action,
    malware_action: newProfile.value.malware_action,
    spx_enabled: newProfile.value.spx_enabled,
    enabled: true
  })
  isModalOpen.value = false
}

const deleteProfile = (id) => {
  smtpProfiles.value = smtpProfiles.value.filter(p => p.id !== id)
}

const releaseQuarantine = (id) => {
  quarantineItems.value = quarantineItems.value.filter(q => q.id !== id)
}

const deleteQuarantine = (id) => {
  quarantineItems.value = quarantineItems.value.filter(q => q.id !== id)
}

const flushQueue = () => {
  spoolItems.value = []
}

const retrySpool = (id) => {
  const item = spoolItems.value.find(s => s.id === id)
  if (item) item.status = 'Retrying...'
}

const deleteSpool = (id) => {
  spoolItems.value = spoolItems.value.filter(s => s.id !== id)
}

const fetchQuarantine = (isManual = false) => {
  if (isManual) isLoading.value = true
  setTimeout(() => {
    isLoading.value = false
  }, 600)
}

onMounted(() => {})
</script>
