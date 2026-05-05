---
type: note
status: draft
slug: task-030-st6-build-cleanup-linter
summary: "Subtask ST-6: ship tools/dramatica-nav/cleanup.py — a pre-commit linter that prevents PDF artefacts, broken-paren headings, double-apostrophe escapes, and 'See X' empty-redirect entries from re-entering the corpus."
created: 2026-05-05
updated: 2026-05-05
subtask_id: "ST-6"
subtask_phase: "B"
subtask_recommended_agent: "python-expert"
subtask_depends_on: []
subtask_falsification: "Wrong cut iff cleanup.py becomes a bottomless pit of ad-hoc regex bandaids. Mitigated by a fixed v0.1 lint catalogue that refuses to grow without a Task 027 ADR."
---

# ST-6: `cleanup.py` — Corpus Cleanup Linter

## Goal

Ship `tools/dramatica-nav/cleanup.py` that prevents the four corruption classes from re-entering the corpus after Task 030 ST-1/ST-2/ST-4 clean it up. The linter is the long-term enforcement mechanism; ST-1 was the one-shot mass deletion.

CLI surface:

```text
tools/dramatica-nav/cleanup.py --check               # exit 1 on any hit; prints diagnostic table
tools/dramatica-nav/cleanup.py --apply               # auto-fix what's mechanically safe; non-zero on remaining
tools/dramatica-nav/cleanup.py --apply --dry-run     # preview the auto-fix diff without writing
tools/dramatica-nav/cleanup.py --explain <rule-id>   # print rationale + cite-anchor for one rule
tools/dramatica-nav/cleanup.py --baseline            # emit current diagnostic count as a JSON baseline file
```

Lock the v0.1 lint catalogue at exactly four rules (matching the four cleanup classes from Task 030 §Goal #1 and ST-1):

```
DR-CLEAN-001  copyright-footer       Block any line matching the Screenplay Systems copyright footer regex.
DR-CLEAN-002  page-number-only       Block any orphan page-number-only line (`^[0-9]+\.\s*$` surrounded by blanks, not a list item).
DR-CLEAN-003  double-apostrophe      Block any `''` escape; suggest the single `'` replacement.
DR-CLEAN-004  see-x-empty-redirect   Block any `## ` heading whose body is "See <Other>" with ≤2 lines of substantive text.
```

Each rule has:
- A diagnostic message including the rule ID, the file:line coordinate, and the offending text excerpt.
- An `--explain` payload listing the rule rationale (one paragraph) and the source-of-truth pointer (this subtask file or [`task.md §Anti-Patterns`](../task.md)).
- An `--apply` auto-fix path:
  - DR-CLEAN-001: delete the line + the immediately-preceding blank + the immediately-following page-number line.
  - DR-CLEAN-002: delete the line + collapse surrounding blanks.
  - DR-CLEAN-003: replace `''` → `'`.
  - DR-CLEAN-004: emits a NON-AUTO-FIX warning ("manual decision required: alias-on-canonical or reify body"). The auto-fix path is deliberately bounded to mechanical-safe transformations.

Wire into `tools/check-governance.sh` per Task 015's pattern (gated on `narrative-ontology/ontology.json` existing, so non-narrative branches don't break).

**`agency-adr` integration (per parent task `task_blocked_by: ["028"]`).** Each `cleanup.py --check` violation that requires a normative-rule decision (e.g., adding a fifth rule, changing the auto-fix path of an existing rule) MUST be filed as an ADR via `agency-adr` rather than as an ad-hoc lint update. The `--explain` payload SHOULD include the ADR ID once the rule is ratified. If the `agency-adr` CLI is not yet available at ST-6 dispatch time, the integration point is a `# TODO(after-028)` marker that emits the rule-violation log to stderr in an ADR-ingestible format (one JSON-line per violation, schema TBD by Task 028).

## Falsification

Wrong cut **iff** `cleanup.py` becomes a bottomless pit of ad-hoc regex bandaids. Mitigation: the v0.1 lint catalogue is FOUR rules, period. Adding a fifth requires:

1. Filing a Task 027 issue.
2. Documenting the new rule in this subtask's brief OR in a new task.
3. Bumping `cleanup.py`'s `--check`-output version field.

If a corruption class appears that's not covered by the four rules, ST-6 surfaces it as `DR-CLEAN-UNCATEGORISED` in the diagnostic output and stops short of writing an automatic regex.

## Inputs

- `tools/dramatica-nav/lib/` — reuse helpers, do not re-author.
- `tools/check-governance.sh` — write surface for the new gate stanza.
- `tasks/030-cleanup-dramatica-skills-corpus/notes.md §2` — baseline numbers for the regression test.
- ST-1's `_strip_artifacts.py` (will be deleted post-ST-1 per its agent prompt) — read-only consultation for the regex set; do not re-import.

