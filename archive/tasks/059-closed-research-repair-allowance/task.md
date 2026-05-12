---
type: task
status: archived
slug: closed-research-repair-allowance
summary: "Amend MAINTENANCE.md T4 absolute-immutability rule for closed research workspaces to permit T1 (frontmatter date bumps) and T2 (broken-link repair) corrections, while preserving T3/T4 content immutability."
created: 2026-05-07
updated: 2026-05-12
task_id: "059"
task_status: archived
task_owner: "claude-opus-4-7"
task_priority: P3
task_uses_prompts: []
task_spawns_research: []
task_spawns_prompts: []
task_blocked_by: []
task_supersedes: []
task_superseded_by: []
task_affects_paths:
  - MAINTENANCE.md
  - RESEARCH.md
  - tools/check-governance.sh
---

# Task 059 — T1/T2 Repair Allowance on Closed Research

## Goal

`MAINTENANCE.md` line 33 (`T4 — Research-touching`) currently forbids any modification to a `research_phase: complete` workspace. This blocks even harmless typo fixes, `updated:` date bumps when surrounding files move, and broken-internal-link repair when a sibling file is renamed. Errors in closed research are permanent by design. The single falsifiable outcome of this Task: `MAINTENANCE.md` is amended so that T1 (mechanical metadata) and T2 (linkage repair) operations are permitted on closed research, while T3 (content semantics) and T4 (synthesis revision) remain forbidden — and the per-mutation linter mapping in `MAINTENANCE.md §1` is updated accordingly.

## Plan

1. **Inventory** the current T1/T2/T3/T4 vocabulary in `MAINTENANCE.md §1` and confirm what each tier currently covers.
2. **Draft** the amendment: split the existing "Research-touching" row into "Research-T1/T2" (allowed-with-rationale) and "Research-T3/T4" (forbidden); define rationale-line and dated-note requirements for any T1/T2 repair, mirroring the §8.4 Resumption Checklist convention.
3. **Decide** whether closed-research T1/T2 repair triggers the §4.7 `updated` lifecycle on the *originating Task* (default: no; record the decision rationale).
4. **Land** the amendment in `MAINTENANCE.md` and a cross-reference in `RESEARCH.md`.
5. **Verify** by running a fixture repair (e.g., bump `updated:` on one closed `research/<slug>/output/SPEC.md`) under the new rule and confirming `tools/check-governance.sh` exits zero.

## Todo

- [ ] Inventory current T1–T4 vocabulary; note ambiguity in `notes.md`.
- [ ] Draft amendment text for `MAINTENANCE.md` and `RESEARCH.md`.
- [ ] Decide §4.7 `updated`-lifecycle interaction; document rationale.
- [ ] Land amendment.
- [ ] Run fixture repair through `tools/check-governance.sh`.
- [ ] Write `friction-log.md` with FL[0–3] declaration on closure.

## Links

- Parent dispatch: [Task 053](../053-core-architecture-review-followups/) finding B.8.
- Affected line at branch-time: [`MAINTENANCE.md:33`](../../MAINTENANCE.md).
- Adjacent: [`RESEARCH.md`](../../RESEARCH.md) — research-workspace lifecycle.
