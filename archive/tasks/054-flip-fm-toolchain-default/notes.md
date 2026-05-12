---
type: note
status: active
slug: 054-flip-fm-toolchain-default-notes
summary: "Parity audit + scope-narrowing notes for the FM_TOOLCHAIN retirement. Legacy shims kept on disk because tools/check-maintenance-bypass.py still reads them."
created: 2026-05-08
updated: 2026-05-08
---

# Task 054 — Notes

## Parity Audit Summary

The legacy frontmatter validator (`tools/legacy/validate-frontmatter.py`)
and the linkage shim (`tools/legacy/lint-linkage.py`) overlap with
`tools/fm/validate.py` (and `--type-check`) on every diagnostic the gate
emits. The structural rule shim (`tools/legacy/lint-structure.py`)
remains the canonical implementation for required-files-per-folder
checks; `tools/lint-structure.py` (a shim that delegates to the
legacy script) is still wired into step `[2/6]` of
`tools/check-governance.sh`. That is independent of the
`FM_TOOLCHAIN` flip and is out of scope here.

## Scope Narrowing

The Task description listed retirement of all four legacy linter
scripts. We narrowed scope to the falsifiable outcome named in the
Goal: "FM_TOOLCHAIN is removed from check-governance.sh,
`tools/fm/validate.py` is the only frontmatter validator invoked".

Reasons the legacy shims stay on disk:

- `tools/check-maintenance-bypass.py:69-70` still calls
  `tools/legacy/lint-structure.py` and `tools/legacy/lint-linkage.py`
  to harvest the structural and cross-reference diagnostics that
  `fm-validate` does not yet emit. Removing the scripts breaks the
  bypass index (PR-blocking).
- The legacy shims are referenced from spec docs (TASK.md, RESEARCH.md,
  PROMPT.md, SKILLS.md, FOLDERS.md, README.md) as the canonical paths.
  Renaming or deleting them is a T3 cross-spec edit that requires its
  own Task — see follow-up below.

## Verification

- `tools/check-governance.sh` (no env vars set) → PASS at the close-out
  commit. `[1/6] Frontmatter linter (fm-validate --type-check)` runs
  unconditionally; no advisory legacy invocation.
- `grep -n FM_TOOLCHAIN tools/check-governance.sh PRE_COMMIT.md MAINTENANCE.md .githooks/pre-commit`
  returns only retirement-mention lines — no env-var read.

## Follow-ups (out of scope here)

- File a Task to fold `lint-structure.py` and `lint-linkage.py` rules
  into `fm-validate` so `tools/check-maintenance-bypass.py` no longer
  needs them, then delete the legacy scripts and update spec docs.
- File a Task to rewrite the spec-doc references from
  `tools/lint-linkage.py` → `tools/fm/validate.py --type-check` and
  from `tools/validate-frontmatter.py` → `tools/fm/validate.py`.
