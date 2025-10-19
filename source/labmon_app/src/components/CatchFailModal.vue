<template>
  <div
    class="modal fade show" tabindex="-1" role="dialog" style="display: block; background-color: rgba(0,0,0,0.5);" @click.self="close"
  >
    <div class="modal-dialog" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">500: Failed!</h5>
          <button type="button" class="btn-close" @click="close" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          The monster got away!
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-primary" @click="close">Aww...</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useUiStore } from '../stores/uiStore';

const uiStore = useUiStore()

function close() {
    uiStore.showCatchFail = false
}
</script>
