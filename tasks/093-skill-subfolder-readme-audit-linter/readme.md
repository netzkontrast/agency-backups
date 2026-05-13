---
type: index
status: active
slug: skill-subfolder-readme-audit-linter
summary: "Directory index for Task 093 — close the SKILLS.md §9.6 readme-audit enforcement gap surfaced by Task 091 ST-1 peer review."
created: 2026-05-12
updated: 2026-05-13
---

# Task 093 — Skill-subfolder readme-audit linter

**What:** Maintenance Task that closes a real tooling gap: governance currently does not flag missing `readme.md` files inside `skills/<slug>/` subfolders, even though [CLAUDE.md §7](../../CLAUDE.md) and [SKILLS.md §9.6](../../SKILLS.md) require them. Task 091 ST-1 was able to ship 14 `skills/sc-*/` without `readme.md` and `tools/check-governance.sh` still exited 0 — the peer review caught it manually.

**Why here:** Surfaced as Observation 1 in [`tasks/091-…/review-st1.md`](../091-port-external-skill-corpora/review-st1.md) during the Task 091 ST-1 peer review. Filed as low-priority (P3) maintenance because the manual catch already resolved Task 091's instance, but the next batch (Task 092 ~75 candidates) benefits from mechanical enforcement.

**Single-subtask Task** — small surface area (validator extension + tests + diagnostic registry entry). No subtasks/ folder needed.

## Navigation

- [task.md](./task.md) — Goal, Plan, Todo, Acceptance Criteria (T093.1.1–T093.1.3).
- [friction-log.md](./friction-log.md) — Session friction log (FL1: sibling sandbox tests required a stub readme.md patch).

## Assumptions Log

- The natural diagnostic code prefix for skill-structural checks is `F.S.*` (mirroring `F.B.*` for `skill_*` frontmatter keys). `F.S.1` is suggested for the missing-readme check; the implementer MAY choose a different code if it conflicts with an existing rule.
- The check belongs in the Flexible toolchain (`tools/fm/validate.py`), not the deprecation shim (`tools/lint-structure.py`). PRE_COMMIT.md §7.A makes the Flexible path canonical.
- Regression-test coverage MUST include every existing `skills/<slug>/` to confirm the rule has zero false positives on `main`.
