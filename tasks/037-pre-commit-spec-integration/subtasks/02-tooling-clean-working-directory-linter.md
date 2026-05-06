---
type: note
status: draft
slug: task-037-st2-tooling-clean-working-directory-linter
summary: "Subtask ST-2: ship tools/check-clean-working-directory.py — closes PC.1.1 by scanning for stray .py/.sh scratchpads at commit time. Exempts /decisions/ per FOLDERS.md §8."
created: 2026-05-06
updated: 2026-05-06
---

# ST-2: `check-clean-working-directory` — Closes PRE_COMMIT.md PC.1.1 Gap

**Executor:** main-agent

**Insertion point:** `[2/5]` directory-structure linter extension.

## Goal

Ship `tools/check-clean-working-directory.py` that scans staged paths for `.py`/`.sh` scratchpads outside designated tool/test directories. Closes PC.1.1 (currently relies on agent discipline). Exempts `/decisions/`, `/tools/`, `/tests/`, `/skills/<slug>/scripts/`, `/maintenance/scripts/` per the §8 FOLDERS.md exemption pattern.

## Falsification

Wrong cut **iff** legitimate `.py` files (e.g., a one-off migration script kept in a task's notes for audit) trigger ERROR. Mitigation: the linter accepts a per-task `.script-allowlist` file with rationale, and emits a suggestion to relocate `.py` to `/tools/<slug>/` rather than block.

## Inputs

- `PRE_COMMIT.md` PC.1.1.
- `FOLDERS.md` §8 exemption table.
- `tools/fm/_core.py`.

## Acceptance Criteria

1. **Surface.** `python3 tools/check-clean-working-directory.py [<paths>]`.
2. **Heuristic.** Flag `.py`/`.sh`/`.log` outside the §8-exempt set; honour `.script-allowlist`.
3. **Diagnostic format.** `<relpath>::WARN:PC.1.1:script-scratchpad`.
4. **Tests.** `tests/test_clean_working_directory.py` covers: clean tree, scratchpad-in-research/workspace (warn), scratchpad-in-/tools (pass), allowlisted (pass).
5. **Integration.** ERROR-tier in step `[2/5]` of `tools/check-governance.sh`.

## Dependencies

None. Phase A.

## Estimated Effort

Small (~80 LOC + 60 LOC tests).
