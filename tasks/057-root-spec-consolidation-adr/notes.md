---
type: note
status: active
slug: 057-root-spec-consolidation-adr-notes
summary: "Implementation notes for Task 057 — root-spec bundle measurement, cross-reference rewrite-cost audit, and the ADR-0009 status-quo decision."
created: 2026-05-11
updated: 2026-05-11
---

# Task 057 — Implementation Notes

## 1. Bundle-token-cost measurement

Measured 2026-05-11 on `claude/complete-three-tasks-n3fZR`. Token estimates use the canonical 4-chars-per-token heuristic.

| File | Lines | Bytes | Tokens (~) |
|---|---:|---:|---:|
| `AGENTS.md` | 517 | 41,096 | 10,274 |
| `TASK.md` | 458 | 39,638 | 9,909 |
| `PROMPT.md` | 245 | 17,022 | 4,255 |
| `RESEARCH.md` | 289 | 20,679 | 5,169 |
| `FOLDERS.md` | 194 | 16,110 | 4,027 |
| `PRE_COMMIT.md` | 257 | 21,822 | 5,455 |
| `FRUSTRATED.md` | 119 | 8,659 | 2,164 |
| `MAINTENANCE.md` | 471 | 48,091 | 12,022 |
| `SKILLS.md` | 276 | 19,414 | 4,853 |
| `README.md` | 343 | 35,320 | 8,830 |
| `maintenance/language-spec.md` | 317 | 14,855 | 3,713 |
| **Bundle total** | **3,486** | **282,706** | **~70,676** |

The README §10 catalogue calls this "9+ root specs"; the **measured** count is **11**. The "9+" is approximate; a T1/T2 edit to README §10 would correct this — noted in ADR-0009 §"Neutral consequences" as a follow-on but explicitly NOT bundled into this decision-class ADR.

## 2. Cross-reference rewrite cost

`grep -rln <spec> --include="*.md" --include="*.py" --include="*.sh"` against the entire repo:

- **`FRUSTRATED.md`**: 206 referencing files (200 md, 5 py, 1 sh).
- **`PRE_COMMIT.md`**: 175 referencing files.
- **Distinct anchor links** (one per spec):
  - `FRUSTRATED.md#when-and-how-to-log-mandatory`
  - `PRE_COMMIT.md#7-mechanical-governance-checks`

**Total rewrite count: 381 files.** Mechanical via `sed`, but each rewritten link MUST be re-verified against the new anchor (e.g. `[FRUSTRATED.md](../../FRUSTRATED.md)` → `[MAINTENANCE.md#friction-logging](../../MAINTENANCE.md#friction-logging)` — the relative path *and* the in-page anchor both change). The resulting links are also longer and slightly less readable.

A measurement that didn't make it into the ADR but is worth recording: of the 200 markdown referencing files for FRUSTRATED.md, the vast majority (~180) are inside `/tasks/<NNN>-<slug>/friction-log.md` files — i.e., they cite FRUSTRATED.md as the FL-declaration governance, not as a section reference. Those citations are uniform string substitutions, which is why the rewrite is mechanical. But the *blame* trail for every one of those files would be replaced by the consolidation-agent's commit, which degrades archaeology.

## 3. Optimistic merge-saving estimate

Section-by-section accounting of what *could* be saved if M1 + M2 land:

- L1 frontmatter + title + 1-paragraph intro per merged file: ~100 tokens × 2 = **~200 tokens**.
- "See [PRE_COMMIT.md](...)" / "See [FRUSTRATED.md](...)" pointers inside other root specs (each pointer ≈ 12 tokens; ~30 pointers across all specs): **~300–600 tokens**.
- Inline scaffolding ("as defined in this section") that exists today as cross-file prose: **~100–300 tokens**.

**Optimistic total: ~600–1,100 tokens** ≈ **0.85 – 1.55 % of the 70,676-token bundle.**

This is the **upper bound**, not the expected value. A realistic estimate is ~600 tokens (~0.85 %).

