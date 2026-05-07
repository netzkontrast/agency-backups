---
type: note
status: active
slug: research-cross-spec-contradiction-baseline-M07
summary: "M07 contradiction log for the cross-spec contradiction baseline research run. Primary method."
created: 2026-05-07
updated: 2026-05-07
---

# M07 — Contradiction Log

## Purpose

This file records the M07 (Contradiction Log) critical-thinking method as applied to the cross-spec normative contradiction baseline research. M07 was the primary method: systematically seeking contradictions in the corpus rather than assuming consistency.

## Application

**Corpus:** 8 root governance specs, ~1644 lines total.

**Approach:** For each topic domain (readme update cadence, friction log placement, slug length, frontmatter requirements, task status semantics, session setup ordering, subfolder thresholds), I asked: "Is there any other spec that makes a conflicting normative claim about this?"

**Validation:** The known CONTR-001 anchor (FRUSTRATED.md §28 ↔ PRE_COMMIT.md §2) was found on the first pass through the readme-update domain, confirming the methodology was operating correctly.

## Summary of Contradictions Found

| ID | Domain | Type | Severity |
|---|---|---|---|
| CONTR-001 | Readme update cadence | Direct | High |
| CONTR-002 | Readme update batching unit | Scope-overlap | Medium |
| CONTR-003 | Slug length ceiling | Scope-overlap | Medium |
| CONTR-004 | T3 tier repair permission | Direct | High |
| CONTR-005 | Session-start governance gate | Direct | High |
| CONTR-006 | Friction log artifact type | Lifecycle | High |
| CONTR-007 | Friction log location wording | Indirect | Low |
| CONTR-008 | Subfolder file-count threshold | Scope-overlap | Medium |
| CONTR-009 | Operational readme.md frontmatter level | Scope-overlap | Medium |
| CONTR-010 | External ingestion same-commit completeness | Lifecycle | Medium |
| CONTR-011 | Research slug = prompt slug constraint | Direct | Medium |
| CONTR-012 | SessionStart hook ordering | Indirect | Low |
| CONTR-013 | Task blocked-status semantics | Scope-overlap | Medium |
| CONTR-014 | Prompt task friction log location | Scope-overlap | High |
| CONTR-015 | RFC 2119 section requirement | Scope-overlap | Low |
| CONTR-016 | Workspace script prohibition timing | Lifecycle | Low |

## M07 Finding

The 8 root specs have a **significant latent contradiction load** — 16 contradictions across 1644 lines, or roughly 1 contradiction per ~100 lines of spec text. Type distribution: 4 Direct, 2 Indirect, 7 Scope-overlap, 3 Lifecycle. This load is concentrated in three high-risk clusters:

1. **Readme update cadence** (CONTR-001, CONTR-002): 2 contradictions, 1 High. The most operationally damaging because agents encounter it on every commit.
2. **Friction log placement** (CONTR-006, CONTR-007, CONTR-014): 3 contradictions, 2 High. The most mechanically enforced because `tools/check-trust.py` is an active linter.
3. **Session setup bypass** (CONTR-004, CONTR-005, CONTR-012): 3 contradictions, 2 High. The most architecturally significant because they govern agent startup behavior. (Note: CONTR-004 reclassified Direct — `MUST NOT X` vs `MAY X` is an absolute prohibition against explicit permission, not a MUST-vs-SHOULD indirect conflict.)

The fact that 15 of 16 contradictions were previously undocumented justifies this research as a necessary pre-chain baseline. Without it, the 032–039 chain's falsification criterion #3 ("root specs MUST NOT gain new contradictory clauses from the chain") could not be verified.
