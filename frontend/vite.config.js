import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// ASR_BACKEND lets the API live elsewhere when :8000 is taken (on the hwtn
// droplet, hwtn.io's own API holds it, so auto-sr runs on :8100 there).
const backend = process.env.ASR_BACKEND || 'http://localhost:8000'

// ASR_BASE mounts the app under a path (e.g. /v2/ behind hwtn.io's nginx);
// the API routes move with it and the prefix is stripped before the backend.
const base = process.env.ASR_BASE || '/'
const prefix = base.replace(/\/$/, '')

// xfwd: true makes the proxy add X-Forwarded-For (and X-Forwarded-Port)
// with the real browser's address -- without it, every request the
// backend sees comes from this proxy's own outbound connection, i.e.
// 127.0.0.1 for everyone, which is what api/app.py's session tracking
// was silently recording until this was added.
const proxied = {
  target: backend,
  xfwd: true,
  ...(prefix ? { rewrite: (path) => path.slice(prefix.length) } : {}),
}
const routes = ['/rules', '/runs', '/catalog', '/library', '/system', '/profile', '/comments']

// ASR_ALLOWED_HOSTS: extra Host names the dev server answers to (comma-
// separated), e.g. hwtn.io when nginx proxies to it. Unset: Vite's default.
const allowedHosts = process.env.ASR_ALLOWED_HOSTS
  ? process.env.ASR_ALLOWED_HOSTS.split(',').map((h) => h.trim())
  : undefined

// https://vite.dev/config/
export default defineConfig({
  base,
  plugins: [react()],
  server: {
    host: true,
    ...(allowedHosts ? { allowedHosts } : {}),
    proxy: Object.fromEntries(routes.map((r) => [prefix + r, proxied])),
  },
})
