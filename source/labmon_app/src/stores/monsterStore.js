import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { _tokenExpired } from '../services/usersApi'
import { _createMonster, _deleteMonster, _fetchAllMonsters, _fetchMonster, _updateMonster } from '../services/monstersApi'

export const useMonsterStore = defineStore('monster', () => {
  const monsters = ref([])
  const currentMonster = ref(null)

  async function fetchAllMonsters() {
    try {
      const res = await _fetchAllMonsters()
      monsters.value = res.data
    } catch (error) {
      if (error.status === 401) {
        _tokenExpired()
      } 
      const message = error.response.data.error
      console.log(message)
    }
  }

  async function createMonster(monsterData) {
    try {
      const res = await _createMonster(monsterData)
      currentMonster.value = res.data
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

  async function fetchMonster(monsterId) {
    try {
      const res = await _fetchMonster(monsterId)
      currentMonster.value = res.data
    } catch (error) {
      if (error.status === 401) {
        _tokenExpired()
      } 
      const message = error.response.data.error
      console.log(message)
    }
  }

  async function updateMonster(monsterId, monsterData) {
    try {
      const res = await _updateMonster(monsterId, monsterData)
      currentMonster.value = res.data
      return "Updated successfully"
    } catch (error) {
      if (error.status === 401) {
        _tokenExpired()
      } 
      const message = error.response.data.error
      console.log(message)
      return message
    }
  }

  async function deleteMonster(monsterId) {
    try {
      const res = await _deleteMonster(monsterId)
      currentMonster.value = null
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
    monsters,
    currentMonster,
    fetchAllMonsters,
    createMonster,
    fetchMonster,
    updateMonster,
    deleteMonster,
    init
  }
})
