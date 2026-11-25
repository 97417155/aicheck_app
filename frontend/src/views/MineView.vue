<script setup>
import { useRouter } from 'vue-router'
import { store, currentPosition, dialog, toast } from '../store'

const router = useRouter()

function about() {
  dialog({ title: '关于', message: '华信员工 3.0\nAI 辅助现场检查移动端', confirmText: '知道了' })
}
</script>

<template>
  <div>
    <div class="navbar">
      <div class="title" style="margin-left: 0">我的</div>
      <div class="na" @click="router.push('/settings')">设置</div>
    </div>

    <div class="profile-hd">
      <div class="av"><img src="/assets/avatar.png" alt="" /></div>
      <div>
        <h3>{{ store.user.name }}</h3>
        <div class="sub">{{ store.user.title }} · {{ currentPosition.name }}</div>
        <div class="org">{{ store.user.org }}<br />{{ store.user.dept }}</div>
      </div>
    </div>

    <div class="mine-body">
      <div class="card">
        <div class="section-title2">岗位信息</div>
        <div class="role-tags">
          <span class="tag tag-blue">{{ store.user.role }}</span>
          <span class="tag tag-green">{{ store.user.title }}</span>
          <span class="tag tag-gray">{{ store.user.branchRole }}</span>
        </div>
        <div class="info-grid">
          <div class="ig"><div class="k">姓名</div><div class="v">{{ store.user.name }}</div></div>
          <div class="ig"><div class="k">岗位编号</div><div class="v">{{ currentPosition.code }}</div></div>
          <div class="ig"><div class="k">所属机构</div><div class="v">{{ store.user.org }}</div></div>
          <div class="ig"><div class="k">所属部门</div><div class="v">{{ store.user.dept }}</div></div>
          <div class="ig"><div class="k">联系网点</div><div class="v">{{ store.user.branch }}</div></div>
          <div class="ig"><div class="k">用户状态</div><div class="v" style="color: var(--ok)">正常</div></div>
        </div>
      </div>

      <div class="list-card">
        <div class="list-row" @click="router.push('/settings')">
          <div class="li" style="background: #1b94f9">⚙</div>
          <div class="ll">切换岗位</div>
          <div class="lv">{{ currentPosition.name }}</div>
          <span class="la">›</span>
        </div>
        <div class="list-row" @click="toast('个人资料暂未开放')">
          <div class="li" style="background: #5fb4ff">👤</div>
          <div class="ll">个人资料</div>
          <span class="la">›</span>
        </div>
        <div class="list-row" @click="router.push('/settings')">
          <div class="li" style="background: #a36aff">🔒</div>
          <div class="ll">安全设置</div>
          <span class="la">›</span>
        </div>
      </div>

      <div class="list-card">
        <div class="list-row" @click="about">
          <div class="li" style="background: #9aa4b2">i</div>
          <div class="ll">关于</div>
          <span class="la">›</span>
        </div>
      </div>
    </div>
  </div>
</template>
