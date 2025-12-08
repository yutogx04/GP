<template>
  <div class="create-offer-page">
    <div class="container">
      <div class="page-header">
        <h1>Create Internship Offer</h1>
        <p>Post a new internship opportunity for medical students</p>
      </div>

      <div class="create-offer-card">
        <form @submit.prevent="submit" class="offer-form">
          <!-- Basic Information -->
          <div class="form-section">
            <h2>Basic Information</h2>
            <div class="form-group">
              <label for="title">Internship Title *</label>
              <input 
                id="title"
                v-model="form.title" 
                placeholder="e.g., Summer Internship in Cardiology"
                required
                :class="{ 'input-error': errors.title }"
              >
              <span v-if="errors.title" class="error-message">{{ errors.title }}</span>
            </div>

            <div class="form-group">
              <label for="description">Description *</label>
              <textarea 
                id="description"
                v-model="form.description" 
                placeholder="Describe the internship, responsibilities, learning objectives..."
                rows="5"
                required
                :class="{ 'input-error': errors.description }"
              ></textarea>
              <div class="field-help">
                Provide detailed information about the internship program
              </div>
            </div>
          </div>

          <!-- Duration & Availability -->
          <div class="form-section">
            <h2>Duration & Availability</h2>
            <div class="form-row">
              <div class="form-group">
                <label for="start_date">Start Date *</label>
                <input 
                  id="start_date"
                  v-model="form.start_date" 
                  type="date"
                  required
                  :class="{ 'input-error': errors.start_date }"
                >
              </div>
              <div class="form-group">
                <label for="end_date">End Date *</label>
                <input 
                  id="end_date"
                  v-model="form.end_date" 
                  type="date"
                  required
                  :class="{ 'input-error': errors.end_date }"
                >
              </div>
            </div>

            <div class="form-group">
              <label for="slots">Number of Available Spots *</label>
              <input 
                id="slots"
                v-model.number="form.slots" 
                type="number"
                min="1"
                max="50"
                required
                :class="{ 'input-error': errors.slots }"
              >
              <div class="field-help">
                Maximum 50 students per internship offer
              </div>
            </div>

            <div class="form-group">
              <label for="application_deadline">Application Deadline *</label>
              <input 
                id="application_deadline"
                v-model="form.application_deadline" 
                type="date"
                required
                :class="{ 'input-error': errors.application_deadline }"
              >
              <div class="field-help">
                Last date for students to apply
              </div>
            </div>
          </div>

          <!-- Location & Department -->
          <div class="form-section">
            <h2>Location & Department</h2>
            <div class="form-group">
              <label for="hospital">Hospital *</label>
              <select 
                id="hospital"
                v-model="form.hospital" 
                required
                @change="onHospitalChange"
                :class="{ 'input-error': errors.hospital }"
              >
                <option value="">Select a hospital</option>
                <option 
                  v-for="h in hospitals" 
                  :key="h.id" 
                  :value="h.id"
                >
                  {{ h.name }}
                </option>
              </select>
            </div>

            <div class="form-group">
              <label for="department">Department *</label>
              <select 
                id="department"
                v-model="form.department" 
                required
                :disabled="!form.hospital"
                :class="{ 'input-error': errors.department }"
              >
                <option value="">{{ form.hospital ? 'Select a department' : 'Select hospital first' }}</option>
                <option 
                  v-for="dept in filteredDepartments" 
                  :key="dept.id" 
                  :value="dept.id"
                >
                  {{ dept.name }}
                </option>
              </select>
            </div>
          </div>

          <!-- Additional Information -->
          <div class="form-section">
            <h2>Additional Information</h2>
            <div class="form-group">
              <label for="requirements">Requirements</label>
              <textarea 
                id="requirements"
                v-model="form.requirements" 
                placeholder="Specific requirements or prerequisites..."
                rows="3"
              ></textarea>
            </div>

            <div class="form-group">
              <label for="benefits">Benefits & Learning Outcomes</label>
              <textarea 
                id="benefits"
                v-model="form.benefits" 
                placeholder="What will students gain from this internship?"
                rows="3"
              ></textarea>
            </div>
          </div>

          <!-- Form Actions -->
          <div class="form-actions">
            <router-link to="/dashboard" class="btn btn-secondary">
              Cancel
            </router-link>
            <button 
              type="submit" 
              class="btn btn-primary" 
              :disabled="loading"
            >
              <span v-if="loading" class="btn-spinner"></span>
              {{ loading ? 'Creating Offer...' : 'Create Internship Offer' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import api from '../services/api'
import { useRouter } from 'vue-router'

const form = reactive({
  title: '',
  description: '',
  start_date: '',
  end_date: '',
  application_deadline: '',
  slots: 1,
  hospital: null,
  department: null,
  prerequisites: '',
  benefits: '',
  type: 'clinical',
  minimum_study_level: 'l3',
  is_paid: false,
  is_urgent: false
})

const hospitals = ref([])
const departments = ref([])
const loading = ref(false)
const errors = ref({})

const router = useRouter()

// Filter departments based on selected hospital
const filteredDepartments = computed(() => {
  if (!form.hospital) return []
  return departments.value.filter(d => d.hospital === form.hospital)
})

// Reset department when hospital changes
const onHospitalChange = () => {
  form.department = null
}

onMounted(async () => {
  try {
    const [hospRes, deptRes] = await Promise.all([
      api.get('/hospitals/'),
      api.get('/departments/')
    ])
    hospitals.value = hospRes.data?.results || hospRes.data || []
    departments.value = deptRes.data?.results || deptRes.data || []
  } catch (error) {
    console.error('Failed to load form data:', error)
  }
})

async function submit() {
  loading.value = true
  errors.value = {}

  // Basic validation
  if (new Date(form.start_date) >= new Date(form.end_date)) {
    errors.value.end_date = 'End date must be after start date'
    loading.value = false
    return
  }

  try {
    await api.post('/internships/create/', form)
    
    alert('Internship offer created successfully!')
    router.push({ name: 'dashboard' })
    
  } catch (error) {
    if (error.response?.data) {
      // Handle backend validation errors
      Object.keys(error.response.data).forEach(key => {
        const val = error.response.data[key]
        errors.value[key] = Array.isArray(val) ? val.join(', ') : val
      })
    } else {
      alert('Failed to create offer. Please try again.')
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.create-offer-page {
  padding: 2rem 0;
  min-height: 80vh;
}

.page-header {
  text-align: center;
  margin-bottom: 3rem;
}

.page-header h1 {
  margin-bottom: 0.5rem;
}

.page-header p {
  color: var(--text-secondary);
  font-size: 1.2rem;
}

.create-offer-card {
  background: var(--surface-color);
  padding: 2rem;
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-sm);
  max-width: 800px;
  margin: 0 auto;
}

.offer-form {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.form-section {
  padding-bottom: 2rem;
  border-bottom: 1px solid var(--border-color);
}

.form-section:last-of-type {
  border-bottom: none;
}

.form-section h2 {
  font-size: 1.5rem;
  margin-bottom: 1.5rem;
  color: var(--text-primary);
  padding-bottom: 0.5rem;
  border-bottom: 2px solid var(--primary-light);
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.form-group label {
  font-weight: 500;
  color: var(--text-secondary);
  font-size: 0.9rem;
}

.form-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

input,
textarea,
select {
  width: 100%;
  padding: 0.75rem 1rem;
  font-size: 1rem;
  border: 2px solid #475569;
  border-radius: var(--border-radius);
  background-color: #1e293b;
  color: var(--text-primary);
  transition: border-color 0.2s, box-shadow 0.2s;
}

input:focus,
textarea:focus,
select:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(14, 165, 233, 0.15);
}

input::placeholder,
textarea::placeholder {
  color: var(--text-light);
  opacity: 0.7;
}

input:disabled,
select:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

textarea {
  resize: vertical;
  min-height: 80px;
}

select {
  cursor: pointer;
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' fill='%2394a3b8' viewBox='0 0 16 16'%3E%3Cpath d='M8 11L3 6h10l-5 5z'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 1rem center;
  padding-right: 2.5rem;
}

.input-error {
  border-color: #ef4444 !important;
}

.error-message {
  color: #ef4444;
  font-size: 0.875rem;
}

.field-help {
  font-size: 0.875rem;
  color: var(--text-light);
  margin-top: 0.25rem;
}

.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  padding-top: 2rem;
  border-top: 1px solid var(--border-color);
}

@media (max-width: 768px) {
  .create-offer-card {
    padding: 1.5rem;
    margin: 0 1rem;
  }
  
  .form-actions {
    flex-direction: column;
  }
  
  .form-actions .btn {
    width: 100%;
  }
}
</style>
