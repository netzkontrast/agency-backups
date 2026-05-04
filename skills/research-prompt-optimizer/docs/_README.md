# docs/ — Module Concept Library

This directory holds one concept document per module in
`/modules/`. Concept docs are the **future-extension surface**: they
record the design decisions, slot inventory, fill provenance, split
decisions, and known extension points for each module.

## Why concept docs exist

Module files (`/modules/.../*.md`) carry:
- **Frontmatter:** machine-readable slot defs, hooks, depth flags
- **Body:** the rendered template that ships into research prompts

Concept docs (`/docs/.../*.md`) carry:
- **Why** the module is structured this way
- **What** the slots represent and where they get filled from
- **How** the module composes with others
- **When** to split it into multiple files
- **Where** future extensions should land

When someone (Michael, future-Claude, a contributor) wants to extend
a module, they read the concept doc first. The concept doc tells them
whether the extension belongs as a new slot, a sibling module, a
partial, a frontmatter flag, or a body restructure.

## Directory structure

```
docs/
├── _README.md                  ← this file
├── _CONCEPT-TEMPLATE.md        ← canonical structure for every module concept doc
├── _BRACKET-INVENTORY.md       ← discovery output: where brackets live and what kind they are
├── _SLOT-PROVENANCE-MAP.md     ← cross-module map: which intent fields fill which slots
├── categories/
│   ├── a-exploration.md
│   ├── b-extraction.md
│   └── c-lifecycle.md
├── methods/
│   ├── m01-falsification.md
│   ├── m02-steelmanning.md
│   ├── ... (m03–m13)
├── frameworks/
│   ├── react.md
│   ├── risen.md
│   ├── tidd-ec.md
│   ├── co-star.md
│   ├── care.md
│   ├── crispe.md
│   └── synthesis.md
├── replication/
│   ├── m0-reflection.md
│   ├── m1-constraint-blocks.md
│   ├── m2-restatement-checkpoint.md
│   ├── m3-batch.md
│   └── m4-pre-synthesis.md
├── cross-pollination/
│   ├── a-into-b.md
│   ├── ... (5 more pairings)
├── partials/
│   ├── react-loop-anchored.md
│   ├── frontmatter-template.md
│   ├── meta-header.md
│   ├── language-warning.md
│   └── synthesis-schema.md
└── verification/
    └── final-checklist.md
```

## How to use

1. **Reading order for a single module:** start at the module's
   concept doc, then read the actual module file in `/modules/`.
2. **Reading order for the system:** `_BRACKET-INVENTORY.md` →
   `_SLOT-PROVENANCE-MAP.md` → individual concept docs as needed.
3. **Editing a module:** read concept doc, decide if change fits
   inside current structure or requires a split / new module / new
   partial. Update both module file AND concept doc.
4. **Adding a new module:** copy `_CONCEPT-TEMPLATE.md`, fill in,
   then add module file under `/modules/`, then add catalog entry.
