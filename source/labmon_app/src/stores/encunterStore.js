import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import router from '../router'

export const useEncounterStore = defineStore('encounter', () => {
    const encounterData = ref(null)
    const isEncounterActive = computed(() => !!encounterData.value)

      async function getEncounter() {
        encounterData.value = {"ciao": "ciao"}
      }

      async function resetEncounter() {
        encounterData.value = null
      }

  return {
    encounterData,
    isEncounterActive,
    getEncounter,
    resetEncounter,
  }
})
