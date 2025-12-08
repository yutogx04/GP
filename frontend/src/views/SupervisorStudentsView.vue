<template>
  <div class="min-h-screen py-8 bg-slate-50 dark:bg-slate-900">
    <div class="container mx-auto px-4">
      <h1 class="text-3xl font-bold text-slate-900 dark:text-white mb-2">My Students</h1>
      <p class="text-slate-600 dark:text-slate-400 mb-8">Students assigned to you for supervision</p>

      <div v-if="loading" class="flex justify-center py-20">
        <div class="w-10 h-10 border-4 border-sky-200 border-t-sky-600 rounded-full animate-spin"></div>
      </div>

      <div v-else-if="error" class="card p-12 text-center flex flex-col items-center">
        <ExclamationTriangleIcon class="w-16 h-16 text-slate-300 dark:text-slate-600 mb-4" />
        <h3 class="text-lg font-semibold text-slate-900 dark:text-white mb-2">Failed to load students</h3>
        <p class="text-slate-600 dark:text-slate-400 mb-4">{{ error }}</p>
        <button @click="loadStudents" class="btn btn-primary">Retry</button>
      </div>

      <div v-else-if="students.length === 0" class="card p-12 text-center flex flex-col items-center">
        <AcademicCapIcon class="w-16 h-16 text-slate-300 dark:text-slate-600 mb-4" />
        <h3 class="text-lg font-semibold text-slate-900 dark:text-white mb-2">No students assigned</h3>
        <p class="text-slate-600 dark:text-slate-400">Students will appear here once assigned to your supervision</p>
      </div>

      <div v-else class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div v-for="student in students" :key="student.id" class="card p-6 hover:border-sky-500/50 transition-all">
          <div class="flex items-center gap-4 mb-4">
            <div class="w-14 h-14 bg-gradient-to-br from-sky-400 to-teal-400 rounded-full flex items-center justify-center text-white font-bold text-lg">
              {{ student.first_name?.[0] }}{{ student.last_name?.[0] }}
            </div>
            <div>
              <h3 class="font-semibold text-slate-900 dark:text-white">{{ student.first_name }} {{ student.last_name }}</h3>
              <p class="text-sm text-slate-500">{{ student.student_profile?.student_number }}</p>
            </div>
          </div>
          
          <div class="space-y-2 text-sm mb-4">
            <div class="flex items-center gap-2 text-slate-600 dark:text-slate-400">
              <AcademicCapIcon class="w-4 h-4" />
              <span>{{ student.student_profile?.niveau_etude || 'N/A' }} - {{ student.student_profile?.specialite || 'N/A' }}</span>
            </div>
            <div class="flex items-center gap-2 text-slate-600 dark:text-slate-400">
              <EnvelopeIcon class="w-4 h-4" />
              <span>{{ student.email }}</span>
            </div>
            <div class="flex items-center gap-2 text-slate-600 dark:text-slate-400">
              <PhoneIcon class="w-4 h-4" />
              <span>{{ student.student_profile?.phone || 'No phone' }}</span>
            </div>
          </div>
          
          <div class="flex gap-2 pt-4 border-t border-slate-100 dark:border-slate-700">
            <router-link :to="`/supervisor/evaluations?student=${student.id}`" class="btn btn-primary btn-sm flex-1 text-center">
              Evaluate
            </router-link>
            <button @click="contactStudent(student)" class="btn btn-outline btn-sm flex-1">
              Message
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api'
import { ExclamationTriangleIcon, AcademicCapIcon, EnvelopeIcon, PhoneIcon } from '@heroicons/vue/24/outline'

const router = useRouter()
const loading = ref(true)
const error = ref(null)
const students = ref([])

const loadStudents = async () => {
  loading.value = true
  error.value = null
  try {
    const response = await api.get('/users/supervisor/students/')
    students.value = response.data?.results || (Array.isArray(response.data) ? response.data : [])
  } catch (err) {
    console.error('Failed to load students:', err)
    error.value = err.response?.data?.detail || 'Could not load students. Please try again.'
    students.value = []
  } finally {
    loading.value = false
  }
}

onMounted(loadStudents)

const contactStudent = (student) => {
  router.push({ name: 'messages', query: { to: student.id } })
}
</script>
