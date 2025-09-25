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
    {{ confirming ? 'Delete Anyway' : 'Delete Account ' }}
    </button>

  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '../stores/authStore'
import { useUserStore } from '../stores/userStore'

const confirming = ref(false)
const loading = ref(false)

const props = defineProps({
  userId: {
    type: Number,
    required: true,
  }
})

const handleClick = async () => {
  const authStore = useAuthStore()
  const userStore = useUserStore()
  if (!confirming.value) {
    confirming.value = true
    return
  }

  loading.value = true
  try {
    await userStore.deleteUser(props.userId)
    if (props.userId === authStore.userId) {
      await authStore.logout()
    } else {
      confirming.value = false
      userStore.fetchAllUsers()
    } 
  } catch (error) {
    console.error('Deletion failed:', error)
  } finally {
    loading.value = false
  }
}
</script>
