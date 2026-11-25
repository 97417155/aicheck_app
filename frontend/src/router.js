import { createRouter, createWebHistory } from 'vue-router'

import HomeView from './views/HomeView.vue'
import InspectionView from './views/InspectionView.vue'
import MaterialView from './views/MaterialView.vue'
import LicenseView from './views/LicenseView.vue'
import MineView from './views/MineView.vue'
import SettingsView from './views/SettingsView.vue'
import MessagesView from './views/MessagesView.vue'

const routes = [
  { path: '/', redirect: '/home' },
  { path: '/home', name: 'home', component: HomeView, meta: { tab: 'home' } },
  { path: '/inspection', name: 'inspection', component: InspectionView, meta: { tab: 'home' } },
  { path: '/material', name: 'material', component: MaterialView, meta: { tab: null } },
  { path: '/license', name: 'license', component: LicenseView, meta: { tab: null } },
  { path: '/mine', name: 'mine', component: MineView, meta: { tab: 'mine' } },
  { path: '/settings', name: 'settings', component: SettingsView, meta: { tab: null } },
  { path: '/messages', name: 'messages', component: MessagesView, meta: { tab: 'messages' } },
  { path: '/:pathMatch(.*)*', redirect: '/home' }
]

export default createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior: () => ({ top: 0 })
})
