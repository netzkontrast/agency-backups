---
type: prompt
status: active
slug: migrate-repo-to-flexible-toolchain
summary: "Migration prompt for Task 017: cut the agency repo over from the four legacy linters to the flexible-frontmatter toolchain (Task 016) in three batches per SPEC §8 — mechanical, additive, structural."
created: 2026-05-05
updated: 2026-05-05
prompt_kind: task-spec
prompt_framework: RISEN+ReAct
prompt_target_agent: "Claude Code"
prompt_relates_to_task: "migrate-repo-to-flexible-toolchain"
prompt_spawned_from_research: "flexible-frontmatter-toolchain"
---

# Migrate the Repo to the Flexible Frontmatter Toolchain — Migration Prompt

## Framework

**RISEN + ReAct.** Migrations are inherently observational; ReAct's Observe step matters because Batch 2's side-by-side comparison surfaces silent disagreements between the legacy validators and `fm-validate`.

## R — Role

You are a release-engineering coordinator. You move the repo from one validator to another *without breaking pre-commit for any contributor*. You commit in small audit-friendly steps and never delete a working tool until its replacement has run silently for a release window.

## I — Input

- `/research/flexible-frontmatter-toolchain/output/SPEC.md` — the contract; §7 (Integration) and §8 (Migration Ladder) drive this prompt.
- `/tasks/017-migrate-repo-to-flexible-toolchain/task.md` — the three-batch plan and todo.
- `/research/flexible-frontmatter-toolchain/reflection/M07-contradiction-log.md` — explains why Task 010 must be scope-narrowed during Batch 3.
- `/tools/check-governance.sh`, `/.githooks/pre-commit`, `/tools/check-maintenance-bypass.py` — the surfaces this migration rebinds.
- `/MAINTENANCE.md`, `/PRE_COMMIT.md` — the prose specs amended in Batch 3.

## S — Steps

1. The migrator MUST verify Task 016 is `task_status: done` before any Batch begins. If not, the migration MUST exit 0 with no changes and a one-line note in `friction-log.md`.
2. The migrator MUST execute Batch 1 (mechanical) in a dedicated commit: a `fm-edit --bump-updated` sweep, plus a move of the four legacy linters into `tools/legacy/` with a deprecation banner header in each.
3. The migrator MUST execute Batch 2 (additive) in two commits: (a) flip `FM_TOOLCHAIN=1` in `tools/check-governance.sh`; (b) re-point `tools/check-maintenance-bypass.py` and `.githooks/pre-commit`.
4. After Batch 2, the migrator MUST run `tools/check-governance.sh` with both validators side-by-side and verify zero disagreements. Any disagreement MUST be triaged — disagreements that surface a real bug in `fm-validate` send the migration back to Task 016 with a friction note.
5. The migrator MUST execute Batch 3 (structural) only after Batch 2's comparison commit is clean. Batch 3 amends `MAINTENANCE.md §3.2` and `PRE_COMMIT.md §7` — these are T3 changes per the Tier ladder, so the amendments MUST be reviewed by a maintainer (a sub-task is acceptable if review is contentious).
6. The migrator MUST scope-narrow `tasks/010-skills-frontmatter-index-suite/task.md` per SPEC §C1: remove the persisted-index deliverables, keep the ten-question CLI surface, redirect the implementation onto `fm-query`. Update the friction-log of Task 010 with a backlink to SPEC §C1.
7. The migrator MUST add the "Step 2.5 — Linter-First Triage" to `prompts/repo-coherence-check/prompt.md` per Task 014 finding F3, citing the new `fm-query` selectors.
8. The migrator MUST run `tools/check-governance.sh` clean after each commit, and MUST NOT remove `tools/legacy/` until every step above is complete.
9. The migrator MUST close with a `friction-log.md` declaring FL[0–3] and append the migration entries to `maintenance/run-log.md` per `MAINTENANCE.md §2.3`.

## E — Expectations

- A series of small, audit-friendly commits — one per Batch step — each leaving `tools/check-governance.sh` clean.
- `tools/legacy/` deleted in the final cleanup commit (only after every other step succeeds).
- `MAINTENANCE.md`, `PRE_COMMIT.md`, `tasks/010-skills-frontmatter-index-suite/task.md`, and `prompts/repo-coherence-check/prompt.md` amended per the plan.
- `tasks/017-migrate-repo-to-flexible-toolchain/friction-log.md` declaring FL[0–3].
- A multi-line append to `maintenance/run-log.md` summarising the migration window.

## Constraints

- **Never bypass `tools/check-governance.sh`.** Every commit MUST exit 0.
- **No `--no-verify`, no force-pushes** on `main`. The migration is reversible by `git revert`.
- **Side-by-side first.** `FM_TOOLCHAIN=1` does not flip from "logging-only" to "deciding" until the comparison commit is clean.
- **`tools/legacy/` is sacred until Step 8.** Premature deletion is a rollback hazard.
- **Root spec amendments are T3.** If maintainer review of `MAINTENANCE.md` / `PRE_COMMIT.md` is contentious, file a sub-task and pause; do NOT push T3 changes through silently.
- **Task 010's frontmatter is updated, not orphaned.** The scope-narrow MUST keep Task 010 actionable; if the narrowing leaves it empty, mark it `done` with a note instead of deleting it.
- **No new dependencies.** This migration MUST run on the same Python 3.11 stdlib as Task 016.
