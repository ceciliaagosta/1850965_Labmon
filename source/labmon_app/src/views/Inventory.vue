<template>
  <div>
    <InventoryGrid 
    :items="inventoryStore.allItems" 
    :inventory="inventoryStore.inventory" 
    />
  </div>
</template>

<script setup>
    import { computed, onMounted } from 'vue';
    import { useInventoryStore } from '../stores/inventoryStore';
    import InventoryGrid from '../components/InventoryGrid.vue';

    const inventoryStore = useInventoryStore()
    const allItems = computed(() => inventoryStore.allItems)

    onMounted( async () => {
        await inventoryStore.fetchInventory()
    })
</script>