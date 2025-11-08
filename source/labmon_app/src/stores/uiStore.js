import { defineStore } from 'pinia'
import { useAuthStore } from './authStore'
import { useEncounterStore } from './encunterStore'
import { ref, computed, stop } from 'vue'
import { _getStats } from '../services/gameApi'


export const useUiStore = defineStore('ui', () => {
  const authStore = useAuthStore()
  const encounterStore = useEncounterStore()
  const notifications = ref([])
  const showNavbar = computed(() => (authStore.isAuthenticated && !encounterStore.isEncounterActive))
  const showCatchSuccess = ref(false)
  const showCatchFail = ref(false)
  const reward = ref(0)
  const timerIsRunning = ref(false)
  const time = ref(0)
  const intervalId = ref(null)
  const catchRateStat = ref(null)
  const claimedStat = ref({})

  function showNotification(message, type) {
    const notification = {"message": message, "type": type}
    notifications.value.push(notification)
    //Automatically remove after 10 seconds
    setTimeout(() => {
    const index = notifications.value.indexOf(notification)
    if (index !== -1) {
      notifications.value.splice(index, 1)
    }
  }, 5000) // 10000 ms = 10 seconds

  }

  async function startTimer() {
    if (timerIsRunning.value) return
    encounterStore.startTimer()

    timerIsRunning.value = true

    intervalId.value = setInterval(() => {
      if (time.value <= 60 * 60 * 99) {
        time.value += 1
      }
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

  async function getStats() {
    try {
      const res = await _getStats()
      catchRateStat.value = res.data.catch_rate
      claimedStat.value = res.data.claimed
    } catch (error) {
      if (error.status === 401) {
        _tokenExpired()
      }
      const message = error.response.data.error
      console.log(message)
      uiStore.showNotification(error.response.data.error, "error")
    }
  }

  async function init() {
    await getStats()
  }

  return {
    notifications,
    showNavbar,
    showCatchSuccess,
    showCatchFail,
    reward,
    time,
    timerIsRunning,
    catchRateStat,
    claimedStat,
    showNotification,
    startTimer,
    stopTimer,
    getStats,
    init
  }
})
