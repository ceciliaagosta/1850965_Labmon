import { defineStore } from 'pinia'
import { useAuthStore } from './authStore'
import { useEncounterStore } from './encunterStore'
import { ref, computed } from 'vue'


export const useUiStore = defineStore('ui', () => {
  const authStore = useAuthStore()
  const encounterStore = useEncounterStore()
  const errors = []
  const showNavbar = computed(() => (authStore.isAuthenticated && !encounterStore.isEncounterActive))

  return {
    errors,
    showNavbar,
  }
})
