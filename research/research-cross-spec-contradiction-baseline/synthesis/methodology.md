---
type: note
status: active
slug: research-cross-spec-contradiction-baseline-methodology
summary: "Methods applied: systematic RFC 2119 cross-indexing (M07 contradiction log) across 8 root specs, 4 conflict-class taxonomy."
created: 2026-05-07
updated: 2026-05-07
---

# Methodology — Cross-Spec Normative Contradiction Baseline

## Methods Applied

**M07 — Contradiction Log:** Primary method. All 8 root specs read in full. Normative clauses (uppercase RFC 2119 keywords) extracted and cross-indexed by topic domain (readme update cadence, friction log placement, slug length, frontmatter requirements, task status semantics, session setup ordering).

**M02 — Falsification Check:** The known CONTR-001 anchor (FRUSTRATED.md §28 ↔ PRE_COMMIT.md §2) was used as a validation anchor before cataloging additional findings. A result of zero new contradictions would have triggered M02 falsification (see brief.md Falsification clause).

## Conflict-Class Taxonomy

| Class | Definition | Count found |
|---|---|---|
| Direct | MUST X vs MUST NOT X on same topic, same actor | 3 |
| Indirect | MUST X vs SHOULD NOT X (or SHOULD X vs MUST NOT X) | 3 |
| Scope-overlap | Incompatible normative claims on same file/path/artifact | 7 |
| Lifecycle | Different ordering or timing for the same action | 3 |

## Corpus Coverage

- Total spec lines read: ~1644 (AGENTS.md 413, TASK.md 416, RESEARCH.md 203, PROMPT.md 119, FOLDERS.md 117, FRUSTRATED.md 32, PRE_COMMIT.md 149, MAINTENANCE.md 195)
- Pairs analyzed: 28 (C(8,2) = 28 spec pairs)
- Plus internal-spec self-contradictions: MAINTENANCE.md §1 vs §3.4 (CONTR-004), RESEARCH.md §3 vs §6.1 (CONTR-011), TASK.md §4 vs §8.7 (CONTR-013)
