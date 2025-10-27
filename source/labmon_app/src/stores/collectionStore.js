import { defineStore } from 'pinia'
import { ref, computed, toRaw } from 'vue'
import { _getCollection, _shard } from '../services/gameApi'
import { useMonsterStore } from './monsterStore'
import { useUiStore } from './uiStore'

export const useCollectionStore = defineStore('collection', () => {

  const monsterStore = useMonsterStore()
  const uiStore = useUiStore()  

  const allMonsters = computed(() => monsterStore.monsters)
  const collections = ref({})
  const collection = ref({})

    async function fetchCollection() {
      await monsterStore.fetchAllMonsters()
      try {
        const res = await _getCollection()
        // console.log(res.data.collection)
        collection.value = res.data.collection
        splitCollections()
      } catch (err) {
        console.log(err)
        uiStore.showNotification(err.response.data.error, "error")
      }
    }

    function splitCollections() {
      // TODO: qua valerio si è perso e questo split va ancora implementato
      const monsters = toRaw(allMonsters.value)
      const foundCollections = []
      for (var m in monsters) {
          const collectionNum = monsters[m].collection
          // if (collectionNum not in)
      }
    }

    async function shardMonster(monsterId) {
      try {
        const res = _shard(monsterId)
      } catch (err) {
        console.log(err)
        uiStore.showNotification(err.response.data.error, "error")
      }
      fetchCollection()
    }

  return {
    allMonsters,
    collection,
    fetchCollection,
    shardMonster,
  }
})
