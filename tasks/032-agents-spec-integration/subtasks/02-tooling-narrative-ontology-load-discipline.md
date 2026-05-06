---
type: note
status: draft
slug: task-032-st2-tooling-narrative-ontology-load-discipline
summary: "Subtask ST-2: ship tools/check-narrative-ontology-load.py — a session-trace linter that warns when an agent loads /maintenance/schemas/narrative-ontology/ during non-narrative work, closing the AGENTS.md NO.5 enforcement gap."
created: 2026-05-06
updated: 2026-05-06
---

# ST-2: `check-narrative-ontology-load` — NO.5 Enforcement

## Goal

Ship `tools/check-narrative-ontology-load.py` that scans a recent session's tool-call log and emits a WARN when the 215-entry `maintenance/schemas/narrative-ontology/ontology.json` was loaded by an agent whose Task did not declare `task_affects_paths` referencing dramatica/ncp/skills folders. Closes the AGENTS.md NO.5 (§251) enforcement gap.

## Falsification

Wrong cut **iff** session-trace data is unavailable to the linter at commit time. Mitigation: tools can read the active task's frontmatter `task_affects_paths` field and the staged-files diff to infer narrative-vs-non-narrative scope without needing live tool-call traces.

## Inputs

- [`AGENTS.md`](../../../AGENTS.md) §NO.1–NO.6 (rules to enforce).
- `tools/dramatica-nav/` (existing narrative-ontology tooling).
- `maintenance/schemas/narrative-ontology/ontology.json`.
- `tools/fm/_core.py` (frontmatter parser).

## Acceptance Criteria

1. **Surface.** `python3 tools/check-narrative-ontology-load.py <task-folder>` exits 0 (no violation) or 2 (WARN — narrative ontology loaded in non-narrative task).
2. **Heuristic.** WARN when (a) the active task's `task_affects_paths` does NOT include `skills/dramatica-*` / `skills/ncp-*` / `skills/novel-*` AND (b) the staged diff shows reads against `maintenance/schemas/narrative-ontology/`.
3. **Tests.** `tests/test_narrative_ontology_load.py` covers: positive case (narrative task loads — pass), negative case (non-narrative task loads — WARN), edge case (no task context — exit 0).
4. **Integration.** Listed in `tools/check-governance.sh` as a WARN-tier check (not gating).
5. **Cookbook entry.** Add a one-line note to `tools/readme.md` describing the new linter.

## Dependencies

None. Phase A.

## Estimated Effort

Small (~80 LOC + 60 LOC tests).

## Execution Brief (for the main agent — do NOT dispatch via /sc:agent)

```text
Implement tools/check-narrative-ontology-load.py for the netzkontrast/agency
repo on branch claude/integrate-repo-specs-cIWtI.

Repo root: /home/user/agency
Read first: AGENTS.md §NO.1–NO.6, tools/fm/_core.py, tools/check-governance.sh.

Acceptance:
  1. CLI as documented.
  2. Heuristic uses task_affects_paths + git diff --cached.
  3. Tests in tests/test_narrative_ontology_load.py.
  4. Integration into tools/check-governance.sh.
  5. Cookbook note in tools/readme.md.

Constraints:
  - Python 3.11 stdlib only.
  - No git binary dependency beyond `git diff --cached --name-only`.
  - Do not gate (exit 1) — WARN-tier (exit 2) only.

When done:
  python3 -m unittest discover -s tests
  python3 tools/check-governance.sh
  Commit "feat(tools): NO.5 narrative-ontology load discipline linter (Task 032 ST-2)".
  Do NOT push.
```
