# partials/

Concept docs for the 5 shared partials.

## What and why

Includes the design rationale for the ReAct-loop-anchored synthesis-table — the KEY INNOVATION that prevents method-drift in long agent runs.

## Contents

| Concept doc | Purpose | Module file |
|-------------|---------|-------------|
| [frontmatter-template.md](./frontmatter-template.md) | Canonical frontmatter shape every module file conforms to. | [⚙️ module](../../modules/partials/frontmatter-template.md) |
| [language-warning.md](./language-warning.md) | Prepended when intent.language != 'en' to warn that templates remain English-tagged. | [⚙️ module](../../modules/partials/language-warning.md) |
| [meta-header.md](./meta-header.md) | Header block prepended to every rendered research prompt. | [⚙️ module](../../modules/partials/meta-header.md) |
| [react-loop-anchored.md](./react-loop-anchored.md) | KEY INNOVATION — inline active-methods table inside the ReAct loop; anti-drift mechanism. | [⚙️ module](../../modules/partials/react-loop-anchored.md) |
| [synthesis-schema.md](./synthesis-schema.md) | Schema definition consumed by the synthesis-protocol framework. | [⚙️ module](../../modules/partials/synthesis-schema.md) |

## Assumptions

_(Document any implicit assumptions about how this folder is used —
file-naming conventions, slot-fill mechanisms, depth ordering, etc.
This block exists to prevent workflow drift; future agents inherit
the rationale instead of re-deriving it. If no assumptions apply,
state that explicitly.)_

- _none recorded yet_

---

_See also:_ [../../AGENTS.md](../../AGENTS.md) · [../../../AGENTS.md](../../../AGENTS.md)
