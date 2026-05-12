---
type: task
status: active
slug: novel-architect-v120-enforcement-epic
summary: "Mini-Epic umbrella for novel-architect@1.2.0 — orchestrates 5 sub-tasks (084-088) that mechanize the prose specifications landed in v1.1.0 Tasks 072/073/075/076 into ERROR-tier linters under tools/novel-architect-checks/, wire render_architecture.py to consume the linter's JSON artefact, and backport MIF L1/L2 entries in references/learnings.md to L3 schema. Standalone Task 089 (files separately, blocked) records legacy retirement gating per ADR-0010 + Task 070 §Legacy Retirement Criterion."
created: 2026-05-12
updated: 2026-05-12
task_id: "083"
task_status: open
task_owner: "claude-code"
task_priority: P2
task_uses_prompts: []
task_spawns_research: []
task_spawns_prompts: []
task_blocked_by: []
task_supersedes: []
task_superseded_by: []
task_affects_paths:
  - tools/novel-architect-checks/
  - tools/check-hard-rules.py
  - tools/check-worksheet-order.py
  - tools/check-scene-audit.py
  - tools/check-canon-status.py
  - tools/check-governance.sh
  - skills/novel-architect/render/render_architecture.py
  - skills/novel-architect/references/learnings.md
  - decisions/0010-novel-architect-error-tier-linter-policy.md
---

# Task 083 — novel-architect@1.2.0 Enforcement Epic

## Goal

Coordinate the v1.2.0 release of `skills/novel-architect/` across 5 linked sub-tasks (084-088). The Epic is `done` when:

1. All 5 sub-tasks have `task_status: done` OR `task_status: updated` with documented disposition.
2. `tools/check-governance.sh` exits 0 (gating checks pass) after all sub-tasks land, including the four new ERROR-tier linter rows.
3. [ADR-0010 `novel-architect-error-tier-linter-policy`](../../decisions/0010-novel-architect-error-tier-linter-policy.md) reaches `adr_status: Accepted` after the 30-day post-landing observation window passes without falsifier F1/F2/F3 firing.
4. The four ERROR-tier linters (`tools/check-{hard-rules,worksheet-order,scene-audit,canon-status}.py`) are registered in the `tools/check-governance.sh` ERROR-tier stage, path-scoped to staged diffs touching `skills/novel-architect*/` or `novel-projects/`.
5. `skills/novel-architect/render/render_architecture.py` Phase 2.13 status-view reads `<workspace>/<slug>/.architecture-validation.json` and renders H1–H12 pass/fail markers + worksheet_audit step completion, with graceful fallback when the file is stale or missing.
6. A v1.2.0 changelog entry is appended to `skills/novel-architect/references/learnings.md` summarising the enforcement layer landed in this Epic.
7. **Test scaffold exists** for `tools/novel-architect-checks/` — ≥3 known-clean + ≥3 known-bad fixtures per linter under `tools/novel-architect-checks/tests/fixtures/`, with a pytest suite passing on `python3 -m pytest tools/novel-architect-checks/tests/ -v`. Mirrors the v1.1.0 Epic's Todo 7 (test-scaffold) discipline from Task 070.

This Task itself contains **no diffs** — diffs land via sub-tasks 084-088. This Task is the orchestration / dependency-tracking artifact.

