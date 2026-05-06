---
type: task
status: active
slug: maintenance-spec-integration
summary: "Operationalize three orphaned research outputs (agentic-eval-trust-improvement-spec, repo-maintenance-protocol-spec, governance-specs-update-research) by lifting them into MAINTENANCE.md normative scope; formalize §3.4 staleness algorithm, document the dual legacy/flexible toolchain transition, resolve the §3.5 duplicate-task_id circular dependency, and add ≥6 Gherkin scenarios."
created: 2026-05-06
updated: 2026-05-06
task_id: "039"
task_status: open
task_owner: "unassigned"
task_priority: P1
task_uses_prompts: []
task_spawns_research: []
task_spawns_prompts: []
task_blocked_by: []
task_affects_paths:
  - MAINTENANCE.md
  - tools/maintenance/staleness-audit.py
  - tools/maintenance/dynamic-readme-partition.py
  - tools/maintenance/trust-audit.py
---

# Task 039 — MAINTENANCE.md Spec Integration

## Goal

Make MAINTENANCE.md the operational home for three orphaned research outputs, and close five governance debts. The Task is `done` when (a) §2.3 references `agentic-eval-trust-improvement-spec/output/SPEC.md` and mandates the trust-audit gate before research closure, (b) §3.2 references `repo-maintenance-protocol-spec/output/SPEC.md` and enforces the static/dynamic readme partition via a new linter, (c) §1.1.2 contains a **THREE-WAY Legacy / Flexible / ADR** toolchain transition table with explicit flip criteria (post-Task-031, the third toolchain is the `agency-adr` CLI per PRE_COMMIT.md §7.C), (d) §3.4 staleness algorithm has a deterministic decision tree backed by `MAINT_STALE_DAYS`, (e) §3.5 duplicate-task_id circular dependency is resolved (when does the coherence run *itself* file the dedup Task vs. waiting for a human, **AND** how does it interact with the new `agency-adr validate` step `[5/5]` in `tools/check-governance.sh`), **and (f) each of the following anchors carries ≥1 Gherkin scenario in MAINTENANCE.md (total ≥7)**:

- **M.B.1 run-log baseline** — `end_commit` recovery when run-log is corrupt.
- **M.B.2 T1/T2/T3 tier classification** — boundary between mechanical / additive / structural changes.
- **M.B.3 stale-task lifecycle** — deterministic bucket assignment per ST-2 algorithm.
- **M.B.4 dup-id handling** — coherence run discovers + flags + escalates without re-discovery loop.
- **M.B.5 trust-audit gating** — research closure blocked until ST-5 aggregator passes (consumes Task 035 ST-4 GATE output).
- **M.B.6 dynamic-readme partition** — static/dynamic section boundary per `repo-maintenance-protocol-spec/output/SPEC.md §3.1`.
- **M.B.7 ADR T4-immutability** — `adr_status: Accepted` files are T4-immutable per FOLDERS.md:115; coherence run MUST refuse to mutate them even at T1/T2 tier.

## Context

MAINTENANCE.md is the governance hub but currently:

- **§2.3 run-log baseline (M.2.2 + §79–83)** — fragile: relies on `end_commit` field; recovery procedure undefined when run-log corrupted. governance-specs-update-research/output/SPEC.md §2 has concrete amendment text awaiting back-port.
- **§3.4 staleness audit** — four buckets (still accurate / drifted / completed-by-drift / no-longer-desirable) with no mechanical decision criteria. `MAINT_STALE_DAYS` is referenced but never declared.
- **§3.5 duplicate task_id** — coherence run discovers collision, declares it T3, files a Task. But the colliding state remains in the working tree until the Task runs. Next coherence-run discovery loop. Circular dependency acknowledged but unresolved.
- **§1.1.2 toolchain migration** — describes legacy + flexible coexistence but omits the *criteria* under which the default flips (default = "after Task 019 completes"). Now that Task 019 is `done` AND Task 031 added a third toolchain (ADR Validator §7.C), the spec is silent on (i) whether the legacy→flexible flip already happened and (ii) how the ADR toolchain composes with the other two.
- **Three orphaned research outputs** (agentic-eval-trust-improvement-spec, repo-maintenance-protocol-spec, governance-specs-update-research) are uncited despite being directly applicable to MAINTENANCE.md responsibilities.
- **NEW: ADR T4-immutability** — FOLDERS.md:115 (post-Task-031) declares that once `adr_status: Accepted`, a `decisions/<NNNN>-<slug>.md` is **T4-immutable per MAINTENANCE.md §1**. But MAINTENANCE.md §1 itself does not enumerate this case; the rule is currently asserted in FOLDERS.md but unsourced in the governance hub. §1 amendment must catch up.

## Preconditions (satisfied at branch-time)

