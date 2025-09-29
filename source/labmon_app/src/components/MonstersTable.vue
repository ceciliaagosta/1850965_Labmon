<template>
  <div class="card my-4 shadow-sm">
    <div class="card-header">
      <h5 class="mb-0">Monsters</h5>
    </div>

    <div class="card-body table-responsive">
      <table class="table table-bordered table-hover mb-0" v-if="data && data.length">
        <thead class="table-light">
          <tr>
            <th
              v-for="(key, index) in objectKeys"
              :key="index"
              class="text-capitalize"
            >
              {{ key }}
            </th>
            <th>
              Edit Monster
            </th>
            <th>
              Delete Monster
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, rowIndex) in data" :key="rowIndex">
            <td v-for="(key, colIndex) in objectKeys" :key="colIndex">
              {{ item[key] }}
            </td>
            <td>
              <button class="btn btn-primary" @click="handleEditMonster(item)">Edit Monster</button>
            </td>
            <td>
              <DeleteMonsterButton :monsterId="item.id" />
            </td>
          </tr>
        </tbody>
      </table>
      <div v-else class="text-center text-muted p-3">
        No data to display.
      </div>
      <button class="btn btn-success mt-2" @click="handleCreateMonster">
        {{ showCreateMonsterForm ? "Create Monster (Hide)" : "Create Monster (Show)" }}
      </button>
      <div class="d-flex gap-3">
        <div v-if="showCreateMonsterForm">
          <CreateMonsterForm/>
        </div>
        <div v-if="currentMonsterData">
          <!-- <EditUserForm :userData="currentUserData" :isAdmin="true" /> -->
            <EditMonsterForm :monsterData="currentMonsterData"/>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import DeleteMonsterButton from './DeleteMonsterButton.vue';
import CreateMonsterForm from './CreateMonsterForm.vue';
import EditMonsterForm from './EditMonsterForm.vue';

const { data } = defineProps({
  data: {
    type: Array,
    required: true,
    default: () => []
  }
})

const showCreateMonsterForm = ref(false)
const currentMonsterData = ref(null)

const objectKeys = computed(() => {
  if (data.length === 0) return []
  const keys = Object.keys(data[0])
  const idIndex = keys.indexOf('id')
  if (idIndex !== -1) {
    keys.splice(idIndex, 1)
    keys.unshift('id')
  }
  const nameIndex = keys.indexOf('name')
  if (nameIndex !== -1) {
    keys.splice(nameIndex, 1)
    keys.unshift('name')
  }
  return keys
})

const handleCreateMonster = async () => {
  showCreateMonsterForm.value = !showCreateMonsterForm.value
};

const handleEditMonster = async (monster) => {
  currentMonsterData.value = monster
};
</script>
