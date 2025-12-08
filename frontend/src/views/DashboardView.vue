<template>
  <div class="min-h-screen py-8 bg-slate-50 dark:bg-slate-900 transition-colors duration-300">
    <div class="container mx-auto px-4 sm:px-6 lg:px-8">
      <!-- Welcome Section -->
      <div class="flex flex-col md:flex-row md:items-center justify-between mb-8 gap-4">
        <div>
          <h1 class="text-3xl font-bold text-slate-900 dark:text-white mb-2 flex items-center gap-2">
            Welcome back, {{ auth.user?.first_name }}! <HandRaisedIcon class="w-8 h-8 text-amber-400" />
          </h1>
          <p class="text-slate-600 dark:text-slate-400">{{ roleDescription }}</p>
        </div>
        <div v-if="auth.isHospitalAdmin">
          <router-link to="/internships/create" class="btn btn-primary shadow-lg shadow-sky-500/20">
            <PlusIcon class="w-5 h-5 mr-2" /> Create New Offer
          </router-link>
        </div>
      </div>

      <!-- STUDENT DASHBOARD -->
      <div v-if="auth.isStudent" class="space-y-8">
        <!-- Stats -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div class="card p-6 border-l-4 border-l-sky-500">
            <div class="flex items-center justify-between mb-4">
              <div class="text-slate-500 dark:text-slate-400 font-medium">Applications</div>
              <div class="w-10 h-10 bg-sky-100 dark:bg-sky-900/30 rounded-lg flex items-center justify-center text-xl">
                <ClipboardDocumentListIcon class="w-6 h-6 text-sky-600 dark:text-sky-400" />
              </div>
            </div>
            <div class="text-3xl font-bold text-slate-900 dark:text-white">{{ applications.length }}</div>
          </div>
          <div class="card p-6 border-l-4 border-l-green-500">
            <div class="flex items-center justify-between mb-4">
              <div class="text-slate-500 dark:text-slate-400 font-medium">Accepted</div>
              <div class="w-10 h-10 bg-green-100 dark:bg-green-900/30 rounded-lg flex items-center justify-center text-xl">
                <CheckCircleIcon class="w-6 h-6 text-green-600 dark:text-green-400" />
              </div>
            </div>
            <div class="text-3xl font-bold text-slate-900 dark:text-white">{{ acceptedApplications.length }}</div>
          </div>
        </div>

        <!-- Recent Applications -->
        <div>
          <div class="flex items-center justify-between mb-6">
            <h2 class="text-xl font-bold text-slate-900 dark:text-white">Recent Applications</h2>
            <router-link to="/applications" class="text-sky-600 hover:text-sky-700 dark:text-sky-400 font-medium hover:underline">
              View All
            </router-link>
          </div>
          
          <div v-if="applications.length === 0" class="card p-12 text-center border-dashed border-2 border-slate-200 dark:border-slate-700 bg-transparent flex flex-col items-center">
            <div class="w-16 h-16 bg-slate-100 dark:bg-slate-800 rounded-full flex items-center justify-center mx-auto mb-4 text-3xl">
              <DocumentTextIcon class="w-8 h-8 text-slate-400" />
            </div>
            <h3 class="text-lg font-semibold text-slate-900 dark:text-white mb-2">No applications yet</h3>
            <router-link to="/internships" class="btn btn-primary mt-4">Browse Internships</router-link>
          </div>

          <div v-else class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div v-for="application in recentApplications" :key="application.id" class="card p-6 hover:border-sky-500/50 transition-colors">
              <div class="flex justify-between items-start mb-4">
                <h4 class="font-bold text-slate-900 dark:text-white line-clamp-1">{{ application.offer.title }}</h4>
                <span :class="`px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(application.status)}`">
                  {{ application.status }}
                </span>
              </div>
              <p class="text-slate-600 dark:text-slate-400 text-sm mb-4 flex items-center gap-2">
                <BuildingOffice2Icon class="w-4 h-4" /> {{ application.offer.hospital.name }}
              </p>
              <div class="flex items-center justify-between mt-auto pt-4 border-t border-slate-100 dark:border-slate-700">
                <span class="text-xs text-slate-500">Applied {{ formatDate(application.applied_at) }}</span>
                <router-link :to="`/internships/${application.offer.id}`" class="text-sm font-medium text-sky-600 hover:text-sky-700 dark:text-sky-400">
                  View Details →
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- HOSPITAL ADMIN DASHBOARD -->
      <div v-else-if="auth.isHospitalAdmin" class="space-y-8">
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div class="card p-6 border-l-4 border-l-sky-500">
            <div class="flex items-center justify-between mb-4">
              <div class="text-slate-500 dark:text-slate-400 font-medium">Active Offers</div>
              <div class="w-10 h-10 bg-sky-100 dark:bg-sky-900/30 rounded-lg flex items-center justify-center text-xl">
                <BuildingOffice2Icon class="w-6 h-6 text-sky-600 dark:text-sky-400" />
              </div>
            </div>
            <div class="text-3xl font-bold text-slate-900 dark:text-white">{{ offers.length }}</div>
          </div>
          <div class="card p-6 border-l-4 border-l-purple-500">
            <div class="flex items-center justify-between mb-4">
              <div class="text-slate-500 dark:text-slate-400 font-medium">Total Applications</div>
              <div class="w-10 h-10 bg-purple-100 dark:bg-purple-900/30 rounded-lg flex items-center justify-center text-xl">
                <UserGroupIcon class="w-6 h-6 text-purple-600 dark:text-purple-400" />
              </div>
            </div>
            <div class="text-3xl font-bold text-slate-900 dark:text-white">{{ totalApplications }}</div>
          </div>
        </div>

        <div>
          <h2 class="text-xl font-bold text-slate-900 dark:text-white mb-6">Your Internship Offers</h2>
          <div v-if="offers.length === 0" class="card p-12 text-center border-dashed border-2 border-slate-200 dark:border-slate-700 bg-transparent">
            <h3 class="text-lg font-semibold text-slate-900 dark:text-white mb-2">No offers created</h3>
            <router-link to="/internships/create" class="btn btn-primary mt-4">Create Offer</router-link>
          </div>
          <div v-else class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div v-for="offer in offers" :key="offer.id" class="card p-6 hover:border-sky-500/50 transition-colors">
              <div class="flex justify-between items-start mb-4">
                <h4 class="font-bold text-slate-900 dark:text-white line-clamp-1">{{ offer.title }}</h4>
                <span class="px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400">Active</span>
              </div>
              <div class="space-y-2 mb-4">
                <p class="text-sm text-slate-600 dark:text-slate-400 flex items-center gap-2"><ClipboardDocumentListIcon class="w-4 h-4" /> {{ offer.department.name }}</p>
                <p class="text-sm text-slate-600 dark:text-slate-400 flex items-center gap-2"><UserGroupIcon class="w-4 h-4" /> {{ offer.applications_count || 0 }} Applications</p>
              </div>
              <div class="flex items-center justify-between mt-auto pt-4 border-t border-slate-100 dark:border-slate-700">
                <span class="text-xs text-slate-500">Created {{ formatDate(offer.created_at) }}</span>
                <router-link :to="`/internships/${offer.id}`" class="text-sm font-medium text-sky-600 hover:text-sky-700 dark:text-sky-400">Manage →</router-link>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- FACULTY ADMIN DASHBOARD -->
      <div v-else-if="auth.isFacultyAdmin" class="space-y-8">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div class="card p-6 border-l-4 border-l-indigo-500">
            <div class="flex items-center justify-between mb-4">
              <div class="text-slate-500 dark:text-slate-400 font-medium">Total Students</div>
              <div class="w-10 h-10 bg-indigo-100 dark:bg-indigo-900/30 rounded-lg flex items-center justify-center text-xl">
                <AcademicCapIcon class="w-6 h-6 text-indigo-600 dark:text-indigo-400" />
              </div>
            </div>
            <div class="text-3xl font-bold text-slate-900 dark:text-white">--</div>
          </div>
          <div class="card p-6 border-l-4 border-l-teal-500">
            <div class="flex items-center justify-between mb-4">
              <div class="text-slate-500 dark:text-slate-400 font-medium">Placements</div>
              <div class="w-10 h-10 bg-teal-100 dark:bg-teal-900/30 rounded-lg flex items-center justify-center text-xl">
                <MapPinIcon class="w-6 h-6 text-teal-600 dark:text-teal-400" />
              </div>
            </div>
            <div class="text-3xl font-bold text-slate-900 dark:text-white">--</div>
          </div>
        </div>
        
        <div class="card p-8 text-center">
          <h2 class="text-xl font-bold text-slate-900 dark:text-white mb-4">Faculty Administration</h2>
          <p class="text-slate-600 dark:text-slate-400 mb-6">Manage students, validate documents, and oversee the internship process.</p>
          <div class="flex justify-center gap-4">
            <router-link to="/faculty/students" class="btn btn-primary">Manage Students</router-link>
            <router-link to="/faculty/reports" class="btn btn-outline">View Reports</router-link>
          </div>
        </div>
      </div>

      <!-- SUPERVISOR (ENCADRANT) DASHBOARD -->
      <div v-else-if="auth.isEncadrant" class="space-y-8">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
           <div class="card p-6 border-l-4 border-l-orange-500">
            <div class="flex items-center justify-between mb-4">
              <div class="text-slate-500 dark:text-slate-400 font-medium">Students Supervised</div>
              <div class="w-10 h-10 bg-orange-100 dark:bg-orange-900/30 rounded-lg flex items-center justify-center text-xl">
                <UserGroupIcon class="w-6 h-6 text-orange-600 dark:text-orange-400" />
              </div>
            </div>
            <div class="text-3xl font-bold text-slate-900 dark:text-white">--</div>
          </div>
           <div class="card p-6 border-l-4 border-l-blue-500">
            <div class="flex items-center justify-between mb-4">
              <div class="text-slate-500 dark:text-slate-400 font-medium">Pending Evaluations</div>
              <div class="w-10 h-10 bg-blue-100 dark:bg-blue-900/30 rounded-lg flex items-center justify-center text-xl">
                <DocumentTextIcon class="w-6 h-6 text-blue-600 dark:text-blue-400" />
              </div>
            </div>
            <div class="text-3xl font-bold text-slate-900 dark:text-white">--</div>
          </div>
        </div>

        <div class="card p-8 text-center">
          <h2 class="text-xl font-bold text-slate-900 dark:text-white mb-4">Supervision Area</h2>
          <p class="text-slate-600 dark:text-slate-400 mb-6">Track student progress and submit internship evaluations.</p>
          <div class="flex justify-center gap-4">
            <router-link to="/supervisor/students" class="btn btn-primary">My Students</router-link>
            <router-link to="/supervisor/evaluations" class="btn btn-outline">Evaluations</router-link>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useAuthStore } from '../stores/auth'
