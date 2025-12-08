<template>
  <div class="applications-view">
    <div class="container mx-auto px-4 py-8">
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-slate-900 dark:text-white">My Applications</h1>
        <p class="text-slate-600 dark:text-slate-400 mt-2">Track and manage your internship applications</p>
      </div>

      <div class="applications-content">
        <!-- Loading State -->
        <div v-if="loading" class="flex flex-col items-center justify-center py-20">
          <div class="w-10 h-10 border-4 border-sky-200 border-t-sky-600 rounded-full animate-spin mb-4"></div>
          <p class="text-slate-500 dark:text-slate-400">Loading your applications...</p>
        </div>

        <!-- Empty State -->
        <div v-else-if="!Array.isArray(applications) || applications.length === 0" class="text-center py-16 bg-white dark:bg-slate-800 rounded-2xl border border-slate-200 dark:border-slate-700">
          <div class="text-4xl mb-4">📝</div>
          <h3 class="text-xl font-semibold text-slate-900 dark:text-white mb-2">No applications yet</h3>
          <p class="text-slate-600 dark:text-slate-400 mb-6">Start applying to internship opportunities to see them here</p>
          <router-link to="/internships" class="btn btn-primary">Browse Internships</router-link>
        </div>

        <!-- Applications List -->
        <div v-else class="grid gap-6">
          <div v-for="application in applications" :key="application.id" class="card p-6">
            <div class="flex flex-col md:flex-row justify-between gap-6">
              <div class="flex-1">
                <div class="flex items-start justify-between mb-4">
                  <h3 class="text-xl font-bold text-slate-900 dark:text-white">{{ application.offer?.title || 'Untitled Offer' }}</h3>
                  <span :class="`px-3 py-1 rounded-full text-sm font-medium ${getStatusClass(application.status)}`">
                    {{ getStatusDisplay(application.status) }}
                  </span>
                </div>
                
                <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-4">
                  <div class="flex items-center gap-2 text-slate-600 dark:text-slate-400">
                    <span class="text-lg">🏥</span>
                    <span class="font-medium">{{ application.offer?.hospital_name || 'N/A' }}</span>
                  </div>
                  <div class="flex items-center gap-2 text-slate-600 dark:text-slate-400">
                    <span class="text-lg">📋</span>
                    <span>{{ application.offer?.department_name || 'N/A' }}</span>
                  </div>
                  <div class="flex items-center gap-2 text-slate-600 dark:text-slate-400">
                    <span class="text-lg">📅</span>
                    <span>{{ formatDate(application.offer?.start_date) }} - {{ formatDate(application.offer?.end_date) }}</span>
                  </div>
                </div>

                <div class="flex items-center gap-4 text-sm text-slate-500">
                  <span>Applied on {{ formatDateTime(application.applied_at) }}</span>
                  <span>ID: #{{ application.id }}</span>
                </div>
              </div>

              <div class="flex md:flex-col gap-3 justify-center md:justify-start min-w-[140px]">
                <router-link :to="`/internships/${application.offer?.id}`" class="btn btn-outline text-center">View Offer</router-link>
                <button 
                  v-if="application.status === 'pending'" 
                  @click="withdrawApplication(application.id)"
                  class="btn bg-red-600 hover:bg-red-700 text-white text-center"
                  :disabled="withdrawing === application.id"
                >
                  {{ withdrawing === application.id ? 'Withdrawing...' : 'Withdraw' }}
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Application Stats -->
        <div v-if="Array.isArray(applications) && applications.length > 0" class="mt-12">
          <h3 class="text-lg font-semibold text-slate-900 dark:text-white mb-6">Application Overview</h3>
          <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div class="card p-4 text-center">
              <div class="text-3xl font-bold text-slate-900 dark:text-white mb-1">{{ applications.length }}</div>
              <div class="text-sm text-slate-500">Total Applications</div>
            </div>
            <div class="card p-4 text-center">
              <div class="text-3xl font-bold text-amber-500 mb-1">{{ pendingApplications.length }}</div>
              <div class="text-sm text-slate-500">Pending Review</div>
            </div>
            <div class="card p-4 text-center">
              <div class="text-3xl font-bold text-green-500 mb-1">{{ acceptedApplications.length }}</div>
              <div class="text-sm text-slate-500">Accepted</div>
            </div>
            <div class="card p-4 text-center">
              <div class="text-3xl font-bold text-red-500 mb-1">{{ rejectedApplications.length }}</div>
              <div class="text-sm text-slate-500">Not Selected</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import api from '../services/api'
import { useToast } from 'vue-toastification'

const toast = useToast()
const applications = ref([])
const loading = ref(true)
const withdrawing = ref(null)

const pendingApplications = computed(() => {
  if (!Array.isArray(applications.value)) return []
  return applications.value.filter(a => a.status === 'pending')
})

const acceptedApplications = computed(() => {
  if (!Array.isArray(applications.value)) return []
  return applications.value.filter(a => a.status === 'accepted')
})

const rejectedApplications = computed(() => {
  if (!Array.isArray(applications.value)) return []
  return applications.value.filter(a => a.status === 'rejected')
})

onMounted(loadApplications)

async function loadApplications() {
  loading.value = true
  try {
    const response = await api.get('/applications/')
    // Handle both paginated and non-paginated responses
    const data = response.data
    applications.value = data?.results || (Array.isArray(data) ? data : [])
    console.log('Loaded applications:', applications.value)
  } catch (error) {
    console.error('Failed to load applications:', error)
    toast.error('Failed to load your applications')
    applications.value = []
  } finally {
    loading.value = false
  }
}

async function withdrawApplication(id) {
  if (!confirm('Are you sure you want to withdraw this application?')) return
  withdrawing.value = id
  try {
    await api.post(`/applications/${id}/withdraw/`)
    toast.success('Application withdrawn successfully')
    await loadApplications()
  } catch (error) {
    console.error('Withdraw failed:', error)
    toast.error('Failed to withdraw application')
  } finally {
    withdrawing.value = null
  }
}

function formatDate(dateString) {
  if (!dateString) return 'N/A'
  return new Date(dateString).toLocaleDateString()
}

function formatDateTime(dateString) {
  if (!dateString) return 'N/A'
  return new Date(dateString).toLocaleDateString('en-US', {
    month: 'short', day: 'numeric', year: 'numeric', hour: '2-digit', minute: '2-digit'
  })
}

function getStatusDisplay(status) {
  const map = { pending: 'Pending Review', accepted: 'Accepted', rejected: 'Not Selected', withdrawn: 'Withdrawn' }
  return map[status] || status
}

function getStatusClass(status) {
  const map = {
    pending: 'bg-amber-100 text-amber-800 dark:bg-amber-900/30 dark:text-amber-400',
    accepted: 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400',
    rejected: 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400',
    withdrawn: 'bg-slate-100 text-slate-800 dark:bg-slate-700 dark:text-slate-300'
  }
  return map[status] || 'bg-slate-100 text-slate-800'
}
</script>