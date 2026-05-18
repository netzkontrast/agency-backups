---
type: index
status: active
slug: improve-maintenance-spec-may-18-2026-readme
summary: "Index for Task 096 — Improve Maintenance Spec from 2026-05-18 Coherence Run. Companion (not successor) to open Tasks 025 / 044 / 064 in the same lineage."
created: 2026-05-18
updated: 2026-05-18
---

# Task 096 — Improve Maintenance Spec (2026-05-18 Coherence Run)

## What and Why

This Task carries the seven findings (F27–F33) distilled from the 2026-05-18 Repo Coherence Check session (see [`maintenance/run-log.md`](../../maintenance/run-log.md) entry for `Run 2026-05-18`). The Goal is to land each finding as a concrete diff against [`MAINTENANCE.md`](../../MAINTENANCE.md), [`prompts/repo-coherence-check/prompt.md`](../../prompts/repo-coherence-check/prompt.md), or [`tools/adr/cli.py`](../../tools/adr/cli.py) — or record a `won't-fix` disposition with rationale. The Task crosses the T3 (Structural) repair tier per [`MAINTENANCE.md §1`](../../MAINTENANCE.md) (root-spec edits across >3 files) and MUST execute the [TASK.md §4.9](../../TASK.md#49-planning-pipeline-for-t3-structural-tasks-sc-ladder) `/sc:analyze → /sc:brainstorm → /sc:design → /sc:workflow` planning ladder before writing detailed implementation diffs.

## Linked Navigation

- [`task.md`](./task.md) — Goal, Findings (F27–F33), Plan, Todo.
- (Future) `friction-log.md` — closure log; created at `task_status: done | updated | abandoned`.
- (Future) `workflow.md` — `/sc:workflow` artefact per T.4.9.2.
- (Future) `notes.md` — running notes, including the F21 falsification dynamic.

## Assumptions Log

- The seven findings F27–F33 are session-distilled from the 2026-05-18 coherence run and have been triaged against Task 044 F14 (overlap is orthogonal: F14 = canonical form, F27 = tier classification) and Task 064 F21 / F23 / F26 (cited as cross-cutting precedents, not duplicates).
- Filing this fourth open `improve-maintenance-spec-*` Task IS the falsification evidence for Task 064 F21's proposed one-open-Task cadence rule. The Task 096 owner SHOULD reference this dynamic when prioritising whether to land F21 ahead of F27–F33.
- The findings target MAINTENANCE.md prose plus one tool (`tools/adr/cli.py`) and one prompt (`prompts/repo-coherence-check/prompt.md`). No new linters, no schema changes.
- P2 priority — clarity improvements to a working system, not gate-blocking defects.
