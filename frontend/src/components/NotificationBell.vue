<template>
  <div class="notification-bell" v-click-outside="closeDropdown">
    <button @click="toggleDropdown" class="bell-btn">
      <span class="icon">🔔</span>
      <span v-if="unreadCount > 0" class="badge">{{ unreadCount }}</span>
    </button>

    <div v-if="isOpen" class="dropdown glass-card">
      <div class="dropdown-header">
        <h3>Notifications</h3>
        <button v-if="unreadCount > 0" @click="markAllRead" class="text-sm text-primary-500 hover:underline">
          Mark all read
        </button>
      </div>

      <div v-if="loading" class="p-4 text-center">
        <div class="spinner"></div>
      </div>

      <div v-else-if="notifications.length === 0" class="p-4 text-center text-gray-500">
        No notifications
      </div>

      <div v-else class="notification-list">
        <div 
          v-for="notification in notifications" 
          :key="notification.id"
          class="notification-item"
          :class="{ 'unread': !notification.is_read }"
          @click="handleNotificationClick(notification)"
        >
          <div class="notification-icon" :class="notification.type">
            {{ getIcon(notification.type) }}
          </div>
          <div class="notification-content">
            <p class="title">{{ notification.title }}</p>
            <p class="message">{{ notification.message }}</p>
            <span class="time">{{ formatTime(notification.created_at) }}</span>
          </div>
          <div v-if="!notification.is_read" class="unread-dot"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import api from '../services/api'
import { useAuthStore } from '../stores/auth'

const auth = useAuthStore()
const isOpen = ref(false)
const notifications = ref([])
const loading = ref(false)
const unreadCount = computed(() => {
  if (!Array.isArray(notifications.value)) return 0
  return notifications.value.filter(n => !n.is_read).length
})
let pollInterval = null

onMounted(() => {
  if (auth.isLoggedIn) {
    loadNotifications()
    // Poll for notifications every minute
    pollInterval = setInterval(loadNotifications, 60000)
  }
})

onUnmounted(() => {
  if (pollInterval) clearInterval(pollInterval)
})

const loadNotifications = async () => {
  try {
    const response = await api.get('/notifications/')
    notifications.value = response.data?.results || (Array.isArray(response.data) ? response.data : [])
  } catch (error) {
    console.error('Failed to load notifications', error)
    notifications.value = []
  }
}

const toggleDropdown = () => {
  isOpen.value = !isOpen.value
}

const closeDropdown = () => {
  isOpen.value = false
}

const markAllRead = async () => {
  try {
    await api.post('/notifications/mark-all-read/')
    notifications.value.forEach(n => n.is_read = true)
  } catch (error) {
    console.error('Failed to mark all read', error)
  }
}

const handleNotificationClick = async (notification) => {
  if (!notification.is_read) {
    try {
      await api.post(`/notifications/${notification.id}/read/`)
      notification.is_read = true
    } catch (error) {
      console.error('Failed to mark read', error)
    }
  }
  
  if (notification.link) {
    // Navigate to link if present
    // router.push(notification.link)
  }
}

const getIcon = (type) => {
  const icons = {
    info: 'ℹ️',
    success: '✅',
    warning: '⚠️',
    error: '❌'
  }
  return icons[type] || 'ℹ️'
}

const formatTime = (dateString) => {
  const date = new Date(dateString)
  const now = new Date()
  const diff = now - date
  
  if (diff < 60000) return 'Just now'
  if (diff < 3600000) return `${Math.floor(diff / 60000)}m ago`
  if (diff < 86400000) return `${Math.floor(diff / 3600000)}h ago`
  return date.toLocaleDateString()
}

// Simple click-outside directive
const vClickOutside = {
  mounted(el, binding) {
    el.clickOutsideEvent = function(event) {
      if (!(el === event.target || el.contains(event.target))) {
        binding.value(event)
      }
    }
    document.body.addEventListener('click', el.clickOutsideEvent)
  },
  unmounted(el) {
    document.body.removeEventListener('click', el.clickOutsideEvent)
  }
}
</script>

<style scoped>
.notification-bell {
  position: relative;
}

.bell-btn {
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 0.5rem;
  position: relative;
  font-size: 1.25rem;
}

.badge {
  position: absolute;
  top: 0;
  right: 0;
  background: var(--error-red);
  color: white;
  font-size: 0.75rem;
  padding: 0.1rem 0.3rem;
  border-radius: 999px;
  min-width: 1.2rem;
}

.dropdown {
  position: absolute;
  top: 100%;
  right: 0;
  width: 320px;
  max-height: 400px;
  overflow-y: auto;
  margin-top: 0.5rem;
  z-index: 50;
}

.dropdown-header {
  padding: 1rem;
  border-bottom: 1px solid var(--gray-200);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.dark .dropdown-header {
  border-color: var(--border-color);
}

.notification-item {
  padding: 1rem;
  display: flex;
  gap: 0.75rem;
  cursor: pointer;
  transition: background-color 0.2s;
  border-bottom: 1px solid var(--gray-100);
}

.dark .notification-item {
  border-color: var(--border-color);
}

.notification-item:hover {
  background-color: var(--gray-50);
}

.dark .notification-item:hover {
  background-color: rgba(255, 255, 255, 0.05);
}

.notification-item.unread {
  background-color: rgba(14, 165, 233, 0.05);
}

.notification-content {
  flex: 1;
}

.title {
  font-weight: 600;
  font-size: 0.875rem;
  margin-bottom: 0.25rem;
}

.message {
  font-size: 0.875rem;
  color: var(--gray-600);
  margin-bottom: 0.25rem;
}

.dark .message {
  color: var(--text-secondary);
}

.time {
  font-size: 0.75rem;
  color: var(--gray-400);
}

.unread-dot {
  width: 8px;
  height: 8px;
  background-color: var(--primary-blue);
  border-radius: 50%;
  align-self: center;
}
</style>
