<template>
  <div class="min-h-screen py-8 bg-slate-50 dark:bg-slate-900">
    <div class="container mx-auto px-4">
      <!-- Header -->
      <div class="flex justify-between items-center mb-8">
        <div>
          <h1 class="text-3xl font-bold text-slate-900 dark:text-white">My Calendar</h1>
          <p class="text-slate-600 dark:text-slate-400">View and manage your internship schedule</p>
        </div>
        <div class="flex gap-3">
          <button @click="exportCalendar" class="btn btn-outline flex items-center gap-2">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/>
            </svg>
            Export iCal
          </button>
          <button @click="showAddModal = true" class="btn btn-primary flex items-center gap-2">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
            </svg>
            Add Event
          </button>
        </div>
      </div>

      <!-- View Toggle -->
      <div class="flex gap-2 mb-6">
        <button 
          v-for="view in ['month', 'week', 'day']" 
          :key="view"
          @click="currentView = view"
          :class="currentView === view ? 'btn-primary' : 'btn-outline'"
          class="btn capitalize"
        >{{ view }}</button>
      </div>

      <!-- Month Navigation -->
      <div class="flex items-center justify-between mb-6">
        <button @click="prevPeriod" class="btn btn-outline">← Previous</button>
        <h2 class="text-xl font-bold text-slate-900 dark:text-white">{{ periodLabel }}</h2>
        <button @click="nextPeriod" class="btn btn-outline">Next →</button>
      </div>

      <!-- Calendar Grid -->
      <div v-if="loading" class="flex justify-center py-20">
        <div class="w-10 h-10 border-4 border-sky-200 border-t-sky-600 rounded-full animate-spin"></div>
      </div>

      <div v-else class="card overflow-hidden">
        <!-- Week Headers -->
        <div class="grid grid-cols-7 bg-slate-100 dark:bg-slate-800">
          <div v-for="day in weekDays" :key="day" class="p-3 text-center text-sm font-semibold text-slate-600 dark:text-slate-300">
            {{ day }}
          </div>
        </div>

        <!-- Calendar Days -->
        <div class="grid grid-cols-7">
          <div 
            v-for="(day, idx) in calendarDays" 
            :key="idx"
            class="min-h-24 p-2 border-t border-r border-slate-100 dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-800/50"
            :class="{ 'bg-slate-50 dark:bg-slate-800/30': !day.isCurrentMonth, 'bg-sky-50 dark:bg-sky-900/20': day.isToday }"
          >
            <div class="text-sm font-medium" :class="day.isToday ? 'text-sky-600' : day.isCurrentMonth ? 'text-slate-900 dark:text-white' : 'text-slate-400'">
              {{ day.date }}
            </div>
            <!-- Events for this day -->
            <div class="mt-1 space-y-1">
              <div 
                v-for="event in getEventsForDay(day.fullDate)" 
                :key="event.id"
                @click="editEvent(event)"
                class="text-xs p-1 rounded truncate cursor-pointer"
                :class="getEventColor(event.event_type)"
              >
                {{ event.start_time?.slice(0, 5) }} {{ event.title }}
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Add/Edit Event Modal -->
      <div v-if="showAddModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
        <div class="card p-6 w-full max-w-md">
          <h3 class="text-lg font-bold text-slate-900 dark:text-white mb-4">
            {{ editingEvent ? 'Edit Event' : 'Add Event' }}
          </h3>
          
          <form @submit.prevent="saveEvent" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Title</label>
              <input v-model="eventForm.title" type="text" class="input-field" required>
            </div>
            
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Date</label>
                <input v-model="eventForm.date" type="date" class="input-field" required>
              </div>
              <div>
                <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Type</label>
                <select v-model="eventForm.event_type" class="input-field">
                  <option value="shift">Shift</option>
                  <option value="meeting">Meeting</option>
                  <option value="training">Training</option>
                  <option value="evaluation">Evaluation</option>
                  <option value="other">Other</option>
                </select>
              </div>
            </div>
            
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Start Time</label>
                <input v-model="eventForm.start_time" type="time" class="input-field" required>
              </div>
              <div>
                <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">End Time</label>
                <input v-model="eventForm.end_time" type="time" class="input-field" required>
              </div>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Location</label>
              <input v-model="eventForm.location" type="text" class="input-field" placeholder="Optional">
            </div>
            
            <div>
              <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Description</label>
              <textarea v-model="eventForm.description" class="input-field" rows="2" placeholder="Optional"></textarea>
            </div>
            
            <div class="flex gap-3 pt-4">
              <button type="button" @click="closeModal" class="btn btn-outline flex-1">Cancel</button>
              <button v-if="editingEvent" type="button" @click="deleteEvent" class="btn bg-red-600 hover:bg-red-700 text-white">Delete</button>
              <button type="submit" class="btn btn-primary flex-1">{{ editingEvent ? 'Update' : 'Add' }}</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '../services/api'
