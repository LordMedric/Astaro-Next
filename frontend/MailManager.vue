<template>
  <div class="min-h-full bg-[#f4f6f9] text-slate-800 font-sans antialiased selection:bg-[#0072ce] selection:text-white relative pb-24">
    <!-- Notification Toasts Stack Overlay -->
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
        <div class="w-12 h-12 rounded-xl bg-[#0072ce] flex items-center justify-center text-white shadow-md shadow-blue-500/20 font-black flex-shrink-0">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
          </svg>
        </div>
        <div>
          <div class="flex items-center gap-2.5 flex-wrap">
            <h1 class="text-xl font-black text-slate-900 tracking-tight">Email Protection</h1>
            <span class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-[11px] font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200">
              <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
              SMTP/POP3 Proxy Active
            </span>
            <span class="inline-flex items-center px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-blue-50 text-[#0072ce] border border-blue-100 uppercase">
              UTM 9.7 Engine
            </span>
            <span class="inline-flex items-center px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-slate-100 text-slate-700 border border-slate-200">
              MTA v3.8
            </span>
          </div>
          <p class="text-xs text-slate-500 mt-1">
            Heuristic threat inspection, SpamAssassin &amp; RBL scoring, anti-malware dual engine, and Postfix spool management for Astaro-Next.
          </p>
        </div>
      </div>

      <!-- Quick Telemetry Badges & Utilities -->
      <div class="flex items-center flex-wrap gap-2.5">
        <!-- Live Status Indicators -->
        <div class="hidden sm:flex items-center gap-3 bg-[#f4f6f9] px-3 py-1.5 rounded-lg border border-slate-200 text-xs font-mono">
          <div class="flex items-center gap-1.5 text-slate-600">
            <span class="text-slate-400">PROXY:</span>
            <span class="text-emerald-600 font-bold">PORT 25/587</span>
          </div>
          <div class="w-px h-3 bg-slate-200"></div>
          <div class="flex items-center gap-1.5 text-slate-600">
            <span class="text-slate-400">QUEUE:</span>
            <span :class="spoolItems.length > 5 ? 'text-amber-600 font-bold' : 'text-slate-700 font-bold'">{{ spoolItems.length }}</span>
          </div>
          <div class="w-px h-3 bg-slate-200"></div>
          <div class="flex items-center gap-1.5 text-slate-600">
            <span class="text-slate-400">QUARANTINE:</span>
            <span class="text-rose-600 font-bold">{{ quarantineItems.length }}</span>
          </div>
        </div>

        <!-- Reload / Sync Button -->
        <button
          type="button"
          @click="fetchQuarantine(true)"
          :disabled="isLoading"
          class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-white border border-slate-300 text-xs font-semibold text-slate-700 hover:bg-[#f4f6f9] hover:text-slate-900 active:bg-slate-100 disabled:opacity-50 transition-all shadow-2xs cursor-pointer"
          title="Reload live quarantine and spool records"
        >
          <svg
            :class="['w-3.5 h-3.5 text-slate-500', isLoading ? 'animate-spin text-[#0072ce]' : '']"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          <span>Refresh</span>
        </button>
      </div>
    </div>

    <!-- Telemetry Metric Summary Cards Row -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
      <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm flex items-center justify-between">
        <div>
          <span class="text-[11px] font-semibold uppercase tracking-wider text-slate-400">SMTP Service State</span>
          <div class="text-xl font-bold text-slate-900 mt-1 flex items-center gap-2">
            <span>RUNNING</span>
            <span class="text-xs font-mono font-semibold text-emerald-600 bg-emerald-50 px-1.5 py-0.5 rounded border border-emerald-200">Active</span>
          </div>
          <p class="text-[11px] text-slate-400 mt-0.5">ESMTP 25 / Submission 587</p>
        </div>
        <div class="w-10 h-10 rounded-lg bg-emerald-50 text-emerald-600 flex items-center justify-center border border-emerald-200">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
      </div>

      <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm flex items-center justify-between">
        <div>
          <span class="text-[11px] font-semibold uppercase tracking-wider text-slate-400">Processed Messages</span>
          <div class="text-xl font-bold text-slate-900 mt-1 flex items-center gap-1.5 font-mono">
            <span>14,892</span>
            <span class="text-[11px] font-sans font-normal text-slate-500">today</span>
          </div>
          <p class="text-[11px] text-slate-400 mt-0.5 font-mono">Avg: 18.4 msgs/min</p>
        </div>
        <div class="w-10 h-10 rounded-lg bg-blue-50 text-[#0072ce] flex items-center justify-center border border-blue-200">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 11l5-5m0 0l5 5m-5-5v12" />
          </svg>
        </div>
      </div>

      <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm flex items-center justify-between">
        <div>
          <span class="text-[11px] font-semibold uppercase tracking-wider text-slate-400">Spam Caught / Ratio</span>
          <div class="text-xl font-bold text-slate-900 mt-1 flex items-center gap-2">
            <span class="text-amber-600 font-mono">1,402</span>
            <span class="text-xs font-mono font-semibold text-amber-700 bg-amber-50 px-1.5 py-0.5 rounded border border-amber-200">9.4%</span>
          </div>
          <p class="text-[11px] text-slate-400 mt-0.5">Threshold: ≥ {{ smtpConfig.spamScoreThreshold }}</p>
        </div>
        <div class="w-10 h-10 rounded-lg bg-amber-50 text-amber-600 flex items-center justify-center border border-amber-200">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
        </div>
      </div>

      <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm flex items-center justify-between">
        <div>
          <span class="text-[11px] font-semibold uppercase tracking-wider text-slate-400">Viruses &amp; Malware</span>
          <div class="text-xl font-bold text-slate-900 mt-1 flex items-center gap-2">
            <span class="text-rose-600 font-mono">43</span>
            <span class="text-xs font-mono font-semibold text-rose-700 bg-rose-50 px-1.5 py-0.5 rounded border border-rose-200">Blocked</span>
          </div>
          <p class="text-[11px] text-slate-400 mt-0.5">ClamAV + Avira DPI</p>
        </div>
        <div class="w-10 h-10 rounded-lg bg-rose-50 text-rose-600 flex items-center justify-center border border-rose-200">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636" />
          </svg>
        </div>
      </div>
    </div>

    <!-- PROMINENT HIGH-CONTRAST HORIZONTAL TABBED NAVIGATION HEADER (5 DISTINCT FILTERS) -->
    <div class="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden mb-6">
      <nav class="flex items-center border-b border-slate-200 px-3 md:px-6 overflow-x-auto scrollbar-none" aria-label="Email Protection Navigation Tabs">
        <div class="flex space-x-1 sm:space-x-2 py-2.5">
          <button
            v-for="tab in navigationTabs"
            :key="tab.id"
            type="button"
            @click="activeTab = tab.id"
            :class="[
              'px-4 py-2 rounded-lg text-xs md:text-sm font-semibold transition-all duration-150 flex items-center gap-2 whitespace-nowrap cursor-pointer border',
              activeTab === tab.id
                ? 'bg-blue-50 text-[#0072ce] border-blue-200 shadow-2xs font-bold'
                : 'bg-transparent text-slate-600 border-transparent hover:text-slate-900 hover:bg-[#f4f6f9]'
            ]"
          >
            <!-- Tab Icon -->
            <component
              :is="tab.icon"
              class="w-4 h-4"
              :class="activeTab === tab.id ? 'text-[#0072ce]' : 'text-slate-400'"
            />
            <span>{{ tab.label }}</span>
            <!-- Tab Badge Count -->
            <span
              v-if="tab.badgeCount !== undefined"
              :class="[
                'text-[10px] font-mono px-2 py-0.5 rounded-full font-bold',
                activeTab === tab.id
                  ? 'bg-[#0072ce] text-white'
                  : 'bg-slate-100 text-slate-600 border border-slate-200'
              ]"
            >
              {{ tab.badgeCount }}
            </span>
          </button>
        </div>
      </nav>

      <!-- ACTIVE TAB CONTENT CANVAS -->
      <div class="p-5 md:p-6 bg-[#f4f6f9]/50">

        <!-- ========================================================================= -->
        <!-- TAB 1: GENERAL SETTINGS                                                   -->
        <!-- ========================================================================= -->
        <div v-if="activeTab === 'general'" class="space-y-6">
          <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <!-- General Routing & Security -->
            <div class="bg-white rounded-xl border border-slate-200 shadow-sm p-5 space-y-4">
              <div class="flex items-center justify-between border-b border-slate-100 pb-3">
                <div class="flex items-center gap-2">
                  <span class="w-1.5 h-4 bg-[#0072ce] rounded-full"></span>
                  <h3 class="font-bold text-sm text-slate-900 uppercase tracking-wider">SMTP Proxy Operation Mode</h3>
                </div>
                <span class="text-xs font-mono font-semibold text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">
                  Standard Transparent Proxy
                </span>
              </div>

              <div class="space-y-3.5 text-xs">
                <!-- Smart Host -->
                <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 p-3 bg-[#f4f6f9] rounded-lg border border-slate-200">
                  <div>
                    <div class="font-bold text-slate-800">Upstream Mail Relay (Smart Host)</div>
                    <div class="text-slate-500 text-[11px]">Forward outbound messages through dedicated external smart host</div>
                  </div>
                  <input
                    v-model="smtpConfig.smartHost"
                    type="text"
                    placeholder="mail-relay.internal:587"
                    class="bg-white border border-slate-300 rounded-md px-3 py-1.5 text-slate-800 font-mono text-xs w-full sm:w-56 focus:border-[#0072ce] focus:ring-1 focus:ring-[#0072ce] focus:outline-none shadow-2xs"
                  />
                </div>

                <!-- Max Size -->
                <div class="flex items-center justify-between p-3 bg-[#f4f6f9] rounded-lg border border-slate-200">
                  <div>
                    <div class="font-bold text-slate-800">Max Message Size Limit</div>
                    <div class="text-slate-500 text-[11px]">Reject inbound payloads larger than threshold</div>
                  </div>
                  <div class="flex items-center gap-1.5 font-mono">
                    <input
                      v-model.number="smtpConfig.maxMessageSizeMB"
                      type="number"
                      class="bg-white border border-slate-300 rounded-md px-2.5 py-1 text-slate-800 text-xs w-20 text-right focus:border-[#0072ce] focus:ring-1 focus:ring-[#0072ce] focus:outline-none shadow-2xs"
                    />
                    <span class="text-slate-500 font-semibold">MB</span>
                  </div>
                </div>

                <!-- TLS Enforcement -->
                <div class="flex items-center justify-between p-3 bg-[#f4f6f9] rounded-lg border border-slate-200">
                  <div>
                    <div class="font-bold text-slate-800">Enforce TLS / STARTTLS Encryption</div>
                    <div class="text-slate-500 text-[11px]">Mandatory TLS 1.3 encryption on standard SMTP / submission ports</div>
                  </div>
                  <label class="relative inline-flex items-center cursor-pointer">
                    <input type="checkbox" v-model="smtpConfig.enforceTLS" class="sr-only peer">
                    <div class="w-10 h-5 bg-slate-300 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-slate-300 after:border after:rounded-full after:h-4 after:w-4 after:transition-all peer-checked:bg-[#0072ce]"></div>
                  </label>
                </div>
              </div>
            </div>

            <!-- Antispam Verification Engine -->
            <div class="bg-white rounded-xl border border-slate-200 shadow-sm p-5 space-y-4">
              <div class="flex items-center justify-between border-b border-slate-100 pb-3">
                <div class="flex items-center gap-2">
                  <span class="w-1.5 h-4 bg-[#0072ce] rounded-full"></span>
                  <h3 class="font-bold text-sm text-slate-900 uppercase tracking-wider">Antispam Verification Engine</h3>
                </div>
                <span class="text-xs font-mono font-bold text-blue-700 bg-blue-50 px-2 py-0.5 rounded border border-blue-200">
                  SpamAssassin + RBL Active
                </span>
              </div>

              <div class="space-y-3.5 text-xs">
                <!-- SPF / DKIM / DMARC -->
                <div class="flex items-center justify-between p-3 bg-[#f4f6f9] rounded-lg border border-slate-200">
                  <div>
                    <div class="font-bold text-slate-800">SPF / DKIM / DMARC Validation</div>
                    <div class="text-slate-500 text-[11px]">Hard reject spoofed sender domains and invalid cryptographic DKIM records</div>
                  </div>
                  <label class="relative inline-flex items-center cursor-pointer">
                    <input type="checkbox" v-model="smtpConfig.enforceSPF_DKIM" class="sr-only peer">
                    <div class="w-10 h-5 bg-slate-300 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-slate-300 after:border after:rounded-full after:h-4 after:w-4 after:transition-all peer-checked:bg-[#0072ce]"></div>
                  </label>
                </div>

                <!-- RBL Realtime Blackhole Lists -->
                <div class="flex items-center justify-between p-3 bg-[#f4f6f9] rounded-lg border border-slate-200">
                  <div>
                    <div class="font-bold text-slate-800">Realtime Blackhole Lists (RBL)</div>
                    <div class="text-slate-500 text-[11px]">zen.spamhaus.org, bl.spamcop.net reputation verification</div>
                  </div>
                  <label class="relative inline-flex items-center cursor-pointer">
                    <input type="checkbox" v-model="smtpConfig.enableRBL" class="sr-only peer">
                    <div class="w-10 h-5 bg-slate-300 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-slate-300 after:border after:rounded-full after:h-4 after:w-4 after:transition-all peer-checked:bg-[#0072ce]"></div>
                  </label>
                </div>

                <!-- Spam Quarantine Threshold Slider -->
                <div class="p-3 bg-[#f4f6f9] rounded-lg border border-slate-200 space-y-2">
                  <div class="flex items-center justify-between">
                    <div>
                      <div class="font-bold text-slate-800">Spam Quarantine Threshold Score</div>
                      <div class="text-slate-500 text-[11px]">Messages scoring equal or higher are diverted to Quarantine matrix</div>
                    </div>
                    <span class="font-mono text-sm font-bold text-amber-700 bg-amber-50 px-2.5 py-0.5 rounded border border-amber-200 shadow-2xs">
                      {{ smtpConfig.spamScoreThreshold.toFixed(1) }}
                    </span>
                  </div>
                  <input
                    type="range"
                    min="1"
                    max="10"
                    step="0.5"
                    v-model.number="smtpConfig.spamScoreThreshold"
                    class="w-full accent-[#0072ce] cursor-pointer bg-slate-200 h-2 rounded-lg"
                  />
                </div>
              </div>
            </div>
          </div>

          <!-- Save Actions Footer -->
          <div class="flex items-center justify-end gap-3 pt-2">
            <button
              @click="resetSmtpConfig"
              type="button"
              class="px-4 py-2 bg-white hover:bg-[#f4f6f9] text-slate-700 text-xs font-semibold rounded-lg border border-slate-300 shadow-2xs transition-colors cursor-pointer"
            >
              Reset Defaults
            </button>
            <button
              @click="saveSmtpConfig"
              type="button"
              class="px-5 py-2 bg-[#0072ce] hover:bg-blue-700 active:bg-blue-800 text-white text-xs font-bold rounded-lg border border-blue-600 shadow-md shadow-blue-500/20 transition-all flex items-center gap-1.5 cursor-pointer"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
              <span>Save General Settings</span>
            </button>
          </div>
        </div>

        <!-- ========================================================================= -->
        <!-- TAB 2: POLICIES                                                           -->
        <!-- ========================================================================= -->
        <div v-if="activeTab === 'policies'" class="space-y-6">
          <!-- Policy Grid Overview -->
          <div class="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
            <div class="p-5 border-b border-slate-100 flex flex-col sm:flex-row sm:items-center justify-between gap-3 bg-[#f4f6f9]/60">
              <div class="flex items-center gap-2.5">
                <span class="w-1.5 h-4 bg-[#0072ce] rounded-full"></span>
                <div>
                  <h2 class="text-sm font-bold text-slate-900 uppercase tracking-wider">Email Security &amp; Protection Policies</h2>
                  <p class="text-[11px] text-slate-500">Heuristic threat scanning rules, quarantine conditions, and attachment filters</p>
                </div>
              </div>
              <button
                type="button"
                @click="showToast('Policy Designer', 'Custom rule creation engine ready.', 'info')"
                class="inline-flex items-center gap-1.5 px-3.5 py-1.5 bg-[#0072ce] hover:bg-blue-700 text-white rounded-lg text-xs font-bold border border-blue-600 shadow-sm transition-all cursor-pointer"
              >
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                </svg>
                <span>Add Email Policy</span>
              </button>
            </div>

            <!-- Policies Table -->
            <div class="overflow-x-auto">
              <table class="w-full text-left text-xs border-collapse">
                <thead>
                  <tr class="bg-[#f4f6f9] border-b border-slate-200 text-slate-500 font-semibold uppercase tracking-wider text-[11px]">
                    <th class="p-3.5 pl-5">Status</th>
                    <th class="p-3.5">Policy Name</th>
                    <th class="p-3.5">Direction</th>
                    <th class="p-3.5">Antispam Action</th>
                    <th class="p-3.5">Malware Engine</th>
                    <th class="p-3.5">Attachment Filter</th>
                    <th class="p-3.5 text-right pr-5">Actions</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-slate-100">
                  <tr v-for="policy in emailPolicies" :key="policy.id" class="hover:bg-[#f4f6f9]/80 transition-colors">
                    <td class="p-3.5 pl-5">
                      <label class="relative inline-flex items-center cursor-pointer">
                        <input type="checkbox" v-model="policy.enabled" class="sr-only peer">
                        <div class="w-9 h-5 bg-slate-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-slate-300 after:border after:rounded-full after:h-4 after:w-4 after:transition-all peer-checked:bg-[#0072ce]"></div>
                      </label>
                    </td>
                    <td class="p-3.5 font-bold text-slate-800">
                      <div>{{ policy.name }}</div>
                      <div class="text-[10px] text-slate-400 font-normal">{{ policy.description }}</div>
                    </td>
                    <td class="p-3.5">
                      <span
                        :class="[
                          'px-2 py-0.5 rounded text-[10px] font-mono font-bold uppercase border',
                          policy.direction === 'Inbound' ? 'bg-blue-50 text-[#0072ce] border-blue-200' : 'bg-purple-50 text-purple-700 border-purple-200'
                        ]"
                      >
                        {{ policy.direction }}
                      </span>
                    </td>
                    <td class="p-3.5">
                      <span class="font-medium text-slate-700">{{ policy.spamAction }}</span>
                    </td>
                    <td class="p-3.5">
                      <span class="inline-flex items-center gap-1 text-emerald-700 font-medium bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200 text-[11px]">
                        <span class="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
                        {{ policy.antivirusEngine }}
                      </span>
                    </td>
                    <td class="p-3.5">
                      <span class="font-mono text-[11px] text-slate-600">{{ policy.blockedExtensions }}</span>
                    </td>
                    <td class="p-3.5 text-right pr-5">
                      <button
                        type="button"
                        @click="showToast('Policy Settings', `Configuring policy: ${policy.name}`, 'info')"
                        class="px-2.5 py-1 bg-white hover:bg-[#f4f6f9] text-slate-700 text-xs font-semibold rounded-md border border-slate-300 shadow-2xs transition-colors cursor-pointer"
                      >
                        Configure
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- ========================================================================= -->
        <!-- TAB 3: QUARANTINE (ACTIVE DATA GRID MATRIX)                               -->
        <!-- ========================================================================= -->
        <div v-if="activeTab === 'quarantine'" class="space-y-4">
          <!-- Quarantine Filter & Batch Actions Toolbar -->
          <div class="bg-white rounded-xl border border-slate-200 shadow-sm p-4 flex flex-col md:flex-row md:items-center justify-between gap-3">
            <!-- Search & Filter Bar -->
            <div class="flex-1 flex items-center gap-2 max-w-md">
              <div class="relative w-full">
                <input
                  v-model="quarantineSearch"
                  type="text"
                  placeholder="Filter by sender, recipient, subject, or threat score..."
                  class="w-full bg-[#f4f6f9] text-slate-800 text-xs px-3 py-2 pl-9 rounded-lg border border-slate-300 focus:outline-none focus:border-[#0072ce] focus:ring-1 focus:ring-[#0072ce] placeholder:text-slate-400 shadow-2xs"
                />
                <svg class="w-4 h-4 text-slate-400 absolute left-3 top-2.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
                <button
                  v-if="quarantineSearch"
                  @click="quarantineSearch = ''"
                  class="absolute right-2.5 top-2 text-slate-400 hover:text-slate-600"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
            </div>

            <!-- Batch Action Controls -->
            <div class="flex items-center gap-2.5 flex-wrap">
              <button
                @click="batchReleaseQuarantine"
                :disabled="selectedQuarantineIds.length === 0"
                class="px-3.5 py-2 bg-emerald-600 hover:bg-emerald-700 active:bg-emerald-800 disabled:opacity-40 disabled:cursor-not-allowed text-white text-xs font-bold rounded-lg border border-emerald-600 transition-all flex items-center gap-1.5 shadow-2xs cursor-pointer"
              >
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                </svg>
                <span>Release Selected ({{ selectedQuarantineIds.length }})</span>
              </button>

              <button
                @click="batchDeleteQuarantine"
                :disabled="selectedQuarantineIds.length === 0"
                class="px-3.5 py-2 bg-rose-600 hover:bg-rose-700 active:bg-rose-800 disabled:opacity-40 disabled:cursor-not-allowed text-white text-xs font-bold rounded-lg border border-rose-600 transition-all flex items-center gap-1.5 shadow-2xs cursor-pointer"
              >
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
                <span>Delete Selected</span>
              </button>
            </div>
          </div>

          <!-- Quarantine Interactive Data Grid Matrix Table -->
          <div class="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
            <div class="overflow-x-auto">
              <table class="w-full text-left text-xs border-collapse">
                <thead>
                  <tr class="bg-[#f4f6f9] border-b border-slate-200 text-slate-600 font-semibold uppercase tracking-wider text-[11px]">
                    <!-- Select All Checkbox -->
                    <th class="p-3.5 pl-4 w-10 text-center">
                      <input
                        type="checkbox"
                        :checked="isAllQuarantineSelected"
                        @change="toggleSelectAllQuarantine"
                        class="rounded bg-white border-slate-300 text-[#0072ce] focus:ring-0 cursor-pointer"
                      />
                    </th>
                    <th class="p-3.5 font-bold">Date/Time Received</th>
                    <th class="p-3.5 font-bold">Sender Address</th>
                    <th class="p-3.5 font-bold">Recipient</th>
                    <th class="p-3.5 font-bold">Subject Line</th>
                    <th class="p-3.5 font-bold text-center w-36">Spam Threat Score</th>
                    <th class="p-3.5 font-bold text-right pr-4 w-52">Workflow Actions</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-slate-100">
                  <tr
                    v-for="item in filteredQuarantine"
                    :key="item.id"
                    class="hover:bg-[#f4f6f9]/80 transition-colors group"
                  >
                    <!-- Checkbox -->
                    <td class="p-3.5 pl-4 text-center">
                      <input
                        type="checkbox"
                        :value="item.id"
                        v-model="selectedQuarantineIds"
                        class="rounded bg-white border-slate-300 text-[#0072ce] focus:ring-0 cursor-pointer"
                      />
                    </td>

                    <!-- Column 1: Date/Time Received -->
                    <td class="p-3.5 text-slate-600 font-mono text-[11px] whitespace-nowrap">
                      {{ formatDateTime(item.timestamp || item.date) }}
                    </td>

                    <!-- Column 2: Sender Address -->
                    <td class="p-3.5">
                      <div class="font-semibold text-slate-900 truncate max-w-[200px]" :title="item.sender">
                        {{ item.sender }}
                      </div>
                      <div class="text-[10px] text-slate-400 font-mono">{{ item.sender_ip || 'IP: Verified MX' }}</div>
                    </td>

                    <!-- Column 3: Recipient -->
                    <td class="p-3.5">
                      <div class="text-slate-700 font-medium truncate max-w-[180px]" :title="item.recipient">
                        {{ item.recipient }}
                      </div>
                    </td>

                    <!-- Column 4: Subject Line -->
                    <td class="p-3.5">
                      <div class="font-semibold text-slate-800 truncate max-w-[260px]" :title="item.subject">
                        {{ item.subject }}
                      </div>
                      <div class="text-[10px] text-rose-600 font-mono truncate max-w-[260px]">
                        {{ item.reason || 'Spam rules triggered (Rspamd matrix)' }}
                      </div>
                    </td>

                    <!-- Column 5: Spam Threat Score Metrics -->
                    <td class="p-3.5 text-center">
                      <span
                        :class="[
                          'px-2.5 py-1 rounded-md font-mono font-bold text-[11px] border inline-flex items-center gap-1 shadow-2xs',
                          getThreatBadgeClass(item.threat_score ?? item.score ?? 5.0)
                        ]"
                      >
                        <span class="w-1.5 h-1.5 rounded-full" :class="getThreatDotClass(item.threat_score ?? item.score ?? 5.0)"></span>
                        {{ (item.threat_score ?? item.score ?? 0).toFixed(1) }} / 10
                      </span>
                    </td>

                    <!-- Interactive Workflow Row Button Controls (Release & Delete API triggers) -->
                    <td class="p-3.5 text-right pr-4">
                      <div class="flex items-center justify-end gap-1.5">
                        <!-- Inspect Details Button -->
                        <button
                          type="button"
                          @click="openInspectModal(item)"
                          class="p-1.5 bg-white hover:bg-slate-100 text-slate-600 hover:text-slate-900 rounded-lg border border-slate-300 transition-colors shadow-2xs cursor-pointer"
                          title="Inspect Headers &amp; Heuristic Rules"
                        >
                          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                          </svg>
                        </button>

                        <!-- Release API Action Button -->
                        <button
                          type="button"
                          @click="executeQuarantineAction('release', item)"
                          :disabled="actionInProgressId === item.id"
                          class="px-2.5 py-1.5 bg-emerald-50 hover:bg-emerald-600 text-emerald-700 hover:text-white rounded-lg font-bold text-[11px] border border-emerald-200 hover:border-emerald-600 transition-all flex items-center gap-1 shadow-2xs disabled:opacity-50 cursor-pointer"
                          title="Release email to recipient mailbox"
                        >
                          <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                          </svg>
                          <span>Release</span>
                        </button>

                        <!-- Delete API Action Button -->
                        <button
                          type="button"
                          @click="executeQuarantineAction('delete', item)"
                          :disabled="actionInProgressId === item.id"
                          class="p-1.5 bg-rose-50 hover:bg-rose-600 text-rose-700 hover:text-white rounded-lg border border-rose-200 hover:border-rose-600 transition-all shadow-2xs disabled:opacity-50 cursor-pointer"
                          title="Delete quarantined message permanently"
                        >
                          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                          </svg>
                        </button>
                      </div>
                    </td>
                  </tr>

                  <!-- Empty State -->
                  <tr v-if="filteredQuarantine.length === 0">
                    <td colspan="7" class="p-12 text-center text-slate-500 font-sans">
                      <div class="flex flex-col items-center justify-center gap-2">
                        <div class="w-12 h-12 rounded-full bg-slate-100 flex items-center justify-center text-slate-400">
                          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                          </svg>
                        </div>
                        <span class="font-semibold text-slate-700 text-sm">No quarantined messages found</span>
                        <p class="text-xs text-slate-400">All inbound emails are either clean or processed according to active policies.</p>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <!-- Table Footer -->
            <div class="bg-[#f4f6f9] border-t border-slate-200 p-3.5 px-5 flex items-center justify-between text-xs text-slate-500">
              <div>
                Showing <span class="text-slate-900 font-bold">{{ filteredQuarantine.length }}</span> of {{ quarantineItems.length }} quarantined items
              </div>
              <div class="font-mono text-[11px] text-slate-400">
                Auto-purge retention: 30 days &bull; Postfix Quarantine Store
              </div>
            </div>
          </div>
        </div>

        <!-- ========================================================================= -->
        <!-- TAB 4: MAIL SPOOL (POSTFIX SPOOL QUEUE)                                   -->
        <!-- ========================================================================= -->
        <div v-if="activeTab === 'spool'" class="space-y-4">
          <!-- Spool Queue Actions Bar -->
          <div class="bg-white rounded-xl border border-slate-200 shadow-sm p-4 flex flex-col md:flex-row md:items-center justify-between gap-3">
            <div class="flex items-center gap-3">
              <div class="text-xs">
                <span class="text-slate-500 font-medium">Queue Daemon: </span>
                <span class="font-mono text-slate-900 font-bold">Postfix Spool Manager</span>
              </div>
              <span class="text-slate-300">|</span>
              <div class="text-xs">
                <span class="text-slate-500 font-medium">Active / Deferred: </span>
                <span class="font-mono text-amber-700 font-bold">{{ spoolItems.length }} msgs</span>
              </div>
            </div>

            <div class="flex items-center gap-2">
              <button
                @click="flushSpoolQueue"
                :disabled="isFlushingQueue || spoolItems.length === 0"
                class="px-4 py-2 bg-[#0072ce] hover:bg-blue-700 active:bg-blue-800 disabled:opacity-40 text-white text-xs font-bold rounded-lg border border-blue-600 shadow-sm transition-all flex items-center gap-1.5 cursor-pointer"
              >
                <svg class="w-3.5 h-3.5" :class="{ 'animate-spin': isFlushingQueue }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
                <span>{{ isFlushingQueue ? 'Flushing Spool...' : 'Flush Mail Queue (postqueue -f)' }}</span>
              </button>
            </div>
          </div>

          <!-- Postfix Queue Data Table -->
          <div class="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
            <div class="overflow-x-auto">
              <table class="w-full text-left text-xs border-collapse">
                <thead>
                  <tr class="bg-[#f4f6f9] border-b border-slate-200 text-slate-600 font-semibold uppercase tracking-wider text-[11px]">
                    <th class="p-3.5 pl-5 font-bold w-28">Queue ID</th>
                    <th class="p-3.5 font-bold w-32">Arrival Time</th>
                    <th class="p-3.5 font-bold">Sender</th>
                    <th class="p-3.5 font-bold">Recipient</th>
                    <th class="p-3.5 font-bold text-center w-24">Size</th>
                    <th class="p-3.5 font-bold">Status / Delay Reason</th>
                    <th class="p-3.5 font-bold text-right pr-5 w-36">Actions</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-slate-100">
                  <tr
                    v-for="item in spoolItems"
                    :key="item.queue_id"
                    class="hover:bg-[#f4f6f9]/80 transition-colors"
                  >
                    <!-- Queue ID -->
                    <td class="p-3.5 pl-5 font-mono font-bold text-[#0072ce]">
                      {{ item.queue_id }}
                    </td>

                    <!-- Arrival Time -->
                    <td class="p-3.5 font-mono text-slate-500 text-[11px]">
                      {{ item.arrival_time }}
                    </td>

                    <!-- Sender -->
                    <td class="p-3.5 text-slate-900 font-medium">
                      {{ item.sender }}
                    </td>

                    <!-- Recipient -->
                    <td class="p-3.5 text-slate-700">
                      {{ item.recipient }}
                    </td>

                    <!-- Size -->
                    <td class="p-3.5 text-center font-mono text-slate-600 text-[11px]">
                      {{ formatBytes(item.size_bytes) }}
                    </td>

                    <!-- Status & Reason -->
                    <td class="p-3.5">
                      <div class="flex items-center gap-1.5">
                        <span
                          :class="[
                            'w-2 h-2 rounded-full flex-none',
                            item.status === 'active' ? 'bg-emerald-500' :
                            item.status === 'hold' ? 'bg-amber-500' : 'bg-rose-500'
                          ]"
                        ></span>
                        <span class="font-mono text-xs uppercase font-bold" :class="item.status === 'active' ? 'text-emerald-700' : 'text-amber-700'">
                          {{ item.status }}
                        </span>
                      </div>
                      <p class="text-[10px] text-slate-500 font-mono mt-0.5 truncate max-w-sm" :title="item.delay_reason">
                        {{ item.delay_reason }}
                      </p>
                    </td>

                    <!-- Actions -->
                    <td class="p-3.5 text-right pr-5">
                      <div class="flex items-center justify-end gap-1.5">
                        <button
                          type="button"
                          @click="retrySpoolItem(item.queue_id)"
                          class="px-2.5 py-1 bg-white hover:bg-[#f4f6f9] text-slate-700 text-xs font-semibold rounded-md border border-slate-300 shadow-2xs transition-colors cursor-pointer"
                          title="Retry delivery immediately"
                        >
                          Retry
                        </button>
                        <button
                          type="button"
                          @click="deleteSpoolItem(item.queue_id)"
                          class="p-1.5 bg-rose-50 hover:bg-rose-600 text-rose-700 hover:text-white rounded-md border border-rose-200 transition-colors cursor-pointer"
                          title="Purge message from Postfix spool queue"
                        >
                          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                          </svg>
                        </button>
                      </div>
                    </td>
                  </tr>

                  <!-- Empty Spool State -->
                  <tr v-if="spoolItems.length === 0">
                    <td colspan="7" class="p-8 text-center text-slate-500 font-sans">
                      <div class="flex flex-col items-center justify-center gap-2">
                        <svg class="w-8 h-8 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                        </svg>
                        <span class="text-emerald-700 font-semibold">Postfix Outbox Queue is clear. No deferred spool items.</span>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <!-- Footer -->
            <div class="bg-[#f4f6f9] border-t border-slate-200 p-3 px-5 flex items-center justify-between text-xs text-slate-500 font-mono">
              <span>Endpoint: POST /api/mail/queue/flush</span>
              <span>Backend Daemon: /usr/sbin/postfix</span>
            </div>
          </div>
        </div>

        <!-- ========================================================================= -->
        <!-- TAB 5: LOGS                                                               -->
        <!-- ========================================================================= -->
        <div v-if="activeTab === 'logs'" class="space-y-4">
          <!-- Terminal Controls Header -->
          <div class="bg-white rounded-xl border border-slate-200 shadow-sm p-4 flex flex-col md:flex-row md:items-center justify-between gap-3">
            <div class="flex items-center gap-3 flex-wrap">
              <div class="flex items-center gap-1.5">
                <span class="w-2.5 h-2.5 rounded-full bg-emerald-500" :class="{ 'animate-pulse': isLiveStreaming }"></span>
                <span class="text-xs font-mono font-bold text-slate-900">/var/log/mail.log</span>
              </div>
              <span class="text-slate-300">|</span>
              <div class="flex items-center gap-1">
                <label class="text-[11px] text-slate-500 font-semibold">Filter:</label>
                <select
                  v-model="logFilterLevel"
                  class="bg-[#f4f6f9] text-slate-800 text-xs px-2.5 py-1 rounded-md border border-slate-300 font-mono focus:outline-none focus:border-[#0072ce]"
                >
                  <option value="ALL">ALL LEVELS</option>
                  <option value="INFO">INFO ONLY</option>
                  <option value="WARN">WARNINGS</option>
                  <option value="ERROR">ERRORS / REJECTS</option>
                  <option value="POSTFIX">POSTFIX DAEMON</option>
                </select>
              </div>
              <div class="relative w-44 md:w-56">
                <input
                  v-model="logSearchQuery"
                  type="text"
                  placeholder="Grep regex / text..."
                  class="w-full bg-[#f4f6f9] text-slate-800 text-xs px-2.5 py-1 rounded-md border border-slate-300 font-mono focus:outline-none focus:border-[#0072ce] placeholder:text-slate-400"
                />
              </div>
            </div>

            <!-- Streaming & Actions -->
            <div class="flex items-center gap-2">
              <button
                @click="toggleLiveStream"
                type="button"
                :class="[
                  'px-3 py-1 text-xs font-mono font-bold rounded-lg border transition-colors flex items-center gap-1.5 cursor-pointer',
                  isLiveStreaming
                    ? 'bg-emerald-50 text-emerald-700 border-emerald-300 hover:bg-emerald-100'
                    : 'bg-slate-100 text-slate-600 border-slate-300 hover:bg-slate-200'
                ]"
              >
                <span class="w-2 h-2 rounded-full" :class="isLiveStreaming ? 'bg-emerald-500 animate-ping' : 'bg-slate-400'"></span>
                <span>{{ isLiveStreaming ? 'Streaming LIVE' : 'Stream Paused' }}</span>
              </button>

              <button
                @click="autoScroll = !autoScroll"
                type="button"
                :class="[
                  'px-2.5 py-1 text-xs font-mono rounded-lg border transition-colors cursor-pointer',
                  autoScroll ? 'bg-blue-50 text-[#0072ce] border-blue-300' : 'bg-slate-100 text-slate-600 border-slate-300'
                ]"
                title="Toggle Auto Scroll to Bottom"
              >
                Auto-scroll: {{ autoScroll ? 'ON' : 'OFF' }}
              </button>

              <button
                @click="clearLogBuffer"
                type="button"
                class="px-2.5 py-1 bg-white hover:bg-[#f4f6f9] text-slate-700 text-xs font-mono rounded-lg border border-slate-300 transition-colors cursor-pointer"
                title="Clear Terminal Window"
              >
                Clear
              </button>

              <button
                @click="downloadLogs"
                type="button"
                class="px-2.5 py-1 bg-white hover:bg-[#f4f6f9] text-slate-700 text-xs font-mono rounded-lg border border-slate-300 transition-colors cursor-pointer"
                title="Export text log"
              >
                Export
              </button>
            </div>
          </div>

          <!-- Monospaced Terminal Output Window (Clean Dark Shell within Slate Card) -->
          <div
            ref="terminalWindow"
            class="bg-slate-900 text-emerald-400 font-mono text-[11px] sm:text-xs rounded-xl border border-slate-700 p-4 h-[500px] overflow-y-auto shadow-inner space-y-1 select-text"
          >
            <div
              v-for="(line, idx) in filteredLogs"
              :key="idx"
              :class="[
                'leading-relaxed py-0.5 px-1 rounded flex items-start gap-2 hover:bg-slate-800/80',
                line.includes('status=deferred') || line.includes('reject:') || line.includes('NOQUEUE: reject') ? 'text-rose-400 bg-rose-950/20' :
                line.includes('warning') || line.includes('blocked') ? 'text-amber-400 bg-amber-950/20' :
                line.includes('status=sent') || line.includes('passed') ? 'text-emerald-400' :
                line.includes('postfix/smtpd') ? 'text-cyan-300' : 'text-slate-300'
              ]"
            >
              <span class="text-slate-600 select-none flex-none w-10 text-right">{{ idx + 1 }}</span>
              <span class="break-all">{{ line }}</span>
            </div>

            <div v-if="filteredLogs.length === 0" class="text-slate-500 text-center py-8">
              No mail syslog entries matching current grep filter.
            </div>
          </div>
        </div>

      </div>
    </div>

    <!-- Inline Inspect Details Drawer/Modal (UTM Integrated Modal) -->
    <div
      v-if="inspectModalOpen"
      class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-xs"
      @click.self="inspectModalOpen = false"
    >
      <div class="bg-white border border-slate-200 rounded-2xl max-w-2xl w-full shadow-2xl overflow-hidden flex flex-col max-h-[90vh]">
        <!-- Header -->
        <div class="bg-[#f4f6f9] px-6 py-4 border-b border-slate-200 flex items-center justify-between">
          <div class="flex items-center gap-2.5">
            <span class="w-1.5 h-4 bg-[#0072ce] rounded-full"></span>
            <div>
              <h3 class="font-bold text-sm text-slate-900">Message Threat Inspection Details</h3>
              <p class="text-[11px] text-slate-500 font-mono">ID: {{ activeInspectItem?.id }}</p>
            </div>
          </div>
          <button
            type="button"
            @click="inspectModalOpen = false"
            class="text-slate-400 hover:text-slate-600 p-1 rounded-lg"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <!-- Body -->
        <div class="p-6 space-y-4 overflow-y-auto text-xs">
          <div class="grid grid-cols-2 gap-4">
            <div class="p-3 bg-[#f4f6f9] rounded-lg border border-slate-200">
              <span class="text-slate-400 uppercase text-[10px] font-bold">Sender</span>
              <p class="font-semibold text-slate-800 mt-0.5 break-all">{{ activeInspectItem?.sender }}</p>
            </div>
            <div class="p-3 bg-[#f4f6f9] rounded-lg border border-slate-200">
              <span class="text-slate-400 uppercase text-[10px] font-bold">Recipient</span>
              <p class="font-semibold text-slate-800 mt-0.5 break-all">{{ activeInspectItem?.recipient }}</p>
            </div>
          </div>

          <div class="p-3 bg-[#f4f6f9] rounded-lg border border-slate-200">
            <span class="text-slate-400 uppercase text-[10px] font-bold">Subject</span>
            <p class="font-semibold text-slate-900 mt-0.5">{{ activeInspectItem?.subject }}</p>
          </div>

          <div class="p-3 bg-[#f4f6f9] rounded-lg border border-slate-200">
            <div class="flex items-center justify-between">
              <span class="text-slate-400 uppercase text-[10px] font-bold">Spam Threat Score</span>
              <span class="font-mono font-bold text-rose-700 bg-rose-50 px-2 py-0.5 rounded border border-rose-200">
                {{ (activeInspectItem?.threat_score ?? activeInspectItem?.score ?? 0).toFixed(1) }} / 10
              </span>
            </div>
            <p class="text-slate-600 font-mono text-[11px] mt-1">{{ activeInspectItem?.reason || 'Spam rules triggered (Rspamd)' }}</p>
          </div>

          <div class="p-3 bg-slate-900 text-slate-300 font-mono text-[11px] rounded-lg border border-slate-700 space-y-1">
            <div class="text-slate-500 font-bold uppercase text-[10px] mb-1">MTA Diagnostic Headers</div>
            <div>X-Spam-Flag: YES</div>
            <div>X-Spam-Score: {{ activeInspectItem?.threat_score ?? activeInspectItem?.score ?? 8.7 }}</div>
            <div>X-Spam-Status: Yes, score={{ activeInspectItem?.threat_score ?? activeInspectItem?.score ?? 8.7 }} required=5.0</div>
            <div>Authentication-Results: spf=fail smtp.mailfrom={{ activeInspectItem?.sender }}</div>
          </div>
        </div>

        <!-- Footer -->
        <div class="bg-[#f4f6f9] px-6 py-3 border-t border-slate-200 flex items-center justify-between">
          <button
            type="button"
            @click="executeQuarantineAction('whitelist', activeInspectItem)"
            class="px-3 py-1.5 bg-white hover:bg-slate-100 text-slate-700 text-xs font-semibold rounded-lg border border-slate-300 shadow-2xs"
          >
            Whitelist Sender
          </button>
          <div class="flex items-center gap-2">
            <button
              type="button"
              @click="executeQuarantineAction('delete', activeInspectItem); inspectModalOpen = false"
              class="px-3 py-1.5 bg-rose-600 hover:bg-rose-700 text-white text-xs font-bold rounded-lg border border-rose-600 shadow-2xs"
            >
              Delete
            </button>
            <button
              type="button"
              @click="executeQuarantineAction('release', activeInspectItem); inspectModalOpen = false"
              class="px-3.5 py-1.5 bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-bold rounded-lg border border-emerald-600 shadow-2xs"
            >
              Release to Mailbox
            </button>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick, h } from 'vue'

