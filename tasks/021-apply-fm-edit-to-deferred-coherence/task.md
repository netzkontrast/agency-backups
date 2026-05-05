---
type: task
status: active
slug: apply-fm-edit-to-deferred-coherence
summary: "Successor to Task 005. Apply the deferred T1/T2 frontmatter stubs across the corpus using the canonical mutator tools/fm/edit.py shipped by Task 016, replacing the legacy hand-rolled approach implied by the original Task."
created: 2026-05-05
updated: 2026-05-05
task_id: "021"
task_status: done
task_owner: "claude-code"
task_priority: P3
task_uses_prompts: []
task_spawns_research: []
task_spawns_prompts: []
task_supersedes:
  - 005
task_blocked_by:
  - 017
task_affects_paths:
  - research/
  - skills/
  - tools/fm/edit.py
---

# Task 021 — Apply fm-edit to Deferred Coherence Stubs

Successor to [Task 005](../005-address-deferred-coherence-issues/task.md). The original Task pre-dated the flexible-frontmatter toolchain (Task 016). Today the canonical mutator is [`tools/fm/edit.py`](../../tools/fm/edit.py) — per [`MAINTENANCE.md §1`](../../MAINTENANCE.md), it is the only sanctioned tool for T1/T2 frontmatter mutations because it preserves body bytes and quoting and takes a file lock. Task 005's plan ("Systematically batch-update missing stubs") gives no instruction on *how* — that gap is closed by Task 017's migration; this Task picks up the residual files Task 017 does not auto-cover.

## Goal

`python3 tools/fm/validate.py` returns zero `F.3.1` / `F.3.2` (missing-key) diagnostics across `/research/`, `/skills/`, and any other operational tree the migration leaves behind. Each fix MUST be a single `tools/fm/edit.py` invocation; no hand-edited YAML.

## Plan

1. **Wait for Task 017.** This Task is `task_blocked_by: ['017']` — Task 017 migrates the bulk corpus and bumps `updated:` for every operational file. Run only after 017 reports `done`.
2. **Capture the residual.** `python3 tools/fm/validate.py 2>&1 | grep -E "F.3.[12]"` over the post-migration tree.
3. **Group by directory.** Cluster missing-key errors by their immediate parent (typically nested research workspaces). Apply `tools/fm/edit.py --set <key>=<derived-value>` per file using `--bump-updated` on the same call.
4. **Avoid T3 escalation.** If a file's `type:` cannot be derived from path classification (per [`header-ontology.json`](../../maintenance/schemas/header-ontology.json) `path_classification`), add a `notes.md` entry and stop — do NOT guess. Escalate as a child Task per `TASK.md §8.5`.
5. **Verify.** Re-run `tools/check-governance.sh`; the validator MUST exit zero on the swept paths.

## Todo

- [x] 1. Confirm Task 017 has `task_status: done` before transitioning to `in_progress`.
- [x] 2. Capture the residual `F.3.1`/`F.3.2` diagnostic list into `notes.md`.
- [x] 3. Apply `tools/fm/edit.py` mutations in tier-1 batches; one commit per logical group. *(No-op — residual was empty post-Task-017; see `notes.md` and `friction-log.md`.)*
- [x] 4. Verify clean validator run; produce `friction-log.md` with FL[0-3]. *(FL1; `python3 tools/fm/validate.py` → 0 diagnostics across 252 files.)*

## Closure Note

Closed 2026-05-05 with `task_status: done`. Residual F.3.1/F.3.2 diagnostic count at run start: **zero**. Task 017's migration (followed by Task 019/020 toolchain and RISEN+ReAct work) cleared the missing-key class entirely; this Task acts as the confirmation gate per `MAINTENANCE.md §1`. See [`notes.md`](./notes.md) for the residual capture and [`friction-log.md`](./friction-log.md) for FL1 reasoning.

## Links

- Predecessor: [`../005-address-deferred-coherence-issues/task.md`](../005-address-deferred-coherence-issues/task.md)
- Canonical mutator: [`tools/fm/edit.py`](../../tools/fm/edit.py)
- Blocker (now `done`): [`../017-migrate-repo-to-flexible-toolchain/task.md`](../017-migrate-repo-to-flexible-toolchain/task.md)
- Governing specs: [`TASK.md`](../../TASK.md), [`MAINTENANCE.md`](../../MAINTENANCE.md) §1
- Closure artifacts: [`notes.md`](./notes.md), [`friction-log.md`](./friction-log.md)
