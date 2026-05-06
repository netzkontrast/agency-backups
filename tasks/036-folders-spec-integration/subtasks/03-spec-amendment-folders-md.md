---
type: note
status: draft
slug: task-036-st3-spec-amendment-folders-md
summary: "Subtask ST-3 (Phase B): apply FOLDERS.md edits — F.1.1 provider+/decisions/ exemption, F.5 promotion to MUST, F.6 dual-surface guidance, ≥5 Gherkin scenarios per F.B.1-F.B.5."
created: 2026-05-06
updated: 2026-05-06
---

# ST-3: Spec Amendment — FOLDERS.md

**Executor:** main-agent

## Goal

Land the FOLDERS.md edits per Task 036 (a)-(d): F.1.1 explicit provider-research + `/decisions/` exemption clause, F.5 promotion to MUST (cross-references ST-1), F.6 dual-surface guidance (cross-references ST-2), ≥5 Gherkin scenarios per F.B.1-F.B.5 anchors.

## Falsification

Wrong cut **iff** F.5 promotion to MUST creates retroactive ERRORs against existing readmes (would break the working tree). Mitigation: ST-1 linter is authored before ST-3 amendment lands; the linter is run pre-amendment to surface fixable readmes; readmes are fixed in the same commit as the amendment.

## Inputs

- ST-1 implementation: `tools/check-readme-frontmatter.py`.
- ST-2 implementation: `tools/check-audit-graph-consistency.py`.
- `research/governance-specs-update-research/output/SPEC.md` §3 (FOLDERS.md amendments).
- `maintenance/schemas/header-ontology.json:208` (decisions/ pattern).

## Acceptance Criteria

1. FOLDERS.md F.1.1 explicitly enumerates `/research/<provider>/<slug>/` + `/decisions/` as exempt.
2. FOLDERS.md F.5 is MUST (not SHOULD) and cites the ST-1 linter.
3. FOLDERS.md F.6 documents dual-surface; cites ST-2 as the consistency check.
4. ≥5 Gherkin scenarios anchored F.B.1-F.B.5 land in a new "## Acceptance Criteria" section.
5. `tools/check-governance.sh` exits 0 (including ST-1 / ST-2).

## Dependencies

ST-1, ST-2 MUST land first.

## Estimated Effort

Small (~1 hour).
