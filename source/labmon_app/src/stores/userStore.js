import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { _deleteUser, _fetchAllUsers, _fetchUser, _manualRegister, _updateUser } from '../services/users'
import { useAuthStore } from './authStore'
import { _tokenExpired } from '../services/auth'

export const useUserStore = defineStore('user', () => {
  const users = ref([])
  const currentUser = ref(null)

  async function fetchAllUsers() {
    try {
      const res = await _fetchAllUsers()
      users.value = res.data
    } catch (error) {
      if (error.status === 401) {
        _tokenExpired()
      } 
      const message = error.response.data.error
      console.log(message)
    }
  }

  async function manualRegister(credentials) {
    try {
      const res = await _manualRegister(credentials)
      currentUser.value = res.data
      return ''
    } catch (error) {
      if (error.status === 401) {
        _tokenExpired()
      } 
      const message = error.response.data.error
      console.log(message)
      return message
    }
  }

  async function fetchUser(userId) {
    try {
      const res = await _fetchUser(userId)
      currentUser.value = res.data
    } catch (error) {
      if (error.status === 401) {
        _tokenExpired()
      } 
      const message = error.response.data.error
      console.log(message)
      // if (useAuthStore().user.id === userId) {
        
      // }
    }
  }

  async function updateUser(userId, userData) {
    try {
      const res = await _updateUser(userId, userData)
      currentUser.value = res.data
    } catch (error) {
      if (error.status === 401) {
        _tokenExpired()
      } 
      const message = error.response.data.error
      console.log(message)
    }
  }

  async function deleteUser(userId) {
    try {
      const res = await _deleteUser(userId)
      currentUser.value = null
    } catch (error) {
      if (error.status === 401) {
        _tokenExpired()
      } 
      const message = error.response.data.error
      console.log(message)
    }
  }

  async function init() {
    return
  }

  return {
    users,
    currentUser,
    fetchAllUsers,
    manualRegister,
    fetchUser,
    updateUser,
    deleteUser,
    init
  }
})
