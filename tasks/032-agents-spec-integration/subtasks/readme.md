---
type: index
status: active
slug: task-032-subtasks-index
summary: "Subtask index for Task 032 — AGENTS.md spec integration. Phase A (parallel): 1 research head + 3 tooling. Phase B: 1 spec amendment depending on Phase A artefacts."
created: 2026-05-06
updated: 2026-05-06
---

# Task 032 — Subtask Index

Each subtask file is self-contained per the Task 019 convention (briefing + inputs + acceptance criteria + falsification clause + agent-prompt block).

## Phase A — Parallel (no inter-dependencies)

| ID | File | Recommended agent | Effort |
|---|---|---|---|
| ST-1 | [`01-research-adr-corpus-extraction.md`](./01-research-adr-corpus-extraction.md) | research-prompt-optimizer + deep-research | M |
| ST-2 | [`02-tooling-narrative-ontology-load-discipline.md`](./02-tooling-narrative-ontology-load-discipline.md) | python-expert | S |
| ST-3 | [`03-tooling-rfc2119-polarity-audit.md`](./03-tooling-rfc2119-polarity-audit.md) | python-expert | M |
| ST-4 | [`04-tooling-assumption-log-substance.md`](./04-tooling-assumption-log-substance.md) | python-expert | S |

## Phase B — Sequential (after Phase A)

| ID | File | Depends on | Recommended agent | Effort |
|---|---|---|---|---|
| ST-5 | [`05-spec-amendment-agents-md.md` (briefing pending — author before dispatch) | ST-1, ST-2, ST-3, ST-4 | technical-writer | S |