## 4. In-flight Task dependency audit

| Task | Status | Affected by merge? |
|---|---|---|
| [Task 037](../037-pre-commit-spec-integration/) — Pre-commit spec integration | `done` | Yes — PC.B.1–PC.B.4 anchors live in `PRE_COMMIT.md §7.A`; merge would invalidate every external citation. |
| [Task 038](../038-frustrated-spec-integration/) — FRUSTRATED.md integration | `updated` | Yes — FR.B.1–FR.B.4 anchors cited from `tools/check-fl-declaration.py` and the AGENTS.md synthesis block. |
| [Task 044](../044-improve-maintenance-spec-may-07-2026/) | `open` | Yes — `task_affects_paths` includes FRUSTRATED.md. |
| [Task 062](../062-frustrated-spec-followup-ac1-ac5/) | `open` | **Yes** — explicitly references `FRUSTRATED.md §28` and `PRE_COMMIT.md §2` byte-identicality, which would either dissolve or require re-engineering as a same-file cross-section contract. |
| [Task 064](../064-improve-maintenance-spec-may-08-2026/) | `open` | Yes — `task_affects_paths` includes FRUSTRATED.md. |

Five Tasks would need coordinated retargeting if M1 + M2 landed today.

## 5. The ADR

Authored at [`decisions/0009-root-spec-no-consolidation.md`](../../decisions/0009-root-spec-no-consolidation.md), `adr_status: Proposed`. Validates clean against `python3 tools/adr/cli.py validate` (1 → 0 diagnostics after summary trimmed to ≤ 240 chars).

The ADR records **three falsifier triggers** (F1–F3) that, when any fires, mandate a successor ADR re-evaluating Options 1 and 2:

- **F1.** Bundle-token cost > 100,000 tokens (today: ~70,676).
- **F2.** Either spec drops below 1,000 tokens AND its dependent-file count drops below 50.
- **F3.** Sustained FL1+ friction citing root-spec count as cause across ≥ 3 sessions in a 14-day window.

The ADR ships at `Proposed` rather than `Accepted` for the same reason as ADR-0008: the triggers have not been observed yet, and `Accepted` would prematurely lock the topology against the very evidence the triggers are designed to surface.

## 6. Why no successor implementation Task is opened

Status quo requires zero migration. A successor ADR (if a trigger fires) would spawn the consolidation Task at that time. Opening a pre-emptive consolidation Task today would invert the falsifier logic.

## 7. Sibling decision pattern with ADR-0008

ADR-0008 (narrative-skills-status-quo) and ADR-0009 (root-spec-no-consolidation) both apply a "**measure the friction, then act**" pattern to topology-amendment questions. The pair establishes a precedent for future architecture-review dispatches: substrate-level topology amendments require **falsifier-trigger evidence**, not just architectural-elegance arguments.

This pattern is intentionally *not* itself ratified as a separate ADR; it is left to emerge as practice. If a third or fourth ADR follows the same shape, a meta-ADR codifying the pattern may be warranted at that point.

## 8. Falsifiability check

The Goal's falsifiable outcome was: "a ratified ADR at `decisions/<NNNN>-root-spec-consolidation.md` recording either {merge-PRE_COMMIT-into-AGENTS + merge-FRUSTRATED-into-MAINTENANCE, partial-merge, status-quo} with measured token-cost data backing the choice."

Satisfied:

1. ADR landed at `decisions/0009-root-spec-no-consolidation.md` (the slug reflects the chosen outcome, not the rejected one — same convention as ADR-0008).
2. `adr_status: Proposed` per the task's permitted set.
3. The three options are all evaluated in §"Considered Options"; the chosen one (status quo) is named in §"Decision Outcome".
4. Measured token-cost data backs the decision: the 11-file table in §"Context and Problem Statement" provides the bundle baseline; the optimistic saving estimate in §"Decision Drivers" → "Measured token-cost saving" provides the upside; the rewrite-cost audit provides the downside.
5. No follow-on implementation Task is opened — justified in §6 above.
