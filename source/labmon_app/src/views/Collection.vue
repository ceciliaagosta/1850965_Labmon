<template>
  <div v-for="(monsters, number) in collectionStore.collections" :key="number">
    <CollectionGrid
      :collection="collectionStore.collection"
      :collectionNumber="number"
      :monsters="monsters"
    />
  </div>
</template>

<script setup>
    import { computed, onMounted } from 'vue';
    import { useCollectionStore } from '../stores/collectionStore';
    import CollectionGrid from '../components/CollectionGrid.vue';

    const collectionStore = useCollectionStore()
    const allMonsters = computed(() => collectionStore.allMonsters)

    onMounted( async () => {
        await collectionStore.fetchCollection()
    })
</script>