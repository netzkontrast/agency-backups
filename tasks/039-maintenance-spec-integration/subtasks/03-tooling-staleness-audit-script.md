---
type: note
status: draft
slug: task-039-st3-tooling-staleness-audit-script
summary: "Subtask ST-3: ship tools/maintenance/staleness-audit.py implementing the deterministic staleness decision tree from ST-2 SPEC. Honours MAINT_STALE_DAYS env var (default 7)."
created: 2026-05-06
updated: 2026-05-06
---

# ST-3: `staleness-audit` — MAINTENANCE.md §3.4 Mechanization

**Executor:** maintenance-agent

**Insertion point:** Not in `tools/check-governance.sh`; invoked by the nightly maintenance run only.

**Parallelism:** Phase A (parallel-grouped, soft-blocked) — runs alongside ST-1/ST-4/ST-5 but soft-depends on ST-2 SPEC. May ship with stub algorithm + upgrade post-ST-2.

## Goal

Ship `tools/maintenance/staleness-audit.py` that, given the active task corpus, assigns each open task to one of {still-accurate, drifted, completed-by-drift, no-longer-desirable} per the deterministic algorithm in ST-2's SPEC. Configurable via `MAINT_STALE_DAYS` (default 7).

## Falsification

Wrong cut **iff** the algorithm's signal-extractor recipes (from ST-2 SPEC §2) cannot be implemented in stdlib + git. Mitigation: ST-2's "≤5 signals; mechanically extractable" constraint is verified during ST-2 authoring.

## Inputs

- ST-2 output: `research/spec-staleness-decision-formalization/output/SPEC.md` §1 algorithm + §2 signals.
- `tools/fm/_core.py`, `tools/fm/query.py`.
- `tools/adr/graph.py` (cycle detection prior art for blocker chains).
- All `tasks/*/task.md` (test corpus).

## Acceptance Criteria

1. **Surface.** `python3 tools/maintenance/staleness-audit.py [--stale-days N]`.
2. **Algorithm.** Implements ST-2 SPEC §1 decision tree.
3. **Output.** Table of (task_id, current_status, bucket, evidence) — markdown for human; JSON via `--format json` for tooling.
4. **Tests.** `tests/maintenance/test_staleness_audit.py` covers each bucket using ST-2 SPEC §3 walkthroughs as fixtures.
5. **Integration.** Invoked by the nightly run; output appended to `maintenance/run-log.md`.

## Dependencies

ST-2 (research) MUST land first.

## Estimated Effort

Medium (~150 LOC + 100 LOC tests).
