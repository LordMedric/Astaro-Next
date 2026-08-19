<template>
  <div class="space-y-6">
    <!-- Header Section -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-slate-200 pb-4">
      <div>
        <div class="flex items-center gap-2">
          <span class="w-1.5 h-5 bg-[#ee7f00] rounded-full"></span>
          <h1 class="text-xl font-bold text-slate-900">Users & Authentication</h1>
        </div>
        <p class="text-xs text-slate-500 mt-1">
          Manage local administrator accounts, remote VPN users, OTP 2-Factor Authentication, and Client Portal access.
        </p>
      </div>

      <div class="flex items-center gap-2">
        <button
          type="button"
          @click="openCreateModal"
          class="inline-flex items-center gap-2 px-3.5 py-1.5 rounded bg-[#005299] hover:bg-[#003d73] text-white text-xs font-bold shadow-xs transition-colors cursor-pointer"
        >
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          <span>New User</span>
        </button>
      </div>
    </div>

    <!-- Users Table -->
    <div class="bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden">
      <table class="w-full text-left text-xs border-collapse">
        <thead class="bg-[#f4f6f9] text-slate-700 font-bold border-b border-slate-200">
          <tr>
            <th class="p-3 pl-4">Username</th>
            <th class="p-3">Real Name</th>
            <th class="p-3">Email Address</th>
            <th class="p-3">Administrative Role</th>
            <th class="p-3 text-center">VPN Access</th>
            <th class="p-3 text-center">User Portal</th>
            <th class="p-3 text-center">2FA / OTP</th>
            <th class="p-3 text-right pr-4">Actions</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-100">
          <tr
            v-for="(user, idx) in users"
            :key="user.id"
            :class="idx % 2 === 0 ? 'bg-white' : 'bg-[#f7f7f7]'"
            class="hover:bg-blue-50/50 transition-colors"
          >
            <td class="p-3 pl-4 font-bold text-slate-900 flex items-center gap-2">
              <span class="w-7 h-7 rounded-full bg-[#005299] text-white font-bold flex items-center justify-center text-xs">
                {{ user.username.charAt(0).toUpperCase() }}
              </span>
              <span>{{ user.username }}</span>
            </td>

            <td class="p-3 text-slate-800 font-medium">
              {{ user.real_name }}
            </td>

            <td class="p-3 text-slate-500 font-mono">
              {{ user.email }}
            </td>

            <td class="p-3">
              <span
                :class="[
                  'px-2 py-0.5 rounded text-[10px] font-bold uppercase border',
                  user.role.includes('Admin')
                    ? 'bg-blue-50 text-[#005299] border-blue-200'
                    : 'bg-slate-100 text-slate-700 border-slate-200'
                ]"
              >
                {{ user.role }}
              </span>
            </td>

            <td class="p-3 text-center">
              <span v-if="user.vpn_access" class="text-emerald-600 font-bold">✓ Enabled</span>
              <span v-else class="text-slate-400">—</span>
            </td>

            <td class="p-3 text-center">
              <span v-if="user.user_portal" class="text-blue-600 font-bold">✓ Active</span>
              <span v-else class="text-slate-400">—</span>
            </td>

            <td class="p-3 text-center">
              <span v-if="user.otp_enabled" class="px-2 py-0.5 rounded text-[10px] font-bold bg-purple-50 text-purple-700 border border-purple-200">
                TOTP Active
              </span>
              <span v-else class="text-slate-400">Disabled</span>
            </td>

            <td class="p-3 text-right pr-4">
              <button
                v-if="user.username !== 'admin'"
                type="button"
                @click="deleteUser(user.id)"
                class="text-rose-600 hover:text-rose-800 text-[11px] font-bold cursor-pointer"
              >
                Delete
              </button>
              <span v-else class="text-slate-400 text-[11px]">System Account</span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- CREATE USER MODAL -->
    <div
      v-if="isModalOpen"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-xs p-4"
    >
      <div class="bg-white rounded-xl shadow-2xl border border-slate-300 max-w-md w-full overflow-hidden">
        <div class="px-5 py-3.5 bg-[#1b232e] text-white flex items-center justify-between border-b-2 border-[#ee7f00]">
          <h3 class="text-sm font-bold uppercase tracking-wider">Create User Account</h3>
          <button @click="isModalOpen = false" class="text-slate-400 hover:text-white font-bold cursor-pointer">✕</button>
        </div>

        <div class="p-5 space-y-4 text-xs">
          <div>
            <label class="block font-bold text-slate-700 mb-1">Username</label>
            <input
              v-model="newUser.username"
              type="text"
              placeholder="e.g. jdoe"
              class="w-full p-2 border border-slate-300 rounded focus:border-[#005299] focus:outline-none"
            />
          </div>

          <div>
            <label class="block font-bold text-slate-700 mb-1">Real Name</label>
            <input
              v-model="newUser.real_name"
              type="text"
              placeholder="e.g. John Doe"
              class="w-full p-2 border border-slate-300 rounded focus:border-[#005299] focus:outline-none"
            />
          </div>

          <div>
            <label class="block font-bold text-slate-700 mb-1">Email Address</label>
            <input
              v-model="newUser.email"
              type="email"
              placeholder="e.g. jdoe@company.com"
              class="w-full p-2 border border-slate-300 rounded focus:border-[#005299] focus:outline-none"
            />
          </div>

          <div>
            <label class="block font-bold text-slate-700 mb-1">Role & Permissions</label>
            <select
              v-model="newUser.role"
              class="w-full p-2 border border-slate-300 rounded focus:border-[#005299] focus:outline-none bg-white"
            >
              <option value="Administrator">Administrator</option>
              <option value="Network Admin">Network Administrator</option>
              <option value="User">Standard User (VPN / Portal)</option>
              <option value="Read-Only">Auditor (Read-Only)</option>
            </select>
          </div>

          <div class="space-y-2 pt-2 border-t border-slate-100">
            <div class="flex items-center gap-2">
              <input id="user-vpn" v-model="newUser.vpn_access" type="checkbox" class="rounded text-[#005299]" />
              <label for="user-vpn" class="text-slate-700 font-semibold cursor-pointer">Allow Remote Access VPN (WireGuard / OpenVPN)</label>
            </div>
            <div class="flex items-center gap-2">
              <input id="user-portal" v-model="newUser.user_portal" type="checkbox" class="rounded text-[#005299]" />
              <label for="user-portal" class="text-slate-700 font-semibold cursor-pointer">Enable Client Portal Self-Service</label>
            </div>
            <div class="flex items-center gap-2">
              <input id="user-otp" v-model="newUser.otp_enabled" type="checkbox" class="rounded text-[#005299]" />
              <label for="user-otp" class="text-slate-700 font-semibold cursor-pointer">Require 2FA One-Time Password (TOTP)</label>
            </div>
          </div>
        </div>

        <div class="p-4 bg-[#f4f6f9] border-t border-slate-200 flex items-center justify-end gap-2">
          <button
            type="button"
            @click="isModalOpen = false"
            class="px-3.5 py-1.5 rounded border border-slate-300 bg-white text-slate-700 text-xs font-bold hover:bg-slate-50 cursor-pointer"
          >
            Cancel
          </button>
          <button
            type="button"
            @click="saveUser"
            class="px-4 py-1.5 rounded bg-[#005299] hover:bg-[#003d73] text-white text-xs font-bold shadow-xs cursor-pointer"
          >
            Save User
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const props = defineProps({
  authToken: {
    type: String,
    default: ''
  }
})

