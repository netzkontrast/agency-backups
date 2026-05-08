---
type: task
status: active
slug: flip-fm-toolchain-default
summary: "Residual cleanup from Tasks 017/019: flip tools/check-governance.sh:33 default branch from legacy-as-gate to fm-as-gate, retire the four legacy linters, drop the FM_TOOLCHAIN env var."
created: 2026-05-07
updated: 2026-05-08
task_id: "054"
task_status: done
task_owner: "claude-opus-4-7"
task_priority: P2
task_uses_prompts: []
task_spawns_research: []
task_spawns_prompts: []
task_blocked_by: []
task_supersedes: []
task_superseded_by: []
task_affects_paths:
  - tools/check-governance.sh
  - tools/validate-frontmatter.py
  - tools/lint-structure.py
  - tools/lint-linkage.py
  - tools/check-trust.py
  - PRE_COMMIT.md
  - MAINTENANCE.md
  - .githooks/pre-commit
---

# Task 054 — Flip `FM_TOOLCHAIN` to default + retire legacy linters

## Goal

`tools/check-governance.sh` lines 33–48 still default to the legacy `validate-frontmatter.py` / `lint-structure.py` / `lint-linkage.py` stack and only switch to `tools/fm/validate.py` when `FM_TOOLCHAIN=1` is set. Tasks 017 and 019 closed leaving the flip pending. The single falsifiable outcome of this Task: `FM_TOOLCHAIN` is removed from `check-governance.sh`, `tools/fm/validate.py` is the only frontmatter validator invoked, and the four legacy `tools/*.py` linters are deleted (or moved to `tools/_archive/` with a deprecation note).

## Plan

1. **Audit** call-sites of the legacy linters (`grep -rn validate-frontmatter\\|lint-structure\\|lint-linkage\\|check-trust`) and confirm `tools/fm/validate.py` covers each diagnostic the legacy stack emits (use the §7.0 mapping table in `TASK.md` as the parity matrix).
2. **Flip** `tools/check-governance.sh` to call `tools/fm/validate.py` unconditionally; remove the `FM_TOOLCHAIN` branch and the advisory legacy run.
3. **Retire** the four legacy linter scripts; either delete or relocate to `tools/_archive/legacy-linters/` with a one-line `README.md` pointing at the fm-equivalent.
4. **Update** `PRE_COMMIT.md`, `MAINTENANCE.md`, and `.githooks/pre-commit` to drop every `FM_TOOLCHAIN` reference and cite the fm-suite as canonical.
5. **Verify** by running `tools/check-governance.sh` on a known-clean commit and a known-dirty fixture; both behaviours match the legacy outcome before deletion.

## Todo

- [ ] Parity audit between legacy linters and `tools/fm/validate.py` (write findings into `notes.md`).
- [ ] Edit `tools/check-governance.sh` — remove `FM_TOOLCHAIN` branch.
- [ ] Delete or archive `tools/validate-frontmatter.py`, `tools/lint-structure.py`, `tools/lint-linkage.py`, `tools/check-trust.py`.
- [ ] Sweep `PRE_COMMIT.md`, `MAINTENANCE.md`, `.githooks/pre-commit` for `FM_TOOLCHAIN` references.
- [ ] Run `tools/check-governance.sh` on clean + dirty fixtures; record results in `notes.md`.
- [ ] Write `friction-log.md` with FL[0–3] declaration on closure.

## Links

- Parent dispatch: [Task 053](../053-core-architecture-review-followups/) finding B.1 (residual gap).
- Predecessor work: [Task 017](../017-migrate-repo-to-flexible-toolchain/), [Task 019](../019-fm-toolchain-suite-integration/).
- Affected file at branch-time: [`tools/check-governance.sh`](../../tools/check-governance.sh) lines 33–48.
- Governance: [`TASK.md §7.0`](../../TASK.md) parity matrix.
