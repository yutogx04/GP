<template>
  <div class="verify-email-page">
    <div class="container">
      <div class="verification-card">
        <div class="verification-icon" :class="status">
          <ClockIcon v-if="status === 'loading'" class="w-16 h-16 text-sky-500 animate-pulse" />
          <CheckCircleIcon v-else-if="status === 'success'" class="w-16 h-16 text-green-500" />
          <XCircleIcon v-else class="w-16 h-16 text-red-500" />
        </div>
        
        <div class="verification-content">
          <h1 v-if="status === 'loading'">Verifying Your Email</h1>
          <h1 v-else-if="status === 'success'">Email Verified!</h1>
          <h1 v-else>Verification Failed</h1>
          
          <p class="verification-message">{{ message }}</p>
          
          <div v-if="status === 'success'" class="success-actions">
            <router-link to="/login" class="btn btn-primary">
              Continue to Login
            </router-link>
          </div>
          
          <div v-else-if="status === 'error'" class="error-actions">
            <button @click="retryVerification" class="btn btn-primary">
              Try Again
            </button>
            <router-link to="/" class="btn btn-secondary">
              Go Home
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../services/api'
import { useRoute } from 'vue-router'
import { ClockIcon } from '@heroicons/vue/24/outline'
import { CheckCircleIcon, XCircleIcon } from '@heroicons/vue/24/solid'

const route = useRoute()
const status = ref('loading') // loading, success, error
const message = ref('Please wait while we verify your email address...')

onMounted(async () => {
  await verifyEmail()
})

async function verifyEmail() {
  try {
    const token = route.query.token
    if (!token) {
      throw new Error('No verification token provided')
    }

    const res = await api.get(`/auth/verify-email/?token=${token}`)
    status.value = 'success'
    message.value = res.data.detail || 'Your email has been successfully verified! You can now log in to your account.'
  } catch (error) {
    status.value = 'error'
    message.value = error.response?.data?.detail || 
                   error.response?.data?.message || 
                   'Email verification failed. The link may be invalid or expired.'
  }
}

function retryVerification() {
  status.value = 'loading'
  message.value = 'Please wait while we verify your email address...'
  verifyEmail()
}
</script>

<style scoped>
.verify-email-page {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 80vh;
  padding: 2rem 0;
}

.verification-card {
  background: var(--surface-color);
  padding: 3rem;
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-lg);
  text-align: center;
  max-width: 500px;
  width: 100%;
  border: 1px solid var(--border-color);
}

.verification-icon {
  font-size: 4rem;
  margin-bottom: 2rem;
}

.verification-icon.loading {
  animation: pulse 2s infinite;
}

.verification-icon.success {
  color: var(--success-color);
}

.verification-icon.error {
  color: var(--error-color);
}

.verification-content h1 {
  margin-bottom: 1rem;
  color: var(--text-primary);
}

.verification-message {
  color: var(--text-secondary);
  line-height: 1.6;
  margin-bottom: 2rem;
  font-size: 1.1rem;
}

.success-actions,
.error-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

@keyframes pulse {
  0% { opacity: 1; }
  50% { opacity: 0.5; }
  100% { opacity: 1; }
}

@media (max-width: 768px) {
  .verification-card {
    padding: 2rem;
    margin: 1rem;
  }
  
  .success-actions,
  .error-actions {
    flex-direction: column;
  }
  
  .success-actions .btn,
  .error-actions .btn {
    width: 100%;
  }
}
</style>