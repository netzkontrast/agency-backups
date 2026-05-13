---
type: task
status: active
slug: skill-subfolder-readme-audit-linter
summary: "Maintenance Task: extend tools/fm/validate.py (or tools/lint-structure.py) to mechanically enforce SKILLS.md §9.6 Readme Audit for skills/<slug>/readme.md. Surfaced when Task 091 ST-1 shipped 14 sc-* skill folders without readme.md and governance still exited 0."
created: 2026-05-12
updated: 2026-05-13
task_id: "093"
task_status: done
task_owner: "claude-code"
task_priority: P3
task_uses_prompts: []
task_spawns_research: []
task_spawns_prompts: []
task_affects_paths:
  - tools/fm/validate.py
  - tools/legacy/lint-structure.py
  - tools/tests/fm/test_validate.py
  - maintenance/schemas/header-ontology.json
---

# Task 093 — Skill-subfolder readme-audit linter

## Goal

Close the mechanical-enforcement gap surfaced by [Task 091 ST-1 peer review Observation 1](../091-port-external-skill-corpora/review-st1.md): `SKILLS.md §9.6` ("Readme Audit") maps to `tools/lint-structure.py`, but the linter does not currently check that every `skills/<slug>/` operational folder contains a `readme.md`. Task 091 ST-1 was able to ship 14 `skills/sc-*/` folders without `readme.md` and `tools/check-governance.sh` still exited 0. The peer review caught this manually; the next batch (Task 092 ST-2 / ST-3, ~75 candidates) would benefit from mechanical enforcement before it lands.

Add a check — emitting a new diagnostic code (suggested: `F.S.1` per the §SKILLS namespace, mirroring `F.B.*` for `skill_*` keys) at ERROR severity when a skill subfolder is missing `readme.md`. The check MUST hook into the canonical `tools/fm/validate.py` Flexible toolchain entry point, not just the legacy shim.

## Context

[CLAUDE.md §7](../../CLAUDE.md) is unambiguous: "EVERY operational folder MUST contain a `readme.md`." [`SKILLS.md §2`](../../SKILLS.md) lists `readme.md # Directory index.` as a top-level entry in the canonical skill folder layout (non-OPTIONAL — only `adapters/` and `references/` carry the OPTIONAL marker). [`SKILLS.md §9.6`](../../SKILLS.md) "Readme Audit" specifies the rule MUST be enforced by `tools/lint-structure.py`.

Empirically: governance currently does NOT catch missing skill-subfolder `readme.md`. The diagnostic was surfaced manually in peer review, not mechanically.

**Repair tier:** T2 additive — adds a new validator check and a new diagnostic code; does not edit existing checks or relax existing rules. Falls within [`MAINTENANCE.md §1`](../../MAINTENANCE.md) "T2 — Additive" allowance for the agent that picks up the Task.

## Plan

1. **Pick the right linter.** Either:
   - **(a)** Extend `tools/fm/validate.py` with a new `_check_skill_readme(repo_root)` function called once per skill folder under `/skills/`. Emit `F.S.1` ERROR when `readme.md` is missing. Hook into the existing entry point alongside `_check_skill_bundles` and `_check_skill_source`.
   - **(b)** Extend `tools/legacy/lint-structure.py` (the actual implementation behind `tools/lint-structure.py` shim) with the same check.
   - **Recommendation:** (a). The Flexible toolchain is the canonical gating path per [`PRE_COMMIT.md §7.A`](../../PRE_COMMIT.md); the legacy shim is being retired.
2. **Register the diagnostic.** Add an entry for `F.S.1` to [`maintenance/schemas/diagnostic-explanations.json`](../../maintenance/schemas/diagnostic-explanations.json) with what / why / fix triplet.
3. **Author tests.** New test file `tools/tests/fm/test_validate_skill_readme.py` covering:
   - skill folder with `readme.md` → 0 diagnostics
   - skill folder without `readme.md` → `F.S.1` ERROR
   - regression: every pre-existing `skills/<slug>/` folder passes (this catches the gap retroactively — Task 091 ST-1 readmes that landed in commit `1fa0ac8` MUST keep passing).
4. **Document the new code.** Add a row to [`PRE_COMMIT.md §7.A`](../../PRE_COMMIT.md) Toolchain Precedence Matrix if a Skills column exists, or to the appropriate concern row.
5. **Bump `updated:`** on `tools/fm/validate.py` callers' frontmatter (validator itself has none; `header-ontology.json` may need a `key_docs` addition for the new check if it's documented there).

## Todo

- [ ] 1. `_check_skill_readme` added to `tools/fm/validate.py` with `F.S.1` ERROR emit
- [ ] 2. `maintenance/schemas/diagnostic-explanations.json` gains `F.S.1` entry
- [ ] 3. `tools/tests/fm/test_validate_skill_readme.py` written; tests pass
- [ ] 4. Regression: `python3 tools/fm/validate.py skills/` over the current repo state (35 skill folders, including Task 091 ST-1's 14 sc-*) exits 0 — confirms no false positives
- [ ] 5. `tools/check-governance.sh` exits 0
- [ ] 6. Friction log authored
- [ ] 7. PR opened; this Task closes `task_status: done`

## Acceptance Criteria

```gherkin
Feature: Skill-subfolder readme.md is mechanically enforced

  # anchor: T093.1.1
  Scenario: Missing readme.md in a skill folder emits F.S.1
    Given a skills/example-skill/SKILL.md exists
    And the same folder has no readme.md
    When `python3 tools/fm/validate.py skills/example-skill/` runs
    Then the validator MUST emit exactly one F.S.1 ERROR diagnostic
    And the exit code MUST be 1

  # anchor: T093.1.2
  Scenario: Skill folders with readme.md validate clean
    Given every existing skills/<slug>/ on `main` has a readme.md (post-Task-091 ST-1 + ST-1-blocker-fix)
    When `python3 tools/fm/validate.py skills/` runs
    Then the exit code MUST be 0
    And no F.S.1 diagnostic MUST be emitted

  # anchor: T093.1.3
  Scenario: Diagnostic explanation is registered
    Given the new check is committed
    When a reader opens maintenance/schemas/diagnostic-explanations.json
    Then the codes dictionary MUST contain an entry keyed F.S.1
    And the entry MUST have non-empty 'what', 'why', and 'fix' fields
```

## Links

- Surfacing review: [Task 091 ST-1 peer review — Observation 1](../091-port-external-skill-corpora/review-st1.md)
- Friction-log entry that documented the manual catch: [Task 091 friction-log § "What didn't"](../091-port-external-skill-corpora/friction-log.md)
- Governing root specs: [SKILLS.md §2 + §9.6](../../SKILLS.md), [CLAUDE.md §7](../../CLAUDE.md), [PRE_COMMIT.md §7.A](../../PRE_COMMIT.md)
- Sibling validator extensions (pattern reference): [`tools/fm/validate.py::_check_skill_bundles`](../../tools/fm/validate.py), [`tools/fm/validate.py::_check_skill_source`](../../tools/fm/validate.py)
- Reciprocal regression target: PR #115 (Task 091 ST-1) — the 14 `skills/sc-*/readme.md` files added in commit `1fa0ac8` MUST keep passing post-Task-093.
