---
type: note
status: draft
slug: task-048-st2-research-existing-task-tooling-inventory
summary: "ST-2 (research head): catalogue every existing `/tools/` script that touches `/tasks/`, classify by lifecycle stage (TASK.md §4), surface gaps against TASK.md §3 / §4 / §7 / §8, and produce the inventory + gap analysis ST-3 consumes for SPEC synthesis."
created: 2026-05-07
updated: 2026-05-11
---

# ST-2: Research — Existing `/tasks/`-side Tooling Inventory + Gap Analysis

**Executor:** main-agent or deep-research subagent.

**Parallelism:** Phase A (parallel) — runs concurrently with ST-1. No inter-dependencies.

## Goal

Produce a structured inventory of every `/tools/` script that touches `/tasks/`, classify each by TASK.md lifecycle stage, and produce a gap analysis showing which TASK.md normative clauses lack mechanical enforcement. The output is consumed by ST-3 as the gap-coverage column of every proposed tool.

## Inputs

- `/home/user/agency/tools/` — full tree. Notable: `fm/`, `adr/`, `dramatica-nav/`, `tests/`, plus root `check-*.py` and `lint-*.py`.
- `/home/user/agency/TASK.md` — §3 (ontology), §4 (lifecycle), §7 (pre-commit), §8 (edge cases). Every normative clause is an enforcement candidate.
- `/home/user/agency/tools/check-governance.sh` — current orchestration of the tooling pipeline.
- `/home/user/agency/.githooks/pre-commit` — current pre-commit gate.
- `/home/user/agency/maintenance/schemas/header-ontology.json` — the schema every existing tool consumes.
- Recent friction-logs that flag tooling gaps:
  - `tasks/033-task-spec-integration/friction-log.md` — duplicate-id linter advisory-by-default rationale; ST-4 helper migration pending.
  - `tasks/068-improve-maintenance-spec-may-2026/friction-log.md` — assumption-log + RFC-2119 polarity tooling.
  - `tasks/067-sync-tasks-index-status-drift/friction-log.md` — index_diff design notes.

## Acceptance Criteria

1. Output at `research/task-tooling-impl-spec/workspace/02-tooling-inventory.md`.
2. **§A** Inventory table listing every script under `tools/` whose surface touches `/tasks/` (≥12 expected: `fm/validate.py`, `fm/edit.py`, `fm/query.py`, `fm/extract.py`, `fm/section.py`, `fm/rename.py`, `fm/fix.py`, `fm/graph.py`, `fm/index_diff.py`, `fm/check-duplicate-task-id.py`, `fm/check-task-lifecycle-classification.py`, `lint-runlog.py`, `check-trust.py`, `check-maintenance-bypass.py`, etc). Each row: script path, one-line purpose, integration point (pre-commit / manual / both), and the TASK.md anchor it enforces (or "—" if it's a generic FM tool).
3. **§B** Lifecycle-coverage matrix: for each TASK.md §4 lifecycle transition (`open → in_progress`, `in_progress → blocked`, `blocked → in_progress`, `in_progress → done`, `in_progress → updated`, `in_progress → abandoned`, `* → renumbered`), name the tool that mechanically gates it (or "—" if no mechanical gate exists).
4. **§C** Gap analysis listing **≥6** unmet TASK.md normative clauses — each with: clause anchor, why no current tool covers it, falsification signal (what would surface that the gap matters), and a *priority score* (`P1` / `P2` / `P3`) for SPEC inclusion.
5. **§D** Composability assessment: does the existing tooling compose into a `task-create` / `task-transition` / `task-close` workflow, or do agents currently stitch these together by hand? Cite specific friction-log evidence.

## Falsification

Wrong cut **iff** fewer than 6 unmet normative clauses surface (would mean the existing toolchain is feature-complete and a SPEC adds no value). Mitigation: TASK.md §4.7 alone has 4 conditions of which only 2 are mechanically checked by ST-4's helper; §8.7 cycle prohibition is unenforced; §7.5 path containment is human-review; §4.8 lineage annotation is partial. The floor of 6 unmet clauses is well-cleared at audit-time.

## Dependencies

None. Phase A.

## Estimated Effort

Medium (~2–3 hours; tool inventory + clause-by-clause cross-check).
