<script setup>
import { useRouter } from 'vue-router'
import { toast } from '../store'

defineProps({ active: { type: String, default: 'home' } })
const router = useRouter()

const items = [
  { key: 'home', label: '首页', img: '/assets/home/u258.svg', to: '/home' },
  { key: 'people', label: '人员', img: '/assets/home/u260.svg', to: '/messages' },
  { key: 'ai', ai: true },
  { key: 'messages', label: '消息', img: '/assets/home/u263.svg', to: '/messages' },
  { key: 'mine', label: '我的', img: '/assets/home/u266.svg', to: '/mine' }
]
</script>

<template>
  <div class="tabbar5">
    <template v-for="it in items" :key="it.key">
      <div v-if="it.ai" class="nav5 ai" @click="toast('AI 助手')">
        <div class="ai-btn">
          <img src="/assets/sphere.png" alt="AI" />
          <span>AI</span>
        </div>
      </div>
      <div v-else class="nav5" :class="{ on: active === it.key }" @click="router.push(it.to)">
        <img :src="it.img" :alt="it.label" />
        <span>{{ it.label }}</span>
      </div>
    </template>
  </div>
</template>
