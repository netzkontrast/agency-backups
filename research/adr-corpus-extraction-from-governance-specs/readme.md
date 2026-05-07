---
type: index
status: active
slug: adr-corpus-extraction-from-governance-specs
summary: "Research workspace: extract implicit ADRs already in force across the 8 root governance specs. Produces SPEC.md catalogue (18 IADRs) and ratifies the P1 subset (5 records) into /decisions/ as Proposed ADRs."
created: 2026-05-07
updated: 2026-05-07
research_phase: complete
research_executes_prompt: research-adr-corpus-extraction
research_friction_level: FL1
---

# Research — ADR Corpus Extraction From Governance Specs

This workspace catalogues the implicit ADRs (IADRs) already binding on every agent in this repository, extracted from the eight root specs. It builds on the IADR inventory at [`../adr-assumption-audit/output/REPORT.md`](../adr-assumption-audit/output/REPORT.md) §2 and conforms to the MADR shape ratified in [`../adr-spec-research-synthesis/output/SPEC.md`](../adr-spec-research-synthesis/output/SPEC.md).

## Layout

- [`output/`](./output/) — `SPEC.md` (the IADR catalogue) plus its `readme.md`.
- [`reflection/`](./reflection/) — Friction log per [`FRUSTRATED.md`](../../FRUSTRATED.md).

## State

`research_phase: complete`. Findings:

- **18 IADRs catalogued** in `output/SPEC.md` §2.
- **5 P1 IADRs ratified** as `decisions/0001-…md` through `decisions/0005-…md` with `adr_status: Proposed`.
- **3 audit-catalogue IADRs explicitly cited** as predecessors (IADR-001/002/003 from `../adr-assumption-audit/output/REPORT.md`).
- **4 candidates rejected** in `output/SPEC.md` §6 (false-positive control).

## Outputs

- [`output/SPEC.md`](./output/SPEC.md) — authoritative IADR catalogue (`type: research`, `research_phase: complete`).
- [`/decisions/0001-mandatory-session-bootstrap.md`](../../decisions/0001-mandatory-session-bootstrap.md) — P1 ratified.
- [`/decisions/0002-operational-folder-topology.md`](../../decisions/0002-operational-folder-topology.md) — P1 ratified.
- [`/decisions/0003-frontmatter-source-of-truth.md`](../../decisions/0003-frontmatter-source-of-truth.md) — P1 ratified.
- [`/decisions/0004-yaml-depth-one-constraint.md`](../../decisions/0004-yaml-depth-one-constraint.md) — P1 ratified.
- [`/decisions/0005-repair-authority-tiers.md`](../../decisions/0005-repair-authority-tiers.md) — P1 ratified.

## Workflow Assumptions

- This run does **not** modify the eight root specs; only reads them and extracts cited clauses.
- Ratified ADRs land with `adr_status: Proposed` so they do not yet contribute to the synthesised AGENTS.md guarded section (per ratified SPEC §8 OQ.5 default).
- The condensed MADR mirror in `output/SPEC.md` §3 MUST round-trip to the full prose in the ratified files; any future edit MUST update both surfaces in the same commit (T2 additive per [`MAINTENANCE.md`](../../MAINTENANCE.md) §1).
