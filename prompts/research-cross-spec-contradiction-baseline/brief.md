---
type: note
status: active
slug: research-cross-spec-contradiction-baseline-brief
summary: "Brief for: catalog all existing inter-spec normative contradictions across the 8 root specs before the 032–039 amendment chain lands."
created: 2026-05-07
updated: 2026-05-07
---

# Brief: Research — Cross-Spec Normative Contradiction Baseline

## Goal

Produce `research/research-cross-spec-contradiction-baseline/output/REPORT.md` cataloging every existing normative contradiction across the 8 root governance specs before the 032–039 amendment chain lands its spec edits. The catalog becomes the pre-chain "before" state that makes falsification criterion #3 of the chain mechanically verifiable.

## Inputs

- `/home/user/agency/AGENTS.md`
- `/home/user/agency/TASK.md`
- `/home/user/agency/RESEARCH.md`
- `/home/user/agency/PROMPT.md`
- `/home/user/agency/FOLDERS.md`
- `/home/user/agency/FRUSTRATED.md`
- `/home/user/agency/PRE_COMMIT.md`
- `/home/user/agency/MAINTENANCE.md`
- `tasks/readme.md` §Chain-Level Falsification (criteria 1–4)
- Known anchor contradiction: FRUSTRATED.md §28 ↔ PRE_COMMIT.md §2 (readme-update cadence)

## Acceptance Criteria

1. REPORT.md §2 contains ≥1 contradiction (anchor CONTR-001 = FRUSTRATED §28 ↔ PRE_COMMIT §2).
2. Every entry in §2 cites exact spec section + quoted clause fragment from both sides.
3. §3 per-spec risk table covers all 8 specs.
4. §4 names at least one amendment-safety note per chain task (032–039).
5. §5 summary statistics are internally consistent with §2 catalog count.
6. `research_phase: complete` in `research/research-cross-spec-contradiction-baseline/readme.md`.
7. `tools/check-governance.sh` exits 0 on the produced commit.

## Falsification

**Wrong cut iff** the catalog finds zero contradictions beyond the known anchor (CONTR-001). That would mean the 8 root specs are internally consistent except for one known case — which contradicts empirical evidence (prior research surfaced multiple friction points between PRE_COMMIT.md §2, FRUSTRATED.md §28, MAINTENANCE.md §1, and TASK.md §4 that were not formally cataloged). A zero-new-contradiction result MUST trigger a M07 contradiction log entry explaining why.

## Estimated Effort

~2–3 hours of systematic reading + cross-reference work across 1644 lines of spec text. One focused session.
