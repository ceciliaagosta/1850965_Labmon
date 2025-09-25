<template>
    <EditUserForm :userData="userData" :isAdmin="false" v-if="userData"/>

    <DeleteAccountButton :userId="authStore.userId"/>
</template>

<script setup>
import { computed } from 'vue';
import DeleteAccountButton from '../components/DeleteAccountButton.vue';
import EditUserForm from '../components/EditUserForm.vue';
import { useAuthStore } from '../stores/authStore';

const authStore = useAuthStore()

const userData = computed(() => authStore.user)

</script>