<template>
  <div class="monster-card">
    <div v-if="caught === false" class="monster-content">
        <div class="header">
            <div class="name">???</div>
            <span class="number">#{{ monster.id }}</span>
        </div>
        <div class="d-flex justify-content-center align-items-center" style="height: 180px;">
            <h1 class="text-secondary m-0">?</h1>
        </div>
    </div>

    <div v-else class="monster-content">
      <div class="header">
        <h3 class="name">{{ monster.name }}</h3>
        <span class="number">#{{ monster.id }}</span>
      </div>

      <div class="image-container">
        <img :src="sprite" :alt="monster.name" class="sprite" />
      </div>

      <div class="rarity">{{ monster.rarity }}</div>

      <div class="footer">
        <button
          class="shard-button"
          :disabled="quantity <= 0"
          @click="handleShard"
        >
          Shard
        </button>
        <span class="quantity">x{{ quantity }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useCollectionStore } from '../stores/collectionStore';

const props = defineProps({
  monster: {
    type: Object,
    required: true,
  },
  quantity: {
    type: Number,
    required: true,
  },
  caught: {
    type: Boolean,
    required: true,
  }
});

const collectionStore = useCollectionStore()

const sprite = "/sprites/" + props.monster.sprite

async function handleShard() {
  console.log("sharded", props.monster.id)
  await collectionStore.shardMonster(props.monster.id)
}
</script>

<style scoped>
.monster-card {
  width: 200px;
  border: 2px solid #ccc;
  border-radius: 10px;
  background: #fafafa;
  padding: 10px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
  transition: transform 0.2s ease;
}

.monster-card:hover {
  transform: scale(1.02);
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  margin-bottom: 8px;
}

.name {
  font-size: 1.1em;
  font-weight: bold;
  margin: 0;
}

.number {
  font-size: 0.8em;
  color: #666;
}

.image-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 120px;
}

.sprite {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.rarity {
  text-align: center;
  font-weight: 500;
  color: #555;
  margin: 8px 0;
}

.footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-top: 1px solid #eee;
  padding-top: 8px;
}

.shard-button {
  background: #4CAF50;
  color: white;
  border: none;
  border-radius: 6px;
  padding: 6px 10px;
  cursor: pointer;
  font-size: 0.9em;
  transition: background 0.2s ease;
}

.shard-button:disabled {
  background: #aaa;
  cursor: not-allowed;
}

.shard-button:not(:disabled):hover {
  background: #45a049;
}

.quantity {
  font-weight: bold;
}
</style>
