<template>
  <div class="not-found-view">
    <div class="container">
      <div class="not-found-content">
        <div class="error-code">404</div>
        <h1>Page Not Found</h1>
        <p>Sorry, the page you're looking for doesn't exist or has been moved.</p>
        <div class="action-buttons">
          <router-link to="/" class="btn btn-primary">
            Go Home
          </router-link>
          <button @click="goBack" class="btn btn-outline">
            Go Back
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const goBack = () => {
  router.back()
}
</script>

<style scoped>
.not-found-view {
  min-height: 80vh;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
}

.not-found-content {
  max-width: 500px;
  margin: 0 auto;
}

.error-code {
  font-size: 8rem;
  font-weight: 700;
  color: var(--primary-blue);
  line-height: 1;
  margin-bottom: var(--space-4);
  opacity: 0.1;
}

.not-found-content h1 {
  font-size: var(--text-3xl);
  margin-bottom: var(--space-4);
  color: var(--gray-900);
}

.not-found-content p {
  font-size: var(--text-lg);
  color: var(--gray-600);
  margin-bottom: var(--space-8);
  line-height: 1.6;
}

.action-buttons {
  display: flex;
  gap: var(--space-4);
  justify-content: center;
  flex-wrap: wrap;
}

@media (max-width: 768px) {
  .error-code {
    font-size: 6rem;
  }
  
  .action-buttons {
    flex-direction: column;
    align-items: center;
  }
  
  .action-buttons .btn {
    width: 100%;
    max-width: 200px;
  }
}
</style>