# `backend/` — TODO & Handoff

> **Read this first.** If you're an LLM coming in cold: this is the data
> spine of the Agency system. The frontend is replaceable; this contract
> is not. Everything you need to understand the design intent is below.

---

## 1 · What this is

A Python service that **watches an Agency repo** (markdown + JSON on
disk + appended JSONL streams) and serves its state to two clients:

- **FastAPI** — REST + SSE for the Next.js frontend
- **FastMCP** — same data exposed as LLM-callable tools (stdio or SSE)

Both surfaces share **one in-memory `RepoState`** kept hot by a
`watchdog`-driven file watcher and `tail -f`-style JSONL readers.

```
   repo/                         backend/agency_backend/
   ├─ tasks/*.md      ─┐         ├─ app.py          # FastAPI + SSE
   ├─ prompts/*.md     ├──→      ├─ mcp_server.py   # FastMCP tools
   ├─ research/*.md    │         ├─ state.py        # RepoState (single source)
   ├─ friction-logs/   │         ├─ watcher.py      # watchdog → reload_path
   ├─ precommit/runs/  │         ├─ parsers.py      # frontmatter walkers
   ├─ coherence/runs/  │         ├─ runtime.py      # JSONL tailer
   ├─ runtime/agents.jsonl       ├─ config.py       # env-var settings
   └─ runtime/chat.jsonl         └─ __main__.py     # `python -m agency_backend`
```

---

## 2 · Design intent

Two principles that override convenience:

1. **The repo is the database.** The backend never persists anything of
   its own. If a fact isn't in markdown / JSON / JSONL on disk, it
   doesn't exist. This makes the system **forkable, diffable,
   git-blameable, and AI-agent-friendly** — the same contract serves
   humans, agents, and LLM tools.

2. **REST and MCP must agree, byte-for-byte.** A tool call from an LLM
   and a `fetch()` from the frontend should see the same `Task` object.
   That's why both surfaces import `state.get_state()` and never reach
   for the filesystem directly.

Side-effects of these:
- No DB, no migrations, no ORM. Adding state = adding a file format +
  a parser + a key on `RepoState`.
- Restart-safe: blow the process away, it rebuilds in <1s from disk.
- Live: every disk write reaches the frontend via SSE within ~50ms.

---

## 3 · Where we left off

| Module                | Status     | Notes                                              |
| --------------------- | ---------- | -------------------------------------------------- |
| `state.py`            | ✅ done    | RepoState + async pub/sub + targeted reload        |
| `parsers.py`          | ✅ done    | Tasks, prompts, research, friction, precommit, coherence + graph |
| `watcher.py`          | ✅ done    | Watchdog → asyncio bridge, prefix-filtered         |
| `runtime.py`          | ✅ done    | `tail_jsonl()` + `read_jsonl()`, rotation-safe     |
| `app.py`              | ✅ done    | All REST endpoints in §5, SSE                      |
| `mcp_server.py`       | ✅ done    | All MCP tools in §6                                |
| `config.py`           | ✅ done    | Env-var settings                                   |
| `tests/`              | ✅ scaffolded | Parsers, state, app — `make test`               |
| `runtime/*.jsonl`     | ✅ samples | Hand-authored fixtures for the frontend           |
| `pyproject.toml`      | ✅ done    | `pip install -e .` works; console scripts wired   |
| `Makefile`            | ✅ done    | `make dev / mcp / test`                           |

**What's missing** to call this v0.1:

1. **Real-world repo soak test** — point at `netzkontrast/agency` itself
   and verify the watcher doesn't thrash on `.git/` writes (the watcher
   already prefix-filters; double-check under load).
2. **Write-side endpoints.** Today only `POST /chat/.../messages` and
   `POST /agents/.../release` mutate. Add: task status transitions,
   prompt creation, friction-log append. Each writes a file on disk and
   lets the watcher pick up the change (no in-memory shortcut).
3. **`POST /api/agents/{id}/cancel`** + a `signal` JSONL stream the
   actual agent runtime can subscribe to. Right now `release` is a no-op
   that only patches `RepoState`.
4. **Auth.** None today. Add a single `AGENCY_TOKEN` shared-secret check
   on a Bearer header before this leaves localhost.
5. **`/api/find?q=`** — fuzzy search across all entities. The MCP
   surface has it (`find()`); promote to REST for the frontend's
   command palette.
6. **Schema export.** `GET /api/openapi.json` is free from FastAPI, but
   we should also emit a `schemas/snapshot.schema.json` to the repo so
   the frontend can codegen `Snapshot` types.

---

## 4 · Repo layout the parsers expect

If your repo doesn't match this, edit `parsers.py` — not the convention
in the repo. The conventions are the product.

```
tasks/{id}-{slug}/TASK.md
  frontmatter: id, slug, status, priority, owner, summary,
               uses_prompts[], spawns_research[], blocked_by[],
               supersedes, superseded_by, created, updated

prompts/{slug}.md
  frontmatter: slug, kind (task-spec | research-proposal | …),
               relates_to_task, summary, created, updated

research/{slug}/RESEARCH.md
  frontmatter: slug, phase (proposed | in_progress | done),
               executes_prompt, summary, created, updated

friction-logs/{task_id}/{ISO8601}.md
  frontmatter: task, level (FL0|FL1|FL2|FL3), session, agent,
               duration, tokens, note?

precommit/runs/{ISO8601}.json
  native JSON: {id, task, status, duration, branch, checks{...}, log?}

coherence/runs/{date}.md
  frontmatter: date, status (pass|partial|fail), issues, deferred, note?

runtime/agents.jsonl   # appended live; upsert-by-id semantics
runtime/chat.jsonl     # appended live; per-line {channel, ...}
```

