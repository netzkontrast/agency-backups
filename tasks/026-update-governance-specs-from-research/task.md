---
type: task
status: active
slug: update-governance-specs-from-research
summary: "Implement the update plan derived from the governance-specs-update-research."
created: 2026-05-05
updated: 2026-05-05
task_id: "026"
task_status: open
task_owner: "jules"
task_priority: P1
task_uses_prompts:
  - governance-specs-update-research
task_spawns_research: []
task_spawns_prompts: []
task_supersedes:
  - "001"
task_affects_paths:
  - MAINTENANCE.md
  - PRE_COMMIT.md
  - FOLDERS.md
  - TASK.md
---

# Task 026 — Update Governance Specs From Research

Successor to Task 001.

## Goal
Implement the recommendations detailed in `research/governance-specs-update-research/output/SPEC.md` to align the root governance specifications (`MAINTENANCE.md`, `PRE_COMMIT.md`, `FOLDERS.md`, `TASK.md`) with the current enforced toolchain and repository realities.

## Plan
1. Apply the detailed section-by-section update plan in `SPEC.md` to `MAINTENANCE.md` (e.g. toolchain migration context, duplicate task ID rules).
2. Apply updates to `PRE_COMMIT.md` (Linter transition documentation, waivers protocol).
3. Apply updates to `FOLDERS.md` (Subfolder heuristics for prompts).
4. Apply updates to `TASK.md` (Clarification on linkage rules for closed tasks and duplicate IDs).
5. Verify changes with linting and commit.

## Todo
- [ ] Update `MAINTENANCE.md`.
- [ ] Update `PRE_COMMIT.md`.
- [ ] Update `FOLDERS.md`.
- [ ] Update `TASK.md`.

## Links
- Output SPEC: [`../../research/governance-specs-update-research/output/SPEC.md`](../../research/governance-specs-update-research/output/SPEC.md)
