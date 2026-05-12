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
- [`triage-notes/`](./triage-notes/) — per-skill rationale where one matrix line could not capture the decision. Currently three notes:
  - [`triage-notes/superclaude-confidence-check.md`](./triage-notes/superclaude-confidence-check.md) — 4 snapshot copies, D.7 audit required at ST-2.
  - [`triage-notes/superpowers-using-superpowers.md`](./triage-notes/superpowers-using-superpowers.md) — meta-skill rewrite for Skill-tool semantics (ST-3).
  - [`triage-notes/superpowers-writing-skills.md`](./triage-notes/superpowers-writing-skills.md) — 22 KB body, heavy `references/` extraction needed at ST-3.

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
