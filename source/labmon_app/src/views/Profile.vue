<template>
    {{ authStore.user }}
    <DeleteAccountButton :userId="authStore.userId"/>
</template>

<script setup>
import DeleteAccountButton from '../components/DeleteAccountButton.vue';
import { useAuthStore } from '../stores/authStore';

const authStore = useAuthStore()
</script>