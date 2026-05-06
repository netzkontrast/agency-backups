---
type: prompt
status: active
slug: spec-amendment-agents-md
summary: "Apply the concrete AGENTS.md edits that close out Task 032 — outside the `<!-- BEGIN/END AGENCY-ADR SYNTHESIS -->` markers — referencing the ST-1 research SPEC, the ST-2/3/4 linters, and the four under-cited research outputs (adr-assumpt..."
created: 2026-05-06
updated: 2026-05-06
prompt_kind: task-spec
prompt_framework: RISEN+ReAct
prompt_target_agent: "Claude Code"
prompt_relates_to_task: agents-spec-integration
---

# ST-5: Spec Amendment — AGENTS.md — Task-Spec Prompt

## Framework

RISEN+ReAct. The prompt declares the framework in frontmatter (`prompt_framework: RISEN+ReAct`) and restates it here for `fm-validate` header conformance. The R/I/S/E sections below carry the canonical roles; a final **Constraints** section groups normative scope/failure rules per repo convention.

## R — Role

You are the **main-agent** dispatched to execute subtask ST-5 of [Task agents-spec-integration](../../tasks/032-agents-spec-integration/task.md). Your remit is bounded by the Acceptance Criteria in [`brief.md`](./brief.md); you MUST NOT expand scope beyond those criteria without surfacing the divergence in `friction-log.md`.

**Parallelism:** Phase B (sequential) — depends on ST-1 (research SPEC) + ST-2/ST-3/ST-4 (linter implementations). MUST wait for all four to land..

## I — Input

- `research/adr-corpus-extraction-from-governance-specs/output/SPEC.md` (ST-1 output, REQUIRED).
- `research/adr-assumption-audit/output/REPORT.md` §1.
- `research/skills-skill-container-capabilities/output/SPEC.md`.
- `research/gemini/agency-adr-governance-spec/`.
- ST-2 / ST-3 / ST-4 linter implementations.
- `tasks/032-agents-spec-integration/task.md` — parent task chain-level context.

## S — Steps

1. The agent MUST produce the artefact required by acceptance criterion: AGENTS.md gains a `§0 Theoretical Foundations` cross-reference to `research/gemini/agency-adr-governance-spec/`.
2. The agent MUST produce the artefact required by acceptance criterion: AGENTS.md §3.3 carries the polarity-inversion footnote citing REPORT.md §1 ASM-001.
3. The agent MUST produce the artefact required by acceptance criterion: AGENTS.md §6 cites U1/U2 operational constraints (no git, no filesystem persistence).
4. The agent MUST produce the artefact required by acceptance criterion: AGENTS.md §6 cites the citation-reproducibility protocol from ncp-novel-co-authoring-spec.
5. The agent MUST produce the artefact required by acceptance criterion: The Gherkin sample anchored `AG.NO5.1` (from task.md "Sample Gherkin") lands as one of ≥4 new scenarios at AGENTS.md §6 acceptance section.
6. The agent MUST produce the artefact required by acceptance criterion: `tools/adr/cli.py validate AGENTS.md` exits 0 (markers intact; no ADR.A.3.5).
7. The agent MUST produce the artefact required by acceptance criterion: `tools/check-governance.sh` exits 0.
8. The agent MUST verify every Acceptance Criterion enumerated in [`brief.md`](./brief.md) holds against the produced artefacts; on any failure the agent MUST iterate the relevant implementation step rather than weakening the criterion.
9. The agent MUST run `tools/check-governance.sh` and resolve every ERROR before committing; a non-zero exit MUST block the commit.
10. The agent SHOULD author or update `tasks/032-agents-spec-integration/friction-log.md` per FRUSTRATED.md FL[0-3] when frictions arise; absence of frictions MAY be recorded as `FL: 0`.
11. The agent MUST commit with a message that names `Task 032 ST-5` in its trailer; the agent MUST NOT push (the maintainer pushes after review).

## E — Expectations

- AGENTS.md gains a `§0 Theoretical Foundations` cross-reference to `research/gemini/agency-adr-governance-spec/`.
- AGENTS.md §3.3 carries the polarity-inversion footnote citing REPORT.md §1 ASM-001.
- AGENTS.md §6 cites U1/U2 operational constraints (no git, no filesystem persistence).
- AGENTS.md §6 cites the citation-reproducibility protocol from ncp-novel-co-authoring-spec.
- The Gherkin sample anchored `AG.NO5.1` (from task.md "Sample Gherkin") lands as one of ≥4 new scenarios at AGENTS.md §6 acceptance section.
- `tools/adr/cli.py validate AGENTS.md` exits 0 (markers intact; no ADR.A.3.5).
- `tools/check-governance.sh` exits 0.
- `tools/check-governance.sh` exits 0 on the produced commit.
- Commit message follows the parent task's convention; the commit cites `Task 032 ST-5` in its trailer.

## Constraints

- Dependency: ST-1 (research) MUST land first (writes the SPEC the §0 reference points at). ST-2 / ST-3 / ST-4 SHOULD land before this so they can be cited; if not, this subtask cites them as forward-references and bumps `task_status` to `blocked` until they land.
- MUST NOT trigger the subtask's Falsification clause: Wrong cut **iff** the edits would land *inside* the AGENCY-ADR SYNTHESIS guarded section. Mitigation: every edit's target line range MUST be verified against `AGENTS.md:339-342` before staging.
- MUST NOT inline this prompt's Goal/Inputs/Acceptance back into the subtask file — the subtask body is now a thin pointer per Task 041.
- MUST run `tools/check-governance.sh` before pushing; a non-zero exit MUST block the push.
- SHOULD cite the parent task's `task_id` in any commit-message trailer for traceability.
