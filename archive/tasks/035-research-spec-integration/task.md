---
type: task
status: archived
slug: research-spec-integration
summary: "Add Gherkin acceptance scenarios to RESEARCH.md, integrate spec-chunking rule from spec-driven-research-agentic-workflows, integrate trust-audit gate from agentic-eval-trust-improvement-spec, integrate session-continuity protocol from agentic-session-continuity-spec, mechanically enforce R.4.4 workspace cleanup and R.6.5 external-result downstream-task creation, and resolve the R.4.3 prompt-snapshot mid-run ambiguity."
created: 2026-05-06
updated: 2026-05-12
task_id: "035"
task_status: archived
task_owner: "claude-opus-4-7 (session claude/complete-tasks-32-39-uSMVT)"
task_priority: P1
task_uses_prompts:
  - research-session-continuity-protocol-instantiation
  - tooling-workspace-cleanliness-linter
  - tooling-external-result-downstream-task-linter
  - tooling-trust-audit-gate
  - spec-amendment-research-md
task_spawns_research: []
task_spawns_prompts: []
task_affects_paths:
  - RESEARCH.md
  - tools/check-workspace-cleanliness.py
  - tools/check-external-result-downstream-task.py
  - tools/check-trust-audit.py
---

# Task 035 — RESEARCH.md Spec Integration

## Goal

Lift three orphaned/under-utilized research outputs into RESEARCH.md normative scope, close two enforcement gaps, and add Gherkin acceptance scenarios. The Task is `done` when **each of the following anchors carries ≥1 Gherkin scenario in RESEARCH.md §5 (total ≥6)**:

- **R.B.1 prompt resolution** — `/prompts/<slug>/prompt.md` exists before `/research/<slug>/` is created.
- **R.B.2 workspace cleanliness** — no stray `.py`/`.sh` in `/workspace/` at commit (ST-2).
- **R.B.3 follow-up filing** — open questions go to `/prompts/<new-slug>/`, never appended to closed research.
- **R.B.4 external ingestion** — every `/research/<provider>/<slug>/result.md` triggers a downstream Task (ST-3).
- **R.B.5 trust-audit gate** — `research_phase: complete` blocked until trust-audit passes (ST-4 / Task 035 ST-4 GATE).
- **R.B.6 session continuity** — multi-session resume works against `/workspace/state.md` per ST-1's protocol.

Plus: (b) §2.2 mandates spec-chunking per `spec-driven-research-agentic-workflows/output/SPEC.md` for synthesis runs over 50k tokens, (c) §5.7 mandates a trust-audit gate per `agentic-eval-trust-improvement-spec/output/SPEC.md` before `research_phase: complete`, (d) §4 references `agentic-session-continuity-spec/output/SPEC.md` for multi-session continuity, (e) R.4.4 workspace cleanup is mechanically enforced, (f) R.6.5 external-result downstream-task creation is mechanically enforced, (g) R.4.3 prompt-snapshot policy is unambiguous on mid-run prompt edits.

## Context

Three completed research outputs are entirely orphaned in RESEARCH.md:

- **agentic-eval-trust-improvement-spec** — proposes a three-tier trust rubric (schema ≥80%, behavioral ≥90%, governance ≥95%) but is uncited in RESEARCH.md §5 or MAINTENANCE.md §2.3.
- **spec-driven-research-agentic-workflows** — proposes spec-chunking heuristics (RFC-2119-aspect boundary preferred) and Gherkin behavioral-rule templates. Zero citations across the codebase.
- **agentic-session-continuity-spec** — proposes Spec-G/H/I (context-pruning, memory state machine, cross-session protocol) for multi-session research runs. Zero citations.

Two known enforcement gaps in RESEARCH.md:

- **R.4.4** "Execution scripts (`.py`, `.sh`) MUST be deleted before final commit" — human-review only; no linter scans `/research/<slug>/workspace/` for stragglers.
- **R.6.5** "Every `result.md` MUST have a corresponding open Task" — human-review only; external results can be ingested without a downstream Task.

One ambiguity:

- **R.4.3** "immutable run-start snapshot" — silent on what happens if `/prompts/<slug>/prompt.md` is edited mid-run. Does the researcher re-snapshot? Lock at start? Diverge?

## Preconditions (satisfied at branch-time)

