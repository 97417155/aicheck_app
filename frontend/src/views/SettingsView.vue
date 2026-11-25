<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { store, currentPosition, dialog, toast } from '../store'

const router = useRouter()
const bio = ref(false)
const showPositions = ref(false)
const keyword = ref('')

function selectPosition(i) {
  store.positionIndex = i
}

function confirmPosition() {
  showPositions.value = false
  toast('已切换至：' + currentPosition.value.name)
}

function logout() {
  dialog({
    message: '确定要退出登录吗？',
    confirmText: '确认退出',
    cancelText: '取消',
    icon: 'warn'
  }).then((ok) => {
    if (!ok) return
    dialog({ message: '已退出登录', confirmText: '重新登录', icon: 'ok' }).then(() => {
      router.push('/home')
    })
  })
}

function filteredPositions() {
  const kw = keyword.value.trim()
  return store.positions
    .map((p, i) => ({ ...p, index: i }))
    .filter((p) => !kw || p.name.includes(kw) || p.code.includes(kw))
}
</script>

<template>
  <div>
    <div class="navbar">
      <div class="back" @click="router.back()">
        <svg viewBox="0 0 24 24"><path fill="currentColor" d="M15.4 7.4L14 6l-6 6 6 6 1.4-1.4-4.6-4.6z"/></svg>
      </div>
      <div class="title">设置</div>
      <div class="na"></div>
    </div>

    <div class="card" style="margin-top: 12px">
      <div class="section-title2">账号与安全</div>
      <div class="list-card" style="margin: 0; box-shadow: none; border-radius: 0">
        <div class="list-row" @click="toast('修改密码暂不可用')">
          <div class="li" style="background: #1b94f9">🔒</div>
          <div class="ll">修改密码</div>
          <span class="la">›</span>
        </div>
        <div class="list-row" @click="bio = !bio; toast(bio ? '已开启' : '已关闭')">
          <div class="li" style="background: #14d4dc">🛡</div>
          <div class="ll">指纹 / 面容登录</div>
          <div class="switch" :class="{ on: bio }"><i></i></div>
        </div>
        <div class="list-row" @click="toast('已绑定手机号')">
          <div class="li" style="background: #5fb4ff">📱</div>
          <div class="ll">绑定手机</div>
          <div class="lv">138****0000</div>
          <span class="la">›</span>
        </div>
      </div>
    </div>

    <div class="card">
      <div class="section-title2">岗位与权限</div>
      <div class="list-card" style="margin: 0; box-shadow: none; border-radius: 0">
        <div class="list-row" @click="showPositions = true">
          <div class="li" style="background: #a36aff">⇄</div>
          <div class="ll">切换岗位</div>
          <div class="lv">{{ currentPosition.name }}</div>
          <span class="la">›</span>
        </div>
      </div>
      <div class="form-hint">切换岗位后，首页展示的功能项将按角色权限自动调整。</div>
    </div>

    <div class="card">
      <div class="section-title2">系统</div>
      <div class="list-card" style="margin: 0; box-shadow: none; border-radius: 0">
        <div class="list-row" @click="toast('已是最新版本 v1.0')">
          <div class="li" style="background: #9aa4b2">i</div>
          <div class="ll">版本信息</div>
          <div class="lv">v1.0</div>
          <span class="la">›</span>
        </div>
      </div>
    </div>

    <div style="padding: 16px 12px 30px">
      <button class="btn btn-danger btn-block" @click="logout">退出登录</button>
    </div>

    <!-- 岗位选择 -->
    <Teleport to="#phone">
      <div v-if="showPositions" class="mask" @click.self="showPositions = false">
        <div class="sheet">
          <div class="sh-head">
            <span>切换岗位</span>
            <span class="sh-close" @click="showPositions = false">×</span>
          </div>
          <div class="sh-body">
            <div class="search-in-sheet">
              <input v-model="keyword" placeholder="请输入岗位关键词" />
            </div>
            <div
              v-for="p in filteredPositions()"
              :key="p.code"
              class="opt-row"
              :class="{ on: p.index === store.positionIndex }"
              @click="selectPosition(p.index)"
            >
              <div>
                <div>{{ p.name }}</div>
                <div style="font-size: 11px; color: #9aa4b2; margin-top: 2px">{{ p.code }} · {{ p.desc }}</div>
              </div>
              <span v-if="p.index === store.positionIndex" class="or-check">✓</span>
            </div>
            <div v-if="!filteredPositions().length" class="empty">无匹配岗位</div>
          </div>
          <div class="sh-foot">
            <button class="btn btn-ghost" @click="showPositions = false">取消</button>
            <button class="btn btn-primary" @click="confirmPosition">完成</button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>
