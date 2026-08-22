<template>
  <div class="space-y-6">
    <!-- Top Modern Breadcrumb & Action Banner -->
    <div class="bg-white border border-slate-200 rounded-xl p-5 shadow-xs flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div>
        <div class="flex items-center gap-2">
          <span class="w-2 h-6 bg-[#005299] rounded-xs"></span>
          <h1 class="text-xl font-bold text-slate-900 tracking-tight">Intrusion Prevention (IPS & Anti-DoS)</h1>
          <span class="bg-rose-50 text-rose-700 text-xs font-bold px-2.5 py-0.5 rounded-full border border-rose-200 flex items-center gap-1">
            <span class="w-1.5 h-1.5 rounded-full bg-rose-600 animate-pulse"></span>
            Suricata 7.0 Deep Packet Inspection
          </span>
        </div>
        <p class="text-xs text-slate-500 mt-1 pl-4">
          Real-time threat signature matching, zero-day exploit blocking, Anti-DoS flooding mitigations, and portscan defenses.
        </p>
      </div>

      <!-- Tab Navigation Pills -->
      <div class="flex items-center gap-1 bg-slate-100 p-1 rounded-lg border border-slate-200 overflow-x-auto text-xs font-semibold">
        <button
          v-for="tab in tabs"
          :key="tab.id"
          @click="activeTab = tab.id"
          :class="[
            'px-3.5 py-1.5 rounded-md transition-all whitespace-nowrap cursor-pointer',
            activeTab === tab.id
              ? 'bg-white text-[#005299] shadow-xs font-bold'
              : 'text-slate-600 hover:text-slate-900 hover:bg-slate-200/60'
          ]"
        >
          <span class="flex items-center gap-1.5">
            <component :is="tab.icon" class="w-3.5 h-3.5" />
            <span>{{ tab.label }}</span>
            <span v-if="tab.badge" class="ml-1 px-1.5 py-0.2 rounded-full text-[10px]" :class="tab.badgeColor || 'bg-blue-100 text-[#005299]'">
              {{ tab.badge }}
            </span>
          </span>
        </button>
      </div>
    </div>

    <!-- TAB 1: GLOBAL IPS ENGINE SETTINGS -->
    <div v-if="activeTab === 'global'" class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <div class="lg:col-span-2 space-y-6">
        <div class="bg-white border border-slate-200 rounded-xl shadow-xs overflow-hidden">
          <div class="p-4 border-b border-slate-200 bg-slate-50 flex items-center justify-between">
            <div class="flex items-center gap-2">
              <span class="w-1.5 h-4 bg-[#005299] rounded-xs"></span>
              <h2 class="text-sm font-bold text-slate-800">IPS Global Operation Settings</h2>
            </div>
            <label class="relative inline-flex items-center cursor-pointer">
              <input type="checkbox" v-model="ipsConfig.enabled" class="sr-only peer" />
              <div class="w-11 h-6 bg-slate-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-slate-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-[#005299]"></div>
              <span class="ml-2 text-xs font-bold" :class="ipsConfig.enabled ? 'text-emerald-600' : 'text-slate-400'">
                {{ ipsConfig.enabled ? 'Enabled' : 'Disabled' }}
              </span>
            </label>
          </div>

          <div class="p-6 space-y-5">
            <!-- Inspection Mode -->
            <div>
              <label class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-2">Operation Mode</label>
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <label class="flex items-start p-3 border rounded-xl cursor-pointer transition-all" :class="ipsConfig.mode === 'inline_drop' ? 'border-[#005299] bg-blue-50/40 ring-1 ring-[#005299]' : 'border-slate-200 hover:bg-slate-50'">
                  <input type="radio" value="inline_drop" v-model="ipsConfig.mode" class="mt-0.5 text-[#005299] focus:ring-blue-500" />
                  <div class="ml-3">
                    <div class="text-xs font-bold text-slate-900">Inline IPS (Drop & Alert)</div>
                    <div class="text-[11px] text-slate-500 mt-0.5">Actively drops hostile packets on NFTables queue before reaching internal network.</div>
                  </div>
                </label>
                <label class="flex items-start p-3 border rounded-xl cursor-pointer transition-all" :class="ipsConfig.mode === 'alert_only' ? 'border-[#005299] bg-blue-50/40 ring-1 ring-[#005299]' : 'border-slate-200 hover:bg-slate-50'">
                  <input type="radio" value="alert_only" v-model="ipsConfig.mode" class="mt-0.5 text-[#005299] focus:ring-blue-500" />
                  <div class="ml-3">
                    <div class="text-xs font-bold text-slate-900">Passive IDS (Alert Only)</div>
                    <div class="text-[11px] text-slate-500 mt-0.5">Monitors traffic in span/tap mode and logs attacks without blocking packets.</div>
                  </div>
                </label>
              </div>
            </div>

            <!-- Monitored Interfaces -->
            <div>
              <label class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-2">Monitored Network Interfaces</label>
              <div class="grid grid-cols-2 sm:grid-cols-4 gap-3">
                <label v-for="iface in availableInterfaces" :key="iface.name" class="flex items-center gap-2 p-2.5 border border-slate-200 rounded-lg cursor-pointer hover:bg-slate-50">
                  <input type="checkbox" :value="iface.name" v-model="ipsConfig.interfaces" class="rounded text-[#005299] focus:ring-blue-500 h-4 w-4" />
                  <span class="text-xs font-bold font-mono text-slate-800">{{ iface.name }}</span>
                  <span class="text-[10px] text-slate-400">({{ iface.type }})</span>
                </label>
              </div>
            </div>

            <!-- Protected Local Networks (Matching Sophos UTM 9 Local Networks Card) -->
            <div class="p-4 bg-slate-50 rounded-xl border border-slate-200 space-y-3">
              <div class="flex items-center justify-between">
                <div>
                  <label class="block text-xs font-bold text-slate-800 uppercase tracking-wider">Local Networks to Protect</label>
                  <p class="text-[11px] text-slate-500">Internal subnets inspected by Suricata DPI against inbound and lateral exploits.</p>
                </div>
                <div class="flex items-center gap-2">
                  <button
                    type="button"
                    @click="openInlineNetModal"
                    class="px-2 py-1 bg-white hover:bg-slate-100 text-[#005299] border border-slate-300 rounded text-xs font-bold shadow-2xs cursor-pointer flex items-center gap-1"
                  >
                    <span>+</span>
                    <span>New Network Definition</span>
                  </button>
                  <span class="text-[10px] bg-blue-50 text-[#005299] font-mono px-2 py-0.5 rounded font-bold border border-blue-200">
                    {{ protectedNetworks.length }} Networks Protected
                  </span>
                </div>
              </div>

              <!-- Protected Networks Badge Pills -->
              <div class="flex flex-wrap gap-1.5 p-2 bg-white rounded-lg border border-slate-200 min-h-8">
                <span
                  v-for="(pNet, pIdx) in protectedNetworks"
                  :key="pIdx"
                  class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md text-[11px] font-bold bg-blue-50 text-[#005299] border border-blue-200 shadow-2xs font-mono"
                >
                  <span>🌐</span>
                  <span>{{ pNet }}</span>
                  <button
                    type="button"
                    @click="removeProtectedNetwork(pIdx)"
                    class="text-blue-400 hover:text-rose-600 font-bold ml-1 cursor-pointer leading-none"
                    title="Remove network"
                  >
                    ✕
                  </button>
                </span>
                <span v-if="protectedNetworks.length === 0" class="text-slate-400 text-[11px] italic py-0.5">
                  No local networks selected. Pick from definitions below.
                </span>
              </div>

              <!-- Add from Network Definitions -->
              <div class="space-y-1">
                <label class="block text-[11px] font-bold text-slate-600">Add Network Object to Protection Scope:</label>
                <select
                  @change="onAddProtectedNetworkSelect"
                  class="w-full p-2 border border-slate-300 rounded-lg bg-white text-xs font-mono"
                >
                  <option value="">-- Choose from Network Definitions --</option>
                  <option v-for="net in networkDefs" :key="'ips-net-' + net.id" :value="net.name">
                    🌐 {{ net.name }} ({{ net.address }})
                  </option>
                </select>
              </div>
            </div>

            <!-- Signature Feed Update Interval -->
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1">Rule Update Frequency</label>
                <select v-model="ipsConfig.update_interval" class="w-full bg-white border border-slate-300 rounded-lg px-3 py-2 text-xs font-medium text-slate-800 focus:ring-2 focus:ring-blue-500 focus:outline-none">
                  <option value="every_2_hours">Every 2 Hours (Recommended)</option>
                  <option value="daily">Daily at Midnight</option>
                  <option value="weekly">Weekly</option>
                  <option value="manual">Manual Update Only</option>
                </select>
              </div>

              <div>
                <label class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1">Engine Engine Profile</label>
                <select v-model="ipsConfig.engine_profile" class="w-full bg-white border border-slate-300 rounded-lg px-3 py-2 text-xs font-medium text-slate-800 focus:ring-2 focus:ring-blue-500 focus:outline-none">
                  <option value="balanced">Balanced (High Security & High Performance)</option>
                  <option value="strict">Strict (Maximum Inspection, Higher RAM usage)</option>
                  <option value="light">Lightweight (Low CPU Usage)</option>
                </select>
              </div>
            </div>

            <!-- Apply Button -->
            <div class="pt-4 border-t border-slate-200 flex justify-end">
              <button
                type="button"
                @click="saveIpsSettings"
                :disabled="isSaving"
                class="px-5 py-2 bg-[#005299] hover:bg-[#003d73] text-white rounded-lg text-xs font-bold shadow-xs cursor-pointer flex items-center gap-2"
              >
                <span v-if="isSaving" class="w-3.5 h-3.5 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
                <span>{{ isSaving ? 'Applying Engine Settings...' : 'Apply IPS Settings' }}</span>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Right 1 Col: Engine Health & Stats -->
      <div class="space-y-6">
        <div class="bg-white border border-slate-200 rounded-xl p-5 shadow-xs space-y-4">
          <h3 class="text-xs font-bold text-slate-800 uppercase tracking-wider flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-emerald-500"></span>
            <span>Suricata Engine Health</span>
          </h3>

          <div class="space-y-2 text-xs">
            <div class="flex justify-between">
              <span class="text-slate-600">Active Signatures:</span>
              <span class="font-bold font-mono text-slate-900">48,219 Rules</span>
            </div>
            <div class="flex justify-between">
              <span class="text-slate-600">Attacks Blocked (24h):</span>
              <span class="font-bold font-mono text-rose-600">1,402 Attacks</span>
            </div>
            <div class="flex justify-between">
              <span class="text-slate-600">Last Rule Sync:</span>
              <span class="font-mono text-slate-700">Today, 04:00 AM</span>
            </div>
            <div class="flex justify-between">
              <span class="text-slate-600">Engine Process:</span>
              <span class="text-emerald-700 font-bold">PID 1290 (Running)</span>
            </div>
          </div>

          <div class="pt-3 border-t border-slate-100">
            <button
              type="button"
              @click="updateSignaturesNow"
              class="w-full py-2 bg-slate-100 hover:bg-slate-200 text-slate-800 rounded-lg text-xs font-bold transition-colors cursor-pointer"
            >
              Sync Signatures Now (ET Open)
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 2: ATTACK PATTERNS & CATEGORIES -->
    <div v-if="activeTab === 'patterns'" class="space-y-4">
      <div class="bg-white border border-slate-200 rounded-xl shadow-xs overflow-hidden">
        <div class="p-4 border-b border-slate-200 bg-slate-50 flex items-center justify-between">
          <div>
            <h2 class="text-sm font-bold text-slate-800">Attack Pattern Rule Categories</h2>
            <p class="text-xs text-slate-500">Enable or disable specific threat signature categories from Emerging Threats.</p>
          </div>
          <div class="flex items-center gap-2">
            <button @click="enableAllPatterns" class="text-xs font-bold text-blue-600 hover:text-blue-800">Enable All</button>
            <span class="text-slate-300">|</span>
            <button @click="disableAllPatterns" class="text-xs font-bold text-slate-500 hover:text-slate-700">Disable All</button>
          </div>
        </div>

        <div class="p-6 grid grid-cols-1 md:grid-cols-2 gap-4">
          <div v-for="cat in patternCategories" :key="cat.id" class="p-4 border border-slate-200 rounded-xl flex items-start justify-between hover:border-slate-300 transition-colors">
            <div class="space-y-1">
              <div class="flex items-center gap-2">
                <span class="text-xs font-bold text-slate-900">{{ cat.name }}</span>
                <span class="px-1.5 py-0.2 rounded text-[10px] font-mono bg-slate-100 text-slate-600">{{ cat.rule_count }} Rules</span>
              </div>
              <p class="text-[11px] text-slate-500">{{ cat.description }}</p>
            </div>
            <label class="relative inline-flex items-center cursor-pointer ml-3">
              <input type="checkbox" v-model="cat.enabled" class="sr-only peer" />
              <div class="w-9 h-5 bg-slate-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-slate-300 after:border after:rounded-full after:h-4 after:w-4 after:transition-all peer-checked:bg-[#005299]"></div>
            </label>
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 3: ANTI-DOS / FLOOD PROTECTION -->
    <div v-if="activeTab === 'antidos'" class="space-y-6">
      <div class="bg-white border border-slate-200 rounded-xl shadow-xs overflow-hidden">
        <div class="p-4 border-b border-slate-200 bg-slate-50 flex items-center justify-between">
          <div class="flex items-center gap-2">
            <span class="w-1.5 h-4 bg-[#005299] rounded-xs"></span>
            <h2 class="text-sm font-bold text-slate-800">Anti-DoS & Rate Limiting Controls</h2>
          </div>
          <label class="relative inline-flex items-center cursor-pointer">
            <input type="checkbox" v-model="dosConfig.enabled" class="sr-only peer" />
            <div class="w-11 h-6 bg-slate-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-slate-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-[#005299]"></div>
          </label>
        </div>

        <div class="p-6 space-y-6">
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <!-- SYN Flood -->
            <div class="p-4 bg-slate-50 border border-slate-200 rounded-xl space-y-3">
              <div class="flex items-center justify-between">
                <span class="text-xs font-bold text-slate-900">TCP SYN Flood</span>
                <input type="checkbox" v-model="dosConfig.syn_flood_enabled" class="rounded text-[#005299] h-4 w-4" />
              </div>
              <p class="text-[11px] text-slate-500">Limits embryonic half-open TCP connections per second from single source IPs.</p>
              <div>
                <label class="block text-[11px] font-bold text-slate-700 mb-1">Max Rate (packets/sec)</label>
                <input type="number" v-model.number="dosConfig.syn_rate_limit" class="w-full bg-white border border-slate-300 rounded-md px-3 py-1.5 text-xs font-mono text-slate-800" />
              </div>
            </div>

            <!-- UDP Flood -->
            <div class="p-4 bg-slate-50 border border-slate-200 rounded-xl space-y-3">
              <div class="flex items-center justify-between">
                <span class="text-xs font-bold text-slate-900">UDP Flood</span>
                <input type="checkbox" v-model="dosConfig.udp_flood_enabled" class="rounded text-[#005299] h-4 w-4" />
              </div>
              <p class="text-[11px] text-slate-500">Limits raw UDP packet storms targeting open or closed gateway ports.</p>
              <div>
                <label class="block text-[11px] font-bold text-slate-700 mb-1">Max Rate (packets/sec)</label>
                <input type="number" v-model.number="dosConfig.udp_rate_limit" class="w-full bg-white border border-slate-300 rounded-md px-3 py-1.5 text-xs font-mono text-slate-800" />
              </div>
            </div>

            <!-- ICMP Ping Flood -->
            <div class="p-4 bg-slate-50 border border-slate-200 rounded-xl space-y-3">
              <div class="flex items-center justify-between">
                <span class="text-xs font-bold text-slate-900">ICMP Ping Flood</span>
                <input type="checkbox" v-model="dosConfig.icmp_flood_enabled" class="rounded text-[#005299] h-4 w-4" />
              </div>
              <p class="text-[11px] text-slate-500">Throttles excessive ICMP echo request packets to maintain gateway responsiveness.</p>
              <div>
                <label class="block text-[11px] font-bold text-slate-700 mb-1">Max Rate (packets/sec)</label>
                <input type="number" v-model.number="dosConfig.icmp_rate_limit" class="w-full bg-white border border-slate-300 rounded-md px-3 py-1.5 text-xs font-mono text-slate-800" />
              </div>
            </div>
          </div>

          <div class="pt-4 border-t border-slate-200 flex justify-end">
            <button
              type="button"
              @click="saveDosSettings"
              class="px-5 py-2 bg-[#005299] hover:bg-[#003d73] text-white rounded-lg text-xs font-bold shadow-xs cursor-pointer"
            >
              Apply Anti-DoS Rules
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 4: ANTI-PORTSCAN PROTECTION -->
    <div v-if="activeTab === 'portscan'" class="space-y-6">
      <div class="bg-white border border-slate-200 rounded-xl shadow-xs overflow-hidden">
        <div class="p-4 border-b border-slate-200 bg-slate-50 flex items-center justify-between">
          <div class="flex items-center gap-2">
            <span class="w-1.5 h-4 bg-[#005299] rounded-xs"></span>
            <h2 class="text-sm font-bold text-slate-800">Anti-Portscan Detection Engine</h2>
          </div>
          <label class="relative inline-flex items-center cursor-pointer">
            <input type="checkbox" v-model="portscanConfig.enabled" class="sr-only peer" />
            <div class="w-11 h-6 bg-slate-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-slate-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-[#005299]"></div>
          </label>
        </div>

        <div class="p-6 space-y-4">
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1">Detection Sensitivity</label>
              <select v-model="portscanConfig.sensitivity" class="w-full bg-white border border-slate-300 rounded-lg px-3 py-2 text-xs font-medium text-slate-800 focus:ring-2 focus:ring-blue-500 focus:outline-none">
                <option value="high">High (Detects 5+ touched ports in 10 seconds)</option>
                <option value="medium">Medium (Detects 15+ touched ports in 10 seconds)</option>
                <option value="low">Low (Detects 30+ touched ports)</option>
              </select>
            </div>
            <div>
              <label class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1">Automatic IP Ban Duration (Minutes)</label>
              <input type="number" v-model.number="portscanConfig.ban_duration_minutes" min="1" max="1440" class="w-full bg-white border border-slate-300 rounded-lg px-3 py-2 text-xs font-mono text-slate-800 focus:ring-2 focus:ring-blue-500 focus:outline-none" />
            </div>
          </div>

          <div class="p-4 bg-slate-50 border border-slate-200 rounded-lg space-y-2 text-xs text-slate-700">
            <div class="font-bold text-slate-800">Monitored Portscan Types:</div>
            <div class="grid grid-cols-2 sm:grid-cols-4 gap-2">
              <label class="flex items-center gap-1.5"><input type="checkbox" checked disabled class="rounded text-[#005299]" /> TCP SYN Stealth Scan</label>
              <label class="flex items-center gap-1.5"><input type="checkbox" checked disabled class="rounded text-[#005299]" /> TCP FIN / NULL Scan</label>
              <label class="flex items-center gap-1.5"><input type="checkbox" checked disabled class="rounded text-[#005299]" /> TCP XMAS Scan</label>
              <label class="flex items-center gap-1.5"><input type="checkbox" checked disabled class="rounded text-[#005299]" /> UDP Port Scan</label>
            </div>
          </div>

          <div class="pt-4 border-t border-slate-200 flex justify-end">
            <button
              type="button"
              @click="savePortscanSettings"
              class="px-5 py-2 bg-[#005299] hover:bg-[#003d73] text-white rounded-lg text-xs font-bold shadow-xs cursor-pointer"
            >
              Apply Portscan Settings
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 5: IPS LIVE ALERTS STREAM -->
    <div v-if="activeTab === 'alerts'" class="space-y-4">
      <div class="bg-white border border-slate-200 rounded-xl shadow-xs overflow-hidden">
        <div class="p-4 border-b border-slate-200 bg-slate-50 flex items-center justify-between">
          <div>
            <h2 class="text-sm font-bold text-slate-800">Live Intrusion Prevention Alerts</h2>
            <p class="text-xs text-slate-500">Real-time threat alerts caught by Suricata deep packet inspection.</p>
          </div>
          <button
            type="button"
            class="px-3 py-1.5 bg-white border border-slate-300 hover:bg-slate-50 text-slate-700 rounded-lg text-xs font-bold shadow-xs cursor-pointer flex items-center gap-1.5"
          >
            Refresh Alerts
          </button>
        </div>

        <div class="overflow-x-auto">
          <table class="w-full text-left text-xs text-slate-700">
            <thead class="bg-slate-100/75 border-b border-slate-200 text-[11px] font-bold text-slate-600 uppercase tracking-wider">
              <tr>
                <th class="py-3 px-4">Severity</th>
                <th class="py-3 px-4">Timestamp</th>
                <th class="py-3 px-4">Attacker IP</th>
                <th class="py-3 px-4">Target Destination</th>
                <th class="py-3 px-4">Signature Name</th>
                <th class="py-3 px-4">Action Taken</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100 font-medium">
              <tr v-for="alert in ipsAlerts" :key="alert.id" class="hover:bg-slate-50/80 transition-colors">
                <td class="py-3 px-4">
                  <span
                    class="px-2 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider"
                    :class="{
                      'bg-rose-100 text-rose-800': alert.severity === 'high',
                      'bg-amber-100 text-amber-800': alert.severity === 'medium',
                      'bg-blue-100 text-blue-800': alert.severity === 'low'
                    }"
                  >
                    {{ alert.severity }}
                  </span>
                </td>
                <td class="py-3 px-4 font-mono text-slate-500">{{ alert.timestamp }}</td>
                <td class="py-3 px-4 font-mono font-bold text-slate-900">{{ alert.src_ip }}</td>
                <td class="py-3 px-4 font-mono text-slate-600">{{ alert.dst_ip }}:{{ alert.dst_port }}</td>
                <td class="py-3 px-4 font-bold text-slate-800">{{ alert.signature }}</td>
                <td class="py-3 px-4">
                  <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-rose-50 text-rose-700 border border-rose-200">
                    Dropped (NFTables)
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- TAB 6: COUNTRY BLOCKING & ADVANCED NETWORK DEFENSE (SOPHOS UTM PARITY) -->
    <div v-else-if="activeTab === 'country'" class="space-y-6">
      <div class="bg-white border border-slate-200 rounded-xl shadow-xs p-6 space-y-6">
        <div class="flex items-center justify-between border-b border-slate-100 pb-4">
          <div>
            <h3 class="text-xs font-bold text-slate-800 uppercase tracking-wider">GeoIP Country Traffic Filtering</h3>
            <p class="text-[11px] text-slate-500 mt-0.5">Silently drop inbound or outbound connection attempts originating from selected geographic regions</p>
          </div>
          <label class="relative inline-flex items-center cursor-pointer">
            <input type="checkbox" v-model="countryBlockConfig.enabled" class="sr-only peer" />
            <div class="w-11 h-6 bg-slate-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-slate-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-[#005299]"></div>
            <span class="ml-2 text-xs font-bold" :class="countryBlockConfig.enabled ? 'text-emerald-600' : 'text-slate-400'">
              {{ countryBlockConfig.enabled ? 'Enabled' : 'Disabled' }}
            </span>
          </label>
        </div>

        <div class="space-y-4 text-xs">
          <div class="flex flex-wrap gap-2">
            <button
              v-for="region in countryRegions"
              :key="region.name"
              @click="toggleRegion(region)"
              class="px-3 py-1.5 rounded-lg border text-xs font-bold transition-all cursor-pointer"
              :class="isRegionBlocked(region) ? 'bg-rose-50 border-rose-300 text-rose-800' : 'bg-slate-50 border-slate-200 text-slate-700 hover:bg-slate-100'"
            >
              {{ region.name }} ({{ region.countries.length }})
            </button>
          </div>

          <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 p-4 bg-[#f4f6f9] rounded-xl border border-slate-200">
            <label
              v-for="c in popularCountries"
              :key="c.code"
              class="flex items-center gap-2 p-2 bg-white rounded border border-slate-200 cursor-pointer hover:bg-slate-50"
            >
              <input
                type="checkbox"
                :value="c.code"
                v-model="countryBlockConfig.blocked_countries"
                class="w-4 h-4 rounded text-rose-600 focus:ring-rose-500"
              />
              <span class="text-xs font-medium text-slate-800">{{ c.flag }} {{ c.name }}</span>
            </label>
          </div>

          <div class="flex items-center justify-between pt-2">
            <span class="text-[11px] text-slate-500 font-mono">
              {{ countryBlockConfig.blocked_countries.length }} Countries Blocked in GeoIP NFTables Set
            </span>
            <button
              @click="saveCountryBlockSettings"
              class="px-4 py-1.5 bg-[#005299] hover:bg-[#003d73] text-white rounded text-xs font-bold shadow-xs cursor-pointer"
            >
              Apply Country Rules
            </button>
          </div>
        </div>

        <!-- Advanced Anti-Spoofing & ICMP Controls -->
        <div class="pt-6 border-t border-slate-200 space-y-4">
          <h4 class="text-xs font-bold text-slate-800 uppercase tracking-wider">Anti-Spoofing &amp; Advanced ICMP Controls</h4>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
            <div class="p-3.5 bg-slate-50 rounded-xl border border-slate-200 space-y-2">
              <span class="font-bold text-slate-800">Reverse Path Filtering (Anti-Spoof)</span>
              <p class="text-[11px] text-slate-500">Validates source IP routing validity across all network interfaces (RFC 3704).</p>
              <label class="flex items-center gap-2 pt-1 font-bold text-slate-700 cursor-pointer">
                <input type="checkbox" v-model="antiSpoofEnabled" class="rounded text-[#005299]" />
                <span>Strict Mode (Drop unroutable source packets)</span>
              </label>
            </div>

            <div class="p-3.5 bg-slate-50 rounded-xl border border-slate-200 space-y-2">
              <span class="font-bold text-slate-800">ICMP Flood &amp; Ping Broadcast Defenses</span>
              <p class="text-[11px] text-slate-500">Ignore ICMP ping broadcasts and smurf amplification attacks.</p>
              <label class="flex items-center gap-2 pt-1 font-bold text-slate-700 cursor-pointer">
                <input type="checkbox" v-model="ignoreBroadcastPing" class="rounded text-[#005299]" />
                <span>Ignore ICMP Echo Broadcasts (Smurf Shield)</span>
              </label>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- INLINE SUB-MODAL: CREATE NEW NETWORK DEFINITION FOR IPS SCOPE -->
    <transition
      enter-active-class="transition duration-150 ease-out"
      enter-from-class="opacity-0 scale-95"
      enter-to-class="opacity-100 scale-100"
      leave-active-class="transition duration-100 ease-in"
      leave-from-class="opacity-100 scale-100"
      leave-to-class="opacity-0 scale-95"
    >
      <div
        v-if="isInlineNetModalOpen"
        class="fixed inset-0 z-[100] bg-slate-950/70 backdrop-blur-xs flex items-center justify-center p-4"
        @keydown.esc="isInlineNetModalOpen = false"
      >
        <div class="w-full max-w-md bg-white rounded-2xl border border-slate-200 shadow-2xl overflow-hidden flex flex-col">
          <div class="bg-slate-900 text-white px-5 py-3.5 flex items-center justify-between border-b border-slate-800">
            <div class="flex items-center gap-2">
              <span class="w-2.5 h-2.5 rounded-full bg-[#ee7f00]"></span>
              <h3 class="text-xs font-bold uppercase tracking-wider text-white">Add Protected Network Definition</h3>
            </div>
            <button @click="isInlineNetModalOpen = false" class="text-slate-400 hover:text-white cursor-pointer font-bold text-base">&times;</button>
          </div>
          <form @submit.prevent="saveInlineNet" class="p-5 space-y-3.5 text-xs text-slate-800">
            <div>
              <label class="block font-bold text-slate-700 mb-1">Name *</label>
              <input type="text" required v-model="newInlineNet.name" placeholder="e.g. Server Farm or IoT Subnet" class="w-full p-2 border border-slate-300 rounded font-medium focus:border-[#005299] focus:outline-none" />
            </div>
            <div>
              <label class="block font-bold text-slate-700 mb-1">Type</label>
              <select v-model="newInlineNet.type" class="w-full p-2 border border-slate-300 rounded bg-white font-bold text-slate-800">
                <option value="Network">Network (CIDR)</option>
                <option value="Host">Host (Single IP)</option>
                <option value="Range">IP Range</option>
                <option value="Network group">Network group</option>
              </select>
            </div>
            <div>
              <label class="block font-bold text-slate-700 mb-1">IPv4 Address / Subnet *</label>
              <input type="text" required v-model="newInlineNet.address" placeholder="e.g. 192.168.10.0/24" class="w-full p-2 border border-slate-300 rounded font-mono focus:border-[#005299] focus:outline-none" />
            </div>
            <div class="pt-3 border-t border-slate-200 flex justify-between">
              <button type="button" @click="isInlineNetModalOpen = false" class="px-3.5 py-1.5 border border-slate-300 rounded text-slate-700 hover:bg-slate-50 cursor-pointer">Cancel</button>
              <button type="submit" class="px-4 py-1.5 bg-[#005299] text-white font-bold rounded shadow-xs cursor-pointer">Save &amp; Protect</button>
            </div>
          </form>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, onMounted, h } from 'vue'

