<template>
<div>
<h2>Register</h2>
<form @submit.prevent="submit">
<input v-model="email" placeholder="Email" required />
<input v-model="first_name" placeholder="First name" />
<input v-model="last_name" placeholder="Last name" />
<input v-model="password" type="password" placeholder="Password" required />
<select v-model="role">
<option value="student">Student</option>
<option value="hospital_admin">Hospital admin</option>
<option value="faculty_admin">Faculty admin</option>
<option value="encadrant">Encadrant</option>
</select>
<button type="submit">Register</button>
</form>
</div>
</template>


<script setup>
import { ref } from 'vue'
import api from '../services/api'
import { useRouter } from 'vue-router'


const email = ref('')
const password = ref('')
const first_name = ref('')
const last_name = ref('')
const role = ref('student')
const router = useRouter()


async function submit(){
try{
await api.post('/auth/register/', { email: email.value, password: password.value, first_name: first_name.value, last_name: last_name.value, role: role.value })
alert('Check your email for verification link')
router.push({ name: 'login' })
}catch(e){
console.error('Registration error:', e)
alert(e.response?.data?.message || 'Register failed')
}
}
</script>