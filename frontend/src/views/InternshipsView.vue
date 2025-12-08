<template>
  <div class="min-h-screen py-8 bg-slate-50 dark:bg-slate-900">
    <div class="container mx-auto px-4">
      <!-- Header -->
      <div class="mb-8 text-center md:text-left">
        <h1 class="text-3xl font-bold text-slate-900 dark:text-white mb-2">Browse Internships</h1>
        <p class="text-slate-600 dark:text-slate-400">Find the perfect medical internship opportunity</p>
      </div>

      <div class="flex flex-col lg:flex-row gap-8">
        <!-- Filters Sidebar -->
        <div class="lg:w-1/4">
          <div class="card p-6 sticky top-24">
            <div class="flex items-center justify-between mb-6">
              <h3 class="font-semibold text-slate-900 dark:text-white">Filters</h3>
              <button @click="clearFilters" class="text-sm text-sky-600 hover:text-sky-700 font-medium">Reset</button>
            </div>
            
            <div class="space-y-5">
              <div>
                <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">Search</label>
                <input v-model="filters.search" type="search" placeholder="Keywords..." class="input-field">
              </div>
              
              <div>
                <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">Hospital</label>
                <select v-model="filters.hospital" class="input-field">
                  <option value="">All Hospitals</option>
                  <option v-for="h in hospitals" :key="h.id" :value="h.id">{{ h.name }}</option>
                </select>
              </div>
              
              <div>
                <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">Department</label>
                <select v-model="filters.department" class="input-field">
                  <option value="">All Departments</option>
                  <option v-for="d in departments" :key="d.id" :value="d.id">{{ d.name }}</option>
                </select>
              </div>
              
              <div>
                <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">Specialty</label>
                <select v-model="filters.specialty" class="input-field">
                  <option value="">All Specialties</option>
                  <option value="general_medicine">General Medicine</option>
                  <option value="surgery">Surgery</option>
                  <option value="pediatrics">Pediatrics</option>
                  <option value="cardiology">Cardiology</option>
                  <option value="neurology">Neurology</option>
                </select>
              </div>
              
              <div>
                <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">Availability</label>
                <select v-model="filters.status" class="input-field">
                  <option value="">All</option>
                  <option value="open">Open Only</option>
                  <option value="closed">Closed</option>
                </select>
              </div>
            </div>
          </div>
        </div>

        <!-- Results -->
        <div class="lg:w-3/4">
          <div class="flex items-center justify-between mb-6">
            <p class="text-slate-600 dark:text-slate-400">
              <span class="font-semibold text-slate-900 dark:text-white">{{ filteredOffers.length }}</span> internships found
            </p>
            <select v-model="sortBy" class="input-field w-auto py-2">
              <option value="newest">Newest First</option>
              <option value="deadline">Deadline Soon</option>
              <option value="title">Alphabetical</option>
            </select>
          </div>

          <!-- Loading -->
          <div v-if="loading" class="flex justify-center py-20">
            <div class="w-10 h-10 border-4 border-sky-200 border-t-sky-600 rounded-full animate-spin"></div>
          </div>

          <!-- Empty State -->
          <div v-else-if="filteredOffers.length === 0" class="card p-12 text-center flex flex-col items-center">
            <MagnifyingGlassIcon class="w-16 h-16 text-slate-300 dark:text-slate-600 mb-4" />
            <h3 class="text-lg font-semibold text-slate-900 dark:text-white mb-2">No internships found</h3>
            <p class="text-slate-600 dark:text-slate-400 mb-6">Try adjusting your filters</p>
            <button @click="clearFilters" class="btn btn-primary">Clear Filters</button>
          </div>

          <!-- Grid -->
          <div v-else class="grid md:grid-cols-2 gap-6">
            <div v-for="offer in sortedOffers" :key="offer.id" class="card p-6 hover:border-sky-500/50 transition-all group">
              <div class="flex justify-between items-start mb-3">
                <h3 class="text-lg font-bold text-slate-900 dark:text-white group-hover:text-sky-600 transition-colors line-clamp-1">
                  {{ offer.title }}
                </h3>
                <span :class="offer.status === 'open' ? 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400' : 'bg-slate-100 text-slate-600'" class="px-2 py-0.5 rounded-full text-xs font-medium">
                  {{ offer.status }}
                </span>
              </div>
              
              <p class="text-sm text-slate-600 dark:text-slate-400 mb-4 line-clamp-2">{{ offer.description }}</p>
              
              <div class="space-y-2 mb-4 text-sm">
                <div class="flex items-center gap-2 text-slate-600 dark:text-slate-400">
                  <BuildingOffice2Icon class="w-5 h-5" />
                  <span class="font-medium">{{ offer.hospital_name }}</span>
                </div>
                <div class="flex items-center gap-2 text-slate-600 dark:text-slate-400">
                  <ClipboardDocumentListIcon class="w-5 h-5" />
                  <span>{{ offer.department_name }}</span>
                </div>
                <div class="flex items-center gap-2 text-slate-600 dark:text-slate-400">
                  <CalendarIcon class="w-5 h-5" />
                  <span>{{ formatDate(offer.start_date) }} - {{ formatDate(offer.end_date) }}</span>
                </div>
                <div class="flex items-center gap-2 text-slate-600 dark:text-slate-400">
                  <UserGroupIcon class="w-5 h-5" />
                  <span>{{ offer.available_slots }} slots available</span>
                </div>
              </div>
              
              <div class="flex gap-3 pt-4 border-t border-slate-100 dark:border-slate-700">
                <router-link :to="`/internships/${offer.id}`" class="btn btn-outline btn-sm flex-1 text-center">
                  View Details
                </router-link>
                <button v-if="auth.isStudent && offer.status === 'open'" @click="applyTo(offer)" class="btn btn-primary btn-sm flex-1" :disabled="hasApplied(offer.id)">
                  {{ hasApplied(offer.id) ? 'Applied ✓' : 'Apply Now' }}
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
import { useAuthStore } from '../stores/auth'
import api from '../services/api'
import { useToast } from 'vue-toastification'
import { MagnifyingGlassIcon, BuildingOffice2Icon, ClipboardDocumentListIcon, CalendarIcon, UserGroupIcon } from '@heroicons/vue/24/outline'

