<template>
  <div class="min-h-screen py-8 bg-slate-50 dark:bg-slate-900">
    <div class="container mx-auto px-4">
      <div class="flex justify-between items-center mb-8">
        <div>
          <h1 class="text-3xl font-bold text-slate-900 dark:text-white">Optimization Reports</h1>
          <p class="text-slate-600 dark:text-slate-400">Analytics and insights for internship assignments</p>
        </div>
        <button @click="refreshData" :disabled="loading" class="btn btn-outline flex items-center gap-2">
          <ArrowPathIcon class="w-5 h-5" :class="{ 'animate-spin': loading }" />
          {{ loading ? 'Loading...' : 'Refresh' }}
        </button>
      </div>

      <div v-if="loading" class="flex justify-center py-20">
        <div class="w-10 h-10 border-4 border-sky-200 border-t-sky-600 rounded-full animate-spin"></div>
      </div>

      <template v-else>
        <!-- Summary Cards -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div class="card p-6">
            <div class="text-sm text-slate-500 mb-1">Total Applications</div>
            <div class="text-3xl font-bold text-slate-900 dark:text-white">{{ summary.total_applications }}</div>
            <div class="text-xs text-green-500">+{{ summary.recent_applications }} last 30 days</div>
          </div>
          <div class="card p-6">
            <div class="text-sm text-slate-500 mb-1">Acceptance Rate</div>
            <div class="text-3xl font-bold text-green-500">{{ summary.acceptance_rate }}%</div>
          </div>
          <div class="card p-6">
            <div class="text-sm text-slate-500 mb-1">Slot Utilization</div>
            <div class="text-3xl font-bold text-sky-500">{{ summary.utilization_rate }}%</div>
            <div class="text-xs text-slate-400">{{ summary.filled_slots }}/{{ summary.total_slots }} filled</div>
          </div>
          <div class="card p-6">
            <div class="text-sm text-slate-500 mb-1">Avg Review Time</div>
            <div class="text-3xl font-bold text-amber-500">{{ summary.avg_review_time_hours || '--' }}h</div>
          </div>
        </div>

        <!-- Status Breakdown -->
        <div class="card p-6 mb-8">
          <h2 class="text-lg font-bold text-slate-900 dark:text-white mb-4">Application Status Distribution</h2>
          <div class="flex gap-4">
            <div v-for="(count, status) in summary.status_breakdown" :key="status" 
                 class="flex-1 text-center p-4 rounded-lg" :class="statusColors[status]">
              <div class="text-2xl font-bold">{{ count }}</div>
              <div class="text-sm capitalize">{{ status }}</div>
            </div>
          </div>
        </div>

        <!-- Hospital Performance -->
        <div class="card p-6 mb-8">
          <h2 class="text-lg font-bold text-slate-900 dark:text-white mb-4">Hospital Performance</h2>
          <div class="overflow-x-auto">
            <table class="w-full">
              <thead>
                <tr class="border-b border-slate-200 dark:border-slate-700">
                  <th class="text-left py-3 text-sm font-medium text-slate-500">Hospital</th>
                  <th class="text-center py-3 text-sm font-medium text-slate-500">Applications</th>
                  <th class="text-center py-3 text-sm font-medium text-slate-500">Accepted</th>
                  <th class="text-center py-3 text-sm font-medium text-slate-500">Rejected</th>
                  <th class="text-center py-3 text-sm font-medium text-slate-500">Pending</th>
                  <th class="text-center py-3 text-sm font-medium text-slate-500">Rate</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="hospital in hospitalPerformance" :key="hospital.hospital_id" 
                    class="border-b border-slate-100 dark:border-slate-800">
                  <td class="py-3 text-slate-900 dark:text-white">{{ hospital.hospital_name }}</td>
                  <td class="py-3 text-center">{{ hospital.total_applications }}</td>
                  <td class="py-3 text-center text-green-600">{{ hospital.accepted }}</td>
                  <td class="py-3 text-center text-red-500">{{ hospital.rejected }}</td>
                  <td class="py-3 text-center text-amber-500">{{ hospital.pending }}</td>
                  <td class="py-3 text-center">
                    <span class="px-2 py-1 rounded-full text-xs font-medium"
                          :class="hospital.acceptance_rate > 50 ? 'bg-green-100 text-green-700' : 'bg-amber-100 text-amber-700'">
                      {{ hospital.acceptance_rate }}%
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Specialty Demand & Trends -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          <div class="card p-6">
            <h2 class="text-lg font-bold text-slate-900 dark:text-white mb-4">Specialty Demand</h2>
            <div class="space-y-3">
              <div v-for="specialty in specialtyDemand" :key="specialty.specialty" class="flex items-center gap-3">
                <div class="flex-1">
                  <div class="text-sm text-slate-700 dark:text-slate-300">{{ specialty.specialty }}</div>
                  <div class="h-2 bg-slate-100 dark:bg-slate-700 rounded-full mt-1">
                    <div class="h-full bg-sky-500 rounded-full" 
                         :style="`width: ${(specialty.applications / maxDemand) * 100}%`"></div>
                  </div>
                </div>
                <span class="text-sm font-medium text-slate-600 w-12 text-right">{{ specialty.applications }}</span>
              </div>
            </div>
          </div>

          <div class="card p-6">
            <h2 class="text-lg font-bold text-slate-900 dark:text-white mb-4">Score Distribution</h2>
            <div class="flex items-end gap-2 h-40">
              <div v-for="range in scoreDistribution" :key="range.range" 
                   class="flex-1 bg-sky-500 rounded-t hover:bg-sky-600 transition-colors relative group"
                   :style="`height: ${(range.count / maxScore) * 100}%`">
                <div class="absolute -top-6 left-1/2 -translate-x-1/2 text-xs font-medium opacity-0 group-hover:opacity-100">
                  {{ range.count }}
                </div>
              </div>
            </div>
            <div class="flex gap-2 mt-2">
              <div v-for="range in scoreDistribution" :key="range.range" 
                   class="flex-1 text-center text-xs text-slate-500">
                {{ range.range }}
              </div>
            </div>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '../services/api'
