<template>
<nav style="display:flex;gap:12px;align-items:center;padding:12px;border-bottom:1px solid #eee">
<router-link to="/">Home</router-link>
<router-link to="/offers">Offers</router-link>
<router-link v-if="!auth.isLoggedIn" to="/login">Login</router-link>
<router-link v-if="!auth.isLoggedIn" to="/register">Register</router-link>
<router-link v-if="auth.isLoggedIn" to="/profile">Profile</router-link>
<router-link v-if="auth.isLoggedIn" to="/dashboard">Dashboard</router-link>
<button v-if="auth.isLoggedIn" @click="logout">Logout</button>
</nav>
</template>


<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '../store/auth'
const auth = useAuthStore()
const router = useRouter()
function logout(){
auth.logout()
router.push('/')
}
</script>