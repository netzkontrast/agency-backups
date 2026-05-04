# modules/

Skill internals — all building-block modules consumed by Phase 2 (selection) and Phase 3 (rendering).

## What and why

Each subfolder holds modules of one type. Phase 2 selects from these
via [`catalog.yaml`](../catalog.yaml); Phase 3 renders the selected
ones into the final research prompt. Files here are loaded lazily —
never edited by Phase 1, never seen by the eagerly-loaded
[`SKILL.md`](../SKILL.md) router.

**Navigation pairing:** every module file here has a 1:1 partner in
[`docs/`](../docs/) — the concept doc explains design rationale,
slot provenance, split decisions, and known extension points. The
folder readmes on both sides cross-link via 📖 concept and ⚙️ module
columns.

## Contents

| Entry | Kind | Purpose |
|-------|------|---------|
| [categories/](./categories/) | folder | 3 category routing files (A-exploration, B-extraction, C-lifecycle) |
| [cross-pollination/](./cross-pollination/) | folder | 6 pairwise cross-pollination blocks (A↔B, A↔C, B↔C) |
| [frameworks/](./frameworks/) | folder | 7 prompt-engineering frameworks (ReAct + 6 structural) |
| [methods/](./methods/) | folder | 13 critical-thinking methods (M01–M13) |
| [partials/](./partials/) | folder | 5 shared partials including ReAct-loop-anchored (KEY INNOVATION) |
| [replication/](./replication/) | folder | 5 replication mechanisms (m0–m4) |
| [verification/](./verification/) | folder | The final-checklist module |


## Assumptions

_(Document any implicit assumptions about how this folder is used —
file-naming conventions, slot-fill mechanisms, depth ordering, etc.
This block exists to prevent workflow drift; future agents inherit
the rationale instead of re-deriving it. If no assumptions apply,
state that explicitly.)_

- _none recorded yet_

---

_See also:_ [../AGENTS.md](../AGENTS.md) · [../../AGENTS.md](../../AGENTS.md)
