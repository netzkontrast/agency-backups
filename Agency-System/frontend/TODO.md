# `frontend/` — TODO & Handoff

> **Read this first.** This file is the bridge between the prototype work
> done in HTML and the production Next.js app you're about to build.
> If you're an LLM coming in cold: everything you need to know is below.

---

## 1 · What this is

**Agency** is the operations frontend for a long-horizon, machine-readable
software repo run by AI agents (`netzkontrast/agency`). The repo's source of
truth is **plain markdown with frontmatter** and JSON files on disk:

```
tasks/{id}-{slug}/TASK.md          # canonical work item
prompts/{slug}.md                  # prompt specs (task-spec, research-proposal…)
research/{slug}/RESEARCH.md        # research outputs
friction-logs/{task_id}/{ts}.md    # friction events (FL0–FL3)
precommit/runs/{id}.json           # pre-commit gate run history
coherence/runs/{date}.md           # daily coherence report
runtime/agents.jsonl               # live agent telemetry (appended)
runtime/chat.jsonl                 # live chat (appended)
```

The **Agency frontend** is the *human* lens onto this repo. It is **not**
a CMS — it is a real-time dashboard for watching agents work, intervening
in their loops, and auditing the audit graph (task ↔ prompt ↔ research).

> *"Machine, Actor, Space"* — the system is a **machine** (deterministic
> pipelines), populated by **actors** (humans + agents), operating in a
> shared **space** (the repo).

---

## 2 · Tone, vocabulary, visual DNA

The look is intentionally **terminal-adjacent / engineering-instrument**,
not "AI dashboard SaaS". Anchors:

- **Background:** `#0B0D17` (near-black), panel `#0D0F18`, border `#1E2028`
- **Type:**
  - **Sans:** Space Grotesk (UI, headlines)
  - **Mono:** JetBrains Mono (telemetry, IDs, code, captions)
  - **Display serif (logo only):** DM Serif Display
- **Accent palette:**
  - `#00FF9F` — primary (signal green; "online / pass / running")
  - `#FFDF00` — caution (yellow; "in-progress / warn")
  - `#FF4D6D` — alarm (red; "fail / blocked")
  - `#7C5CFF` — research (purple)
  - `#FFB454` — sentinel / watcher (orange)
- **Micro-detail:** small mono labels in `rgba(255,255,255,0.3)` like
  `AGENCY // DASHBOARD // 2026-05-05`, scanline patterns, glow filters on
  status dots, blinking cursor blocks.
- **No** rounded-corner-with-left-accent cards. **No** generic AI gradients.
  **No** emoji. Use placeholders for missing imagery.
- **Density:** comfortable but information-dense. 12–14px is the working
  range; mono captions can drop to 9–11px. Never below 9px.

The **logo** lives at `frontend/assets/logo.svg` (also copied to project
root as `agency-logo.svg`):
- Wordmark: **A** (green serif) + **gency** (white serif, smaller)
- Claim: `MACHINE · ACTOR · SPACE` in mono
- Credit: `by netzkontrast` (netz green, kontrast white)
- **Freigestellt** — transparent background, no frame.

---

## 3 · Where we left off

The **current state of `frontend/`** is a *prototype-stage* artifact:

| File                              | Status         | Notes                                      |
| --------------------------------- | -------------- | ------------------------------------------ |
| `frontend/index.html`             | placeholder    | Linked from project root README            |
| `frontend/agency-data.js`         | reference data | Static JSON dump matching the API shape    |
| `frontend/assets/logo.svg`        | **canonical**  | Use exactly. Don't re-draw.                |
| `frontend/assets/hero.svg`        | for README     | Header banner only                         |
| `frontend/brand-assets.html`      | scratch        | Visual review of logo/hero — delete later  |
| `frontend/tweaks-panel.jsx`       | unused here    | Was a prototype-only Tweaks panel          |

The **real** prototype that defines the product is at the project root:

