---
type: spec
status: active
slug: codex-md
summary: "Codex entry-point instructions for this repository: mandatory bootstrap, routing to canonical specs, and close-out obligations."
created: 2026-05-12
updated: 2026-05-12
---

# CODEX.md — Codex Agent Instructions

This file is the Codex entry point for the **`agency`** repository. It routes to canonical governance specs and does not supersede them. When this file and a root spec diverge, the root spec is authoritative.

Primary specs to follow:

- [AGENTS.md](./AGENTS.md) — global requirements and closing-run contract.
- [TASK.md](./TASK.md), [PROMPT.md](./PROMPT.md), [RESEARCH.md](./RESEARCH.md), [SKILLS.md](./SKILLS.md) — lifecycle routing and folder contracts.
- [FOLDERS.md](./FOLDERS.md), [PRE_COMMIT.md](./PRE_COMMIT.md), [FRUSTRATED.md](./FRUSTRATED.md), [MAINTENANCE.md](./MAINTENANCE.md) — structure, checks, feedback loop, and maintenance boundaries.
- [decisions/readme.md](./decisions/readme.md) — ADR governance path for architecture-level convention changes.

## 1. Mandatory bootstrap (every session)

Before reading, editing, or validating repository files, run:

```bash
./install.sh
tools/check-governance.sh
```

Rules:

1. `install.sh` is idempotent; do not skip it.
2. `tools/check-governance.sh` gates work. If it exits non-zero, stop and report diagnostics.
3. Do not continue on top of a broken governance state.

## 2. Route the request before writing

Choose one operating path and follow the corresponding root spec:

- Task orchestration → `/tasks/` + [TASK.md](./TASK.md)
- Prompt authoring → `/prompts/` + [PROMPT.md](./PROMPT.md)
- Research execution/synthesis → `/research/` + [RESEARCH.md](./RESEARCH.md)
- Skill authoring/maintenance → `/skills/` + [SKILLS.md](./SKILLS.md)

Separation of concerns is mandatory: Tasks link to prompts; prompts execute into research; research findings that require new work become new prompts/tasks.

## 3. Frontmatter, readmes, and structure

Operational files MUST satisfy layered frontmatter requirements (L1 + namespace L2) and directory contracts. Use repository tooling and follow:

- [AGENTS.md § Frontmatter Ontology (Summary)](./AGENTS.md#frontmatter-ontology-summary) as the root-level ontology summary, with [TASK.md §3](./TASK.md) as the canonical operational key matrix.
- [FOLDERS.md](./FOLDERS.md) for mandatory `readme.md` coverage and assumptions logging.
- [PRE_COMMIT.md](./PRE_COMMIT.md) for the full check matrix executed by `tools/check-governance.sh`.

## 4. Close-out contract (all Codex sessions)

Before declaring completion, satisfy the four-step closing procedure in [AGENTS.md § Closing Run Procedure](./AGENTS.md#closing-run-procedure):

1. Record Frustration Level (FL0–FL3), including FL0 sessions.
2. Sync `tasks/readme.md` if task statuses changed.
3. Ensure `tools/check-governance.sh` passes for final state.
4. Open a **draft** PR (or confirm an existing PR covers branch commits) via `make_pr`; include required Task-slug and FL references.

Re-invocation of step 4 on a branch with an open PR MUST be treated as a no-op.
