---
type: note
status: active
slug: task-094-st1-pr123-review
summary: "Peer review of PR #123 (Task 094 ST-1): root-spec hookup (54 skills) + skill_kind enum F.B.11 + triage-note typo sweep. Verdict: APPROVED with 6 advisory items — count-discrepancy not propagated, ST-3 forward-references stated as present fact, sweep count mismatch, test run-instruction inconsistency, null-valued skill_kind edge case untested, cross-spec orchestrator count divergence undocumented."
created: 2026-05-12
updated: 2026-05-12
---

# Review — PR #123 · Task 094 ST-1: root-spec hookup (54 skills) + skill_kind enum + triage-note typo sweep

**Reviewer:** claude-sonnet-4-6  
**PR:** [#123](https://github.com/netzkontrast/agency/pull/123)  
**Branch:** `claude/execute-skill-integration-task-RAuYR` → `main`  
**Commit:** `6c37950`  
**Date:** 2026-05-12  
**Prompt source:** Task 094 Epic `task.md` + `subtasks/01-root-spec-hookup.md` (no `/prompts/` entry; `task_uses_prompts: []`)

---

## Verdict: APPROVED (6 advisory items)

The ST-1 deliverables are complete and correct: all 54 imported skills are now cited in ≥ 1 root spec (zero orphans), the 9-value `skill_kind` enum is properly ratified with a gating validator diagnostic (F.B.11), the T1 typo sweep is clean, and governance exits 0. Six advisory items — none blocking merge — warrant attention before ST-4 or the Epic close.

---

## What works

### T094.1.1 — Zero orphan skills

Every `skills/sc-*` and `skills/superpowers-*` slug is now reachable from at least one root spec. The AGENTS.md "Skill Index by Category" section (112 new lines) and CLAUDE.md §13 expansion (25 new lines) provide two independent citation surfaces. AC satisfied. ✓

### T094.1.2 — Enum validation (F.B.11) wired correctly

`_check_skill_kind_enum` in `tools/fm/validate.py` follows the existing `_check_skill_source` idiom (F.B.8/F.B.9) precisely:

- Absent key → no diagnostic (correct; key is optional during classification).
- Present but out-of-enum string → F.B.11 ERROR (correct).
- `SKILL_KIND_ENUM` is a `frozenset` — O(1) membership test — consistent with style elsewhere in the file.

The pytest fixture covers all 9 valid values (9 subtests), 3 invalid values (3 subtests), absent-key pass, and a repo-regression guard against all 75 `skills/**` files. AC satisfied. ✓

### T094.1.3 — T1 typo sweep complete

`grep -r "superclaude_framework@v4.3.0" tasks/092-port-skill-corpora-phase-2/references/triage-notes/` returns zero matches. AC satisfied. ✓

### T094.1.4 — Governance green

`tools/check-governance.sh` exits 0. The validate-related pytest battery (40 tests including the new `test_validate_skill_kind.py`) passes. ✓

### Frontmatter in new review file

`maintenance/schemas/diagnostic-explanations.json` correctly registers F.B.11 with `what` / `why` / `fix` fields matching the ADR-0012 + ADR-0011 schema precedents. ✓

### Branch deviation documented

The session-assigned branch `claude/execute-skill-integration-task-RAuYR` diverges from the spec-suggested `claude/task-094-st1-root-spec-hookup`. This is a session-policy override (CLAUDE.md §11) — correctly logged in the friction-log and the PR body. Not a friction event per the spec. ✓

---

## Advisory A1 — Count discrepancy (52 → 54) not propagated to source-of-truth fields

**Severity:** Advisory — T1 repair; stale summary field misleads future readers.

**What happened:**

The actual skill count after Task 092 is **54** (39 sc-* + 15 superpowers-*). The PR body acknowledges this and documents it in the friction-log. However, two source-of-truth frontmatter fields still assert the stale count:

| File | Stale field | Value |
|---|---|---|
| `tasks/094-skill-integration-agency-default/task.md` | `summary:` | "Integrate the **52** imported skills (39 sc-* + **13** superpowers-*)" |
| `tasks/094-skill-integration-agency-default/subtasks/01-root-spec-hookup.md` | `summary:` | "cite every imported skill (**52** total)" |

The CLAUDE.md and AGENTS.md changes in this PR correctly cite 54 — but the task artifact that documents the Epic's intent still says 52. A reader auditing Task 094 will find the task.md summary contradicting the root specs.

**Recommended fix (T1/T2 in-place via `tools/fm/edit.py`):**

```bash
python3 tools/fm/edit.py tasks/094-skill-integration-agency-default/task.md \
  --set summary "Epic: Integrate the 54 imported skills (39 sc-* + 15 superpowers-*) into Agency's default operating surface — root-spec citations (every orphan skill cited), .claude/ directory + .claude-plugin/plugin.json (agency@1.0.0), 5 D.7-compliant event-driven hooks, and carried-forward closure of the Task 092 T3 (skill_kind enum) + T1 (triage-note typos) follow-ups." \
  --bump-updated

python3 tools/fm/edit.py tasks/094-skill-integration-agency-default/subtasks/01-root-spec-hookup.md \
  --set summary "ST-1 (Task 094 Epic): cite every imported skill (54 total) in ≥ 1 root spec; ratify the expanded skill_kind enum (T3, 9 values) in SKILLS.md §3; add validator enum check (F.B.11); fix triage-note typos (T1) carried forward from Task 092." \
  --bump-updated
```

---

## Advisory A2 — ST-3 forward-references in AGENTS.md stated as present fact

**Severity:** Advisory — documentation drift; behavior described does not exist yet.

**What happened:**

The new "Discipline skills (8) — Superpowers gates" section in AGENTS.md contains:

> "Pre-commit / pre-completion discipline gates routed through **PreToolUse / Stop hooks (Task 094 ST-3 surface)**. Each gate emits an audit line under **`.claude/audit/`** when triggered."

ST-3 has not landed. `.claude/audit/` does not exist. No PreToolUse or Stop hooks are registered. A reader following the AGENTS.md instructions today will find no hooks and no audit directory — the text describes future behavior as if it were current state.

This is a governance concern: AGENTS.md is T1/T2-mutable but not T4-immutable; the spec-level claim that hooks "emit an audit line" when they do not yet exist is a behavioral assertion that should be either (a) softened to future tense or (b) deferred until ST-3 lands.

**Recommended fix:**

Replace the paragraph:

> Pre-commit / pre-completion discipline gates routed through PreToolUse / Stop hooks (Task 094 ST-3 surface). Each gate emits an audit line under `.claude/audit/` when triggered.

With:

> Pre-commit / pre-completion discipline gates. Task 094 ST-3 will register these as PreToolUse / Stop hooks emitting audit lines under `.claude/audit/`; until ST-3 lands, invoke explicitly via the Skill tool.

---

## Advisory A3 — T1 sweep count discrepancy (spec says 12 files; PR fixes 11)

**Severity:** Advisory — count mismatch between spec and delivered change.

**What happened:**

`subtasks/01-root-spec-hookup.md` §T1 typo sweep states:

> "12 files affected; cosmetic only"

The PR diff shows **11** triage-note files changed. Verify the full count:

```bash
grep -rl "superclaude_framework@v4.3.0" \
  tasks/092-port-skill-corpora-phase-2/references/triage-notes/ 2>/dev/null | wc -l
```

If the result is 0 (sweep complete) but the spec said 12, the subtask spec carries a stale count. If 1 file was missed, the AC is violated. The PR body says "11 files in the triage-notes" which matches the diff — most likely the spec overcounted by 1.

**Recommended fix:** After confirming zero remaining matches, update the subtask spec's count annotation from "12" → "11" via `tools/fm/edit.py --bump-updated`.

---

## Advisory A4 — Test file run instruction inconsistency

**Severity:** Advisory — minor documentation friction for future contributors.

**What happened:**

`tools/tests/fm/test_validate_skill_kind.py` module docstring says:

```
Run: python3 -m unittest tools/tests/fm/test_validate_skill_kind.py
```

But the PR body's "Test plan" section consistently uses:

```
python3 -m pytest tools/tests/fm/test_validate_skill_kind.py -q
```

All sibling files in `tools/tests/fm/` (e.g. `test_validate.py`, `test_validate_skill_source.py`) use `pytest` exclusively. The `unittest` invocation is technically valid (pytest discovers and runs `TestCase` subclasses) but diverges from the project's established test invocation pattern and will confuse contributors scanning the file for "how to run this."

**Recommended fix:** Update the module docstring to `Run: python3 -m pytest tools/tests/fm/test_validate_skill_kind.py -q`.

---

## Advisory A5 — `skill_kind: null` (present but None-valued) edge case untested

**Severity:** Advisory — behavioral gap in test coverage.

**What happened:**

In YAML, `skill_kind:` without a value (or `skill_kind: null`) parses to Python `None`. The validator's path is:

1. `if "skill_kind" not in fm: return out` — **skipped** (key is present, value is `None`).
2. `if not isinstance(value, str) or value not in SKILL_KIND_ENUM:` — `isinstance(None, str)` is `False` → **F.B.11 fires** (correct behavior).

So the null-valued case is handled correctly by the production code. However, no test covers it. The "absent key is fine" guarantee and the "null value is invalid" behavior are not distinguished in the test suite, leaving a gap that could silently regress if the absence-check path is refactored.

**Recommended fix:** Add a subtest to `test_invalid_kind_emits_fb11`:

```python
with self.subTest(skill_kind="null_value"):
    sb, td = self._new_sandbox()
    try:
        sb.write(
            "skills/example-null/SKILL.md",
            _skill_md(skill_kind=None),  # writes "skill_kind: null" in YAML
        )
        rc, output = sb.run("skills/example-null/SKILL.md")
        self.assertEqual(rc, 1, output)
        self.assertIn("F.B.11", output)
    finally:
        td.cleanup()
```

(Requires `_skill_md` to handle `skill_kind=None` specially — write the key with empty/null value vs. omitting it entirely.)

---

## Advisory A6 — Cross-spec orchestrator count (9 vs 12) undocumented

**Severity:** Advisory — maintainability risk; future editors will be confused by the divergence.

**What happened:**

CLAUDE.md §13.1 categorises `sc-*` skills only and lists **orchestrator (9)**, while AGENTS.md SK.AGENTS.orchestrator.1 lists **Orchestrator skills (12)** (9 sc-* + 3 superpowers-*: `superpowers-dispatching-parallel-agents`, `superpowers-requesting-code-review`, `superpowers-subagent-driven-development`).

Both counts are *correct* given their respective partitioning axes — CLAUDE.md §13 partitions by `skill_source` (vendor), AGENTS.md groups by `skill_kind` regardless of source. But no cross-reference or annotation explains the discrepancy to a reader who sees 9 in one spec and 12 in the other.

This will re-emerge as a false-positive in any future "count drift" audit.

**Recommended fix:** Add a parenthetical to CLAUDE.md §13.1:

> `- **orchestrator (9):** ...` → `- **orchestrator (9 sc-\* only; 3 superpowers-\* orchestrators appear in AGENTS.md SK.AGENTS.orchestrator.1):**`

Or add a brief note below the `##13.1` heading: "The AGENTS.md Skill Index groups by `skill_kind` across both vendors; the counts per category differ because `superpowers-*` orchestrators appear there but not under §13.1."

---

## Summary table

| # | Issue | Severity | Tier | Action |
|---|---|---|---|---|
| A1 | `task.md` + subtask `summary:` still say 52/13 skills | Advisory | T1 | `tools/fm/edit.py --set summary` |
| A2 | AGENTS.md discipline section states ST-3 hooks as existing | Advisory | T2 | Soften to future tense |
| A3 | T1 sweep spec says 12 files; PR fixes 11 | Advisory | T1 | Confirm count; update annotation |
| A4 | Test file docstring says `unittest`; project uses `pytest` | Advisory | T1 | Update docstring one-liner |
| A5 | `skill_kind: null` not tested (covered by code; not by tests) | Advisory | T2 additive | Add null-value subtest |
| A6 | Orchestrator count 9 (CLAUDE.md) vs 12 (AGENTS.md) unexplained | Advisory | T1 | Add cross-reference note |

**No blocking issues.** ST-1 is complete; ST-2 (`.claude/` directory + ADR-0013) may proceed.
