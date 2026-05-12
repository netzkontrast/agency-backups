---
type: note
status: draft
slug: task-019-st6-legacy-linter-rewrite
summary: "Subtask ST-6: rewrite the legacy linters (lint-structure.py, lint-linkage.py, check-trust.py, check-maintenance-bypass.py) as thin shims around fm-* tools, then move them under tools/legacy/ behind a deprecation flag. Sequential — depends on ST-5."
created: 2026-05-05
updated: 2026-05-05
---

# ST-6: Legacy Linter Rewrite

## Goal

Replace the four legacy linters' parsing-and-graph logic with thin shims that call `fm-validate --type-check` and `fm-query`. Move the legacy `.py` files under `tools/legacy/` so the deprecation is structural, not just commented. Update `tools/check-governance.sh` to default to the fm-toolchain when `FM_TOOLCHAIN=1` is set (kept opt-in here; ST-8 + Task close flips the default).

## Falsification

Wrong cut **iff** the legacy linters do something `fm-validate --type-check` cannot replicate. Mitigation: ST-6 is gated behind ST-5 specifically because `--type-check` is the highest-risk new capability — landing it first lets ST-6 fail fast before code gets rewritten.

## Inputs

- [`/tools/lint-structure.py`](../../../tools/lint-structure.py) — file-presence checks.
- [`/tools/lint-linkage.py`](../../../tools/lint-linkage.py) — cross-reference resolution (now subsumed by `--type-check`).
- [`/tools/check-trust.py`](../../../tools/check-trust.py) — Spec-J/K/L trust audit (friction-log presence).
- [`/tools/check-maintenance-bypass.py`](../../../tools/check-maintenance-bypass.py) — bypass-mode logic.
- [`/tools/check-governance.sh`](../../../tools/check-governance.sh) — the orchestrator.

## Acceptance Criteria

1. **Move.** Every legacy linter file moves to `tools/legacy/<name>.py`. The path becomes part of the deprecation signal.
2. **Shim semantics.** Each legacy file becomes ≤ 30 lines that delegate to `fm-validate` / `fm-query`, preserving the original CLI surface so `tools/check-governance.sh` does not break.
3. **No behavioural regression.** `tools/check-governance.sh` (default mode, no `FM_TOOLCHAIN`) MUST produce the same exit code on the live tree before/after the rewrite.
4. **Tests.** New file `tests/fm/test_legacy_shims.py` that runs each legacy entrypoint and asserts the output matches a fixture captured *before* the rewrite (test-of-equivalence). Capture the fixture in the same commit.
5. **Cookbook update.** Append a "Migrating from legacy linters" section to whatever cookbook ST-7 produces.

## Dependencies

**ST-5 must be complete first** (`--type-check` is the substitute for `lint-linkage.py`). Phase B.

## Estimated Effort

Large (~80 LOC of shims + ~150 LOC test fixtures + careful cross-checks).

## Agent Prompt

```text
You are rewriting the legacy linters in the netzkontrast/agency repo on
branch claude/execute-task-16-ZrBJe. ST-5 is already merged — assume
fm-validate --type-check exists and works.

Repo root: /home/user/agency

Context files (read first):
  - tools/lint-structure.py
  - tools/lint-linkage.py
  - tools/check-trust.py
  - tools/check-maintenance-bypass.py
  - tools/check-governance.sh
  - tools/fm/validate.py            (with ST-5 extensions)
  - tools/fm/query.py
  - research/flexible-frontmatter-toolchain/output/SPEC.md  (§8 migration ladder)

Acceptance criteria:
  1. Capture a baseline of the legacy linters' output on the live tree:
     tools/check-governance.sh --no-trust > /tmp/before.txt 2>&1
  2. Move tools/{lint-structure,lint-linkage,check-trust,check-maintenance-bypass}.py
     under tools/legacy/. Keep path-based imports working by leaving a thin
     forwarder at the original path that imports from tools.legacy.
  3. Replace the moved files' parsing logic with calls to fm-validate
     (with appropriate flags) and fm-query. Each shim ≤ 30 LOC.
  4. Verify equivalence:
     tools/check-governance.sh --no-trust > /tmp/after.txt 2>&1
     diff /tmp/before.txt /tmp/after.txt   # MUST be empty
  5. tests/fm/test_legacy_shims.py asserting each shim's CLI exits with the
     same code on a known-clean fixture and on a known-dirty fixture.
  6. tools/check-governance.sh continues to gate on the legacy flow by
     default (FM_TOOLCHAIN unset). The flip to fm-* default is owned by
     the umbrella Task 019 close, NOT by this subtask.

Constraints:
  - Python 3.11 stdlib only.
  - Do NOT delete the legacy files outright — the move-with-forwarder is
    the deprecation mechanism. Deletion is a follow-up task.
  - Do NOT touch tools/fm/*.py modules (they are already at v1).

When done:
  - python3 -m unittest discover -s tests/fm -t .
  - tools/check-governance.sh --no-trust   (must pass)
  - diff /tmp/before.txt /tmp/after.txt   (must be empty)
  Commit "refactor(tools/legacy): rewrite four linters as fm-* shims (Task 019 ST-6)".
  Do NOT push.
```
