import { defineStore } from 'pinia'
import { useAuthStore } from './authStore'
import { ref, computed } from 'vue'

export const useUiStore = defineStore('ui', () => {
  const authStore = useAuthStore()
  const errors = []
  const showNavbar = computed(() => authStore.isAuthenticated)

  return {
    errors,
    showNavbar,
  }
})
