<template>
    <div class="px-4">
        <UsersTable :data="allUsers"/>
        <MonstersTable :data="allMonsters" />
        <ItemsTable :data="allItems" />
    </div>
</template>

<script setup>
import { computed, onMounted } from 'vue';
import { useUserStore } from '../stores/userStore';
import { useMonsterStore } from '../stores/monsterStore';
import { useItemStore } from '../stores/itemStore';

import UsersTable from '../components/UsersTable.vue';
import MonstersTable from '../components/MonstersTable.vue';
import ItemsTable from '../components/ItemsTable.vue';

const userStore = useUserStore()
const monsterStore = useMonsterStore()
const itemStore = useItemStore()

onMounted(async () => {
  await userStore.fetchAllUsers()
  await monsterStore.fetchAllMonsters()
  await itemStore.fetchAllItems()
})

const allUsers = computed(() => userStore.users)
const allMonsters = computed(() => monsterStore.monsters)
const allItems = computed(() => itemStore.items)
</script>