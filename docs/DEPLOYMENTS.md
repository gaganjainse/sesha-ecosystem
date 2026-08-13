# Deployments — where each project runs, and how to make it live

Status: living · last updated 2026-08-13

This is the single source of truth for "is X live, and how do I deploy it."
Everything repo-side (configs, adapters, blueprints) is committed and pushed;
the parts that need **your** Vercel/Render account are spelled out per repo.

## Platform matrix (honest)

| Repo | App type | Platform | Why | Status |
|---|---|---|---|---|
| portfolio | Astro (static) | Vercel | Native | ✅ live — gaganjain.vercel.app |
| vyakrti-ide | Vite React SPA | Vercel | Static demo | ✅ live — vyakrti.vercel.app (editor only; the Rust compile/REPL backend is not on Vercel — see note) |
| GameVault | Next.js 15 + Supabase | **Vercel** | Next.js is Vercel-native; Supabase is already external | 🔧 config committed; needs your Vercel import + 2 env vars |
| FWRS | Flask (stateless, CSV) | **Vercel** | No DB, no state — serverless fits | 🔧 adapter committed (`api/index.py` + `vercel.json`), verified locally |
| AIM | Flask + MySQL | Vercel = **demo page only**; full app = Render/Railway/Fly | Real app needs MySQL, file uploads, mysql/mysqldump binaries | ✅ demo live (aim-live.vercel.app); 🔧 `render.yaml` committed for the full app |
| grievance-portal | Laravel 12 + MySQL | Render/Railway/Fly | Laravel + MySQL is not Vercel-serverless-shaped | 🔧 `Dockerfile` (demo-grade) + `render.yaml` committed |
| rag-service | FastAPI + ChromaDB | Render/Railway/Fly | ChromaDB needs persistent disk | 🔧 `render.yaml` committed |
| llm-eval-harness | CLI library | — | not a web app | n/a |
| Vyakrti | Rust compiler | — | IDE frontend is vyakrti-ide (above) | n/a |
| ePustakalay | placeholder | — | empty repo, nothing to deploy | ⬜ decide: build or archive |
| shesh-*, SheshAOS | local-first components | — | desktop/agent infra, not web | n/a |

## What I cannot do from here (your clicks)

1. **Vercel deploy** — importing a repo, setting env vars, and clicking Deploy
   happens in *your* Vercel dashboard. I've committed every config so it's a
   one-click import with zero code changes.
2. **Provision a database** — MySQL/Postgres/vector-DB services need an account
   (Railway MySQL, Aiven, TiDB, Neon, Supabase, Render private service…).
3. **Secret values** — FLASK_SECRET, APP_KEY, Supabase keys, DB passwords are
   generated/pasted by you; they must never be committed.

## Per-repo steps

### GameVault → Vercel (best fit)
1. Vercel dashboard → **Add New → Project → Import `gaganjainse/GameVault`**.
   Framework auto-detected as Next.js (no build settings needed).
2. Environment variables (Project → Settings → Environment Variables):
   - `NEXT_PUBLIC_SUPABASE_URL` — your Supabase project URL
   - `NEXT_PUBLIC_SUPABASE_ANON_KEY` — the anon (public) key
3. Deploy. Build is `next build` (verified green locally; CI also builds it).
4. Note: `gamevault.vercel.app` currently returns **HTTP 402 (Payment
   Required)** — either that subdomain belongs to another Vercel account or a
   Vercel team hit a plan limit. Pick a different subdomain (e.g.
   `gamevault-demo.vercel.app`) or check your Vercel team's usage.

### FWRS → Vercel
1. Import `gaganjainse/FWRS`. It has `vercel.json` + `api/index.py` (a
   stateless Flask adapter — verified locally: GET/POST return 200 with LP
   results). No env vars needed.
2. The CLI (`main.py`), Tkinter GUI (`ui/desktop_app.py`), and map generator
   (`ui/map_generator.py`) are not web-facing; they stay local.

### AIM — full app (the Vercel site is only a demo page)
`aim-live.vercel.app` serves `templates/demo.html` via `api/index.py` — an
intentional stub that says "needs MySQL". The **real** app:
1. Provision MySQL (Railway/Aiven/TiDB, or Render private service).
2. Render: **New + → Blueprint → select `gaganjainse/AIM`** (uses the committed
   `render.yaml` + production Dockerfile: gunicorn, non-root, healthcheck).
3. Fill DB_HOST / DB_USER / DB_PASSWORD; FLASK_SECRET is auto-generated.
4. One-time: load the schema → `mysql -h <host> -u <user> -p attendance_db < database/schema.sql`.
5. Optional: keep the Vercel demo page as the public landing and link it to the
   real app.

### grievance-portal
1. Provision MySQL.
2. Render Blueprint (committed `render.yaml`) — the Dockerfile is demo-grade
   (`php artisan serve`, auto-runs `migrate --force`). **For production, swap to
   php-fpm + nginx** (noted in the Dockerfile).
3. Generate `APP_KEY` locally: `php artisan key:generate --show`, paste it.
4. The app has mail/SMS env keys (MAIL_*, SMS_*) — leave blank for demo; the
   Laravel 11→12 upgrade already cleared its dependency alerts.

### rag-service
1. Render Blueprint (committed `render.yaml`, Dockerfile runs uvicorn).
2. **ChromaDB persists to the container disk and resets on redeploy.** For
   durable storage, attach a Render disk and point ChromaDB at it, or swap the
   store for a hosted vector DB.

### vyakrti-ide (already live — but understand what's deployed)
The Vercel site is the **editor UI only**. Compile/REPL/LSP need the Rust axum
backend (`vyakrti-ide/backend` in the Vyakrti repo), which cannot run on
Vercel. If you want a fully functional IDE demo, host the backend on
Railway/Render/Fly and point the frontend's API base URL at it.

## Env var reference (do not commit these)

| Repo | Var | How to get it |
|---|---|---|
| GameVault | NEXT_PUBLIC_SUPABASE_URL / ANON_KEY | Supabase → Project Settings → API |
| AIM | FLASK_SECRET | auto (Render generateValue) or `openssl rand -hex 32` |
| AIM | DB_HOST/DB_USER/DB_PASSWORD/DB_NAME | your MySQL provider |
| grievance-portal | APP_KEY | `php artisan key:generate --show` |
| grievance-portal | DB_* | your MySQL provider |
| rag-service | (none) | — |
