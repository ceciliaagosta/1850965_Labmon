<template>
  <div class="container d-flex align-items-center my-2">
    <div class="card shadow p-4" style="width: 100%; min-width: 400px;">
      <h2 class="mb-4 text-center">Create User</h2>

      <form @submit.prevent="handleRegister">
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
        <div class="mb-3">
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

        <!-- Password -->
        <div class="mb-3">
          <label for="password" class="form-label">Password</label>
          <input
            type="password"
            id="password"
            class="form-control"
            v-model="password"
            required
          />
        </div>

        <!-- Confirm Password -->
        <div class="mb-3">
          <label for="confirmPassword" class="form-label">Confirm Password</label>
          <input
            type="password"
            id="confirmPassword"
            class="form-control"
            v-model="confirmPassword"
            required
          />
        </div>

        <!-- Error Message -->
        <div v-if="error" class="alert alert-danger py-2">
          {{ error }}
        </div>

        <!-- Submit Button -->
        <button type="submit" class="btn btn-success w-100" :disabled="loading">
          <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
          Create user
        </button>
      </form>

    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
// import { useAuthStore } from '../stores/authStore';
import router from '../router';
import { useUserStore } from '../stores/userStore';


const userStore = useUserStore()

const username = ref('');
const email = ref('');
const role = ref('user');
const password = ref('');
const confirmPassword = ref('');
const loading = ref(false);
const error = ref('');

const handleRegister = async () => {
  error.value = '';

  if (password.value.length < 8) {
    error.value = 'Password must be at least 8 characters long.';
    return;
  }

  if (password.value !== confirmPassword.value) {
    error.value = 'Passwords do not match.';
    return;
  }

  loading.value = true;

  error.value = await userStore.manualRegister({
    username: username.value,
    email: email.value,
    password: password.value,
    role: role.value,
  });
  userStore.fetchAllUsers()
  loading.value = false;
};
</script>
