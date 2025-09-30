<template>
  <div class="container d-flex align-items-center my-2">
    <div class="card shadow p-4" style="width: 100%; min-width: 400px;">
      <h2 class="mb-4 text-center">Create Item</h2>
        <form @submit.prevent="handleSubmit">
            <div class="mb-3">
            <label for="name" class="form-label">Item Name</label>
            <input v-model="form.name" type="text" id="name" class="form-control" required />
            </div>

            <div class="mb-3">
            <label for="price" class="form-label">Price</label>
            <input v-model="form.price" type="text" id="price" class="form-control" required />
            </div>

            <div class="mb-3">
            <label for="description" class="form-label">Description</label>
            <input v-model="form.description" type="text" id="description" class="form-control" required />
            </div>

            <div class="mb-3">
            <label for="effect" class="form-label">Effect</label>
            <input v-model="form.effect" type="text" id="effect" class="form-control" required />
            </div>

            <div class="mb-3">
            <label for="sprite" class="form-label">Sprite URL</label>
            <input v-model="form.sprite" type="text" id="sprite" class="form-control" required />
            </div>

            <button type="submit" class="btn btn-success">Create Item</button>

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
import { useItemStore } from '../stores/itemStore'

const form = ref({
  name: '',
  price: '',
  description: '',
  effect: '',
  sprite: ''
})

const successMessage = ref('')
const errorMessage = ref('')

const handleSubmit = async () => {
  successMessage.value = ''
  errorMessage.value = ''
  const itemStore = useItemStore()
  try {
    await itemStore.createItem(form.value)
    console.log(form.value)
    successMessage.value = 'Item created successfully!'
    form.value = {
      name: '',
      price: '',
      description: '',
      effect: '',
      sprite: ''
    }
    await itemStore.fetchAllItems()
  } catch (err) {
    errorMessage.value = err.response?.data?.message || 'Failed to create item.'
  }
}
</script>
