<template>
    <div class="timer-section">
        <Timer class="mt-4"/>
        <button class="start-encounter-button" v-if="uiStore.timerIsRunning" @click="handleStartEncounter">
            Request encounter
        </button>
        <button class="start-button" v-if="!uiStore.timerIsRunning" @click="uiStore.startTimer">
            Start debugging!
        </button>
    </div>

    <!-- <div v-if="uiStore.showCatchSuccess" class="modal-overlay" @click.self="uiStore.showCatchSuccess = false">
      <div class="success-card">
        <h3>Success!</h3>
        <p>The encounter was successfully started.</p>
        <button @click="uiStore.showCatchSuccess = false">Close</button>
      </div>
    </div> -->

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

async function handleStartEncounter() {
    var result = await encounterStore.requestEncounter()
    if (result) {
        const elapsedTime = uiStore.stopTimer()
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
  background-color: #55f;
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

<!-- .modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5); /* semi-transparent overlay */
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000; /* high enough to sit on top */
}

.success-card {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
  max-width: 400px;
  width: 90%;
  text-align: center;
  z-index: 1001;
}
 -->