The legacy-retirement follow-up Task 089 is filed standalone (not as a sub-task of 083) per the gated-Task pattern established in [Task 070 §Legacy Retirement Criterion](../070-novel-architect-v110-epic/task.md#legacy-retirement-criterion-pr-101-review-43). Epic 083 closure does NOT require Task 089 closure; 089 unblocks independently when criteria (a)/(b)/(c) hold.

## Context

v1.1.0 (Epic [Task 070](../070-novel-architect-v110-epic/task.md), closed via PR #102) shipped four prose specifications carrying normative `MUST` / `MUST NOT` clauses but no mechanical enforcement:

| v1.1.0 source | Binding clause | Enforcement gap |
|---|---|---|
| [Task 072 worksheet-loop](../072-novel-architect-phase2-worksheet-loop/task.md) | Phase 2 sub-phases MUST follow Worksheet Steps 0–8 | No `check-worksheet-order.py` linter |
| [Task 073 hard-rules](../073-novel-architect-hard-rules-validation/task.md) | H1–H12 MUST pass before Gate 3 | No `check-hard-rules.py` linter |
| [Task 075 scene-level-bridge](../075-novel-architect-scene-level-bridge/task.md) | Every moment MUST carry Q1–Q5 fields | No `check-scene-audit.py` linter |
| [Task 076 canon-status-schema](../076-novel-architect-canon-status-schema/task.md) | `decanonized` MUST NOT be referenced in active phases | No `check-canon-status.py` linter |

Without mechanical enforcement these prose `MUST` clauses degrade silently — storyform schema-drift propagates through Phase 3+ before becoming visible, and the v1.1.0 Epic's `tools/check-governance.sh exit 0` Goal was met without protecting the post-merge state from regression. The [Task 070 friction log §"What worked"](../070-novel-architect-v110-epic/friction-log.md#what-worked) explicitly defers each linter (`CLI linter <name>.py deferred`) per sub-task as v1.2.0 work.

In parallel, [Task 072's closure summary §3](../072-novel-architect-phase2-worksheet-loop/task.md#closure-2026-05-11) grew `architecture.yaml` with `story_points` / `crucial_element` / `signposts` / `journeys` / `ending_type` / `genre_mode` / `worksheet_audit` fields, but [`skills/novel-architect/render/render_architecture.py`](../../skills/novel-architect/render/render_architecture.py) Phase 2.13 status-view was not updated to surface H1–H12 pass/fail markers from the (not-yet-shipped) hard-rules check. This Epic closes both gaps in one coordinated effort.

Severity policy for the four new linters is governed by [ADR-0010 `novel-architect-error-tier-linter-policy`](../../decisions/0010-novel-architect-error-tier-linter-policy.md) (`adr_status: Proposed` at this Epic's filing). ADR-0010 permits ERROR-tier promotion under three preconditions: (i) fixture corpus ≥3 clean + ≥3 bad, (ii) <500ms per linter / +<2s aggregate budget, (iii) maintenance-bypass wiring covers the new rule-IDs. Each sub-task carries the precondition obligations.

## Sub-Tasks (children)

| Task ID | Title | Blocks/Blocked-by | Affects |
|---------|-------|-------------------|---------|
| **084** | Storyform Integrity Linter (foundation: shared lib + `check-hard-rules.py` + `worksheet_audit` body-schema) | foundation (blocked by 083 only) | `tools/novel-architect-checks/`, `tools/check-hard-rules.py`, `tools/check-governance.sh` |
| **085** | Phase-Flow Linters (`check-worksheet-order.py` + `check-scene-audit.py`) | blocked by 084 | `tools/check-worksheet-order.py`, `tools/check-scene-audit.py`, shared lib in 084 |
| **086** | Canon-Status Linter (`check-canon-status.py`) | blocked by 084 | `tools/check-canon-status.py`, shared lib in 084 |
| **087** | Render-Architecture Wiring (Phase 2.13 + JSON-artefact consumption) | blocked by 084 | `skills/novel-architect/render/render_architecture.py`, JSON-artefact contract |
| **088** | MIF L3 Backport (retroactive MIF L3 frontmatter on `references/learnings.md` historical entries) | independent | `skills/novel-architect/references/learnings.md`, `skills/novel-architect/schemas/mif-level3.yaml` |

**Dependency graph:**

```
083 Epic ──┬──── 084 (foundation: shared lib + hard-rules + worksheet_audit)
           │              │
           │              ├──── 085 (phase-flow linters)
           │              │
           │              ├──── 086 (canon-status linter)
           │              │
           │              └──── 087 (renderer wiring; reads JSON from 084)
           │
           └──── 088 (MIF L3 backport — independent)
```

Standalone (NOT a sub-task of 083): **089** `retire-novel-architect-legacy` — gated on Task 070 §Legacy Retirement Criterion (a)/(b)/(c).

## Plan

1. **Land 084** (Storyform Integrity Linter) first — establishes the `tools/novel-architect-checks/` shared library (loader + Finding dataclass + Severity helper + JSON-artefact writer), the `tools/check-hard-rules.py` thin entry point at ERROR-tier, and the `worksheet_audit` body-schema check folded into the same linter under rule-IDs `WA.STEP_*_SET`. Output: shared library callable from sub-tasks 085-087; first ERROR-tier row in `tools/check-governance.sh`; ADR-0010 precondition (i)-(iii) satisfied for the first linter.
2. **Land 085, 086, 087 in parallel** — each blocked_by 084 only (shared-lib dependency). Order does not matter among themselves; commits can be sequential or interleaved. 085 adds `check-worksheet-order.py` + `check-scene-audit.py`; 086 adds `check-canon-status.py`; 087 wires `render_architecture.py` to read the JSON artefact produced by 084's hard-rules linter.
3. **Land 088 independently** — touches `skills/novel-architect/references/learnings.md` only; no dependency on the linter cluster. Subset MIF L3 schema applied retroactively to v1.1.0-era entries; `decay_rate` conservative; `derivation_chain` populated where reconstructable from git history.
4. **Verify Epic acceptance** — all 5 sub-tasks `done`/`updated`; `tools/check-governance.sh` exit 0 with the new ERROR-tier stage active; v1.2.0 changelog appended to `references/learnings.md`; fixture-corpus pytest suite passing; observe 30-day window post-landing for ADR-0010 falsifier F1/F2; flip ADR-0010 to `adr_status: Accepted` if window closes clean.

## Todo

- [ ] 1. Land Task 084 (foundation: shared lib + hard-rules + worksheet_audit body-schema)
- [ ] 2. Land Task 085 (phase-flow linters — worksheet-order + scene-audit)
- [ ] 3. Land Task 086 (canon-status linter)
- [ ] 4. Land Task 087 (render_architecture.py JSON-artefact wiring)
- [ ] 5. Land Task 088 (MIF L3 backport)
- [ ] 6. Append v1.2.0 changelog entry to `skills/novel-architect/references/learnings.md`
- [ ] 7. Confirm `tools/check-governance.sh` includes the four new ERROR-tier linter rows
- [ ] 8. Confirm fixture-corpus pytest suite at `tools/novel-architect-checks/tests/` runs green (≥3 clean + ≥3 bad per linter)
- [ ] 9. Observe 30-day post-landing window for ADR-0010 falsifier triggers F1/F2; capture evidence in this Epic's friction log
- [ ] 10. If window closes clean, flip ADR-0010 to `adr_status: Accepted` via a follow-up commit on the ADR's own change-control path

## Acceptance

```gherkin
Feature: Epic 083 closes when sub-tasks land, governance gates pass, ADR-0010 is ratified, and the renderer consumes the linter artefact

  # anchor: 083.AC.1
  Scenario: Sub-task completion gate
    Given Tasks 084, 085, 086, 087, 088 exist under /tasks/
    When the agent queries each task_status via tools/fm/extract.py
    Then every task_status MUST be "done" or "updated" with documented disposition in the Task body
    And the dependency graph (084 → {085, 086, 087}; 088 independent) MUST be reflected in each task_blocked_by frontmatter field

  # anchor: 083.AC.2
  Scenario: ADR-0010 + linter integration gate
    Given Epic 083 sub-tasks 084-086 have landed at ERROR-tier
    And the 30-day post-landing observation window has elapsed
    And neither falsifier F1 (≥5 maintenance-bypass invocations / 30 days) nor F2 (≥3 simultaneous open bypass entries / >30 days) has fired
    When a maintainer reviews ADR-0010
    Then adr_status MUST be flippable from "Proposed" to "Accepted"
    And tools/check-governance.sh MUST list tools/check-hard-rules.py, tools/check-worksheet-order.py, tools/check-scene-audit.py, tools/check-canon-status.py as ERROR-tier rows
    And each linter MUST complete in <500ms on the reference consciousness-novel workspace
    And the aggregate ERROR-tier-stage budget MUST be <2s

  # anchor: 083.AC.3
  Scenario: Renderer wiring gate
    Given Task 084's check-hard-rules.py writes <workspace>/<slug>/.architecture-validation.json with the schema declared in ADR-0010 Cross-references
    And the workspace's architecture.yaml is fresh (post Gate 3)
    When skills/novel-architect/render/render_architecture.py renders the Phase 2.13 status-view
    Then the status-view MUST include H1-H12 pass/fail markers (🟢/🔴) derived from architecture-validation.json
    And it MUST include worksheet_audit step_0_set..step_v_set completion markers
    And when architecture-validation.json is missing or stale (checked_at < architecture.yaml mtime) the renderer MUST emit "⚠ Validation report stale — rerun tools/check-hard-rules.py" without crashing

  # anchor: 083.AC.4
  Scenario: MIF L3 backport gate
    Given Task 088 has landed
    When the agent queries tools/fm/validate.py --check-body on skills/novel-architect/references/learnings.md
    Then every v1.1.0-era entry MUST carry the subset MIF L3 frontmatter (cognitive_type, decay_rate, derivation_chain) declared in skills/novel-architect/schemas/mif-level3.yaml
    And the v1.2.0 changelog entry (Epic 083 Todo 6) MUST be present at the bottom of learnings.md
    And T4-immutable entries (status: archived) MUST receive only metadata-frontmatter additions per MAINTENANCE.md §1.0.1, with no body edits
```

## Links

- Governing specs: [`TASK.md`](../../TASK.md), [`SKILLS.md`](../../SKILLS.md), [`AGENTS.md`](../../AGENTS.md), [`MAINTENANCE.md`](../../MAINTENANCE.md), [`PRE_COMMIT.md`](../../PRE_COMMIT.md)
- Predecessor Epic: [Task 070 — novel-architect@1.1.0 Epic](../070-novel-architect-v110-epic/task.md) (closed via PR #102)
- Predecessor sub-tasks (binding prose specs this Epic enforces):
  - [Task 072 — Phase 2 Worksheet-Loop](../072-novel-architect-phase2-worksheet-loop/task.md)
  - [Task 073 — Hard Rules Validation](../073-novel-architect-hard-rules-validation/task.md)
  - [Task 075 — Scene-Level-Bridge](../075-novel-architect-scene-level-bridge/task.md)
  - [Task 076 — Canon-Status Schema](../076-novel-architect-canon-status-schema/task.md)
  - [Task 077 — MIF Level 3 + SessionStart-Hook](../077-novel-architect-mif-learnings-sessionhook/task.md) (informs sub-task 088 backport scope)
- Sub-Tasks of this Epic:
  - [Task 084 — Storyform Integrity Linter](../084-novel-architect-storyform-integrity-linter/task.md)
  - [Task 085 — Phase-Flow Linters](../085-novel-architect-phase-flow-linters/task.md)
  - [Task 086 — Canon-Status Linter](../086-novel-architect-canon-status-linter/task.md)
  - [Task 087 — Render-Architecture Wiring](../087-novel-architect-render-architecture-wiring/task.md)
  - [Task 088 — MIF L3 Backport](../088-novel-architect-mif-l3-backport/task.md)
- Standalone gated Task (NOT a sub-task — files separately, blocked on observable criteria):
  - [Task 089 — Retire Novel-Architect Legacy](../089-retire-novel-architect-legacy/task.md)
- Governing ADR: [ADR-0010 — Novel-Architect ERROR-Tier Linter Policy (Narrow)](../../decisions/0010-novel-architect-error-tier-linter-policy.md)
- Implementation target: [`skills/novel-architect/render/render_architecture.py`](../../skills/novel-architect/render/render_architecture.py)
- Skill: [`skills/novel-architect/`](../../skills/novel-architect/), [`skills/novel-architect-structure/`](../../skills/novel-architect-structure/), [`skills/novel-architect-scene/`](../../skills/novel-architect-scene/), [`skills/novel-architect-character/`](../../skills/novel-architect-character/), [`skills/novel-architect-world/`](../../skills/novel-architect-world/)
