# Notes — Task 007 (Reconcile Closed-Task Linkage Drift)

## Strategy Decision (2026-05-04)

**Chosen: Strategy A (Re-open and finish) + Strategy C (Path-resolution fix).**

Rejected:

- **Strategy B (Schema extension — `task_spawns_prompts`)** — would solve the
  prompt-vs-research conflation by adding a new L2 key, but introduces a
  schema change for two closed tasks. The spawned-prompts relationship is
  already captured naturally by each follow-up prompt's
  `prompt_spawned_from_research` back-link. Adding a forward `task_spawns_prompts`
  field would be redundant linkage with the same maintenance cost as adding
  reciprocity to `task_uses_prompts`.
- **Strategy D (Mark stale prompts as archived)** — the five follow-up prompts
  are not stale; they capture genuine open questions surfaced by tasks 002
  and 003 that should remain executable when an agent picks them up. Archiving
  would discard signal.

## What Was Applied

1. **Friction logs** (Strategy A) — both missing files authored adjacent to
   their tasks, each with an FL[0-3] declaration per FRUSTRATED.md.
2. **Task 003's `task_spawns_research`** (Strategy A) — emptied. The three
   listed slugs were follow-up *prompts*, not research workspaces.
   Scaffolding empty workspaces would violate FOLDERS.md §4 ("No Empty
   Scaffolding").
3. **`prompt_relates_to_task` reciprocity** (Strategy A + spec clarification)
   — removed the field from all five follow-up prompts. The clarification
   in PROMPT.md §6.6 now states that the field encodes a *uses* relationship
   requiring reciprocity, and that follow-up prompts not yet adopted by any
   Task MUST omit it. Lineage survives via `prompt_spawned_from_research`.
4. **Provider-subfolder research resolution** (Strategy C) — extended
   `tools/lint-linkage.py` with `research_slug_resolves()` which walks both
   `/research/<slug>/` and `/research/<provider>/<slug>/`. PROMPT.md §6.5
   updated to make this explicit.

## Verification

`bash tools/check-governance.sh` exits 0 with all four linters reporting zero
diagnostics (was 15 errors when this task was filed).

## Closing PR

This task was closed by the same PR that delivered the fix:
[`fix(governance): restore green check-governance + clarify spec semantics`](https://github.com/netzkontrast/agency/pull/27).
