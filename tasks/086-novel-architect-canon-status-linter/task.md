---
type: task
status: active
slug: novel-architect-canon-status-linter
summary: "Ship tools/check-canon-status.py at ERROR-tier validating canon-meta.md entries against the canon-status hierarchy (confirmed > provisional > disputed > uncertain > decanonized) per Task 076 prose spec. Linter fails when canon_status: disputed blocks an active phase OR canon_status: decanonized is still referenced from a non-archived NCP moment. Consumes the tools/novel-architect-checks/ shared library bootstrapped by Task 084."
created: 2026-05-12
updated: 2026-05-12
task_id: "086"
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
  - tools/novel-architect-checks/canon_status.py
  - tools/check-canon-status.py
  - tools/check-governance.sh
  - tools/check-maintenance-bypass.py
---

# Task 086 — Canon-Status Linter

## Goal

Ship `tools/check-canon-status.py` at ERROR-tier validating `canon-meta.md` entries against the canon-status hierarchy declared in [Task 076 prose spec](../076-novel-architect-canon-status-schema/task.md). The linter MUST fail on these violations:

| Rule-ID | Violation |
|---|---|
| `CS.DISPUTED_BLOCKS_ACTIVE` | `canon_status: disputed` entry referenced by a moment in an active (non-`archived`) Phase 4/5/6 NCP file |
| `CS.DECANONIZED_REFERENCED` | `canon_status: decanonized` entry referenced from any non-archived NCP file |
| `CS.MISSING_PROVENANCE` | `canon_status: disputed` entry lacks a `variants:` block enumerating ≥2 conflicting variants with provenance |
| `CS.INVALID_STATUS` | `canon_status` value not in `{confirmed, provisional, disputed, uncertain, decanonized}` |

`done` when:

1. `tools/novel-architect-checks/canon_status.py` exists with `walk_canon_meta(canon_meta_path) -> list[Entry]` + `walk_ncp_references(workspace_root) -> dict[entry_id, list[NcpRef]]` helpers + `check_canon_status()` rule function.
2. `tools/check-canon-status.py` thin CLI entry point exists, accepts `path/to/canon-meta.md` and (optionally) workspace root on argv.
3. Fixture corpus at `tools/novel-architect-checks/tests/fixtures/canon-meta/` contains ≥3 known-clean + ≥3 known-bad fixtures. Bad fixtures cover: `disputed` blocking an active Phase 5 moment (`CS.DISPUTED_BLOCKS_ACTIVE`); `decanonized` still referenced from Phase 6 (`CS.DECANONIZED_REFERENCED`); `disputed` without `variants:` block (`CS.MISSING_PROVENANCE`).
4. Pytest suite `tools/novel-architect-checks/tests/test_canon_status.py` passes with green-path + red-path per rule-ID.
5. `tools/check-canon-status.py` appears as an ERROR-tier row in `tools/check-governance.sh`, path-scoped to staged diffs touching `novel-projects/*/canon-meta.md` or `novel-projects/*/ncp/`.
6. `tools/check-maintenance-bypass.py` rule-ID allowlist extended for `CS.DISPUTED_BLOCKS_ACTIVE`, `CS.DECANONIZED_REFERENCED`, `CS.MISSING_PROVENANCE`, `CS.INVALID_STATUS`.
7. Linter completes in <500ms on the reference `consciousness-novel` workspace.

## Context

