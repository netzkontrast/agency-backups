---
type: index
status: active
slug: task-091-full-plan-index
summary: "Index for the four-part complete planning record embedded as references/ for Task 091. Split for tool-call size constraints; logically one document."
created: 2026-05-12
updated: 2026-05-12
---

# Task 091 — Full Plan (Index)

The complete planning record produced during the `/sc:brainstorm` → `/sc:design` → `/sc:implement` cycle that authored Task 091. The four parts below are split for tool-call size constraints only; logically the plan is one continuous document.

Read in order:

1. [`full-plan-part-1.md`](./full-plan-part-1.md) — Editorial note + Context + §1 Recap + §2 SuperClaude inventory + §3 Superpowers inventory.
2. [`full-plan-part-2.md`](./full-plan-part-2.md) — §4 Porting policy (becomes ADR-0011) + §5 Task scaffolds + §6 Critical files + §7 Verification + §8 Out of scope.
3. [`full-plan-part-3.md`](./full-plan-part-3.md) — §9 Brainstorm refinement (execution requirements + 5 resolved open questions OQ1–OQ5).
4. [`full-plan-part-4.md`](./full-plan-part-4.md) — §10 Design specifications (ADR-0011 detailed structure + validator extension + per-skill SKILL.md design + root-spec citation diffs + Task A/B → ST-1/ST-2 scaffolds + build-order DAG + verification recipe).

The two Tasks in §10.5 ("Task A" / "Task B") are realized as **ST-1** ([`../subtasks/01-phase-1-corpus.md`](../subtasks/01-phase-1-corpus.md)) and **ST-2** ([`../subtasks/02-phase-1-hookup.md`](../subtasks/02-phase-1-hookup.md)) of this Epic.

The originally-numbered `ADR-0010` was renumbered to [`ADR-0011`](../../../decisions/0011-external-skill-corpora-import.md) post-hoc due to a slot collision with [`decisions/0010-novel-architect-error-tier-linter-policy.md`](../../../decisions/0010-novel-architect-error-tier-linter-policy.md). The renumber is detailed in the editorial note at the top of part 1.
