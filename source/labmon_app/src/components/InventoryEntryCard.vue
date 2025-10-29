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

      <div class="footer">
        <span class="quantity">x{{ quantity }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useInventoryStore } from '../stores/inventoryStore';

const props = defineProps({
  item: {
    type: Object,
    required: true,
  },
  quantity: {
    type: Number,
    required: true,
  }
});

const inventoryStore = useInventoryStore()

const sprite = "/sprites/" + props.item.sprite

</script>

<style scoped>
.item-card {
  width: 200px;
  height: 300px;
  border: 2px solid #ccc;
  border-radius: 10px;
  background: #fafafa;
  padding: 10px;
  display: flex;
  flex-direction: column;
  justify-content: space-between; 
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
  height: 80 px;             
  margin: 10px 0;            
}

.sprite {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.footer {
  display: flex;
  justify-content: center; 
  align-items: center;
  border-top: 1px solid #eee;
  height: 30px; 
  padding-top: 6px;
}

.quantity {
  font-weight: bold;
}
</style>