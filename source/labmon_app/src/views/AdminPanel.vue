<template>
    <div class="px-4">
        <UsersTable :data="allUsers"/>
        <MonstersTable :data="allMonsters" />
    </div>
</template>

<script setup>
import { computed, onMounted } from 'vue';
import { useUserStore } from '../stores/userStore';
import { useMonsterStore } from '../stores/monsterStore';
import UsersTable from '../components/UsersTable.vue';
import MonstersTable from '../components/MonstersTable.vue';

const userStore = useUserStore()
const monsterStore = useMonsterStore()

onMounted(async () => {
  await userStore.fetchAllUsers()
  await monsterStore.fetchAllMonsters()
})

const allUsers = computed(() => userStore.users)
const allMonsters = computed(() => monsterStore.monsters)
</script>