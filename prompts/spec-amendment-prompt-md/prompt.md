---
type: prompt
status: active
slug: spec-amendment-prompt-md
summary: "Land the PROMPT.md edits closing Task 034: ≥6 Gherkin scenarios per P.B.1-P.B.6 anchors (one per principle), §4.3 framework-selection decision tree, §6.5 provider-folder backward-link clarification, references to ST-2/ST-3 linters."
created: 2026-05-06
updated: 2026-05-06
prompt_kind: task-spec
prompt_framework: RISEN+ReAct
prompt_target_agent: "Claude Code"
prompt_relates_to_task: prompt-spec-integration
prompt_spawned_from_research: ""
---

# ST-4: Spec Amendment — PROMPT.md — Task-Spec Prompt

## Framework

RISEN+ReAct. The prompt declares the framework in frontmatter (`prompt_framework: RISEN+ReAct`) and restates it here for `fm-validate` header conformance. The R/I/S/E sections below carry the canonical roles; a final **Constraints** section groups normative scope/failure rules per repo convention.

## R — Role

You are the **main-agent** dispatched to execute subtask ST-4 of [Task prompt-spec-integration](../../tasks/034-prompt-spec-integration/task.md). Your remit is bounded by the Acceptance Criteria in [`brief.md`](./brief.md); you MUST NOT expand scope beyond those criteria without surfacing the divergence in `friction-log.md`.

**Parallelism:** Phase B (sequential) — depends on ST-1, ST-2, ST-3. MUST wait for Phase A converge..

## I — Input

- ST-1 output: `research/prompt-engineering-principle-mechanizability/output/SPEC.md`.
- ST-2 implementation: `tools/check-prompt-self-containedness.py`.
- ST-3 implementation: `tools/check-prompt-framework-declaration.py`.
- `skills/research-prompt-optimizer/SKILL.md` (decision-tree prior art).
- `tasks/034-prompt-spec-integration/task.md` — parent task chain-level context.

## S — Steps

1. Satisfy acceptance criterion: PROMPT.md §6 has ≥6 new Gherkin scenarios anchored P.B.1..P.B.6 (one per topic).
2. Satisfy acceptance criterion: PROMPT.md §4.3 has a decision tree (≥5 nodes) replacing the current 5-line list.
3. Satisfy acceptance criterion: PROMPT.md §6.5 explains `prompt_spawned_from_research` resolution for `/research/<provider>/<slug>/`.
4. Satisfy acceptance criterion: PROMPT.md cites ST-2 + ST-3 linters in §6 (Pre-Commit Checks).
5. Satisfy acceptance criterion: `tools/check-governance.sh` exits 0.
6. Run `tools/check-governance.sh` and resolve every ERROR before committing.
7. Author or update `tasks/034-prompt-spec-integration/friction-log.md` (or note that none is required for this subtask) and commit per the parent task's commit-message convention.

## E — Expectations

- PROMPT.md §6 has ≥6 new Gherkin scenarios anchored P.B.1..P.B.6 (one per topic).
- PROMPT.md §4.3 has a decision tree (≥5 nodes) replacing the current 5-line list.
- PROMPT.md §6.5 explains `prompt_spawned_from_research` resolution for `/research/<provider>/<slug>/`.
- PROMPT.md cites ST-2 + ST-3 linters in §6 (Pre-Commit Checks).
- `tools/check-governance.sh` exits 0.
- `tools/check-governance.sh` exits 0 on the produced commit.
- Commit message follows the parent task's convention; the commit cites `Task 034 ST-4` in its trailer.

## Constraints

- Dependency: ST-1, ST-2, ST-3 MUST land first.
- MUST NOT trigger the subtask's Falsification clause: Wrong cut **iff** the framework decision tree adds >5 new framework names beyond the canonical RISEN/RISE-DX/ReAct/RISEN+ReAct/CoT. Mitigation: ST-1's research output bounds the set.
- MUST NOT inline this prompt's Goal/Inputs/Acceptance back into the subtask file — the subtask body is now a thin pointer per Task 041.
- MUST run `tools/check-governance.sh` before pushing; a non-zero exit MUST block the push.
- SHOULD cite the parent task's `task_id` in any commit-message trailer for traceability.