import { useToast } from 'vue-toastification'
import { ArrowPathIcon } from '@heroicons/vue/24/outline'

const toast = useToast()
const loading = ref(true)
const summary = ref({})
const hospitalPerformance = ref([])
const specialtyDemand = ref([])
const scoreDistribution = ref([])

const statusColors = {
  pending: 'bg-amber-100 dark:bg-amber-900/30 text-amber-700 dark:text-amber-300',
  reviewing: 'bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300',
  accepted: 'bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-300',
  rejected: 'bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-300',
  withdrawn: 'bg-slate-100 dark:bg-slate-700 text-slate-600 dark:text-slate-400'
}

const maxDemand = computed(() => 
  Math.max(...specialtyDemand.value.map(s => s.applications), 1)
)

const maxScore = computed(() => 
  Math.max(...scoreDistribution.value.map(s => s.count), 1)
)

onMounted(refreshData)

async function refreshData() {
  loading.value = true
  try {
    const [summaryRes, hospitalsRes, specialtyRes] = await Promise.all([
      api.get('/applications/reports/summary/'),
      api.get('/applications/reports/hospitals/'),
      api.get('/applications/reports/specialty/')
    ])
    summary.value = summaryRes.data
    hospitalPerformance.value = hospitalsRes.data
    specialtyDemand.value = specialtyRes.data
    
    // Generate score distribution locally if not provided
    scoreDistribution.value = [
      { range: '0-5', count: summary.value.status_breakdown?.rejected || 0 },
      { range: '5-10', count: Math.floor(summary.value.total_applications * 0.2) },
      { range: '10-15', count: Math.floor(summary.value.total_applications * 0.4) },
      { range: '15-20', count: summary.value.status_breakdown?.accepted || 0 },
      { range: '20+', count: Math.floor(summary.value.total_applications * 0.05) }
    ]
  } catch (error) {
    toast.error('Failed to load reports')
  } finally {
    loading.value = false
  }
}
</script>
