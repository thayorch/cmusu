# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

CMU Student Union (สโมสรนักศึกษามหาวิทยาลัยเชียงใหม่) website — a full-stack portal for student services: news, activities, equipment borrowing, and issue reporting.

**Stack:** Vue 3 (Composition API) + Vite 5 + Tailwind CSS 3 (frontend) · FastAPI + Python 3.11 + Uvicorn (backend) · Supabase (PostgreSQL + Auth) · Microsoft Azure OAuth · Deployed on Vercel

## Development Commands

### Local (Docker — recommended)
```bash
docker-compose up          # starts both frontend (:5173) and backend (:8000)
```

### Frontend only
```bash
cd frontend
npm install
npm run dev                # Vite dev server on :5173
npm run build              # production build → dist/
npm run preview            # preview production build
```

### Backend only
```bash
cd backend
pip install -r requirements.txt
python main.py             # Uvicorn with --reload on :8000
```

No test suite or linter is configured for either side.

## Architecture

### Request flow
```
Browser → Vue Router (SPA)
       → /api/* → Vite proxy (dev) or Vercel rewrite (prod) → FastAPI backend
                                                             → Supabase PostgreSQL
```

In **development**, `frontend/vite.config.js` proxies `/api` to the production backend on Vercel (not to the local Docker backend). If you need to test against the local backend, update the proxy target in `vite.config.js`.

In **production**, `frontend/vercel.json` rewrites `/api/(.*)` to `https://subackend.vercel.app/api/$1` and all other paths to `index.html` for SPA routing.

### Backend (`backend/`)
- `main.py` — app entry point, mounts all routers under `/api`, configures CORS
- `routers/` — one file per domain: `auth`, `borrow`, `admin`, `news`, `activity`, `reports`, `csrf`
- `dependencies.py` — `get_current_user_role()` and `admin_required` FastAPI dependency guards
- `db/database.py` — Supabase client singleton
- `models/schemas.py` — Pydantic models for all request/response bodies
- `utils/email.py` — Gmail SMTP via `fastapi-mail`, called via `BackgroundTasks`

### Frontend (`frontend/src/`)
- `router/index.js` — all routes; `/admin` and `/borrow-central` require auth
- `Pages/` — full-page components (one per route)
- `components/` — shared components including `Admin/` sub-folder for admin dashboard panels
- `composables/useAlert.js` — global alert state
- `composables/useCsrf.js` — fetches and stores the CSRF token from `/api/csrf/token`

### Authentication
- Microsoft Azure OAuth via Supabase Auth — initiated at `/api/auth/login`, callback at `/api/auth/callback`
- Token stored in an HTTP-only cookie (`access_token`, `samesite=lax`)
- Admin role stored in `app_metadata.role` on the Supabase user record

### CSRF
All mutating requests from the frontend must include the `X-CSRF-Token` header. The token is fetched once per session via `useCsrf.js` and attached to requests manually (not via Axios interceptors — the project uses native `fetch`).

### Database
Key Supabase tables: `equipments`, `borrow_requests`, `borrow_request_items`, `faculties_equipments`, `news`, `activities`, `reports`. Complex checkout logic runs through a Supabase RPC function `checkout_borrow_cart`.

## Environment

Backend config lives in `backend/.env` (not committed). Required variables:
- `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY`
- `CSRF_SECRET_KEY`
- `FRONTEND_URL`, `BACKEND_URL`
- Gmail SMTP credentials for email notifications
