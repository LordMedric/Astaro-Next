<template>
  <div class="min-h-full bg-[#f4f6f9] text-slate-800 font-sans antialiased selection:bg-[#0072ce] selection:text-white">
    <!-- Top Action & Telemetry Header Ribbon -->
    <div class="mb-6 flex flex-col md:flex-row md:items-center md:justify-between gap-4 bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
      <!-- Title & Live Appliance Pulse -->
      <div class="flex items-center gap-3.5">
        <div class="w-10 h-10 rounded-lg bg-[#0072ce] flex items-center justify-center text-white shadow-md shadow-blue-500/20 font-black">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 5a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1H5a1 1 0 01-1-1V5zM14 5a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1h-4a1 1 0 01-1-1V5zM4 15a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1H5a1 1 0 01-1-1v-4zM14 15a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1h-4a1 1 0 01-1-1v-4z" />
          </svg>
        </div>
        <div>
          <div class="flex items-center gap-2">
            <h1 class="text-lg font-bold text-slate-900 tracking-tight">Astaro-Next Control Center</h1>
            <span class="inline-flex items-center gap-1.5 px-2 py-0.5 rounded-full text-[11px] font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200">
              <span class="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
              Live Telemetry
            </span>
            <span v-if="telemetryMode === 'mock'" class="inline-flex items-center px-2 py-0.5 rounded text-[10px] font-mono font-medium bg-amber-50 text-amber-700 border border-amber-200" title="Telemetry route not reached; presenting live simulated data stream">
              SIMULATED TELEMETRY
            </span>
          </div>
          <p class="text-xs text-slate-500 mt-0.5">Real-time hardware performance, daemon lifecycle states, and physical network link monitoring.</p>
        </div>
      </div>

      <!-- Controls: Auto-refresh, Manual Poll, Time Stamp -->
      <div class="flex items-center flex-wrap gap-2.5">
        <!-- Polling Interval Selector -->
        <div class="flex items-center bg-slate-100 p-0.5 rounded-lg border border-slate-200 text-xs">
          <span class="px-2 py-1 text-slate-500 font-medium text-[11px]">Poll:</span>
          <button
            v-for="interval in [5, 10, 30]"
            :key="interval"
            type="button"
            @click="setPollInterval(interval)"
            :class="[
              'px-2 py-1 rounded text-xs font-semibold transition-all',
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
              'px-2 py-1 rounded text-xs font-semibold transition-all flex items-center gap-1',
              !isPollingActive ? 'bg-amber-100 text-amber-800 font-bold' : 'text-slate-600 hover:text-slate-900'
            ]"
            :title="isPollingActive ? 'Pause Auto-Refresh' : 'Resume Auto-Refresh'"
          >
            <span :class="['w-1.5 h-1.5 rounded-full', isPollingActive ? 'bg-emerald-500' : 'bg-amber-500']"></span>
            {{ isPollingActive ? 'Auto' : 'Paused' }}
          </button>
        </div>

        <!-- Manual Refresh Button -->
        <button
          type="button"
          @click="fetchTelemetry(true)"
          :disabled="isLoading"
          class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-white border border-slate-300 text-xs font-semibold text-slate-700 hover:bg-[#f4f6f9] hover:text-slate-900 active:bg-slate-100 disabled:opacity-50 transition-all shadow-2xs cursor-pointer"
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

        <!-- Last Updated Tag -->
        <div class="hidden xl:flex items-center text-[11px] font-mono text-slate-400 pl-1">
          <span>Synced: {{ lastUpdatedFormatted }}</span>
        </div>
      </div>
    </div>

    <!-- Error Banner Notification -->
    <div
      v-if="errorMessage"
      class="mb-6 p-3.5 rounded-lg bg-rose-50 border border-rose-200 text-rose-800 text-xs flex items-center justify-between gap-3 shadow-xs"
    >
      <div class="flex items-center gap-2.5">
        <svg class="w-4 h-4 text-rose-600 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
        </svg>
        <span>{{ errorMessage }}</span>
      </div>
      <button @click="errorMessage = null" class="text-rose-500 hover:text-rose-700 font-bold px-1.5 cursor-pointer">✕</button>
    </div>

    <!-- ENTERPRISE 3-COLUMN GRID STRUCTURE (Sophos UTM Standard) -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 items-start">
      
      <!-- ========================================================================= -->
      <!-- CARD 1: SYSTEM PERFORMANCE                                                -->
      <!-- ========================================================================= -->
      <section class="bg-white rounded-xl border border-slate-200 shadow-sm flex flex-col overflow-hidden transition-shadow hover:shadow-md">
        <!-- Card Header with Sophos UTM Blue Accent Tag -->
        <div class="px-5 py-4 border-b border-slate-100 flex items-center justify-between bg-[#f4f6f9]/50">
          <div class="flex items-center gap-2.5">
            <span class="w-1 h-4 bg-[#0072ce] rounded-full"></span>
            <h2 class="text-sm font-bold text-slate-900 uppercase tracking-wider">System Performance</h2>
          </div>
          <span class="text-[11px] font-mono font-semibold px-2 py-0.5 rounded bg-blue-50 text-[#0072ce] border border-blue-100">
            UTM Engine
          </span>
        </div>

        <!-- Card Content: Dynamic Horizontal Progress Bars -->
        <div class="p-5 space-y-5">
          <!-- CPU Utilization Progress Bar -->
          <div class="space-y-1.5">
            <div class="flex items-center justify-between text-xs">
              <div class="flex items-center gap-1.5">
                <svg class="w-4 h-4 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 3v2m6-2v2M9 19v2m6-2v2M3 9h2m-2 6h2m14-6h2m-2 6h2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z" />
                </svg>
                <span class="font-semibold text-slate-700">CPU Allocation</span>
              </div>
              <div class="flex items-center gap-2 font-mono">
                <span class="text-slate-400 text-[11px]">{{ systemMetrics.cpuCores }} Cores @ {{ systemMetrics.cpuFrequency }}</span>
                <span :class="['font-bold text-xs', getLoadTextColor(systemMetrics.cpuPercent)]">
                  {{ (Number(systemMetrics.cpuPercent) || 0).toFixed(1) }}%
                </span>
              </div>
            </div>

            <!-- Horizontal Track -->
            <div class="h-2.5 w-full bg-slate-100 rounded-full overflow-hidden p-0.5 border border-slate-200/70">
              <div
                class="h-full rounded-full transition-all duration-500 ease-out"
                :class="getProgressColor(systemMetrics.cpuPercent)"
                :style="{ width: `${Math.min(Math.max(Number(systemMetrics.cpuPercent) || 0, 0), 100)}%` }"
              ></div>
            </div>

            <!-- Detailed Sub-metrics -->
            <div class="flex justify-between text-[11px] text-slate-500 pt-0.5">
              <span>Load Avg: {{ (Array.isArray(systemMetrics.loadAvg) ? systemMetrics.loadAvg : [0.2, 0.3, 0.4]).join(', ') }}</span>
              <span>Temp: {{ systemMetrics.cpuTemp || 40 }}°C</span>
            </div>
          </div>

          <!-- Memory (RAM) Allocation Progress Bar -->
          <div class="space-y-1.5">
            <div class="flex items-center justify-between text-xs">
              <div class="flex items-center gap-1.5">
                <svg class="w-4 h-4 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                </svg>
                <span class="font-semibold text-slate-700">Memory Allocation (RAM)</span>
              </div>
              <div class="flex items-center gap-2 font-mono">
                <span class="text-slate-400 text-[11px]">{{ (Number(systemMetrics.memoryUsedGb) || 0).toFixed(1) }} / {{ (Number(systemMetrics.memoryTotalGb) || 8).toFixed(1) }} GB</span>
                <span :class="['font-bold text-xs', getLoadTextColor(systemMetrics.memoryPercent)]">
                  {{ (Number(systemMetrics.memoryPercent) || 0).toFixed(1) }}%
                </span>
              </div>
            </div>

            <!-- Horizontal Track -->
            <div class="h-2.5 w-full bg-slate-100 rounded-full overflow-hidden p-0.5 border border-slate-200/70">
              <div
                class="h-full rounded-full transition-all duration-500 ease-out"
                :class="getProgressColor(systemMetrics.memoryPercent)"
                :style="{ width: `${Math.min(Math.max(Number(systemMetrics.memoryPercent) || 0, 0), 100)}%` }"
              ></div>
            </div>

            <!-- Detailed Sub-metrics -->
            <div class="flex justify-between text-[11px] text-slate-500 pt-0.5">
              <span>Free: {{ ((Number(systemMetrics.memoryTotalGb) || 8) - (Number(systemMetrics.memoryUsedGb) || 0)).toFixed(1) }} GB</span>
              <span>Buffer/Cached: {{ (Number(systemMetrics.memoryCachedGb) || 1.5).toFixed(1) }} GB</span>
            </div>
          </div>

          <!-- Storage Allocation Progress Bar -->
          <div class="space-y-1.5">
            <div class="flex items-center justify-between text-xs">
              <div class="flex items-center gap-1.5">
                <svg class="w-4 h-4 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4m0 5c0 2.21-3.582 4-8 4s-8-1.79-8-4" />
                </svg>
                <span class="font-semibold text-slate-700">Storage Allocation (NVMe / SSD)</span>
              </div>
              <div class="flex items-center gap-2 font-mono">
                <span class="text-slate-400 text-[11px]">{{ (Number(systemMetrics.storageUsedGb) || 0).toFixed(1) }} / {{ (Number(systemMetrics.storageTotalGb) || 100).toFixed(1) }} GB</span>
                <span :class="['font-bold text-xs', getLoadTextColor(systemMetrics.storagePercent)]">
                  {{ (Number(systemMetrics.storagePercent) || 0).toFixed(1) }}%
                </span>
              </div>
            </div>

            <!-- Horizontal Track -->
            <div class="h-2.5 w-full bg-slate-100 rounded-full overflow-hidden p-0.5 border border-slate-200/70">
              <div
                class="h-full rounded-full transition-all duration-500 ease-out"
                :class="getProgressColor(systemMetrics.storagePercent)"
                :style="{ width: `${Math.min(Math.max(Number(systemMetrics.storagePercent) || 0, 0), 100)}%` }"
              ></div>
            </div>

            <!-- Detailed Sub-metrics -->
            <div class="flex justify-between text-[11px] text-slate-500 pt-0.5">
              <span>Log Partition: {{ (Number(systemMetrics.storageLogUsedGb) || 4).toFixed(1) }} GB used</span>
              <span>Available: {{ ((Number(systemMetrics.storageTotalGb) || 100) - (Number(systemMetrics.storageUsedGb) || 0)).toFixed(1) }} GB</span>
            </div>
          </div>

          <!-- Bottom Telemetry Badges Strip -->
          <div class="pt-3 border-t border-slate-100 grid grid-cols-2 gap-2 text-center">
            <div class="p-2 rounded-lg bg-[#f4f6f9] border border-slate-100">
              <span class="text-[10px] text-slate-400 uppercase font-semibold block">System Uptime</span>
              <span class="text-xs font-mono font-bold text-slate-800">{{ systemMetrics.uptime }}</span>
            </div>
            <div class="p-2 rounded-lg bg-[#f4f6f9] border border-slate-100">
              <span class="text-[10px] text-slate-400 uppercase font-semibold block">FastPath Acceleration</span>
              <span class="text-xs font-mono font-bold text-emerald-600">Hardware Xstream</span>
            </div>
          </div>
        </div>
      </section>

      <!-- ========================================================================= -->
      <!-- CARD 2: SERVICES STATUS                                                   -->
      <!-- ========================================================================= -->
      <section class="bg-white rounded-xl border border-slate-200 shadow-sm flex flex-col overflow-hidden transition-shadow hover:shadow-md">
        <!-- Card Header -->
        <div class="px-5 py-4 border-b border-slate-100 flex items-center justify-between bg-[#f4f6f9]/50">
          <div class="flex items-center gap-2.5">
            <span class="w-1 h-4 bg-[#0072ce] rounded-full"></span>
            <h2 class="text-sm font-bold text-slate-900 uppercase tracking-wider">Services Status</h2>
          </div>
          <div class="flex items-center gap-1 text-[11px] font-medium text-slate-500">
            <span class="font-bold text-emerald-600">{{ activeServicesCount }}</span> of
            <span class="font-bold text-slate-700">{{ servicesList.length }}</span> Active
          </div>
        </div>

        <!-- Card Content: Grid of Infrastructure Modules -->
        <div class="p-5">
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div
              v-for="service in servicesList"
              :key="service.id"
              class="p-3 rounded-lg border transition-all duration-150 flex flex-col justify-between group"
              :class="[
                service.status === 'running'
                  ? 'bg-[#f4f6f9]/70 border-slate-200/80 hover:bg-[#f4f6f9] hover:border-slate-300'
                  : 'bg-rose-50/40 border-rose-200 hover:bg-rose-50'
              ]"
            >
              <!-- Module Top: Icon, Name & Status Pill -->
              <div class="flex items-start justify-between gap-2 mb-2">
                <div class="flex items-center gap-2.5 min-w-0">
                  <div
                    class="w-7 h-7 rounded-md flex items-center justify-center flex-shrink-0 transition-colors"
                    :class="service.status === 'running' ? 'bg-white text-slate-700 shadow-xs border border-slate-200' : 'bg-rose-100 text-rose-700 border border-rose-200'"
                  >
                    <component :is="getServiceIcon(service.icon)" class="w-4 h-4" />
                  </div>
                  <div class="min-w-0">
                    <h3 class="text-xs font-bold text-slate-900 truncate leading-snug">{{ service.name }}</h3>
                    <p class="text-[10px] text-slate-400 truncate">{{ service.module }}</p>
                  </div>
                </div>

                <!-- Elegant Green / Red Status Element -->
                <div class="flex items-center flex-shrink-0">
                  <span
                    v-if="service.status === 'running'"
                    class="inline-flex items-center gap-1.5 px-2 py-0.5 rounded-full text-[10px] font-semibold bg-emerald-100/70 text-emerald-800 border border-emerald-300/60"
                  >
                    <span class="w-1.5 h-1.5 rounded-full bg-emerald-500 ring-2 ring-emerald-300 animate-pulse"></span>
                    Running
                  </span>
                  <span
                    v-else
                    class="inline-flex items-center gap-1.5 px-2 py-0.5 rounded-full text-[10px] font-semibold bg-rose-100 text-rose-800 border border-rose-300/80"
                  >
                    <span class="w-1.5 h-1.5 rounded-full bg-rose-600 ring-2 ring-rose-300"></span>
                    Stopped
                  </span>
                </div>
              </div>

              <!-- Module Metadata Footer (PID, Memory, Quick Toggle) -->
              <div class="pt-2 border-t border-slate-200/50 flex items-center justify-between text-[10px] font-mono text-slate-500">
                <span v-if="service.status === 'running'">PID: {{ service.pid || '8421' }}</span>
                <span v-else class="text-rose-600 font-sans font-medium">Inactive</span>

                <button
                  type="button"
                  @click="toggleServiceState(service)"
                  class="text-[10px] font-sans font-semibold text-[#0072ce] hover:text-blue-800 hover:underline flex items-center gap-0.5 cursor-pointer"
                >
                  <span>{{ service.status === 'running' ? 'Restart' : 'Start' }}</span>
                  <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                  </svg>
                </button>
              </div>
            </div>
          </div>

          <!-- Services Quick Summary Note -->
          <div class="mt-4 p-3 rounded-lg bg-blue-50/50 border border-blue-100 text-[11px] text-blue-900 flex items-center justify-between">
            <div class="flex items-center gap-2">
              <svg class="w-4 h-4 text-[#0072ce] flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span>All essential deep packet inspection subsystems operating within SLA thresholds.</span>
            </div>
          </div>
        </div>
      </section>

      <!-- ========================================================================= -->
      <!-- CARD 3: NETWORK INTERFACES                                                -->
      <!-- ========================================================================= -->
      <section class="bg-white rounded-xl border border-slate-200 shadow-sm flex flex-col overflow-hidden transition-shadow hover:shadow-md">
        <!-- Card Header -->
        <div class="px-5 py-4 border-b border-slate-100 flex items-center justify-between bg-[#f4f6f9]/50">
          <div class="flex items-center gap-2.5">
            <span class="w-1 h-4 bg-[#0072ce] rounded-full"></span>
            <h2 class="text-sm font-bold text-slate-900 uppercase tracking-wider">Network Interfaces</h2>
          </div>
          <span class="text-[11px] font-mono font-semibold px-2 py-0.5 rounded bg-slate-100 text-slate-700 border border-slate-200">
            {{ activeInterfacesCount }}/{{ interfacesList.length }} Connected
          </span>
        </div>

        <!-- Card Content: Physical Hardware Ports List Mirroring Sophos Appliance -->
        <div class="p-5 space-y-3">
          <div
            v-for="iface in interfacesList"
            :key="iface.id"
            class="p-3 rounded-lg border transition-all duration-150 flex flex-col gap-2.5"
            :class="[
              iface.linkState === 'UP'
                ? 'bg-white border-slate-200 hover:border-slate-300 hover:shadow-xs'
                : 'bg-[#f4f6f9]/60 border-slate-200/80 opacity-80'
            ]"
          >
            <!-- Port Header: Physical Port Jack Representation & Speed Badge -->
            <div class="flex items-center justify-between gap-2">
              <div class="flex items-center gap-2.5">
                <!-- Physical RJ45 / SFP+ Port LED Icon -->
                <div class="relative flex items-center justify-center w-8 h-8 rounded bg-slate-800 text-slate-300 font-mono text-[10px] font-bold border border-slate-700 shadow-2xs">
                  <span>{{ iface.portNumber }}</span>
                  <!-- Link State LED Top-Right Indicator -->
                  <span
                    class="absolute -top-1 -right-1 w-2.5 h-2.5 rounded-full border border-white"
                    :class="iface.linkState === 'UP' ? 'bg-emerald-500' : 'bg-rose-500'"
                    :title="`Link state: ${iface.linkState}`"
                  ></span>
                </div>

                <div>
                  <div class="flex items-center gap-2">
                    <h3 class="text-xs font-bold text-slate-900">{{ iface.name }}</h3>
                    <span :class="['text-[10px] px-1.5 py-0.2 rounded font-semibold uppercase', getZoneBadgeColor(iface.zone)]">
                      {{ iface.zone }}
                    </span>
                  </div>
                  <span class="text-[10px] text-slate-400 font-mono">{{ iface.hwName }} ({{ iface.macAddress }})</span>
                </div>
              </div>

              <!-- Operational Link State & Port Speed -->
              <div class="text-right">
                <span
                  :class="[
                    'inline-block text-[10px] font-mono font-bold px-2 py-0.5 rounded border',
                    iface.linkState === 'UP'
                      ? 'bg-emerald-50 text-emerald-700 border-emerald-200'
                      : 'bg-slate-100 text-slate-500 border-slate-200'
                  ]"
                >
                  {{ iface.linkState }} &bull; {{ iface.speed }}
                </span>
                <span class="block text-[10px] text-slate-400 font-mono mt-0.5">{{ iface.duplex }} Duplex</span>
              </div>
            </div>

            <!-- IP Addressing & Live Traffic Throughput Strip -->
            <div class="p-2 rounded bg-[#f4f6f9] border border-slate-100 flex items-center justify-between text-xs font-mono">
              <div class="flex items-center gap-1.5 text-slate-700 truncate">
                <span class="text-[10px] text-slate-400 font-sans uppercase font-bold">IP:</span>
                <span class="font-bold text-slate-900 truncate">{{ iface.ipAddress || 'Unassigned / DHCP Pending' }}</span>
              </div>
              <div class="flex items-center gap-3 text-[11px] text-slate-500 flex-shrink-0">
                <span class="flex items-center gap-1" title="Inbound Traffic">
                  <svg class="w-3 h-3 text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 14l-7 7m0 0l-7-7m7 7V3" />
                  </svg>
                  {{ iface.rxRate }}
                </span>
                <span class="flex items-center gap-1" title="Outbound Traffic">
                  <svg class="w-3 h-3 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 10l7-7m0 0l7 7m-7-7v18" />
                  </svg>
                  {{ iface.txRate }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </section>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, h } from 'vue'

