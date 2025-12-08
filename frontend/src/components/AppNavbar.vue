<template>
  <nav class="sticky top-0 z-50 w-full bg-white/80 dark:bg-slate-900/80 backdrop-blur-md border-b border-slate-200 dark:border-slate-800 transition-colors duration-300">
    <div class="container mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-16">
        
        <!-- Logo -->
        <div class="flex-shrink-0 flex items-center gap-2 cursor-pointer" @click="$router.push('/')">
          <div class="w-8 h-8 bg-gradient-to-br from-sky-500 to-teal-500 rounded-lg flex items-center justify-center text-white font-bold text-lg shadow-lg shadow-sky-500/20">
            M
          </div>
          <span class="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-slate-900 to-slate-700 dark:from-white dark:to-slate-300">
            MedIntern
          </span>
        </div>

        <!-- Desktop Navigation -->
        <div class="hidden md:flex items-center gap-1">
          <router-link to="/" class="nav-link">Home</router-link>
          
          <template v-if="auth.isLoggedIn">
            <router-link to="/dashboard" class="nav-link">Dashboard</router-link>
            
            <!-- Student Links -->
            <template v-if="auth.isStudent">
              <router-link to="/internships" class="nav-link">Internships</router-link>
              <router-link to="/applications" class="nav-link">My Applications</router-link>
              <router-link to="/journal" class="nav-link">Journal</router-link>
              <router-link to="/evaluations" class="nav-link">Evaluations</router-link>
            </template>
            
            <!-- Hospital Admin Links -->
            <template v-if="auth.isHospitalAdmin">
              <router-link to="/offers/create" class="nav-link">Create Offer</router-link>
              <router-link to="/offers/manage" class="nav-link">Manage Offers</router-link>
              <router-link to="/hospital/applications" class="nav-link">Applications</router-link>
              <router-link to="/hospital/internships" class="nav-link">Internships</router-link>
              <router-link to="/hospital/staff" class="nav-link">Staff</router-link>
            </template>
            
            <!-- Supervisor Links -->
            <template v-if="auth.isEncadrant">
              <router-link to="/supervisor/students" class="nav-link">My Students</router-link>
              <router-link to="/supervisor/evaluations" class="nav-link">Evaluations</router-link>
            </template>
            
            <!-- Faculty Admin Links -->
            <template v-if="auth.isFacultyAdmin">
              <router-link to="/faculty/students" class="nav-link">Students</router-link>
              <router-link to="/faculty/offers" class="nav-link">Validate Offers</router-link>
              <router-link to="/faculty/reports" class="nav-link">Reports</router-link>
            </template>
            
            <!-- Common Links -->
            <router-link to="/calendar" class="nav-link">Calendar</router-link>
            <router-link to="/messages" class="nav-link">Messages</router-link>
          </template>
        </div>

        <!-- Right Side Actions -->
        <div class="hidden md:flex items-center gap-4">
          <ThemeToggle />
          
          <template v-if="auth.isLoggedIn">
            <NotificationBell />
            
            <!-- User Dropdown -->
            <div class="relative group">
              <button class="flex items-center gap-2 text-sm font-medium text-slate-700 dark:text-slate-200 hover:text-sky-600 dark:hover:text-sky-400 transition-colors">
                <div class="w-8 h-8 rounded-full bg-sky-100 dark:bg-sky-900/30 flex items-center justify-center text-sky-700 dark:text-sky-400 border border-sky-200 dark:border-sky-800">
                  {{ auth.user?.first_name?.[0] || 'U' }}
                </div>
                <span>{{ auth.user?.first_name }}</span>
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 opacity-50" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                </svg>
              </button>

              <!-- Dropdown Menu -->
              <div class="absolute right-0 mt-2 w-48 bg-white dark:bg-slate-800 rounded-xl shadow-xl border border-slate-100 dark:border-slate-700 opacity-0 invisible group-hover:opacity-100 group-hover:visible transform group-hover:translate-y-0 translate-y-2 transition-all duration-200">
                <div class="py-1">
                  <router-link to="/profile" class="block px-4 py-2 text-sm text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-700/50">
                    Profile
                  </router-link>
                  <router-link to="/settings" class="block px-4 py-2 text-sm text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-700/50">
                    Settings
                  </router-link>
                  <div class="border-t border-slate-100 dark:border-slate-700 my-1"></div>
                  <button @click="handleLogout" class="w-full text-left px-4 py-2 text-sm text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20">
                    Sign out
                  </button>
                </div>
              </div>
            </div>
          </template>

          <template v-else>
            <router-link to="/login" class="btn btn-primary btn-sm">
              Log in
            </router-link>
          </template>
        </div>

        <!-- Mobile Menu Button -->
        <div class="md:hidden flex items-center gap-4">
          <ThemeToggle />
          <button @click="isMobileMenuOpen = !isMobileMenuOpen" class="text-slate-700 dark:text-slate-200 p-2">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path v-if="!isMobileMenuOpen" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
              <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Mobile Menu -->
    <div v-show="isMobileMenuOpen" class="md:hidden border-t border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900">
      <div class="px-4 pt-2 pb-4 space-y-1">
        <router-link to="/" class="mobile-nav-link" @click="isMobileMenuOpen = false">Home</router-link>
        
        <template v-if="auth.isLoggedIn">
          <router-link to="/dashboard" class="mobile-nav-link" @click="isMobileMenuOpen = false">Dashboard</router-link>
          
          <!-- Student -->
          <template v-if="auth.isStudent">
            <router-link to="/internships" class="mobile-nav-link" @click="isMobileMenuOpen = false">Internships</router-link>
            <router-link to="/applications" class="mobile-nav-link" @click="isMobileMenuOpen = false">My Applications</router-link>
            <router-link to="/evaluations" class="mobile-nav-link" @click="isMobileMenuOpen = false">Evaluations</router-link>
          </template>
          
          <!-- Hospital Admin -->
          <template v-if="auth.isHospitalAdmin">
            <router-link to="/offers/create" class="mobile-nav-link" @click="isMobileMenuOpen = false">Create Offer</router-link>
            <router-link to="/offers/manage" class="mobile-nav-link" @click="isMobileMenuOpen = false">Manage Offers</router-link>
            <router-link to="/hospital/applications" class="mobile-nav-link" @click="isMobileMenuOpen = false">Applications</router-link>
            <router-link to="/hospital/staff" class="mobile-nav-link" @click="isMobileMenuOpen = false">Staff</router-link>
          </template>
          
          <!-- Supervisor -->
          <template v-if="auth.isEncadrant">
            <router-link to="/supervisor/students" class="mobile-nav-link" @click="isMobileMenuOpen = false">My Students</router-link>
            <router-link to="/supervisor/evaluations" class="mobile-nav-link" @click="isMobileMenuOpen = false">Evaluations</router-link>
          </template>
          
          <!-- Faculty Admin -->
          <template v-if="auth.isFacultyAdmin">
            <router-link to="/faculty/students" class="mobile-nav-link" @click="isMobileMenuOpen = false">Students</router-link>
            <router-link to="/faculty/offers" class="mobile-nav-link" @click="isMobileMenuOpen = false">Validate Offers</router-link>
            <router-link to="/faculty/reports" class="mobile-nav-link" @click="isMobileMenuOpen = false">Reports</router-link>
          </template>
          
          <router-link to="/messages" class="mobile-nav-link" @click="isMobileMenuOpen = false">Messages</router-link>
          
          <div class="border-t border-slate-100 dark:border-slate-800 my-2 pt-2">
            <router-link to="/profile" class="mobile-nav-link" @click="isMobileMenuOpen = false">Profile</router-link>
            <router-link to="/settings" class="mobile-nav-link" @click="isMobileMenuOpen = false">Settings</router-link>
            <button @click="handleLogout" class="mobile-nav-link text-red-600 dark:text-red-400 w-full text-left">Sign out</button>
          </div>
        </template>
        
        <template v-else>
          <router-link to="/login" class="mobile-nav-link text-sky-600 dark:text-sky-400 font-medium" @click="isMobileMenuOpen = false">Log in</router-link>
        </template>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import ThemeToggle from './ThemeToggle.vue'
import NotificationBell from './NotificationBell.vue'

const router = useRouter()
const auth = useAuthStore()
const isMobileMenuOpen = ref(false)

const handleLogout = () => {
  auth.logout()
  router.push('/login')
  isMobileMenuOpen.value = false
}
</script>

<style scoped>
.nav-link {
  @apply px-4 py-2 text-sm font-medium text-slate-600 dark:text-slate-300 hover:text-sky-600 dark:hover:text-sky-400 transition-colors rounded-lg hover:bg-slate-50 dark:hover:bg-slate-800/50;
}

.router-link-active {
  @apply text-sky-600 dark:text-sky-400 bg-sky-50 dark:bg-sky-900/20;
}

.mobile-nav-link {
  @apply block px-3 py-2 text-base font-medium text-slate-600 dark:text-slate-300 hover:text-sky-600 dark:hover:text-sky-400 hover:bg-slate-50 dark:hover:bg-slate-800 rounded-lg transition-colors;
}
</style>