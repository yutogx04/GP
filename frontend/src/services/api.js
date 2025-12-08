import axios from 'axios'
import { useAuthStore } from '../stores/auth'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000,
})

// Request interceptor
api.interceptors.request.use(
  (config) => {
    const authStore = useAuthStore()
    const token = authStore.accessToken

    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }

    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor
api.interceptors.response.use(
  (response) => {
    return response
  },
  async (error) => {
    const originalRequest = error.config
    const authStore = useAuthStore()

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      try {
        const refreshToken = authStore.refreshToken
        if (refreshToken) {
          const response = await axios.post(
            `${api.defaults.baseURL}/auth/token/refresh/`,
            { refresh: refreshToken }
          )

          const newAccessToken = response.data.access
          authStore.setAccessToken(newAccessToken)
          originalRequest.headers.Authorization = `Bearer ${newAccessToken}`
          return api(originalRequest)
        }
      } catch (refreshError) {
        authStore.logout()
        // Use router for navigation instead of hard reload
        const router = require('./router').default
        router.push({ name: 'login', query: { redirect: window.location.pathname } })
        return Promise.reject(refreshError)
      }
    }

    return Promise.reject(error)
  }
)

export default api