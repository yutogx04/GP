<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <!-- Header -->
    <div class="flex justify-between items-center mb-8">
      <div>
        <h1 class="text-3xl font-bold text-gray-900 dark:text-white">Manage Internship Offers</h1>
        <p class="mt-2 text-gray-600 dark:text-gray-400">Create and manage your hospital's internship opportunities</p>
      </div>
      <router-link to="/offers/create" class="btn btn-primary">
        <PlusIcon class="btn-icon w-5 h-5 mr-1" />
        New Offer
      </router-link>
    </div>

    <!-- Stats -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
      <div class="card p-6">
        <div class="flex items-center">
          <div class="w-12 h-12 bg-blue-100 dark:bg-blue-900/30 rounded-lg flex items-center justify-center">
            <BriefcaseIcon class="w-6 h-6 text-blue-600 dark:text-blue-400" />
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Total Offers</p>
            <p class="text-2xl font-semibold text-gray-900 dark:text-white">{{ stats.total }}</p>
          </div>
        </div>
      </div>

      <div class="card p-6">
        <div class="flex items-center">
          <div class="w-12 h-12 bg-green-100 dark:bg-green-900/30 rounded-lg flex items-center justify-center">
            <EyeIcon class="w-6 h-6 text-green-600 dark:text-green-400" />
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Active</p>
            <p class="text-2xl font-semibold text-gray-900 dark:text-white">{{ stats.active }}</p>
          </div>
        </div>
      </div>

      <div class="card p-6">
        <div class="flex items-center">
          <div class="w-12 h-12 bg-orange-100 dark:bg-orange-900/30 rounded-lg flex items-center justify-center">
            <UserGroupIcon class="w-6 h-6 text-orange-600 dark:text-orange-400" />
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Applications</p>
            <p class="text-2xl font-semibold text-gray-900 dark:text-white">{{ stats.applications }}</p>
          </div>
        </div>
      </div>

      <div class="card p-6">
        <div class="flex items-center">
          <div class="w-12 h-12 bg-purple-100 dark:bg-purple-900/30 rounded-lg flex items-center justify-center">
            <ChartBarIcon class="w-6 h-6 text-purple-600 dark:text-purple-400" />
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Fill Rate</p>
            <p class="text-2xl font-semibold text-gray-900 dark:text-white">{{ stats.fill_rate }}%</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Offers Table -->
    <div class="card">
      <div class="p-6 border-b border-gray-200 dark:border-slate-700">
        <div class="flex justify-between items-center">
          <h2 class="text-lg font-semibold text-gray-900 dark:text-white">Internship Offers</h2>
          <div class="flex space-x-3">
            <select v-model="filters.status" class="input-field w-auto">
              <option value="">All Status</option>
              <option value="published">Published</option>
              <option value="draft">Draft</option>
              <option value="closed">Closed</option>
            </select>
            <input 
              v-model="filters.search" 
              type="text" 
              placeholder="Search offers..." 
              class="input-field w-64"
            >
          </div>
        </div>
      </div>

      <div v-if="loading" class="p-8 text-center">
        <div class="w-10 h-10 border-4 border-sky-200 border-t-sky-600 rounded-full animate-spin mx-auto"></div>
        <p class="mt-2 text-gray-600 dark:text-gray-400">Loading offers...</p>
      </div>

      <div v-else-if="!Array.isArray(offers) || offers.length === 0" class="p-8 text-center flex flex-col items-center">
        <BriefcaseIcon class="w-16 h-16 text-slate-300 dark:text-slate-600 mb-3" />
        <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-2">No offers yet</h3>
        <p class="text-gray-500 dark:text-gray-400 mb-4">Create your first internship offer to get started.</p>
        <router-link to="/offers/create" class="btn btn-primary">Create Offer</router-link>
      </div>

      <div v-else class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200 dark:divide-slate-700">
          <thead class="bg-gray-50 dark:bg-slate-800">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">Internship Details</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">Department & Dates</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">Applications</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">Status</th>
              <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">Actions</th>
            </tr>
          </thead>
          <tbody class="bg-white dark:bg-slate-900 divide-y divide-gray-200 dark:divide-slate-700">
            <tr v-for="offer in filteredOffers" :key="offer.id" class="hover:bg-gray-50 dark:hover:bg-slate-800/50">
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm font-medium text-gray-900 dark:text-white">{{ offer.title }}</div>
                <div class="text-sm text-gray-500">{{ offer.hospital?.name || 'N/A' }}</div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm text-gray-900 dark:text-white">{{ offer.department?.name || 'N/A' }}</div>
                <div class="text-sm text-gray-500">{{ formatDate(offer.start_date) }} - {{ formatDate(offer.end_date) }}</div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm text-gray-900 dark:text-white">{{ offer.applications_count || 0 }} applications</div>
                <div class="text-sm text-gray-500">{{ offer.slots }} slots available</div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span :class="getStatusBadgeClass(offer.status)" class="px-2.5 py-0.5 rounded-full text-xs font-medium">
                  {{ offer.status }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                <div class="flex justify-end space-x-2">
                  <router-link :to="`/internships/${offer.id}`" class="btn btn-outline btn-sm">View</router-link>
                  <button @click="deleteOffer(offer.id)" class="btn btn-sm bg-red-600 hover:bg-red-700 text-white">Delete</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useToast } from 'vue-toastification'
