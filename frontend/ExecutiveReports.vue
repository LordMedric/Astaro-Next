<template>
  <div class="space-y-6">
    <!-- Top Modern Breadcrumb & Action Banner -->
    <div class="bg-white border border-slate-200 rounded-xl p-5 shadow-xs flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div>
        <div class="flex items-center gap-2">
          <span class="w-2 h-6 bg-[#ee7f00] rounded-xs"></span>
          <h1 class="text-xl font-bold text-slate-900 tracking-tight">Executive &amp; Security Statistics</h1>
          <span class="bg-blue-50 text-[#005299] text-xs font-bold px-2.5 py-0.5 rounded-full border border-blue-200">
            Real-Time Accounting Engine
          </span>
        </div>
        <p class="text-xs text-slate-500 mt-1 pl-4">
          Interactive traffic accounting, application category analytics, firewall drop statistics, and scheduled executive reports.
        </p>
      </div>

      <!-- Tab Navigation Pills (Matching Astaro-Next Sections) -->
      <div class="flex items-center gap-1 bg-slate-100 p-1 rounded-lg border border-slate-200 overflow-x-auto text-xs font-semibold">
        <button
          v-for="tab in tabs"
          :key="tab.id"
          @click="activeTab = tab.id"
          :class="[
            'px-3.5 py-1.5 rounded-md transition-all whitespace-nowrap cursor-pointer flex items-center gap-1.5',
            activeTab === tab.id
              ? 'bg-white text-[#005299] shadow-xs font-bold'
              : 'text-slate-600 hover:text-slate-900 hover:bg-slate-200/60'
          ]"
        >
          <span>{{ tab.icon }}</span>
          <span>{{ tab.label }}</span>
        </button>
      </div>
    </div>

    <!-- ========================================================================= -->
    <!-- TAB 1: NETWORK STATISTICS (TODAY) - Astaro-Next PARITY                    -->
    <!-- ========================================================================= -->
    <div v-if="activeTab === 'network_stats'" class="space-y-6">
      <div class="flex items-center justify-between">
        <h2 class="text-xs font-bold uppercase tracking-wider text-slate-700">Network Statistics — Today</h2>
        <span class="text-[11px] font-mono text-slate-500">Total packets: 3,562,702 &bull; Total traffic: 3.9 GB</span>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- Panel 1: Top Accounting Services -->
        <div class="bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden">
          <div class="p-3.5 bg-[#f4f6f9] border-b border-slate-200 flex items-center justify-between">
            <span class="text-xs font-bold text-slate-800">Top Accounting Services</span>
            <span class="text-[#0072ce] text-xs font-bold cursor-pointer hover:underline">▶</span>
          </div>

          <div class="p-4 flex flex-col sm:flex-row items-center gap-6">
            <!-- SVG Pie Chart -->
            <div class="w-32 h-32 flex-shrink-0 relative">
              <svg viewBox="-55 -55 110 110" class="w-full h-full transform -rotate-90">
                <path
                  v-for="(slice, sIdx) in accountingServicesSlices"
                  :key="sIdx"
                  :d="slice.path"
                  :fill="slice.color"
                  stroke="#ffffff"
                  stroke-width="1.5"
                  class="transition-transform duration-200 hover:scale-105"
                >
                  <title>{{ slice.name }}: {{ slice.traffic }} ({{ slice.pct }}%)</title>
                </path>
              </svg>
            </div>

            <!-- Data Table -->
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

        <!-- Panel 2: Top Source Hosts -->
        <div class="bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden">
          <div class="p-3.5 bg-[#f4f6f9] border-b border-slate-200 flex items-center justify-between">
            <span class="text-xs font-bold text-slate-800">Top Source Hosts</span>
            <span class="text-[#0072ce] text-xs font-bold cursor-pointer hover:underline">▶</span>
          </div>

          <div class="p-4 flex flex-col sm:flex-row items-center gap-6">
            <!-- SVG Pie Chart -->
            <div class="w-32 h-32 flex-shrink-0 relative">
              <svg viewBox="-55 -55 110 110" class="w-full h-full transform -rotate-90">
                <path
                  v-for="(slice, sIdx) in sourceHostsSlices"
                  :key="sIdx"
                  :d="slice.path"
                  :fill="slice.color"
                  stroke="#ffffff"
                  stroke-width="1.5"
                  class="transition-transform duration-200 hover:scale-105"
                >
                  <title>{{ slice.name }}: {{ slice.traffic }} ({{ slice.pct }}%)</title>
                </path>
              </svg>
            </div>

            <!-- Data Table -->
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

      <!-- Panel 3: Concurrent Connections Today (Live Interactive Area Graph) -->
      <div class="bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden">
        <div class="p-3.5 bg-[#f4f6f9] border-b border-slate-200 flex items-center justify-between">
          <div class="flex items-center gap-2">
            <span class="w-1.5 h-3.5 bg-[#0072ce] rounded-xs"></span>
            <span class="text-xs font-bold text-slate-800">Concurrent Connections Today</span>
          </div>
          <span class="text-[11px] font-mono text-slate-500">Peak: <strong>888 connections</strong> at 21:40</span>
        </div>

        <div class="p-6">
          <div class="relative w-full h-56">
            <svg class="w-full h-full overflow-visible" viewBox="0 0 1000 220" preserveAspectRatio="none">
              <defs>
                <linearGradient id="connGradient" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stop-color="#0072ce" stop-opacity="0.45" />
                  <stop offset="100%" stop-color="#0072ce" stop-opacity="0.02" />
                </linearGradient>
              </defs>

              <!-- Grid Lines -->
              <line x1="0" y1="0" x2="1000" y2="0" stroke="#e2e8f0" stroke-dasharray="4" />
              <line x1="0" y1="55" x2="1000" y2="55" stroke="#e2e8f0" stroke-dasharray="4" />
              <line x1="0" y1="110" x2="1000" y2="110" stroke="#e2e8f0" stroke-dasharray="4" />
              <line x1="0" y1="165" x2="1000" y2="165" stroke="#e2e8f0" stroke-dasharray="4" />
              <line x1="0" y1="220" x2="1000" y2="220" stroke="#cbd5e1" stroke-width="1.5" />

              <!-- Y-Axis Labels -->
              <text x="5" y="15" fill="#64748b" font-size="11" font-family="monospace">888</text>
              <text x="5" y="70" fill="#64748b" font-size="11" font-family="monospace">666</text>
              <text x="5" y="125" fill="#64748b" font-size="11" font-family="monospace">444</text>
              <text x="5" y="180" fill="#64748b" font-size="11" font-family="monospace">222</text>
              <text x="5" y="215" fill="#64748b" font-size="11" font-family="monospace">0</text>

              <!-- Gradient Fill Area -->
              <path
                d="M 50 220 L 50 180 L 100 80 L 150 150 L 200 120 L 250 90 L 300 110 L 350 180 L 400 190 L 450 170 L 500 160 L 550 25 L 600 70 L 650 170 L 700 160 L 750 150 L 800 160 L 850 110 L 900 130 L 950 80 L 1000 140 L 1000 220 Z"
                fill="url(#connGradient)"
              />

              <!-- Smooth Curve Line -->
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

          <!-- X-Axis Timestamps -->
          <div class="flex justify-between text-[10px] font-mono text-slate-400 pt-2 border-t border-slate-100">
            <span>12:05</span>
            <span>14:04</span>
            <span>16:04</span>
            <span>18:03</span>
            <span>20:03</span>
            <span class="font-bold text-[#0072ce]">22:02 (Peak)</span>
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
    <!-- TAB 2: NETWORK PROTECTION STATISTICS (TODAY) - EXACT Astaro-Next PARITY   -->
    <!-- ========================================================================= -->
    <div v-if="activeTab === 'network_protection'" class="space-y-6">
      <div class="flex items-center justify-between">
        <h2 class="text-xs font-bold uppercase tracking-wider text-slate-700">Network Protection Statistics — Today</h2>
        <span class="text-[11px] font-mono text-slate-500">Total dropped packets: 34,793</span>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- Panel 1: Top Dropped Source Hosts -->
        <div class="bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden">
          <div class="p-3.5 bg-[#f4f6f9] border-b border-slate-200 flex items-center justify-between">
            <span class="text-xs font-bold text-slate-800">Top Dropped Source Hosts</span>
            <span class="text-[#0072ce] text-xs font-bold cursor-pointer hover:underline">▶</span>
          </div>

          <div class="p-4 flex flex-col sm:flex-row items-center gap-6">
            <!-- SVG Pie Chart -->
            <div class="w-32 h-32 flex-shrink-0 relative">
              <svg viewBox="-55 -55 110 110" class="w-full h-full transform -rotate-90">
                <path
                  v-for="(slice, sIdx) in droppedSourceSlices"
                  :key="sIdx"
                  :d="slice.path"
                  :fill="slice.color"
                  stroke="#ffffff"
                  stroke-width="1.5"
                  class="transition-transform duration-200 hover:scale-105"
                >
                  <title>{{ slice.name }}: {{ slice.packets }} pkts ({{ slice.pct }}%)</title>
                </path>
              </svg>
            </div>

            <!-- Table -->
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

        <!-- Panel 2: Top Dropped Destination Services/Hosts -->
        <div class="bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden">
          <div class="p-3.5 bg-[#f4f6f9] border-b border-slate-200 flex items-center justify-between">
            <span class="text-xs font-bold text-slate-800">Top Dropped Destination Services/Hosts</span>
            <span class="text-[#0072ce] text-xs font-bold cursor-pointer hover:underline">▶</span>
          </div>

          <div class="p-4 flex flex-col sm:flex-row items-center gap-6">
            <!-- SVG Pie Chart -->
            <div class="w-32 h-32 flex-shrink-0 relative">
              <svg viewBox="-55 -55 110 110" class="w-full h-full transform -rotate-90">
                <path
                  v-for="(slice, sIdx) in droppedDestSlices"
                  :key="sIdx"
                  :d="slice.path"
                  :fill="slice.color"
                  stroke="#ffffff"
                  stroke-width="1.5"
                  class="transition-transform duration-200 hover:scale-105"
                >
                  <title>{{ slice.service }} -> {{ slice.dest }}: {{ slice.packets }} pkts ({{ slice.pct }}%)</title>
                </path>
              </svg>
            </div>

            <!-- Table -->
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

      <!-- Collapsible Panel 3: IPS Top Blocked Attacks -->
      <div class="bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden">
        <div class="p-3.5 bg-[#f4f6f9] border-b border-slate-200 flex items-center justify-between">
          <span class="text-xs font-bold text-slate-800">IPS: Top Blocked Attacks</span>
          <span class="text-[#0072ce] text-xs font-bold cursor-pointer hover:underline">▶</span>
        </div>
        <div class="p-4 text-center text-xs text-slate-400">No data is available for this report</div>
      </div>

      <!-- Collapsible Panel 4: IPS Top Attackers -->
      <div class="bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden">
        <div class="p-3.5 bg-[#f4f6f9] border-b border-slate-200 flex items-center justify-between">
          <span class="text-xs font-bold text-slate-800">IPS: Top Attackers</span>
          <span class="text-[#0072ce] text-xs font-bold cursor-pointer hover:underline">▶</span>
        </div>
        <div class="p-4 text-center text-xs text-slate-400">No data is available for this report</div>
      </div>
    </div>

    <!-- ========================================================================= -->
    <!-- TAB 3: WEB PROTECTION STATISTICS (TODAY) - EXACT Astaro-Next PARITY       -->
    <!-- ========================================================================= -->
    <div v-if="activeTab === 'web_protection'" class="space-y-6">
      <div class="flex items-center justify-between">
        <h2 class="text-xs font-bold uppercase tracking-wider text-slate-700">Web Protection Statistics — Today</h2>
        <span class="text-[11px] font-mono text-slate-500">Total packets: 3,562,702</span>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- Panel 1: Top Applications -->
        <div class="bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden">
          <div class="p-3.5 bg-[#f4f6f9] border-b border-slate-200 flex items-center justify-between">
            <span class="text-xs font-bold text-slate-800">Top Applications</span>
            <span class="text-[#0072ce] text-xs font-bold cursor-pointer hover:underline">▶</span>
          </div>

          <div class="p-4 flex flex-col sm:flex-row items-center gap-6">
            <!-- SVG Pie Chart -->
            <div class="w-32 h-32 flex-shrink-0 relative">
              <svg viewBox="-55 -55 110 110" class="w-full h-full transform -rotate-90">
                <path
                  v-for="(slice, sIdx) in topAppsSlices"
                  :key="sIdx"
                  :d="slice.path"
                  :fill="slice.color"
                  stroke="#ffffff"
                  stroke-width="1.5"
                  class="transition-transform duration-200 hover:scale-105"
                >
                  <title>{{ slice.name }}: {{ slice.traffic }} ({{ slice.pct }}%)</title>
                </path>
              </svg>
            </div>

            <!-- Table -->
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

        <!-- Panel 2: Top Application Categories -->
        <div class="bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden">
          <div class="p-3.5 bg-[#f4f6f9] border-b border-slate-200 flex items-center justify-between">
            <span class="text-xs font-bold text-slate-800">Top Application Categories</span>
            <span class="text-[#0072ce] text-xs font-bold cursor-pointer hover:underline">▶</span>
          </div>

          <div class="p-4 flex flex-col sm:flex-row items-center gap-6">
            <!-- SVG Pie Chart -->
            <div class="w-32 h-32 flex-shrink-0 relative">
              <svg viewBox="-55 -55 110 110" class="w-full h-full transform -rotate-90">
                <path
                  v-for="(slice, sIdx) in topAppCategoriesSlices"
                  :key="sIdx"
                  :d="slice.path"
                  :fill="slice.color"
                  stroke="#ffffff"
                  stroke-width="1.5"
                  class="transition-transform duration-200 hover:scale-105"
                >
                  <title>{{ slice.name }}: {{ slice.traffic }} ({{ slice.pct }}%)</title>
                </path>
              </svg>
            </div>

            <!-- Table -->
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

      <!-- Additional Web Protection Report Rows -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
        <div class="bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden">
          <div class="p-3 bg-[#f4f6f9] border-b border-slate-200 font-bold text-slate-800 flex justify-between">
            <span>Top Sites By Time Spent</span>
            <span class="text-[#0072ce]">▶</span>
          </div>
          <div class="p-3 text-center text-slate-400">No data is available for this report</div>
        </div>

        <div class="bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden">
          <div class="p-3 bg-[#f4f6f9] border-b border-slate-200 font-bold text-slate-800 flex justify-between">
            <span>Top Users By Time Spent</span>
            <span class="text-[#0072ce]">▶</span>
          </div>
          <div class="p-3 text-center text-slate-400">No data is available for this report</div>
        </div>

        <div class="bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden">
          <div class="p-3 bg-[#f4f6f9] border-b border-slate-200 font-bold text-slate-800 flex justify-between">
            <span>Top Sites By Traffic</span>
            <span class="text-[#0072ce]">▶</span>
          </div>
          <div class="p-3 text-center text-slate-400">No data is available for this report</div>
        </div>

        <div class="bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden">
          <div class="p-3 bg-[#f4f6f9] border-b border-slate-200 font-bold text-slate-800 flex justify-between">
            <span>Top Blocked Categories</span>
            <span class="text-[#0072ce]">▶</span>
          </div>
          <div class="p-3 text-center text-slate-400">No data is available for this report</div>
        </div>
      </div>
    </div>

    <!-- ========================================================================= -->
    <!-- TAB 4: EXECUTIVE SUMMARY & PDF REPORTS                                     -->
    <!-- ========================================================================= -->
    <div v-if="activeTab === 'executive'" class="space-y-6">
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div class="bg-white border border-slate-200 rounded-xl p-4 shadow-xs">
          <div class="text-[11px] font-bold text-slate-500 uppercase tracking-wider">Total Threats Blocked</div>
          <div class="text-2xl font-black text-rose-600 mt-1">14,892</div>
          <div class="text-[10px] text-emerald-600 font-semibold mt-1 flex items-center gap-1">
            <span>&uarr; 12%</span> vs last week
          </div>
        </div>

        <div class="bg-white border border-slate-200 rounded-xl p-4 shadow-xs">
          <div class="text-[11px] font-bold text-slate-500 uppercase tracking-wider">Network Traffic Inspected</div>
          <div class="text-2xl font-black text-blue-700 mt-1">3.9 GB</div>
          <div class="text-[10px] text-slate-500 mt-1">3,562,702 packets today</div>
        </div>

        <div class="bg-white border border-slate-200 rounded-xl p-4 shadow-xs">
          <div class="text-[11px] font-bold text-slate-500 uppercase tracking-wider">Spam &amp; Phishing Filtered</div>
          <div class="text-2xl font-black text-amber-600 mt-1">3,410</div>
          <div class="text-[10px] text-slate-500 mt-1">99.4% Spam Catch Rate</div>
        </div>

        <div class="bg-white border border-slate-200 rounded-xl p-4 shadow-xs">
          <div class="text-[11px] font-bold text-slate-500 uppercase tracking-wider">Gateway Uptime</div>
          <div class="text-2xl font-black text-emerald-600 mt-1">99.98%</div>
          <div class="text-[10px] text-slate-500 mt-1">No unscheduled outages</div>
        </div>
      </div>

      <!-- Action: Generate Executive Report PDF -->
      <div class="bg-gradient-to-r from-[#005299] to-[#003366] rounded-xl p-6 text-white shadow-xs flex flex-col sm:flex-row items-center justify-between gap-4">
        <div>
          <h2 class="text-base font-bold">Generate Comprehensive Executive Report (PDF)</h2>
          <p class="text-xs text-blue-100 mt-1">Compile full network accounting, top threats, web protection logs, and mail activity into a branded report.</p>
        </div>
        <button
          type="button"
          @click="generatePdfReport"
          class="px-5 py-2.5 bg-white hover:bg-slate-100 text-[#005299] rounded-lg text-xs font-bold shadow-xs cursor-pointer flex items-center gap-2 whitespace-nowrap"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          <span>Download Executive PDF</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  authToken: {
    type: String,
    default: ''
  }
})