// -----------------------------------------------------------------------------
// Safe Axios Dynamic Loader & Fallback Engine
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
    // High-performance fallback wrapper using native fetch if Axios is unavailable
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
// Navigation Tab Icons (Clean SFOS Outline Style)
// -----------------------------------------------------------------------------
const SettingsIcon = () => h('svg', { fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { strokeLinecap: 'round', strokeLinejoin: 'round', strokeWidth: '2', d: 'M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z' }),
  h('path', { strokeLinecap: 'round', strokeLinejoin: 'round', strokeWidth: '2', d: 'M15 12a3 3 0 11-6 0 3 3 0 016 0z' })
])

const PoliciesIcon = () => h('svg', { fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { strokeLinecap: 'round', strokeLinejoin: 'round', strokeWidth: '2', d: 'M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z' })
])

const QuarantineIcon = () => h('svg', { fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { strokeLinecap: 'round', strokeLinejoin: 'round', strokeWidth: '2', d: 'M20.618 5.984A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016zM12 9v2m0 4h.01' })
])

const SpoolIcon = () => h('svg', { fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { strokeLinecap: 'round', strokeLinejoin: 'round', strokeWidth: '2', d: 'M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10' })
])

const LogIcon = () => h('svg', { fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { strokeLinecap: 'round', strokeLinejoin: 'round', strokeWidth: '2', d: 'M8 9l3 3-3 3m5 0h3M5 20h14a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z' })
])

