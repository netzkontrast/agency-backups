---
type: note
status: draft
slug: task-032-st1-research-adr-corpus-extraction
summary: "Subtask ST-1 (research head): extract implicit ADR-style architectural decisions already embedded in the 8 root specs and propose them as the bootstrap ADR-0001..N corpus, mitigating ASM-007 (cultural assumption that humans author ADRs proactively)."
created: 2026-05-06
updated: 2026-05-06
---

# ST-1: Research — ADR Corpus Extraction from Governance Specs

**Executor:** main-agent

## Goal

Produce `research/adr-corpus-extraction-from-governance-specs/output/SPEC.md` containing 15–30 implicit ADRs already in force across `AGENTS.md`, `TASK.md`, `PROMPT.md`, `RESEARCH.md`, `FOLDERS.md`, `PRE_COMMIT.md`, `FRUSTRATED.md`, `MAINTENANCE.md`, formatted in the MADR shape mandated by `research/adr-spec-research-synthesis/output/SPEC.md`. Each implicit ADR includes (a) extracted decision, (b) source clause + line number, (c) supersession history if any, (d) rationale, (e) consequences, (f) recommended ADR ID.

## Falsification

Wrong cut **iff** fewer than 12 distinct extractable decisions exist across the corpus. Mitigation: `research/adr-assumption-audit/output/REPORT.md §2 IADR Inventory` already enumerates 11 implicit ADRs from a narrower scan; expanding to all 8 specs MUST yield ≥15.

## Phase 1 Intent (research-prompt-optimizer Schema 1)

```yaml
research_question: >-
  Which architectural decisions are *already in force* in this repo via root
  governance specs, and how should they be reified as ADR-0001..N records that
  pass `agency-adr` (the spec from Task 027) validation?
research_question_unpacked: >-
  This is NOT "what ADRs should we write next" (that is policy). It is
  "what ADRs already exist as latent decisions and need formalization to
  prevent silent drift" — an extractive, evidence-bearing audit.
audience: maintainer (Claude Code or human, with read access to repo) preparing the bootstrap ADR migration
output_format: structured Markdown SPEC.md (one MADR block per ADR, plus a §0 method statement and §N appendix listing the false-positives that were considered and rejected)
temporal_scope: {from: "2026-05-04", to: "2026-05-06"}  # current root-spec corpus snapshot
language: en
depth: standard
success_criterion: >-
  ≥15 implicit ADRs extracted, each anchored to a verbatim quote from a
  root spec with file:line citation; each tagged with supersession-status
  (active / superseded-by / supersedes); zero ADRs duplicate the 11 IADRs
  in research/adr-assumption-audit/output/REPORT.md §2 without citing them
  as predecessors.
process_gates:
  - "research_phase: complete on the produced workspace"
  - "reflection/friction-log.md present with FL[0-3] declaration"
  - "/research/readme.md updated to list the new entry per RESEARCH.md §4 Step 5"
  - "tools/check-governance.sh exits 0 against the produced workspace"
known_priors: >-
  research/adr-assumption-audit/output/REPORT.md §2 already lists 11 IADRs
  (5 P1, 4 P2, 2 P3). research/adr-spec-research-synthesis/output/SPEC.md
  defines the canonical ADR format. Tasks 027-029 are done.
known_constraints: >-
  Read-only against root specs — do NOT propose new policy. Cite
  RESEARCH.md §6 for any external-research-derived ADR. No ADRs about
  Tasks/Prompts/Research artefacts (those are governance, not architecture).
domain_context: >-
  This repo decouples Machine/Actor/Space concerns and uses RFC-2119 +
  Gherkin governance. ADRs are managed under tools/adr/ per Task 028's
  implementation plan.
category_signal: A  # adversarial extraction with explicit falsifiability
```

## Phase 2 Plan Hints (catalog modules)

- **Methods:** M01 (Falsification-First), M06 (Source Triangulation across all 8 specs), M07 (Contradiction Log on overlapping rules), M13 (Adversarial Query Expansion across abstraction/orthogonal axes)
- **Frameworks:** ADR-pattern (MADR), repo-native ADR spec from Task 027
- **Seed queries:** "MUST" / "MUST NOT" clauses in root specs; tooling-architecture decisions in tools/; workflow-architecture decisions in lifecycle sections
- **Orthogonal lens:** What architectural decisions are *missing* from the specs but enforced by tooling alone (tooling-only ADRs)?

## Inputs

- All 8 root specs at `/home/user/agency/{AGENTS,TASK,PROMPT,RESEARCH,FOLDERS,PRE_COMMIT,FRUSTRATED,MAINTENANCE}.md`.
- [`research/adr-assumption-audit/output/REPORT.md`](../../../research/adr-assumption-audit/output/REPORT.md) §2 (11 IADRs already enumerated).
- [`research/adr-spec-research-synthesis/output/SPEC.md`](../../../research/adr-spec-research-synthesis/output/SPEC.md) (canonical ADR format).
- [`tasks/028-adr-tooling-impl-plan/implementation-plan.md`](../../028-adr-tooling-impl-plan/implementation-plan.md) §B (PD↔OD cross-reference).
- **NEW (post-Task-031):** `tools/adr/extract.py`, `tools/adr/synthesize.py`, `tools/adr/cli.py validate` — the deployed CLI suite. ST-1 USES these tools rather than reimplementing extraction; the research output is the *curated* MADR corpus, the *tool* does the mechanical scan.
- **NEW:** `decisions/` folder (now operational). The ratified subset is filed here as actual `decisions/<NNNN>-<slug>.md` files with `adr_status: Proposed` so the synthesizer (`tools/adr/cli.py synthesize`) can route them into AGENTS.md's guarded section.

## Acceptance Criteria

1. SPEC.md exists at `/research/adr-corpus-extraction-from-governance-specs/output/SPEC.md` with ≥15 MADR-shaped candidates.
2. Each candidate has frontmatter compatible with the `adr_*` L2 namespace ratified by Task 027 and registered as `types.adr` in `maintenance/schemas/header-ontology.json`.
3. Each candidate cites file:line for the source clause; no synthesized clauses.
4. §N Appendix lists ≥3 candidates that were rejected and why (false-positive control).
5. `research_phase: complete`; reflection/friction-log.md present with FL[0-3] declaration.
6. Reciprocity: ≥3 of the 11 IADRs from REPORT.md §2 are cross-referenced as predecessors.
7. **NEW gate:** the ratified subset (cardinality decided by maintainer review) is filed as `decisions/<NNNN>-<slug>.md` files; `python3 tools/adr/cli.py validate decisions/` exits 0; `python3 tools/adr/cli.py synthesize --dry-run --token-limit 6000` succeeds (no ADR.A.3.3 budget overrun).

## Dependencies

None. Phase A.

## Estimated Effort

Medium (~3 hours focused research; 8-spec scan).

## Execution Brief (for the main agent — do NOT dispatch via /sc:agent)

```text
You are running Phase 1–3 of the research-prompt-optimizer pipeline against the
following intent. Use the Phase 1 Intent block above verbatim as the
intent_<slug>.yaml seed.

Repo root: /home/user/agency
Branch: claude/integrate-repo-specs-cIWtI

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
