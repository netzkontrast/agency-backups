---
type: task
status: active
slug: reconcile-closed-task-linkage
summary: "Found by coherence check 2026-05-04: Tasks 002 and 003-analyze closed with unresolved linkage drift (missing friction-logs, prompts confused with research, broken reciprocity, namespaced research path)."
created: 2026-05-04
updated: 2026-05-04
task_id: "007"
task_status: done
task_owner: "claude-code"
task_priority: P1
task_uses_prompts: []
task_spawns_research: []
task_affects_paths:
  - tasks/002-token-efficiency-tool-suite/
  - tasks/003-analyze-skillmd-novel-authoring/
  - prompts/budget-enforcer-fallback/prompt.md
  - prompts/context-pruner-differentiation/prompt.md
  - prompts/cross-skill-context-poisoning/prompt.md
  - prompts/mega-context-limit-management/prompt.md
  - prompts/subjective-quality-evaluation/prompt.md
  - TASK.md
---

# Task 007 — Reconcile Closed-Task Linkage Drift

## Goal

The pre-commit governance check (`tools/check-governance.sh`) reports 13 linkage errors and 2 trust-audit errors traceable to two closed tasks (002 and 003-analyze). Restore mechanical conformance so `check-governance.sh` exits zero, OR document a justified waiver that the linters honor.

## Background — What the Coherence Check Found

1. **Missing friction-logs on closed tasks** (TASK.md §7.7, Spec-L.3.1):
   - `tasks/002-token-efficiency-tool-suite/friction-log.md` does not exist.
   - `tasks/003-analyze-skillmd-novel-authoring/friction-log.md` does not exist.

2. **`task_spawns_research` references that do not resolve to research workspaces** (TASK.md §7.3):
   - Task 003 lists `mega-context-limit-management`, `cross-skill-context-poisoning`, `subjective-quality-evaluation` — but those slugs exist as `/prompts/<slug>/` (follow-up prompts), not as `/research/<slug>/` workspaces. The task confused *prompts that need to be executed* with *research workspaces that have been produced*.

3. **Reciprocity breakage on `prompt_relates_to_task`** (FOLDERS.md §6):
   - Task 002 does not list `budget-enforcer-fallback` or `context-pruner-differentiation` in `task_uses_prompts`, although both prompts back-link to it.
   - Task 003 does not list `cross-skill-context-poisoning`, `mega-context-limit-management`, or `subjective-quality-evaluation`, although all three back-link to it.
   - The reciprocity rule conflates two relations: *prompts a Task executed* (input) and *prompts a Task produced* (output). The current schema only has `task_uses_prompts`. Follow-up prompts have no clean home.

4. **`prompt_spawned_from_research` resolution failure** (PROMPT.md §6.5):
   - Three prompts reference research slug `github-skillmd-novel-authoring-de-en`. The workspace exists at `research/gemini/github-skillmd-novel-authoring-de-en/` but the linter searches only the top-level `research/` namespace. The validator does not understand the `gemini/` provider sub-namespace introduced by external research ingestion.

## Plan

1. Decide reconciliation strategy per group (the linker MAY accept any consistent option):
   - **A. Re-open and finish** — set `task_status: in_progress` on Tasks 002 and 003, perform the missing work (write friction-logs; create or remove research workspaces; correct linkages), close again.
   - **B. Schema extension** — add a `task_spawns_prompts` (and possibly `task_spawns_research_pending`) L2 key to `TASK.md §3.3` and the validator, then fix the offending tasks and prompts to use it.
   - **C. Path-resolution fix** — extend `tools/lint-linkage.py` to accept `research/<provider>/<slug>/` namespaces (e.g. `gemini/`).
   - **D. Mark stale prompts** — set `status: archived` (or move to a holding folder) for follow-up prompts whose research will not be executed.
2. Apply the chosen strategy. Update `TASK.md` and the linters together so the schema and the enforcement stay in lockstep.
3. Author the missing `friction-log.md` files (FL declaration mandatory, even if FL0).
4. Run `tools/check-governance.sh` until it exits zero, or until every remaining error has a documented waiver entry per the project's waiver convention.

## Todo

- [x] Choose reconciliation strategy (A/B/C/D or mix) and record the decision in `notes.md`. (Strategy A + C; details in `notes.md`.)
- [x] ~~If strategy B: extend `TASK.md §3.3` with `task_spawns_prompts` and update `tools/lint-linkage.py`.~~ Strategy B not chosen.
- [x] If strategy C: extend `tools/lint-linkage.py` to resolve `research/<provider>/<slug>/`. (`research_slug_resolves()` added.)
- [x] Author `tasks/002-token-efficiency-tool-suite/friction-log.md`. (Extracted from inline `## Frustration Log` in `task.md`; FL1.)
- [x] Author `tasks/003-analyze-skillmd-novel-authoring/friction-log.md`. (Reconstructed FL1 in retrospect.)
- [x] Reconcile `task_spawns_research` in `tasks/003-analyze-skillmd-novel-authoring/task.md` so every listed slug resolves OR is moved to a different field. (Emptied — the slugs were follow-up *prompts*, not research.)
- [x] Reconcile `task_uses_prompts` in `tasks/002-token-efficiency-tool-suite/task.md` and `tasks/003-analyze-skillmd-novel-authoring/task.md`. (No additions needed — `prompt_relates_to_task` removed from the 5 follow-up prompts that had no using-task; the spec was clarified in PROMPT.md §6.6 to state that follow-ups not yet adopted MUST omit the field.)
- [x] Run `tools/check-governance.sh` and confirm zero errors.

## Links

- Found by: coherence check run `maintenance/run-log.md` entry 2026-05-04 (second).
- Related governance: [TASK.md](../../TASK.md) §3.3, §7.3, §7.7; [PROMPT.md](../../PROMPT.md) §6.5, §6.6; [FOLDERS.md](../../FOLDERS.md) §6.
- Related research workspace (mis-linked): [research/gemini/github-skillmd-novel-authoring-de-en/](../../research/gemini/github-skillmd-novel-authoring-de-en/).
