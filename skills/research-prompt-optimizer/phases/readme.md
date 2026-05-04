# phases/

Detail-level specs for each pipeline phase. Loaded lazily by the SKILL.md router only when an edge case forces it.

## What and why

Files here are intentionally verbose — they hold worked examples, contradiction-resolution patterns, sub-enum dispatch tables, and the full slot-resolution semantics. The thin `SKILL.md` summarizes the algorithm; these files are the source of truth for behaviour at the boundary.

## Contents

| Entry | Kind | Purpose |
|-------|------|---------|
| [phase1-intent-capture.md](./phase1-intent-capture.md) | file | Edge-case spec for Phase 1 — worked examples, contradiction-resolution patterns, slot-to-question mapping |
| [phase2-planning.md](./phase2-planning.md) | file | Edge-case spec for Phase 2 — decision-tree detail, override-trigger logic, sub-enum dispatch, §12 self-applied critical thinking |
| [phase3-render.md](./phase3-render.md) | file | Renderer implementation detail — slot-resolution semantics, fill_from handler registry, Schema-3 assembly order |


## Assumptions

_(Document any implicit assumptions about how this folder is used —
file-naming conventions, slot-fill mechanisms, depth ordering, etc.
This block exists to prevent workflow drift; future agents inherit
the rationale instead of re-deriving it. If no assumptions apply,
state that explicitly.)_

- _none recorded yet_

---

_See also:_ [../AGENTS.md](../AGENTS.md) · [../../AGENTS.md](../../AGENTS.md)