- **Task 016/017** — flexible-frontmatter toolchain (substrate for ST-2 + ST-3).
- **Task 028/031** — ADR run-log pattern (`tools/adr/runlog.py`); ST-4 trust-audit GATE follows the same diagnostic-format contract.

## Build-On

- **`tools/adr/runlog.py`** — diagnostic-format contract (`<relpath>::ERROR:<code>:<message>`); ST-4 (trust-audit GATE) emits in this shape so MAINTENANCE.md aggregation can ingest both ADR + trust-audit findings via a single parser.
- **`tools/fm/extract.py`** — workspace scan (`/research/<slug>/workspace/*`) reuse for ST-2 cleanliness check.
- **`tools/fm/query.py`** — `referenced-by=<slug>` to find downstream Tasks for ST-3 external-result enforcement.

## Trust-Audit Partition (per spec-panel C3)

ST-4 here ships the **GATE** — invoked at `research_phase: complete` transition; emits per-workspace diagnostics. The **AGGREGATOR** (Task 039 ST-5) imports ST-4's diagnostic schema and rolls findings across workspaces for the maintenance run. ST-4 MUST NOT include cross-workspace logic; that belongs in Task 039.

## Plan

1. **Phase 1 — Research head.** Subtask `01-research-session-continuity-protocol-instantiation` translates Spec-I from `agentic-session-continuity-spec` into a concrete checkpoint/restore protocol that fits a `/research/<slug>/workspace/state.md` file.
2. **Phase 2 — Tooling.** Subtask `02-tooling-workspace-cleanliness-linter` (R.4.4). Subtask `03-tooling-external-result-downstream-task-linter` (R.6.5). Subtask `04-tooling-trust-audit-gate` (§5.7 new — GATE only, per C3 partition).
3. **Phase 3 — Spec amendment.** Subtask `05-spec-amendment-research-md` adds §2.2 chunking rule, §4 continuity reference, §5.7 trust-audit clause, R.4.3 snapshot disambiguation, and one Gherkin per R.B.1–R.B.6 anchor.

## Sample Gherkin (shape the maintainer authoring subtask 05 should produce)

```gherkin
# anchor: R.B.5 — trust-audit gate
Scenario: Research closure blocked on trust-audit failure
  Given a research workspace at `/research/<slug>/` with `research_phase: synthesis`
  And `/output/SPEC.md` exists
  When the agent attempts to set `research_phase: complete` and commit
  Then `tools/check-trust-audit.py <workspace>` MUST run as part of pre-commit
  And the commit MUST be blocked if any of the trust-audit thresholds fail
      (schema-conformance ≥ 80%, behavioral ≥ 90%, governance ≥ 95%)
  And the diagnostic format MUST match the ADR validator pattern
      `<relpath>::ERROR:TRUST.<code>:<message>` (per Build-On)
```

## Todo

- [x] 1. Dispatch subtask `01-research-session-continuity-protocol-instantiation`.
- [x] 2. Dispatch subtask `02-tooling-workspace-cleanliness-linter` (Phase A).
- [x] 3. Dispatch subtask `03-tooling-external-result-downstream-task-linter` (Phase A).
- [x] 4. Dispatch subtask `04-tooling-trust-audit-gate` (Phase A).
- [x] 5. Dispatch subtask `05-spec-amendment-research-md` (Phase B).
- [x] 6. Run `tools/check-governance.sh`.
- [x] 7. Update `README.md §6` if linter table changes.
- [x] 8. Update `tasks/readme.md`.
- [x] 9. Author `friction-log.md`.
- [x] 10. Set `task_status: done`.

## Links

- Subtask index: [`subtasks/readme.md`](./subtasks/readme.md)
- Source research (orphaned, to be operationalized):
  - [`research/agentic-eval-trust-improvement-spec/output/SPEC.md`](../../research/agentic-eval-trust-improvement-spec/output/SPEC.md)
  - [`research/spec-driven-research-agentic-workflows/output/SPEC.md`](../../research/spec-driven-research-agentic-workflows/output/SPEC.md)
  - [`research/agentic-session-continuity-spec/output/SPEC.md`](../../research/agentic-session-continuity-spec/output/SPEC.md)
- Governing specs: [`RESEARCH.md`](../../RESEARCH.md), [`PROMPT.md`](../../PROMPT.md), [`MAINTENANCE.md`](../../MAINTENANCE.md), [`README.md`](../../README.md) §11.3
