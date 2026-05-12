---
type: note
status: active
slug: task-092-st2-superclaude-phase-2
summary: "ST-2 (Task 092 Epic): port the SuperClaude_Framework keep-list (per ST-1 triage matrix) into skills/sc-<slug>/; bundle the 5 unbundled MODE files; ADR-0011 D.8 body adaptation as flagged."
created: 2026-05-12
updated: 2026-05-12
---

# ST-2 — SuperClaude Phase 2 batch

**Executor:** main-agent invoking `/sc:implement` over the keep-list rows from ST-1's triage matrix.

**Parallelism:** Sequential after ST-1. MAY parallelise per-skill writes within this subtask (Task 091 ST-1 demonstrated 14 SKILL.md files generated from a single Python script — same pattern applies).

**Depends on:** ST-1 ([`01-triage.md`](./01-triage.md)) at `task_status: done`; ADR-0011 amendment (FL1.1 carry-over, `decisions/0012-…`) Accepted.

## Scope

For every row in [`../references/triage-matrix.md`](../references/triage-matrix.md) with `Vendor=superclaude` and `Decision ∈ {port, adapt}`:

- **SKILL.md.** Author `skills/sc-<slug>/SKILL.md` following the canonical shape from Task 091 ST-1 (Anthropic `name`+`description` + Agency L2 keys + `skill_source: "superclaude@v4.3.0"` pin). Body MUST be ≤ 5 KB; D.6 overflow extracts to `references/` and is cited from `## References`.
- **Verbatim mirror.** Place the snapshot file's verbatim body at `skills/sc-<slug>/references/upstream-sc-<slug>.md` with the canonical attribution header (`<!-- Mirror of … @ <SHA>. DO NOT EDIT — re-sync via a new Task. -->`).
- **Readme.** Add `skills/sc-<slug>/readme.md` per the Task 091 ST-1 post-review pattern (L1 frontmatter, navigation, Assumptions Log) — CLAUDE.md §7 requires this.
- **D.8 adaptation.** For every row marked `adapt`, rewrite `## How to use` and `## Compatibility` so any non-Agency MCP (Tavily, Serena, Morphllm, Magic, Chrome-DevTools, Playwright) appears ONLY in `## Compatibility` marked OPTIONAL; built-in Claude Code primitives (Read/Write/Edit/Bash/WebSearch/WebFetch/Glob/Grep) take their place in `## How to use`. Archive the verbatim Tavily-or-MCP-first upstream body to `references/upstream-sc-<slug>.md`.
- **D.7 enforcement.** Strip every SessionStart-injection clause from imported bodies. The 5 modes (`MODE_Brainstorming.md`, `MODE_Business_Panel.md`, `MODE_Introspection.md`, `MODE_Task_Management.md`, `MODE_Token_Efficiency.md`) bundle into the skill that activates them per the triage matrix; if no skill in the keep-list activates a given mode, the mode is `skip`-classified and does NOT ship.
- **Validator pin.** Every SKILL.md MUST validate clean: `python3 tools/fm/validate.py skills/sc-*/SKILL.md` exits 0.
- **`skills/readme.md`.** Extend the "Imported from SuperClaude (v4.3.0)" section with the new entries.

## Out of scope

- Superpowers content — that is ST-3's scope.
- Modifying root specs (AGENTS.md, RESEARCH.md, etc.) — separate Tasks per MAINTENANCE.md §1.
- Re-syncing from a newer upstream release — ADR-0011 D.9 forbids it within this Epic.

## Acceptance Criteria (Gherkin)

```gherkin
Feature: ST-2 lands the SuperClaude Phase 2 keep-list

  # anchor: T092.2.1
  Scenario: Every keep-list row produces a /skills/sc-*/ folder
    Given ST-2 is complete
    When a reader cross-references the triage matrix
    Then every row with Vendor=superclaude AND Decision ∈ {port, adapt}
        MUST have a corresponding skills/sc-<slug>/SKILL.md on the branch
    And every such SKILL.md MUST carry skill_source: "superclaude@v4.3.0"

  # anchor: T092.2.2
  Scenario: D.8 adaptation enforced where flagged
    Given a triage row's Decision = "adapt" AND ADR-0011 clauses contain "D.8"
    When a reader greps the new SKILL.md
    Then every named non-Agency MCP MUST appear ONLY in "## Compatibility" marked OPTIONAL
    And the "## How to use" section MUST cite a built-in Claude Code primitive instead

  # anchor: T092.2.3
  Scenario: T2 body cap holds across the batch
    Given ST-2 is complete
    When `python3 tools/fm/validate.py --check-body skills/sc-*/SKILL.md` runs
    Then exit code MUST be 0 (every body ≤ 5 KB per ADR-0011 D.6)

  # anchor: T092.2.4
  Scenario: skills/readme.md reflects the new entries
    Given ST-2 is complete
    When a reader opens skills/readme.md
    Then the "Imported from SuperClaude (v4.3.0)" section MUST list every new sc-<slug>
    And the section MUST cite ADR-0011 + Task 092 as authority
```

## Branch + PR shape

Author on a fresh branch (`claude/task-092-st2-…`). PR title: `Task 092 ST-2: SuperClaude Phase 2 batch (~N skills)`. PR body MUST include:

- Per-skill body-byte table (analogous to Task 091 ST-1 output).
- Confirmation that `tools/check-governance.sh` exits 0.
- Friction-log declaration.
