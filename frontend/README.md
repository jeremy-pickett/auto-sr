# ASR frontend (2.x)

The dark-observatory web interface for Autonomous Semantic Ruliology 2.x: library browser, run
player with six render styles, rule detail with provenance, the Invent view over the generation
stream, modifier catalog, optional Firebase Email/Password sign-in with a personal library, and
the System view.

Built with Vite and React 19. Started from the Vite React template; the template's own README is
in version history.

## Commands

- `npm run dev` — dev server on :5173, proxying `/rules /runs /catalog /library /system /profile
  /comments` to the backend on :8000. Binds `0.0.0.0` deliberately (`server.host: true`) — this
  machine is reached by external IP, and a loopback-only bind looks "up but unreachable."
- `npm run build` — production build
- `npm run lint` — oxlint (config in `.oxlintrc.json`)

Two recurring gotchas, documented in `CLAUDE.md`: a new top-level backend route must be added to
the dev proxy list or it fails silently in dev; and if the dev server is unreachable, check
`ss -tlnp | grep 5173` for a loopback-only bind before debugging anything else.

Sign-in needs `VITE_FIREBASE_*` values in `frontend/.env` (see `.env.example`); the app runs
anonymously without them.

The full subsystem deep-dive is `documents/deep-dive/06-frontend.md`.
