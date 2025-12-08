<template>
  <div class="min-h-screen py-8 bg-slate-50 dark:bg-slate-900">
    <div class="container mx-auto px-4">
      <div class="flex justify-between items-center mb-8">
        <div>
          <h1 class="text-3xl font-bold text-slate-900 dark:text-white">Faculty Students</h1>
          <p class="text-slate-600 dark:text-slate-400">Manage students from your faculty</p>
        </div>
        <div class="flex gap-3">
          <input v-model="search" type="search" placeholder="Search students..." class="input-field w-64">
          <button @click="openAddModal" class="btn btn-primary">+ Add Student</button>
          <button @click="exportStudents" class="btn btn-outline">Export CSV</button>
        </div>
      </div>

      <div v-if="loading" class="flex justify-center py-20">
        <div class="w-10 h-10 border-4 border-sky-200 border-t-sky-600 rounded-full animate-spin"></div>
      </div>

      <div v-else-if="error" class="card p-12 text-center flex flex-col items-center">
        <ExclamationTriangleIcon class="w-16 h-16 text-slate-300 dark:text-slate-600 mb-4" />
        <h3 class="text-lg font-semibold text-slate-900 dark:text-white mb-2">Failed to load students</h3>
        <p class="text-slate-600 dark:text-slate-400 mb-4">{{ error }}</p>
        <button @click="loadStudents" class="btn btn-primary">Retry</button>
      </div>

      <div v-else-if="!Array.isArray(students) || students.length === 0" class="card p-12 text-center flex flex-col items-center">
        <AcademicCapIcon class="w-16 h-16 text-slate-300 dark:text-slate-600 mb-4" />
        <h3 class="text-lg font-semibold text-slate-900 dark:text-white mb-2">No students found</h3>
        <p class="text-slate-600 dark:text-slate-400 mb-4">Add your first student to get started</p>
        <button @click="openAddModal" class="btn btn-primary">Add Student</button>
      </div>

      <div v-else class="card overflow-hidden">
        <table class="w-full">
          <thead class="bg-slate-50 dark:bg-slate-800">
            <tr>
              <th class="px-6 py-4 text-left text-sm font-semibold text-slate-900 dark:text-white">Student</th>
              <th class="px-6 py-4 text-left text-sm font-semibold text-slate-900 dark:text-white">Matricule</th>
              <th class="px-6 py-4 text-left text-sm font-semibold text-slate-900 dark:text-white">Level</th>
              <th class="px-6 py-4 text-left text-sm font-semibold text-slate-900 dark:text-white">Specialty</th>
              <th class="px-6 py-4 text-left text-sm font-semibold text-slate-900 dark:text-white">Status</th>
              <th class="px-6 py-4 text-right text-sm font-semibold text-slate-900 dark:text-white">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100 dark:divide-slate-700">
            <tr v-for="student in filteredStudents" :key="student.id" class="hover:bg-slate-50 dark:hover:bg-slate-800/50">
              <td class="px-6 py-4">
                <div class="flex items-center gap-3">
                  <div class="w-10 h-10 bg-sky-100 dark:bg-sky-900/30 rounded-full flex items-center justify-center text-sky-600 font-bold">
                    {{ student.first_name?.[0] }}{{ student.last_name?.[0] }}
                  </div>
                  <div>
                    <div class="font-medium text-slate-900 dark:text-white">{{ student.first_name }} {{ student.last_name }}</div>
                    <div class="text-sm text-slate-500">{{ student.email }}</div>
                  </div>
                </div>
              </td>
              <td class="px-6 py-4 font-mono text-slate-600 dark:text-slate-400">{{ student.student_profile?.student_number }}</td>
              <td class="px-6 py-4 text-slate-600 dark:text-slate-400">{{ student.student_profile?.niveau_etude }}</td>
              <td class="px-6 py-4 text-slate-600 dark:text-slate-400">{{ student.student_profile?.specialite }}</td>
              <td class="px-6 py-4">
                <span :class="student.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'" class="px-2 py-1 rounded-full text-xs font-medium">
                  {{ student.is_active ? 'Active' : 'Inactive' }}
                </span>
              </td>
              <td class="px-6 py-4 text-right">
                <button @click="openEditModal(student)" class="text-sky-600 hover:text-sky-700 mr-3">Edit</button>
                <button @click="toggleActive(student)" class="text-slate-600 hover:text-sky-600 mr-3">
                  {{ student.is_active ? 'Deactivate' : 'Activate' }}
                </button>
                <button @click="confirmDelete(student)" class="text-red-600 hover:text-red-700">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Add/Edit Modal -->
    <div v-if="showModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50" @click.self="closeModal">
      <div class="bg-white dark:bg-slate-800 rounded-xl p-6 w-full max-w-lg max-h-[90vh] overflow-y-auto">
        <h2 class="text-xl font-bold text-slate-900 dark:text-white mb-6">
          {{ editingStudent ? 'Edit Student' : 'Add New Student' }}
        </h2>
        
        <form @submit.prevent="saveStudent" class="space-y-4">
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
            <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Email</label>
            <input v-model="form.email" type="email" :disabled="editingStudent" class="input-field w-full" placeholder="Optional">
          </div>
          
          <div v-if="!editingStudent">
            <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Password *</label>
            <input v-model="form.password" type="password" required class="input-field w-full">
          </div>
          
          <div>
            <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Student Number (Matricule) *</label>
            <input v-model="form.student_number" type="text" required maxlength="12" class="input-field w-full" placeholder="12-digit matricule">
          </div>
          
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Level</label>
              <select v-model="form.niveau_etude" class="input-field w-full">
                <option value="">Select level</option>
                <option value="L1">L1</option>
                <option value="L2">L2</option>
                <option value="L3">L3</option>
                <option value="M1">M1</option>
                <option value="M2">M2</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Specialty</label>
              <input v-model="form.specialite" type="text" class="input-field w-full">
            </div>
          </div>
          
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Faculty</label>
              <input v-model="form.faculty" type="text" class="input-field w-full">
            </div>
            <div>
              <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Phone</label>
              <input v-model="form.phone" type="tel" class="input-field w-full">
            </div>
          </div>
          
          <div v-if="formError" class="text-red-500 text-sm">{{ formError }}</div>
          
          <div class="flex justify-end gap-3 pt-4">
            <button type="button" @click="closeModal" class="btn btn-secondary">Cancel</button>
            <button type="submit" :disabled="saving" class="btn btn-primary">
              {{ saving ? 'Saving...' : (editingStudent ? 'Update' : 'Create') }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div class="bg-white dark:bg-slate-800 rounded-xl p-6 w-full max-w-md">
        <h2 class="text-xl font-bold text-slate-900 dark:text-white mb-4">Delete Student</h2>
        <p class="text-slate-600 dark:text-slate-400 mb-6">
          Are you sure you want to delete <strong>{{ studentToDelete?.first_name }} {{ studentToDelete?.last_name }}</strong>? 
          This action cannot be undone.
        </p>
        <div class="flex justify-end gap-3">
          <button @click="showDeleteModal = false" class="btn btn-secondary">Cancel</button>
          <button @click="deleteStudent" :disabled="deleting" class="btn bg-red-600 text-white hover:bg-red-700">
            {{ deleting ? 'Deleting...' : 'Delete' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '../services/api'
import { ExclamationTriangleIcon, AcademicCapIcon } from '@heroicons/vue/24/outline'

const loading = ref(true)
const error = ref(null)
const students = ref([])
const search = ref('')

// Modal state
const showModal = ref(false)
const editingStudent = ref(null)
const saving = ref(false)
const formError = ref('')

// Delete modal state
const showDeleteModal = ref(false)
const studentToDelete = ref(null)
const deleting = ref(false)

// Form data
const form = ref({
  first_name: '',
  last_name: '',
  email: '',
  password: '',
  student_number: '',
  niveau_etude: '',
  specialite: '',
  faculty: '',
  phone: ''
})

const filteredStudents = computed(() => {
  if (!Array.isArray(students.value)) return []
  if (!search.value) return students.value
  const s = search.value.toLowerCase()
  return students.value.filter(st => 
    st.first_name?.toLowerCase().includes(s) || 
    st.last_name?.toLowerCase().includes(s) ||
    st.student_profile?.student_number?.includes(s)
  )
})

onMounted(loadStudents)

async function loadStudents() {
  loading.value = true
  error.value = null
  try {
    const response = await api.get('/users/faculty/students/')
    students.value = response.data?.results || response.data || []
  } catch (err) {
    console.error('Failed to load students:', err)
    error.value = err.response?.data?.detail || 'Could not load students. Please try again.'
  } finally {
    loading.value = false
  }
}

function openAddModal() {
  editingStudent.value = null
  form.value = {
    first_name: '',
    last_name: '',
    email: '',
    password: '',
    student_number: '',
    niveau_etude: '',
    specialite: '',
    faculty: '',
    phone: ''
  }
  formError.value = ''
  showModal.value = true
}

function openEditModal(student) {
  editingStudent.value = student
  form.value = {
    first_name: student.first_name,
    last_name: student.last_name,
    email: student.email,
    password: '',
    student_number: student.student_profile?.student_number || '',
    niveau_etude: student.student_profile?.niveau_etude || '',
    specialite: student.student_profile?.specialite || '',
    faculty: student.student_profile?.faculty || '',
    phone: student.student_profile?.phone || ''
  }
  formError.value = ''
  showModal.value = true
}

function closeModal() {
  showModal.value = false
  editingStudent.value = null
}

async function saveStudent() {
  saving.value = true
  formError.value = ''
  
  try {
    if (editingStudent.value) {
      await api.put(`/users/faculty/students/${editingStudent.value.id}/`, form.value)
    } else {
      await api.post('/users/faculty/students/create/', form.value)
    }
    closeModal()
    loadStudents()
  } catch (err) {
    formError.value = err.response?.data?.detail || 'Failed to save student'
  } finally {
    saving.value = false
  }
}

function confirmDelete(student) {
  studentToDelete.value = student
  showDeleteModal.value = true
}

async function deleteStudent() {
  deleting.value = true
  try {
    await api.delete(`/users/faculty/students/${studentToDelete.value.id}/`)
    showDeleteModal.value = false
    loadStudents()
  } catch (err) {
    alert(err.response?.data?.detail || 'Failed to delete student')
  } finally {
    deleting.value = false
  }
}

async function toggleActive(student) {
  try {
    await api.patch(`/users/${student.id}/toggle-active/`)
    loadStudents()
  } catch (err) {
    alert('Failed to toggle status')
  }
}

function exportStudents() {
  const headers = ['Name', 'Email', 'Matricule', 'Level', 'Specialty', 'Status']
  const rows = students.value.map(s => [
    `${s.first_name} ${s.last_name}`,
    s.email,
    s.student_profile?.student_number || '',
    s.student_profile?.niveau_etude || '',
    s.student_profile?.specialite || '',
    s.is_active ? 'Active' : 'Inactive'
  ])
  
  const csv = [headers, ...rows].map(r => r.join(',')).join('\n')
  const blob = new Blob([csv], { type: 'text/csv' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = 'students.csv'
  a.click()
}
</script>
