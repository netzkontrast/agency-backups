---
type: prompt
status: active
slug: fix-ft1-scope-drift
summary: "Resolve the F.T.1 spec/implementation drift: TASK.md §7.3 documents enforcement scope as `task_status ∈ {done, updated, abandoned}` only, but `tools/fm/validate.py --type-check` enforces unconditionally. Decide which surface wins, align both, and prove the chosen path."
created: 2026-05-07
updated: 2026-05-07
prompt_kind: tool-instruction
prompt_framework: RISEN+ReAct
prompt_target_agent: "Claude Code"
---

# Fix F.T.1 Enforcement-Scope Drift

## Framework

RISEN+ReAct. The frontmatter declares the framework (`prompt_framework: RISEN+ReAct`) and this section restates it for `fm-validate` header conformance. R/I/S/E carry the canonical roles; **Constraints** groups normative scope/failure rules.

## R — Role

You are the **main-agent** dispatched to resolve the F.T.1 spec/implementation drift surfaced in PR #81 R-2. Your remit is bounded by the Acceptance Criteria in [`brief.md`](./brief.md); you MUST NOT expand scope to other validators or other diagnostic codes without surfacing the divergence in `friction-log.md`.

## I — Input

- [`TASK.md`](../../TASK.md) §7.3 — prose enforcement scope.
- [`tools/fm/validate.py`](../../tools/fm/validate.py) `type_check()` — implementation.
- [`tasks/048-task-tooling-impl-spec/readme.md`](../../tasks/048-task-tooling-impl-spec/readme.md) Assumptions Log — first explicit drift documentation.
- [`tasks/033-task-spec-integration/friction-log.md`](../../tasks/033-task-spec-integration/friction-log.md) Notes — original workaround surface.
- [`maintenance/pr-81-review.md`](../../maintenance/pr-81-review.md) §R-2 — review-finding rationale.
- `git log --follow tools/fm/validate.py | grep -i "ST-5\|F.T.1\|type-check"` — original-intent provenance.

## S — Steps

1. The agent MUST read every input listed in **I — Input** before proposing a resolution. Skipping the git-history step is a falsification (the brief explicitly names the original commit as canonical).
2. The agent MUST decide between the two clean alignments documented in `brief.md` Goal — loosen linter OR tighten prose — and record the decision in a short ADR or research note per Acceptance Criterion 1.
3. The agent MUST update both surfaces (TASK.md §7.3 prose AND `tools/fm/validate.py`) in the same commit so they agree.
4. The agent MUST add or update a test that proves the chosen resolution holds against a `task_status: open` task with pre-declared prompt slugs.
5. The agent MUST run `tools/check-governance.sh` and resolve every ERROR before committing; pre-existing baseline ERRORs are documented in `friction-log.md` per the Task 032 / Task 033 precedent.
6. The agent MUST commit with a message that names this prompt slug in its trailer.
7. The agent MUST NOT push (the maintainer pushes after review).

## E — Expectations

- Decision recorded in `decisions/<NNNN>-ft1-enforcement-scope.md` OR `research/ft1-enforcement-scope-decision/output/SPEC.md` (≤ 2 pages).
- `TASK.md §7.3` and `tools/fm/validate.py` agree.
- New or updated test in `tools/tests/fm/test_validate.py` (or `tools/tests/fm/test_falsification_attacks.py`) proves the resolution.
- Task 048 `task_uses_prompts` field can carry the three planned prompt slugs without F.T.1 rejection (acceptance integration test).
- `tools/check-governance.sh` exits 0 (or remaining ERRORs documented).
- Commit message follows repo convention; trailer cites this prompt slug for traceability.

## Constraints

- Dependency: None. Independent investigation. SHOULD complete before Task 048 ST-3 begins synthesis.
- MUST NOT trigger the brief's Falsification clauses: regression-after-loosening, missing alternative-pattern after tightening, or skipping the original-commit-history check.
- MUST NOT expand scope to F.T.2 (reciprocity) or other dangling-reference fields beyond `task_uses_prompts` / `task_spawns_prompts` without surfacing the divergence.
- SHOULD prefer an ADR if the decision touches the validator's contract; SHOULD prefer a research note if it is an implementation-detail tightening.
- MUST run `tools/check-governance.sh` before pushing; a non-zero exit MUST block the push.
