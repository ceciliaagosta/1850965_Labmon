<template>
  <div class="container">
    <div class="d-flex">
      <div class="col-8">
        <EncounterPanel
          :monster="wildMonster"
          :onCatch="handleCatch"
          :onEscape="handleEscape"
          />
      </div>
      <div class="col-4 bg-secondary" v-if="false">
        <ItemsPanel/>
      </div>
    </div>
  </div>
</template>

<script setup>
import EncounterPanel from '../components/EncounterPanel.vue';
import ItemsPanel from '../components/ItemsPanel.vue';
import { useEncounterStore } from '../stores/encunterStore';
import { onBeforeRouteLeave } from 'vue-router';

const encounterStore = useEncounterStore()
const encounterId = 0

onBeforeRouteLeave((to, from, next) => {
  encounterStore.resetEncounter()
  next();
});

function handleCatch() {
  console.log('Tried to catch the monster!')
}

function handleEscape() {
  console.log('Escaped from the monster!')
  encounterStore.escapeEncounter(encounterId)
}

const wildMonster = {
  name: 'Wild Gengar',
  sprite: 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/94.png'
}

</script> 