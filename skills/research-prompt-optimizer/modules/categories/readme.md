# categories/

The 3 routing files for the A/B/C category system: A-exploration, B-extraction, C-lifecycle.

## What and why

These files are read at Phase-2 entry to determine routing. Each declares its `signal_words`, `default_methods`, `default_framework_structural`, and `cross_pollination_pair`. Tie or no signal triggers a 3-option askuser at Phase 2.2.

## Contents

| Module file | Purpose | Concept doc |
|-------------|---------|-------------|
| [a-exploration.md](./a-exploration.md) | Cat-A: open exploration. Signal words include 'explore', 'investigate', 'survey'. ReAct + RISEN default. | [📖 concept](../../docs/categories/a-exploration.md) |
| [b-extraction.md](./b-extraction.md) | Cat-B: structured extraction. Signal words include 'compare', 'list', 'extract'. ReAct + TIDD-EC default. | [📖 concept](../../docs/categories/b-extraction.md) |
| [c-lifecycle.md](./c-lifecycle.md) | Cat-C: lifecycle / process research. Signal words include 'monitor', 'track', 'evolution'. ReAct + CO-STAR default. | [📖 concept](../../docs/categories/c-lifecycle.md) |

## Assumptions

_(Document any implicit assumptions about how this folder is used —
file-naming conventions, slot-fill mechanisms, depth ordering, etc.
This block exists to prevent workflow drift; future agents inherit
the rationale instead of re-deriving it. If no assumptions apply,
state that explicitly.)_

- _none recorded yet_

---

_See also:_ [../../AGENTS.md](../../AGENTS.md) · [../../../AGENTS.md](../../../AGENTS.md)
