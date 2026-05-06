---
type: note
status: active
slug: tooling-dynamic-readme-partition-linter-brief
summary: "Brief for prompt tooling-dynamic-readme-partition-linter — extracted from tasks/039-maintenance-spec-integration/subtasks/04-tooling-dynamic-readme-partition-linter.md per Task 041 (PR #70 review C.3 audit-graph repair)."
created: 2026-05-06
updated: 2026-05-06
---

# Brief — ST-4: `dynamic-readme-partition` — Operationalizes repo-maintenance-protocol-spec §3.1

## Raw User Request

> Extract the inlined Execution Brief from `tasks/039-maintenance-spec-integration/subtasks/04-tooling-dynamic-readme-partition-linter.md` (ST-4) into a registered `/prompts/<slug>/` artefact, restoring the `task_uses_prompts ↔ prompt_relates_to_task` audit-graph edge severed in PR #70 (review finding C.3).

## Target Audience

The dispatched executor for [Task 039 `maintenance-spec-integration`](../../tasks/039-maintenance-spec-integration/task.md), specifically subtask ST-4 (04-tooling-dynamic-readme-partition-linter.md). Default executor: **maintenance-agent**.

## Intended Model / Agent

Claude Code (or any agent that satisfies the executor declaration in the parent subtask file).

## Use-Case Context

This prompt drives subtask ST-4 of [Task maintenance-spec-integration](../../tasks/039-maintenance-spec-integration/task.md). The parent task's chain-level rationale lives in its `task.md`; this brief records only the subtask's local goal + inputs + acceptance + dependencies + effort, lifted verbatim from the subtask file at extraction time.

**Parallelism:** Phase A (parallel) — runs concurrently with ST-1, ST-2, ST-3, ST-5. No inter-dependencies.

**Insertion point:** `[opt]` WARN-tier — runs over operational-folder readmes only; advisory.

## Goal (from subtask)

Ship `tools/maintenance/dynamic-readme-partition.py` that scans operational-folder `readme.md` files and verifies the static/dynamic section partition: static sections (Purpose, Navigation, Assumptions Log) live above the `<!-- BEGIN DYNAMIC -->` marker; dynamic sections (Current State, Recent Activity, Open Blockers) live below. Closes the orphaning of `repo-maintenance-protocol-spec/output/SPEC.md §3.1`.

## Falsification (from subtask)

Wrong cut **iff** existing readmes have no markers and the linter retroactively breaks them. Mitigation: WARN-tier only; readmes lacking markers emit a one-time "consider partitioning" diagnostic, never an ERROR.

## Inputs (from subtask)

- `research/repo-maintenance-protocol-spec/output/SPEC.md` §3.1 (partition rule).
- All operational-folder `readme.md` (test corpus).
- `tools/fm/extract.py --section`.

## Acceptance Criteria (from subtask)

1. **Surface.** `python3 tools/maintenance/dynamic-readme-partition.py [<paths>]`.
2. **Heuristic.** Detect `<!-- BEGIN DYNAMIC -->` / `<!-- END DYNAMIC -->` marker pair; verify section-name allocation per the static/dynamic taxonomy.
3. **Diagnostic format.** `<relpath>::WARN:M.B.6:<missing-marker|misplaced-section>:<details>`.
4. **Tests.** `tests/maintenance/test_dynamic_readme_partition.py` covers: partitioned readme (pass), no-markers (advisory warn), section-in-wrong-half (warn).
5. **Integration.** WARN-tier `[opt]` in `tools/check-governance.sh`.

## Dependencies (from subtask)

None. Phase A.

## Estimated Effort (from subtask)

Medium (~120 LOC + 100 LOC tests).
