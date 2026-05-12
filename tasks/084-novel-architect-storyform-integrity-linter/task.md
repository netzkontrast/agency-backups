---
type: task
status: active
slug: novel-architect-storyform-integrity-linter
summary: "Foundation sub-task for Epic 083. Bootstrap tools/novel-architect-checks/ shared library (loader, Finding dataclass, Severity helper, JSON-artefact writer) and ship tools/check-hard-rules.py at ERROR-tier validating H1-H12 against architecture.yaml per Task 073 prose spec, with worksheet_audit body-schema check (step_*_set flags per Task 072 closure) folded into the same linter. Writes <workspace>/<slug>/.architecture-validation.json consumed by Task 087's render_architecture.py wiring. Establishes the shared library that Tasks 085 and 086 will import."
created: 2026-05-12
updated: 2026-05-12
task_id: "084"
task_status: open
task_owner: ""
task_priority: P2
task_uses_prompts: []
task_spawns_research: []
task_spawns_prompts: []
task_blocked_by:
  - "083"
task_supersedes: []
task_superseded_by: []
task_affects_paths:
  - tools/novel-architect-checks/
  - tools/check-hard-rules.py
  - tools/check-governance.sh
  - tools/check-maintenance-bypass.py
---

# Task 084 — Storyform Integrity Linter (foundation)

## Goal

Ship the `tools/novel-architect-checks/` shared library and the first ERROR-tier consumer `tools/check-hard-rules.py`. The linter MUST validate H1–H12 (per [Task 073 hard-rules spec](../073-novel-architect-hard-rules-validation/task.md)) against an `architecture.yaml`, AND validate the `worksheet_audit.step_*_set` body-schema invariant added in [Task 072's architecture.yaml schema growth](../072-novel-architect-phase2-worksheet-loop/task.md#closure-2026-05-11). The linter MUST write `<workspace>/<slug>/.architecture-validation.json` per the JSON-artefact contract declared in [ADR-0010](../../decisions/0010-novel-architect-error-tier-linter-policy.md) (consumed by Task 087's renderer wiring).

`done` when:

1. `tools/novel-architect-checks/` shared library exists with the literal file layout from `/sc:design §2`: `__init__.py`, `loader.py` (YAML loaders), `findings.py` (`Finding` dataclass + `Severity` enum + `emit_text` / `emit_json` / `exit_code`), `hard_rules.py` (H1–H12 + `WA.STEP_*_SET` rule implementations), `validation_report.py` (JSON-artefact writer).
2. `tools/check-hard-rules.py` thin entry point exists, imports from the shared library, and accepts `path/to/architecture.yaml` on argv.
3. Fixture corpus at `tools/novel-architect-checks/tests/fixtures/` contains ≥3 known-clean + ≥3 known-bad `architecture.yaml` files; bad fixtures cover at least H2 (Class double-assignment), H7 (PRCO-violation), and `WA.STEP_2_SET` (Classes step missing while `gate_3_approved: true`).
4. Pytest suite at `tools/novel-architect-checks/tests/` passes on `python3 -m pytest tools/novel-architect-checks/tests/ -v` with each H-rule + worksheet_audit rule covered by at least one green-path and one fail-path test.
5. `tools/check-governance.sh` carries a new ERROR-tier row invoking `tools/check-hard-rules.py` on staged diffs touching `skills/novel-architect*/` or `novel-projects/`. The row is **path-scoped**; non-narrative diffs pay zero cost.
6. `tools/check-maintenance-bypass.py` accepts rule-IDs of the shape `HR.H{1..12}.*` and `WA.STEP_{0..7,V}_SET` so transition false-positives can be waived via an open Task (per ADR-0010 precondition iii).
7. `tools/check-hard-rules.py` completes in <500ms on the reference `consciousness-novel` workspace and contributes <500ms to the aggregate ERROR-tier-stage budget (per ADR-0010 precondition ii).

## Context

