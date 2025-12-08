<template>
  <div class="card p-6 flex flex-col h-full hover:border-sky-500/50 transition-all duration-300 group">
    <div class="mb-4">
      <div class="flex justify-between items-start mb-2">
        <h3 class="text-xl font-bold text-slate-900 dark:text-white line-clamp-1 group-hover:text-sky-600 dark:group-hover:text-sky-400 transition-colors">
          {{ internship.title }}
        </h3>
        <span :class="`px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(internship.status)}`">
          {{ internship.status }}
        </span>
      </div>
      <div class="flex items-center gap-2 text-sm text-slate-500 dark:text-slate-400">
        <span class="flex items-center gap-1">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
          </svg>
          {{ internship.available_slots }} slots
        </span>
      </div>
    </div>

    <div class="flex-1 space-y-4 mb-6">
      <p class="text-slate-600 dark:text-slate-300 text-sm line-clamp-2">
        {{ internship.description }}
      </p>
      
      <div class="space-y-2">
        <div class="flex items-center gap-3 text-sm text-slate-600 dark:text-slate-400">
          <span class="w-5 text-center">🏥</span>
          <span class="font-medium">{{ internship.hospital_name }}</span>
        </div>
        <div class="flex items-center gap-3 text-sm text-slate-600 dark:text-slate-400">
          <span class="w-5 text-center">📋</span>
          <span>{{ internship.department_name }}</span>
        </div>
        <div class="flex items-center gap-3 text-sm text-slate-600 dark:text-slate-400">
          <span class="w-5 text-center">📅</span>
          <span>{{ formatDate(internship.start_date) }} - {{ formatDate(internship.end_date) }}</span>
        </div>
      </div>
    </div>

    <div class="pt-4 border-t border-slate-100 dark:border-slate-700 flex items-center justify-between gap-4">
      <router-link :to="`/internships/${internship.id}`" class="btn btn-outline btn-sm flex-1 text-center">
        Details
      </router-link>
      
      <button 
        v-if="auth.isStudent && !hasApplied" 
        @click="$emit('apply', internship)"
        class="btn btn-primary btn-sm flex-1"
        :disabled="applying"
      >
        {{ applying ? 'Applying...' : 'Apply Now' }}
      </button>
      
      <span v-else-if="auth.isStudent" class="flex-1 text-center px-4 py-2 bg-green-50 text-green-700 dark:bg-green-900/20 dark:text-green-400 rounded-lg text-sm font-medium border border-green-200 dark:border-green-900/50">
        ✓ Applied
      </span>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useAuthStore } from '../stores/auth'

const props = defineProps({
  internship: {
    type: Object,
    required: true
  },
  userApplications: {
    type: Array,
    default: () => []
  },
  applying: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['apply'])
const auth = useAuthStore()

const hasApplied = computed(() => {
  return props.userApplications.some(app => app.offer.id === props.internship.id)
})

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  })
}

const getStatusColor = (status) => {
  return status === 'open' 
    ? 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400'
    : 'bg-slate-100 text-slate-800 dark:bg-slate-700 dark:text-slate-300'
}
</script>