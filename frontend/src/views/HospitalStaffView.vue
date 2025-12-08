<template>
  <div class="min-h-screen py-8 bg-slate-50 dark:bg-slate-900">
    <div class="container mx-auto px-4">
      <div class="flex justify-between items-center mb-8">
        <div>
          <h1 class="text-3xl font-bold text-slate-900 dark:text-white">Staff Management</h1>
          <p class="text-slate-600 dark:text-slate-400">Manage supervisors and mentors at your hospital</p>
        </div>
        <button @click="openAddModal" class="btn btn-primary">+ Add Supervisor</button>
      </div>

      <div v-if="loading" class="flex justify-center py-20">
        <div class="w-10 h-10 border-4 border-sky-200 border-t-sky-600 rounded-full animate-spin"></div>
      </div>

      <div v-else-if="error" class="card p-12 text-center flex flex-col items-center">
        <ExclamationTriangleIcon class="w-16 h-16 text-slate-300 dark:text-slate-600 mb-4" />
        <h3 class="text-lg font-semibold text-slate-900 dark:text-white mb-2">Failed to load staff</h3>
        <p class="text-slate-600 dark:text-slate-400 mb-4">{{ error }}</p>
        <button @click="loadStaff" class="btn btn-primary">Retry</button>
      </div>

      <div v-else-if="staff.length === 0" class="card p-12 text-center flex flex-col items-center">
        <UserGroupIcon class="w-16 h-16 text-slate-300 dark:text-slate-600 mb-4" />
        <h3 class="text-lg font-semibold text-slate-900 dark:text-white mb-2">No staff members</h3>
        <p class="text-slate-600 dark:text-slate-400 mb-4">Add supervisors to manage interns</p>
        <button @click="openAddModal" class="btn btn-primary">Add First Supervisor</button>
      </div>

      <div v-else class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div v-for="person in staff" :key="person.id" class="card p-6">
          <div class="flex items-start justify-between mb-4">
            <div class="flex items-center gap-3">
              <div class="w-12 h-12 bg-teal-100 dark:bg-teal-900/30 rounded-full flex items-center justify-center text-teal-600 font-bold text-lg">
                {{ person.first_name?.[0] }}{{ person.last_name?.[0] }}
              </div>
              <div>
                <h3 class="font-semibold text-slate-900 dark:text-white">{{ person.first_name }} {{ person.last_name }}</h3>
                <p class="text-sm text-slate-500">{{ person.email }}</p>
              </div>
            </div>
            <div class="relative">
              <button @click="toggleMenu(person.id)" class="p-2 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-lg">
                <EllipsisVerticalIcon class="w-5 h-5 text-slate-500" />
              </button>
              <div v-if="menuOpen === person.id" class="absolute right-0 mt-1 w-36 bg-white dark:bg-slate-800 rounded-lg shadow-xl border border-slate-200 dark:border-slate-700 z-10">
                <button @click="openEditModal(person)" class="w-full px-4 py-2 text-left text-sm hover:bg-slate-50 dark:hover:bg-slate-700">
                  Edit
                </button>
                <button @click="toggleActive(person)" class="w-full px-4 py-2 text-left text-sm hover:bg-slate-50 dark:hover:bg-slate-700">
                  {{ person.is_active ? 'Deactivate' : 'Activate' }}
                </button>
                <button @click="resetPassword(person)" class="w-full px-4 py-2 text-left text-sm text-amber-600 hover:bg-slate-50 dark:hover:bg-slate-700">
                  Reset Password
                </button>
                <button @click="confirmDelete(person)" class="w-full px-4 py-2 text-left text-sm text-red-600 hover:bg-slate-50 dark:hover:bg-slate-700">
                  Delete
                </button>
              </div>
            </div>
          </div>
          
          <div class="space-y-2 text-sm">
            <div class="flex justify-between">
              <span class="text-slate-500">Students</span>
              <span class="text-slate-900 dark:text-white">{{ person.assigned_students_count || 0 }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-slate-500">Status</span>
              <span :class="person.is_active ? 'text-green-600' : 'text-red-600'">
                {{ person.is_active ? 'Active' : 'Inactive' }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Add/Edit Modal -->
    <div v-if="showModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50" @click.self="closeModal">
      <div class="bg-white dark:bg-slate-800 rounded-xl p-6 w-full max-w-md">
        <h2 class="text-xl font-bold text-slate-900 dark:text-white mb-6">
          {{ editingStaff ? 'Edit Staff Member' : 'Add New Supervisor' }}
        </h2>
        
        <form @submit.prevent="saveStaff" class="space-y-4">
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">First Name *</label>
              <input v-model="form.first_name" type="text" required class="input-field w-full">
            </div>
            <div>
              <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Last Name *</label>
              <input v-model="form.last_name" type="text" required class="input-field w-full">
            </div>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Email *</label>
            <input v-model="form.email" type="email" required :disabled="editingStaff" class="input-field w-full">
          </div>
          
          <div v-if="!editingStaff">
            <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Password *</label>
            <input v-model="form.password" type="password" required class="input-field w-full">
            <p class="text-xs text-slate-500 mt-1">User will be prompted to change password on first login</p>
          </div>
          
          <div v-if="formError" class="text-red-500 text-sm">{{ formError }}</div>
          
          <div class="flex justify-end gap-3 pt-4">
            <button type="button" @click="closeModal" class="btn btn-secondary">Cancel</button>
            <button type="submit" :disabled="saving" class="btn btn-primary">
              {{ saving ? 'Saving...' : (editingStaff ? 'Update' : 'Create') }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div class="bg-white dark:bg-slate-800 rounded-xl p-6 w-full max-w-md">
        <h2 class="text-xl font-bold text-slate-900 dark:text-white mb-4">Delete Staff Member</h2>
        <p class="text-slate-600 dark:text-slate-400 mb-6">
          Are you sure you want to delete <strong>{{ staffToDelete?.first_name }} {{ staffToDelete?.last_name }}</strong>? 
          This action cannot be undone.
        </p>
        <div class="flex justify-end gap-3">
          <button @click="showDeleteModal = false" class="btn btn-secondary">Cancel</button>
          <button @click="deleteStaff" :disabled="deleting" class="btn bg-red-600 text-white hover:bg-red-700">
            {{ deleting ? 'Deleting...' : 'Delete' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../services/api'
import { ExclamationTriangleIcon, UserGroupIcon, EllipsisVerticalIcon } from '@heroicons/vue/24/outline'

const loading = ref(true)
const error = ref(null)
const staff = ref([])
const menuOpen = ref(null)

// Modal state
const showModal = ref(false)
const editingStaff = ref(null)
const saving = ref(false)
const formError = ref('')

// Delete modal state
const showDeleteModal = ref(false)
const staffToDelete = ref(null)
const deleting = ref(false)

// Form data
const form = ref({
  first_name: '',
  last_name: '',
  email: '',
  password: ''
})

onMounted(loadStaff)

async function loadStaff() {
  loading.value = true
  error.value = null
  try {
    const response = await api.get('/users/hospital-staff/')
    staff.value = response.data?.results || response.data || []
  } catch (err) {
    console.error('Failed to load staff:', err)
    error.value = err.response?.data?.detail || 'Could not load staff. Please try again.'
  } finally {
    loading.value = false
  }
}

function toggleMenu(id) {
  menuOpen.value = menuOpen.value === id ? null : id
}

function openAddModal() {
  editingStaff.value = null
  form.value = { first_name: '', last_name: '', email: '', password: '' }
  formError.value = ''
  showModal.value = true
  menuOpen.value = null
}

function openEditModal(person) {
  editingStaff.value = person
  form.value = {
    first_name: person.first_name,
    last_name: person.last_name,
    email: person.email,
    password: ''
  }
  formError.value = ''
  showModal.value = true
  menuOpen.value = null
}

function closeModal() {
  showModal.value = false
  editingStaff.value = null
}

async function saveStaff() {
  saving.value = true
  formError.value = ''
  
  try {
    if (editingStaff.value) {
      await api.put(`/users/hospital-staff/${editingStaff.value.id}/`, form.value)
    } else {
      await api.post('/users/hospital-staff/create/', form.value)
    }
    closeModal()
    loadStaff()
  } catch (err) {
    formError.value = err.response?.data?.detail || 'Failed to save staff member'
  } finally {
    saving.value = false
  }
}

function confirmDelete(person) {
  staffToDelete.value = person
  showDeleteModal.value = true
  menuOpen.value = null
}

async function deleteStaff() {
  deleting.value = true
  try {
    await api.delete(`/users/hospital-staff/${staffToDelete.value.id}/`)
    showDeleteModal.value = false
    loadStaff()
  } catch (err) {
    alert(err.response?.data?.detail || 'Failed to delete staff member')
  } finally {
    deleting.value = false
  }
}

async function toggleActive(person) {
  menuOpen.value = null
  try {
    await api.patch(`/users/${person.id}/toggle-active/`)
    loadStaff()
  } catch (err) {
    alert('Failed to toggle status')
  }
}

async function resetPassword(person) {
  menuOpen.value = null
  try {
    await api.post(`/users/${person.id}/reset-password/`)
    alert('Password reset email sent')
  } catch (err) {
    alert('Failed to send password reset')
  }
}
</script>
