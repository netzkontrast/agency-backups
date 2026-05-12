---
type: index
status: active
slug: port-external-skill-corpora
summary: "Directory index for Task 091 Epic — port SuperClaude_Framework v4.3.0 + Superpowers v4.0.3 skill corpora into /skills/ under vendor-prefixed namespaces per ADR-0011. Two sequential subtasks: ST-1 corpus + ST-2 hookup."
created: 2026-05-12
updated: 2026-05-12
---

# Task 091 — Port External Skill Corpora (Epic)

**What:** Epic umbrella for the Phase 1 execution of [ADR-0011](../../decisions/0011-external-skill-corpora-import.md). Resolves the five dangling `/sc:*` references in [`CLAUDE.md §13`](../../CLAUDE.md) and the remote-URL citation in [`AGENTS.md` Closing Run Procedure](../../AGENTS.md#closing-run-procedure) by porting 14 SuperClaude skills (5 commands + 9 supporting agents) into `skills/sc-*/` under the policy ratified in ADR-0011. Contains no code diffs itself — diffs land via two sequential subtasks.

**Why here:** Per [TASK.md §2](../../TASK.md), every coordination unit lives in `/tasks/<NNN>-<slug>/`. The Phase 1 work spans `tools/fm/validate.py` (new `skill_source` L2 key + 2 diagnostics), 14 new `skills/sc-*/` folders (corpus), and two root-spec edits (AGENTS.md + RESEARCH.md hookup). Splitting into ST-1 (corpus) + ST-2 (hookup) keeps each PR independently reviewable; ST-2 depends on ST-1 being merged because the AGENTS.md rewrite cites a path materialized only by ST-1.

## Navigation

- [task.md](./task.md) — Epic spec: Goal, Context, Plan, Todo, Acceptance, Links.
- [subtasks/](./subtasks/) — ST-1 (corpus) + ST-2 (hookup) briefs.
  - [subtasks/readme.md](./subtasks/readme.md) — subtask index with sequencing.
  - [subtasks/01-phase-1-corpus.md](./subtasks/01-phase-1-corpus.md) — validator extension + 14 skill folders.
  - [subtasks/02-phase-1-hookup.md](./subtasks/02-phase-1-hookup.md) — AGENTS.md + RESEARCH.md citation rewrite.
- [references/](./references/) — Complete planning record (4-part 83 KB document).
  - [references/readme.md](./references/readme.md) — plan index.
  - [references/full-plan-part-1.md](./references/full-plan-part-1.md) — editorial note + context + §1 recap + §2/§3 upstream catalogs.
  - [references/full-plan-part-2.md](./references/full-plan-part-2.md) — §4 porting policy (now ADR-0011) + §5 task scaffolds + §6 critical files + §7 verification + §8 out-of-scope.
  - [references/full-plan-part-3.md](./references/full-plan-part-3.md) — §9 brainstorm refinement (execution requirements + 5 resolved open questions).
  - [references/full-plan-part-4.md](./references/full-plan-part-4.md) — §10 design specifications (ADR detail + validator extension + per-skill SKILL.md design + root-spec citation diffs + Task A/B → ST-1/ST-2 scaffolds + verification recipe).

## Assumptions Log

- The 14-item Phase 1 batch (per `references/full-plan-part-1.md` §2.1 and `references/full-plan-part-4.md` §10.3) is the minimum viable cut to close the dangling references in `CLAUDE.md §13`. Phase 2 (`/sc:troubleshoot`, `/sc:cleanup`, `/sc:document`, `/sc:explain`, plus the Superpowers corpus) is deferred to a follow-up Epic; not blocking the dangling-reference fix.
- The originally-numbered `ADR-0010` was renumbered post-hoc to `ADR-0011` due to a slot collision with [`decisions/0010-novel-architect-error-tier-linter-policy.md`](../../decisions/0010-novel-architect-error-tier-linter-policy.md) (created the same day, indexed only in the same PR session). The renumber preserved all content verbatim. See PR #107 description for the audit trail.
- The Epic was originally filed as **Task 090** and renumbered to **Task 091** when this branch was synced with `main`. Main had two pre-existing `tasks/090-*` folders ([`090-codex-pr-review`](../090-codex-pr-review/) and [`090-review-pr109-archive-spec`](../090-review-pr109-archive-spec/)) both claiming `task_id: "090"` — itself a `TASK.md §8.1` duplicate awaiting a renumber-Task on main. Taking the next free slot (091) avoided compounding the duplicate into a triple-collision.
- `skill_source` pin format is **tag only** (`superclaude@v4.3.0`, `superpowers@v4.0.3`) per `references/full-plan-part-3.md` §9.7 OQ5 resolution. Tag-rot risk acknowledged; mitigations listed in ADR-0011 F2 falsifier trigger.
