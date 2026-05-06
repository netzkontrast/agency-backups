---
type: brief
status: active
slug: research-adr-corpus-extraction-brief
summary: "Brief for prompt research-adr-corpus-extraction — extracted from tasks/032-agents-spec-integration/subtasks/01-research-adr-corpus-extraction.md per Task 041 (PR #70 review C.3 audit-graph repair)."
created: 2026-05-06
updated: 2026-05-06
---

# Brief — ST-1: Research — ADR Corpus Extraction from Governance Specs

## Raw User Request

> Extract the inlined Execution Brief from `tasks/032-agents-spec-integration/subtasks/01-research-adr-corpus-extraction.md` (ST-1) into a registered `/prompts/<slug>/` artefact, restoring the `task_uses_prompts ↔ prompt_relates_to_task` audit-graph edge severed in PR #70 (review finding C.3).

## Target Audience

The dispatched executor for [Task 032 `agents-spec-integration`](../../tasks/032-agents-spec-integration/task.md), specifically subtask ST-1 (01-research-adr-corpus-extraction.md). Default executor: **main-agent**.

## Intended Model / Agent

Claude Code (or any agent that satisfies the executor declaration in the parent subtask file).

## Use-Case Context

This prompt drives subtask ST-1 of [Task agents-spec-integration](../../tasks/032-agents-spec-integration/task.md). The parent task's chain-level rationale lives in its `task.md`; this brief records only the subtask's local goal + inputs + acceptance + dependencies + effort, lifted verbatim from the subtask file at extraction time.

**Parallelism:** Phase A (parallel) — runs concurrently with ST-2, ST-3, ST-4. No inter-dependencies.

## Goal (from subtask)

Produce `research/adr-corpus-extraction-from-governance-specs/output/SPEC.md` containing 15–30 implicit ADRs already in force across `AGENTS.md`, `TASK.md`, `PROMPT.md`, `RESEARCH.md`, `FOLDERS.md`, `PRE_COMMIT.md`, `FRUSTRATED.md`, `MAINTENANCE.md`, formatted in the MADR shape mandated by `research/adr-spec-research-synthesis/output/SPEC.md`. Each implicit ADR includes (a) extracted decision, (b) source clause + line number, (c) supersession history if any, (d) rationale, (e) consequences, (f) recommended ADR ID.

## Falsification (from subtask)

Wrong cut **iff** fewer than 12 distinct extractable decisions exist across the corpus. Mitigation: `research/adr-assumption-audit/output/REPORT.md §2 IADR Inventory` already enumerates 11 implicit ADRs from a narrower scan; expanding to all 8 specs MUST yield ≥15.

## Inputs (from subtask)

- All 8 root specs at the repo root (`AGENTS.md`, `TASK.md`, `PROMPT.md`, `RESEARCH.md`, `FOLDERS.md`, `PRE_COMMIT.md`, `FRUSTRATED.md`, `MAINTENANCE.md`).
- [`research/adr-assumption-audit/output/REPORT.md`](../../../research/adr-assumption-audit/output/REPORT.md) §2 (11 IADRs already enumerated).
- [`research/adr-spec-research-synthesis/output/SPEC.md`](../../../research/adr-spec-research-synthesis/output/SPEC.md) (canonical ADR format).
- [`tasks/028-adr-tooling-impl-plan/implementation-plan.md`](../../028-adr-tooling-impl-plan/implementation-plan.md) §B (PD↔OD cross-reference).
- **NEW (post-Task-031):** `tools/adr/extract.py`, `tools/adr/synthesize.py`, `tools/adr/cli.py validate` — the deployed CLI suite. ST-1 USES these tools rather than reimplementing extraction; the research output is the *curated* MADR corpus, the *tool* does the mechanical scan.
- **NEW:** `decisions/` folder (now operational). The ratified subset is filed here as actual `decisions/<NNNN>-<slug>.md` files with `adr_status: Proposed` so the synthesizer (`tools/adr/cli.py synthesize`) can route them into AGENTS.md's guarded section.

## Acceptance Criteria (from subtask)

1. SPEC.md exists at `/research/adr-corpus-extraction-from-governance-specs/output/SPEC.md` with ≥15 MADR-shaped candidates.
2. Each candidate has frontmatter compatible with the `adr_*` L2 namespace ratified by Task 027 and registered as `types.adr` in `maintenance/schemas/header-ontology.json`.
3. Each candidate cites file:line for the source clause; no synthesized clauses.
4. §N Appendix lists ≥3 candidates that were rejected and why (false-positive control).
5. `research_phase: complete`; reflection/friction-log.md present with FL[0-3] declaration.
6. Reciprocity: ≥3 of the 11 IADRs from REPORT.md §2 are cross-referenced as predecessors.
7. **NEW gate:** the ratified subset (cardinality decided by maintainer review) is filed as `decisions/<NNNN>-<slug>.md` files; `python3 tools/adr/cli.py validate decisions/` exits 0; `python3 tools/adr/cli.py synthesize --dry-run --token-limit 6000` succeeds (no ADR.A.3.3 budget overrun).

## Dependencies (from subtask)

None. Phase A.

## Estimated Effort (from subtask)

Medium (~3 hours focused research; 8-spec scan).