import api from '../services/api'
import { BriefcaseIcon, EyeIcon, UserGroupIcon, ChartBarIcon, PlusIcon } from '@heroicons/vue/24/outline'

const offers = ref([])
const loading = ref(true)
const filters = ref({ status: '', search: '' })
const stats = ref({ total: 0, active: 0, applications: 0, fill_rate: 0 })

const router = useRouter()
const toast = useToast()

const filteredOffers = computed(() => {
  if (!Array.isArray(offers.value)) return []
  return offers.value.filter(offer => {
    const matchesStatus = !filters.value.status || offer.status === filters.value.status
    const matchesSearch = !filters.value.search || 
      offer.title?.toLowerCase().includes(filters.value.search.toLowerCase()) ||
      offer.department?.name?.toLowerCase().includes(filters.value.search.toLowerCase())
    return matchesStatus && matchesSearch
  })
})

onMounted(loadOffers)

async function loadOffers() {
  loading.value = true
  try {
    const response = await api.get('/internships/hospital/')
    // Handle both paginated and non-paginated responses
    const data = response.data
    offers.value = data?.results || (Array.isArray(data) ? data : [])
    console.log('Loaded offers:', offers.value)
    updateStats()
  } catch (error) {
    console.error('Error loading offers:', error)
    offers.value = []
  } finally {
    loading.value = false
  }
}

function updateStats() {
  if (!Array.isArray(offers.value)) {
    stats.value = { total: 0, active: 0, applications: 0, fill_rate: 0 }
    return
  }
  const totalSlots = offers.value.reduce((sum, offer) => sum + (offer.slots || 0), 0)
  const totalApps = offers.value.reduce((sum, offer) => sum + (offer.applications_count || 0), 0)
  stats.value = {
    total: offers.value.length,
    active: offers.value.filter(offer => offer.status === 'published').length,
    applications: totalApps,
    fill_rate: totalSlots > 0 ? Math.round((totalApps / totalSlots) * 100) : 0
  }
}

async function deleteOffer(offerId) {
  if (!confirm('Are you sure you want to delete this offer?')) return
  try {
    await api.delete(`/internships/${offerId}/delete/`)
    offers.value = offers.value.filter(offer => offer.id !== offerId)
    updateStats()
    alert('Offer deleted successfully')
  } catch (error) {
    console.error('Delete error:', error)
    alert('Failed to delete offer')
  }
}

function getStatusBadgeClass(status) {
  const classes = {
    published: 'bg-green-100 text-green-800',
    draft: 'bg-amber-100 text-amber-800',
    closed: 'bg-gray-100 text-gray-800'
  }
  return classes[status] || 'bg-gray-100 text-gray-800'
}

function formatDate(dateString) {
  return dateString ? new Date(dateString).toLocaleDateString() : 'N/A'
}
</script>