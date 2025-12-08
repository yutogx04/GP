<template>
  <div class="min-h-screen py-8 bg-slate-50 dark:bg-slate-900">
    <div class="container mx-auto px-4">
      <h1 class="text-3xl font-bold text-slate-900 dark:text-white mb-2">Validate Offers</h1>
      <p class="text-slate-600 dark:text-slate-400 mb-8">Review and approve internship offers from hospitals</p>

      <div class="flex gap-4 mb-6">
        <button @click="filter = 'pending'" :class="filter === 'pending' ? 'btn-primary' : 'btn-outline'" class="btn">
          Pending ({{ pendingOffers.length }})
        </button>
        <button @click="filter = 'approved'" :class="filter === 'approved' ? 'btn-primary' : 'btn-outline'" class="btn">
          Approved
        </button>
        <button @click="filter = 'rejected'" :class="filter === 'rejected' ? 'btn-primary' : 'btn-outline'" class="btn">
          Rejected
        </button>
      </div>

      <div v-if="loading" class="flex justify-center py-20">
        <div class="w-10 h-10 border-4 border-sky-200 border-t-sky-600 rounded-full animate-spin"></div>
      </div>

      <div v-else-if="error" class="card p-12 text-center flex flex-col items-center">
        <ExclamationTriangleIcon class="w-16 h-16 text-slate-300 dark:text-slate-600 mb-4" />
        <h3 class="text-lg font-semibold text-slate-900 dark:text-white mb-2">Failed to load offers</h3>
        <p class="text-slate-600 dark:text-slate-400 mb-4">{{ error }}</p>
        <button @click="loadOffers" class="btn btn-primary">Retry</button>
      </div>

      <div v-else-if="filteredOffers.length === 0" class="card p-12 text-center flex flex-col items-center">
        <ClipboardDocumentListIcon class="w-16 h-16 text-slate-300 dark:text-slate-600 mb-4" />
        <h3 class="text-lg font-semibold text-slate-900 dark:text-white mb-2">No {{ filter }} offers</h3>
      </div>

      <div v-else class="space-y-4">
        <div v-for="offer in filteredOffers" :key="offer.id" class="card p-6">
          <div class="flex flex-col lg:flex-row justify-between gap-6">
            <div class="flex-1">
              <div class="flex items-center gap-3 mb-3">
                <h3 class="text-xl font-bold text-slate-900 dark:text-white">{{ offer.title }}</h3>
                <span :class="getStatusClass(offer.validation_status)" class="px-2 py-1 rounded-full text-xs font-medium">
                  {{ offer.validation_status }}
                </span>
              </div>
              
              <div class="grid grid-cols-2 lg:grid-cols-4 gap-4 text-sm mb-4">
                <div class="flex items-center gap-2 text-slate-600 dark:text-slate-400">
                  <BuildingOffice2Icon class="w-4 h-4" /><span>{{ offer.hospital_name || 'N/A' }}</span>
                </div>
                <div class="flex items-center gap-2 text-slate-600 dark:text-slate-400">
                  <ClipboardDocumentListIcon class="w-4 h-4" /><span>{{ offer.department_name || 'N/A' }}</span>
                </div>
                <div class="flex items-center gap-2 text-slate-600 dark:text-slate-400">
                  <CalendarIcon class="w-4 h-4" /><span>{{ formatDate(offer.start_date) }} - {{ formatDate(offer.end_date) }}</span>
                </div>
                <div class="flex items-center gap-2 text-slate-600 dark:text-slate-400">
                  <UserGroupIcon class="w-4 h-4" /><span>{{ offer.slots }} slots</span>
                </div>
              </div>
              
              <p class="text-slate-600 dark:text-slate-400 text-sm line-clamp-2">{{ offer.description }}</p>
            </div>
            
            <div v-if="offer.validation_status === 'pending'" class="flex lg:flex-col gap-3 justify-center">
              <button @click="validateOffer(offer.id, 'approved')" class="btn bg-green-600 hover:bg-green-700 text-white">Approve</button>
              <button @click="validateOffer(offer.id, 'rejected')" class="btn bg-red-600 hover:bg-red-700 text-white">Reject</button>
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
import { ExclamationTriangleIcon, ClipboardDocumentListIcon, BuildingOffice2Icon, CalendarIcon, UserGroupIcon } from '@heroicons/vue/24/outline'

const toast = useToast()
const loading = ref(true)
const error = ref(null)
const offers = ref([])
const filter = ref('pending')

const pendingOffers = computed(() => {
  if (!Array.isArray(offers.value)) return []
  return offers.value.filter(o => o.validation_status === 'pending')
})

const filteredOffers = computed(() => {
  if (!Array.isArray(offers.value)) return []
  return offers.value.filter(o => o.validation_status === filter.value)
})

onMounted(loadOffers)

async function loadOffers() {
  loading.value = true
  error.value = null
  try {
    const response = await api.get('/internships/all/')
    // Handle both paginated and non-paginated responses
    const data = response.data
    offers.value = data?.results || (Array.isArray(data) ? data : [])
    console.log('Loaded faculty offers:', offers.value)
  } catch (err) {
    console.error('Failed to load offers:', err)
    error.value = err.response?.data?.detail || 'Could not load offers.'
    offers.value = []
  } finally {
    loading.value = false
  }
}

async function validateOffer(id, status) {
  try {
    await api.patch(`/internships/${id}/validate/`, { validation_status: status })
    const offer = offers.value.find(o => o.id === id)
    if (offer) offer.validation_status = status
    toast.success(`Offer ${status}`)
  } catch (e) {
    toast.error('Failed to update offer')
  }
}

function getStatusClass(status) {
  const map = {
    pending: 'bg-amber-100 text-amber-800',
    approved: 'bg-green-100 text-green-800',
    rejected: 'bg-red-100 text-red-800'
  }
  return map[status] || 'bg-slate-100 text-slate-800'
}

function formatDate(date) {
  return date ? new Date(date).toLocaleDateString() : 'N/A'
}
</script>
