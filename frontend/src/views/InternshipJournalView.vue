<template>
  <div class="min-h-screen py-8 bg-slate-50 dark:bg-slate-900">
    <div class="container mx-auto px-4 max-w-4xl">
      <!-- Header -->
      <div class="flex justify-between items-center mb-8">
        <div>
          <h1 class="text-3xl font-bold text-slate-900 dark:text-white">Internship Journal</h1>
          <p class="text-slate-600 dark:text-slate-400" v-if="internship">
            {{ internship.offer?.title }} - {{ internship.supervisor?.first_name }} {{ internship.supervisor?.last_name }}
          </p>
        </div>
        <button @click="showAddEntry = true" class="btn btn-primary">
          <PlusIcon class="w-5 h-5 mr-1" /> Add Entry
        </button>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="flex justify-center py-20">
        <div class="w-10 h-10 border-4 border-sky-200 border-t-sky-600 rounded-full animate-spin"></div>
      </div>

      <!-- No Internship -->
      <div v-else-if="!internship" class="card p-12 text-center flex flex-col items-center">
        <ClipboardDocumentListIcon class="w-16 h-16 text-slate-300 dark:text-slate-600 mb-4" />
        <h3 class="text-lg font-semibold text-slate-900 dark:text-white mb-2">No active internship</h3>
        <p class="text-slate-600 dark:text-slate-400 mb-6">Your internship journal will appear here once you start an internship</p>
        <router-link to="/internships" class="btn btn-primary">Browse Internships</router-link>
      </div>

      <!-- Journal Entries -->
      <div v-else>
        <!-- Internship Status Banner -->
        <div class="card p-4 mb-6 flex items-center justify-between">
          <div class="flex items-center gap-3">
            <span :class="getStatusClass(internship.status)" class="px-3 py-1 rounded-full text-sm font-medium">
              {{ internship.status }}
            </span>
            <span class="text-slate-600 dark:text-slate-400">
              {{ formatDate(internship.start_date) }} - {{ formatDate(internship.end_date) }}
            </span>
          </div>
        </div>

        <!-- Empty State -->
        <div v-if="entries.length === 0" class="card p-12 text-center flex flex-col items-center">
          <DocumentTextIcon class="w-16 h-16 text-slate-300 dark:text-slate-600 mb-4" />
          <h3 class="text-lg font-semibold text-slate-900 dark:text-white mb-2">No journal entries yet</h3>
          <p class="text-slate-600 dark:text-slate-400 mb-6">Start documenting your internship experience</p>
          <button @click="showAddEntry = true" class="btn btn-primary">Add First Entry</button>
        </div>

        <!-- Entries List -->
        <div v-else class="space-y-6">
          <div v-for="entry in entries" :key="entry.id" class="card p-6">
            <div class="flex justify-between items-start mb-4">
              <div>
                <div class="text-lg font-semibold text-slate-900 dark:text-white">
                  {{ formatDate(entry.date) }}
                </div>
                <div class="text-sm text-slate-500">
                  {{ getDayOfWeek(entry.date) }}
                </div>
              </div>
              <button @click="editEntry(entry)" class="text-sky-600 hover:text-sky-700 text-sm">
                Edit
              </button>
            </div>
            
            <div class="space-y-4">
              <div>
                <h4 class="text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Activities</h4>
                <p class="text-slate-600 dark:text-slate-400 whitespace-pre-line">{{ entry.activities || 'No activities recorded' }}</p>
              </div>
              
              <div v-if="entry.skills_practiced?.length > 0">
                <h4 class="text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Skills Practiced</h4>
                <div class="flex flex-wrap gap-2">
                  <span v-for="skill in entry.skills_practiced" :key="skill" 
                    class="px-2 py-1 bg-sky-100 dark:bg-sky-900/30 text-sky-700 dark:text-sky-300 rounded text-sm">
                    {{ skill }}
                  </span>
                </div>
              </div>
              
              <div v-if="entry.challenges">
                <h4 class="text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Challenges</h4>
                <p class="text-slate-600 dark:text-slate-400">{{ entry.challenges }}</p>
              </div>
              
              <div v-if="entry.supervisor_comments" class="bg-amber-50 dark:bg-amber-900/20 rounded-lg p-4 mt-4">
                <h4 class="text-sm font-medium text-amber-800 dark:text-amber-300 mb-1">Supervisor Comments</h4>
                <p class="text-amber-700 dark:text-amber-400">{{ entry.supervisor_comments }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Add/Edit Entry Modal -->
    <div v-if="showAddEntry" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div class="bg-white dark:bg-slate-800 rounded-2xl shadow-xl max-w-lg w-full max-h-[90vh] overflow-y-auto">
        <div class="p-6 border-b border-slate-200 dark:border-slate-700">
          <h3 class="text-xl font-bold text-slate-900 dark:text-white">
            {{ editingEntry ? 'Edit Entry' : 'Add Journal Entry' }}
          </h3>
        </div>
        
        <form @submit.prevent="saveEntry" class="p-6 space-y-4">
          <div>
            <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Date *</label>
            <input v-model="entryForm.date" type="date" class="input-field" required>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Activities *</label>
            <textarea v-model="entryForm.activities" class="input-field" rows="4" 
              placeholder="What did you work on today?" required></textarea>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Skills Practiced</label>
            <input v-model="skillsInput" type="text" class="input-field" 
              placeholder="Enter skills separated by commas">
            <p class="text-xs text-slate-500 mt-1">e.g., Patient care, ECG reading, Documentation</p>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Challenges</label>
            <textarea v-model="entryForm.challenges" class="input-field" rows="2" 
              placeholder="Any difficulties or challenges you faced?"></textarea>
          </div>
          
          <div class="flex gap-3 pt-4">
            <button type="button" @click="closeModal" class="btn btn-outline flex-1">Cancel</button>
            <button type="submit" :disabled="saving" class="btn btn-primary flex-1">
              {{ saving ? 'Saving...' : 'Save Entry' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import api from '../services/api'
import { useToast } from 'vue-toastification'
import { ClipboardDocumentListIcon, DocumentTextIcon, PlusIcon } from '@heroicons/vue/24/outline'

const toast = useToast()
const loading = ref(true)
const saving = ref(false)
const internship = ref(null)
const entries = ref([])
const showAddEntry = ref(false)
const editingEntry = ref(null)
const skillsInput = ref('')

const entryForm = ref({
  date: new Date().toISOString().split('T')[0],
  activities: '',
  skills_practiced: [],
  challenges: ''
})

onMounted(async () => {
  await loadInternship()
})

async function loadInternship() {
  loading.value = true
  try {
    const response = await api.get('/internships/my-internships/')
    const internships = response.data?.results || (Array.isArray(response.data) ? response.data : [])
    
    // Get first active internship
    internship.value = internships.find(i => i.status !== 'completed' && i.status !== 'cancelled') || internships[0]
    
    if (internship.value) {
      await loadEntries()
    }
  } catch (error) {
    console.error('Failed to load internship:', error)
  } finally {
    loading.value = false
  }
}

async function loadEntries() {
  if (!internship.value) return
  try {
    const response = await api.get(`/internships/placement/${internship.value.id}/journal/`)
    entries.value = response.data?.results || (Array.isArray(response.data) ? response.data : [])
  } catch (error) {
    console.error('Failed to load journal entries:', error)
    entries.value = []
  }
}

function editEntry(entry) {
  editingEntry.value = entry
  entryForm.value = {
    date: entry.date,
    activities: entry.activities,
    skills_practiced: entry.skills_practiced || [],
    challenges: entry.challenges || ''
  }
  skillsInput.value = (entry.skills_practiced || []).join(', ')
  showAddEntry.value = true
}

function closeModal() {
  showAddEntry.value = false
  editingEntry.value = null
  entryForm.value = {
    date: new Date().toISOString().split('T')[0],
    activities: '',
    skills_practiced: [],
    challenges: ''
  }
  skillsInput.value = ''
}

async function saveEntry() {
  saving.value = true
  
  // Parse skills from comma-separated input
  const skills = skillsInput.value.split(',').map(s => s.trim()).filter(s => s)
  
  const payload = {
    ...entryForm.value,
    skills_practiced: skills
  }
  
  try {
    if (editingEntry.value) {
      await api.patch(`/internships/placement/${internship.value.id}/journal/${editingEntry.value.id}/`, payload)
      toast.success('Entry updated')
    } else {
      await api.post(`/internships/placement/${internship.value.id}/journal/`, payload)
      toast.success('Entry added')
    }
    await loadEntries()
    closeModal()
  } catch (error) {
    console.error('Save failed:', error)
    toast.error(error.response?.data?.detail || 'Failed to save entry')
  } finally {
    saving.value = false
  }
}

function formatDate(date) {
  if (!date) return 'N/A'
  return new Date(date).toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' })
}

function getDayOfWeek(date) {
  if (!date) return ''
  return new Date(date).toLocaleDateString('en-US', { weekday: 'long' })
}

const getStatusClass = (status) => ({
  pending: 'bg-amber-100 text-amber-800 dark:bg-amber-900/30 dark:text-amber-400',
  ongoing: 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400',
  completed: 'bg-sky-100 text-sky-800 dark:bg-sky-900/30 dark:text-sky-400',
  cancelled: 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400'
}[status] || 'bg-slate-100 text-slate-800')
</script>
