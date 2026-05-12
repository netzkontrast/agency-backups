---
type: note
status: active
slug: task-092-st1-review
summary: "Peer review of PR #116 (Task 092 ST-1): Phase 2 triage matrix. One blocking issue: frontmatter count mismatch (port=20/adapt=22 vs. body table port=18/adapt=24). One substantive concern: four D.6-overflow rows misclassified as `port` instead of `adapt`. Two advisory items."
created: 2026-05-12
updated: 2026-05-12
---

# Review — PR #116 · Task 092 ST-1: Phase 2 Triage Matrix

**Reviewer:** claude-sonnet-4-6  
**PR:** [#116](https://github.com/netzkontrast/agency/pull/116)  
**Branch:** `claude/task-92-superclaude-FWvaT` → `main`  
**Commit:** `8bcddc0`  
**Date:** 2026-05-12

---

## Verdict: CHANGES REQUESTED

The triage matrix is a solid artefact — 81 rows, well-structured, clean ADR-0011 clause
citations for adapt rows, no external GitHub URLs (T092.1.3 ✓), and the 21 triage-notes
provide enough per-skill detail to give ST-2 / ST-3 clear port recipes. Governance passes
clean (`tools/check-governance.sh` exits 0). Methodology (three parallel `Explore`
subagents + matrix synthesis) is sound and the FL0 declaration is credible.

Two issues prevent merge as-is:

1. **Frontmatter `summary:` field carries wrong port/adapt counts** (T1 mechanical repair —
   trivial, but the wrong summary is load-bearing for token-efficient reads).
2. **Four rows marked `port` should be `adapt`** (bodies > 5 KB, references/ extraction
   required per the spec definition) — will cause predictable ST-3 rework if not fixed here.

Two advisory items are also noted but are not merge-blockers.

---

## What works

### Coverage and row density

81 rows covering the full non-Phase-1 snapshot catalogue: 26 SC commands, 11 SC agents,
5 SC modes, 10 SC skills (including all four `confidence-check` copies), 14 SP skills, and
15 SP infra artefacts (hooks, lib, docs, manifest). The ≥ 75-row floor (AC T092.1.4) is
met with margin.

### ADR-0011 clause discipline for adapt rows

Every `adapt` row correctly cites at least one of D.6 / D.7 / D.8 (AC T092.1.2 ✓).
The D.8 MCP bindings catalogue (Sequential, Serena, Morphllm, Magic, Context7, Playwright,
Chrome-DevTools) is consistently applied and the D.7 SessionStart prohibition is correctly
applied to all three Superpowers hook artefacts (rows 71–73).

### External-URL discipline

`grep -rn "https://github.com" tasks/092-port-skill-corpora-phase-2/references/` returns
zero matches (AC T092.1.3 ✓). Every source citation resolves to a local snapshot path.

### Triage-note quality

The 21 notes are well-scoped. Highlights:

- **`sc-pure-ports-cluster.md`** — the nine-row batch note with the exact port recipe
  (frontmatter strip, Agency header, readme scaffold, `tools/fm/validate.py` gate) is
  exactly what ST-2 needs to batch-port cleanly.
- **`validator-touchpoints.md`** — the ST-2/ST-3 diagnostic cheat-sheet (`F.A.1`,
  `F.A.2`, `F.B.8`, `F.B.9`, `F.B.10`) is a valuable operational aid. The ADR-0012
  dependency note is correctly hedged.
- **`superpowers-writing-skills.md`** — correctly identifies the 4.4× D.6 overflow,
  proposes the `references/` split, and surfaces the deconfliction requirement with
  Agency's existing skill-authoring tooling. Net-new analytical value.
- **`superpowers-finishing-a-branch.md`** — good catch that this skill adds the "discard"
  branch absent from Agency's Closing Run Procedure (AGENTS.md CR.1–CR.7). Cross-reference
  plan is concrete.

### Classification logic for skip rows

The 39 skip decisions are well-reasoned. Plugin wrapper deduplication (rows 44–51),
SessionStart hook rejection (rows 71–73), and platform-specific doc rejection
(rows 76–77, 79) all follow the correct ADR-0011 logic. The `superpowers/lib/skills-core.js`
skip (row 74) correctly identifies the Node runtime as incompatible with Agency's Python
tooling.

---

## Issue 1 (BLOCKING): Frontmatter `summary:` carries wrong port/adapt counts

**Severity:** Blocking (T1 repair) — the summary field is the primary token-saving lever
for downstream agents scanning the index. An incorrect count in `summary:` will silently
mislead every future reader relying on it as the fast path.

**Evidence:**

Matrix frontmatter (`tasks/092-port-skill-corpora-phase-2/references/triage-matrix.md`):

```yaml
summary: "Phase 2 triage decision matrix. 81 rows … Counts: port=20, adapt=22, skip=39."
```

Matrix body count table (same file, end of document):

| Decision | Total |
|---|---|
| `port` | **18** |
| `adapt` | **24** |
| `skip` | **39** |

PR body (`#116`) also reports `port=18, adapt=24, skip=39`.

The frontmatter says `port=20, adapt=22` but the authoritative body table says
`port=18, adapt=24`. The summary is wrong by 2 in each direction.

**Repair (T1 — Mechanical):** Update `summary:` via `tools/fm/edit.py --set` to match
the body counts:

```
port=18, adapt=24, skip=39
```

---

## Issue 2 (Substantive concern): Four D.6-overflow rows misclassified as `port`

**Severity:** Non-blocking by the letter of the four ST-1 Gherkin ACs, but will cause
**guaranteed ST-3 rework** — all four rows will fail `tools/fm/validate.py F.B.10` the
moment an ST-3 agent attempts a verbatim port. Recommend fixing here rather than at
ST-3 boundary.

**Spec definition (subtasks/01-triage.md §Scope):**

> **`port`** — verbatim or near-verbatim mirror is suitable; **body fits 5 KB**; no
> MCP-binding adaptation needed.
>
> **`adapt`** — body requires ADR-0011 D.8 rewrite, **or D.6 overflow (> 5 KB body)
> requires references/ extraction**, or a SessionStart-injection clause needs stripping.

`port` is defined as "body fits 5 KB". Any row where the body exceeds the cap and
`references/` extraction is required is by definition an `adapt` row.

**Affected rows:**

| Row | Snapshot artefact | Body KB | Decision (current) | Decision (correct) |
|---|---|---|---|---|
| 54 | `superpowers/skills/using-git-worktrees/SKILL.md` | 5.6 | `port` D.1, D.6 | **`adapt`** D.1, D.6 |
| 56 | `superpowers/skills/receiving-code-review/SKILL.md` | 6.3 | `port` D.1, D.6 | **`adapt`** D.1, D.6 |
| 57 | `superpowers/skills/systematic-debugging/SKILL.md` | 9.9 | `port` D.1, D.6 | **`adapt`** D.1, D.6 |
| 58 | `superpowers/skills/test-driven-development/SKILL.md` | 9.9 | `port` D.1, D.6 | **`adapt`** D.1, D.6 |

All four rows already cite D.6 in the clauses column — the clause citation is correct, only the
decision label needs updating.

**Row 53 (borderline — advisory):** `superpowers/skills/finishing-a-development-branch/SKILL.md`
is listed as `port` with body 5.3 KB "≈ cap (verify)", yet D.6 is **not** cited in the matrix
row (only D.1). If the body verifies to > 5 KB, this row also requires `adapt` + D.6 citation.
The triage note correctly flags the verify requirement but the matrix row itself is ambiguous.

**Updated counts after correction:**

| Decision | Current | Corrected |
|---|---|---|
| `port` | 18 | **14** (or 13 if row 53 also corrects) |
| `adapt` | 24 | **28** (or 29) |
| `skip` | 39 | 39 |
| **Total** | **81** | **81** |

The total remains 81, AC T092.1.4 still passes. AC T092.1.2 is unaffected (adapt rows
already have D.* citations; reclassifying adds four more adapt rows that also carry D.6).

**Repair:** Update the four `port` decisions to `adapt` in the matrix table. Update the
body count table counts. Update `summary:` in frontmatter. For row 53: verify body size
via `wc -c tasks/091-port-external-skill-corpora/references/upstream-snapshot/superpowers/skills/finishing-a-development-branch/SKILL.md` — if > 5120 bytes, reclassify to `adapt` and add D.6 to its clauses column.

---

## Issue 3 (Advisory): Superpowers infra section header says "13 rows" but contains 15

**Section header (matrix body, after row 66):**

> `## Superpowers v4.0.3 — commands / agents / hooks / lib / docs / manifest (13 rows)`

**Actual rows in section:** rows 67–81 = **15 rows**. The discrepancy is cosmetic but
may confuse ST-3 authors expecting a 13-row inventory.

**Repair:** Update the header to `(15 rows)`.

---

## Issue 4 (Advisory): Row 53 — D.6 absent from matrix clauses column despite acknowledged overflow

As noted under Issue 2 above: the triage note `superpowers-finishing-a-branch.md`
explicitly says "5.3 KB body — slightly over the D.6 5 KB cap; verify exact bytes …
during ST-3 import", yet the matrix row cites only `D.1`. If the body is over cap, D.6
MUST be cited in the matrix (AC T092.1.2 would require it once the decision column
becomes `adapt`). Adding D.6 to row 53's clauses column now — ahead of the body
verification — would make the matrix self-consistent regardless of the exact byte count.

---

## Checklist against T092.1.1–T092.1.4

| Criterion | Status | Notes |
|---|---|---|
| **T092.1.1** — every candidate has a row | ✅ | 81 rows; Phase-1 ports correctly excluded |
| **T092.1.2** — every `adapt` row cites D.* | ✅ | All current 24 adapt rows have citations |
| **T092.1.3** — no external GitHub URLs | ✅ | `grep` returns zero matches |
| **T092.1.4** — ≥ 75 rows | ✅ | 81 rows; corrections do not affect total |

---

## Summary of required actions before merging

| # | Severity | Action | File(s) |
|---|---|---|---|
| 1 | **Blocking (T1)** | Fix `summary:` frontmatter counts to `port=18, adapt=24, skip=39` | `references/triage-matrix.md` |
| 2 | **Strongly recommended** | Reclassify rows 54, 56, 57, 58 from `port` → `adapt`; update body count table | `references/triage-matrix.md` |
| 3 | Advisory | Verify row 53 body size; if > 5 KB, reclassify to `adapt` + add D.6 to clauses | `references/triage-matrix.md` |
| 4 | Advisory | Fix section header "(13 rows)" → "(15 rows)" for Superpowers infra section | `references/triage-matrix.md` |

Items 1 and 2 can be addressed in a single follow-up commit on `claude/task-92-superclaude-FWvaT`.
Items 3 and 4 may be batched with the same commit or deferred to a T1 follow-up.

---

## Assumptions Log

- Body-byte counts cited in the matrix rationale column are subagent-reported approximations;
  this review treats the stated values as ground truth for classification purposes. ST-3 MUST
  re-measure against `F.B.10` before porting regardless.
- The matrix's own "Assumptions Log" note (end of document) acknowledges approximate byte
  counts — this review does not contradict that; the argument is that approximate ≥ 5 KB
  is sufficient to classify `adapt`, not that exact byte counts were independently verified.
