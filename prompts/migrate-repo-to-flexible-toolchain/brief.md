# Brief — migrate-repo-to-flexible-toolchain

## Raw user request

Spawned from `/research/flexible-frontmatter-toolchain/output/SPEC.md §8` (Migration Ladder). The original user request (see `/prompts/flexible-frontmatter-toolchain/brief.md`) explicitly asks for "a new Task to Migrate the repo to this Tools". This prompt is that migration prompt.

## Target audience / intended model

- Executor: Claude Code or any equivalent release-engineering agent.
- Runtime: same Python 3.11 stdlib as Task 016. Git CLI is available in this repo's environment.

## Use-case context

- The migration Task is `/tasks/017-migrate-repo-to-flexible-toolchain/`.
- The Task is `task_status: blocked` until Task 016 reaches `task_status: done`.
- Three batches per SPEC §8: mechanical (T1) → additive (T2) → structural (T3).
- The structural batch amends MAINTENANCE.md / PRE_COMMIT.md and scope-narrows Task 010 per `M07-contradiction-log.md §C1`.

## Decisions captured before drafting

- Side-by-side validator comparison MUST run silent before flipping the default decision-maker.
- `tools/legacy/` survives until the final cleanup commit.
- Root-spec amendments are T3 — maintainer review may carve them into a sub-task.
- No `--no-verify`, no force-pushes on main; the migration is reversible by `git revert`.