import api from '../services/api'
import {
  HandRaisedIcon, PlusIcon, ClipboardDocumentListIcon, CheckCircleIcon, 
  DocumentTextIcon, BuildingOffice2Icon, UserGroupIcon, AcademicCapIcon, MapPinIcon
} from '@heroicons/vue/24/outline'

const auth = useAuthStore()
const applications = ref([])
const offers = ref([])

const roleDescription = computed(() => {
  if (auth.isStudent) return "Track your applications and find new opportunities"
  if (auth.isHospitalAdmin) return "Manage internship offers and applications"
  if (auth.isFacultyAdmin) return "Oversee student placements and academic requirements"
  if (auth.isEncadrant) return "Evaluate and supervise medical interns"
  return "Welcome to MedIntern"
})

onMounted(async () => {
  try {
    if (auth.isStudent) {
      const response = await api.get('/applications/')
      applications.value = response.data?.results || (Array.isArray(response.data) ? response.data : [])
    } else if (auth.isHospitalAdmin) {
      const response = await api.get('/internships/')
      offers.value = response.data?.results || (Array.isArray(response.data) ? response.data : [])
    }
    // Add API calls for other roles here when endpoints are ready
  } catch (error) {
    console.error('Failed to load dashboard data:', error)
    applications.value = []
    offers.value = []
  }
})

const acceptedApplications = computed(() => {
  if (!Array.isArray(applications.value)) return []
  return applications.value.filter(app => app.status === 'accepted')
})

const recentApplications = computed(() => {
  if (!Array.isArray(applications.value)) return []
  return [...applications.value]
    .sort((a, b) => new Date(b.applied_at) - new Date(a.applied_at))
    .slice(0, 6)
})

const totalApplications = computed(() => {
  if (!Array.isArray(offers.value)) return 0
  return offers.value.reduce((acc, offer) => acc + (offer.applications_count || 0), 0)
})

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  })
}

const getStatusColor = (status) => {
  const colors = {
    pending: 'bg-amber-100 text-amber-800 dark:bg-amber-900/30 dark:text-amber-400',
    accepted: 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400',
    rejected: 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400'
  }
  return colors[status] || 'bg-slate-100 text-slate-800'
}
</script>
