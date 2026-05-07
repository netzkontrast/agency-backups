---
type: note
status: active
slug: research-cross-spec-contradiction-baseline-tracks
summary: "Per-track work breakdown for the cross-spec contradiction baseline research run."
created: 2026-05-07
updated: 2026-05-07
---

# Tracks — Cross-Spec Normative Contradiction Baseline

## Track A — Readme Update Cadence Cluster

**Specs:** FRUSTRATED.md §28, PRE_COMMIT.md §2, FOLDERS.md §3
**Contradictions:** CONTR-001 (High), CONTR-002 (Medium)
**Finding:** The readme-update-cadence cluster is the most entangled 3-way conflict. PRE_COMMIT.md mandates the batch update; FOLDERS.md defines the batching concept; FRUSTRATED.md flags the per-file form as FL2 without clearly exempting the batch. Tasks 036, 037, 038 must coordinate on resolution.

## Track B — Friction Log Placement Cluster

**Specs:** FRUSTRATED.md §32, TASK.md §7, PROMPT.md §6.8
**Contradictions:** CONTR-006 (High), CONTR-007 (Low), CONTR-014 (High)
**Finding:** Two independent High-severity contradictions (CONTR-006 from FRUSTRATED.md, CONTR-014 from PROMPT.md) arise from the same root: TASK.md §7 prohibits inline commit-message friction logs but both other specs permit them. Tasks 033, 034, 038 must coordinate. CONTR-014 is a separate entry because it gives Tasks 033 and 034 the opportunity to resolve it from different sides.

## Track C — Slug Length Ceiling Conflict

**Specs:** FOLDERS.md §2, RESEARCH.md §6.1
**Contradictions:** CONTR-003 (Medium)
**Finding:** FOLDERS.md's universal 5-token ceiling conflicts with RESEARCH.md's 6-token allowance for external research slugs. Cleanest resolution: explicit FOLDERS.md carve-out. Tasks 035, 036 should coordinate.

## Track D — Session Setup Ordering Cluster

**Specs:** AGENTS.md SS.1/SS.2, MAINTENANCE.md §4.1, §2.1
**Contradictions:** CONTR-005 (High), CONTR-012 (Low)
**Finding:** AGENTS.md SS.2's absolute gate conflicts with MAINTENANCE.md's bypass. The bypass is intentional and correct in context; the issue is that neither spec cross-references the other. Tasks 032, 039 need coordinated cross-references.

## Track E — Internal Self-Contradictions

**Specs:** MAINTENANCE.md §1 vs §3.4, RESEARCH.md §3 vs §6.1, TASK.md §4 vs §8.7
**Contradictions:** CONTR-004 (High), CONTR-011 (Medium), CONTR-013 (Medium)
**Finding:** Three specs contain internal contradictions — clauses within the same spec that conflict. These are the easiest to resolve since they require only intra-spec amendments without cross-spec coordination.

## Track F — Frontmatter Obligation Level

**Specs:** AGENTS.md, TASK.md, FOLDERS.md §5
**Contradictions:** CONTR-009 (Medium), CONTR-015 (Low)
**Finding:** Two lower-severity conflicts about whether readme.md files in operational folders must carry frontmatter (MUST vs SHOULD). Task 036 can resolve CONTR-009; CONTR-015 (RFC 2119 section requirement) is a T3 effort that may warrant its own follow-up Task.
