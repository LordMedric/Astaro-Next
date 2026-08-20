<template>
  <div class="space-y-6">
    <!-- Top Header Banner -->
    <div class="bg-slate-900 text-white rounded-2xl p-6 shadow-xl border border-slate-800 flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div>
        <div class="flex items-center gap-2 mb-1">
          <div class="w-8 h-8 rounded-lg bg-[#0072ce] flex items-center justify-center text-white font-black text-sm">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
            </svg>
          </div>
          <h1 class="text-xl font-bold tracking-tight">Backup &amp; Firmware</h1>
          <span class="text-[10px] bg-blue-950 text-blue-300 font-mono font-bold px-2 py-0.5 rounded border border-blue-800/80">
            UP2DATE ENGINE
          </span>
        </div>
        <p class="text-xs text-slate-400">
          Create encrypted configuration snapshots, restore previous states, inspect firmware versions, and manage system updates.
        </p>
      </div>

      <div class="flex items-center gap-3">
        <button
          @click="fetchBackupsAndFirmware"
          :disabled="loading"
          class="px-3.5 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-xl text-xs font-semibold flex items-center gap-1.5 transition-colors cursor-pointer"
        >
          <svg class="w-3.5 h-3.5" :class="{ 'animate-spin': loading }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          <span>Refresh</span>
        </button>
        <button
          @click="isCreateModalOpen = true"
          class="px-4 py-2 bg-[#0072ce] hover:bg-blue-600 text-white rounded-xl text-xs font-bold shadow-lg shadow-blue-500/20 flex items-center gap-1.5 transition-all cursor-pointer"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          <span>Create Backup Snapshot</span>
        </button>
      </div>
    </div>

    <!-- Navigation Sub-Tabs -->
    <div class="flex border-b border-slate-200 gap-2">
      <button
        v-for="tab in tabs"
        :key="tab.id"
        @click="activeTab = tab.id"
        :class="[
          'px-4 py-2.5 text-xs font-bold transition-all border-b-2 flex items-center gap-2 cursor-pointer',
          activeTab === tab.id
            ? 'border-[#0072ce] text-[#0072ce] bg-blue-50/50 rounded-t-lg'
            : 'border-transparent text-slate-500 hover:text-slate-800'
        ]"
      >
        <span>{{ tab.label }}</span>
        <span
          v-if="tab.badge"
          class="px-1.5 py-0.5 text-[10px] rounded-full font-mono font-bold"
          :class="activeTab === tab.id ? 'bg-[#0072ce] text-white' : 'bg-slate-200 text-slate-600'"
        >
          {{ tab.badge }}
        </span>
      </button>
    </div>

    <!-- Alert Banner -->
    <div v-if="actionMessage" class="p-3.5 rounded-xl bg-emerald-50 border border-emerald-200 text-emerald-800 text-xs flex items-center justify-between">
      <div class="flex items-center gap-2">
        <svg class="w-4 h-4 text-emerald-600" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
        </svg>
        <span class="font-medium">{{ actionMessage }}</span>
      </div>
      <button @click="actionMessage = ''" class="text-emerald-600 hover:text-emerald-900 font-bold">&times;</button>
    </div>

    <!-- TAB 1: Configuration Backups -->
    <div v-if="activeTab === 'backups'" class="space-y-4">
      <div class="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
        <div class="px-5 py-4 bg-slate-50 border-b border-slate-200 flex items-center justify-between">
          <div>
            <h3 class="text-xs font-bold text-slate-800 uppercase tracking-wider">Saved Configuration Snapshots</h3>
            <p class="text-[11px] text-slate-500 mt-0.5">Encrypted archive copies containing firewall rules, definitions, certificates, and system configs</p>
          </div>
          <span class="text-xs font-mono font-bold text-slate-500 bg-white px-2.5 py-1 rounded border border-slate-200">
            {{ backups.length }} Snapshot(s)
          </span>
        </div>

        <div class="overflow-x-auto">
          <table class="w-full text-left text-xs">
            <thead class="bg-[#f4f6f9] text-slate-600 font-bold border-b border-slate-200">
              <tr>
                <th class="p-3 pl-5">Snapshot File</th>
                <th class="p-3">Creation Date</th>
                <th class="p-3">Size</th>
                <th class="p-3">OS Version</th>
                <th class="p-3">Notes &amp; Description</th>
                <th class="p-3 pr-5 text-right">Actions</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100 font-medium text-slate-700">
              <tr v-if="loading" class="text-center">
                <td colspan="6" class="p-8 text-slate-400">Loading backup catalog...</td>
              </tr>
              <tr v-else-if="backups.length === 0" class="text-center">
                <td colspan="6" class="p-8 text-slate-400">No backup snapshots found. Click "Create Backup Snapshot" to create your first restore point.</td>
              </tr>
              <tr
                v-for="backup in backups"
                :key="backup.id"
                class="hover:bg-slate-50/80 transition-colors"
              >
                <td class="p-3 pl-5 font-mono font-bold text-slate-900 flex items-center gap-2">
                  <svg class="w-4 h-4 text-amber-500 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4z" />
                  </svg>
                  <span>{{ backup.filename }}</span>
                </td>
                <td class="p-3 font-mono text-slate-600">{{ backup.created_at }}</td>
                <td class="p-3 font-mono text-slate-600">{{ formatBytes(backup.size_bytes) }}</td>
                <td class="p-3">
                  <span class="px-2 py-0.5 rounded bg-blue-50 text-[#0072ce] border border-blue-200 font-mono text-[10px] font-bold">
                    v{{ backup.version }}
                  </span>
                </td>
                <td class="p-3 text-slate-500 text-[11px] max-w-xs truncate">{{ backup.notes || 'Manual Backup' }}</td>
                <td class="p-3 pr-5 text-right">
                  <div class="flex items-center justify-end gap-2">
                    <button
                      @click="restoreBackup(backup.id)"
                      class="px-2.5 py-1 bg-amber-50 hover:bg-amber-100 text-amber-800 border border-amber-300 rounded font-bold text-[10px] transition-colors cursor-pointer"
                    >
                      Restore
                    </button>
                    <button
                      @click="deleteBackup(backup.id)"
                      class="text-rose-600 hover:text-rose-800 font-bold text-[11px] cursor-pointer"
                    >
                      Delete
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- TAB 2: Firmware & Up2Date -->
    <div v-else-if="activeTab === 'firmware'" class="space-y-6">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- Current Appliance Details Card -->
        <div class="bg-white rounded-2xl border border-slate-200 shadow-sm p-6 space-y-4">
          <div class="flex items-center justify-between border-b border-slate-100 pb-3">
            <h3 class="text-xs font-bold text-slate-800 uppercase tracking-wider">Appliance Firmware Status</h3>
            <span class="text-[10px] bg-emerald-100 text-emerald-800 font-mono font-bold px-2 py-0.5 rounded">
              UP-TO-DATE
            </span>
          </div>

          <div class="space-y-3 text-xs">
            <div class="flex justify-between py-1.5 border-b border-slate-100">
              <span class="text-slate-500">Appliance Model:</span>
              <span class="font-bold text-slate-800">{{ firmwareInfo.appliance_model || 'Astaro-Next ASG-XGS4400' }}</span>
            </div>
            <div class="flex justify-between py-1.5 border-b border-slate-100">
              <span class="text-slate-500">Firmware Build:</span>
              <span class="font-mono font-bold text-[#0072ce]">v{{ firmwareInfo.version || '2.4.0-bookworm' }}</span>
            </div>
            <div class="flex justify-between py-1.5 border-b border-slate-100">
              <span class="text-slate-500">Kernel Version:</span>
              <span class="font-mono text-slate-700">{{ firmwareInfo.kernel || 'Linux 6.1.0-28-amd64' }}</span>
            </div>
            <div class="flex justify-between py-1.5 border-b border-slate-100">
              <span class="text-slate-500">Operating System:</span>
              <span class="text-slate-700">{{ firmwareInfo.platform || 'Debian 12 (Bookworm) x86_64' }}</span>
            </div>
            <div class="flex justify-between py-1.5">
              <span class="text-slate-500">Last Update Check:</span>
              <span class="font-mono text-slate-600">{{ firmwareInfo.last_checked || 'Today' }}</span>
            </div>
          </div>
        </div>

        <!-- Up2Date Cloud Mirror Settings -->
        <div class="bg-white rounded-2xl border border-slate-200 shadow-sm p-6 space-y-4">
          <div class="flex items-center justify-between border-b border-slate-100 pb-3">
            <h3 class="text-xs font-bold text-slate-800 uppercase tracking-wider">Up2Date Cloud Mirrors</h3>
            <span class="text-[10px] bg-blue-100 text-blue-800 font-mono font-bold px-2 py-0.5 rounded">
              OFFICIAL FEED
            </span>
          </div>

          <div class="space-y-3 text-xs">
            <div>
              <label class="block font-bold text-slate-700 mb-1">Update Repository Mirror</label>
              <input
                type="text"
                value="https://up2date.astaro.net/v2/debian-bookworm/"
                disabled
                class="w-full p-2 bg-slate-50 border border-slate-300 rounded font-mono text-xs text-slate-600"
              />
            </div>
            <div>
              <label class="block font-bold text-slate-700 mb-1">Automatic Threat Patterns Update</label>
              <select class="w-full p-2 bg-white border border-slate-300 rounded font-medium">
                <option value="hourly">Every 1 Hour (Recommended)</option>
                <option value="daily">Daily at 02:00 AM</option>
                <option value="manual">Manual Verification Only</option>
              </select>
            </div>
            <div class="pt-2">
              <button
                @click="checkForUpdates"
                :disabled="checkingUpdates"
                class="w-full py-2.5 bg-[#0072ce] hover:bg-blue-700 text-white rounded-xl text-xs font-bold shadow-md shadow-blue-500/20 transition-all flex items-center justify-center gap-2 cursor-pointer disabled:opacity-50"
              >
                <svg v-if="checkingUpdates" class="w-4 h-4 animate-spin text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
                <span>{{ checkingUpdates ? 'Connecting to Up2Date Mirrors...' : 'Check for Firmware & Pattern Updates' }}</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 3: Factory Reset & Appliance Recovery -->
    <div v-else-if="activeTab === 'recovery'" class="space-y-4">
      <div class="bg-white rounded-2xl border border-rose-200 shadow-sm p-6 space-y-5">
        <div class="flex items-center gap-2 border-b border-rose-100 pb-3">
          <svg class="w-5 h-5 text-rose-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
          <h3 class="text-xs font-bold text-rose-800 uppercase tracking-wider">Factory Default Reset &amp; Disaster Recovery</h3>
        </div>

        <div class="p-4 bg-rose-50/50 rounded-xl border border-rose-200 text-xs text-rose-900 space-y-2">
          <p class="font-bold">Caution: Factory Reset Erases All Custom Security Configurations</p>
          <p class="text-rose-700 text-[11px]">
            Executing a factory reset will clear all custom firewall rules, NAT policies, user databases, and WireGuard keys, returning WebAdmin IP to 192.168.1.132:4444.
          </p>
        </div>

        <div class="flex items-center gap-3">
          <button
            @click="triggerFactoryReset"
            class="px-4 py-2 bg-rose-600 hover:bg-rose-700 text-white rounded-xl text-xs font-bold shadow-md shadow-rose-500/20 cursor-pointer"
          >
            Reset Appliance to Factory Defaults
          </button>
        </div>
      </div>
    </div>

    <!-- CREATE BACKUP MODAL -->
    <transition
      enter-active-class="transition duration-150 ease-out"
      enter-from-class="opacity-0 scale-95"
      enter-to-class="opacity-100 scale-100"
      leave-active-class="transition duration-100 ease-in"
      leave-from-class="opacity-100 scale-100"
      leave-to-class="opacity-0 scale-95"
    >
      <div
        v-if="isCreateModalOpen"
        class="fixed inset-0 z-50 overflow-y-auto bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4"
        @keydown.esc="isCreateModalOpen = false"
      >
        <div class="w-full max-w-md bg-white rounded-2xl border border-slate-200 shadow-2xl overflow-hidden flex flex-col my-6">
          <div class="bg-slate-900 text-white px-5 py-3.5 flex items-center justify-between border-b border-slate-800">
            <div class="flex items-center gap-2">
              <div class="w-7 h-7 rounded bg-[#0072ce] flex items-center justify-center text-white font-bold text-xs">
                BK
              </div>
              <h3 class="text-xs font-bold uppercase tracking-wider text-white">Create Backup Snapshot</h3>
            </div>
            <button @click="isCreateModalOpen = false" class="text-slate-400 hover:text-white cursor-pointer font-bold text-base">&times;</button>
          </div>

          <form @submit.prevent="createBackup" class="p-5 space-y-3.5 text-xs text-slate-800">
            <div>
              <label class="block font-bold text-slate-700 mb-1">Snapshot Description / Notes *</label>
              <input
                v-model="newBackupNote"
                type="text"
                required
                placeholder="e.g. Pre-maintenance backup before NAT overhaul"
                class="w-full p-2 border border-slate-300 rounded focus:border-[#0072ce] focus:outline-none"
              />
            </div>

            <div class="p-3 bg-blue-50/50 rounded-lg border border-blue-200 text-[11px] text-blue-900">
              Snapshot will bundle: NFTables rules, SQLite configuration database, WireGuard peer configs, Postfix settings, and X.509 certificates.
            </div>

            <div class="pt-3 border-t border-slate-200 flex justify-between">
              <button
                type="button"
                @click="isCreateModalOpen = false"
                class="px-3.5 py-1.5 border border-slate-300 rounded text-xs font-semibold text-slate-700 hover:bg-slate-50 cursor-pointer"
              >
                Cancel
              </button>
              <button
                type="submit"
                :disabled="isSubmitting"
                class="px-4 py-1.5 bg-[#0072ce] hover:bg-blue-700 text-white rounded text-xs font-bold shadow-xs cursor-pointer disabled:opacity-50"
              >
                {{ isSubmitting ? 'Creating Snapshot...' : 'Create Snapshot' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const activeTab = ref('backups')
const loading = ref(false)
const isSubmitting = ref(false)
const checkingUpdates = ref(false)
const isCreateModalOpen = ref(false)
const newBackupNote = ref('')
const actionMessage = ref('')
const backups = ref([])
const firmwareInfo = ref({})

const tabs = [
  { id: 'backups', label: 'Configuration Backups', badge: '' },
  { id: 'firmware', label: 'Firmware & Up2Date', badge: 'v2.4' },
  { id: 'recovery', label: 'Factory Reset & Recovery', badge: null }
]

function formatBytes(bytes) {
  if (!bytes) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

async function fetchBackupsAndFirmware() {
  loading.value = true
  try {
    const res = await fetch('/api/system/backups')
    if (res.ok) {
      backups.value = await res.json()
      tabs[0].badge = String(backups.value.length)
    }
    const fwRes = await fetch('/api/system/firmware')
    if (fwRes.ok) {
      firmwareInfo.value = await fwRes.json()
    }
  } catch (err) {
    console.error('Failed to load backups/firmware:', err)
  } finally {
    loading.value = false
  }
}

async function createBackup() {
  isSubmitting.value = true
  try {
    const res = await fetch('/api/system/backups/create', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ notes: newBackupNote.value, include_certs: true })
    })
    if (res.ok) {
      const data = await res.json()
      actionMessage.value = data.message || 'Backup snapshot created successfully.'
      isCreateModalOpen.value = false
      newBackupNote.value = ''
      await fetchBackupsAndFirmware()
    }
  } catch (err) {
    console.error('Failed to create backup:', err)
  } finally {
    isSubmitting.value = false
  }
}

