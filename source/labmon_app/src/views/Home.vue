<template>
    CIAO
    <button class="btn" @click="handleStartEncounter()">
        Start Encounter
    </button>
    [is encounter active {{ encounterStore.isEncounterActive }}]
</template>

<script setup>
import { computed } from 'vue';
import { useAuthStore } from '../stores/authStore';
import { useEncounterStore } from '../stores/encunterStore';
import router from '../router';

const authStore = useAuthStore()
const encounterStore = useEncounterStore()

function handleStartEncounter() {
    encounterStore.getEncounter()
    router.push("/encounter")
}
</script>