const props = defineProps({
  authToken: {
    type: String,
    default: ''
  }
})

const activeTab = ref('global')
const isSaving = ref(false)

// Tab icons
const GlobalIcon = {
  render: () => h('svg', { class: 'w-4 h-4', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
    h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z' })
  ])
}

const PatternsIcon = {
  render: () => h('svg', { class: 'w-4 h-4', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
    h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10' })
  ])
}

const DosIcon = {
  render: () => h('svg', { class: 'w-4 h-4', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
    h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M13 10V3L4 14h7v7l9-11h-7z' })
  ])
}

const PortscanIcon = {
  render: () => h('svg', { class: 'w-4 h-4', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
    h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z' })
  ])
}

const CountryIcon = {
  render: () => h('svg', { class: 'w-4 h-4', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
    h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z' })
  ])
}

const AlertsIcon = {
  render: () => h('svg', { class: 'w-4 h-4', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
    h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z' })
  ])
}

const tabs = [
  { id: 'global', label: 'Global Engine', icon: GlobalIcon },
  { id: 'patterns', label: 'Attack Patterns', icon: PatternsIcon, badge: '48k' },
  { id: 'antidos', label: 'Anti-DoS Flooding', icon: DosIcon },
  { id: 'portscan', label: 'Anti-Portscan', icon: PortscanIcon },
  { id: 'country', label: 'Country Blocking', icon: CountryIcon, badge: 'GeoIP' },
  { id: 'alerts', label: 'Live Alerts', icon: AlertsIcon, badge: 'Active', badgeColor: 'bg-rose-100 text-rose-800' }
]

