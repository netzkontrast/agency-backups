---
type: prompt
status: active
slug: research-adr-corpus-extraction
summary: "Produce `research/adr-corpus-extraction-from-governance-specs/output/SPEC.md` containing 15–30 implicit ADRs already in force across `AGENTS.md`, `TASK.md`, `PROMPT.md`, `RESEARCH.md`, `FOLDERS.md`, `PRE_COMMIT.md`, `FRUSTRATED.md`, `MAI..."
created: 2026-05-06
updated: 2026-05-06
prompt_kind: task-spec
prompt_framework: RISEN+ReAct
prompt_target_agent: "Claude Code"
prompt_relates_to_task: agents-spec-integration
prompt_spawned_from_research: ""
---

# ST-1: Research — ADR Corpus Extraction from Governance Specs — Task-Spec Prompt

## Framework

RISEN+ReAct. The prompt declares the framework in frontmatter (`prompt_framework: RISEN+ReAct`) and restates it here for `fm-validate` header conformance. The R/I/S/E sections below carry the canonical roles; a final **Constraints** section groups normative scope/failure rules per repo convention.

## R — Role

You are the **main-agent** dispatched to execute subtask ST-1 of [Task agents-spec-integration](../../tasks/032-agents-spec-integration/task.md). Your remit is bounded by the Acceptance Criteria in [`brief.md`](./brief.md); you MUST NOT expand scope beyond those criteria without surfacing the divergence in `friction-log.md`.

**Parallelism:** Phase A (parallel) — runs concurrently with ST-2, ST-3, ST-4. No inter-dependencies..

## I — Input

- All 8 root specs at the repo root (`AGENTS.md`, `TASK.md`, `PROMPT.md`, `RESEARCH.md`, `FOLDERS.md`, `PRE_COMMIT.md`, `FRUSTRATED.md`, `MAINTENANCE.md`).
- [`research/adr-assumption-audit/output/REPORT.md`](../../../research/adr-assumption-audit/output/REPORT.md) §2 (11 IADRs already enumerated).
- [`research/adr-spec-research-synthesis/output/SPEC.md`](../../../research/adr-spec-research-synthesis/output/SPEC.md) (canonical ADR format).
- [`tasks/028-adr-tooling-impl-plan/implementation-plan.md`](../../028-adr-tooling-impl-plan/implementation-plan.md) §B (PD↔OD cross-reference).
- **NEW (post-Task-031):** `tools/adr/extract.py`, `tools/adr/synthesize.py`, `tools/adr/cli.py validate` — the deployed CLI suite. ST-1 USES these tools rather than reimplementing extraction; the research output is the *curated* MADR corpus, the *tool* does the mechanical scan.
- **NEW:** `decisions/` folder (now operational). The ratified subset is filed here as actual `decisions/<NNNN>-<slug>.md` files with `adr_status: Proposed` so the synthesizer (`tools/adr/cli.py synthesize`) can route them into AGENTS.md's guarded section.
- `tasks/032-agents-spec-integration/task.md` — parent task chain-level context.

## S — Steps

1. Execute the following instruction block faithfully — it is the verbatim Execution Brief from the parent subtask file:

```text
You are running Phase 1–3 of the research-prompt-optimizer pipeline against the
following intent. Use the Phase 1 Intent block above verbatim as the
intent_<slug>.yaml seed.


Tasks:
1. Confirm Phase 1 intent matches the YAML above (no new asks needed; user
   already produced canonical priors). Skip Phase 1 askuser loop.
2. Phase 2: select modules per the catalog hints above (M01, M06, M07, M13);
   author Constraint Blocks CB0–CB4 from the known_constraints field.
3. Phase 3: render the research-prompt to /research/adr-corpus-extraction-from-governance-specs/research-prompt.md.
4. Execute the research yourself (you are also the executor); produce
   /research/adr-corpus-extraction-from-governance-specs/output/SPEC.md per the acceptance criteria above.
5. Author /research/adr-corpus-extraction-from-governance-specs/reflection/friction-log.md with FL declaration.
6. Run `tools/check-governance.sh`; fix every ERROR.
7. Update /research/readme.md to add the new entry per RESEARCH.md §4 Step 5.
8. Do NOT push. Commit with message "research(adr-corpus-extraction): bootstrap ADR-0001..N extraction (Task 032 ST-1)".
```
2. Verify every Acceptance Criterion in [`brief.md`](./brief.md) is satisfied by the produced artefacts.
3. Run `tools/check-governance.sh` and resolve every ERROR before committing.

## E — Expectations

- SPEC.md exists at `/research/adr-corpus-extraction-from-governance-specs/output/SPEC.md` with ≥15 MADR-shaped candidates.
- Each candidate has frontmatter compatible with the `adr_*` L2 namespace ratified by Task 027 and registered as `types.adr` in `maintenance/schemas/header-ontology.json`.
- Each candidate cites file:line for the source clause; no synthesized clauses.
- §N Appendix lists ≥3 candidates that were rejected and why (false-positive control).
- `research_phase: complete`; reflection/friction-log.md present with FL[0-3] declaration.
- Reciprocity: ≥3 of the 11 IADRs from REPORT.md §2 are cross-referenced as predecessors.
- **NEW gate:** the ratified subset (cardinality decided by maintainer review) is filed as `decisions/<NNNN>-<slug>.md` files; `python3 tools/adr/cli.py validate decisions/` exits 0; `python3 tools/adr/cli.py synthesize --dry-run --token-limit 6000` succeeds (no ADR.A.3.3 budget overrun).
- `tools/check-governance.sh` exits 0 on the produced commit.
- Commit message follows the parent task's convention; the commit cites `Task 032 ST-1` in its trailer.

## Constraints

- Dependency: None. Phase A.
- MUST NOT trigger the subtask's Falsification clause: Wrong cut **iff** fewer than 12 distinct extractable decisions exist across the corpus. Mitigation: `research/adr-assumption-audit/output/REPORT.md §2 IADR Inventory` already enumerates 11 implicit ADRs from a narrower scan; expanding to all 8 specs MUST yield ≥15.
- MUST NOT inline this prompt's Goal/Inputs/Acceptance back into the subtask file — the subtask body is now a thin pointer per Task 041.
- MUST run `tools/check-governance.sh` before pushing; a non-zero exit MUST block the push.
- SHOULD cite the parent task's `task_id` in any commit-message trailer for traceability.
