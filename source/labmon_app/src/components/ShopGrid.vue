<template>
  <div>
    <!-- Empty shop -->
    <p v-if="props.items.length === 0" class="empty-message">
      {Error} Shop is empty. Wait for a restock()!
    </p>

    <div v-else class="item-grid">
      <ShopEntryCard
        v-for="item in props.items"
        :key="item.id"
        :item="mapItem(item)"
      />
    </div>
  </div>
</template>

<script setup>
import ShopEntryCard from './ShopEntryCard.vue'

const props = defineProps({
  items: {
    type: Array,
    default: () => []
  },
})


const mapItem = (i) => ({
  id: i.id,
  name: i.name, 
  sprite: i.sprite,
  price: i.price
 })

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