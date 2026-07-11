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

**Day 1 of 10 — scaffolding complete.**
- [x] Backend boots, connects to SQLite, `/health` returns 200
- [x] `resources` table schema created (matches PRD Section 8)
- [x] Frontend boots (Vite dev server)
- [ ] `/resources` CRUD endpoints (Day 2)
- [ ] Seed dataset (Day 2)
- [ ] Manual search/filter UI (Day 3)
- [ ] AI triage (Day 4–6)
- [ ] Human review UI + export (Day 6–7)
- [ ] Admin UI / reliability testing / docs (Day 8–10)

See `docs/PRD.md` Section 12 for the full day-by-day plan.

## Running locally

### Backend
```bash
cd backend
pip install -r requirements.txt --break-system-packages   # or use a venv
python3 -m uvicorn app.main:app --reload --port 8000
```
Visit `http://localhost:8000/health` — should return `{"status": "ok"}`.

### Frontend
```bash
cd frontend
npm install
npm run dev
```
Visit `http://localhost:5173`.
