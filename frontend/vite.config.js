import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// ASR_BACKEND lets the API live elsewhere when :8000 is taken (on the hwtn
// droplet, hwtn.io's own API holds it, so auto-sr runs on :8100 there).
const backend = process.env.ASR_BACKEND || 'http://localhost:8000'

// xfwd: true makes the proxy add X-Forwarded-For (and X-Forwarded-Port)
// with the real browser's address -- without it, every request the
// backend sees comes from this proxy's own outbound connection, i.e.
// 127.0.0.1 for everyone, which is what api/app.py's session tracking
// was silently recording until this was added.
const proxied = { target: backend, xfwd: true }

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: true,
    proxy: {
      '/rules': proxied,
      '/runs': proxied,
      '/catalog': proxied,
      '/library': proxied,
      '/system': proxied,
      '/profile': proxied,
      '/comments': proxied,
    },
  },
})
