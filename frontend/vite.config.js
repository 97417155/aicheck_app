import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

const API_TARGET = process.env.API_TARGET || 'http://127.0.0.1:5000'

export default defineConfig({
  plugins: [
    vue({
      // 素材放在 public/ 下以绝对路径引用，交给浏览器直接请求，不做模块解析
      template: { transformAssetUrls: false }
    })
  ],
  server: {
    host: '0.0.0.0',
    port: 5173,
    proxy: {
      '/api': { target: API_TARGET, changeOrigin: true }
    }
  },
  build: {
    outDir: 'dist',
    emptyOutDir: true
  }
})
