import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
// https://vite.dev/config/
export default defineConfig({
  plugins: [react(),  tailwindcss(),],
  base: process.env.NODE_ENV === 'development' ? '/' : '/final-web-app-SC310006/', // ใช้ '/' ในการพัฒนาและ '/final-web-app-SC310006/' ในการ build
})