[Task 076 closure](../076-novel-architect-canon-status-schema/task.md) shipped the canon-status lifecycle prose spec at [`skills/novel-architect-structure/assets/canon-meta-schema.md`](../../skills/novel-architect-structure/assets/canon-meta-schema.md), adopting the Dual-Kernel entity-conflict schema (`canon_status` hierarchy: `confirmed > provisional > disputed > uncertain > decanonized`; multi-variant entries carry explicit provenance via `variants:` block). [Task 070's friction log](../070-novel-architect-v110-epic/friction-log.md#sub-task-summary) deferred the corresponding linter:

> | 076 | done | `assets/canon-meta-schema.md` (canon-status lifecycle) | CLI linter `tools/check-canon-status.py` deferred |

Without mechanical enforcement, a `disputed` entry can continue blocking an active phase and a `decanonized` entry can remain referenced in NCP moments — both states violate the prose spec but render visually unremarkable in `render_intent.py` / `render_architecture.py` status-views. This linter closes that gap.

Per [Epic 083 sub-task DAG](../083-novel-architect-v120-enforcement-epic/task.md#dependency-graph), this Task is independent from 085 and 087 — it touches a different file domain (`canon-meta.md` + NCP references) and shares only the Findings emitter from the [Task 084 shared library](../084-novel-architect-storyform-integrity-linter/).

## Plan

1. **Add `canon_status.py` to the shared library** — `walk_canon_meta()` parses `canon-meta.md` frontmatter + body entries; `walk_ncp_references()` scans NCP moment files for entity references; both helpers return structured objects.
2. **Implement `check_canon_status()` rule function** — composes the four rule-IDs (`CS.DISPUTED_BLOCKS_ACTIVE`, `CS.DECANONIZED_REFERENCED`, `CS.MISSING_PROVENANCE`, `CS.INVALID_STATUS`) over the canon-meta entries and (optional) workspace NCP corpus.
3. **Build fixture corpus + pytest suite** — ≥3 clean + ≥3 bad `canon-meta.md` files plus supporting NCP fixtures for the reference-detection rules. Test each rule-ID green/red.
4. **Wire `tools/check-canon-status.py` into governance integration** — thin CLI entry point; ERROR-tier row in `tools/check-governance.sh` (path-scoped); extend `tools/check-maintenance-bypass.py` allowlist; verify <500ms latency.

## Todo

- [ ] 1. Add `tools/novel-architect-checks/canon_status.py` with `walk_canon_meta()` + `walk_ncp_references()` + `check_canon_status()`.
- [ ] 2. Build fixture corpus at `tools/novel-architect-checks/tests/fixtures/canon-meta/` (3 clean + 3 bad covering each rule-ID).
- [ ] 3. Author `tools/novel-architect-checks/tests/test_canon_status.py`.
- [ ] 4. Create `tools/check-canon-status.py` CLI entry point.
- [ ] 5. Extend `tools/check-maintenance-bypass.py` rule-ID allowlist.
- [ ] 6. Add ERROR-tier row to `tools/check-governance.sh`, path-scoped to canon-meta + NCP paths.
- [ ] 7. Run `tools/check-governance.sh` on `consciousness-novel`; confirm <500ms latency and aggregate budget <2s.

## Acceptance

```gherkin
Feature: tools/check-canon-status.py enforces the canon-status hierarchy at ERROR-tier

  # anchor: 086.AC.1
  Scenario: Clean canon-meta.md passes canon-status check
    Given a canon-meta.md with entries at valid statuses and no decanonized references in active NCPs (fixture: canon-meta-clean-1.md)
    When the agent runs tools/check-canon-status.py path/to/canon-meta.md
    Then the linter MUST exit 0
    And stderr MUST NOT contain any "CS." finding code

  # anchor: 086.AC.2
  Scenario: Disputed entry blocks active Phase 5 moment fails canon-status
    Given a canon-meta.md with entry "char-Aurelia" at canon_status: disputed
    And a Phase 5 scene-matrix moment "M-12" referencing entity "char-Aurelia"
    When the agent runs tools/check-canon-status.py path/to/canon-meta.md
    Then the linter MUST exit 1
    And stderr MUST contain "CS.DISPUTED_BLOCKS_ACTIVE"
    And the finding MUST include the offending entity_id and moment_id

  # anchor: 086.AC.3
  Scenario: Decanonized entry still referenced fails canon-status
    Given a canon-meta.md with entry "loc-Spire" at canon_status: decanonized
    And a non-archived NCP file referencing "loc-Spire" (fixture: canon-meta-bad-decanonized.md + ncp/scene-matrix.md)
    When the agent runs tools/check-canon-status.py path/to/canon-meta.md
    Then the linter MUST exit 1
    And stderr MUST contain "CS.DECANONIZED_REFERENCED"

  # anchor: 086.AC.4
  Scenario: Disputed entry without variants block fails canon-status
    Given a canon-meta.md with an entry at canon_status: disputed but no variants: block (fixture: canon-meta-bad-no-variants.md)
    When the agent runs tools/check-canon-status.py path/to/canon-meta.md
    Then the linter MUST exit 1
    And stderr MUST contain "CS.MISSING_PROVENANCE"
```

## Links

- Parent Epic: [Task 083](../083-novel-architect-v120-enforcement-epic/task.md)
- Blocked by: [Task 084](../084-novel-architect-storyform-integrity-linter/task.md) (shared library foundation)
- Source prose spec: [Task 076 canon-status-schema](../076-novel-architect-canon-status-schema/task.md)
- Governing ADR: [ADR-0010](../../decisions/0010-novel-architect-error-tier-linter-policy.md)
- Governing specs: [`TASK.md`](../../TASK.md), [`PRE_COMMIT.md`](../../PRE_COMMIT.md)
- Skill reference: [`skills/novel-architect-structure/assets/canon-meta-schema.md`](../../skills/novel-architect-structure/assets/canon-meta-schema.md)
- Implementation target: [`tools/check-governance.sh`](../../tools/check-governance.sh)
