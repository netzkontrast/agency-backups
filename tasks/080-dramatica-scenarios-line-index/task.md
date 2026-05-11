---
type: task
status: active
slug: dramatica-scenarios-line-index
summary: "Cohort-1 Foundation Task in the dramatica-scenarios Epic (078). Implement build-time line-indexing for ontology.json per SPEC.md §2 — every entry's term_file pointer gains a sibling term_file_line:<int> and term_file_anchor:<str> field, indexed across vocabulary refs + dramatica-theory chunks + the new scenarios/*.md (self-indexing). Idempotent precompile; integrates with the existing tools/dramatica-nav/precompile.py pipeline."
created: 2026-05-11
updated: 2026-05-11
task_id: "080"
task_status: open
task_owner: "unassigned"
task_priority: P1
task_uses_prompts: []
task_spawns_research: []
task_spawns_prompts: []
task_blocked_by:
  - "078"
task_supersedes: []
task_superseded_by: []
task_affects_paths:
  - tools/dramatica-nav/lib_line_index.py
  - tools/dramatica-nav/lib_ontology.py
  - tools/dramatica-nav/precompile.py
  - tools/dramatica-nav/tests/test_line_index.py
  - maintenance/schemas/narrative-ontology/ontology.json
  - .githooks/pre-commit
---

# Task 080 — Build-time line-indexing for ontology.json

## Goal

Implement the build-time line-indexing pipeline from SPEC.md §2 so every
entry in `maintenance/schemas/narrative-ontology/ontology.json` carries
`term_file_line: <int>` and `term_file_anchor: <str>` next to the existing
`term_file:` pointer. Index scope: `skills/dramatica-vocabulary/references/*.md`
(24 files) + `skills/dramatica-theory/references/*.md` (15 files) + the
new `skills/dramatica-theory/scenarios/*.md` files as they land (self-
indexing). Re-runs idempotently — byte-identical `ontology.json` if no
inputs changed.

`done` when:

1. `tools/dramatica-nav/lib_line_index.py` — new module with the anchor →
   line resolution algorithm per SPEC.md §2.2.
2. `tools/dramatica-nav/precompile.py` integrates the new step at the
   point identified by SPEC.md §2.1 (between existing ontology load and
   write).
3. `maintenance/schemas/narrative-ontology/ontology.json` — every entry's
   `term_file` resolves to a `term_file_line:<int>` + `term_file_anchor:
   <slug>`. Orphan entries (anchor missing from file) handled per §2.3
   failure-tier spec.
4. `tools/dramatica-nav/tests/test_line_index.py` — covers: happy-path
   resolution, orphan-entry diagnostic, duplicate-anchor diagnostic,
   idempotency (byte-identical re-run), self-indexing of `scenarios/*.md`
   when files appear/disappear, cross-corpus ordering stability.
5. The pre-commit hook (`.githooks/pre-commit`) runs the precompile step
   whenever a file under the indexed scope changes, per SPEC.md §2.5.
6. Existing `tools/dramatica-nav/tests/` (test_validate.py et al.) still
   pass — the new fields are additive, not breaking.

## Context

Parent Epic: [Task 078](../078-dramatica-scenarios-epic/task.md). Drives
the SPEC.md §2 deliverable. Parallel-safe with [Task 079](../079-dramatica-
scenarios-content-template/task.md) and [Task 081](../081-dramatica-
scenarios-nav-instruct/task.md). Precedes [Task 082](../082-dramatica-
scenarios-taxonomy/task.md) (which writes to ontology.json — needs the
line-index integration point stable) and all Cohort-3 + Cohort-4 Tasks.

**Why this matters for the Task 072 trigger:** the SELF-INTEREST/MORALITY
worked-example bug happened because the calling agent reasoned from
metadata alone. With `term_file_line:`, `nav.py instruct` (Task 081) can
extract the exact paragraph from the source file rather than expecting
the agent to navigate the file from scratch — closes the indirection gap.

## Plan

1. Read SPEC.md §2 end-to-end. Verify the integration point at §2.1
   resolves against the current `tools/dramatica-nav/precompile.py`
   structure.
2. Implement `lib_line_index.py` — anchor → line resolution (case-
   insensitive matching, slug normalization per §2.2; duplicate-anchor
   handling per §2.3).
3. Wire into `precompile.py` at the §2.1 integration point. Persist
   `term_file_line:` + `term_file_anchor:` per entry.
4. Run end-to-end once → review the diff against `ontology.json`. Spot-
   check 10 random entries that anchor → line resolves correctly.
5. Pass 2: deterministic re-run produces byte-identical output. If not,
   fix non-determinism (sort order, dict iteration, line endings).
6. Test scaffold: 6+ test cases covering happy-path, orphan, duplicate,
   idempotency, self-indexing churn, cross-corpus stability.
7. Pre-commit hook integration: scope-detect file changes; trigger
   precompile only when relevant files change (avoid full rebuild on
   every commit).

## Todo

- [ ] 1. Read SPEC.md §2.1-§2.6
- [ ] 2. Implement `lib_line_index.py` anchor resolver
- [ ] 3. Wire into `precompile.py` at §2.1 integration point
- [ ] 4. Run one precompile; diff-review the ontology.json output
- [ ] 5. Confirm idempotency (byte-identical re-run)
- [ ] 6. Write `test_line_index.py` (≥ 6 cases)
- [ ] 7. Update pre-commit hook for scope-aware re-run
- [ ] 8. Run full `tools/dramatica-nav/tests/` — confirm no regression

## Links

- Parent epic: [Task 078](../078-dramatica-scenarios-epic/task.md)
- Source spec: `research/dramatica-scenarios-foundation/output/SPEC.md §2`
- Sister Foundation tasks: [Task 079](../079-dramatica-scenarios-content-template/task.md),
  [Task 081](../081-dramatica-scenarios-nav-instruct/task.md)
- Blocks: [Task 082](../082-dramatica-scenarios-taxonomy/task.md) + all
  Cohort-3 + Cohort-4 Tasks
