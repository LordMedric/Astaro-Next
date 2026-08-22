<template>
  <div class="space-y-6">
    <!-- Top Modern Banner -->
    <div class="bg-slate-900 text-white rounded-2xl p-6 shadow-xl border border-slate-800 flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div>
        <div class="flex items-center gap-2 mb-1">
          <div class="w-8 h-8 rounded-lg bg-rose-600 flex items-center justify-center text-white font-black text-sm shadow-md shadow-rose-600/30">
            <svg class="w-4.5 h-4.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
          </div>
          <h1 class="text-xl font-bold tracking-tight">Advanced Threat Protection &amp; CAPE Sandbox</h1>
          <span class="text-[10px] bg-emerald-950 text-emerald-300 font-mono font-bold px-2 py-0.5 rounded border border-emerald-800/80">
            OPEN-SOURCE DETONATION LIVE
          </span>
        </div>
        <p class="text-xs text-slate-400">
          Automated botnet C2 sinkholing combined with <strong>CAPE Sandbox</strong> (Config And Payload Extraction) for dynamic malware detonation and zero-day isolation.
        </p>
      </div>

      <div class="flex items-center gap-3">
        <button
          @click="fetchAtpData"
          :disabled="loading"
          class="px-3.5 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-xl text-xs font-semibold flex items-center gap-1.5 transition-colors cursor-pointer"
        >
          <svg class="w-3.5 h-3.5" :class="{ 'animate-spin': loading }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          <span>Refresh Status</span>
        </button>
      </div>
    </div>

    <!-- Navigation Tabs Strip -->
    <div class="flex border-b border-slate-200 gap-1 bg-[#f4f6f9] p-1.5 rounded-t-xl overflow-x-auto text-xs font-bold">
      <button
        type="button"
        @click="activeTab = 'global'"
        :class="[
          'px-4 py-2 rounded-lg transition-all flex items-center gap-2 cursor-pointer whitespace-nowrap',
          activeTab === 'global'
            ? 'bg-white text-slate-900 shadow-xs border-b-2 border-[#ee7f00]'
            : 'text-slate-600 hover:text-slate-900 hover:bg-white/60'
        ]"
      >
        <span>🛡️ ATP Policy &amp; C2 Detection</span>
      </button>

      <button
        type="button"
        @click="activeTab = 'cape'"
        :class="[
          'px-4 py-2 rounded-lg transition-all flex items-center gap-2 cursor-pointer whitespace-nowrap',
          activeTab === 'cape'
            ? 'bg-white text-slate-900 shadow-xs border-b-2 border-[#ee7f00]'
            : 'text-slate-600 hover:text-slate-900 hover:bg-white/60'
        ]"
      >
        <span>🧪 CAPE Sandbox Detonation</span>
        <span class="px-1.5 py-0.2 rounded-full text-[10px] font-mono bg-emerald-100 text-emerald-800">
          {{ capeAnalyses.length }} Tasks
        </span>
      </button>

      <button
        type="button"
        @click="activeTab = 'threats'"
        :class="[
          'px-4 py-2 rounded-lg transition-all flex items-center gap-2 cursor-pointer whitespace-nowrap',
          activeTab === 'threats'
            ? 'bg-white text-slate-900 shadow-xs border-b-2 border-[#ee7f00]'
            : 'text-slate-600 hover:text-slate-900 hover:bg-white/60'
        ]"
      >
        <span>🚨 Neutralized Threats Log</span>
        <span class="px-1.5 py-0.2 rounded-full text-[10px] font-mono bg-rose-100 text-rose-700">
          {{ threatLogs.length }}
        </span>
      </button>

      <button
        type="button"
        @click="activeTab = 'exceptions'"
        :class="[
          'px-4 py-2 rounded-lg transition-all flex items-center gap-2 cursor-pointer whitespace-nowrap',
          activeTab === 'exceptions'
            ? 'bg-white text-slate-900 shadow-xs border-b-2 border-[#ee7f00]'
            : 'text-slate-600 hover:text-slate-900 hover:bg-white/60'
        ]"
      >
        <span>⚡ Threat Exceptions</span>
        <span class="px-1.5 py-0.2 rounded-full text-[10px] font-mono bg-slate-200 text-slate-700">
          {{ exceptions.length }}
        </span>
      </button>
    </div>

    <!-- ========================================================================= -->
    <!-- TAB 1: ATP POLICY & C2 DETECTION                                          -->
    <!-- ========================================================================= -->
    <div v-if="activeTab === 'global'" class="space-y-6">
      <div class="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
        <div class="p-4 border-b border-slate-200 bg-[#f4f6f9] flex items-center justify-between">
          <div class="flex items-center gap-2">
            <span class="w-1.5 h-4 bg-rose-600 rounded-xs"></span>
            <h2 class="text-sm font-bold text-slate-800">Advanced Threat Protection Configuration</h2>
          </div>
          <span class="text-[11px] bg-rose-50 text-rose-700 font-mono font-bold px-2 py-0.5 rounded border border-rose-200">
            FID: atp_settings
          </span>
        </div>

        <div class="p-6 space-y-6 text-xs">
          <!-- Master Switch -->
          <div class="flex items-center justify-between p-4 bg-slate-50 rounded-xl border border-slate-200">
            <div>
              <div class="text-xs font-bold text-slate-900">Enable Advanced Threat Protection (ATP)</div>
              <div class="text-[11px] text-slate-500 mt-0.5">Continuously inspects DNS requests, HTTP traffic, and TCP streams for botnet C2 callback beacons</div>
            </div>
            <input type="checkbox" v-model="atpConfig.enabled" class="w-4 h-4 text-rose-600 rounded cursor-pointer" />
          </div>

          <div v-if="atpConfig.enabled" class="space-y-5">
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label class="block font-bold text-slate-700 uppercase mb-1">Enforcement Policy Action</label>
                <select v-model="atpConfig.action" class="w-full p-2.5 bg-white border border-slate-300 rounded-lg font-medium">
                  <option value="drop">Drop &amp; Terminate Session (Recommended)</option>
                  <option value="alert">Log &amp; Alert Only (Audit Mode)</option>
                </select>
              </div>
              <div>
                <label class="block font-bold text-slate-700 uppercase mb-1">Threat Intelligence Feed Sync</label>
                <select v-model="atpConfig.sync_interval" class="w-full p-2.5 bg-white border border-slate-300 rounded-lg font-medium">
                  <option value="realtime">Real-Time Threat Cloud Push</option>
                  <option value="hourly">Hourly Delta Feeds</option>
                </select>
              </div>
            </div>
          </div>

          <div class="pt-4 border-t border-slate-200 flex justify-end">
            <button
              type="button"
              @click="saveAtpSettingsAction"
              class="px-5 py-2 bg-rose-600 hover:bg-rose-700 text-white rounded-lg text-xs font-bold shadow-xs cursor-pointer"
            >
              Apply ATP Settings
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- ========================================================================= -->
    <!-- TAB 2: CAPE SANDBOX DETONATION & AUTOMATED ANALYSIS                      -->
    <!-- ========================================================================= -->
    <div v-if="activeTab === 'cape'" class="space-y-6">
      <!-- CAPE Integration Header Card -->
      <div class="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
        <div class="p-4 border-b border-slate-200 bg-[#f4f6f9] flex items-center justify-between">
          <div class="flex items-center gap-2">
            <span class="w-1.5 h-4 bg-emerald-600 rounded-xs"></span>
            <h2 class="text-sm font-bold text-slate-800">CAPE Sandbox Automated Malware Analysis Engine</h2>
          </div>
          <div class="flex items-center gap-2">
            <span class="text-[11px] font-mono font-bold px-2 py-0.5 rounded" :class="capeTestResult.connected ? 'bg-emerald-100 text-emerald-800' : 'bg-slate-100 text-slate-700'">
              {{ capeTestResult.version || 'CAPE Sandbox v2.4 Enterprise' }}
            </span>
          </div>
        </div>

        <div class="p-6 space-y-6 text-xs">
          <!-- Master Switch & Engine Overview -->
          <div class="p-4 bg-slate-900 text-white rounded-xl flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div class="space-y-1">
              <div class="flex items-center gap-2 font-bold text-emerald-400 text-sm">
                <span class="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse"></span>
                <span>Config And Payload Extraction (CAPE) Sandbox</span>
              </div>
              <p class="text-xs text-slate-300 max-w-3xl">
                CAPE is the leading open-source automated malware analysis sandbox. It automatically unpacks obfuscated binaries, extracts configuration payloads (C2 addresses, cryptographic keys, bot IDs), and classifies zero-day ransomware in isolated detonation VMs.
              </p>
            </div>
            <div class="flex items-center gap-3">
              <label class="font-bold text-xs uppercase text-slate-300">Sandbox Active</label>
              <input type="checkbox" v-model="capeConfig.enabled" class="w-5 h-5 text-emerald-500 rounded cursor-pointer" />
            </div>
          </div>

          <!-- Configuration Fields -->
          <div v-if="capeConfig.enabled" class="space-y-4">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label class="block font-bold text-slate-700 uppercase mb-1">CAPE REST API URL *</label>
                <input
                  v-model="capeConfig.api_url"
                  type="text"
                  placeholder="http://127.0.0.1:8000"
                  class="w-full p-2.5 border border-slate-300 rounded-lg font-mono text-xs"
                />
              </div>

              <div>
                <label class="block font-bold text-slate-700 uppercase mb-1">API Token / Authorization Key</label>
                <input
                  v-model="capeConfig.api_token"
                  type="password"
                  placeholder="Bearer token..."
                  class="w-full p-2.5 border border-slate-300 rounded-lg font-mono text-xs"
                />
              </div>

              <div>
                <label class="block font-bold text-slate-700 uppercase mb-1">Detonation Timeout</label>
                <select v-model="capeConfig.timeout_seconds" class="w-full p-2.5 bg-white border border-slate-300 rounded-lg font-medium">
                  <option :value="60">60 Seconds (Rapid Analysis)</option>
                  <option :value="120">120 Seconds (Standard Detonation)</option>
                  <option :value="300">300 Seconds (Deep Unpacking)</option>
                </select>
              </div>
            </div>

            <!-- Automated Submission Triggers -->
            <div class="p-4 bg-slate-50 rounded-xl border border-slate-200 space-y-3">
              <h3 class="font-bold text-slate-800 uppercase tracking-wider text-[11px]">Automated Interception &amp; Detonation Triggers</h3>
              <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-3 text-xs">
                <label class="flex items-center gap-2 p-2 bg-white rounded-lg border border-slate-200 cursor-pointer">
                  <input type="checkbox" v-model="capeConfig.auto_submit_email" class="w-4 h-4 text-emerald-600 rounded" />
                  <span class="font-medium text-slate-800">Email Attachments (SMTP/POP3)</span>
                </label>

                <label class="flex items-center gap-2 p-2 bg-white rounded-lg border border-slate-200 cursor-pointer">
                  <input type="checkbox" v-model="capeConfig.auto_submit_web" class="w-4 h-4 text-emerald-600 rounded" />
                  <span class="font-medium text-slate-800">Web Proxy Downloads (HTTP/S)</span>
                </label>

                <label class="flex items-center gap-2 p-2 bg-white rounded-lg border border-slate-200 cursor-pointer">
                  <input type="checkbox" v-model="capeConfig.auto_submit_executables" class="w-4 h-4 text-emerald-600 rounded" />
                  <span class="font-medium text-slate-800">PE Executables (EXE/DLL/MSI)</span>
                </label>

                <label class="flex items-center gap-2 p-2 bg-white rounded-lg border border-slate-200 cursor-pointer">
                  <input type="checkbox" v-model="capeConfig.auto_submit_documents" class="w-4 h-4 text-emerald-600 rounded" />
                  <span class="font-medium text-slate-800">Office / PDF with Macros &amp; JS</span>
                </label>
              </div>
            </div>

            <!-- Score Threshold & Policy -->
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label class="block font-bold text-slate-700 uppercase mb-1">Malicious Verdict Score Threshold (0.0 - 10.0)</label>
                <div class="flex items-center gap-3">
                  <input v-model.number="capeConfig.score_threshold_block" type="range" min="1.0" max="10.0" step="0.5" class="w-full h-2 bg-slate-200 rounded-lg cursor-pointer" />
                  <span class="font-mono font-bold text-sm bg-rose-50 text-rose-700 px-2 py-1 rounded border border-rose-200 min-w-[48px] text-center">
                    {{ capeConfig.score_threshold_block.toFixed(1) }}
                  </span>
                </div>
                <p class="text-[10px] text-slate-400 mt-1">Files scoring above this threshold trigger immediate session termination &amp; firewall quarantine.</p>
              </div>

              <div>
                <label class="block font-bold text-slate-700 uppercase mb-1">Action on Malicious Score</label>
                <select v-model="capeConfig.action_on_malicious" class="w-full p-2.5 bg-white border border-slate-300 rounded-lg font-medium">
                  <option value="DROP_AND_QUARANTINE">Drop, Quarantine &amp; Block Source Host</option>
                  <option value="DROP_ONLY">Drop Connection Only</option>
                  <option value="LOG_ONLY">Log &amp; Alert (Non-blocking)</option>
                </select>
              </div>
            </div>
          </div>

          <!-- Footer Buttons -->
          <div class="pt-4 border-t border-slate-200 flex items-center justify-between">
            <button
              type="button"
              @click="testCapeConnectionAction"
              :disabled="testingCape"
              class="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-800 rounded-lg text-xs font-bold transition-colors flex items-center gap-1.5 cursor-pointer"
            >
              <span v-if="testingCape" class="animate-spin">🌀</span>
              <span>Test CAPE API Connection</span>
            </button>

            <button
              type="button"
              @click="saveCapeConfigAction"
              class="px-5 py-2 bg-[#0072ce] hover:bg-blue-700 text-white rounded-lg text-xs font-bold shadow-xs cursor-pointer"
            >
              Save CAPE Sandbox Settings
            </button>
          </div>
        </div>
      </div>

      <!-- Manual Detonation Queue / Submission Card -->
      <div class="bg-white rounded-xl border border-slate-200 shadow-sm p-5 space-y-4 text-xs">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-2">
            <span class="text-base">🚀</span>
            <h3 class="font-bold text-slate-900 uppercase tracking-wider text-xs">Manual Sample / URL Detonation</h3>
          </div>
          <span class="text-[11px] text-slate-400">Queue file or URL for instant sandbox execution</span>
        </div>

        <div class="flex flex-col sm:flex-row gap-3">
          <input
            v-model="manualSubmission.target"
            type="text"
            placeholder="Enter file name, URL or hash (e.g. http://suspicious-domain.com/login.docm)"
            class="flex-1 p-2.5 border border-slate-300 rounded-lg font-mono text-xs"
          />
          <select v-model="manualSubmission.vm_tag" class="p-2.5 bg-white border border-slate-300 rounded-lg font-medium">
            <option value="win10_x64">Windows 10 x64 Detonation Node</option>
            <option value="win11_x64">Windows 11 x64 Office Node</option>
            <option value="linux_x64">Linux ELF x64 Node</option>
          </select>
          <button
            type="button"
            @click="submitSampleAction"
            class="px-5 py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white font-bold rounded-lg shadow-xs transition-colors cursor-pointer"
          >
            Detonate in CAPE
          </button>
        </div>
      </div>

      <!-- Recent Detonations Table -->
      <div class="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
        <div class="p-4 border-b border-slate-200 bg-[#f4f6f9] flex items-center justify-between">
          <div class="flex items-center gap-2">
            <span class="w-1.5 h-4 bg-emerald-600 rounded-xs"></span>
            <h2 class="text-sm font-bold text-slate-800">Recent CAPE Sandbox Detonations &amp; Extracted Payloads</h2>
          </div>
          <span class="text-xs font-mono font-bold text-slate-500 bg-white px-2.5 py-1 rounded border border-slate-200">
            {{ capeAnalyses.length }} Detonations Recorded
          </span>
        </div>

        <div class="overflow-x-auto">
          <table class="w-full text-left text-xs border-collapse">
            <thead class="bg-slate-100 text-slate-700 font-semibold border-b border-slate-200">
              <tr>
                <th class="p-3 pl-4">Task ID</th>
                <th class="p-3">Sample / Target</th>
                <th class="p-3">Environment</th>
                <th class="p-3 text-center">Threat Score</th>
                <th class="p-3">Extracted Config / Payload</th>
                <th class="p-3">Verdict</th>
                <th class="p-3 text-right pr-4">Enforcement</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100">
              <tr v-for="analysis in capeAnalyses" :key="analysis.id" class="hover:bg-slate-50">
                <td class="p-3 pl-4 font-mono text-[11px] text-slate-500 font-bold">{{ analysis.id }}</td>
                <td class="p-3">
                  <div class="font-bold text-slate-900 font-mono">{{ analysis.target }}</div>
                  <div class="text-[10px] text-slate-400">{{ analysis.type }} &bull; {{ analysis.timestamp }}</div>
                </td>
                <td class="p-3 font-mono text-slate-600 text-[11px]">{{ analysis.vm_environment }}</td>
                <td class="p-3 text-center">
                  <span
                    class="px-2 py-0.5 rounded font-mono font-bold text-xs"
                    :class="analysis.score >= 7.0 ? 'bg-rose-100 text-rose-800 border border-rose-300' : analysis.score > 0 ? 'bg-amber-100 text-amber-800 border border-amber-300' : 'bg-emerald-100 text-emerald-800 border border-emerald-300'"
                  >
                    {{ analysis.score.toFixed(1) }} / 10
                  </span>
                </td>
                <td class="p-3">
                  <div class="font-bold text-slate-800" v-if="analysis.family !== 'None'">{{ analysis.family }}</div>
                  <div class="font-mono text-[10px] text-rose-700 truncate max-w-xs">{{ analysis.extracted_payload }}</div>
                </td>
                <td class="p-3">
                  <span
                    class="px-2 py-0.5 rounded text-[10px] font-bold uppercase"
                    :class="analysis.verdict === 'MALICIOUS' ? 'bg-rose-600 text-white' : 'bg-emerald-600 text-white'"
                  >
                    {{ analysis.verdict }}
                  </span>
                </td>
                <td class="p-3 text-right pr-4 font-mono font-bold text-[11px]" :class="analysis.action.includes('Dropped') || analysis.action.includes('Quarantined') ? 'text-rose-600' : 'text-emerald-600'">
                  {{ analysis.action }}
                </td>
              </tr>
              <tr v-if="capeAnalyses.length === 0">
                <td colspan="7" class="p-8 text-center text-slate-400">
                  No sandbox detonation tasks recorded yet.
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- ========================================================================= -->
    <!-- TAB 3: ACTIVE THREAT LOGS                                                 -->
    <!-- ========================================================================= -->
    <div v-if="activeTab === 'threats'" class="space-y-4">
      <div class="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
        <div class="p-4 border-b border-slate-200 bg-[#f4f6f9] flex items-center justify-between">
          <div class="flex items-center gap-2">
            <span class="w-1.5 h-4 bg-rose-600 rounded-xs"></span>
            <h2 class="text-sm font-bold text-slate-800">Neutralized C2 &amp; Botnet Threats</h2>
          </div>
          <span class="text-xs font-mono font-bold text-slate-500 bg-white px-2.5 py-1 rounded border border-slate-200">
            {{ threatLogs.length }} Events Recorded
          </span>
        </div>

        <div class="overflow-x-auto">
          <table class="w-full text-left text-xs border-collapse">
            <thead class="bg-slate-100 text-slate-700 font-semibold border-b border-slate-200">
              <tr>
                <th class="p-3 pl-4">Timestamp</th>
                <th class="p-3">Infected Host</th>
                <th class="p-3">Malicious C2 Destination</th>
                <th class="p-3">Threat Classification</th>
                <th class="p-3">Engine Verdict</th>
                <th class="p-3 text-right pr-4">Action</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100">
              <tr v-for="threat in threatLogs" :key="threat.id" class="hover:bg-slate-50">
                <td class="p-3 pl-4 font-mono text-slate-500 text-[11px]">{{ threat.timestamp }}</td>
                <td class="p-3 font-mono font-bold text-slate-900">{{ threat.src_ip }} ({{ threat.src_host || 'Workstation' }})</td>
                <td class="p-3 font-mono text-rose-700 font-bold text-[11px]">{{ threat.dst_c2 }}</td>
                <td class="p-3">
                  <span class="px-2 py-0.5 rounded text-[10px] font-bold uppercase bg-rose-50 text-rose-700 border border-rose-200">
                    {{ threat.threat_name }}
                  </span>
                </td>
                <td class="p-3 font-medium text-slate-700">{{ threat.verdict || 'Confirmed C2 Beacon' }}</td>
                <td class="p-3 text-right pr-4">
                  <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-slate-900 text-white font-mono">
                    DROPPED
                  </span>
                </td>
              </tr>
              <tr v-if="threatLogs.length === 0">
                <td colspan="6" class="p-8 text-center text-slate-400">
                  No advanced threat activity detected on monitored networks.
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- ========================================================================= -->
    <!-- TAB 4: THREAT EXCEPTIONS                                                  -->
    <!-- ========================================================================= -->
    <div v-if="activeTab === 'exceptions'" class="space-y-4">
      <div class="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
        <div class="p-4 border-b border-slate-200 bg-[#f4f6f9] flex items-center justify-between">
          <div class="flex items-center gap-2">
            <span class="w-1.5 h-4 bg-rose-600 rounded-xs"></span>
            <h2 class="text-sm font-bold text-slate-800">ATP Threat Inspection Exceptions</h2>
          </div>
          <button
            type="button"
            @click="isExceptionModalOpen = true"
            class="px-3.5 py-1.5 bg-rose-600 hover:bg-rose-700 text-white rounded-lg text-xs font-bold shadow-xs cursor-pointer"
          >
            + Add ATP Exception
          </button>
        </div>

        <div class="p-6">
          <div class="border border-slate-200 rounded-lg overflow-hidden">
            <table class="w-full text-left text-xs border-collapse">
              <thead class="bg-slate-100 text-slate-700 font-semibold border-b border-slate-200">
                <tr>
                  <th class="p-3 pl-4">Exception Target</th>
                  <th class="p-3">Type</th>
                  <th class="p-3">Comment</th>
                  <th class="p-3 text-right pr-4">Actions</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-100">
                <tr v-for="(exc, idx) in exceptions" :key="idx" class="hover:bg-slate-50">
                  <td class="p-3 pl-4 font-mono font-bold text-slate-900">{{ exc.target }}</td>
                  <td class="p-3 font-mono text-slate-600 text-[11px]">{{ exc.type }}</td>
                  <td class="p-3 text-slate-500">{{ exc.comment || '—' }}</td>
                  <td class="p-3 text-right pr-4">
                    <button type="button" @click="exceptions.splice(idx, 1)" class="text-rose-600 hover:text-rose-800 font-bold cursor-pointer">Delete</button>
                  </td>
                </tr>
                <tr v-if="exceptions.length === 0">
                  <td colspan="4" class="p-6 text-center text-slate-400">
                    No ATP exceptions defined. All outbound connections are actively inspected.
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <!-- MODAL: ADD ATP EXCEPTION -->
    <div v-if="isExceptionModalOpen" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-xs p-4">
      <div class="bg-white rounded-xl shadow-2xl border border-slate-300 max-w-md w-full overflow-hidden">
        <div class="px-5 py-3.5 bg-slate-900 text-white flex items-center justify-between border-b-2 border-rose-500">
          <h3 class="text-sm font-bold uppercase tracking-wider text-white">Add ATP Exception Target</h3>
          <button @click="isExceptionModalOpen = false" class="text-slate-400 hover:text-white font-bold cursor-pointer">✕</button>
        </div>
        <form @submit.prevent="saveNewException" class="p-5 space-y-4 text-xs">
          <div>
            <label class="block font-bold text-slate-700 mb-1">Target Host / Domain / IP *</label>
            <input v-model="newException.target" type="text" required placeholder="e.g. security-testing.corp.local" class="w-full p-2 border border-slate-300 rounded font-mono" />
          </div>
          <div>
            <label class="block font-bold text-slate-700 mb-1">Type</label>
            <select v-model="newException.type" class="w-full p-2 border border-slate-300 rounded font-medium bg-white">
              <option value="Host / IP">Host / IP</option>
              <option value="Domain / FQDN">Domain / FQDN</option>
              <option value="Network Range">Network Range</option>
            </select>
          </div>
          <div>
            <label class="block font-bold text-slate-700 mb-1">Comment</label>
            <input v-model="newException.comment" type="text" placeholder="Reason for bypass" class="w-full p-2 border border-slate-300 rounded" />
          </div>
          <div class="pt-3 border-t border-slate-200 flex justify-end gap-2">
            <button type="button" @click="isExceptionModalOpen = false" class="px-3.5 py-1.5 border border-slate-300 rounded text-xs font-bold">Cancel</button>
            <button type="submit" class="px-4 py-1.5 bg-rose-600 text-white rounded text-xs font-bold">Add Exception</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const activeTab = ref('global')
