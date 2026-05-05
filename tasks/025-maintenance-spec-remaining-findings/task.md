---
type: task
status: active
slug: maintenance-spec-remaining-findings
summary: "Successor to Task 014. Carry forward only the F1–F7 findings that Task 008 did not already resolve. F2/F3/F4/F7 remain open; F1, F5, F6 are absorbed by Task 008 / Task 016 deliverables."
created: 2026-05-05
updated: 2026-05-05
task_id: "025"
task_status: open
task_owner: "unassigned"
task_priority: P2
task_uses_prompts:
  - repo-coherence-check
task_spawns_research: []
task_spawns_prompts: []
task_supersedes:
  - "014"
task_blocked_by:
  - "019"
task_affects_paths:
  - MAINTENANCE.md
  - prompts/repo-coherence-check/prompt.md
  - tools/check-governance.sh
---

# Task 025 — Maintenance-Spec Remaining Findings

Successor to [Task 014](../014-improve-maintenance-spec-from-session/task.md). Task 014 captured seven findings (F1–F7) from the 2026-05-05 coherence session. Several of those have since been absorbed:

- **F1 (duplicate `task_id` not mechanically detected)** — addressed by [Task 008](../008-harden-coherence-baseline-protocol/task.md) (duplicate-id pre-creation check in the coherence prompt) and partially by `tools/fm/validate.py` (Task 016).
- **F5 (`task_spawns_prompts` missing from template)** — fixed: the template now carries every required L2 key (verified 2026-05-05).
- **F6 (run-log baseline survives squash)** — verified by Task 008's hardening.

The findings still open are F2, F3, F4, F7. This Task carries them forward; F2 in particular needs a concrete tier assignment now that `tools/fm/edit.py` exists as the canonical T1/T2 mutator.

## Goal

Each remaining finding (F2, F3, F4, F7) lands as a concrete diff against `MAINTENANCE.md`, `prompts/repo-coherence-check/prompt.md`, or `tools/check-governance.sh`, with the disposition recorded in `notes.md`. The Task is `done` when no finding is unaddressed.

## Plan

1. **F2 — duplicate-key renumber tier.** Add an explicit row to `MAINTENANCE.md §1` covering the renumber-on-collision repair. Recommend T2 if executed via `tools/fm/edit.py --set task_id=...` plus a `git mv`; T3 if it requires manual cross-reference rewrites across closed tasks (per Task 024's plan).
2. **F3 — linter-first triage.** Add a Step 2.5 to `prompts/repo-coherence-check/prompt.md` instructing the agent to run `tools/check-governance.sh` first and treat its output as the authoritative T1/T2 worklist.
3. **F4 — spec-bearing vs review-bearing research.** Distinguish `output/SPEC.md`-bearing research workspaces from one-shot review artefacts in the prompt's T3 drift checklist.
4. **F7 — verify linters pass post-repair.** Add a Step 4.5 ("Verify Linters Pass") before Commit; the step MUST run `tools/check-governance.sh` and abort the commit if it exits non-zero.
5. Append a `friction-log.md` recording the disposition of every finding (FL[0-3]).

## Todo

- [ ] 1. Confirm Task 019 (and the linter rewrite under it) has `task_status: done` before starting — F2 / F7 phrasing depends on the new linter surface.
- [ ] 2. Land F2 amendment to `MAINTENANCE.md §1`.
- [ ] 3. Land F3 amendment (Step 2.5) to the coherence prompt.
- [ ] 4. Land F4 amendment to the coherence prompt T3 checklist.
- [ ] 5. Land F7 amendment (Step 4.5) to the coherence prompt.
- [ ] 6. Produce `friction-log.md` with FL[0-3] declaration.

## Links

- Predecessor: [`../014-improve-maintenance-spec-from-session/task.md`](../014-improve-maintenance-spec-from-session/task.md)
- Already-addressed siblings: [`../008-harden-coherence-baseline-protocol/task.md`](../008-harden-coherence-baseline-protocol/task.md), [`../016-flexible-frontmatter-toolchain/task.md`](../016-flexible-frontmatter-toolchain/task.md)
- Blocker: [`../019-fm-toolchain-suite-integration/task.md`](../019-fm-toolchain-suite-integration/task.md)
- Governing specs: [`TASK.md`](../../TASK.md), [`MAINTENANCE.md`](../../MAINTENANCE.md), [`PROMPT.md`](../../PROMPT.md)
