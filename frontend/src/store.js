import { reactive, computed } from 'vue'
import { api } from './api'

export const store = reactive({
  ready: false,
  error: '',
  brand: { name: '', short: '' },
  user: {},
  positions: [],
  homeFunctions: [],
  courses: [],
  notices: [],
  messages: [],
  inspectionFuncs: [],
  orgTree: [],
  scenes: [],
  effects: { material: [], license: [] },
  positionIndex: 0,
  toast: { visible: false, msg: '' },
  dialog: {
    visible: false,
    message: '',
    icon: 'warn',
    confirmText: '确认',
    cancelText: '',
    _resolve: null
  }
})

export const currentPosition = computed(
  () => store.positions[store.positionIndex] || { name: '', code: '', desc: '' }
)

export async function bootstrap() {
  try {
    const data = await api.get('/api/bootstrap')
    Object.assign(store, data)
    store.error = ''
  } catch (e) {
    store.error = e.message || '数据加载失败'
  } finally {
    store.ready = true
  }
}

let toastTimer = null
export function toast(msg, ms = 1800) {
  store.toast.msg = msg
  store.toast.visible = true
  clearTimeout(toastTimer)
  toastTimer = setTimeout(() => {
    store.toast.visible = false
  }, ms)
}

export function dialog(opts = {}) {
  return new Promise((resolve) => {
    Object.assign(
      store.dialog,
      { visible: true, message: '', icon: 'warn', confirmText: '确认', cancelText: '', _resolve: resolve },
      opts
    )
  })
}

export function closeDialog(ok) {
  store.dialog.visible = false
  const resolve = store.dialog._resolve
  store.dialog._resolve = null
  if (resolve) resolve(ok)
}