const isModalOpen = ref(false)
const users = ref([])

const newUser = ref({
  username: '',
  real_name: '',
  email: '',
  role: 'User',
  vpn_access: true,
  user_portal: true,
  otp_enabled: false
})

const fetchUsers = async () => {
  const axiosLib = (typeof window !== 'undefined' && window.axios) ? window.axios : null
  if (!axiosLib) return
  try {
    const res = await axiosLib.get('/api/users')
    if (res.data) users.value = res.data
  } catch (err) {
    console.error('Failed to fetch users:', err)
  }
}

const openCreateModal = () => {
  newUser.value = {
    username: '',
    real_name: '',
    email: '',
    role: 'User',
    vpn_access: true,
    user_portal: true,
    otp_enabled: false
  }
  isModalOpen.value = true
}

const saveUser = async () => {
  const axiosLib = (typeof window !== 'undefined' && window.axios) ? window.axios : null
  if (!axiosLib) return

  try {
    if (!newUser.value.username || !newUser.value.email) return
    await axiosLib.post('/api/users', newUser.value)
    isModalOpen.value = false
    await fetchUsers()
  } catch (err) {
    console.error('Failed to save user:', err)
  }
}

const deleteUser = async (id) => {
  const axiosLib = (typeof window !== 'undefined' && window.axios) ? window.axios : null
  if (!axiosLib) return
  try {
    await axiosLib.delete(`/api/users/${id}`)
    await fetchUsers()
  } catch (err) {
    console.error('Failed to delete user:', err)
  }
}

onMounted(() => {
  fetchUsers()
})
</script>
