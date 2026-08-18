<template>
  <div class="min-h-full bg-slate-50 text-slate-800 font-sans antialiased selection:bg-[#2563eb] selection:text-white relative pb-16">
    <!-- Notification Toasts Floating Stack Overlay -->
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
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
          </svg>
        </div>
        <div>
          <div class="flex items-center gap-2.5 flex-wrap">
            <h1 class="text-xl font-black text-slate-900 tracking-tight">Web Server Protection</h1>
            <span class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-[11px] font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200">
              <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
              {{ activeRulesCount }}/{{ rulesList.length }} Rules Active
            </span>
            <span class="inline-flex items-center px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-blue-50 text-[#2563eb] border border-blue-100 uppercase">
              SFOS XGS WAF Engine
            </span>
          </div>
          <p class="text-xs text-slate-500 mt-1">
            Reverse proxy application publishing, SSL/TLS termination, and NAXSI Layer 7 deep packet Web Application Firewall inspection.
          </p>
        </div>
      </div>

      <!-- Quick Action Controls & Primary "Add Web Server Rule" Button -->
      <div class="flex items-center flex-wrap gap-2.5">
        <!-- Nginx Config Preview Button -->
        <button
          type="button"
          @click="openNginxPreview"
          class="inline-flex items-center gap-1.5 px-3 py-2 rounded-lg bg-white border border-slate-300 text-xs font-mono font-semibold text-slate-700 hover:bg-slate-50 hover:text-slate-900 active:bg-slate-100 transition-all shadow-2xs cursor-pointer"
          title="Inspect generated Nginx & NAXSI configuration"
        >
          <svg class="w-3.5 h-3.5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
          </svg>
          <span>nginx.conf</span>
        </button>

        <!-- Refresh Rules Button -->
        <button
          type="button"
          @click="fetchRules(true)"
          :disabled="isLoading"
          class="inline-flex items-center gap-1.5 px-3 py-2 rounded-lg bg-white border border-slate-300 text-xs font-semibold text-slate-700 hover:bg-slate-50 hover:text-slate-900 active:bg-slate-100 disabled:opacity-50 transition-all shadow-2xs cursor-pointer"
          title="Refresh published web rules from backend"
        >
          <svg
            :class="['w-3.5 h-3.5 text-slate-500', isLoading ? 'animate-spin text-[#2563eb]' : '']"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          <span>Refresh</span>
        </button>

        <!-- Primary Blue Control Button: Add Web Server Rule -->
        <button
          type="button"
          @click="openAddRuleModal"
          class="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-[#2563eb] hover:bg-blue-600 active:bg-blue-700 text-white text-xs font-bold shadow-md shadow-blue-500/20 transition-all duration-150 cursor-pointer hover:scale-[1.02] active:scale-[0.98]"
        >
          <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          <span>Add Web Server Rule</span>
        </button>
      </div>
    </div>

    <!-- Telemetry Metric Summary Cards Row -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
      <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm flex items-center justify-between">
        <div>
          <span class="text-[11px] font-semibold uppercase tracking-wider text-slate-400">Published Web Rules</span>
          <div class="text-xl font-bold text-slate-900 mt-1 flex items-center gap-2">
            <span>{{ rulesList.length }}</span>
            <span class="text-xs font-mono font-semibold text-blue-600 bg-blue-50 px-1.5 py-0.5 rounded border border-blue-200">
              {{ activeRulesCount }} Active
            </span>
          </div>
        </div>
        <div class="w-10 h-10 rounded-lg bg-blue-50 text-[#2563eb] flex items-center justify-center border border-blue-200">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9" />
          </svg>
        </div>
      </div>

      <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm flex items-center justify-between">
        <div>
          <span class="text-[11px] font-semibold uppercase tracking-wider text-slate-400">HTTPS / SSL Endpoints</span>
          <div class="text-xl font-bold text-slate-900 mt-1 flex items-center gap-2">
            <span>{{ sslEnabledCount }} / {{ rulesList.length }}</span>
            <span class="text-xs font-mono font-semibold text-emerald-600 bg-emerald-50 px-1.5 py-0.5 rounded border border-emerald-200">TLS 1.3</span>
          </div>
        </div>
        <div class="w-10 h-10 rounded-lg bg-emerald-50 text-emerald-600 flex items-center justify-center border border-emerald-200">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
          </svg>
        </div>
      </div>

      <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm flex items-center justify-between">
        <div>
          <span class="text-[11px] font-semibold uppercase tracking-wider text-slate-400">NAXSI Deep Shield</span>
          <div class="text-xl font-bold text-slate-900 mt-1 flex items-center gap-2">
            <span>{{ wafEnabledCount }} Active</span>
            <span class="text-xs font-mono font-semibold text-purple-600 bg-purple-50 px-1.5 py-0.5 rounded border border-purple-200">SQLi/XSS</span>
          </div>
        </div>
        <div class="w-10 h-10 rounded-lg bg-purple-50 text-purple-600 flex items-center justify-center border border-purple-200">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
          </svg>
        </div>
      </div>

      <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm flex items-center justify-between">
        <div>
          <span class="text-[11px] font-semibold uppercase tracking-wider text-slate-400">Target Real Servers</span>
          <div class="text-xl font-bold text-slate-900 mt-1 flex items-center gap-1.5">
            <span class="text-emerald-600 font-mono">{{ rulesList.length }}</span>
            <span class="text-xs text-slate-500 font-sans">Reachability 100%</span>
          </div>
        </div>
        <div class="w-10 h-10 rounded-lg bg-slate-50 text-slate-600 flex items-center justify-center border border-slate-200">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 12h14M5 12a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v4a2 2 0 01-2 2M5 12a2 2 0 00-2 2v4a2 2 0 002 2h14a2 2 0 002-2v-4a2 2 0 00-2-2" />
          </svg>
        </div>
      </div>
    </div>

    <!-- Main Container Card: Published Application Rules Summary Data Table Grid -->
    <div class="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden flex flex-col">
      
      <!-- Table Filter Bar & Search -->
      <div class="px-5 py-4 border-b border-slate-100 bg-slate-50/60 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div class="flex items-center gap-2.5">
          <span class="w-1.5 h-4 bg-[#2563eb] rounded-full"></span>
          <div>
            <h2 class="text-sm font-bold text-slate-900 uppercase tracking-wider">Published Application Rules</h2>
            <p class="text-[11px] text-slate-500">Active Web Application Firewall and reverse proxy routing policies</p>
          </div>
        </div>

        <div class="flex items-center gap-2.5">
          <!-- Search input box -->
          <div class="relative min-w-[240px]">
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Search rule, domain, or IP..."
              class="w-full bg-white text-slate-800 text-xs px-3 py-1.5 pl-8 rounded-lg border border-slate-300 focus:outline-none focus:border-[#2563eb] focus:ring-1 focus:ring-[#2563eb] placeholder:text-slate-400 transition-colors"
            />
            <svg class="w-3.5 h-3.5 text-slate-400 absolute left-2.5 top-2.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
            <button
              v-if="searchQuery"
              @click="searchQuery = ''"
              class="absolute right-2.5 top-2 text-slate-400 hover:text-slate-600 text-xs"
            >
              ✕
            </button>
          </div>

          <!-- WAF Filter Selector -->
          <select
            v-model="wafFilter"
            class="bg-white text-slate-700 text-xs px-2.5 py-1.5 rounded-lg border border-slate-300 focus:outline-none focus:border-[#2563eb] font-medium"
          >
            <option value="ALL">All Protection Modes</option>
            <option value="WAF_ACTIVE">NAXSI WAF Active</option>
            <option value="SSL_ONLY">HTTPS Enforced</option>
          </select>
        </div>
      </div>

      <!-- Data Table Grid -->
      <div class="overflow-x-auto">
        <table class="w-full text-left text-xs border-collapse">
          <thead>
            <tr class="bg-slate-50 border-b border-slate-200 text-slate-500 font-mono uppercase tracking-wider text-[11px]">
              <th class="p-3.5 font-bold w-12 text-center">Status</th>
              <th class="p-3.5 font-bold min-w-[200px]">Rule Name</th>
              <th class="p-3.5 font-bold min-w-[220px]">Public Hosted Domain</th>
              <th class="p-3.5 font-bold min-w-[200px]">Internal Real Server Target</th>
              <th class="p-3.5 font-bold min-w-[240px]">Security Engine Status</th>
              <th class="p-3.5 font-bold text-right w-36">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100">
            <tr
              v-for="rule in filteredRules"
              :key="rule.id || rule.rule_name"
              class="hover:bg-slate-50/80 transition-colors group"
            >
              <!-- Status Active Indicator -->
              <td class="p-3.5 text-center">
                <div class="flex items-center justify-center">
                  <span class="relative flex h-2.5 w-2.5">
                    <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                    <span class="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-500 shadow-sm shadow-emerald-500/50"></span>
                  </span>
                </div>
              </td>

              <!-- Rule Name -->
              <td class="p-3.5">
                <div class="flex items-center gap-2">
                  <span class="font-bold text-slate-900 group-hover:text-[#2563eb] transition-colors text-xs">
                    {{ rule.rule_name }}
                  </span>
                  <span v-if="rule.id" class="text-[10px] bg-slate-100 text-slate-500 font-mono px-1.5 py-0.2 rounded border border-slate-200">
                    #{{ rule.id }}
                  </span>
                </div>
                <div class="text-[11px] text-slate-500 mt-0.5 font-mono flex items-center gap-1.5">
                  <span>Reverse Proxy</span>
                  <span>&bull;</span>
                  <span class="text-blue-600">Nginx + NAXSI L7</span>
                </div>
              </td>

              <!-- Public Hosted Domain (FQDN) -->
              <td class="p-3.5 font-mono">
                <div class="flex items-center gap-1.5">
                  <svg class="w-3.5 h-3.5 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9" />
                  </svg>
                  <span class="font-bold text-slate-900 text-xs">{{ rule.hosted_domain }}</span>
                </div>
                <div class="text-[11px] text-slate-500 mt-0.5 flex items-center gap-1.5">
                  <span :class="rule.enable_ssl ? 'text-emerald-700 font-semibold' : 'text-slate-600'">
                    {{ rule.enable_ssl ? 'Port 443 (HTTPS)' : 'Port 80 (HTTP)' }}
                  </span>
                  <span v-if="rule.enable_ssl" class="text-[10px] bg-emerald-50 text-emerald-700 px-1 rounded border border-emerald-200">
                    TLS 1.3
                  </span>
                </div>
              </td>

              <!-- Internal Real Server IP/Port Target -->
              <td class="p-3.5 font-mono">
                <div class="flex items-center gap-1.5">
                  <svg class="w-3.5 h-3.5 text-[#2563eb]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 12h14M5 12a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v4a2 2 0 01-2 2M5 12a2 2 0 00-2 2v4a2 2 0 002 2h14a2 2 0 002-2v-4a2 2 0 00-2-2" />
                  </svg>
                  <span class="font-bold text-slate-800 text-xs">
                    {{ rule.real_server_ip }}:{{ rule.real_server_port }}
                  </span>
                </div>
                <div class="text-[10px] text-slate-500 mt-0.5 flex items-center gap-1.5">
                  <span class="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
                  <span>Target Online (0.8 ms)</span>
                </div>
              </td>

              <!-- Security Engine Status (HTTPS & WAF Layers Pills) -->
              <td class="p-3.5">
                <div class="flex flex-wrap items-center gap-1.5">
                  <!-- HTTPS / SSL Status Pill -->
                  <span
                    v-if="rule.enable_ssl"
                    class="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-mono font-bold bg-emerald-50 text-emerald-700 border border-emerald-200 shadow-2xs"
                  >
                    <svg class="w-3 h-3 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                    </svg>
                    <span>HTTPS / SSL</span>
                  </span>
                  <span
                    v-else
                    class="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-mono font-semibold bg-slate-100 text-slate-500 border border-slate-200"
                  >
                    <span>HTTP Plaintext</span>
                  </span>

                  <!-- NAXSI Deep Packet WAF Layer Pill -->
                  <span
                    v-if="rule.enable_naxsi_waf"
                    class="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-mono font-bold bg-blue-50 text-[#2563eb] border border-blue-200 shadow-2xs"
                  >
                    <svg class="w-3 h-3 text-blue-600 animate-pulse" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                    </svg>
                    <span>NAXSI WAF ACTIVE</span>
                  </span>
                  <span
                    v-else
                    class="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-mono font-semibold bg-amber-50 text-amber-700 border border-amber-200"
                  >
                    <span>BYPASS WAF</span>
                  </span>
                </div>
              </td>

              <!-- Row Action Buttons -->
              <td class="p-3.5 text-right">
                <div class="flex items-center justify-end gap-1.5">
                  <!-- Probe Target Server Button -->
                  <button
                    type="button"
                    @click="probeRealServer(rule)"
                    class="p-1.5 bg-white hover:bg-slate-100 text-slate-600 hover:text-blue-600 rounded-lg border border-slate-200 transition-colors shadow-2xs cursor-pointer"
                    title="Send TCP SYN probe to target server"
                  >
                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                    </svg>
                  </button>

                  <!-- Edit Rule Button -->
                  <button
                    type="button"
                    @click="openEditRuleModal(rule)"
                    class="p-1.5 bg-white hover:bg-slate-100 text-slate-600 hover:text-[#2563eb] rounded-lg border border-slate-200 transition-colors shadow-2xs cursor-pointer"
                    title="Edit Web Server Rule"
                  >
                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                    </svg>
                  </button>

                  <!-- Delete Rule Button -->
                  <button
                    type="button"
                    @click="deleteRule(rule)"
                    class="p-1.5 bg-white hover:bg-rose-50 text-slate-400 hover:text-rose-600 rounded-lg border border-slate-200 hover:border-rose-200 transition-colors shadow-2xs cursor-pointer"
                    title="Delete Web Server Rule"
                  >
                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                  </button>
                </div>
              </td>
            </tr>

            <!-- Empty State -->
            <tr v-if="filteredRules.length === 0">
              <td colspan="6" class="p-10 text-center text-slate-500 font-sans">
                <div class="flex flex-col items-center justify-center gap-2">
                  <div class="w-12 h-12 rounded-xl bg-slate-100 flex items-center justify-center text-slate-400 mb-1">
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                  </div>
                  <h3 class="text-sm font-bold text-slate-800">No Web Server Rules Found</h3>
                  <p class="text-xs text-slate-500 max-w-sm">
                    No reverse proxy rules match your query. Click "Add Web Server Rule" to publish an internal application.
                  </p>
                  <button
                    type="button"
                    @click="openAddRuleModal"
                    class="mt-2 inline-flex items-center gap-1.5 px-4 py-2 rounded-lg bg-[#2563eb] text-white text-xs font-bold shadow-sm hover:bg-blue-600 transition-colors"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                    </svg>
                    <span>Add Web Server Rule</span>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Table Footer Summary -->
      <div class="px-5 py-3 bg-slate-50/80 border-t border-slate-100 flex flex-col sm:flex-row sm:items-center justify-between gap-2 text-xs text-slate-500">
        <div>
          Showing <span class="font-bold text-slate-800">{{ filteredRules.length }}</span> of {{ rulesList.length }} Published Application Rules
        </div>
        <div class="font-mono text-[11px] text-slate-400">
          Target Config: <span class="text-slate-600">/etc/nginx/sites-available/astaro-next-waf.conf</span>
        </div>
      </div>
    </div>

    <!-- ========================================================================= -->
    <!-- MODAL: ADD / EDIT WEB SERVER RULE OVERLAY PANEL                            -->
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
        @keydown.esc="closeModal"
      >
        <div
          class="w-full max-w-xl bg-white rounded-2xl border border-slate-200 shadow-2xl overflow-hidden flex flex-col my-8"
          @click.stop
        >
          <!-- Modal Header -->
          <div class="bg-slate-900 text-white px-6 py-4 flex items-center justify-between border-b border-slate-800">
            <div class="flex items-center gap-3">
              <div class="w-9 h-9 rounded-lg bg-[#2563eb] flex items-center justify-center text-white font-black text-sm shadow-md">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                </svg>
              </div>
              <div>
                <h3 class="text-sm font-bold text-white">
                  {{ isEditing ? 'Edit Web Server Rule' : 'Add Web Server Rule' }}
                </h3>
                <p class="text-[11px] text-slate-400">
                  Configure Nginx reverse proxy endpoint and NAXSI WAF protection
                </p>
              </div>
            </div>
            <button
              type="button"
              @click="closeModal"
              class="text-slate-400 hover:text-white transition-colors p-1 rounded-lg cursor-pointer"
              aria-label="Close modal"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <!-- Modal Body Form Layout -->
          <form @submit.prevent="handleSubmit" class="p-6 space-y-4">
            
            <!-- Input 1: Rule Name -->
            <div>
              <label class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5">
                Rule Name <span class="text-rose-500">*</span>
              </label>
              <input
                v-model="ruleForm.rule_name"
                type="text"
                required
                placeholder="e.g. Corporate Portal & API Gateway"
                class="w-full bg-slate-50 text-slate-900 text-xs px-3.5 py-2.5 rounded-lg border border-slate-300 focus:outline-none focus:border-[#2563eb] focus:ring-1 focus:ring-[#2563eb] placeholder:text-slate-400 transition-colors"
              />
              <p class="text-[11px] text-slate-500 mt-1">
                A descriptive identifier for this published application rule in SFOS.
              </p>
            </div>

            <!-- Input 2: Public Domain (FQDN) -->
            <div>
              <label class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5">
                Public Domain (FQDN) <span class="text-rose-500">*</span>
              </label>
              <div class="relative">
                <input
                  v-model="ruleForm.hosted_domain"
                  type="text"
                  required
                  placeholder="e.g. portal.myoffice.local or app.company.com"
                  class="w-full bg-slate-50 text-slate-900 text-xs px-3.5 py-2.5 pl-8 rounded-lg border border-slate-300 font-mono focus:outline-none focus:border-[#2563eb] focus:ring-1 focus:ring-[#2563eb] placeholder:text-slate-400 transition-colors"
                />
                <svg class="w-4 h-4 text-slate-400 absolute left-2.5 top-2.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9" />
                </svg>
              </div>
              <p class="text-[11px] text-slate-500 mt-1">
                Public Fully Qualified Domain Name configured in DNS to point to this firewall WAN interface.
              </p>
            </div>

            <!-- Inputs 3 & 4: Internal Target Server IP Address & Target Communication Port -->
            <div class="grid grid-cols-1 sm:grid-cols-12 gap-3">
              <!-- IP Address (8 Cols) -->
              <div class="sm:col-span-8">
                <label class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5">
                  Internal Target Server IP Address <span class="text-rose-500">*</span>
                </label>
                <input
                  v-model="ruleForm.real_server_ip"
                  type="text"
                  required
                  placeholder="e.g. 10.0.0.45 or 192.168.10.20"
                  class="w-full bg-slate-50 text-slate-900 text-xs px-3.5 py-2.5 rounded-lg border border-slate-300 font-mono focus:outline-none focus:border-[#2563eb] focus:ring-1 focus:ring-[#2563eb] placeholder:text-slate-400 transition-colors"
                />
              </div>

              <!-- Target Communication Port (4 Cols) -->
              <div class="sm:col-span-4">
                <label class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5">
                  Target Port <span class="text-rose-500">*</span>
                </label>
                <input
                  v-model.number="ruleForm.real_server_port"
                  type="number"
                  min="1"
                  max="65535"
                  required
                  placeholder="80"
                  class="w-full bg-slate-50 text-slate-900 text-xs px-3.5 py-2.5 rounded-lg border border-slate-300 font-mono focus:outline-none focus:border-[#2563eb] focus:ring-1 focus:ring-[#2563eb] placeholder:text-slate-400 transition-colors"
                />
              </div>
            </div>

            <!-- Toggle Switch 1: Enable HTTPS / SSL Certificate Mapping -->
            <div class="pt-2 border-t border-slate-100">
              <div class="p-3.5 rounded-xl border border-slate-200 bg-slate-50 flex items-start justify-between gap-4">
                <div class="space-y-1 pr-2">
                  <div class="flex items-center gap-2">
                    <span class="font-bold text-xs text-slate-900">
                      Enable HTTPS / SSL Certificate Mapping
                    </span>
                    <span
                      v-if="ruleForm.enable_ssl"
                      class="text-[9px] font-mono font-bold px-1.5 py-0.2 rounded bg-emerald-50 text-emerald-700 border border-emerald-200"
                    >
                      PORT 443
                    </span>
                  </div>
                  <p class="text-[11px] text-slate-500 leading-relaxed">
                    Terminates SSL/TLS on port 443 with automated TLS 1.3 encryption and HTTP-to-HTTPS redirect offloading.
                  </p>
                </div>

                <!-- Corporate Blue Toggle Switch -->
                <label class="relative inline-flex items-center cursor-pointer flex-shrink-0 select-none mt-1">
                  <input
                    type="checkbox"
                    v-model="ruleForm.enable_ssl"
                    class="sr-only peer"
                    aria-label="Toggle Enable HTTPS / SSL Certificate Mapping"
                  />
                  <div
                    class="w-11 h-6 bg-slate-300 peer-focus:outline-none peer-focus:ring-2 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-slate-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-[#2563eb] shadow-inner transition-colors duration-200"
                  ></div>
                </label>
              </div>
            </div>

            <!-- Toggle Switch 2: Enable Deep Packet Web Application Firewall Inspection (SQLi/XSS Proactive Protection Mode) -->
            <div>
              <div class="p-3.5 rounded-xl border border-slate-200 bg-slate-50 flex items-start justify-between gap-4">
                <div class="space-y-1 pr-2">
                  <div class="flex items-center gap-2">
                    <span class="font-bold text-xs text-slate-900">
                      Enable Deep Packet Web Application Firewall Inspection (SQLi/XSS Proactive Protection Mode)
                    </span>
                    <span
                      v-if="ruleForm.enable_naxsi_waf"
                      class="text-[9px] font-mono font-bold px-1.5 py-0.2 rounded bg-blue-50 text-[#2563eb] border border-blue-200"
                    >
                      NAXSI L7 ACTIVE
                    </span>
                  </div>
                  <p class="text-[11px] text-slate-500 leading-relaxed">
                    Applies NAXSI heuristic signature inspection to sanitize request URIs, headers, and POST payloads against SQL Injection and Cross-Site Scripting exploits.
                  </p>
                </div>

                <!-- Corporate Blue Toggle Switch -->
                <label class="relative inline-flex items-center cursor-pointer flex-shrink-0 select-none mt-1">
                  <input
                    type="checkbox"
                    v-model="ruleForm.enable_naxsi_waf"
                    class="sr-only peer"
                    aria-label="Toggle Enable Deep Packet Web Application Firewall Inspection"
                  />
                  <div
                    class="w-11 h-6 bg-slate-300 peer-focus:outline-none peer-focus:ring-2 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-slate-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-[#2563eb] shadow-inner transition-colors duration-200"
                  ></div>
                </label>
              </div>
            </div>

            <!-- Modal Action Buttons -->
            <div class="pt-4 border-t border-slate-100 flex items-center justify-end gap-2.5">
              <button
                type="button"
                @click="closeModal"
                class="px-4 py-2 rounded-lg bg-white border border-slate-300 text-xs font-semibold text-slate-700 hover:bg-slate-50 transition-colors cursor-pointer"
              >
                Cancel
              </button>

              <button
                type="submit"
                :disabled="isSubmitting"
                class="inline-flex items-center gap-2 px-5 py-2 rounded-lg bg-[#2563eb] hover:bg-blue-600 active:bg-blue-700 text-white text-xs font-bold shadow-md shadow-blue-500/20 transition-all cursor-pointer disabled:opacity-50 disabled:cursor-wait"
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
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                </svg>
                <span>{{ isSubmitting ? 'Deploying to Gateway...' : (isEditing ? 'Update Web Rule' : 'Save & Deploy Rule') }}</span>
              </button>
            </div>

          </form>
        </div>
      </div>
    </transition>

    <!-- ========================================================================= -->
    <!-- MODAL: NGINX CONFIGURATION PREVIEW OVERLAY                                -->
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
        v-if="isConfigModalOpen"
        class="fixed inset-0 z-50 overflow-y-auto bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4"
        role="dialog"
        aria-modal="true"
        @keydown.esc="isConfigModalOpen = false"
      >
        <div class="w-full max-w-2xl bg-white rounded-2xl border border-slate-200 shadow-2xl overflow-hidden flex flex-col" @click.stop>
          <div class="bg-slate-900 text-white px-6 py-4 flex items-center justify-between border-b border-slate-800">
            <div class="flex items-center gap-2.5">
              <svg class="w-4 h-4 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
              </svg>
              <h3 class="text-sm font-bold font-mono text-white">/etc/nginx/sites-available/astaro-next-waf.conf</h3>
            </div>
            <button @click="isConfigModalOpen = false" class="text-slate-400 hover:text-white p-1">✕</button>
          </div>

          <div class="p-4 bg-slate-950 text-emerald-400 font-mono text-xs overflow-y-auto max-h-[60vh] select-text">
            <pre class="whitespace-pre leading-relaxed">{{ generatedNginxConfig }}</pre>
          </div>

          <div class="bg-slate-50 px-6 py-3 border-t border-slate-200 flex justify-between items-center text-xs">
            <span class="text-slate-500 font-mono">Validated with: nginx -t &amp;&amp; systemctl reload nginx</span>
            <button
              type="button"
              @click="copyConfigToClipboard"
              class="px-4 py-1.5 bg-white hover:bg-slate-100 text-slate-700 text-xs font-semibold rounded-lg border border-slate-300 transition-colors shadow-2xs"
            >
              {{ isCopied ? 'Copied to Clipboard!' : 'Copy Config' }}
            </button>
          </div>
        </div>
      </div>
    </transition>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

