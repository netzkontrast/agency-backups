---
type: prompt
status: active
slug: tooling-per-rule-waiver-mechanism
summary: "Refactor `tools/.frontmatter-waivers` from per-file scope to per-rule scope. Each waiver row now carries (path-glob, rule-id, rationale, expires) where rule-id is a diagnostic code (e.g., `L1.summary-too-long`, `ADR.A.3.5`, `R.4.4`). Clo..."
created: 2026-05-06
updated: 2026-05-06
prompt_kind: task-spec
prompt_framework: RISEN+ReAct
prompt_target_agent: "Claude Code"
prompt_relates_to_task: pre-commit-spec-integration
prompt_spawned_from_research: ""
---

# ST-3: `per-rule-waiver-mechanism` — PC.7.B Refactor — Task-Spec Prompt

## Framework

RISEN+ReAct. The prompt declares the framework in frontmatter (`prompt_framework: RISEN+ReAct`) and restates it here for `fm-validate` header conformance. The R/I/S/E sections below carry the canonical roles; a final **Constraints** section groups normative scope/failure rules per repo convention.

## R — Role

You are the **main-agent** dispatched to execute subtask ST-3 of [Task pre-commit-spec-integration](../../tasks/037-pre-commit-spec-integration/task.md). Your remit is bounded by the Acceptance Criteria in [`brief.md`](./brief.md); you MUST NOT expand scope beyond those criteria without surfacing the divergence in `friction-log.md`.

**Parallelism:** Phase A (parallel) — runs concurrently with ST-1, ST-2. No inter-dependencies..

## I — Input

- `PRE_COMMIT.md` §7.B (current per-file rule + acknowledged weakness).
- Current `tools/.frontmatter-waivers` corpus.
- `tools/fm/validate.py` (waiver loader).
- `tools/adr/cli.py` (`ADR.A.*` diagnostic codes that must be accepted as rule-ids).
- `tasks/037-pre-commit-spec-integration/task.md` — parent task chain-level context.

## S — Steps

1. Satisfy acceptance criterion: `tools/.frontmatter-waivers` schema is `<path-glob>\t<rule-id>\t<rationale>\t<expires-iso8601>` (TSV).
2. Satisfy acceptance criterion: Migration script `tools/scripts/migrate-waivers.py` translates legacy per-file rows to per-rule wildcard rows.
3. Satisfy acceptance criterion: `tools/fm/validate.py` accepts the new format; rejects mixed legacy+new in one file.
4. Satisfy acceptance criterion: **Tests.** `tests/fm/test_per_rule_waivers.py` covers: per-rule match, wildcard, expired, malformed, mixed-format-rejection.
5. Satisfy acceptance criterion: `tools/adr/cli.py validate` correctly applies ADR-scope waivers.
6. Run `tools/check-governance.sh` and resolve every ERROR before committing.
7. Author or update `tasks/037-pre-commit-spec-integration/friction-log.md` (or note that none is required for this subtask) and commit per the parent task's commit-message convention.

## E — Expectations

- `tools/.frontmatter-waivers` schema is `<path-glob>\t<rule-id>\t<rationale>\t<expires-iso8601>` (TSV).
- Migration script `tools/scripts/migrate-waivers.py` translates legacy per-file rows to per-rule wildcard rows.
- `tools/fm/validate.py` accepts the new format; rejects mixed legacy+new in one file.
- **Tests.** `tests/fm/test_per_rule_waivers.py` covers: per-rule match, wildcard, expired, malformed, mixed-format-rejection.
- `tools/adr/cli.py validate` correctly applies ADR-scope waivers.
- `tools/check-governance.sh` exits 0 on the produced commit.
- Commit message follows the parent task's convention; the commit cites `Task 037 ST-3` in its trailer.

## Constraints

- Dependency: None. Phase A.
- MUST NOT trigger the subtask's Falsification clause: Wrong cut **iff** the new format breaks parsing of existing per-file waivers. Mitigation: a one-time migration script translates legacy per-file waivers to per-rule waivers using the rule-id `*` (wildcard) — semantically identical. Migration runs once in this subtask; legacy format support is dropped after.
- MUST NOT inline this prompt's Goal/Inputs/Acceptance back into the subtask file — the subtask body is now a thin pointer per Task 041.
- MUST run `tools/check-governance.sh` before pushing; a non-zero exit MUST block the push.
- SHOULD cite the parent task's `task_id` in any commit-message trailer for traceability.
