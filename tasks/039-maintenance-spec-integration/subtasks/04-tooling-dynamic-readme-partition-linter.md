---
type: note
status: draft
slug: task-039-st4-tooling-dynamic-readme-partition-linter
summary: "Subtask ST-4: ship tools/maintenance/dynamic-readme-partition.py implementing the static/dynamic partition rule from research/repo-maintenance-protocol-spec/output/SPEC.md §3.1."
created: 2026-05-06
updated: 2026-05-06
---

# ST-4: `dynamic-readme-partition` — Operationalizes repo-maintenance-protocol-spec §3.1

**Executor:** maintenance-agent

**Insertion point:** `[opt]` WARN-tier — runs over operational-folder readmes only; advisory.

## Goal

Ship `tools/maintenance/dynamic-readme-partition.py` that scans operational-folder `readme.md` files and verifies the static/dynamic section partition: static sections (Purpose, Navigation, Assumptions Log) live above the `<!-- BEGIN DYNAMIC -->` marker; dynamic sections (Current State, Recent Activity, Open Blockers) live below. Closes the orphaning of `repo-maintenance-protocol-spec/output/SPEC.md §3.1`.

## Falsification

Wrong cut **iff** existing readmes have no markers and the linter retroactively breaks them. Mitigation: WARN-tier only; readmes lacking markers emit a one-time "consider partitioning" diagnostic, never an ERROR.

## Inputs

- `research/repo-maintenance-protocol-spec/output/SPEC.md` §3.1 (partition rule).
- All operational-folder `readme.md` (test corpus).
- `tools/fm/extract.py --section`.

## Acceptance Criteria

1. **Surface.** `python3 tools/maintenance/dynamic-readme-partition.py [<paths>]`.
2. **Heuristic.** Detect `<!-- BEGIN DYNAMIC -->` / `<!-- END DYNAMIC -->` marker pair; verify section-name allocation per the static/dynamic taxonomy.
3. **Diagnostic format.** `<relpath>::WARN:M.B.6:<missing-marker|misplaced-section>:<details>`.
4. **Tests.** `tests/maintenance/test_dynamic_readme_partition.py` covers: partitioned readme (pass), no-markers (advisory warn), section-in-wrong-half (warn).
5. **Integration.** WARN-tier `[opt]` in `tools/check-governance.sh`.

## Dependencies

None. Phase A.

## Estimated Effort

Medium (~120 LOC + 100 LOC tests).