- **`Agency Frontend v3.html`** ← canonical source of truth for layout,
  vocabulary, and view-by-view behavior. Read this end-to-end before
  starting. Every view below has been built once there.

---

## 4 · Mission

Replace `Agency Frontend v3.html` with a **production Next.js app** under
`frontend/` that:

1. Consumes the **FastAPI** REST + **SSE** surface in `backend/` (see
   `backend/README.md` for the contract).
2. Preserves the prototype's vocabulary, density, and visual DNA exactly —
   pixel-fidelity to v3 is the goal, not "reinterpretation".
3. Is **typed end-to-end** (TypeScript strict, generated types from the
   API where useful).
4. Stays a **single-window app**: there is no marketing site, no auth, no
   tenancy. One operator, one repo.

---

## 5 · Stack decisions (committed)

- **Next.js 14, App Router, RSC where it helps, TS strict**
- **Tailwind CSS** for layout primitives + a small `tokens.css` for the
  exact palette/type vars below — *do not* let Tailwind invent colors.
- **Data:**
  - One-shot fetch of `/api/snapshot` on first paint (RSC).
  - Client `useSnapshot()` hook hydrates from RSC, then subscribes to
    `/api/events` via `EventSource` and patches the in-memory store on
    `agent.update`, `chat.message`, `tasks.update`, etc.
  - No React Query, no Redux. A `useSyncExternalStore` over a tiny
    pub/sub is plenty (the SSE stream *is* the cache invalidator).
- **Routing = the sidebar.** One route per view (see §7). No modals for
  primary nav.
- **No SSR fetching from inside the API route handlers** — the Next app
  is a pure client of the FastAPI backend. (Optional: add a thin
  `/api/proxy/*` rewrite if CORS gets in the way during dev.)

---

## 6 · Token bridge (Tailwind ⇄ prototype)

Add this to `app/globals.css`. **Do not** re-derive colors elsewhere.

```css
:root {
  --bg:        #0B0D17;
  --panel:    #0D0F18;
  --panel-2:  #06080F;
  --border:   #1E2028;
  --border-2: #2A2D38;

  --fg:       #FFFFFF;
  --fg-2:     rgba(255,255,255,0.78);
  --fg-3:     rgba(255,255,255,0.55);
  --fg-4:     rgba(255,255,255,0.30);
  --fg-5:     rgba(255,255,255,0.18);

  --accent:    #00FF9F;
  --warn:      #FFDF00;
  --alarm:     #FF4D6D;
  --research:  #7C5CFF;
  --sentinel:  #FFB454;

  --font-sans: 'Space Grotesk', system-ui, sans-serif;
  --font-mono: 'JetBrains Mono', ui-monospace, monospace;
  --font-serif:'DM Serif Display', Georgia, serif; /* logo only */
}
```

Map these in `tailwind.config.ts` under `theme.extend.colors` and
`theme.extend.fontFamily` so utility classes like `bg-panel text-fg-3
font-mono` work.

---

## 7 · Views to port (each = one route)

Source of truth for every view: `Agency Frontend v3.html`. For each, lift
the **layout, copy, status logic, and ASCII flourishes** verbatim, then
re-implement against the API.

| Route             | Component         | API consumed                                          |
| ----------------- | ----------------- | ----------------------------------------------------- |
| `/`               | `<Dashboard/>`    | `/api/snapshot` + SSE                                 |
| `/tasks`          | `<TasksList/>`    | `/api/tasks` (filters in querystring)                 |
| `/tasks/[id]`     | `<TaskDetail/>`   | `/api/tasks/{id}` + related prompts/research/friction |
| `/prompts`        | `<PromptsList/>`  | `/api/prompts`                                        |
| `/prompts/[slug]` | `<PromptDetail/>` | `/api/prompts/{slug}`                                 |
| `/research`       | `<Research/>`     | `/api/research`                                       |
| `/friction`       | `<FrictionLog/>`  | `/api/friction-logs` (FL0–FL3 filter tiles)           |
| `/precommit`      | `<Precommit/>`    | `/api/precommit/runs`                                 |
| `/agents`         | `<Agents/>`       | `/api/agents` + `agent.update` SSE                    |
| `/chat`           | `<Chat/>`         | `/api/chat/channels` + `/api/chat/{ch}/messages`      |
| `/graph`          | `<RepoGraph/>`    | `/api/graph`                                          |
| `/settings`       | `<Settings/>`     | static + `.agency/config.toml` (read-only for now)    |

