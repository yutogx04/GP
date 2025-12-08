<template>
  <div class="min-h-screen py-8 bg-slate-50 dark:bg-slate-900">
    <div class="container mx-auto px-4">
      <div class="flex justify-between items-center mb-8">
        <div>
          <h1 class="text-3xl font-bold text-slate-900 dark:text-white">Applications</h1>
          <p class="text-slate-600 dark:text-slate-400">Review and manage internship applications</p>
        </div>
        <div class="flex gap-3">
          <select v-model="statusFilter" class="input-field w-auto">
            <option value="">All Status</option>
            <option value="pending">Pending</option>
            <option value="accepted">Accepted</option>
            <option value="rejected">Rejected</option>
          </select>
        </div>
      </div>

      <div v-if="loading" class="flex justify-center py-20">
        <div class="w-10 h-10 border-4 border-sky-200 border-t-sky-600 rounded-full animate-spin"></div>
      </div>

      <div v-else-if="filteredApplications.length === 0" class="card p-12 text-center">
        <div class="text-5xl mb-4">📋</div>
        <h3 class="text-lg font-semibold text-slate-900 dark:text-white mb-2">No applications found</h3>
        <p class="text-slate-600 dark:text-slate-400">Applications to your internship offers will appear here</p>
      </div>

      <div v-else class="space-y-4">
        <div v-for="app in filteredApplications" :key="app.id" class="card p-6">
          <div class="flex flex-col md:flex-row justify-between gap-4">
            <div class="flex-1">
              <div class="flex items-center gap-3 mb-2">
                <div class="w-10 h-10 bg-sky-100 dark:bg-sky-900/30 rounded-full flex items-center justify-center text-sky-600 font-bold">
                  {{ app.student?.first_name?.[0] }}{{ app.student?.last_name?.[0] }}
                </div>
                <div>
                  <h3 class="font-semibold text-slate-900 dark:text-white">{{ app.student?.first_name }} {{ app.student?.last_name }}</h3>
                  <p class="text-sm text-slate-500">{{ app.student?.email }}</p>
                </div>
              </div>
              <div class="mt-3 flex flex-wrap gap-4 text-sm text-slate-600 dark:text-slate-400">
                <span>📋 {{ app.offer?.title }}</span>
                <span>📅 Applied {{ formatDate(app.applied_at) }}</span>
                <span>🎓 {{ app.student_profile?.niveau_etude }}</span>
              </div>
            </div>
            
            <div class="flex items-center gap-3">
              <span :class="getStatusClass(app.status)" class="px-3 py-1 rounded-full text-sm font-medium">
                {{ app.status }}
              </span>
              <div v-if="app.status === 'pending'" class="flex gap-2">
                <button @click="openAcceptModal(app)" class="btn btn-sm bg-green-600 hover:bg-green-700 text-white">
                  Accept
                </button>
                <button @click="rejectApplication(app.id)" class="btn btn-sm bg-red-600 hover:bg-red-700 text-white">
                  Reject
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Accept Application Modal with Supervisor Selection -->
    <div v-if="showAcceptModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div class="bg-white dark:bg-slate-800 rounded-2xl shadow-xl max-w-md w-full">
        <div class="p-6 border-b border-slate-200 dark:border-slate-700">
          <h3 class="text-xl font-bold text-slate-900 dark:text-white">Accept Application</h3>
          <p class="text-slate-600 dark:text-slate-400 mt-1">
            Accept {{ selectedApplication?.student?.first_name }} {{ selectedApplication?.student?.last_name }} for 
            <span class="font-medium">{{ selectedApplication?.offer?.title }}</span>
          </p>
        </div>
        
        <div class="p-6">
          <div class="mb-6">
            <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">
              Assign Supervisor (Encadrant) *
            </label>
            <select 
              v-model="selectedSupervisorId" 
              class="input-field"
              :class="{ 'border-red-500': supervisorError }"
            >
              <option value="">Select a supervisor...</option>
              <option v-for="sup in supervisors" :key="sup.id" :value="sup.id">
                {{ sup.first_name }} {{ sup.last_name }} - {{ sup.email }}
              </option>
            </select>
            <p v-if="supervisorError" class="text-red-500 text-sm mt-1">{{ supervisorError }}</p>
            <p v-if="supervisors.length === 0 && !loadingSupervisors" class="text-amber-500 text-sm mt-1">
              No supervisors available. Please create an encadrant account first.
            </p>
          </div>
          
          <div class="bg-sky-50 dark:bg-sky-900/20 rounded-lg p-4 mb-6">
            <h4 class="font-medium text-slate-900 dark:text-white mb-2">What happens next:</h4>
            <ul class="text-sm text-slate-600 dark:text-slate-400 space-y-1">
              <li>✅ An internship record will be created</li>
              <li>✅ The supervisor will see this student in their dashboard</li>
              <li>✅ The student will be notified of acceptance</li>
            </ul>
          </div>
          
          <div class="flex gap-3">
            <button @click="closeAcceptModal" class="btn btn-outline flex-1">
              Cancel
            </button>
            <button 
              @click="confirmAccept" 
              :disabled="!selectedSupervisorId || accepting"
              class="btn btn-primary flex-1"
            >
              {{ accepting ? 'Processing...' : 'Accept & Assign' }}
            </button>
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
const loadingSupervisors = ref(false)
const applications = ref([])
const supervisors = ref([])
const statusFilter = ref('')