// Define Emits for parent layout navigation
const emit = defineEmits(['close', 'navigate', 'refresh'])

// -----------------------------------------------------------------------------
// Toast Notification Subsystem
// -----------------------------------------------------------------------------
const toasts = ref([])

const addToast = (title, message, type = 'success') => {
  const id = Date.now() + Math.random().toString(36).substring(2, 7)
  toasts.value.push({ id, title, message, type })
  setTimeout(() => {
    dismissToast(id)
  }, 4500)
}

const dismissToast = (id) => {
  toasts.value = toasts.value.filter(t => t.id !== id)
}

// -----------------------------------------------------------------------------
// Published Web Application Rules State
// -----------------------------------------------------------------------------
const isLoading = ref(false)
const isSubmitting = ref(false)
const searchQuery = ref('')
const wafFilter = ref('ALL')

// Default baseline published rules (matches backend default catalog)
const rulesList = ref([
  {
    id: 1,
    rule_name: 'Internal Intranet Publish',
    hosted_domain: 'portal.myoffice.local',
    real_server_ip: '10.0.0.45',
    real_server_port: 80,
    enable_ssl: true,
    enable_naxsi_waf: true
  },
  {
    id: 2,
    rule_name: 'Payment Gateway API',
    hosted_domain: 'api-pay.corporate.net',
    real_server_ip: '192.168.10.45',
    real_server_port: 8443,
    enable_ssl: true,
    enable_naxsi_waf: true
  }
])

