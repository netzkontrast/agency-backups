# Concept Template

> Copy this for every new module. Keep it tight — concept docs are
> reference material, not essays. Aim for 30–60 lines per module.

---

# `<module-id>` — `<full name>`

**File:** `modules/<type>/<filename>.md`
**Type:** category | method | framework | replication | cross-pollination | partial | verification
**Mandatory:** yes | no
**Self-applied in Phase 2:** yes (sub-phase X.Y, hook role: ...) | no

## Purpose

One paragraph. What does this module do for the rendered research prompt? Why does it exist?

## Slot inventory

Table of every slot defined in the module's frontmatter, plus any
[BRACKETS] in the body that are NOT slots (= structural markers).

| Slot name | Type | Filled by | Required | Notes |
|-----------|------|-----------|----------|-------|
| `slot_a` | `phase2_fill` | `intent.research_question` (truncate 100 chars) | yes | — |
| `slot_b` | `agent_runtime_fill` | agent during execution | no | runtime — not pre-filled |
| `slot_c` | `phase2_fill_or_runtime` | intent if available, else agent | no | hybrid |
| `slot_d` | `fill_from` | programmatic (Phase 3 render: `{{intent.title}}`) | yes | computed |

**Structural markers (NOT slots):**

- `[Reason 1]`, `[Reason 2]`, `[Reason N]` — iteration markers in
  ReAct loop; preserved in body, not converted to slots
- `[ITEM N]` — batch-iteration placeholder

## Body composition

Where does this module sit in the rendered research prompt?

- **Section anchor:** e.g., `### Method: <name>` (under §2 Methods),
  or `## Synthesis` (top-level)
- **Order constraint:** before X / after Y / standalone
- **Composition partner:** pairs with `<other module>` when ...

## Split decision

**Currently:** single file
**Should it split?** No — reasons: ...
**OR:** Yes — into:
  - `<file-1>.md` — covers the X aspect
  - `<file-2>.md` — covers the Y aspect
  Trigger for split: when ... (specific condition)

## Future extension points

What COULD be added without breaking the current design? Ideas
parked for later:

1. **Extension idea 1** — what it'd add, where it'd live (new slot?
   new partial? sibling module?)
2. **Extension idea 2** — ...

## Open questions

Any unresolved design questions for this specific module:

- [ ] Question 1 — context, options
- [ ] Question 2 — ...

## Catalog cross-reference

- Catalog entry: `catalog.yaml` under `modules.<id>` (or `categories.<id>` for categories)
- Triggered by signals: `<list>` (or `n/a`)
- Default for category: `<A | B | C | none>`
- Self-applied hook (if yes): see `catalog.yaml` → `modules.<id>.self_applied_phase2`

## Change log

- `YYYY-MM-DD` (vX.Y): initial concept doc, captured during template-fix sweep.
