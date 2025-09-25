<template>
  <div class="card my-4 shadow-sm">
    <div class="card-header">
      <h5 class="mb-0">Users</h5>
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
              Edit User
            </th>
            <th>
              Delete User
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, rowIndex) in data" :key="rowIndex">
            <td v-for="(key, colIndex) in objectKeys" :key="colIndex">
              {{ item[key] }}
            </td>
            <td>
              <button class="btn btn-primary btn" @click="handleEditUser(item)">Edit User</button>
            </td>
            <td>
              <DeleteAccountButton :userId="item.id"/>
            </td>
          </tr>
        </tbody>
      </table>
      <div v-else class="text-center text-muted p-3">
        No data to display.
      </div>
      <button class="btn btn-success mt-2" @click="handleCreateUser">
        {{ showRegisterForm ? "Create user (Hide)" : "Create user (Show)" }}
      </button>
      <div class="d-flex gap-3">
        <div v-if="showRegisterForm">
          <ManualRegisterForm />
        </div>
        <div v-if="currentUserData">
          <EditUserForm :userData="currentUserData" :isAdmin="true" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import ManualRegisterForm from './ManualRegisterForm.vue'
import DeleteAccountButton from './DeleteAccountButton.vue'
import EditUserForm from './EditUserForm.vue'

const { data } = defineProps({
  data: {
    type: Array,
    required: true,
    default: () => []
  }
})

const showRegisterForm = ref(false)
const currentUserData = ref(null)

const objectKeys = computed(() => {
  return data.length > 0 ? Object.keys(data[0]) : []
})

const handleCreateUser = async () => {
  showRegisterForm.value = !showRegisterForm.value
};

const handleEditUser = async (user) => {
  currentUserData.value = user
};
</script>
