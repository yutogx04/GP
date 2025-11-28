<template>
<div>
<h2>{{offer.title}}</h2>
<p>{{offer.description}}</p>
<p>From {{offer.start_date}} to {{offer.end_date}} — slots: {{offer.number_places}}</p>
<div v-if="auth.isLoggedIn && auth.user.role === 'student'">
<button @click="apply">Apply</button>
</div>
</div>
</template>


<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import api from '../services/api'
import { useAuthStore } from '../store/auth'


const route = useRoute()
const auth = useAuthStore()
const offer = ref(null)


onMounted(async ()=>{
const res = await api.get(`/offers/offers/${route.params.id}/`)
offer.value = res.data
})


async function apply(){
try{
const form = new FormData()
form.append('offer', offer.value.id)
await api.post('/candidacies/apply/', form)
alert('Applied successfully')
}catch(e){
alert('Error applying: '+(e.response?.data?.detail || e.message))
}
}
</script>