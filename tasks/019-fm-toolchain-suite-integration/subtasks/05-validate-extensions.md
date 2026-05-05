---
type: note
status: draft
slug: task-019-st5-validate-extensions
summary: "Subtask ST-5: extend tools/fm/validate.py with --explain (per-code rationale), --baseline (only show new diagnostics relative to a git ref), and --type-check (cross-file slug resolution). Unblocks ST-6 (legacy-linter retirement)."
created: 2026-05-05
updated: 2026-05-05
---

# ST-5: `fm-validate` Extensions — `--explain`, `--baseline`, `--type-check`

## Goal

Add three flags to `tools/fm/validate.py`:

- `--explain` emits a human-readable rationale and a remediation hint for each diagnostic code, sourced from a side JSON file so the explanations stay close to the codes themselves.
- `--baseline <git-ref>` shows only diagnostics for *newly introduced* violations (compared to the named git ref). Critical for incremental adoption — landing a new validator without a flag-day breaks every CI run.
- `--type-check` performs cross-file slug resolution: every list-valued reference (e.g. `task_uses_prompts: [foo]`) MUST resolve to an existing operational file. Required before ST-6 can rewrite the legacy linkage linter.

## Falsification

Wrong cut **iff** `--explain` becomes a documentation-maintenance burden divorced from the validator. Mitigation: explanations live in `maintenance/schemas/diagnostic-explanations.json`, reviewed alongside the SPEC; CI fails if a code is emitted without a matching explanation entry.

## Inputs

- [`/tools/fm/validate.py`](../../../tools/fm/validate.py).
- [`/research/flexible-frontmatter-toolchain/output/SPEC.md`](../../../research/flexible-frontmatter-toolchain/output/SPEC.md) §5.1 (diagnostic codes).
- [`/maintenance/schemas/header-ontology.json`](../../../maintenance/schemas/header-ontology.json) — defines list-valued L2 keys whose targets must resolve.

## Acceptance Criteria

1. **`--explain`.** New flag. When set with no other flags, prints the explanation table for every known F.* code and exits 0. When set alongside a normal validation run, each diagnostic line is followed (in `--format=text`) by a wrapped paragraph from the explanations table. JSON output adds an `explanation` field per diagnostic.
2. **`--baseline <git-ref>`.** New flag. Runs validation against HEAD AND `<git-ref>`; emits only diagnostics that exist in HEAD but not in `<git-ref>`. Implementation: collect (path, line, code, message) tuples; set-difference. Tolerates the missing ref with a clear stderr message and falls back to whole-tree validation.
3. **`--type-check`.** New flag. For every list-valued L2 key referencing a slug, verify the target slug resolves to an operational file. Emit `F.T.1` (target missing), `F.T.2` (reciprocity broken: A references B but B doesn't reference A back where reciprocity is required by the ontology).
4. **Diagnostic-explanation file.** Author `maintenance/schemas/diagnostic-explanations.json` with one entry per known F.* code: `{code, severity_hint, what, why, fix}`. Cover F.3.1, F.3.2, F.3.3, F.3.4, F.4.2, F.B.1, F.B.2, F.B.3, F.B.4, F.B.5, F.B.6, F.B.7, F.T.1, F.T.2.
5. **Tests.** Extend `tests/fm/test_validate.py` (or add `test_validate_extensions.py`). Cover each new flag; cover the explanation-coverage CI guard (every emitted code MUST have a matching explanation).
6. **Backwards compatibility.** All existing 64 tests still pass. New flags default off.

## Dependencies

None. Phase A. ST-6 depends on this subtask (specifically `--type-check`).

## Estimated Effort

Medium (~150 LOC across validate.py + new JSON + ~120 LOC tests).

## Agent Prompt

```text
You are extending tools/fm/validate.py for the netzkontrast/agency repo on
branch claude/execute-task-16-ZrBJe.

Repo root: /home/user/agency

Context files (read first):
  - tools/fm/validate.py
  - tools/fm/_core.py
  - tools/fm/query.py                        (model the cross-file scan)
  - research/flexible-frontmatter-toolchain/output/SPEC.md  (§5.1, §12.4)
  - maintenance/schemas/header-ontology.json
  - tests/fm/test_validate.py                (extend or sibling-add)

Acceptance criteria:
  1. --explain : print rationale per emitted diagnostic, sourced from
     maintenance/schemas/diagnostic-explanations.json (new file you create).
  2. --baseline <git-ref> : compute set-difference of (path,line,code,message)
     between HEAD and <git-ref>. Use `git show <ref>:<path>` for the baseline
     read; tolerate missing ref with a stderr warning.
  3. --type-check : new code family F.T.* — F.T.1 dangling reference,
     F.T.2 reciprocity break.
  4. New JSON file maintenance/schemas/diagnostic-explanations.json with
     entries for: F.3.1, F.3.2, F.3.3, F.3.4, F.4.2, F.B.1–F.B.7, F.T.1, F.T.2.
     Schema per entry: {code, severity_hint, what, why, fix}.
  5. CI guard: a unit test that emits every F.* code from a fixture and
     verifies each is present in diagnostic-explanations.json.
  6. All existing 64 tests still pass.

Constraints:
  - Python 3.11 stdlib only.
  - --baseline shells out to git via subprocess; no GitPython.
  - Reciprocity rules: task_uses_prompts ↔ prompt_relates_to_task; prompt
    references research via prompt_spawned_from_research, etc. Use the
    ontology to drive this — do NOT hardcode the rules in Python.

When done:
  - python3 -m unittest discover -s tests/fm -t .
  - python3 tools/validate-frontmatter.py
  - Smoke: python3 tools/fm/validate.py --explain | head -20
  - Smoke: python3 tools/fm/validate.py --type-check tasks/016-flexible-frontmatter-toolchain/
  Commit "feat(fm/validate): --explain, --baseline, --type-check (Task 019 ST-5)".
  Do NOT push.
```
