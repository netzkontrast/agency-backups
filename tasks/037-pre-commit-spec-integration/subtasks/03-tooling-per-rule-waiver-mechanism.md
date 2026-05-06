---
type: note
status: draft
slug: task-037-st3-tooling-per-rule-waiver-mechanism
summary: "Subtask ST-3: refactor tools/.frontmatter-waivers from per-file to per-rule scope. Accepts ADR.A.* diagnostic codes from §7.C as valid rule scopes."
created: 2026-05-06
updated: 2026-05-06
---

# ST-3: `per-rule-waiver-mechanism` — PC.7.B Refactor

**Executor:** main-agent

**Insertion point:** `[1/5]` frontmatter linter — modifies the existing waiver-loading pathway in `tools/fm/validate.py`.

## Goal

Refactor `tools/.frontmatter-waivers` from per-file scope to per-rule scope. Each waiver row now carries (path-glob, rule-id, rationale, expires) where rule-id is a diagnostic code (e.g., `L1.summary-too-long`, `ADR.A.3.5`, `R.4.4`). Closes the spec-acknowledged weakness in PC.7.B.

## Falsification

Wrong cut **iff** the new format breaks parsing of existing per-file waivers. Mitigation: a one-time migration script translates legacy per-file waivers to per-rule waivers using the rule-id `*` (wildcard) — semantically identical. Migration runs once in this subtask; legacy format support is dropped after.

## Inputs

- `PRE_COMMIT.md` §7.B (current per-file rule + acknowledged weakness).
- Current `tools/.frontmatter-waivers` corpus.
- `tools/fm/validate.py` (waiver loader).
- `tools/adr/cli.py` (`ADR.A.*` diagnostic codes that must be accepted as rule-ids).

## Acceptance Criteria

1. `tools/.frontmatter-waivers` schema is `<path-glob>\t<rule-id>\t<rationale>\t<expires-iso8601>` (TSV).
2. Migration script `tools/scripts/migrate-waivers.py` translates legacy per-file rows to per-rule wildcard rows.
3. `tools/fm/validate.py` accepts the new format; rejects mixed legacy+new in one file.
4. **Tests.** `tests/fm/test_per_rule_waivers.py` covers: per-rule match, wildcard, expired, malformed, mixed-format-rejection.
5. `tools/adr/cli.py validate` correctly applies ADR-scope waivers.

## Dependencies

None. Phase A.

## Estimated Effort

Medium (~150 LOC refactor + migration + 100 LOC tests).
