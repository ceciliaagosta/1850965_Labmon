<template>
  <div
    class="card flex-row align-items-center p-2 mb-2"
    :class="{
      'border-primary bg-primary-subtle': props.isSelected,
      'border-secondary bg-white': !props.isSelected,
    }"
    style="max-width: 300px; cursor: pointer;"
    @click="handleSelect"
    v-if="!isLoading"
  >
    <img
      :src="sprite"
      alt="Item sprite"
      class="img-fluid rounded-start"
      style="width: 50px; height: 50px; object-fit: contain;"
    />
    <div class="ms-3">
      <h6 class="mb-1">{{ itemData.name }}</h6>
      <p class="mb-0 text-muted">Qty: {{ props.itemData.qty }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useItemStore } from '../stores/itemStore'

const props = defineProps({
  itemData: {
    type: Object,
    required: true,
  },
  onSelect: {
    type: Function,
    default: (x) => x,
  },
  isSelected: {
    type: Boolean,
    required: true,
  },
})

const isLoading = ref(true)
const itemStore = useItemStore()
const itemData = ref({})
const sprite = ref("")

onMounted(async () => {
  await itemStore.fetchItem(props.itemData.item_id)
  itemData.value = itemStore.getCurrentItem()
  sprite.value = "/sprites/" + itemData.value.sprite
  isLoading.value = false
})

function handleSelect() {
  props.onSelect(props.itemData.item_id)
}
</script>

<style scoped>
.card {
  border: 2px solid;
  border-radius: 0.5rem;
  transition: border-color 0.2s ease, background-color 0.2s ease;
}
</style>
