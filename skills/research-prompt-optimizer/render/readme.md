# render/

Phase 3 implementation. Single-file Python renderer (pure stdlib + pyyaml).

## What and why

`render.py` is invoked after Phase 2 approval: it reads the meta-prompt YAML, resolves the four slot types, composes Schema-3-ordered Markdown, and writes the final research prompt. `phases/phase3-render.md` documents the slot-resolution semantics and the fill_from handler registry.

## Contents

| Entry | Kind | Purpose |
|-------|------|---------|
| [render.py](./render.py) | file | Phase-3 renderer entry-point — reads meta-prompt YAML, resolves slots, composes Schema-3 Markdown, writes research-prompt.md |


## Assumptions

_(Document any implicit assumptions about how this folder is used —
file-naming conventions, slot-fill mechanisms, depth ordering, etc.
This block exists to prevent workflow drift; future agents inherit
the rationale instead of re-deriving it. If no assumptions apply,
state that explicitly.)_

- _none recorded yet_

---

_See also:_ [../AGENTS.md](../AGENTS.md) · [../../AGENTS.md](../../AGENTS.md)
