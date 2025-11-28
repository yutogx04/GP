<template>
<div class="card" style="border:1px solid #ddd;padding:12px;margin-bottom:8px">
<h3>{{offer.title}}</h3>
<p>{{offer.description.substring(0,140)}}...</p>
<small>Service: {{offer.service.name}} | Establishment: {{offer.establishment.name}}</small>
<div style="margin-top:8px">
<router-link :to="`/offers/${offer.id}`">View</router-link>
</div>
</div>
</template>


<script setup>
defineProps({ offer: Object })
</script>