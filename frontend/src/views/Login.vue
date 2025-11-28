<template>
<div>
<h2>Login</h2>
<form @submit.prevent="submit">
<div><input v-model="email" placeholder="Email" required /></div>
<div><input type="password" v-model="password" placeholder="Password" required /></div>
<button type="submit">Login</button>
</form>
</div>
</template>


<script setup>
import { ref } from 'vue'
import api from '../services/api'
import { useAuthStore } from '../store/auth'
import { useRouter } from 'vue-router'


const email = ref('')
const password = ref('')
const auth = useAuthStore()
const router = useRouter()


async function submit(){
try{
const res = await api.post('/auth/token/', { email: email.value, password: password.value })
auth.setTokens({ access: res.data.access, refresh: res.data.refresh })
// fetch user profile
const me = await api.get('/auth/me/')
auth.setUser(me.data)
router.push({ name: 'dashboard' })
}catch(e){
console.error('Login failed:', e)
alert('Login failed: ' + (e.response?.data?.detail || e.message))
}
}
</script>