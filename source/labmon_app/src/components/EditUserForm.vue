<template>
    <div class="container d-flex align-items-center my-2">
      <div class="card shadow p-4" style="width: 100%; min-width: 400px;">
        <h2 class="mb-4 text-center">Edit User {{ props.userData.username }}</h2>
  
        <form @submit.prevent="handleEdit">
          <!-- Username -->
          <div class="mb-3">
            <label for="username" class="form-label">Username</label>
            <input
              type="text"
              id="username"
              class="form-control"
              v-model="username"
              required
            />
          </div>
  
          <!-- Email -->
          <div class="mb-3">
            <label for="email" class="form-label">Email</label>
            <input
              type="email"
              id="email"
              class="form-control"
              v-model="email"
              required
            />
          </div>
  
          <!-- Role -->
          <div class="mb-3" v-if="isAdmin">
            <label for="role" class="form-label">Role</label>
            <select
              id="role"
              class="form-select"
              v-model="role"
              required
            >
              <option value="user">User</option>
              <option value="admin">Admin</option>
            </select>
          </div>

          <div class="mb-3">
            <button class="btn btn-success" v-if="userData.id == authStore.user.id && !changingPassword" @click="handleToggleChangePassword">
              Change password
            </button>
          </div>
  
          <!-- Password -->
          <div class="mb-3" v-if="changingPassword">
            <label for="password" class="form-label">Password</label>
            <input
              type="password"
              id="password"
              class="form-control"
              v-model="password"
              required
            />
          </div>
  
          <!-- Old Password -->
          <div class="mb-3" v-if="changingPassword">
            <label for="oldPassword" class="form-label">Confirm Password</label>
            <input
              type="password"
              id="oldPassword"
              class="form-control"
              v-model="oldPassword"
              required
            />
          </div>
  
          <!-- Error Message -->
          <div v-if="successMessage" class="alert alert-success mt-3">
            {{ successMessage }}
          </div>

          <div v-if="errorMessage" class="alert alert-danger mt-3">
            {{ errorMessage }}
          </div>
  
          <!-- Submit Button -->
          <button type="submit" class="btn btn-success w-100" :disabled="loading">
            <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
            Edit user
          </button>
        </form>
  
      </div>
    </div>
  </template>
  
  <script setup>
  import { computed, ref, watch } from 'vue';
  // import { useAuthStore } from '../stores/authStore';
  import router from '../router';
  import { useUserStore } from '../stores/userStore';
import { isAxiosError } from 'axios';
import { useAuthStore } from '../stores/authStore';
  
  
  const userStore = useUserStore()

  const authStore = useAuthStore()
  
  const props = defineProps({
    userData: {
      type: Object,
      required: true
    },
    isAdmin: {
      type: Boolean,
      required: true
    }
  })

  const username = ref(props.userData.username);
  const email = ref(props.userData.email);
  const role = ref(props.userData.role);
  const password = ref('');
  const oldPassword = ref('');

  const changingPassword = ref(false);
  const loading = ref(false);
  const errorMessage = ref('');
  const successMessage = ref('');

  watch(
    () => props.userData,
    (newUserData) => {
      if (newUserData) {
        username.value = newUserData.username;
        email.value = newUserData.email;
        role.value = newUserData.role;
        changingPassword.value = false;
      }
    },
    {immediate: true}
  )

  const handleToggleChangePassword = async () => {
    changingPassword.value = !changingPassword.value
  };
  
  const handleEdit = async () => {
    errorMessage.value = '';
    successMessage.value = '';
    loading.value = true;

    if (props.isAdmin) {
      errorMessage.value = await userStore.updateUser(props.userData.id, {
        username: username.value,
        email: email.value,
        role: role.value,
        });
    } else {
      if ((password.value.length < 8) && changingPassword.value) {
        errorMessage.value = 'Password must be at least 8 characters long.';
        loading.value = false
        return;
      }
       
      if (changingPassword.value) {
        errorMessage.value = await userStore.updateUser(props.userData.id, {
        username: username.value,
        email: email.value,
        password: password.value,
        old_password: oldPassword.value
        });
      } else {
        errorMessage.value = await userStore.updateUser(props.userData.id, {
        username: username.value,
        email: email.value,
        });
      }
    }
    
    if (errorMessage.value) {
    loading.value = false;
    return;
    }

    if (props.isAdmin) {
      successMessage.value = 'User updated successfully!'
      userStore.fetchAllUsers()
    } else {
      const authStore = useAuthStore()
      authStore.user = userStore.currentUser
    }
    
    loading.value = false;
  };
  </script>
  