<template>
  <div>
    <p v-if="confirming" class="text-danger mb-2">
      Are you sure? This action is <strong>irreversible</strong>.
    </p>
    <button
    class="btn btn-danger"
    @click="handleClick"
    :disabled="loading"
    >
    <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
    {{ confirming ? 'Delete Anyway' : 'Delete Item ' }}
    </button>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useItemStore } from '../stores/itemStore'

const confirming = ref(false)
const loading = ref(false)

const props = defineProps({
  itemId: {
    type: Number,
    required: true,
  }
})

const handleClick = async () => {
  const itemStore = useItemStore()
  if (!confirming.value) {
    confirming.value = true
    return
  }

  loading.value = true
  try {
    await itemStore.deleteItem(props.itemId)
    await itemStore.fetchAllItems()
  } catch (error) {
    console.error('Deletion failed:', error)
  } finally {
    loading.value = false
  }
}
</script>