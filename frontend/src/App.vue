<template>
<div>
<Navbar />
<main class="container">
<router-view />
</main>
</div>
</template>


<script setup>
import Navbar from './components/Navbar.vue'
</script>


<style>
.container{padding:16px;max-width:1000px;margin:0 auto}
</style>