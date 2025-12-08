<template>
  <button 
    @click="toggleTheme" 
    class="theme-toggle"
    :title="isDark ? 'Switch to Light Mode' : 'Switch to Dark Mode'"
  >
    <SunIcon v-if="isDark" class="w-6 h-6 text-yellow-500" />
    <MoonIcon v-else class="w-6 h-6 text-slate-700 dark:text-slate-200" />
  </button>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { SunIcon, MoonIcon } from '@heroicons/vue/24/outline'

const isDark = ref(false)

onMounted(() => {
  // Check local storage or system preference
  if (localStorage.theme === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    isDark.value = true
    document.documentElement.classList.add('dark')
  } else {
    isDark.value = false
    document.documentElement.classList.remove('dark')
  }
})

const toggleTheme = () => {
  isDark.value = !isDark.value
  if (isDark.value) {
    document.documentElement.classList.add('dark')
    localStorage.theme = 'dark'
  } else {
    document.documentElement.classList.remove('dark')
    localStorage.theme = 'light'
  }
}
</script>

<style scoped>
.theme-toggle {
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 50%;
  transition: background-color 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.theme-toggle:hover {
  background-color: rgba(0, 0, 0, 0.05);
}

.dark .theme-toggle:hover {
  background-color: rgba(255, 255, 255, 0.1);
}
</style>