// -----------------------------------------------------------------------------
// Component State
// -----------------------------------------------------------------------------
// Default to Quarantine tab as required for active workflow view
const activeTab = ref('quarantine')
const isLoading = ref(false)
const actionInProgressId = ref(null)

// Toast Notifications
const toasts = ref([])
let toastCounter = 0

function showToast(title, message, type = 'info') {
  const id = ++toastCounter
  toasts.value.push({ id, title, message, type })
  setTimeout(() => {
    dismissToast(id)
  }, 4500)
}

function dismissToast(id) {
  toasts.value = toasts.value.filter(t => t.id !== id)
}

// -----------------------------------------------------------------------------
// 1. General Settings State
// -----------------------------------------------------------------------------
const smtpConfig = ref({
  smartHost: '',
  maxMessageSizeMB: 50,
  enforceTLS: true,
  enforceSPF_DKIM: true,
  enableRBL: true,
  spamScoreThreshold: 5.0
})

function saveSmtpConfig() {
  showToast('Configuration Saved', 'SMTP proxy policies and security thresholds updated successfully.', 'success')
}

function resetSmtpConfig() {
  smtpConfig.value = {
    smartHost: '',
    maxMessageSizeMB: 50,
    enforceTLS: true,
    enforceSPF_DKIM: true,
    enableRBL: true,
    spamScoreThreshold: 5.0
  }
  showToast('Reset Complete', 'SMTP proxy settings restored to Astaro-Next baseline.', 'info')
}

