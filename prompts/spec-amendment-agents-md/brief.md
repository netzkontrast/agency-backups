---
type: note
status: active
slug: spec-amendment-agents-md-brief
summary: "Brief for prompt spec-amendment-agents-md — extracted from tasks/032-agents-spec-integration/subtasks/05-spec-amendment-agents-md.md per Task 041 (PR #70 review C.3 audit-graph repair)."
created: 2026-05-06
updated: 2026-05-06
---

# Brief — ST-5: Spec Amendment — AGENTS.md

## Raw User Request

> Extract the inlined Execution Brief from `tasks/032-agents-spec-integration/subtasks/05-spec-amendment-agents-md.md` (ST-5) into a registered `/prompts/<slug>/` artefact, restoring the `task_uses_prompts ↔ prompt_relates_to_task` audit-graph edge severed in PR #70 (review finding C.3).

## Target Audience

The dispatched executor for [Task 032 `agents-spec-integration`](../../tasks/032-agents-spec-integration/task.md), specifically subtask ST-5 (05-spec-amendment-agents-md.md). Default executor: **main-agent**.

## Intended Model / Agent

Claude Code (or any agent that satisfies the executor declaration in the parent subtask file).

## Use-Case Context

This prompt drives subtask ST-5 of [Task agents-spec-integration](../../tasks/032-agents-spec-integration/task.md). The parent task's chain-level rationale lives in its `task.md`; this brief records only the subtask's local goal + inputs + acceptance + dependencies + effort, lifted verbatim from the subtask file at extraction time.

**Parallelism:** Phase B (sequential) — depends on ST-1 (research SPEC) + ST-2/ST-3/ST-4 (linter implementations). MUST wait for all four to land.

## Goal (from subtask)

Apply the concrete AGENTS.md edits that close out Task 032 — outside the `<!-- BEGIN/END AGENCY-ADR SYNTHESIS -->` markers — referencing the ST-1 research SPEC, the ST-2/3/4 linters, and the four under-cited research outputs (adr-assumption-audit ASM-001/004/005/009, skills-skill-container-capabilities U1-U2, gemini agency-adr-governance-spec, ncp-novel-co-authoring-spec).

## Falsification (from subtask)

Wrong cut **iff** the edits would land *inside* the AGENCY-ADR SYNTHESIS guarded section. Mitigation: every edit's target line range MUST be verified against `AGENTS.md:339-342` before staging.

## Inputs (from subtask)

- `research/adr-corpus-extraction-from-governance-specs/output/SPEC.md` (ST-1 output, REQUIRED).
- `research/adr-assumption-audit/output/REPORT.md` §1.
- `research/skills-skill-container-capabilities/output/SPEC.md`.
- `research/gemini/agency-adr-governance-spec/`.
- ST-2 / ST-3 / ST-4 linter implementations.

## Acceptance Criteria (from subtask)

1. AGENTS.md gains a `§0 Theoretical Foundations` cross-reference to `research/gemini/agency-adr-governance-spec/`.
2. AGENTS.md §3.3 carries the polarity-inversion footnote citing REPORT.md §1 ASM-001.
3. AGENTS.md §6 cites U1/U2 operational constraints (no git, no filesystem persistence).
4. AGENTS.md §6 cites the citation-reproducibility protocol from ncp-novel-co-authoring-spec.
5. The Gherkin sample anchored `AG.NO5.1` (from task.md "Sample Gherkin") lands as one of ≥4 new scenarios at AGENTS.md §6 acceptance section.
6. `tools/adr/cli.py validate AGENTS.md` exits 0 (markers intact; no ADR.A.3.5).
7. `tools/check-governance.sh` exits 0.

## Dependencies (from subtask)

ST-1 (research) MUST land first (writes the SPEC the §0 reference points at). ST-2 / ST-3 / ST-4 SHOULD land before this so they can be cited; if not, this subtask cites them as forward-references and bumps `task_status` to `blocked` until they land.

## Estimated Effort (from subtask)

Small (~1 hour focused editing; mostly mechanical insertion of cross-references).
