# examples/

Worked YAML outputs for each phase, used as fixtures by the renderer smoke test.

## What and why

`example-intent.yaml` shows a complete approved Phase-1 output. `example-meta-prompt.yaml` shows the corresponding Phase-2 output (EU-AI-Act-Compliance case). Both must conform to their schemas in `meta-prompt-spec.md` and round-trip cleanly through `render.py`.

## Contents

| Entry | Kind | Purpose |
|-------|------|---------|
| [example-intent.yaml](./example-intent.yaml) | file | Worked Phase-1 output — complete approved intent.yaml for the EU-AI-Act-Compliance test case |
| [example-meta-prompt.yaml](./example-meta-prompt.yaml) | file | Worked Phase-2 output — corresponding meta-prompt.yaml with full self_reflection block, used as the renderer smoke-test fixture |


## Assumptions

_(Document any implicit assumptions about how this folder is used —
file-naming conventions, slot-fill mechanisms, depth ordering, etc.
This block exists to prevent workflow drift; future agents inherit
the rationale instead of re-deriving it. If no assumptions apply,
state that explicitly.)_

- _none recorded yet_

---

_See also:_ [../AGENTS.md](../AGENTS.md) · [../../AGENTS.md](../../AGENTS.md)
