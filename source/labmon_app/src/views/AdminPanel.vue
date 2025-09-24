<template>
    <div class="px-4">
        <UsersTable :data="allUsers"/>
    </div>
</template>

<script setup>
import { computed, onMounted } from 'vue';
import { useUserStore } from '../stores/userStore';
import UsersTable from '../components/UsersTable.vue';

const userStore = useUserStore()

onMounted(async () => {
  await userStore.fetchAllUsers()
  // await userStore.fetchUser(2)
})

const allUsers = computed(() => userStore.users)
const user2 = computed(() => userStore.currentUser)
</script>