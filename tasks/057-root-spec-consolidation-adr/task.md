---
type: task
status: active
slug: root-spec-consolidation-adr
summary: "Decision-class Task: produce an ADR evaluating consolidation of the 9+ root spec files (PRE_COMMIT.md -> AGENTS.md, FRUSTRATED.md -> MAINTENANCE.md) to reduce session-boot token cost."
created: 2026-05-07
updated: 2026-05-11
task_id: "057"
task_status: done
task_owner: "claude-code"
task_priority: P3
task_uses_prompts: []
task_spawns_research: []
task_spawns_prompts: []
task_blocked_by: []
task_supersedes: []
task_superseded_by: []
task_affects_paths:
  - decisions/
  - tasks/057-root-spec-consolidation-adr/
---

# Task 057 — Root-Spec Consolidation (ADR)

## Goal

Every agent session boot reads 9+ root spec files (`AGENTS.md`, `TASK.md`, `PROMPT.md`, `RESEARCH.md`, `FOLDERS.md`, `PRE_COMMIT.md`, `FRUSTRATED.md`, `MAINTENANCE.md`, `maintenance/language-spec.md`) per `README.md §10`. The token cost is substantial. This Task evaluates two specific consolidations and produces an ADR with the decision. Falsifiable outcome: a ratified ADR at `decisions/<NNNN>-root-spec-consolidation.md` recording either {merge-PRE_COMMIT-into-AGENTS + merge-FRUSTRATED-into-MAINTENANCE, partial-merge, status-quo} with measured token-cost data backing the choice.

## Plan

1. **Measure** the actual token cost of the current 9-spec boot bundle vs. a hypothetical 7-spec bundle after the two proposed merges.
2. **Audit** cross-references: every `[FRUSTRATED.md](...)` and `[PRE_COMMIT.md](...)` link in the repo would need either anchor-rewriting (if merged) or status-quo preservation (if not).
3. **Draft** the merged section drafts in scratch files (do not commit live spec changes here) so the ADR can include "what the merged document would look like" without prematurely shipping.
4. **Author** `decisions/<NNNN>-root-spec-consolidation.md` per the ADR template; capture the cross-reference rewrite cost as a table.
5. **Open** an implementation successor Task if the ADR is Accepted; otherwise close with rationale.

## Todo

- [ ] Measure boot-bundle token cost (current vs. merged) — record in `notes.md`.
- [ ] Audit `grep -rn 'PRE_COMMIT\\.md\\|FRUSTRATED\\.md'` cross-references.
- [ ] Draft merged-section sketches in `notes.md`.
- [ ] Author ADR at `decisions/<NNNN>-root-spec-consolidation.md`.
- [ ] If Accepted with merge: open implementation Task.
- [ ] Write `friction-log.md` with FL[0–3] declaration on closure.

## Links

- Parent dispatch: [Task 053](../053-core-architecture-review-followups/) finding B.6.
- Affected catalogue at branch-time: [`README.md §10`](../../README.md) (lines 179–190).
- Governance: [`research/adr-spec-research-synthesis/output/SPEC.md`](../../research/adr-spec-research-synthesis/output/SPEC.md).
