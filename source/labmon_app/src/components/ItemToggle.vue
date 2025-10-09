<template>
  <div
    class="card flex-row align-items-center p-2 mb-2"
    :class="{
      'border-primary': isSelected,
      'border-secondary': !isSelected
    }"
    style="max-width: 300px; cursor: pointer;"
    @click="handleSelect"
  >
    <img
      :src="itemData.sprite"
      alt="Item sprite"
      class="img-fluid rounded-start"
      style="width: 50px; height: 50px; object-fit: contain;"
    />
    <div class="ms-3">
      <h6 class="mb-1">{{ itemData.name }}</h6>
      <p class="mb-0 text-muted">Qty: {{ itemData.quantity }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  itemData: {
    type: Object,
    required: true,
    default: () => ({
      id: null,
      name: '',
      quantity: 0,
      sprite: ''
    })
  },
  onSelect: {
    type: Function,
    default: (x) => {return x}
  }
})

const isSelected = ref(false)

function handleSelect() {
  isSelected.value = !isSelected.value
  if (isSelected.value) {
    props.onSelect(props.itemData.id)
  }
}
</script>

<style scoped>
.card {
  border: 2px solid;
  border-radius: 0.5rem;
  transition: border-color 0.2s ease;
}
</style>
