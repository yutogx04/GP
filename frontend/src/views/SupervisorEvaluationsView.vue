<template>
  <div class="min-h-screen py-8 bg-slate-50 dark:bg-slate-900">
    <div class="container mx-auto px-4">
      <h1 class="text-3xl font-bold text-slate-900 dark:text-white mb-2">Evaluations</h1>
      <p class="text-slate-600 dark:text-slate-400 mb-8">Complete evaluations for your assigned students</p>

      <div v-if="loading" class="flex justify-center py-20">
        <div class="w-10 h-10 border-4 border-sky-200 border-t-sky-600 rounded-full animate-spin"></div>
      </div>

      <div v-else-if="error" class="card p-12 text-center flex flex-col items-center">
        <ExclamationTriangleIcon class="w-16 h-16 text-slate-300 dark:text-slate-600 mb-4" />
        <h3 class="text-lg font-semibold text-slate-900 dark:text-white mb-2">Failed to load evaluations</h3>
        <p class="text-slate-600 dark:text-slate-400 mb-4">{{ error }}</p>
        <button @click="loadData" class="btn btn-primary">Retry</button>
      </div>

      <!-- Pending Evaluations -->
      <div v-else>
        <h2 class="text-lg font-semibold text-slate-900 dark:text-white mb-4">Pending Evaluations</h2>
        
        <div v-if="pendingEvaluations.length === 0" class="card p-8 text-center mb-8">
          <p class="text-slate-600 dark:text-slate-400">No pending evaluations</p>
        </div>
        
        <div v-else class="grid md:grid-cols-2 gap-6 mb-8">
          <div v-for="internship in pendingEvaluations" :key="internship.id" class="card p-6">
            <div class="flex items-center gap-4 mb-4">
              <div class="w-12 h-12 bg-amber-100 dark:bg-amber-900/30 rounded-full flex items-center justify-center text-amber-600 font-bold">
                {{ internship.student?.first_name?.[0] }}{{ internship.student?.last_name?.[0] }}
              </div>
              <div>
                <h3 class="font-semibold text-slate-900 dark:text-white">{{ internship.student?.first_name }} {{ internship.student?.last_name }}</h3>
                <p class="text-sm text-slate-500">{{ internship.offer?.title }}</p>
              </div>
            </div>
            <div class="text-sm text-slate-600 dark:text-slate-400 mb-4">
              {{ formatDate(internship.start_date) }} - {{ formatDate(internship.end_date) }}
            </div>
            <button @click="openEvaluationForm(internship)" class="btn btn-primary w-full">
              Complete Evaluation
            </button>
          </div>
        </div>

        <h2 class="text-lg font-semibold text-slate-900 dark:text-white mb-4">Completed Evaluations</h2>
        
        <div v-if="completedEvaluations.length === 0" class="card p-8 text-center">
          <p class="text-slate-600 dark:text-slate-400">No completed evaluations yet</p>
        </div>
        
        <div v-else class="space-y-4">
          <div v-for="evaluation in completedEvaluations" :key="evaluation.id" class="card p-6">
            <div class="flex justify-between items-center">
              <div>
                <h3 class="font-semibold text-slate-900 dark:text-white">{{ evaluation.internship?.student?.first_name }} {{ evaluation.internship?.student?.last_name }}</h3>
                <p class="text-sm text-slate-500">{{ evaluation.internship?.offer?.title }}</p>
              </div>
              <div class="text-right">
                <div class="text-2xl font-bold text-sky-600">{{ evaluation.final_grade?.toFixed(1) }}/20</div>
                <span :class="evaluation.is_validated ? 'text-green-600' : 'text-amber-600'" class="text-sm flex items-center justify-end gap-1">
                  <CheckCircleIcon v-if="evaluation.is_validated" class="w-4 h-4" />
                  {{ evaluation.is_validated ? 'Validated' : 'Pending validation' }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Evaluation Modal -->
      <div v-if="showModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
        <div class="bg-white dark:bg-slate-800 rounded-2xl shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
          <div class="p-6 border-b border-slate-200 dark:border-slate-700">
            <h3 class="text-xl font-bold text-slate-900 dark:text-white">Evaluation Form</h3>
            <p class="text-slate-600 dark:text-slate-400">{{ selectedInternship?.student?.first_name }} {{ selectedInternship?.student?.last_name }}</p>
          </div>
          
          <form @submit.prevent="submitEvaluation" class="p-6 space-y-6">
            <div class="grid grid-cols-2 gap-4">
              <div v-for="field in gradeFields" :key="field.key">
                <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">{{ field.label }}</label>
                <input v-model.number="evaluationForm[field.key]" type="number" min="0" max="20" step="0.5" class="input-field" required>
              </div>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Overall Comments</label>
              <textarea v-model="evaluationForm.overall_appreciation" rows="4" class="input-field" placeholder="Provide detailed feedback..."></textarea>
            </div>
            
            <div class="flex items-center gap-2">
              <input v-model="evaluationForm.supervisor_signature" type="checkbox" id="signature" class="w-4 h-4">
              <label for="signature" class="text-sm text-slate-700 dark:text-slate-300">I confirm this evaluation (Digital Signature)</label>
            </div>
            
            <div class="flex gap-3 pt-4 border-t border-slate-200 dark:border-slate-700">
              <button type="button" @click="showModal = false" class="btn btn-ghost flex-1">Cancel</button>
              <button type="submit" class="btn btn-primary flex-1" :disabled="submitting">
                {{ submitting ? 'Submitting...' : 'Submit Evaluation' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import api from '../services/api'
import { useToast } from 'vue-toastification'

import { ExclamationTriangleIcon, CheckCircleIcon } from '@heroicons/vue/24/outline'

const toast = useToast()
const loading = ref(true)
const error = ref(null)
const showModal = ref(false)
const submitting = ref(false)
const internships = ref([])
const evaluations = ref([])
const selectedInternship = ref(null)

const gradeFields = [
  { key: 'technical_skills', label: 'Technical Skills (0-20)' },
  { key: 'attendance_punctuality', label: 'Attendance (0-20)' },
  { key: 'patient_relation', label: 'Patient Relations (0-20)' },
  { key: 'teamwork', label: 'Teamwork (0-20)' },
  { key: 'initiative_autonomy', label: 'Initiative (0-20)' },
  { key: 'theoretical_knowledge', label: 'Theory (0-20)' }
]

const evaluationForm = reactive({
  technical_skills: null,
  attendance_punctuality: null,
  patient_relation: null,
  teamwork: null,
  initiative_autonomy: null,
  theoretical_knowledge: null,
  overall_appreciation: '',
  supervisor_signature: false
})

const pendingEvaluations = computed(() => {
  if (!Array.isArray(internships.value) || !Array.isArray(evaluations.value)) return []
  return internships.value.filter(i => !evaluations.value.find(e => e.internship?.id === i.id))
})

const completedEvaluations = computed(() => {
  if (!Array.isArray(evaluations.value)) return []
  return evaluations.value
})

const loadData = async () => {
  loading.value = true
  error.value = null
  try {
    const [intRes, evalRes] = await Promise.all([
      api.get('/internships/supervisor/'),
      api.get('/evaluations/supervisor/')
    ])
    internships.value = intRes.data || []
    evaluations.value = evalRes.data || []
  } catch (err) {
    console.error('Failed to load data:', err)
    error.value = err.response?.data?.detail || 'Could not load evaluations. Please try again.'
  } finally {
    loading.value = false
  }
}

onMounted(loadData)

const openEvaluationForm = (internship) => {
  selectedInternship.value = internship
  Object.keys(evaluationForm).forEach(key => {
    evaluationForm[key] = key === 'supervisor_signature' ? false : key === 'overall_appreciation' ? '' : null
  })
  showModal.value = true
}

const submitEvaluation = async () => {
  if (!evaluationForm.supervisor_signature) {
    toast.warning('Please confirm with your digital signature')
    return
  }
  
  submitting.value = true
  try {
    const response = await api.post('/evaluations/', {
      internship: selectedInternship.value.id,
      ...evaluationForm
    })
    evaluations.value.push(response.data)
    showModal.value = false
    toast.success('Evaluation submitted successfully')
  } catch (err) {
    toast.error('Failed to submit evaluation')
  } finally {
    submitting.value = false
  }
}

const formatDate = (date) => date ? new Date(date).toLocaleDateString() : 'N/A'
</script>
