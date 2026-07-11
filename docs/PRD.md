# Community Resource Navigator
### Product Requirements Document
**Author:** [Your Name]
**Context:** Anthropic + CodePath Claude Corps Fellowship — application centerpiece
**Status:** Draft v1
**Last updated:** July 2026

---

## 1. Problem Statement

Nonprofit caseworkers (at food banks, shelters, family service agencies, community health centers, etc.) regularly meet clients who need help with more than one problem at once — for example, someone facing eviction who also needs food assistance and childcare. Matching a client's specific situation to the *right* combination of local resources requires the caseworker to:

- Know an enormous, constantly-changing list of local programs, eligibility rules, hours, and application processes
- Mentally cross-reference multiple, disconnected criteria (income, location, immigration status, family size, urgency)
- Do this in a short intake window, often under emotional and time pressure

In practice, this knowledge lives in caseworkers' heads, spreadsheets, and binders. New or part-time staff and volunteers are especially disadvantaged, and referrals are frequently incomplete, outdated, or based on whichever resource the caseworker happens to remember that day.

**The problem is not "we need an AI chatbot."** The problem is: *caseworkers need a fast, reliable way to go from "here's what's going on with this client" to "here is a reviewed, correct, actionable list of resources" — without replacing their judgment.*

---

## 2. Users

### Primary user: Caseworker / Case Manager
Front-line nonprofit staff (or trained volunteers) who conduct client intake and make referrals. Time-constrained, not necessarily technical, needs to trust the tool's output because their clients' wellbeing depends on it. This is the **only** user role the MVP designs for.

### Secondary user: Program/Resource Admin
Someone (could be the same caseworker, could be an office manager) responsible for keeping the resource list accurate — adding new programs, marking ones as closed/full, updating hours. Without this role, the tool decays into another outdated binder within a month.

### Explicitly out of scope as a user
**Clients themselves.** This is an internal staff tool. A public-facing self-service version is a plausible *future* product, but it is a different set of design, privacy, and liability constraints (see Non-Goals). Building both in one fellowship project would dilute both.

---

## 3. Goals

1. Let a caseworker describe a client's situation in plain language and get a short, ranked list of *relevant, currently-accurate* resources with a plain-language rationale for each.
2. Keep a human decisively in control: the AI **suggests**, the caseworker **reviews, edits, and approves** before anything is finalized or handed to a client.
3. Produce a clean, shareable referral output (printable or copyable) the caseworker can hand to the client or attach to a case file.
4. Make the resource list itself easy to keep current, so the tool doesn't rot.
5. Be something a real, small nonprofit could actually run — no exotic infra, no ongoing maintenance burden, clear docs for handoff to another developer or a non-technical staff member.

## 4. Non-Goals (for this MVP)

Being explicit about this is as important as the goals list — this is where most "resume-padding" scope creep tries to sneak in.

- **Not** a public-facing client chatbot or self-service portal.
- **Not** an integration with live third-party data (211, Aunt Bertha/findhelp, government APIs). Real integrations are brittle, rate-limited, and often require partnership agreements — wrong bet for a 10-day demo. We use a curated local dataset instead, with a data model that *could* support a real feed later (documented as a stretch/future direction, not built).
- **Not** a full case management system (no case history, no client records, no scheduling, no notes-over-time).
- **Not** multi-organization / multi-tenant. One organization's resource list.
- **Not** user authentication / role-based access control beyond, at most, a single shared staff password gate. Building real auth is a distraction from the AI-application skills this fellowship is evaluating.
- **Not** an autonomous agent that contacts resources, books appointments, or takes any action outside the app. The AI only reads the situation description and the resource list, and proposes.
- **Not** optimized for scale. Tens to low hundreds of resources, one office's worth of concurrent staff. Correctness and clarity matter far more than throughput here.

---

## 4a. Scope Adjustment: 10-Day / Part-Time Timeline

**Reality check:** this project is being built in 10 days at ~2–3 hrs/day — roughly **20–25 total hours**, not the 4-week plan originally scoped. That budget does not fit the full MVP as written in Section 5 below. Rather than quietly hoping it'll work out, the cuts are made explicit here, in priority order. This tiering is itself a deliverable — it shows the judgment call, not just the code.

**Tier 1 — Must ship, non-negotiable (this is the actual demo):**
- Curated resource dataset (kept smaller: ~20–25 resources, not 30–50)
- Manual search/filter over the directory
- AI triage: situation → ranked suggestions with rationale
- Hallucination-filter safeguard (FR7) — this is the one piece of real engineering rigor in the project; it does not get cut
- Human review/edit layer before export
- Plain-text/print referral export
- AI-down fallback to manual search (FR8) — cheap to build, and it's the single best "production thinking" signal in the project, so it stays

