---
type: task
status: active
slug: novel-architect-phase-flow-linters
summary: "Ship tools/check-worksheet-order.py + tools/check-scene-audit.py at ERROR-tier, both consuming the tools/novel-architect-checks/ shared library bootstrapped by Task 084. check-worksheet-order.py validates Phase 2 sub-phase ordering against Worksheet Steps 0-8 per Task 072 prose spec. check-scene-audit.py validates that every scene-matrix moment carries Q1-Q5 fields populated per Task 075 prose spec. Both linters share the structural-walk helper added to the shared library."
created: 2026-05-12
updated: 2026-05-12
task_id: "085"
task_status: open
task_owner: ""
task_priority: P2
task_uses_prompts: []
task_spawns_research: []
task_spawns_prompts: []
task_blocked_by:
  - "083"
  - "084"
task_supersedes: []
task_superseded_by: []
task_affects_paths:
  - tools/novel-architect-checks/phase_flow.py
  - tools/check-worksheet-order.py
  - tools/check-scene-audit.py
  - tools/check-governance.sh
  - tools/check-maintenance-bypass.py
---

# Task 085 — Phase-Flow Linters

## Goal

Ship two ERROR-tier linters that share a `tools/novel-architect-checks/phase_flow.py` helper module and validate operational sequence over the novel-architect skill's phase/moment files. The first, `tools/check-worksheet-order.py`, MUST fail when Phase 2 sub-phase ordering in [`skills/novel-architect/phases/phase2-narrative-architecture.md`](../../skills/novel-architect/phases/phase2-narrative-architecture.md) deviates from Worksheet Steps 0–8 + Validation per [Task 072 prose spec](../072-novel-architect-phase2-worksheet-loop/task.md). The second, `tools/check-scene-audit.py`, MUST fail when any scene-matrix moment is missing one or more of Q1–Q5 fields (`throughline_focus`, `secondary_throughlines`, `operating_level`, `plot_story_point`, `motivation_elements`) per [Task 075 prose spec](../075-novel-architect-scene-level-bridge/task.md).

`done` when:

1. `tools/novel-architect-checks/phase_flow.py` exists with the structural-walk helper (`walk_phase_steps(markdown_path) -> list[Step]`, `walk_scene_moments(markdown_path) -> list[Moment]`).
2. `tools/check-worksheet-order.py` thin CLI entry point exists, imports `phase_flow.check_worksheet_order`, accepts a phase2 markdown path on argv, exits 1 on out-of-order Steps with `WS.STEP_ORDER` finding code.
3. `tools/check-scene-audit.py` thin CLI entry point exists, imports `phase_flow.check_scene_audit`, accepts a scene-matrix markdown path on argv, exits 1 with `SC.Q*_MISSING` finding codes per missing field.
4. Fixture corpus at `tools/novel-architect-checks/tests/fixtures/` adds ≥3 known-clean + ≥3 known-bad fixtures per linter (6 new clean + 6 new bad). Bad fixtures cover: out-of-order Step 2→4 skipping Step 3 (worksheet-order); missing Q3 operating_level on a moment (scene-audit); empty Q5 motivation_elements list on a moment (scene-audit).
5. Pytest suite at `tools/novel-architect-checks/tests/test_phase_flow.py` passes with both green-path and red-path coverage for each rule-ID.
6. Both linters appear as ERROR-tier rows in `tools/check-governance.sh`, path-scoped to staged diffs touching the relevant phase files.
7. `tools/check-maintenance-bypass.py` rule-ID allowlist extended for `WS.STEP_ORDER` and `SC.Q{1..5}_MISSING`.
8. Each linter completes in <500ms; aggregate ERROR-tier-stage budget remains <2s per ADR-0010 precondition (ii).

## Context

