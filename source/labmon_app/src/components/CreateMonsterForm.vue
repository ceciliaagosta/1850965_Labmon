<template>
  <div class="container d-flex align-items-center my-2">
    <div class="card shadow p-4" style="width: 100%; min-width: 400px;">
      <h2 class="mb-4 text-center">Create Monster</h2>
        <form @submit.prevent="handleSubmit">
            <div class="mb-3">
              <label for="name" class="form-label">Monster Name</label>
              <input v-model="form.name" type="text" id="name" class="form-control" required />
            </div>

            <div class="mb-3">
              <label for="catch_rate" class="form-label">Catch Rate</label>
              <input v-model="form.catch_rate" type="text" id="catchRate" class="form-control" required />
            </div>

            <div class="mb-3">
              <label for="collection" class="form-label">Collection</label>
              <input v-model="form.collection" type="text" id="collection" class="form-control" required />
            </div>

            <div class="mb-3">
              <label for="rarity" class="form-label">Rarity</label>
              <input v-model="form.rarity" type="text" id="rarity" class="form-control" required />
            </div>

            <div class="mb-3">
              <label for="sprite" class="form-label">Sprite URL</label>
              <input v-model="form.sprite" type="text" id="sprite" class="form-control" required />
            </div>

            <button type="submit" class="btn btn-success w-100" :disabled="loading">
              <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
              Create monster
            </button>

            <div v-if="successMessage" class="alert alert-success mt-3">
              {{ successMessage }}
            </div>

            <div v-if="errorMessage" class="alert alert-danger mt-3">
              {{ errorMessage }}
            </div>
        </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useMonsterStore } from '../stores/monsterStore'

const form = ref({
  name: '',
  catch_rate: '',
  collection: '',
  rarity: '',
  sprite: ''
})

const loading = ref(false);
const successMessage = ref('')
const errorMessage = ref('')

const handleSubmit = async () => {
  successMessage.value = ''
  errorMessage.value = ''
  const monsterStore = useMonsterStore()
  loading.value = true;
  errorMessage.value = await monsterStore.createMonster(form.value)

  console.log(form.value)

  if (errorMessage.value) {
    loading.value = false;
    return;
  }

  successMessage.value = 'Monster created successfully!'

  form.value = {
    name: '',
    catch_rate: '',
    collection: '',
    rarity: '',
    sprite: ''
  }

  await monsterStore.fetchAllMonsters()
  loading.value = false;
}
</script>
