import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { _login, _register } from '../services/usersApi'
import { jwtDecode } from 'jwt-decode'
import router from '../router'
import { useUserStore } from './userStore'
import { useUiStore } from './uiStore'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || null)
  const userId = ref(null)
  const role = ref(null)
  const user = ref(null)
  const isAuthenticated = computed(() => !!token.value)
  const isAdmin = computed(() => role.value === 'admin')

  const uiStore = useUiStore()

  function setToken(newToken) {
    token.value = newToken
    localStorage.setItem('token', newToken)
  }

  function clearToken() {
    token.value = null
    localStorage.removeItem('token')
  }

  async function register(credentials) {
    try {
      const res = await _register(credentials)
      setToken(res.data.token)
      const decoded = jwtDecode(token.value)
      userId.value = decoded.user_id
      role.value = decoded.role
      const userStore = useUserStore()
      await userStore.fetchUser(userId.value)
      user.value = userStore.currentUser
    } catch (error) {
      const message = error.response.data.error
      console.log(message)
      uiStore.showNotification(message, "error")
    }
  }

  async function login(credentials) {
    try{
      const res = await _login(credentials)
      setToken(res.data.token)
      const decoded = jwtDecode(token.value)
      userId.value = decoded.user_id
      role.value = decoded.role
      const userStore = useUserStore()
      await userStore.fetchUser(userId.value)
      user.value = userStore.currentUser
    } catch (error) {
      const message = error.response.data.error
      console.log(message)
      uiStore.showNotification(message, "error")
    }
  }

  async function logout() {
    clearToken()
    userId.value = null
    role.value = null
    user.value = null
    router.push('/login')
  }

  async function init() {
    if (token.value && !user.value) {
      try {
        const decoded = jwtDecode(token.value)
        userId.value = decoded.user_id
        role.value = decoded.role
        const userStore = useUserStore()
        await userStore.fetchUser(userId.value)
        user.value = userStore.currentUser
      } catch (error) {
        console.warn('Auth rehydration failed, logging out:', error)
        logout()
        uiStore.showNotification(error.response.data.error, "error")
      }
    }
  }

  return {
    token,
    role,
    userId,
    user,
    isAuthenticated,
    isAdmin,
    register,
    login,
    logout,
    init
  }
})
