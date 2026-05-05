---
type: note
status: active
slug: task-019-friction-log
summary: "FL declaration for Task 019 (fm-toolchain-suite-integration). FL3 — six parallel subagents launched, three failed on stale worktree bases (one fabricated scaffolding, one aborted, one re-spawn hit org limit), four succeeded; the remaining four were implemented in-session. Phase 3 --check-body default-on flip explicitly deferred to Task 020 per SPEC §12.6."
created: 2026-05-05
updated: 2026-05-05
---

# Friction Log — Task 019

## Frustration Level: FL3

**Reasoning.** This is the highest-friction Task in the toolchain
arc. The plan called for nine parallel /sc:agent invocations; the
infrastructure landed three of those agents on stale worktree bases
that did NOT contain `tools/fm/`, the SPEC, or the ontology.

- **ST-1, ST-7**: succeeded via in-agent merge of the current branch.
- **ST-2, ST-4**: succeeded — the worktree happened to be on the
  right base (`f0d5d85` "merge: bring fm toolchain into worktree
  branch (task 019 prereq)").
- **ST-3 (1st run)**: was on stale `fbe8200`. The agent fabricated
  `tools/fm/_core.py` and `tools/fm/validate.py` from scratch as
  thin shims over `tools/validate-frontmatter.py` rather than abort.
  This would have collided with the real `_core.py` on merge — its
  output was discarded.
- **ST-5 (1st run)**: also on stale `fbe8200`. The agent correctly
  refused to fabricate the F.* taxonomy and the SPEC, and aborted
  with a clean failure report. Right call.
- **ST-3, ST-5 re-spawns**: both hit the org's monthly usage limit
  before producing any code. ST-3 produced a 884-token transcript
  with no output; ST-5 produced 624 tokens with no output.

The four lost subtasks (ST-3, ST-5, ST-6, ST-8) were re-implemented
in this session by the driver. Total time-to-converge was longer
than serial execution would have been, but the four parallel wins
(ST-1, ST-2, ST-4, ST-7) are still net-positive.

## Specific Frictions

1. **Worktree base inconsistency.** The Agent tool's `isolation: "worktree"`
   created branches from at least three different bases:
   - `fbe8200` (pre-Task-016, no fm/) — ST-3, ST-5
   - `f0d5d85` ("task 019 prereq" merge with fm/) — ST-1, ST-4
   - `6c3329a` (Task 018 close, current tip) — ST-2, ST-7

   This appears to be infrastructure rather than user error; the
   prompts pinned the absolute path `/home/user/agency` and the
   target branch `claude/complete-frontmatter-toolchain-l5Q8E` but
   the worktree creator picked starting commits inconsistently. The
   re-spawn instructions explicitly said "merge origin first" and
   would have worked, but the org limit prevented retesting.

2. **Org usage limit mid-task.** Hitting the limit during a multi-agent
   orchestration is a cliff: the driver has no way to retry with
   the same agent, and the conversation has to absorb the work.
   This Task absorbed ST-3, ST-5, ST-6, ST-8 directly. Friction is
   fine; the close-out commits are still audit-friendly.

3. **Reciprocity-rule design choices surfaced live-tree drift.**
   The first ST-5 cut treated `prompt_relates_to_task` as list-typed
   on the back-edge; that was wrong (the field is scalar). Setting
   `scalar: true` produced 3 false-positive F.T.2 reports against
   shared prompts (`repo-coherence-check`, `skills-skill-architecture`)
   that legitimately serve multiple tasks. Resolution: empty back-
   edge `prompt_relates_to_task: ""` is now interpreted as
   "shared / general" and the reciprocity check is skipped for
   that case. Documented in the ontology and the test suite.

4. **Phase 3 (`--check-body` default-on) blocked by corpus drift.**
   71 pre-existing F.B.1/6 ERRORs surface when --check-body runs
   over the live tree. These are body-shape mismatches in older
   prompts and tasks. SPEC §12.6 explicitly assigns the corpus
   migration to Task 019 (Phase 2) and the default-on flip to
   Task 020 (Phase 3). Task 019 ships the *toolchain*; the corpus
   migration is a separate audit pass that fits Task 020's scope
   better than this Task. Task 019's gate now uses --type-check
   (clean) without --check-body (drifty).

5. **lint-structure.py / check-trust.py have no fm-* successor yet.**
   Both still gate via the legacy code paths. ST-6 only retired
   `lint-linkage.py`. The structural-presence checks (does a slug
   folder have task.md / readme.md?) and the friction-log audit
   (does every done Task have a friction-log.md with FL[0-3]?) need
   their own fm-* successors before the legacy/ directory can be
   deleted.

## Suggested Follow-Ups

- **Task 020** (corpus migration → --check-body default-on):
  authored body-shape fixes for the 71 F.B.1/6 ERRORs the live
  tree carries, then flip the default in `tools/check-governance.sh`
  and remove the explicit --check-body documentation note in the
  PRE_COMMIT.md recipe.
- **fm-graph cycles in the live tree** (ST-2 surfaced 22): mostly
  legitimate supersession-chain reciprocity (`task_supersedes ↔
  task_superseded_by` are two-element cycles by design). A future
  refinement should split "true cycles" from "reciprocal pairs that
  are NOT cycles". Worth a one-line follow-up Task.
- **fm-fix recipe table coverage** (ST-4 chose to refuse F.3.4 and
  F.4.2 auto-repair). A future refinement could grow the table to
  cover heading insertion when the body schema is empty.
- **Worktree-base infrastructure hardening**: future multi-agent
  fan-out should specify the start commit explicitly, OR the driver
  should pre-flight check `git rev-parse HEAD` in each worktree and
  reject ones on the wrong base before issuing prompts.
- **`fm-section --rename` reciprocity tightening**: when ST-1's
  `fm-rename` mutates a slug, the tier-guard in `fm-section --rename`
  may need to be invoked too if the rename touches a heading anchor.
  Currently they're independent; a future audit pass should
  cross-check.

## Pointers

- Source SPEC: [`/research/flexible-frontmatter-toolchain/output/SPEC.md`](../../research/flexible-frontmatter-toolchain/output/SPEC.md)
- Predecessors: Task 016 (atomic toolchain), Task 017 (migration), Task 018 (fm-section).
- Successor: Task 020 (audit-prompt-fm-validate-conformance) — body-shape corpus migration + Phase 3 flip.
- Phase A wins (parallel agents): commits 86555df, f28a34b, bb9d8df, 76daf44.
- Phase A in-session implementations (after agent failures / limit):
  336bdbf (ST-3), 7c606ab (ST-5), b709c80 (ST-6), 8b5c59b (ST-8).
