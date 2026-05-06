---
type: brief
status: active
slug: tooling-clean-working-directory-linter-brief
summary: "Brief for prompt tooling-clean-working-directory-linter — extracted from tasks/037-pre-commit-spec-integration/subtasks/02-tooling-clean-working-directory-linter.md per Task 041 (PR #70 review C.3 audit-graph repair)."
created: 2026-05-06
updated: 2026-05-06
---

# Brief — ST-2: `check-clean-working-directory` — Closes PRE_COMMIT.md PC.1.1 Gap

## Raw User Request

> Extract the inlined Execution Brief from `tasks/037-pre-commit-spec-integration/subtasks/02-tooling-clean-working-directory-linter.md` (ST-2) into a registered `/prompts/<slug>/` artefact, restoring the `task_uses_prompts ↔ prompt_relates_to_task` audit-graph edge severed in PR #70 (review finding C.3).

## Target Audience

The dispatched executor for [Task 037 `pre-commit-spec-integration`](../../tasks/037-pre-commit-spec-integration/task.md), specifically subtask ST-2 (02-tooling-clean-working-directory-linter.md). Default executor: **main-agent**.

## Intended Model / Agent

Claude Code (or any agent that satisfies the executor declaration in the parent subtask file).

## Use-Case Context

This prompt drives subtask ST-2 of [Task pre-commit-spec-integration](../../tasks/037-pre-commit-spec-integration/task.md). The parent task's chain-level rationale lives in its `task.md`; this brief records only the subtask's local goal + inputs + acceptance + dependencies + effort, lifted verbatim from the subtask file at extraction time.

**Parallelism:** Phase A (parallel) — runs concurrently with ST-1, ST-3. No inter-dependencies.

**Insertion point:** `[2/5]` directory-structure linter extension.

## Goal (from subtask)

Ship `tools/check-clean-working-directory.py` that scans staged paths for `.py`/`.sh` scratchpads outside designated tool/test directories. Closes PC.1.1 (currently relies on agent discipline). Exempts `/decisions/`, `/tools/`, `/tests/`, `/skills/<slug>/scripts/`, `/maintenance/scripts/` per the §8 FOLDERS.md exemption pattern.

## Falsification (from subtask)

Wrong cut **iff** legitimate `.py` files (e.g., a one-off migration script kept in a task's notes for audit) trigger ERROR. Mitigation: the linter accepts a per-task `.script-allowlist` file with rationale, and emits a suggestion to relocate `.py` to `/tools/<slug>/` rather than block.

## Inputs (from subtask)

- `PRE_COMMIT.md` PC.1.1.
- `FOLDERS.md` §8 exemption table.
- `tools/fm/_core.py`.

## Acceptance Criteria (from subtask)

1. **Surface.** `python3 tools/check-clean-working-directory.py [<paths>]`.
2. **Heuristic.** Flag `.py`/`.sh`/`.log` outside the §8-exempt set; honour `.script-allowlist`.
3. **Diagnostic format.** `<relpath>::WARN:PC.1.1:script-scratchpad`.
4. **Tests.** `tests/test_clean_working_directory.py` covers: clean tree, scratchpad-in-research/workspace (warn), scratchpad-in-/tools (pass), allowlisted (pass).
5. **Integration.** ERROR-tier in step `[2/5]` of `tools/check-governance.sh`.

## Dependencies (from subtask)

None. Phase A.

## Estimated Effort (from subtask)

Small (~80 LOC + 60 LOC tests).
