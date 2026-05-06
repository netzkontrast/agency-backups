---
type: note
status: draft
slug: task-032-st3-tooling-duplicate-task-id-linter
summary: "Subtask ST-3: ship tools/fm/check-duplicate-task-id.py — a pre-commit gating linter that closes the TASK.md §8.1 acknowledged-but-unenforced gap. Detects duplicate task_id values (currently 006/006 and 009/009) and exits 1."
created: 2026-05-06
updated: 2026-05-06
---

# ST-3: `check-duplicate-task-id` — Closes TASK.md §8.1 Enforcement Gap

## Goal

Ship `tools/fm/check-duplicate-task-id.py` that scans `tasks/<NNN>-<slug>/task.md` files, extracts `task_id` from each frontmatter, and exits 1 if any value appears more than once across active (non-`updated`, non-`abandoned`) tasks. Closes the gap acknowledged in TASK.md §8.1 (lines 321–336).

## Falsification

Wrong cut **iff** the linter cannot distinguish active from `updated` predecessors. Mitigation: filter on `task_status` ∈ {open, in_progress, blocked, done} only; predecessors with `task_status: updated` are explicitly allowed to share the original id with their successor only if `task_supersedes`/`task_superseded_by` reciprocity holds.

## Inputs

- [`TASK.md`](../../../TASK.md) §8.1 (rule statement).
- [`tasks/024-renumber-duplicate-task-ids-v2/`](../../024-renumber-duplicate-task-ids-v2/) (the manual cleanup task this linter supersedes).
- `tools/fm/_core.py` (iter_operational_files, frontmatter parser).
- All current `tasks/*/task.md` (test corpus — should fail until Task 024 lands).

## Acceptance Criteria

1. **Surface.** `python3 tools/fm/check-duplicate-task-id.py [<paths>]` (defaults to scanning `tasks/`).
2. **Algorithm.**
   - Build `{task_id: [paths]}` map across active tasks.
   - For each id with `len(paths) > 1`, check whether the supersession reciprocity (predecessor.task_superseded_by ↔ successor.task_supersedes) explains it.
   - Unexplained duplicates → ERROR exit 1; explained → INFO exit 0.
3. **Tests.** `tests/fm/test_duplicate_task_id.py` covers: clean repo (pass), 006/006 collision (fail), 009/009 collision (fail), supersession-explained duplicate (pass).
4. **Integration.** Add to `tools/check-governance.sh` as ERROR-tier when `FM_TOOLCHAIN=1`; default-off in legacy mode (until the migration window closes per Task 038 ST-1).
5. **Documentation.** Cite TASK.md §8.1 in the script docstring.

## Dependencies

None. Phase A. NOTE: this linter is *expected to fail* on the current repo (006/006 and 009/009 are unresolved); that signals Task 024 is the natural unblocking work.

## Estimated Effort

Small (~100 LOC + 80 LOC tests).

## Agent Prompt

```text
Implement tools/fm/check-duplicate-task-id.py.

Repo root: /home/user/agency
Branch: claude/integrate-repo-specs-cIWtI

Read first: TASK.md §8.1, tasks/024-renumber-duplicate-task-ids-v2/task.md, tools/fm/_core.py.

Acceptance: as documented above.

Note: When you run the linter against the current repo, you SHOULD see
two ERRORs (006/006 and 009/009). Do NOT fix those; this subtask only
ships the linter. Task 024 fixes the underlying collisions.

When done:
  python3 -m unittest discover -s tests/fm
  python3 tools/fm/check-duplicate-task-id.py tasks/   # expect 2 ERRORs
  Commit "feat(tools/fm): duplicate task_id linter (Task 032 ST-3, closes TASK.md §8.1 gap)".
  Do NOT push.
```
