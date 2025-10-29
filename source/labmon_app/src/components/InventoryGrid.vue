<template>
  <div>
    <!-- Empty inventory -->
    <p v-if="props.items.filter(item => getQuantity(item) > 0).length === 0" class="empty-message">
      {Error} Inventory buffer empty. Fetch some items from the shop()!
    </p>

    <div v-else class="item-grid">
      <InventoryEntryCard
        v-for="item in props.items.filter(item => getQuantity(item) > 0)"
        :key="item.id"
        :item="mapItem(item)"
        :quantity="getQuantity(item)"
      />
    </div>
  </div>
</template>

<script setup>
import InventoryEntryCard from './InventoryEntryCard.vue'
import { useItemStore } from '../stores/itemStore'
import { computed } from 'vue'

const itemStore = useItemStore()

const items = computed(() => itemStore.items)

const props = defineProps({
  items: {
    type: Array,
    default: () => []
  },
  inventory: {
    type: Array,
    default: () => []
  }
})


const mapItem = (i) => ({
  id: i.id,
  name: i.name, 
  sprite: i.sprite
 })

const getQuantity = (item) => {
  console.log(props)
  const entry = props.inventory.find(i => i.item_id === item.id)
  return entry ? entry.qty : 0
}

</script>

<style scoped>
.item-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 16px;
  padding: 16px;
}

.empty-message {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 200px; 
  width: 60%; 
  margin: 60px auto; 
  padding: 16px 24px;

  font-family: 'Courier New', monospace;
  font-size: 1.1em;
  font-weight: bold;
  color: #ff4d4d;
  text-align: center;

  background-color: #111; 
  border: 2px solid #ff4d4d;
  border-radius: 8px;
  box-shadow: 0 0 8px rgba(255, 77, 77, 0.3);
}
</style>