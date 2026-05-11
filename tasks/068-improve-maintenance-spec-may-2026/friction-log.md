---
type: note
status: active
slug: task-032-friction-log
summary: "Friction log for Task 032 (improve-maintenance-spec-may-2026). Records the disposition of each finding F8–F13 and any session-level friction encountered while landing the diffs."
created: 2026-05-07
updated: 2026-05-07
---

# Task 032 — Friction Log

**FL1**

## Per-Finding Disposition

| Finding | Disposition | Reference |
|---|---|---|
| F8 — `tools/check-governance.sh` FAIL on missing optional `jsonschema` | **landed** | `tools/dramatica-nav/validate.py` now WARNs and exits 0 when `jsonschema` is absent (alternative path of F8); MAINTENANCE.md §5.1 added to document it as a soft prerequisite. The preferred path (install.sh pin) was already implicitly satisfied by `tools/requirements.txt` carrying `jsonschema>=4.18` and `install.sh` running `pip install -r tools/requirements.txt`; the gap was that contributors who skip `./install.sh` see the misleading FAIL. The graceful-degrade closes that gap without forcing the run-cost on contributors who are not exercising the narrative-ontology validator. |
| F9 — Run-log mixes coherence vs task-implementation records | **landed** | `routine_type:` field added to `maintenance/run-log.md`'s "Record Format" block with enum `bootstrap | coherence-check | nightly-maintenance | task-implementation`. Backfilled across all 13 existing records. MAINTENANCE.md §2.3 amended to call out the four record types and the awk-fall-forward semantics. |
| F10 — Coherence prompt has no post-repair linter gate | **delegated to Task 025** | Task 025 §Plan-4 already owns the same diff (insert "Step 4.5 — Verify Linters Pass" between Step 4 and Step 5). Task 025 was previously blocked by Task 019; Task 019 is now `done`, so Task 025 is unblockable. Recording the delegation here per the Task 032 plan ("recommend Task 025 since it was filed first"). No diff to the coherence prompt landed under this Task. |
| F11 — TASK.md §7.11 mechanical-check promise was deferred | **landed (already)** | `TASK.md §7.0` row §7.11 already cites `tools/fm/index_diff.py` and links to Task 031, which closed and shipped the linter (verified at HEAD; see `maintenance/run-log.md` 2026-05-07 Task 031 implementation record). Added a one-line MAINTENANCE.md §3.4 note pointing the Stale-Task Audit at the §7.11 mechanical surface so the cross-reference is bidirectional. |
| F12 — `MAINTENANCE.md §1.1` describes a coexistence state that no longer exists | **landed** | §1.1 rewritten for the post-migration state: fm-validate canonical and gating, legacy validators advisory shims at `tools/legacy/` silenced by `FM_LEGACY_QUIET=1`, `FM_TOOLCHAIN=0` documented as an escape hatch but not the supported configuration. The `tools/.frontmatter-waivers` paragraph dropped — the file does not exist on disk and Task 017 Batch 2c re-pointed `tools/check-maintenance-bypass.py` at fm-validate's diagnostic stream rather than a path-list waiver mechanism. §4.1 prose extended to describe `check-maintenance-bypass.py`'s post-Task-017 behaviour. |
| F13 — Cross-branch duplicate-task_id check missing from coherence prompt | **landed** | Coherence prompt Step 4 now requires both the local `ls tasks/` check and the cross-branch `git ls-tree origin/main` check before staging a new Task folder, with a direct cross-reference to TASK.md §8.1 bullet 2 and the recurring Tasks 013 / 024 / 043 lineage. |

## Session Friction

**FL1** — minor friction, two notes:

1. **F11 was already done.** The 2026-05-07 Task 031 implementation amended TASK.md §7.0 row §7.11 to cite `tools/fm/index_diff.py` and Task 031, which is exactly the diff this Task's F11 plan called for. The remaining work was bidirectional cross-referencing (MAINTENANCE.md §3.4 → §7.11), not the original retarget. Not a blocker — the Task 032 plan already anticipated this kind of overlap by classifying findings as `landed` / `delegated` / `won't-fix`.

2. **The duplicate `task_id: "032"` collision is unresolved at close time.** This Task folder shares `task_id: "032"` with `tasks/032-agents-spec-integration/`. Task 043 (renumber-duplicate-task-ids-v3) is the dedicated fix and proposes renumbering this folder to `046` — but slot `046` is now also claimed by `tasks/046-github-workflow-research/` (filed after Task 043), so Task 043's plan will need to pick the next free pair at staging. None of that affects Task 032's findings landing; the renumber is mechanical follow-up tracked separately.

## Closure Note

All six findings have either a landed diff in this branch or a recorded disposition above (one delegation to Task 025, one acknowledgement that F11 already shipped under Task 031). Per `task.md` Goal: "The Task closes only when every finding has either a landed diff or a recorded disposition."