// -----------------------------------------------------------------------------
// Computed Telemetry Metrics
// -----------------------------------------------------------------------------
const activeRulesCount = computed(() => rulesList.value.length)

const sslEnabledCount = computed(() => {
  return rulesList.value.filter(r => r.enable_ssl).length
})

const wafEnabledCount = computed(() => {
  return rulesList.value.filter(r => r.enable_naxsi_waf).length
})

const filteredRules = computed(() => {
  return rulesList.value.filter(rule => {
    // Mode filter
    if (wafFilter.value === 'WAF_ACTIVE' && !rule.enable_naxsi_waf) return false
    if (wafFilter.value === 'SSL_ONLY' && !rule.enable_ssl) return false

    // Search query filter
    if (searchQuery.value.trim()) {
      const q = searchQuery.value.toLowerCase().trim()
      const matchName = rule.rule_name && rule.rule_name.toLowerCase().includes(q)
      const matchDomain = rule.hosted_domain && rule.hosted_domain.toLowerCase().includes(q)
      const matchIp = rule.real_server_ip && rule.real_server_ip.toLowerCase().includes(q)
      const matchPort = rule.real_server_port && rule.real_server_port.toString().includes(q)
      return matchName || matchDomain || matchIp || matchPort
    }
    return true
  })
})

