---
type: note
status: active
slug: task-094-st1-root-spec-hookup
summary: "ST-1 (Task 094 Epic): cite every imported skill (52 total) in ≥ 1 root spec; ratify the expanded skill_kind enum (T3, 9 values) in SKILLS.md §3; add validator enum check (F.B.11); fix triage-note typos (T1) carried forward from Task 092."
created: 2026-05-12
updated: 2026-05-12
---

# ST-1 — Root-spec hookup + T3 enum + T1 typo sweep

**Executor:** main-agent invoking `Read` + `Edit` over the seven root specs + `tools/fm/validate.py` extension + `Edit` sweep over `tasks/092-…/references/triage-notes/`.

**Parallelism:** Sequential within ST-1 (root-spec edits chain). MAY parallelise the T1 typo sweep + the validator extension via independent commits.

**Depends on:** Task 092 closed `done` (provides the full 52-skill corpus + the friction-log carried-forward items).

## Scope

### Root-spec citation expansion

For every skill folder under `skills/sc-*` + `skills/superpowers-*`, add a citation in at least one root spec. Idiom precedent: Task 091 ST-2's `AGENTS.md CR.7` + `RESEARCH.md §7` patterns.

**Files changed:**

- **`CLAUDE.md §13`** — expand the "Skills, Skills SDK, and SuperClaude `/sc:*` commands" section from 7 lines to ~40 lines. Add stable anchors `SK.13.SUPERCLAUDE` and `SK.13.SUPERPOWERS`. Enumerate all 52 skills grouped by `skill_kind`.
- **`AGENTS.md`** — new H2 section "Skill Index by Category" added after the Closing Run Procedure (after CR.7), ~400 lines, with anchors `SK.AGENTS.<kind>.<n>` per category.
- **`TASK.md §4.9`** — inline-cite the four planning-ladder skills (`/sc:analyze`, `/sc:brainstorm`, `/sc:design`, `/sc:workflow`) with their `skills/sc-*/SKILL.md` paths.
- **`RESEARCH.md §7`** — expand the "Skill-driven research runs" section from ~5 lines to ~15 lines listing `sc-research`, `sc-analyze`, `sc-deep-research-agent`, and the relevant `superpowers-*` discipline gates (e.g. `superpowers-systematic-debugging`).
- **`SKILLS.md §3`** — **T3 absorbed**: ratify the expanded enum to 9 values `{domain, tool, orchestrator, meta, discipline, workflow, persona, analysis, agent-template}`. Cite Task 092 PR #120 review A1 as the trigger.

### Validator extension (T3 enforcement)

- **`tools/fm/validate.py`** — add a new check `_check_skill_kind_enum` emitting diagnostic `F.B.11` ERROR when `skill_kind` is not in the 9-value enum. Pattern precedent: `F.B.8` / `F.B.9` from ADR-0012.
- **`tools/tests/fm/test_validate_skill_kind.py`** — new pytest fixture covering each of the 9 valid values + 3 invalid values (negative cases).
- **`maintenance/schemas/diagnostic-explanations.json`** — register `F.B.11` (what / why / fix) so `tools/fm/validate.py --explain F.B.11` produces useful output.

### T1 typo sweep

- **`tasks/092-port-skill-corpora-phase-2/references/triage-notes/*.md`** — `grep -l "superclaude_framework@v4.3.0"` then sweep to canonical `superclaude@v4.3.0`. Use `Edit` per file (12 files affected; cosmetic only).
- This is a **T1/T2 repair** on closed research per [`MAINTENANCE.md §1.0.1`](../../../MAINTENANCE.md#101-closed-research-t1t2-repair-allowance-task-059) — narrow allowance for `updated:` bumps and link-text fixes; the closed-research T4 immutability applies to *body content*, not these surface typo corrections.

## Out of scope

- Per-skill SKILL.md body changes — none.
- New ADR — the enum ratification rides under ADR-0011 D.2 (`skill_source` regex precedent) + ADR-0012 (diagnostic-code numbering precedent); no new ADR needed.
- Plugin / `.claude/` work — that is ST-2's scope.
- Hooks — that is ST-3's scope.

## Acceptance Criteria (Gherkin)

```gherkin
Feature: ST-1 closes the root-spec citation gap + T3 + T1 follow-ups

  # anchor: T094.1.1
  Scenario: Zero orphan skills
    Given ST-1 is complete
    When a reader greps each root spec (AGENTS.md / CLAUDE.md / SKILLS.md / TASK.md / RESEARCH.md)
        for every slug under skills/sc-* and skills/superpowers-*
    Then every slug MUST produce ≥ 1 match in at least one spec
    And no slug MAY be cited solely by example-list aside

  # anchor: T094.1.2
  Scenario: Expanded skill_kind enum validates
    Given ST-1 is complete
    When `python3 tools/fm/validate.py skills/` runs
    Then exit code MUST be 0
    And every SKILL.md frontmatter's skill_kind value MUST be in
        {domain, tool, orchestrator, meta, discipline, workflow, persona, analysis, agent-template}
    And a synthetic SKILL.md with `skill_kind: bogus` MUST emit diagnostic F.B.11 ERROR

  # anchor: T094.1.3
  Scenario: T1 typo sweep complete
    Given ST-1 is complete
    When a reader greps tasks/092-…/references/triage-notes/ for the literal "superclaude_framework@v4.3.0"
    Then the grep MUST return zero matches

  # anchor: T094.1.4
  Scenario: Governance still green
    Given ST-1 is complete
    When `tools/check-governance.sh` runs
    Then exit code MUST be 0
```

## Branch + PR shape

Branch: `claude/task-094-st1-root-spec-hookup`. PR title: `Task 094 ST-1: root-spec hookup (52 skills) + skill_kind enum + triage-note typo sweep`. PR body MUST include:

- Per-spec diff stats (lines added per root spec).
- Confirmation grep for AC T094.1.1: zero orphans.
- Output of `python3 tools/fm/validate.py skills/` (0 diagnostics).
- T1 typo sweep confirmation grep (0 matches for the bad slug).
- Friction-log declaration.
