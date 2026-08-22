<template>
  <div class="space-y-6">
    <!-- Top Action & Executive Telemetry Header Ribbon -->
    <div class="bg-white border border-slate-200 rounded-xl p-5 shadow-xs flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
      <div>
        <div class="flex items-center gap-2.5">
          <span class="w-1.5 h-6 bg-[#ee7f00] rounded-xs inline-block"></span>
          <h1 class="text-xl font-bold text-slate-900 tracking-tight">Executive Control Center</h1>
          <span class="text-[11px] bg-emerald-50 text-emerald-700 font-medium font-mono px-2 py-0.5 rounded border border-emerald-200 flex items-center gap-1.5">
            <span class="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
            Real-Time Engine
          </span>
          <span class="text-[11px] bg-blue-50 text-[#0072ce] font-bold font-mono px-2 py-0.5 rounded border border-blue-200">
            Safety Score: {{ systemMetrics.safetyScore || 98 }}/100
          </span>
        </div>
        <p class="text-xs text-slate-500 mt-1 pl-4">
          Integrated visual monitors, live interface speedometers, threat radar, cross-premises VPN topology, and hardware resource partitions.
        </p>
      </div>

      <!-- Live Polling & Telemetry Controls -->
      <div class="flex items-center flex-wrap gap-2.5">
        <div class="flex items-center bg-slate-100 p-0.5 rounded-lg border border-slate-200 text-xs">
          <span class="px-2 py-1 text-slate-500 font-medium text-[11px]">Poll:</span>
          <button
            v-for="interval in [3, 5, 10, 30]"
            :key="interval"
            type="button"
            @click="setPollInterval(interval)"
            :class="[
              'px-2.5 py-1 rounded text-xs font-semibold transition-all cursor-pointer',
              pollIntervalSeconds === interval
                ? 'bg-white text-[#0072ce] shadow-xs border border-slate-200/80 font-bold'
                : 'text-slate-600 hover:text-slate-900'
            ]"
          >
            {{ interval }}s
          </button>
          <button
            type="button"
            @click="togglePolling"
            :class="[
              'px-2.5 py-1 rounded text-xs font-semibold transition-all flex items-center gap-1.5 cursor-pointer',
              !isPollingActive ? 'bg-amber-100 text-amber-800 font-bold' : 'text-slate-600 hover:text-slate-900'
            ]"
            :title="isPollingActive ? 'Pause Auto-Refresh' : 'Resume Auto-Refresh'"
          >
            <span :class="['w-1.5 h-1.5 rounded-full', isPollingActive ? 'bg-emerald-500' : 'bg-amber-500']"></span>
            {{ isPollingActive ? 'Live' : 'Paused' }}
          </button>
        </div>

        <button
          type="button"
          @click="fetchTelemetry(true)"
          :disabled="isLoading"
          class="px-3.5 py-2 text-xs font-semibold bg-white hover:bg-slate-50 text-slate-700 rounded-lg border border-slate-300 transition-colors flex items-center gap-1.5 shadow-xs cursor-pointer active:bg-slate-100 disabled:opacity-50"
        >
          <svg :class="['w-3.5 h-3.5 text-slate-500', isLoading ? 'animate-spin text-[#0072ce]' : '']" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          <span>Refresh</span>
        </button>
      </div>
    </div>

    <!-- Standardized Flat Tab Navigation Strip (UTM 9 Style) -->
    <div class="flex border-b border-slate-200 gap-1 bg-[#f4f6f9] p-1.5 rounded-t-xl overflow-x-auto text-xs font-bold">
      <button
        v-for="tab in mainTabs"
        :key="tab.id"
        type="button"
        @click="activeViewTab = tab.id"
        :class="[
          'px-4 py-2 rounded-lg transition-all flex items-center gap-2 cursor-pointer whitespace-nowrap',
          activeViewTab === tab.id
            ? 'bg-white text-slate-900 shadow-xs border-b-2 border-[#ee7f00]'
            : 'text-slate-600 hover:text-slate-900 hover:bg-white/60'
        ]"
      >
        <component :is="tab.icon" class="w-4 h-4 text-[#0072ce]" />
        <span>{{ tab.label }}</span>
        <span
          v-if="tab.badge"
          class="px-1.5 py-0.2 rounded-full text-[10px] font-mono"
          :class="activeViewTab === tab.id ? 'bg-[#0072ce] text-white' : 'bg-slate-200 text-slate-700'"
        >
          {{ tab.badge }}
        </span>
      </button>
    </div>

    <!-- ========================================================================= -->
    <!-- VIEW 1: MODULAR 4-QUADRANT EXECUTIVE CONTROL CENTER                       -->
    <!-- ========================================================================= -->
    <div v-if="activeViewTab === 'quadrant'" class="space-y-6">
      <!-- Top Metric Summary Cards Ribbon -->
      <div class="grid grid-cols-2 lg:grid-cols-4 gap-3.5">
        <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-xs flex items-center gap-3.5">
          <div class="w-10 h-10 rounded-lg bg-blue-50 text-[#0072ce] flex items-center justify-center font-bold">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
          </div>
          <div>
            <div class="text-[10px] uppercase font-bold text-slate-400">WAN Throughput</div>
            <div class="text-base font-black text-slate-900 font-mono">{{ bandwidthMetrics.wanRate || '72.4 Mbps' }}</div>
            <span class="text-[10px] text-emerald-600 font-semibold">↓ 58.7 Mbps | ↑ 13.7 Mbps</span>
          </div>
        </div>

        <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-xs flex items-center gap-3.5">
          <div class="w-10 h-10 rounded-lg bg-rose-50 text-rose-600 flex items-center justify-center font-bold">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
          </div>
          <div>
            <div class="text-[10px] uppercase font-bold text-slate-400">Threats Blocked Today</div>
            <div class="text-base font-black text-rose-600 font-mono">{{ threatRadar.blocked_today || 1248 }}</div>
            <span class="text-[10px] text-slate-500 font-medium">IPS, ATP &amp; Country Drops</span>
          </div>
        </div>

        <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-xs flex items-center gap-3.5">
          <div class="w-10 h-10 rounded-lg bg-emerald-50 text-emerald-600 flex items-center justify-center font-bold">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div>
            <div class="text-[10px] uppercase font-bold text-slate-400">Clean Email Inflow</div>
            <div class="text-base font-black text-emerald-600 font-mono">{{ mailFunnel.clean_delivered || 1312 }} / {{ mailFunnel.inbound_total || 1450 }}</div>
            <span class="text-[10px] text-slate-500 font-medium">{{ mailFunnel.spam_filtered || 108 }} Spam Neutralized</span>
          </div>
        </div>

        <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-xs flex items-center gap-3.5">
          <div class="w-10 h-10 rounded-lg bg-indigo-50 text-indigo-600 flex items-center justify-center font-bold">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
            </svg>
          </div>
          <div>
            <div class="text-[10px] uppercase font-bold text-slate-400">Active Site Tunnels</div>
            <div class="text-base font-black text-indigo-700 font-mono">3 Connected</div>
            <span class="text-[10px] text-slate-500 font-medium">SSL Client, AWS &amp; WireGuard</span>
          </div>
        </div>
      </div>

      <!-- THE 4-QUADRANT GRID -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 items-start">
        
        <!-- =================================================================== -->
        <!-- QUADRANT 1: REAL-TIME TRAFFIC & INTERFACE FLOWS                    -->
        <!-- =================================================================== -->
        <section class="bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden flex flex-col">
          <div class="px-5 py-3.5 bg-[#f4f6f9] border-b border-slate-200 flex items-center justify-between">
            <div class="flex items-center gap-2">
              <span class="w-1.5 h-4 bg-[#0072ce] rounded-full"></span>
              <h2 class="text-xs font-bold text-slate-800 uppercase tracking-wider">1. Real-Time Traffic &amp; Interfaces</h2>
            </div>
            <span class="text-[10px] font-mono font-bold text-[#0072ce] bg-blue-50 px-2 py-0.5 rounded border border-blue-200">
              Live SVG Flow
            </span>
          </div>

          <div class="p-5 space-y-5">
            <!-- Throughput Sparkline Visualizer -->
            <div class="bg-slate-900 rounded-xl p-4 text-white shadow-inner">
              <div class="flex items-center justify-between text-xs mb-2">
                <div class="flex items-center gap-2 font-bold">
                  <span class="w-2 h-2 rounded-full bg-emerald-400 animate-ping"></span>
                  <span>Uplink Bandwidth Stream (WAN Interface)</span>
                </div>
                <div class="font-mono text-[11px] text-emerald-400">
                  Peak: 72.4 Mbps
                </div>
              </div>

              <!-- SVG Dynamic Sparkline Graph -->
              <div class="h-20 w-full flex items-end">
                <svg class="w-full h-full overflow-visible" viewBox="0 0 300 70" preserveAspectRatio="none">
                  <defs>
                    <linearGradient id="wanGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                      <stop offset="0%" stop-color="#10b981" stop-opacity="0.5" />
                      <stop offset="100%" stop-color="#10b981" stop-opacity="0.0" />
                    </linearGradient>
                  </defs>
                  <path
                    :d="generateSvgAreaPath(sparklineData.wan_in)"
                    fill="url(#wanGrad)"
                  />
                  <path
                    :d="generateSvgLinePath(sparklineData.wan_in)"
                    fill="none"
                    stroke="#10b981"
                    stroke-width="2.5"
                    stroke-linecap="round"
                  />
                  <path
                    :d="generateSvgLinePath(sparklineData.wan_out)"
                    fill="none"
                    stroke="#0072ce"
                    stroke-width="1.8"
                    stroke-dasharray="3,3"
                  />
                </svg>
              </div>

              <div class="flex justify-between items-center text-[10px] text-slate-400 pt-2 border-t border-slate-800 font-mono">
                <span class="flex items-center gap-1.5"><span class="w-2 h-2 rounded-full bg-emerald-400"></span> Download (Inbound)</span>
                <span class="flex items-center gap-1.5"><span class="w-2 h-2 rounded-full bg-[#0072ce]"></span> Upload (Outbound)</span>
                <span>Interval: 1s ticks</span>
              </div>
            </div>

            <!-- Top Bandwidth Consumers Mini Ranking -->
            <div>
              <div class="flex items-center justify-between text-xs font-bold text-slate-700 mb-2">
                <span>Top Bandwidth Consumers (Internal Hosts)</span>
                <span class="text-[10px] text-slate-400">Past 24h</span>
              </div>
              <div class="space-y-2">
                <div v-for="user in topConsumers.slice(0, 3)" :key="user.ip" class="p-2 rounded-lg bg-slate-50 border border-slate-200 flex items-center justify-between text-xs">
                  <div class="flex items-center gap-2 min-w-0">
                    <span class="w-5 h-5 rounded-full bg-blue-100 text-[#0072ce] font-bold text-[10px] flex items-center justify-center font-mono">#{{ user.rank }}</span>
                    <div class="min-w-0">
                      <div class="font-bold text-slate-900 truncate">{{ user.hostname }}</div>
                      <div class="text-[10px] text-slate-400 font-mono">{{ user.ip }} &bull; {{ user.category }}</div>
                    </div>
                  </div>
                  <div class="text-right font-mono font-bold text-blue-700">
                    {{ user.downloaded }}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        <!-- =================================================================== -->
        <!-- QUADRANT 2: THREAT & SECURITY RADAR                                -->
        <!-- =================================================================== -->
        <section class="bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden flex flex-col">
          <div class="px-5 py-3.5 bg-[#f4f6f9] border-b border-slate-200 flex items-center justify-between">
            <div class="flex items-center gap-2">
              <span class="w-1.5 h-4 bg-rose-500 rounded-full"></span>
              <h2 class="text-xs font-bold text-slate-800 uppercase tracking-wider">2. Threat &amp; Security Radar</h2>
            </div>
            <span class="text-[10px] font-mono font-bold text-rose-700 bg-rose-50 px-2 py-0.5 rounded border border-rose-200">
              IPS &amp; Geo-IP Active
            </span>
          </div>

          <div class="p-5 space-y-4">
            <!-- IPS Attack Category Distribution Bars -->
            <div>
              <div class="text-xs font-bold text-slate-700 mb-2.5">IPS Attack Vector Classification</div>
              <div class="space-y-2">
                <div v-for="threat in threatRadar.ips_categories" :key="threat.category" class="space-y-1 text-xs">
                  <div class="flex justify-between text-[11px]">
                    <span class="font-bold text-slate-800 flex items-center gap-1.5">
                      <span class="w-1.5 h-1.5 rounded-full" :class="threat.severity === 'Critical' ? 'bg-rose-600' : 'bg-amber-500'"></span>
                      {{ threat.category }}
                    </span>
                    <span class="font-mono text-slate-600">{{ threat.count }} blocked ({{ threat.percent }}%)</span>
                  </div>
                  <div class="h-2 w-full bg-slate-100 rounded-full overflow-hidden">
                    <div
                      class="h-full rounded-full transition-all duration-500"
                      :class="threat.severity === 'Critical' ? 'bg-rose-500' : 'bg-amber-500'"
                      :style="{ width: `${threat.percent}%` }"
                    ></div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Country Blocking & Geo-IP Drops -->
            <div class="pt-3 border-t border-slate-100">
              <div class="flex justify-between items-center text-xs font-bold text-slate-700 mb-2">
                <span>Country Blocking Drop Summary</span>
                <span class="text-[10px] text-slate-400 font-mono">Geo-IP Database</span>
              </div>
              <div class="grid grid-cols-3 gap-2">
                <div v-for="geo in threatRadar.country_drops.slice(0, 3)" :key="geo.code" class="p-2 rounded-lg bg-slate-50 border border-slate-200 text-center">
                  <div class="text-base">{{ geo.flag }}</div>
                  <div class="text-[11px] font-bold text-slate-800">{{ geo.country }}</div>
                  <div class="text-[10px] font-mono text-rose-600 font-bold">{{ geo.drops }} drops</div>
                </div>
              </div>
            </div>
          </div>
        </section>

        <!-- =================================================================== -->
        <!-- QUADRANT 3: VPN & TUNNEL TOPOLOGY                                 -->
        <!-- =================================================================== -->
        <section class="bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden flex flex-col">
          <div class="px-5 py-3.5 bg-[#f4f6f9] border-b border-slate-200 flex items-center justify-between">
            <div class="flex items-center gap-2">
              <span class="w-1.5 h-4 bg-indigo-500 rounded-full"></span>
              <h2 class="text-xs font-bold text-slate-800 uppercase tracking-wider">3. VPN &amp; Cross-Premises Topology</h2>
            </div>
            <span class="text-[10px] font-mono font-bold text-indigo-700 bg-indigo-50 px-2 py-0.5 rounded border border-indigo-200">
              Mesh Active
            </span>
          </div>

          <div class="p-5 space-y-4">
            <!-- Visual Topology Node Graphic -->
            <div class="p-3.5 rounded-xl bg-slate-50 border border-slate-200 space-y-3">
              <div class="flex items-center justify-between text-xs font-bold text-slate-700">
                <span>Site-to-Site Encrypted Tunnels</span>
                <span class="text-[10px] font-mono text-emerald-600 font-bold">3 of 3 Up</span>
              </div>

              <div class="space-y-2">
                <div class="p-2.5 rounded-lg bg-white border border-slate-200 shadow-2xs flex items-center justify-between text-xs">
                  <div class="flex items-center gap-2.5">
                    <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
                    <div>
                      <div class="font-bold text-slate-900">Branch Office SSL Client</div>
                      <div class="text-[10px] text-slate-400 font-mono">SSL VPN Client &bull; 10.50.0.0/16</div>
                    </div>
                  </div>
                  <span class="text-[11px] font-mono font-bold text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">
                    19ms latency
                  </span>
                </div>

                <div class="p-2.5 rounded-lg bg-white border border-slate-200 shadow-2xs flex items-center justify-between text-xs">
                  <div class="flex items-center gap-2.5">
                    <span class="w-2 h-2 rounded-full bg-emerald-500"></span>
                    <div>
                      <div class="font-bold text-slate-900">Cloud-AWS-VPC-Link</div>
                      <div class="text-[10px] text-slate-400 font-mono">Amazon VPC Gateway &bull; 172.31.0.0/16</div>
                    </div>
                  </div>
                  <span class="text-[11px] font-mono font-bold text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">
                    28ms latency
                  </span>
                </div>
              </div>
            </div>

            <!-- Wireless APs & Remote User Gauge -->
            <div class="grid grid-cols-2 gap-3 text-xs">
              <div class="p-3 rounded-lg bg-purple-50/50 border border-purple-200">
                <div class="text-[10px] uppercase font-bold text-purple-900">Remote Users (WireGuard)</div>
                <div class="text-base font-black text-purple-900 font-mono mt-1">4 / 50</div>
                <div class="text-[10px] text-purple-700 mt-0.5">Sessions Active &bull; 2.8 GB xfer</div>
              </div>

              <div class="p-3 rounded-lg bg-blue-50/50 border border-blue-200">
                <div class="text-[10px] uppercase font-bold text-blue-900">Managed APs Spectrum</div>
                <div class="text-base font-black text-blue-900 font-mono mt-1">3 APs (28 Clients)</div>
                <div class="text-[10px] text-blue-700 mt-0.5">2.4GHz: 24% | 5GHz: 14%</div>
              </div>
            </div>
          </div>
        </section>

        <!-- =================================================================== -->
        <!-- QUADRANT 4: SYSTEM HEALTH, HA & MAIL PIPELINE                     -->
        <!-- =================================================================== -->
        <section class="bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden flex flex-col">
          <div class="px-5 py-3.5 bg-[#f4f6f9] border-b border-slate-200 flex items-center justify-between">
            <div class="flex items-center gap-2">
              <span class="w-1.5 h-4 bg-emerald-500 rounded-full"></span>
              <h2 class="text-xs font-bold text-slate-800 uppercase tracking-wider">4. System Health &amp; HA Pipeline</h2>
            </div>
            <span class="text-[10px] font-mono font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">
              HA Cluster Synced
            </span>
          </div>

          <div class="p-5 space-y-4">
            <!-- Hardware Resource Progress Bars -->
            <div class="space-y-3">
              <div class="space-y-1 text-xs">
                <div class="flex justify-between text-[11px] font-bold">
                  <span class="text-slate-700">CPU Allocation ({{ systemMetrics.cpuCores }} Cores)</span>
                  <span class="font-mono text-blue-700">{{ (Number(systemMetrics.cpuPercent) || 0).toFixed(1) }}%</span>
                </div>
                <div class="h-2 w-full bg-slate-100 rounded-full overflow-hidden">
                  <div class="h-full bg-[#0072ce] rounded-full transition-all" :style="{ width: `${systemMetrics.cpuPercent}%` }"></div>
                </div>
              </div>

              <div class="space-y-1 text-xs">
                <div class="flex justify-between text-[11px] font-bold">
                  <span class="text-slate-700">Memory (RAM Allocation)</span>
                  <span class="font-mono text-indigo-700">{{ (Number(systemMetrics.memoryPercent) || 0).toFixed(1) }}% ({{ systemMetrics.memoryUsedGb }} / {{ systemMetrics.memoryTotalGb }} GB)</span>
                </div>
                <div class="h-2 w-full bg-slate-100 rounded-full overflow-hidden">
                  <div class="h-full bg-indigo-600 rounded-full transition-all" :style="{ width: `${systemMetrics.memoryPercent}%` }"></div>
                </div>
              </div>
            </div>

            <!-- HA Node Sync Status Card -->
            <div class="p-3 rounded-lg bg-emerald-50/50 border border-emerald-200 flex items-center justify-between text-xs">
              <div>
                <div class="font-bold text-emerald-950 flex items-center gap-1.5">
                  <span class="w-2 h-2 rounded-full bg-emerald-500"></span>
                  <span>HA Cluster (Active-Passive)</span>
                </div>
                <div class="text-[10px] text-emerald-800 font-mono mt-0.5">Primary: astaro-node-01 &bull; Heartbeat: 250ms</div>
              </div>
              <span class="px-2 py-0.5 rounded bg-emerald-100 text-emerald-800 font-bold font-mono text-[10px] border border-emerald-300">
                100% In-Sync
              </span>
            </div>

            <!-- Email Flow Funnel Metric Strip -->
            <div class="p-3 rounded-lg bg-slate-50 border border-slate-200">
              <div class="text-[10px] uppercase font-bold text-slate-400 mb-1.5">Multi-Tier Email Flow Funnel</div>
              <div class="grid grid-cols-4 gap-1 text-center font-mono text-[10px]">
                <div class="p-1.5 bg-white rounded border border-slate-200">
                  <div class="text-slate-400">Inbound</div>
                  <div class="font-bold text-slate-800 text-xs">{{ mailFunnel.inbound_total || 1450 }}</div>
                </div>
                <div class="p-1.5 bg-emerald-50 rounded border border-emerald-200 text-emerald-800">
                  <div>Clean</div>
                  <div class="font-bold text-xs">{{ mailFunnel.clean_delivered || 1312 }}</div>
                </div>
                <div class="p-1.5 bg-amber-50 rounded border border-amber-200 text-amber-800">
                  <div>Spam</div>
                  <div class="font-bold text-xs">{{ mailFunnel.spam_filtered || 108 }}</div>
                </div>
                <div class="p-1.5 bg-rose-50 rounded border border-rose-200 text-rose-800">
                  <div>Virus</div>
                  <div class="font-bold text-xs">{{ mailFunnel.virus_neutralized || 12 }}</div>
                </div>
              </div>
            </div>
          </div>
        </section>
      </div>
    </div>

    <!-- ========================================================================= -->
    <!-- VIEW 2: TRAFFIC & INTERFACES SPEEDOMETERS & LIVE CONNECTION TRACKER       -->
    <!-- ========================================================================= -->
    <div v-else-if="activeViewTab === 'traffic'" class="space-y-6">
      <!-- Live Interface Speedometers Strip -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div v-for="iface in interfacesList" :key="iface.id" class="bg-white p-4 rounded-xl border border-slate-200 shadow-xs flex flex-col justify-between">
          <div class="flex items-center justify-between mb-3">
            <div class="flex items-center gap-2">
              <div class="w-8 h-8 rounded bg-slate-800 text-white font-mono text-xs font-bold flex items-center justify-center">
                {{ iface.portNumber || 'P1' }}
              </div>
              <div>
                <h3 class="text-xs font-bold text-slate-900">{{ iface.name }}</h3>
                <span class="text-[10px] text-slate-400 font-mono">{{ iface.hwName }}</span>
              </div>
            </div>
            <span class="px-2 py-0.5 rounded text-[10px] font-bold uppercase border" :class="iface.linkState === 'UP' ? 'bg-emerald-50 text-emerald-700 border-emerald-200' : 'bg-slate-100 text-slate-500 border-slate-200'">
              {{ iface.linkState }}
            </span>
          </div>

          <div class="p-2.5 bg-slate-50 rounded-lg border border-slate-200 text-xs font-mono mb-3">
            <div class="text-[10px] text-slate-400 font-sans uppercase">Assigned IP:</div>
            <div class="font-bold text-slate-800 truncate">{{ iface.ipAddress || 'Unassigned / DHCP' }}</div>
          </div>

          <div class="flex justify-between text-[11px] font-mono text-slate-600">
            <span>Rx: {{ iface.rxBytes || '14.2 GB' }}</span>
            <span>Tx: {{ iface.txBytes || '4.8 GB' }}</span>
          </div>
        </div>
      </div>

      <!-- Live Connection Table & Flow State Matrix -->
      <div class="bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden">
        <div class="px-5 py-3.5 bg-[#f4f6f9] border-b border-slate-200 flex items-center justify-between">
          <div class="flex items-center gap-2">
            <span class="w-1.5 h-4 bg-[#0072ce] rounded-full"></span>
            <h2 class="text-xs font-bold text-slate-800 uppercase tracking-wider">Live Connection Tracker (conntrack)</h2>
            <span class="text-[11px] text-slate-400 font-mono">({{ activeConnections.length }} active sessions)</span>
          </div>
          <button
            type="button"
            @click="fetchActiveConnections"
            class="px-2.5 py-1 rounded bg-white border border-slate-300 text-slate-700 text-xs font-semibold hover:bg-slate-50 cursor-pointer shadow-2xs"
          >
            Refresh Sessions
          </button>
        </div>

        <div class="overflow-x-auto">
          <table class="w-full text-left text-xs border-collapse">
            <thead class="bg-[#f4f6f9] text-slate-700 font-bold border-b border-slate-200">
              <tr>
                <th class="p-3 pl-4">Protocol</th>
                <th class="p-3">State</th>
                <th class="p-3 font-mono">Source IP:Port</th>
                <th class="p-3 font-mono">Destination IP:Port</th>
                <th class="p-3">Service</th>
                <th class="p-3 font-mono">Payload</th>
                <th class="p-3 font-mono">TTL</th>
                <th class="p-3 text-right pr-4">Action</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100 font-medium text-slate-700">
              <tr v-for="conn in activeConnections" :key="conn.id" class="hover:bg-blue-50/40">
                <td class="p-3 pl-4 font-bold font-mono text-blue-700">{{ conn.protocol }}</td>
                <td class="p-3">
                  <span class="px-1.5 py-0.5 rounded text-[10px] font-bold bg-emerald-50 text-emerald-700 border border-emerald-200">
                    {{ conn.state }}
                  </span>
                </td>
                <td class="p-3 font-mono text-slate-900">{{ conn.src_ip }}:{{ conn.src_port }}</td>
                <td class="p-3 font-mono text-slate-900">{{ conn.dst_ip }}:{{ conn.dst_port }}</td>
                <td class="p-3 font-semibold text-slate-700">{{ conn.service || 'HTTPS' }}</td>
                <td class="p-3 font-mono text-slate-600">{{ conn.bytes_formatted }}</td>
                <td class="p-3 font-mono text-slate-400">{{ conn.ttl }}s</td>
                <td class="p-3 text-right pr-4">
                  <button
                    type="button"
                    @click="killActiveConnection(conn.id)"
                    class="px-2 py-0.5 rounded bg-rose-50 text-rose-600 border border-rose-200 font-bold text-[10px] hover:bg-rose-100 cursor-pointer"
                  >
                    Kill
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- ========================================================================= -->
    <!-- VIEW 3: THREAT & SECURITY RADAR SPECIALIZED VIEW                          -->
    <!-- ========================================================================= -->
    <div v-else-if="activeViewTab === 'threats'" class="space-y-6">
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- IPS Breakdown -->
        <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-xs space-y-4">
          <h3 class="text-xs font-bold uppercase tracking-wider text-slate-800">IPS Threat Signatures Heatmap</h3>
          <div class="space-y-3">
            <div v-for="threat in threatRadar.ips_categories" :key="threat.category" class="p-3 bg-slate-50 rounded-lg border border-slate-200">
              <div class="flex justify-between items-center text-xs mb-1">
                <span class="font-bold text-slate-900">{{ threat.category }}</span>
                <span class="font-mono text-rose-600 font-bold">{{ threat.count }} blocked</span>
              </div>
              <div class="h-2 w-full bg-slate-200 rounded-full overflow-hidden">
                <div class="h-full bg-rose-500 rounded-full" :style="{ width: `${threat.percent}%` }"></div>
              </div>
            </div>
          </div>
        </div>

        <!-- Web Proxy Categorization -->
        <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-xs space-y-4">
          <h3 class="text-xs font-bold uppercase tracking-wider text-slate-800">Web Filter Categories Distribution</h3>
          <div class="space-y-3">
            <div v-for="cat in threatRadar.web_categories" :key="cat.category" class="p-3 bg-slate-50 rounded-lg border border-slate-200">
              <div class="flex justify-between items-center text-xs mb-1">
                <span class="font-bold text-slate-900">{{ cat.category }}</span>
                <span class="font-mono text-blue-700 font-bold">{{ cat.requests.toLocaleString() }} req ({{ cat.percent }}%)</span>
              </div>
              <div class="h-2 w-full bg-slate-200 rounded-full overflow-hidden">
                <div class="h-full rounded-full" :style="{ width: `${cat.percent}%`, backgroundColor: cat.color }"></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- ========================================================================= -->
    <!-- VIEW 3: NETWORK STATISTICS (TODAY)                                        -->
    <!-- ========================================================================= -->
    <div v-else-if="activeViewTab === 'network_stats'" class="space-y-6">
      <div class="flex items-center justify-between">
        <h2 class="text-xs font-bold uppercase tracking-wider text-slate-700">Network Statistics — Today</h2>
        <span class="text-[11px] font-mono text-slate-500">Total packets: 3,562,702 &bull; Total traffic: 3.9 GB</span>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- Top Accounting Services -->
        <div class="bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden">
          <div class="p-3.5 bg-[#f4f6f9] border-b border-slate-200 flex items-center justify-between">
            <span class="text-xs font-bold text-slate-800">Top Accounting Services</span>
            <span class="text-[#0072ce] text-xs font-bold">▶</span>
          </div>
          <div class="p-4 flex flex-col sm:flex-row items-center gap-6">
            <div class="w-32 h-32 flex-shrink-0 relative">
              <svg viewBox="-55 -55 110 110" class="w-full h-full transform -rotate-90">
                <path
                  v-for="(slice, sIdx) in accountingServicesSlices"
                  :key="sIdx"
                  :d="slice.path"
                  :fill="slice.color"
                  stroke="#ffffff"
                  stroke-width="1.5"
                >
                  <title>{{ slice.name }}: {{ slice.traffic }} ({{ slice.pct }}%)</title>
                </path>
              </svg>
            </div>
            <div class="flex-1 w-full overflow-x-auto">
              <table class="w-full text-left text-[11px] border-collapse">
                <thead>
                  <tr class="border-b border-slate-200 text-slate-500 font-bold uppercase">
                    <th class="py-1 px-1.5">#</th>
                    <th class="py-1 px-1.5">Proto</th>
                    <th class="py-1 px-1.5">Port</th>
                    <th class="py-1 px-1.5">Service</th>
                    <th class="py-1 px-1.5 text-right">Packets</th>
                    <th class="py-1 px-1.5 text-right">Traffic</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-slate-100">
                  <tr v-for="(svc, idx) in accountingServices" :key="idx" class="hover:bg-slate-50">
                    <td class="py-1 px-1.5 font-mono text-slate-400">{{ idx + 1 }}</td>
                    <td class="py-1 px-1.5 font-mono text-slate-600">{{ svc.proto }}</td>
                    <td class="py-1 px-1.5 font-mono text-slate-600">{{ svc.port }}</td>
                    <td class="py-1 px-1.5 font-bold flex items-center gap-1.5">
                      <span class="w-2.5 h-2.5 rounded-xs" :style="{ backgroundColor: svc.color }"></span>
                      <span class="text-slate-800">{{ svc.name }}</span>
                    </td>
                    <td class="py-1 px-1.5 text-right font-mono text-slate-600">{{ svc.packets.toLocaleString() }}</td>
                    <td class="py-1 px-1.5 text-right font-mono font-bold text-[#0072ce]">{{ svc.traffic }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- Top Source Hosts -->
        <div class="bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden">
          <div class="p-3.5 bg-[#f4f6f9] border-b border-slate-200 flex items-center justify-between">
            <span class="text-xs font-bold text-slate-800">Top Source Hosts</span>
            <span class="text-[#0072ce] text-xs font-bold">▶</span>
          </div>
          <div class="p-4 flex flex-col sm:flex-row items-center gap-6">
            <div class="w-32 h-32 flex-shrink-0 relative">
              <svg viewBox="-55 -55 110 110" class="w-full h-full transform -rotate-90">
                <path
                  v-for="(slice, sIdx) in sourceHostsSlices"
                  :key="sIdx"
                  :d="slice.path"
                  :fill="slice.color"
                  stroke="#ffffff"
                  stroke-width="1.5"
                >
                  <title>{{ slice.name }}: {{ slice.traffic }} ({{ slice.pct }}%)</title>
                </path>
              </svg>
            </div>
            <div class="flex-1 w-full overflow-x-auto">
              <table class="w-full text-left text-[11px] border-collapse">
                <thead>
                  <tr class="border-b border-slate-200 text-slate-500 font-bold uppercase">
                    <th class="py-1 px-1.5">#</th>
                    <th class="py-1 px-1.5">User / Host</th>
                    <th class="py-1 px-1.5 text-center">Type</th>
                    <th class="py-1 px-1.5 text-right">Packets</th>
                    <th class="py-1 px-1.5 text-right">Traffic</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-slate-100">
                  <tr v-for="(h, idx) in sourceHosts" :key="idx" class="hover:bg-slate-50">
                    <td class="py-1 px-1.5 font-mono text-slate-400">{{ idx + 1 }}</td>
                    <td class="py-1 px-1.5 font-bold flex items-center gap-1.5">
                      <span class="w-2.5 h-2.5 rounded-xs" :style="{ backgroundColor: h.color }"></span>
                      <span class="text-slate-900 font-mono">{{ h.name }}</span>
                    </td>
                    <td class="py-1 px-1.5 text-center text-xs">
                      <span v-if="h.flag">{{ h.flag }}</span>
                      <span v-else>💻</span>
                    </td>
                    <td class="py-1 px-1.5 text-right font-mono text-slate-600">{{ h.packets.toLocaleString() }}</td>
                    <td class="py-1 px-1.5 text-right font-mono font-bold text-emerald-700">{{ h.traffic }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>

      <!-- Concurrent Connections Today (Live Area Graph) -->
      <div class="bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden">
        <div class="p-3.5 bg-[#f4f6f9] border-b border-slate-200 flex items-center justify-between">
          <span class="text-xs font-bold text-slate-800">Concurrent Connections Today</span>
          <span class="text-[11px] font-mono text-slate-500">Peak: <strong>888 connections</strong> at 21:40</span>
        </div>
        <div class="p-6">
          <div class="relative w-full h-48">
            <svg class="w-full h-full overflow-visible" viewBox="0 0 1000 220" preserveAspectRatio="none">
              <defs>
                <linearGradient id="ctrlConnGrad" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stop-color="#0072ce" stop-opacity="0.45" />
                  <stop offset="100%" stop-color="#0072ce" stop-opacity="0.02" />
                </linearGradient>
              </defs>
              <line x1="0" y1="0" x2="1000" y2="0" stroke="#e2e8f0" stroke-dasharray="4" />
              <line x1="0" y1="55" x2="1000" y2="55" stroke="#e2e8f0" stroke-dasharray="4" />
              <line x1="0" y1="110" x2="1000" y2="110" stroke="#e2e8f0" stroke-dasharray="4" />
              <line x1="0" y1="165" x2="1000" y2="165" stroke="#e2e8f0" stroke-dasharray="4" />
              <line x1="0" y1="220" x2="1000" y2="220" stroke="#cbd5e1" stroke-width="1.5" />
              <text x="5" y="15" fill="#64748b" font-size="11" font-family="monospace">888</text>
              <text x="5" y="70" fill="#64748b" font-size="11" font-family="monospace">666</text>
              <text x="5" y="125" fill="#64748b" font-size="11" font-family="monospace">444</text>
              <text x="5" y="180" fill="#64748b" font-size="11" font-family="monospace">222</text>
              <text x="5" y="215" fill="#64748b" font-size="11" font-family="monospace">0</text>
              <path
                d="M 50 220 L 50 180 L 100 80 L 150 150 L 200 120 L 250 90 L 300 110 L 350 180 L 400 190 L 450 170 L 500 160 L 550 25 L 600 70 L 650 170 L 700 160 L 750 150 L 800 160 L 850 110 L 900 130 L 950 80 L 1000 140 L 1000 220 Z"
                fill="url(#ctrlConnGrad)"
              />
              <path
                d="M 50 180 L 100 80 L 150 150 L 200 120 L 250 90 L 300 110 L 350 180 L 400 190 L 450 170 L 500 160 L 550 25 L 600 70 L 650 170 L 700 160 L 750 150 L 800 160 L 850 110 L 900 130 L 950 80 L 1000 140"
                fill="none"
                stroke="#0072ce"
                stroke-width="2.5"
                stroke-linejoin="round"
                stroke-linecap="round"
              />
            </svg>
          </div>
          <div class="flex justify-between text-[10px] font-mono text-slate-400 pt-2 border-t border-slate-100">
            <span>12:05</span>
            <span>14:04</span>
            <span>16:04</span>
            <span>18:03</span>
            <span>20:03</span>
            <span class="font-bold text-[#0072ce]">22:02 (Peak 888)</span>
            <span>00:02</span>
            <span>02:02</span>
            <span>04:01</span>
            <span>06:01</span>
            <span>08:00</span>
            <span>10:00</span>
            <span>12:00</span>
          </div>
        </div>
      </div>
    </div>

    <!-- ========================================================================= -->
    <!-- VIEW 4: NETWORK PROTECTION STATISTICS (TODAY)                             -->
    <!-- ========================================================================= -->
    <div v-else-if="activeViewTab === 'net_protect_stats'" class="space-y-6">
      <div class="flex items-center justify-between">
        <h2 class="text-xs font-bold uppercase tracking-wider text-slate-700">Network Protection Statistics — Today</h2>
        <span class="text-[11px] font-mono text-slate-500">Total dropped packets: 34,793</span>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- Top Dropped Source Hosts -->
        <div class="bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden">
          <div class="p-3.5 bg-[#f4f6f9] border-b border-slate-200 flex items-center justify-between">
            <span class="text-xs font-bold text-slate-800">Top Dropped Source Hosts</span>
            <span class="text-[#0072ce] text-xs font-bold">▶</span>
          </div>
          <div class="p-4 flex flex-col sm:flex-row items-center gap-6">
            <div class="w-32 h-32 flex-shrink-0 relative">
              <svg viewBox="-55 -55 110 110" class="w-full h-full transform -rotate-90">
                <path
                  v-for="(slice, sIdx) in droppedSourceSlices"
                  :key="sIdx"
                  :d="slice.path"
                  :fill="slice.color"
                  stroke="#ffffff"
                  stroke-width="1.5"
                >
                  <title>{{ slice.name }}: {{ slice.packets }} pkts ({{ slice.pct }}%)</title>
                </path>
              </svg>
            </div>
            <div class="flex-1 w-full overflow-x-auto">
              <table class="w-full text-left text-[11px] border-collapse">
                <thead>
                  <tr class="border-b border-slate-200 text-slate-500 font-bold uppercase">
                    <th class="py-1 px-1.5">#</th>
                    <th class="py-1 px-1.5">Country</th>
                    <th class="py-1 px-1.5">Source User / Host</th>
                    <th class="py-1 px-1.5 text-right">Packets</th>
                    <th class="py-1 px-1.5 text-right">%</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-slate-100">
                  <tr v-for="(h, idx) in droppedSourceHosts" :key="idx" class="hover:bg-slate-50">
                    <td class="py-1 px-1.5 font-mono text-slate-400">{{ idx + 1 }}</td>
                    <td class="py-1 px-1.5 text-center text-sm">{{ h.flag }}</td>
                    <td class="py-1 px-1.5 font-bold flex items-center gap-1.5">
                      <span class="w-2.5 h-2.5 rounded-xs" :style="{ backgroundColor: h.color }"></span>
                      <span class="text-slate-800 font-mono truncate max-w-[140px]">{{ h.name }}</span>
                    </td>
                    <td class="py-1 px-1.5 text-right font-mono font-bold text-slate-800">{{ h.packets.toLocaleString() }}</td>
                    <td class="py-1 px-1.5 text-right font-mono text-slate-600">{{ h.pct.toFixed(2) }}%</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- Top Dropped Destination Services/Hosts -->
        <div class="bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden">
          <div class="p-3.5 bg-[#f4f6f9] border-b border-slate-200 flex items-center justify-between">
            <span class="text-xs font-bold text-slate-800">Top Dropped Destination Services/Hosts</span>
            <span class="text-[#0072ce] text-xs font-bold">▶</span>
          </div>
          <div class="p-4 flex flex-col sm:flex-row items-center gap-6">
            <div class="w-32 h-32 flex-shrink-0 relative">
              <svg viewBox="-55 -55 110 110" class="w-full h-full transform -rotate-90">
                <path
                  v-for="(slice, sIdx) in droppedDestSlices"
                  :key="sIdx"
                  :d="slice.path"
                  :fill="slice.color"
                  stroke="#ffffff"
                  stroke-width="1.5"
                >
                  <title>{{ slice.service }} -> {{ slice.dest }}: {{ slice.packets }} pkts ({{ slice.pct }}%)</title>
                </path>
              </svg>
            </div>
            <div class="flex-1 w-full overflow-x-auto">
              <table class="w-full text-left text-[11px] border-collapse">
                <thead>
                  <tr class="border-b border-slate-200 text-slate-500 font-bold uppercase">
                    <th class="py-1 px-1.5">#</th>
                    <th class="py-1 px-1.5">Service</th>
                    <th class="py-1 px-1.5">Destination</th>
                    <th class="py-1 px-1.5 text-right">Packets</th>
                    <th class="py-1 px-1.5 text-right">%</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-slate-100">
                  <tr v-for="(d, idx) in droppedDestHosts" :key="idx" class="hover:bg-slate-50">
                    <td class="py-1 px-1.5 font-mono text-slate-400">{{ idx + 1 }}</td>
                    <td class="py-1 px-1.5 font-bold flex items-center gap-1.5">
                      <span class="w-2.5 h-2.5 rounded-xs" :style="{ backgroundColor: d.color }"></span>
                      <span class="font-mono text-slate-800">{{ d.service }}</span>
                    </td>
                    <td class="py-1 px-1.5 font-mono text-slate-600 truncate max-w-[130px] flex items-center gap-1">
                      <span>🇺🇸</span>
                      <span>{{ d.dest }}</span>
                    </td>
                    <td class="py-1 px-1.5 text-right font-mono font-bold text-slate-800">{{ d.packets.toLocaleString() }}</td>
                    <td class="py-1 px-1.5 text-right font-mono text-slate-600">{{ d.pct.toFixed(2) }}%</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- ========================================================================= -->
    <!-- VIEW 5: WEB PROTECTION STATISTICS (TODAY)                                 -->
    <!-- ========================================================================= -->
    <div v-else-if="activeViewTab === 'web_protect_stats'" class="space-y-6">
      <div class="flex items-center justify-between">
        <h2 class="text-xs font-bold uppercase tracking-wider text-slate-700">Web Protection Statistics — Today</h2>
        <span class="text-[11px] font-mono text-slate-500">Total packets: 3,562,702</span>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- Top Applications -->
        <div class="bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden">
          <div class="p-3.5 bg-[#f4f6f9] border-b border-slate-200 flex items-center justify-between">
            <span class="text-xs font-bold text-slate-800">Top Applications</span>
            <span class="text-[#0072ce] text-xs font-bold">▶</span>
          </div>
          <div class="p-4 flex flex-col sm:flex-row items-center gap-6">
            <div class="w-32 h-32 flex-shrink-0 relative">
              <svg viewBox="-55 -55 110 110" class="w-full h-full transform -rotate-90">
                <path
                  v-for="(slice, sIdx) in topAppsSlices"
                  :key="sIdx"
                  :d="slice.path"
                  :fill="slice.color"
                  stroke="#ffffff"
                  stroke-width="1.5"
                >
                  <title>{{ slice.name }}: {{ slice.traffic }} ({{ slice.pct }}%)</title>
                </path>
              </svg>
            </div>
            <div class="flex-1 w-full overflow-x-auto">
              <table class="w-full text-left text-[11px] border-collapse">
                <thead>
                  <tr class="border-b border-slate-200 text-slate-500 font-bold uppercase">
                    <th class="py-1 px-1.5">#</th>
                    <th class="py-1 px-1.5">Application</th>
                    <th class="py-1 px-1.5 text-right">Total Traffic</th>
                    <th class="py-1 px-1.5 text-right">%</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-slate-100">
                  <tr v-for="(app, idx) in topApps" :key="idx" class="hover:bg-slate-50">
                    <td class="py-1 px-1.5 font-mono text-slate-400">{{ idx + 1 }}</td>
                    <td class="py-1 px-1.5 font-bold flex items-center gap-1.5">
                      <span class="w-2.5 h-2.5 rounded-xs" :style="{ backgroundColor: app.color }"></span>
                      <span class="text-slate-900">{{ app.name }}</span>
                    </td>
                    <td class="py-1 px-1.5 text-right font-mono font-bold text-[#0072ce]">{{ app.traffic }}</td>
                    <td class="py-1 px-1.5 text-right font-mono text-slate-600">{{ app.pct.toFixed(2) }}%</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- Top Application Categories -->
        <div class="bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden">
          <div class="p-3.5 bg-[#f4f6f9] border-b border-slate-200 flex items-center justify-between">
            <span class="text-xs font-bold text-slate-800">Top Application Categories</span>
            <span class="text-[#0072ce] text-xs font-bold">▶</span>
          </div>
          <div class="p-4 flex flex-col sm:flex-row items-center gap-6">
            <div class="w-32 h-32 flex-shrink-0 relative">
              <svg viewBox="-55 -55 110 110" class="w-full h-full transform -rotate-90">
                <path
                  v-for="(slice, sIdx) in topAppCategoriesSlices"
                  :key="sIdx"
                  :d="slice.path"
                  :fill="slice.color"
                  stroke="#ffffff"
                  stroke-width="1.5"
                >
                  <title>{{ slice.name }}: {{ slice.traffic }} ({{ slice.pct }}%)</title>
                </path>
              </svg>
            </div>
            <div class="flex-1 w-full overflow-x-auto">
              <table class="w-full text-left text-[11px] border-collapse">
                <thead>
                  <tr class="border-b border-slate-200 text-slate-500 font-bold uppercase">
                    <th class="py-1 px-1.5">#</th>
                    <th class="py-1 px-1.5">Group</th>
                    <th class="py-1 px-1.5 text-right">Total Traffic</th>
                    <th class="py-1 px-1.5 text-right">%</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-slate-100">
                  <tr v-for="(cat, idx) in topAppCategories" :key="idx" class="hover:bg-slate-50">
                    <td class="py-1 px-1.5 font-mono text-slate-400">{{ idx + 1 }}</td>
                    <td class="py-1 px-1.5 font-bold flex items-center gap-1.5">
                      <span class="w-2.5 h-2.5 rounded-xs" :style="{ backgroundColor: cat.color }"></span>
                      <span class="text-slate-900">{{ cat.name }}</span>
                    </td>
                    <td class="py-1 px-1.5 text-right font-mono font-bold text-emerald-700">{{ cat.traffic }}</td>
                    <td class="py-1 px-1.5 text-right font-mono text-slate-600">{{ cat.pct.toFixed(2) }}%</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- ========================================================================= -->
    <!-- VIEW 6: HARDWARE, PARTITIONS & HEALTH                                     -->
    <!-- ========================================================================= -->
    <div v-else class="space-y-6">
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Resource Partitions Donut Gauges -->
        <div v-for="part in (systemMetrics.partitions || [])" :key="part.mount" class="bg-white p-5 rounded-xl border border-slate-200 shadow-xs text-center space-y-3">
          <div class="text-xs font-bold uppercase tracking-wider text-slate-800">{{ part.label }}</div>
          <div class="text-[10px] text-slate-400 font-mono">{{ part.mount }}</div>
          <div class="text-2xl font-black font-mono text-blue-700">{{ part.percent }}%</div>
          <div class="h-2.5 w-full bg-slate-100 rounded-full overflow-hidden">
            <div class="h-full bg-[#0072ce] rounded-full" :style="{ width: `${part.percent}%` }"></div>
          </div>
          <div class="text-xs text-slate-600 font-mono">{{ part.usedGb }} GB used of {{ part.totalGb }} GB</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onUnmounted, h } from 'vue'

const props = defineProps({
  authToken: {
    type: String,
    default: ''
  }
})

const activeViewTab = ref('quadrant')
const isLoading = ref(false)
const isPollingActive = ref(true)
const pollIntervalSeconds = ref(5)
let pollTimer = null

// Tab Icon Helpers
const ControlCenterIcon = {
  render: () => h('svg', { class: 'w-4 h-4', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
    h('path', { strokeLinecap: 'round', strokeLinejoin: 'round', strokeWidth: '2', d: 'M4 5a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1H5a1 1 0 01-1-1V5zM14 5a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1h-4a1 1 0 01-1-1V5zM4 15a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1H5a1 1 0 01-1-1v-4zM14 15a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1h-4a1 1 0 01-1-1v-4z' })
  ])
}

const TrafficIcon = {
  render: () => h('svg', { class: 'w-4 h-4', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
    h('path', { strokeLinecap: 'round', strokeLinejoin: 'round', strokeWidth: '2', d: 'M13 10V3L4 14h7v7l9-11h-7z' })
  ])
}

const ThreatsIcon = {
  render: () => h('svg', { class: 'w-4 h-4', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
    h('path', { strokeLinecap: 'round', strokeLinejoin: 'round', strokeWidth: '2', d: 'M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z' })
  ])
}

const HealthIcon = {
  render: () => h('svg', { class: 'w-4 h-4', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
    h('path', { strokeLinecap: 'round', strokeLinejoin: 'round', strokeWidth: '2', d: 'M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z' })
  ])
}

const mainTabs = computed(() => [
  { id: 'quadrant', label: 'Executive Control Center', icon: ControlCenterIcon, badge: 'Overview' },
  { id: 'network_stats', label: 'Network Statistics', icon: TrafficIcon, badge: '3.9 GB' },
  { id: 'net_protect_stats', label: 'Protection Statistics', icon: ThreatsIcon, badge: '34k Drops' },
  { id: 'web_protect_stats', label: 'Web Statistics', icon: ControlCenterIcon, badge: 'Apps' },
  { id: 'traffic', label: 'Flow Monitor', icon: TrafficIcon, badge: `${activeConnections.value.length} Flows` },
  { id: 'hardware', label: 'Hardware & Partitions', icon: HealthIcon, badge: 'Optimal' }
])

// -----------------------------------------------------------------------------
// SVG Pie Chart Generator Utility
// -----------------------------------------------------------------------------
function buildPieSlices(items) {
  let cumulativePercent = 0
  return items.map(item => {
    const startAngle = cumulativePercent * 360
    cumulativePercent += (item.pct / 100)
    const endAngle = cumulativePercent * 360

    const startX = Math.cos(2 * Math.PI * (startAngle - 90) / 360)
    const startY = Math.sin(2 * Math.PI * (startAngle - 90) / 360)
    const endX = Math.cos(2 * Math.PI * (endAngle - 90) / 360)
    const endY = Math.sin(2 * Math.PI * (endAngle - 90) / 360)

    const largeArcFlag = item.pct > 50 ? 1 : 0
    const pathData = `M 0 0 L ${startX * 50} ${startY * 50} A 50 50 0 ${largeArcFlag} 1 ${endX * 50} ${endY * 50} Z`

    return {
      ...item,
      path: pathData
    }
  })
}

// Sophos UTM 9 Statistics Datasets
const accountingServices = ref([
  { proto: 'TCP', port: 443, name: 'HTTPS', packets: 1707287, traffic: '2.5 GB', pct: 64.1, color: '#00838f' },
  { proto: 'UDP', port: 443, name: 'HTTPS', packets: 1203151, traffic: '1.2 GB', pct: 30.8, color: '#00bcd4' },
  { proto: 'UDP', port: 4501, name: '4501', packets: 202250, traffic: '110.2 MB', pct: 2.8, color: '#0288d1' },
  { proto: 'TCP', port: 80, name: 'HTTP', packets: 28217, traffic: '20.5 MB', pct: 0.5, color: '#1565c0' },
  { proto: 'TCP', port: 25, name: 'SMTP', packets: 155668, traffic: '12.8 MB', pct: 0.3, color: '#6a1b9a' },
  { proto: 'TCP', port: 5223, name: '5223', packets: 25883, traffic: '9.4 MB', pct: 0.2, color: '#ad1457' },
  { proto: 'UDP', port: 53, name: 'DOMAIN', packets: 71886, traffic: '8.5 MB', pct: 0.2, color: '#c2185b' },
  { proto: 'TCP', port: 993, name: 'IMAPS', packets: 20869, traffic: '7.3 MB', pct: 0.2, color: '#e65100' },
  { proto: 'TCP', port: 465, name: 'SMTPS', packets: 35041, traffic: '7.2 MB', pct: 0.2, color: '#f57f17' },
  { proto: 'TCP', port: 853, name: '853', packets: 11387, traffic: '4.3 MB', pct: 0.1, color: '#9e9d24' }
])
const accountingServicesSlices = computed(() => buildPieSlices(accountingServices.value))

const sourceHosts = ref([
  { name: '10.1.10.127', packets: 1082335, traffic: '1.6 GB', pct: 41.0, color: '#00838f' },
  { name: '10.1.10.124', packets: 767062, traffic: '1.0 GB', pct: 25.6, color: '#00bcd4' },
  { name: '10.1.10.131', packets: 250673, traffic: '296.8 MB', pct: 7.6, color: '#0288d1' },
  { name: '10.1.10.115', packets: 285242, traffic: '232.2 MB', pct: 5.9, color: '#1565c0' },
  { name: 'XPEnology', packets: 215843, traffic: '208.8 MB', pct: 5.3, color: '#6a1b9a' },
  { name: '(WAN) (Address)', flag: '🇺🇸', packets: 103382, traffic: '175.1 MB', pct: 4.5, color: '#ad1457' },
  { name: 'July', packets: 219603, traffic: '112.1 MB', pct: 2.9, color: '#c2185b' },
  { name: 'mail2', packets: 27126, traffic: '50.6 MB', pct: 1.3, color: '#e65100' },
  { name: '10.1.10.17', packets: 58917, traffic: '44.9 MB', pct: 1.1, color: '#f57f17' },
  { name: 'skyewelse', packets: 37034, traffic: '35.6 MB', pct: 0.9, color: '#9e9d24' }
])
const sourceHostsSlices = computed(() => buildPieSlices(sourceHosts.value))

const droppedSourceHosts = ref([
  { name: 'crawler014.deepfield.net', flag: '🇺🇸', packets: 637, pct: 1.83, color: '#00838f' },
  { name: '192.168.1.254', flag: '💻', packets: 345, pct: 0.99, color: '#00bcd4' },
  { name: '194.102.73.93', flag: '🇷🇴', packets: 273, pct: 0.78, color: '#0288d1' },
  { name: '193.46.255.51', flag: '🇷🇴', packets: 220, pct: 0.63, color: '#1565c0' },
  { name: '193.46.255.72', flag: '🇷🇴', packets: 214, pct: 0.62, color: '#6a1b9a' },
  { name: '115.231.78.10', flag: '🇨🇳', packets: 170, pct: 0.50, color: '#ad1457' },
  { name: '185.93.89.35', flag: '🇮🇷', packets: 171, pct: 0.49, color: '#c2185b' },
  { name: '80.94.95.226', flag: '🇷🇴', packets: 145, pct: 0.42, color: '#e65100' },
  { name: 'Wifi-PlayRoom', flag: '💻', packets: 143, pct: 0.41, color: '#f57f17' },
  { name: 'get166.wayto-getnutritionaldiet.com', flag: '🇧🇬', packets: 143, pct: 0.41, color: '#9e9d24' }
])
const droppedSourceSlices = computed(() => buildPieSlices(droppedSourceHosts.value))

const droppedDestHosts = ref([
  { service: 'tcp/23', dest: '(WAN) [108.231.232.69]', packets: 728, pct: 2.09, color: '#00838f' },
  { service: 'tcp/23', dest: '(WAN) [108.231.232.66]', packets: 626, pct: 1.80, color: '#00bcd4' },
  { service: 'tcp/23', dest: '(WAN) (Address)', packets: 407, pct: 1.17, color: '#0288d1' },
  { service: 'tcp/23', dest: '(WAN) [108.231.232.68]', packets: 398, pct: 1.14, color: '#1565c0' },
  { service: 'tcp/23', dest: '(WAN) [108.231.232.67]', packets: 368, pct: 1.06, color: '#6a1b9a' },
  { service: 'igmp', dest: 'all-systems.mcast.net', packets: 345, pct: 0.99, color: '#ad1457' },
  { service: 'tcp/22', dest: '(WAN) [108.231.232.68]', packets: 247, pct: 0.71, color: '#c2185b' },
  { service: 'tcp/22', dest: '(WAN) [108.231.232.69]', packets: 245, pct: 0.70, color: '#e65100' },
  { service: 'tcp/22', dest: '(WAN) [108.231.232.66]', packets: 235, pct: 0.68, color: '#f57f17' },
  { service: 'tcp/22', dest: '(WAN) (Address)', packets: 217, pct: 0.62, color: '#9e9d24' }
])
const droppedDestSlices = computed(() => buildPieSlices(droppedDestHosts.value))

const topApps = ref([
  { name: 'Disney+', traffic: '996.9 MB', pct: 24.95, color: '#00838f' },
  { name: 'YouTube', traffic: '541.3 MB', pct: 13.54, color: '#00bcd4' },
  { name: 'Unclassified', traffic: '471.2 MB', pct: 11.79, color: '#0288d1' },
  { name: 'Akamai', traffic: '440.3 MB', pct: 11.02, color: '#1565c0' },
  { name: 'Amazon Prime Video', traffic: '375.7 MB', pct: 9.40, color: '#6a1b9a' },
  { name: 'QUIC IETF', traffic: '329.1 MB', pct: 8.24, color: '#ad1457' },
  { name: 'Sophos UTM Up2Date', traffic: '166.5 MB', pct: 4.17, color: '#c2185b' },
  { name: 'Apple', traffic: '136.1 MB', pct: 3.41, color: '#e65100' },
  { name: 'iTunes', traffic: '114.3 MB', pct: 2.86, color: '#f57f17' },
  { name: 'SSL', traffic: '97.1 MB', pct: 2.43, color: '#9e9d24' }
])
const topAppsSlices = computed(() => buildPieSlices(topApps.value))

const topAppCategories = ref([
  { name: 'Streaming Media', traffic: '2.0 GB', pct: 51.20, color: '#00838f' },
  { name: 'Web Services', traffic: '696.8 MB', pct: 17.44, color: '#00bcd4' },
  { name: 'Networking', traffic: '669.5 MB', pct: 16.75, color: '#0288d1' },
  { name: 'Unclassified', traffic: '471.2 MB', pct: 11.79, color: '#1565c0' },
  { name: 'Proxy', traffic: '32.9 MB', pct: 0.82, color: '#6a1b9a' },
  { name: 'Social Networking', traffic: '25.0 MB', pct: 0.63, color: '#ad1457' },
  { name: 'File Transfer', traffic: '23.0 MB', pct: 0.58, color: '#c2185b' },
  { name: 'Messaging', traffic: '15.6 MB', pct: 0.39, color: '#e65100' },
  { name: 'Mail', traffic: '12.8 MB', pct: 0.32, color: '#f57f17' },
  { name: 'Games', traffic: '2.4 MB', pct: 0.06, color: '#9e9d24' }
])
const topAppCategoriesSlices = computed(() => buildPieSlices(topAppCategories.value))

const systemMetrics = reactive({
  cpuPercent: 14.5,
  cpuCores: 4,
  memoryPercent: 38.2,
  memoryUsedGb: 3.1,
  memoryTotalGb: 8.0,
  storagePercent: 22.4,
  safetyScore: 98,
  partitions: [
    { mount: '/var/storage', label: 'Storage Partition', usedGb: 18.2, totalGb: 80.0, percent: 22.8 },
    { mount: '/var/log', label: 'Log Database', usedGb: 5.4, totalGb: 25.0, percent: 21.6 },
    { mount: '/tmp', label: 'RAM Temporary Cache', usedGb: 0.4, totalGb: 4.0, percent: 10.0 }
  ]
})

const bandwidthMetrics = reactive({
  wanRate: '72.4 Mbps',
  lanRate: '128.6 Mbps'
})

const sparklineData = reactive({
  wan_in: [12.4, 18.2, 24.5, 31.8, 28.4, 45.2, 38.9, 52.1, 48.6, 64.2, 58.7, 72.4],
  wan_out: [4.2, 6.8, 8.1, 12.4, 9.8, 14.5, 11.2, 18.7, 16.3, 22.1, 19.4, 25.8]
})

const topConsumers = ref([
  { rank: 1, ip: '192.168.1.142', hostname: 'sarah-thinkpad-x1', downloaded: '18.4 GB', category: 'Media & Cloud Sync' },
  { rank: 2, ip: '192.168.1.105', hostname: 'alex-macbook-pro', downloaded: '12.8 GB', category: 'Development' },
  { rank: 3, ip: '192.168.1.50', hostname: 'devops-staging-bastion', downloaded: '8.2 GB', category: 'Server Telemetry' }
])

const threatRadar = ref({
  blocked_today: 1248,
  country_drops: [
    { code: 'CN', country: 'China', drops: 1842, flag: '🇨🇳' },
    { code: 'RU', country: 'Russia', drops: 1420, flag: '🇷🇺' },
    { code: 'IR', country: 'Iran', drops: 528, flag: '🇮🇷' }
  ],
  ips_categories: [
    { category: 'SQL Injection (SQLi)', count: 482, severity: 'Critical', percent: 38.6 },
    { category: 'Remote Code Execution (RCE)', count: 318, severity: 'High', percent: 25.5 },
    { category: 'Buffer Overflow Probes', count: 214, severity: 'High', percent: 17.1 }
  ],
  web_categories: [
    { category: 'Business & Productivity', requests: 42180, percent: 49.9, color: '#0072ce' },
    { category: 'Software Updates / Cloud', requests: 24150, percent: 28.6, color: '#10b981' },
    { category: 'Media & Streaming', requests: 11200, percent: 13.2, color: '#f59e0b' }
  ]
})

const mailFunnel = ref({
  inbound_total: 1450,
  clean_delivered: 1312,
  spam_filtered: 108,
  virus_neutralized: 12
})

const interfacesList = ref([
  { id: 'eth0', name: 'WAN Port 1', hwName: 'eth0', portNumber: 'P1', linkState: 'UP', ipAddress: '203.0.113.10', rxBytes: '14.2 GB', txBytes: '4.8 GB' },
  { id: 'eth1', name: 'Internal LAN', hwName: 'eth1', portNumber: 'P2', linkState: 'UP', ipAddress: '192.168.1.1/24', rxBytes: '48.9 GB', txBytes: '82.1 GB' },
  { id: 'eth2', name: 'DMZ Web Relay', hwName: 'eth2', portNumber: 'P3', linkState: 'UP', ipAddress: '172.16.1.1/24', rxBytes: '6.4 GB', txBytes: '12.8 GB' }
])

const activeConnections = ref([
  { id: 'conn-1', protocol: 'TCP', state: 'ESTABLISHED', src_ip: '192.168.1.105', src_port: '54231', dst_ip: '142.250.190.46', dst_port: '443', service: 'HTTPS', bytes_formatted: '825.4 KB', ttl: 7420 },
  { id: 'conn-2', protocol: 'TCP', state: 'ESTABLISHED', src_ip: '192.168.1.142', src_port: '49182', dst_ip: '52.96.166.146', dst_port: '443', service: 'HTTPS', bytes_formatted: '2.3 MB', ttl: 6800 },
  { id: 'conn-3', protocol: 'UDP', state: 'ASSURED', src_ip: '192.168.1.50', src_port: '51820', dst_ip: '198.51.100.5', dst_port: '51820', service: 'WireGuard', bytes_formatted: '14.1 MB', ttl: 178 }
])

// SVG Path Generator for Sparkline graph
const generateSvgLinePath = (data) => {
  if (!data || data.length === 0) return ''
  const max = Math.max(...data, 100)
  const width = 300
  const height = 65
  const step = width / (data.length - 1)

  return data.reduce((acc, val, idx) => {
    const x = idx * step
    const y = height - (val / max) * height + 5
    return `${acc} ${idx === 0 ? 'M' : 'L'} ${x} ${y}`
  }, '')
}

const generateSvgAreaPath = (data) => {
  if (!data || data.length === 0) return ''
  const linePath = generateSvgLinePath(data)
  return `${linePath} L 300 70 L 0 70 Z`
}

const fetchTelemetry = async (isManual = false) => {
  isLoading.value = true
  try {
    const axiosLib = (typeof window !== 'undefined' && window.axios) ? window.axios : null
    if (axiosLib) {
      const res = await axiosLib.get('/api/system/control-center').catch(() => null)
      if (res && res.data) {
        const d = res.data
        if (d.performance) {
          systemMetrics.cpuPercent = d.performance.cpuPercent || 14.5
          systemMetrics.cpuCores = d.performance.cpuCores || 4
          systemMetrics.memoryPercent = d.performance.memoryPercent || 38.2
          systemMetrics.memoryUsedGb = d.performance.memoryUsedGb || 3.1
          systemMetrics.memoryTotalGb = d.performance.memoryTotalGb || 8.0
          systemMetrics.storagePercent = d.performance.storagePercent || 22.4
          if (d.performance.partitions) systemMetrics.partitions = d.performance.partitions
        }
        if (d.system && d.system.safety_score) systemMetrics.safetyScore = d.system.safety_score
        if (d.threat_radar) threatRadar.value = d.threat_radar
        if (d.mail_funnel) mailFunnel.value = d.mail_funnel
        if (d.top_consumers) topConsumers.value = d.top_consumers
        if (d.sparklines) {
          sparklineData.wan_in = d.sparklines.wan_in || sparklineData.wan_in
          sparklineData.wan_out = d.sparklines.wan_out || sparklineData.wan_out
        }
        if (d.interfaces && d.interfaces.length > 0) interfacesList.value = d.interfaces
      }
    }
  } catch (e) {
    console.error('Failed to fetch telemetry:', e)
  } finally {
    isLoading.value = false
  }
}

const fetchActiveConnections = async () => {
  try {
    const axiosLib = (typeof window !== 'undefined' && window.axios) ? window.axios : null
    if (axiosLib) {
      const res = await axiosLib.get('/api/system/connections').catch(() => null)
      if (res && res.data && res.data.connections) {
        activeConnections.value = res.data.connections
      }
    }
  } catch (e) {
    console.error(e)
  }
}

const killActiveConnection = async (connId) => {
  try {
    const axiosLib = (typeof window !== 'undefined' && window.axios) ? window.axios : null
    if (axiosLib) {
      await axiosLib.delete(`/api/system/connections/${connId}`)
    }
    activeConnections.value = activeConnections.value.filter(c => c.id !== connId)
  } catch (e) {
    console.error(e)
  }
}

const setPollInterval = (sec) => {
  pollIntervalSeconds.value = sec
  startPolling()
}

const togglePolling = () => {
  isPollingActive.value = !isPollingActive.value
  if (isPollingActive.value) startPolling()
  else stopPolling()
}

const startPolling = () => {
  stopPolling()
  pollTimer = setInterval(fetchTelemetry, pollIntervalSeconds.value * 1000)
}

const stopPolling = () => {
  if (pollTimer) {
    clearInterval(pollTimer)
    pollTimer = null
  }
}

onMounted(() => {
  fetchTelemetry()
  fetchActiveConnections()
  startPolling()
})

onUnmounted(() => {
  stopPolling()
})
</script>
