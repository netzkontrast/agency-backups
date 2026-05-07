---
type: note
status: active
slug: fix-ft1-scope-drift-brief
summary: "Brief for prompt fix-ft1-scope-drift — investigate and resolve the spec/implementation drift on F.T.1: TASK.md §7.3 documents enforcement scope as `task_status ∈ {done, updated, abandoned}` only, but `tools/fm/validate.py --type-check` enforces `task_uses_prompts` / `task_spawns_prompts` resolution unconditionally. Decide which side wins and align the other."
created: 2026-05-07
updated: 2026-05-07
---

# Brief — F.T.1 Spec/Implementation Scope Drift

## Raw User Request

> Surfaced during PR #81 review (R-2, MODERATE) and Task 048 scaffolding: the F.T.1 dangling-reference linter rejects pre-declared prompt slugs on `task_status: open` tasks even though TASK.md §7.3 explicitly says enforcement is closure-only.

## Target Audience

Default executor: **main-agent**. The work is a small spec-or-tooling change with a research preamble.

## Intended Model / Agent

Claude Code (or any agent that can read the TASK.md prose, the validate.py source, and the prior-art ADR / friction-log evidence and decide between two clean alignments).

## Use-Case Context

PR #81 introduced [Task 048](../../tasks/048-task-tooling-impl-spec/) which would have benefited from pre-declaring three planned prompt slugs in `task_uses_prompts` / `task_spawns_prompts` so the audit graph was correct from the moment the task entered the repo. The F.T.1 linter rejected that — the task was authored with empty prompt-list fields and a workaround note in the readme Assumptions Log. PR #81 review R-2 escalated this from "workaround in one task readme" to "candidate Task-044 finding deserving its own audit-graph artefact" per AGENTS.md AG.2.1 + PROMPT.md §1(2).

## Goal

Resolve the drift by either (a) loosening `tools/fm/validate.py --type-check` to honour the documented closure-only enforcement scope for `task_uses_prompts` / `task_spawns_prompts`, or (b) tightening TASK.md §7.3 prose to match the linter's actual behaviour. Whichever wins, both surfaces MUST agree.

## Falsification

The chosen resolution is the **wrong cut** iff:

1. The "loosen linter" path is taken but a regression follow-up Task 048-style scenario (planning a Task that pre-declares prompts) still fails the linter on `task_status: open`.
2. The "tighten prose" path is taken but the existing convention of pre-declaring planned prompts (recorded in Task 033's task.md until the F.T.1 rejection was discovered) is left without a documented alternative pattern (e.g. `task_planned_prompts` advisory list, comment in template).
3. The decision is made without reading the original commit that introduced F.T.1 (Task 019 ST-5 per the validate.py docstring) — the commit message is the canonical source for which scope was intended.

## Inputs

- [`TASK.md`](../../TASK.md) §7.3 — current prose: "tools/lint-linkage.py only runs this check when task_status ∈ {done, updated, abandoned}"; §7.0 row §7.3.
- [`tools/fm/validate.py`](../../tools/fm/validate.py) `type_check()` — the implementation. Note `_LIST_REF_FIELDS` includes `task_uses_prompts`, `task_spawns_prompts`, `task_blocked_by`, etc., all enforced unconditionally.
- [`tasks/048-task-tooling-impl-spec/readme.md`](../../tasks/048-task-tooling-impl-spec/readme.md) Assumptions Log — first explicit documentation of the drift.
- [`tasks/033-task-spec-integration/friction-log.md`](../../tasks/033-task-spec-integration/friction-log.md) Notes — the original surface where the workaround was applied.
- [`maintenance/pr-81-review.md`](../../maintenance/pr-81-review.md) §R-2 — review-finding rationale.
- The Task 019 ST-5 commit history for `tools/fm/validate.py` (find via `git log --follow tools/fm/validate.py | grep "ST-5\|F.T.1\|type-check"`).

## Acceptance Criteria

1. Decision recorded in a short ADR or research note (≤ 2 pages) at `decisions/<NNNN>-ft1-enforcement-scope.md` OR `research/ft1-enforcement-scope-decision/output/SPEC.md`. The choice between ADR vs. research is itself part of the decision (an ADR is appropriate if the decision touches the validator's contract; a research note is appropriate if the decision is an implementation-detail tightening).
2. Whichever side wins, both `TASK.md §7.3` AND `tools/fm/validate.py` are updated in the same commit so they agree.
3. If linter-side: a new test in `tools/tests/fm/test_validate.py` proves pre-declared prompt slugs on `task_status: open` are accepted.
4. If prose-side: the `task_uses_prompts` pre-declaration pattern is migrated to a clearly-named alternative (e.g. `## Planned Prompts` body section, or a comment block in `templates/task.md`).
5. `tools/check-governance.sh` exits 0 (or remaining ERRORs are pre-existing per the Task 032 / Task 033 precedent).
6. Task 048's `task_uses_prompts` field can carry the three planned prompt slugs without F.T.1 rejection (this is the integration test for the chosen path).

## Dependencies

None. Independent investigation. SHOULD complete before Task 048 ST-3 begins synthesis (so the synthesis SPEC's tooling proposals don't bake in the wrong behaviour).

## Estimated Effort

Small (~2 hours: 1h investigation + 1h implementation + tests).
