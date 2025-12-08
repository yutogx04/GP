<template>
  <div class="min-h-screen">
    <!-- Hero Section -->
    <section class="relative bg-white dark:bg-slate-900 pt-20 pb-32 overflow-hidden">
      <div class="container mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        <div class="text-center max-w-4xl mx-auto">
          <div class="inline-flex items-center px-4 py-2 rounded-full bg-sky-50 dark:bg-sky-900/30 text-sky-600 dark:text-sky-400 text-sm font-medium mb-8 animate-fade-in-up">
            <span class="flex h-2 w-2 rounded-full bg-sky-600 mr-2"></span>
            Now accepting applications for 2025
          </div>
          
          <h1 class="text-5xl md:text-7xl font-extrabold tracking-tight text-slate-900 dark:text-white mb-8 animate-fade-in-up delay-100">
            Launch Your <span class="text-transparent bg-clip-text bg-gradient-to-r from-sky-600 to-teal-500">Medical Career</span>
          </h1>
          
          <p class="text-xl text-slate-600 dark:text-slate-300 mb-10 max-w-2xl mx-auto leading-relaxed animate-fade-in-up delay-200">
            Connect with top-tier hospitals, manage your internship applications, and track your progress—all in one professional platform.
          </p>
          
          <div class="flex flex-col sm:flex-row gap-4 justify-center animate-fade-in-up delay-300">
            <router-link to="/internships" class="btn btn-primary text-lg px-8 py-4 rounded-full shadow-xl shadow-sky-500/20 hover:shadow-sky-500/30 transform hover:-translate-y-1 transition-all">
              Find Internships
            </router-link>

          </div>
        </div>
      </div>
      
      <!-- Background Elements -->
      <div class="absolute top-0 left-0 w-full h-full overflow-hidden -z-0">
        <div class="absolute -top-40 -right-40 w-96 h-96 bg-sky-100 dark:bg-sky-900/20 rounded-full blur-3xl opacity-50"></div>
        <div class="absolute top-40 -left-20 w-72 h-72 bg-teal-100 dark:bg-teal-900/20 rounded-full blur-3xl opacity-50"></div>
      </div>
    </section>

    <!-- Features Grid -->
    <section class="py-24 bg-slate-50 dark:bg-slate-800/50">
      <div class="container mx-auto px-4 sm:px-6 lg:px-8">
        <div class="grid md:grid-cols-3 gap-8">
          <!-- Feature 1 -->
          <div class="card p-8 hover:border-sky-500/50 transition-colors group">
            <div class="w-14 h-14 bg-sky-100 dark:bg-sky-900/30 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300">
              <BuildingOffice2Icon class="w-8 h-8 text-sky-600 dark:text-sky-400" />
            </div>
            <h3 class="text-xl font-bold text-slate-900 dark:text-white mb-3">Premium Hospitals</h3>
            <p class="text-slate-600 dark:text-slate-400 leading-relaxed">
              Access exclusive opportunities at accredited university hospitals and leading medical centers across the region.
            </p>
          </div>

          <!-- Feature 2 -->
          <div class="card p-8 hover:border-teal-500/50 transition-colors group">
            <div class="w-14 h-14 bg-teal-100 dark:bg-teal-900/30 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300">
              <BoltIcon class="w-8 h-8 text-teal-600 dark:text-teal-400" />
            </div>
            <h3 class="text-xl font-bold text-slate-900 dark:text-white mb-3">Instant Applications</h3>
            <p class="text-slate-600 dark:text-slate-400 leading-relaxed">
              Apply to multiple departments with a single click. Our streamlined process saves you time for what matters most.
            </p>
          </div>

          <!-- Feature 3 -->
          <div class="card p-8 hover:border-amber-500/50 transition-colors group">
            <div class="w-14 h-14 bg-amber-100 dark:bg-amber-900/30 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300">
              <BellIcon class="w-8 h-8 text-amber-600 dark:text-amber-400" />
            </div>
            <h3 class="text-xl font-bold text-slate-900 dark:text-white mb-3">Real-time Updates</h3>
            <p class="text-slate-600 dark:text-slate-400 leading-relaxed">
              Never miss a deadline. Get instant notifications about your application status and new opportunities.
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- Stats Section -->
    <section class="py-20 border-t border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900">
      <div class="container mx-auto px-4">
        <div class="grid grid-cols-2 md:grid-cols-4 gap-12 text-center">
          <div>
            <div class="text-4xl font-extrabold text-sky-600 dark:text-sky-400 mb-2">50+</div>
            <div class="text-sm font-medium text-slate-500 uppercase tracking-wide">Partner Hospitals</div>
          </div>
          <div>
            <div class="text-4xl font-extrabold text-teal-600 dark:text-teal-400 mb-2">1k+</div>
            <div class="text-sm font-medium text-slate-500 uppercase tracking-wide">Active Students</div>
          </div>
          <div>
            <div class="text-4xl font-extrabold text-indigo-600 dark:text-indigo-400 mb-2">200+</div>
            <div class="text-sm font-medium text-slate-500 uppercase tracking-wide">Open Positions</div>
          </div>
          <div>
            <div class="text-4xl font-extrabold text-amber-500 dark:text-amber-400 mb-2">98%</div>
            <div class="text-sm font-medium text-slate-500 uppercase tracking-wide">Placement Rate</div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { useAuthStore } from '../stores/auth'
import { BuildingOffice2Icon, BoltIcon, BellIcon } from '@heroicons/vue/24/outline'

const auth = useAuthStore()
</script>

<style scoped>
.delay-100 { animation-delay: 100ms; }
.delay-200 { animation-delay: 200ms; }
.delay-300 { animation-delay: 300ms; }

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fade-in-up {
  animation: fadeInUp 0.6s ease-out forwards;
  opacity: 0;
}
</style>