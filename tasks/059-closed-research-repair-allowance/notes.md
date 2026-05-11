---
type: note
status: active
slug: 059-closed-research-repair-allowance-notes
summary: "Inventory of T1-T4 vocabulary and §4.7 lifecycle interaction decision for the closed-research repair allowance."
created: 2026-05-08
updated: 2026-05-08
---

# Task 059 — Notes

## Inventory of `MAINTENANCE.md §1` Tier Vocabulary (Pre-Amendment)

| Tier | Coverage | Permitted on closed research |
|---|---|---|
| T1 — Mechanical | `updated:` bump, derived `slug:`, broken-link repair, missing `readme.md` stub | NO (T4 blanket) |
| T2 — Additive | Adding unambiguous L1/L2 keys | NO (T4 blanket) |
| T3 — Structural | Heading rewrites, schema migrations, slug renames | NO (T4 blanket) |
| T4 — Research-touching | "Any modification" to a `research_phase: complete` workspace | NO (the rule itself) |

The pre-amendment T4 was a blanket "MUST NOT touch" — strictly more
restrictive than the §1 ladder for every other file type, where T1
and T2 are always allowed.

## Amendment Shape

**Split T4 into content vs metadata.** The amendment renames the
existing tier to "T4 — Research-touching (content)" and adds a §1.0.1
allowance carving out T1 and T2 on closed research. T3 stays
forbidden on closed research because heading rewrites and schema
migrations *are* content-shape changes even when the prose is
preserved.

The §1.0.1 wording matches the existing §8.4 Resumption Checklist
convention by requiring (a) a one-line rationale in the commit
message and (b) a bumped `updated:` on the workspace itself, so the
repair is discoverable in the commit log and in the workspace's own
metadata.

## §4.7 Lifecycle Decision

**Decision: closed-research T1/T2 repair MUST NOT trip the
originating Task's `task_status` lifecycle.**

Rationale: §4.7's lifecycle classifier exists to detect when a
`done` Task drifts back into open work. A T1/T2 repair on the Task's
research output is not new work — it is downstream remediation of an
unrelated rename or move. Treating the repair as a re-open would
create a perverse incentive (file the repair as a fresh Task, leave
the upstream rename's commit churning across multiple Tasks).

The repair commit SHOULD cite the originating Task slug so the audit
trail is preserved, but `tools/fm/check-task-lifecycle-classification.py`
MUST NOT flip `task_status: done` to `updated` on the basis of a
T1/T2 closed-research repair commit alone.

## Cross-Reference Touchpoints

- `MAINTENANCE.md §1` — main amendment (split T4 + §1.0.1 allowance).
- `RESEARCH.md §7 (Anti-Patterns)` — pointer to MAINTENANCE.md §1.0.1
  on the existing "MUST NOT edit" bullet so RESEARCH.md doesn't
  contradict the new allowance.
- `CLAUDE.md §8 (Repair tiers)` — same split, plus pointer to §1.0.1.
