---
type: note
status: active
slug: tooling-adr-mirror-roundtrip-check-brief
summary: "Brief for prompt tooling-adr-mirror-roundtrip-check — addresses PR #79 review R-5: no mechanical check exists that a SPEC.md mirror row's source citation and adr_id match the corresponding decisions/<NNNN>-<slug>.md body."
created: 2026-05-07
updated: 2026-05-07
---

# Brief — tooling-adr-mirror-roundtrip-check

## Raw User Request

> Address PR #79 review finding R-5: file a follow-up prompt so the SPEC.md ↔ `decisions/<NNNN>-<slug>.md` round-trip gap surfaced in [Task 032's friction log](../../tasks/032-agents-spec-integration/friction-log.md) lands in the audit graph rather than the friction log alone.

## Target Audience

The dispatched executor for the successor Task that claims this prompt via `task_uses_prompts`. Default executor: **main-agent** (or a `python-expert` subagent for the linter implementation).

## Intended Model / Agent

Claude Code (or any agent that satisfies the executor declaration in the parent task).

## Use-Case Context

Task 032 ST-1 produced `research/adr-corpus-extraction-from-governance-specs/output/SPEC.md` cataloguing 18 IADRs in a condensed table-style mirror. The 5 P1 IADRs were filed as full MADR-shaped `decisions/0001-..0005-*.md`. **No mechanical check verifies that the SPEC mirror row's source `file:line` citation and `adr_id` match the corresponding `decisions/` body.** A maintainer who edits the SPEC mirror without re-deriving the body (or vice versa) introduces silent drift between the two artefacts. The PR #79 reviewer escalated this from FL1 friction to a normative R-5 follow-up because PROMPT.md §1 item 2 requires unsolved problems to land in `/prompts/`, not the friction log.

## Goal

Ship `tools/check-adr-mirror-roundtrip.py` that scans `research/adr-corpus-extraction-from-governance-specs/output/SPEC.md` for IADR rows ratified into `/decisions/`, parses each row's `adr_id` + source `file:line` citation, opens the corresponding `decisions/<NNNN>-<slug>.md`, and verifies:

1. **`adr_id` parity** — the mirror's recommended `ADR-NNNN` matches the body's frontmatter `adr_id`.
2. **Source-citation parity** — the mirror's quoted source clause's `file:line` resolves to a region whose text the body's `## Context and Problem Statement` section quotes verbatim (or via a tolerant whitespace-collapsed substring match).
3. **Slug parity** — the mirror's slug stem matches the body filename's slug stem.

## Falsification

Wrong cut **iff** the SPEC mirror format diverges from a row-shaped pattern such that no parser can extract `(adr_id, slug, source_citation)` deterministically. Mitigation: the linter MUST refuse to run on a SPEC.md whose row schema does not pass a structural pre-check, exiting 2 with a `MIRROR.SCHEMA` diagnostic rather than producing false positives.

## Inputs

- `research/adr-corpus-extraction-from-governance-specs/output/SPEC.md` — the mirror (parsed for ratified rows).
- `decisions/<NNNN>-<slug>.md` — the bodies (parsed for `adr_id` + Context section).
- `research/adr-spec-research-synthesis/output/SPEC.md` — canonical MADR shape, for citation-format reference.
- `tools/fm/_core.py` — frontmatter parser.

## Acceptance Criteria

1. **Surface.** `python3 tools/check-adr-mirror-roundtrip.py` exits 0 (parity holds) or 2 (WARN — drift detected).
2. **Diagnostic codes.** `MIRROR.ID_MISMATCH` (adr_id), `MIRROR.SOURCE_DRIFT` (citation text), `MIRROR.SLUG_MISMATCH` (filename slug), `MIRROR.SCHEMA` (row-parse failure).
3. **Tests.** `tools/tests/test_adr_mirror_roundtrip.py` covers each diagnostic code with fixtures + a positive case (no drift).
4. **Integration.** Add an `[adv]` advisory block to `tools/check-governance.sh` after the `[5/6]` ADR validator. Advisory only — never sets FAIL=1 (matches the polarity / assumption-log pattern).
5. **Cookbook.** One-line entry added to `tools/readme.md`.

## Dependencies

None. Builds atop existing artefacts from Task 032 ST-1; no parallel coordination required.

## Estimated Effort

Small (~150 LOC + 100 LOC tests; row-parser is the bulk).
