<template>
<div>
<h2>Your Profile</h2>
<form @submit.prevent="save">
<input v-model="form.numero_etudiant" placeholder="Student number" />
<input v-model="form.niveau_etude" placeholder="Level" />
<input v-model="form.contact_phone" placeholder="Phone" />
<button type="submit">Save</button>
</form>
</div>
</template>


<script setup>
import { ref, onMounted } from 'vue'
import api from '../services/api'
import { useAuthStore } from '../store/auth'


const auth = useAuthStore()
const form = ref({ numero_etudiant:'', niveau_etude:'', contact_phone:'' })


onMounted(async ()=>{
try{
const res = await api.get('/profile/me/')
Object.assign(form.value, res.data)
}catch(e){console.error(e)}
})


async function save(){
try{
await api.patch('/profile/me/', form.value)
alert('Profile saved')
// optionally call backend to mark profile complete
}catch(e){
  console.error(e);
  alert('Save failed');
}
}
</script>