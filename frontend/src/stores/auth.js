import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '../services/api'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const accessToken = ref(localStorage.getItem('accessToken'))
  const refreshToken = ref(localStorage.getItem('refreshToken'))
  const isLoading = ref(false)
  const isInitialized = ref(false)

  // Promise to track initial load completion
  let initPromise = null

  const isLoggedIn = computed(() => !!accessToken.value)
  const userRole = computed(() => user.value?.role)
  const isStudent = computed(() => userRole.value === 'student')
  const isHospitalAdmin = computed(() => userRole.value === 'hospital_admin')
  const isFacultyAdmin = computed(() => userRole.value === 'faculty_admin')
  const isEncadrant = computed(() => userRole.value === 'encadrant')

  function setTokens(tokens) {
    accessToken.value = tokens.access
    refreshToken.value = tokens.refresh
    localStorage.setItem('accessToken', tokens.access)
    localStorage.setItem('refreshToken', tokens.refresh)
  }

  function setAccessToken(token) {
    accessToken.value = token
    localStorage.setItem('accessToken', token)
  }

  function setUser(userData) {
    user.value = userData
  }

  function logout() {
    user.value = null
    accessToken.value = null
    refreshToken.value = null
    localStorage.removeItem('accessToken')
    localStorage.removeItem('refreshToken')
  }

  async function login(credentials) {
    isLoading.value = true
    try {
      const response = await api.post('/auth/login/', credentials)
      setTokens(response.data)
      // Also load user data after login
      await loadUser()
      return response
    } catch (error) {
      console.error('Login failed:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  async function loadUser() {
    if (!accessToken.value) {
      isInitialized.value = true
      return
    }

    isLoading.value = true
    try {
      const response = await api.get('/auth/me/')
      setUser(response.data)
    } catch (error) {
      console.error('Failed to load user:', error)
      // Only logout if it's an auth error (401), not network error
      if (error.response && error.response.status === 401) {
        logout()
      }
    } finally {
      isLoading.value = false
      isInitialized.value = true
    }
  }

  // Wait for initialization to complete
  async function waitForInit() {
    if (isInitialized.value) return
    if (initPromise) return initPromise
    return Promise.resolve()
  }

  // Initialize user if token exists
  if (accessToken.value) {
    initPromise = loadUser()
  } else {
    isInitialized.value = true
  }

  return {
    user,
    accessToken,
    refreshToken,
    isLoading,
    isLoggedIn,
    isInitialized,
    userRole,
    isStudent,
    isHospitalAdmin,
    isFacultyAdmin,
    isEncadrant,
    setTokens,
    setAccessToken,
    setUser,
    logout,
    login,
    loadUser,
    waitForInit,
  }
})