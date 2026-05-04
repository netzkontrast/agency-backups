# `care` — CARE Framework (Context, Action, Result, Examples)

**File:** `modules/frameworks/care.md`
**Type:** framework (structural)
**Mandatory:** no (optional structural framework, picked when override triggers fire)
**Self-applied in Phase 2:** no

## Purpose

CARE is a structural framework that organizes the agent's research output into four sections: Context, Action, Result, Examples. Best fit for cases where the research must produce a self-contained recommendation document for a specific stakeholder — the framing is action-oriented and stakeholder-driven.

## Slot inventory

| Slot name | Type | Filled by | Required | Notes |
|-----------|------|-----------|----------|-------|
| (none) | — | — | — | Frontmatter: `slots: {}` — body is pure schema |

The body lays out the four-section schema as instruction text. No template variables — the agent reading the rendered prompt fills the four sections during execution.

**Structural markers:** none.

## Body composition

- **Section anchor:** `## Structural Framework — CARE`
- **Order constraint:** appears after the Epistemological Layer (category block) and before any methods. Structural framework sets the OUTPUT skeleton.
- **Composition partner:** ReAct (always paired — every prompt has both a structural framework and ReAct as agentic loop).

## Split decision

**Currently:** single file
**Should it split?** No — CARE is a tightly coupled four-section format. Splitting would lose the C → A → R → E sequence.

## Future extension points

1. **Stakeholder-specific Context block** — add slot `target_stakeholder` (`phase2_fill` from `intent.audience` field, when added to Phase-1 schema) to pre-fill the C section's framing.
2. **Examples-section size guidance** — currently free-form. Could add slot `examples_min_count` (default 2) for cases where breadth of examples matters.

## Open questions

- [ ] Should CARE have explicit override_triggers in catalog? Currently it's a category-default for some categories (TBD which); explicit triggers would let it override defaults from other categories.

## Catalog cross-reference

- Catalog entry: `catalog.yaml` → `modules.care`
- Triggered by signals: (see catalog override_trigger field)
- Default for category: see `categories.<X>.default_framework_structural` in catalog
- Self-applied hook: no

## Change log

- `2026-05-02` (v3.0-phase2): initial concept doc; body unchanged (zero brackets).