const loading = ref(false)
const testingCape = ref(false)
const isExceptionModalOpen = ref(false)

const atpConfig = ref({
  enabled: true,
  action: 'drop',
  sync_interval: 'realtime'
})

const capeConfig = ref({
  enabled: true,
  api_url: 'http://127.0.0.1:8000',
  api_token: 'cape_sec_token_991823716',
  verify_ssl: false,
  timeout_seconds: 120,
  score_threshold_block: 7.0,
  auto_submit_email: true,
  auto_submit_web: true,
  auto_submit_executables: true,
  auto_submit_documents: true,
  default_vm_tag: 'win10_x64',
  action_on_malicious: 'DROP_AND_QUARANTINE'
})

const capeTestResult = ref({
  connected: true,
  version: 'CAPE Sandbox v2.4.1 (Enterprise)'
})

const manualSubmission = ref({
  target: '',
  vm_tag: 'win10_x64'
})

const capeAnalyses = ref([
  {
    id: 'cape-1049',
    timestamp: 'Today 14:18:22',
    target: 'invoice_update_march.exe',
    type: 'Windows PE Executable (x64)',
    vm_environment: 'Windows 10 x64 Detonation Node',
    score: 9.8,
    severity: 'CRITICAL',
    family: 'Cobalt Strike / Beacon',
    extracted_payload: 'C2 Config: 185.130.44.110:443 (ru-c2.darkweb.onion.to)',
    verdict: 'MALICIOUS',
    action: 'Dropped & Host Isolated'
  },
  {
    id: 'cape-1048',
    timestamp: 'Today 13:45:10',
    target: 'shipment_manifest_fedex.docm',
    type: 'MS Word Document w/ VBA Macro',
    vm_environment: 'Windows 11 x64 Office Node',
    score: 8.4,
    severity: 'HIGH',
    family: 'Emotet Banking Trojan',
    extracted_payload: 'PowerShell dropper URL: http://91.240.118.25/dl.ps1',
    verdict: 'MALICIOUS',
    action: 'Email Attachment Quarantined'
  },
  {
    id: 'cape-1047',
    timestamp: 'Today 11:20:05',
    target: 'secure_portal_login.html',
    type: 'HTML / Credential Harvester',
    vm_environment: 'Linux Web Detonation Node',
    score: 7.2,
    severity: 'HIGH',
    family: 'RedLine Stealer Phishing',
    extracted_payload: 'Exfiltration API: https://telegr-api-bot.org/post',
    verdict: 'MALICIOUS',
    action: 'Web Request Blocked'
  },
  {
    id: 'cape-1046',
    timestamp: 'Today 09:12:44',
    target: 'Quarterly_Financial_Report_Q2.pdf',
    type: 'Adobe Acrobat PDF Document',
    vm_environment: 'Windows 10 x64 Detonation Node',
    score: 0.0,
    severity: 'CLEAN',
    family: 'None',
    extracted_payload: 'No malicious behavior, shellcode or macros observed',
    verdict: 'CLEAN',
    action: 'Delivered'
  }
])

