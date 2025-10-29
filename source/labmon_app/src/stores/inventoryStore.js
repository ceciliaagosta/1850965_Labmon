import { defineStore } from 'pinia'
import { ref, computed, toRaw } from 'vue'
import { _getInventory } from '../services/gameApi'
import { useItemStore } from './itemStore'
import { useUiStore } from './uiStore'

export const useInventoryStore = defineStore('inventory', () => {
    const itemStore = useItemStore()
    const uiStore = useUiStore()  

    const allItems = computed(() => itemStore.items)
    const inventory = ref({})

    async function fetchInventory() {
        await itemStore.fetchAllItems()
        try {
            const res = await _getInventory()
            inventory.value = res.data.inventory
        } catch (err) {
            console.log(err)
            uiStore.showNotification(err.response.data.error, "error")
        }
    }

    return {
        allItems,
        inventory,
        fetchInventory
    }

})