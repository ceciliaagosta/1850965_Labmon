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
    {{ confirming ? 'Delete Anyway' : 'Delete Monster ' }}
    </button>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useMonsterStore } from '../stores/monsterStore'

const confirming = ref(false)
const loading = ref(false)

const props = defineProps({
  monsterId: {
    type: Number,
    required: true,
  }
})

const handleClick = async () => {
  const monsterStore = useMonsterStore()
  if (!confirming.value) {
    confirming.value = true
    return
  }

  loading.value = true
  try {
    await monsterStore.deleteMonster(props.monsterId)
    await monsterStore.fetchAllMonsters()
  } catch (error) {
    console.error('Deletion failed:', error)
  } finally {
    loading.value = false
  }
}
</script>