const activeTab = ref('network_stats')

const tabs = [
  { id: 'network_stats', label: 'Network Statistics', icon: '🌐' },
  { id: 'network_protection', label: 'Network Protection', icon: '🛡️' },
  { id: 'web_protection', label: 'Web Protection', icon: '🌍' },
  { id: 'executive', label: 'Executive Summary & PDF', icon: '📊' }
]

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

// -----------------------------------------------------------------------------
// Tab 1: Network Statistics Data (Matching Screenshot 4)
// -----------------------------------------------------------------------------
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

// -----------------------------------------------------------------------------
// Tab 2: Network Protection Statistics Data (Matching Screenshots 1 & 5)
// -----------------------------------------------------------------------------
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

// -----------------------------------------------------------------------------
// Tab 3: Web Protection Statistics Data (Matching Screenshot 2)
// -----------------------------------------------------------------------------
const topApps = ref([
  { name: 'Disney+', traffic: '996.9 MB', pct: 24.95, color: '#00838f' },
  { name: 'YouTube', traffic: '541.3 MB', pct: 13.54, color: '#00bcd4' },
  { name: 'Unclassified', traffic: '471.2 MB', pct: 11.79, color: '#0288d1' },
  { name: 'Akamai', traffic: '440.3 MB', pct: 11.02, color: '#1565c0' },
  { name: 'Amazon Prime Video', traffic: '375.7 MB', pct: 9.40, color: '#6a1b9a' },
  { name: 'QUIC IETF', traffic: '329.1 MB', pct: 8.24, color: '#ad1457' },
  { name: 'Astaro Up2Date', traffic: '166.5 MB', pct: 4.17, color: '#c2185b' },
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

const generatePdfReport = () => {
  alert('Generated Astaro-Next Weekly Executive Security Report (PDF).')
}
</script>
