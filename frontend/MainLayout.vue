<template>
  <div class="min-h-screen bg-[#161e29] text-slate-100 font-sans flex flex-col antialiased selection:bg-[#0072ce] selection:text-white">
    <!-- Top Global System Header Bar (Astaro / Sophos UTM Style) -->
    <header class="bg-[#1b232e] border-b border-slate-700/80 sticky top-0 z-50 flex-none shadow-sm">
      <!-- High-contrast corporate Astaro Orange top accent bar -->
      <div class="h-1 w-full bg-[#ee7f00]"></div>

      <div class="px-4 py-2.5 flex items-center justify-between gap-4">
        <!-- Left: Brand Logo & Mobile Toggle -->
        <div class="flex items-center gap-3">
          <!-- Mobile Menu Drawer Toggle -->
          <button
            type="button"
            @click="isMobileMenuOpen = !isMobileMenuOpen"
            class="lg:hidden inline-flex items-center justify-center p-2 rounded-md text-slate-400 hover:text-white hover:bg-slate-800 focus:outline-none focus:ring-2 focus:ring-[#ee7f00] transition-colors"
            aria-label="Toggle navigation menu"
            :aria-expanded="isMobileMenuOpen"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path v-if="!isMobileMenuOpen" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
              <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>

          <!-- Astaro-Next Appliance Brand Identity -->
          <div class="flex items-center gap-3 select-none">
            <div class="w-8 h-8 rounded bg-[#005299] flex items-center justify-center shadow-md font-extrabold text-white text-base tracking-wider ring-1 ring-blue-400/30">
              <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
              </svg>
            </div>
            <div class="flex flex-col">
              <div class="flex items-center gap-2">
                <span class="text-sm font-black tracking-tight text-white uppercase">Astaro<span class="text-[#ee7f00]">-Next</span></span>
                <span class="text-[10px] bg-blue-950 text-blue-300 font-mono font-bold px-1.5 py-0.5 rounded border border-blue-800/60">v2.4.0</span>
              </div>
              <span class="text-[10px] text-slate-400 font-medium tracking-wide">Next-Gen Firewall OS</span>
            </div>
          </div>
        </div>

        <!-- Center: Quick Search Filter Bar -->
        <div class="hidden md:flex flex-1 max-w-md mx-4">
          <div class="relative w-full">
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Search features, definitions, rules, interfaces..."
              class="w-full bg-slate-950/80 text-slate-200 text-xs px-3 py-1.5 pl-8 rounded-md border border-slate-700/80 focus:outline-none focus:border-[#0072ce] focus:ring-1 focus:ring-[#0072ce] placeholder:text-slate-500 transition-colors"
            />
            <svg class="w-3.5 h-3.5 text-slate-400 absolute left-2.5 top-2.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
            <button
              v-if="searchQuery"
              @click="searchQuery = ''"
              class="absolute right-2.5 top-2 text-slate-500 hover:text-slate-300"
            >
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>

        <!-- Right: Appliance Telemetry & Admin Profile -->
        <div class="flex items-center gap-4 text-xs font-mono">
          <!-- Telemetry Badges (Desktop) -->
          <div class="hidden xl:flex items-center gap-4 bg-slate-950/60 px-3 py-1.5 rounded-md border border-slate-800">
            <!-- Hostname -->
            <div class="flex items-center gap-1.5 text-slate-300">
              <span class="w-2 h-2 rounded-full bg-emerald-500"></span>
              <span class="text-slate-400">HOST:</span>
              <span class="font-semibold text-slate-200">{{ applianceHost }}</span>
            </div>
            <div class="w-px h-3.5 bg-slate-800"></div>

            <!-- CPU Metric -->
            <div class="flex items-center gap-1.5">
              <span class="text-slate-400">CPU:</span>
              <span :class="cpuUsage > 80 ? 'text-rose-400 font-bold' : 'text-emerald-400 font-semibold'">{{ cpuUsage }}%</span>
            </div>
            <div class="w-px h-3.5 bg-slate-800"></div>

            <!-- RAM Metric -->
            <div class="flex items-center gap-1.5">
              <span class="text-slate-400">RAM:</span>
              <span :class="memUsage > 85 ? 'text-rose-400 font-bold' : 'text-emerald-400 font-semibold'">{{ memUsage }}%</span>
            </div>
            <div class="w-px h-3.5 bg-slate-800"></div>

            <!-- Uptime -->
            <div class="flex items-center gap-1.5 text-slate-400">
              <span>UP:</span>
              <span class="text-slate-200">{{ uptime }}</span>
            </div>
          </div>

          <!-- User Account Menu & Logout -->
          <div class="flex items-center gap-3">
            <div class="hidden sm:flex flex-col text-right">
              <span class="text-xs font-semibold text-slate-200">{{ currentUser }}</span>
              <span class="text-[10px] text-emerald-400 font-sans flex items-center justify-end gap-1">
                <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span> Administrator
              </span>
            </div>

            <button
              type="button"
              @click="handleLogout"
              class="px-2.5 py-1.5 text-xs font-medium rounded bg-slate-800 hover:bg-rose-600 hover:text-white text-slate-300 border border-slate-700 hover:border-rose-500 transition-colors flex items-center gap-1.5"
              title="Log out of SFOS Console"
            >
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
              </svg>
              <span class="hidden sm:inline font-sans">Logout</span>
            </button>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Body: Sidebar Navigation + Light Main Content Area -->
    <div class="flex-1 flex overflow-hidden">
      <!-- Mobile Backdrop Overlay -->
      <div
        v-if="isMobileMenuOpen"
        @click="isMobileMenuOpen = false"
        class="fixed inset-0 bg-slate-950/80 backdrop-blur-sm z-30 lg:hidden"
        aria-hidden="true"
      ></div>

      <!-- Sophos UTM Dark Slate Sidebar Container (bg-[#1a2332]) -->
      <aside
        :class="[
          'fixed lg:static inset-y-0 left-0 z-40 w-64 bg-[#1a2332] border-r border-slate-700/80 flex flex-col transition-transform duration-200 ease-in-out lg:translate-x-0 select-none shadow-xl lg:shadow-none',
          isMobileMenuOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'
        ]"
        role="navigation"
        aria-label="Sophos UTM 9 Main Navigation"
      >
        <!-- Four Hardcoded Vertical Navigation Groupings -->
        <nav class="flex-1 overflow-y-auto py-3 px-2.5 space-y-4 scrollbar-thin scrollbar-thumb-slate-700">
          <div
            v-for="group in filteredNavGroups"
            :key="group.id"
            class="space-y-1"
          >
            <!-- Cleanly capitalized group header in small, dim text -->
            <div class="px-2.5 pt-2 pb-1 text-[10px] font-bold tracking-wider text-slate-400 uppercase">
              {{ group.header }}
            </div>

            <!-- Standard interactive flex row list links beneath each group header -->
            <ul class="space-y-0.5" role="list">
              <li v-for="item in group.items" :key="item.id">
                <a
                  href="#"
                  @click.prevent="selectNavItem(item.id, group.id)"
                  :class="[
                    'group w-full flex items-center justify-between px-2.5 py-2 rounded-md text-xs font-medium transition-all duration-150 relative',
                    isItemActive(item.id)
                      ? 'bg-[#0072ce] text-white shadow-sm font-semibold'
                      : 'text-slate-300 hover:text-white hover:bg-[#232f42]'
                  ]"
                  :aria-current="isItemActive(item.id) ? 'page' : undefined"
                >
                  <!-- Content Flex Row: Icon + Label -->
                  <div class="flex items-center gap-2.5 min-w-0">
                    <span
                      :class="[
                        'flex-shrink-0 transition-colors',
                        isItemActive(item.id) ? 'text-white' : 'text-slate-400 group-hover:text-cyan-400'
                      ]"
                    >
                      <component :is="item.icon" class="w-4 h-4" />
                    </span>
                    <span class="truncate">{{ item.label }}</span>
                  </div>

                  <!-- Optional Subtitle/Badge (dim text indicator) -->
                  <div class="flex items-center gap-1.5 flex-shrink-0">
                    <span
                      v-if="item.badge"
                      :class="[
                        'text-[10px] px-1.5 py-0.5 rounded font-mono font-medium',
                        isItemActive(item.id)
                          ? 'bg-blue-900/80 text-blue-100'
                          : 'bg-slate-800/90 text-slate-400 group-hover:bg-slate-700 group-hover:text-slate-200'
                      ]"
                    >
                      {{ item.badge }}
                    </span>

                    <span
                      v-if="isItemActive(item.id)"
                      class="w-1.5 h-1.5 rounded-full bg-white animate-pulse"
                    ></span>
                  </div>
                </a>
              </li>
            </ul>
          </div>

          <!-- Empty search state -->
          <div v-if="filteredNavGroups.length === 0" class="px-3 py-6 text-center text-xs text-slate-500">
            <svg class="w-6 h-6 mx-auto mb-2 text-slate-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            No matches found for "<span class="text-slate-400">{{ searchQuery }}</span>"
          </div>
        </nav>

        <!-- Sidebar Footer Status -->
        <div class="p-3 border-t border-slate-700/80 bg-[#141b25] text-xs text-slate-400 flex items-center justify-between">
          <div class="flex items-center gap-2">
            <span class="relative flex h-2 w-2">
              <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              <span class="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
            </span>
            <span class="text-[11px] font-medium text-slate-300">UTM Engine Active</span>
          </div>
          <span class="text-[10px] font-mono text-slate-400">UTM v9.7</span>
        </div>
      </aside>

      <!-- Clean Light Gray Main Content Workspace Area (bg-[#f4f6f9]) -->
      <main class="flex-1 overflow-y-auto bg-[#f4f6f9] text-slate-800 p-4 md:p-6 lg:p-8 flex flex-col space-y-6">
        <!-- Top Context Header & Breadcrumb Panel -->
        <div class="bg-white border border-slate-200 rounded-lg p-4 shadow-sm flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div>
            <!-- Breadcrumbs -->
            <nav class="flex items-center gap-2 text-xs font-mono text-slate-500 uppercase tracking-wider mb-1" aria-label="Breadcrumb">
              <span>UTM 9</span>
              <svg class="w-3 h-3 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
              <span class="text-slate-600 font-semibold">{{ currentGroupHeader }}</span>
              <svg class="w-3 h-3 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
              <span class="text-[#0072ce] font-bold">{{ currentItemTitle }}</span>
            </nav>

            <!-- Page Title with UTM Blue Accent Mark -->
            <div class="flex items-center gap-2.5">
              <span class="w-1.5 h-6 bg-[#0072ce] rounded-sm inline-block"></span>
              <h1 class="text-xl font-black text-slate-900 tracking-tight">
                {{ currentItemTitle }}
              </h1>
              <span v-if="currentItemBadge" class="text-[11px] bg-blue-50 text-[#0072ce] font-medium font-mono px-2 py-0.5 rounded border border-blue-200">
                {{ currentItemBadge }}
              </span>
            </div>
          </div>

          <!-- Dynamic Header Action Slot -->
          <div class="flex items-center gap-2.5 flex-wrap">
            <slot name="header-actions">
              <button
                type="button"
                @click="emitRefresh"
                class="px-3.5 py-1.5 text-xs font-semibold bg-white hover:bg-slate-100 text-slate-700 rounded-md border border-slate-300 transition-colors flex items-center gap-1.5 shadow-sm active:bg-slate-200"
              >
                <svg class="w-3.5 h-3.5 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
                <span>Refresh</span>
              </button>
              <button
                type="button"
                class="px-3.5 py-1.5 text-xs font-semibold bg-[#0072ce] hover:bg-[#005ea6] text-white rounded-md border border-blue-700 transition-colors shadow-sm flex items-center gap-1.5 active:bg-[#004b87]"
              >
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                </svg>
                <span>Apply Configuration</span>
              </button>
            </slot>
          </div>
        </div>

        <!-- Primary View Slot (Passes activeItem and activeGroup to child components) -->
        <div class="flex-1">
          <slot :activeItem="activeItemId" :activeGroup="activeGroupId" :activeSection="activeGroupId">
            <!-- Default Content Placeholder -->
            <div class="bg-white border border-slate-200 rounded-lg p-6 shadow-sm">
              <div class="flex items-center justify-between border-b border-slate-100 pb-4 mb-4">
                <div>
                  <h2 class="text-base font-bold text-slate-900 flex items-center gap-2">
                    <span class="w-1.5 h-4 bg-[#0072ce] rounded-sm"></span>
                    {{ currentItemTitle }} Management
                  </h2>
                  <p class="text-xs text-slate-500 mt-1">Configure parameters and operational status for {{ currentItemTitle }}.</p>
                </div>
                <span class="px-2 py-0.5 rounded bg-emerald-50 text-emerald-700 border border-emerald-200 font-mono text-xs font-semibold flex items-center gap-1">
                  <span class="w-1.5 h-1.5 rounded-full bg-emerald-500"></span> Service Active
                </span>
              </div>

              <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                <div class="p-4 bg-[#f4f6f9] border border-slate-200 rounded-md">
                  <div class="text-xs text-slate-500 font-medium uppercase">Active Group</div>
                  <div class="text-lg font-bold text-slate-900 mt-1">{{ currentGroupHeader }}</div>
                </div>
                <div class="p-4 bg-[#f4f6f9] border border-slate-200 rounded-md">
                  <div class="text-xs text-slate-500 font-medium uppercase">Module Key</div>
                  <div class="text-lg font-mono font-bold text-[#0072ce] mt-1">{{ activeItemId }}</div>
                </div>
                <div class="p-4 bg-[#f4f6f9] border border-slate-200 rounded-md">
                  <div class="text-xs text-slate-500 font-medium uppercase">Protection Level</div>
                  <div class="text-lg font-bold text-emerald-600 mt-1">Enterprise UTM 9</div>
                </div>
              </div>

              <p class="text-sm text-slate-600 leading-relaxed">
                Astaro-Next navigation shell initialized. Use this container to host child modules such as Rules & Policies, Zenarmor Web Protection, Mail Manager, Nginx WAF, Network Interfaces, WireGuard VPN, and System Diagnostics.
              </p>
            </div>
          </slot>
        </div>

        <!-- Astaro-Next Bottom Footer Bar -->
        <footer class="pt-4 border-t border-slate-200 text-xs text-slate-500 flex flex-col sm:flex-row items-center justify-between gap-2">
          <div class="flex items-center gap-2">
            <span class="font-bold text-slate-700">Astaro-Next Security Gateway</span>
            <span>&bull;</span>
            <span>Debian Linux Core Engine</span>
          </div>
          <div class="font-mono text-slate-500 text-[11px] flex items-center gap-2">
            <span>HTTPS Port 4444</span>
            <span>&bull;</span>
            <span>WebAdmin Console Session</span>
          </div>
        </footer>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, h } from 'vue'

// Props definitions
const props = defineProps({
  initialGroup: {
    type: String,
    default: 'monitor_analyze'
  },
  initialSection: {
    type: String,
    default: ''
  },
  initialItem: {
    type: String,
    default: 'control_center'
  },
  currentUser: {
    type: String,
    default: 'admin'
  },
  applianceHost: {
    type: String,
    default: 'astaro-next.internal'
  },
  cpuUsage: {
    type: Number,
    default: 18
  },
  memUsage: {
    type: Number,
    default: 44
  },
  uptime: {
    type: String,
    default: '24d 11h 05m'
  }
})

// Emits for routing/navigation events, authentication, and manual refreshes
const emit = defineEmits(['navigate', 'logout', 'refresh'])

// Mobile drawer visibility toggle
const isMobileMenuOpen = ref(false)

// Global quick search filter query
const searchQuery = ref('')

// SVG Icon Helper Definitions
const ControlCenterIcon = {
  render: () => h('svg', { class: 'w-4 h-4', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
    h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M4 5a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1H5a1 1 0 01-1-1V5zM14 5a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1h-4a1 1 0 01-1-1V5zM4 15a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1H5a1 1 0 01-1-1v-4zM14 15a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1h-4a1 1 0 01-1-1v-4z' })
  ])
}

const RulesPoliciesIcon = {
  render: () => h('svg', { class: 'w-4 h-4', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
    h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z' })
  ])
}

const WebIcon = {
  render: () => h('svg', { class: 'w-4 h-4', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
    h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9' })
  ])
}

const EmailIcon = {
  render: () => h('svg', { class: 'w-4 h-4', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
    h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z' })
  ])
}

const WebServerIcon = {
  render: () => h('svg', { class: 'w-4 h-4', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
    h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M5 12h14M5 12a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v4a2 2 0 01-2 2M5 12a2 2 0 00-2 2v4a2 2 0 002 2h14a2 2 0 002-2v-4a2 2 0 00-2-2m-2-4h.01M17 16h.01' })
  ])
}

const NetworkIcon = {
  render: () => h('svg', { class: 'w-4 h-4', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
    h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M8 9l3 3-3 3m5 0h3M5 20h14a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z' })
  ])
}

const RoutingIcon = {
  render: () => h('svg', { class: 'w-4 h-4', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
    h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M13 7h8m0 0v8m0-8l-8 8-4-4-6 6' })
  ])
}

const VpnIcon = {
  render: () => h('svg', { class: 'w-4 h-4', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
    h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z' })
  ])
}

const CertificatesIcon = {
  render: () => h('svg', { class: 'w-4 h-4', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
    h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z' })
  ])
}

const NatIcon = {
  render: () => h('svg', { class: 'w-4 h-4', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
    h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4' })
  ])
}

const DefinitionsIcon = {
  render: () => h('svg', { class: 'w-4 h-4', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
    h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10' })
  ])
}

const BackupFirmwareIcon = {
  render: () => h('svg', { class: 'w-4 h-4', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
    h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12' })
  ])
}

// Sophos UTM 9 (SFOS) Four Clean Vertical Navigation Groupings
const navGroups = [
  {
    id: 'monitor_analyze',
    header: 'MONITOR & ANALYZE',
    items: [
      {
        id: 'control_center',
        aliases: ['dashboard', 'system_overview', 'resource_graphs', 'executive_report'],
        label: 'Control Center',
        badge: 'Dashboard',
        icon: ControlCenterIcon
      }
    ]
  },
  {
    id: 'protect',
    header: 'PROTECT',
    items: [
      {
        id: 'rules_policies',
        aliases: ['firewall_rules', 'firewall'],
        label: 'Firewall Rules',
        badge: 'NFTables',
        icon: RulesPoliciesIcon
      },
      {
        id: 'nat_rules',
        aliases: ['nat', 'masquerading', 'dnat', 'snat'],
        label: 'NAT & Masquerading',
        badge: 'SNAT/DNAT',
        icon: NatIcon
      },
      {
        id: 'web',
        aliases: ['zenarmor_profiles', 'zenarmor', 'web_protection'],
        label: 'Web',
        badge: 'Zenarmor',
        icon: WebIcon
      },
      {
        id: 'email',
        aliases: ['mail_manager', 'mail', 'mail_quarantine', 'postfix'],
        label: 'Email',
        badge: 'Mail Manager',
        icon: EmailIcon
      },
      {
        id: 'web_server',
        aliases: ['waf_reverse_proxy', 'waf', 'waf_settings', 'nginx_waf'],
        label: 'Web Server',
        badge: 'Nginx WAF',
        icon: WebServerIcon
      }
    ]
  },
  {
    id: 'configure',
    header: 'CONFIGURE',
    items: [
      {
        id: 'definitions',
        aliases: ['objects', 'network_definitions', 'service_definitions'],
        label: 'Definitions & Objects',
        badge: 'Objects',
        icon: DefinitionsIcon
      },
      {
        id: 'network',
        aliases: ['interfaces', 'network_interfaces'],
        label: 'Network',
        badge: 'Interfaces',
        icon: NetworkIcon
      },
      {
        id: 'routing',
        aliases: ['static_routes', 'bgp', 'ospf'],
        label: 'Routing',
        badge: null,
        icon: RoutingIcon
      },
      {
        id: 'vpn',
        aliases: ['wireguard_vpn', 'wireguard', 'ipsec', 'openvpn'],
        label: 'VPN',
        badge: 'WireGuard',
        icon: VpnIcon
      }
    ]
  },
  {
    id: 'system',
    header: 'SYSTEM',
    items: [
      {
        id: 'certificates',
        aliases: ['tls_certs', 'ca_certificates'],
        label: 'Certificates',
        badge: 'Let\'s Encrypt',
        icon: CertificatesIcon
      },
      {
        id: 'backup_firmware',
        aliases: ['firmware', 'backup_restore', 'updates'],
        label: 'Backup & Firmware',
        badge: null,
        icon: BackupFirmwareIcon
      }
    ]
  }
]

// Normalize initial item / group matching with alias support
const resolveInitialSelection = () => {
  const targetItem = props.initialItem || ''
  const targetGroup = props.initialGroup || props.initialSection || ''

  for (const group of navGroups) {
    for (const item of group.items) {
      if (
        item.id === targetItem ||
        (item.aliases && item.aliases.includes(targetItem))
      ) {
        return { groupId: group.id, itemId: item.id }
      }
    }
  }

  // If group matched
  if (targetGroup) {
    const groupMatch = navGroups.find(
      g => g.id === targetGroup || g.header.toLowerCase().includes(targetGroup.toLowerCase())
    )
    if (groupMatch && groupMatch.items.length > 0) {
      return { groupId: groupMatch.id, itemId: groupMatch.items[0].id }
    }
  }

  return { groupId: 'monitor_analyze', itemId: 'control_center' }
}

const initialSelection = resolveInitialSelection()
const activeGroupId = ref(initialSelection.groupId)
const activeItemId = ref(initialSelection.itemId)

// Filtered nav groups for quick-search jumping
const filteredNavGroups = computed(() => {
  if (!searchQuery.value.trim()) return navGroups
  const query = searchQuery.value.toLowerCase().trim()

  return navGroups
    .map(group => {
      const headerMatch = group.header.toLowerCase().includes(query)
      const matchingItems = group.items.filter(item => {
        return (
          item.label.toLowerCase().includes(query) ||
          (item.badge && item.badge.toLowerCase().includes(query)) ||
          (item.aliases && item.aliases.some(a => a.toLowerCase().includes(query)))
        )
      })

      if (headerMatch || matchingItems.length > 0) {
        return {
          ...group,
          items: headerMatch ? group.items : matchingItems
        }
      }
      return null
    })
    .filter(Boolean)
})

// Check if an item is currently active
const isItemActive = (itemId) => {
  if (activeItemId.value === itemId) return true

  for (const group of navGroups) {
    const itm = group.items.find(i => i.id === itemId)
    if (itm && itm.aliases && itm.aliases.includes(activeItemId.value)) {
      return true
    }
  }
  return false
}

// Navigation click handler
const selectNavItem = (itemId, groupId) => {
  activeItemId.value = itemId
  activeGroupId.value = groupId
  isMobileMenuOpen.value = false

  emit('navigate', {
    groupId,
    itemId,
    sectionId: groupId
  })
}

// Computed properties for breadcrumbs and title
const currentGroupHeader = computed(() => {
  const group = navGroups.find(g => g.id === activeGroupId.value)
  return group ? group.header : 'SYSTEM'
})

const currentItemObject = computed(() => {
  for (const group of navGroups) {
    const item = group.items.find(
      i => i.id === activeItemId.value || (i.aliases && i.aliases.includes(activeItemId.value))
    )
    if (item) return item
  }
  return navGroups[0].items[0]
})

const currentItemTitle = computed(() => {
  return currentItemObject.value ? currentItemObject.value.label : 'Control Center'
})

const currentItemBadge = computed(() => {
  return currentItemObject.value ? currentItemObject.value.badge : null
})

const handleLogout = () => {
  emit('logout')
}

const emitRefresh = () => {
  emit('refresh')
}
</script>

<style scoped>
/* High-precision scrollbar styling */
.scrollbar-thin::-webkit-scrollbar {
  width: 5px;
}
.scrollbar-thin::-webkit-scrollbar-track {
  background: #090d16;
}
.scrollbar-thin::-webkit-scrollbar-thumb {
  background: #1e293b;
  border-radius: 2.5px;
}
.scrollbar-thin::-webkit-scrollbar-thumb:hover {
  background: #334155;
}
</style>
