<template>
    <div class="timer-section">
        <Timer class="mt-4"/>
        <button class="start-encounter-button" v-if="uiStore.timerIsRunning" @click="handleStartEncounter">
            Fix bug!
        </button>
        <button class="start-button" v-if="!uiStore.timerIsRunning" @click="uiStore.startTimer">
            Start debugging!
        </button>
    </div>

    <div class="catch-rate">
        {{ formattedCatchRate }}
    </div>

    <CatchSuccessModal v-if="uiStore.showCatchSuccess"/>
    <CatchFailModal v-if="uiStore.showCatchFail"/>
</template>

<script setup>
import { computed } from 'vue';
import { useAuthStore } from '../stores/authStore';
import { useUiStore } from '../stores/uiStore';
import { useEncounterStore } from '../stores/encunterStore';
import router from '../router';
import Timer from '../components/Timer.vue';
import CatchSuccessModal from '../components/CatchSuccessModal.vue';
import CatchFailModal from '../components/CatchFailModal.vue';

const authStore = useAuthStore()
const uiStore = useUiStore()
const encounterStore = useEncounterStore()

const formattedCatchRate = computed(() => {
  const rate = uiStore.catchRateStat || 0
  return `Community catch rate: ${(rate * 100).toFixed(1)}%`
})

async function handleStartEncounter() {
    const result = await encounterStore.requestEncounter()
    if (result) {
        uiStore.stopTimer()
        router.push("/encounter")
    }
}
</script>

<style>
.timer-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: start;
  height: 70vh;
  color: #ffffff;
  font-family: 'Courier New', Courier, monospace;
}

.start-button,
.start-encounter-button {
  font-size: 1.5rem;
  padding: 0.75rem 2rem;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.start-button {
  background-color: #4caf50;
}
.start-encounter-button {
  background-color: #55f;
}

.start-button:hover:enabled {
  background-color: #45a049;
}


.catch-rate {
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 2em; 
  font-weight: bold;
  color: #505050; 
  text-align: center;
  margin-top: 2rem;
}
</style>
