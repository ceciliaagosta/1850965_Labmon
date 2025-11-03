<template>

  <ItemToggle v-for="item in inventory" 
    :itemData="item" 
    :onSelect="handleItemSelected" 
    :isSelected="item.item_id==encounterStore.selectedItem" />
  
</template>

<script setup>
import ItemToggle from './ItemToggle.vue'
import { ref } from 'vue'
import { useInventoryStore } from '../stores/inventoryStore'
import { useEncounterStore } from '../stores/encunterStore'
import { computed } from 'vue'

const inventoryStore = useInventoryStore()
const encounterStore = useEncounterStore()

const inventory = computed(() => inventoryStore.inventory)

function handleItemSelected(itemId) {
  if (itemId == encounterStore.selectedItem) {
    encounterStore.selectedItem = -1
  } else {
    encounterStore.selectedItem = itemId
  }
}

</script>