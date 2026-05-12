---
type: index
status: active
slug: task-092-references
summary: "References directory for Task 092 (Phase 2 skill-corpora port). ST-1 populated this folder with triage-matrix.md (81-row decision matrix) and triage-notes/ rationale files; ST-2 + ST-3 read it as input."
created: 2026-05-12
updated: 2026-05-12
---

# Task 092 — References

**What:** Container for the ST-1 triage outputs. ST-1 authored two artifact families here:

- [`triage-matrix.md`](./triage-matrix.md) — single canonical decision matrix; one row per snapshot candidate. Columns: `# | Snapshot path | Proposed Agency slug | Tier | Decision | ADR-0011 clauses | Rationale`. **Counts:** port = 18, adapt = 24, skip = 39 (total 81 rows; satisfies AC T092.1.4 ≥ 75).
- [`triage-notes/`](./triage-notes/) — per-skill rationale where one matrix line could not capture the decision. **21 notes** providing complete coverage of all port + adapt rows + skip rationales.

### SuperClaude_Framework triage notes

- [`triage-notes/sc-pure-ports-cluster.md`](./triage-notes/sc-pure-ports-cluster.md) — 9 mechanical-port rows (analyze, design, document + 6 agents); shared port recipe.
- [`triage-notes/sc-light-mcp-adapts.md`](./triage-notes/sc-light-mcp-adapts.md) — 5 light-MCP adapt rows (build, cleanup, estimate, explain, index); shared strip pattern.
- [`triage-notes/sc-brainstorm.md`](./triage-notes/sc-brainstorm.md) — heavy 6-MCP adapt for `commands/brainstorm.md`.
- [`triage-notes/sc-business-panel.md`](./triage-notes/sc-business-panel.md) — command + agent + mode trio consolidation strategy.
- [`triage-notes/sc-serena-trio.md`](./triage-notes/sc-serena-trio.md) — Serena→Agency filesystem rewrite for load/save/reflect.
- [`triage-notes/sc-spec-panel.md`](./triage-notes/sc-spec-panel.md) — 18 KB body + 11-expert extraction plan.
- [`triage-notes/sc-task-workflow.md`](./triage-notes/sc-task-workflow.md) — heavy 6-MCP adapt pair (sc-task + sc-workflow).
- [`triage-notes/sc-socratic-mentor.md`](./triage-notes/sc-socratic-mentor.md) — 12 KB body + Sequential strip + book-corpus extraction.
- [`triage-notes/sc-troubleshoot.md`](./triage-notes/sc-troubleshoot.md) — deconfliction with `superpowers-systematic-debugging`.
- [`triage-notes/sc-modes-bundling.md`](./triage-notes/sc-modes-bundling.md) — mode→host-skill `references/` bundling strategy (Phase 1 precedent).
- [`triage-notes/superclaude-confidence-check.md`](./triage-notes/superclaude-confidence-check.md) — 4 snapshot copies, D.7 audit required at ST-2.

### Superpowers triage notes

- [`triage-notes/superpowers-discipline-cluster.md`](./triage-notes/superpowers-discipline-cluster.md) — 4-skill discipline-gates cluster (TDD, systematic-debug, verification, receiving-review).
- [`triage-notes/superpowers-orchestration-cluster.md`](./triage-notes/superpowers-orchestration-cluster.md) — 6-artefact orchestration cluster; Agent-tool re-binding.
- [`triage-notes/superpowers-brainstorming.md`](./triage-notes/superpowers-brainstorming.md) — deconfliction with `sc-brainstorm` + `sc-requirements-analyst`.
- [`triage-notes/superpowers-finishing-a-branch.md`](./triage-notes/superpowers-finishing-a-branch.md) — overlaps Closing Run Procedure; adds discard option.
- [`triage-notes/superpowers-git-worktrees.md`](./triage-notes/superpowers-git-worktrees.md) — 5.6 KB body; worked-example extraction.
- [`triage-notes/superpowers-using-superpowers.md`](./triage-notes/superpowers-using-superpowers.md) — meta-skill rewrite for Skill-tool semantics.
- [`triage-notes/superpowers-writing-skills.md`](./triage-notes/superpowers-writing-skills.md) — 22 KB body, heavy `references/` extraction.
- [`triage-notes/superpowers-hooks-skip.md`](./triage-notes/superpowers-hooks-skip.md) — D.7 rationale for all 3 hook files (skip).

### Cross-cutting notes

- [`triage-notes/skip-rationale-summary.md`](./triage-notes/skip-rationale-summary.md) — 6-class roll-up covering all 39 skip rows.
- [`triage-notes/validator-touchpoints.md`](./triage-notes/validator-touchpoints.md) — ST-2/3 cheat sheet on `tools/fm/validate.py` diagnostics + ADR-0012 dependency.

**Why here:** Per [TASK.md §3.4](../../../TASK.md) `task_spawns_research: []` (Task 092 does not spawn an external research workspace), so triage outputs live inside the Task folder. The decision matrix is the source of truth that ST-2 + ST-3 consume.

## Anti-patterns avoided (ST-1 audit)

- No external upstream blob-URL citations (AC T092.1.3 — every source path resolves under `tasks/091-…/references/upstream-snapshot/`).
- No `/skills/` writes during ST-1 (read-only triage scope).
- No re-evaluation of the 14 Phase-1 ports.

## Assumptions Log

- Triage citations MUST resolve to local paths under `tasks/091-…/references/upstream-snapshot/` — per [Task 092 Note](../task.md#note--internal-research-only), external GitHub URLs are an anti-pattern for this Epic.
- Once ST-2 and ST-3 close, the matrix becomes historical — it documents the rationale for what shipped and what was skipped, but the source of truth for "what is a Phase 2 skill" shifts to `/skills/sc-*/` and `/skills/superpowers-*/`. The matrix MUST NOT be edited after ST-4 closes (effectively T4 once the Epic is `done`).
- Body-byte counts cited in the matrix's "Rationale" column are subagent-reported approximations; ST-2 / ST-3 MUST re-measure against `tools/fm/validate.py` body-cap diagnostics (per [decisions/0012](../../../decisions/) when Accepted) before merge.
- Tier (L1–L4) is ST-1's best-effort estimate; ST-2 / ST-3 MAY re-tier as porting reveals concrete `skill_references_skills` edges.
