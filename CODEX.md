---
type: spec
status: active
slug: codex-md
summary: "Instructions for Codex agents operating in this repository; routes to AGENTS.md and all binding governance specs."
created: 2026-05-12
updated: 2026-05-12
---

# CODEX.md — Codex Agent Instructions

This file is the Codex entry point for the **`agency`** repository. It does **not** supersede any governance specification. The binding authority is [AGENTS.md](./AGENTS.md), followed by the root governance specs ([TASK.md](./TASK.md), [PROMPT.md](./PROMPT.md), [RESEARCH.md](./RESEARCH.md), [SKILLS.md](./SKILLS.md), [FOLDERS.md](./FOLDERS.md), [PRE_COMMIT.md](./PRE_COMMIT.md), [FRUSTRATED.md](./FRUSTRATED.md), [MAINTENANCE.md](./MAINTENANCE.md)).

If this file diverges from any root spec, the root spec wins and this file MUST be reconciled in the same change set.

## 1) Mandatory startup for every Codex session

Run these commands from repo root before reading or writing repository files:

```bash
./install.sh
tools/check-governance.sh
```

- `install.sh` is idempotent and installs required tooling from `tools/requirements.txt`.
- If `tools/check-governance.sh` exits non-zero, stop and surface the diagnostics; do not continue work on top of a failing governance state.

## 2) Routing rule: choose the right spec first

Before editing anything, route the request to the proper operating model:

- Task orchestration work → [TASK.md](./TASK.md) and `/tasks/`
- Prompt authoring work → [PROMPT.md](./PROMPT.md) and `/prompts/`
- Research execution/evidence work → [RESEARCH.md](./RESEARCH.md) and `/research/`
- Skill authoring/modification work → [SKILLS.md](./SKILLS.md) and `/skills/`

Separation of concerns is mandatory: Tasks link to prompts, prompts execute into research, and discovered follow-up questions become new prompts.

## 3) Frontmatter and structure are non-negotiable

Operational files MUST carry valid L1+L2 frontmatter and follow the layered schema defined in [TASK.md §3](./TASK.md). Use repository tooling for safe metadata edits and honor readme/index sync rules in [FOLDERS.md](./FOLDERS.md).

## 4) Session close contract

Before declaring completion, follow [AGENTS.md § Closing Run Procedure](./AGENTS.md#closing-run-procedure):

1. Friction log captured (FL0–FL3, including FL0 runs).
2. `tasks/readme.md` synced if any task statuses changed.
3. `tools/check-governance.sh` green on final commit.
4. Pull request opened (or existing PR confirmed as covering the branch commits), with required Task-slug and FL references.

For Codex usage in this repo, step 4 is satisfied via the platform PR primitive used by this runtime.
