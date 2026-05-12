---
type: note
status: draft
slug: task-019-st8-fm-cli-wrapper
summary: "Subtask ST-8: ship a single `fm` entry point with subcommands (fm validate/extract/edit/query/section/rename/graph/new/fix). Sequential — depends on every Phase A subtask landing first."
created: 2026-05-05
updated: 2026-05-05
---

# ST-8: Single `fm` CLI Wrapper

## Goal

Replace `python3 tools/fm/<name>.py …` with `fm <name> …` — one entry point, lazy subcommand dispatch, no import-time cost beyond what's strictly needed for the invoked subcommand. Improves discoverability (`fm --help` lists the suite) and makes packaging trivially possible.

## Falsification

Wrong cut **iff** the unified wrapper introduces import latency that breaks the per-invocation budget. Mitigation: lazy import — the wrapper only imports the subcommand module that's actually invoked, never all of them.

## Inputs

- All Phase A subcommands: validate, extract, edit, query, section (Task 018), rename (ST-1), graph (ST-2), new (ST-3), fix (ST-4).
- Existing per-tool `main(argv)` functions (the API contract Task 016 established).

## Acceptance Criteria

1. **Entry point.** `tools/fm/fm.py` with a CLI that dispatches: `fm <subcommand> [args...]`. Subcommand names match the existing per-tool module names (`validate`, `extract`, `edit`, `query`, `section`, `rename`, `graph`, `new`, `fix`).
2. **Lazy imports.** The dispatcher MUST import only the requested subcommand module, never the full set. Verify with a test that monkey-patches `importlib.import_module` and asserts only one call per invocation.
3. **`fm --help`** lists every subcommand with its one-line summary (sourced from each module's `__doc__`).
4. **Existing per-module entry points keep working.** `python3 tools/fm/validate.py …` still functions.
5. **Optional installable script.** Add a `tools/fm/__main__.py` so `python -m tools.fm <subcommand>` also works. This is the path used by future `pip install` wrappers.
6. **Cookbook update (loose coupling with ST-7).** Append a "Single-command entry" section showing `fm validate` instead of `python3 tools/fm/validate.py`.
7. **Tests.** New file `tests/fm/test_fm_wrapper.py`. Cover: each subcommand dispatches correctly; `fm --help` lists every subcommand; lazy-import invariant holds; unknown subcommand exits 2 with a helpful list.

## Dependencies

**All Phase A subtasks (ST-1 through ST-7) must be merged first.** This is the integration step.

## Estimated Effort

Medium (~120 LOC + 100 LOC tests + small README touch).

## Agent Prompt

```text
You are implementing tools/fm/fm.py for the netzkontrast/agency repo on
branch claude/execute-task-16-ZrBJe. ST-1..ST-5 + ST-7 are already merged;
Task 018 (fm-section) is also merged.

Repo root: /home/user/agency

Context files (read first):
  - tools/fm/__init__.py
  - tools/fm/validate.py        (note the main(argv) contract)
  - tools/fm/extract.py
  - tools/fm/edit.py
  - tools/fm/query.py
  - tools/fm/section.py         (from Task 018)
  - tools/fm/rename.py          (from ST-1)
  - tools/fm/graph.py           (from ST-2)
  - tools/fm/new.py             (from ST-3)
  - tools/fm/fix.py             (from ST-4)

Acceptance criteria:
  1. tools/fm/fm.py with dispatcher: `fm <subcommand> <args...>`
     Each subcommand maps to a module's main(argv) function.
  2. tools/fm/__main__.py so `python3 -m tools.fm <subcommand>` works.
  3. Lazy imports: when invoked with `fm validate ...`, only validate.py
     gets imported. Use importlib at dispatch time.
  4. fm --help lists every subcommand with the first line of its docstring.
  5. tools/fm/validate.py and the others CONTINUE to work standalone via
     `python3 tools/fm/validate.py …`. Do NOT break the existing entry
     points.
  6. tests/fm/test_fm_wrapper.py:
       - dispatch test for each subcommand
       - --help format test
       - lazy-import invariant (monkey-patch importlib, count imports)
       - unknown subcommand → exit 2 + "did you mean" list

Constraints:
  - Python 3.11 stdlib only.
  - Do NOT touch other tools/fm/*.py files except to add the docstring
    summary on line 1 if missing (T1 fix).

When done:
  - python3 -m unittest discover -s tests/fm -t .
  - python3 -m tools.fm validate    (smoke)
  - python3 tools/fm/fm.py extract --help
  Commit "feat(fm): single `fm` wrapper with lazy subcommand dispatch (Task 019 ST-8)".
  Do NOT push.
```