---

## 5 · REST contract (frozen)

Every endpoint returns plain JSON. Filters are query-string. No pagination
yet — snapshot is small enough to ship whole.

```
GET    /api/snapshot                       → full RepoState
GET    /api/tasks?status=&priority=        → Task[]
GET    /api/tasks/{id}                     → Task
GET    /api/prompts?kind=                  → Prompt[]
GET    /api/prompts/{slug}                 → Prompt
GET    /api/research?phase=                → Research[]
GET    /api/research/{slug}                → Research
GET    /api/friction-logs                  → FrictionLog[]
GET    /api/precommit/runs                 → PrecommitRun[]
GET    /api/coherence/runs                 → CoherenceRun[]
GET    /api/agents?status=                 → Agent[]
GET    /api/agents/{id}                    → Agent
POST   /api/agents/{id}/release            → {ok, agent}
GET    /api/chat/channels                  → Channel[]
GET    /api/chat/{channel}/messages?limit= → Message[]
POST   /api/chat/{channel}/messages        → {ok, message}
GET    /api/graph                          → {nodes[], edges[]}
GET    /api/events  (text/event-stream)    → SSE
```

SSE event types: `snapshot`, `tasks.update`, `prompts.update`,
`research.update`, `friction.update`, `precommit.update`,
`coherence.update`, `agent.update`, `chat.message`, `channels.update`.

---

## 6 · MCP contract

Tools (all return JSON, all read from `RepoState`):

```
list_tasks(status?, priority?)        get_task(id)
list_prompts(kind?)                   list_research(phase?)
list_agents(status?)
tail_chat(channel, limit?)            post_chat(channel, text, author?)
find(query, limit?)                   repo_graph()
repo_summary()
```

Run `python -m agency_backend.mcp_server` for stdio (default) or
`AGENCY_MCP_TRANSPORT=sse` for SSE on `:8765`.

---

## 7 · Concrete work plan (next-up)

Tackle in this order. Each step is a single commit.

1. **`/api/find`.** Promote `find()` from MCP. One line in `app.py` plus
   reuse of the MCP impl.
2. **Auth middleware.** `Authorization: Bearer ${AGENCY_TOKEN}` if
   `AGENCY_TOKEN` is set; otherwise open. Bypass for `/health`.
3. **Write endpoints** (in order of utility):
   1. `POST /api/tasks/{id}/status` — writes back to `TASK.md` frontmatter
   2. `POST /api/friction-logs` — appends a new `friction-logs/{task}/{ts}.md`
   3. `POST /api/prompts` — creates `prompts/{slug}.md`
   Each writes the file, then lets the watcher trigger the SSE event.
4. **`schemas/`.** Emit JSON Schemas for every entity (Pydantic →
   `model_json_schema()`); commit them to the repo so the frontend can
   codegen.
5. **Soak test.** Run against the real repo for 24h; confirm
   memory/CPU stays flat.
6. **Health + metrics.** `/health`, `/metrics` (Prometheus text format).
7. **Container.** `Dockerfile` (multi-stage, ~80MB), `docker-compose.yml`
   pairing backend + frontend.

---

## 8 · Non-negotiables / common traps

- **Never persist outside the repo.** No SQLite cache, no Redis. The
  filesystem is the source of truth; if you cache, cache *in process*.
- **Watcher must be prefix-filtered.** Watching the whole repo
  recursively without prefix-filtering will fire on `.git/`, `node_modules/`,
  `dist/`. The current `WATCHED_PREFIXES` whitelist is the right model —
  extend it, don't bypass it.
- **All mutations go through `RepoState`** (which publishes). If you
  mutate an internal list directly, the SSE stream will silently miss
  the update.
- **JSONL tailers are the only allowed background loops.** Anything
  else lives in the lifespan handler so it's cancelled cleanly on
  shutdown.
- **REST and MCP must stay byte-equivalent.** When you add a field to
  `Task`, both surfaces start returning it for free because they read
  the same dict. Don't introduce surface-specific shaping.
- **Pydantic models are for request/response shaping only**, not for
  the in-memory state. Keep `RepoState` as plain dicts/lists so it
  stays JSON-trivial to publish.

---

## 9 · Open questions for the human

- **Conflict policy** when an agent and a human edit the same file at
  the same time. Today: last-write-wins because we're just `tail`-ing.
  Do we need an optimistic-lock (`If-Match: <sha>`) on POST endpoints?
- **History/audit.** The repo *is* the history (git), but the SSE
  stream is ephemeral. Do we want an append-only `events.jsonl` so the
  frontend can scroll back through what happened overnight?
- **Multi-repo.** Today: one process per repo via `AGENCY_REPO_ROOT`.
  Tomorrow: a parent process with N `RepoState` instances keyed by
  repo? Decide before adding auth — affects the URL shape
  (`/api/{repo}/snapshot`) or header (`X-Agency-Repo`).
- **Agent runtime ↔ backend.** Right now `agents.jsonl` and
  `chat.jsonl` are written by *whoever* runs the agents. Should the
  backend grow an inverse channel — a JSONL file the agents *read* —
  so the frontend can issue commands (`release`, `cancel`,
  `assign-task`) without each runtime inventing its own protocol?
