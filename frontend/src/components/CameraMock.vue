<script setup>
import { computed, ref, watch } from 'vue'
import { store } from '../store'

const props = defineProps({
  visible: Boolean,
  mode: { type: String, default: 'material' }
})
const emit = defineEmits(['close', 'capture'])

const ratio = ref('portrait')
const effect = ref('normal')

watch(
  () => props.visible,
  (v) => {
    if (v) {
      ratio.value = 'portrait'
      effect.value = 'normal'
    }
  }
)

const isLicense = computed(() => props.mode === 'license')
const effects = computed(() => store.effects?.[props.mode] || [])
const focusLabel = computed(() =>
  isLicense.value ? '请将金融许可证国徽对准定位框' : '请将宣传物料放入定位框'
)
const requirement = computed(() =>
  isLicense.value
    ? '证件国徽对准定位框 · 文字清晰 · 分辨率 1440 以上'
    : '摆放方向正常 · 没有旋转 · 文字清晰 · 单张照片物料不超过 8 个'
)

function shutter() {
  const photo = {
    id: Date.now() + Math.floor(Math.random() * 1000),
    effect: effect.value,
    ratio: ratio.value,
    scene: isLicense.value
      ? 'license'
      : effect.value === 'content'
        ? 'poster-bad'
        : 'poster'
  }
  emit('capture', photo)
}
</script>

<template>
  <Teleport to="#phone">
    <div v-if="visible" class="shot-overlay">
      <div class="shot-top">
        <span class="sc" @click="emit('close')">×</span>
        <span class="st">{{ isLicense ? '拍摄金融许可证' : '拍摄宣传物料' }}</span>
        <div class="ratio-switch" style="background: rgba(255, 255, 255, 0.16)">
          <button :class="{ on: ratio === 'portrait' }" @click="ratio = 'portrait'">竖屏</button>
          <button :class="{ on: ratio === 'landscape' }" @click="ratio = 'landscape'">横屏</button>
        </div>
      </div>

      <div class="shot-stage">
        <div v-if="isLicense" class="sc-scene sc-lic">
          <div class="lic-doc">
            <div class="lic-emblem">★</div>
            <div class="lic-title">金融许可证</div>
            <div class="lic-line"></div>
            <div class="lic-line s"></div>
            <div class="lic-line"></div>
            <div class="lic-line s"></div>
            <div class="lic-seal"></div>
          </div>
        </div>
        <div v-else class="sc-scene">
          <div class="sc-poster" :class="{ bad: effect === 'content' }">
            <div class="sc-title">线上取号 · 减少等候</div>
            <div class="sc-sub">业务办理快人一步</div>
            <div class="sc-phones"><div class="ph"></div><div class="ph"></div></div>
            <div class="sc-qr"></div>
            <div v-if="effect === 'content'" class="sc-hot">扫码办理</div>
            <div v-if="effect === 'content'" class="sc-tel">010-8888 8888</div>
            <div class="sc-foot"><span class="sc-logo"></span>营业部 · 客户服务</div>
          </div>
        </div>

        <div class="shot-mask"></div>
        <div class="focus-frame" :class="{ portrait: ratio === 'portrait' }">
          <div class="ff-label">{{ focusLabel }}</div>
        </div>
        <div class="shot-req">{{ requirement }}</div>
      </div>

      <div class="shot-effects">
        <span class="elab">拍摄效果</span>
        <span
          v-for="e in effects"
          :key="e.id"
          class="eff-chip"
          :class="{ on: effect === e.id }"
          @click="effect = e.id"
        >
          {{ e.label }}
        </span>
      </div>

      <div class="shot-bottom">
        <div class="shutter" @click="shutter"></div>
      </div>
    </div>
  </Teleport>
</template>
