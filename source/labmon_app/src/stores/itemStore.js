import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { _tokenExpired } from '../services/auth'
import { _createItem, _deleteItem, _fetchAllItems, _fetchItem, _updateItem } from '../services/itemsApi'

export const useItemStore = defineStore('item', () => {
  const items = ref([])
  const currentItem = ref(null)

  async function fetchAllItems() {
    try {
      const res = await _fetchAllItems()
      items.value = res.data
    } catch (error) {
      if (error.status === 401) {
        _tokenExpired()
      } 
      const message = error.response.data.error
      console.log(message)
    }
  }

  async function createItem(itemData) {
    try {
      const res = await _createItem(itemData)
      currentItem.value = res.data
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

  async function fetchItem(itemId) {
    try {
      const res = await _fetchItem(itemId)
      currentItem.value = res.data
    } catch (error) {
      if (error.status === 401) {
        _tokenExpired()
      } 
      const message = error.response.data.error
      console.log(message)
    }
  }

  async function updateItem(itemId, itemData) {
    try {
      const res = await _updateItem(itemId, itemData)
      currentItem.value = res.data
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

  async function deleteItem(itemId) {
    try {
      const res = await _deleteItem(itemId)
      currentItem.value = null
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
    items,
    currentItem,
    fetchAllItems,
    createItem,
    fetchItem,
    updateItem,
    deleteItem,
    init
  }
})
