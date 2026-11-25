<script setup>
import { computed, ref, watch } from 'vue'
import { store } from '../store'

const props = defineProps({ visible: Boolean })
const emit = defineEmits(['close', 'select'])

const l1 = ref(0)
const l2 = ref(0)
const l3 = ref(0)

watch(
  () => props.visible,
  (v) => {
    if (v) {
      l1.value = 0
      l2.value = 0
      l3.value = 0
    }
  }
)

const level1 = computed(() => store.orgTree || [])
const level2 = computed(() => level1.value[l1.value]?.children || [])
const level3 = computed(() => level2.value[l2.value]?.children || [])

function pick1(i) {
  l1.value = i
  l2.value = 0
  l3.value = 0
}
function pick2(i) {
  l2.value = i
  l3.value = 0
}

function confirm() {
  const node = level3.value[l3.value]
  if (!node) return
  emit('select', {
    name: node.name,
    code: node.code,
    path: [level1.value[l1.value]?.name, level2.value[l2.value]?.name, node.name]
  })
}
</script>

<template>
  <Teleport to="#phone">
    <div v-if="visible" class="mask" @click.self="emit('close')">
      <div class="sheet">
        <div class="sh-head">
          <span>选择被查机构</span>
          <span class="sh-close" @click="emit('close')">×</span>
        </div>
        <div class="sh-body">
          <div class="org-cols">
            <div class="org-col">
              <div
                v-for="(n, i) in level1"
                :key="n.code"
                class="opt-row"
                :class="{ on: i === l1 }"
                @click="pick1(i)"
              >
                <span>{{ n.name }}</span>
                <span v-if="i === l1" class="or-check">✓</span>
              </div>
            </div>
            <div class="org-col">
              <div
                v-for="(n, i) in level2"
                :key="n.code"
                class="opt-row"
                :class="{ on: i === l2 }"
                @click="pick2(i)"
              >
                <span>{{ n.name }}</span>
                <span v-if="i === l2" class="or-check">✓</span>
              </div>
              <div v-if="!level2.length" class="empty" style="padding:20px 8px;font-size:12px">无下级</div>
            </div>
            <div class="org-col">
              <div
                v-for="(n, i) in level3"
                :key="n.code"
                class="opt-row"
                :class="{ on: i === l3 }"
                @click="l3 = i"
              >
                <span>{{ n.name }}</span>
                <span v-if="i === l3" class="or-check">✓</span>
              </div>
              <div v-if="!level3.length" class="empty" style="padding:20px 8px;font-size:12px">请选择上级</div>
            </div>
          </div>
        </div>
        <div class="sh-foot">
          <button class="btn btn-ghost" @click="emit('close')">取消</button>
          <button class="btn btn-primary" @click="confirm">确定</button>
        </div>
      </div>
    </div>
  </Teleport>
</template>