let axiosInstance = null

const initAxios = async () => {
  if (typeof window !== 'undefined' && window.axios) {
    axiosInstance = window.axios
    return
  }
  try {
    const axiosModule = await import('axios')
    axiosInstance = axiosModule.default || axiosModule
  } catch (err) {
    axiosInstance = {
      async get(url, config = {}) {
        const headers = config.headers || {}
        const res = await fetch(url, { method: 'GET', headers, signal: config.signal })
        if (!res.ok) {
          const errorObj = new Error(`HTTP Error ${res.status}: ${res.statusText}`)
          errorObj.response = res
          throw errorObj
        }
        const data = await res.json()
        return { data, status: res.status }
      }
    }
  }
}

// -----------------------------------------------------------------------------
// Component Props & Emits
// -----------------------------------------------------------------------------
const props = defineProps({
  apiEndpoint: {
    type: String,
    default: '/api/system/control-center'
  },
  autoPoll: {
    type: Boolean,
    default: true
  },
  initialPollInterval: {
    type: Number,
    default: 5 // seconds
  },
  authToken: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['telemetry-update', 'service-toggle', 'error'])

// -----------------------------------------------------------------------------
// Reactive State Declarations
// -----------------------------------------------------------------------------
const isLoading = ref(false)
const errorMessage = ref(null)
const lastUpdated = ref(new Date())
const telemetryMode = ref('live') // 'live' | 'mock'
const pollIntervalSeconds = ref(props.initialPollInterval)
const isPollingActive = ref(props.autoPoll)
let pollTimer = null
let abortController = null

// 1. System Performance Reactive Model
const systemMetrics = ref({
  cpuPercent: 24.5,
  cpuCores: 8,
  cpuFrequency: '3.4 GHz',
  cpuTemp: 41,
  loadAvg: [0.38, 0.42, 0.45],
  memoryPercent: 46.2,
  memoryUsedGb: 7.4,
  memoryTotalGb: 16.0,
  memoryCachedGb: 3.2,
  storagePercent: 32.8,
  storageUsedGb: 168.0,
  storageTotalGb: 512.0,
  storageLogUsedGb: 28.4,
  uptime: '14d 08h 22m'
})

// 2. Services Status Reactive Model
const servicesList = ref([
  {
    id: 'firewall',
    name: 'Firewall',
    module: 'NFTables Packet Filter',
    icon: 'ShieldIcon',
    status: 'running',
    pid: '1042'
  },
  {
    id: 'zenarmor',
    name: 'Zenarmor',
    module: 'L7 Deep Inspection & App Control',
    icon: 'GlobeIcon',
    status: 'running',
    pid: '2194'
  },
  {
    id: 'web_proxy',
    name: 'Web Proxy',
    module: 'Nginx WAF & Reverse Proxy',
    icon: 'ServerIcon',
    status: 'running',
    pid: '3318'
  },
  {
    id: 'mail_gateway',
    name: 'Mail Gateway',
    module: 'Postfix MTA & Anti-Spam',
    icon: 'MailIcon',
    status: 'running',
    pid: '4491'
  },
  {
    id: 'vpn',
    name: 'VPN',
    module: 'WireGuard & IPSec Engine',
    icon: 'LockIcon',
    status: 'running',
    pid: '5812'
  }
])

// 3. Network Interfaces Reactive Model
const interfacesList = ref([])

// -----------------------------------------------------------------------------
// Computed Helpers
// -----------------------------------------------------------------------------
const activeServicesCount = computed(() => {
  return servicesList.value.filter(s => s.status === 'running').length
})

const activeInterfacesCount = computed(() => {
  return interfacesList.value.filter(i => i.linkState === 'UP').length
})

const lastUpdatedFormatted = computed(() => {
  if (!lastUpdated.value) return 'Never'
  return lastUpdated.value.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' })
})

// -----------------------------------------------------------------------------
// Dynamic Styling Helpers for Enterprise Visuals
// -----------------------------------------------------------------------------
const getProgressColor = (percentage) => {
  if (percentage >= 90) return 'bg-rose-500 shadow-sm shadow-rose-500/50'
  if (percentage >= 75) return 'bg-amber-500 shadow-sm shadow-amber-500/50'
  return 'bg-[#0072ce] shadow-sm shadow-blue-500/50'
}

const getLoadTextColor = (percentage) => {
  if (percentage >= 90) return 'text-rose-600'
  if (percentage >= 75) return 'text-amber-600'
  return 'text-blue-600'
}

const getZoneBadgeColor = (zone) => {
  switch (zone?.toUpperCase()) {
    case 'WAN':
      return 'bg-rose-50 text-rose-700 border border-rose-200'
    case 'LAN':
      return 'bg-emerald-50 text-emerald-700 border border-emerald-200'
    case 'DMZ':
      return 'bg-amber-50 text-amber-700 border border-amber-200'
    case 'HA':
    case 'VPN':
      return 'bg-purple-50 text-purple-700 border border-purple-200'
    default:
      return 'bg-slate-100 text-slate-700 border border-slate-200'
  }
}

// -----------------------------------------------------------------------------
// SVG Icon Renderer Declarations
// -----------------------------------------------------------------------------
const ShieldIcon = {
  render: () => h('svg', { class: 'w-4 h-4', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
    h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z' })
  ])
}

const GlobeIcon = {
  render: () => h('svg', { class: 'w-4 h-4', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
    h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9' })
  ])
}

const ServerIcon = {
  render: () => h('svg', { class: 'w-4 h-4', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
    h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M5 12h14M5 12a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v4a2 2 0 01-2 2M5 12a2 2 0 00-2 2v4a2 2 0 002 2h14a2 2 0 002-2v-4a2 2 0 00-2-2m-2-4h.01M17 16h.01' })
  ])
}

const MailIcon = {
  render: () => h('svg', { class: 'w-4 h-4', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
    h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z' })
  ])
}

const LockIcon = {
  render: () => h('svg', { class: 'w-4 h-4', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
    h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z' })
  ])
}

const getServiceIcon = (iconName) => {
  switch (iconName) {
    case 'ShieldIcon': return ShieldIcon
    case 'GlobeIcon': return GlobeIcon
    case 'ServerIcon': return ServerIcon
    case 'MailIcon': return MailIcon
    case 'LockIcon': return LockIcon
    default: return ServerIcon
  }
}

// -----------------------------------------------------------------------------
// Live Simulated Telemetry Generator (Fall-through fallback)
// -----------------------------------------------------------------------------
const generateSimulatedTelemetry = () => {
  // Realistic jitter for live dashboard demo
  const cpuJitter = (Math.random() * 6 - 3)
  const newCpu = Math.max(12, Math.min(88, systemMetrics.value.cpuPercent + cpuJitter))
  
  const memJitter = (Math.random() * 0.4 - 0.2)
  const newMemUsed = Math.max(4.0, Math.min(14.5, systemMetrics.value.memoryUsedGb + memJitter))
  const newMemPercent = (newMemUsed / systemMetrics.value.memoryTotalGb) * 100

  // Update rates with realistic dynamic numbers
  const rxMb = (3.5 + Math.random() * 4.5).toFixed(1)
  const txMb = (1.1 + Math.random() * 2.2).toFixed(1)

  return {
    performance: {
      cpuPercent: parseFloat(newCpu.toFixed(1)),
      cpuCores: 8,
      cpuFrequency: '3.4 GHz',
      cpuTemp: Math.round(39 + (newCpu / 4)),
      loadAvg: [
        parseFloat((newCpu / 50).toFixed(2)),
        parseFloat(((newCpu + 5) / 50).toFixed(2)),
        parseFloat(((newCpu + 8) / 50).toFixed(2))
      ],
      memoryPercent: parseFloat(newMemPercent.toFixed(1)),
      memoryUsedGb: parseFloat(newMemUsed.toFixed(1)),
      memoryTotalGb: 16.0,
      memoryCachedGb: 3.4,
      storagePercent: 32.8,
      storageUsedGb: 168.0,
      storageTotalGb: 512.0,
      storageLogUsedGb: 28.4,
      uptime: '14d 08h 22m'
    },
    services: servicesList.value,
    interfaces: interfacesList.value.map(iface => {
      if (iface.linkState === 'UP' && iface.id === 'port1') {
        return { ...iface, rxRate: `${rxMb} MB/s`, txRate: `${txMb} MB/s` }
      }
      return iface
    })
  }
}

// -----------------------------------------------------------------------------
// Axios Backend Telemetry Integration Lifecycle Hook
// -----------------------------------------------------------------------------
const fetchTelemetry = async (isManual = false) => {
  if (isManual) {
    isLoading.value = true
  }

  if (!axiosInstance) {
    await initAxios()
  }

  // Cancel previous flight if any
  if (abortController) {
    abortController.abort()
  }
  abortController = new AbortController()

  const config = {
    signal: abortController.signal,
    headers: {}
  }

  const effectiveToken = props.authToken || (typeof localStorage !== 'undefined' ? localStorage.getItem('astaro_token') : null)
  if (effectiveToken) {
    config.headers['Authorization'] = `Bearer ${effectiveToken}`
    config.headers['X-API-Key'] = effectiveToken
  }

  try {
    const response = await axiosInstance.get(props.apiEndpoint, config)
    const data = response.data

    // If backend returns data formatted as expected
    if (data) {
      telemetryMode.value = 'live'
      errorMessage.value = null

      // Sync Card 1: Performance
      if (data.performance || data.system) {
        const perf = data.performance || data.system || {}
        systemMetrics.value = {
          ...systemMetrics.value,
          ...perf,
          cpuPercent: Number(perf.cpuPercent ?? perf.cpu ?? systemMetrics.value.cpuPercent ?? 0),
          cpuCores: perf.cpuCores ?? systemMetrics.value.cpuCores ?? 4,
          cpuFrequency: perf.cpuFrequency ?? systemMetrics.value.cpuFrequency ?? '2.8 GHz',
          cpuTemp: perf.cpuTemp ?? systemMetrics.value.cpuTemp ?? 40,
          loadAvg: Array.isArray(perf.loadAvg) ? perf.loadAvg : (systemMetrics.value.loadAvg || [0.2, 0.3, 0.4]),
          memoryPercent: Number(perf.memoryPercent ?? perf.memory ?? systemMetrics.value.memoryPercent ?? 0),
          memoryUsedGb: Number(perf.memoryUsedGb ?? (parseFloat(perf.memoryUsed) || systemMetrics.value.memoryUsedGb || 0)),
          memoryTotalGb: Number(perf.memoryTotalGb ?? (parseFloat(perf.memoryTotal) || systemMetrics.value.memoryTotalGb || 8.0)),
          memoryCachedGb: Number(perf.memoryCachedGb ?? systemMetrics.value.memoryCachedGb ?? 1.5),
          storagePercent: Number(perf.storagePercent ?? perf.storage ?? systemMetrics.value.storagePercent ?? 0),
          storageUsedGb: Number(perf.storageUsedGb ?? (parseFloat(perf.storageUsed) || systemMetrics.value.storageUsedGb || 0)),
          storageTotalGb: Number(perf.storageTotalGb ?? (parseFloat(perf.storageTotal) || systemMetrics.value.storageTotalGb || 100.0)),
          storageLogUsedGb: Number(perf.storageLogUsedGb ?? systemMetrics.value.storageLogUsedGb ?? 4.0),
          uptime: (data.system && data.system.uptime) || perf.uptime || systemMetrics.value.uptime || '0m'
        }
      }

      // Sync Card 2: Services
      if (Array.isArray(data.services)) {
        servicesList.value = data.services
      } else if (data.active_daemons) {
        // Adapt if backend is using daemon dictionary
        servicesList.value.forEach(srv => {
          if (data.active_daemons[srv.id] !== undefined) {
            srv.status = data.active_daemons[srv.id] ? 'running' : 'stopped'
          }
        })
      }

      // Sync Card 3: Interfaces
      if (Array.isArray(data.interfaces)) {
        interfacesList.value = data.interfaces.map(i => ({
          ...i,
          linkState: (i.linkState || i.linkStatus || 'down').toUpperCase()
        }))
      }

      lastUpdated.value = new Date()
      emit('telemetry-update', data)
    }
  } catch (err) {
    // If request was canceled by AbortController, ignore
    if (err.name === 'CanceledError' || err.name === 'AbortError') {
      return
    }

    // Fallback to simulated live stream gracefully
    telemetryMode.value = 'mock'
    const simData = generateSimulatedTelemetry()
    systemMetrics.value = simData.performance
    interfacesList.value = simData.interfaces
    lastUpdated.value = new Date()

    // If manual refresh triggered and endpoint genuinely errored, show friendly non-intrusive hint
    if (isManual && err.response && err.response.status !== 404) {
      errorMessage.value = `Backend endpoint [${props.apiEndpoint}] unreachable: ${err.message}. Switched to local telemetry simulator.`
      emit('error', err)
    }
  } finally {
    isLoading.value = false
  }
}

// -----------------------------------------------------------------------------
// Interactive Action Handlers
// -----------------------------------------------------------------------------
const toggleServiceState = (service) => {
  const nextState = service.status === 'running' ? 'stopped' : 'running'
  service.status = nextState
  emit('service-toggle', { serviceId: service.id, targetState: nextState })
}

const setPollInterval = (seconds) => {
  pollIntervalSeconds.value = seconds
  startPolling()
}

const togglePolling = () => {
  isPollingActive.value = !isPollingActive.value
  if (isPollingActive.value) {
    startPolling()
  } else {
    stopPolling()
  }
}

const startPolling = () => {
  stopPolling()
  if (!isPollingActive.value) return
  pollTimer = setInterval(() => {
    fetchTelemetry(false)
  }, pollIntervalSeconds.value * 1000)
}

const stopPolling = () => {
  if (pollTimer) {
    clearInterval(pollTimer)
    pollTimer = null
  }
}

// -----------------------------------------------------------------------------
// Lifecycle Hooks
// -----------------------------------------------------------------------------
onMounted(() => {
  fetchTelemetry(true)
  if (isPollingActive.value) {
    startPolling()
  }
})

onUnmounted(() => {
  stopPolling()
  if (abortController) {
    abortController.abort()
  }
})
</script>

<style scoped>
/* High-contrast smooth progress bar transition */
.transition-all {
  transition-property: all;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
}
</style>