[Task 070's friction log §"Sub-task summary"](../070-novel-architect-v110-epic/friction-log.md#sub-task-summary) deferred both linters at v1.1.0 close:

> | 072 | done | `methods/storyform/worksheet-loop.md` (Phase 2 slot order) | CLI linter `tools/check-worksheet-order.py` deferred |
> | 075 | done | `novel-architect-scene/methods/scene-level-bridge.md` (Q1-Q5 audit) | CLI linter `tools/check-scene-audit.py` deferred |

Both prose specs are operational-sequence specifications (one over phase steps, one over scene moments). The shared `phase_flow.py` helper consolidates the markdown-walking pattern they both need (heading-extraction, sub-heading enumeration, field-presence checking inside a structured block). Splitting into two linters with one shared helper is the design-doc compromise between "one linter handles both" (too much surface in one entry point) and "fully duplicate parsers" (DRY violation).

Per [ADR-0010 Decision Outcome](../../decisions/0010-novel-architect-error-tier-linter-policy.md) and the [/sc:design §1 lumping rationale](../083-novel-architect-v120-enforcement-epic/task.md#sub-tasks-children), the two linters live in one sub-task because they share the structural-walk helper and similar shape. Their fixture corpora are independent.

## Plan

1. **Add `phase_flow.py` to the shared library** — `walk_phase_steps()` parses Phase 2 sub-phase headings + the Worksheet-Step binding declared in the worksheet-loop spec; `walk_scene_moments()` parses moment blocks in a scene-matrix markdown file and extracts Q1–Q5 field presence + non-emptiness. Both helpers return structured objects the rule functions iterate over.
2. **Implement `check_worksheet_order()`** in `phase_flow.py` — yields `WS.STEP_ORDER` Findings when consecutive sub-phases violate the canonical Worksheet Step order (0 → 1 → 2 → ... → 7 → V). Tolerant of split sub-phases inside a single Worksheet Step (e.g., 2.4 + 2.5 both bound to Step 2).
3. **Implement `check_scene_audit()`** in `phase_flow.py` — yields `SC.Q{1..5}_MISSING` Findings per moment missing a Q-field, plus `SC.Q5_EMPTY` for empty motivation_elements lists. Pure-function; iterates output of `walk_scene_moments()`.
4. **Wire CLI entry points + governance integration** — create `tools/check-worksheet-order.py` and `tools/check-scene-audit.py` thin wrappers; add both as ERROR-tier rows in `tools/check-governance.sh` (path-scoped); extend `tools/check-maintenance-bypass.py` allowlist; build fixture corpus; ship pytest suite; verify <500ms per linter + <2s aggregate.

## Todo

- [ ] 1. Add `tools/novel-architect-checks/phase_flow.py` with `walk_phase_steps()` + `walk_scene_moments()` helpers.
- [ ] 2. Implement `check_worksheet_order()` rule function in `phase_flow.py`.
- [ ] 3. Implement `check_scene_audit()` rule function (covering Q1–Q5 presence + Q5 non-emptiness) in `phase_flow.py`.
- [ ] 4. Build fixture corpus: 3 clean + 3 bad for each of (a) worksheet-order phase2 markdown, (b) scene-matrix moments.
- [ ] 5. Author `tools/novel-architect-checks/tests/test_phase_flow.py` covering all rule-IDs.
- [ ] 6. Create `tools/check-worksheet-order.py` and `tools/check-scene-audit.py` CLI entry points.
- [ ] 7. Extend `tools/check-maintenance-bypass.py` rule-ID allowlist for `WS.STEP_ORDER` and `SC.Q{1..5}_MISSING` / `SC.Q5_EMPTY`.
- [ ] 8. Add two ERROR-tier rows to `tools/check-governance.sh`, path-scoped to `skills/novel-architect*/phases/` and `novel-projects/*/scene-matrix/`.
- [ ] 9. Run `tools/check-governance.sh` on the reference `consciousness-novel` workspace; confirm <500ms per linter + <2s aggregate budget.

## Acceptance

```gherkin
Feature: tools/check-worksheet-order.py and tools/check-scene-audit.py enforce Phase 2 step ordering and scene-matrix Q1-Q5 completeness at ERROR-tier

  # anchor: 085.AC.1
  Scenario: Clean Phase 2 markdown passes worksheet-order check
    Given a phase2-narrative-architecture.md with sub-phases bound 2.1→Step 0, 2.2→Step 1, ..., 2.8→Step 7+V (fixture: phase2-clean-1.md)
    When the agent runs tools/check-worksheet-order.py path/to/phase2-narrative-architecture.md
    Then the linter MUST exit 0
    And stderr MUST NOT contain "WS.STEP_ORDER"

  # anchor: 085.AC.2
  Scenario: Step-skip in Phase 2 fails worksheet-order
    Given a phase2-narrative-architecture.md where sub-phase 2.3 is bound to Step 4, skipping Step 3 (fixture: phase2-bad-step-skip.md)
    When the agent runs tools/check-worksheet-order.py path/to/phase2-narrative-architecture.md
    Then the linter MUST exit 1
    And stderr MUST contain "WS.STEP_ORDER"

  # anchor: 085.AC.3
  Scenario: Clean scene-matrix passes scene-audit
    Given a scene-matrix markdown where every moment carries Q1-Q5 populated (fixture: scene-matrix-clean-1.md)
    When the agent runs tools/check-scene-audit.py path/to/scene-matrix.md
    Then the linter MUST exit 0
    And stderr MUST NOT contain "SC.Q"

  # anchor: 085.AC.4
  Scenario: Moment missing Q3 operating_level fails scene-audit
    Given a scene-matrix markdown where moment "M-04" lacks operating_level (fixture: scene-matrix-bad-q3.md)
    When the agent runs tools/check-scene-audit.py path/to/scene-matrix.md
    Then the linter MUST exit 1
    And stderr MUST contain "SC.Q3_MISSING"

  # anchor: 085.AC.5
  Scenario: Empty Q5 motivation_elements list fails scene-audit
    Given a scene-matrix markdown where moment "M-07" has motivation_elements: [] (fixture: scene-matrix-bad-q5-empty.md)
    When the agent runs tools/check-scene-audit.py path/to/scene-matrix.md
    Then the linter MUST exit 1
    And stderr MUST contain "SC.Q5_EMPTY"
```

## Links

- Parent Epic: [Task 083](../083-novel-architect-v120-enforcement-epic/task.md)
- Blocked by: [Task 084](../084-novel-architect-storyform-integrity-linter/task.md) (shared library foundation)
- Source prose specs: [Task 072 worksheet-loop](../072-novel-architect-phase2-worksheet-loop/task.md), [Task 075 scene-level-bridge](../075-novel-architect-scene-level-bridge/task.md)
- Governing ADR: [ADR-0010](../../decisions/0010-novel-architect-error-tier-linter-policy.md)
- Governing specs: [`TASK.md`](../../TASK.md), [`PRE_COMMIT.md`](../../PRE_COMMIT.md)
- Skill references: [`skills/novel-architect-structure/methods/storyform/worksheet-loop.md`](../../skills/novel-architect-structure/methods/storyform/worksheet-loop.md), [`skills/novel-architect-scene/methods/scene-level-bridge.md`](../../skills/novel-architect-scene/methods/scene-level-bridge.md)
- Implementation target: [`tools/check-governance.sh`](../../tools/check-governance.sh)
