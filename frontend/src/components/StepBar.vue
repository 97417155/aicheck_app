<script setup>
defineProps({
  labels: { type: Array, required: true },
  current: { type: Number, default: 1 }
})
</script>

<template>
  <div class="steps">
    <template v-for="(label, i) in labels" :key="label">
      <div class="step" :class="{ done: i + 1 < current, active: i + 1 === current }">
        <div class="s-circle">{{ i + 1 < current ? '✓' : i + 1 }}</div>
        <div class="s-label">{{ label }}</div>
      </div>
      <div v-if="i < labels.length - 1" class="step-line" :class="{ done: i + 1 < current }"></div>
    </template>
  </div>
</template>