// Accept modal state
const showAcceptModal = ref(false)
const selectedApplication = ref(null)
const selectedSupervisorId = ref('')
const supervisorError = ref('')
const accepting = ref(false)

const filteredApplications = computed(() => {
  if (!Array.isArray(applications.value)) return []
  if (!statusFilter.value) return applications.value
  return applications.value.filter(a => a.status === statusFilter.value)
})

onMounted(async () => {
  await Promise.all([loadApplications(), loadSupervisors()])
})

async function loadApplications() {
  loading.value = true
  try {
    const response = await api.get('/applications/hospital/')
    applications.value = response.data?.results || (Array.isArray(response.data) ? response.data : [])
  } catch (error) {
    console.error('Failed to load applications:', error)
    applications.value = []
  } finally {
    loading.value = false
  }
}

async function loadSupervisors() {
  loadingSupervisors.value = true
  try {
    // Get all encadrants from staff list
    const response = await api.get('/users/staff/')
    const allStaff = response.data?.results || (Array.isArray(response.data) ? response.data : [])
    supervisors.value = allStaff.filter(s => s.role === 'encadrant')
  } catch (error) {
    console.error('Failed to load supervisors:', error)
    supervisors.value = []
  } finally {
    loadingSupervisors.value = false
  }
}

function openAcceptModal(app) {
  selectedApplication.value = app
  selectedSupervisorId.value = ''
  supervisorError.value = ''
  showAcceptModal.value = true
}

function closeAcceptModal() {
  showAcceptModal.value = false
  selectedApplication.value = null
  selectedSupervisorId.value = ''
  supervisorError.value = ''
}

async function confirmAccept() {
  if (!selectedSupervisorId.value) {
    supervisorError.value = 'Please select a supervisor'
    return
  }
  
  accepting.value = true
  supervisorError.value = ''
  
  try {
    const response = await api.post(`/applications/${selectedApplication.value.id}/accept/`, {
      supervisor_id: selectedSupervisorId.value
    })
    
    // Update local state
    const app = applications.value.find(a => a.id === selectedApplication.value.id)
    if (app) app.status = 'accepted'
    
    toast.success(`Application accepted! Internship created for ${selectedApplication.value.student?.first_name}`)
    closeAcceptModal()
  } catch (error) {
    console.error('Accept failed:', error)
    supervisorError.value = error.response?.data?.detail || 'Failed to accept application'
    toast.error(supervisorError.value)
  } finally {
    accepting.value = false
  }
}

async function rejectApplication(id) {
  if (!confirm('Are you sure you want to reject this application?')) return
  
  try {
    await api.patch(`/applications/${id}/update/`, { status: 'rejected' })
    const app = applications.value.find(a => a.id === id)
    if (app) app.status = 'rejected'
    toast.success('Application rejected')
  } catch (error) {
    toast.error('Failed to reject application')
  }
}

const getStatusClass = (status) => ({
  pending: 'bg-amber-100 text-amber-800 dark:bg-amber-900/30 dark:text-amber-400',
  accepted: 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400',
  rejected: 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400'
}[status] || 'bg-slate-100 text-slate-800')

const formatDate = (date) => date ? new Date(date).toLocaleDateString() : 'N/A'
</script>
