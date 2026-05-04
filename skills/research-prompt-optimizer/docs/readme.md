# docs/

Per-module concept documentation. Background, design rationale, and worked usage notes for each module.

## What and why

Mirrors the structure of [`modules/`](../modules/) — one subfolder per
module type. These files explain the *why* behind each module's
design (slot provenance, split decisions, future extension points,
open questions). They are not consumed by the renderer or by Phase 2
logic, only by humans and agents trying to understand or extend the
catalog.

**Navigation pairing:** every concept doc here has a 1:1 partner in
[`modules/`](../modules/). The folder readmes on both sides
cross-link, so you can jump from a module file to its concept doc
(📖 concept) and back (⚙️ module).

## Master docs (top-level)

| File | Purpose |
|------|---------|
| [_README.md](./_README.md) | Original docs-tree overview and reading order |
| [_CONCEPT-TEMPLATE.md](./_CONCEPT-TEMPLATE.md) | Canonical structure every per-module concept doc follows |
| [_BRACKET-INVENTORY.md](./_BRACKET-INVENTORY.md) | Classification of every `[BRACKET]` in module bodies (structural / method-anchor / true-variable) |
| [_SLOT-PROVENANCE-MAP.md](./_SLOT-PROVENANCE-MAP.md) | Cross-module map: which intent fields fill which slots |

## Contents

| Entry | Kind | Purpose |
|-------|------|---------|
| [categories/](./categories/) | folder | Concept docs for the 3 routing categories (A/B/C) |
| [cross-pollination/](./cross-pollination/) | folder | Concept docs for the 6 cross-pollination blocks |
| [frameworks/](./frameworks/) | folder | Concept docs for the 7 prompt-engineering frameworks |
| [methods/](./methods/) | folder | Concept docs for the 13 critical-thinking methods (M01–M13) |
| [partials/](./partials/) | folder | Concept docs for the 5 shared partials |
| [replication/](./replication/) | folder | Concept docs for the 5 replication mechanisms (m0–m4) |
| [verification/](./verification/) | folder | Concept doc for the final-checklist module |


## Assumptions

_(Document any implicit assumptions about how this folder is used —
file-naming conventions, slot-fill mechanisms, depth ordering, etc.
This block exists to prevent workflow drift; future agents inherit
the rationale instead of re-deriving it. If no assumptions apply,
state that explicitly.)_

- _none recorded yet_

---

_See also:_ [../AGENTS.md](../AGENTS.md) · [../../AGENTS.md](../../AGENTS.md)
