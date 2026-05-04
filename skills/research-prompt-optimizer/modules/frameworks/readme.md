# frameworks/

The 7 prompt-engineering frameworks (ReAct, RISEN, TIDD-EC, CO-STAR, CARE, CRISPE, plus a bespoke synthesis protocol).

## What and why

ReAct is the always-present agentic framework. Exactly one structural framework is selected per category by Phase 2; if ≥ 2 override-triggers fire, Phase 2 instead selects `synthesis.md` for bespoke composition (Q3 lenient · v1.1 spec).

## Contents

| Module file | Purpose | Concept doc |
|-------------|---------|-------------|
| [care.md](./care.md) | Context · Action · Result · Example — concise structural framework. | [📖 concept](../../docs/frameworks/care.md) |
| [co-star.md](./co-star.md) | Context · Objective · Style · Tone · Audience · Response — for audience-specific deliverables. | [📖 concept](../../docs/frameworks/co-star.md) |
| [crispe.md](./crispe.md) | Capacity · Role · Insight · Statement · Personality · Experiment — for exploratory research. | [📖 concept](../../docs/frameworks/crispe.md) |
| [react.md](./react.md) | Reasoning + Acting loop — the always-present agentic framework anchoring all method calls. | [📖 concept](../../docs/frameworks/react.md) |
| [risen.md](./risen.md) | Role · Input · Steps · Expectation · Narrowing — structural framework for well-bounded research. | [📖 concept](../../docs/frameworks/risen.md) |
| [synthesis.md](./synthesis.md) | Bespoke synthesis protocol — selected when ≥2 framework override-triggers fire (Q3 lenient · v1.1). | [📖 concept](../../docs/frameworks/synthesis.md) |
| [tidd-ec.md](./tidd-ec.md) | Task · Input · Decomposition · Domain · Examples · Constraints — for compositional decomposition. | [📖 concept](../../docs/frameworks/tidd-ec.md) |

## Assumptions

_(Document any implicit assumptions about how this folder is used —
file-naming conventions, slot-fill mechanisms, depth ordering, etc.
This block exists to prevent workflow drift; future agents inherit
the rationale instead of re-deriving it. If no assumptions apply,
state that explicitly.)_

- _none recorded yet_

---

_See also:_ [../../AGENTS.md](../../AGENTS.md) · [../../../AGENTS.md](../../../AGENTS.md)
