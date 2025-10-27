<template>
    <CollectionGrid
        :collection="collectionStore.collection"
        :collectionNumber="1"    
    />
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