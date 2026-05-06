---
type: prompt
status: active
slug: research-staleness-decision-formalization
summary: "ST-2: Research — Staleness Decision Formalization (cross-link)"
created: 2026-05-06
updated: 2026-05-06
prompt_kind: task-spec
prompt_framework: RISEN+ReAct
prompt_target_agent: "Claude Code"
prompt_relates_to_task: maintenance-spec-integration
prompt_spawned_from_research: ""
---

# ST-2: Research — Staleness Decision Formalization (cross-link) — Task-Spec Prompt

## Framework

RISEN+ReAct. The prompt declares the framework in frontmatter (`prompt_framework: RISEN+ReAct`) and restates it here for `fm-validate` header conformance. The R/I/S/E sections below carry the canonical roles; a final **Constraints** section groups normative scope/failure rules per repo convention.

## R — Role

You are the **main-agent** dispatched to execute subtask ST-2 of [Task maintenance-spec-integration](../../tasks/039-maintenance-spec-integration/task.md). Your remit is bounded by the Acceptance Criteria in [`brief.md`](./brief.md); you MUST NOT expand scope beyond those criteria without surfacing the divergence in `friction-log.md`.

**Parallelism:** Phase A (parallel) — **Cross-Task shared with Task 033 ST-2** — see that file for the canonical briefing; this is a cross-link stub. Whichever Task dispatches first authors the SPEC; the second consumes via filesystem detection (`test -f`)..

## I — Input

- `tasks/039-maintenance-spec-integration/subtasks/02-research-staleness-decision-formalization.md` — the parent subtask file (lifted verbatim into this prompt's `brief.md`).
- `tasks/039-maintenance-spec-integration/task.md` — parent task chain-level context.

## S — Steps

1. Run `tools/check-governance.sh` and resolve every ERROR before committing.
2. Author or update `tasks/039-maintenance-spec-integration/friction-log.md` (or note that none is required for this subtask) and commit per the parent task's commit-message convention.
3. Verify all parent-task `Acceptance Criteria` referenced by this subtask still hold.

## E — Expectations

- All Acceptance Criteria from the parent subtask brief are satisfied.
- `tools/check-governance.sh` exits 0 on the produced commit.
- Commit message follows the parent task's convention; the commit cites `Task 039 ST-2` in its trailer.

## Constraints

- Dependency: Either Task 033 ST-2 OR Task 039 ST-2 — exactly one runs the actual research. The other reads the output.
- MUST NOT trigger the subtask's Falsification clause: If both Tasks dispatch this subtask in parallel without coordination, the second one MUST detect the existing output via a `test -f` check and abort with a "stub-already-fulfilled" message rather than re-running.
- MUST NOT inline this prompt's Goal/Inputs/Acceptance back into the subtask file — the subtask body is now a thin pointer per Task 041.
- MUST run `tools/check-governance.sh` before pushing; a non-zero exit MUST block the push.
- SHOULD cite the parent task's `task_id` in any commit-message trailer for traceability.
