<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { store, bootstrap } from './store'
import TabBar from './components/TabBar.vue'
import AppDialog from './components/AppDialog.vue'
import ToastBar from './components/ToastBar.vue'

const route = useRoute()
const tab = computed(() => route.meta.tab || null)
const clock = ref('09:41')
let timer = null

function tick() {
  const d = new Date()
  clock.value = `${String(d.getHours()).padStart(2, '0')}:${String(d.getMinutes()).padStart(2, '0')}`
}

async function reload() {
  store.ready = false
  await bootstrap()
}

onMounted(async () => {
  tick()
  timer = setInterval(tick, 30000)
  await bootstrap()
})

onUnmounted(() => clearInterval(timer))
</script>

<template>
  <div id="phone">
    <div class="statusbar">
      <span class="sb-time">{{ clock }}</span>
      <span class="sb-brand">{{ store.brand.short || '移动工作台' }}</span>
      <span class="sb-icons">
        <svg viewBox="0 0 24 24" width="13" height="13"><path fill="currentColor" d="M2 17h2v3H2zm4-4h2v7H6zm4-4h2v11h-2zm4-5h2v16h-2zm4-4h2v20h-2z"/></svg>
        <svg viewBox="0 0 24 24" width="14" height="14"><path fill="currentColor" d="M12 4C7 4 2.7 7 1 11.5 2.7 16 7 19 12 19s9.3-3 11-7.5C21.3 7 17 4 12 4zm0 12.5a5 5 0 110-10 5 5 0 010 10zm0-8a3 3 0 100 6 3 3 0 000-6z"/></svg>
        <span class="sb-battery"><i></i></span>
      </span>
    </div>

    <div class="app-body">
      <div class="page">
        <div v-if="!store.ready" class="loading-inline">
          <div class="spinner"></div>
          <div>正在加载…</div>
        </div>
        <div v-else-if="store.error" class="empty" style="padding-top:80px">
          {{ store.error }}
          <div style="margin-top:14px">
            <button class="btn btn-primary" @click="reload">重试</button>
          </div>
        </div>
        <router-view v-else />
      </div>
    </div>

    <TabBar v-if="tab" :active="tab" />
    <AppDialog />
    <ToastBar />
  </div>
</template>
