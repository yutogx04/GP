<template>
<div>
<h2>Dashboard</h2>
<div v-if="auth.user">
<p>Welcome, {{auth.user.email}} — role: {{auth.user.role}}</p>
</div>
<div>
<router-link to="/offers">Browse offers</router-link>
<router-link v-if="auth.user && auth.user.role === 'hospital_admin'" to="/create-offer">Create Offer</router-link>
</div>
</div>
</template>


<script setup>
import { useAuthStore } from '../store/auth'
const auth = useAuthStore()
</script>