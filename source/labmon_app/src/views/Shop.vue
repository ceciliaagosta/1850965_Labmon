<template>
  <div>
    <ShopGrid 
    :items="itemStore.items"
    />
  </div>
</template>

<script setup>
    import { onMounted } from 'vue';
    import { useItemStore } from '../stores/itemStore';
    import ShopGrid from '../components/ShopGrid.vue';

    const itemStore = useItemStore()

    onMounted( async () => {
        await itemStore.fetchAllItems()
    })
</script>