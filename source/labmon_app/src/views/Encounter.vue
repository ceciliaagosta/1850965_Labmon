<template>
  <div class="container">
    <div class="d-flex">
      <div class="col-8">
        <EncounterPanel v-if="!isLoading"
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
import { ref, onMounted, computed } from 'vue';
import EncounterPanel from '../components/EncounterPanel.vue';
import ItemsPanel from '../components/ItemsPanel.vue';
import { useEncounterStore } from '../stores/encunterStore';
import { onBeforeRouteLeave } from 'vue-router';
import { useMonsterStore } from '../stores/monsterStore';

const encounterStore = useEncounterStore();
const monsterStore = useMonsterStore();

const monster_id = encounterStore.encounterData.monster_id;
const isLoading = ref(true);
const wildMonster = computed(() => monsterStore.currentMonster);

onMounted(async () => {
  await monsterStore.fetchMonster(monster_id);
  isLoading.value = false;
});

onBeforeRouteLeave((to, from, next) => {
  encounterStore.resetEncounter();
  next();
});

function handleCatch() {
  console.log('Tried to catch the monster!');
  encounterStore.catchMonster(encounterStore.encounterData.encounter_id)
}

function handleEscape() {
  console.log('Escaped from the monster!');
  encounterStore.escapeEncounter(encounterStore.encounterData.encounter_id); 
}
</script>