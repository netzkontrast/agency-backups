# partials/

The 5 shared partials used across multiple module types.

## What and why

Includes the ReAct-loop-anchored synthesis-table (KEY INNOVATION — anti-drift mechanism), the language-warning prepended when `intent.language != "en"`, the synthesis-schema, the meta-header, and the frontmatter template.

## Contents

| Module file | Purpose | Concept doc |
|-------------|---------|-------------|
| [frontmatter-template.md](./frontmatter-template.md) | Canonical frontmatter shape every module file conforms to. | [📖 concept](../../docs/partials/frontmatter-template.md) |
| [language-warning.md](./language-warning.md) | Prepended when intent.language != 'en' to warn that templates remain English-tagged. | [📖 concept](../../docs/partials/language-warning.md) |
| [meta-header.md](./meta-header.md) | Header block prepended to every rendered research prompt. | [📖 concept](../../docs/partials/meta-header.md) |
| [react-loop-anchored.md](./react-loop-anchored.md) | KEY INNOVATION — inline active-methods table inside the ReAct loop; anti-drift mechanism. | [📖 concept](../../docs/partials/react-loop-anchored.md) |
| [synthesis-schema.md](./synthesis-schema.md) | Schema definition consumed by the synthesis-protocol framework. | [📖 concept](../../docs/partials/synthesis-schema.md) |

## Assumptions

_(Document any implicit assumptions about how this folder is used —
file-naming conventions, slot-fill mechanisms, depth ordering, etc.
This block exists to prevent workflow drift; future agents inherit
the rationale instead of re-deriving it. If no assumptions apply,
state that explicitly.)_

- _none recorded yet_

---

_See also:_ [../../AGENTS.md](../../AGENTS.md) · [../../../AGENTS.md](../../../AGENTS.md)
