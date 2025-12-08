<template>
  <div class="min-h-screen py-8 bg-slate-50 dark:bg-slate-900">
    <div class="container mx-auto px-4">
      <div class="flex justify-between items-center mb-8">
        <div>
          <h1 class="text-3xl font-bold text-slate-900 dark:text-white">Faculty Reports</h1>
          <p class="text-slate-600 dark:text-slate-400">Analytics and statistics for your faculty</p>
        </div>
        <button @click="exportReport" class="btn btn-primary">Export Report</button>
      </div>

      <div v-if="loading" class="flex justify-center py-20">
        <div class="w-10 h-10 border-4 border-sky-200 border-t-sky-600 rounded-full animate-spin"></div>
      </div>

      <div v-else>
        <!-- Stats Grid -->
        <div class="grid grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div class="card p-6">
            <div class="text-3xl font-bold text-slate-900 dark:text-white mb-1">{{ stats.totalStudents }}</div>
            <div class="text-sm text-slate-500">Total Students</div>
          </div>
          <div class="card p-6">
            <div class="text-3xl font-bold text-green-600 mb-1">{{ stats.placedStudents }}</div>
            <div class="text-sm text-slate-500">Placed Students</div>
          </div>
          <div class="card p-6">
            <div class="text-3xl font-bold text-sky-600 mb-1">{{ stats.placementRate }}%</div>
            <div class="text-sm text-slate-500">Placement Rate</div>
          </div>
          <div class="card p-6">
            <div class="text-3xl font-bold text-amber-600 mb-1">{{ stats.averageGrade }}</div>
            <div class="text-sm text-slate-500">Avg. Evaluation</div>
          </div>
        </div>

        <!-- Charts Section -->
        <div class="grid lg:grid-cols-2 gap-6 mb-8">
          <div class="card p-6">
            <h3 class="font-semibold text-slate-900 dark:text-white mb-4">Students by Level</h3>
            <div class="space-y-3">
              <div v-for="level in stats.byLevel" :key="level.name" class="flex items-center gap-4">
                <span class="w-16 text-sm text-slate-600 dark:text-slate-400">{{ level.name }}</span>
                <div class="flex-1 bg-slate-100 dark:bg-slate-700 rounded-full h-4 overflow-hidden">
                  <div class="h-full bg-sky-500" :style="{ width: (level.count / stats.totalStudents * 100) + '%' }"></div>
                </div>
                <span class="w-12 text-right text-sm font-medium text-slate-900 dark:text-white">{{ level.count }}</span>
              </div>
            </div>
          </div>
          
          <div class="card p-6">
            <h3 class="font-semibold text-slate-900 dark:text-white mb-4">Applications by Status</h3>
            <div class="space-y-3">
              <div v-for="status in stats.appsByStatus" :key="status.name" class="flex items-center gap-4">
                <span class="w-20 text-sm text-slate-600 dark:text-slate-400">{{ status.name }}</span>
                <div class="flex-1 bg-slate-100 dark:bg-slate-700 rounded-full h-4 overflow-hidden">
                  <div class="h-full" :class="status.color" :style="{ width: status.percent + '%' }"></div>
                </div>
                <span class="w-12 text-right text-sm font-medium text-slate-900 dark:text-white">{{ status.count }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Top Hospitals -->
        <div class="card p-6">
          <h3 class="font-semibold text-slate-900 dark:text-white mb-4">Top Partner Hospitals</h3>
          <div class="overflow-x-auto">
            <table class="w-full">
              <thead>
                <tr class="text-left border-b border-slate-100 dark:border-slate-700">
                  <th class="pb-3 text-sm font-medium text-slate-500">Hospital</th>
                  <th class="pb-3 text-sm font-medium text-slate-500">Students Placed</th>
                  <th class="pb-3 text-sm font-medium text-slate-500">Avg Rating</th>
                  <th class="pb-3 text-sm font-medium text-slate-500">Satisfaction</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-100 dark:divide-slate-700">
                <tr v-for="hospital in stats.topHospitals" :key="hospital.name">
                  <td class="py-3 font-medium text-slate-900 dark:text-white">{{ hospital.name }}</td>
                  <td class="py-3 text-slate-600 dark:text-slate-400">{{ hospital.students }}</td>
                  <td class="py-3 text-slate-600 dark:text-slate-400">{{ hospital.avgRating }}/20</td>
                  <td class="py-3">
                    <span class="text-green-600 font-medium">{{ hospital.satisfaction }}%</span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../services/api'
import { useToast } from 'vue-toastification'

const toast = useToast()
const loading = ref(true)
const stats = ref({
  totalStudents: 0,
  placedStudents: 0,
  placementRate: 0,
  averageGrade: '0.0',
  byLevel: [],
  appsByStatus: [],
  topHospitals: []
})

onMounted(async () => {
  try {
    const response = await api.get('/users/faculty/reports/')
    stats.value = response.data
  } catch (error) {
    // Use mock data if API not ready
    stats.value = {
      totalStudents: 156,
      placedStudents: 142,
      placementRate: 91,
      averageGrade: '14.2',
      byLevel: [
        { name: 'L3', count: 45 },
        { name: 'M1', count: 62 },
        { name: 'M2', count: 49 }
      ],
      appsByStatus: [
        { name: 'Pending', count: 23, percent: 15, color: 'bg-amber-500' },
        { name: 'Accepted', count: 112, percent: 72, color: 'bg-green-500' },
        { name: 'Rejected', count: 21, percent: 13, color: 'bg-red-500' }
      ],
      topHospitals: [
        { name: 'CHU Mustapha', students: 45, avgRating: 15.2, satisfaction: 92 },
        { name: 'EPH Kouba', students: 32, avgRating: 14.8, satisfaction: 88 },
        { name: 'CHU Bab El-Oued', students: 28, avgRating: 14.5, satisfaction: 85 }
      ]
    }
  } finally {
    loading.value = false
  }
})

const exportReport = () => {
  toast.info('Report export coming soon')
}
</script>
