---
type: note
status: active
slug: tooling-assumption-log-substance-brief
summary: "Brief for prompt tooling-assumption-log-substance — extracted from tasks/032-agents-spec-integration/subtasks/04-tooling-assumption-log-substance.md per Task 041 (PR #70 review C.3 audit-graph repair)."
created: 2026-05-06
updated: 2026-05-06
---

# Brief — ST-4: `check-assumption-log` — FOLDERS.md F.3 / AGENTS.md §60-65 Enforcement

## Raw User Request

> Extract the inlined Execution Brief from `tasks/032-agents-spec-integration/subtasks/04-tooling-assumption-log-substance.md` (ST-4) into a registered `/prompts/<slug>/` artefact, restoring the `task_uses_prompts ↔ prompt_relates_to_task` audit-graph edge severed in PR #70 (review finding C.3).

## Target Audience

The dispatched executor for [Task 032 `agents-spec-integration`](../../tasks/032-agents-spec-integration/task.md), specifically subtask ST-4 (04-tooling-assumption-log-substance.md). Default executor: **main-agent**.

## Intended Model / Agent

Claude Code (or any agent that satisfies the executor declaration in the parent subtask file).

## Use-Case Context

This prompt drives subtask ST-4 of [Task agents-spec-integration](../../tasks/032-agents-spec-integration/task.md). The parent task's chain-level rationale lives in its `task.md`; this brief records only the subtask's local goal + inputs + acceptance + dependencies + effort, lifted verbatim from the subtask file at extraction time.

**Parallelism:** Phase A (parallel) — runs concurrently with ST-1, ST-2, ST-3. No inter-dependencies.

**Insertion point:** `[opt]` WARN-tier — invoked over operational `readme.md` files only; never gating.

## Goal (from subtask)

Ship `tools/check-assumption-log.py` that scans every operational-folder `readme.md` for an `## Assumptions Log` section and validates: (a) section exists when the parent task involved a non-trivial decision, (b) entries are not stale (currency check via `updated:` frontmatter), (c) entries are non-empty (substance check).

## Falsification (from subtask)

Wrong cut **iff** the substance check produces too many false positives on legitimate "no assumptions" cases. Mitigation: empty section with explicit "(none)" line is permitted; the linter only flags absent-or-truly-empty.

## Inputs (from subtask)

- [`FOLDERS.md`](../../../FOLDERS.md) §3 (Required Content for readme.md including Assumptions Log).
- [`AGENTS.md`](../../../AGENTS.md) §60–65 (assumption-logging rule).
- All `tasks/<NNN>-<slug>/readme.md` (test corpus).
- All `research/<slug>/readme.md` (test corpus).
- `tools/fm/extract.py` (section extraction).

## Acceptance Criteria (from subtask)

1. **Surface.** `python3 tools/check-assumption-log.py <folder>` exits 0 (pass) or 2 (WARN).
2. **Checks.**
   - Section heading `## Assumptions Log` present.
   - Section body non-empty OR contains exact line `(none)`.
   - If parent folder's frontmatter `updated` is more recent than the readme's, surface `STALE` warning.
3. **Tests.** `tests/test_assumption_log.py` covers all three checks.
4. **Integration.** `tools/check-governance.sh` runs WARN-tier on `tasks/<NNN>-<slug>/readme.md` and `research/<slug>/readme.md`.

## Dependencies (from subtask)

Reuses `tools/fm/extract.py` — gracefully degrade to grep if not available.

## Estimated Effort (from subtask)

Small (~80 LOC + 60 LOC tests).