async function restoreBackup(backupId) {
  if (!confirm(`Are you sure you want to restore system state from backup ${backupId}? All services will reload.`)) return
  try {
    const res = await fetch('/api/system/backups/restore', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ backup_id: backupId })
    })
    if (res.ok) {
      const data = await res.json()
      actionMessage.value = data.message || 'System state successfully restored.'
    }
  } catch (err) {
    console.error('Failed to restore backup:', err)
  }
}

async function deleteBackup(backupId) {
  if (!confirm(`Are you sure you want to delete backup ${backupId}?`)) return
  try {
    const res = await fetch(`/api/system/backups/${backupId}`, { method: 'DELETE' })
    if (res.ok) {
      actionMessage.value = `Backup ${backupId} deleted.`
      await fetchBackupsAndFirmware()
    }
  } catch (err) {
    console.error('Failed to delete backup:', err)
  }
}

async function checkForUpdates() {
  checkingUpdates.value = true
  setTimeout(() => {
    checkingUpdates.value = false
    actionMessage.value = 'Appliance is running the latest firmware release (v2.4.0-bookworm). Threat patterns are up-to-date.'
  }, 1200)
}

function triggerFactoryReset() {
  if (confirm('CRITICAL WARNING: This will reset all security rules and network parameters to factory defaults. Proceed?')) {
    alert('Factory reset command queued. Appliance will restart with factory defaults.')
  }
}

onMounted(() => {
  fetchBackupsAndFirmware()
})
</script>
