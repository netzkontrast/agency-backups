---
type: note
status: active
slug: task-061-friction-log
summary: "Friction log for Task 061 — governance-integration-test-scaffold. FL1: §7.10 reciprocity check is not yet wired into the ontology so the mutator downgrades to F.T.1 dangling. Otherwise FL0."
created: 2026-05-13
updated: 2026-05-13
---

# Task 061 — Friction Log

**Highest Frustration Level: FL1**

## Context

Built `tests/integration/{conftest.py,test_governance_e2e.py,fixtures/seed/}`
plus an `INTEGRATION=1`-gated row in `tools/check-governance.sh` that runs
`pytest tests/integration/`. Twelve mutator-tests cover TASK.md §7.0 rows
§7.1–§7.11 and §8.1; §7.5 (path containment) has no mechanical check and is
explicitly skipped.

## Friction entries

### FL1.1 — §7.10 supersession reciprocity has no ontology rule

**What happened.** TASK.md §7.0 row §7.10 maps the supersession-reciprocity
invariant to `fm-validate --type-check` and the diagnostic code `F.T.2`.
Inspection of `maintenance/schemas/header-ontology.json:reciprocity.rules`
showed only one rule defined: `task_uses_prompts` ↔
`prompt_relates_to_task` (the §7.3 / §7.4 mechanism). The
`task_supersedes` ↔ `task_superseded_by` pair documented in TASK.md §7.10
is not in the rules array, so a mutator that adds a non-reciprocating
sibling Task does not surface F.T.2 — fm-validate exits 0.

**Resolution in scope of Task 061.** The §7.10 mutator targets the closest
mechanical surface still backed by the linter: a dangling `task_supersedes`
slug, which surfaces `F.T.1`. The test asserts `F.T.1` rather than `F.T.2`
and the suite's `readme.md` row-coverage table notes the downgrade.

**Recommended follow-up.** File a sibling Task to add the
`task_supersedes` ↔ `task_superseded_by` reciprocity rule to
`maintenance/schemas/header-ontology.json` (under `reciprocity.rules`),
then flip the §7.10 mutator back to a non-reciprocating sibling Task and
the expected token from `F.T.1` to `F.T.2`. The mutator scaffold for the
non-reciprocating sibling existed in an earlier draft of this commit and
is preserved in the git history if the future session wants it back.

### FL0.2 — Body-schema §7.6 invariant only emits the inverse direction

**What happened.** TASK.md §7.0 row §7.6 documents the failure mode as
"`task_status: done` with unchecked `- [ ]` items" and cites `F.B.7`.
Reading `tools/fm/validate.py`, `F.B.7` actually emits the **inverse**
WARN ("all items checked but task_status disagrees with 'done'"). The
mutator therefore flips `task_status` from `done` to `in_progress` while
leaving the checkboxes ticked. The WARN surfaces under `--strict` and the
test passes, but the test does *not* cover the literal direction TASK.md
§7.0 describes. FL0 because the diagnostic ID and linter are correct;
only the mutation direction differs from the prose.

## Closure

All 13 tests pass (12 parametrised + 1 skipped placeholder for §7.5).
Default `tools/check-governance.sh` exit 0; `INTEGRATION=1` exit 0.
Runtime ≈ 1.1 s.
