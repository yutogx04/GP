<template>
  <div class="min-h-screen py-8 bg-slate-50 dark:bg-slate-900 transition-colors duration-300">
    <div class="container mx-auto px-4 sm:px-6 lg:px-8 max-w-4xl">
      <h1 class="text-3xl font-bold text-slate-900 dark:text-white mb-2">{{ t('settings.title') }}</h1>
      <p class="text-slate-600 dark:text-slate-400 mb-8">{{ t('settings.subtitle') }}</p>

      <div class="flex flex-col md:flex-row gap-8">
        <!-- Sidebar Navigation -->
        <div class="md:w-1/4">
          <div class="card p-4 space-y-2">
            <button 
              @click="activeTab = 'general'"
              :class="['w-full text-left px-4 py-2 rounded-lg transition-colors', activeTab === 'general' ? 'bg-sky-50 text-sky-700 dark:bg-sky-900/30 dark:text-sky-400 font-medium' : 'text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800']"
            >
              General
            </button>
            <button 
              @click="activeTab = 'security'"
              :class="['w-full text-left px-4 py-2 rounded-lg transition-colors', activeTab === 'security' ? 'bg-sky-50 text-sky-700 dark:bg-sky-900/30 dark:text-sky-400 font-medium' : 'text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800']"
            >
              {{ t('settings.security') }}
            </button>
            <button 
              @click="activeTab = 'notifications'"
              :class="['w-full text-left px-4 py-2 rounded-lg transition-colors', activeTab === 'notifications' ? 'bg-sky-50 text-sky-700 dark:bg-sky-900/30 dark:text-sky-400 font-medium' : 'text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800']"
            >
              {{ t('settings.notifications') }}
            </button>
          </div>
        </div>

        <!-- Content Area -->
        <div class="md:w-3/4">
          <!-- General Settings -->
          <div v-if="activeTab === 'general'" class="card p-6 space-y-8">
            <div>
              <h2 class="text-xl font-semibold text-slate-900 dark:text-white mb-4">{{ t('settings.appearance') }}</h2>
              <div class="flex items-center justify-between p-4 border border-slate-200 dark:border-slate-700 rounded-lg">
                <div>
                  <div class="font-medium text-slate-900 dark:text-white">{{ t('settings.theme') }}</div>
                  <div class="text-sm text-slate-500 dark:text-slate-400">Switch between light and dark themes</div>
                </div>
                <ThemeToggle />
              </div>
            </div>

            <div>
              <h2 class="text-xl font-semibold text-slate-900 dark:text-white mb-4">{{ t('settings.language') }}</h2>
              <div class="space-y-3">
                <div 
                  v-for="lang in languages" 
                  :key="lang.code"
                  @click="changeLanguage(lang.code)"
                  :class="[
                    'flex items-center justify-between p-4 border rounded-lg cursor-pointer transition-all',
                    locale === lang.code 
                      ? 'border-sky-500 bg-sky-50 dark:bg-sky-900/20' 
                      : 'border-slate-200 dark:border-slate-700 hover:border-sky-300 dark:hover:border-sky-700'
                  ]"
                >
                  <div class="flex items-center gap-3">
                    <span class="text-2xl">{{ lang.flag }}</span>
                    <div>
                      <div class="font-medium text-slate-900 dark:text-white">{{ lang.name }}</div>
                      <div class="text-sm text-slate-500 dark:text-slate-400">{{ lang.native }}</div>
                    </div>
                  </div>
                  <div v-if="locale === lang.code" class="w-5 h-5 bg-sky-500 rounded-full flex items-center justify-center">
                    <svg class="w-3 h-3 text-white" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                    </svg>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Security Settings -->
          <div v-if="activeTab === 'security'" class="card p-6 space-y-8">
            <div>
              <h2 class="text-xl font-semibold text-slate-900 dark:text-white mb-4">{{ t('settings.password') }}</h2>
              <p class="text-sm text-slate-500 dark:text-slate-400 mb-6">
                Ensure your account is using a long, random password to stay secure.
              </p>

              <form @submit.prevent="handleChangePassword" class="space-y-4">
                <div class="space-y-1">
                  <label class="block text-sm font-medium text-slate-700 dark:text-slate-300">{{ t('settings.password.current') }}</label>
                  <input 
                    v-model="passwordForm.old_password" 
                    type="password" 
                    class="input-field"
                    required
                  >
                </div>

                <div class="space-y-1">
                  <label class="block text-sm font-medium text-slate-700 dark:text-slate-300">{{ t('settings.password.new') }}</label>
                  <input 
                    v-model="passwordForm.new_password" 
                    type="password" 
                    class="input-field"
                    required
                    minlength="8"
                  >
                </div>

                <div class="space-y-1">
                  <label class="block text-sm font-medium text-slate-700 dark:text-slate-300">{{ t('settings.password.confirm') }}</label>
                  <input 
                    v-model="passwordForm.confirm_password" 
                    type="password" 
                    class="input-field"
                    required
                  >
                </div>

                <div v-if="passwordMessage" :class="['p-3 rounded-lg text-sm', passwordSuccess ? 'bg-green-50 text-green-700 dark:bg-green-900/20 dark:text-green-400' : 'bg-red-50 text-red-700 dark:bg-red-900/20 dark:text-red-400']">
                  {{ passwordMessage }}
                </div>

                <div class="pt-4">
                  <button 
                    type="submit" 
                    class="btn btn-primary"
                    :disabled="loading"
                  >
                    <span v-if="loading" class="btn-spinner mr-2"></span>
                    {{ loading ? t('common.loading') : t('settings.password.update') }}
                  </button>
                </div>
              </form>
            </div>
          </div>

          <!-- Notification Settings -->
          <div v-if="activeTab === 'notifications'" class="card p-6 space-y-6">
            <h2 class="text-xl font-semibold text-slate-900 dark:text-white mb-4">{{ t('settings.notifications') }}</h2>
            
            <div class="space-y-4">
              <div class="flex items-center justify-between p-4 border border-slate-200 dark:border-slate-700 rounded-lg">
                <div>
                  <div class="font-medium text-slate-900 dark:text-white">{{ t('settings.notifications.email') }}</div>
                  <div class="text-sm text-slate-500 dark:text-slate-400">Receive email notifications for important updates</div>
                </div>
                <label class="relative inline-flex items-center cursor-pointer">
                  <input v-model="notificationSettings.email" type="checkbox" class="sr-only peer">
                  <div class="w-11 h-6 bg-slate-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-sky-300 dark:peer-focus:ring-sky-800 rounded-full peer dark:bg-slate-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-slate-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-slate-600 peer-checked:bg-sky-600"></div>
                </label>
              </div>
              
              <div class="flex items-center justify-between p-4 border border-slate-200 dark:border-slate-700 rounded-lg">
                <div>
                  <div class="font-medium text-slate-900 dark:text-white">{{ t('settings.notifications.push') }}</div>
                  <div class="text-sm text-slate-500 dark:text-slate-400">Receive push notifications in your browser</div>
                </div>
                <label class="relative inline-flex items-center cursor-pointer">
                  <input v-model="notificationSettings.push" type="checkbox" class="sr-only peer">
                  <div class="w-11 h-6 bg-slate-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-sky-300 dark:peer-focus:ring-sky-800 rounded-full peer dark:bg-slate-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-slate-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-slate-600 peer-checked:bg-sky-600"></div>
                </label>
              </div>

              <div class="flex items-center justify-between p-4 border border-slate-200 dark:border-slate-700 rounded-lg">
                <div>
                  <div class="font-medium text-slate-900 dark:text-white">Application Updates</div>
                  <div class="text-sm text-slate-500 dark:text-slate-400">Get notified when your application status changes</div>
                </div>
                <label class="relative inline-flex items-center cursor-pointer">
                  <input v-model="notificationSettings.applications" type="checkbox" class="sr-only peer">
                  <div class="w-11 h-6 bg-slate-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-sky-300 dark:peer-focus:ring-sky-800 rounded-full peer dark:bg-slate-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-slate-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-slate-600 peer-checked:bg-sky-600"></div>
                </label>
              </div>
            </div>

            <button @click="saveNotificationSettings" class="btn btn-primary">
              {{ t('common.save') }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import ThemeToggle from '../components/ThemeToggle.vue'
import api from '../services/api'
import { useAuthStore } from '../stores/auth'
import { useI18n } from '../i18n'
import { useToast } from 'vue-toastification'

const { t, locale, setLocale } = useI18n()
const toast = useToast()
const auth = useAuthStore()

const activeTab = ref('general')
const loading = ref(false)
const passwordMessage = ref('')
const passwordSuccess = ref(false)

const languages = [
  { code: 'en', name: 'English', native: 'English', flag: '🇬🇧' },
  { code: 'fr', name: 'French', native: 'Français', flag: '🇫🇷' }
]

const notificationSettings = reactive({
  email: true,
  push: true,
  applications: true
})

const passwordForm = reactive({
  old_password: '',
  new_password: '',
  confirm_password: ''
})

const changeLanguage = (code) => {
  setLocale(code)
  toast.success(code === 'fr' ? 'Langue changée en Français' : 'Language changed to English')
}

const handleChangePassword = async () => {
  if (passwordForm.new_password !== passwordForm.confirm_password) {
    passwordMessage.value = "New passwords do not match"
    passwordSuccess.value = false
    return
  }

  loading.value = true
  passwordMessage.value = ''

  try {
    await api.put('/auth/change-password/', {
      old_password: passwordForm.old_password,
      new_password: passwordForm.new_password
    })
    
    passwordMessage.value = "Password updated successfully"
    passwordSuccess.value = true
    
    passwordForm.old_password = ''
    passwordForm.new_password = ''
    passwordForm.confirm_password = ''
    
    if (auth.user?.force_password_change) {
      auth.user.force_password_change = false
    }
  } catch (error) {
    passwordMessage.value = error.response?.data?.old_password?.[0] || "Failed to update password"
    passwordSuccess.value = false
  } finally {
    loading.value = false
  }
}

const saveNotificationSettings = () => {
  toast.success('Notification settings saved')
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
</style>
