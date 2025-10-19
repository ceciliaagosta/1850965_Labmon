<template>
    <div class="timer-display">
      {{ formattedTime }}
    </div>
</template>

<script setup>
import { computed } from 'vue'
import { useUiStore } from '../stores/uiStore'

const uiStore = useUiStore()

// Format seconds into hh:mm:ss
const formattedTime = computed(() => {
  const totalSeconds = uiStore.time
  const hours = Math.floor(totalSeconds / 3600).toString().padStart(2, '0')
  const minutes = Math.floor((totalSeconds % 3600) / 60).toString().padStart(2, '0')
  const seconds = (totalSeconds % 60).toString().padStart(2, '0')
  return `${hours}:${minutes}:${seconds}`
})
</script>

<style scoped>
.timer-display {
  font-size: 6rem;
  margin-bottom: 2rem;
  color: #20ff60;
  background: #202020;
  padding: 1rem 2rem;
  border-radius: 10px;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.5);
  letter-spacing: 0.1em;
}
</style>

