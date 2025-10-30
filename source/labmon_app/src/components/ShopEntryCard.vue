<template>
  <div class="item-card">
    
    <div class="item-content">
      <div class="header">
        <h3 class="name">{{ item.name }}</h3>
        <span class="number">#{{ item.id }}</span>
      </div>

      <div class="image-container">
        <img :src="sprite" :alt="item.name" class="sprite" />
      </div>    
      
      <div class="description">
        {{ item.description }}
      </div>

      <div class="footer">
        <button
          class="buy-button"
          @click="handleBuy"
        >
          ${{ item.price }}
        </button>

      </div>
    </div>
  </div>
</template>

<script setup>

import { _buy } from '../services/gameApi'
import { useUiStore } from '../stores/uiStore'
import { useUserStore } from '../stores/userStore'

const props = defineProps({
  item: {
    type: Object,
    required: true,
  }
});

const sprite = "/sprites/" + props.item.sprite
const uiStore = useUiStore()
const userStore = useUserStore()

async function handleBuy() {
  try {
    let res = await _buy(props.item.id)
    console.log("bought", props.item.id)
    userStore.fetchPlayerCurrency()
    uiStore.showNotification(`You bought the ${props.item.name}.`, "success")
  } catch(err) {
    console.log(err)
    uiStore.showNotification(err.response.data.error, "error")
  }
}

</script>

<style scoped>
.buy-button {
  background-color: #007bff; /* Bright blue */
  color: white;
  border: none;
  border-radius: 6px;
  padding: 10px 16px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.buy-button:hover {
  background-color: #0056b3; /* Darker blue on hover */
}

.footer {
  display: flex;
  justify-content: center;
  align-items: center;
  border-top: 1px solid #eee;
  height: 50px; 
  padding-top: 6px;
  margin-top: auto;
}

.item-card {
  width: 200px;
  height: 300px;
  border: 2px solid #ccc;
  border-radius: 10px;
  background: #fafafa;
  padding: 10px;
  display: flex;
  flex-direction: column;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
  transition: transform 0.2s ease;
  overflow: hidden;
}

.number {
  font-size: 0.8em;
  color: #666;
}

.item-card:hover {
  transform: scale(1.02);
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  text-align: center;
  min-height: 40px;
}

.name {
  font-size: 1.1em;
  font-weight: bold;
  margin: 0;
  line-height: 1.2em;
  white-space: normal;      
  word-break: break-word;    
  text-align: center;
}

.image-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 80px; /* fixed height */
  margin: 10px 0;            
}

.sprite {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

/* 🆕 Description area: fixed height so all cards align perfectly */
.description {
  flex: 0 0 85; /* fixed space reserved for text */
  overflow-y: auto;
  font-size: 0.9rem;
  line-height: 1.2rem;
  color: #444;
  text-align: center;
  padding: 4px;
  scrollbar-width: thin;
}

/* 🆕 Ensure footer stays anchored at the bottom */
.item-content {
  display: flex;
  flex-direction: column;
  height: 100%;
}
</style>