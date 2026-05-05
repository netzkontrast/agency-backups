---
type: prompt
status: active
slug: adr-spec-research-synthesis
summary: "Run-start snapshot of the executing prompt. Immutable per RESEARCH.md §5.1. Source of truth lives at /prompts/adr-spec-research-synthesis/prompt.md."
created: 2026-05-05
updated: 2026-05-05
prompt_kind: research-proposal
prompt_framework: RISEN+ReAct
prompt_target_agent: "Claude Code"
prompt_relates_to_task: adr-spec-research-synthesis
---

# ADR Spec Research Synthesis — Research-Proposal Prompt (Snapshot)

This is the verbatim run-start snapshot of [`/prompts/adr-spec-research-synthesis/prompt.md`](../../prompts/adr-spec-research-synthesis/prompt.md). The body below MUST match the source at run-start; if they diverge after the run, the source is authoritative for new runs and this snapshot is the historical record of what THIS run executed.

## R — Role

You are the **Repository Governance Architect** for `netzkontrast/agency`. Your mission is to produce a single, authoritative ADR governance specification that is simultaneously:
- Theoretically sound (grounded in the Gemini draft's MDL, DAG, and Gherkin framework)
- Structurally compatible (honoring the repo's existing Frontmatter Ontology, tooling surface, and branching conventions)
- Immediately deployable (every normative statement has a mechanical enforcement path in this specific repo)

You are not permitted to copy the Gemini draft verbatim. Every §0–§9 section must be re-derived against the actual repo content you find during execution.

## I — Input

1. **Repo root specs:** `AGENTS.md`, `TASK.md`, `PROMPT.md`, `RESEARCH.md`, `FOLDERS.md`, `PRE_COMMIT.md`, `MAINTENANCE.md`, `FRUSTRATED.md`, `README.md`
2. **Tooling:** `tools/check-governance.sh`, `tools/fm/validate.py`, `tools/fm/extract.py`, `tools/fm/edit.py`, `tools/fm/query.py`
3. **Existing schemas:** `maintenance/schemas/header-ontology.json`
4. **Gemini ADR draft:** `research/gemini/agency-adr-governance-spec/adr-governance-spec.md` (theoretical reference only)
5. **Gemini research prompt:** `research/gemini/agency-adr-governance-spec/research-prompt_agency-adr-governance-spec.md`

## S — Steps

Step 0 — Initialise the research workspace per `RESEARCH.md §2`.
Step 1 — `/sc:analyze` root specs and tooling; record findings in `workspace/analysis.md`.
Step 2 — `/sc:brainstorm` the five integration points; record in `workspace/brainstorm.md` with `[RESOLVED] / [OPEN] / [DEFERRED]` labels.
Step 3 — Apply [M13] Adversarial Query Expansion across four axes; record in `reflection/M13-query-expansion.md`. Apply [M08] for high-stakes claims.
Step 4 — Draft `output/SPEC.md` per the §0–§9 schema, re-derived from the prior steps. Do not copy from the Gemini draft.
Step 5 — Run all five CB0 reflection checkpoints; produce `friction-log.md`; run `tools/check-governance.sh`.
Step 6 — Mark Task 027 `done`; verify Tasks 028 and 029 remain `open`.

## E — Expectations

- `output/SPEC.md` exists with §0–§9 populated.
- Every MUST has a Gherkin scenario with an `# anchor:` comment.
- Every `[OPEN]` item from Step 2 appears in §8.
- `tools/check-governance.sh` exits 0.
- Friction log declares FL[0–3].

## N — Narrowing

- Output schema locked to §0–§9. No additional top-level sections.
- Source priority: repo files first; Gemini draft is reference only.
- Temporal scope: 2011-01-01 through 2026-05-05.
- BCP-14 keyword density: exactly one per normative sentence.
- ADR JSON-Schema MUST set `additionalProperties: true` to allow future L2 extension.
