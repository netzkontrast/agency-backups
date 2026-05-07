---
type: task
status: active
slug: frustrated-spec-followup-ac1-ac5
summary: "Successor to Task 038 (set `task_status: updated` on PR #87 review). Closes the two acceptance criteria deferred from 038: AC-1 (FRUSTRATED.md §28 / PRE_COMMIT.md §2 byte-identical reconciliation, joint with Task 037 ST-4) and AC-5 (Reflexion-pattern lift into §FL.Log.1, blocked on `research/gemini/superclaude-agency-orchestration-spec/` arriving on the branch). Also covers the eventual `FM_FL_DECLARATION_STRICT=1` flip after remediating historical malformed logs in tasks 030 + 033."
created: 2026-05-07
updated: 2026-05-07
task_id: "053"
task_status: open
task_owner: "unassigned"
task_priority: P2
task_uses_prompts: []
task_spawns_research: []
task_spawns_prompts: []
task_blocked_by: []
task_supersedes:
  - 038
task_superseded_by: []
task_affects_paths:
  - FRUSTRATED.md
  - PRE_COMMIT.md
  - tasks/030-cleanup-dramatica-skills-corpus/friction-log.md
  - tasks/033-task-spec-integration/friction-log.md
  - tools/check-governance.sh
---

# Task 053 — FRUSTRATED.md Spec Integration Follow-Up (AC-1 + AC-5 + Strict-Mode Flip)

## Goal

Land the work Task 038 explicitly deferred. The Task is `done` when **all three** acceptance bundles below close, in order:

- **B-1 (AC-1).** FRUSTRATED.md §28 wording is byte-identical (modulo spec-name prefix) with PRE_COMMIT.md §2, verified by `diff` and a test in `tools/tests/`. Joint commit with [Task 037 ST-4](../037-pre-commit-spec-integration/subtasks/readme.md).
- **B-2 (AC-5).** §FL.Log.1 in FRUSTRATED.md lifts the *Reflexion pattern* concept from `research/gemini/superclaude-agency-orchestration-spec/superclaude-agency-orchestration-spec.md §7.1` (one paragraph) and anchors a new Gherkin scenario `FR.B.REFLEX.1` per Task 040 §B remap table. **Halt-condition:** if the cited research file is still absent from the branch when this Task is dispatched, file a precondition Task to publish that research before B-2 is attempted.
- **B-3 (Strict-mode flip).** Remediate the two historical malformed logs (tasks 030, 033) so they pass `tools/check-fl-declaration.py` under default mode, then promote the linter from advisory to gating by setting `FM_FL_DECLARATION_STRICT=1` as the default in `tools/check-governance.sh`. README.md §6 linter table updated.

## Context — Why this Task exists

PR #87 review (`tasks/038-frustrated-spec-integration/review-claude-brave-darwin.md` D1, D2) flagged that closing Task 038 as `task_status: done` violated TASK.md §4 because two acceptance criteria were not met:

- **AC-1** required §28/§2 byte-identical reconciliation — but Task 037 ST-4 was never written, so the `diff`-verification of byte-identicality could not be performed in the 038 close. Task 038's friction-log §1 documented the deferral honestly; the reviewer's correct response was "the deferral makes the close premature".
- **AC-5** required lifting the Reflexion-pattern from a Gemini research output that does not exist on the current branch. Task 038's friction-log §4 documented the absence; the reviewer's correct response was "absence of the source is a legitimate blocker, but the absence of a tracking task is not".

Task 038 has been re-stated as `task_status: updated` and points at this Task as its successor. This Task carries B-1 + B-2 + B-3 to completion.

## Preconditions

- **B-1:** Task 037 ST-4 must be authored, OR this Task absorbs Task 037 ST-4 directly. Decision belongs to the dispatcher.
- **B-2:** `research/gemini/superclaude-agency-orchestration-spec/superclaude-agency-orchestration-spec.md` must exist on the branch. If absent, file a precondition Task to publish it; do not invent the content.
- **B-3:** `tools/check-fl-declaration.py` must exist (already shipped by Task 038 ST-2; verify it has not regressed under main).

## Plan