**Tier 2 — Build if Tier 1 lands with time to spare:**
- Minimal admin add/edit UI (single simple page: list + form, no polish). If this doesn't get built, the fallback is a documented process: admin edits a structured `resources.json`/CSV and re-runs a seed script. That's a legitimate, honestly-documented MVP decision for a 10-day project — not a cop-out, as long as it's written down as a deliberate trade-off in the README.
- Basic accessibility pass, UI polish.

**Tier 3 — Cut entirely for this version, listed as "Future Work" in the README, not attempted:**
- All previous Section 6 stretch goals (PDF export, staleness warnings, usage log, multi-language, CSV import/export)
- Live hosted deployment. A local demo + a 2–3 minute screen-recorded walkthrough is a fine, common, and time-honest way to present this for an application — don't burn hours on Render/Vercel config unless Tier 1 and 2 are done with a full day to spare.

If you find yourself behind schedule mid-project, cut in reverse tier order (Tier 3 first, obviously already cut; then Tier 2) — never trim Tier 1's core loop or the hallucination safeguard to save time elsewhere.

---

## 5. MVP Feature Set

*(Note: read alongside Section 4a — everything below is the full original feature set; Section 4a defines what actually gets built first given the real timeline.)*

### 5.1 Resource Directory (foundation)
- A structured database of local resources: name, category (housing, food, healthcare, legal, childcare, employment, financial assistance, etc.), eligibility notes, service area, hours, contact info, application process, "active/inactive" flag, last-verified date.
- Manual search & filter (by category, keyword, active status) — this must work **even if the AI is down or misbehaves.** This is the reliability fallback and is non-negotiable.
- Basic CRUD admin view to add/edit/deactivate resources, so the directory can stay current without touching code or a database console.

### 5.2 AI-Assisted Intake Triage
- Caseworker enters a free-text description of the client's situation ("single mom, 2 kids, facing eviction next week, no car, needs food assistance too").
- Claude analyzes the situation against the **current resource directory only** (not general knowledge, not invented resources) and returns:
  - A ranked shortlist (not the whole directory) of relevant resources
  - A one-line, plain-language rationale per suggestion ("matches: emergency housing + serves families with children")
  - Any flagged gaps ("no immigration-status-specific resource found matching this")
- This is a **retrieval + reasoning** task, not open-ended generation. Claude is explicitly constrained (via prompt + provided context) to only recommend resources that exist in the directory, to prevent hallucinated programs — a real harm in this domain.

### 5.3 Human Review & Edit Layer
- Suggestions appear as an editable list: caseworker can remove a suggestion, add a resource manually from the full directory, and re-order.
- Nothing is exported or considered "final" until the caseworker explicitly approves.
- This is the core "human-in-the-loop" requirement — the UI should make it *obvious* that the list is a draft pending review, not a finished answer.

### 5.4 Referral Output
- One click to generate a clean, printable/copyable summary: client-facing language, list of approved resources with contact info and next steps.
- Exportable as plain text/print view for MVP (PDF generation is a reasonable stretch, not a requirement).

### 5.5 Reliability Fallback
- If the AI call fails or times out, the caseworker is not stuck — they land directly on the manual search/filter view with a clear, non-alarming message. The tool must be *useful even with zero AI availability.*

---

## 6. Stretch Goals / Future Work

**Status: cut for this 10-day build (see Section 4a).** Listed here for completeness and to show forward thinking in documentation/handoff — not to be attempted during the 10 days. Ordered by value-to-effort ratio, for whoever picks this project up next:

