---
type: note
status: active
slug: task-093-friction-log
summary: "Friction log for Task 093. FL1: in-sandbox sibling tests for skill_bundles, skill_kind, and skill_source needed a one-line patch each to write a stub readme.md alongside SKILL.md once F.S.1 began to fire."
created: 2026-05-13
updated: 2026-05-13
---

# Task 093 — Friction Log

**Highest Frustration Level: FL1**

## Context

Task 093 extends `tools/fm/validate.py` with `_check_skill_readme()` — a new ERROR-tier check (`F.S.1`) that fires whenever a `skills/<slug>/SKILL.md` exists without a sibling `readme.md`. Adds the `F.S.1` row to `maintenance/schemas/diagnostic-explanations.json`, authors `tools/tests/fm/test_validate_skill_readme.py` covering Gherkin anchors T093.1.1 / T093.1.2 / T093.1.3, and flips the Task to `done`.

## Friction entries

### FL1.1 — Sibling sandbox tests broke until they wrote a readme.md

**What happened.** After the F.S.1 check landed, the live skills corpus stayed clean (75 SKILL.md / readme.md pairs validate at 0 diagnostics, exactly as Task 091 ST-1's manual catch fixed back in commit `1fa0ac8`). But `python3 -m pytest tools/tests/fm/` surfaced 16 newly failing tests across three sibling files:

- `test_validate_skill_bundles.py` (9 tests)
- `test_validate_skill_kind.py` (subtest sweep + 1 absent-key test)
- `test_validate_skill_source.py` (3 tests)

Every failure was the same shape: the sandbox `_Sandbox` writes a synthetic `skills/<slug>/SKILL.md` to a temp directory and expects `rc == 0`. Once F.S.1 began enforcing the sibling readme, those sandboxes silently became invalid skill folders and tripped the new check.

**Resolution.** Two-step:
1. Patched `_Sandbox.write()` in each of the three affected sibling test files to auto-write a stub `readme.md` whenever a `SKILL.md` is dropped (idempotent — only writes if the sibling does not already exist). Six lines per file; preserves every test's intent.
2. Added a regression scenario inside `test_validate_skill_readme.py` (`test_live_skills_corpus_validates_clean`) that runs the validator over the real `skills/` tree and asserts `rc == 0` AND `F.S.1` is absent — locks in the Task 091 ST-1 fix and serves as a permanent canary for future skill imports.

**Why FL1 not FL0.** The validator extension itself was already pre-staged in the worktree (uncommitted modifications to `tools/fm/validate.py` + `diagnostic-explanations.json`); the work for this session was the test scaffolding and closure. The sandbox-collision discovery was a 30-second pytest run, but it would have caught a reviewer off-guard if landed without fixing — minor real friction, hence FL1 not FL0.

**Recommendation for future skill-folder linters.** Any new structural check on `skills/<slug>/` SHOULD ship a `_Sandbox.write` helper pattern that pre-populates the canonical siblings (`SKILL.md` + `readme.md`) so individual checks don't bleed through into unrelated test sandboxes. Worth folding into a shared helper in `tools/tests/fm/_skill_helpers.py` next time three+ files need it.

### FL0.1 — Branch name divergence (informational)

The task launcher cited `claude/execute-parallel-tasks-QntXs` as the worktree branch; the actual worktree is on `worktree-agent-adb98033ad9f7f251`. Standard isolated-worktree naming pattern; not blocking — commits will be merged back via the parent session. Recorded as FL0 for transparency.

## What didn't go wrong (FL0 baseline)

- The validator implementation was already cleanly scoped to `_check_skill_readme(path, rel)`, hooked under `type_for_keys == "skill"` alongside `_check_skill_bundles` / `_check_skill_source` / `_check_skill_kind_enum`. No rewiring needed.
- `tools/check-governance.sh` exited 0 on the first try after fixes — no waiver triage required.
- The diagnostic-explanations.json registry entry was well-formed at the L3 anchor (T093.1.3 passes on first run).
- All 5 new tests in `test_validate_skill_readme.py` passed on the first run.
- 7 pre-existing unrelated failures (`test_duplicate_task_id` integration test, `test_fm_wrapper` AttributeErrors) were confirmed via `git stash` to predate this session — out of scope.

## Carry-forward signals

None. Task 093 is single-shot maintenance; no follow-up Tasks expected. The shared-helper recommendation above is advisory; file as a Task only if a fourth skill-structural linter lands.
