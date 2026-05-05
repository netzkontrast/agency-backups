---
type: note
status: active
slug: adr-assumption-audit-methodology
summary: "Methods applied: M13 (adversarial query expansion, Subagent A), M07 (contradiction log, Subagent B), M06 (source triangulation) + M08 (pre-commitment) (Subagent C). Plus the prompt's CB0 reflection regime."
created: 2026-05-05
updated: 2026-05-05
---

# Methodology

The four methods (M06, M07, M08, M13) are inherited from the originating Gemini research prompt at [`research/gemini/agency-adr-governance-spec/research-prompt_agency-adr-governance-spec.md`](../../gemini/agency-adr-governance-spec/research-prompt_agency-adr-governance-spec.md). Each is applied here against the *audit target* (Task 027 SPEC + Task 028 plan) rather than against external literature.

## [M13] Adversarial Query Expansion (Subagent A)

Run across all four axes (adjacent / opposing / abstraction / orthogonal) per the prompt's pre-specification of the orthogonal axis as the MDL lens. Output: `workspace/m13-hidden-assumptions.md`.

**Method delta from the Task 027 application:** the Task 027 M13 *hardened* the spec; this audit M13 *attacks* it. Different mode of the same method.

## [M07] Contradiction Log (Subagent B)

Applied as a *scan*: walk every root spec and tool file, identify normative architectural choices that are enacted-but-not-stated, log each as an IADR candidate. Where two IADRs contradict each other, log a sub-entry with the resolution requirement. Output: `workspace/m07-implicit-adrs.md`.

**Method delta:** the Task 027 M07 catalogued contradictions *between Gemini and the repo*; this audit M07 catalogues contradictions *within the repo's own implicit governance*.

## [M06] Source Triangulation (Subagent C)

For every pending decision, require ≥ 3 of 4 sources to agree before marking `resolved`. Sources: SPEC §8, plan §6, M13 output, M07 output. The 4-source matrix lives in `workspace/m06-m08-pending-decisions.md` "Triangulation Audit Trail".

## [M08] What Would Change My Mind / Pre-Commitment (Subagent C)

For every PD Option, record the concrete observable evidence that would confirm it. This is the *pre-commitment* discipline: the auditor commits in advance to what evidence would resolve the question, preventing post-hoc rationalisation.

## CB0 — Reflection Regime

Three explicit reflection files capture the five mandatory checkpoints:

| Checkpoint | File | Status |
|---|---|---|
| Kickoff | [`../reflection/kickoff.md`](../reflection/kickoff.md) | Five Q1–Q5 answers + pre-commitments. |
| Mid-run | [`../reflection/mid-run.md`](../reflection/mid-run.md) | Captured between Subagent B and Subagent C. |
| Post-M13 | implicit in `workspace/m13-hidden-assumptions.md` "Worst-Case Compression-Ratio Scenario" | Documented inline. |
| Pre-synthesis | implicit in `workspace/m06-m08-pending-decisions.md` "Triangulation Audit Trail" | The matrix is the pre-synthesis check that `[resolved]` PDs really do have ≥ 3 source agreement. |
| Post-synthesis | [`../reflection/post-synthesis.md`](../reflection/post-synthesis.md) | Confidence assessment + identification of unaddressed findings. |

## Quality Gate

Every finding (ASM, IADR, PD) carries a `Where embedded:` or `Evidence:` field with a `file:line` or `file §section` anchor. Findings without an anchor were rejected at workspace draft time.

## Friction Declaration

Highest FL: **FL1**. Two recurring frictions documented in [`../reflection/friction-log.md`](../reflection/friction-log.md). One is a known recurrence (subagent semantics ambiguity, also seen in Task 027); one is novel (cross-task amendment to a closed Task's plan).
