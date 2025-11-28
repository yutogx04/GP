import { defineStore } from 'pinia'
import { ref } from 'vue'


export const useAuthStore = defineStore('auth', () => {
const user = ref(null)
const accessToken = ref(localStorage.getItem('access') || null)
const refreshToken = ref(localStorage.getItem('refresh') || null)


function setTokens({ access, refresh }) {
accessToken.value = access
refreshToken.value = refresh
localStorage.setItem('access', access)
localStorage.setItem('refresh', refresh)
}
function setAccessToken(access) {
accessToken.value = access
localStorage.setItem('access', access)
}
function setUser(u) {
user.value = u
}
function logout() {
user.value = null
accessToken.value = null
refreshToken.value = null
localStorage.removeItem('access')
localStorage.removeItem('refresh')
}


return { user, accessToken, refreshToken, setTokens, setUser, setAccessToken, logout, isLoggedIn: !!accessToken.value }
})