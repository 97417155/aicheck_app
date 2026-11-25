<script setup>
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import { dialog, toast } from '../store'
import { api } from '../api'
import StepBar from '../components/StepBar.vue'
import OrgPicker from '../components/OrgPicker.vue'
import ScenePicker from '../components/ScenePicker.vue'
import CameraMock from '../components/CameraMock.vue'

const router = useRouter()
const labels = ['编辑基础信息', '拍摄照片', '智能比对']

const step = ref(1)
const org = ref(null)
const scene = ref(null)
const photos = ref([])
const quality = ref({ ok: true, messages: [] })
const result = ref(null)
const submitting = ref(false)

const showOrg = ref(false)
const showScene = ref(false)
const showCamera = ref(false)

const badCount = computed(
  () => photos.value.filter((p) => p.effect === 'blur' || p.effect === 'lowres').length
)
const hasAnomaly = computed(() => result.value?.result === 'anomaly')
const anomalies = computed(() => result.value?.anomalies || [])

function photoOk(p) {
  return p.effect !== 'blur' && p.effect !== 'lowres'
}

async function refreshQuality() {
  if (!photos.value.length) {
    quality.value = { ok: true, messages: [] }
    return
  }
  try {
    quality.value = await api.post('/api/quality/material', {
      photos: photos.value.map((p) => ({ effect: p.effect, ratio: p.ratio }))
    })
  } catch (e) {
    /* 忽略瞬时错误 */
  }
}

function onCapture(photo) {
  photos.value.push(photo)
  showCamera.value = false
  refreshQuality()
}

function removePhoto(id) {
  photos.value = photos.value.filter((p) => p.id !== id)
  refreshQuality()
}

function nextFromStep1() {
  if (!org.value && !scene.value) return dialog({ message: '请选择被查机构及场景！', icon: 'err' })
  if (!org.value) return dialog({ message: '请选择被查机构！', icon: 'err' })
  if (!scene.value) return dialog({ message: '请选择场景！', icon: 'err' })
  step.value = 2
}

async function nextFromStep2() {
  if (!photos.value.length) return dialog({ message: '请至少拍摄一张宣传物料照片！', icon: 'err' })
  if (!quality.value.ok) return dialog({ message: '请删除校验不通过的照片后再进行下一步！', icon: 'err' })
  submitting.value = true
  try {
    result.value = await api.post('/api/checks/material', {
      org: org.value,
      sceneId: scene.value.id,
      photos: photos.value.map((p) => ({ effect: p.effect, ratio: p.ratio }))
    })
    step.value = 3
  } catch (e) {
    dialog({ message: e.message || '提交失败，请稍后重试', icon: 'err' })
  } finally {
    submitting.value = false
  }
}

function closePage() {
  router.push('/inspection')
}

const onSelectOrg = (o) => {
  org.value = o
  showOrg.value = false
}
const onSelectScene = (s) => {
  scene.value = s
  showScene.value = false
}
</script>

