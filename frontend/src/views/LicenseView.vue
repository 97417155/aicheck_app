<script setup>
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import { dialog } from '../store'
import { api } from '../api'
import StepBar from '../components/StepBar.vue'
import OrgPicker from '../components/OrgPicker.vue'
import CameraMock from '../components/CameraMock.vue'

const router = useRouter()
const labels = ['选择机构', '拍摄证件', '智能核验']

const step = ref(1)
const org = ref(null)
const record = ref(null)
const photos = ref([])
const quality = ref({ ok: true, messages: [] })
const result = ref(null)
const submitting = ref(false)

const showOrg = ref(false)
const showCamera = ref(false)

const hasAnomaly = computed(() => result.value?.result === 'anomaly')
const diffs = computed(() => result.value?.diffs || [])

function photoOk(p) {
  return p.effect !== 'blur' && p.effect !== 'lowres'
}

async function onSelectOrg(o) {
  org.value = o
  showOrg.value = false
  record.value = null
  try {
    record.value = await api.get(`/api/license/records/${o.code}`)
  } catch (e) {
    dialog({ message: '该机构暂无备案数据', icon: 'err' })
  }
}

async function refreshQuality() {
  if (!photos.value.length) {
    quality.value = { ok: true, messages: [] }
    return
  }
  try {
    quality.value = await api.post('/api/quality/license', {
      photos: photos.value.map((p) => ({ effect: p.effect, ratio: p.ratio }))
    })
  } catch (e) {
    /* ignore */
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
  if (!org.value) return dialog({ message: '请选择被查机构！', icon: 'err' })
  if (!record.value) return dialog({ message: '该机构暂无备案数据', icon: 'err' })
  step.value = 2
}

async function nextFromStep2() {
  if (!photos.value.length) return dialog({ message: '请拍摄金融许可证照片！', icon: 'err' })
  if (!quality.value.ok) return dialog({ message: '请提供通过校验的金融许可证照片！', icon: 'err' })
  submitting.value = true
  try {
    result.value = await api.post('/api/checks/license', {
      org: org.value,
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
</script>

<template>
  <div>
    <div class="navbar">
      <div class="back" @click="step === 1 ? closePage() : step === 2 ? (step = 1) : (step = 2)">
        <svg viewBox="0 0 24 24"><path fill="currentColor" d="M15.4 7.4L14 6l-6 6 6 6 1.4-1.4-4.6-4.6z"/></svg>
      </div>
      <div class="title">金融许可证核验</div>
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
        <div class="form-hint">选择机构后，系统将展示新一代网点管理系统中的备案数据用于核验比对。</div>
      </div>

      <div v-if="record" class="record-card">
        <h4>备案数据（新一代网点管理系统）</h4>
        <div class="record-line"><div class="k">机构编号</div><div class="v">{{ record.code }}</div></div>
        <div class="record-line"><div class="k">机构名称</div><div class="v">{{ record.name }}</div></div>
        <div class="record-line"><div class="k">机构地址</div><div class="v">{{ record.address }}</div></div>
      </div>

      <div v-if="record" class="req-box" style="margin-top: 0">
        <h4>监管要求</h4>
        <div class="req-row">
          <div class="n">!</div>
          <div class="tt">金融许可证信息是否与网点管理系统记录信息<b>完全一致</b>（机构编号、机构名称、机构地址）。</div>
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
        机构：<b style="color: var(--text)">{{ org?.name }}</b><br />
        拍摄要求：证件国徽对准定位框、证件文字清晰、分辨率 1440 以上。
      </div>

      <div class="photo-list">
        <div class="pl-title"><span>许可证照片</span><small>已拍摄 {{ photos.length }} 张</small></div>
        <div class="photo-grid">
          <div v-for="p in photos" :key="p.id" class="photo-item" :class="{ bad: !photoOk(p) }">
            <div class="photo-mini"><div class="mini-doc"></div></div>
            <div class="pi-del" @click="removePhoto(p.id)">×</div>
            <div class="pi-status" :class="photoOk(p) ? 'ok' : 'err'">
              {{ photoOk(p) ? '✓ 校验通过' : '✕ 质量异常' }}
            </div>
          </div>
          <div class="photo-add" @click="showCamera = true">
            <svg viewBox="0 0 24 24"><path fill="currentColor" d="M11 4h2v7h7v2h-7v7h-2v-7H4v-2h7z"/></svg>
            <span>拍摄照片</span>
          </div>
        </div>
      </div>

      <div v-if="photos.length" class="check-result">
        <div class="cr-head" :class="quality.ok ? 'ok' : 'bad'">
          <div class="cr-icon">{{ quality.ok ? '✓' : '!' }}</div>
          <div>{{ quality.ok ? '拍摄质量校验通过' : '拍摄质量校验：不通过' }}</div>
        </div>
        <div class="cr-body">
          <template v-if="quality.ok">
            <div class="cr-line">
              <div class="cl-dot" style="background: var(--success)"></div>
              <div class="cl-text">证件国徽对准、文字清晰、分辨率达标，可进行智能核验。</div>
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
          {{ submitting ? '核验中…' : '下一步 · 智能核验' }}
        </button>
      </div>
    </template>

    <!-- 步骤三 -->
    <template v-else>
      <div class="result-hero">
        <div class="rh-icon" :class="hasAnomaly ? 'bad' : 'ok'">{{ hasAnomaly ? '!' : '✓' }}</div>
        <h3>{{ hasAnomaly ? '金融许可证核验发现异常' : '金融许可证核验通过' }}</h3>
        <p>{{ org?.name }}<br />{{ record?.code }}</p>
      </div>

      <div class="compare-panel">
        <div class="cr-head" :class="hasAnomaly ? 'bad' : 'ok'" style="margin: 0; border-radius: 14px 14px 0 0">
          <div class="cr-icon">{{ hasAnomaly ? '!' : '✓' }}</div>
          <div>{{ hasAnomaly ? `发现 ${diffs.length} 项信息不一致` : '信息完全一致' }}</div>
        </div>
        <div class="compare-row">
          <h5>金融许可证识别信息 <span class="tag tag-gray">OCR</span></h5>
          <div class="compare-val">
            编号：{{ result?.ocr?.code }}<br />
            名称：{{ result?.ocr?.name }}<br />
            地址：{{ result?.ocr?.address }}
          </div>
        </div>
        <div class="compare-row">
          <h5>网点管理系统备案数据 <span class="tag tag-blue">备案</span></h5>
          <div class="compare-val">
            编号：{{ result?.record?.code }}<br />
            名称：{{ result?.record?.name }}<br />
            地址：{{ result?.record?.address }}
          </div>
        </div>
        <div v-if="diffs.length" class="compare-row">
          <h5>差异项 <span class="tag tag-red">{{ diffs.length }} 项</span></h5>
          <div v-for="(d, i) in diffs" :key="i" class="cr-line">
            <div class="cl-dot"></div>
            <div class="cl-text">
              <b>{{ d.field }}：</b>金融许可证信息（<span class="hl">{{ d.ocr }}</span>）与网点管理系统（<span class="hl">{{ d.record }}</span>）不一致
            </div>
          </div>
        </div>
      </div>

      <div class="card" style="padding: 12px 14px">
        <div style="font-size: 13px; font-weight: 600; margin-bottom: 10px">显示拍摄照片</div>
        <div class="photo-grid">
          <div v-for="p in photos" :key="p.id" class="photo-item">
            <div class="photo-mini"><div class="mini-doc"></div></div>
          </div>
        </div>
      </div>

      <div class="bottom-actions">
        <button class="btn btn-ghost" @click="step = 2">返回上一步</button>
        <button class="btn btn-primary" @click="closePage">关闭页面</button>
      </div>
    </template>

    <OrgPicker :visible="showOrg" @close="showOrg = false" @select="onSelectOrg" />
    <CameraMock :visible="showCamera" mode="license" @close="showCamera = false" @capture="onCapture" />
  </div>
</template>
