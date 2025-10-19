import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { _catchEncounter, _fetchAllEncounters, _fetchEncounter, _generateEncounter, _quitEncounter, _startTimer } from '../services/gameApi'
import router from '../router'
import { useUiStore } from './uiStore'

export const useEncounterStore = defineStore('encounter', () => {
  const encounterData = ref(null)
  const isEncounterActive = computed(() => !!encounterData.value)

  const uiStore = useUiStore()

    async function fetchAllEncounters() {
      try {
        const res = await _fetchAllEncounters()
      } catch (err) {
        console.log(err)
        uiStore.showNotification(err.response.data.error, "error")
      }
    }

    // TODO: keep for debug. Request encounters with requestEncounter
    async function getEncounter() {
      encounterData.value = {"ciao": "ciao"}
    }

    async function requestEncounter() {
      try {
        const res = await _generateEncounter()
        encounterData.value = res.data
      } catch (err) {
        if (err.status === 403) {
          uiStore.showNotification("You didn't find a monster", "info")
          return
        } 
        console.log(err)
        uiStore.showNotification(err.response.data.error, "error")
      }
    }

    async function startTimer() {
      try {
        const res = await _startTimer()
      } catch (err) {
        console.log(err)
        uiStore.showNotification(err.response.data.error, "error")
      }
    }

    async function fetchEncounter(encounterId) {
      try {
        const res = await _fetchEncounter(encounterId)
      } catch (err) {
        console.log(err)
        uiStore.showNotification(err.response.data.error, "error")
      }
    }

    async function escapeEncounter(encounterId) {
      try {
        const res = await _quitEncounter(encounterId)
      } catch (err) {
        console.log(err)
        uiStore.showNotification(err.response.data.error, "error")
      }
      router.push('/')
    }

    async function catchMonster(encounterId) {
      try {
        const res = await _catchEncounter(encounterId)
        console.log(res.data)
        if (res.data.message == "Monster caught successfully!") {
          uiStore.showCatchSuccess = true
          uiStore.reward = res.data.reward
        }
        if (res.data.message == "Failed to catch the monster.") {
          uiStore.showCatchFail = true
        }
        router.push('/')
      } catch (err) {
        console.log(err.message)
        uiStore.showNotification(err.message, "error")
      }
    }

    async function resetEncounter() {
      encounterData.value = null
    }

  return {
    encounterData,
    isEncounterActive,
    fetchAllEncounters,
    requestEncounter,
    startTimer,
    fetchEncounter,
    escapeEncounter,
    catchMonster,
    getEncounter,
    resetEncounter,
  }
})
