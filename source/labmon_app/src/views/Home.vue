<template>
    <div class="timer-section">
        <Timer class="mt-4"/>
        <button class="start-encounter-button" v-if="uiStore.timerIsRunning" @click="handleStartEncounter">
            DEBUG: Start Encounter
        </button>
        <button class="start-button" v-if="!uiStore.timerIsRunning" @click="uiStore.startTimer">
            Start debugging!
        </button>
    </div>
</template>

<script setup>
import { computed } from 'vue';
import { useAuthStore } from '../stores/authStore';
import { useUiStore } from '../stores/uiStore';
import { useEncounterStore } from '../stores/encunterStore';
import router from '../router';
import Timer from '../components/Timer.vue';

const authStore = useAuthStore()
const uiStore = useUiStore()
const encounterStore = useEncounterStore()

function handleStartEncounter() {
    const elapsedTime = uiStore.stopTimer()
    encounterStore.getEncounter()
    router.push("/encounter")
}
</script>

<style>

.timer-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: start;
  height: 100vh;
  /* background-color: #1e1e2f; */
  color: #ffffff;
  font-family: 'Courier New', Courier, monospace;
}

.start-button {
  font-size: 1.5rem;
  padding: 0.75rem 2rem;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.start-encounter-button {
  background-color: #777;
  font-size: 1.5rem;
  padding: 0.75rem 2rem;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.start-button:hover:enabled {
  background-color: #45a049;
}

</style>