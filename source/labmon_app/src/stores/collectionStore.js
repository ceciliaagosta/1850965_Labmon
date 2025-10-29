import { defineStore } from 'pinia'
import { ref, computed, toRaw } from 'vue'
import { _claim, _getCollection, _shard } from '../services/gameApi'
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
        collection.value = res.data.collection
        splitCollections()
      } catch (err) {
        console.log(err)
        uiStore.showNotification(err.response.data.error, "error")
      }
    }

    function splitCollections() {
    const monsters = toRaw(allMonsters.value)
    const userCollection = toRaw(collection.value)
    const splittedCollections = {}

    monsters.forEach((monster) => {
      const collNum = monster.collection

      if (!(collNum in splittedCollections)) {
        splittedCollections[collNum] = []
      }

      // add caught info
      const quantity = userCollection[monster.id] ?? 0
      splittedCollections[collNum].push({
        ...monster,
        quantity,
        caught: monster.id in userCollection
      })
    })

    collections.value = splittedCollections
  }

    async function shardMonster(monsterId) {
      try {
        const res = await _shard(monsterId)
        const reward = res.data.reward
        uiStore.showNotification(`Monster shredded! You gained ${reward} shards.`, "success")
      } catch (err) {
        console.log(err)
        uiStore.showNotification(err.response.data.error, "error")
      }
      fetchCollection()
    }

    async function claimCollection(collectionId) {
      try {
        console.log(collectionId)
        const res = await _claim(collectionId)
        const reward = res.data.reward
        uiStore.showNotification(`Collection claimed! You gained ${reward} shards.`, "success")
      } catch (err) {
        console.log(err)
        uiStore.showNotification(err.response.data.error, "error")
      }

    }

  return {
    allMonsters,
    collections,
    collection,
    fetchCollection,
    shardMonster,
    claimCollection
  }
})
