# `synthesis` (catalog id: `bespoke`) — Bespoke Synthesis Framework

**File:** `modules/frameworks/synthesis.md`
**Type:** framework (structural — composite)
**Mandatory:** no — selected when Q3-lenient trigger fires (≥2 catalog framework override_triggers fire simultaneously)
**Self-applied in Phase 2:** no

## Purpose

When NO single catalog framework (RISEN, TIDD-EC, CO-STAR, CARE, CRISPE) cleanly fits the intent's structural needs, Phase 2 composes a **bespoke synthesis framework** by picking the strongest components from multiple catalog frameworks and assembling a custom acronym.

The Q3 v1.1 lenient threshold (≥2 override_triggers) intentionally errs toward bespoke because forcing a single catalog framework on a multi-demand intent is a silent failure mode worth preventing.

The body of this module is the **template** for the rendered bespoke framework block: it shows the bespoke acronym, the components, and the provenance (which catalog framework each letter came from).

## Slot inventory

| Slot name | Type | Filled by | Required | Notes |
|-----------|------|-----------|----------|-------|
| `bespoke_acronym` | `phase2_fill` | Phase 2 sub-phase 4.3 — Claude generates from selected components | yes | New acronym name (e.g., "T-RICE", "RISER", etc.) |
| `components` | `phase2_fill` | Phase 2 sub-phase 4.3 — Claude generates as structured list | yes | List of `{letter, name, definition, source_framework}` objects |
| `components_render_block` | `fill_from` (programmatic) | Phase 3 render — emits one Markdown bullet per component from `components` slot | yes | `- **<letter> — <name>**: <definition>` per component |
| `provenance_render_block` | `fill_from` (programmatic) | Phase 3 render — emits provenance line per component | yes | `- Component <letter> is adapted from the <source_framework> framework.` per component |
| `first_action_directive` | `phase2_fill` | Phase 2 — Claude generates from `intent.research_question` | yes | One-line directive setting the agent's first action under the bespoke framework |

**Structural markers (NOT slots):**

- `[CATALOG FRAMEWORK NAME]` — appears in instructional prose about handoff behavior. The agent at runtime fills with whichever catalog framework they're handing off to. Pedagogical example, not a slot. Stays.
- `[Name]`, `[LETTER 1]` etc. — also pedagogical examples in body prose.

## Body composition — special Phase-3 semantics

This is the **most complex framework** because Phase 3 must render two iteration blocks (`components_render_block` and `provenance_render_block`) from a single source list (`components`).

### Phase-3 render pseudocode

```python
# Read slot content
acronym = meta_prompt["framework_structural_state"]["bespoke_acronym"]
components = meta_prompt["framework_structural_state"]["components"]  # list of dicts
first_action = meta_prompt["framework_structural_state"]["first_action_directive"]

# Render the components bullet block
components_block = ""
for c in components:
    components_block += f"- **{c['letter']} — {c['name']}**: {c['definition']}\n"

# Render the provenance lines block
provenance_block = "**Provenance** (which catalog framework each component came from):\n"
for c in components:
    provenance_block += f"- Component {c['letter']} is adapted from the {c['source_framework']} framework.\n"

# Substitute slots in body template
body = template.format(
    bespoke_acronym=acronym,
    components_render_block=components_block,
    provenance_render_block=provenance_block,
    first_action_directive=first_action,
    # 'components' slot is NOT directly substituted — it's the source for the two render blocks above
)
```

The `components` slot is **structured data**, not a string — it lives in the meta-prompt as a list. Phase 3 derives the two render blocks from it.

## Body composition — placement

- **Section anchor:** `## Structural Framework — Bespoke Synthesis ({{bespoke_acronym}})`
- **Order constraint:** same as other structural frameworks — after Epistemological Layer, before methods.
- **Composition partner:** ReAct (always paired). The bespoke framework SHAPES the output; ReAct DRIVES the loop.

## Split decision

**Currently:** single file with companion partial `partials/synthesis-schema.md`
**Should it split?** Already split — main file has the framework-as-rendered template; partial has the meta-schema (component object structure) used by Phase 2 to GENERATE the components list.

## Future extension points

1. **Component library** — currently bespoke synthesis pulls from the 5 catalog frameworks. Could expand the source pool to include external frameworks (BAB, BLUF, etc.) via a `bespoke_source_pool` slot listing eligible source frameworks.
2. **Acronym-quality validation** — bespoke acronyms should be pronounceable and memorable. Add Phase-3 check: if the generated acronym fails (all-consonants, > 7 letters), regenerate.
3. **Bespoke-of-bespoke prevention** — if a bespoke acronym is once generated for a given intent type, future similar intents could reuse it. Would need a `bespoke_acronym_registry.yaml` catalog. Premature for now.

## Open questions

- [ ] The `components` slot is `phase2_fill` but the catalog only documents 2 slots (acronym + components). The 3 derived slots (`components_render_block`, `provenance_render_block`, `first_action_directive`) are in the module's frontmatter but missing from `catalog.yaml` → `modules.bespoke.slots`. **Catalog-frontmatter sync needed** in next polish pass.
- [ ] How should Phase 2 handle the case where `first_action_directive` cannot be cleanly generated? Currently no fallback. Add `default_first_action_directive` constant for that case.

## Catalog cross-reference

- Catalog entry: `catalog.yaml` → `modules.bespoke` (note: catalog id is `bespoke`, file is `synthesis.md`)
- Triggered by: Q3-lenient logic (≥2 override_triggers fire simultaneously)
- Default for category: never default — only via Q3-lenient trigger
- Self-applied hook: no

## Change log

- `2026-05-02` (v3.0-phase2): initial concept doc; body unchanged. Confirmed `[CATALOG FRAMEWORK NAME]`, `[Name]`, `[LETTER 1]` etc. are structural pedagogy, not slots. Catalog-frontmatter sync flagged as open issue.