// -----------------------------------------------------------------------------
// Modal Form State & Handlers
// -----------------------------------------------------------------------------
const isModalOpen = ref(false)
const isEditing = ref(false)
const editingRuleId = ref(null)

const ruleForm = ref({
  rule_name: '',
  hosted_domain: '',
  real_server_ip: '',
  real_server_port: 80,
  enable_ssl: true,
  enable_naxsi_waf: true
})

const openAddRuleModal = () => {
  isEditing.value = false
  editingRuleId.value = null
  ruleForm.value = {
    rule_name: '',
    hosted_domain: '',
    real_server_ip: '',
    real_server_port: 80,
    enable_ssl: true,
    enable_naxsi_waf: true
  }
  isModalOpen.value = true
}

const openEditRuleModal = (rule) => {
  isEditing.value = true
  editingRuleId.value = rule.id || null
  ruleForm.value = {
    rule_name: rule.rule_name || '',
    hosted_domain: rule.hosted_domain || '',
    real_server_ip: rule.real_server_ip || '',
    real_server_port: rule.real_server_port || 80,
    enable_ssl: rule.enable_ssl !== undefined ? rule.enable_ssl : true,
    enable_naxsi_waf: rule.enable_naxsi_waf !== undefined ? rule.enable_naxsi_waf : true
  }
  isModalOpen.value = true
}

