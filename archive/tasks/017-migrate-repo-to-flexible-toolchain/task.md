---
type: task
status: archived
slug: migrate-repo-to-flexible-toolchain
summary: "Migrate the agency repo onto the flexible-frontmatter toolchain shipped by Task 016: bump-updated all operational files, retire the legacy validators, flip the FM_TOOLCHAIN feature flag default, and narrow Task 010 to a stateless query CLI."
created: 2026-05-05
updated: 2026-05-12
task_id: "017"
task_status: archived
task_owner: "claude-code"
task_priority: P2
task_uses_prompts:
  - migrate-repo-to-flexible-toolchain
task_spawns_research: []
task_spawns_prompts: []
task_affects_paths:
  - tools/check-governance.sh
  - tools/legacy/
  - tools/validate-frontmatter.py
  - tools/lint-structure.py
  - tools/lint-linkage.py
  - tools/_frontmatter.py
  - tools/check-maintenance-bypass.py
  - .githooks/pre-commit
  - MAINTENANCE.md
  - PRE_COMMIT.md
  - prompts/repo-coherence-check/prompt.md
  - tasks/010-skills-frontmatter-index-suite/task.md
---

# Task 017 — Migrate the Repo to the Flexible Frontmatter Toolchain

## Goal

The migration is `done` when (a) `tools/check-governance.sh` decides exit codes via `fm-validate` (with `FM_TOOLCHAIN=1` as the default), (b) the four legacy linters live under `tools/legacy/` for one release and are removed in a final cleanup commit, (c) every operational file passes `fm-validate` without `--strict`, and (d) `tasks/010-skills-frontmatter-index-suite/task.md` has been amended to drop the persisted index and keep only the query CLI surface (per `research/flexible-frontmatter-toolchain/reflection/M07-contradiction-log.md §C1`).

This Task is `blocked` until Task 016 ships the toolchain.

## Plan

Three batches per SPEC §8.

### Batch 1 — Mechanical (T1, automatable)

1. Run `tools/fm/edit.py --bump-updated` over every operational file the migration touches; commit in a single audit-friendly commit.
2. Re-export the legacy validators from `tools/legacy/` (move + add a deprecation banner). The originals at `tools/validate-frontmatter.py`, `tools/lint-structure.py`, `tools/lint-linkage.py` become thin shims for one release window.

### Batch 2 — Additive (T2, automatable with review)

3. Flip `FM_TOOLCHAIN=1` in `tools/check-governance.sh` so `fm-validate` decides exit codes. Keep the legacy validators running side-by-side for diff-comparison; surface any disagreement as a WARN (not a fail).
4. Re-point `tools/check-maintenance-bypass.py` at `fm-validate`'s diagnostic format (per SPEC §7.3).
5. Update `.githooks/pre-commit` to call `tools/check-governance.sh --delta` (the new delta-aware mode from Task 016 step 8).

### Batch 3 — Structural (T3, requires Task review)

6. Amend `MAINTENANCE.md §3.2` and `PRE_COMMIT.md §7` to reference `fm-validate` as the canonical linter; preserve the T1/T2/T3/T4 ladder verbatim.
7. Amend `prompts/repo-coherence-check/prompt.md` to add a "Step 2.5 — Linter-First Triage" that uses `fm-query missing-key=…` (Task 014 finding F3).
8. Narrow `tasks/010-skills-frontmatter-index-suite/task.md`: drop `.agent_cache/frontmatter-index.json`; keep the ten-question CLI surface but re-target it to `fm-query`. Update the friction-log of Task 010 to point at SPEC §C1 for the rationale.
9. Final cleanup commit: remove `tools/legacy/`. Verify `tools/check-governance.sh` still exits 0.

## Todo

- [x] 1. Confirm Task 016 is `done` (gate; this task is `blocked` until then).
- [x] 2. Batch 1: `fm-edit --bump-updated` sweep + commit.
- [x] 3. Batch 1: move legacy validators to `tools/legacy/` with deprecation banner.
- [x] 4. Batch 2: flip `FM_TOOLCHAIN=1`; verify side-by-side run is silent.
- [x] 5. Batch 2: re-point `check-maintenance-bypass.py`.
- [x] 6. Batch 2: switch `.githooks/pre-commit` to `--delta`.
- [x] 7. Batch 3: amend `MAINTENANCE.md §3.2` + `PRE_COMMIT.md §7` (T3 — file as a sub-task if review is contentious).
- [x] 8. Batch 3: amend `prompts/repo-coherence-check/prompt.md` Step 2.5.
- [x] 9. Batch 3: scope-narrow Task 010 per SPEC §C1; cross-reference back to this task.
- [x] 10. Resolve SPEC §10 Q3 (programmatic API for non-Python callers) in `notes.md`.
- [x] 11. Final commit: remove `tools/legacy/`; rerun `tools/check-governance.sh`.
- [x] 12. Set `task_status: done`, `updated:`; write `friction-log.md`; append `maintenance/run-log.md`.

## Links

- Source SPEC: [`/research/flexible-frontmatter-toolchain/output/SPEC.md`](../../research/flexible-frontmatter-toolchain/output/SPEC.md)
- Executing prompt: [`/prompts/migrate-repo-to-flexible-toolchain/prompt.md`](../../prompts/migrate-repo-to-flexible-toolchain/prompt.md)
- Hard dependency: [`/tasks/016-flexible-frontmatter-toolchain/`](../016-flexible-frontmatter-toolchain/)
- Adjacent (scope-narrowed by §C1): [`/tasks/010-skills-frontmatter-index-suite/`](../010-skills-frontmatter-index-suite/)
- Adjacent (informs Step 2.5): [`/tasks/014-improve-maintenance-spec-from-session/`](../014-improve-maintenance-spec-from-session/)
- Governing specs: [`MAINTENANCE.md`](../../MAINTENANCE.md), [`PRE_COMMIT.md`](../../PRE_COMMIT.md), [`TASK.md`](../../TASK.md)