### Cross-cutting UI
- **Sidebar** with collapse toggle, logo at top (use `assets/logo.svg`),
  active-route highlight, and the bottom status pill (`◼ agency/<view>`).
- **Command palette** (`⌘K`) — fuzzy across tasks/prompts/research; backed
  by the future `/api/find?q=` (or do client-side over the snapshot for
  now).
- **Toast/log strip** for SSE events the user should notice (e.g.
  `precommit.update status=fail`).

---

## 8 · Concrete work plan

Tackle in this order. Each step ends in a commit.

1. **Scaffold.** `pnpm create next-app frontend --ts --tailwind --app
   --src-dir --import-alias "@/*"`. Add `globals.css` tokens from §6.
2. **API client.** `src/lib/api.ts` — typed fetchers for every endpoint
   in `backend/README.md`. Generate `Snapshot`, `Task`, `Prompt`,
   `Research`, `Agent`, `Message`, `PrecommitRun`, `FrictionLog`,
   `CoherenceRun`, `GraphNode`, `GraphEdge`. No `any`.
3. **SSE hook.** `src/lib/useSnapshot.ts` — hydrate from RSC, then
   `new EventSource('/api/events')` and patch by event type.
4. **Shell.** `src/app/layout.tsx` with sidebar + logo + status footer.
   Move all layout chrome from `Agency Frontend v3.html` here.
5. **Port views** in the order above (`/`, `/tasks`, `/tasks/[id]`, …).
   Each view: lift markup → React, swap inline data refs for hook calls,
   keep the mono captions and status dots intact.
6. **Command palette.**
7. **README.md + `.env.example`.** Document `NEXT_PUBLIC_API_BASE`
   pointing at `http://localhost:8000`.
8. **Smoke test.** Boot backend (`make -C ../backend dev`), boot
   frontend (`pnpm dev`), open every route, verify SSE patches a chat
   message live.

---

## 9 · Non-negotiables / common traps

- **No emoji**, ever, in UI. Mono captions and ASCII glyphs (`◼ ◇ ▮ ›`)
  are the visual vocabulary.
- **No new colors.** If you need one, it goes in `tokens.css` first and
  is justified in the commit message.
- **No "AI assistant" chrome** (sparkles, gradient buttons, etc.). This
  is an instrument panel, not a chatbot.
- **Status logic lives in one place.** Build a `statusOf(task | run |
  agent)` helper that returns `{ label, color, dot }` so every list and
  pill reads the same.
- **Don't fan-out fetch.** `/api/snapshot` returns the whole world; only
  the detail pages issue extra fetches.
- **Logo is fixed.** Don't re-draw it. If the brief changes, edit
  `assets/logo.svg` once and let every consumer pick it up.
- **Speaker-notes / deck conventions don't apply** — this is an app, not
  a deck.

---

## 10 · Open questions for the human

- Authentication boundary: is this strictly localhost, or does it ever
  ship behind a tunnel? (Affects CORS + `EventSource` auth.)
- Write actions beyond `POST /api/chat/.../messages` and
  `POST /api/agents/.../release` — do we add task-status mutation here,
  or stay read-mostly and let the agents own all writes?
- `/graph` view fidelity: is the existing v3 prototype's force-directed
  layout the target, or do we want a Sugiyama/DAG layout once the data
  shape is real?
- Multi-repo: today the backend serves one repo via `AGENCY_REPO_ROOT`.
  If we ever go multi-repo, that's a header (`X-Agency-Repo`) and a
  repo-picker in the sidebar — flag this before assuming single-tenancy
  is permanent.
