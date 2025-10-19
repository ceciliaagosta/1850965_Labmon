<template>
  <div
    class="modal fade show" tabindex="-1" role="dialog" style="display: block; background-color: rgba(0,0,0,0.5);" @click.self="close"
  >
    <div class="modal-dialog" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">200: Success!</h5>
          <button type="button" class="btn-close" @click="close" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <slot>
            <div v-if="caughtMonster">
                <div class="text-center">
                    <img
                    :src="caughtMonster.sprite"
                    :alt="caughtMonster.name"
                    class="img-fluid"
                    style="max-height: 150px;"
                    />
                    <h4 class="mt-3">{{ caughtMonster.name }}</h4>
                    Reward: +{{ reward }}
                </div>
                </div>
                <div v-else>
                <p>Loading monster info...</p>
                </div>
          </slot>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-primary" @click="close">Continue</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useMonsterStore } from '../stores/monsterStore';
import { useUiStore } from '../stores/uiStore';
import { useEncounterStore } from '../stores/encunterStore';

const uiStore = useUiStore()
const monsterStore = useMonsterStore()

const caughtMonster = computed(() => monsterStore.currentMonster)
const reward = computed(() => uiStore.reward)

function close() {
    uiStore.showCatchSuccess = false
}
</script>