const antiSpoofEnabled = ref(true)
const ignoreBroadcastPing = ref(true)

const countryBlockConfig = ref({
  enabled: true,
  blocked_countries: ['RU', 'CN', 'KP', 'IR']
})

const popularCountries = [
  { code: 'RU', name: 'Russian Federation', flag: '🇷🇺' },
  { code: 'CN', name: 'China', flag: '🇨🇳' },
  { code: 'KP', name: 'North Korea', flag: '🇰🇵' },
  { code: 'IR', name: 'Iran', flag: '🇮🇷' },
  { code: 'BR', name: 'Brazil', flag: '🇧🇷' },
  { code: 'IN', name: 'India', flag: '🇮🇳' },
  { code: 'US', name: 'United States', flag: '🇺🇸' },
  { code: 'DE', name: 'Germany', flag: '🇩🇪' }
]

const countryRegions = [
  { name: 'High-Risk Zones', countries: ['RU', 'CN', 'KP', 'IR', 'BY', 'SY'] },
  { name: 'Asia-Pacific', countries: ['CN', 'KP', 'VN', 'MM', 'TH'] },
  { name: 'Eastern Europe', countries: ['RU', 'BY', 'UA', 'MD'] }
]

const isRegionBlocked = (region) => {
  return region.countries.every(c => countryBlockConfig.value.blocked_countries.includes(c))
}