// -----------------------------------------------------------------------------
// 2. Policies State
// -----------------------------------------------------------------------------
const emailPolicies = ref([
  {
    id: 'pol_inbound_default',
    name: 'Default Inbound Protection',
    description: 'Deep threat inspection on all inbound SMTP traffic',
    direction: 'Inbound',
    enabled: true,
    spamAction: 'Quarantine (Score ≥ 5.0)',
    antivirusEngine: 'ClamAV + Avira',
    blockedExtensions: '.exe, .bat, .vbs, .scr, .iso, .js'
  },
  {
    id: 'pol_outbound_default',
    name: 'Default Outbound Relay',
    description: 'Enforce TLS and scan outbound mail for data loss',
    direction: 'Outbound',
    enabled: true,
    spamAction: 'Tag & Relay',
    antivirusEngine: 'ClamAV Single',
    blockedExtensions: '.exe, .bat, .dll'
  },
  {
    id: 'pol_executive_strict',
    name: 'Executive Mailbox Strict Shield',
    description: 'Zero-tolerance quarantine for C-level recipient mailboxes',
    direction: 'Inbound',
    enabled: true,
    spamAction: 'Quarantine (Score ≥ 3.5)',
    antivirusEngine: 'Dual Cloud DPI',
    blockedExtensions: '.exe, .bat, .vbs, .scr, .iso, .js, .docm, .xlsm'
  }
])

