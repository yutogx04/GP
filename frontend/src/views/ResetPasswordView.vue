<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 py-12 px-4">
    <div class="max-w-md w-full">
      <!-- Logo -->
      <div class="text-center mb-8">
        <router-link to="/" class="inline-block">
          <span class="text-3xl font-bold">
            <span class="text-sky-400">Med</span><span class="text-white">Intern</span>
          </span>
        </router-link>
      </div>

      <!-- Reset Password Card -->
      <div class="card p-8">
        <!-- Success State -->
        <div v-if="success" class="text-center">
          <div class="w-16 h-16 bg-green-100 dark:bg-green-900/30 rounded-full flex items-center justify-center mx-auto mb-4">
            <CheckCircleIcon class="w-8 h-8 text-green-600 dark:text-green-400" />
          </div>
          <h1 class="text-2xl font-bold text-slate-900 dark:text-white mb-2">Password Reset!</h1>
          <p class="text-slate-600 dark:text-slate-400 mb-6">Your password has been successfully reset. You can now log in with your new password.</p>
          <router-link to="/login" class="btn btn-primary w-full">Go to Login</router-link>
        </div>

        <!-- Reset Form -->
        <div v-else>
          <h1 class="text-2xl font-bold text-slate-900 dark:text-white mb-2">Reset Password</h1>
          <p class="text-slate-600 dark:text-slate-400 mb-6">Enter your new password below.</p>

          <form @submit.prevent="handleSubmit" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">New Password</label>
              <input 
                v-model="form.password" 
                type="password" 
                class="input-field" 
                placeholder="Enter new password"
                minlength="8"
                required
              >
            </div>

            <div>
              <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Confirm Password</label>
              <input 
                v-model="form.confirmPassword" 
                type="password" 
                class="input-field" 
                placeholder="Confirm new password"
                required
              >
            </div>

            <div v-if="error" class="p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg text-red-600 dark:text-red-400 text-sm">
              {{ error }}
            </div>

            <button type="submit" class="btn btn-primary w-full" :disabled="loading">
              <span v-if="loading" class="mr-2">
                <svg class="animate-spin h-4 w-4 inline" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none"/>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"/>
                </svg>
              </span>
              {{ loading ? 'Resetting...' : 'Reset Password' }}
            </button>
          </form>

          <div class="mt-6 text-center">
            <router-link to="/login" class="text-sm text-sky-500 hover:text-sky-400">Back to Login</router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '../services/api'
import { useToast } from 'vue-toastification'
import { CheckCircleIcon } from '@heroicons/vue/24/solid'

const route = useRoute()
const router = useRouter()
const toast = useToast()

const form = ref({
  password: '',
  confirmPassword: ''
})
const loading = ref(false)
const error = ref('')
const success = ref(false)

const uid = ref('')
const token = ref('')

onMounted(() => {
  uid.value = route.query.uid
  token.value = route.query.token
  
  if (!uid.value || !token.value) {
    error.value = 'Invalid or missing reset link parameters'
  }
})

async function handleSubmit() {
  error.value = ''
  
  if (form.value.password !== form.value.confirmPassword) {
    error.value = 'Passwords do not match'
    return
  }
  
  if (form.value.password.length < 8) {
    error.value = 'Password must be at least 8 characters'
    return
  }
  
  loading.value = true
  
  try {
    await api.post('/auth/password-reset-confirm/', {
      uid: uid.value,
      token: token.value,
      new_password: form.value.password
    })
    
    success.value = true
    toast.success('Password reset successfully!')
  } catch (err) {
    error.value = err.response?.data?.detail || 'Password reset failed. The link may have expired.'
  } finally {
    loading.value = false
  }
}
</script>
