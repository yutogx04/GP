<template>
  <div class="min-h-screen py-8 bg-slate-50 dark:bg-slate-900">
    <div class="container mx-auto px-4">
      <!-- Header -->
      <div class="flex justify-between items-center mb-8">
        <div>
          <h1 class="text-3xl font-bold text-slate-900 dark:text-white">Assignment Board</h1>
          <p class="text-slate-600 dark:text-slate-400">Drag and drop applications to change their status</p>
        </div>
        <button @click="calculateScores" :disabled="calculating" class="btn btn-outline flex items-center gap-2">
          <CalculatorIcon class="w-5 h-5" />
          {{ calculating ? 'Calculating...' : 'Calculate Scores' }}
        </button>
      </div>

      <div v-if="loading" class="flex justify-center py-20">
        <div class="w-10 h-10 border-4 border-sky-200 border-t-sky-600 rounded-full animate-spin"></div>
      </div>

      <!-- Kanban Board -->
      <div v-else class="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div 
          v-for="column in columns" 
          :key="column.status"
          class="bg-white dark:bg-slate-800 rounded-xl shadow-sm border border-slate-200 dark:border-slate-700"
        >
          <!-- Column Header -->
          <div class="p-4 border-b border-slate-200 dark:border-slate-700 flex items-center gap-2">
            <component :is="column.icon" class="w-5 h-5" />
            <div>
              <h3 class="font-semibold text-slate-900 dark:text-white">{{ column.title }}</h3>
              <span class="text-xs text-slate-500">{{ applications[column.status]?.length || 0 }} items</span>
            </div>
          </div>

          <!-- Droppable Area -->
          <div 
            class="p-3 min-h-96 space-y-3"
            @dragover.prevent
            @dragenter.prevent="onDragEnter($event, column.status)"
            @dragleave="onDragLeave($event)"
            @drop="onDrop($event, column.status)"
            :class="{ 'bg-sky-50 dark:bg-sky-900/20': dragOverColumn === column.status }"
          >
            <!-- Application Cards -->
            <div 
              v-for="app in applications[column.status]" 
              :key="app.id"
              draggable="true"
              @dragstart="onDragStart($event, app)"
              @dragend="onDragEnd"
              class="bg-slate-50 dark:bg-slate-700/50 rounded-lg p-3 cursor-move hover:shadow-md transition-shadow border border-transparent hover:border-sky-500/30"
            >
              <div class="flex justify-between items-start mb-2">
                <h4 class="font-medium text-slate-900 dark:text-white text-sm line-clamp-1">
                  {{ app.offer_title }}
                </h4>
                <span v-if="app.score" class="text-xs bg-sky-100 dark:bg-sky-900/30 text-sky-700 dark:text-sky-300 px-2 py-0.5 rounded-full">
                  {{ app.score?.toFixed(1) }}
                </span>
              </div>
              <p class="text-sm text-slate-600 dark:text-slate-400 mb-2">{{ app.student_name }}</p>
              <div class="flex items-center justify-between text-xs text-slate-500">
                <span>{{ app.hospital }}</span>
                <span v-if="app.priority" class="bg-amber-100 dark:bg-amber-900/30 text-amber-700 dark:text-amber-300 px-1.5 py-0.5 rounded">
                  P{{ app.priority }}
                </span>
              </div>
            </div>

            <!-- Empty State -->
            <div v-if="!applications[column.status]?.length" class="text-center py-8 text-slate-400 text-sm">
              No applications
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../services/api'
import { useToast } from 'vue-toastification'
import { ClockIcon, EyeIcon, CheckCircleIcon, XCircleIcon, CalculatorIcon } from '@heroicons/vue/24/outline'

const toast = useToast()
const loading = ref(true)
const calculating = ref(false)
const applications = ref({
  pending: [],
  reviewing: [],
  accepted: [],
  rejected: []
})

const draggedApp = ref(null)
const dragOverColumn = ref(null)

const columns = [
  { status: 'pending', title: 'Pending', icon: ClockIcon, iconBg: 'bg-amber-100 dark:bg-amber-900/30' },
  { status: 'reviewing', title: 'Reviewing', icon: EyeIcon, iconBg: 'bg-blue-100 dark:bg-blue-900/30' },
  { status: 'accepted', title: 'Accepted', icon: CheckCircleIcon, iconBg: 'bg-green-100 dark:bg-green-900/30' },
  { status: 'rejected', title: 'Rejected', icon: XCircleIcon, iconBg: 'bg-red-100 dark:bg-red-900/30' }
]

onMounted(loadBoard)

async function loadBoard() {
  loading.value = true
  try {
    const response = await api.get('/applications/board/')
    applications.value = response.data
  } catch (error) {
    console.error('Failed to load board:', error)
    toast.error('Failed to load assignment board')
  } finally {
    loading.value = false
  }
}

async function calculateScores() {
  calculating.value = true
  try {
    await api.post('/applications/calculate-scores/')
    toast.success('Scores calculated')
    loadBoard()
  } catch (error) {
    toast.error('Failed to calculate scores')
  } finally {
    calculating.value = false
  }
}

function onDragStart(event, app) {
  draggedApp.value = app
  event.dataTransfer.effectAllowed = 'move'
  event.target.classList.add('opacity-50')
}

function onDragEnd(event) {
  event.target.classList.remove('opacity-50')
  draggedApp.value = null
  dragOverColumn.value = null
}

function onDragEnter(event, status) {
  dragOverColumn.value = status
}

function onDragLeave(event) {
  // Only clear if leaving the column entirely
  if (!event.currentTarget.contains(event.relatedTarget)) {
    dragOverColumn.value = null
  }
}

async function onDrop(event, newStatus) {
  dragOverColumn.value = null
  
  if (!draggedApp.value || draggedApp.value.status === newStatus) return
  
  const app = draggedApp.value
  const oldStatus = app.status

  // Optimistic update
  const idx = applications.value[oldStatus].findIndex(a => a.id === app.id)
  if (idx !== -1) {
    applications.value[oldStatus].splice(idx, 1)
    app.status = newStatus
    applications.value[newStatus].push(app)
  }

  try {
    await api.patch('/applications/bulk-update/', {
      updates: [{ id: app.id, status: newStatus }]
    })
    toast.success(`Moved to ${newStatus}`)
  } catch (error) {
    // Revert on error
    const revertIdx = applications.value[newStatus].findIndex(a => a.id === app.id)
    if (revertIdx !== -1) {
      applications.value[newStatus].splice(revertIdx, 1)
      app.status = oldStatus
      applications.value[oldStatus].push(app)
    }
    toast.error('Failed to update status')
  }
}
</script>
