<template>
  <div id="app">
    <Navbar v-if="uiStore.showNavbar"/>
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
import { onMounted } from 'vue';

// store rehydration
const authStore = useAuthStore()
const uiStore = useUiStore()
onMounted(() => {
  authStore.init()
  uiStore.init()
})

</script>

