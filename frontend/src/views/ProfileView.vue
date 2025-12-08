<template>
  <div class="min-h-screen py-8 bg-slate-50 dark:bg-slate-900">
    <div class="container mx-auto px-4 max-w-4xl">
      <!-- Header -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-slate-900 dark:text-white">My Profile</h1>
        <p class="text-slate-600 dark:text-slate-400 mt-1">Manage your personal information and documents</p>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="flex justify-center py-20">
        <div class="w-10 h-10 border-4 border-sky-200 border-t-sky-600 rounded-full animate-spin"></div>
      </div>

      <div v-else class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Left: Avatar Card -->
        <div class="lg:col-span-1">
          <div class="card p-6 text-center">
            <div class="w-28 h-28 mx-auto bg-gradient-to-br from-sky-400 to-teal-400 rounded-full flex items-center justify-center text-4xl text-white font-bold shadow-lg mb-4">
              {{ user?.first_name?.[0] || 'U' }}{{ user?.last_name?.[0] || '' }}
            </div>
            <h2 class="text-xl font-bold text-slate-900 dark:text-white">
              {{ user?.first_name }} {{ user?.last_name }}
            </h2>
            <p class="text-sky-600 dark:text-sky-400 font-medium capitalize">
              {{ user?.role?.replace('_', ' ') }}
            </p>
            
            <div class="mt-6 pt-6 border-t border-slate-100 dark:border-slate-700 space-y-3 text-left text-sm">
              <div class="flex justify-between">
                <span class="text-slate-500">Member Since</span>
                <span class="font-medium text-slate-900 dark:text-white">{{ formatDate(user?.date_joined) }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-slate-500">Email</span>
                <span :class="user?.email_verified ? 'text-green-600' : 'text-amber-600'">
                  {{ user?.email_verified ? 'Verified' : 'Not Verified' }}
                </span>
              </div>
            </div>
          </div>
        </div>

        <!-- Right: Forms -->
        <div class="lg:col-span-2 space-y-6">
          <!-- Personal Info -->
          <div class="card p-6">
            <div class="flex justify-between items-center mb-6">
              <h3 class="text-lg font-semibold text-slate-900 dark:text-white flex items-center gap-2">
                <span class="w-1 h-6 bg-sky-500 rounded-full"></span>
                Personal Information
              </h3>
              <button @click="toggleEdit" class="btn btn-sm" :class="editMode ? 'btn-secondary' : 'btn-outline'">
                {{ editMode ? 'Cancel' : 'Edit' }}
              </button>
            </div>

            <form @submit.prevent="saveProfile" class="space-y-4">
              <div class="grid grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">First Name</label>
                  <input v-model="form.first_name" type="text" class="input-field" :disabled="!editMode">
                </div>
                <div>
                  <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Last Name</label>
                  <input v-model="form.last_name" type="text" class="input-field" :disabled="!editMode">
                </div>
              </div>

              <div>
                <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Email</label>
                <input :value="user?.email" type="email" class="input-field bg-slate-100 dark:bg-slate-800" disabled>
                <p class="text-xs text-slate-500 mt-1">Email cannot be changed</p>
              </div>

              <!-- Student-specific fields -->
              <template v-if="auth.isStudent && profile">
                <div class="grid grid-cols-2 gap-4">
                  <div>
                    <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Student Number</label>
                    <input :value="profile.student_number" type="text" class="input-field bg-slate-100 dark:bg-slate-800" disabled>
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Phone</label>
                    <input v-model="form.phone" type="tel" class="input-field" :disabled="!editMode">
                  </div>
                </div>
                <div class="grid grid-cols-2 gap-4">
                  <div>
                    <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Study Level</label>
                    <select v-model="form.niveau_etude" class="input-field" :disabled="!editMode">
                      <option value="l1">Licence 1st year</option>
                      <option value="l2">Licence 2nd year</option>
                      <option value="l3">Licence 3rd year</option>
                      <option value="m1">Master 1st year</option>
                      <option value="m2">Master 2nd year</option>
                      <option value="intern">Intern</option>
                    </select>
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Specialty</label>
                    <select v-model="form.specialite" class="input-field" :disabled="!editMode">
                      <option value="general_medicine">General Medicine</option>
                      <option value="surgery">Surgery</option>
                      <option value="pediatrics">Pediatrics</option>
                      <option value="cardiology">Cardiology</option>
                      <option value="neurology">Neurology</option>
                    </select>
                  </div>
                </div>
                <div>
                  <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Faculty</label>
                  <input v-model="form.faculty" type="text" class="input-field" :disabled="!editMode">
                </div>
              </template>

              <div v-if="editMode" class="flex justify-end gap-3 pt-4">
                <button type="button" @click="toggleEdit" class="btn btn-ghost">Cancel</button>
                <button type="submit" class="btn btn-primary" :disabled="saving">
                  {{ saving ? 'Saving...' : 'Save Changes' }}
                </button>
              </div>
            </form>
          </div>

          <!-- Documents (Student only) -->
          <div v-if="auth.isStudent" class="card p-6">
            <h3 class="text-lg font-semibold text-slate-900 dark:text-white mb-6 flex items-center gap-2">
              <span class="w-1 h-6 bg-teal-500 rounded-full"></span>
              Documents
            </h3>

            <div v-if="documents.length === 0" class="text-center py-8 border-2 border-dashed border-slate-200 dark:border-slate-700 rounded-xl flex flex-col items-center">
              <DocumentIcon class="w-12 h-12 text-slate-300 dark:text-slate-600 mb-3" />
              <p class="text-slate-500">No documents uploaded yet</p>
            </div>

            <div v-else class="space-y-3 mb-6">
              <div v-for="doc in documents" :key="doc.id" class="flex items-center justify-between p-3 bg-slate-50 dark:bg-slate-800 rounded-lg">
                <div class="flex items-center gap-3">
                  <component :is="docIcons[doc.document_type] || DocumentIcon" class="w-8 h-8 text-sky-600 dark:text-sky-400" />
                  <div>
                    <p class="font-medium text-slate-900 dark:text-white">{{ doc.name }}</p>
                    <p class="text-xs text-slate-500">{{ doc.document_type }} • {{ formatDate(doc.upload_date) }}</p>
                  </div>
                </div>
                <span :class="doc.is_validated ? 'text-green-600' : 'text-amber-600'" class="text-sm font-medium flex items-center gap-1">
                  <component :is="doc.is_validated ? CheckCircleIcon : ClockIcon" class="w-4 h-4" />
                  {{ doc.is_validated ? 'Validated' : 'Pending' }}
                </span>
              </div>
            </div>

            <!-- Upload Form -->
            <div class="border-t border-slate-100 dark:border-slate-700 pt-6">
              <h4 class="font-medium text-slate-900 dark:text-white mb-4">Upload New Document</h4>
              <form @submit.prevent="uploadDocument" class="space-y-4">
                <div class="grid grid-cols-2 gap-4">
                  <div>
                    <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Document Type</label>
                    <select v-model="docForm.type" class="input-field" required>
                      <option value="">Select type...</option>
                      <option value="cv">CV</option>
                      <option value="transcript">Academic Transcript</option>
                      <option value="id_card">ID Card</option>
                      <option value="insurance">Insurance Certificate</option>
                      <option value="medical_certificate">Medical Certificate</option>
                      <option value="other">Other</option>
                    </select>
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Document Name</label>
                    <input v-model="docForm.name" type="text" class="input-field" placeholder="e.g., My CV 2024" required>
                  </div>
                </div>
                <div>
                  <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">File</label>
                  <input type="file" @change="handleFileSelect" class="input-field" accept=".pdf,.doc,.docx,.jpg,.png" required>
                  <p class="text-xs text-slate-500 mt-1">Max 5MB. Accepted: PDF, DOC, DOCX, JPG, PNG</p>
                </div>
                <button type="submit" class="btn btn-primary" :disabled="uploading">
                  {{ uploading ? 'Uploading...' : 'Upload Document' }}
                </button>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import api from '../services/api'
import { useToast } from 'vue-toastification'
import { 
  DocumentIcon, DocumentTextIcon, ChartBarIcon, IdentificationIcon, 
  ShieldCheckIcon, HeartIcon, CheckCircleIcon, ClockIcon 
} from '@heroicons/vue/24/outline'

const auth = useAuthStore()
const toast = useToast()

const loading = ref(true)
const saving = ref(false)
const uploading = ref(false)
const editMode = ref(false)
const user = ref(null)
const profile = ref(null)
const documents = ref([])

const form = reactive({
  first_name: '',
  last_name: '',
  phone: '',
  niveau_etude: '',
  specialite: '',
  faculty: ''
})

const docForm = reactive({
  type: '',
  name: '',
  file: null
})

onMounted(async () => {
  try {
    const response = await api.get('/auth/me/')
    user.value = response.data
    profile.value = response.data.student_profile || null
    
    form.first_name = user.value.first_name
    form.last_name = user.value.last_name
    
    if (profile.value) {
      form.phone = profile.value.phone || ''
      form.niveau_etude = profile.value.niveau_etude || ''
      form.specialite = profile.value.specialite || ''
      form.faculty = profile.value.faculty || ''
      
      // Load documents
      const docsRes = await api.get('/users/documents/')
      documents.value = docsRes.data
    }
  } catch (error) {
    console.error('Failed to load profile:', error)
    toast.error('Failed to load profile')
  } finally {
    loading.value = false
  }
})

const toggleEdit = () => {
  if (editMode.value) {
    // Reset form
    form.first_name = user.value.first_name
    form.last_name = user.value.last_name
    if (profile.value) {
      form.phone = profile.value.phone || ''
      form.niveau_etude = profile.value.niveau_etude || ''
      form.specialite = profile.value.specialite || ''
      form.faculty = profile.value.faculty || ''
    }
  }
  editMode.value = !editMode.value
}

const saveProfile = async () => {
  saving.value = true
  try {
    await api.patch('/auth/me/', form)
    user.value.first_name = form.first_name
    user.value.last_name = form.last_name
    toast.success('Profile updated successfully')
    editMode.value = false
  } catch (error) {
    toast.error('Failed to update profile')
  } finally {
    saving.value = false
  }
}

const handleFileSelect = (e) => {
  const file = e.target.files[0]
  if (file && file.size > 5 * 1024 * 1024) {
    toast.error('File size must be less than 5MB')
    e.target.value = ''
    return
  }
  docForm.file = file
}

const uploadDocument = async () => {
  if (!docForm.file) return
  
  uploading.value = true
  const formData = new FormData()
  formData.append('document_type', docForm.type)
  formData.append('name', docForm.name)
  formData.append('file', docForm.file)
  
  try {
    const response = await api.post('/users/documents/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    documents.value.push(response.data)
    docForm.type = ''
    docForm.name = ''
    docForm.file = null
    toast.success('Document uploaded successfully')
  } catch (error) {
    toast.error('Failed to upload document')
  } finally {
    uploading.value = false
  }
}

const formatDate = (date) => {
  if (!date) return 'N/A'
  return new Date(date).toLocaleDateString('en-US', { month: 'short', year: 'numeric' })
}

const docIcons = {
  cv: DocumentTextIcon,
  transcript: ChartBarIcon,
  id_card: IdentificationIcon,
  insurance: ShieldCheckIcon,
  medical_certificate: HeartIcon,
  other: DocumentIcon
}
</script>
