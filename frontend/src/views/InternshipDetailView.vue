<template>
  <div class="min-h-screen py-8 bg-slate-50 dark:bg-slate-900">
    <div class="container mx-auto px-4">
      <div v-if="loading" class="flex justify-center py-20">
        <div class="w-10 h-10 border-4 border-sky-200 border-t-sky-600 rounded-full animate-spin"></div>
      </div>

      <div v-else-if="internship" class="max-w-4xl mx-auto">
        <!-- Breadcrumb -->
        <router-link to="/internships" class="inline-flex items-center gap-2 text-slate-600 dark:text-slate-400 hover:text-sky-600 mb-6">
          ← Back to Internships
        </router-link>

        <!-- Header Card -->
        <div class="card p-8 mb-6">
          <div class="flex flex-col md:flex-row justify-between gap-6">
            <div class="flex-1">
              <div class="flex items-center gap-3 mb-3">
                <span :class="internship.status === 'open' ? 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400' : 'bg-slate-100 text-slate-600'" class="px-3 py-1 rounded-full text-sm font-medium">
                  {{ internship.status }}
                </span>
                <span v-if="internship.is_urgent" class="bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400 px-3 py-1 rounded-full text-sm font-medium">
                  Urgent
                </span>
              </div>
              <h1 class="text-3xl font-bold text-slate-900 dark:text-white mb-4">{{ internship.title }}</h1>
              
              <div class="grid grid-cols-2 gap-4 text-sm">
                <div class="flex items-center gap-2 text-slate-600 dark:text-slate-400">
                  <BuildingOffice2Icon class="w-5 h-5" />
                  <span class="font-medium">{{ internship.hospital_name }}</span>
                </div>
                <div class="flex items-center gap-2 text-slate-600 dark:text-slate-400">
                  <ClipboardDocumentListIcon class="w-5 h-5" />
                  <span>{{ internship.department_name }}</span>
                </div>
                <div class="flex items-center gap-2 text-slate-600 dark:text-slate-400">
                  <CalendarIcon class="w-5 h-5" />
                  <span>{{ formatDate(internship.start_date) }} - {{ formatDate(internship.end_date) }}</span>
                </div>
                <div class="flex items-center gap-2 text-slate-600 dark:text-slate-400">
                  <UserGroupIcon class="w-5 h-5" />
                  <span>{{ internship.available_slots }} / {{ internship.slots }} slots</span>
                </div>
              </div>
            </div>
            
            <div class="md:text-right space-y-3">
              <div class="text-sm text-slate-500">
                <span class="font-medium">Deadline:</span> {{ formatDate(internship.application_deadline) }}
              </div>
              
              <template v-if="auth.isStudent">
                <button v-if="!hasApplied && internship.status === 'open'" @click="applyNow" class="btn btn-primary btn-lg" :disabled="applying">
                  {{ applying ? 'Applying...' : 'Apply Now' }}
                </button>
                <div v-else-if="hasApplied" class="inline-flex items-center gap-2 px-4 py-2 bg-green-100 dark:bg-green-900/30 text-green-800 dark:text-green-400 rounded-lg font-medium">
                  <CheckCircleIcon class="w-5 h-5" /> Application Submitted
                </div>
              </template>
              
              <router-link v-if="!auth.isLoggedIn" to="/login" class="btn btn-primary">Login to Apply</router-link>
            </div>
          </div>
        </div>

        <!-- Content Grid -->
        <div class="grid lg:grid-cols-3 gap-6">
          <div class="lg:col-span-2 space-y-6">
            <!-- Description -->
            <div class="card p-6">
              <h2 class="text-lg font-semibold text-slate-900 dark:text-white mb-4 flex items-center gap-2">
                <span class="w-1 h-6 bg-sky-500 rounded-full"></span>
                Description
              </h2>
              <div class="prose dark:prose-invert max-w-none text-slate-600 dark:text-slate-300">
                {{ internship.description }}
              </div>
            </div>

            <!-- Requirements -->
            <div v-if="internship.prerequisites" class="card p-6">
              <h2 class="text-lg font-semibold text-slate-900 dark:text-white mb-4 flex items-center gap-2">
                <span class="w-1 h-6 bg-amber-500 rounded-full"></span>
                Requirements
              </h2>
              <div class="prose dark:prose-invert max-w-none text-slate-600 dark:text-slate-300">
                {{ internship.prerequisites }}
              </div>
            </div>

            <!-- Benefits -->
            <div v-if="internship.benefits" class="card p-6">
              <h2 class="text-lg font-semibold text-slate-900 dark:text-white mb-4 flex items-center gap-2">
                <span class="w-1 h-6 bg-green-500 rounded-full"></span>
                Benefits
              </h2>
              <div class="prose dark:prose-invert max-w-none text-slate-600 dark:text-slate-300">
                {{ internship.benefits }}
              </div>
            </div>
          </div>

          <!-- Sidebar -->
          <div class="space-y-6">
            <div class="card p-6">
              <h3 class="font-semibold text-slate-900 dark:text-white mb-4">Details</h3>
              <dl class="space-y-3 text-sm">
                <div class="flex justify-between">
                  <dt class="text-slate-500">Type</dt>
                  <dd class="font-medium text-slate-900 dark:text-white">{{ internship.type_display || 'Clinical' }}</dd>
                </div>
                <div class="flex justify-between">
                  <dt class="text-slate-500">Min. Level</dt>
                  <dd class="font-medium text-slate-900 dark:text-white">{{ internship.minimum_study_level_display || 'L3' }}</dd>
                </div>
                <div v-if="internship.is_paid" class="flex justify-between">
                  <dt class="text-slate-500">Compensation</dt>
                  <dd class="font-medium text-green-600">{{ internship.payment_amount }} DZD/month</dd>
                </div>
              </dl>
            </div>

            <div v-if="internship.required_skills?.length" class="card p-6">
              <h3 class="font-semibold text-slate-900 dark:text-white mb-4">Required Skills</h3>
              <div class="flex flex-wrap gap-2">
                <span v-for="skill in internship.required_skills" :key="skill" class="px-3 py-1 bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 rounded-full text-sm">
                  {{ skill }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-else class="text-center py-20">
        <p class="text-slate-500">Internship not found</p>
        <router-link to="/internships" class="btn btn-primary mt-4">Browse Internships</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import api from '../services/api'
import { useToast } from 'vue-toastification'
import { BuildingOffice2Icon, ClipboardDocumentListIcon, CalendarIcon, UserGroupIcon } from '@heroicons/vue/24/outline'
import { CheckCircleIcon } from '@heroicons/vue/24/solid'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()
const toast = useToast()

const loading = ref(true)
const applying = ref(false)
const internship = ref(null)
const userApplications = ref([])

const hasApplied = computed(() => {
  return userApplications.value.some(app => app.offer?.id === internship.value?.id)
})

onMounted(async () => {
  try {
    const offerRes = await api.get(`/internships/${route.params.id}/`)
    internship.value = offerRes.data
    console.log('Loaded internship:', internship.value)
    
    if (auth.isLoggedIn && auth.isStudent) {
      const appsRes = await api.get('/applications/')
      const appsData = appsRes.data
      userApplications.value = appsData?.results || (Array.isArray(appsData) ? appsData : [])
    }
  } catch (error) {
    console.error('Failed to load internship:', error)
    toast.error('Failed to load internship details')
  } finally {
    loading.value = false
  }
})

const applyNow = async () => {
  applying.value = true
  try {
    await api.post('/applications/create/', { offer: internship.value.id })
    userApplications.value.push({ offer: { id: internship.value.id } })
    toast.success('Application submitted successfully!')
  } catch (error) {
    toast.error(error.response?.data?.detail || 'Failed to submit application')
  } finally {
    applying.value = false
  }
}

const formatDate = (date) => {
  if (!date) return 'N/A'
  return new Date(date).toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' })
}
</script>
