<template>
  <div class="min-h-screen flex items-center justify-center py-12 px-4 bg-slate-50 dark:bg-slate-900">
    <div class="w-full max-w-md">
      <div class="card p-8">
        <!-- Header -->
        <div class="text-center mb-8">
          <div class="w-16 h-16 mx-auto bg-gradient-to-br from-sky-500 to-teal-500 rounded-2xl flex items-center justify-center text-white text-2xl font-bold shadow-lg mb-4">
            M
          </div>
          <h1 class="text-2xl font-bold text-slate-900 dark:text-white">Reset Password</h1>
          <p class="text-slate-600 dark:text-slate-400 mt-2">Enter your email to receive a reset link</p>
        </div>

        <!-- Success State -->
        <div v-if="emailSent" class="text-center">
          <div class="w-16 h-16 mx-auto bg-green-100 dark:bg-green-900/30 rounded-full flex items-center justify-center text-3xl mb-4">
            ✉️
          </div>
          <h3 class="text-lg font-semibold text-slate-900 dark:text-white mb-2">Check Your Email</h3>
          <p class="text-slate-600 dark:text-slate-400 mb-6">
            We've sent a password reset link to<br>
            <span class="font-medium text-slate-900 dark:text-white">{{ email }}</span>
          </p>
          <p class="text-sm text-slate-500 mb-6">
            Didn't receive it? Check your spam folder or
            <button @click="emailSent = false" class="text-sky-600 hover:underline">try again</button>
          </p>
          <router-link to="/login" class="btn btn-primary w-full">Back to Login</router-link>
        </div>

        <!-- Form -->
        <form v-else @submit.prevent="handleSubmit" class="space-y-6">
          <div>
            <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">Email Address</label>
            <input
              v-model="email"
              type="email"
              required
              class="input-field"
              placeholder="you@example.com"
            >
          </div>

          <div v-if="error" class="p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg text-red-700 dark:text-red-400 text-sm">
            {{ error }}
          </div>

          <button type="submit" class="btn btn-primary w-full" :disabled="loading">
            <span v-if="loading" class="inline-block w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin mr-2"></span>
            {{ loading ? 'Sending...' : 'Send Reset Link' }}
          </button>

          <p class="text-center text-sm text-slate-600 dark:text-slate-400">
            Remember your password?
            <router-link to="/login" class="text-sky-600 hover:text-sky-700 font-medium">Sign in</router-link>
          </p>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import api from '../services/api'

const email = ref('')
const loading = ref(false)
const error = ref('')
const emailSent = ref(false)

const handleSubmit = async () => {
  loading.value = true
  error.value = ''
  
  try {
    await api.post('/auth/password-reset/', { email: email.value })
    emailSent.value = true
  } catch (err) {
    error.value = err.response?.data?.detail || 'Failed to send reset email. Please try again.'
  } finally {
    loading.value = false
  }
}
</script>
