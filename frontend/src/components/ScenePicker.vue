<script setup>
import { computed, ref, watch } from 'vue'
import { store } from '../store'

const props = defineProps({ visible: Boolean, modelValue: String })
const emit = defineEmits(['close', 'select'])

const keyword = ref('')
const selected = ref('')

watch(
  () => props.visible,
  (v) => {
    if (v) {
      keyword.value = ''
      selected.value = props.modelValue || ''
    }
  }
)

const list = computed(() => {
  const kw = keyword.value.trim()
  return (store.scenes || []).filter((s) => !kw || s.name.includes(kw))
})

function confirm() {
  const scene = (store.scenes || []).find((s) => s.id === selected.value)
  if (!scene) return
  emit('select', scene)
}
</script>

<template>
  <Teleport to="#phone">
    <div v-if="visible" class="mask" @click.self="emit('close')">
      <div class="sheet">
        <div class="sh-head">
          <span>选择场景</span>
          <span class="sh-close" @click="emit('close')">×</span>
        </div>
        <div class="sh-body">
          <div class="search-in-sheet">
            <input v-model="keyword" placeholder="请输入关键词" />
          </div>
          <div v-for="s in list" :key="s.id" class="opt-row" :class="{ on: s.id === selected }" @click="selected = s.id">
            <span>{{ s.name }}</span>
            <span v-if="s.id === selected" class="or-check">✓</span>
          </div>
          <div v-if="!list.length" class="empty">无匹配场景</div>
        </div>
        <div class="sh-foot">
          <button class="btn btn-ghost" @click="emit('close')">取消</button>
          <button class="btn btn-primary" @click="confirm">完成</button>
        </div>
      </div>
    </div>
  </Teleport>
</template>
