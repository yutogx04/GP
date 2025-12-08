<template>
  <div id="app" class="min-h-screen flex flex-col bg-gray-50 dark:bg-dark-bg text-gray-900 dark:text-dark-text transition-colors duration-300">
    <AppNavbar />
    
    <!-- Global Loading State -->
    <div v-if="auth.isLoading" class="flex-1 flex items-center justify-center min-h-[60vh]">
      <div class="flex flex-col items-center gap-4">
        <div class="w-12 h-12 border-4 border-sky-200 border-t-sky-600 rounded-full animate-spin"></div>
        <p class="text-slate-500 font-medium animate-pulse">Loading...</p>
      </div>
    </div>

    <main v-else class="flex-1 pt-6 pb-16">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
    
    <AppFooter />
  </div>
</template>

<script setup>
import AppNavbar from './components/AppNavbar.vue'
import AppFooter from './components/AppFooter.vue'
import { useAuthStore } from './stores/auth'

const auth = useAuthStore()
</script>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>