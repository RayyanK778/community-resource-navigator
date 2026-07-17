# Community Resource Navigator

An internal tool for nonprofit caseworkers: describe a client's situation in
plain language, get AI-suggested resources with rationale, review/edit before
anything is finalized, and export a clean referral summary.

Built for the Anthropic + CodePath Claude Corps Fellowship. Full product
requirements, scope decisions, and architecture rationale are in
[`docs/PRD.md`](docs/PRD.md) — read that first, especially Section 4a (scope
tiering for the 10-day build) and Section 11 (architecture decisions).

## Project structure

```
community-resource-navigator/
├── backend/          FastAPI + SQLite API
│   └── app/
│       ├── main.py         app entrypoint, health check
│       ├── database.py     SQLite engine/session
│       ├── models.py       SQLAlchemy Resource model
│       ├── schemas.py      Pydantic request/response schemas
│       └── constants.py    fixed category list
├── frontend/          React (Vite) SPA
└── docs/
    └── PRD.md
```

## Status

**Milestone 2 of 10-day plan — resource directory complete.**
- [x] Backend boots, connects to SQLite, `/health` returns 200
- [x] `resources` table schema created (matches PRD Section 8)
- [x] Frontend boots (Vite dev server)
- [x] Seed script with 24 fictional King County resources (7 categories, idempotent)
- [x] `GET /resources` — list, keyword search (`q`), category filter, `include_inactive` flag
- [x] `GET /resources/{id}` — detail, 404 on missing id
- [x] `GET /resources/categories` — category list with display labels
- [ ] Manual search/filter UI (next)
- [ ] AI triage
- [ ] Human review UI + export
- [ ] Admin UI / reliability testing / docs

See `docs/PRD.md` Section 12 for the full day-by-day plan.

## API reference (current)

| Method | Path | Notes |
|---|---|---|
| GET | `/health` | Health check |
| GET | `/resources` | Query params: `category`, `q`, `include_inactive` |
| GET | `/resources/{id}` | 404 if not found |
| GET | `/resources/categories` | `[{value, label}, ...]` for UI dropdowns |

Interactive docs available at `http://localhost:8000/docs` when the server is running.

## Seeding the database

**macOS / Linux:**
```bash
cd backend
python3 -m app.seed
```

**Windows (PowerShell):**
```powershell
cd backend
python -m app.seed
```

Safe to re-run — matches existing rows by name and updates them rather than duplicating.

## Running locally

### Backend

**macOS / Linux:**
```bash
cd backend
pip install -r requirements.txt --break-system-packages   # or use a venv
python3 -m uvicorn app.main:app --reload --port 8000
```

**Windows (PowerShell):**
```powershell
cd backend
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```
> If `Activate.ps1` is blocked by execution policy, run PowerShell as Administrator once and use:
> `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

Visit `http://localhost:8000/health` — should return `{"status": "ok"}`.

### Frontend

**macOS / Linux / Windows (PowerShell) — identical:**
```bash
cd frontend
npm install
npm run dev
```
Visit `http://localhost:5173`.
