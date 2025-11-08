<template>
  <div class="d-flex justify-content-between align-items-center mx-3 mb-3">
    <div>
      <h2 class="mb-0">Collection {{ collectionNumber }}</h2>
      claimed by {{ formattedClaimedStat }}
    </div>
    <button class="btn btn-primary me-3" @click="handleClaim">
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
import { useCollectionStore } from '../stores/collectionStore'
import { useMonsterStore } from '../stores/monsterStore'
import { computed } from 'vue'
import { useUiStore } from '../stores/uiStore'

const collectionStore = useCollectionStore()
const uiStore = useUiStore()

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

const claimedStatRaw = computed(() => uiStore.claimedStat[props.collectionNumber] || 0)
const formattedClaimedStat = computed(() => `${(claimedStatRaw.value * 100).toFixed(1)}%`)

const handleClaim = async () => {
  await collectionStore.claimCollection(props.collectionNumber)
}

const mapMonster = (m) => ({
  id: m.id,
  name: m.name,
  collectionNumber: m.collection,
  sprite: m.sprite,
  rarity: `Rarity ${m.rarity}`,
})

const getQuantity = (monster) => props.collection[monster.id] ?? 0
const isCaught = (monster) => monster.id in props.collection
const onShard = (monster) => console.log("sharded")
</script>

<style scoped>
.monster-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 16px;
  padding: 16px;
}
</style>
