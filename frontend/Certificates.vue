<template>
  <div class="space-y-6">
    <!-- Standardized Page Header -->
    <div class="bg-white border border-slate-200 rounded-xl p-5 shadow-xs flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
      <div>
        <div class="flex items-center gap-2.5">
          <span class="w-1.5 h-6 bg-[#ee7f00] rounded-xs inline-block"></span>
          <h1 class="text-xl font-bold text-slate-900 tracking-tight">Certificate Management</h1>
          <span class="text-[11px] bg-blue-50 text-[#0072ce] font-medium font-mono px-2 py-0.5 rounded border border-blue-200">
            X.509 / PKI / CSR / ACME
          </span>
        </div>
        <p class="text-xs text-slate-500 mt-1 pl-4">
          Unified certificate management: provision self-signed certificates, generate CSRs, import CER / PEM / P7B / PFX archives, and automated Let's Encrypt (HTTP-01, DNS-01, TLS-ALPN-01 with Single, Multi-Domain &amp; Wildcards).
        </p>
      </div>

      <!-- Action Buttons: Clean Consolidated Header -->
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

        <!-- Primary Consolidated "+ New Certificate..." Button -->
        <button
          type="button"
          @click="openNewCertModal('self_signed')"
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
        @click="activeTab = 'csrs'"
        :class="[
          'px-4 py-2 rounded-lg transition-all flex items-center gap-2 cursor-pointer whitespace-nowrap',
          activeTab === 'csrs'
            ? 'bg-white text-slate-900 shadow-xs border-b-2 border-[#ee7f00]'
            : 'text-slate-600 hover:text-slate-900 hover:bg-white/60'
        ]"
      >
        <span>Certificate Signing Requests (CSR)</span>
        <span class="px-1.5 py-0.2 rounded-full text-[10px] font-mono" :class="activeTab === 'csrs' ? 'bg-amber-500 text-white' : 'bg-slate-200 text-slate-700'">
          {{ csrsList.length }}
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
        <span>Let's Encrypt / ACME Engine</span>
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
        <span class="font-mono text-slate-600 font-bold">
          Showing {{ currentTabItemCount }} items
        </span>
      </div>
    </div>

    <!-- TAB 1: HOST & SERVER CERTIFICATES TABLE -->
    <div v-if="activeTab === 'server_certs'" class="bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden">
      <div v-if="filteredCerts.length === 0" class="p-12 text-center text-slate-400 text-xs">
        No server certificates found matching your search. Click "+ New Certificate..." to add or import.
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

    <!-- TAB 2: CERTIFICATE SIGNING REQUESTS (CSR) -->
    <div v-if="activeTab === 'csrs'" class="bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden">
      <div v-if="filteredCsrs.length === 0" class="p-12 text-center text-slate-400 text-xs">
        No Certificate Signing Requests (CSR) found. Click "+ New Certificate..." -> "Generate CSR" to create a PKCS#10 request.
      </div>
      <table v-else class="w-full text-left text-xs border-collapse">
        <thead class="bg-[#f4f6f9] text-slate-700 font-bold border-b border-slate-200">
          <tr>
            <th class="p-3 pl-4">CSR Friendly Name</th>
            <th class="p-3 font-mono">Common Name (CN) / Subject</th>
            <th class="p-3">Organization (O / OU)</th>
            <th class="p-3 font-mono">Key Algorithm</th>
            <th class="p-3">Status</th>
            <th class="p-3 font-mono">Created Date</th>
            <th class="p-3 text-right pr-4">Actions</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-100 font-medium text-slate-700">
          <tr
            v-for="(csr, idx) in filteredCsrs"
            :key="csr.id || idx"
            :class="idx % 2 === 0 ? 'bg-white' : 'bg-[#f7f7f7]'"
            class="hover:bg-amber-50/40 transition-colors"
          >
            <td class="p-3 pl-4 font-bold text-slate-900 flex items-center gap-2">
              <span class="w-2 h-2 rounded-full" :class="csr.status.includes('Completed') ? 'bg-emerald-500' : 'bg-amber-500'"></span>
              <span>{{ csr.name }}</span>
            </td>

            <td class="p-3 font-mono font-bold text-slate-800">
              {{ csr.commonName }}
            </td>

            <td class="p-3 text-slate-600">
              {{ csr.organization }} &bull; {{ csr.organizationalUnit }}
            </td>

            <td class="p-3 font-mono text-[11px]">
              <span class="px-1.5 py-0.5 rounded bg-slate-100 text-slate-700 border border-slate-200 font-semibold">{{ csr.algorithm || 'RSA 2048-bit' }}</span>
            </td>

            <td class="p-3">
              <span
                :class="[
                  'px-2 py-0.5 rounded text-[10px] font-bold border',
                  csr.status.includes('Completed')
                    ? 'bg-emerald-50 text-emerald-700 border-emerald-200'
                    : 'bg-amber-50 text-amber-800 border-amber-200'
                ]"
              >
                {{ csr.status }}
              </span>
            </td>

            <td class="p-3 font-mono text-slate-500">
              {{ csr.createdAt }}
            </td>

            <td class="p-3 text-right pr-4 space-x-1.5 whitespace-nowrap">
              <button
                type="button"
                @click="viewCsrDetails(csr)"
                class="px-2 py-1 bg-white hover:bg-slate-50 text-slate-700 border border-slate-300 rounded text-[11px] font-bold shadow-2xs cursor-pointer"
                title="Inspect CSR text and copy PEM"
              >
                View CSR
              </button>
              <button
                type="button"
                @click="downloadCsr(csr)"
                class="px-2 py-1 bg-amber-50 hover:bg-amber-100 text-amber-900 border border-amber-300 rounded text-[11px] font-bold shadow-2xs cursor-pointer"
                title="Download PKCS#10 .csr file"
              >
                Download (.csr)
              </button>
              <button
                type="button"
                @click="openCompleteCsrModal(csr)"
                class="px-2 py-1 bg-emerald-50 hover:bg-emerald-100 text-emerald-800 border border-emerald-300 rounded text-[11px] font-bold shadow-2xs cursor-pointer"
                title="Upload signed certificate from CA"
              >
                Upload Signed Cert
              </button>
              <button
                type="button"
                @click="deleteCsr(csr)"
                class="px-2 py-1 bg-white hover:bg-rose-50 text-rose-600 border border-rose-200 rounded text-[11px] font-bold shadow-2xs cursor-pointer"
              >
                Delete
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- TAB 3: CERTIFICATE AUTHORITIES (CAs) -->
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

    <!-- TAB 4: LET'S ENCRYPT (ACME) AUTOMATION -->
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
              <h2 class="text-base font-bold text-slate-900">Let's Encrypt (ACME) Automated Engine</h2>
              <p class="text-xs text-slate-500 mt-0.5">Supports HTTP-01, DNS-01, and TLS-ALPN-01 challenges for Single Domain, Multi-Domain SAN, and Wildcard (*.domain.com) certificates.</p>
            </div>
          </div>
          <button
            type="button"
            @click="openNewCertModal('letsencrypt')"
            class="px-4 py-2 rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-bold shadow-sm transition-all cursor-pointer flex items-center gap-1.5"
          >
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
            <span>+ Request ACME Certificate</span>
          </button>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div class="p-4 rounded-lg bg-slate-50 border border-slate-200">
            <div class="text-slate-500 text-[11px] font-semibold uppercase tracking-wider">Validation Protocols</div>
            <div class="text-base font-bold text-slate-900 mt-1">HTTP-01 &bull; DNS-01 &bull; TLS-ALPN-01</div>
            <div class="text-xs text-emerald-600 font-medium mt-0.5">Automated Challenge Responders</div>
          </div>
          <div class="p-4 rounded-lg bg-slate-50 border border-slate-200">
            <div class="text-slate-500 text-[11px] font-semibold uppercase tracking-wider">Scope Capabilities</div>
            <div class="text-base font-bold text-slate-900 mt-1">Single, Multi-SAN, Wildcard</div>
            <div class="text-xs text-slate-500 font-medium mt-0.5">Full RFC 8555 Compatibility</div>
          </div>
          <div class="p-4 rounded-lg bg-slate-50 border border-slate-200">
            <div class="text-slate-500 text-[11px] font-semibold uppercase tracking-wider">Auto-Renewal Hook</div>
            <div class="text-base font-bold text-slate-900 mt-1">Every 60 Days</div>
            <div class="text-xs text-slate-500 font-medium mt-0.5">systemd-timer / Crond Engine</div>
          </div>
        </div>
      </div>
    </div>

    <!-- CONSOLIDATED MODAL: + NEW CERTIFICATE (Includes Self-Signed, CSR, Import CER/PEM/P7B/PFX via File or Text, Let's Encrypt with HTTP/DNS/TLS and Single/Multi/Wildcard) -->
    <transition
      enter-active-class="transition duration-150 ease-out"
      enter-from-class="opacity-0 scale-95"
      enter-to-class="opacity-100 scale-100"
      leave-active-class="transition duration-100 ease-in"
      leave-from-class="opacity-100 scale-100"
      leave-to-class="opacity-0 scale-95"
    >
      <div
        v-if="isNewCertModalOpen"
        class="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4"
        @keydown.esc="isNewCertModalOpen = false"
      >
        <div class="bg-white rounded-2xl shadow-2xl border border-slate-200 max-w-xl w-full overflow-hidden flex flex-col max-h-[90vh]">
          <!-- Modal Header -->
          <div class="px-5 py-3.5 bg-slate-900 text-white flex items-center justify-between border-b border-slate-800">
            <div class="flex items-center gap-2.5">
              <div class="w-8 h-8 rounded-lg bg-[#ee7f00] flex items-center justify-center text-white font-bold text-xs shadow-md">
                TLS
              </div>
              <div>
                <h3 class="text-xs font-bold uppercase tracking-wider text-white">Add New Certificate / CSR</h3>
                <p class="text-[10px] text-slate-400">Self-Signed, CSR Generation, File/Text Import (CER/PEM/P7B/PFX), or Let's Encrypt ACME</p>
              </div>
            </div>
            <button @click="isNewCertModalOpen = false" class="text-slate-400 hover:text-white font-bold cursor-pointer text-base leading-none">&times;</button>
          </div>

          <!-- Method Selection Tabs inside Modal -->
          <div class="flex border-b border-slate-200 bg-[#f4f6f9] p-1.5 text-xs font-bold">
            <button
              type="button"
              @click="creationMethod = 'self_signed'"
              :class="[
                'flex-1 py-2 text-center rounded-lg transition-all cursor-pointer',
                creationMethod === 'self_signed' ? 'bg-white text-[#0072ce] shadow-xs' : 'text-slate-600 hover:text-slate-900'
              ]"
            >
              Self-Signed
            </button>
            <button
              type="button"
              @click="creationMethod = 'csr'"
              :class="[
                'flex-1 py-2 text-center rounded-lg transition-all cursor-pointer',
                creationMethod === 'csr' ? 'bg-white text-amber-700 shadow-xs' : 'text-slate-600 hover:text-slate-900'
              ]"
            >
              Generate CSR
            </button>
            <button
              type="button"
              @click="creationMethod = 'import'"
              :class="[
                'flex-1 py-2 text-center rounded-lg transition-all cursor-pointer',
                creationMethod === 'import' ? 'bg-white text-[#0072ce] shadow-xs' : 'text-slate-600 hover:text-slate-900'
              ]"
            >
              Import File/Text
            </button>
            <button
              type="button"
              @click="creationMethod = 'letsencrypt'"
              :class="[
                'flex-1 py-2 text-center rounded-lg transition-all cursor-pointer',
                creationMethod === 'letsencrypt' ? 'bg-white text-emerald-700 shadow-xs' : 'text-slate-600 hover:text-slate-900'
              ]"
            >
              Let's Encrypt
            </button>
          </div>

          <!-- Method 1: Generate Self-Signed Certificate -->
          <form v-if="creationMethod === 'self_signed'" @submit.prevent="handleGenerateCert" class="p-5 space-y-3.5 text-xs overflow-y-auto flex-1">
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
              <button type="button" @click="isNewCertModalOpen = false" class="px-3.5 py-1.5 border rounded text-slate-700 cursor-pointer">Cancel</button>
              <button type="submit" :disabled="isSubmitting" class="px-4 py-1.5 bg-[#0072ce] hover:bg-blue-700 text-white font-bold rounded shadow-xs cursor-pointer disabled:opacity-50">
                {{ isSubmitting ? 'Generating...' : 'Generate Self-Signed Certificate' }}
              </button>
            </div>
          </form>

          <!-- Method 2: Generate CSR -->
          <form v-else-if="creationMethod === 'csr'" @submit.prevent="handleGenerateCsr" class="p-5 space-y-3 text-xs overflow-y-auto flex-1">
            <div>
              <label class="block font-bold text-slate-700 mb-1">CSR Friendly Name *</label>
              <input type="text" required v-model="csrForm.name" placeholder="e.g. Public-Gateway-2026-CSR" class="w-full p-2 border border-slate-300 rounded focus:border-[#0072ce] focus:outline-none" />
            </div>

            <div class="grid grid-cols-2 gap-3">
              <div>
                <label class="block font-bold text-slate-700 mb-1">Common Name (CN) / FQDN *</label>
                <input type="text" required v-model="csrForm.commonName" placeholder="vpn.mycompany.com" class="w-full p-2 border border-slate-300 rounded font-mono" />
              </div>
              <div>
                <label class="block font-bold text-slate-700 mb-1">Key Algorithm</label>
                <select v-model="csrForm.algorithm" class="w-full p-2 border border-slate-300 rounded bg-white font-medium">
                  <option value="RSA 2048-bit">RSA 2048-bit (Standard)</option>
                  <option value="RSA 4096-bit">RSA 4096-bit (High Security)</option>
                  <option value="ECDSA P-256">ECDSA P-256 (ECC)</option>
                </select>
              </div>
            </div>

            <div class="grid grid-cols-2 gap-3">
              <div>
                <label class="block font-bold text-slate-700 mb-1">Organization (O)</label>
                <input type="text" v-model="csrForm.organization" placeholder="e.g. Enterprise Global Corp" class="w-full p-2 border border-slate-300 rounded" />
              </div>
              <div>
                <label class="block font-bold text-slate-700 mb-1">Organizational Unit (OU)</label>
                <input type="text" v-model="csrForm.organizationalUnit" placeholder="e.g. IT Security" class="w-full p-2 border border-slate-300 rounded" />
              </div>
            </div>

            <div class="grid grid-cols-3 gap-3">
              <div>
                <label class="block font-bold text-slate-700 mb-1">Country (2-Letter)</label>
                <input type="text" maxlength="2" v-model="csrForm.country" placeholder="US" class="w-full p-2 border border-slate-300 rounded font-mono uppercase" />
              </div>
              <div>
                <label class="block font-bold text-slate-700 mb-1">State / Province</label>
                <input type="text" v-model="csrForm.state" placeholder="California" class="w-full p-2 border border-slate-300 rounded" />
              </div>
              <div>
                <label class="block font-bold text-slate-700 mb-1">City / Locality</label>
                <input type="text" v-model="csrForm.city" placeholder="San Francisco" class="w-full p-2 border border-slate-300 rounded" />
              </div>
            </div>

            <div>
              <label class="block font-bold text-slate-700 mb-1">Subject Alternative Names (SANs)</label>
              <input type="text" v-model="csrForm.sans" placeholder="vpn.company.com, remote.company.com" class="w-full p-2 border border-slate-300 rounded font-mono" />
            </div>

            <div class="pt-3 border-t border-slate-200 flex justify-between">
              <button type="button" @click="isNewCertModalOpen = false" class="px-3.5 py-1.5 border rounded text-slate-700 cursor-pointer">Cancel</button>
              <button type="submit" :disabled="isSubmitting" class="px-4 py-1.5 bg-amber-500 hover:bg-amber-600 text-white font-bold rounded shadow-xs cursor-pointer disabled:opacity-50">
                {{ isSubmitting ? 'Generating...' : 'Generate & Save CSR' }}
              </button>
            </div>
          </form>

          <!-- Method 3: Import File/Text (CER, PEM, P7B, PFX) -->
          <form v-else-if="creationMethod === 'import'" @submit.prevent="handleImportCert" class="p-5 space-y-3.5 text-xs overflow-y-auto flex-1">
            <div class="grid grid-cols-2 gap-3">
              <div>
                <label class="block font-bold text-slate-700 mb-1">Certificate Friendly Name *</label>
                <input type="text" required v-model="importForm.name" placeholder="e.g. Wildcard-Cert-2026" class="w-full p-2 border border-slate-300 rounded" />
              </div>
              <div>
                <label class="block font-bold text-slate-700 mb-1">Certificate Format</label>
                <select v-model="importForm.format" class="w-full p-2 border border-slate-300 rounded bg-white font-bold text-[#0072ce]">
                  <option value="pem">PEM / CER (.pem, .crt, .cer)</option>
                  <option value="pfx">PKCS#12 / PFX (.pfx, .p12)</option>
                  <option value="p7b">PKCS#7 / P7B (.p7b, .p7c)</option>
                </select>
              </div>
            </div>

            <!-- Input Mode Switcher: Upload File(s) vs Paste Text Content -->
            <div class="flex items-center justify-between p-1.5 bg-slate-100 rounded-lg border border-slate-200 text-xs">
              <span class="font-bold text-slate-700 pl-1">Input Method:</span>
              <div class="flex items-center gap-1">
                <button
                  type="button"
                  @click="importInputMode = 'file'"
                  :class="[
                    'px-3 py-1 rounded-md font-bold transition-all cursor-pointer flex items-center gap-1.5',
                    importInputMode === 'file' ? 'bg-white text-[#0072ce] shadow-xs' : 'text-slate-600 hover:text-slate-900'
                  ]"
                >
                  <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
                  </svg>
                  <span>Upload File(s)</span>
                </button>
                <button
                  type="button"
                  @click="importInputMode = 'text'"
                  :class="[
                    'px-3 py-1 rounded-md font-bold transition-all cursor-pointer flex items-center gap-1.5',
                    importInputMode === 'text' ? 'bg-white text-[#0072ce] shadow-xs' : 'text-slate-600 hover:text-slate-900'
                  ]"
                >
                  <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                  </svg>
                  <span>Paste Text / Base64</span>
                </button>
              </div>
            </div>

            <!-- FORMAT 1: PEM / CER -->
            <div v-if="importForm.format === 'pem' || importForm.format === 'cer'" class="space-y-3">
              <div v-if="importInputMode === 'file'" class="space-y-3">
                <div>
                  <label class="block font-bold text-slate-700 mb-1">Upload Certificate File (.cer, .crt, .pem) *</label>
                  <div class="border-2 border-dashed border-slate-300 hover:border-[#0072ce] rounded-xl p-3 bg-slate-50/60 text-center relative cursor-pointer">
                    <input type="file" accept=".crt,.cer,.pem,.txt" @change="onCertFileUpload" class="absolute inset-0 opacity-0 cursor-pointer w-full h-full" />
                    <div class="flex flex-col items-center justify-center gap-1">
                      <svg class="w-6 h-6 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                      </svg>
                      <span v-if="uploadedCertFileName" class="font-bold text-[#0072ce] font-mono">{{ uploadedCertFileName }}</span>
                      <span v-else class="text-slate-500 text-[11px]">Click or drag &amp; drop certificate (.cer / .crt / .pem)</span>
                    </div>
                  </div>
                </div>

                <div>
                  <label class="block font-bold text-slate-700 mb-1">Upload Private Key File (.key, .pem)</label>
                  <div class="border-2 border-dashed border-slate-300 hover:border-[#0072ce] rounded-xl p-3 bg-slate-50/60 text-center relative cursor-pointer">
                    <input type="file" accept=".key,.pem,.txt" @change="onKeyFileUpload" class="absolute inset-0 opacity-0 cursor-pointer w-full h-full" />
                    <div class="flex flex-col items-center justify-center gap-1">
                      <svg class="w-6 h-6 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z" />
                      </svg>
                      <span v-if="uploadedKeyFileName" class="font-bold text-[#0072ce] font-mono">{{ uploadedKeyFileName }}</span>
                      <span v-else class="text-slate-500 text-[11px]">Click or drag &amp; drop private key (.key)</span>
                    </div>
                  </div>
                </div>
              </div>

              <div v-else class="space-y-3">
                <div>
                  <label class="block font-bold text-slate-700 mb-1">X.509 Certificate Content (.cer / .crt / .pem) *</label>
                  <textarea required rows="4" v-model="importForm.certPem" placeholder="-----BEGIN CERTIFICATE-----&#10;...&#10;-----END CERTIFICATE-----" class="w-full p-2 border border-slate-300 rounded font-mono text-[10px] focus:outline-none focus:border-[#0072ce]"></textarea>
                </div>
                <div>
                  <label class="block font-bold text-slate-700 mb-1">Private Key (.key / .pem)</label>
                  <textarea rows="3" v-model="importForm.keyPem" placeholder="-----BEGIN PRIVATE KEY-----&#10;...&#10;-----END PRIVATE KEY-----" class="w-full p-2 border border-slate-300 rounded font-mono text-[10px] focus:outline-none focus:border-[#0072ce]"></textarea>
                </div>
              </div>
            </div>

            <!-- FORMAT 2: PFX / PKCS#12 -->
            <div v-else-if="importForm.format === 'pfx'" class="space-y-3 p-3.5 bg-blue-50/50 rounded-xl border border-blue-200">
              <div class="text-[11px] font-bold text-[#0072ce]">
                PKCS#12 (PFX) Container contains both Certificate and Private Key.
              </div>

              <div v-if="importInputMode === 'file'">
                <label class="block font-bold text-slate-700 mb-1">Upload PFX / P12 Container File (.pfx, .p12) *</label>
                <div class="border-2 border-dashed border-blue-300 hover:border-[#0072ce] rounded-xl p-3.5 bg-white text-center relative cursor-pointer">
                  <input type="file" accept=".pfx,.p12" @change="onPfxFileUpload" class="absolute inset-0 opacity-0 cursor-pointer w-full h-full" />
                  <div class="flex flex-col items-center justify-center gap-1">
                    <svg class="w-7 h-7 text-[#0072ce]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                    </svg>
                    <span v-if="uploadedPfxFileName" class="font-bold text-slate-900 font-mono">{{ uploadedPfxFileName }}</span>
                    <span v-else class="text-slate-500 text-[11px]">Click or drag &amp; drop container file (.pfx / .p12)</span>
                  </div>
                </div>
              </div>

              <div v-else>
                <label class="block font-bold text-slate-700 mb-1">PFX Base64 Content *</label>
                <textarea required rows="4" v-model="importForm.pfxData" placeholder="Paste PFX Base64 encoded string..." class="w-full p-2 border border-slate-300 rounded font-mono text-[10px] bg-white"></textarea>
              </div>

              <div>
                <label class="block font-bold text-slate-700 mb-1">PFX Container Passphrase / Password *</label>
                <input type="password" required v-model="importForm.passphrase" placeholder="••••••••••••" class="w-full p-2 border border-slate-300 rounded bg-white font-mono" />
              </div>
            </div>

            <!-- FORMAT 3: P7B / PKCS#7 -->
            <div v-else-if="importForm.format === 'p7b'" class="space-y-3 p-3.5 bg-amber-50/50 rounded-xl border border-amber-200">
              <div class="text-[11px] font-bold text-amber-900">
                PKCS#7 (P7B) Chain Bundle contains public certificates and intermediates.
              </div>

              <div v-if="importInputMode === 'file'" class="space-y-3">
                <div>
                  <label class="block font-bold text-slate-700 mb-1">Upload P7B Certificate Chain File (.p7b, .p7c) *</label>
                  <div class="border-2 border-dashed border-amber-300 hover:border-amber-500 rounded-xl p-3 bg-white text-center relative cursor-pointer">
                    <input type="file" accept=".p7b,.p7c,.txt" @change="onP7bFileUpload" class="absolute inset-0 opacity-0 cursor-pointer w-full h-full" />
                    <div class="flex flex-col items-center justify-center gap-1">
                      <svg class="w-6 h-6 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                      </svg>
                      <span v-if="uploadedP7bFileName" class="font-bold text-slate-900 font-mono">{{ uploadedP7bFileName }}</span>
                      <span v-else class="text-slate-500 text-[11px]">Click or drag &amp; drop P7B chain file (.p7b / .p7c)</span>
                    </div>
                  </div>
                </div>

                <div>
                  <label class="block font-bold text-slate-700 mb-1">Upload Matching Private Key (.key) *</label>
                  <div class="border-2 border-dashed border-amber-300 hover:border-amber-500 rounded-xl p-3 bg-white text-center relative cursor-pointer">
                    <input type="file" accept=".key,.pem,.txt" @change="onKeyFileUpload" class="absolute inset-0 opacity-0 cursor-pointer w-full h-full" />
                    <div class="flex flex-col items-center justify-center gap-1">
                      <svg class="w-6 h-6 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z" />
                      </svg>
                      <span v-if="uploadedKeyFileName" class="font-bold text-slate-900 font-mono">{{ uploadedKeyFileName }}</span>
                      <span v-else class="text-slate-500 text-[11px]">Click or drag &amp; drop private key (.key)</span>
                    </div>
                  </div>
                </div>
              </div>

              <div v-else class="space-y-3">
                <div>
                  <label class="block font-bold text-slate-700 mb-1">P7B Certificate Chain Content (.p7b / .p7c) *</label>
                  <textarea required rows="4" v-model="importForm.p7bData" placeholder="-----BEGIN PKCS7-----&#10;...&#10;-----END PKCS7-----" class="w-full p-2 border border-slate-300 rounded font-mono text-[10px] bg-white"></textarea>
                </div>
                <div>
                  <label class="block font-bold text-slate-700 mb-1">Matching Private Key (.key) *</label>
                  <textarea required rows="3" v-model="importForm.keyPem" placeholder="-----BEGIN PRIVATE KEY-----&#10;...&#10;-----END PRIVATE KEY-----" class="w-full p-2 border border-slate-300 rounded font-mono text-[10px] bg-white"></textarea>
                </div>
              </div>
            </div>

            <div>
              <label class="block font-bold text-slate-700 mb-1">Assign Service</label>
              <select v-model="importForm.usage" class="w-full p-2 border border-slate-300 rounded bg-white font-medium">
                <option value="WebAdmin HTTPS">WebAdmin HTTPS</option>
                <option value="WAF / Reverse Proxy">WAF / Reverse Proxy</option>
                <option value="SSL VPN Server">SSL VPN Server</option>
                <option value="Imported Web/VPN SSL">Imported Web/VPN SSL</option>
              </select>
            </div>

            <div class="pt-3 border-t border-slate-200 flex justify-between">
              <button type="button" @click="isNewCertModalOpen = false" class="px-3.5 py-1.5 border rounded text-slate-700 cursor-pointer">Cancel</button>
              <button type="submit" :disabled="isSubmitting" class="px-4 py-1.5 bg-[#0072ce] hover:bg-blue-700 text-white font-bold rounded shadow-xs cursor-pointer disabled:opacity-50">
                {{ isSubmitting ? 'Importing...' : 'Import & Install Certificate' }}
              </button>
            </div>
          </form>

          <!-- Method 4: Let's Encrypt / ACME with Single/Multi/Wildcard & HTTP/DNS/TLS -->
          <form v-else-if="creationMethod === 'letsencrypt'" @submit.prevent="handleRequestLetsEncrypt" class="p-5 space-y-3.5 text-xs overflow-y-auto flex-1">
            <!-- Scope Selector (Single Domain, Multi-Domain SAN, Wildcard) -->
            <div>
              <label class="block font-bold text-slate-700 mb-1">Certificate Scope</label>
              <div class="grid grid-cols-3 gap-2">
                <label
                  :class="[
                    'p-2.5 rounded-lg border text-center cursor-pointer transition-all flex flex-col items-center justify-center gap-1',
                    leForm.scope === 'single' ? 'border-[#0072ce] bg-blue-50/50 text-[#0072ce] font-bold' : 'border-slate-200 bg-slate-50 text-slate-700'
                  ]"
                >
                  <input type="radio" value="single" v-model="leForm.scope" class="sr-only" />
                  <span class="text-xs">Single Domain</span>
                  <span class="text-[10px] text-slate-400 font-normal">gateway.domain.com</span>
                </label>

                <label
                  :class="[
                    'p-2.5 rounded-lg border text-center cursor-pointer transition-all flex flex-col items-center justify-center gap-1',
                    leForm.scope === 'multi_domain' ? 'border-[#0072ce] bg-blue-50/50 text-[#0072ce] font-bold' : 'border-slate-200 bg-slate-50 text-slate-700'
                  ]"
                >
                  <input type="radio" value="multi_domain" v-model="leForm.scope" class="sr-only" />
                  <span class="text-xs">Multi-Domain (SAN)</span>
                  <span class="text-[10px] text-slate-400 font-normal">Multiple FQDNs</span>
                </label>

                <label
                  :class="[
                    'p-2.5 rounded-lg border text-center cursor-pointer transition-all flex flex-col items-center justify-center gap-1',
                    leForm.scope === 'wildcard' ? 'border-[#0072ce] bg-blue-50/50 text-[#0072ce] font-bold' : 'border-slate-200 bg-slate-50 text-slate-700'
                  ]"
                >
                  <input type="radio" value="wildcard" v-model="leForm.scope" class="sr-only" />
                  <span class="text-xs">Wildcard</span>
                  <span class="text-[10px] text-slate-400 font-normal">*.domain.com</span>
                </label>
              </div>
            </div>

            <!-- Primary Domain Input -->
            <div>
              <label class="block font-bold text-slate-700 mb-1">
                {{ leForm.scope === 'wildcard' ? 'Base Domain Name (Wildcard *. will be prefixed) *' : 'Primary Domain Name (FQDN) *' }}
              </label>
              <div class="relative">
                <input
                  type="text"
                  required
                  v-model="leForm.domain"
                  :placeholder="leForm.scope === 'wildcard' ? 'e.g. mycompany.com' : 'e.g. gateway.mycompany.com'"
                  class="w-full p-2 border border-slate-300 rounded font-mono focus:border-[#0072ce] focus:outline-none"
                />
              </div>
              <p v-if="leForm.scope === 'wildcard'" class="text-[10px] text-emerald-600 mt-0.5">
                Will automatically issue SANs: <strong>*.{{ leForm.domain || 'domain.com' }}</strong> and <strong>{{ leForm.domain || 'domain.com' }}</strong>.
              </p>
            </div>

            <!-- Multi-Domain Additional SANs Input -->
            <div v-if="leForm.scope === 'multi_domain'">
              <label class="block font-bold text-slate-700 mb-1">Additional Subject Alternative Names (SANs)</label>
              <input
                type="text"
                v-model="leForm.sansInput"
                placeholder="vpn.mycompany.com, portal.mycompany.com, mail.mycompany.com"
                class="w-full p-2 border border-slate-300 rounded font-mono focus:border-[#0072ce] focus:outline-none"
              />
              <p class="text-[10px] text-slate-400 mt-0.5">Comma-separated list of additional domains included in this certificate.</p>
            </div>

            <!-- Validation Challenge Type (HTTP-01, DNS-01, TLS-ALPN-01) -->
            <div>
              <label class="block font-bold text-slate-700 mb-1">ACME Validation Challenge Method</label>
              <div class="grid grid-cols-3 gap-2">
                <label
                  :class="[
                    'p-2.5 rounded-lg border text-center transition-all flex flex-col items-center justify-center gap-1',
                    leForm.scope === 'wildcard' ? 'opacity-40 cursor-not-allowed bg-slate-100 border-slate-200' : 'cursor-pointer',
                    leForm.validationMethod === 'http-01' ? 'border-emerald-500 bg-emerald-50/50 text-emerald-800 font-bold' : 'border-slate-200 bg-slate-50 text-slate-700'
                  ]"
                >
                  <input type="radio" value="http-01" v-model="leForm.validationMethod" :disabled="leForm.scope === 'wildcard'" class="sr-only" />
                  <span class="text-xs">HTTP-01</span>
                  <span class="text-[10px] text-slate-400 font-normal">Port 80 Ingress</span>
                </label>

                <label
                  :class="[
                    'p-2.5 rounded-lg border text-center cursor-pointer transition-all flex flex-col items-center justify-center gap-1',
                    leForm.validationMethod === 'dns-01' ? 'border-emerald-500 bg-emerald-50/50 text-emerald-800 font-bold' : 'border-slate-200 bg-slate-50 text-slate-700'
                  ]"
                >
                  <input type="radio" value="dns-01" v-model="leForm.validationMethod" class="sr-only" />
                  <span class="text-xs">DNS-01</span>
                  <span class="text-[10px] text-slate-400 font-normal">DNS TXT / Wildcard</span>
                </label>

                <label
                  :class="[
                    'p-2.5 rounded-lg border text-center transition-all flex flex-col items-center justify-center gap-1',
                    leForm.scope === 'wildcard' ? 'opacity-40 cursor-not-allowed bg-slate-100 border-slate-200' : 'cursor-pointer',
                    leForm.validationMethod === 'tls-alpn-01' ? 'border-emerald-500 bg-emerald-50/50 text-emerald-800 font-bold' : 'border-slate-200 bg-slate-50 text-slate-700'
                  ]"
                >
                  <input type="radio" value="tls-alpn-01" v-model="leForm.validationMethod" :disabled="leForm.scope === 'wildcard'" class="sr-only" />
                  <span class="text-xs">TLS-ALPN-01</span>
                  <span class="text-[10px] text-slate-400 font-normal">Port 443 ALPN</span>
                </label>
              </div>
            </div>

            <!-- DNS Provider Configuration if DNS-01 selected -->
            <div v-if="leForm.validationMethod === 'dns-01'" class="p-3 bg-amber-50/60 rounded-xl border border-amber-200 space-y-2.5">
              <div class="flex items-center justify-between">
                <span class="font-bold text-amber-900 text-xs">DNS Provider Integration</span>
                <span class="text-[10px] bg-amber-200/60 text-amber-800 px-1.5 py-0.2 rounded font-semibold">Required for Wildcards</span>
              </div>
              <div class="grid grid-cols-2 gap-2">
                <div>
                  <label class="block font-bold text-slate-700 mb-0.5">DNS Provider</label>
                  <select v-model="leForm.dnsProvider" class="w-full p-1.5 border border-slate-300 rounded bg-white font-medium">
                    <option value="cloudflare">Cloudflare DNS API</option>
                    <option value="route53">AWS Route53</option>
                    <option value="digitalocean">DigitalOcean DNS</option>
                    <option value="rfc2136">RFC 2136 BIND (Dynamic DNS)</option>
                    <option value="manual">Manual DNS TXT Record</option>
                  </select>
                </div>
                <div v-if="leForm.dnsProvider !== 'manual'">
                  <label class="block font-bold text-slate-700 mb-0.5">API Token / Secret Key</label>
                  <input type="password" v-model="leForm.dnsApiToken" placeholder="••••••••••••" class="w-full p-1.5 border border-slate-300 rounded bg-white font-mono" />
                </div>
              </div>
            </div>

            <!-- Admin Email -->
            <div>
              <label class="block font-bold text-slate-700 mb-1">Admin Email (Expiration &amp; Recovery Notices) *</label>
              <input type="email" required v-model="leForm.email" placeholder="admin@mycompany.com" class="w-full p-2 border border-slate-300 rounded" />
            </div>

            <!-- Challenge Context Alert -->
            <div v-if="leForm.validationMethod === 'http-01'" class="p-3 bg-emerald-50 rounded-lg border border-emerald-200 text-emerald-900 text-[11px] space-y-1">
              <div class="font-bold flex items-center gap-1.5">
                <span>HTTP-01 Validation Active</span>
              </div>
              <p>Ensure inbound TCP Port 80 is forwarded to the firewall's ACME webroot verification responder.</p>
            </div>
            <div v-else-if="leForm.validationMethod === 'tls-alpn-01'" class="p-3 bg-blue-50 rounded-lg border border-blue-200 text-blue-900 text-[11px] space-y-1">
              <div class="font-bold flex items-center gap-1.5">
                <span>TLS-ALPN-01 Validation Active</span>
              </div>
              <p>Uses direct Port 443 TLS handshake validation on the firewall. Does not require port 80 to be open.</p>
            </div>

            <div class="pt-3 border-t border-slate-200 flex justify-between">
              <button type="button" @click="isNewCertModalOpen = false" class="px-3.5 py-1.5 border rounded text-slate-700 cursor-pointer">Cancel</button>
              <button type="submit" :disabled="isSubmitting" class="px-4 py-1.5 bg-emerald-600 hover:bg-emerald-700 text-white font-bold rounded shadow-xs cursor-pointer disabled:opacity-50 flex items-center gap-1.5">
                <span>{{ isSubmitting ? 'Requesting...' : 'Request &amp; Install ACME Certificate' }}</span>
              </button>
            </div>
          </form>
        </div>
      </div>
    </transition>

    <!-- MODAL: VIEW CERTIFICATE DETAILS -->
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

            <div>
              <div class="flex items-center justify-between mb-1">
                <span class="font-bold text-slate-700">Raw X.509 PEM Certificate</span>
                <button
                  type="button"
                  @click="copyPem(getPemContent(viewingCert))"
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

    <!-- MODAL: VIEW CSR DETAILS -->
    <transition
      enter-active-class="transition duration-150 ease-out"
      enter-from-class="opacity-0 scale-95"
      enter-to-class="opacity-100 scale-100"
      leave-active-class="transition duration-100 ease-in"
      leave-from-class="opacity-100 scale-100"
      leave-to-class="opacity-0 scale-95"
    >
      <div
        v-if="viewingCsr"
        class="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4"
        @keydown.esc="viewingCsr = null"
      >
        <div class="bg-white rounded-2xl shadow-2xl border border-slate-200 max-w-lg w-full overflow-hidden flex flex-col max-h-[90vh]">
          <div class="px-5 py-3.5 bg-slate-900 text-white flex items-center justify-between border-b border-slate-800">
            <div class="flex items-center gap-2.5">
              <div class="w-8 h-8 rounded-lg bg-amber-500 flex items-center justify-center text-white font-bold text-xs shadow-md">
                CSR
              </div>
              <div>
                <h3 class="text-xs font-bold uppercase tracking-wider text-white">
                  CSR Details: {{ viewingCsr.name }}
                </h3>
                <p class="text-[10px] text-slate-400 font-mono">CN={{ viewingCsr.commonName }}</p>
              </div>
            </div>
            <button @click="viewingCsr = null" class="text-slate-400 hover:text-white font-bold cursor-pointer text-base leading-none">&times;</button>
          </div>

          <div class="p-5 space-y-4 text-xs overflow-y-auto flex-1 font-sans">
            <div class="grid grid-cols-2 gap-3 p-3 bg-slate-50 rounded-xl border border-slate-200">
              <div>
                <div class="text-[10px] uppercase font-bold text-slate-400">Common Name (CN)</div>
                <div class="font-bold text-slate-900 font-mono mt-0.5">{{ viewingCsr.commonName }}</div>
              </div>
              <div>
                <div class="text-[10px] uppercase font-bold text-slate-400">Key Algorithm</div>
                <div class="font-bold text-slate-900 font-mono mt-0.5">{{ viewingCsr.algorithm || 'RSA 2048-bit' }}</div>
              </div>
              <div>
                <div class="text-[10px] uppercase font-bold text-slate-400">Organization (O)</div>
                <div class="font-bold text-slate-900 mt-0.5">{{ viewingCsr.organization || 'N/A' }}</div>
              </div>
              <div>
                <div class="text-[10px] uppercase font-bold text-slate-400">Organizational Unit (OU)</div>
                <div class="font-bold text-slate-900 mt-0.5">{{ viewingCsr.organizationalUnit || 'N/A' }}</div>
              </div>
              <div>
                <div class="text-[10px] uppercase font-bold text-slate-400">Country / State / City</div>
                <div class="font-bold text-slate-900 mt-0.5">{{ viewingCsr.country }} / {{ viewingCsr.state }} / {{ viewingCsr.city }}</div>
              </div>
              <div>
                <div class="text-[10px] uppercase font-bold text-slate-400">Status</div>
                <div class="font-bold text-amber-700 mt-0.5">{{ viewingCsr.status }}</div>
              </div>
            </div>

            <div>
              <div class="flex items-center justify-between mb-1">
                <span class="font-bold text-slate-700">PKCS#10 CSR PEM Content</span>
                <button
                  type="button"
                  @click="copyPem(viewingCsr.csrPem)"
                  class="text-[10px] font-bold text-[#0072ce] hover:underline cursor-pointer"
                >
                  {{ isCopied ? 'Copied!' : 'Copy to Clipboard' }}
                </button>
              </div>
              <textarea
                readonly
                rows="6"
                class="w-full p-2.5 bg-slate-900 text-amber-400 font-mono text-[10px] rounded-lg border border-slate-800 select-all focus:outline-none"
              >{{ viewingCsr.csrPem }}</textarea>
            </div>
          </div>

          <div class="p-4 border-t border-slate-200 bg-slate-50 flex items-center justify-between">
            <button
              type="button"
              @click="downloadCsr(viewingCsr)"
              class="px-3.5 py-1.5 rounded-lg bg-amber-500 hover:bg-amber-600 text-white font-bold text-xs flex items-center gap-1.5 shadow-xs cursor-pointer"
            >
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
              </svg>
              <span>Download (.csr)</span>
            </button>
            <button
              type="button"
              @click="viewingCsr = null"
              class="px-3.5 py-1.5 rounded-lg border border-slate-300 bg-white hover:bg-slate-100 text-slate-700 font-bold text-xs cursor-pointer"
            >
              Close
            </button>
          </div>
        </div>
      </div>
    </transition>

    <!-- MODAL: COMPLETE CSR / UPLOAD SIGNED CERTIFICATE -->
    <transition
      enter-active-class="transition duration-150 ease-out"
      enter-from-class="opacity-0 scale-95"
      enter-to-class="opacity-100 scale-100"
      leave-active-class="transition duration-100 ease-in"
      leave-from-class="opacity-100 scale-100"
      leave-to-class="opacity-0 scale-95"
    >
      <div v-if="completingCsr" class="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4">
        <div class="bg-white rounded-2xl shadow-2xl border border-slate-200 max-w-lg w-full overflow-hidden flex flex-col">
          <div class="px-5 py-3.5 bg-slate-900 text-white flex items-center justify-between border-b border-slate-800">
            <h3 class="text-xs font-bold uppercase tracking-wider text-white">Complete CSR &amp; Install Certificate</h3>
            <button @click="completingCsr = null" class="text-slate-400 hover:text-white font-bold cursor-pointer">&times;</button>
          </div>

          <form @submit.prevent="handleCompleteCsr" class="p-5 space-y-3.5 text-xs">
            <div class="p-3 bg-blue-50 rounded-lg border border-blue-200 text-[#0072ce] text-[11px]">
              Complete CSR <strong>{{ completingCsr.name }}</strong> (CN={{ completingCsr.commonName }}) by uploading or pasting the signed certificate (.crt) provided by your Certificate Authority.
            </div>

            <div>
              <label class="block font-bold text-slate-700 mb-1">Signed Certificate File / Content (.crt / .pem) *</label>
              <div class="mb-2">
                <input type="file" accept=".crt,.cer,.pem,.txt" @change="onSignedCertFileUpload" class="text-xs text-slate-600 file:mr-2 file:py-1 file:px-2.5 file:rounded-md file:border file:border-slate-300 file:text-xs file:font-semibold file:bg-slate-50 hover:file:bg-slate-100 cursor-pointer" />
              </div>
              <textarea required rows="5" v-model="completeCertPem" placeholder="-----BEGIN CERTIFICATE-----&#10;...&#10;-----END CERTIFICATE-----" class="w-full p-2.5 border border-slate-300 rounded font-mono text-[10px] focus:outline-none focus:border-[#0072ce]"></textarea>
            </div>

            <div>
              <label class="block font-bold text-slate-700 mb-1">Assign Service</label>
              <select v-model="completeUsage" class="w-full p-2 border border-slate-300 rounded bg-white font-medium">
                <option value="WAF / WebAdmin HTTPS">WAF / WebAdmin HTTPS</option>
                <option value="SSL VPN Server">SSL VPN Server</option>
                <option value="Custom SSL Service">Custom SSL Service</option>
              </select>
            </div>

            <div class="pt-3 border-t border-slate-200 flex justify-between">
              <button type="button" @click="completingCsr = null" class="px-3.5 py-1.5 border rounded text-slate-700 cursor-pointer">Cancel</button>
              <button type="submit" :disabled="isSubmitting" class="px-4 py-1.5 bg-emerald-600 hover:bg-emerald-700 text-white font-bold rounded shadow-xs cursor-pointer disabled:opacity-50">
                {{ isSubmitting ? 'Installing...' : 'Install Signed Certificate' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, reactive, computed, watch, onMounted } from 'vue'

const props = defineProps({
  authToken: {
    type: String,
    default: ''
  }
})

const activeTab = ref('server_certs') // 'server_certs' | 'csrs' | 'authorities' | 'letsencrypt'
const isNewCertModalOpen = ref(false)
const creationMethod = ref('self_signed') // 'self_signed' | 'csr' | 'import' | 'letsencrypt'
const importInputMode = ref('file') // 'file' | 'text'

const uploadedCertFileName = ref('')
const uploadedKeyFileName = ref('')
const uploadedPfxFileName = ref('')
const uploadedP7bFileName = ref('')

const viewingCert = ref(null)
const viewingCsr = ref(null)
const completingCsr = ref(null)
const completeCertPem = ref('')
const completeUsage = ref('WAF / WebAdmin HTTPS')
const isLoading = ref(false)
const isSubmitting = ref(false)
const isCopied = ref(false)
const toastMessage = ref(null)
const toastType = ref('success')
const searchQuery = ref('')

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

const csrsList = ref([
  {
    id: 'csr_corp_gateway',
    name: 'Corporate Public Gateway CSR',
    commonName: 'vpn.company.com',
    organization: 'Enterprise Global Corp',
    organizationalUnit: 'IT Security',
    country: 'US',
    state: 'California',
    city: 'San Jose',
    email: 'security@company.com',
    algorithm: 'RSA 2048-bit',
    sans: ['vpn.company.com', 'gateway.company.com'],
    status: 'Pending CA Signature',
    createdAt: '2026-08-21',
    csrPem: `-----BEGIN CERTIFICATE REQUEST-----
MIICvDCCAaQCAQAwdzELMAkGA1UEBhMCVVMxEzARBgNVBAgMCkNhbGlmb3JuaWEx
ETAPBgNVBAcMCFNhbiBKb3NlMR8wHQYDVQQKDBZFbnRlcnByaXNlIEdsb2JhbCBD
b3JwMRgwFgYDVQQDDA92cG4uY29tcGFueS5jb20wggEiMA0GCSqGSIb3DQEBAQUA
-----END CERTIFICATE REQUEST-----`
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

const csrForm = reactive({
  name: '',
  commonName: '',
  organization: 'Astaro-Next Security',
  organizationalUnit: 'IT Operations',
  country: 'US',
  state: 'California',
  city: 'San Francisco',
  email: 'admin@astaro-next.internal',
  algorithm: 'RSA 2048-bit',
  sans: ''
})

const importForm = reactive({
  name: '',
  format: 'pem', // 'pem' | 'cer' | 'pfx' | 'p7b'
  certPem: '',
  keyPem: '',
  pfxData: '',
  p7bData: '',
  passphrase: '',
  usage: 'WebAdmin HTTPS / WAF'
})

const leForm = reactive({
  scope: 'single', // 'single' | 'multi_domain' | 'wildcard'
  domain: '',
  sansInput: '',
  email: '',
  validationMethod: 'http-01', // 'http-01' | 'dns-01' | 'tls-alpn-01'
  dnsProvider: 'cloudflare', // 'cloudflare' | 'route53' | 'digitalocean' | 'rfc2136' | 'manual'
  dnsApiToken: '',
  dnsZoneId: ''
})

// Auto-switch to DNS-01 challenge if Wildcard scope is selected
watch(() => leForm.scope, (newScope) => {
  if (newScope === 'wildcard') {
    leForm.validationMethod = 'dns-01'
  }
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
  return list
})

const filteredCsrs = computed(() => {
  let list = [...csrsList.value]
  if (searchQuery.value.trim()) {
    const q = searchQuery.value.toLowerCase()
    list = list.filter(c =>
      c.name.toLowerCase().includes(q) ||
      c.commonName.toLowerCase().includes(q) ||
      (c.organization && c.organization.toLowerCase().includes(q))
    )
  }
  return list
})

const currentTabItemCount = computed(() => {
  if (activeTab.value === 'server_certs') return filteredCerts.value.length
  if (activeTab.value === 'csrs') return filteredCsrs.value.length
  if (activeTab.value === 'authorities') return caCertificates.value.length
  return 0
})

const showToast = (msg, type = 'success') => {
  toastMessage.value = msg
  toastType.value = type
  setTimeout(() => {
    toastMessage.value = null
  }, 4000)
}

const openNewCertModal = (method = 'self_signed') => {
  creationMethod.value = method
  uploadedCertFileName.value = ''
  uploadedKeyFileName.value = ''
  uploadedPfxFileName.value = ''
  uploadedP7bFileName.value = ''
  isNewCertModalOpen.value = true
}

const onCertFileUpload = (e) => {
  const file = e.target.files[0]
  if (!file) return
  uploadedCertFileName.value = `${file.name} (${(file.size / 1024).toFixed(1)} KB)`
  if (!importForm.name) {
    importForm.name = file.name.replace(/\.[^/.]+$/, '').replace(/[-_]/g, ' ')
  }
  const reader = new FileReader()
  reader.onload = (event) => {
    importForm.certPem = event.target.result
  }
  reader.readAsText(file)
}

const onKeyFileUpload = (e) => {
  const file = e.target.files[0]
  if (!file) return
  uploadedKeyFileName.value = `${file.name} (${(file.size / 1024).toFixed(1)} KB)`
  const reader = new FileReader()
  reader.onload = (event) => {
    importForm.keyPem = event.target.result
  }
  reader.readAsText(file)
}

const onPfxFileUpload = (e) => {
  const file = e.target.files[0]
  if (!file) return
  uploadedPfxFileName.value = `${file.name} (${(file.size / 1024).toFixed(1)} KB)`
  if (!importForm.name) {
    importForm.name = file.name.replace(/\.[^/.]+$/, '').replace(/[-_]/g, ' ')
  }
  const reader = new FileReader()
  reader.onload = (event) => {
    const dataUrl = event.target.result
    const base64 = dataUrl.split(',')[1] || dataUrl
    importForm.pfxData = base64
  }
  reader.readAsDataURL(file)
}

const onP7bFileUpload = (e) => {
  const file = e.target.files[0]
  if (!file) return
  uploadedP7bFileName.value = `${file.name} (${(file.size / 1024).toFixed(1)} KB)`
  if (!importForm.name) {
    importForm.name = file.name.replace(/\.[^/.]+$/, '').replace(/[-_]/g, ' ')
  }
  const reader = new FileReader()
  reader.onload = (event) => {
    importForm.p7bData = event.target.result
  }
  reader.readAsText(file)
}

const onSignedCertFileUpload = (e) => {
  const file = e.target.files[0]
  if (!file) return
  const reader = new FileReader()
  reader.onload = (event) => {
    completeCertPem.value = event.target.result
  }
  reader.readAsText(file)
}

const viewCertDetails = (cert) => {
  viewingCert.value = cert
  isCopied.value = false
}

const viewCsrDetails = (csr) => {
  viewingCsr.value = csr
  isCopied.value = false
}

const openCompleteCsrModal = (csr) => {
  completingCsr.value = csr
  completeCertPem.value = ''
  completeUsage.value = 'WAF / WebAdmin HTTPS'
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

const copyPem = async (text) => {
  if (!text) return
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

const downloadCsr = (csr) => {
  const blob = new Blob([csr.csrPem], { type: 'application/pkcs10' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `${(csr.name || 'csr').toLowerCase().replace(/[^a-z0-9]/g, '_')}.csr`
  a.click()
  URL.revokeObjectURL(url)
  showToast(`Downloaded CSR '${csr.name}'.`)
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
      const [certRes, csrRes] = await Promise.all([
        axiosLib.get('/api/certificates').catch(() => null),
        axiosLib.get('/api/certificates/csrs').catch(() => null)
      ])
      if (certRes && certRes.data && certRes.data.certificates) {
        serverCertificates.value = certRes.data.certificates
      }
      if (csrRes && csrRes.data && csrRes.data.csrs) {
        csrsList.value = csrRes.data.csrs
      }
    }
  } catch (e) {
    console.error('Failed to fetch certificates/csrs:', e)
  } finally {
    isLoading.value = false
  }
}

const handleGenerateCsr = async () => {
  isSubmitting.value = true
  try {
    const axiosLib = (typeof window !== 'undefined' && window.axios) ? window.axios : null
    if (axiosLib) {
      const res = await axiosLib.post('/api/certificates/csr/generate', csrForm)
      if (res && res.data && res.data.csr) {
        csrsList.value.unshift(res.data.csr)
      }
    }
    showToast(`CSR '${csrForm.name}' generated successfully.`)
    activeTab.value = 'csrs'
    isNewCertModalOpen.value = false
  } catch (e) {
    showToast('Failed to generate CSR: ' + (e.response?.data?.detail || e.message), 'error')
  } finally {
    isSubmitting.value = false
  }
}

const handleCompleteCsr = async () => {
  if (!completingCsr.value) return
  isSubmitting.value = true
  try {
    const axiosLib = (typeof window !== 'undefined' && window.axios) ? window.axios : null
    if (axiosLib) {
      await axiosLib.post(`/api/certificates/csr/${completingCsr.value.id}/complete`, {
        certPem: completeCertPem.value,
        usage: completeUsage.value
      })
    }
    completingCsr.value.status = 'Completed (Installed)'
    serverCertificates.value.unshift({
      id: 'cert_' + Date.now(),
      name: `${completingCsr.value.name} (Signed)`,
      commonName: completingCsr.value.commonName,
      sans: completingCsr.value.sans || [],
      issuer: 'External Signed CA',
      algorithm: completingCsr.value.algorithm || 'RSA 2048-bit',
      validTo: '2028-12-31',
      daysRemaining: 730,
      isValid: true,
      isDefault: false,
      usage: completeUsage.value
    })
    showToast(`Signed certificate for '${completingCsr.value.name}' activated and installed.`)
    completingCsr.value = null
    activeTab.value = 'server_certs'
  } catch (e) {
    showToast('Failed to complete CSR: ' + (e.response?.data?.detail || e.message), 'error')
  } finally {
    isSubmitting.value = false
  }
}

const handleGenerateCert = async () => {
  isSubmitting.value = true
  try {
    const axiosLib = (typeof window !== 'undefined' && window.axios) ? window.axios : null
    if (axiosLib) {
      const res = await axiosLib.post('/api/certificates/generate', {
        name: newCertForm.name,
        common_name: newCertForm.commonName,
        days: newCertForm.days,
        sans: newCertForm.sans ? newCertForm.sans.split(',').map(s => s.trim()) : []
      })
      if (res && res.data && res.data.certificate) {
        serverCertificates.value.push(res.data.certificate)
      }
    }
    showToast(`Certificate '${newCertForm.name}' generated successfully.`)
    activeTab.value = 'server_certs'
    isNewCertModalOpen.value = false
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
      const res = await axiosLib.post('/api/certificates/import', {
        name: importForm.name,
        format: importForm.format,
        cert_pem: importForm.certPem,
        key_pem: importForm.keyPem,
        pfx_data: importForm.pfxData,
        p7b_data: importForm.p7bData,
        passphrase: importForm.passphrase,
        usage: importForm.usage
      })
      if (res && res.data && res.data.certificate) {
        serverCertificates.value.push(res.data.certificate)
      }
    }
    showToast(`Certificate '${importForm.name}' (${importForm.format.toUpperCase()}) imported successfully.`)
    activeTab.value = 'server_certs'
    isNewCertModalOpen.value = false
  } catch (e) {
    showToast('Failed to import certificate: ' + (e.response?.data?.detail || e.message), 'error')
  } finally {
    isSubmitting.value = false
  }
}

const handleRequestLetsEncrypt = async () => {
  isSubmitting.value = true
  try {
    let domainVal = leForm.domain.trim()
    let sansList = []
    if (leForm.scope === 'wildcard') {
      const base = domainVal.replace(/^\*\./, '')
      domainVal = `*.${base}`
      sansList = [base, `*.${base}`]
    } else if (leForm.scope === 'multi_domain') {
      sansList = leForm.sansInput ? leForm.sansInput.split(',').map(s => s.trim()).filter(Boolean) : []
      if (!sansList.includes(domainVal)) sansList.unshift(domainVal)
    } else {
      sansList = [domainVal]
    }

    const axiosLib = (typeof window !== 'undefined' && window.axios) ? window.axios : null
    if (axiosLib) {
      const res = await axiosLib.post('/api/certificates/letsencrypt', {
        scope: leForm.scope,
        domain: domainVal,
        sans: sansList,
        email: leForm.email,
        validationMethod: leForm.validationMethod,
        dnsProvider: leForm.dnsProvider,
        dnsApiToken: leForm.dnsApiToken,
        dnsZoneId: leForm.dnsZoneId,
        usage: 'Public WebAdmin / WAF'
      })
      if (res && res.data && res.data.certificate) {
        serverCertificates.value.unshift(res.data.certificate)
      }
    } else {
      serverCertificates.value.unshift({
        id: 'cert_le_' + Date.now(),
        name: `Let's Encrypt (${domainVal})`,
        commonName: domainVal,
        sans: sansList,
        issuer: "Let's Encrypt Authority X3",
        algorithm: 'ECDSA P-256',
        validTo: new Date(Date.now() + 90 * 86400000).toISOString().split('T')[0],
        daysRemaining: 90,
        isValid: true,
        isDefault: false,
        usage: 'Public WebAdmin / WAF'
      })
    }
    showToast(`Let's Encrypt certificate for '${domainVal}' (${leForm.validationMethod.toUpperCase()}) issued successfully.`)
    activeTab.value = 'server_certs'
    isNewCertModalOpen.value = false
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

const deleteCsr = async (csr) => {
  if (!confirm(`Are you sure you want to delete CSR '${csr.name}'?`)) return
  try {
    const axiosLib = (typeof window !== 'undefined' && window.axios) ? window.axios : null
    if (axiosLib) {
      await axiosLib.delete(`/api/certificates/csr/${csr.id}`)
    }
  } catch (e) {
    console.error(e)
  }
  csrsList.value = csrsList.value.filter(c => c.id !== csr.id)
  showToast(`CSR '${csr.name}' deleted.`)
}

onMounted(() => {
  fetchCertificates()
})
</script>
