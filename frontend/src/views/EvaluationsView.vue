<template>
  <div class="min-h-screen py-8 bg-slate-50 dark:bg-slate-900">
    <div class="container mx-auto px-4">
      <h1 class="text-3xl font-bold text-slate-900 dark:text-white mb-2">My Evaluations</h1>
      <p class="text-slate-600 dark:text-slate-400 mb-8">View your internship evaluations and feedback</p>

      <div v-if="loading" class="flex justify-center py-20">
        <div class="w-10 h-10 border-4 border-sky-200 border-t-sky-600 rounded-full animate-spin"></div>
      </div>

      <div v-else-if="evaluations.length === 0" class="card p-12 text-center flex flex-col items-center">
        <ChartBarIcon class="w-16 h-16 text-slate-300 dark:text-slate-600 mb-4" />
        <h3 class="text-lg font-semibold text-slate-900 dark:text-white mb-2">No evaluations yet</h3>
        <p class="text-slate-600 dark:text-slate-400">Complete an internship to receive evaluations</p>
      </div>

      <div v-else class="space-y-6">
        <div v-for="evaluation in evaluations" :key="evaluation.id" class="card p-6">
          <div class="flex justify-between items-start mb-4">
            <div>
              <h3 class="text-xl font-bold text-slate-900 dark:text-white">{{ evaluation.internship?.offer?.title }}</h3>
              <p class="text-slate-600 dark:text-slate-400">{{ evaluation.internship?.offer?.hospital_name }}</p>
            </div>
            <div class="text-right">
              <div class="text-3xl font-bold" :class="getGradeColor(evaluation.final_grade)">
                {{ evaluation.final_grade?.toFixed(1) || '—' }}/20
              </div>
              <p class="text-sm text-slate-500">{{ getMention(evaluation.final_grade) }}</p>
            </div>
          </div>
          
          <div class="grid grid-cols-3 gap-4 mb-6">
            <div class="text-center p-3 bg-slate-50 dark:bg-slate-800 rounded-lg">
              <div class="text-lg font-bold text-slate-900 dark:text-white">{{ evaluation.technical_skills || '—' }}</div>
              <div class="text-xs text-slate-500">Technical</div>
            </div>
            <div class="text-center p-3 bg-slate-50 dark:bg-slate-800 rounded-lg">
              <div class="text-lg font-bold text-slate-900 dark:text-white">{{ evaluation.teamwork || '—' }}</div>
              <div class="text-xs text-slate-500">Teamwork</div>
            </div>
            <div class="text-center p-3 bg-slate-50 dark:bg-slate-800 rounded-lg">
              <div class="text-lg font-bold text-slate-900 dark:text-white">{{ evaluation.attendance_punctuality || '—' }}</div>
              <div class="text-xs text-slate-500">Attendance</div>
            </div>
          </div>
          
          <div v-if="evaluation.overall_appreciation" class="border-t border-slate-100 dark:border-slate-700 pt-4 mb-4">
            <h4 class="font-medium text-slate-900 dark:text-white mb-2">Supervisor's Comments</h4>
            <p class="text-slate-600 dark:text-slate-400 text-sm">{{ evaluation.overall_appreciation }}</p>
          </div>

          <!-- Download PDF Button -->
          <div class="flex justify-end pt-4 border-t border-slate-100 dark:border-slate-700">
            <button 
              @click="downloadPDF(evaluation.id)" 
              class="btn btn-outline flex items-center gap-2"
              :disabled="downloading === evaluation.id"
            >
              <svg v-if="downloading !== evaluation.id" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
              </svg>
              <svg v-else class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"/>
              </svg>
              {{ downloading === evaluation.id ? 'Downloading...' : 'Download PDF' }}
            </button>
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
import { ChartBarIcon } from '@heroicons/vue/24/outline'

const toast = useToast()
const loading = ref(true)
const evaluations = ref([])
const downloading = ref(null)

onMounted(async () => {
  try {
    const response = await api.get('/evaluations/student/')
    evaluations.value = response.data?.results || (Array.isArray(response.data) ? response.data : [])
  } catch (error) {
    console.error('Failed to load evaluations:', error)
    evaluations.value = []
  } finally {
    loading.value = false
  }
})

const downloadPDF = async (evaluationId) => {
  downloading.value = evaluationId
  try {
    const response = await api.get(`/evaluations/${evaluationId}/pdf/`, {
      responseType: 'blob'
    })
    
    // Create download link
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `evaluation_${evaluationId}.pdf`)
    document.body.appendChild(link)
    link.click()
    link.remove()
    window.URL.revokeObjectURL(url)
    
    toast.success('Evaluation downloaded successfully')
  } catch (error) {
    console.error('Failed to download PDF:', error)
    toast.error('Failed to download evaluation')
  } finally {
    downloading.value = null
  }
}

const getGradeColor = (grade) => {
  if (!grade) return 'text-slate-400'
  if (grade >= 16) return 'text-green-600'
  if (grade >= 14) return 'text-sky-600'
  if (grade >= 10) return 'text-amber-600'
  return 'text-red-600'
}

const getMention = (grade) => {
  if (!grade) return 'Not graded'
  if (grade >= 16) return 'Very Good'
  if (grade >= 14) return 'Good'
  if (grade >= 12) return 'Fairly Good'
  if (grade >= 10) return 'Passable'
  return 'Needs Improvement'
}
</script>

