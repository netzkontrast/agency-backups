---
type: index
status: active
slug: task-001-refactor-governance-from-specs
summary: "Folder index for Task 001: encode the rules from Spec-A/B/C, G/H/I, and J/K/L into mechanically-enforced repository governance."
created: 2026-05-04
updated: 2026-05-04
status: completed
---

# Task 001 — Folder Index

**What is this folder?** The orchestration workspace for Task 001. It holds the task spec, optional running notes, and (on closure) a friction log.

**Why is it here?** Task 001 is the first instance of the new `/tasks/` orchestration layer introduced by the architecture refactor on 2026-05-04. It is also the meta-task that converts the theoretical research specs (A/B/C, G/H/I, J/K/L) into enforced repository rules.

## Contents

- [`task.md`](./task.md) — The task spec: frontmatter, Goal, Plan, Todo, Links. **Status: done.**
- [`friction-log.md`](./friction-log.md) — FL1 friction log per `FRUSTRATED.md`.

## Workflow Assumptions

- The executing prompt lives at [`/prompts/refactor-governance-from-specs/prompt.md`](../../prompts/refactor-governance-from-specs/prompt.md).
- Running notes would go in `notes.md`; none were needed for this task.
- This task delivered: `tools/lint-structure.py`, `tools/lint-linkage.py`, `tools/check-trust.py`, `tools/check-governance.sh`, `.githooks/pre-commit`, `templates/notes.md`, updated `PRE_COMMIT.md`, and retrofitted frontmatter on 14 pre-existing research files.
