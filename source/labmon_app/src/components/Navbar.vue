<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <div class="container">
      <!-- Brand -->
      <router-link to="/" class="navbar-brand">Labmon</router-link>

      <!-- Toggler -->
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarNav"
        aria-controls="navbarNav"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav me-auto">
          <!-- Home -->
          <li class="nav-item">
            <router-link to="/" class="nav-link" exact>Home</router-link>
          </li>
          <!-- Collection -->
          <li class="nav-item" v-if="authStore.isAuthenticated">
            <router-link to="/collection" class="nav-link">Collection</router-link>
          </li>
          <!-- Inventory -->
          <li class="nav-item" v-if="authStore.isAuthenticated">
            <router-link to="/inventory" class="nav-link">Inventory</router-link>
          </li>
          <!-- Shop -->
          <li class="nav-item" v-if="authStore.isAuthenticated">
            <router-link to="/shop" class="nav-link">Shop</router-link>
          </li>
        </ul>

        <ul class="navbar-nav">
          <!-- Money counter -->
           
          <!-- Account dropdown if logged in -->
          <li class="nav-item dropdown" v-if="authStore.isAuthenticated">
            <a
              class="nav-link dropdown-toggle"
              href="#"
              role="button"
              data-bs-toggle="dropdown"
              aria-expanded="false"
            >
              {{ authStore.user?.username }}
                <!-- Account -->
            </a>
            <ul class="dropdown-menu dropdown-menu-end">
              <!-- Profile -->
              <li>
                <router-link to="/profile" class="dropdown-item">
                  Profile
                </router-link>
              </li>
              <!-- Admin panel -->
              <li>
                <router-link to="/admin_panel" v-if="authStore.isAdmin" class="dropdown-item">
                  Admin panel
                </router-link>
              </li>
              <li><hr class="dropdown-divider" /></li>
              <!-- Logout -->
              <li>
                <button class="dropdown-item text-danger" @click="handleLogout">
                  Logout
                </button>
              </li>
            </ul>
          </li>

          <!-- Login if not logged in -->
          <li class="nav-item" v-else>
            <router-link to="/login" class="nav-link">Login</router-link>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { useAuthStore } from '../stores/authStore';
import { useRouter } from 'vue-router';

const authStore = useAuthStore();
const router = useRouter();

const handleLogout = async () => {
  await authStore.logout();
};
</script>