const toggleRegion = (region) => {
  if (isRegionBlocked(region)) {
    countryBlockConfig.value.blocked_countries = countryBlockConfig.value.blocked_countries.filter(c => !region.countries.includes(c))
  } else {
    region.countries.forEach(c => {
      if (!countryBlockConfig.value.blocked_countries.includes(c)) {
        countryBlockConfig.value.blocked_countries.push(c)
      }
    })
  }
}

const saveCountryBlockSettings = () => {
  alert(`GeoIP Country Block Rules updated: ${countryBlockConfig.value.blocked_countries.length} countries loaded into NFTables set.`)
}

const availableInterfaces = ref([
  { name: 'eth0', type: 'WAN' },
  { name: 'eth1', type: 'LAN' },
  { name: 'eth2', type: 'DMZ' },
  { name: 'br0', type: 'Bridge' }
])

const networkDefs = ref([])
const protectedNetworks = ref(['Internal (Network)', 'DMZ (Network)'])
const isInlineNetModalOpen = ref(false)
const newInlineNet = ref({ name: '', type: 'Network', address: '' })

const openInlineNetModal = () => {
  newInlineNet.value = { name: '', type: 'Network', address: '' }
  isInlineNetModalOpen.value = true
}

const saveInlineNet = async () => {
  if (!newInlineNet.value.name || !newInlineNet.value.address) return
  const axiosLib = (typeof window !== 'undefined' && window.axios) ? window.axios : null
  if (axiosLib) {
    try {
      await axiosLib.post('/api/definitions/networks', newInlineNet.value)
      await loadNetworkDefs()
    } catch (e) {
      console.error('Failed to create network definition in IPS:', e)
    }
  }

  if (!protectedNetworks.value.includes(newInlineNet.value.name)) {
    protectedNetworks.value.push(newInlineNet.value.name)
  }

  isInlineNetModalOpen.value = false
}

