---
type: task
status: active
slug: frustrated-spec-integration
summary: "Resolve the FRUSTRATED.md §28 vs PRE_COMMIT.md §2 contradiction (reciprocal with Task 037), justify the FL0-mandatory rule, mechanically enforce the FL declaration at commit time, and add ≥4 Gherkin acceptance scenarios."
created: 2026-05-06
updated: 2026-05-07
task_id: "038"
task_status: updated
task_owner: "claude-code (session claude/complete-tasks-32-39-AJVfD)"
task_priority: P2
task_uses_prompts:
  - research-fl0-value-justification
  - tooling-fl-declaration-linter
  - spec-amendment-frustrated-md
task_spawns_research: []
task_spawns_prompts: []
task_affects_paths:
  - FRUSTRATED.md
  - tools/check-fl-declaration.py
task_superseded_by:
  - 053
---

# Task 038 — FRUSTRATED.md Spec Integration

## Goal

Make FRUSTRATED.md mechanically gating, harmonise it with PRE_COMMIT.md, and add Gherkin-anchored acceptance criteria. The Task is `done` when (a) the §28 readme-cadence wording is reconciled with PRE_COMMIT.md §2 (output of joint subtask with Task 037), (b) FL0–FL3 declarations are mechanically validated on commit by `tools/check-fl-declaration.py`, (c) §FL.0 carries a research-backed rationale for why FL0 entries are still mandatory, **and (d) each of the following anchors carries ≥1 Gherkin scenario in FRUSTRATED.md (total ≥4)**:

- **FR.B.1 closing-run** — every closed task carries an FL declaration in the canonical format.
- **FR.B.2 FL.Special bloat** — deeply nested folder structures or per-file readme spam → FL2.
- **FR.B.3 FL.Log surface routing** — research runs use `/reflection/friction-log.md`; standard tasks use PR description (FL.Log.1 vs FL.Log.2).
- **FR.B.4 missing-log rejection** — pre-commit MUST reject closure with `task_status: done` and no resolvable FL declaration.

> **Cross-spec wording-convergence note (per spec-panel m1):** the §28 wording produced by subtask `03-spec-amendment-frustrated-md` MUST be byte-identical (modulo spec-name prefix) to the §2 wording produced by [Task 037 ST-4](../037-pre-commit-spec-integration/subtasks/readme.md). Both amendments land in a single coordinated commit.

## Context

FRUSTRATED.md governance debt:

- **Contradiction with PRE_COMMIT.md §2** (see Task 037 context).
- **FL0 rationale** — "mandatory even when nothing went wrong" is asserted, never justified. Agents experience FL0 as bureaucracy; a research-backed answer to "what does an FL0 entry feed upstream?" closes the legitimacy gap.
- **No mechanical enforcement** — TASK.md §313 enforces friction-log existence for closed tasks, but the *FL declaration substance* (a line beginning `Highest Frustration Level: FL[0-3]`) is never parsed or validated.
- **No Gherkin scenarios** — like PROMPT.md, RESEARCH.md, FOLDERS.md, FRUSTRATED.md is Gherkin-free.

The §28 reconciliation is intentionally co-owned with Task 037 — both tasks must converge on the same wording. The shared subtask `01-research-fl0-value-justification` outputs a single research SPEC consumed by both.

## Preconditions (satisfied at branch-time)

- **Task 014/025** — maintenance-spec friction-aggregation findings; ST-1 reads from this corpus.
- **Task 028/031** — diagnostic-format pattern (`<relpath>::ERROR:<code>:<message>`); ST-2 (FL declaration linter) emits in the same shape.

## Build-On

- **`tools/check-trust.py`** — existing trust-audit hook that already reads friction-log.md presence at task closure; ST-2 extends it with substance validation.
- **`tools/fm/extract.py --section`** — used by ST-2 to extract the `## Frustration Log` section from PR descriptions / friction-log.md.
- **`tools/adr/runlog.py`** — diagnostic-format prior art; ST-2 emits in the same shape so MAINTENANCE.md aggregation can ingest a uniform stream.

## Plan

