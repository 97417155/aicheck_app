<script setup>
import { store, closeDialog } from '../store'

const iconMap = { warn: '!', err: '!', ok: '✓' }
</script>

<template>
  <Transition name="fade">
    <div v-if="store.dialog.visible" class="mask" @click.self="store.dialog.cancelText && closeDialog(false)">
      <div class="dialog">
        <div class="dg-body">
          <div class="dg-icon" :class="store.dialog.icon">{{ iconMap[store.dialog.icon] || '!' }}</div>
          <div>{{ store.dialog.message }}</div>
        </div>
        <div class="dg-foot">
          <button v-if="store.dialog.cancelText" @click="closeDialog(false)">
            {{ store.dialog.cancelText }}
          </button>
          <button class="primary" @click="closeDialog(true)">
            {{ store.dialog.confirmText }}
          </button>
        </div>
      </div>
    </div>
  </Transition>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.15s;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
