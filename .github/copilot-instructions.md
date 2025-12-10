<!-- .github/copilot-instructions.md - guidance for AI coding agents -->
# Repository notes for Copilot-style coding agents

This file contains concise, actionable information to help an AI agent be productive in this repository.

## Big picture
- Backend: Flask app (factory `create_app()` in `backend/app/__init__.py`) exposing REST APIs under `/api/*` via Blueprints.
- Frontend: Astro + React in `frontend/` (pages in `src/pages`, components in `src/components`). Frontend calls backend at `http://localhost:5000` during development.
- DB: PostgreSQL via SQLAlchemy (`backend/app/models.py`). Migrations live under `backend/migrations/` (Alembic / Flask-Migrate).

## Key files & patterns (quick reference)
- `backend/app/__init__.py` - app factory, registers blueprints and extensions (`db`, `migrate`, `jwt`, `CORS`).
- `backend/app/config.py` - `Config` class. Env vars: `DATABASE_URL`, `SECRET_KEY`, `JWT_SECRET_KEY`.
- `backend/app/models.py` - `User`, `Court`, `Booking`. Prices use `Numeric` (Decimal); datetimes are stored as `DateTime`.
- `backend/app/routes/*.py` - route handlers grouped by blueprint and mounted as:
  - `/api/auth` (register/login)
  - `/api/courts` (list courts, availability)
  - `/api/bookings` (protected; create/list user's bookings)
  - `/api/admin` (admin-only endpoints)
- `backend/run.py` - simple script to create app and run on port 5000 (dev).
- `backend/seed.py` - creates an admin user and sample courts; run inside project virtualenv.
- `frontend/src/lib/api.js` - helper wrapper for backend calls; stores token in `localStorage` key `token`.

## Authentication & API conventions
- Auth: `Flask-JWT-Extended`. `access_token` returned by `/api/auth/login` and `/api/auth/register`.
- Client stores token in `localStorage` under key `token`. Requests use header: `Authorization: Bearer <token>`.
- Dates: APIs accept and return ISO 8601 datetime strings. Backend uses `datetime.fromisoformat()` to parse.
- Errors: JSON responses often include `{"msg": "..."}` with messages in Spanish. Preserve this format when calling or mocking endpoints.
- Prices: Backend uses `Decimal`/`Numeric` and serializes prices as strings in JSON (use `str()` before returning).

## Local development workflows (Windows PowerShell examples)
- Backend setup (recommended):
```
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r backend\requirements.txt
```
- Run DB migrations (set env var for Flask CLI if you use `flask`):
```
$env:FLASK_APP='run.py'; $env:FLASK_ENV='development'; python -m flask db upgrade
```
- Start backend (dev):
```
python backend\run.py
```
- Seed initial data:
```
python backend\seed.py
```
- Frontend (from `frontend/`):
```
npm install
npm run dev
```

## Useful examples (curl)
- Register:
```
curl -X POST http://localhost:5000/api/auth/register -H "Content-Type: application/json" -d '{"email":"u@x.com","password":"pass"}'
```
- Login and store token (bash example):
```
TOKEN=$(curl -s -X POST http://localhost:5000/api/auth/login -H "Content-Type: application/json" -d '{"email":"admin@local","password":"admin123"}' | jq -r .access_token)
curl -H "Authorization: Bearer $TOKEN" http://localhost:5000/api/bookings
```

## Implementation notes & gotchas
- Blueprints mount at `/api/<name>`; ensure frontend requests include that prefix.
- Booking overlap check: `Booking.start_time < end && Booking.end_time > start` — use same logic when testing or creating bookings to match server behavior.
- Converting JWT identity: server stores identity as `str(user.id)`; routes often call `int(get_jwt_identity())`.
- Availability endpoint accepts `date=YYYY-MM-DD` and returns hourly slots between 08:00 and 22:00.
- Migrations are present — do NOT re-run `flask db init`; instead use `flask db upgrade` to apply existing migrations.

## Where to look when you need examples
- API contract examples: `backend/app/routes/*.py` (auth, bookings, courts, admin).
- Model shapes & relationships: `backend/app/models.py`.
- Frontend token handling & API base: `frontend/src/lib/api.js` and `frontend/src/components/Login.tsx`.

If anything above is unclear or incomplete, tell me which part you'd like expanded (run steps, more API examples, or explicit request/response schemas) and I'll iterate.