[Task 070's friction log §"Sub-task summary"](../070-novel-architect-v110-epic/friction-log.md#sub-task-summary) explicitly deferred the hard-rules linter (`'tools/check-hard-rules.py' deferred`) at v1.1.0 close. v1.1.0 shipped the prose spec at [`skills/novel-architect-structure/methods/validation/hard-rules.md`](../../skills/novel-architect-structure/methods/validation/hard-rules.md) + [`assets/hard-rules-check.md`](../../skills/novel-architect-structure/assets/hard-rules-check.md), but the rules ran by reviewer attention only.

[Task 072's closure summary §2](../072-novel-architect-phase2-worksheet-loop/task.md#closure-2026-05-11) grew `architecture.yaml` with a `worksheet_audit` step-completion tracker (`step_0_set` through `step_v_set`). Per the prose spec, when `gate_3_approved: true` every `step_*_set` MUST be true; the body-schema check enforcing this never landed. Folding the worksheet_audit check into `check-hard-rules.py` is cheaper than a separate linter (same loader, same target file) and matches `/sc:design §1`'s pairing rationale.

The shared library is the seed of [Epic 083's](./../083-novel-architect-v120-enforcement-epic/task.md) `tools/novel-architect-checks/` package — Tasks 085 (phase-flow linters), 086 (canon-status linter), and 087 (renderer wiring) all depend on its loaders, Finding dataclass, and JSON-artefact writer.

Severity is ERROR-tier per [ADR-0010 Decision Outcome](../../decisions/0010-novel-architect-error-tier-linter-policy.md). Preconditions (i) fixture corpus, (ii) <500ms latency, (iii) maintenance-bypass wiring all materialize as acceptance criteria below.

## Plan

1. **Bootstrap the shared library structure** — create `tools/novel-architect-checks/{__init__.py, loader.py, findings.py, validation_report.py}` with the API surface declared in `/sc:design §2`. Findings dataclass + Severity enum + `emit_text/emit_json/exit_code()` shipped before any rule logic so subsequent rule modules import from a stable surface.
2. **Implement `hard_rules.py`** — pure functions per H-rule (`check_h1(loaded_yaml) -> list[Finding]`, ..., `check_h12(loaded_yaml) -> list[Finding]`) plus `check_worksheet_audit(loaded_yaml) -> list[Finding]` gated on `gate_3_approved: true`. Compose into `check_all()` returning aggregated findings.
3. **Fixture corpus + pytest suite** — ≥3 clean + ≥3 bad fixtures per rule family in `tools/novel-architect-checks/tests/fixtures/`; pytest modules `test_loader.py`, `test_findings.py`, `test_hard_rules.py`, `test_worksheet_audit.py`, `test_validation_report.py`. Each H-rule covered by ≥1 green + ≥1 red test.
4. **Wire `tools/check-hard-rules.py` entry point into `tools/check-governance.sh`** — path-scoped ERROR-tier row; verify <500ms latency on `consciousness-novel`; extend `tools/check-maintenance-bypass.py` rule-ID allowlist for `HR.H*` + `WA.STEP_*_SET`; run full `tools/check-governance.sh` baseline to confirm aggregate ERROR-tier-stage budget remains <2s.

## Todo

- [ ] 1. Create `tools/novel-architect-checks/__init__.py` + `findings.py` (Finding dataclass + Severity enum + emit helpers + exit_code).
- [ ] 2. Create `tools/novel-architect-checks/loader.py` (YAML loaders for `architecture.yaml`; tolerant of missing optional sections).
- [ ] 3. Create `tools/novel-architect-checks/validation_report.py` (JSON-artefact writer + schema-version 1.0 contract).
- [ ] 4. Create `tools/novel-architect-checks/hard_rules.py` (H1–H12 checks + worksheet_audit step-completion check + `check_all()`).
- [ ] 5. Build fixture corpus: ≥3 known-clean + ≥3 known-bad `architecture.yaml` files; bad fixtures cover H2, H7, WA.STEP_2_SET at minimum.
- [ ] 6. Author pytest suite: per-module tests + end-to-end test producing `architecture-validation.json` with expected shape.
- [ ] 7. Create `tools/check-hard-rules.py` thin CLI entry point.
- [ ] 8. Extend `tools/check-maintenance-bypass.py` rule-ID allowlist for `HR.H*` + `WA.STEP_*_SET`.
- [ ] 9. Add ERROR-tier row to `tools/check-governance.sh` path-scoped to `skills/novel-architect*/` and `novel-projects/`.
- [ ] 10. Run `tools/check-governance.sh` on the reference `consciousness-novel` workspace; confirm <500ms per linter + <2s aggregate budget; document timing in a comment block near the new row.

## Acceptance

```gherkin
Feature: tools/check-hard-rules.py enforces H1-H12 + worksheet_audit at ERROR-tier

  # anchor: 084.AC.1
  Scenario: Clean architecture.yaml passes hard-rules check
    Given an architecture.yaml satisfying H1-H12 and worksheet_audit.step_*_set: true (fixture: architecture-clean-1.yaml)
    When the agent runs tools/check-hard-rules.py path/to/architecture.yaml
    Then the linter MUST exit 0
    And the linter MUST write architecture-validation.json with summary.failed == 0
    And the JSON artefact MUST conform to the schema-version 1.0 contract declared in tools/novel-architect-checks/validation_report.py

  # anchor: 084.AC.2
  Scenario: H2 violation (Class double-assignment) fails hard-rules
    Given an architecture.yaml where two throughlines share a Class (fixture: architecture-bad-h2.yaml)
    When the agent runs tools/check-hard-rules.py path/to/architecture.yaml
    Then the linter MUST exit 1
    And stderr MUST contain "HR.H2.CLASS_DOUBLE_ASSIGN"
    And architecture-validation.json MUST report hard_rules.H2.status == "fail"

  # anchor: 084.AC.3
  Scenario: worksheet_audit step missing while gate_3_approved fails
    Given an architecture.yaml with gate_3_approved: true and worksheet_audit.step_2_set: false (fixture: architecture-bad-wa-step2.yaml)
    When the agent runs tools/check-hard-rules.py path/to/architecture.yaml
    Then the linter MUST exit 1
    And stderr MUST contain "WA.STEP_2_SET"
    And architecture-validation.json MUST report worksheet_audit.step_2_set == false

  # anchor: 084.AC.4
  Scenario: Shared-library contract is importable by sibling linters
    Given tools/novel-architect-checks/ exists with the layout per /sc:design §2
    When sibling sub-tasks 085 or 086 import "from tools.novel_architect_checks.findings import Finding, Severity, emit_text"
    Then the imports MUST succeed without ModuleNotFoundError
    And Finding(code="HR.H1.X", severity=Severity.ERROR, path=..., line=None, detail="...", remediation="...") MUST construct without TypeError

  # anchor: 084.AC.5
  Scenario: Governance integration meets ADR-0010 preconditions
    Given tools/check-hard-rules.py is registered in tools/check-governance.sh at ERROR-tier
    And tools/check-maintenance-bypass.py rule-ID allowlist includes "HR.H1..HR.H12" and "WA.STEP_0_SET..WA.STEP_V_SET"
    When the agent runs tools/check-governance.sh on the reference consciousness-novel workspace
    Then tools/check-hard-rules.py MUST complete in <500ms
    And the aggregate ERROR-tier-stage budget delta MUST be <2s versus the pre-084 baseline
```

## Links

- Parent Epic: [Task 083](../083-novel-architect-v120-enforcement-epic/task.md)
- Blocks: [Task 085](../085-novel-architect-phase-flow-linters/task.md), [Task 086](../086-novel-architect-canon-status-linter/task.md), [Task 087](../087-novel-architect-render-architecture-wiring/task.md)
- Source prose specs: [Task 073 hard-rules](../073-novel-architect-hard-rules-validation/task.md), [Task 072 worksheet-loop closure §2](../072-novel-architect-phase2-worksheet-loop/task.md#closure-2026-05-11)
- Governing ADR: [ADR-0010](../../decisions/0010-novel-architect-error-tier-linter-policy.md)
- Governing specs: [`TASK.md`](../../TASK.md), [`PRE_COMMIT.md`](../../PRE_COMMIT.md), [`SKILLS.md`](../../SKILLS.md)
- Skill reference: [`skills/novel-architect-structure/methods/validation/hard-rules.md`](../../skills/novel-architect-structure/methods/validation/hard-rules.md), [`assets/hard-rules-check.md`](../../skills/novel-architect-structure/assets/hard-rules-check.md)
- Implementation target: [`tools/check-governance.sh`](../../tools/check-governance.sh), [`tools/check-maintenance-bypass.py`](../../tools/check-maintenance-bypass.py)
