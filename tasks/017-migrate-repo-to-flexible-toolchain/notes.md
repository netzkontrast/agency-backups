# Notes — Task 017 (Blocked-State Reasoning)

`task_status: blocked` is declared because the migration MUST NOT begin until Task 016 sets `task_status: done`. Per `TASK.md §8.4` / Spec-I.3.1, blocked Tasks declare their blocker here.

## Blocker

- **Hard dependency:** [`/tasks/016-flexible-frontmatter-toolchain/`](../016-flexible-frontmatter-toolchain/) — Task 017 cannot run until the four CLI tools (`fm-validate`, `fm-extract`, `fm-edit`, `fm-query`) and the header-ontology JSON are in place. Concretely:
  - `fm-edit --bump-updated` is required for Batch 1.
  - `fm-validate` is the validator that flips `FM_TOOLCHAIN=1` activates in Batch 2.
  - `fm-query missing-key=…` is referenced by the Coherence-Check prompt amendment in Batch 3.

## Unblock Conditions

- `tasks/016-flexible-frontmatter-toolchain/task.md` shows `task_status: done`.
- `tools/check-governance.sh` exits 0 with `FM_TOOLCHAIN=1` set on the staged tree (Batch 2 dry-run).
- Maintainer review of the planned `MAINTENANCE.md §3.2` and `PRE_COMMIT.md §7` amendments has been recorded (T3 changes per `MAINTENANCE.md §1`).

## Risk Notes

- Removing `tools/legacy/` prematurely is a rollback hazard — the final cleanup commit is reversible only while `tools/legacy/` lives.
- Side-by-side disagreements between `fm-validate` and the legacy validator MUST be triaged into Task 016 friction notes; they are NOT to be silenced.
- Scope-narrowing Task 010 risks orphaning its `task.md` if the narrowing leaves no actionable steps. If that happens, mark Task 010 `done` with a backlink to SPEC §C1 instead of deleting it.
