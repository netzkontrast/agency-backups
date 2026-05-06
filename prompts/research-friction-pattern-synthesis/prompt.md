---
type: prompt
status: active
slug: research-friction-pattern-synthesis
summary: "Produce `research/friction-pattern-synthesis/output/SPEC.md` aggregating every `friction-log.md` in `/tasks/<NNN>-<slug>/` and `/research/<slug>/reflection/` into a structured synthesis: (a) FL distribution histogram, (b) recurring root-..."
created: 2026-05-06
updated: 2026-05-06
prompt_kind: task-spec
prompt_framework: RISEN+ReAct
prompt_target_agent: "Claude Code"
prompt_relates_to_task: task-spec-integration
prompt_spawned_from_research: ""
---

# ST-1: Research — Friction Pattern Synthesis — Task-Spec Prompt

## Framework

RISEN+ReAct. The prompt declares the framework in frontmatter (`prompt_framework: RISEN+ReAct`) and restates it here for `fm-validate` header conformance. The R/I/S/E sections below carry the canonical roles; a final **Constraints** section groups normative scope/failure rules per repo convention.

## R — Role

You are the **main-agent** dispatched to execute subtask ST-1 of [Task task-spec-integration](../../tasks/033-task-spec-integration/task.md). Your remit is bounded by the Acceptance Criteria in [`brief.md`](./brief.md); you MUST NOT expand scope beyond those criteria without surfacing the divergence in `friction-log.md`.

**Parallelism:** Phase A (parallel) — runs concurrently with ST-2, ST-3, ST-4. No inter-dependencies. Sibling research subtask Task 038 ST-1 (FL0 justification) reads same corpus and may run in parallel for token-cost amortization..

## I — Input

- All `tasks/<NNN>-<slug>/friction-log.md` (~20 files; closed tasks only).
- All `research/<slug>/reflection/friction-log.md`.
- [`tasks/030-cleanup-dramatica-skills-corpus/notes.md`](../../030-cleanup-dramatica-skills-corpus/notes.md) §3 (FE-1..FE-10 already classified).
- [`research/adr-assumption-audit/output/REPORT.md`](../../../research/adr-assumption-audit/output/REPORT.md) §1 (high-blast assumptions).
- `tasks/033-task-spec-integration/task.md` — parent task chain-level context.

## S — Steps

1. Execute the following instruction block faithfully — it is the verbatim Execution Brief from the parent subtask file:

```text
Run the research-prompt-optimizer pipeline (Phase 1–3) against the intent
block above.

Phase 1 intent is canonical (above) — skip the askuser loop.
Phase 2: select M07 / M12 / M02 modules; author CBs from constraints.
Phase 3: render to /research/friction-pattern-synthesis/research-prompt.md.
Then EXECUTE: produce /research/friction-pattern-synthesis/output/SPEC.md
meeting the acceptance criteria; author the reflection friction-log.md;
update /research/readme.md.

Run tools/check-governance.sh and fix every ERROR.
Commit "research(friction-pattern-synthesis): cross-task friction taxonomy (Task 033 ST-1)".
Do NOT push.
```
2. Verify every Acceptance Criterion in [`brief.md`](./brief.md) is satisfied by the produced artefacts.
3. Run `tools/check-governance.sh` and resolve every ERROR before committing.

## E — Expectations

- SPEC.md at `/research/friction-pattern-synthesis/output/SPEC.md`.
- §1 histogram counts FL0/FL1/FL2/FL3 across both surfaces (PR descriptions + reflection files); covers ≥15 closed tasks.
- §2 root-cause taxonomy has ≥6 categories with frequency counts.
- §3 per-spec attribution: which root spec each FL2+ entry implicates.
- §4 amendments: ≥3 verbatim spec-text proposals with file:line targets.
- `research_phase: complete`; friction-log.md present.
- `tools/check-governance.sh` exits 0 on the produced commit.
- Commit message follows the parent task's convention; the commit cites `Task 033 ST-1` in its trailer.

## Constraints

- Dependency: None. Phase A.
- MUST NOT trigger the subtask's Falsification clause: Wrong cut **iff** fewer than 15 closed tasks have a non-empty friction-log.md. Mitigation: 16 closed tasks (per Task 029 closure note) already exist; this is a sufficient corpus.
- MUST NOT inline this prompt's Goal/Inputs/Acceptance back into the subtask file — the subtask body is now a thin pointer per Task 041.
- MUST run `tools/check-governance.sh` before pushing; a non-zero exit MUST block the push.
- SHOULD cite the parent task's `task_id` in any commit-message trailer for traceability.
