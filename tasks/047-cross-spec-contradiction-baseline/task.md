---
type: task
status: active
slug: cross-spec-contradiction-baseline
summary: "Pre-chain contradiction baseline: execute the research-cross-spec-contradiction-baseline prompt to catalog all existing inter-spec normative conflicts across the 8 root governance specs before the 032–039 amendment chain lands."
created: 2026-05-07
updated: 2026-05-07
task_id: "047"
task_status: done
task_owner: "claude"
task_priority: P1
task_uses_prompts:
  - research-cross-spec-contradiction-baseline
task_spawns_research:
  - research-cross-spec-contradiction-baseline
task_spawns_prompts: []
task_supersedes: []
task_superseded_by: []
task_blocked_by: []
task_affects_paths:
  - research/research-cross-spec-contradiction-baseline/
  - prompts/research-cross-spec-contradiction-baseline/
  - tasks/047-cross-spec-contradiction-baseline/
---

# Task 047 — Cross-Spec Normative Contradiction Baseline

## Goal

Execute [`prompts/research-cross-spec-contradiction-baseline/prompt.md`](../../prompts/research-cross-spec-contradiction-baseline/prompt.md) to produce a pre-chain contradiction catalog across the 8 root governance specs before the 032–039 amendment chain lands its spec edits.

The catalog is the "before" state that makes tasks 032–039 chain falsification criterion #3 mechanically verifiable: *"Root specs MUST NOT end up with mutually contradictory normative clauses introduced by this chain."* Without a pre-chain baseline, "newly introduced" cannot be distinguished from "pre-existing."

## Background

Spawned from a brainstorm session on 2026-05-07 that analyzed all 18 existing research workspaces and 9 pending research subtasks, then identified this gap: no pre-chain contradiction baseline existed for any of the 8 specs targeted by the 032–039 amendment chain.

## Output

[`research/research-cross-spec-contradiction-baseline/output/REPORT.md`](../../research/research-cross-spec-contradiction-baseline/output/REPORT.md)

**Findings:**
- **16 contradictions** cataloged (CONTR-001 through CONTR-016).
- 1 previously known (CONTR-001 = FRUSTRATED.md §28 ↔ PRE_COMMIT.md §2).
- 15 newly discovered.
- **5 High-severity** (CONTR-001,004,005,006,014): friction-log placement cluster, session-start bypass conflict, MAINTENANCE.md T3 internal contradiction.
- **7 Medium** (CONTR-002,003,008,009,010,011,013).
- **4 Low** (CONTR-007,012,015,016).
- §4 provides per-task amendment-safety notes for each of Tasks 032–039.

## Acceptance Criteria (Gherkin)

```gherkin
Feature: Pre-chain contradiction baseline complete

  Scenario: Anchor contradiction captured
    Given the known FRUSTRATED.md §28 ↔ PRE_COMMIT.md §2 conflict
    When the research run completes
    Then CONTR-001 appears in REPORT.md §2 with both clause quotes and High severity

  Scenario: Amendment-safety notes cover all chain tasks
    When REPORT.md §4 is read
    Then each of Tasks 032–039 has at least one amendment-safety note

  Scenario: Per-spec risk table complete
    When REPORT.md §3 is read
    Then all 8 root specs (AGENTS.md through MAINTENANCE.md) appear in the table

  Scenario: Summary statistics internally consistent
    When REPORT.md §5 total count is compared to §2 CONTR-NNN entries
    Then the counts match
```

## Plan

Single-phase research execution run. No subtasks — the research prompt specifies all steps internally.

1. Author prompt + brief at `/prompts/research-cross-spec-contradiction-baseline/`.
2. Initialize research workspace scaffold.
3. Execute research via deep-research agent (read all 8 root specs, catalog contradictions).
4. Populate output/REPORT.md, synthesis files, reflection/friction-log.md.
5. Run `tools/check-governance.sh`. Fix every ERROR.
6. Commit. Do NOT push until maintainer review.

## Links

- Prompt: [`/prompts/research-cross-spec-contradiction-baseline/`](../../prompts/research-cross-spec-contradiction-baseline/)
- Research output: [`/research/research-cross-spec-contradiction-baseline/output/REPORT.md`](../../research/research-cross-spec-contradiction-baseline/output/REPORT.md)
- Feeds: Tasks [032](../032-agents-spec-integration/), [033](../033-task-spec-integration/), [034](../034-prompt-spec-integration/), [035](../035-research-spec-integration/), [036](../036-folders-spec-integration/), [037](../037-pre-commit-spec-integration/), [038](../038-frustrated-spec-integration/), [039](../039-maintenance-spec-integration/) — amendment-safety notes per task in REPORT.md §4.
- Addresses: Chain falsification criterion #3 in [`tasks/readme.md`](../readme.md) §Chain-Level Falsification.

## Todo

- [x] 1. Author prompt + brief at `/prompts/research-cross-spec-contradiction-baseline/`.
- [x] 2. Initialize research workspace at `/research/research-cross-spec-contradiction-baseline/`.
- [x] 3. Execute research: read all 8 root specs, catalog contradictions.
- [x] 4. Deliver `output/REPORT.md` (§1–§5).
- [x] 5. Complete synthesis files (`methodology.md`, `tracks.md`, `post-synthesis-log.md`, `state.md`).
- [x] 6. Write `reflection/friction-log.md` (FL0) and `reflection/M07-contradiction-log.md`.
- [x] 7. Run `tools/check-governance.sh` — exits 0.
- [x] 8. Set `task_status: done`. Commit and push.
