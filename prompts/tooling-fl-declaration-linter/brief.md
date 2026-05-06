---
type: brief
status: active
slug: tooling-fl-declaration-linter-brief
summary: "Brief for prompt tooling-fl-declaration-linter — extracted from tasks/038-frustrated-spec-integration/subtasks/02-tooling-fl-declaration-linter.md per Task 041 (PR #70 review C.3 audit-graph repair)."
created: 2026-05-06
updated: 2026-05-06
---

# Brief — ST-2: `check-fl-declaration` — Mechanical FL-Declaration Gate

## Raw User Request

> Extract the inlined Execution Brief from `tasks/038-frustrated-spec-integration/subtasks/02-tooling-fl-declaration-linter.md` (ST-2) into a registered `/prompts/<slug>/` artefact, restoring the `task_uses_prompts ↔ prompt_relates_to_task` audit-graph edge severed in PR #70 (review finding C.3).

## Target Audience

The dispatched executor for [Task 038 `frustrated-spec-integration`](../../tasks/038-frustrated-spec-integration/task.md), specifically subtask ST-2 (02-tooling-fl-declaration-linter.md). Default executor: **main-agent**.

## Intended Model / Agent

Claude Code (or any agent that satisfies the executor declaration in the parent subtask file).

## Use-Case Context

This prompt drives subtask ST-2 of [Task frustrated-spec-integration](../../tasks/038-frustrated-spec-integration/task.md). The parent task's chain-level rationale lives in its `task.md`; this brief records only the subtask's local goal + inputs + acceptance + dependencies + effort, lifted verbatim from the subtask file at extraction time.

**Parallelism:** Phase A (parallel-grouped, soft-blocked) — runs alongside ST-1 but soft-depends on ST-1 SPEC §2 (variant-form set). Phase A may ship with strict canonical form + upgrade post-ST-1.

**Insertion point:** `[trust]` step — extends `tools/check-trust.py` rather than introducing a parallel pipeline.

## Goal (from subtask)

Ship `tools/check-fl-declaration.py` that parses `friction-log.md` (research) and PR-description `## Frustration Log` sections (standard), validates the presence of a canonical `Highest Frustration Level: FL[0-3]` line, and rejects task closure when the declaration is missing or malformed. Closes the FRUSTRATED.md enforcement gap.

## Falsification (from subtask)

Wrong cut **iff** the canonical-format regex is too strict and rejects legitimate variations (`Final FL: FL2`, `FL2 declared`). Mitigation: ST-1's research output enumerates the variant forms found in the existing corpus; the linter accepts that bounded set.

## Inputs (from subtask)

- ST-1 output: `research/fl0-value-justification/output/SPEC.md` §2 (variant forms in corpus).
- `FRUSTRATED.md` (FL.Log.1, FL.Log.2 — both surfaces).
- `TASK.md` §313 (existence enforcement; ST-2 adds substance enforcement).
- `tools/check-trust.py` (the existing extension point).
- `tools/adr/runlog.py` (diagnostic format prior art).

## Acceptance Criteria (from subtask)

1. **Surface.** `python3 tools/check-fl-declaration.py <task-folder-or-pr-body>` exits 0/1.
2. **Heuristic.** Parse `friction-log.md` first; fall back to PR-description `## Frustration Log` section; reject only if neither surface has a parseable declaration.
3. **Diagnostic format.** `<relpath>::ERROR:FR.B.4:<missing|malformed>:<details>`.
4. **Tests.** `tests/test_fl_declaration.py` covers: clean FL0, clean FL2, missing log, malformed value, both surfaces present (no warn).
5. **Integration.** Hooked into `tools/check-trust.py` for tasks transitioning to `done`.

## Dependencies (from subtask)

ST-1 SHOULD land first (provides variant-form set). If absent, ST-2 ships with the strict canonical form only and is upgraded post-ST-1.

## Estimated Effort (from subtask)

Small (~80 LOC + 80 LOC tests).
