<template>
  <div class="flex gap-3">
    <!-- Export Dropdown -->
    <div class="relative">
      <button @click="showExportMenu = !showExportMenu" class="btn btn-outline flex items-center">
        <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/>
        </svg>
        Export
      </button>
      <div v-if="showExportMenu" class="absolute right-0 mt-2 w-48 bg-white dark:bg-slate-800 rounded-lg shadow-lg z-10 py-1 border dark:border-slate-700">
        <button @click="exportOffers('csv')" class="w-full px-4 py-2 text-left hover:bg-slate-100 dark:hover:bg-slate-700 text-sm text-slate-700 dark:text-slate-300">
          📄 Export as CSV
        </button>
        <button @click="exportOffers('json')" class="w-full px-4 py-2 text-left hover:bg-slate-100 dark:hover:bg-slate-700 text-sm text-slate-700 dark:text-slate-300">
          📋 Export as JSON
        </button>
      </div>
    </div>

    <!-- Import Button -->
    <button @click="showImportModal = true" class="btn btn-outline flex items-center">
      <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"/>
      </svg>
      Import
    </button>

    <!-- Import Modal -->
    <div v-if="showImportModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
      <div class="card p-6 w-full max-w-md">
        <h3 class="text-lg font-bold text-slate-900 dark:text-white mb-4">Import Offers</h3>
        
        <p class="text-sm text-slate-600 dark:text-slate-400 mb-4">
          Upload a CSV or JSON file to bulk import internship offers.
        </p>
        
        <div class="mb-4">
          <button @click="downloadTemplate" class="text-sm text-sky-500 hover:text-sky-600">
            📥 Download CSV Template
          </button>
        </div>
        
        <div class="mb-6">
          <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">
            Select File (CSV or JSON)
          </label>
          <input 
            type="file" 
            accept=".csv,.json"
            @change="onFileSelect"
            class="block w-full text-sm text-slate-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-medium file:bg-sky-50 file:text-sky-700 hover:file:bg-sky-100 dark:file:bg-sky-900/30 dark:file:text-sky-400"
          >
          <p v-if="selectedFile" class="mt-2 text-sm text-green-600">
            Selected: {{ selectedFile.name }}
          </p>
        </div>
        
        <div class="flex gap-3">
          <button @click="closeImportModal" class="btn btn-outline flex-1">Cancel</button>
          <button @click="handleImport" :disabled="!selectedFile || importing" class="btn btn-primary flex-1">
            {{ importing ? 'Importing...' : 'Import' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import api from '../services/api'
import { useToast } from 'vue-toastification'

const emit = defineEmits(['imported'])
const toast = useToast()

const showExportMenu = ref(false)
const showImportModal = ref(false)
const selectedFile = ref(null)
const importing = ref(false)

async function exportOffers(format) {
  showExportMenu.value = false
  try {
    const response = await api.get(`/internships/export/?format=${format}`, { responseType: 'blob' })
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `offers.${format}`)
    document.body.appendChild(link)
    link.click()
    link.remove()
    window.URL.revokeObjectURL(url)
    toast.success(`Offers exported as ${format.toUpperCase()}`)
  } catch (error) {
    toast.error('Export failed')
  }
}

async function downloadTemplate() {
  try {
    const response = await api.get('/internships/import/template/', { responseType: 'blob' })
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', 'import_template.csv')
    document.body.appendChild(link)
    link.click()
    link.remove()
    window.URL.revokeObjectURL(url)
  } catch (error) {
    toast.error('Failed to download template')
  }
}

function onFileSelect(event) {
  selectedFile.value = event.target.files[0]
}

function closeImportModal() {
  showImportModal.value = false
  selectedFile.value = null
}

async function handleImport() {
  if (!selectedFile.value) return
  
  importing.value = true
  const formData = new FormData()
  formData.append('file', selectedFile.value)
  
  try {
    const response = await api.post('/internships/import/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    toast.success(response.data.message || `Imported ${response.data.success} offers`)
    closeImportModal()
    emit('imported')
  } catch (error) {
    const errors = error.response?.data?.errors || ['Import failed']
    if (Array.isArray(errors)) {
      errors.slice(0, 3).forEach(err => toast.error(err))
    } else {
      toast.error('Import failed')
    }
  } finally {
    importing.value = false
  }
}

// Close export menu on click outside
function handleClickOutside(event) {
  if (showExportMenu.value && !event.target.closest('.relative')) {
    showExportMenu.value = false
  }
}
</script>
