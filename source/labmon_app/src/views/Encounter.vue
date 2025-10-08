<template>
<EncounterPanel/>
<ItemsPanel/>

</template>

<script setup>
import EncounterPanel from '../components/EncounterPanel.vue';
import ItemsPanel from '../components/ItemsPanel.vue';
import { useEncounterStore } from '../stores/encunterStore';
import { onBeforeRouteLeave } from 'vue-router';

onBeforeRouteLeave((to, from, next) => {
  const encounterStore = useEncounterStore()
  encounterStore.resetEncounter()
  next();
});

</script> 