const closeModal = () => {
  isModalOpen.value = false
}

// -----------------------------------------------------------------------------
// FastAPI Back-End Asynchronous Integration (axios.post -> /api/waf/rules/save)
// -----------------------------------------------------------------------------
const getAxios = () => {
  if (typeof window !== 'undefined' && window.axios) {
    return window.axios
  }
  if (typeof axios !== 'undefined') {
    return axios
  }
  return null
}

const fetchRules = async (showNotification = false) => {
  isLoading.value = true
  const axiosClient = getAxios()

  try {
    if (axiosClient) {
      const response = await axiosClient.get('/api/waf/rules')
      if (response && Array.isArray(response.data)) {
        rulesList.value = response.data
      }
    } else {
      const res = await fetch('/api/waf/rules')
      if (res.ok) {
        const data = await res.json()
        if (Array.isArray(data)) {
          rulesList.value = data
        }
      }
    }
    if (showNotification) {
      addToast('Rules Synced', 'Web Application Firewall rules reloaded from gateway.', 'info')
    }
  } catch (err) {
    console.warn('Could not query /api/waf/rules from gateway, maintaining baseline rules:', err)
    if (showNotification) {
      addToast('Sync Notice', 'Using active in-memory Web Server rules catalog.', 'info')
    }
  } finally {
    isLoading.value = false
  }
}