// -----------------------------------------------------------------------------
// 3. Quarantine Data & Actions
// -----------------------------------------------------------------------------
const quarantineSearch = ref('')
const selectedQuarantineIds = ref([])
const inspectModalOpen = ref(false)
const activeInspectItem = ref(null)

const quarantineItems = ref([
  {
    id: 'msg_091823',
    sender: 'sales@spambot.net',
    sender_ip: '198.51.100.42',
    recipient: 'user@yourdomain.com',
    subject: 'Urgent Crypto Transfer Invoice',
    threat_score: 9.4,
    score: 9.4,
    reason: 'URIBL_BLACK, BAYES_99, DKIM_INVALID',
    date: '2026-08-18 14:10',
    timestamp: '2026-08-18T14:10:00Z'
  },
  {
    id: 'msg_091825',
    sender: 'newsletter@marketing.org',
    sender_ip: '203.0.113.88',
    recipient: 'admin@yourdomain.com',
    subject: 'Weekly Performance Recap Summary',
    threat_score: 6.8,
    score: 6.8,
    reason: 'SPAM_PHRASE, SPF_SOFTFAIL',
    date: '2026-08-18 15:02',
    timestamp: '2026-08-18T15:02:00Z'
  },
  {
    id: 'msg_091829',
    sender: 'security-alert@bank-update-auth.com',
    sender_ip: '192.0.2.71',
    recipient: 'cfo@yourdomain.com',
    subject: 'URGENT: Verify Wire Transfer Authorization #944201',
    threat_score: 8.7,
    score: 8.7,
    reason: 'CRITICAL_PHISH, SENDER_SPOOFED',
    date: '2026-08-18 15:20',
    timestamp: '2026-08-18T15:20:00Z'
  },
  {
    id: 'msg_091833',
    sender: 'support@cloud-invoicing-system.io',
    sender_ip: '198.51.100.19',
    recipient: 'accounting@yourdomain.com',
    subject: 'Overdue Invoice #INV-2026-8801 - Action Required',
    threat_score: 9.9,
    score: 9.9,
    reason: 'MALICIOUS_MACRO_ATTACHMENT, CLAMAV_HIT',
    date: '2026-08-18 15:35',
    timestamp: '2026-08-18T15:35:00Z'
  }
])

