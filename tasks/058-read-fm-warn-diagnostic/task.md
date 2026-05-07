---
type: task
status: active
slug: read-fm-warn-diagnostic
summary: "Make tools/fm/_core.py read_fm() emit a WARN-tier Diag when strict=False parsing of a non-empty file collapses to an empty dict, so downstream linters can distinguish 'no frontmatter' from 'malformed frontmatter'."
created: 2026-05-07
updated: 2026-05-07
task_id: "058"
task_status: open
task_owner: "unassigned"
task_priority: P2
task_uses_prompts: []
task_spawns_research: []
task_spawns_prompts: []
task_blocked_by: []
task_supersedes: []
task_superseded_by: []
task_affects_paths:
  - tools/fm/_core.py
  - tools/fm/validate.py
  - tests/fm/test_core.py
  - tests/fm/test_falsification_attacks.py
---

# Task 058 — `read_fm` WARN Diagnostic on Silent `{}`

## Goal

`tools/fm/_core.py:145-149` `read_fm()` swallows `OSError` and `Diag` and returns `{}`. A file with malformed frontmatter ends up indistinguishable from a file with no frontmatter, and downstream linters report misleading "missing key" errors instead of "parse error". The single falsifiable outcome of this Task: a fixture file with malformed YAML emits a `WARN` (or `ERROR` under `--strict`) with the parse error message — not a cascade of "missing key" diagnostics.

## Plan

1. **Choose** the surface change. Two options to evaluate in `notes.md`:
   - (a) Make `read_fm` emit a WARN `Diag` directly via a module-level diagnostic sink; or
   - (b) Add a second return value (`tuple[dict, Diag | None]`) so callers can decide whether to surface or suppress.
   Pick one with a one-paragraph rationale.
2. **Implement** the chosen surface change in `tools/fm/_core.py`; thread it into `tools/fm/validate.py` so the WARN reaches the user.
3. **Add** a falsification fixture under `tests/fm/test_falsification_attacks.py`: a file with `---\nkey: [unbalanced\n---\n# body` MUST produce a parse-error diagnostic (cite the diagnostic code), NOT a "missing required key `type`" diagnostic.
4. **Verify** existing tests still pass; add unit coverage for the empty-file, missing-frontmatter, and malformed-frontmatter cases as three distinct expected outcomes.

## Todo

- [ ] Decide surface (a) vs (b); record rationale in `notes.md`.
- [ ] Implement chosen surface in `tools/fm/_core.py`.
- [ ] Thread WARN into `tools/fm/validate.py`.
- [ ] Add falsification fixture covering malformed YAML.
- [ ] Add three-way unit coverage (empty / no-fm / malformed-fm).
- [ ] Run `pytest tests/fm/` clean.
- [ ] Write `friction-log.md` with FL[0–3] declaration on closure.

## Links

- Parent dispatch: [Task 053](../053-core-architecture-review-followups/) finding B.7.
- Affected lines at branch-time: [`tools/fm/_core.py:145-149`](../../tools/fm/_core.py).
- Reference: [`tests/fm/test_falsification_attacks.py`](../../tests/fm/test_falsification_attacks.py) — existing P-series adversarial tests.
