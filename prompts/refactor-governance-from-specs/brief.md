# Brief — Refactor Governance from Specs

## Raw Request

Convert the theoretical recommendations in three completed research specs (Spec-A/B/C "3-Systems SDD", Spec-G/H/I "Session Continuity", Spec-J/K/L "Eval/Trust/Improvement") into mechanically-enforced repository rules. Produce frontmatter linters, directory-structure linters, linkage validators, pre-commit hooks, and copy-and-edit templates so the next agent cannot drift from the architecture without the hook flagging it.

## Target Audience / Agent

- Primary executor: Claude Code (terminal-native agent).
- Secondary executors: any RFC-2119-aware coding agent.

## Use-Case Context

This prompt is the instruction set for [`/tasks/001-refactor-governance-from-specs/`](../../tasks/001-refactor-governance-from-specs/). It is a **task-spec** prompt — meaning it is invoked by exactly one Task and produces enforcement artifacts (linters + hooks + templates), not a research workspace.

## Spawned From

This prompt was authored alongside the introduction of the `/tasks/` orchestration layer on 2026-05-04. It is not a follow-up from a prior research run; it is a synthesis-driven task derived from the closure of three sibling research runs.

## Constraints (carry-over to `prompt.md`)

- Output enforcement scripts MUST be POSIX-shell or pure Python 3 (no heavy dependencies).
- Linters MUST exit non-zero on any violation and print a structured diagnostic.
- The pre-commit hook MUST be opt-in via `core.hooksPath` so it does not break clones that have not yet adopted the rules.
- The Task is **closed** when running the linters against the current repo produces zero diagnostics OR every remaining diagnostic has a documented waiver.
