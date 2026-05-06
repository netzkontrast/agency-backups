---
type: note
status: draft
slug: task-034-st4-spec-amendment-prompt-md
summary: "Subtask ST-4 (Phase B): apply the PROMPT.md edits — Gherkin scenarios per P.B.1-P.B.6 anchors, §4.3 framework-selection decision tree, §6.5 provider-folder clarification."
created: 2026-05-06
updated: 2026-05-06
---

# ST-4: Spec Amendment — PROMPT.md

**Executor:** main-agent

## Goal

Land the PROMPT.md edits closing Task 034: ≥6 Gherkin scenarios per P.B.1-P.B.6 anchors (one per principle), §4.3 framework-selection decision tree, §6.5 provider-folder backward-link clarification, references to ST-2/ST-3 linters.

## Falsification

Wrong cut **iff** the framework decision tree adds >5 new framework names beyond the canonical RISEN/RISE-DX/ReAct/RISEN+ReAct/CoT. Mitigation: ST-1's research output bounds the set.

## Inputs

- ST-1 output: `research/prompt-engineering-principle-mechanizability/output/SPEC.md`.
- ST-2 implementation: `tools/check-prompt-self-containedness.py`.
- ST-3 implementation: `tools/check-prompt-framework-declaration.py`.
- `skills/research-prompt-optimizer/SKILL.md` (decision-tree prior art).

## Acceptance Criteria

1. PROMPT.md §6 has ≥6 new Gherkin scenarios anchored P.B.1..P.B.6 (one per topic).
2. PROMPT.md §4.3 has a decision tree (≥5 nodes) replacing the current 5-line list.
3. PROMPT.md §6.5 explains `prompt_spawned_from_research` resolution for `/research/<provider>/<slug>/`.
4. PROMPT.md cites ST-2 + ST-3 linters in §6 (Pre-Commit Checks).
5. `tools/check-governance.sh` exits 0.

## Dependencies

ST-1, ST-2, ST-3 MUST land first.

## Estimated Effort

Medium (~2 hours; 6 scenarios + decision tree authoring).