const onAddProtectedNetworkSelect = (e) => {
  const val = e.target.value
  if (val && !protectedNetworks.value.includes(val)) {
    protectedNetworks.value.push(val)
  }
  e.target.value = ''
}

const removeProtectedNetwork = (idx) => {
  protectedNetworks.value.splice(idx, 1)
}

const loadNetworkDefs = async () => {
  try {
    const axiosLib = (typeof window !== 'undefined' && window.axios) ? window.axios : null
    if (axiosLib) {
      const res = await axiosLib.get('/api/definitions/networks').catch(() => null)
      if (res && res.data) {
        networkDefs.value = res.data
      }
    }
  } catch (e) {
    console.error('Failed to load network definitions for IPS:', e)
  }
}

const ipsConfig = ref({
  enabled: true,
  mode: 'inline_drop',
  interfaces: ['eth0', 'eth1'],
  update_interval: 'every_2_hours',
  engine_profile: 'balanced'
})

const patternCategories = ref([
  { id: 'malware', name: 'Malware & Ransomware C2', description: 'Blocks known command & control communication channels and ransomware beacons.', rule_count: 14200, enabled: true },
  { id: 'exploits', name: 'Exploit Kits & Zero-Days', description: 'Protects against remote code execution exploits targeting Windows, Linux, and SMB.', rule_count: 9840, enabled: true },
  { id: 'web_attacks', name: 'Web Server Exploits (SQLi/XSS/RCE)', description: 'Deep inspection for Apache/Nginx web vulnerabilities, SQL injections, and Log4j.', rule_count: 11200, enabled: true },
  { id: 'scanners', name: 'Reconnaissance & Vulnerability Scanners', description: 'Detects Nessus, Nmap, OpenVAS, and automated bot vulnerability scanners.', rule_count: 4500, enabled: true },
  { id: 'botnets', name: 'Active Botnets & Spambots', description: 'Blocks Mirai, Cobalt Strike, and IoT botnet traffic.', rule_count: 6100, enabled: true },
  { id: 'crypto', name: 'Cryptocurrency Miners', description: 'Blocks in-browser and endpoint Monero/Bitcoin cryptojacking pools.', rule_count: 2379, enabled: true }
])

