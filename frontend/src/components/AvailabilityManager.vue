<template>
  <div class="card">
    <div class="p-6 border-b border-slate-200 dark:border-slate-700">
      <h3 class="text-lg font-bold text-slate-900 dark:text-white">Availability Schedule</h3>
      <p class="text-sm text-slate-500">Set your weekly recurring availability slots</p>
    </div>

    <div class="p-6">
      <!-- Weekly View -->
      <div class="grid grid-cols-7 gap-2 mb-6">
        <div 
          v-for="(day, idx) in days" 
          :key="idx"
          class="text-center"
        >
          <div class="text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">{{ day }}</div>
          <div class="space-y-1 min-h-32">
            <div 
              v-for="slot in getSlotsByDay(idx)" 
              :key="slot.id"
              @click="editSlot(slot)"
              :class="slotTypeColors[slot.slot_type]"
              class="text-xs p-1.5 rounded cursor-pointer hover:opacity-80 transition-opacity"
            >
              <div class="font-medium">{{ slot.start_time }} - {{ slot.end_time }}</div>
              <div class="opacity-75">{{ slot.slot_type }}</div>
            </div>
            <button 
              @click="addSlot(idx)"
              class="w-full text-xs text-slate-400 hover:text-sky-500 p-1 border border-dashed border-slate-300 dark:border-slate-600 rounded hover:border-sky-500 transition-colors"
            >
              + Add
            </button>
          </div>
        </div>
      </div>

      <!-- Slot Modal -->
      <div v-if="showModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
        <div class="card p-6 w-full max-w-md">
          <h4 class="text-lg font-bold text-slate-900 dark:text-white mb-4">
            {{ editingSlot ? 'Edit' : 'Add' }} Availability Slot
          </h4>
          
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Day</label>
              <select v-model="form.day_of_week" class="input-field">
                <option v-for="(day, idx) in days" :key="idx" :value="idx">{{ day }}</option>
              </select>
            </div>
            
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Start Time</label>
                <input type="time" v-model="form.start_time" class="input-field">
              </div>
              <div>
                <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">End Time</label>
                <input type="time" v-model="form.end_time" class="input-field">
              </div>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Type</label>
              <select v-model="form.slot_type" class="input-field">
                <option value="supervision">Student Supervision</option>
                <option value="meeting">Meetings</option>
                <option value="evaluation">Evaluations</option>
                <option value="orientation">Orientation Sessions</option>
                <option value="other">Other</option>
              </select>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Max Students</label>
              <input type="number" v-model="form.max_students" min="1" class="input-field">
            </div>
            
            <div>
              <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Location (optional)</label>
              <input type="text" v-model="form.location" class="input-field" placeholder="e.g., Room 204">
            </div>
          </div>
          
          <div class="flex gap-3 mt-6">
            <button @click="closeModal" class="btn btn-outline flex-1">Cancel</button>
            <button v-if="editingSlot" @click="deleteSlot" class="btn bg-red-500 hover:bg-red-600 text-white">Delete</button>
            <button @click="saveSlot" class="btn btn-primary flex-1">Save</button>
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

const toast = useToast()
const slots = ref([])
const showModal = ref(false)
const editingSlot = ref(null)

const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

const slotTypeColors = {
  supervision: 'bg-sky-100 dark:bg-sky-900/30 text-sky-700 dark:text-sky-300',
  meeting: 'bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-300',
  evaluation: 'bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-300',
  orientation: 'bg-amber-100 dark:bg-amber-900/30 text-amber-700 dark:text-amber-300',
  other: 'bg-slate-100 dark:bg-slate-700 text-slate-700 dark:text-slate-300'
}

const form = ref({
  day_of_week: 0,
  start_time: '09:00',
  end_time: '10:00',
  slot_type: 'supervision',
  max_students: 1,
  location: ''
})

onMounted(loadSlots)

async function loadSlots() {
  try {
    const response = await api.get('/users/availability/')
    slots.value = response.data
  } catch (error) {
    console.error('Failed to load availability:', error)
  }
}

function getSlotsByDay(dayIndex) {
  return slots.value.filter(s => s.day_of_week === dayIndex)
}

function addSlot(dayIndex) {
  editingSlot.value = null
  form.value = {
    day_of_week: dayIndex,
    start_time: '09:00',
    end_time: '10:00',
    slot_type: 'supervision',
    max_students: 1,
    location: ''
  }
  showModal.value = true
}

function editSlot(slot) {
  editingSlot.value = slot
  form.value = { ...slot }
  showModal.value = true
}

function closeModal() {
  showModal.value = false
  editingSlot.value = null
}

async function saveSlot() {
  try {
    if (editingSlot.value) {
      await api.put(`/users/availability/${editingSlot.value.id}/`, form.value)
      toast.success('Slot updated')
    } else {
      await api.post('/users/availability/', form.value)
      toast.success('Slot added')
    }
    loadSlots()
    closeModal()
  } catch (error) {
    toast.error(error.response?.data?.detail || 'Failed to save slot')
  }
}

async function deleteSlot() {
  if (!confirm('Delete this availability slot?')) return
  try {
    await api.delete(`/users/availability/${editingSlot.value.id}/`)
    toast.success('Slot deleted')
    loadSlots()
    closeModal()
  } catch (error) {
    toast.error('Failed to delete slot')
  }
}
</script>
