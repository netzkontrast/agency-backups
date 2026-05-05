---
type: note
status: active
slug: adr-assumption-audit-post-synthesis-log
summary: "Per-section merge log into output/REPORT.md."
created: 2026-05-05
updated: 2026-05-05
---

# Post-Synthesis Log

| Section of REPORT.md | Source artefact | Open loops surfaced |
|---|---|---|
| §0 Scope and Provenance | this synthesis run | none |
| §1 Hidden Assumptions | `workspace/m13-hidden-assumptions.md` | ASM-007 (cultural) flagged with no direct mitigation. |
| §2 Implicit ADRs in Force | `workspace/m07-implicit-adrs.md` | Two inter-IADR contradictions surfaced as separate sub-rows. |
| §3 Pending Decisions | `workspace/m06-m08-pending-decisions.md` | PD-002, PD-006, PD-007 open. |
| §4 Recommended Actions | synthetic (this run only) | None new; every Action maps to a numbered finding. |

## Merge Order

1. §0 written first (anchors every later section to its workspace source).
2. §1, §2, §3 written in subagent order (A, B, C) for consistency with the prompt's Steps.
3. §4 written last because it consumes §1–§3.

## Bytes-Equivalence

REPORT.md does NOT copy verbatim from the workspace files. It restructures (sort by blast radius / priority / blocking) and *summarises* (one row per finding instead of full evidence blocks). Full evidence remains in the workspace files. This preserves audit traceability while keeping REPORT.md skim-readable.

## Idempotency

A second run of this synthesis under unchanged subagent outputs would produce a near-identical REPORT.md. The only non-deterministic content is §4's prose framing of the Recommended Actions, which is judgement-driven; the action IDs and mappings are deterministic.
