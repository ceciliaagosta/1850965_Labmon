import { defineStore } from 'pinia'
import { useAuthStore } from './authStore'
import { useEncounterStore } from './encunterStore'
import { ref, computed, stop } from 'vue'


export const useUiStore = defineStore('ui', () => {
  const authStore = useAuthStore()
  const encounterStore = useEncounterStore()
  const errors = []
  const showNavbar = computed(() => (authStore.isAuthenticated && !encounterStore.isEncounterActive))
  const timerIsRunning = ref(false)
  const time = ref(0)
  const intervalId = ref(null)

  async function startTimer() {
    if (timerIsRunning.value) return
    timerIsRunning.value = true

    intervalId.value = setInterval(() => {
      time.value += 1
    }, 1000)
  }

  async function stopTimer() {
    if (!timerIsRunning.value) return
    timerIsRunning.value = false

    const elapsedTime = time.value
    time.value = 0

    clearInterval(intervalId.value)

    return elapsedTime
  }

  return {
    errors,
    showNavbar,
    time,
    timerIsRunning,
    startTimer,
    stopTimer
  }
})
