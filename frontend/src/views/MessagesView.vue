<script setup>
import { store, toast } from '../store'

const colors = ['#1b94f9', '#14d4dc', '#a36aff']
</script>

<template>
  <div>
    <div class="navbar">
      <div class="title" style="margin-left: 0">消息</div>
    </div>

    <div class="list-card">
      <div
        v-for="(m, i) in store.messages"
        :key="i"
        class="list-row"
        @click="toast(m.title)"
      >
        <div class="li" :style="{ background: colors[i % colors.length] }">🔔</div>
        <div class="ll">
          <div>{{ m.title }}</div>
          <div style="font-size: 11px; color: #9aa4b2; margin-top: 2px">{{ m.desc }}</div>
        </div>
        <div class="lv">{{ m.time }}</div>
      </div>
    </div>

    <div class="empty">已全部加载</div>
  </div>
</template>