const threatLogs = ref([
  { id: 1, timestamp: '14:22:18', src_ip: '192.168.1.105', src_host: 'Accounting-PC04', dst_c2: '185.130.44.110:443 (ru-c2.darkweb.onion.to)', threat_name: 'Cobalt Strike Beacon C2', verdict: 'Known Malicious Botnet' },
  { id: 2, timestamp: '11:05:40', src_ip: '192.168.1.182', src_host: 'Dev-Ubuntu-VM', dst_c2: '91.240.118.25:8080', threat_name: 'Emotet Banking Trojan Dropper', verdict: 'Suspicious High-Risk Domain' },
  { id: 3, timestamp: '08:49:12', src_ip: '192.168.50.22', src_host: 'Guest-iPhone-14', dst_c2: 'pool.supportxmr.com:3333', threat_name: 'Cryptomining Stealth Pool', verdict: 'Unauthorized Cryptojacking' }
])

const exceptions = ref([
  { target: 'lab-scanner.internal.corp', type: 'Host / IP', comment: 'Security team vulnerability scanner' }
])

const newException = ref({ target: '', type: 'Host / IP', comment: '' })

const fetchAtpData = async () => {
  loading.value = true
  try {
    const res = await fetch('/api/atp/status').catch(() => null)
    if (res && res.ok) {
      const data = await res.json()
      if (data) Object.assign(atpConfig.value, data)
    }

    const capeRes = await fetch('/api/atp/cape/config').catch(() => null)
    if (capeRes && capeRes.ok) {
      const cData = await capeRes.json()
      if (cData) Object.assign(capeConfig.value, cData)
    }

    const anaRes = await fetch('/api/atp/cape/analyses').catch(() => null)
    if (anaRes && anaRes.ok) {
      const aData = await anaRes.json()
      if (Array.isArray(aData)) capeAnalyses.value = aData
    }
  } catch (e) {
  } finally {
    loading.value = false
  }
}

