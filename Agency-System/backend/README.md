# Agency Backend

Python service that **watches your repo**, parses frontmatter for tasks /
prompts / research / friction-logs / pre-commit runs / agents / chat, and
serves the data as:

- a **FastAPI** REST + SSE API (consumed by `frontend/`)
- an **MCP server** (FastMCP) exposing the same data as tools an LLM can call

Both surfaces share one in-memory **`RepoState`** kept hot by a
`watchdog`-driven file system watcher.

```
   repo/                       backend/
   ├─ tasks/*.md      ─┐       ├─ app.py          # FastAPI app + SSE
   ├─ prompts/*.md     ├──→    ├─ mcp_server.py   # FastMCP tools
   ├─ research/*.md    │       ├─ state.py        # RepoState (single source of truth)
   ├─ friction-logs/   │       ├─ watcher.py      # watchdog → state.reload(path)
   ├─ precommit/runs/  │       ├─ parsers.py      # frontmatter + dir walkers
   ├─ agents.jsonl     │       └─ runtime.py      # tail agents.jsonl + chat.jsonl
   └─ chat.jsonl      ─┘
```

## Quickstart

```bash
cd backend
pip install -r requirements.txt
export AGENCY_REPO_ROOT=/path/to/your/repo
python -m agency_backend                 # FastAPI on :8000
python -m agency_backend.mcp_server      # MCP server on stdio (or :8765 SSE)
```

Frontend wiring — point `agency-data.js` at the live API:

```html
<!-- replace the static <script src="agency-data.js"></script> with: -->
<script>
  fetch('http://localhost:8000/api/snapshot')
    .then(r => r.json())
    .then(d => { window.AGENCY_DATA = d; window.dispatchEvent(new Event('agency-data-ready')); });
</script>
```

…or subscribe to live updates:

```js
const es = new EventSource('http://localhost:8000/api/events');
es.addEventListener('snapshot', e => { window.AGENCY_DATA = JSON.parse(e.data); rerender(); });
es.addEventListener('agent.update', e => { /* patch one agent */ });
es.addEventListener('chat.message', e => { /* append to channel */ });
```

## Endpoints

| Method | Path                              | Returns                                    |
| ------ | --------------------------------- | ------------------------------------------ |
| GET    | `/api/snapshot`                   | full `AGENCY_DATA` shape (one shot)        |
| GET    | `/api/tasks`                      | all tasks                                  |
| GET    | `/api/tasks/{id}`                 | single task                                |
| GET    | `/api/prompts`                    | all prompts                                |
| GET    | `/api/prompts/{slug}`             | single prompt                              |
| GET    | `/api/research`                   | all research                               |
| GET    | `/api/research/{slug}`            | single research                            |
| GET    | `/api/friction-logs`              | friction logs                              |
| GET    | `/api/precommit/runs`             | pre-commit run history                     |
| GET    | `/api/coherence/runs`             | coherence run history                      |
| GET    | `/api/agents`                     | live agents                                |
| GET    | `/api/agents/{id}`                | single agent                               |
| POST   | `/api/agents/{id}/release`        | release context (mock action)              |
| GET    | `/api/chat/channels`              | channels + DMs                             |
| GET    | `/api/chat/{channel}/messages`    | messages in a channel                      |
| POST   | `/api/chat/{channel}/messages`    | post a message; routes to agent runtime    |
| GET    | `/api/graph`                      | nodes + edges (audit graph)                |
| GET    | `/api/events`                     | SSE stream of live updates                 |

## MCP Tools

Exposed via `mcp_server.py` (stdio by default, SSE optional):

- `list_tasks(status?, priority?)` → `Task[]`
- `get_task(id)` → `Task`
- `list_prompts(kind?)` → `Prompt[]`
- `list_research(phase?)` → `Research[]`
- `list_agents(status?)` → `Agent[]`
- `tail_chat(channel, limit?)` → `Message[]`
- `post_chat(channel, text)` → `{ok: true}`
- `find(query)` → fuzzy entity search across all kinds
- `repo_graph()` → graph nodes + edges
- `recent_changes(since?)` → file changes seen by watcher

## Configuration

Environment vars (all optional):

| Var                       | Default                  | Purpose                           |
| ------------------------- | ------------------------ | --------------------------------- |
| `AGENCY_REPO_ROOT`        | `..`                     | Repo to watch                     |
| `AGENCY_HOST`             | `0.0.0.0`                | FastAPI host                      |
| `AGENCY_PORT`             | `8000`                   | FastAPI port                      |
| `AGENCY_MCP_TRANSPORT`    | `stdio`                  | `stdio` or `sse`                  |
| `AGENCY_MCP_PORT`         | `8765`                   | MCP SSE port                      |
| `AGENCY_AGENTS_FILE`      | `runtime/agents.jsonl`   | Tailed for agent updates          |
| `AGENCY_CHAT_FILE`        | `runtime/chat.jsonl`     | Tailed for chat updates           |

## Layout assumptions

The parsers expect the repo to look roughly like this — adjust globs in
`parsers.py` if yours differs.

```
tasks/{id}-{slug}/TASK.md          # frontmatter: id, slug, status, priority, owner, summary, uses_prompts, spawns_research
prompts/{slug}.md                  # frontmatter: slug, kind, relates_to_task, summary
research/{slug}/RESEARCH.md        # frontmatter: slug, phase, executes_prompt, summary
friction-logs/{task_id}/{ts}.md    # frontmatter: task, level, session, agent, duration, tokens
precommit/runs/{id}.json           # native JSON, schema mirrors precommitRuns shape
coherence/runs/{date}.md           # frontmatter: date, status, issues, deferred
runtime/agents.jsonl               # one JSON per line; appended live
runtime/chat.jsonl                 # one JSON per line; appended live
```