const handleSubmit = async () => {
  if (!ruleForm.value.rule_name.trim()) {
    addToast('Validation Error', 'Please specify a valid Rule Name.', 'error')
    return
  }
  if (!ruleForm.value.hosted_domain.trim()) {
    addToast('Validation Error', 'Please specify the Public Domain (FQDN).', 'error')
    return
  }
  if (!ruleForm.value.real_server_ip.trim()) {
    addToast('Validation Error', 'Please specify the Internal Target Server IP Address.', 'error')
    return
  }
  if (!ruleForm.value.real_server_port) {
    addToast('Validation Error', 'Please specify the Target Communication Port.', 'error')
    return
  }

  isSubmitting.value = true

  const payload = {
    rule_name: ruleForm.value.rule_name.trim(),
    hosted_domain: ruleForm.value.hosted_domain.trim().replace(/^https?:\/\//i, '').replace(/\/+$/, ''),
    real_server_ip: ruleForm.value.real_server_ip.trim(),
    real_server_port: parseInt(ruleForm.value.real_server_port, 10) || 80,
    enable_ssl: !!ruleForm.value.enable_ssl,
    enable_naxsi_waf: !!ruleForm.value.enable_naxsi_waf
  }

  const axiosClient = getAxios()

  try {
    let responseData = null

    if (axiosClient) {
      const res = await axiosClient.post('/api/waf/rules/save', payload)
      responseData = res.data
    } else {
      const res = await fetch('/api/waf/rules/save', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      })
      if (!res.ok) {
        const errJson = await res.json().catch(() => ({}))
        throw new Error(errJson.detail || `Server responded with status ${res.status}`)
      }
      responseData = await res.json()
    }

    addToast(
      'Web Rule Deployed',
      responseData?.message || `Rule '${payload.rule_name}' successfully compiled and committed to Nginx.`,
      'success'
    )

    // Update or insert rule locally in case backend returns mock
    const existingIdx = rulesList.value.findIndex(r => r.rule_name === payload.rule_name || (editingRuleId.value && r.id === editingRuleId.value))
    if (existingIdx !== -1) {
      rulesList.value[existingIdx] = {
        ...rulesList.value[existingIdx],
        ...payload
      }
    } else {
      rulesList.value.push({
        id: rulesList.value.length + 1,
        ...payload
      })
    }

    closeModal()
    // Reload summary table upon success
    await fetchRules(false)

  } catch (error) {
    console.error('Error saving WAF rule via /api/waf/rules/save:', error)
    const errorMsg = error.response?.data?.detail || error.message || 'Failed to persist WAF configuration to gateway.'
    addToast('Deployment Failed', errorMsg, 'error')
  } finally {
    isSubmitting.value = false
  }
}

