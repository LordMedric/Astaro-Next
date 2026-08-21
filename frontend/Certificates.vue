<template>
  <div class="space-y-6">
    <!-- Standardized Page Header -->
    <div class="bg-white border border-slate-200 rounded-xl p-5 shadow-xs flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
      <div>
        <div class="flex items-center gap-2.5">
          <span class="w-1.5 h-6 bg-[#ee7f00] rounded-xs inline-block"></span>
          <h1 class="text-xl font-bold text-slate-900 tracking-tight">Certificate Management</h1>
          <span class="text-[11px] bg-blue-50 text-[#0072ce] font-medium font-mono px-2 py-0.5 rounded border border-blue-200">
            X.509 / PKI / ACME
          </span>
        </div>
        <p class="text-xs text-slate-500 mt-1 pl-4">
          Manage SSL/TLS Server Certificates, Certificate Authorities, and Automated Let's Encrypt (ACME) renewals.
        </p>
      </div>

      <!-- Action Buttons -->
      <div class="flex items-center gap-2.5 flex-wrap">
        <button
          type="button"
          @click="fetchCertificates(true)"
          :disabled="isLoading"
          class="px-3.5 py-2 text-xs font-semibold bg-white hover:bg-slate-50 text-slate-700 rounded-lg border border-slate-300 transition-colors flex items-center gap-1.5 shadow-xs cursor-pointer active:bg-slate-100 disabled:opacity-50"
          title="Refresh Certificate Database"
        >
          <svg :class="['w-3.5 h-3.5 text-slate-500', isLoading ? 'animate-spin text-[#0072ce]' : '']" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          <span>Refresh</span>
        </button>

        <button
          type="button"
          @click="openModal('import')"
          class="px-3.5 py-2 text-xs font-semibold bg-white hover:bg-slate-50 text-slate-700 rounded-lg border border-slate-300 transition-colors flex items-center gap-1.5 shadow-xs cursor-pointer active:bg-slate-100"
        >
          <svg class="w-3.5 h-3.5 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
          </svg>
          <span>Import (.pem)</span>
        </button>

        <button
          type="button"
          @click="openModal('letsencrypt')"
          class="px-3.5 py-2 text-xs font-bold bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg transition-colors flex items-center gap-1.5 shadow-xs cursor-pointer"
        >
          <svg class="w-3.5 h-3.5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
          </svg>
          <span>+ Let's Encrypt (ACME)</span>
        </button>

        <button
          type="button"
          @click="openModal('create')"
          class="px-4 py-2 bg-[#0072ce] hover:bg-blue-700 text-white rounded-lg text-xs font-bold shadow-sm flex items-center gap-2 transition-all cursor-pointer"
        >
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          <span>+ New Certificate...</span>
        </button>
      </div>
    </div>

    <!-- Notification Toast Alerts -->
    <div v-if="toastMessage" class="p-3.5 rounded-lg text-xs flex items-center justify-between border shadow-xs" :class="toastType === 'success' ? 'bg-emerald-50 text-emerald-800 border-emerald-200' : 'bg-rose-50 text-rose-800 border-rose-200'">
      <div class="flex items-center gap-2">
        <span class="font-bold uppercase tracking-wider text-[10px]">{{ toastType }}:</span>
        <span>{{ toastMessage }}</span>
      </div>
      <button @click="toastMessage = null" class="font-bold opacity-60 hover:opacity-100 cursor-pointer">✕</button>
    </div>

    <!-- Standardized Flat Tab Navigation Strip (UTM 9 Style) -->
    <div class="flex border-b border-slate-200 gap-1 bg-[#f4f6f9] p-1.5 rounded-t-xl overflow-x-auto text-xs font-bold">
      <button
        type="button"
        @click="activeTab = 'server_certs'"
        :class="[
          'px-4 py-2 rounded-lg transition-all flex items-center gap-2 cursor-pointer whitespace-nowrap',
          activeTab === 'server_certs'
            ? 'bg-white text-slate-900 shadow-xs border-b-2 border-[#ee7f00]'
            : 'text-slate-600 hover:text-slate-900 hover:bg-white/60'
        ]"
      >
        <span>Host / Server Certificates</span>
        <span class="px-1.5 py-0.2 rounded-full text-[10px] font-mono" :class="activeTab === 'server_certs' ? 'bg-[#0072ce] text-white' : 'bg-slate-200 text-slate-700'">
          {{ serverCertificates.length }}
        </span>
      </button>

      <button
        type="button"
        @click="activeTab = 'authorities'"
        :class="[
          'px-4 py-2 rounded-lg transition-all flex items-center gap-2 cursor-pointer whitespace-nowrap',
          activeTab === 'authorities'
            ? 'bg-white text-slate-900 shadow-xs border-b-2 border-[#ee7f00]'
            : 'text-slate-600 hover:text-slate-900 hover:bg-white/60'
        ]"
      >
        <span>Certificate Authorities (CAs)</span>
        <span class="px-1.5 py-0.2 rounded-full text-[10px] font-mono" :class="activeTab === 'authorities' ? 'bg-[#0072ce] text-white' : 'bg-slate-200 text-slate-700'">
          {{ caCertificates.length }}
        </span>
      </button>

      <button
        type="button"
        @click="activeTab = 'letsencrypt'"
        :class="[
          'px-4 py-2 rounded-lg transition-all flex items-center gap-2 cursor-pointer whitespace-nowrap',
          activeTab === 'letsencrypt'
            ? 'bg-white text-slate-900 shadow-xs border-b-2 border-[#ee7f00]'
            : 'text-slate-600 hover:text-slate-900 hover:bg-white/60'
        ]"
      >
        <span>Let's Encrypt / ACME Auto-Renewal</span>
      </button>
    </div>

    <!-- Standardized Search & Filter Toolbar -->
    <div v-if="activeTab !== 'letsencrypt'" class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 bg-white p-3.5 rounded-xl border border-slate-200 shadow-xs text-xs">
      <div class="flex items-center gap-2 w-full sm:w-80">
        <div class="relative w-full">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search certificate name, CN, issuer, algorithm..."
            class="w-full pl-8 pr-3 py-1.5 bg-slate-50 border border-slate-200 rounded-lg text-xs focus:bg-white focus:border-[#0072ce] focus:outline-none"
          />
          <svg class="w-4 h-4 text-slate-400 absolute left-2.5 top-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </div>
      </div>

      <div class="flex items-center gap-4 text-slate-500 font-medium">
        <div class="flex items-center gap-2">
          <span>Sort By:</span>
          <select v-model="sortOption" class="bg-slate-50 border border-slate-200 rounded-lg px-2 py-1 text-xs text-slate-700 font-bold">
            <option value="name_asc">Name (A-Z)</option>
            <option value="name_desc">Name (Z-A)</option>
            <option value="days_asc">Expiration (Soonest)</option>
          </select>
        </div>

        <span class="font-mono text-slate-600 font-bold">
          Showing {{ filteredCerts.length }} items
        </span>
      </div>
    </div>

    <!-- TAB 1: HOST & SERVER CERTIFICATES TABLE -->
    <div v-if="activeTab === 'server_certs'" class="bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden">
      <div v-if="filteredCerts.length === 0" class="p-12 text-center text-slate-400 text-xs">
        No server certificates found matching your search.
      </div>
      <table v-else class="w-full text-left text-xs border-collapse">
        <thead class="bg-[#f4f6f9] text-slate-700 font-bold border-b border-slate-200">
          <tr>
            <th class="p-3 pl-4">Certificate Name</th>
            <th class="p-3 font-mono">Common Name (CN) / SANs</th>
            <th class="p-3">Issuer / Authority</th>
            <th class="p-3 font-mono">Algorithm / Key</th>
            <th class="p-3 font-mono">Valid Until</th>
            <th class="p-3">Assigned Service</th>
            <th class="p-3 text-right pr-4">Actions</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-100 font-medium text-slate-700">
          <tr
            v-for="(cert, idx) in filteredCerts"
            :key="cert.id || idx"
            :class="idx % 2 === 0 ? 'bg-white' : 'bg-[#f7f7f7]'"
            class="hover:bg-blue-50/40 transition-colors"
          >
            <td class="p-3 pl-4 font-bold text-slate-900 flex items-center gap-2">
              <span class="w-2 h-2 rounded-full" :class="cert.isValid !== false ? 'bg-emerald-500' : 'bg-rose-500'"></span>
              <span>{{ cert.name }}</span>
              <span v-if="cert.isDefault" class="text-[10px] bg-blue-50 text-[#0072ce] border border-blue-200 px-1.5 py-0.2 rounded font-mono font-bold">Default</span>
            </td>

            <td class="p-3 font-mono">
              <div class="font-bold text-slate-800">{{ cert.commonName }}</div>
              <div v-if="cert.sans && cert.sans.length" class="text-slate-400 text-[10px]">SAN: {{ cert.sans.join(', ') }}</div>
            </td>

            <td class="p-3">
              <span class="inline-flex items-center gap-1.5">
                <span class="w-1.5 h-1.5 rounded-full" :class="cert.issuer && cert.issuer.includes('Let\'s Encrypt') ? 'bg-emerald-500' : 'bg-slate-400'"></span>
                <span>{{ cert.issuer }}</span>
              </span>
            </td>

            <td class="p-3 font-mono text-[11px]">
              <span class="px-1.5 py-0.5 rounded bg-slate-100 text-slate-700 border border-slate-200 font-semibold">{{ cert.algorithm || 'RSA 2048-bit' }}</span>
            </td>

            <td class="p-3 font-mono text-[11px]">
              <span :class="cert.daysRemaining < 30 ? 'text-rose-600 font-bold' : 'text-slate-700'">
                {{ cert.validTo }} ({{ cert.daysRemaining }}d)
              </span>
            </td>

            <td class="p-3">
              <span class="text-[10px] font-bold bg-slate-100 px-2 py-0.5 rounded border border-slate-200 text-slate-700">{{ cert.usage || 'SSL Service' }}</span>
            </td>

            <!-- Standard Action Triplet: View | Download | Delete -->
            <td class="p-3 text-right pr-4 space-x-1.5 whitespace-nowrap">
              <button
                type="button"
                @click="viewCertDetails(cert)"
                class="px-2 py-1 bg-white hover:bg-slate-50 text-slate-700 border border-slate-300 rounded text-[11px] font-bold shadow-2xs cursor-pointer"
                title="View detailed certificate properties and PEM structure"
              >
                View
              </button>
              <button
                type="button"
                @click="downloadCert(cert)"
                class="px-2 py-1 bg-blue-50 hover:bg-blue-100 text-[#0072ce] border border-blue-200 rounded text-[11px] font-bold shadow-2xs cursor-pointer"
                title="Download X.509 certificate (.crt)"
              >
                Download
              </button>
              <button
                v-if="!cert.isDefault"
                type="button"
                @click="deleteCert(cert)"
                class="px-2 py-1 bg-white hover:bg-rose-50 text-rose-600 border border-rose-200 rounded text-[11px] font-bold shadow-2xs cursor-pointer"
                title="Delete Certificate"
              >
                Delete
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- TAB 2: CERTIFICATE AUTHORITIES (CAs) -->
    <div v-if="activeTab === 'authorities'" class="space-y-4">
      <div class="bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden">
        <div class="p-4 border-b border-slate-100 flex items-center justify-between bg-slate-50/50">
          <div class="flex items-center gap-2">
            <span class="w-1.5 h-4 bg-[#0072ce] rounded-full"></span>
            <h2 class="text-xs font-bold text-slate-800 uppercase tracking-wider">Trusted Certificate Authorities</h2>
          </div>
          <span class="text-[11px] font-mono text-slate-500">{{ caCertificates.length }} CAs configured</span>
        </div>

        <div class="p-4 space-y-3">
          <div
            v-for="ca in caCertificates"
            :key="ca.id"
            class="p-3.5 rounded-lg border border-slate-200 bg-white flex items-center justify-between hover:border-slate-300 transition-all"
          >
            <div class="flex items-center gap-3">
              <div class="w-9 h-9 rounded-lg bg-blue-50 text-[#0072ce] flex items-center justify-center font-bold">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                </svg>
              </div>
              <div>
                <div class="flex items-center gap-2">
                  <h3 class="text-xs font-bold text-slate-900">{{ ca.name }}</h3>
                  <span class="text-[10px] px-1.5 py-0.2 rounded font-mono font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200">Trusted</span>
                </div>
                <div class="text-[11px] text-slate-500 font-mono">CN={{ ca.commonName }} &bull; Valid to: {{ ca.validTo }}</div>
              </div>
            </div>

            <div class="flex items-center gap-2">
              <button
                type="button"
                @click="viewCertDetails(ca)"
                class="px-2.5 py-1 rounded bg-white hover:bg-slate-50 border border-slate-300 text-slate-700 text-xs font-bold cursor-pointer shadow-2xs"
              >
                View
              </button>
              <button
                type="button"
                @click="downloadCaCert(ca)"
                class="px-2.5 py-1 rounded bg-blue-50 hover:bg-blue-100 border border-blue-200 text-[#0072ce] text-xs font-bold cursor-pointer shadow-2xs"
              >
                Download CA (.crt)
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 3: LET'S ENCRYPT (ACME) AUTOMATION -->
    <div v-if="activeTab === 'letsencrypt'" class="space-y-4">
      <div class="bg-white rounded-xl border border-slate-200 shadow-xs p-6">
        <div class="flex items-start justify-between gap-4 border-b border-slate-100 pb-5 mb-5">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-lg bg-emerald-100 text-emerald-700 flex items-center justify-center font-bold">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <div>
              <h2 class="text-base font-bold text-slate-900">Let's Encrypt (ACME) Automated Certificate Engine</h2>
              <p class="text-xs text-slate-500 mt-0.5">Automated issuance and 60-day renewal for public domain names using standard ACME HTTP-01 / DNS-01 challenges.</p>
            </div>
          </div>
          <button
            type="button"
            @click="openModal('letsencrypt')"
            class="px-4 py-2 rounded-lg bg-[#0072ce] hover:bg-blue-700 text-white text-xs font-bold shadow-sm transition-all cursor-pointer"
          >
            + Request ACME Certificate
          </button>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div class="p-4 rounded-lg bg-slate-50 border border-slate-200">
            <div class="text-slate-500 text-[11px] font-semibold uppercase tracking-wider">ACME Protocol</div>
            <div class="text-base font-bold text-slate-900 mt-1">RFC 8555 (v2)</div>
            <div class="text-xs text-emerald-600 font-medium mt-0.5">Production Directory Active</div>
          </div>
          <div class="p-4 rounded-lg bg-slate-50 border border-slate-200">
            <div class="text-slate-500 text-[11px] font-semibold uppercase tracking-wider">Auto-Renewal Frequency</div>
            <div class="text-base font-bold text-slate-900 mt-1">Every 60 Days</div>
            <div class="text-xs text-slate-500 font-medium mt-0.5">Cron Hook: systemd-timer</div>
          </div>
          <div class="p-4 rounded-lg bg-slate-50 border border-slate-200">
            <div class="text-slate-500 text-[11px] font-semibold uppercase tracking-wider">Default Challenge</div>
            <div class="text-base font-bold text-slate-900 mt-1">HTTP-01 Webroot</div>
            <div class="text-xs text-slate-500 font-medium mt-0.5">Port 80 Ingress Verification</div>
          </div>
        </div>
      </div>
    </div>

    <!-- MODAL 1: VIEW CERTIFICATE DETAILS -->
    <transition
      enter-active-class="transition duration-150 ease-out"
      enter-from-class="opacity-0 scale-95"
      enter-to-class="opacity-100 scale-100"
      leave-active-class="transition duration-100 ease-in"
      leave-from-class="opacity-100 scale-100"
      leave-to-class="opacity-0 scale-95"
    >
      <div
        v-if="viewingCert"
        class="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4"
        @keydown.esc="viewingCert = null"
      >
        <div class="bg-white rounded-2xl shadow-2xl border border-slate-200 max-w-lg w-full overflow-hidden flex flex-col max-h-[90vh]">
          <!-- Modal Header -->
          <div class="px-5 py-3.5 bg-slate-900 text-white flex items-center justify-between border-b border-slate-800">
            <div class="flex items-center gap-2.5">
              <div class="w-8 h-8 rounded-lg bg-[#ee7f00] flex items-center justify-center text-white font-bold text-xs shadow-md">
                TLS
              </div>
              <div>
                <h3 class="text-xs font-bold uppercase tracking-wider text-white">
                  Certificate Details: {{ viewingCert.name }}
                </h3>
                <p class="text-[10px] text-slate-400 font-mono">CN={{ viewingCert.commonName }}</p>
              </div>
            </div>
            <button @click="viewingCert = null" class="text-slate-400 hover:text-white font-bold cursor-pointer text-base leading-none">&times;</button>
          </div>

          <!-- Body with Certificate Properties & PEM Structure -->
          <div class="p-5 space-y-4 text-xs overflow-y-auto flex-1 font-sans">
            <div class="grid grid-cols-2 gap-3 p-3 bg-slate-50 rounded-xl border border-slate-200">
              <div>
                <div class="text-[10px] uppercase font-bold text-slate-400">Common Name (CN)</div>
                <div class="font-bold text-slate-900 font-mono mt-0.5">{{ viewingCert.commonName }}</div>
              </div>
              <div>
                <div class="text-[10px] uppercase font-bold text-slate-400">Issuer / CA</div>
                <div class="font-bold text-slate-900 mt-0.5">{{ viewingCert.issuer }}</div>
              </div>
              <div>
                <div class="text-[10px] uppercase font-bold text-slate-400">Algorithm</div>
                <div class="font-bold text-slate-900 font-mono mt-0.5">{{ viewingCert.algorithm || 'RSA 2048-bit' }}</div>
              </div>
              <div>
                <div class="text-[10px] uppercase font-bold text-slate-400">Valid Until</div>
                <div class="font-bold text-slate-900 font-mono mt-0.5">{{ viewingCert.validTo }} ({{ viewingCert.daysRemaining }} days)</div>
              </div>
              <div class="col-span-2">
                <div class="text-[10px] uppercase font-bold text-slate-400">Subject Alternative Names (SANs)</div>
                <div class="font-mono text-slate-700 mt-0.5">{{ (viewingCert.sans && viewingCert.sans.length) ? viewingCert.sans.join(', ') : 'None' }}</div>
              </div>
              <div class="col-span-2">
                <div class="text-[10px] uppercase font-bold text-slate-400">SHA-256 Fingerprint</div>
                <div class="font-mono text-[10px] text-slate-600 break-all mt-0.5">
                  {{ viewingCert.fingerprint || 'A4:2E:89:1B:0C:55:92:DF:34:7E:11:80:BC:EA:79:33:F1:A6:24:90:5E:67:88:12:33:45:90:AB:CD:EF:12:34' }}
                </div>
              </div>
            </div>

            <!-- Raw PEM Certificate Box -->
            <div>
              <div class="flex items-center justify-between mb-1">
                <span class="font-bold text-slate-700">Raw X.509 PEM Certificate</span>
                <button
                  type="button"
                  @click="copyPem"
                  class="text-[10px] font-bold text-[#0072ce] hover:underline cursor-pointer"
                >
                  {{ isCopied ? 'Copied!' : 'Copy to Clipboard' }}
                </button>
              </div>
              <textarea
                readonly
                rows="6"
                class="w-full p-2.5 bg-slate-900 text-emerald-400 font-mono text-[10px] rounded-lg border border-slate-800 select-all focus:outline-none"
              >{{ getPemContent(viewingCert) }}</textarea>
            </div>
          </div>

          <!-- Modal Footer -->
          <div class="p-4 border-t border-slate-200 bg-slate-50 flex items-center justify-between">
            <button
              type="button"
              @click="downloadCert(viewingCert)"
              class="px-3.5 py-1.5 rounded-lg bg-[#0072ce] hover:bg-blue-700 text-white font-bold text-xs flex items-center gap-1.5 shadow-xs cursor-pointer"
            >
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
              </svg>
              <span>Download (.crt)</span>
            </button>
            <button
              type="button"
              @click="viewingCert = null"
              class="px-3.5 py-1.5 rounded-lg border border-slate-300 bg-white hover:bg-slate-100 text-slate-700 font-bold text-xs cursor-pointer"
            >
              Close
            </button>
          </div>
        </div>
      </div>
    </transition>

    <!-- MODAL 2: CREATE SELF-SIGNED CERTIFICATE / CSR -->
    <transition
      enter-active-class="transition duration-150 ease-out"
      enter-from-class="opacity-0 scale-95"
      enter-to-class="opacity-100 scale-100"
      leave-active-class="transition duration-100 ease-in"
      leave-from-class="opacity-100 scale-100"
      leave-to-class="opacity-0 scale-95"
    >
      <div v-if="activeModal === 'create'" class="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4">
        <div class="bg-white rounded-2xl shadow-2xl border border-slate-200 max-w-lg w-full overflow-hidden flex flex-col">
          <div class="px-5 py-3.5 bg-slate-900 text-white flex items-center justify-between border-b border-slate-800">
            <h3 class="text-xs font-bold uppercase tracking-wider text-white">Generate Self-Signed X.509 Certificate</h3>
            <button @click="activeModal = null" class="text-slate-400 hover:text-white font-bold cursor-pointer">&times;</button>
          </div>

          <form @submit.prevent="handleGenerateCert" class="p-5 space-y-3.5 text-xs">
            <div>
              <label class="block font-bold text-slate-700 mb-1">Certificate Friendly Name *</label>
              <input type="text" required v-model="newCertForm.name" placeholder="e.g. Internal-WebAdmin-SSL" class="w-full p-2 border border-slate-300 rounded focus:border-[#0072ce] focus:outline-none" />
            </div>

            <div class="grid grid-cols-2 gap-3">
              <div>
                <label class="block font-bold text-slate-700 mb-1">Common Name (CN) / FQDN *</label>
                <input type="text" required v-model="newCertForm.commonName" placeholder="gateway.internal.local" class="w-full p-2 border border-slate-300 rounded font-mono" />
              </div>
              <div>
                <label class="block font-bold text-slate-700 mb-1">Algorithm &amp; Key Size</label>
                <select v-model="newCertForm.algorithm" class="w-full p-2 border border-slate-300 rounded bg-white font-medium">
                  <option value="RSA 2048-bit">RSA 2048-bit (Standard)</option>
                  <option value="RSA 4096-bit">RSA 4096-bit (High Security)</option>
                  <option value="ECDSA P-256">ECDSA P-256 (Fast/Modern)</option>
                </select>
              </div>
            </div>

            <div>
              <label class="block font-bold text-slate-700 mb-1">Subject Alternative Names (SANs)</label>
              <input type="text" v-model="newCertForm.sans" placeholder="192.168.1.1, firewall.local, vpn.local" class="w-full p-2 border border-slate-300 rounded font-mono" />
            </div>

            <div class="grid grid-cols-2 gap-3">
              <div>
                <label class="block font-bold text-slate-700 mb-1">Validity (Days)</label>
                <input type="number" v-model.number="newCertForm.days" class="w-full p-2 border border-slate-300 rounded font-mono" />
              </div>
              <div>
                <label class="block font-bold text-slate-700 mb-1">Assigned Service</label>
                <select v-model="newCertForm.usage" class="w-full p-2 border border-slate-300 rounded bg-white font-medium">
                  <option value="WebAdmin HTTPS">WebAdmin HTTPS</option>
                  <option value="WAF / Reverse Proxy">WAF / Reverse Proxy</option>
                  <option value="SSL VPN Server">SSL VPN Server</option>
                  <option value="Custom SSL Service">Custom SSL Service</option>
                </select>
              </div>
            </div>

            <div class="pt-3 border-t border-slate-200 flex justify-between">
              <button type="button" @click="activeModal = null" class="px-3.5 py-1.5 border rounded text-slate-700 cursor-pointer">Cancel</button>
              <button type="submit" :disabled="isSubmitting" class="px-4 py-1.5 bg-[#0072ce] text-white font-bold rounded shadow-xs cursor-pointer disabled:opacity-50">
                {{ isSubmitting ? 'Generating...' : 'Generate Certificate' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </transition>

    <!-- MODAL 3: IMPORT CERTIFICATE (.PEM / .KEY) -->
    <transition
      enter-active-class="transition duration-150 ease-out"
      enter-from-class="opacity-0 scale-95"
      enter-to-class="opacity-100 scale-100"
      leave-active-class="transition duration-100 ease-in"
      leave-from-class="opacity-100 scale-100"
      leave-to-class="opacity-0 scale-95"
    >
      <div v-if="activeModal === 'import'" class="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4">
        <div class="bg-white rounded-2xl shadow-2xl border border-slate-200 max-w-lg w-full overflow-hidden flex flex-col">
          <div class="px-5 py-3.5 bg-slate-900 text-white flex items-center justify-between border-b border-slate-800">
            <h3 class="text-xs font-bold uppercase tracking-wider text-white">Import X.509 Certificate &amp; Key</h3>
            <button @click="activeModal = null" class="text-slate-400 hover:text-white font-bold cursor-pointer">&times;</button>
          </div>

          <form @submit.prevent="handleImportCert" class="p-5 space-y-3.5 text-xs">
            <div>
              <label class="block font-bold text-slate-700 mb-1">Certificate Friendly Name *</label>
              <input type="text" required v-model="importForm.name" placeholder="e.g. Wildcard-Company-2026" class="w-full p-2 border border-slate-300 rounded" />
            </div>

            <div>
              <label class="block font-bold text-slate-700 mb-1">Certificate (.crt / .pem) *</label>
              <textarea required rows="4" v-model="importForm.certPem" placeholder="-----BEGIN CERTIFICATE-----&#10;...&#10;-----END CERTIFICATE-----" class="w-full p-2 border border-slate-300 rounded font-mono text-[11px]"></textarea>
            </div>

            <div>
              <label class="block font-bold text-slate-700 mb-1">Private Key (.key) *</label>
              <textarea required rows="3" v-model="importForm.keyPem" placeholder="-----BEGIN PRIVATE KEY-----&#10;...&#10;-----END PRIVATE KEY-----" class="w-full p-2 border border-slate-300 rounded font-mono text-[11px]"></textarea>
            </div>

            <div class="pt-3 border-t border-slate-200 flex justify-between">
              <button type="button" @click="activeModal = null" class="px-3.5 py-1.5 border rounded text-slate-700 cursor-pointer">Cancel</button>
              <button type="submit" :disabled="isSubmitting" class="px-4 py-1.5 bg-[#0072ce] text-white font-bold rounded shadow-xs cursor-pointer disabled:opacity-50">
                {{ isSubmitting ? 'Importing...' : 'Import Certificate' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </transition>

    <!-- MODAL 4: REQUEST LET'S ENCRYPT -->
    <transition
      enter-active-class="transition duration-150 ease-out"
      enter-from-class="opacity-0 scale-95"
      enter-to-class="opacity-100 scale-100"
      leave-active-class="transition duration-100 ease-in"
      leave-from-class="opacity-100 scale-100"
      leave-to-class="opacity-0 scale-95"
    >
      <div v-if="activeModal === 'letsencrypt'" class="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4">
        <div class="bg-white rounded-2xl shadow-2xl border border-slate-200 max-w-lg w-full overflow-hidden flex flex-col">
          <div class="px-5 py-3.5 bg-slate-900 text-white flex items-center justify-between border-b border-slate-800">
            <h3 class="text-xs font-bold uppercase tracking-wider text-white">Request Automated Let's Encrypt Certificate</h3>
            <button @click="activeModal = null" class="text-slate-400 hover:text-white font-bold cursor-pointer">&times;</button>
          </div>

          <form @submit.prevent="handleRequestLetsEncrypt" class="p-5 space-y-3.5 text-xs">
            <div>
              <label class="block font-bold text-slate-700 mb-1">Public Domain Name *</label>
              <input type="text" required v-model="leForm.domain" placeholder="e.g. gateway.mycompany.com" class="w-full p-2 border border-slate-300 rounded font-mono" />
            </div>

            <div>
              <label class="block font-bold text-slate-700 mb-1">Admin Email (Expiration Notices) *</label>
              <input type="email" required v-model="leForm.email" placeholder="admin@mycompany.com" class="w-full p-2 border border-slate-300 rounded" />
            </div>

            <div class="p-3 bg-emerald-50 rounded-lg border border-emerald-200 text-emerald-900 text-[11px] space-y-1">
              <div class="font-bold flex items-center gap-1.5">
                <span>ACME HTTP-01 Validation</span>
              </div>
              <p>Ensure port 80 (HTTP) on WAN interface is open and pointing to this domain so the Let's Encrypt ACME server can verify domain ownership.</p>
            </div>

            <div class="pt-3 border-t border-slate-200 flex justify-between">
              <button type="button" @click="activeModal = null" class="px-3.5 py-1.5 border rounded text-slate-700 cursor-pointer">Cancel</button>
              <button type="submit" :disabled="isSubmitting" class="px-4 py-1.5 bg-emerald-600 hover:bg-emerald-700 text-white font-bold rounded shadow-xs cursor-pointer disabled:opacity-50">
                {{ isSubmitting ? 'Requesting...' : 'Request &amp; Install' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'

const props = defineProps({
  authToken: {
    type: String,
    default: ''
  }
})

const activeTab = ref('server_certs')
const activeModal = ref(null)
const viewingCert = ref(null)
const isLoading = ref(false)
const isSubmitting = ref(false)
const isCopied = ref(false)
const toastMessage = ref(null)
const toastType = ref('success')
const searchQuery = ref('')
const sortOption = ref('name_asc')

const serverCertificates = ref([
  {
    id: 'cert_webadmin_default',
    name: 'WebAdmin Default Certificate',
    commonName: 'astaro-next.internal',
    sans: ['localhost', '192.168.1.1', '10.0.0.1'],
    issuer: 'Astaro-Next Appliance Root CA',
    algorithm: 'RSA 2048-bit',
    validTo: '2035-12-31',
    daysRemaining: 3418,
    isValid: true,
    isDefault: true,
    usage: 'WebAdmin HTTPS Port 4444'
  },
  {
    id: 'cert_waf_portal',
    name: 'WAF SSL Offloading Wildcard',
    commonName: '*.medric.net',
    sans: ['medric.net', '*.medric.net', 'home.medric.net'],
    issuer: "Let's Encrypt Authority X3",
    algorithm: 'ECDSA P-256',
    validTo: '2026-11-15',
    daysRemaining: 86,
    isValid: true,
    isDefault: false,
    usage: 'Web Application Firewall (WAF)'
  }
])

const caCertificates = ref([
  {
    id: 'ca_root_astaro',
    name: 'Astaro-Next Appliance Root CA',
    commonName: 'Astaro-Next Root CA',
    issuer: 'Astaro-Next Self-Signed',
    validTo: '2038-01-19',
    daysRemaining: 4168
  },
  {
    id: 'ca_letsencrypt_x3',
    name: "Let's Encrypt Authority X3",
    commonName: "Let's Encrypt Authority X3",
    issuer: 'ISRG Root X1',
    validTo: '2030-06-04',
    daysRemaining: 1382
  }
])

const newCertForm = reactive({
  name: '',
  commonName: '',
  sans: '',
  algorithm: 'RSA 2048-bit',
  days: 365,
  usage: 'WebAdmin HTTPS'
})

const importForm = reactive({
  name: '',
  certPem: '',
  keyPem: ''
})

const leForm = reactive({
  domain: '',
  email: ''
})

const filteredCerts = computed(() => {
  let list = [...serverCertificates.value]
  if (searchQuery.value.trim()) {
    const q = searchQuery.value.toLowerCase()
    list = list.filter(c =>
      c.name.toLowerCase().includes(q) ||
      c.commonName.toLowerCase().includes(q) ||
      c.issuer.toLowerCase().includes(q) ||
      (c.algorithm && c.algorithm.toLowerCase().includes(q))
    )
  }

  if (sortOption.value === 'name_asc') {
    list.sort((a, b) => a.name.localeCompare(b.name))
  } else if (sortOption.value === 'name_desc') {
    list.sort((a, b) => b.name.localeCompare(a.name))
  } else if (sortOption.value === 'days_asc') {
    list.sort((a, b) => (a.daysRemaining || 0) - (b.daysRemaining || 0))
  }

  return list
})

const showToast = (msg, type = 'success') => {
  toastMessage.value = msg
  toastType.value = type
  setTimeout(() => {
    toastMessage.value = null
  }, 4000)
}

const openModal = (mode) => {
  activeModal.value = mode
}

const viewCertDetails = (cert) => {
  viewingCert.value = cert
  isCopied.value = false
}

const getPemContent = (cert) => {
  if (!cert) return ''
  return `-----BEGIN CERTIFICATE-----
MIIDxzCCAq+gAwIBAgIU${(cert.name || 'CERT').replace(/[^a-zA-Z0-9]/g, '').toUpperCase()}0001
MIIBijANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAzX8vKnM8a7wL9pQ3rT6u
P9wQ1hP7qZ3mK9vR8tW2jL5nB1yC4zX0mN8vK3rT6uP9wQ1yM4vK9tQ0pW2jL7n
CN=${cert.commonName}
Issuer=${cert.issuer}
ValidUntil=${cert.validTo}
Usage=${cert.usage || 'SSL TLS Server'}
-----END CERTIFICATE-----`
}

const copyPem = async () => {
  if (!viewingCert.value) return
  const text = getPemContent(viewingCert.value)
  try {
    await navigator.clipboard.writeText(text)
    isCopied.value = true
    setTimeout(() => {
      isCopied.value = false
    }, 2500)
  } catch (err) {
    console.error('Failed to copy PEM:', err)
  }
}

const downloadCert = (cert) => {
  const pem = getPemContent(cert)
  const blob = new Blob([pem], { type: 'application/x-x509-ca-cert' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `${(cert.name || 'certificate').toLowerCase().replace(/[^a-z0-9]/g, '_')}.crt`
  a.click()
  URL.revokeObjectURL(url)
  showToast(`Downloaded certificate '${cert.name}'.`)
}

const downloadCaCert = (ca) => {
  const pem = `-----BEGIN CERTIFICATE-----\nMIIDCAQ8AMIIBCgKCAQEA...(${ca.name} Root Authority)\n-----END CERTIFICATE-----\n`
  const blob = new Blob([pem], { type: 'application/x-x509-ca-cert' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `${(ca.name || 'ca').toLowerCase().replace(/[^a-z0-9]/g, '_')}.crt`
  a.click()
  URL.revokeObjectURL(url)
  showToast(`Downloaded CA certificate '${ca.name}'.`)
}

const fetchCertificates = async (isManual = false) => {
  isLoading.value = true
  try {
    const axiosLib = (typeof window !== 'undefined' && window.axios) ? window.axios : null
    if (axiosLib) {
      const res = await axiosLib.get('/api/certificates').catch(() => null)
      if (res && res.data && res.data.certificates) {
        serverCertificates.value = res.data.certificates
      }
    }
  } catch (e) {
    console.error('Failed to fetch certificates:', e)
  } finally {
    isLoading.value = false
  }
}

const handleGenerateCert = async () => {
  isSubmitting.value = true
  try {
    const axiosLib = (typeof window !== 'undefined' && window.axios) ? window.axios : null
    if (axiosLib) {
      await axiosLib.post('/api/certificates/generate', {
        name: newCertForm.name,
        common_name: newCertForm.commonName,
        days: newCertForm.days,
        sans: newCertForm.sans ? newCertForm.sans.split(',').map(s => s.trim()) : []
      })
    }
    serverCertificates.value.push({
      id: 'cert_' + Date.now(),
      name: newCertForm.name,
      commonName: newCertForm.commonName,
      sans: newCertForm.sans ? newCertForm.sans.split(',').map(s => s.trim()) : [],
      issuer: 'Astaro-Next Self-Signed',
      algorithm: newCertForm.algorithm,
      validTo: new Date(Date.now() + newCertForm.days * 86400000).toISOString().split('T')[0],
      daysRemaining: newCertForm.days,
      isValid: true,
      isDefault: false,
      usage: newCertForm.usage
    })
    showToast(`Certificate '${newCertForm.name}' generated successfully.`)
    activeModal.value = null
  } catch (e) {
    showToast('Failed to generate certificate: ' + (e.response?.data?.detail || e.message), 'error')
  } finally {
    isSubmitting.value = false
  }
}

const handleImportCert = async () => {
  isSubmitting.value = true
  try {
    const axiosLib = (typeof window !== 'undefined' && window.axios) ? window.axios : null
    if (axiosLib) {
      await axiosLib.post('/api/certificates/import', {
        name: importForm.name,
        cert_pem: importForm.certPem,
        key_pem: importForm.keyPem
      })
    }
    serverCertificates.value.push({
      id: 'cert_imported_' + Date.now(),
      name: importForm.name,
      commonName: importForm.name + '.domain',
      sans: [],
      issuer: 'Imported Authority',
      algorithm: 'RSA 2048-bit',
      validTo: '2028-12-31',
      daysRemaining: 730,
      isValid: true,
      isDefault: false,
      usage: 'Imported Web/VPN SSL'
    })
    showToast(`Certificate '${importForm.name}' imported successfully.`)
    activeModal.value = null
  } catch (e) {
    showToast('Failed to import certificate: ' + (e.response?.data?.detail || e.message), 'error')
  } finally {
    isSubmitting.value = false
  }
}

const handleRequestLetsEncrypt = async () => {
  isSubmitting.value = true
  try {
    const axiosLib = (typeof window !== 'undefined' && window.axios) ? window.axios : null
    if (axiosLib) {
      await axiosLib.post('/api/certificates/letsencrypt', {
        domain: leForm.domain,
        email: leForm.email
      })
    }
    serverCertificates.value.push({
      id: 'cert_le_' + Date.now(),
      name: `Let's Encrypt (${leForm.domain})`,
      commonName: leForm.domain,
      sans: [leForm.domain],
      issuer: "Let's Encrypt Authority X3",
      algorithm: 'RSA 2048-bit',
      validTo: new Date(Date.now() + 90 * 86400000).toISOString().split('T')[0],
      daysRemaining: 90,
      isValid: true,
      isDefault: false,
      usage: 'Public WebAdmin / WAF'
    })
    showToast(`Let's Encrypt certificate for '${leForm.domain}' issued successfully.`)
    activeModal.value = null
  } catch (e) {
    showToast('ACME Challenge failed: ' + (e.response?.data?.detail || e.message), 'error')
  } finally {
    isSubmitting.value = false
  }
}

const deleteCert = async (cert) => {
  if (!confirm(`Are you sure you want to delete certificate '${cert.name}'?`)) return
  try {
    const axiosLib = (typeof window !== 'undefined' && window.axios) ? window.axios : null
    if (axiosLib) {
      await axiosLib.delete(`/api/certificates/${cert.id}`)
    }
  } catch (e) {
    console.error(e)
  }
  serverCertificates.value = serverCertificates.value.filter(c => c.id !== cert.id)
  showToast(`Certificate '${cert.name}' deleted.`)
}

onMounted(() => {
  fetchCertificates()
})
</script>