- **Task 014/025** — maintenance-spec friction findings (F2/F3/F4/F7); §3 amendments build on these.
- **Task 016/017** — flexible toolchain (the second column of the §1.1.2 three-way table).
- **Task 028/031** — ADR machinery (the third column of the §1.1.2 table); FOLDERS.md:115 ADR T4-immutability anchor.

## Build-On

- **`tools/adr/runlog.py`** — diagnostic-format and run-log persistence pattern; ST-3 (staleness audit) emits findings in this shape so the coherence run-log unifies ADR + maintenance + trust signals.
- **`tools/adr/graph.py`** — DAG cycle detection; ST-3 reuses for stale-task chains where blockers may form cycles.
- **`tools/fm/_core.py`** + **`tools/fm/query.py`** — frontmatter access + query semantics for ST-3 + ST-4 + ST-5.

## Trust-Audit Partition (per spec-panel C3)

ST-5 here ships the **AGGREGATOR** — cross-research roll-up. It MUST import (not duplicate) the per-workspace GATE shipped by [Task 035 ST-4](../../035-research-spec-integration/subtasks/readme.md). The aggregator subscribes to GATE diagnostics emitted at `research_phase: complete` transitions and rolls them into the nightly maintenance run output for §3.2 friction-aggregation consumption.

## Plan

1. **Phase 1 — Research head.** Subtask `01-research-toolchain-flip-criteria` produces the deterministic flip criteria + post-flip cleanup list. Subtask `02-research-staleness-decision-formalization` (shared with Task 033; consume Task 033 output if it lands first).
2. **Phase 2 — Tooling.** Subtask `03-tooling-staleness-audit-script`. Subtask `04-tooling-dynamic-readme-partition-linter`. Subtask `05-tooling-trust-audit-integration` (AGGREGATOR only, per C3 partition).

## Sample Gherkin (shape the maintainer authoring subtask 06 should produce)

```gherkin
# anchor: M.B.7 — ADR T4-immutability
Scenario: Coherence run refuses to mutate Accepted ADR
  Given a `decisions/0042-storage-path.md` with frontmatter `adr_status: Accepted`
  And a coherence-run agent identifies a missing `updated:` date as a T1 repair
  When the agent attempts to apply the T1 repair via `tools/fm/edit.py`
  Then `tools/fm/edit.py` MUST refuse with diagnostic
        `M.B.7:adr-accepted-immutable:cannot apply T1 to adr_status=Accepted`
  And the agent MUST file a Task at the next free `<NNN>` instead of mutating
  And `tasks/readme.md` MUST be updated in the same commit per TASK.md §4.8
```
3. **Phase 3 — Spec amendment.** Subtask `06-spec-amendment-maintenance-md` lifts research outputs and tooling references into §1.1.2, §2.3, §3.2, §3.4, §3.5 + Gherkin scenarios.

## Todo

- [ ] 1. Dispatch subtask `01-research-toolchain-flip-criteria`.
- [ ] 2. Dispatch subtask `02-research-staleness-decision-formalization` (cross-Task; shared input with Task 033).
- [ ] 3. Dispatch subtask `03-tooling-staleness-audit-script` (Phase A).
- [ ] 4. Dispatch subtask `04-tooling-dynamic-readme-partition-linter` (Phase A).
- [ ] 5. Dispatch subtask `05-tooling-trust-audit-integration` (Phase A).
- [ ] 6. Dispatch subtask `06-spec-amendment-maintenance-md` (Phase B).
- [ ] 7. Run `tools/check-governance.sh`.
- [ ] 8. Update `README.md §6` per R.7.
- [ ] 9. Update `tasks/readme.md`.
- [ ] 10. Author `friction-log.md`.
- [ ] 11. Set `task_status: done`.

## Links

- Subtask index: [`subtasks/readme.md`](./subtasks/readme.md)
- Source research (orphaned, to be operationalized):
  - [`research/agentic-eval-trust-improvement-spec/output/SPEC.md`](../../research/agentic-eval-trust-improvement-spec/output/SPEC.md)
  - [`research/repo-maintenance-protocol-spec/output/SPEC.md`](../../research/repo-maintenance-protocol-spec/output/SPEC.md)
  - [`research/governance-specs-update-research/output/SPEC.md`](../../research/governance-specs-update-research/output/SPEC.md) §2 (MAINTENANCE.md amendments — toolchain context, drift checks)
- Sibling: [Task 033 — TASK.md spec integration](../033-task-spec-integration/task.md) (shared staleness research subtask).
- Governing specs: [`MAINTENANCE.md`](../../MAINTENANCE.md), [`TASK.md`](../../TASK.md), [`PRE_COMMIT.md`](../../PRE_COMMIT.md), [`README.md`](../../README.md) §11.3