import { useToast } from 'vue-toastification'

const toast = useToast()
const loading = ref(true)
const events = ref([])
const currentView = ref('month')
const currentDate = ref(new Date())
const showAddModal = ref(false)
const editingEvent = ref(null)

const weekDays = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']

const eventForm = ref({
  title: '',
  date: '',
  start_time: '09:00',
  end_time: '17:00',
  event_type: 'shift',
  location: '',
  description: ''
})

const periodLabel = computed(() => {
  const options = { year: 'numeric', month: 'long' }
  return currentDate.value.toLocaleDateString('en-US', options)
})

const calendarDays = computed(() => {
  const year = currentDate.value.getFullYear()
  const month = currentDate.value.getMonth()
  
  const firstDay = new Date(year, month, 1)
  const lastDay = new Date(year, month + 1, 0)
  const startPadding = firstDay.getDay()
  
  const days = []
  const today = new Date()
  
  // Previous month padding
  const prevMonth = new Date(year, month, 0)
  for (let i = startPadding - 1; i >= 0; i--) {
    days.push({
      date: prevMonth.getDate() - i,
      fullDate: formatDate(new Date(year, month - 1, prevMonth.getDate() - i)),
      isCurrentMonth: false,
      isToday: false
    })
  }
  
  // Current month
  for (let i = 1; i <= lastDay.getDate(); i++) {
    const d = new Date(year, month, i)
    days.push({
      date: i,
      fullDate: formatDate(d),
      isCurrentMonth: true,
      isToday: d.toDateString() === today.toDateString()
    })
  }
  
  // Next month padding
  const remaining = 42 - days.length
  for (let i = 1; i <= remaining; i++) {
    days.push({
      date: i,
      fullDate: formatDate(new Date(year, month + 1, i)),
      isCurrentMonth: false,
      isToday: false
    })
  }
  
  return days
})

function formatDate(date) {
  return date.toISOString().split('T')[0]
}

function getEventsForDay(dateStr) {
  return events.value.filter(e => e.date === dateStr)
}

function getEventColor(type) {
  const colors = {
    shift: 'bg-sky-100 text-sky-800 dark:bg-sky-900/30 dark:text-sky-300',
    meeting: 'bg-violet-100 text-violet-800 dark:bg-violet-900/30 dark:text-violet-300',
    training: 'bg-amber-100 text-amber-800 dark:bg-amber-900/30 dark:text-amber-300',
    evaluation: 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300',
    other: 'bg-slate-100 text-slate-800 dark:bg-slate-700 dark:text-slate-300'
  }
  return colors[type] || colors.other
}

function prevPeriod() {
  currentDate.value = new Date(currentDate.value.getFullYear(), currentDate.value.getMonth() - 1, 1)
  loadEvents()
}

function nextPeriod() {
  currentDate.value = new Date(currentDate.value.getFullYear(), currentDate.value.getMonth() + 1, 1)
  loadEvents()
}

function editEvent(event) {
  editingEvent.value = event
  eventForm.value = { ...event }
  showAddModal.value = true
}

function closeModal() {
  showAddModal.value = false
  editingEvent.value = null
  eventForm.value = { title: '', date: '', start_time: '09:00', end_time: '17:00', event_type: 'shift', location: '', description: '' }
}

async function loadEvents() {
  loading.value = true
  try {
    const year = currentDate.value.getFullYear()
    const month = currentDate.value.getMonth()
    const start = formatDate(new Date(year, month - 1, 1))
    const end = formatDate(new Date(year, month + 2, 0))
    
    const response = await api.get(`/internships/schedule/?start=${start}&end=${end}`)
    events.value = response.data?.results || (Array.isArray(response.data) ? response.data : [])
  } catch (error) {
    console.error('Failed to load events:', error)
    events.value = []
  } finally {
    loading.value = false
  }
}

async function saveEvent() {
  try {
    if (editingEvent.value) {
      await api.put(`/internships/schedule/${editingEvent.value.id}/`, eventForm.value)
      toast.success('Event updated')
    } else {
      await api.post('/internships/schedule/', eventForm.value)
      toast.success('Event added')
    }
    closeModal()
    loadEvents()
  } catch (error) {
    toast.error('Failed to save event')
  }
}

async function deleteEvent() {
  if (!confirm('Delete this event?')) return
  try {
    await api.delete(`/internships/schedule/${editingEvent.value.id}/`)
    toast.success('Event deleted')
    closeModal()
    loadEvents()
  } catch (error) {
    toast.error('Failed to delete event')
  }
}

async function exportCalendar() {
  try {
    const response = await api.get('/internships/schedule/export/', { responseType: 'blob' })
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', 'medintern_calendar.ics')
    document.body.appendChild(link)
    link.click()
    link.remove()
    toast.success('Calendar exported')
  } catch (error) {
    toast.error('Failed to export calendar')
  }
}

onMounted(loadEvents)
</script>
