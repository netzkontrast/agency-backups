---
type: index
status: active
slug: novel-architect-v120-enforcement-epic
summary: "Directory index for Task 083 — Mini-Epic umbrella for novel-architect@1.2.0 enforcement layer. Orchestrates 5 sub-tasks (084-088) that mechanize v1.1.0 prose specs into ERROR-tier linters, wire the renderer to consume the JSON validation artefact, and backport MIF L3 frontmatter."
created: 2026-05-12
updated: 2026-05-12
---

# Task 083 — novel-architect@1.2.0 Enforcement Epic

**What:** Mini-Epic umbrella for the v1.2.0 release of the `novel-architect` skill. Coordinates 5 linked sub-tasks (084-088) that close the enforcement gap left open by v1.1.0 (Epic [Task 070](../070-novel-architect-v110-epic/)) — converting prose `MUST` clauses from Tasks 072/073/075/076 into mechanically-enforced ERROR-tier linters under `tools/novel-architect-checks/`, wiring `render_architecture.py` to consume the linter's JSON artefact, and retroactively applying MIF L3 frontmatter to `skills/novel-architect/references/learnings.md`. Contains no code diffs itself — diffs land via sub-tasks.

**Why here:** Per [TASK.md §2](../../TASK.md), every coordination unit lives in `/tasks/<NNN>-<slug>/`. The v1.2.0 work spans the `tools/`-side linter family, the skill-side renderer wiring, and the skill-side MIF L3 backport; splitting into 5 sub-tasks with explicit `task_blocked_by` chains keeps each unit independently reviewable while preserving the dependency DAG (084 foundation → 085/086/087 parallel; 088 independent). Severity policy for the new linters is governed by the sibling [ADR-0010](../../decisions/0010-novel-architect-error-tier-linter-policy.md) filed alongside this Epic.

## Navigation

- [task.md](./task.md) — Epic spec: Goal, Context, Sub-Tasks table, Plan, Todo, Acceptance, Links.
- [friction-log.md](./friction-log.md) — Friction log for the scaffold session (this commit) and subsequent Epic-closure sessions.

## Assumptions Log

- (none)
