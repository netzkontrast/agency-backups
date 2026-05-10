---
type: note
status: active
slug: task-064-friction-log
summary: "Friction log for Task 064 filing during the 2026-05-10 coherence run."
created: 2026-05-10
updated: 2026-05-10
---

# Task 064 — Friction Log

Highest Frustration Level: FL1

## What landed

Filed Task 064 by the 2026-05-10 coherence run after `python3 tools/fm/validate.py --check-body` surfaced 2 pre-existing F.B.1 ERRORs against `tasks/039-maintenance-spec-integration/task.md` that the gate did not block on (because `--check-body` is not wired into `tools/check-governance.sh`).

## Friction (FL1)

- **F1 — Dead forward reference.** `prompts/repo-coherence-check/prompt.md §Step 2.5` says `When --check-body lands as default-on (Task 019), promote here`. Task 019 closed weeks ago; the forward reference rotted. The promotion never landed and the comment is the only reason a coherence agent might think the gating wiring is pending. The correct cleanup is to drop the parenthetical and promote the line.
- **F2 — Tier-classification gap on closed Tasks.** `MAINTENANCE.md §1`'s repair-tier table covers heading renames (T3) and frontmatter mutations (T1/T2) but does not address body-shape repairs on `task_status: done` files. The 2 F.B.1 ERRORs on the closed Task 039 sit in the gap: not a frontmatter mutation (so not T1/T2), not a heading rename (so not obviously T3 by the table). The classification needs an explicit row.

## Falsification clause

If the new gating step in `tools/check-governance.sh` adds more than ~250ms to the pre-commit gate on a 391-file scan, the wiring is wrong (it should reuse the existing `--type-check` walk rather than re-walking the corpus). Measure with `time tools/check-governance.sh` before and after.

## Recommendation

The Task 064 plan addresses both F1 and F2 in the same commit. No separate Task needed.
