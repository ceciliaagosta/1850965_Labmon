<template>
  <div class="d-flex justify-content-between align-items-center mx-3 mb-3">
    <h2 class="mb-0">Collection {{ collectionNumber }}</h2>
    <button class="btn btn-primary me-3">
      Claim
    </button>
  </div>
  <div class="monster-grid">
    <CollectionEntryCard
      v-for="monster in props.monsters"
      :key="monster.id"
      :monster="mapMonster(monster)"
      :quantity="getQuantity(monster)"
      :caught="isCaught(monster)"
      @shard="onShard"
    />
  </div>
</template>

<script setup>
import CollectionEntryCard from './CollectionEntryCard.vue'
import { useMonsterStore } from '../stores/monsterStore'
import { computed } from 'vue'

const monsterStore = useMonsterStore()

const monsters = computed(() => monsterStore.monsters)

const props = defineProps({
  monsters: {
    type: Array,
    default: () => []
  },
  collection: {
    type: Object,
    default: () => ({}),
  },
  collectionNumber: {
    type: Number,
    required: true
  }
})


const mapMonster = (m) => ({
  id: m.id,
  name: m.name,
  collectionNumber: m.collection,
  sprite: m.sprite,
  rarity: `Rarity ${m.rarity}`,
})

const getQuantity = (monster) => props.collection[monster.id] ?? 0

const isCaught = (monster) => monster.id in props.collection

const onShard = (monster) => {
  console.log("sharded")
}
</script>

<style scoped>
.monster-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 16px;
  padding: 16px;
}
</style>
