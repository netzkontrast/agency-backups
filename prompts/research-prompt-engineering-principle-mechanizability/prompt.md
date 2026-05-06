---
type: prompt
status: active
slug: research-prompt-engineering-principle-mechanizability
summary: "Produce `research/prompt-engineering-principle-mechanizability/output/SPEC.md` containing a per-principle assessment for PROMPT.md §5.1 (self-containedness), §5.2 (framework declaration), §5.3 (RFC 2119), §5.4 (deliverable lock), §5.5 (a..."
created: 2026-05-06
updated: 2026-05-06
prompt_kind: task-spec
prompt_framework: RISEN+ReAct
prompt_target_agent: "Claude Code"
prompt_relates_to_task: prompt-spec-integration
prompt_spawned_from_research: ""
---

# ST-1: Research — Prompt-Engineering Principle Mechanizability — Task-Spec Prompt

## Framework

RISEN+ReAct. The prompt declares the framework in frontmatter (`prompt_framework: RISEN+ReAct`) and restates it here for `fm-validate` header conformance. The R/I/S/E sections below carry the canonical roles; a final **Constraints** section groups normative scope/failure rules per repo convention.

## R — Role

You are the **main-agent** dispatched to execute subtask ST-1 of [Task prompt-spec-integration](../../tasks/034-prompt-spec-integration/task.md). Your remit is bounded by the Acceptance Criteria in [`brief.md`](./brief.md); you MUST NOT expand scope beyond those criteria without surfacing the divergence in `friction-log.md`.

**Parallelism:** Phase A (parallel) — runs concurrently with ST-2, ST-3. No inter-dependencies..

## I — Input

- [`PROMPT.md`](../../../PROMPT.md) §5 (the seven principles).
- All `/prompts/<slug>/prompt.md` files (~33 active).
- [`skills/research-prompt-optimizer/SKILL.md`](../../../skills/research-prompt-optimizer/SKILL.md) (Phase 4 reader-test prior art).
- [`research/agent-prompt-specs-3-systems-sdd/output/SPEC.md`](../../../research/agent-prompt-specs-3-systems-sdd/output/SPEC.md) §A.2 (RFC-2119 + Gherkin contract).
- `tasks/034-prompt-spec-integration/task.md` — parent task chain-level context.

## S — Steps

1. Execute the following instruction block faithfully — it is the verbatim Execution Brief from the parent subtask file:

```text
Run research-prompt-optimizer Phase 1–3 against the intent. Repo root:


Skip Phase 1 askuser. Render to /research/prompt-engineering-principle-mechanizability/research-prompt.md.
Execute and produce /research/prompt-engineering-principle-mechanizability/output/SPEC.md.
Scan all /prompts/<slug>/prompt.md files; report exact corpus size.
Author reflection/friction-log.md.
Run tools/check-governance.sh.
Commit "research(prompt-principle-mechanizability): per-principle FPR assessment (Task 034 ST-1)".
Do NOT push.
```
2. Verify every Acceptance Criterion in [`brief.md`](./brief.md) is satisfied by the produced artefacts.
3. Run `tools/check-governance.sh` and resolve every ERROR before committing.

## E — Expectations

- SPEC.md at `/research/prompt-engineering-principle-mechanizability/output/SPEC.md`.
- §1 table: 7 rows × 5 columns (principle, mechanical recipe, FPR, ERROR/WARN/human, sample-size).
- §2 documents the FPR-measurement methodology reproducibly.
- §3 specifies tooling for each enforceable principle (the spec for ST-2 + ST-3 to consume).
- §4 names the principles that stay human-review.
- `research_phase: complete`; reflection friction-log.
- `tools/check-governance.sh` exits 0 on the produced commit.
- Commit message follows the parent task's convention; the commit cites `Task 034 ST-1` in its trailer.

## Constraints

- Dependency: None. Phase A.
- MUST NOT trigger the subtask's Falsification clause: Wrong cut **iff** none of P.5.1–P.5.7 (other than P.5.3 which is already linted) admits a mechanical check below 20% false-positive rate. Mitigation: P.5.1 (self-containedness) is testable via "render the prompt to a fresh-context agent and ask for fidelity" — research-prompt-optimizer Phase 4 prior art proves the pattern.
- MUST NOT inline this prompt's Goal/Inputs/Acceptance back into the subtask file — the subtask body is now a thin pointer per Task 041.
- MUST run `tools/check-governance.sh` before pushing; a non-zero exit MUST block the push.
- SHOULD cite the parent task's `task_id` in any commit-message trailer for traceability.