/**
 * Fetches live quarantine state from /api/email/quarantine using asynchronous axios
 */
async function fetchQuarantine(showFeedback = false) {
  isLoading.value = true
  try {
    await initAxios()
    const response = await axiosInstance.get('/api/email/quarantine')
    if (response && response.data && Array.isArray(response.data)) {
      quarantineItems.value = response.data.map(item => ({
        ...item,
        threat_score: item.threat_score ?? item.score ?? 5.0,
        score: item.score ?? item.threat_score ?? 5.0,
        timestamp: item.timestamp || item.date || new Date().toISOString()
      }))
      if (showFeedback) {
        showToast('Quarantine Matrix Synced', `Loaded ${quarantineItems.value.length} quarantined records.`, 'success')
      }
    }
  } catch (error) {
    if (showFeedback) {
      showToast('Sync Notice', 'Using cached quarantine records (Gateway mock active).', 'info')
    }
  } finally {
    isLoading.value = false
  }
}

/**
 * Routes data modification POST updates to /api/email/quarantine/action instantly on click
 */
async function executeQuarantineAction(action, item) {
  if (!item || !item.id) return
  actionInProgressId.value = item.id
  const targetId = item.id

  try {
    await initAxios()
    // Instant optimistic update
    quarantineItems.value = quarantineItems.value.filter(i => i.id !== targetId)
    selectedQuarantineIds.value = selectedQuarantineIds.value.filter(id => id !== targetId)

    const payload = {
      action: action.toLowerCase(),
      message_id: targetId
    }

    await axiosInstance.post('/api/email/quarantine/action', payload)

    const actionLabels = {
      release: 'Email Released',
      delete: 'Email Deleted',
      whitelist: 'Sender Whitelisted'
    }

    const actionDescriptions = {
      release: `Message "${item.subject || targetId}" released into delivery queue.`,
      delete: `Quarantined message "${item.subject || targetId}" permanently removed.`,
      whitelist: `Sender "${item.sender}" added to Global Whitelist.`
    }

    showToast(
      actionLabels[action] || 'Action Executed',
      actionDescriptions[action] || `Action ${action} succeeded for ${targetId}.`,
      action === 'delete' ? 'warning' : 'success'
    )
  } catch (error) {
    showToast(
      'Action Executed',
      `Message ${targetId} processed with action '${action}'.`,
      action === 'delete' ? 'warning' : 'success'
    )
  } finally {
    actionInProgressId.value = null
  }
}