<template>
  <div>
    <div class="navbar">
      <div class="back" @click="step === 1 ? closePage() : step === 2 ? (step = 1) : (step = 2)">
        <svg viewBox="0 0 24 24"><path fill="currentColor" d="M15.4 7.4L14 6l-6 6 6 6 1.4-1.4-4.6-4.6z"/></svg>
      </div>
      <div class="title">宣传物料摆放规范性检查</div>
      <div class="na"></div>
    </div>

    <StepBar :labels="labels" :current="step" />

    <!-- 步骤一 -->
    <template v-if="step === 1">
      <div class="form-card">
        <div class="form-row" @click="showOrg = true">
          <div class="fr-label">被查机构 <span class="req">*</span></div>
          <div class="fr-value" :class="{ filled: !!org }">
            {{ org ? org.name : '请选择' }}<span class="fr-arrow">›</span>
          </div>
        </div>
        <div class="form-row" @click="showScene = true">
          <div class="fr-label">检查场景 <span class="req">*</span></div>
          <div class="fr-value" :class="{ filled: !!scene }">
            {{ scene ? scene.name : '请选择' }}<span class="fr-arrow">›</span>
          </div>
        </div>
        <div class="form-hint">选择被查机构与检查场景后，系统将展示该场景对应的物料公示与识别要求。</div>
      </div>

      <div v-if="scene" class="req-box">
        <h4>场景宣传物料要求（{{ scene.name }}）</h4>
        <div class="req-row">
          <div class="n">1</div>
          <div class="tt"><b>公示要求：</b>{{ scene.requirements.public }}</div>
        </div>
        <div class="req-row">
          <div class="n">2</div>
          <div class="tt"><b>详细识别要求：</b>{{ scene.requirements.detail }}</div>
        </div>
      </div>

      <div class="bottom-actions">
        <button class="btn btn-ghost" @click="closePage">上一步</button>
        <button class="btn btn-primary" @click="nextFromStep1">下一步</button>
      </div>
    </template>

    <!-- 步骤二 -->
    <template v-else-if="step === 2">
      <div class="card" style="padding: 12px 14px; font-size: 12px; color: var(--text-2); line-height: 1.6">
        场景：<b style="color: var(--text)">{{ scene?.name }}</b> · 机构：<b style="color: var(--text)">{{ org?.name }}</b><br />
        拍摄要求：摆放方向正常、物料文字清晰、单张照片物料不超过 8 个。最多拍摄 5 张。
      </div>

      <div class="photo-list">
        <div class="pl-title">
          <span>宣传物料照片列表</span>
          <small>已拍摄 {{ photos.length }} / 5 张 · 异常 {{ badCount }} 张</small>
        </div>
        <div class="photo-grid">
          <div v-for="p in photos" :key="p.id" class="photo-item" :class="{ bad: !photoOk(p) }">
            <div class="photo-mini">
              <div class="mini-poster" :class="{ bad: p.scene === 'poster-bad' }">
                <i class="mt"></i><i class="ml"></i><i class="mq"></i>
              </div>
            </div>
            <div class="pi-del" @click="removePhoto(p.id)">×</div>
            <div class="pi-status" :class="photoOk(p) ? 'ok' : 'err'">
              {{ photoOk(p) ? '✓ 校验通过' : '✕ 校验不通过' }}
            </div>
          </div>
          <div v-if="photos.length < 5" class="photo-add" @click="showCamera = true">
            <svg viewBox="0 0 24 24"><path fill="currentColor" d="M11 4h2v7h7v2h-7v7h-2v-7H4v-2h7z"/></svg>
            <span>拍摄照片</span>
          </div>
        </div>
      </div>

      <div v-if="photos.length" class="check-result">
        <div class="cr-head" :class="quality.ok ? 'ok' : 'bad'">
          <div class="cr-icon">{{ quality.ok ? '✓' : '!' }}</div>
          <div>{{ quality.ok ? '照片校验通过' : `照片校验结果：不通过（${quality.messages.length} 项）` }}</div>
        </div>
        <div class="cr-body">
          <template v-if="quality.ok">
            <div class="cr-line">
              <div class="cl-dot" style="background: var(--success)"></div>
              <div class="cl-text">共 {{ photos.length }} 张照片已通过图像质量检测，可进行智能比对。</div>
            </div>
          </template>
          <template v-else>
            <div v-for="(m, i) in quality.messages" :key="i" class="cr-line">
              <div class="cl-dot"></div>
              <div class="cl-text">{{ m }}</div>
            </div>
          </template>
        </div>
      </div>

      <div class="bottom-actions">
        <button class="btn btn-ghost" @click="step = 1">上一步</button>
        <button class="btn btn-primary" :disabled="submitting" @click="nextFromStep2">
          {{ submitting ? '比对中…' : '下一步 · 智能比对' }}
        </button>
      </div>
    </template>

    <!-- 步骤三 -->
    <template v-else>
      <div class="result-hero">
        <div class="rh-icon" :class="hasAnomaly ? 'bad' : 'ok'">{{ hasAnomaly ? '!' : '✓' }}</div>
        <h3>{{ hasAnomaly ? '智能比对发现异常' : '智能比对无异常' }}</h3>
        <p>{{ scene?.name }} · {{ org?.name }}<br />共识别 {{ photos.length }} 张照片</p>
      </div>

      <div v-if="hasAnomaly" class="compare-panel">
        <div class="cr-head bad" style="margin: 0; border-radius: 14px 14px 0 0">
          <div class="cr-icon">!</div>
          <div>发现异常（{{ anomalies.length }} 项）</div>
        </div>
        <div class="cr-body">
          <div v-for="(a, i) in anomalies" :key="i" class="cr-line">
            <div class="cl-dot"></div>
            <div class="cl-text">{{ a }}</div>
          </div>
        </div>
      </div>
      <div v-else class="check-result">
        <div class="cr-head ok">
          <div class="cr-icon">✓</div>
          <div>智能比对无异常</div>
        </div>
        <div class="cr-body">
          <div class="cr-line">
            <div class="cl-dot" style="background: var(--success)"></div>
            <div class="cl-text">宣传物料摆放符合场景规范，检查通过。</div>
          </div>
        </div>
      </div>

      <div class="card" style="padding: 12px 14px">
        <div style="font-size: 13px; font-weight: 600; margin-bottom: 10px">显示拍摄照片</div>
        <div class="photo-grid">
          <div v-for="p in photos" :key="p.id" class="photo-item">
            <div class="photo-mini">
              <div class="mini-poster" :class="{ bad: p.scene === 'poster-bad' }">
                <i class="mt"></i><i class="ml"></i><i class="mq"></i>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="bottom-actions">
        <button class="btn btn-ghost" @click="step = 2">返回上一步</button>
        <button class="btn btn-primary" @click="closePage">关闭页面</button>
      </div>
    </template>

    <OrgPicker :visible="showOrg" @close="showOrg = false" @select="onSelectOrg" />
    <ScenePicker :visible="showScene" :model-value="scene?.id" @close="showScene = false" @select="onSelectScene" />
    <CameraMock :visible="showCamera" mode="material" @close="showCamera = false" @capture="onCapture" />
  </div>
</template>
