---
type: note
status: draft
slug: task-034-st3-tooling-framework-declaration-validator
summary: "Subtask ST-3: ship tools/check-prompt-framework-declaration.py — verifies every /prompts/<slug>/prompt.md declares one of the canonical frameworks per PROMPT.md §4.3."
created: 2026-05-06
updated: 2026-05-06
---

# ST-3: `check-prompt-framework-declaration` — Mechanizes P.5.2

**Executor:** main-agent

**Insertion point:** `[opt]` WARN-tier — runs only on changed `/prompts/<slug>/prompt.md` files.

## Goal

Ship `tools/check-prompt-framework-declaration.py` that scans `/prompts/<slug>/prompt.md` and verifies (a) frontmatter `prompt_framework` is set to a canonical value (`RISEN`, `RISE-DX`, `ReAct`, `RISEN+ReAct`, `CoT`, or the post-ST-1-decision-tree-extended set), (b) a `## Framework` section in the body exists and matches the frontmatter value, (c) the body declares why this framework fits.

## Falsification

Wrong cut **iff** ST-1's empirical FPR study shows P.5.2 framework-declaration enforcement causes >20% false-positive rate on the existing prompt corpus. Mitigation: the linter is WARN-tier only.

## Inputs

- ST-1 output: `research/prompt-engineering-principle-mechanizability/output/SPEC.md` §3 framework-declaration recipe.
- `PROMPT.md` §4.3 (canonical framework list).
- All `/prompts/<slug>/prompt.md` (test corpus).
- `tools/fm/_core.py` (frontmatter parser).
- `tools/fm/extract.py --section Framework` (body section extraction).

## Acceptance Criteria

1. **Surface.** `python3 tools/check-prompt-framework-declaration.py <prompt.md>` exits 0 (pass) or 2 (WARN).
2. **Checks.** Frontmatter+body framework declaration consistency per ST-1 SPEC §3.
3. **Tests.** `tests/test_prompt_framework_declaration.py` covers: missing frontmatter, missing section, mismatch between frontmatter and section, valid declaration.
4. **Integration.** `tools/check-governance.sh` runs WARN-tier on changed `/prompts/<slug>/prompt.md`.

## Dependencies

ST-1 MUST land first.

## Estimated Effort

Small (~80 LOC + 60 LOC tests).
