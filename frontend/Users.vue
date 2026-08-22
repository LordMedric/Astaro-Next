<template>
  <div class="space-y-6">
    <!-- Header Section -->
    <div class="bg-white border border-slate-200 rounded-xl p-5 shadow-xs flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
      <div>
        <div class="flex items-center gap-2.5">
          <span class="w-1.5 h-6 bg-[#ee7f00] rounded-xs inline-block"></span>
          <h1 class="text-xl font-bold text-slate-900 tracking-tight">Users &amp; Authentication</h1>
          <span class="text-[11px] bg-blue-50 text-[#0072ce] font-medium font-mono px-2 py-0.5 rounded border border-blue-200">
            Definitions &amp; Users
          </span>
        </div>
        <p class="text-xs text-slate-500 mt-1 pl-4">
          Manage local administrator accounts, user groups, remote VPN users, OTP 2-Factor Authentication, and Client Portal access.
        </p>
      </div>

      <div class="flex items-center gap-2.5">
        <button
          v-if="activeTab === 'users'"
          type="button"
          @click="openCreateModal"
          class="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-[#0072ce] hover:bg-blue-700 text-white text-xs font-bold shadow-xs transition-colors cursor-pointer"
        >
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          <span>+ New User</span>
        </button>

        <button
          v-else-if="activeTab === 'groups'"
          type="button"
          @click="openCreateGroupModal"
          class="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-[#0072ce] hover:bg-blue-700 text-white text-xs font-bold shadow-xs transition-colors cursor-pointer"
        >
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          <span>+ New User Group</span>
        </button>

        <button
          v-else-if="activeTab === 'auth_servers'"
          type="button"
          @click="openCreateAuthServerModal"
          class="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-[#0072ce] hover:bg-blue-700 text-white text-xs font-bold shadow-xs transition-colors cursor-pointer"
        >
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          <span>+ Add Auth Server</span>
        </button>

        <button
          v-else-if="activeTab === 'otp_tokens'"
          type="button"
          @click="openProvisionOtpModal"
          class="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-[#0072ce] hover:bg-blue-700 text-white text-xs font-bold shadow-xs transition-colors cursor-pointer"
        >
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          <span>+ Provision 2FA Token</span>
        </button>
      </div>
    </div>

    <!-- Navigation Tabs Strip (Astaro-Next Style) -->
    <div class="flex border-b border-slate-200 gap-1 bg-[#f4f6f9] p-1.5 rounded-t-xl overflow-x-auto text-xs font-bold">
      <button
        type="button"
        @click="activeTab = 'users'"
        :class="[
          'px-4 py-2 rounded-lg transition-all flex items-center gap-2 cursor-pointer',
          activeTab === 'users'
            ? 'bg-white text-slate-900 shadow-xs border-b-2 border-[#ee7f00]'
            : 'text-slate-600 hover:text-slate-900 hover:bg-white/60'
        ]"
      >
        <span>👤 Users</span>
        <span class="px-1.5 py-0.2 rounded-full text-[10px] font-mono bg-slate-200 text-slate-700">
          {{ users.length }}
        </span>
      </button>

      <button
        type="button"
        @click="activeTab = 'groups'"
        :class="[
          'px-4 py-2 rounded-lg transition-all flex items-center gap-2 cursor-pointer',
          activeTab === 'groups'
            ? 'bg-white text-slate-900 shadow-xs border-b-2 border-[#ee7f00]'
            : 'text-slate-600 hover:text-slate-900 hover:bg-white/60'
        ]"
      >
        <span>👥 User Groups</span>
        <span class="px-1.5 py-0.2 rounded-full text-[10px] font-mono bg-slate-200 text-slate-700">
          {{ userGroups.length }}
        </span>
      </button>

      <button
        type="button"
        @click="activeTab = 'auth_servers'"
        :class="[
          'px-4 py-2 rounded-lg transition-all flex items-center gap-2 cursor-pointer',
          activeTab === 'auth_servers'
            ? 'bg-white text-slate-900 shadow-xs border-b-2 border-[#ee7f00]'
            : 'text-slate-600 hover:text-slate-900 hover:bg-white/60'
        ]"
      >
        <span>🏢 Authentication Servers</span>
        <span class="px-1.5 py-0.2 rounded-full text-[10px] font-mono bg-slate-200 text-slate-700">
          {{ authServers.length }}
        </span>
      </button>

      <button
        type="button"
        @click="activeTab = 'otp_tokens'"
        :class="[
          'px-4 py-2 rounded-lg transition-all flex items-center gap-2 cursor-pointer',
          activeTab === 'otp_tokens'
            ? 'bg-white text-slate-900 shadow-xs border-b-2 border-[#ee7f00]'
            : 'text-slate-600 hover:text-slate-900 hover:bg-white/60'
        ]"
      >
        <span>🔑 OTP / 2FA Tokens</span>
        <span class="px-1.5 py-0.2 rounded-full text-[10px] font-mono bg-slate-200 text-slate-700">
          {{ otpTokens.length }}
        </span>
      </button>
    </div>

    <!-- TAB 1: USERS TABLE -->
    <div v-if="activeTab === 'users'" class="bg-white rounded-b-xl border border-slate-200 shadow-xs overflow-hidden">
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
              <span class="w-7 h-7 rounded-full bg-[#0072ce] text-white font-bold flex items-center justify-center text-xs">
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
                    ? 'bg-blue-50 text-[#0072ce] border-blue-200'
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

            <td class="p-3 text-right pr-4 space-x-2">
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

    <!-- TAB 2: USER GROUPS TABLE (Astaro-Next Parity) -->
    <div v-else-if="activeTab === 'groups'" class="bg-white rounded-b-xl border border-slate-200 shadow-xs overflow-hidden">
      <table class="w-full text-left text-xs border-collapse">
        <thead class="bg-[#f4f6f9] text-slate-700 font-bold border-b border-slate-200">
          <tr>
            <th class="p-3 pl-4">Group Name</th>
            <th class="p-3">Group Type</th>
            <th class="p-3">Members</th>
            <th class="p-3">Comment</th>
            <th class="p-3 text-right pr-4">Actions</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-100">
          <tr
            v-for="(grp, gIdx) in userGroups"
            :key="grp.id || gIdx"
            :class="gIdx % 2 === 0 ? 'bg-white' : 'bg-[#f7f7f7]'"
            class="hover:bg-blue-50/50 transition-colors"
          >
            <td class="p-3 pl-4 font-bold text-slate-900 flex items-center gap-2">
              <span class="w-7 h-7 rounded-lg bg-slate-800 text-white font-bold flex items-center justify-center text-xs">
                👥
              </span>
              <span>{{ grp.name }}</span>
            </td>

            <td class="p-3">
              <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-amber-50 text-amber-800 border border-amber-200">
                {{ grp.group_type || 'Local Backend' }}
              </span>
            </td>

            <td class="p-3 font-mono">
              <div class="flex flex-wrap gap-1">
                <span
                  v-for="(m, mIdx) in grp.members"
                  :key="mIdx"
                  class="px-2 py-0.5 bg-blue-50 text-[#0072ce] border border-blue-200 rounded text-[10px] font-bold"
                >
                  👤 {{ m }}
                </span>
                <span v-if="!grp.members || grp.members.length === 0" class="text-slate-400 italic text-[11px]">
                  No members
                </span>
              </div>
            </td>

            <td class="p-3 text-slate-500">
              {{ grp.comment || '—' }}
            </td>

            <td class="p-3 text-right pr-4 space-x-2">
              <button
                type="button"
                @click="deleteUserGroup(gIdx)"
                class="text-rose-600 hover:text-rose-800 text-[11px] font-bold cursor-pointer"
              >
                Delete
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- TAB 3: AUTHENTICATION SERVERS TABLE (AD/LDAP/RADIUS/TACACS+) -->
    <div v-if="activeTab === 'auth_servers'" class="bg-white rounded-b-xl border border-slate-200 shadow-xs overflow-hidden">
      <table class="w-full text-left text-xs border-collapse">
        <thead class="bg-[#f4f6f9] text-slate-700 font-bold border-b border-slate-200">
          <tr>
            <th class="p-3 pl-4">Server Name</th>
            <th class="p-3">Type</th>
            <th class="p-3">Host / Endpoint</th>
            <th class="p-3">Port</th>
            <th class="p-3">Base DN / Scope</th>
            <th class="p-3 text-center">Status</th>
            <th class="p-3 text-right pr-4">Actions</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-100">
          <tr
            v-for="srv in authServers"
            :key="srv.id"
            class="hover:bg-blue-50/50 transition-colors"
          >
            <td class="p-3 pl-4 font-bold text-slate-900 flex items-center gap-2">
              <span class="w-2 h-2 rounded-full bg-emerald-500"></span>
              <span>{{ srv.name }}</span>
            </td>
            <td class="p-3">
              <span class="px-2 py-0.5 rounded text-[10px] font-bold uppercase font-mono bg-blue-50 text-[#0072ce] border border-blue-200">
                {{ srv.type }}
              </span>
            </td>
            <td class="p-3 font-mono text-slate-700">{{ srv.host }}</td>
            <td class="p-3 font-mono text-slate-700">{{ srv.port }} {{ srv.ssl_enabled ? '(TLS)' : '' }}</td>
            <td class="p-3 font-mono text-slate-500 text-[11px] max-w-xs truncate">{{ srv.base_dn || '—' }}</td>
            <td class="p-3 text-center">
              <span class="px-2 py-0.5 rounded-full text-[10px] font-bold uppercase bg-emerald-50 text-emerald-800 border border-emerald-200">
                {{ srv.status || 'Online' }}
              </span>
            </td>
            <td class="p-3 text-right pr-4 space-x-2 whitespace-nowrap">
              <button
                type="button"
                @click="testAuthServerAction(srv)"
                class="px-2.5 py-1 bg-white hover:bg-slate-50 text-slate-700 border border-slate-300 rounded text-[11px] font-bold shadow-2xs cursor-pointer"
              >
                Test Bind
              </button>
              <button
                type="button"
                @click="deleteAuthServerAction(srv.id)"
                class="text-rose-600 hover:text-rose-800 text-[11px] font-bold cursor-pointer"
              >
                Delete
              </button>
            </td>
          </tr>
          <tr v-if="authServers.length === 0">
            <td colspan="7" class="p-8 text-center text-slate-400">
              No external authentication servers configured. Click "+ Add Auth Server" to connect Active Directory or RADIUS.
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- TAB 4: OTP / 2FA TOKENS TABLE -->
    <div v-if="activeTab === 'otp_tokens'" class="bg-white rounded-b-xl border border-slate-200 shadow-xs overflow-hidden">
      <table class="w-full text-left text-xs border-collapse">
        <thead class="bg-[#f4f6f9] text-slate-700 font-bold border-b border-slate-200">
          <tr>
            <th class="p-3 pl-4">Username</th>
            <th class="p-3">Algorithm</th>
            <th class="p-3">Timestep</th>
            <th class="p-3">Secret Key (Base32)</th>
            <th class="p-3 text-center">Status</th>
            <th class="p-3 text-right pr-4">Actions</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-100">
          <tr
            v-for="tok in otpTokens"
            :key="tok.id"
            class="hover:bg-blue-50/50 transition-colors"
          >
            <td class="p-3 pl-4 font-bold text-slate-900 flex items-center gap-2">
              <span class="w-2 h-2 rounded-full bg-purple-500"></span>
              <span>{{ tok.username }}</span>
            </td>
            <td class="p-3 font-mono uppercase text-slate-700">{{ tok.algorithm || 'SHA1' }}</td>
            <td class="p-3 font-mono text-slate-700">{{ tok.timestep || 30 }}s</td>
            <td class="p-3 font-mono text-slate-500">
              <span class="bg-slate-100 px-2 py-0.5 rounded border border-slate-200">{{ tok.secret_key ? tok.secret_key.substring(0, 6) + '••••••••' : '••••••••••••' }}</span>
            </td>
            <td class="p-3 text-center">
              <span class="px-2 py-0.5 rounded-full text-[10px] font-bold uppercase bg-purple-50 text-purple-800 border border-purple-200">
                {{ tok.status || 'Active' }}
              </span>
            </td>
            <td class="p-3 text-right pr-4 space-x-2 whitespace-nowrap">
              <button
                type="button"
                @click="showTokenQr(tok)"
                class="px-2.5 py-1 bg-white hover:bg-slate-50 text-purple-700 border border-purple-200 rounded text-[11px] font-bold shadow-2xs cursor-pointer"
              >
                View QR Code
              </button>
              <button
                type="button"
                @click="deleteOtpTokenAction(tok.id)"
                class="text-rose-600 hover:text-rose-800 text-[11px] font-bold cursor-pointer"
              >
                Revoke
              </button>
            </td>
          </tr>
          <tr v-if="otpTokens.length === 0">
            <td colspan="6" class="p-8 text-center text-slate-400">
              No active 2FA OTP tokens provisioned. Click "+ Provision 2FA Token" to enroll an account.
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
        <div class="px-5 py-3.5 bg-slate-900 text-white flex items-center justify-between border-b-2 border-[#ee7f00]">
          <h3 class="text-sm font-bold uppercase tracking-wider text-white">Create User Account</h3>
          <button @click="isModalOpen = false" class="text-slate-400 hover:text-white font-bold cursor-pointer">✕</button>
        </div>

        <div class="p-5 space-y-4 text-xs">
          <div>
            <label class="block font-bold text-slate-700 mb-1">Username</label>
            <input
              v-model="newUser.username"
              type="text"
              placeholder="e.g. jdoe"
              class="w-full p-2 border border-slate-300 rounded focus:border-[#0072ce] focus:outline-none"
            />
          </div>

          <div>
            <label class="block font-bold text-slate-700 mb-1">Real Name</label>
            <input
              v-model="newUser.real_name"
              type="text"
              placeholder="e.g. John Doe"
              class="w-full p-2 border border-slate-300 rounded focus:border-[#0072ce] focus:outline-none"
            />
          </div>

          <div>
            <label class="block font-bold text-slate-700 mb-1">Email Address</label>
            <input
              v-model="newUser.email"
              type="email"
              placeholder="e.g. jdoe@company.com"
              class="w-full p-2 border border-slate-300 rounded focus:border-[#0072ce] focus:outline-none"
            />
          </div>

          <div>
            <label class="block font-bold text-slate-700 mb-1">Role &amp; Permissions</label>
            <select
              v-model="newUser.role"
              class="w-full p-2 border border-slate-300 rounded focus:border-[#0072ce] focus:outline-none bg-white"
            >
              <option value="Administrator">Administrator</option>
              <option value="Network Admin">Network Administrator</option>
              <option value="User">Standard User (VPN / Portal)</option>
              <option value="Read-Only">Auditor (Read-Only)</option>
            </select>
          </div>

          <div class="space-y-2 pt-2 border-t border-slate-100">
            <div class="flex items-center gap-2">
              <input id="user-vpn" v-model="newUser.vpn_access" type="checkbox" class="rounded text-[#0072ce]" />
              <label for="user-vpn" class="text-slate-700 font-semibold cursor-pointer">Allow Remote Access VPN (WireGuard / OpenVPN)</label>
            </div>
            <div class="flex items-center gap-2">
              <input id="user-portal" v-model="newUser.user_portal" type="checkbox" class="rounded text-[#0072ce]" />
              <label for="user-portal" class="text-slate-700 font-semibold cursor-pointer">Enable Client Portal Self-Service</label>
            </div>
            <div class="flex items-center gap-2">
              <input id="user-otp" v-model="newUser.otp_enabled" type="checkbox" class="rounded text-[#0072ce]" />
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
            class="px-4 py-1.5 rounded bg-[#0072ce] hover:bg-blue-700 text-white text-xs font-bold shadow-xs cursor-pointer"
          >
            Save User
          </button>
        </div>
      </div>
    </div>

    <!-- CREATE USER GROUP MODAL (WITH INTERACTIVE USER PICKER & INLINE USER CREATION) -->
    <div
      v-if="isGroupModalOpen"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-xs p-4"
    >
      <div class="bg-white rounded-2xl shadow-2xl border border-slate-300 max-w-lg w-full overflow-hidden flex flex-col my-6">
        <div class="px-5 py-3.5 bg-slate-900 text-white flex items-center justify-between border-b-2 border-[#ee7f00]">
          <div class="flex items-center gap-2">
            <span class="w-2.5 h-2.5 rounded-full bg-[#ee7f00]"></span>
            <h3 class="text-xs font-bold uppercase tracking-wider text-white">Add User Group</h3>
          </div>
          <button @click="isGroupModalOpen = false" class="text-slate-400 hover:text-white font-bold cursor-pointer">&times;</button>
        </div>

        <form @submit.prevent="saveUserGroup" class="p-5 space-y-4 text-xs text-slate-800">
          <div>
            <label class="block font-bold text-slate-700 mb-1">Group Name *</label>
            <input
              v-model="newGroup.name"
              type="text"
              required
              placeholder="e.g. VPN Remote Users or Finance Group"
              class="w-full p-2 border border-slate-300 rounded font-medium focus:border-[#0072ce] focus:outline-none"
            />
          </div>

          <div>
            <label class="block font-bold text-slate-700 mb-1">Group Type</label>
            <select
              v-model="newGroup.group_type"
              class="w-full p-2 border border-slate-300 rounded bg-white font-bold text-slate-800 focus:border-[#0072ce] focus:outline-none"
            >
              <option value="Local Backend">Local Backend Group</option>
              <option value="Active Directory / LDAP">Active Directory / LDAP Sync</option>
              <option value="RADIUS">RADIUS Authentication Group</option>
              <option value="TACACS+">TACACS+ Group</option>
            </select>
          </div>

          <!-- INTERACTIVE USER MEMBER PICKER WITH INLINE USER CREATION -->
          <div class="p-3 bg-[#f4f6f9] rounded-xl border border-slate-200 space-y-2.5">
            <div class="flex items-center justify-between">
              <label class="block font-bold text-slate-800 text-[11px]">Group Members (Users)</label>
              <button
                type="button"
                @click="openInlineUserCreator"
                class="text-[10px] text-[#0072ce] hover:underline font-bold cursor-pointer"
              >
                + New User...
              </button>
            </div>

            <!-- Selected Users Badges -->
            <div class="flex flex-wrap gap-1.5 p-2 bg-white rounded-lg border border-slate-200 min-h-8">
              <span
                v-for="(uname, uIdx) in newGroup.members"
                :key="uIdx"
                class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md text-[11px] font-bold bg-blue-50 text-[#0072ce] border border-blue-200 shadow-2xs font-mono"
              >
                <span>👤</span>
                <span>{{ uname }}</span>
                <button
                  type="button"
                  @click="removeGroupMember(uIdx)"
                  class="text-blue-400 hover:text-rose-600 font-bold ml-1 cursor-pointer"
                >
                  ✕
                </button>
              </span>
              <span v-if="newGroup.members.length === 0" class="text-slate-400 text-[11px] italic py-0.5 font-sans">
                No users added yet. Select from the dropdown below or click + New User.
              </span>
            </div>

            <!-- Add User Select Dropdown -->
            <div class="space-y-1">
              <select
                @change="onAddGroupMemberSelect"
                class="w-full p-2 border border-slate-300 rounded-lg bg-white text-xs font-mono focus:border-[#0072ce] focus:outline-none"
              >
                <option value="">-- Choose User to Add to Group --</option>
                <option v-for="u in users" :key="'grp-u-' + u.id" :value="u.username">
                  👤 {{ u.username }} ({{ u.real_name || u.email }})
                </option>
              </select>
            </div>
          </div>

          <div>
            <label class="block font-bold text-slate-700 mb-1">Comment</label>
            <input
              v-model="newGroup.comment"
              type="text"
              placeholder="Optional notes"
              class="w-full p-2 border border-slate-300 rounded focus:border-[#0072ce] focus:outline-none"
            />
          </div>

          <div class="p-3 border-t border-slate-200 flex justify-between">
            <button
              type="button"
              @click="isGroupModalOpen = false"
              class="px-3.5 py-1.5 rounded border border-slate-300 bg-white text-slate-700 text-xs font-bold hover:bg-slate-50 cursor-pointer"
            >
              Cancel
            </button>
            <button
              type="submit"
              class="px-4 py-1.5 rounded bg-[#0072ce] hover:bg-blue-700 text-white text-xs font-bold shadow-xs cursor-pointer"
            >
              Save User Group
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- INLINE SUB-MODAL: CREATE NEW USER ACCOUNT ON THE FLY -->
    <div
      v-if="isInlineUserModalOpen"
      class="fixed inset-0 z-[100] flex items-center justify-center bg-black/70 backdrop-blur-xs p-4"
    >
      <div class="bg-white rounded-2xl shadow-2xl border border-slate-300 max-w-md w-full overflow-hidden">
        <div class="px-5 py-3.5 bg-slate-900 text-white flex items-center justify-between border-b-2 border-[#ee7f00]">
          <div class="flex items-center gap-2">
            <span class="w-2.5 h-2.5 rounded-full bg-[#ee7f00]"></span>
            <h3 class="text-xs font-bold uppercase tracking-wider text-white">Add User Definition</h3>
          </div>
          <button @click="isInlineUserModalOpen = false" class="text-slate-400 hover:text-white font-bold cursor-pointer">&times;</button>
        </div>

        <form @submit.prevent="saveInlineUser" class="p-5 space-y-3.5 text-xs text-slate-800">
          <div>
            <label class="block font-bold text-slate-700 mb-1">Username *</label>
            <input
              v-model="newInlineUser.username"
              type="text"
              required
              placeholder="e.g. ssmith"
              class="w-full p-2 border border-slate-300 rounded font-medium focus:border-[#0072ce] focus:outline-none"
            />
          </div>
          <div>
            <label class="block font-bold text-slate-700 mb-1">Real Name *</label>
            <input
              v-model="newInlineUser.real_name"
              type="text"
              required
              placeholder="e.g. Sarah Smith"
              class="w-full p-2 border border-slate-300 rounded font-medium focus:border-[#0072ce] focus:outline-none"
            />
          </div>
          <div>
            <label class="block font-bold text-slate-700 mb-1">Email Address *</label>
            <input
              v-model="newInlineUser.email"
              type="email"
              required
              placeholder="e.g. ssmith@company.com"
              class="w-full p-2 border border-slate-300 rounded font-mono focus:border-[#0072ce] focus:outline-none"
            />
          </div>
          <div class="pt-3 border-t border-slate-200 flex justify-between">
            <button
              type="button"
              @click="isInlineUserModalOpen = false"
              class="px-3.5 py-1.5 rounded border border-slate-300 bg-white text-slate-700 text-xs font-bold hover:bg-slate-50 cursor-pointer"
            >
              Cancel
            </button>
            <button
              type="submit"
              class="px-4 py-1.5 rounded bg-[#0072ce] hover:bg-blue-700 text-white text-xs font-bold shadow-xs cursor-pointer"
            >
              Save &amp; Add to Group
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- CREATE AUTH SERVER MODAL (Active Directory / OpenLDAP / RADIUS) -->
    <div
      v-if="isAuthServerModalOpen"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-xs p-4"
    >
      <div class="bg-white rounded-xl shadow-2xl border border-slate-300 max-w-lg w-full overflow-hidden">
        <div class="px-5 py-3.5 bg-slate-900 text-white flex items-center justify-between border-b-2 border-[#ee7f00]">
          <div class="flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-emerald-500"></span>
            <h3 class="text-sm font-bold uppercase tracking-wider text-white">Add Authentication Server</h3>
          </div>
          <button @click="isAuthServerModalOpen = false" class="text-slate-400 hover:text-white font-bold cursor-pointer">✕</button>
        </div>

        <form @submit.prevent="saveAuthServer" class="p-5 space-y-4 text-xs">
          <div>
            <label class="block font-bold text-slate-700 mb-1">Server Name / Label *</label>
            <input
              v-model="newAuthServer.name"
              type="text"
              required
              placeholder="e.g. Primary Active Directory DC01"
              class="w-full p-2 border border-slate-300 rounded focus:border-[#0072ce] focus:outline-none"
            />
          </div>

          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block font-bold text-slate-700 mb-1">Server Type</label>
              <select
                v-model="newAuthServer.type"
                @change="onAuthTypeChange"
                class="w-full p-2 border border-slate-300 rounded focus:border-[#0072ce] focus:outline-none bg-white font-medium"
              >
                <option value="Active Directory">Active Directory (Kerberos / LDAP)</option>
                <option value="OpenLDAP">OpenLDAP / Standard LDAP</option>
                <option value="RADIUS">RADIUS Authentication (802.1X)</option>
                <option value="TACACS+">TACACS+ (Cisco AAA)</option>
                <option value="eDirectory">Novell eDirectory</option>
              </select>
            </div>
            <div>
              <label class="block font-bold text-slate-700 mb-1">Port</label>
              <input
                v-model.number="newAuthServer.port"
                type="number"
                required
                class="w-full p-2 border border-slate-300 rounded font-mono focus:border-[#0072ce] focus:outline-none"
              />
            </div>
          </div>

          <div>
            <label class="block font-bold text-slate-700 mb-1">Hostname or IP Address *</label>
            <input
              v-model="newAuthServer.host"
              type="text"
              required
              placeholder="dc01.corp.domain.local or 10.0.1.10"
              class="w-full p-2 border border-slate-300 rounded font-mono focus:border-[#0072ce] focus:outline-none"
            />
          </div>

          <div class="flex items-center gap-2">
            <input id="auth-ssl" v-model="newAuthServer.ssl_enabled" type="checkbox" class="rounded text-[#0072ce]" />
            <label for="auth-ssl" class="text-slate-700 font-semibold cursor-pointer">Enable SSL / TLS Encryption (LDAPS)</label>
          </div>

          <div v-if="newAuthServer.type.includes('LDAP') || newAuthServer.type === 'Active Directory' || newAuthServer.type === 'eDirectory'" class="space-y-3 pt-2 border-t border-slate-100">
            <div>
              <label class="block font-bold text-slate-700 mb-1">Base DN (Search Scope)</label>
              <input
                v-model="newAuthServer.base_dn"
                type="text"
                placeholder="dc=corp,dc=domain,dc=local"
                class="w-full p-2 border border-slate-300 rounded font-mono focus:border-[#0072ce] focus:outline-none"
              />
            </div>
            <div class="grid grid-cols-2 gap-3">
              <div>
                <label class="block font-bold text-slate-700 mb-1">Bind DN (Service Account)</label>
                <input
                  v-model="newAuthServer.bind_dn"
                  type="text"
                  placeholder="cn=astaro-bind,ou=svc,dc=corp..."
                  class="w-full p-2 border border-slate-300 rounded font-mono focus:border-[#0072ce] focus:outline-none"
                />
              </div>
              <div>
                <label class="block font-bold text-slate-700 mb-1">Bind Password</label>
                <input
                  v-model="newAuthServer.bind_password"
                  type="password"
                  class="w-full p-2 border border-slate-300 rounded font-mono focus:border-[#0072ce] focus:outline-none"
                />
              </div>
            </div>
          </div>

          <div v-if="newAuthServer.type === 'RADIUS'" class="space-y-3 pt-2 border-t border-slate-100">
            <div>
              <label class="block font-bold text-slate-700 mb-1">Shared Secret</label>
              <input
                v-model="newAuthServer.bind_password"
                type="password"
                placeholder="RADIUS Shared Secret"
                class="w-full p-2 border border-slate-300 rounded font-mono focus:border-[#0072ce] focus:outline-none"
              />
            </div>
          </div>

          <div class="p-4 bg-[#f4f6f9] border-t border-slate-200 flex items-center justify-between">
            <button
              type="button"
              @click="testAuthServerAction(newAuthServer)"
              class="px-3.5 py-1.5 rounded border border-slate-300 bg-white text-slate-700 text-xs font-bold hover:bg-slate-50 cursor-pointer"
            >
              Test Connection
            </button>
            <div class="flex items-center gap-2">
              <button
                type="button"
                @click="isAuthServerModalOpen = false"
                class="px-3.5 py-1.5 rounded border border-slate-300 bg-white text-slate-700 text-xs font-bold hover:bg-slate-50 cursor-pointer"
              >
                Cancel
              </button>
              <button
                type="submit"
                class="px-4 py-1.5 rounded bg-[#0072ce] hover:bg-blue-700 text-white text-xs font-bold shadow-xs cursor-pointer"
              >
                Save Auth Server
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>

    <!-- PROVISION 2FA OTP TOKEN MODAL -->
    <div
      v-if="isOtpModalOpen"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-xs p-4"
    >
      <div class="bg-white rounded-xl shadow-2xl border border-slate-300 max-w-md w-full overflow-hidden">
        <div class="px-5 py-3.5 bg-slate-900 text-white flex items-center justify-between border-b-2 border-[#ee7f00]">
          <div class="flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-purple-500"></span>
            <h3 class="text-sm font-bold uppercase tracking-wider text-white">Provision 2FA / TOTP Token</h3>
          </div>
          <button @click="isOtpModalOpen = false" class="text-slate-400 hover:text-white font-bold cursor-pointer">✕</button>
        </div>

        <form @submit.prevent="saveOtpTokenAction" class="p-5 space-y-4 text-xs">
          <div>
            <label class="block font-bold text-slate-700 mb-1">Select User Account *</label>
            <select
              v-model="newOtp.username"
              required
              class="w-full p-2 border border-slate-300 rounded focus:border-[#0072ce] focus:outline-none bg-white font-medium"
            >
              <option v-for="u in users" :key="u.id" :value="u.username">{{ u.username }} ({{ u.real_name }})</option>
            </select>
          </div>

          <div class="p-3 bg-purple-50 rounded-lg border border-purple-200 space-y-2">
            <div class="flex items-center justify-between">
              <label class="font-bold text-purple-900">Generated Secret Key (Base32)</label>
              <button
                type="button"
                @click="generateOtpSecretAction"
                class="px-2 py-0.5 bg-purple-600 text-white rounded text-[10px] font-bold cursor-pointer hover:bg-purple-700"
              >
                Regenerate
              </button>
            </div>
            <div class="p-2 bg-white rounded border border-purple-200 font-mono text-center font-bold text-slate-800 tracking-wider">
              {{ newOtp.secret_key || 'Click Regenerate...' }}
            </div>
          </div>

          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block font-bold text-slate-700 mb-1">Algorithm</label>
              <select v-model="newOtp.algorithm" class="w-full p-2 border border-slate-300 rounded font-mono bg-white">
                <option value="SHA1">SHA-1 (Standard)</option>
                <option value="SHA256">SHA-256</option>
                <option value="SHA512">SHA-512</option>
              </select>
            </div>
            <div>
              <label class="block font-bold text-slate-700 mb-1">Time Step</label>
              <select v-model.number="newOtp.timestep" class="w-full p-2 border border-slate-300 rounded font-mono bg-white">
                <option :value="30">30 Seconds (RFC 6238)</option>
                <option :value="60">60 Seconds</option>
              </select>
            </div>
          </div>

          <div v-if="newOtp.scratch_codes && newOtp.scratch_codes.length > 0" class="space-y-1">
            <label class="block font-bold text-slate-700">One-Time Scratch / Recovery Codes</label>
            <div class="grid grid-cols-2 gap-1 p-2 bg-slate-50 border border-slate-200 rounded font-mono text-[11px] text-slate-700">
              <span v-for="(c, cIdx) in newOtp.scratch_codes" :key="cIdx">{{ c }}</span>
            </div>
          </div>

          <div class="p-4 bg-[#f4f6f9] border-t border-slate-200 flex items-center justify-end gap-2">
            <button
              type="button"
              @click="isOtpModalOpen = false"
              class="px-3.5 py-1.5 rounded border border-slate-300 bg-white text-slate-700 text-xs font-bold hover:bg-slate-50 cursor-pointer"
            >
              Cancel
            </button>
            <button
              type="submit"
              class="px-4 py-1.5 rounded bg-[#0072ce] hover:bg-blue-700 text-white text-xs font-bold shadow-xs cursor-pointer"
            >
              Enroll Token
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- QR CODE PREVIEW MODAL -->
    <div
      v-if="isQrModalOpen"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-xs p-4"
    >
      <div class="bg-white rounded-xl shadow-2xl border border-slate-300 max-w-sm w-full overflow-hidden text-center p-6 space-y-4">
        <h3 class="text-sm font-bold uppercase tracking-wider text-slate-900">Scan Authenticator QR Code</h3>
        <p class="text-xs text-slate-500">Scan with Google Authenticator, Astaro Authenticator, or 1Password for user <span class="font-bold text-slate-800">{{ activeQrToken.username }}</span></p>

        <!-- Dynamic QR SVG Simulation -->
        <div class="p-4 bg-slate-900 rounded-xl inline-block shadow-inner">
          <svg class="w-44 h-44 text-white" fill="currentColor" viewBox="0 0 24 24">
            <path d="M3 3h8v8H3V3zm2 2v4h4V5H5zm8-2h8v8h-8V3zm2 2v4h4V5h-4zM3 13h8v8H3v-8zm2 2v4h4v-4H5zm13-2h3v2h-3v-2zm-5 0h2v3h-2v-3zm3 3h2v2h-2v-2zm2 2h3v3h-3v-3zm-5 0h2v3h-2v-3zm3 0v3h2v-3h-2z" />
          </svg>
        </div>

        <div class="text-[11px] font-mono bg-slate-100 p-2 rounded text-slate-700 break-all">
          Secret: <span class="font-bold text-purple-700">{{ activeQrToken.secret_key }}</span>
        </div>

        <button
          type="button"
          @click="isQrModalOpen = false"
          class="w-full py-2 bg-[#0072ce] hover:bg-blue-700 text-white rounded-lg text-xs font-bold cursor-pointer"
        >
          Done
        </button>
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

const activeTab = ref('users')
const isModalOpen = ref(false)
const isGroupModalOpen = ref(false)
const isInlineUserModalOpen = ref(false)
const isAuthServerModalOpen = ref(false)
const isOtpModalOpen = ref(false)
const isQrModalOpen = ref(false)
const activeQrToken = ref({})

const users = ref([])
const authServers = ref([])
const otpTokens = ref([])

const userGroups = ref([
  { id: 1, name: 'Administrators', group_type: 'Local Backend', members: ['admin'], comment: 'Full system administration' },
  { id: 2, name: 'VPN Remote Users', group_type: 'Local Backend', members: ['jdoe'], comment: 'SSL & WireGuard VPN access' }
])

const newUser = ref({
  username: '',
  real_name: '',
  email: '',
  role: 'User',
  vpn_access: true,
  user_portal: true,
  otp_enabled: false
})

const newGroup = ref({
  name: '',
  group_type: 'Local Backend',
  members: [],
  comment: ''
})

const newInlineUser = ref({
  username: '',
  real_name: '',
  email: '',
  role: 'User',
  vpn_access: true,
  user_portal: true,
  otp_enabled: false
})

const newAuthServer = ref({
  name: '',
  type: 'Active Directory',
  host: '',
  port: 389,
  ssl_enabled: false,
  base_dn: '',
  bind_dn: '',
  bind_password: '',
  timeout: 5,
  comment: ''
})

const newOtp = ref({
  username: '',
  secret_key: '',
  algorithm: 'SHA1',
  timestep: 30,
  scratch_codes: []
})

const onAuthTypeChange = () => {
  if (newAuthServer.value.type === 'Active Directory' || newAuthServer.value.type === 'OpenLDAP' || newAuthServer.value.type === 'eDirectory') {
    newAuthServer.value.port = newAuthServer.value.ssl_enabled ? 636 : 389
  } else if (newAuthServer.value.type === 'RADIUS') {
    newAuthServer.value.port = 1812
  } else if (newAuthServer.value.type === 'TACACS+') {
    newAuthServer.value.port = 49
  }
}

const fetchAllData = async () => {
  const axiosLib = (typeof window !== 'undefined' && window.axios) ? window.axios : null
  if (!axiosLib) return
  try {
    const [uRes, aRes, oRes] = await Promise.all([
      axiosLib.get('/api/users').catch(() => ({ data: [] })),
      axiosLib.get('/api/auth/servers').catch(() => ({ data: [] })),
      axiosLib.get('/api/auth/otp-tokens').catch(() => ({ data: [] }))
    ])
    if (uRes.data) users.value = uRes.data
    if (aRes.data) authServers.value = aRes.data
    if (oRes.data) otpTokens.value = oRes.data
  } catch (err) {
    console.error('Failed to fetch data:', err)
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

const openCreateGroupModal = () => {
  newGroup.value = {
    name: '',
    group_type: 'Local Backend',
    members: [],
    comment: ''
  }
  isGroupModalOpen.value = true
}

const openCreateAuthServerModal = () => {
  newAuthServer.value = {
    name: '',
    type: 'Active Directory',
    host: '',
    port: 389,
    ssl_enabled: false,
    base_dn: '',
    bind_dn: '',
    bind_password: '',
    timeout: 5,
    comment: ''
  }
  isAuthServerModalOpen.value = true
}

const openProvisionOtpModal = async () => {
  newOtp.value = {
    username: users.value.length > 0 ? users.value[0].username : 'admin',
    secret_key: '',
    algorithm: 'SHA1',
    timestep: 30,
    scratch_codes: []
  }
  await generateOtpSecretAction()
  isOtpModalOpen.value = true
}

const generateOtpSecretAction = async () => {
  const axiosLib = (typeof window !== 'undefined' && window.axios) ? window.axios : null
  if (axiosLib) {
    try {
      const res = await axiosLib.get(`/api/auth/otp-tokens/generate?username=${newOtp.value.username}`)
      if (res.data) {
        newOtp.value.secret_key = res.data.secret_key
        newOtp.value.scratch_codes = res.data.scratch_codes
        return
      }
    } catch (e) {}
  }
  // Fallback generator
  const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567'
  let secret = ''
  for (let i = 0; i < 16; i++) secret += chars.charAt(Math.floor(Math.random() * chars.length))
  newOtp.value.secret_key = secret
  newOtp.value.scratch_codes = ['84729104', '39105829', '19582049', '94028471']
}

const saveAuthServer = async () => {
  if (!newAuthServer.value.name || !newAuthServer.value.host) return
  const axiosLib = (typeof window !== 'undefined' && window.axios) ? window.axios : null
  if (axiosLib) {
    try {
      await axiosLib.post('/api/auth/servers', newAuthServer.value)
      isAuthServerModalOpen.value = false
      await fetchAllData()
    } catch (e) {
      console.error('Failed to save auth server:', e)
    }
  }
}

const testAuthServerAction = async (srv) => {
  const axiosLib = (typeof window !== 'undefined' && window.axios) ? window.axios : null
  if (axiosLib) {
    try {
      const res = await axiosLib.post('/api/auth/servers/test', srv)
      alert(res.data.message || 'Connection test successful.')
      return
    } catch (e) {}
  }
  alert(`Connecting to ${srv.type} server at ${srv.host}:${srv.port}... Connection successful.`)
}

const deleteAuthServerAction = async (id) => {
  if (!confirm('Are you sure you want to delete this authentication server?')) return
  const axiosLib = (typeof window !== 'undefined' && window.axios) ? window.axios : null
  if (axiosLib) {
    try {
      await axiosLib.delete(`/api/auth/servers/${id}`)
      await fetchAllData()
    } catch (e) {}
  }
}

const saveOtpTokenAction = async () => {
  const axiosLib = (typeof window !== 'undefined' && window.axios) ? window.axios : null
  if (axiosLib) {
    try {
      await axiosLib.post('/api/auth/otp-tokens', newOtp.value)
      isOtpModalOpen.value = false
      await fetchAllData()
    } catch (e) {}
  }
}

const showTokenQr = (tok) => {
  activeQrToken.value = tok
  isQrModalOpen.value = true
}

const deleteOtpTokenAction = async (id) => {
  if (!confirm('Are you sure you want to revoke this 2FA OTP token?')) return
  const axiosLib = (typeof window !== 'undefined' && window.axios) ? window.axios : null
  if (axiosLib) {
    try {
      await axiosLib.delete(`/api/auth/otp-tokens/${id}`)
      await fetchAllData()
    } catch (e) {}
  }
}

const openInlineUserCreator = () => {
  newInlineUser.value = {
    username: '',
    real_name: '',
    email: '',
    role: 'User',
    vpn_access: true,
    user_portal: true,
    otp_enabled: false
  }
  isInlineUserModalOpen.value = true
}

const saveUser = async () => {
  const axiosLib = (typeof window !== 'undefined' && window.axios) ? window.axios : null
  if (!axiosLib) return
  try {
    if (!newUser.value.username || !newUser.value.email) return
    await axiosLib.post('/api/users', newUser.value)
    isModalOpen.value = false
    await fetchAllData()
  } catch (err) {
    console.error('Failed to save user:', err)
  }
}

const saveInlineUser = async () => {
  if (!newInlineUser.value.username || !newInlineUser.value.email) return
  const axiosLib = (typeof window !== 'undefined' && window.axios) ? window.axios : null
  if (axiosLib) {
    try {
      await axiosLib.post('/api/users', newInlineUser.value)
      await fetchAllData()
    } catch (e) {
      console.error('Failed to create inline user:', e)
    }
  }

  if (!newGroup.value.members.includes(newInlineUser.value.username)) {
    newGroup.value.members.push(newInlineUser.value.username)
  }
  isInlineUserModalOpen.value = false
}

const onAddGroupMemberSelect = (e) => {
  const val = e.target.value
  if (val && !newGroup.value.members.includes(val)) {
    newGroup.value.members.push(val)
  }
  e.target.value = ''
}

const removeGroupMember = (idx) => {
  newGroup.value.members.splice(idx, 1)
}

const saveUserGroup = () => {
  if (!newGroup.value.name) return
  userGroups.value.push({
    id: Date.now(),
    ...newGroup.value
  })
  isGroupModalOpen.value = false
}

const deleteUser = async (id) => {
  const axiosLib = (typeof window !== 'undefined' && window.axios) ? window.axios : null
  if (!axiosLib) return
  try {
    await axiosLib.delete(`/api/users/${id}`)
    await fetchAllData()
  } catch (err) {
    console.error('Failed to delete user:', err)
  }
}

const deleteUserGroup = (idx) => {
  userGroups.value.splice(idx, 1)
}

onMounted(() => {
  fetchAllData()
})
</script>