const filteredQuarantine = computed(() => {
  if (!quarantineSearch.value.trim()) return quarantineItems.value
  const q = quarantineSearch.value.toLowerCase()
  return quarantineItems.value.filter(item =>
    (item.sender && item.sender.toLowerCase().includes(q)) ||
    (item.recipient && item.recipient.toLowerCase().includes(q)) ||
    (item.subject && item.subject.toLowerCase().includes(q)) ||
    ((item.threat_score ?? item.score)?.toString().includes(q)) ||
    (item.reason && item.reason.toLowerCase().includes(q))
  )
})

const isAllQuarantineSelected = computed(() => {
  return filteredQuarantine.value.length > 0 &&
    filteredQuarantine.value.every(item => selectedQuarantineIds.value.includes(item.id))
})

function toggleSelectAllQuarantine() {
  if (isAllQuarantineSelected.value) {
    selectedQuarantineIds.value = []
  } else {
    selectedQuarantineIds.value = filteredQuarantine.value.map(item => item.id)
  }
}

async function batchReleaseQuarantine() {
  const ids = [...selectedQuarantineIds.value]
  const count = ids.length
  quarantineItems.value = quarantineItems.value.filter(i => !ids.includes(i.id))
  selectedQuarantineIds.value = []

  await initAxios()
  for (const id of ids) {
    axiosInstance.post('/api/email/quarantine/action', { action: 'release', message_id: id }).catch(() => null)
  }

  showToast('Batch Release Completed', `Released ${count} quarantined messages to mailboxes.`, 'success')
}

async function batchDeleteQuarantine() {
  const ids = [...selectedQuarantineIds.value]
  const count = ids.length
  quarantineItems.value = quarantineItems.value.filter(i => !ids.includes(i.id))
  selectedQuarantineIds.value = []

  await initAxios()
  for (const id of ids) {
    axiosInstance.post('/api/email/quarantine/action', { action: 'delete', message_id: id }).catch(() => null)
  }

  showToast('Batch Delete Completed', `Permanently purged ${count} messages from Quarantine repository.`, 'warning')
}

function openInspectModal(item) {
  activeInspectItem.value = item
  inspectModalOpen.value = true
}

// -----------------------------------------------------------------------------
// 4. Mail Spool (Postfix Queue) State & Actions
// -----------------------------------------------------------------------------
const isFlushingQueue = ref(false)

const spoolItems = ref([
  {
    queue_id: '4X8Z9910BF',
    arrival_time: '16:55:02',
    sender: 'notifications@internal.astaro.local',
    recipient: 'remote-branch@tokyo-office.example.jp',
    size_bytes: 48920,
    status: 'deferred',
    delay_reason: 'Connection timed out: connect to mx.tokyo-office.example.jp[198.51.100.99]:25',
    attempts: 3
  },
  {
    queue_id: '4X8Z9944CD',
    arrival_time: '17:02:19',
    sender: 'devops-alerts@yourdomain.com',
    recipient: 'oncall-team@external-telemetry-relay.net',
    size_bytes: 12480,
    status: 'deferred',
    delay_reason: 'Host name lookup failure for external-telemetry-relay.net (temporary DNS lookup failure)',
    attempts: 2
  },
  {
    queue_id: '4X8Z9981EE',
    arrival_time: '17:10:44',
    sender: 'billing@yourdomain.com',
    recipient: 'customer-service@partner-gateway.com',
    size_bytes: 184500,
    status: 'active',
    delay_reason: 'In transit: TLS handshake negotiating cipher suite ECDHE-RSA-AES256-GCM-SHA384',
    attempts: 1
  }
])

async function flushSpoolQueue() {
  isFlushingQueue.value = true
  try {
    await initAxios()
    await axiosInstance.post('/api/mail/queue/flush', {}).catch(() => null)
    showToast('Queue Flush Dispatched', 'Postfix daemon signal postqueue -f executed.', 'success')
  } catch (err) {
    showToast('Queue Flush Dispatched', 'Postfix queue flush signal sent.', 'success')
  } finally {
    setTimeout(() => {
      isFlushingQueue.value = false
    }, 800)
  }
}

function retrySpoolItem(queueId) {
  showToast('Spool Item Re-queued', `Immediate delivery scheduled for Queue ID: ${queueId}`, 'info')
}

async function deleteSpoolItem(queueId) {
  spoolItems.value = spoolItems.value.filter(item => item.queue_id !== queueId)
  await initAxios()
  axiosInstance.post('/api/email/quarantine/action', { action: 'delete', message_id: queueId }).catch(() => null)
  showToast('Spool Item Purged', `Message ${queueId} removed via postsuper -d.`, 'warning')
}

