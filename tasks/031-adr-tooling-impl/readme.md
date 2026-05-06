---
type: index
status: active
slug: adr-tooling-impl
summary: "Index for Task 031 — implementation successor to Task 028 (plan-only). Lands the agency-adr CLI suite, the test suite, the GitHub Actions workflow, the governance hook integration, and the AGENTS.md guarded-section markers per the build contract in tasks/028-adr-tooling-impl-plan/implementation-plan.md."
created: 2026-05-06
updated: 2026-05-06
---

# Task 031 — ADR Tooling Implementation

## What and Why

Task 028 produced an "interface contracts yes, working code no" implementation plan. The prompt that drove it explicitly listed `tools/adr/*.py`, the test fixtures, and the GitHub Actions YAML as **non-goals**. Task 031 is the natural successor — it executes the build contract end-to-end on a `claude/<topic>-<date>` branch and merges via `/sc:createPR`.

This Task was authored after the implementation work was already pushed (PR [#67](https://github.com/netzkontrast/agency/pull/67)), to satisfy the governance findings in [`../028-adr-tooling-impl-plan/pr67-review.md`](../028-adr-tooling-impl-plan/pr67-review.md) (G.1: missing Task entry; G.2: missing prompt artifact). The Task remains `in_progress` until PR #67's CI is green and the merge lands; on merge, `task_status` flips to `done` and the friction log is finalised.

## Linked Navigation

- [`task.md`](./task.md) — Goal, Plan, Todo (15 done items + 2 outstanding), and Links.
- [`friction-log.md`](./friction-log.md) — In-progress friction log; FL2 declared (so far). Promoted to a closure log on merge.
- Predecessor Task: [`../028-adr-tooling-impl-plan/`](../028-adr-tooling-impl-plan/) — `task_status: done`. Owns the build contract.
- Build contract: [`../028-adr-tooling-impl-plan/implementation-plan.md`](../028-adr-tooling-impl-plan/implementation-plan.md) — §1–§7 specification.
- PR #67 review: [`../028-adr-tooling-impl-plan/pr67-review.md`](../028-adr-tooling-impl-plan/pr67-review.md) — five-finding governance + technical review; T.1–T.4 addressed in commit `6a30991`, G.1 + G.2 addressed in this Task.
- Task-spec prompt: [`../../prompts/adr-tooling-impl/prompt.md`](../../prompts/adr-tooling-impl/prompt.md) — the executable instruction set this Task carries out.
- Implementation surface: [`../../tools/adr/`](../../tools/adr/) (CLI), [`../../tests/adr/`](../../tests/adr/) (tests), [`../../.github/workflows/adr-validate.yml`](../../.github/workflows/adr-validate.yml) (CI).