1. **PDF export** of the referral summary (nicer handoff artifact than plain text).
2. **"Last verified" staleness warnings** — flag resources not reviewed in 90+ days in the admin view (demonstrates thinking about long-term data quality, a real org problem).
3. **Basic usage log** (not analytics — just "which resources get suggested/approved most," to help an org see what's in demand). Read-only, no PII.
4. **Multi-language input** for the intake description (Claude already handles this reasonably well; mostly a UI/i18n exercise for the output template).
5. **CSV import/export** for the resource directory, so an org's existing spreadsheet becomes the seed data instead of manual re-entry.

Explicitly **not** stretch goals: authentication systems, a vector database/embeddings search layer (unnecessary at this data scale — a well-structured prompt with the full directory as context is simpler, cheaper, and just as accurate for a few dozen–few hundred resources), microservices, real-time collaboration, mobile app.

---

## 7. User Stories

| # | Story |
|---|---|
| 1 | As a caseworker, I can describe my client's situation in my own words so I don't have to know the exact program names or categories in advance. |
| 2 | As a caseworker, I can see *why* each resource was suggested so I can judge whether it actually fits, not just trust a black box. |
| 3 | As a caseworker, I can remove a bad suggestion or add a resource I know about that the AI missed, before anything is finalized. |
| 4 | As a caseworker, I can fall back to plain manual search/filter at any time, including when the AI feature is unavailable. |
| 5 | As a caseworker, I can generate a clean summary to hand to my client or attach to their file. |
| 6 | As a resource admin, I can add a new program or mark one inactive in a couple of clicks, without needing a developer. |
| 7 | As a resource admin, I can see when a resource was last verified so I know what's at risk of being stale. |
| 8 | As a new/volunteer staff member, I can use this tool on day one without training, because the workflow is obvious and the AI explains its reasoning in plain language. |

---

## 8. Functional Requirements

**Directory**
- FR1: System stores resources with fields: id, name, category, description, eligibility notes, service area, address/contact, hours, application process, active flag, last-verified date.
- FR2: Users can filter/search the directory by keyword and category without invoking AI.
- FR3: Admin can create, edit, and deactivate (soft-delete) resources.

**AI Triage**
- FR4: User submits free-text situation description.
- FR5: System sends the situation + the current active resource directory to Claude, constrained by a system prompt that requires recommendations to be drawn only from the provided list.
- FR6: System displays a ranked shortlist (target: 3–7 items) with a rationale per item.
- FR7: If Claude's response references a resource not in the directory, the system filters it out before display (defense-in-depth against hallucination) and logs the discrepancy.
- FR8: If the AI call errors or times out (e.g., 8s), the UI degrades to the manual search view with a clear, non-blaming message.

**Review & Export**
- FR9: User can remove, add, or reorder resources in the suggested list before finalizing.
- FR10: User can generate a printable/copyable referral summary from the finalized list.
- FR11: No referral is generated from unreviewed AI output — the approval step is mandatory, not skippable.

---

## 9. Non-Functional Requirements

- **Reliability:** The manual directory/search path must have zero dependency on the AI service being up. Reliability > feature count.
- **Simplicity:** Prefer boring, well-understood technology. No dependency should be added without a clear reason tied to a requirement above.
- **Maintainability:** Clear separation of concerns (data layer / API / UI), meaningful naming, comments where logic is non-obvious, and a README that lets a new engineer (or a CodePath reviewer) understand the system in under 10 minutes.
- **Data integrity:** The AI must never fabricate a resource. All displayed suggestions must be traceable to a real directory entry.
- **Performance:** AI suggestion round-trip target under ~5 seconds for a typical situation description; directory search is near-instant (local query, no network round-trip).
- **Accessibility:** Usable with keyboard navigation, sufficient color contrast, readable font sizes — this is a tool used by busy, non-technical staff, some of whom may have accessibility needs themselves.
- **Privacy:** No client names or identifying details need to be stored by the system — the intake description is used transiently for the AI call and is not persisted beyond the current session by default. This should be stated plainly in the docs as a deliberate design choice, not an oversight.
- **Documentation:** Architecture diagram, setup instructions, a short "how to add/update a resource" guide for non-technical admin users, and a demo script.

---

## 10. Success Metrics

Since this isn't shipping to a live organization (yet), metrics should demonstrate *rigor*, not vanity numbers:

- **Suggestion relevance:** For a test set of ~15–20 realistic sample situations you write yourself, what % of AI-suggested resources would a knowledgeable reviewer (you, acting as domain expert) judge as genuinely relevant? Target: ≥85%.
- **Zero hallucination rate:** 0 instances of the AI recommending a resource not present in the directory, across the test set — enforced both by prompt design and by the FR7 filtering safeguard, and verified by tests.
- **Time-to-referral (simulated):** Rough before/after comparison — manually scanning a 50-resource spreadsheet vs. using the tool — to make the value proposition concrete in your write-up/demo.
- **Fallback reliability:** 100% of manual search functionality works correctly with the AI service intentionally disabled (this should be an actual test you run and can show).
- **Usability:** If possible, a short walkthrough with 2–3 people unfamiliar with the project (classmates, friends) completing the core workflow unassisted, to demonstrate human-centered design was actually validated, not assumed.

---

## 11. Technical Architecture

Kept intentionally simple — this is the architecture of a tool a solo fellow maintains and hands off, not a system designed to impress with complexity.

```
┌─────────────────────────┐
│        Frontend          │   React (Vite) SPA
│  - Intake form            │   - Talks only to the backend API
│  - Suggestion review UI   │     (never calls Claude directly —
│  - Manual search/filter   │      keeps the API key server-side)
│  - Admin CRUD screens     │
└────────────┬─────────────┘
             │ REST (JSON)
┌────────────▼─────────────┐
│        Backend API        │   Node/Express (or FastAPI — pick
│  - /resources CRUD         │   whichever you're stronger in;
│  - /triage (AI endpoint)   │   this is a judgment call, not a
│  - Input validation         │   fixed requirement)
│  - Hallucination filter    │
│  - Calls Claude API         │
└────────────┬─────────────┘
             │
      ┌──────┴───────┐
      ▼              ▼
┌───────────┐  ┌─────────────┐
│  SQLite    │  │  Claude API  │
│  resource  │  │ (Sonnet-tier │
│  database  │  │ model, single │
│            │  │ call per       │
│            │  │ triage request)│
└───────────┘  └─────────────┘
```

**Why these choices:**
- **SQLite, not Postgres/Mongo:** dozens–hundreds of rows, single-writer admin usage, zero ops overhead, trivially portable as a single file — exactly matches the actual scale and matches "simplicity/maintainability" over "resume padding."
- **No vector DB / embeddings:** at this data scale, passing the full active resource list as structured context in the prompt is simpler, cheaper, fully accurate, and easier to debug than a retrieval pipeline. Introducing embeddings here would be over-engineering relative to the problem size — call this out explicitly in your write-up as a considered decision, not an oversight.
- **Backend proxies the Claude call:** keeps the API key off the client, and is the natural place to enforce the "only recommend real resources" safety filter (FR7) — this is also where you'd log/monitor in a real deployment.
- **No auth system:** a single shared access mechanism (or none, for a pure demo) is enough to demonstrate the workflow. Real auth is a separate, well-solved problem not central to what this fellowship is evaluating.
- **Plain REST, no GraphQL/tRPC/websockets:** nothing here is real-time or has complex query shapes. REST is boring and correct.

---

## 12. Development Milestones (10-day plan, ~2–3 hrs/day, ~20–25 hrs total)

This assumes Tier 1 from Section 4a is the target; Tier 2 (minimal admin UI) is attempted only if the schedule holds. Each day is scoped to fit the time budget — resist the urge to gold-plate a day-3 task while day-8 tasks are still unbuilt.

| Day | Focus | Output |
|---|---|---|
| **1** | Lock scope (this PRD), pick stack (backend language, confirm React frontend), scaffold both repos/folders, define resource schema. | Repo skeleton, schema decided. |
| **2** | Write the curated dataset (~20–25 resources, 5–6 categories) directly as structured JSON/CSV. Build SQLite seed script. Backend: read-only `/resources` endpoint. | Real data in a real (if minimal) DB, queryable. |
| **3** | Frontend shell + manual search/filter UI wired to `/resources`. | A working, if bare, standalone tool — good early checkpoint that de-risks the rest. |
| **4** | Design the triage prompt (constrained-to-directory recommendations, rationale, structured JSON output). Build `/triage` endpoint calling Claude. | AI returns suggestions for a hand-tested situation or two. |
| **5** | Add the hallucination-filter safeguard (FR7) and timeout/error handling (FR8). Run the ~10–15 sample-situation test set (smaller than original 15–20, given time), record relevance %. | Triage is safe and its accuracy is measured, not assumed. |
| **6** | Frontend: suggestion review/edit UI (remove/add/reorder) wired to the triage endpoint. | The full AI → human-review loop works end-to-end. |
| **7** | Referral export (plain text/print view) from the approved list. | Complete core user journey, start to finish. |
| **8** | *If on schedule:* minimal admin add/edit page (Tier 2). *If behind:* skip, and instead write the "how to update resources" doc as the documented fallback, per Section 4a. | Either a working admin page, or an honest, well-documented alternative. |
| **9** | Explicit fallback test (disable AI, confirm manual search still fully works) + light polish/accessibility pass on the core screens only. | Reliability is verified, not assumed — this is your strongest "production readiness" evidence. |
| **10** | README, architecture doc (can reuse Section 11 of this PRD), short demo script, and a 2–3 min screen recording of the core workflow. Final end-to-end smoke test. | A submittable, well-documented project. |

**Buffer note:** there is no slack day built in above — a 10-day/25-hour budget doesn't have room for one. If something on Day 4–5 (the AI integration) runs long, that's the point to cut Day 8 (admin UI) rather than compress Day 9's reliability testing or Day 10's documentation. Those two are what make this read as *production-quality* work rather than a weekend hack, and they're also the cheapest days to protect since they don't depend on anything going technically wrong.

---

## 13. Open Questions to Resolve Before Coding

Worth deciding deliberately rather than defaulting:
1. Backend language: Node/Express vs. Python/FastAPI — pick based on your own fluency, not resume value; this is invisible to the fellowship except through code quality.
2. Exact prompt structure for triage (system prompt constraints, output format — JSON vs. structured text) — worth a short design pass before implementation.
3. How much of the sample resource dataset should be real (actual local orgs, with permission/attribution) vs. clearly-labeled fictional data — matters for demo credibility and for avoiding implying you speak for real organizations.

---

*This document is intended to be a living reference for the project — update it as decisions are made, don't treat it as fixed once coding starts.*