1. **B-1 — §28/§2 reconciliation.** Coordinate with Task 037 ST-4. Decide on the canonical wording, land it in BOTH FRUSTRATED.md §28 AND PRE_COMMIT.md §2 in a single commit. Add a `tools/tests/test_section_byte_identicality.py` test that asserts the two sections produce a zero-line `diff` after stripping the spec-name prefix.
2. **B-2 — Reflexion-pattern lift.** Verify `research/gemini/...§7.1` is on the branch. Lift the concept into FRUSTRATED.md §FL.Log.1 as one paragraph (≤10 lines). Anchor a new Gherkin scenario `FR.B.REFLEX.1` per Task 040 §B remap. No Skill citations (Task 040 §A rejection of `sc-document` and `confidence-check`).
3. **B-3 — Strict-mode flip.** Remediate `tasks/030-cleanup-dramatica-skills-corpus/friction-log.md` (add a single canonical "Highest Frustration Level: FL2" line preserving the existing per-event detail) and `tasks/033-task-spec-integration/friction-log.md` (lift the FL1 declaration from frontmatter `summary:` into the body). Then flip `tools/check-governance.sh` to `FM_FL_DECLARATION_STRICT=1` by default and update README.md §6's table row.
4. **Update FR.B.4 Gherkin scenarios** to reflect the post-flip behaviour (default-gate, `FM_FL_DECLARATION_STRICT=0` for advisory). Mirror change in this Task's friction-log so the rationale is auditable.
5. **Closing run.** `git push` → `/sc:createPR` per AGENTS.md CR.1. PR cites this Task slug and the FL declaration.

## Acceptance Criteria

- [ ] B-1.1 — FRUSTRATED.md §28 and PRE_COMMIT.md §2 produce a zero-line `diff` (modulo spec-name prefix).
- [ ] B-1.2 — `tools/tests/test_section_byte_identicality.py` passes.
- [ ] B-2.1 — FRUSTRATED.md §FL.Log.1 carries the Reflexion-pattern paragraph (verbatim concept from Gemini research §7.1) — OR a documented Halt-condition disposition because the source is still absent.
- [ ] B-2.2 — `FR.B.REFLEX.1` Gherkin scenario lands in FRUSTRATED.md.
- [ ] B-3.1 — Tasks 030 + 033 friction-logs pass `tools/check-fl-declaration.py` under default mode.
- [ ] B-3.2 — `tools/check-governance.sh` defaults `FM_FL_DECLARATION_STRICT=1`.
- [ ] B-3.3 — README.md §6 table row says "Default-gate (Task 053)" instead of "Advisory".
- [ ] B-4 — FR.B.4 Gherkin scenarios in FRUSTRATED.md reflect post-flip semantics.
- [ ] friction-log.md exists with FL declaration.
- [ ] `tools/check-governance.sh` exits 0 on the closing commit.

## Todo

- [ ] 1. Coordinate with Task 037 ST-4 OR absorb its §2 amendment scope into B-1.
- [ ] 2. Verify `research/gemini/superclaude-agency-orchestration-spec/` exists on the branch; file precondition Task if absent.
- [ ] 3. Land B-1 reconciliation + diff test.
- [ ] 4. Land B-2 Reflexion-pattern lift + `FR.B.REFLEX.1` Gherkin (or record Halt disposition).
- [ ] 5. Remediate `tasks/030/friction-log.md` and `tasks/033/friction-log.md`.
- [ ] 6. Flip `FM_FL_DECLARATION_STRICT` default in `tools/check-governance.sh`; update FR.B.4 Gherkin.
- [ ] 7. Update README.md §6 linter-table row.
- [ ] 8. Author `friction-log.md` with FL declaration.
- [ ] 9. `tools/check-governance.sh` exits 0; run `pytest tools/tests/`.
- [ ] 10. `git push` → `/sc:createPR` citing this Task and Task 038 closure context.

## Links

- Predecessor (carries the substantive ST-1 / ST-2 / partial ST-3 deliverables): [`Task 038`](../038-frustrated-spec-integration/task.md) (`task_status: updated`).
- Reciprocal scope: [`Task 037 ST-4`](../037-pre-commit-spec-integration/subtasks/readme.md) — the §28/§2 reconciliation lives in both Tasks; B-1 absorbs or coordinates with it.
- Review-of-record: [`tasks/038-frustrated-spec-integration/review-claude-brave-darwin.md`](../038-frustrated-spec-integration/review-claude-brave-darwin.md) (D1 + D2).
- Governing specs: [`FRUSTRATED.md`](../../FRUSTRATED.md), [`PRE_COMMIT.md`](../../PRE_COMMIT.md) §2, [`TASK.md`](../../TASK.md) §4 / §313, [`README.md`](../../README.md) §6.
- Source for AC-5 (precondition): `research/gemini/superclaude-agency-orchestration-spec/superclaude-agency-orchestration-spec.md §7.1` — must exist on the branch before B-2 is attempted.

## Assumptions Log

- Task 053 is filed as the documented successor to Task 038; Task 038's `task_supersedes` reciprocity is set in the same commit that creates this Task.
- B-3 (strict-mode flip) is gated on B-2's resolution OR a documented decision to ship strict-mode without the Reflexion-pattern lift.
- The `diff`-based byte-identicality test in B-1 strips the leading spec-name in the heading line only; body bytes must match exactly.