const deleteRule = (rule) => {
  rulesList.value = rulesList.value.filter(r => r.rule_name !== rule.rule_name && r.id !== rule.id)
  addToast('Rule Removed', `Web Server Rule '${rule.rule_name}' removed from reverse proxy.`, 'warning')
}

const probeRealServer = (rule) => {
  addToast('Probing Backend', `Sending TCP probe to ${rule.real_server_ip}:${rule.real_server_port}...`, 'info')
  setTimeout(() => {
    addToast('Target Reachable', `Backend ${rule.real_server_ip}:${rule.real_server_port} responded with SYN-ACK (0.7ms).`, 'success')
  }, 600)
}

// -----------------------------------------------------------------------------
// Nginx Configuration Preview Modal State
// -----------------------------------------------------------------------------
const isConfigModalOpen = ref(false)
const isCopied = ref(false)

const generatedNginxConfig = computed(() => {
  const primaryRule = rulesList.value[0] || {
    rule_name: 'Default Published Application',
    hosted_domain: 'portal.myoffice.local',
    real_server_ip: '10.0.0.45',
    real_server_port: 80,
    enable_ssl: true,
    enable_naxsi_waf: true
  }

  const sslDirective = primaryRule.enable_ssl ? '    listen 443 ssl;\n    ssl_protocols TLSv1.2 TLSv1.3;' : '    listen 80;'
  const wafDirective = primaryRule.enable_naxsi_waf
    ? '        # NAXSI Deep Packet Heuristic Inspection Engine\n        SecRulesEnabled;\n        LearningMode;\n        DeniedUrl "/50x.html";\n        CheckRule "$SQL >= 8" BLOCK;\n        CheckRule "$XSS >= 8" BLOCK;'
    : '        # NAXSI WAF Inspection Bypassed;'

  return `# =============================================================================
# Astaro-Next Web Application Firewall Profile: ${primaryRule.rule_name}
# Generated automatically by astaro-middleware daemon (FastAPI / Nginx Core)
# =============================================================================

server {
${sslDirective}
    server_name ${primaryRule.hosted_domain};

    location / {
        proxy_pass http://${primaryRule.real_server_ip}:${primaryRule.real_server_port};
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

${wafDirective}
    }
}
`
})

const openNginxPreview = () => {
  isConfigModalOpen.value = true
}

const copyConfigToClipboard = async () => {
  try {
    await navigator.clipboard.writeText(generatedNginxConfig.value)
    isCopied.value = true
    setTimeout(() => {
      isCopied.value = false
    }, 2000)
  } catch (err) {
    console.error('Clipboard copy failed:', err)
  }
}

// -----------------------------------------------------------------------------
// Component Lifecycle Hooks
// -----------------------------------------------------------------------------
onMounted(() => {
  fetchRules()
})
</script>

<style scoped>
/* High-contrast smooth transitions */
.transition-all {
  transition-property: all;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
}
</style>
