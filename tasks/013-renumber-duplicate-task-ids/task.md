---
type: task
status: active
slug: renumber-duplicate-task-ids
summary: "Found by coherence check 2026-05-05: two pairs of tasks share task_id values (006 and 009), violating TASK.md §8.1."
created: 2026-05-05
updated: 2026-05-05
task_id: "013"
task_status: updated
task_owner: "claude-code"
task_priority: P2
task_uses_prompts: []
task_spawns_research: []
task_spawns_prompts: []
task_superseded_by:
  - "024"
task_affects_paths:
  - tasks/006-skills-navigation-bootstrap/
  - tasks/006-surface-skills-architecture/
  - tasks/009-author-skills-root-spec/
  - tasks/009-review-pr28-readme-spec/
  - tasks/readme.md
  - maintenance/run-log.md
---

# Task 013 — Renumber Duplicate `task_id` Values

## Goal

The repository MUST have unique `task_id` values across `/tasks/`. Today two pairs collide:

- `tasks/006-skills-navigation-bootstrap/` (`task_id: "006"`, created 15:09:04 UTC, `task_status: done`)
- `tasks/006-surface-skills-architecture/` (`task_id: "006"`, claimed at 14:23:05 UTC by the previous coherence run)
- `tasks/009-author-skills-root-spec/` (`task_id: "009"`, created 15:03:15 UTC)
- `tasks/009-review-pr28-readme-spec/` (`task_id: "009"`, created 15:04:00 UTC)

Per `TASK.md §8.1`, the later claimer MUST renumber to the next free `<NNN>`; the slug stays stable, only the folder prefix and the `task_id` field change.

The conformant end state is: every `task.md` carries a unique `task_id`, the folder name reflects the new prefix, and every reference to the old prefix in cross-linked files is updated.

## Plan

1. Rename `tasks/006-skills-navigation-bootstrap/` → `tasks/014-skills-navigation-bootstrap/`; update `task_id: "014"` in `task.md`. (Newer claimer of 006.)
2. Rename `tasks/009-review-pr28-readme-spec/` → `tasks/015-review-pr28-readme-spec/`; update `task_id: "015"` in `task.md`. (Newer claimer of 009.)
3. Sweep cross-references with `grep -rn "tasks/006-skills-navigation-bootstrap\|tasks/009-review-pr28-readme-spec"` and update every hit (path-form references only — slug-only references are stable).
4. Re-run `tools/check-governance.sh`; the linter MUST pass.
5. Append a note to `maintenance/run-log.md` recording the renumber.

## Todo

- [ ] Choose final new IDs (013/014/015) — the choice MUST keep slugs stable per TASK.md §8.1.
- [ ] Rename the two folders and update `task_id` in each `task.md`.
- [ ] Update all cross-references in `tasks/readme.md`, `tasks/008-harden-coherence-baseline-protocol/notes.md`, prompts that path-link to the renamed folders, and any research workspace that references them.
- [ ] Re-run `tools/check-governance.sh` and confirm zero diagnostics.
- [ ] Add a `friction-log.md` recording any FL[0-3] friction encountered.

## Links

- Found by: coherence check `maintenance/run-log.md` entry 2026-05-05.
- Spec rule: [`TASK.md §8.1`](../../TASK.md).
- Prior renumber precedent: run-log entry 2026-05-04 (claude-code session zVZBH) renamed `tasks/003-surface-skills-architecture/` → `tasks/006-surface-skills-architecture/`.