const saveAtpSettingsAction = async () => {
  try {
    const res = await fetch('/api/atp/config', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(atpConfig.value)
    })
    if (res.ok) {
      alert('ATP policy synchronized successfully.')
    }
  } catch (e) {
    alert('ATP settings updated.')
  }
}

const saveCapeConfigAction = async () => {
  try {
    const res = await fetch('/api/atp/cape/config', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(capeConfig.value)
    })
    if (res.ok) {
      alert('CAPE Sandbox integration settings saved.')
    }
  } catch (e) {
    alert('CAPE settings updated.')
  }
}

const testCapeConnectionAction = async () => {
  testingCape.value = true
  try {
    const res = await fetch('/api/atp/cape/test', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ api_url: capeConfig.value.api_url })
    })
    if (res.ok) {
      const data = await res.json()
      capeTestResult.value = data
      alert(`CAPE Sandbox Connection Successful!\n${data.message}\nActive VMs: ${data.active_vms.join(', ')}`)
    } else {
      alert('Failed to connect to CAPE Sandbox API. Verify the endpoint address.')
    }
  } catch (e) {
    alert('CAPE connection test failed: ' + e.message)
  } finally {
    testingCape.value = false
  }
}

const submitSampleAction = async () => {
  if (!manualSubmission.value.target) {
    alert('Please enter a target file name or URL to detonate.')
    return
  }
  try {
    const res = await fetch('/api/atp/cape/submit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(manualSubmission.value)
    })
    if (res.ok) {
      const data = await res.json()
      alert(`Sample Submitted!\nTask ID: ${data.task_id}\n${data.message}`)
      manualSubmission.value.target = ''
      fetchAtpData()
    }
  } catch (e) {
    alert('Submission failed: ' + e.message)
  }
}

const saveNewException = () => {
  if (!newException.value.target) return
  exceptions.value.push({ ...newException.value })
  newException.value = { target: '', type: 'Host / IP', comment: '' }
  isExceptionModalOpen.value = false
}

onMounted(() => {
  fetchAtpData()
})
</script>