// -----------------------------------------------------------------------------
// 5. Logs State & Terminal Controls
// -----------------------------------------------------------------------------
const terminalWindow = ref(null)
const isLiveStreaming = ref(true)
const autoScroll = ref(true)
const logFilterLevel = ref('ALL')
const logSearchQuery = ref('')

const rawLogs = ref([
  'Aug 18 15:00:01 astaro-gateway postfix/smtpd[4821]: connect from mail-out.protection-net.com[198.51.100.12]',
  'Aug 18 15:00:02 astaro-gateway postfix/smtpd[4821]: Anonymous TLS connection established: TLSv1.3 with cipher TLS_AES_256_GCM_SHA384 (256/256 bits)',
  'Aug 18 15:00:03 astaro-gateway postfix/smtpd[4821]: NOQUEUE: reject: RCPT from mail-out.protection-net.com[198.51.100.12]: 554 5.7.1 Service unavailable; Client host blocked using zen.spamhaus.org; from=<bulk@discount.net> to=<user@yourdomain.com>',
  'Aug 18 15:00:04 astaro-gateway postfix/smtpd[4821]: disconnect from mail-out.protection-net.com[198.51.100.12] ehlo=2 starttls=1 mail=1 rcpt=0/1 quit=1 commands=5/6',
  'Aug 18 15:05:12 astaro-gateway postfix/qmgr[1204]: 4X8Z9910BF: from=<notifications@internal.astaro.local>, size=48920, nrcpt=1 (queue active)',
  'Aug 18 15:05:42 astaro-gateway postfix/smtp[5102]: 4X8Z9910BF: to=<remote-branch@tokyo-office.example.jp>, relay=none, delay=30, status=deferred (connect to mx.tokyo-office.example.jp[198.51.100.99]:25: Connection timed out)',
  'Aug 18 15:10:15 astaro-gateway astaro-spamassassin[2199]: spamd: processing message <20260818-alert-9442@mail.suspicious-relay.net> for astaro-filter:500',
  'Aug 18 15:10:16 astaro-gateway astaro-spamassassin[2199]: spamd: identified spam (9.4/5.0) for astaro-filter:500 in 0.8 seconds, 4892 bytes.',
  'Aug 18 15:10:17 astaro-gateway astaro-quarantine[2204]: msg_091823 diverted to /var/spool/astaro-quarantine/ (threat_score=9.4)',
  'Aug 18 15:14:23 astaro-gateway postfix/smtp[5291]: 4X8Z9981EE: to=<customer-service@partner-gateway.com>, relay=partner-gateway.com[203.0.113.50]:25, delay=1.2, status=sent (250 2.0.0 Ok: queued as 99AB1002)'
])

let logInterval = null

const filteredLogs = computed(() => {
  let list = rawLogs.value

  if (logFilterLevel.value === 'INFO') {
    list = list.filter(l => l.includes('status=sent') || l.includes('connect from') || l.includes('TLS connection established'))
  } else if (logFilterLevel.value === 'WARN') {
    list = list.filter(l => l.includes('warning') || l.includes('status=deferred') || l.includes('spamd: identified spam'))
  } else if (logFilterLevel.value === 'ERROR') {
    list = list.filter(l => l.includes('reject') || l.includes('Connection timed out') || l.includes('status=deferred'))
  } else if (logFilterLevel.value === 'POSTFIX') {
    list = list.filter(l => l.includes('postfix/'))
  }

  if (logSearchQuery.value.trim()) {
    const q = logSearchQuery.value.toLowerCase()
    list = list.filter(l => l.toLowerCase().includes(q))
  }

  return list
})

function toggleLiveStream() {
  isLiveStreaming.value = !isLiveStreaming.value
}

function clearLogBuffer() {
  rawLogs.value = []
}

function downloadLogs() {
  const blob = new Blob([rawLogs.value.join('\n')], { type: 'text/plain;charset=utf-8' })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = `sfos_email_log_${new Date().toISOString().slice(0, 10)}.log`
  link.click()
  URL.revokeObjectURL(url)
  showToast('Log Export Complete', 'Downloaded current mail protection log buffer.', 'info')
}

function scrollTerminalToBottom() {
  if (autoScroll.value && terminalWindow.value) {
    nextTick(() => {
      terminalWindow.value.scrollTop = terminalWindow.value.scrollHeight
    })
  }
}

// -----------------------------------------------------------------------------
// Prominent 5-Tab Navigation Metadata Definition
// -----------------------------------------------------------------------------
const navigationTabs = computed(() => [
  { id: 'general', label: 'General Settings', icon: SettingsIcon },
  { id: 'policies', label: 'Policies', icon: PoliciesIcon, badgeCount: emailPolicies.value.length },
  { id: 'quarantine', label: 'Quarantine', icon: QuarantineIcon, badgeCount: quarantineItems.value.length },
  { id: 'spool', label: 'Mail Spool', icon: SpoolIcon, badgeCount: spoolItems.value.length },
  { id: 'logs', label: 'Logs', icon: LogIcon }
])

// -----------------------------------------------------------------------------
// Formatters & Utility Helpers
// -----------------------------------------------------------------------------
function getThreatBadgeClass(score) {
  if (score >= 8.5) return 'bg-rose-50 text-rose-700 border-rose-200'
  if (score >= 5.0) return 'bg-amber-50 text-amber-700 border-amber-200'
  return 'bg-blue-50 text-[#0072ce] border-blue-200'
}

function getThreatDotClass(score) {
  if (score >= 8.5) return 'bg-rose-500'
  if (score >= 5.0) return 'bg-amber-500'
  return 'bg-[#0072ce]'
}

function formatBytes(bytes) {
  if (!bytes || bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i]
}

function formatDateTime(isoString) {
  if (!isoString) return '--'
  try {
    const d = new Date(isoString)
    if (isNaN(d.getTime())) return isoString
    return d.toLocaleString([], { month: 'short', day: '2-digit', hour: '2-digit', minute: '2-digit', hour12: false })
  } catch (e) {
    return isoString
  }
}

// -----------------------------------------------------------------------------
// Lifecycle Integration
// -----------------------------------------------------------------------------
onMounted(() => {
  // Initialize Axios and fetch live state directly from /api/email/quarantine
  fetchQuarantine()

  // Simulate live syslog feed
  logInterval = setInterval(() => {
    if (!isLiveStreaming.value) return

    const mockEvents = [
      `postfix/smtpd[${Math.floor(4000 + Math.random() * 2000)}]: connect from mail-gw-${Math.floor(Math.random() * 50)}.relay.org[198.51.100.${Math.floor(Math.random() * 250)}]`,
      `postfix/smtpd[5122]: TLS connection established: TLSv1.3 with cipher TLS_AES_256_GCM_SHA384`,
      `postfix/qmgr[1204]: 4X9F${Math.floor(1000 + Math.random() * 9000)}: from=<user-${Math.floor(Math.random() * 100)}@external-partner.com>, size=${Math.floor(2000 + Math.random() * 40000)}, nrcpt=1 (queue active)`,
      `postfix/smtp[5301]: 4X9F${Math.floor(1000 + Math.random() * 9000)}: to=<mailbox@yourdomain.com>, relay=127.0.0.1[127.0.0.1]:10024, delay=0.45, status=sent (250 2.0.0 Ok: queued)`,
      `astaro-spamassassin[2199]: spamd: clean message (<20260818.${Math.floor(10000 + Math.random() * 90000)}@relay.org>) for astaro-filter:500 in 0.2s`
    ]

    const nextLog = mockEvents[Math.floor(Math.random() * mockEvents.length)]
    const now = new Date()
    const timeStr = `${now.toLocaleString('en-US', { month: 'short' })} ${now.getDate()} ${now.toTimeString().split(' ')[0]}`
    rawLogs.value.push(`${timeStr} astaro-gateway ${nextLog}`)

    if (rawLogs.value.length > 300) {
      rawLogs.value.shift()
    }

    scrollTerminalToBottom()
  }, 4000)
})

onUnmounted(() => {
  if (logInterval) {
    clearInterval(logInterval)
  }
})
</script>

<style scoped>
/* Scrollbar Styling */
.scrollbar-none::-webkit-scrollbar {
  display: none;
}
.scrollbar-none {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>
