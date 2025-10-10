import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { _catchEncounter, _fetchAllEncounters, _fetchEncounter, _quitEncounter } from '../services/gameApi'
import router from '../router'

export const useEncounterStore = defineStore('encounter', () => {
  const encounterData = ref(null)
  const isEncounterActive = computed(() => !!encounterData.value)

    async function fetchAllEncounters() {
      try {
        const res = _fetchAllEncounters()
      } catch (err) {
        console.log(err)
      }
    }

    // TODO: keep for debug. Request encounters with requestEncounter
    async function getEncounter() {
      encounterData.value = {"ciao": "ciao"}
    }

    async function requestEncounter() {
      return
    }

    async function fetchEncounter(encounterId) {
      try {
        const res = _fetchEncounter(encounterId)
      } catch (err) {
        console.log(err)
      }
    }

    async function escapeEncounter(encounterId) {
      try {
        // const res = _quitEncounter(encounterId)
        router.push('/')
      } catch (err) {
        console.log(err)
      }
    }

    async function catchMonster(encounterId) {
      try {
        const res = _catchEncounter(encounterId)
      } catch (err) {
        console.log(err)
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
    fetchEncounter,
    escapeEncounter,
    catchMonster,
    getEncounter,
    resetEncounter,
  }
})
