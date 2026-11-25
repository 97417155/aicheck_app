<script setup>
import { useRouter } from 'vue-router'
import { store } from '../store'

const router = useRouter()

function open(func) {
  router.push(func.id === 'material' ? '/material' : '/license')
}

const iconPath = {
  card: 'M3 5h18a2 2 0 012 2v10a2 2 0 01-2 2H3a2 2 0 01-2-2V7a2 2 0 012-2zm0 4v6h18V9zm3 4h6v1.5H6z',
  image: 'M4 4h16a2 2 0 012 2v12a2 2 0 01-2 2H4a2 2 0 01-2-2V6a2 2 0 012-2zm1 13h14l-4.5-6-3 4-2-2.5zM8 9a1.5 1.5 0 100-3 1.5 1.5 0 000 3z'
}
</script>

<template>
  <div>
    <div class="insp-nav">
      <div class="back" @click="router.push('/home')">‹</div>
      <div class="t">督导检查</div>
    </div>

    <div class="insp-hero" :style="{ backgroundImage: `url('/assets/insp/u1017.png')` }">
      <h2>督导检查</h2>
      <p>深度融合AI能力，优化渠运督导资源配置，提升网点运营合规性与风险防控能力</p>
    </div>

    <div class="insp-body">
      <div class="insp-notice">
        <span class="tag">公告</span>
        <span class="txt">{{ store.notices[0] }}</span>
      </div>

      <div v-for="f in store.inspectionFuncs" :key="f.id" class="insp-card" @click="open(f)">
        <div class="ic" :style="{ background: `linear-gradient(135deg, ${f.color}, #3fdffe)` }">
          <svg viewBox="0 0 24 24" width="24" height="24">
            <path fill="currentColor" :d="iconPath[f.icon] || iconPath.card" />
          </svg>
        </div>
        <div class="bd">
          <h3>{{ f.title }}</h3>
          <p>{{ f.desc }}</p>
        </div>
        <div class="tap">☝</div>
      </div>
    </div>
  </div>
</template>
