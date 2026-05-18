---
type: prompt
status: active
slug: improve-maintenance-spec-may-18-2026-brief
summary: "Acceptance brief for Task 096 — Improve Maintenance Spec from 2026-05-18 Coherence Run. Seven Gherkin scenarios (AC-F27 through AC-F33) bind the spec amendments; the brief is the executable acceptance contract referenced from prompt.md."
created: 2026-05-18
updated: 2026-05-18
prompt_kind: task-spec
prompt_framework: RISEN+ReAct
prompt_target_agent: "Claude Code"
prompt_relates_to_task: improve-maintenance-spec-may-18-2026
---

# Brief — Acceptance Criteria for Task 096

## Scope

This brief is the executable acceptance contract for [`prompt.md`](./prompt.md). The Task closes when every Gherkin scenario below either passes (diff landed) or carries a documented `won't-fix:` disposition in `friction-log.md`.

## Gherkin Acceptance Scenarios

```gherkin
Feature: Maintenance spec amendments from the 2026-05-18 coherence run

  # anchor: AC-F27 — tier classification of FL-declaration repairs
  Scenario: A maintenance agent finds a non-canonical FL syntax and classifies it as T1
    Given `tasks/<NNN>-<slug>/friction-log.md` contains `**FL: 1** — minor friction.`
    And `tools/check-fl-declaration.py` rejects the line with diagnostic `FR.B.4:malformed`
    And `MAINTENANCE.md §1` carries the F27 T1-row amendment
    When the maintenance agent classifies the repair
    Then the agent MUST classify it as T1 (Mechanical) per the new row
    And the agent MUST apply the repair via `tools/fm/edit.py` (frontmatter bump) + in-place Edit (body) without filing a Task

  # anchor: AC-F28 — AGGREGATOR dedup predicate
  Scenario: AGGREGATOR friction recommendation is skipped when an open Task already covers the path
    Given `tools/maintenance/trust-audit.py` emits `research/<slug>::WARN:MAINT.TRUST.FRICTION:FL1:...:recommend-task`
    And an open Task `tasks/<NNN>-<slug>/task.md` has `task_affects_paths` containing `research/<slug>/`
    And `MAINTENANCE.md §3.3` carries the F28 dedup-predicate amendment
    When the maintenance agent triages the AGGREGATOR output
    Then the agent MUST skip-with-citation (per Task 064 F26) rather than file a duplicate Task
    And the agent MUST record the skip in `maintenance/run-log.md` `notes:` citing the absorbing Task slug

  # anchor: AC-F29 — coherence baseline filter
  Scenario: Last run-log record is adr-synthesize; agent recovers most-recent coherence baseline
    Given `maintenance/run-log.md` last record has `routine_type: adr-synthesize` and `end_commit: <adr-sha>`
    And the most-recent `routine_type: coherence-check` record has `end_commit: <coh-sha>`
    And `prompts/repo-coherence-check/prompt.md` Step 1a carries the F29 awk filter
    When the coherence-run agent executes Step 1a
    Then the agent MUST recover `<coh-sha>` as the baseline (not `<adr-sha>`)
    And the agent MUST NOT use the `adr-synthesize` `end_commit:` as the delta source

  # anchor: AC-F30 — staleness triage threshold
  Scenario: Staleness audit emits >=3 non-still_accurate buckets; agent files ONE triage Task
    Given `tools/maintenance/staleness-audit.py` emits 4 lines with bucket ∈ {drifted, completed_by_drift, no_longer_desirable}
    And `MAINT_STALENESS_TRIAGE_THRESHOLD` resolves to `3` (default)
    And `MAINTENANCE.md §3.4` carries the F30 triage-threshold amendment
    When the maintenance agent processes the audit output
    Then the agent MUST file exactly ONE triage Task with all 4 affected Task slugs in `task_affects_paths`
    And the triage Task body MUST preserve the per-Task bucket assignment as a table
    And the agent MUST NOT file N=4 individual lifecycle Tasks

  # anchor: AC-F31 — T3 row cross-link to §4.9 ladder
  Scenario: Agent files a T3 Task; spec routes them to the /sc:* planning ladder
    Given an agent classifies a finding as T3 (Structural) per MAINTENANCE.md §1
    And `MAINTENANCE.md §1` T3 row carries the F31 cross-link to TASK.md §4.9
    When the agent reads §1 to decide next-action
    Then the agent MUST see a relative link to TASK.md §4.9
    And the agent SHOULD execute /sc:analyze → /sc:brainstorm → /sc:design → /sc:workflow before authoring the Task's `## Plan` section

  # anchor: AC-F32 — bypass scope clarification
  Scenario: tools/check-governance.sh emits advisory ERROR lines; reader does not misread as bypass admission
    Given `tools/check-governance.sh` exit code is 0 (PASS)
    And `[opt]` advisory steps emitted ERROR-tier diagnostic lines
    And `MAINTENANCE.md §4.1` carries the F32 advisory-scope clarification sentence
    When a reader (human or AI) skims the output
    Then the spec MUST explicitly state that advisory diagnostics do NOT participate in the bypass calculation
    And the bypass MUST be understood to apply only to gating steps `[1/6]–[6/6]`

  # anchor: AC-F33 — adr-synthesize no-op suppression
  Scenario: tools/adr/cli.py synthesize is invoked but produces no change; no run-log record is appended
    Given `tools/adr/cli.py synthesize` is invoked
    And `start_commit == end_commit`
    And no ADR was added or rewritten (synthesis output byte-identical to pre-existing AGENTS.md block)
    When the synthesize command completes
    Then the command MUST NOT append a record to `maintenance/run-log.md`
    And the command MUST log the suppression to stderr so the action is observable
```

## Tooling Anchors

- [`tools/fm/edit.py`](../../tools/fm/edit.py) — canonical frontmatter mutator.
- [`tools/check-fl-declaration.py`](../../tools/check-fl-declaration.py) — 15-variant FL acceptance set (F27 ratification anchor).
- [`tools/maintenance/trust-audit.py`](../../tools/maintenance/trust-audit.py) — AGGREGATOR whose output drives F28.
- [`tools/maintenance/staleness-audit.py`](../../tools/maintenance/staleness-audit.py) — per-Task bucket assignment for F30.
- [`tools/check-governance.sh`](../../tools/check-governance.sh) — gate that MUST exit 0 after every commit.

## Out of Scope

- New linters or schema changes (the seven findings target prose + one prompt-awk + one synthesize-suppression).
- Closure / supersession of Tasks 025 / 044 / 064 — those Tasks have their own owners; this Task only cites them as cross-references.
- T3 promotion of Task 064 F21 (one-open-Task cadence rule) — referenced as recognised pre-condition; landing F21 is its own Task's work.
