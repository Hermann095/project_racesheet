/// <reference types="vitest" />
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'
import tsconfigPaths from 'vite-tsconfig-paths'
import http from 'http'

const agent = new http.Agent({ keepAlive: true })

// https://vitejs.dev/config https://vitest.dev/config
export default defineConfig({
  plugins: [react(), tsconfigPaths()],
  test: {
    globals: true,
    environment: 'happy-dom',
    setupFiles: '.vitest/setup',
    include: ['**/test.{ts,tsx}']
  },
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:5000/',
        changeOrigin: true,
        secure: false,
        agent
      },
      '/websocket': {
        target: 'ws://localhost:5000/',
        changeOrigin: true,
        secure: false,
        ws: true,
        agent
      },
      'ws://localhost:5000/': {
        target: 'ws://localhost:5000/',
        changeOrigin: true,
        secure: false,
        ws: true,
        agent
      }
    }
  }
})