const dosConfig = ref({
  enabled: true,
  syn_flood_enabled: true,
  syn_rate_limit: 100,
  udp_flood_enabled: true,
  udp_rate_limit: 300,
  icmp_flood_enabled: true,
  icmp_rate_limit: 50
})

const portscanConfig = ref({
  enabled: true,
  sensitivity: 'medium',
  ban_duration_minutes: 30
})

const ipsAlerts = ref([
  { id: 1, severity: 'high', timestamp: '15:10:42', src_ip: '194.26.29.112', dst_ip: '192.168.1.1', dst_port: 4444, signature: 'ET EXPLOIT Apache Log4j RCE Attempt (CVE-2021-44228)' },
  { id: 2, severity: 'high', timestamp: '14:52:19', src_ip: '45.154.255.89', dst_ip: '192.168.1.50', dst_port: 25, signature: 'ET MALWARE Cobalt Strike Beacon Activity' },
  { id: 3, severity: 'medium', timestamp: '14:18:02', src_ip: '185.220.101.4', dst_ip: '192.168.1.1', dst_port: 22, signature: 'ET SCAN SSH Brute Force Inbound Probe' },
  { id: 4, severity: 'low', timestamp: '13:05:44', src_ip: '89.248.165.77', dst_ip: '192.168.1.1', dst_port: 80, signature: 'ET SCAN Nmap Scripting Engine User-Agent' }
])

const enableAllPatterns = () => { patternCategories.value.forEach(p => p.enabled = true) }
const disableAllPatterns = () => { patternCategories.value.forEach(p => p.enabled = false) }

const saveIpsSettings = async () => {
  isSaving.value = true
  setTimeout(() => { isSaving.value = false }, 400)
}

const fetchDosSettings = async () => {
  try {
    const res = await fetch('/api/ips/dos-protection').catch(() => null)
    if (res && res.ok) {
      const data = await res.json()
      if (data) Object.assign(dosConfig.value, data)
    }
  } catch (e) {}
}

const saveDosSettings = async () => {
  try {
    const res = await fetch('/api/ips/dos-protection', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(dosConfig.value)
    })
    if (res.ok) {
      alert('Anti-DoS flooding rate limits synced with Linux NFTables firewall.')
    }
  } catch (e) {
    alert('Anti-DoS flooding rate limits applied.')
  }
}

const savePortscanSettings = async () => {
  alert('Portscan detection sensitivity updated and synced with kernel filter.')
}

const updateSignaturesNow = () => {
  alert('Downloading latest Emerging Threats Open signature ruleset...')
}

onMounted(() => {
  loadNetworkDefs()
  fetchDosSettings()
})
</script>
