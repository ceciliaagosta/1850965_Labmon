<template>
  <div class="card p-4 shadow-sm mb-3 d-flex flex-column justify-content-between align-items-center text-center monster-encounter">
    <!-- Monster Sprite -->
    <img
      :src="sprite"
      alt="Monster sprite"
      class="monster-sprite mb-3"
    />
    <!-- Monster Name -->
    <h4 class="mb-4">{{ monster.name }}</h4>

    <!-- Buttons -->
    <div class="d-flex gap-3 w-100 justify-content-center mt-auto">
      <button class="btn btn-secondary flex-fill" @click="onEscape">Escape</button>
      <button class="btn btn-primary flex-fill" @click="onCatch">Try & Catch</button>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  monster: {
    type: Object,
    required: true,
    default: () => ({
      name: '',
      sprite: ''
    })
  },
  onCatch: {
    type: Function,
    required: true
  },
  onEscape: {
    type: Function,
    required: true
  }
});

const sprite = "/sprites/" + props.monster.sprite
</script>

<style scoped>
.monster-encounter {
  min-height: 400px;
  border: 1px solid #dee2e6;
  border-radius: 0.5rem;
  background-color: #fff;
}

.monster-sprite {
  width: 450px;
  height: 450px;
  object-fit: contain;
}
</style>
