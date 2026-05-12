---
type: task
status: archived
slug: renumber-duplicate-task-ids-v2
summary: "Successor to Task 013. The duplicate task_id pairs (006/006 and 009/009) remain unresolved; the original Task 013 plan targeted slots 014/015, both of which are now occupied. Renumber the duplicates into the next free slots (026/027) per TASK.md §8.1."
created: 2026-05-05
updated: 2026-05-12
task_id: "024"
task_status: archived
task_owner: "claude-code"
task_priority: P2
task_uses_prompts: []
task_spawns_research: []
task_spawns_prompts: []
task_supersedes:
  - 013
task_blocked_by: []
task_affects_paths:
  - tasks/006-skills-navigation-bootstrap/
  - tasks/006-surface-skills-architecture/
  - tasks/009-author-skills-root-spec/
  - tasks/009-review-pr28-readme-spec/
  - tasks/readme.md
  - maintenance/run-log.md
---

# Task 024 — Renumber Duplicate task_id Values (v2)

Successor to [Task 013](../013-renumber-duplicate-task-ids/task.md). The original plan correctly identified the two duplicate-`task_id` collisions (006/006 and 009/009) but proposed renumbering into slots 014 and 015 — both of which were subsequently claimed by other Tasks before 013 ran. The slot assumptions are stale; the duplicates persist. This Task picks up where 013 left off, with a current-state-aware renumber plan.

## Goal

Every `task_id` value across `/tasks/*/task.md` MUST be unique. Specifically:

- `tasks/006-skills-navigation-bootstrap/` (the *later* claimer of `task_id: "006"`, currently `task_status: done`) MUST be renumbered to the next free slot (proposed: `026`).
- `tasks/009-review-pr28-readme-spec/` (the *later* claimer of `task_id: "009"`, currently `task_status: in_progress`) MUST be renumbered to the next free slot (proposed: `027`).

The slugs MUST remain stable across the renumber per TASK.md §8.1; only the folder prefix and the `task_id` field change.

## Plan

1. **Lock current free slots.** `ls tasks/ | sort | tail` immediately before staging; if 026/027 are taken, pick the next free pair.
2. **Rename folders.**
   - `git mv tasks/006-skills-navigation-bootstrap tasks/026-skills-navigation-bootstrap`
   - `git mv tasks/009-review-pr28-readme-spec tasks/027-review-pr28-readme-spec`
3. **Update `task_id` fields.** Use `tools/fm/edit.py --set task_id="026"` and `--set task_id="027"`; bump `updated:` on the same call.
4. **Sweep cross-references.** `grep -rn "tasks/006-skills-navigation-bootstrap\|tasks/009-review-pr28-readme-spec"` and update every hit. Also sweep frontmatter references in `task_supersedes`, `task_superseded_by`, `task_blocked_by` lists across all tasks.
5. **Re-run linters.** `python3 tools/lint-linkage.py && python3 tools/fm/validate.py` MUST exit zero on the affected tree.
6. **Append run-log entry.** Document the renumber in `maintenance/run-log.md` per the previous renumber precedent (run-log entry 2026-05-04 session zVZBH).

## Todo

- [x] 1. Verify 065/066 (next-free at staging time; 026/027 long since claimed) are unclaimed.
- [x] 2. Rename `006-skills-navigation-bootstrap` → `065-skills-navigation-bootstrap`; update `task_id` to `"065"`.
- [x] 3. Rename `009-review-pr28-readme-spec` → `066-review-pr28-readme-spec`; update `task_id` to `"066"`.
- [x] 4. Sweep cross-references (`task_affects_paths`, `tasks/readme.md` bullets, in-folder self-references). Backtick prose mentions in T4-immutable closed research left intact per MAINTENANCE.md §1.0.1 (no markdown links were broken).
- [x] 5. Run `tools/check-governance.sh`; PASS.
- [x] 6. Append `maintenance/run-log.md` entry; produce `friction-log.md` with FL declaration.

## Links

- Predecessor: [`../013-renumber-duplicate-task-ids/task.md`](../013-renumber-duplicate-task-ids/task.md)
- Spec rule: [`TASK.md §8.1`](../../TASK.md)
- Renumber precedent: `maintenance/run-log.md` entry 2026-05-04 (claude-code session zVZBH).
- Governing specs: [`TASK.md`](../../TASK.md), [`MAINTENANCE.md`](../../MAINTENANCE.md)
