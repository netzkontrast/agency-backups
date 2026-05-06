---
type: note
status: draft
slug: task-036-st1-tooling-readme-frontmatter-validator
summary: "Subtask ST-1: ship tools/check-readme-frontmatter.py — promotes FOLDERS.md F.5 from SHOULD to mechanically-enforced MUST."
created: 2026-05-06
updated: 2026-05-06
---

# ST-1: `check-readme-frontmatter` — F.5 SHOULD → MUST

**Executor:** main-agent

**Insertion point:** `[2/5]` directory-structure linter — extends `tools/lint-structure.py`.

**Parallelism:** Phase A (parallel) — runs concurrently with ST-2. No inter-dependencies.

## Goal

Ship `tools/check-readme-frontmatter.py` that scans every operational-folder `readme.md` and verifies L1 Vault Core frontmatter is present (type, status, slug, summary, created, updated). Promotes F.5 from SHOULD to mechanically-enforced MUST in the post-Task-035 amendment.

## Falsification

Wrong cut **iff** legitimate readmes (e.g. provider-folder `readme.md` under `/research/<provider>/`) need different frontmatter shape. Mitigation: the linter honours the `types.index` and `types.readme` patterns from `header-ontology.json` and falls back to L1 only.

## Inputs

- `FOLDERS.md` F.5 (rule statement).
- `maintenance/schemas/header-ontology.json` (type-aware required-key matrix).
- `tools/fm/_core.py`, `tools/fm/validate.py`.

## Acceptance Criteria

1. **Surface.** `python3 tools/check-readme-frontmatter.py [<paths>]`.
2. **Checks.** L1 Vault Core key presence + slug-vs-folder agreement.
3. **Tests.** `tests/test_readme_frontmatter.py` covers: clean, missing-key, slug-mismatch, exempt provider folder.
4. **Integration.** ERROR-tier in step `[2/5]` of `tools/check-governance.sh`.

## Dependencies

None. Phase A.

## Estimated Effort

Small (~80 LOC + 60 LOC tests).
