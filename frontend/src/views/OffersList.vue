<template>
<div>
<h2>Offers</h2>
<div v-if="loading">Loading...</div>
<div v-else>
<OfferCard v-for="o in offers" :key="o.id" :offer="o" />
</div>
</div>
</template>


<script setup>
import { ref, onMounted } from 'vue'
import api from '../services/api'
import OfferCard from '../components/OfferCard.vue'


const offers = ref([])
const loading = ref(true)


onMounted(async () => {
try{
const res = await api.get('/offers/offers/')
offers.value = res.data
}catch(e){
console.error(e)
}finally{ loading.value = false }
})
</script>