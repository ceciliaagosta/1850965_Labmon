<template>
  <div class="card my-4 shadow-sm">
    <div class="card-header">
      <h5 class="mb-0">Items</h5>
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
              Edit Item
            </th>
            <th>
              Delete Item
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, rowIndex) in data" :key="rowIndex">
            <td v-for="(key, colIndex) in objectKeys" :key="colIndex">
              {{ item[key] }}
            </td>
            <td>
              <button class="btn btn-primary" @click="handleEditItem(item)">Edit Item</button>
            </td>
            <td>
              <DeleteItemButton :itemId="item.id" />
            </td>
          </tr>
        </tbody>
      </table>
      <div v-else class="text-center text-muted p-3">
        No data to display.
      </div>
      <button class="btn btn-success mt-2" @click="handleCreateItem">
        {{ showCreateItemForm ? "Create Item (Hide)" : "Create Item (Show)" }}
      </button>
      <div class="d-flex gap-3">
        <div v-if="showCreateItemForm">
          <CreateItemForm/>
        </div>
        <div v-if="currentItemData">
          <!-- <EditUserForm :userData="currentUserData" :isAdmin="true" /> -->
            <EditItemForm :itemData="currentItemData"/>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import DeleteItemButton from './DeleteItemButton.vue';
import CreateItemForm from './CreateItemForm.vue';
import EditItemForm from './EditItemForm.vue';

const { data } = defineProps({
  data: {
    type: Array,
    required: true,
    default: () => []
  }
})

const showCreateItemForm = ref(false)
const currentItemData = ref(null)

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

const handleCreateItem = async () => {
  showCreateItemForm.value = !showCreateItemForm.value
};

const handleEditItem = async (item) => {
  currentItemData.value = item
};
</script>
