<template>
  <div class="position-fixed top-3 end-0 p-3" style="z-index: 1050;">
    <div
      v-for="(notification, index) in notifications"
      :key="index"
      :class="['alert', alertClass(notification.type), 'alert-dismissible', 'fade', 'show']"
      role="alert"
    >
      {{ notification.message }}
      <button type="button" class="btn-close" @click="removeNotification(index)" aria-label="Close"></button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useUiStore } from '../stores/uiStore';

const uiStore = useUiStore();

const notifications = computed(() => uiStore.notifications);

function alertClass(type) {
  switch (type) {
    case 'success':
      return 'alert-success';
    case 'error':
      return 'alert-danger';
    case 'info':
    default:
      return 'alert-info';
  }
}

function removeNotification(index) {
  uiStore.notifications.splice(index, 1); // Assuming notifications is a reactive array
}
</script>