const auth = useAuthStore()
const toast = useToast()

const loading = ref(true)
const offers = ref([])
const hospitals = ref([])
const departments = ref([])
const userApplications = ref([])
const sortBy = ref('newest')

const filters = ref({
  search: '',
  hospital: '',
  department: '',
  specialty: '',
  status: ''
})

onMounted(async () => {
  try {
    const [offersRes, hospitalsRes, deptsRes] = await Promise.all([
      api.get('/internships/'),
      api.get('/hospitals/'),
      api.get('/departments/')
    ])
    
    offers.value = offersRes.data?.results || (Array.isArray(offersRes.data) ? offersRes.data : [])
    hospitals.value = hospitalsRes.data?.results || (Array.isArray(hospitalsRes.data) ? hospitalsRes.data : [])
    departments.value = deptsRes.data?.results || (Array.isArray(deptsRes.data) ? deptsRes.data : [])
    
    console.log('Loaded offers:', offers.value)
    
    if (auth.isLoggedIn && auth.isStudent) {
      const appsRes = await api.get('/applications/')
      userApplications.value = appsRes.data?.results || (Array.isArray(appsRes.data) ? appsRes.data : [])
    }
  } catch (error) {
    console.error('Failed to load internships:', error)
    toast.error('Failed to load internships')
  } finally {
    loading.value = false
  }
})

const filteredOffers = computed(() => {
  if (!Array.isArray(offers.value)) return []
  return offers.value.filter(offer => {
    if (filters.value.search && !offer.title.toLowerCase().includes(filters.value.search.toLowerCase()) && 
        !offer.description.toLowerCase().includes(filters.value.search.toLowerCase())) return false
    if (filters.value.hospital && offer.hospital !== filters.value.hospital) return false
    if (filters.value.department && offer.department !== filters.value.department) return false
    if (filters.value.status && offer.status !== filters.value.status) return false
    return true
  })
})

const sortedOffers = computed(() => {
  const sorted = [...filteredOffers.value]
  if (sortBy.value === 'newest') {
    sorted.sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
  } else if (sortBy.value === 'deadline') {
    sorted.sort((a, b) => new Date(a.application_deadline) - new Date(b.application_deadline))
  } else {
    sorted.sort((a, b) => a.title.localeCompare(b.title))
  }
  return sorted
})

const hasApplied = (offerId) => {
  return userApplications.value.some(app => app.offer?.id === offerId)
}

const applyTo = async (offer) => {
  if (!auth.isLoggedIn) {
    toast.warning('Please log in to apply')
    return
  }
  
  try {
    await api.post('/applications/', { offer: offer.id })
    userApplications.value.push({ offer: { id: offer.id } })
    toast.success('Application submitted!')
  } catch (error) {
    toast.error(error.response?.data?.detail || 'Failed to apply')
  }
}

const clearFilters = () => {
  filters.value = { search: '', hospital: '', department: '', specialty: '', status: '' }
}

const formatDate = (date) => {
  if (!date) return 'N/A'
  return new Date(date).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
}
</script>
