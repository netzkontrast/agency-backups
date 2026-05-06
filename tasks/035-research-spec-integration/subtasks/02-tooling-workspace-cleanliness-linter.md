---
type: note
status: draft
slug: task-035-st2-tooling-workspace-cleanliness-linter
summary: "Subtask ST-2: ship tools/check-workspace-cleanliness.py — closes the R.4.4 enforcement gap by scanning /research/<slug>/workspace/ for stragglers (.py/.sh/.log) at commit time."
created: 2026-05-06
updated: 2026-05-06
---

# ST-2: `check-workspace-cleanliness` — Closes RESEARCH.md R.4.4 Gap

**Executor:** main-agent

**Insertion point:** `[opt]` WARN-tier — runs over changed `/research/<slug>/workspace/` paths only.

**Parallelism:** Phase A (parallel) — runs concurrently with ST-1, ST-3, ST-4. No inter-dependencies.

## Goal

Ship `tools/check-workspace-cleanliness.py` that scans staged `/research/<slug>/workspace/` paths for execution-script stragglers (`.py`, `.sh`, `.log`) and emits a WARN diagnostic. Closes the R.4.4 enforcement gap (currently human-review only).

## Falsification

Wrong cut **iff** legitimate `.py` files for the worked-example need to live under `/workspace/` long-term. Mitigation: the linter accepts a `.cleanignore` file at the workspace root listing exempt paths with rationale.

## Inputs

- `RESEARCH.md` R.4.4 (rule statement).
- `tools/fm/_core.py` (path iteration helpers).
- `tools/adr/runlog.py` (diagnostic format prior art).

## Acceptance Criteria

1. **Surface.** `python3 tools/check-workspace-cleanliness.py [<paths>]` (defaults to scanning `research/`).
2. **Heuristic.** Flag any `.py`/`.sh`/`.log` under `/research/<slug>/workspace/`; honour `.cleanignore`.
3. **Diagnostic format.** `<relpath>::WARN:R.4.4:execution-script-not-cleaned`.
4. **Tests.** `tests/test_workspace_cleanliness.py` covers: clean workspace, straggler `.py`, ignored path, missing-workspace edge case.
5. **Integration.** `tools/check-governance.sh` runs WARN-tier.

## Dependencies

None. Phase A.

## Estimated Effort

Small (~80 LOC + 60 LOC tests).
