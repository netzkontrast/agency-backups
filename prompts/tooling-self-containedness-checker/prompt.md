---
type: prompt
status: active
slug: tooling-self-containedness-checker
summary: "Ship `tools/check-prompt-self-containedness.py` that scans `/prompts/<slug>/prompt.md` files and detects self-containedness violations: external context references that the executor cannot resolve. Per the FPR taxonomy from Task 034 ST-1..."
created: 2026-05-06
updated: 2026-05-06
prompt_kind: task-spec
prompt_framework: RISEN+ReAct
prompt_target_agent: "Claude Code"
prompt_relates_to_task: prompt-spec-integration
---

# ST-2: `check-prompt-self-containedness` — Mechanizes P.5.1 — Task-Spec Prompt

## Framework

RISEN+ReAct. The prompt declares the framework in frontmatter (`prompt_framework: RISEN+ReAct`) and restates it here for `fm-validate` header conformance. The R/I/S/E sections below carry the canonical roles; a final **Constraints** section groups normative scope/failure rules per repo convention.

## R — Role

You are the **main-agent** dispatched to execute subtask ST-2 of [Task prompt-spec-integration](../../tasks/034-prompt-spec-integration/task.md). Your remit is bounded by the Acceptance Criteria in [`brief.md`](./brief.md); you MUST NOT expand scope beyond those criteria without surfacing the divergence in `friction-log.md`.

**Parallelism:** Phase A (parallel-grouped, soft-blocked) — runs alongside ST-3 but soft-depends on ST-1 SPEC §3 heuristic recipe. Phase A may proceed with stub heuristic + upgrade post-ST-1..

## I — Input

- `research/prompt-engineering-principle-mechanizability/output/SPEC.md` (Task 034 ST-1 output) §3 self-containedness recipe.
- [`PROMPT.md`](../../../PROMPT.md) §5.1.
- [`skills/research-prompt-optimizer/phases/phase4-reader-test.md`](../../../skills/research-prompt-optimizer/phases/phase4-reader-test.md) (prior art).
- All `/prompts/<slug>/prompt.md` (test corpus).
- `tasks/034-prompt-spec-integration/task.md` — parent task chain-level context.

## S — Steps

1. The agent MUST treat the following preamble as authoritative orientation before executing any subsequent step: Implement tools/check-prompt-self-containedness.py per ST-1 SPEC §3. Pre-flight: test -f research/prompt-engineering-principle-mechanizability/output/SPEC.md If absent, abort. When done: python3 -m unittest discover -s tests python3 tools/check-prompt-self-containedness.py prompts/*/prompt.md Commit "feat(tools): prompt self-containedness checker (Task 034 ST-2, mechanizes P.5.1)". Do NOT push.
2. The agent MUST verify every Acceptance Criterion enumerated in [`brief.md`](./brief.md) holds against the produced artefacts; on any failure the agent MUST iterate the relevant implementation step rather than weakening the criterion.
3. The agent MUST run `tools/check-governance.sh` and resolve every ERROR before committing; a non-zero exit MUST block the commit.
4. The agent SHOULD author or update `tasks/034-prompt-spec-integration/friction-log.md` per FRUSTRATED.md FL[0-3] when frictions arise; absence of frictions MAY be recorded as `FL: 0`.
5. The agent MUST commit with a message that names `Task 034 ST-2` in its trailer; the agent MUST NOT push (the maintainer pushes after review).

## E — Expectations

- **Surface.** `python3 tools/check-prompt-self-containedness.py <prompt.md>` exits 0 (pass) or 2 (WARN).
- **Checks.** Implements the regex + structural rules from ST-1 SPEC §3.
- **Tests.** `tests/test_prompt_self_containedness.py` includes synthetic prompts that trigger each ST-1 rule.
- **Integration.** `tools/check-governance.sh` runs WARN-tier on changed `/prompts/<slug>/prompt.md`.
- `tools/check-governance.sh` exits 0 on the produced commit.
- Commit message follows the parent task's convention; the commit cites `Task 034 ST-2` in its trailer.

## Constraints

- Dependency: ST-1 (research) MUST land first.
- MUST NOT trigger the subtask's Falsification clause: Wrong cut **iff** false-positive rate exceeds the threshold set by ST-1's empirical study. Mitigation: ST-1 SPEC §3 specifies the exact heuristics; ST-2 implements them faithfully.
- MUST NOT inline this prompt's Goal/Inputs/Acceptance back into the subtask file — the subtask body is now a thin pointer per Task 041.
- MUST run `tools/check-governance.sh` before pushing; a non-zero exit MUST block the push.
- SHOULD cite the parent task's `task_id` in any commit-message trailer for traceability.
