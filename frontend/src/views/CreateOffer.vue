<template>
<div>
<h2>Create Offer</h2>
<form @submit.prevent="submit">
<input v-model="title" placeholder="Title" required />
<textarea v-model="description" placeholder="Description" />
<input type="date" v-model="start_date" />
<input type="date" v-model="end_date" />
<input type="number" v-model.number="number_places" min="1" />
<select v-model="establishment_id">
<option v-for="e in establishments" :value="e.id" :key="e.id">{{e.name}}</option>
</select>
<select v-model="service_id">
<option v-for="s in services" :value="s.id" :key="s.id">{{s.name}}</option>
</select>
<button type="submit">Create</button>
</form>
</div>
</template>


<script setup>
import { ref, onMounted } from 'vue'
import api from '../services/api'
import { useRouter } from 'vue-router'


const title = ref('')
const description = ref('')
const start_date = ref('')
const end_date = ref('')
const number_places = ref(1)
const establishment_id = ref(null)
const service_id = ref(null)
const establishments = ref([])
const services = ref([])
const router = useRouter()


onMounted(async ()=>{
const res = await api.get('/establishments/')
establishments.value = res.data
const res2 = await api.get('/establishments/services/')
services.value = res2.data
})


async function submit(){
try{
await api.post('/offers/create/', { title: title.value, description: description.value, start_date: start_date.value, end_date: end_date.value, number_places: number_places.value, establishment_id: establishment_id.value, service_id: service_id.value })
alert('Created')
router.push({ name: 'offers' })
}catch(e){
console.error('Error creating offer:', e)
alert('Error creating offer: ' + (e.response?.data?.message || e.message))
}
}
</script>