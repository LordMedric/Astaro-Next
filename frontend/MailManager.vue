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
          Next-generation SMTP/POP3 Mail Proxy with multi-domain SMTP Profiles, Postfix routing, DKIM, and Layer 7 Email Security.
        </p>
      </div>

      <!-- Action Buttons -->
      <div class="flex items-center gap-2">
        <button
          type="button"
          @click="fetchQuarantine(true)"
          :disabled="isLoading"
          class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-white hover:bg-slate-50 text-slate-700 border border-slate-300 text-xs font-semibold shadow-xs cursor-pointer"
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
          class="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-lg bg-[#005299] hover:bg-[#003d73] text-white text-xs font-bold shadow-xs transition-all cursor-pointer"
        >
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          <span>New SMTP Profile</span>
        </button>
      </div>
    </div>

    <!-- Tab Navigation Strip (Modern Sophos UTM Style with Orange Accent) -->
    <div class="flex border-b border-slate-200 gap-1 bg-[#f4f6f9] p-1.5 rounded-t-xl overflow-x-auto">
      <button
        type="button"
        @click="activeTab = 'general'"
        :class="[
          'px-4 py-2 text-xs font-bold rounded-lg transition-all flex items-center gap-2 cursor-pointer whitespace-nowrap',
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
          'px-4 py-2 text-xs font-bold rounded-lg transition-all flex items-center gap-2 cursor-pointer whitespace-nowrap',
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
          'px-4 py-2 text-xs font-bold rounded-lg transition-all flex items-center gap-2 cursor-pointer whitespace-nowrap',
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
          'px-4 py-2 text-xs font-bold rounded-lg transition-all flex items-center gap-2 cursor-pointer whitespace-nowrap',
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
        @click="activeTab = 'advanced'"
        :class="[
          'px-4 py-2 text-xs font-bold rounded-lg transition-all flex items-center gap-2 cursor-pointer whitespace-nowrap',
          activeTab === 'advanced'
            ? 'bg-white text-slate-900 shadow-xs border-b-2 border-[#ee7f00]'
            : 'text-slate-600 hover:text-slate-900 hover:bg-white/60'
        ]"
      >
        <svg class="w-4 h-4 text-[#005299]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4" />
        </svg>
        <span>Advanced (DKIM / TLS / BATV)</span>
      </button>

      <button
        type="button"
        @click="activeTab = 'quarantine'"
        :class="[
          'px-4 py-2 text-xs font-bold rounded-lg transition-all flex items-center gap-2 cursor-pointer whitespace-nowrap',
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
          'px-4 py-2 text-xs font-bold rounded-lg transition-all flex items-center gap-2 cursor-pointer whitespace-nowrap',
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

    <!-- TAB 1: GLOBAL & OPERATION MODE -->
    <div v-if="activeTab === 'general'" class="space-y-6">
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
              'px-2.5 py-1 rounded-full text-xs font-bold font-mono border',
              operationMode === 'profile'
                ? 'bg-purple-50 text-purple-700 border-purple-200'
                : 'bg-blue-50 text-[#005299] border-blue-200'
            ]"
          >
            {{ operationMode === 'profile' ? 'PROFILE MODE ACTIVE' : 'SIMPLE MODE ACTIVE' }}
          </span>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 pt-2">
          <!-- Simple Mode Card -->
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

          <!-- Profile Mode Card -->
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
          <div class="p-3 bg-[#f4f6f9] rounded-xl border border-slate-200">
            <div class="text-slate-500 text-[10px] uppercase font-bold">Inbound Listener</div>
            <div class="text-slate-900 font-mono font-bold text-sm mt-1">Port 25 (ESMTP)</div>
          </div>
          <div class="p-3 bg-[#f4f6f9] rounded-xl border border-slate-200">
            <div class="text-slate-500 text-[10px] uppercase font-bold">Submission Port</div>
            <div class="text-slate-900 font-mono font-bold text-sm mt-1">Port 587 (STARTTLS)</div>
          </div>
          <div class="p-3 bg-[#f4f6f9] rounded-xl border border-slate-200">
            <div class="text-slate-500 text-[10px] uppercase font-bold">Max Message Size</div>
            <div class="text-slate-900 font-mono font-bold text-sm mt-1">{{ advancedSettings.max_message_size_mb }} MB</div>
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 2: SMTP PROFILES (Modern Sophos UTM 9 Layout with 17 Option Groups in Modal) -->
    <div v-if="activeTab === 'profiles'" class="space-y-4">
      <!-- Search & Filters -->
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 bg-white p-3 rounded-xl border border-slate-200 shadow-xs">
        <div class="relative w-72">
          <input
            v-model="profileSearch"
            type="text"
            placeholder="Search profiles, domains..."
            class="w-full text-xs px-3 py-1.5 pl-8 rounded-lg border border-slate-300 bg-white focus:outline-none focus:border-[#005299]"
          />
          <svg class="w-3.5 h-3.5 text-slate-400 absolute left-2.5 top-2.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </div>
        <span class="text-xs text-slate-400 font-mono">
          Showing {{ filteredProfiles.length }} of {{ smtpProfiles.length }} profiles
        </span>
      </div>

      <!-- Modern Profiles Table -->
      <div class="bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden">
        <table class="w-full text-left text-xs border-collapse">
          <thead class="bg-[#f4f6f9] text-slate-700 font-bold border-b border-slate-200">
            <tr>
              <th class="p-3 pl-4 w-14 text-center">Status</th>
              <th class="p-3">Profile Name</th>
              <th class="p-3 font-mono">Protected Domains</th>
              <th class="p-3 font-mono">Target Host</th>
              <th class="p-3">Recipient Verification</th>
              <th class="p-3">Spam Action</th>
              <th class="p-3 text-center">SPX Encryption</th>
              <th class="p-3 text-right pr-4">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100">
            <tr
              v-for="(prof, idx) in filteredProfiles"
              :key="prof.id"
              :class="idx % 2 === 0 ? 'bg-white' : 'bg-[#f7f7f7]'"
              class="hover:bg-blue-50/50 transition-colors"
            >
              <td class="p-3 pl-4 text-center">
                <button
                  type="button"
                  @click="prof.enabled = !prof.enabled"
                  class="relative inline-flex h-4 w-8 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out"
                  :class="prof.enabled ? 'bg-emerald-500' : 'bg-slate-300'"
                >
                  <span
                    class="inline-block h-3 w-3 transform rounded-full bg-white shadow-sm transition duration-200"
                    :class="prof.enabled ? 'translate-x-4' : 'translate-x-0'"
                  ></span>
                </button>
              </td>

              <td class="p-3 font-bold text-slate-900 flex items-center gap-2">
                <span class="w-2 h-2 rounded-full bg-[#005299]"></span>
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
                &rarr; {{ prof.target_host }}:{{ prof.target_port || 25 }}
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

              <td class="p-3 text-right pr-4 space-x-1.5 whitespace-nowrap">
                <button
                  type="button"
                  @click="openEditProfileModal(prof)"
                  class="px-2.5 py-1 bg-slate-100 hover:bg-slate-200 text-slate-800 rounded-md font-bold cursor-pointer text-[11px] transition-colors"
                >
                  Edit
                </button>
                <button
                  type="button"
                  @click="cloneProfile(prof)"
                  class="px-2.5 py-1 bg-blue-50 hover:bg-blue-100 text-[#005299] border border-blue-200 rounded-md font-bold cursor-pointer text-[11px] transition-colors"
                >
                  Clone
                </button>
                <button
                  type="button"
                  @click="deleteProfile(prof.id)"
                  class="px-2.5 py-1 text-rose-600 hover:text-rose-800 font-bold cursor-pointer text-[11px] transition-colors"
                >
                  Delete
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- TAB 3: ROUTING & RELAYING -->
    <div v-if="activeTab === 'routing'" class="space-y-6">
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
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
                class="w-full p-2 border border-slate-300 rounded-lg font-mono focus:border-[#005299] focus:outline-none"
              />
            </div>
            <div class="grid grid-cols-2 gap-3">
              <div>
                <label class="block font-bold text-slate-700 mb-1">Port</label>
                <input
                  v-model="smarthost.port"
                  type="number"
                  placeholder="587"
                  class="w-full p-2 border border-slate-300 rounded-lg font-mono focus:border-[#005299] focus:outline-none"
                />
              </div>
              <div>
                <label class="block font-bold text-slate-700 mb-1">Authentication</label>
                <select v-model="smarthost.auth" class="w-full p-2 border border-slate-300 rounded-lg bg-white">
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
                  class="w-full p-2 border border-slate-300 rounded-lg focus:border-[#005299] focus:outline-none"
                />
              </div>
              <div>
                <label class="block font-bold text-slate-700 mb-1">Password</label>
                <input
                  v-model="smarthost.password"
                  type="password"
                  placeholder="••••••••••••"
                  class="w-full p-2 border border-slate-300 rounded-lg focus:border-[#005299] focus:outline-none"
                />
              </div>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-xl border border-slate-200 shadow-xs p-5 space-y-4">
          <div class="border-b border-slate-100 pb-3">
            <h3 class="font-bold text-sm text-slate-900">Allowed Relaying Networks</h3>
            <p class="text-xs text-slate-500 mt-0.5">Internal networks permitted to relay unauthenticated outbound mail.</p>
          </div>

          <div class="space-y-3 text-xs">
            <div class="p-3 bg-[#f4f6f9] rounded-xl border border-slate-200 space-y-2 font-mono">
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
                  class="w-full p-2 border border-slate-300 rounded-lg font-mono focus:border-[#005299] focus:outline-none"
                />
              </div>
              <div>
                <label class="block font-bold text-slate-700 mb-1">Blackhole Threshold</label>
                <input
                  v-model="spamSettings.blackhole_threshold"
                  type="number"
                  step="0.5"
                  class="w-full p-2 border border-slate-300 rounded-lg font-mono focus:border-[#005299] focus:outline-none"
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
                <input id="chk-dkim-verify" v-model="spamSettings.dkim" type="checkbox" class="rounded text-[#005299]" />
                <label for="chk-dkim-verify" class="text-slate-700 font-semibold cursor-pointer">Inbound DKIM Verification &amp; Spam Scoring</label>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-xl border border-slate-200 shadow-xs p-5 space-y-4 text-xs">
          <div class="border-b border-slate-100 pb-3">
            <h3 class="font-bold text-sm text-slate-900">Antivirus &amp; Attachment Blocker</h3>
            <p class="text-slate-500 mt-0.5">Dual-engine malware scanning and dangerous file extension filtering.</p>
          </div>

          <div class="space-y-3">
            <div class="flex items-center justify-between p-3 bg-emerald-50 rounded-xl border border-emerald-200 text-emerald-900">
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
                class="w-full p-2 border border-slate-300 rounded-lg font-mono focus:border-[#005299] focus:outline-none"
              />
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 5: ADVANCED (Sophos UTM 9 SMTP Advanced Tab + DKIM) -->
    <div v-if="activeTab === 'advanced'" class="space-y-6">
      <div class="bg-white rounded-xl border border-slate-200 shadow-xs p-5 space-y-4 text-xs">
        <div class="border-b border-slate-100 pb-3 flex items-center justify-between">
          <div>
            <h3 class="font-bold text-sm text-slate-900">Advanced Settings</h3>
            <p class="text-slate-500 mt-0.5">HELO greetings, postmaster notification address, and MTA connection concurrency limits.</p>
          </div>
          <span class="px-2 py-0.5 rounded-full text-[10px] font-mono font-bold bg-blue-50 text-[#005299] border border-blue-200">
            Postfix MTA Core
          </span>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="block font-bold text-slate-700 mb-1">SMTP Hostname (HELO / EHLO)</label>
            <input
              v-model="advancedSettings.smtp_hostname"
              type="text"
              placeholder="e.g. mail.company.com or astaro-gateway.internal"
              class="w-full p-2 border border-slate-300 rounded-lg font-mono focus:border-[#005299] focus:outline-none"
            />
          </div>

          <div>
            <label class="block font-bold text-slate-700 mb-1">Postmaster Address</label>
            <input
              v-model="advancedSettings.postmaster_address"
              type="email"
              placeholder="postmaster@company.com"
              class="w-full p-2 border border-slate-300 rounded-lg font-mono focus:border-[#005299] focus:outline-none"
            />
          </div>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-4 gap-4 pt-2 border-t border-slate-100">
          <div>
            <label class="block font-bold text-slate-700 mb-1">Max Message Size (MB)</label>
            <input
              v-model="advancedSettings.max_message_size_mb"
              type="number"
              min="1"
              max="500"
              class="w-full p-2 border border-slate-300 rounded-lg font-mono focus:border-[#005299] focus:outline-none"
            />
          </div>
          <div>
            <label class="block font-bold text-slate-700 mb-1">Max Connections</label>
            <input
              v-model="advancedSettings.max_connections"
              type="number"
              min="10"
              max="1000"
              class="w-full p-2 border border-slate-300 rounded-lg font-mono focus:border-[#005299] focus:outline-none"
            />
          </div>
          <div>
            <label class="block font-bold text-slate-700 mb-1">Max Connections / Host</label>
            <input
              v-model="advancedSettings.max_connections_per_host"
              type="number"
              min="1"
              max="100"
              class="w-full p-2 border border-slate-300 rounded-lg font-mono focus:border-[#005299] focus:outline-none"
            />
          </div>
          <div>
            <label class="block font-bold text-slate-700 mb-1">Max Recipients / Msg</label>
            <input
              v-model="advancedSettings.max_recipients_per_message"
              type="number"
              min="1"
              max="500"
              class="w-full p-2 border border-slate-300 rounded-lg font-mono focus:border-[#005299] focus:outline-none"
            />
          </div>
        </div>
      </div>

      <!-- TLS / SSL Settings -->
      <div class="bg-white rounded-xl border border-slate-200 shadow-xs p-5 space-y-4 text-xs">
        <div class="border-b border-slate-100 pb-3">
          <h3 class="font-bold text-sm text-slate-900">TLS / SSL Encryption &amp; Certificate Binding</h3>
          <p class="text-slate-500 mt-0.5">STARTTLS opportunistic and mandatory encryption on inbound and outbound SMTP.</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="block font-bold text-slate-700 mb-1">TLS Certificate for SMTP</label>
            <select
              v-model="advancedSettings.tls_cert_name"
              class="w-full p-2 border border-slate-300 rounded-lg bg-white font-semibold focus:border-[#005299] focus:outline-none"
            >
              <option value="Default Appliance SSL">Default Appliance SSL (Self-Signed)</option>
              <option value="Let's Encrypt Wildcard">Let's Encrypt Wildcard (*.company.com)</option>
              <option value="Custom Corporate PKI">Custom Corporate PKI Certificate</option>
            </select>
          </div>

          <div class="space-y-2 pt-2">
            <div class="flex items-center gap-2">
              <input id="adv-tls-req" v-model="advancedSettings.tls_required" type="checkbox" class="rounded text-[#005299]" />
              <label for="adv-tls-req" class="text-slate-700 font-semibold cursor-pointer">Require TLS Negotiation (STARTTLS Mandatory)</label>
            </div>
            <div class="flex items-center gap-2">
              <input id="adv-tls-strict" v-model="advancedSettings.tls_strict_ciphers" type="checkbox" class="rounded text-[#005299]" />
              <label for="adv-tls-strict" class="text-slate-700 font-semibold cursor-pointer">Enforce Strict TLS 1.2 / TLS 1.3 Ciphers with PFS</label>
            </div>
          </div>
        </div>
      </div>

      <!-- DomainKeys Identified Mail (DKIM) Inside Advanced -->
      <div class="bg-white rounded-xl border border-slate-200 shadow-xs p-5 space-y-4 text-xs">
        <div class="border-b border-slate-100 pb-3 flex items-center justify-between">
          <div>
            <h3 class="font-bold text-sm text-slate-900">DomainKeys Identified Mail (DKIM)</h3>
            <p class="text-slate-500 mt-0.5">Manage domain cryptographic RSA key pairs, selector bindings, and DNS TXT public records.</p>
          </div>
          <button
            type="button"
            @click="openCreateDkimModal"
            class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-[#005299] hover:bg-[#003d73] text-white text-xs font-bold shadow-xs cursor-pointer"
          >
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
            </svg>
            <span>New DKIM Key</span>
          </button>
        </div>

        <div class="bg-white rounded-xl border border-slate-200 overflow-hidden">
          <table class="w-full text-left text-xs border-collapse">
            <thead class="bg-[#f4f6f9] text-slate-700 font-bold border-b border-slate-200">
              <tr>
                <th class="p-3 pl-4 w-12 text-center">Status</th>
                <th class="p-3">Domain</th>
                <th class="p-3 font-mono">Selector</th>
                <th class="p-3">Key Size</th>
                <th class="p-3 font-mono">DNS Host Record</th>
                <th class="p-3 text-right pr-4">Actions</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100">
              <tr
                v-for="(dkim, idx) in dkimKeys"
                :key="dkim.id"
                :class="idx % 2 === 0 ? 'bg-white' : 'bg-[#f7f7f7]'"
                class="hover:bg-blue-50/50 transition-colors"
              >
                <td class="p-3 pl-4 text-center">
                  <button
                    type="button"
                    @click="dkim.enabled = !dkim.enabled"
                    class="relative inline-flex h-4 w-8 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out"
                    :class="dkim.enabled ? 'bg-emerald-500' : 'bg-slate-300'"
                  >
                    <span
                      class="inline-block h-3 w-3 transform rounded-full bg-white shadow-sm transition duration-200"
                      :class="dkim.enabled ? 'translate-x-4' : 'translate-x-0'"
                    ></span>
                  </button>
                </td>

                <td class="p-3 font-bold text-slate-900 flex items-center gap-2">
                  <span class="w-2 h-2 rounded-full bg-emerald-500"></span>
                  {{ dkim.domain }}
                </td>

                <td class="p-3 font-mono font-bold text-[#005299]">
                  {{ dkim.selector }}
                </td>

                <td class="p-3">
                  <span class="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-slate-100 text-slate-700 border border-slate-200">
                    {{ dkim.key_size }}-bit RSA
                  </span>
                </td>

                <td class="p-3 font-mono text-slate-700 font-semibold truncate max-w-xs">
                  {{ dkim.dns_host_name }}
                </td>

                <td class="p-3 text-right pr-4 space-x-2">
                  <button
                    type="button"
                    @click="viewDnsRecord(dkim)"
                    class="px-2.5 py-1 bg-blue-50 hover:bg-blue-100 text-[#005299] border border-blue-200 rounded-md font-bold cursor-pointer text-[11px]"
                  >
                    View DNS TXT
                  </button>
                  <button
                    type="button"
                    @click="deleteDkimKey(dkim.id)"
                    class="text-rose-600 hover:text-rose-800 font-bold cursor-pointer text-[11px]"
                  >
                    Delete
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Save Button Bar -->
      <div class="flex items-center justify-end gap-3 p-4 bg-white rounded-xl border border-slate-200 shadow-xs">
        <button
          type="button"
          @click="saveAdvancedSettings"
          :disabled="isSavingAdvanced"
          class="inline-flex items-center gap-2 px-5 py-2 rounded-lg bg-[#005299] hover:bg-[#003d73] text-white text-xs font-bold shadow-xs transition-colors cursor-pointer disabled:opacity-50"
        >
          <svg v-if="isSavingAdvanced" class="w-3.5 h-3.5 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          <span>{{ isSavingAdvanced ? 'Saving Postfix Configuration...' : 'Save Advanced Settings' }}</span>
        </button>
      </div>
    </div>

    <!-- TAB 6: QUARANTINE MANAGER -->
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

    <!-- TAB 7: MAIL SPOOL / QUEUE -->
    <div v-if="activeTab === 'spool'" class="bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden">
      <div class="p-3 bg-[#f4f6f9] border-b border-slate-200 flex items-center justify-between">
        <span class="text-xs font-bold text-slate-700">Postfix Active &amp; Deferred Spool Queue</span>
        <button
          type="button"
          @click="flushQueue"
          class="px-3.5 py-1.5 rounded-lg bg-[#005299] hover:bg-[#003d73] text-white text-xs font-bold shadow-xs cursor-pointer"
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

    <!-- MODERN FULL-FEATURED 17-OPTION-GROUP SMTP PROFILE MODAL -->
    <div
      v-if="isModalOpen"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-xs p-4 overflow-y-auto"
    >
      <div class="bg-white rounded-2xl shadow-2xl border border-slate-300 max-w-3xl w-full my-8 overflow-hidden">
        <!-- Modal Header -->
        <div class="px-6 py-4 bg-[#1b232e] text-white flex items-center justify-between border-b-2 border-[#ee7f00]">
          <div>
            <h3 class="text-sm font-bold uppercase tracking-wider">
              {{ editingProfileId ? 'Edit SMTP Profile' : 'Create SMTP Profile' }}
            </h3>
            <p class="text-[11px] text-slate-400 mt-0.5">
              Configure multi-domain mail routing, antispam scoring, ClamAV malware inspection, and DLP.
            </p>
          </div>
          <button @click="isModalOpen = false" class="text-slate-400 hover:text-white font-bold text-lg cursor-pointer">✕</button>
        </div>

        <!-- Modal Body (Scrollable with Modern Accordions) -->
        <div class="p-6 space-y-5 text-xs max-h-[75vh] overflow-y-auto">
          
          <!-- Top Row: Profile Name & Domains -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block font-bold text-slate-700 mb-1">Profile Name</label>
              <input
                v-model="editProfileData.name"
                type="text"
                placeholder="e.g. Medricnetworks.com"
                class="w-full p-2.5 border border-slate-300 rounded-lg focus:border-[#005299] focus:outline-none bg-white font-semibold"
              />
            </div>

            <div>
              <label class="block font-bold text-slate-700 mb-1">Protected Domains (Comma-separated)</label>
              <input
                v-model="editProfileData.domains_input"
                type="text"
                placeholder="e.g. medricnetworks.com, mail.medricnetworks.com"
                class="w-full p-2.5 border border-slate-300 rounded-lg font-mono focus:border-[#005299] focus:outline-none bg-white"
              />
            </div>
          </div>

          <!-- ALL 17 SOPHOS UTM 9 OPTION GROUPS (Clean Modern Accordions) -->
          <div class="space-y-2 pt-2 border-t border-slate-200">
            <h4 class="font-bold text-slate-900 uppercase text-[11px] tracking-wider text-slate-500 mb-2">
              Sophos UTM Security &amp; Policy Option Groups (17 Groups)
            </h4>

            <!-- 1. Routing -->
            <div class="border border-slate-200 rounded-xl overflow-hidden shadow-2xs">
              <button
                type="button"
                @click="toggleAccordion('routing')"
                class="w-full px-4 py-2.5 bg-[#f8fafc] hover:bg-slate-100 flex items-center justify-between font-bold text-slate-800 cursor-pointer transition-colors"
              >
                <div class="flex items-center gap-2.5">
                  <span class="w-5 h-5 rounded-full bg-[#005299] text-white text-[11px] flex items-center justify-center font-bold">1</span>
                  <span>Routing</span>
                </div>
                <span class="text-slate-400 text-xs">{{ openAccordions.includes('routing') ? '▲ Collapse' : '▼ Expand' }}</span>
              </button>
              <div v-if="openAccordions.includes('routing')" class="p-4 bg-white space-y-3 border-t border-slate-200">
                <div class="grid grid-cols-2 gap-3">
                  <div>
                    <label class="block font-bold text-slate-700 mb-1">Target Host / IP</label>
                    <input v-model="editProfileData.target_host" type="text" class="w-full p-2 border border-slate-300 rounded-lg font-mono" placeholder="192.168.1.50" />
                  </div>
                  <div>
                    <label class="block font-bold text-slate-700 mb-1">Target Port</label>
                    <input v-model="editProfileData.target_port" type="number" class="w-full p-2 border border-slate-300 rounded-lg font-mono" placeholder="25" />
                  </div>
                </div>
              </div>
            </div>

            <!-- 2. Recipient Verification -->
            <div class="border border-slate-200 rounded-xl overflow-hidden shadow-2xs">
              <button
                type="button"
                @click="toggleAccordion('recipient_verification')"
                class="w-full px-4 py-2.5 bg-[#f8fafc] hover:bg-slate-100 flex items-center justify-between font-bold text-slate-800 cursor-pointer transition-colors"
              >
                <div class="flex items-center gap-2.5">
                  <span class="w-5 h-5 rounded-full bg-slate-200 text-slate-700 text-[11px] flex items-center justify-center font-bold">2</span>
                  <span>Recipient Verification</span>
                </div>
                <span class="text-slate-400 text-xs">{{ openAccordions.includes('recipient_verification') ? '▲ Collapse' : '▼ Expand' }}</span>
              </button>
              <div v-if="openAccordions.includes('recipient_verification')" class="p-4 bg-white space-y-2 border-t border-slate-200">
                <label class="block font-bold text-slate-700 mb-1">Verification Method</label>
                <select v-model="editProfileData.recipient_verification" class="w-full p-2 border border-slate-300 rounded-lg bg-white">
                  <option value="Active Directory (LDAP)">Active Directory (LDAP)</option>
                  <option value="SMTP Callout">SMTP Callout</option>
                  <option value="None">None (Accept All)</option>
                </select>
              </div>
            </div>

            <!-- 3. Sophos UTM RBLs -->
            <div class="border border-slate-200 rounded-xl overflow-hidden shadow-2xs">
              <button
                type="button"
                @click="toggleAccordion('sophos_rbls')"
                class="w-full px-4 py-2.5 bg-[#f8fafc] hover:bg-slate-100 flex items-center justify-between font-bold text-slate-800 cursor-pointer transition-colors"
              >
                <div class="flex items-center gap-2.5">
                  <span class="w-5 h-5 rounded-full bg-slate-200 text-slate-700 text-[11px] flex items-center justify-center font-bold">3</span>
                  <span>Sophos UTM RBLs</span>
                </div>
                <span class="text-slate-400 text-xs">{{ openAccordions.includes('sophos_rbls') ? '▲ Collapse' : '▼ Expand' }}</span>
              </button>
              <div v-if="openAccordions.includes('sophos_rbls')" class="p-4 bg-white space-y-2 border-t border-slate-200">
                <div class="flex items-center gap-2">
                  <input id="rbl-sophos-m" v-model="editProfileData.use_sophos_rbls" type="checkbox" class="rounded text-[#005299]" />
                  <label for="rbl-sophos-m" class="font-bold text-slate-700 cursor-pointer">Use Sophos Real-time Blacklists (SBL/XBL/PBL)</label>
                </div>
              </div>
            </div>

            <!-- 4. Extra RBLs -->
            <div class="border border-slate-200 rounded-xl overflow-hidden shadow-2xs">
              <button
                type="button"
                @click="toggleAccordion('extra_rbls')"
                class="w-full px-4 py-2.5 bg-[#f8fafc] hover:bg-slate-100 flex items-center justify-between font-bold text-slate-800 cursor-pointer transition-colors"
              >
                <div class="flex items-center gap-2.5">
                  <span class="w-5 h-5 rounded-full bg-slate-200 text-slate-700 text-[11px] flex items-center justify-center font-bold">4</span>
                  <span>Extra RBLs</span>
                </div>
                <span class="text-slate-400 text-xs">{{ openAccordions.includes('extra_rbls') ? '▲ Collapse' : '▼ Expand' }}</span>
              </button>
              <div v-if="openAccordions.includes('extra_rbls')" class="p-4 bg-white space-y-2 border-t border-slate-200">
                <label class="block font-bold text-slate-700 mb-1">Additional DNSBL / RBL Hosts</label>
                <textarea v-model="editProfileData.extra_rbls" rows="2" class="w-full p-2 border border-slate-300 rounded-lg font-mono" placeholder="zen.spamhaus.org&#10;bl.spamcop.net"></textarea>
              </div>
            </div>

            <!-- 5. BATV/RDNS/HELO/SPF/Greylisting -->
            <div class="border border-slate-200 rounded-xl overflow-hidden shadow-2xs">
              <button
                type="button"
                @click="toggleAccordion('mta_checks')"
                class="w-full px-4 py-2.5 bg-[#f8fafc] hover:bg-slate-100 flex items-center justify-between font-bold text-slate-800 cursor-pointer transition-colors"
              >
                <div class="flex items-center gap-2.5">
                  <span class="w-5 h-5 rounded-full bg-slate-200 text-slate-700 text-[11px] flex items-center justify-center font-bold">5</span>
                  <span>BATV/RDNS/HELO/SPF/Greylisting</span>
                </div>
                <span class="text-slate-400 text-xs">{{ openAccordions.includes('mta_checks') ? '▲ Collapse' : '▼ Expand' }}</span>
              </button>
              <div v-if="openAccordions.includes('mta_checks')" class="p-4 bg-white space-y-3 border-t border-slate-200">
                <div class="grid grid-cols-2 gap-3">
                  <div class="flex items-center gap-2">
                    <input id="chk-batv-m" v-model="editProfileData.batv" type="checkbox" class="rounded text-[#005299]" />
                    <label for="chk-batv-m" class="cursor-pointer font-semibold">BATV Signing (Anti-Backscatter)</label>
                  </div>
                  <div class="flex items-center gap-2">
                    <input id="chk-rdns-m" v-model="editProfileData.rdns" type="checkbox" class="rounded text-[#005299]" />
                    <label for="chk-rdns-m" class="cursor-pointer font-semibold">Reverse DNS Check</label>
                  </div>
                  <div class="flex items-center gap-2">
                    <input id="chk-helo-m" v-model="editProfileData.helo" type="checkbox" class="rounded text-[#005299]" />
                    <label for="chk-helo-m" class="cursor-pointer font-semibold">Strict HELO / EHLO Check</label>
                  </div>
                  <div class="flex items-center gap-2">
                    <input id="chk-spf-m" v-model="editProfileData.spf" type="checkbox" class="rounded text-[#005299]" />
                    <label for="chk-spf-m" class="cursor-pointer font-semibold">SPF Verification</label>
                  </div>
                  <div class="flex items-center gap-2">
                    <input id="chk-grey-m" v-model="editProfileData.greylisting" type="checkbox" class="rounded text-[#005299]" />
                    <label for="chk-grey-m" class="cursor-pointer font-semibold">Greylisting</label>
                  </div>
                </div>
              </div>
            </div>

            <!-- 6. Malware Scanning -->
            <div class="border border-slate-200 rounded-xl overflow-hidden shadow-2xs">
              <button
                type="button"
                @click="toggleAccordion('malware')"
                class="w-full px-4 py-2.5 bg-[#f8fafc] hover:bg-slate-100 flex items-center justify-between font-bold text-slate-800 cursor-pointer transition-colors"
              >
                <div class="flex items-center gap-2.5">
                  <span class="w-5 h-5 rounded-full bg-slate-200 text-slate-700 text-[11px] flex items-center justify-center font-bold">6</span>
                  <span>Malware Scanning</span>
                </div>
                <span class="text-slate-400 text-xs">{{ openAccordions.includes('malware') ? '▲ Collapse' : '▼ Expand' }}</span>
              </button>
              <div v-if="openAccordions.includes('malware')" class="p-4 bg-white space-y-3 border-t border-slate-200">
                <div class="grid grid-cols-2 gap-3">
                  <div>
                    <label class="block font-bold text-slate-700 mb-1">Dual-Engine Scanning</label>
                    <select v-model="editProfileData.malware_engine" class="w-full p-2 border border-slate-300 rounded-lg bg-white">
                      <option value="ClamAV + Avira">ClamAV + Avira</option>
                      <option value="ClamAV Only">ClamAV Only</option>
                    </select>
                  </div>
                  <div>
                    <label class="block font-bold text-slate-700 mb-1">Action on Virus</label>
                    <select v-model="editProfileData.malware_action" class="w-full p-2 border border-slate-300 rounded-lg bg-white font-bold">
                      <option value="Quarantine">Quarantine</option>
                      <option value="Drop">Drop Attachment</option>
                      <option value="Reject">Reject (550)</option>
                    </select>
                  </div>
                </div>
              </div>
            </div>

            <!-- 7. Antispam Scanning -->
            <div class="border border-slate-200 rounded-xl overflow-hidden shadow-2xs">
              <button
                type="button"
                @click="toggleAccordion('antispam')"
                class="w-full px-4 py-2.5 bg-[#f8fafc] hover:bg-slate-100 flex items-center justify-between font-bold text-slate-800 cursor-pointer transition-colors"
              >
                <div class="flex items-center gap-2.5">
                  <span class="w-5 h-5 rounded-full bg-slate-200 text-slate-700 text-[11px] flex items-center justify-center font-bold">7</span>
                  <span>Antispam Scanning</span>
                </div>
                <span class="text-slate-400 text-xs">{{ openAccordions.includes('antispam') ? '▲ Collapse' : '▼ Expand' }}</span>
              </button>
              <div v-if="openAccordions.includes('antispam')" class="p-4 bg-white space-y-3 border-t border-slate-200">
                <div class="grid grid-cols-2 gap-3">
                  <div>
                    <label class="block font-bold text-slate-700 mb-1">Spam Score Threshold</label>
                    <input v-model="editProfileData.spam_score" type="number" step="0.5" class="w-full p-2 border border-slate-300 rounded-lg font-mono" />
                  </div>
                  <div>
                    <label class="block font-bold text-slate-700 mb-1">Action on Spam</label>
                    <select v-model="editProfileData.spam_action" class="w-full p-2 border border-slate-300 rounded-lg bg-white font-bold">
                      <option value="Quarantine">Quarantine</option>
                      <option value="Tag [SPAM]">Tag Subject [SPAM]</option>
                      <option value="Reject">Reject (550)</option>
                      <option value="Blackhole">Blackhole</option>
                    </select>
                  </div>
                </div>
              </div>
            </div>

            <!-- 8. Sender Blacklist -->
            <div class="border border-slate-200 rounded-xl overflow-hidden shadow-2xs">
              <button
                type="button"
                @click="toggleAccordion('sender_blacklist')"
                class="w-full px-4 py-2.5 bg-[#f8fafc] hover:bg-slate-100 flex items-center justify-between font-bold text-slate-800 cursor-pointer transition-colors"
              >
                <div class="flex items-center gap-2.5">
                  <span class="w-5 h-5 rounded-full bg-slate-200 text-slate-700 text-[11px] flex items-center justify-center font-bold">8</span>
                  <span>Sender Blacklist</span>
                </div>
                <span class="text-slate-400 text-xs">{{ openAccordions.includes('sender_blacklist') ? '▲ Collapse' : '▼ Expand' }}</span>
              </button>
              <div v-if="openAccordions.includes('sender_blacklist')" class="p-4 bg-white space-y-2 border-t border-slate-200">
                <textarea v-model="editProfileData.sender_blacklist" rows="2" class="w-full p-2 border border-slate-300 rounded-lg font-mono" placeholder="*@spammer.com&#10;badactor@domain.xyz"></textarea>
              </div>
            </div>

            <!-- 9. MIME Audio/Video/Executables blocking -->
            <div class="border border-slate-200 rounded-xl overflow-hidden shadow-2xs">
              <button
                type="button"
                @click="toggleAccordion('mime_blocking')"
                class="w-full px-4 py-2.5 bg-[#f8fafc] hover:bg-slate-100 flex items-center justify-between font-bold text-slate-800 cursor-pointer transition-colors"
              >
                <div class="flex items-center gap-2.5">
                  <span class="w-5 h-5 rounded-full bg-slate-200 text-slate-700 text-[11px] flex items-center justify-center font-bold">9</span>
                  <span>MIME Audio/Video/Executables blocking</span>
                </div>
                <span class="text-slate-400 text-xs">{{ openAccordions.includes('mime_blocking') ? '▲ Collapse' : '▼ Expand' }}</span>
              </button>
              <div v-if="openAccordions.includes('mime_blocking')" class="p-4 bg-white space-y-2 border-t border-slate-200">
                <div class="space-y-1.5">
                  <div class="flex items-center gap-2">
                    <input id="chk-blk-exe-m" v-model="editProfileData.block_executables" type="checkbox" class="rounded text-[#005299]" />
                    <label for="chk-blk-exe-m" class="cursor-pointer font-semibold">Block Executables (.exe, .scr, .com, .bat)</label>
                  </div>
                  <div class="flex items-center gap-2">
                    <input id="chk-blk-media-m" v-model="editProfileData.block_media" type="checkbox" class="rounded text-[#005299]" />
                    <label for="chk-blk-media-m" class="cursor-pointer font-semibold">Block Audio &amp; Video Streams</label>
                  </div>
                </div>
              </div>
            </div>

            <!-- 10. MIME Type Blacklist -->
            <div class="border border-slate-200 rounded-xl overflow-hidden shadow-2xs">
              <button
                type="button"
                @click="toggleAccordion('mime_blacklist')"
                class="w-full px-4 py-2.5 bg-[#f8fafc] hover:bg-slate-100 flex items-center justify-between font-bold text-slate-800 cursor-pointer transition-colors"
              >
                <div class="flex items-center gap-2.5">
                  <span class="w-5 h-5 rounded-full bg-slate-200 text-slate-700 text-[11px] flex items-center justify-center font-bold">10</span>
                  <span>MIME Type Blacklist</span>
                </div>
                <span class="text-slate-400 text-xs">{{ openAccordions.includes('mime_blacklist') ? '▲ Collapse' : '▼ Expand' }}</span>
              </button>
              <div v-if="openAccordions.includes('mime_blacklist')" class="p-4 bg-white space-y-2 border-t border-slate-200">
                <textarea v-model="editProfileData.mime_blacklist" rows="2" class="w-full p-2 border border-slate-300 rounded-lg font-mono" placeholder="application/x-msdownload&#10;application/x-dosexec"></textarea>
              </div>
            </div>

            <!-- 11. MIME Type Whitelist -->
            <div class="border border-slate-200 rounded-xl overflow-hidden shadow-2xs">
              <button
                type="button"
                @click="toggleAccordion('mime_whitelist')"
                class="w-full px-4 py-2.5 bg-[#f8fafc] hover:bg-slate-100 flex items-center justify-between font-bold text-slate-800 cursor-pointer transition-colors"
              >
                <div class="flex items-center gap-2.5">
                  <span class="w-5 h-5 rounded-full bg-slate-200 text-slate-700 text-[11px] flex items-center justify-center font-bold">11</span>
                  <span>MIME Type Whitelist</span>
                </div>
                <span class="text-slate-400 text-xs">{{ openAccordions.includes('mime_whitelist') ? '▲ Collapse' : '▼ Expand' }}</span>
              </button>
              <div v-if="openAccordions.includes('mime_whitelist')" class="p-4 bg-white space-y-2 border-t border-slate-200">
                <textarea v-model="editProfileData.mime_whitelist" rows="2" class="w-full p-2 border border-slate-300 rounded-lg font-mono" placeholder="application/pdf&#10;image/png"></textarea>
              </div>
            </div>

            <!-- 12. Blocked File Extensions -->
            <div class="border border-slate-200 rounded-xl overflow-hidden shadow-2xs">
              <button
                type="button"
                @click="toggleAccordion('blocked_ext')"
                class="w-full px-4 py-2.5 bg-[#f8fafc] hover:bg-slate-100 flex items-center justify-between font-bold text-slate-800 cursor-pointer transition-colors"
              >
                <div class="flex items-center gap-2.5">
                  <span class="w-5 h-5 rounded-full bg-slate-200 text-slate-700 text-[11px] flex items-center justify-center font-bold">12</span>
                  <span>Blocked File Extensions</span>
                </div>
                <span class="text-slate-400 text-xs">{{ openAccordions.includes('blocked_ext') ? '▲ Collapse' : '▼ Expand' }}</span>
              </button>
              <div v-if="openAccordions.includes('blocked_ext')" class="p-4 bg-white space-y-2 border-t border-slate-200">
                <input v-model="editProfileData.blocked_extensions" type="text" class="w-full p-2 border border-slate-300 rounded-lg font-mono" placeholder=".exe, .scr, .bat, .vbs, .js, .pif" />
              </div>
            </div>

            <!-- 13. Blocked Expressions -->
            <div class="border border-slate-200 rounded-xl overflow-hidden shadow-2xs">
              <button
                type="button"
                @click="toggleAccordion('blocked_expressions')"
                class="w-full px-4 py-2.5 bg-[#f8fafc] hover:bg-slate-100 flex items-center justify-between font-bold text-slate-800 cursor-pointer transition-colors"
              >
                <div class="flex items-center gap-2.5">
                  <span class="w-5 h-5 rounded-full bg-slate-200 text-slate-700 text-[11px] flex items-center justify-center font-bold">13</span>
                  <span>Blocked Expressions</span>
                </div>
                <span class="text-slate-400 text-xs">{{ openAccordions.includes('blocked_expressions') ? '▲ Collapse' : '▼ Expand' }}</span>
              </button>
              <div v-if="openAccordions.includes('blocked_expressions')" class="p-4 bg-white space-y-2 border-t border-slate-200">
                <textarea v-model="editProfileData.blocked_expressions" rows="2" class="w-full p-2 border border-slate-300 rounded-lg font-mono" placeholder="urgent wire transfer&#10;claim your prize"></textarea>
              </div>
            </div>

            <!-- 14. Confidentiality Footer -->
            <div class="border border-slate-200 rounded-xl overflow-hidden shadow-2xs">
              <button
                type="button"
                @click="toggleAccordion('footer')"
                class="w-full px-4 py-2.5 bg-[#f8fafc] hover:bg-slate-100 flex items-center justify-between font-bold text-slate-800 cursor-pointer transition-colors"
              >
                <div class="flex items-center gap-2.5">
                  <span class="w-5 h-5 rounded-full bg-slate-200 text-slate-700 text-[11px] flex items-center justify-center font-bold">14</span>
                  <span>Confidentiality Footer</span>
                </div>
                <span class="text-slate-400 text-xs">{{ openAccordions.includes('footer') ? '▲ Collapse' : '▼ Expand' }}</span>
              </button>
              <div v-if="openAccordions.includes('footer')" class="p-4 bg-white space-y-2 border-t border-slate-200">
                <div class="flex items-center gap-2">
                  <input id="chk-footer-m" v-model="editProfileData.append_footer" type="checkbox" class="rounded text-[#005299]" />
                  <label for="chk-footer-m" class="font-bold text-slate-700 cursor-pointer">Append Outbound Legal Disclaimer</label>
                </div>
                <textarea v-if="editProfileData.append_footer" v-model="editProfileData.footer_text" rows="3" class="w-full p-2 border border-slate-300 rounded-lg font-mono" placeholder="<p>Confidential...</p>"></textarea>
              </div>
            </div>

            <!-- 15. SPX Template Selection -->
            <div class="border border-slate-200 rounded-xl overflow-hidden shadow-2xs">
              <button
                type="button"
                @click="toggleAccordion('spx')"
                class="w-full px-4 py-2.5 bg-[#f8fafc] hover:bg-slate-100 flex items-center justify-between font-bold text-slate-800 cursor-pointer transition-colors"
              >
                <div class="flex items-center gap-2.5">
                  <span class="w-5 h-5 rounded-full bg-slate-200 text-slate-700 text-[11px] flex items-center justify-center font-bold">15</span>
                  <span>SPX Template Selection</span>
                </div>
                <span class="text-slate-400 text-xs">{{ openAccordions.includes('spx') ? '▲ Collapse' : '▼ Expand' }}</span>
              </button>
              <div v-if="openAccordions.includes('spx')" class="p-4 bg-white space-y-2 border-t border-slate-200">
                <label class="block font-bold text-slate-700 mb-1">SPX PDF Encryption Template</label>
                <select v-model="editProfileData.spx_template" class="w-full p-2 border border-slate-300 rounded-lg bg-white">
                  <option value="Default SPX Template">Default SPX Template (Password Protected PDF)</option>
                  <option value="Corporate Secure Mail Template">Corporate Secure Mail Template</option>
                  <option value="Disabled">Disabled</option>
                </select>
              </div>
            </div>

            <!-- 16. Data Protection Configuration -->
            <div class="border border-slate-200 rounded-xl overflow-hidden shadow-2xs">
              <button
                type="button"
                @click="toggleAccordion('dlp')"
                class="w-full px-4 py-2.5 bg-[#f8fafc] hover:bg-slate-100 flex items-center justify-between font-bold text-slate-800 cursor-pointer transition-colors"
              >
                <div class="flex items-center gap-2.5">
                  <span class="w-5 h-5 rounded-full bg-slate-200 text-slate-700 text-[11px] flex items-center justify-center font-bold">16</span>
                  <span>Data Protection Configuration</span>
                </div>
                <span class="text-slate-400 text-xs">{{ openAccordions.includes('dlp') ? '▲ Collapse' : '▼ Expand' }}</span>
              </button>
              <div v-if="openAccordions.includes('dlp')" class="p-4 bg-white space-y-2 border-t border-slate-200">
                <div class="space-y-1.5">
                  <div class="flex items-center gap-2">
                    <input id="chk-dlp-cc-m" v-model="editProfileData.dlp_credit_cards" type="checkbox" class="rounded text-[#005299]" />
                    <label for="chk-dlp-cc-m" class="cursor-pointer font-semibold">Inspect &amp; Block Credit Card Numbers (PCI-DSS)</label>
                  </div>
                  <div class="flex items-center gap-2">
                    <input id="chk-dlp-ssn-m" v-model="editProfileData.dlp_ssn" type="checkbox" class="rounded text-[#005299]" />
                    <label for="chk-dlp-ssn-m" class="cursor-pointer font-semibold">Inspect &amp; Block Social Security Numbers (SSN)</label>
                  </div>
                </div>
              </div>
            </div>

            <!-- 17. Header Modifications -->
            <div class="border border-slate-200 rounded-xl overflow-hidden shadow-2xs">
              <button
                type="button"
                @click="toggleAccordion('headers')"
                class="w-full px-4 py-2.5 bg-[#f8fafc] hover:bg-slate-100 flex items-center justify-between font-bold text-slate-800 cursor-pointer transition-colors"
              >
                <div class="flex items-center gap-2.5">
                  <span class="w-5 h-5 rounded-full bg-slate-200 text-slate-700 text-[11px] flex items-center justify-center font-bold">17</span>
                  <span>Header Modifications</span>
                </div>
                <span class="text-slate-400 text-xs">{{ openAccordions.includes('headers') ? '▲ Collapse' : '▼ Expand' }}</span>
              </button>
              <div v-if="openAccordions.includes('headers')" class="p-4 bg-white space-y-2 border-t border-slate-200">
                <textarea v-model="editProfileData.custom_headers" rows="2" class="w-full p-2 border border-slate-300 rounded-lg font-mono" placeholder="X-Astaro-Scanned: true&#10;X-Spam-Status: Clean"></textarea>
              </div>
            </div>

          </div>

          <!-- Comment Field -->
          <div class="pt-2">
            <label class="block font-bold text-slate-700 mb-1">Comment</label>
            <input
              v-model="editProfileData.comment"
              type="text"
              class="w-full p-2.5 border border-slate-300 rounded-lg bg-white"
              placeholder="Optional notes or administrative documentation"
            />
          </div>

        </div>

        <!-- Modal Footer -->
        <div class="px-6 py-4 bg-[#f8fafc] border-t border-slate-200 flex items-center justify-end gap-3">
          <button
            type="button"
            @click="isModalOpen = false"
            class="px-4 py-2 rounded-lg border border-slate-300 bg-white text-slate-700 text-xs font-bold hover:bg-slate-50 cursor-pointer transition-colors"
          >
            Cancel
          </button>
          <button
            type="button"
            @click="saveProfileModal"
            class="px-5 py-2 rounded-lg bg-[#005299] hover:bg-[#003d73] text-white text-xs font-bold shadow-xs cursor-pointer transition-all"
          >
            {{ editingProfileId ? 'Save Changes' : 'Create Profile' }}
          </button>
        </div>
      </div>
    </div>

    <!-- CREATE DKIM KEY MODAL -->
    <div
      v-if="isDkimModalOpen"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-xs p-4"
    >
      <div class="bg-white rounded-2xl shadow-2xl border border-slate-300 max-w-md w-full overflow-hidden">
        <div class="px-5 py-3.5 bg-[#1b232e] text-white flex items-center justify-between border-b-2 border-[#ee7f00]">
          <h3 class="text-sm font-bold uppercase tracking-wider">Generate New DKIM Key Pair</h3>
          <button @click="isDkimModalOpen = false" class="text-slate-400 hover:text-white font-bold cursor-pointer">✕</button>
        </div>

        <div class="p-5 space-y-4 text-xs">
          <div>
            <label class="block font-bold text-slate-700 mb-1">Domain Name</label>
            <input
              v-model="newDkim.domain"
              type="text"
              placeholder="e.g. company.com or sales.company.com"
              class="w-full p-2 border border-slate-300 rounded-lg font-mono focus:border-[#005299] focus:outline-none"
            />
          </div>

          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block font-bold text-slate-700 mb-1">DKIM Selector</label>
              <input
                v-model="newDkim.selector"
                type="text"
                placeholder="astaro"
                class="w-full p-2 border border-slate-300 rounded-lg font-mono focus:border-[#005299] focus:outline-none"
              />
            </div>
            <div>
              <label class="block font-bold text-slate-700 mb-1">Key Size</label>
              <select v-model="newDkim.key_size" class="w-full p-2 border border-slate-300 rounded-lg bg-white font-mono">
                <option :value="2048">2048-bit (Standard)</option>
                <option :value="1024">1024-bit (Legacy)</option>
              </select>
            </div>
          </div>
        </div>

        <div class="p-4 bg-[#f8fafc] border-t border-slate-200 flex items-center justify-end gap-2">
          <button
            type="button"
            @click="isDkimModalOpen = false"
            class="px-3.5 py-1.5 rounded-lg border border-slate-300 bg-white text-slate-700 text-xs font-bold hover:bg-slate-50 cursor-pointer"
          >
            Cancel
          </button>
          <button
            type="button"
            @click="generateDkimKey"
            :disabled="isGeneratingDkim"
            class="inline-flex items-center gap-2 px-4 py-1.5 rounded-lg bg-[#005299] hover:bg-[#003d73] text-white text-xs font-bold shadow-xs cursor-pointer disabled:opacity-50"
          >
            <svg v-if="isGeneratingDkim" class="w-3.5 h-3.5 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            <span>{{ isGeneratingDkim ? 'Generating RSA Key...' : 'Generate Key Pair' }}</span>
          </button>
        </div>
      </div>
    </div>

    <!-- VIEW DNS TXT RECORD MODAL -->
    <div
      v-if="isDnsViewModalOpen"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-xs p-4"
    >
      <div class="bg-white rounded-2xl shadow-2xl border border-slate-300 max-w-xl w-full overflow-hidden">
        <div class="px-5 py-3.5 bg-[#1b232e] text-white flex items-center justify-between border-b-2 border-[#ee7f00]">
          <h3 class="text-sm font-bold uppercase tracking-wider">DNS TXT Record for {{ selectedDkim?.domain }}</h3>
          <button @click="isDnsViewModalOpen = false" class="text-slate-400 hover:text-white font-bold cursor-pointer">✕</button>
        </div>

        <div class="p-5 space-y-4 text-xs">
          <p class="text-slate-600">
            Publish this TXT record with your DNS provider (e.g. Cloudflare, AWS Route53, GoDaddy) to authenticate outgoing emails.
          </p>

          <div class="space-y-3">
            <div>
              <label class="block font-bold text-slate-700 mb-1">Host / Name / Subdomain</label>
              <div class="flex items-center gap-2">
                <input
                  type="text"
                  readonly
                  :value="selectedDkim?.dns_host_name"
                  class="w-full p-2 border border-slate-300 rounded-lg font-mono bg-slate-50 text-slate-900 select-all"
                />
                <button
                  type="button"
                  @click="copyToClipboard(selectedDkim?.dns_host_name, 'host')"
                  class="px-3 py-2 bg-white border border-slate-300 rounded-lg hover:bg-slate-50 font-bold text-slate-700 cursor-pointer"
                >
                  {{ copyStatus === 'host' ? 'Copied!' : 'Copy' }}
                </button>
              </div>
            </div>

            <div>
              <label class="block font-bold text-slate-700 mb-1">Record Type</label>
              <input
                type="text"
                readonly
                value="TXT"
                class="w-24 p-2 border border-slate-300 rounded-lg font-mono bg-slate-50 text-slate-900 font-bold"
              />
            </div>

            <div>
              <label class="block font-bold text-slate-700 mb-1">Record Value / TXT Data</label>
              <textarea
                readonly
                rows="4"
                :value="selectedDkim?.dns_txt_record"
                class="w-full p-2 border border-slate-300 rounded-lg font-mono bg-slate-50 text-slate-900 text-[11px] select-all leading-relaxed"
              ></textarea>
            </div>
          </div>
        </div>

        <div class="p-4 bg-[#f8fafc] border-t border-slate-200 flex items-center justify-between">
          <button
            type="button"
            @click="copyToClipboard(selectedDkim?.dns_txt_record, 'value')"
            class="px-4 py-1.5 rounded-lg bg-[#005299] hover:bg-[#003d73] text-white text-xs font-bold shadow-xs cursor-pointer"
          >
            {{ copyStatus === 'value' ? 'Copied to Clipboard!' : 'Copy Full TXT Value' }}
          </button>
          <button
            type="button"
            @click="isDnsViewModalOpen = false"
            class="px-3.5 py-1.5 rounded-lg border border-slate-300 bg-white text-slate-700 text-xs font-bold hover:bg-slate-50 cursor-pointer"
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

const activeTab = ref('profiles') // 'general' | 'profiles' | 'routing' | 'antispam' | 'advanced' | 'quarantine' | 'spool'
const operationMode = ref('profile') // 'simple' | 'profile'
const smtpProxyEnabled = ref(true)
const isLoading = ref(false)
const isSavingAdvanced = ref(false)
const isGeneratingDkim = ref(false)

const profileSearch = ref('')
const isModalOpen = ref(false)
const editingProfileId = ref(null)
const openAccordions = ref(['routing', 'recipient_verification', 'mta_checks', 'malware', 'antispam'])

const isDkimModalOpen = ref(false)
const isDnsViewModalOpen = ref(false)
const selectedDkim = ref(null)
const copyStatus = ref('')

const smtpProfiles = ref([
  {
    id: 1,
    name: 'Medricnetworks.com',
    domains: ['Medricnetworks.com'],
    target_host: '192.168.1.50',
    target_port: 25,
    recipient_verification: 'Active Directory (LDAP)',
    use_sophos_rbls: true,
    extra_rbls: 'zen.spamhaus.org\nbl.spamcop.net',
    batv: true,
    rdns: true,
    helo: true,
    spf: true,
    greylisting: true,
    malware_engine: 'ClamAV + Avira',
    malware_action: 'Quarantine',
    spam_score: 5.0,
    spam_action: 'Quarantine',
    sender_blacklist: '',
    block_executables: true,
    block_media: false,
    mime_blacklist: '',
    mime_whitelist: '',
    blocked_extensions: '.exe, .scr, .bat, .vbs, .js, .pif',
    blocked_expressions: '',
    append_footer: false,
    footer_text: '',
    spx_template: 'Default SPX Template',
    spx_enabled: true,
    dlp_credit_cards: false,
    dlp_ssn: false,
    custom_headers: '',
    comment: 'Primary production mail profile',
    enabled: true
  },
  {
    id: 2,
    name: 'mail.castletrublue.com',
    domains: ['castletrublue.com'],
    target_host: '192.168.1.60',
    target_port: 25,
    recipient_verification: 'SMTP Callout',
    use_sophos_rbls: true,
    extra_rbls: '',
    batv: true,
    rdns: true,
    helo: true,
    spf: true,
    greylisting: false,
    malware_engine: 'ClamAV Only',
    malware_action: 'Quarantine',
    spam_score: 5.0,
    spam_action: 'Tag [SPAM]',
    sender_blacklist: '',
    block_executables: true,
    block_media: false,
    mime_blacklist: '',
    mime_whitelist: '',
    blocked_extensions: '.exe, .scr, .bat',
    blocked_expressions: '',
    append_footer: false,
    footer_text: '',
    spx_template: 'Disabled',
    spx_enabled: false,
    dlp_credit_cards: false,
    dlp_ssn: false,
    custom_headers: '',
    comment: 'Branch domain profile',
    enabled: true
  },
  {
    id: 3,
    name: 'mail.medric.net',
    domains: ['medric.net'],
    target_host: '192.168.1.70',
    target_port: 25,
    recipient_verification: 'None',
    use_sophos_rbls: true,
    extra_rbls: '',
    batv: true,
    rdns: true,
    helo: true,
    spf: true,
    greylisting: true,
    malware_engine: 'ClamAV + Avira',
    malware_action: 'Quarantine',
    spam_score: 5.0,
    spam_action: 'Quarantine',
    sender_blacklist: '',
    block_executables: true,
    block_media: false,
    mime_blacklist: '',
    mime_whitelist: '',
    blocked_extensions: '.exe, .scr, .bat, .vbs, .js, .pif',
    blocked_expressions: '',
    append_footer: false,
    footer_text: '',
    spx_template: 'Default SPX Template',
    spx_enabled: true,
    dlp_credit_cards: false,
    dlp_ssn: false,
    custom_headers: '',
    comment: 'Corporate root domain',
    enabled: true
  }
])

const editProfileData = ref({
  name: '',
  domains_input: '',
  target_host: '192.168.1.50',
  target_port: 25,
  recipient_verification: 'Active Directory (LDAP)',
  use_sophos_rbls: true,
  extra_rbls: '',
  batv: true,
  rdns: true,
  helo: true,
  spf: true,
  greylisting: true,
  malware_engine: 'ClamAV + Avira',
  malware_action: 'Quarantine',
  spam_score: 5.0,
  spam_action: 'Quarantine',
  sender_blacklist: '',
  block_executables: true,
  block_media: false,
  mime_blacklist: '',
  mime_whitelist: '',
  blocked_extensions: '.exe, .scr, .bat, .vbs, .js, .pif',
  blocked_expressions: '',
  append_footer: false,
  footer_text: '',
  spx_template: 'Default SPX Template',
  spx_enabled: true,
  dlp_credit_cards: false,
  dlp_ssn: false,
  custom_headers: '',
  comment: ''
})

const filteredProfiles = computed(() => {
  if (!profileSearch.value) return smtpProfiles.value
  const q = profileSearch.value.toLowerCase()
  return smtpProfiles.value.filter(p =>
    p.name.toLowerCase().includes(q) ||
    p.domains.some(d => d.toLowerCase().includes(q))
  )
})

const toggleAccordion = (name) => {
  if (openAccordions.value.includes(name)) {
    openAccordions.value = openAccordions.value.filter(a => a !== name)
  } else {
    openAccordions.value.push(name)
  }
}

const openCreateProfileModal = () => {
  editingProfileId.value = null
  editProfileData.value = {
    name: '',
    domains_input: '',
    target_host: '192.168.1.50',
    target_port: 25,
    recipient_verification: 'Active Directory (LDAP)',
    use_sophos_rbls: true,
    extra_rbls: '',
    batv: true,
    rdns: true,
    helo: true,
    spf: true,
    greylisting: true,
    malware_engine: 'ClamAV + Avira',
    malware_action: 'Quarantine',
    spam_score: 5.0,
    spam_action: 'Quarantine',
    sender_blacklist: '',
    block_executables: true,
    block_media: false,
    mime_blacklist: '',
    mime_whitelist: '',
    blocked_extensions: '.exe, .scr, .bat, .vbs, .js, .pif',
    blocked_expressions: '',
    append_footer: false,
    footer_text: '',
    spx_template: 'Default SPX Template',
    spx_enabled: true,
    dlp_credit_cards: false,
    dlp_ssn: false,
    custom_headers: '',
    comment: ''
  }
  isModalOpen.value = true
}

const openEditProfileModal = (prof) => {
  editingProfileId.value = prof.id
  editProfileData.value = {
    ...JSON.parse(JSON.stringify(prof)),
    domains_input: Array.isArray(prof.domains) ? prof.domains.join(', ') : prof.domains
  }
  isModalOpen.value = true
}

const cloneProfile = (prof) => {
  editingProfileId.value = null
  const cloned = JSON.parse(JSON.stringify(prof))
  cloned.name = `${prof.name} (Clone)`
  cloned.domains_input = Array.isArray(prof.domains) ? prof.domains.join(', ') : prof.domains
  editProfileData.value = cloned
  isModalOpen.value = true
}

const saveProfileModal = () => {
  if (!editProfileData.value.name) return
  const doms = editProfileData.value.domains_input
    ? editProfileData.value.domains_input.split(',').map(d => d.trim()).filter(Boolean)
    : []

  const payload = {
    ...JSON.parse(JSON.stringify(editProfileData.value)),
    domains: doms
  }

  if (editingProfileId.value !== null) {
    const existing = smtpProfiles.value.find(p => p.id === editingProfileId.value)
    if (existing) {
      Object.assign(existing, payload)
    }
  } else {
    smtpProfiles.value.push({
      id: smtpProfiles.value.length + 1,
      ...payload,
      enabled: true
    })
  }
  isModalOpen.value = false
}

const deleteProfile = (id) => {
  smtpProfiles.value = smtpProfiles.value.filter(p => p.id !== id)
}

// DKIM & Advanced state
const dkimKeys = ref([
  {
    id: 'dkim-1',
    domain: 'medricnetworks.com',
    selector: 'astaro',
    key_size: 2048,
    dns_host_name: 'astaro._domainkey.medricnetworks.com',
    dns_txt_record: 'v=DKIM1; k=rsa; p=MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA1v7kR9m0QzL3bW1kPq5X9xYzN5v1e7j8R3kP8l0w==',
    enabled: true
  }
])

const newDkim = ref({ domain: '', selector: 'astaro', key_size: 2048 })
const smarthost = ref({ host: 'smtp.sendgrid.net', port: 587, auth: true, username: 'apikey', password: '••••••••••••' })
const spamSettings = ref({ threshold: 5.0, blackhole_threshold: 12.0, greylisting: true, spf: true, dkim: true })
const advancedSettings = ref({
  smtp_hostname: 'mail.medric.net',
  postmaster_address: 'postmaster@medric.net',
  max_message_size_mb: 50,
  max_connections: 100,
  max_connections_per_host: 10,
  max_recipients_per_message: 50,
  tls_required: true,
  tls_cert_name: 'Default Appliance SSL',
  tls_strict_ciphers: true
})
const blockedExtensions = ref('.exe, .scr, .bat, .vbs, .js, .pif, .hta, .cmd')

const quarantineItems = ref([
  { id: 1, time: '14:22:10', sender: 'phish@fake-invoice.com', recipient: 'finance@medricnetworks.com', subject: 'Urgent Wire Transfer Request', reason: 'Spam', score: 9.8 },
  { id: 2, time: '12:05:41', sender: 'promo@freelotto.xyz', recipient: 'admin@medricnetworks.com', subject: 'Claim Your $5,000 Voucher', reason: 'Spam', score: 8.2 },
  { id: 3, time: '09:14:22', sender: 'attacker@bad-domain.ru', recipient: 'it@medricnetworks.com', subject: 'Invoice_Attachment.zip', reason: 'Malware', score: 10.0 }
])

const spoolItems = ref([
  { id: 1, queue_id: '4F89A1201B', sender: 'billing@medricnetworks.com', recipient: 'client@remote-server.org', size: '42.1 KB', status: 'Deferred (Connection timeout)' }
])

const openCreateDkimModal = () => {
  newDkim.value = { domain: '', selector: 'astaro', key_size: 2048 }
  isDkimModalOpen.value = true
}

const generateDkimKey = async () => {
  if (!newDkim.value.domain || !newDkim.value.selector) return
  isGeneratingDkim.value = true
  try {
    const axiosLib = (typeof window !== 'undefined' && window.axios) ? window.axios : null
    if (axiosLib) {
      const res = await axiosLib.post('/api/mail/dkim/generate', newDkim.value)
      if (res.data && res.data.key) {
        dkimKeys.value.push(res.data.key)
      }
    }
    isDkimModalOpen.value = false
  } catch (e) {
    console.error('Failed to generate DKIM key:', e)
  } finally {
    isGeneratingDkim.value = false
  }
}

const deleteDkimKey = async (id) => {
  try {
    const axiosLib = (typeof window !== 'undefined' && window.axios) ? window.axios : null
    if (axiosLib) {
      await axiosLib.delete(`/api/mail/dkim/keys/${id}`)
    }
    dkimKeys.value = dkimKeys.value.filter(d => d.id !== id)
  } catch (e) {
    console.error('Failed to delete DKIM key:', e)
  }
}

const viewDnsRecord = (dkim) => {
  selectedDkim.value = dkim
  copyStatus.value = ''
  isDnsViewModalOpen.value = true
}

const copyToClipboard = (text, type) => {
  if (!text) return
  navigator.clipboard.writeText(text)
  copyStatus.value = type
  setTimeout(() => { copyStatus.value = '' }, 2000)
}

const fetchAdvancedSettings = async () => {
  try {
    const axiosLib = (typeof window !== 'undefined' && window.axios) ? window.axios : null
    if (!axiosLib) return
    const res = await axiosLib.get('/api/mail/advanced')
    if (res.data) advancedSettings.value = res.data
  } catch (e) {
    console.error('Failed to fetch advanced settings:', e)
  }
}

const saveAdvancedSettings = async () => {
  isSavingAdvanced.value = true
  try {
    const axiosLib = (typeof window !== 'undefined' && window.axios) ? window.axios : null
    if (axiosLib) {
      await axiosLib.post('/api/mail/advanced', advancedSettings.value)
    }
  } catch (e) {
    console.error('Failed to save advanced settings:', e)
  } finally {
    setTimeout(() => { isSavingAdvanced.value = false }, 400)
  }
}

const releaseQuarantine = (id) => {
  quarantineItems.value = quarantineItems.value.filter(q => q.id !== id)
}

const deleteQuarantine = (id) => {
  quarantineItems.value = quarantineItems.value.filter(q => q.id !== id)
}

const flushQueue = () => { spoolItems.value = [] }
const retrySpool = (id) => {
  const item = spoolItems.value.find(s => s.id === id)
  if (item) item.status = 'Retrying...'
}
const deleteSpool = (id) => {
  spoolItems.value = spoolItems.value.filter(s => s.id !== id)
}

const fetchQuarantine = (isManual = false) => {
  if (isManual) isLoading.value = true
  setTimeout(() => { isLoading.value = false }, 600)
}

onMounted(() => {
  fetchAdvancedSettings()
})
</script>
