<template>
  <div class="min-h-screen py-12 bg-slate-50 dark:bg-slate-900 transition-colors duration-300 flex items-center justify-center">
    <div class="container max-w-5xl mx-auto px-4">
      <div class="flex flex-col md:flex-row overflow-hidden card shadow-2xl">
        
        <!-- Login Form Section -->
        <div class="w-full md:w-1/2 p-8 md:p-12 bg-white dark:bg-slate-800">
          <div class="text-center md:text-left mb-8">
            <h1 class="text-3xl font-bold text-slate-900 dark:text-white mb-2">Welcome Back</h1>
            <p class="text-slate-600 dark:text-slate-400">Sign in to your MedIntern account</p>
          </div>

          <form @submit.prevent="handleLogin" class="space-y-6">
            <div class="space-y-1">
              <label for="username" class="block text-sm font-medium text-slate-700 dark:text-slate-300">
                Email or Student Number
              </label>
              <input
                id="username"
                v-model="form.username"
                type="text"
                class="input-field"
                placeholder="email@example.com or 123456789012"
                required
                :class="{ 'border-red-500 focus:ring-red-500': errors.username }"
              >
              <span v-if="errors.username" class="text-red-500 text-xs mt-1">{{ errors.username }}</span>
            </div>

            <div class="space-y-1">
              <div class="flex items-center justify-between">
                <label for="password" class="block text-sm font-medium text-slate-700 dark:text-slate-300">Password</label>
                <a href="#" class="text-xs font-medium text-sky-600 hover:text-sky-500 dark:text-sky-400">Forgot password?</a>
              </div>
              <input
                id="password"
                v-model="form.password"
                type="password"
                class="input-field"
                placeholder="Enter your password"
                required
                :class="{ 'border-red-500 focus:ring-red-500': errors.password }"
              >
              <span v-if="errors.password" class="text-red-500 text-xs mt-1">{{ errors.password }}</span>
            </div>

            <div v-if="errors.general" class="p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg text-red-600 dark:text-red-400 text-sm">
              {{ errors.general }}
            </div>

            <button type="submit" class="btn btn-primary w-full py-3 text-lg shadow-lg shadow-sky-500/20 hover:shadow-sky-500/30 transform hover:-translate-y-0.5 transition-all" :disabled="loading">
              <span v-if="loading" class="btn-spinner mr-2"></span>
              {{ loading ? 'Signing In...' : 'Sign In' }}
            </button>
          </form>

          <div class="mt-8 text-center text-sm text-slate-500 dark:text-slate-400">
            <p>Protected by MedIntern Security</p>
          </div>

          <!-- Demo Accounts (Optional - can be removed for prod) -->
          <div class="mt-8 pt-6 border-t border-slate-200 dark:border-slate-700">
            <h3 class="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-4 text-center">Demo Accounts</h3>
            <div class="grid grid-cols-2 gap-4">
              <div class="p-3 border border-slate-200 dark:border-slate-700 rounded-lg cursor-pointer hover:bg-slate-50 dark:hover:bg-slate-700/50 transition-colors" @click="fillDemo('student')">
                <div class="font-medium text-slate-900 dark:text-white text-sm">Student</div>
                <div class="text-xs text-slate-500 truncate">123456789012</div>
              </div>
              <div class="p-3 border border-slate-200 dark:border-slate-700 rounded-lg cursor-pointer hover:bg-slate-50 dark:hover:bg-slate-700/50 transition-colors" @click="fillDemo('hospital')">
                <div class="font-medium text-slate-900 dark:text-white text-sm">Hospital Admin</div>
                <div class="text-xs text-slate-500 truncate">admin@example.com</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Side Content -->
        <div class="hidden md:flex w-1/2 bg-gradient-to-br from-sky-600 to-teal-600 p-12 text-white items-center justify-center relative overflow-hidden">
          <div class="absolute inset-0 bg-grid-pattern opacity-10"></div>
          <div class="relative z-10 max-w-md">
            <BuildingOffice2Icon class="w-16 h-16 text-white mb-8 opacity-90" />
            <h2 class="text-3xl font-bold mb-6">Internal Access Only</h2>
            <p class="text-sky-100 text-lg mb-8 leading-relaxed">
              This portal is restricted to authorized medical students, faculty, and hospital administrators.
            </p>
            <div class="space-y-4">
              <div class="flex items-center gap-3">
                <div class="w-8 h-8 rounded-full bg-white/20 flex items-center justify-center">
                  <AcademicCapIcon class="w-5 h-5 text-white" />
                </div>
                <span class="font-medium">Students: Use your 12-digit Matricule</span>
              </div>
              <div class="flex items-center gap-3">
                <div class="w-8 h-8 rounded-full bg-white/20 flex items-center justify-center">
                  <IdentificationIcon class="w-5 h-5 text-white" />
                </div>
                <span class="font-medium">Staff: Use your professional Email</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { BuildingOffice2Icon, AcademicCapIcon, IdentificationIcon } from '@heroicons/vue/24/outline'

const router = useRouter()
const auth = useAuthStore()
const loading = ref(false)
const errors = reactive({
  username: '',
  password: '',
  general: ''
})

const form = reactive({
  username: '',
  password: ''
})

const fillDemo = (role) => {
  if (role === 'student') {
    form.username = '123456789012'
    form.password = 'password123'
  } else if (role === 'hospital') {
    form.username = 'admin@example.com'
    form.password = 'password123'
  }
}

const handleLogin = async () => {
  loading.value = true
  errors.username = ''
  errors.password = ''
  errors.general = ''

  try {
    await auth.login({
      email: form.username, // The backend serializer expects 'email' key but handles matricule logic
      password: form.password
    })
    
    // Check for forced password change
    if (auth.user?.force_password_change) {
      router.push('/settings')
    } else {
      router.push('/dashboard')
    }
  } catch (error) {
    if (error.response?.status === 401) {
      errors.general = 'Invalid credentials. Please check your Matricule/Email and Password.'
    } else {
      errors.general = 'An error occurred. Please try again.'
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.btn-spinner {
  width: 16px;
  height: 16px;
  border: 2px solid transparent;
  border-left: 2px solid currentColor;
  border-radius: 50%;
  display: inline-block;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.bg-grid-pattern {
  background-image: radial-gradient(rgba(255, 255, 255, 0.2) 1px, transparent 1px);
  background-size: 20px 20px;
}
</style>
