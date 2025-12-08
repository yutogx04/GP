<template>
  <div class="min-h-screen py-8 bg-slate-50 dark:bg-slate-900">
    <div class="container mx-auto px-4">
      <div class="flex justify-between items-center mb-8">
        <div>
          <h1 class="text-3xl font-bold text-slate-900 dark:text-white">Active Internships</h1>
          <p class="text-slate-600 dark:text-slate-400">Manage ongoing internship placements</p>
        </div>
        <div class="flex gap-3">
          <select v-model="statusFilter" class="input-field w-auto">
            <option value="">All Status</option>
            <option value="pending">Pending Start</option>
            <option value="ongoing">Ongoing</option>
            <option value="completed">Completed</option>
          </select>
        </div>
      </div>

      <div v-if="loading" class="flex justify-center py-20">
        <div class="w-10 h-10 border-4 border-sky-200 border-t-sky-600 rounded-full animate-spin"></div>
      </div>

      <div v-else-if="filteredInternships.length === 0" class="card p-12 text-center">
        <div class="text-5xl mb-4">🎓</div>
        <h3 class="text-lg font-semibold text-slate-900 dark:text-white mb-2">No internships found</h3>
        <p class="text-slate-600 dark:text-slate-400">Active internships will appear here when students are accepted for offers</p>
      </div>

      <div v-else class="space-y-4">
        <div v-for="internship in filteredInternships" :key="internship.id" class="card p-6">
          <div class="flex flex-col md:flex-row justify-between gap-4">
            <div class="flex-1">
              <div class="flex items-center gap-3 mb-3">
                <div class="w-12 h-12 bg-gradient-to-br from-sky-400 to-teal-400 rounded-full flex items-center justify-center text-white font-bold">
                  {{ internship.student?.first_name?.[0] }}{{ internship.student?.last_name?.[0] }}
                </div>
                <div>
                  <h3 class="font-semibold text-slate-900 dark:text-white">
                    {{ internship.student?.first_name }} {{ internship.student?.last_name }}
                  </h3>
                  <p class="text-sm text-slate-500">{{ internship.student?.email }}</p>
                </div>
              </div>
              
              <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                <div>
                  <span class="text-slate-500">Offer:</span>
                  <span class="font-medium text-slate-900 dark:text-white"> {{ internship.offer?.title }}</span>
                </div>
                <div>
                  <span class="text-slate-500">Supervisor:</span>
                  <span class="font-medium text-slate-900 dark:text-white"> {{ internship.supervisor?.first_name }} {{ internship.supervisor?.last_name }}</span>
                </div>
                <div>
                  <span class="text-slate-500">Period:</span>
                  <span class="font-medium text-slate-900 dark:text-white"> {{ formatDate(internship.start_date) }} - {{ formatDate(internship.end_date) }}</span>
                </div>
              </div>
            </div>
            
            <div class="flex flex-col items-end gap-3">
              <span :class="getStatusClass(internship.status)" class="px-3 py-1 rounded-full text-sm font-medium">
                {{ getStatusLabel(internship.status) }}
              </span>
              
              <div class="flex gap-2">
                <button 
                  v-if="internship.status === 'pending'" 
                  @click="updateStatus(internship, 'ongoing')"
                  :disabled="updating === internship.id"
                  class="btn btn-sm bg-green-600 hover:bg-green-700 text-white"
                >
                  {{ updating === internship.id ? '...' : '▶ Start' }}
                </button>
                <button 
                  v-if="internship.status === 'ongoing'" 
                  @click="updateStatus(internship, 'completed')"
                  :disabled="updating === internship.id"
                  class="btn btn-sm bg-sky-600 hover:bg-sky-700 text-white"
                >
                  {{ updating === internship.id ? '...' : '✓ Complete' }}
                </button>
                <button 
                  v-if="['pending', 'ongoing'].includes(internship.status)" 
                  @click="updateStatus(internship, 'cancelled')"
                  :disabled="updating === internship.id"
                  class="btn btn-sm btn-outline text-red-600 border-red-300 hover:bg-red-50"
                >
                  Cancel
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '../services/api'
import { useToast } from 'vue-toastification'

const toast = useToast()
const loading = ref(true)
const updating = ref(null)
const internships = ref([])
const statusFilter = ref('')

const filteredInternships = computed(() => {
  if (!Array.isArray(internships.value)) return []
  if (!statusFilter.value) return internships.value
  return internships.value.filter(i => i.status === statusFilter.value)
})

onMounted(loadInternships)

async function loadInternships() {
  loading.value = true
  try {
    // Get all internships for this hospital admin's offers
    const response = await api.get('/internships/supervisor/')
    internships.value = response.data?.results || (Array.isArray(response.data) ? response.data : [])
  } catch (error) {
    console.error('Failed to load internships:', error)
    internships.value = []
  } finally {
    loading.value = false
  }
}

async function updateStatus(internship, newStatus) {
  if (!confirm(`Are you sure you want to ${newStatus === 'cancelled' ? 'cancel' : newStatus} this internship?`)) return
  
  updating.value = internship.id
  try {
    await api.patch(`/internships/placement/${internship.id}/status/`, { status: newStatus })
    internship.status = newStatus
    toast.success(`Internship ${newStatus === 'completed' ? 'marked as completed' : newStatus}`)
    
    if (newStatus === 'completed') {
      toast.info('Evaluation form is now available for the supervisor')
    }
  } catch (error) {
    const detail = error.response?.data?.detail || 'Failed to update status'
    toast.error(detail)
  } finally {
    updating.value = null
  }
}

function formatDate(date) {
  if (!date) return 'N/A'
  return new Date(date).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
}

const getStatusClass = (status) => ({
  pending: 'bg-amber-100 text-amber-800 dark:bg-amber-900/30 dark:text-amber-400',
  ongoing: 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400',
  completed: 'bg-sky-100 text-sky-800 dark:bg-sky-900/30 dark:text-sky-400',
  cancelled: 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400'
}[status] || 'bg-slate-100 text-slate-800')

const getStatusLabel = (status) => ({
  pending: 'Pending Start',
  ongoing: 'Ongoing',
  completed: 'Completed',
  cancelled: 'Cancelled'
}[status] || status)
</script>