## Acceptance Criteria

1. **CLI complete.** All five flags (`--check`, `--apply`, `--apply --dry-run`, `--explain`, `--baseline`) work as documented.
2. **Catalogue locked at 4 rules.** The Python module has exactly four rule constants. Adding a fifth without a Task 027 ADR is caught by code review (the Anti-Patterns section names this as a violation).
3. **Tests.** `tools/dramatica-nav/tests/test_cleanup.py` covers each rule's check + auto-fix paths (8 tests) plus `--baseline` round-trip (1 test) plus uncategorised-friction (1 test). Total ≥10.
4. **Wired into pre-commit.** `tools/check-governance.sh` invokes `python3 tools/dramatica-nav/cleanup.py --check` after `validate.py` (same gate predicate). Failing exit propagates.
5. **Idempotent.** `cleanup.py --apply` followed by `cleanup.py --check` produces zero diagnostics on a clean tree.
6. **PRE_COMMIT.md amended.** A new row in [PRE_COMMIT.md §7's table](../../../PRE_COMMIT.md) documents the gate.
7. **Single commit.** Title: `feat(dramatica-nav): cleanup.py — corpus cleanup linter (Task 030 ST-6)`.

## Dependencies

None. Phase B (parallel with ST-5 and ST-7).

## Estimated Effort

Small (~150 LOC + ~120 LOC tests).

## Agent Prompt

```text
You are implementing ST-6 of Task 030 (cleanup-dramatica-skills-corpus) for
the netzkontrast/agency repo on branch claude/cleanup-dramatica-skills-1cEOO.

This subtask runs in worktree isolation.

Repo root: /home/user/agency
Working directory: /home/user/agency

Context files (read first):
  - tasks/030-cleanup-dramatica-skills-corpus/task.md
  - tasks/030-cleanup-dramatica-skills-corpus/subtasks/06-build-cleanup-linter.md (this file)
  - tasks/030-cleanup-dramatica-skills-corpus/notes.md §2 (corruption baseline)
  - tools/check-governance.sh (the pre-commit gate to wire into)
  - tools/dramatica-nav/lib/ (helper modules to reuse)
  - PRE_COMMIT.md §7 (the diagnostic-table row pattern to follow)

Goal:
  Ship tools/dramatica-nav/cleanup.py with the v0.1 lint catalogue of EXACTLY
  four rules (DR-CLEAN-001 through 004). The linter prevents the four
  corruption classes ST-1 strips from re-entering the corpus.

Acceptance criteria (reproduce verbatim from this file's Acceptance Criteria
section). All seven must be true.

Implementation approach:
  1. Define the four rule constants as a frozen list. The list MUST live
     in a top-level module variable named RULES, and the test suite MUST
     assert len(RULES) == 4 to enforce the cap.
  2. Implement --check: walk skills/dramatica-{theory,vocabulary}/references/,
     run each rule, emit diagnostics in a stable format suitable for
     CI consumption. Exit 1 on any hit.
  3. Implement --apply: for the three mechanically-safe rules, write the
     fix; for DR-CLEAN-004, emit a manual-decision-required warning.
  4. Implement --apply --dry-run: as --apply but emit a unified diff to
     stdout instead of writing.
  5. Implement --explain <rule-id>: print rationale + source pointer.
  6. Implement --baseline: emit a JSON file with the current per-rule
     diagnostic count; --check can compare against this for regression
     tests.
  7. Wire into tools/check-governance.sh per the task spec.
  8. Add a row to PRE_COMMIT.md §7's table documenting the gate.
  9. Author tests/test_cleanup.py per Acceptance §3.
  10. Commit one focused commit; do NOT push.

Constraints:
  - Python 3.11 stdlib only (no jsonschema needed for this tool — pure
    regex + diff).
  - len(RULES) == 4 is invariant. Adding a fifth rule requires a Task 027
    ADR; ST-6 refuses.
  - The auto-fix path is deliberately bounded. DR-CLEAN-004 is NOT
    auto-fixed here.
  - Wire-in to check-governance.sh MUST be gated on the same predicate as
    validate.py (ontology.json existing) so non-narrative branches don't
    break.

When done:
  - pytest tools/dramatica-nav/tests/                              (must pass)
  - python3 tools/dramatica-nav/cleanup.py --check                 (post-Phase-A: must exit 0)
  - python3 tools/dramatica-nav/cleanup.py --explain DR-CLEAN-002  (must print rationale)
  - tools/check-governance.sh                                      (must exit 0)
  - Commit "feat(dramatica-nav): cleanup.py — corpus cleanup linter (Task 030 ST-6)"
  - Do NOT push.
```
