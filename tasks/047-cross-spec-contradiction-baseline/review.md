---
type: note
status: active
slug: task-047-review
summary: "PR #77 review by Claude Code (claude/brave-darwin-wC1z5). Two critical data-consistency errors in REPORT.md §5 heat map and type table, plus three softer issues."
created: 2026-05-07
updated: 2026-05-07
---

# PR #77 Review — Task 047 Cross-Spec Contradiction Baseline

**Reviewer:** Claude Code (session `claude/brave-darwin-wC1z5`)
**PR:** [#77](https://github.com/netzkontrast/agency/pull/77) — `claude/busy-cori-9v8wp → main`
**Head SHA:** `e026c764`
**Review date:** 2026-05-07

---

## Summary

The work is substantive and valuable. 16 contradictions are cataloged with verbatim quotes, per-spec risk tables, and per-task amendment-safety recommendations covering all 8 chain tasks. Governance checks pass. All acceptance criteria from `brief.md` are met in spirit. However, two data-consistency errors in `REPORT.md §5` directly contradict acceptance criterion 5 ("§5 statistics are internally consistent with §2 catalog"), and three softer issues warrant attention before merge.

---

## P-1 — Critical: CONTR-007 type mismatch between §2 and §5

**Location:** `research/research-cross-spec-contradiction-baseline/output/REPORT.md`

**§2 declaration (CONTR-007):**
```
**Type:** Indirect
```

**§5 By-Type table:**
```
| Indirect | 3 | CONTR-004, CONTR-008, CONTR-012 |
| Scope-overlap | 7 | CONTR-002, CONTR-003, CONTR-007, CONTR-009, CONTR-013, CONTR-014, CONTR-015 |
```

CONTR-007 is labeled `Indirect` in the §2 catalog entry but placed in the `Scope-overlap` row in the §5 type-count table. This is an internal inconsistency: either the §2 label or the §5 row is wrong.

Looking at the CONTR-007 conflict description ("PR description or **submit message**" vs PR description or **commit message**"), the conflict is a wording-divergence between two specs covering the same artifact with slightly different language — which fits `Scope-overlap` better than the report's own definition of `Indirect` ("MUST X vs SHOULD NOT X"). The fix is to correct §2's `Type: Indirect` to `Type: Scope-overlap`, giving:

- Indirect: 3 → 3 (CONTR-004, CONTR-008, CONTR-012) — unchanged
- Scope-overlap: 7 → 7 (same list) — unchanged, CONTR-007 already in the right row

The total count of 16 is unaffected; only the §2 label on CONTR-007 needs correction.

**Verdict:** Fix required before merge — violates `brief.md` acceptance criterion 5 directly.

---

## P-2 — Critical: CONTR-016† misattributed to AGENTS.md in §3 and §5

**Location:** `REPORT.md §3 (AGENTS.md risk table)` and `REPORT.md §5 (heat map)`

**§5 heat map (AGENTS.md row):**
```
| AGENTS.md | 5 (CONTR-005, CONTR-009, CONTR-012, CONTR-015, CONTR-016†) |
```

**§3 AGENTS.md table:**
```
| Contradictions involving this spec | 5 (CONTR-005, CONTR-009, CONTR-012, CONTR-015, CONTR-016†) |
```

**§2 CONTR-016 entry:**
- Spec A: `RESEARCH.md §4` — execution scripts in `/workspace`
- Spec B: `PRE_COMMIT.md §1` — general clean-working-directory check
- AGENTS.md is not referenced anywhere in the §2 CONTR-016 description.

There is no stated or derivable connection between CONTR-016 and AGENTS.md. The attribution inflates AGENTS.md's count from 4 to 5. Combined with the undefined `†` symbol (see P-3 below), a reader cannot understand why AGENTS.md appears in this row at all.

The PRE_COMMIT.md heat map row has a parallel anomaly: `CONTR-005†` (5 involvements), but CONTR-005 concerns AGENTS.md SS.2 ↔ MAINTENANCE.md §4.1 — PRE_COMMIT.md is not directly involved per §2.

**Verdict:** Fix required before merge. Either:
(a) Remove `CONTR-016†` from AGENTS.md's row (correcting count to 4), and remove `CONTR-005†` from PRE_COMMIT.md's row, OR
(b) Add explicit explanatory prose in §3 for each `†` entry, defining the dagger notation and the indirect-involvement rationale.

---

## P-3 — Minor: `†` notation used in §3 and §5 without a legend

**Location:** `REPORT.md §3` (multiple spec tables) and `REPORT.md §5` (heat map)

The `†` symbol appears on `CONTR-005†` in the PRE_COMMIT.md row and on `CONTR-016†` in the AGENTS.md row, but no legend is defined anywhere in the document. A reader cannot determine whether `†` denotes "indirect involvement", "partial involvement", "mentioned only in passing", or something else.

If `†` is intentional (indicating indirect/tangential involvement), a single-sentence legend immediately above or below the heat map table would suffice:
> `†` denotes tangential involvement — the spec is referenced in the conflict resolution path but is not one of the two primary clause sources.

**Verdict:** Non-blocking but should be addressed with P-2.

---

## F-A — Soft: `prompt_relates_to_task: ""` in `prompts/research-cross-spec-contradiction-baseline/prompt.md`

**Location:** `prompts/research-cross-spec-contradiction-baseline/prompt.md` frontmatter

Task 047 lists this prompt in `task_uses_prompts`. Per `PROMPT.md §6.6` (Forward Link Reciprocity), when a Task already lists a prompt in `task_uses_prompts`, the prompt's `prompt_relates_to_task` SHOULD be set to the task slug. The current value `""` (empty string) leaves the reciprocal link incomplete.

Correct value: `cross-spec-contradiction-baseline` (the slug of Task 047).

Alternatively, the field may be omitted entirely — `PROMPT.md §3` marks it OPTIONAL. An explicit empty string is neither the intended "set" nor the intended "omit" state and could produce confusing lint output.

**Verdict:** Non-blocking. Fix in a follow-up commit or as part of the amendment-chain Task 034 (which touches PROMPT.md frontmatter anyway).

---

## F-B — Soft: CONTR-004 type classification "Indirect" is inconsistent with the report's own taxonomy

**Location:** `REPORT.md §2 CONTR-004`

The report defines the four conflict classes in §1 as:

> **Indirect conflict** — Spec A says MUST X; Spec B says SHOULD NOT X (or Spec A says SHOULD X; Spec B says MUST NOT X).

CONTR-004's conflict is:
- MAINTENANCE.md §1 + §3.1: "**MUST NOT** fix directly"
- MAINTENANCE.md §3.4: "**MAY** perform the transition directly"

This is a `MUST NOT X` vs `MAY X` conflict — an absolute prohibition pitted against an explicit permission. By the report's own taxonomy, that is closer to **Direct** (two obligations that cannot simultaneously be satisfied) than to **Indirect** (a MUST vs a SHOULD NOT, where partial compliance is theoretically possible).

Note: this is a judgment call, and "Indirect" is defensible if the author reads §3.4's "MAY" as weaker than §1's "MUST NOT" (the MUST NOT wins, so there is no strict logical contradiction, only a confusing permission). The finding is flagged here for transparency, not as a required fix.

**Verdict:** Non-blocking. Consider adding a note in §2 CONTR-004 explaining the classification choice.

---

## What is correct and works well

- All 8 root specs are covered in §3 (acceptance criterion 3 met).
- CONTR-001 (anchor) appears first, labeled High, with both clause quotes verbatim (acceptance criterion 1 met).
- §4 provides at least one amendment-safety note per chain task 032–039 (acceptance criterion 4 met).
- `research_phase: complete` in `research/research-cross-spec-contradiction-baseline/readme.md` (acceptance criterion 6 met).
- `tools/check-governance.sh` exits 0 on the branch (acceptance criterion 7 met per commit message).
- Total count of 16 in §5 is consistent with §2's CONTR-001 through CONTR-016 entries.
- Pre-existing Task 041 `friction-log.md` trust-check bug correctly identified and fixed.
- Workspace structure is fully compliant: `prompt.md`, `workspace/`, `synthesis/`, `reflection/`, `output/` all present with required sub-files.
- The three internal self-contradictions (CONTR-004, CONTR-011, CONTR-013) are a valuable addition that the prompt did not explicitly demand but are directly relevant to the use case.

---

## Required actions before merge

| ID | Severity | Action |
|---|---|---|
| P-1 | **Required** | Fix `**Type:** Indirect` → `**Type:** Scope-overlap` in §2 CONTR-007 |
| P-2 | **Required** | Remove spurious `CONTR-016†` from AGENTS.md row (and `CONTR-005†` from PRE_COMMIT.md row) in §3 and §5, or add legend + rationale |
| P-3 | Recommended | Add `†` legend to §5 heat map if P-2 retains dagger notation |
| F-A | Optional | Set `prompt_relates_to_task: cross-spec-contradiction-baseline` or omit the empty-string field |
| F-B | Optional | Add a classification-rationale note to CONTR-004 §2 entry |