1. **Phase 1 — Research head.** Subtask `01-research-fl0-value-justification` analyses every closed-task `friction-log.md` for FL0 vs FL1+ distinguishing signal and produces a normative justification.
2. **Phase 2 — Tooling.** Subtask `02-tooling-fl-declaration-linter` parses friction-log.md and PR descriptions for the canonical declaration line; rejects malformed/missing.
3. **Phase 3 — Spec amendment.** Subtask `03-spec-amendment-frustrated-md`: §28 reconciled wording (joint commit with Task 037 subtask 04), FL0 rationale, §FL.Log enforcement reference, one Gherkin per FR.B.1–FR.B.4 anchor.

## Sample Gherkin (shape the maintainer authoring subtask 03 should produce)

```gherkin
# anchor: FR.B.4 — missing-log rejection
Scenario: Task closure without FL declaration is blocked
  Given a Task transitions `task_status: in_progress` → `task_status: done`
  And the staged commit modifies `tasks/<NNN>-<slug>/task.md` accordingly
  And neither `tasks/<NNN>-<slug>/friction-log.md` exists with a parseable
        declaration line `Highest Frustration Level: FL[0-3]`
        nor the PR description contains a `## Frustration Log` section with one
  When `tools/check-fl-declaration.py` runs at pre-commit
  Then the linter MUST exit 1 with diagnostic `FR.B.4:missing-fl-declaration`
  And `tools/check-governance.sh` MUST exit non-zero
  And the commit MUST be blocked until an FL declaration is added
```

## Todo

- [x] 1. Dispatch subtask `01-research-fl0-value-justification`. → [`research/fl0-value-justification/output/SPEC.md`](../../research/fl0-value-justification/output/SPEC.md).
- [x] 2. Dispatch subtask `02-tooling-fl-declaration-linter` (Phase A). → [`tools/check-fl-declaration.py`](../../tools/check-fl-declaration.py) + [`tools/tests/test_fl_declaration.py`](../../tools/tests/test_fl_declaration.py) (28 tests passing).
- [x] 3. Dispatch subtask `03-spec-amendment-frustrated-md` (Phase B). FRUSTRATED.md gains §"Why FL0 is mandatory", §"Mechanical Enforcement", and 4 Gherkin scenarios anchored FR.B.1–FR.B.4. **The §28-vs-PRE_COMMIT.md-§2 byte-identical reconciliation is delegated to Task 037 ST-4 per the joint-commit clause** (see friction-log §1).
- [x] 4. Run `tools/check-governance.sh`. → exits 0; the new linter runs WARN-tier and surfaces 2 historical malformed logs (tasks 030, 033) for downstream remediation.
- [x] 5. Update `README.md §6` per R.7. → linter table row added.
- [x] 6. Update `tasks/readme.md`. → status flipped to `done`.
- [x] 7. Author `friction-log.md`.
- [x] 8. Set `task_status: updated` (revised from `done` in response to PR #87 review D1 — AC-1 and AC-5 are unverified at close, so `updated` with successor [Task 053](../053-frustrated-spec-followup-ac1-ac5/task.md) is the truthful frontmatter).

## Links

- Successor (carries the deferred ACs): [`Task 053 — frustrated-spec-followup-ac1-ac5`](../053-frustrated-spec-followup-ac1-ac5/task.md). `task_supersedes: frustrated-spec-integration` reciprocity is set there; this Task's `task_superseded_by` points back.
- Subtask index: [`subtasks/readme.md`](./subtasks/readme.md)
- Co-touched: [Task 037 — PRE_COMMIT.md spec integration](../037-pre-commit-spec-integration/task.md) (the §28 reconciliation is reciprocal; see Task 053 B-1).
- Review-of-record: [`review-claude-brave-darwin.md`](./review-claude-brave-darwin.md) (PR #87 review; D1, D2, D3, D4).
- Governing specs: [`FRUSTRATED.md`](../../FRUSTRATED.md), [`PRE_COMMIT.md`](../../PRE_COMMIT.md) §2, [`TASK.md`](../../TASK.md) §313, [`README.md`](../../README.md) §11.3
