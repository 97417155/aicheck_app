<script setup>
import { useRouter } from 'vue-router'
import { store, currentPosition, dialog, toast } from '../store'

const router = useRouter()

function openFunc() {
  router.push('/inspection')
}

function openCourse(course) {
  dialog({
    title: '课程',
    message: `"${course.title}"\n课程详情暂未开放。`,
    confirmText: '知道了'
  })
}
</script>

<template>
  <div>
    <div class="home-hd">
      <div class="hd-bar">
        <img class="hd-logo" src="/assets/home/u150.svg" alt="" />
        <div class="hd-search" @click="toast('搜索功能、课程、人员等')">
          <img src="/assets/home/u148.svg" alt="" />
          <span>搜索功能、课程、人员等</span>
        </div>
        <img class="hd-scan" src="/assets/home/u151.svg" alt="" @click="toast('扫一扫')" />
      </div>

      <div class="hd-hero">
        <div class="hd-hero-text">
          <h1>{{ store.brand.name }}</h1>
          <div class="hd-new">
            <span class="pill">新功能介绍</span>
            <span class="link" @click="router.push('/inspection')">点击查看</span>
          </div>
        </div>
        <img class="hd-cube" src="/assets/ai-cube.png" alt="" />
      </div>
    </div>

    <div class="home-body">
      <div class="grid-card">
        <div class="grid4">
          <div v-for="f in store.homeFunctions" :key="f.id" class="cell" @click="openFunc(f)">
            <div class="gicon" :style="{ background: f.grad }">
              <img :src="'/' + f.icon" :alt="f.label" />
            </div>
            <div class="glabel">{{ f.label }}</div>
          </div>
        </div>
      </div>

      <div class="course-sec">
        <div class="sec-head">
          <span class="st">精选课程 <span class="caret">⌄</span></span>
          <span class="refresh" @click="toast('已为您更换一批课程')">换一换 ↻</span>
        </div>
        <div class="course-cards">
          <div v-for="(c, i) in store.courses" :key="i" class="course-card" @click="openCourse(c)">
            <div class="cc-thumb"><div class="cc-play"></div></div>
            <div class="cc-title">{{ c.title }}</div>
          </div>
        </div>
        <div style="height: 10px"></div>
      </div>

      <div class="loaded-tip">已全部加载</div>
    </div>
  </div>
</template>
