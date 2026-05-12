---
type: task
status: active
slug: novel-architect-render-architecture-wiring
summary: "Wire skills/novel-architect/render/render_architecture.py Phase 2.13 status-view to consume <workspace>/<slug>/.architecture-validation.json produced by Task 084's check-hard-rules.py. Surface H1-H12 pass/fail markers + worksheet_audit step completion in the rendered status-view; emit a stale-artefact warning when checked_at < architecture.yaml mtime. Coupling is artefact-based (JSON read) not import-based — preserves skill portability for claude.ai deployment per AGENTS.md Skills Architecture."
created: 2026-05-12
updated: 2026-05-12
task_id: "087"
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
  - skills/novel-architect/render/render_architecture.py
  - skills/novel-architect/render/tests/test_render_architecture.py
---

# Task 087 — Render-Architecture Wiring

## Goal

Extend `skills/novel-architect/render/render_architecture.py` so its Phase 2.13 status-view consumes `<workspace>/<slug>/.architecture-validation.json` (produced by [Task 084's `tools/check-hard-rules.py`](../084-novel-architect-storyform-integrity-linter/task.md)) and surfaces H1–H12 pass/fail markers plus `worksheet_audit.step_*_set` completion flags. The coupling MUST be artefact-based (JSON read with file-mtime freshness check), NOT import-based — the skill MUST remain deployable to claude.ai per [AGENTS.md "Skills Architecture"](../../AGENTS.md#skills-architecture--container-capabilities-and-citation-protocol) without `tools/novel-architect-checks/` being importable.

`done` when:

1. `render_architecture.py` reads `<workspace>/<slug>/.architecture-validation.json` when rendering the Phase 2.13 status-view; the path is derived from the same workspace-root resolution `render_intent.py` already uses.
2. The rendered status-view includes a "Hard Rules" sub-section listing each of H1–H12 with a 🟢 / 🔴 marker derived from `hard_rules.H{N}.status`; a 🔴 row additionally shows the `detail` and `remediation` strings from the JSON artefact.
3. The rendered status-view includes a "Worksheet Audit" sub-section listing `step_0_set` through `step_v_set` with ✓ / ✗ markers derived from `worksheet_audit.step_*_set`.
4. **Stale-artefact fallback**: when `.architecture-validation.json` is missing OR `checked_at` is older than the `architecture.yaml` mtime, the rendered status-view MUST emit `⚠ Validation report stale — rerun tools/check-hard-rules.py` in place of the markers AND MUST NOT crash. The renderer MUST gracefully tolerate a missing or malformed JSON file.
5. Pytest cases at `skills/novel-architect/render/tests/test_render_architecture.py` extended with: (a) fresh-artefact → markers render; (b) stale-artefact (mocked mtime) → warning renders; (c) missing-artefact → warning renders; (d) malformed-JSON (invalid schema_version) → warning renders + no crash.
6. The renderer continues to function with `tools/novel-architect-checks/` absent from the Python path (skill-portability check; mock-import or path-removal in pytest).
7. v1.2.0 changelog entry in `skills/novel-architect/references/learnings.md` references this Task's wiring + the JSON contract version it targets.

## Context

[Task 072's closure §2](../072-novel-architect-phase2-worksheet-loop/task.md#closure-2026-05-11) grew `architecture.yaml` with `story_points`, `crucial_element`, `signposts`, `journeys`, `ending_type`, `genre_mode`, and `worksheet_audit` fields. [Task 070's friction log](../070-novel-architect-v110-epic/friction-log.md#sub-task-summary) closed the v1.1.0 Epic without updating `render_architecture.py` to surface validation status from the (then-deferred) hard-rules check. This Task is the missing wiring.

The JSON-artefact contract is declared in [ADR-0010 Cross-references](../../decisions/0010-novel-architect-error-tier-linter-policy.md) (the schema-version 1.0 shape produced by Task 084's `validation_report.py`). The renderer reads, never writes, the JSON artefact; the linter writes, never reads. This producer-consumer split keeps the renderer pure with respect to the validation state and avoids the import-coupling that would break claude.ai skill deployment.

Per [Epic 083 sub-task DAG](../083-novel-architect-v120-enforcement-epic/task.md#dependency-graph), this Task `task_blocked_by: [084]` because the JSON-artefact schema must be locked in 084 before 087 can write a stable reader for it. 087 does NOT depend on 085 or 086 (they produce their own findings but the renderer's Phase 2.13 view only consumes hard-rules + worksheet-audit data from 084).

## Plan

1. **Add JSON-artefact reader** to `render_architecture.py` — a private `_load_validation_report(workspace_root: pathlib.Path) -> dict | None` helper that returns `None` on missing/malformed/stale artefact and a parsed dict on fresh. `_is_stale(report, architecture_yaml_path)` compares `report["checked_at"]` to `architecture_yaml_path.stat().st_mtime`.
2. **Extend the Phase 2.13 status-view markdown rendering** — new "Hard Rules" + "Worksheet Audit" sub-sections gated on `_load_validation_report()` returning non-None. Stale/missing/malformed → emit the warning string instead. Existing rendering paths untouched.
3. **Author pytest coverage** — fresh-artefact / stale-artefact / missing-artefact / malformed-artefact paths; plus a skill-portability test that removes `tools/` from `sys.path` and confirms `render_architecture.py` still imports.
4. **Append v1.2.0 changelog entry** to `skills/novel-architect/references/learnings.md` citing the JSON-contract version + this Task's anchor for downstream cross-references.

## Todo

- [ ] 1. Add `_load_validation_report()` + `_is_stale()` helpers to `render_architecture.py`.
- [ ] 2. Extend the Phase 2.13 status-view rendering with Hard Rules + Worksheet Audit sub-sections.
- [ ] 3. Implement the stale/missing/malformed fallback emitting the warning string without crashing.
- [ ] 4. Author pytest cases (4 fresh/stale/missing/malformed + 1 portability).
- [ ] 5. Confirm import-portability: `render_architecture.py` MUST import cleanly with `tools/` removed from `sys.path`.
- [ ] 6. Append v1.2.0 changelog entry to `skills/novel-architect/references/learnings.md` referencing this Task and the JSON contract version.
- [ ] 7. Run `python3 -m pytest skills/novel-architect/render/tests/test_render_architecture.py -v` → all new + existing tests green.

## Acceptance

```gherkin
Feature: render_architecture.py consumes .architecture-validation.json and renders pass/fail markers without coupling to tools/

  # anchor: 087.AC.1
  Scenario: Fresh artefact renders Hard Rules + Worksheet Audit markers
    Given a workspace with a fresh architecture-validation.json (checked_at > architecture.yaml mtime)
    And architecture-validation.json reports hard_rules.H7.status == "fail" with detail "PRCO violation: ..."
    When render_architecture.py renders the Phase 2.13 status-view
    Then the output MUST include a "## Hard Rules" sub-section listing H1-H12
    And the H7 row MUST display 🔴 followed by the detail and remediation strings
    And the output MUST include a "## Worksheet Audit" sub-section listing step_0_set through step_v_set with ✓/✗ markers

  # anchor: 087.AC.2
  Scenario: Stale artefact triggers freshness warning
    Given a workspace where architecture.yaml has been edited after architecture-validation.json was written (mocked mtime)
    When render_architecture.py renders the Phase 2.13 status-view
    Then the output MUST contain "⚠ Validation report stale — rerun tools/check-hard-rules.py"
    And the output MUST NOT contain any pass/fail markers from the stale report

  # anchor: 087.AC.3
  Scenario: Missing artefact triggers freshness warning
    Given a workspace where architecture-validation.json does not exist
    When render_architecture.py renders the Phase 2.13 status-view
    Then the output MUST contain "⚠ Validation report stale — rerun tools/check-hard-rules.py"
    And render_architecture.py MUST NOT raise

  # anchor: 087.AC.4
  Scenario: Skill portability preserved (no import coupling to tools/)
    Given sys.path has been pruned to exclude any path containing "tools/"
    When import skills.novel_architect.render.render_architecture
    Then the import MUST succeed without ModuleNotFoundError
    And calling render_architecture.render_status_view(...) MUST behave per AC.1-AC.3 above
```

## Links

- Parent Epic: [Task 083](../083-novel-architect-v120-enforcement-epic/task.md)
- Blocked by: [Task 084](../084-novel-architect-storyform-integrity-linter/task.md) (JSON-artefact contract)
- Upstream context: [Task 072 closure §2](../072-novel-architect-phase2-worksheet-loop/task.md#closure-2026-05-11) (architecture.yaml schema growth)
- Governing ADR: [ADR-0010](../../decisions/0010-novel-architect-error-tier-linter-policy.md)
- Governing specs: [`TASK.md`](../../TASK.md), [`SKILLS.md`](../../SKILLS.md), [`AGENTS.md`](../../AGENTS.md) ("Skills Architecture" — skill-portability constraint)
- Implementation target: [`skills/novel-architect/render/render_architecture.py`](../../skills/novel-architect/render/render_architecture.py)
- Test target: [`skills/novel-architect/render/tests/test_render_architecture.py`](../../skills/novel-architect/render/tests/test_render_architecture.py)
- Changelog target: [`skills/novel-architect/references/learnings.md`](../../skills/novel-architect/references/learnings.md)
