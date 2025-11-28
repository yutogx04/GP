<template>
<div>
<h2>Verify Email</h2>
<p v-if="message">{{message}}</p>
</div>
</template>


<script setup>
import { onMounted, ref } from 'vue'
import api from '../services/api'
import { useRoute } from 'vue-router'


const route = useRoute()
const message = ref('Verifying...')


onMounted(async ()=>{
try{
const token = route.query.token
const res = await api.get(`/auth/verify-email/?token=${token}`)
message.value = res.data.detail || 'Verified — you can login.'
}catch(e){
message.value = e.response?.data?.detail || 'Verification failed'
}
})
</script>