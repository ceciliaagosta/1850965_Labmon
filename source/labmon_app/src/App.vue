<template>
  <div id="app">
    <Navbar v-if="uiStore.showNavbar"/>

    <!-- 💰 Currency display -->
    <div v-if="uiStore.showNavbar" class="currency-display">
      💰 {{ userStore.currency }}
    </div>

    <Notifications/>
    <main class="py-4">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import Navbar from './components/Navbar.vue';
import Notifications from './components/Notifications.vue';
import { useUiStore } from './stores/uiStore';
import { useAuthStore } from './stores/authStore';
import { useUserStore } from './stores/userStore';
import { onMounted } from 'vue';

// store rehydration
const authStore = useAuthStore()
onMounted(() => {
  authStore.init()

  // If the user is logged in, get their currency from the backend
  if (authStore.isAuthenticated) {
    userStore.fetchPlayerCurrency()
  }
})

const uiStore = useUiStore()
const userStore = useUserStore()

</script>

<style scoped>
.currency-display {
  position: fixed;
  top: 10px;
  right: 15px;
  background: #222;
  color: #fff;
  padding: 6px 12px;
  border-radius: 6px;
  font-weight: bold;
  z-index: 1000;
  font-family: monospace;
}
</style>
