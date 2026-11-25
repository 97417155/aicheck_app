<script setup>
import { store } from '../store'
</script>

<template>
  <div id="toastRoot">
    <Transition name="pop">
      <div v-if="store.toast.visible" class="toast">{{ store.toast.msg }}</div>
    </Transition>
  </div>
</template>

<style scoped>
.pop-enter-active {
  transition: all 0.18s ease;
}
.pop-enter-from {
  opacity: 0;
  transform: scale(0.92);
}
</style>
