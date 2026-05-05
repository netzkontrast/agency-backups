---
type: task
status: active
slug: improve-maintenance-spec-from-session
summary: "Captures maintenance-spec improvement opportunities surfaced during the 2026-05-05 Repo Coherence Check; proposes amendments to MAINTENANCE.md and the coherence-check prompt."
created: 2026-05-05
updated: 2026-05-05
task_id: "014"
task_status: updated
task_owner: "claude-code"
task_priority: P2
task_uses_prompts:
  - repo-coherence-check
task_spawns_research: []
task_spawns_prompts: []
task_superseded_by:
  - "025"
task_affects_paths:
  - MAINTENANCE.md
  - prompts/repo-coherence-check/prompt.md
  - tools/check-governance.sh
  - tools/lint-linkage.py
---

# Task 014 — Improve Maintenance Spec From 2026-05-05 Session

## Goal

The 2026-05-05 Repo Coherence Check (this session) surfaced friction patterns that the current `MAINTENANCE.md` and `prompts/repo-coherence-check/prompt.md` do not yet address. This Task captures those patterns as concrete amendments. The Task is complete when each finding below has either been merged into the spec/prompt or rejected with a rationale recorded in `notes.md`.

## Findings From This Session

### F1 — Duplicate `task_id` is not mechanically detected

The session found two duplicate `task_id` collisions (006, 009). `tools/check-governance.sh` reports zero diagnostics for these because no linter scans `task_id` uniqueness across `/tasks/`. The coherence agent only catches them through manual inspection.

**Proposed amendment:** Extend `tools/lint-linkage.py` (or a new linter) to fail when two `task.md` files share a `task_id`. Add a corresponding row to `TASK.md §7.0` and reference it from the coherence prompt's T1/T2 checklist.

### F2 — The renumber-on-collision repair is ambiguous between T2 and T3

`MAINTENANCE.md §1` lists T2 as "Adding a missing L1 or L2 frontmatter key" and T3 as "Changing section headings, rewriting content, altering schema definitions". A folder rename plus cross-reference sweep fits neither category cleanly. The previous coherence run (2026-05-04, session zVZBH) treated it as T2; this run filed it as T3 (Task 013) because the cross-reference sweep affects ~10 files including a closed task workspace.

**Proposed amendment:** `MAINTENANCE.md §1` SHOULD add an explicit row for "duplicate-key renumber per `TASK.md §8.1`" with a clear tier assignment (recommend T2 if linker-driven, T3 if it requires manual cross-reference rewrites across closed tasks).

### F3 — The coherence prompt does not budget for large deltas

This run had 131 changed files. The prompt's Step 2 says to "build a triage table" for every file in the delta but offers no guidance for budget-bounded scans. The session leveraged `tools/check-governance.sh` to drive triage instead — a strategy the previous run also used, but the prompt does not document.

**Proposed amendment:** Add a Step 2.5 ("Linter-First Triage") to `prompts/repo-coherence-check/prompt.md` that instructs the agent to run `tools/check-governance.sh` first, treat its output as the authoritative T1/T2 worklist, and reserve direct file scanning for T3 patterns the linter cannot detect (research-to-governance drift, broken links).

### F4 — Research-to-governance drift detection is manual and noisy

The prompt's T3 checklist (§Step 4) instructs the agent to grep AGENTS.md/TASK.md/MAINTENANCE.md for each completed research slug. In this session, three completed research workspaces (`skills-navigation-bootstrap`, `skills-skill-container-capabilities`, `pr27-governance-review`) had no governance hits, but only the first two are arguably authoritative; `pr27-governance-review` is a one-shot review artifact. The prompt does not differentiate.

**Proposed amendment:** The T3 drift checklist SHOULD distinguish "spec-bearing research" (output named `SPEC.md`) from "review-bearing research" (output named `REVIEW.md` or similar). Only spec-bearing research is candidate for governance surfacing.

### F5 — `task_spawns_prompts` is mandatory but not always added on task creation

This session's two T2 fixes both added a missing `task_spawns_prompts: []` key. The key has been mandatory since the L2 schema was finalised, but newly-created tasks (`tasks/006-skills-navigation-bootstrap/task.md`, `tasks/012-review-pr-29/task.md`) shipped without it.

**Proposed amendment:** `templates/task.md` SHOULD include `task_spawns_prompts: []` as a default empty list. Verify the template carries every L1 + L2 key, and add a CI check that any new `task.md` instantiated via copy-of-template carries every required key before its first commit.

### F6 — Run-log baseline survives PR squash now (good), but not branch deletion

The 2026-05-04 runs hit baseline-loss-after-squash. Task 008 hardened the baseline protocol; this session inherited that and used `2ac93bd` cleanly. Verify the protocol still handles branch-deletion (e.g. when a feature branch's tip commit no longer exists post-merge-and-prune).

**Proposed amendment:** Add a "post-task-008 verification" gherkin scenario to `MAINTENANCE.md §2.3` that asserts the baseline is recoverable across all six common git history mutations (squash, rebase, force-push, branch-delete, tag-rewrite, history-rewrite via filter-repo).

### F7 — Coherence prompt does not require running the linter to verify the run is clean

The prompt's "Expectations" table mentions "No regressions: the repo MUST pass any existing lint or pre-commit checks after the repair commit" but no Step explicitly invokes `tools/check-governance.sh` post-repair as a verification gate.

**Proposed amendment:** Add a "Step 4.5 — Verify Linters Pass" before Step 5 (Commit). The Step MUST run `tools/check-governance.sh` and abort the commit if it exits non-zero.

## Plan

1. Review each finding F1–F7 with the maintainer; mark each as ACCEPTED, DEFERRED, or REJECTED in `notes.md`.
2. For ACCEPTED findings, write the concrete diff against `MAINTENANCE.md`, `prompts/repo-coherence-check/prompt.md`, `tools/`, or `templates/task.md`.
3. Open a follow-up Coherence Hardening sub-task per item if the diff is non-trivial.
4. Run `tools/check-governance.sh` after every change; ensure it stays green.
5. Close this Task with a `friction-log.md` recording the disposition of each finding.

## Todo

- [ ] Triage F1 — duplicate task_id linter (high value, low effort).
- [ ] Triage F2 — renumber tier ambiguity (spec wording).
- [ ] Triage F3 — linter-first triage as canonical Step 2.5 in coherence prompt.
- [ ] Triage F4 — distinguish SPEC-bearing vs. REVIEW-bearing research for drift checks.
- [ ] Triage F5 — template defaults for `task_spawns_prompts`.
- [ ] Triage F6 — gherkin scenarios for baseline-recovery across all git mutations.
- [ ] Triage F7 — explicit linter-verification step in coherence prompt.
- [ ] Author the diffs for ACCEPTED findings.
- [ ] Re-run `tools/check-governance.sh` post-merge.
- [ ] Write `friction-log.md` with FL[0-3] disposition.

## Links

- Found by: coherence check `maintenance/run-log.md` entry 2026-05-05.
- Source prompt: [`prompts/repo-coherence-check/prompt.md`](../../prompts/repo-coherence-check/prompt.md).
- Predecessor hardening: [`tasks/008-harden-coherence-baseline-protocol/`](../008-harden-coherence-baseline-protocol/).
- Sibling discovery from same run: [`tasks/013-renumber-duplicate-task-ids/`](../013-renumber-duplicate-task-ids/).
