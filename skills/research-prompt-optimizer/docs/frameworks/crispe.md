# `crispe` — CRISPE Framework (Capacity, Role, Insight, Statement, Personality, Experiment)

**File:** `modules/frameworks/crispe.md`
**Type:** framework (structural)
**Mandatory:** no (optional structural framework)
**Self-applied in Phase 2:** no

## Purpose

CRISPE is a structural framework whose distinguishing feature is the **Experiment** axis — it organizes research around explicit experimental variants of the question, not just a single linear answer. Best fit when the research benefits from multiple framings of the same question being explored in parallel (Cat-A exploration, multi-hypothesis cases).

The Capacity / Role / Personality fields together form a richer agent-persona than most other structural frameworks.

## Slot inventory

| Slot name | Type | Filled by | Required | Notes |
|-----------|------|-----------|----------|-------|
| `experiment_axis_count` | `phase2_fill` | Phase 2 from `intent.exploration_breadth` if present, else default 3 | yes | Number of experimental variants the agent must produce |

**Structural markers:** none.

## Body composition

- **Section anchor:** `## Structural Framework — CRISPE`
- **Order constraint:** after Epistemological Layer, before methods.
- **Composition partner:** ReAct (always paired). Pairs naturally with Category A (Exploration) because both push for breadth over single-answer commitment.

## Split decision

**Currently:** single file
**Should it split?** No — the six axes form a unified persona+experiment structure.

## Future extension points

1. **Experiment-axis taxonomy** — currently free-form variants. Could constrain via slot `experiment_axis_taxonomy` (e.g., `divergent` / `convergent` / `lateral`) for systematic coverage.
2. **Per-experiment success criterion** — each experimental variant could carry its own success criterion. Add slot `experiment_success_criteria[]` for stricter falsifiability per variant.

## Open questions

- [ ] `experiment_axis_count` default of 3 is a guess. First Cat-A intents using CRISPE will calibrate.
- [ ] Should CRISPE be the default framework for Cat-A instead of RISEN? RISEN is currently default; CRISPE is arguably better-fit for exploration. Defer to Real-Use feedback.

## Catalog cross-reference

- Catalog entry: `catalog.yaml` → `modules.crispe`
- Triggered by signals: (see catalog override_trigger)
- Default for category: see `categories.<X>.default_framework_structural`
- Self-applied hook: no

## Change log

- `2026-05-02` (v3.0-phase2): initial concept doc; body unchanged (zero brackets).
