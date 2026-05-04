# replication/

Concept docs for the 5 replication mechanisms.

## What and why

Covers why each replication mechanism is mandatory (or conditional, in M3's case), and how it interacts with the ReAct loop in `partials/react-loop-anchored.md`.

## Contents

| Concept doc | Purpose | Module file |
|-------------|---------|-------------|
| [m0-reflection.md](./m0-reflection.md) | Mid-loop reflection mechanism — 5-question full or 2-question mini variant. | [⚙️ module](../../modules/replication/m0-reflection.md) |
| [m1-constraint-blocks.md](./m1-constraint-blocks.md) | Explicit constraint blocks (Source Priority, Temporal, Output Exclusions, etc.) governing the whole prompt. | [⚙️ module](../../modules/replication/m1-constraint-blocks.md) |
| [m2-restatement-checkpoint.md](./m2-restatement-checkpoint.md) | Forces the agent to restate the research question in its own words before proceeding. | [⚙️ module](../../modules/replication/m2-restatement-checkpoint.md) |
| [m3-batch.md](./m3-batch.md) | Batch-iteration mechanism — present when Phase 2 detects batchable items. | [⚙️ module](../../modules/replication/m3-batch.md) |
| [m4-pre-synthesis.md](./m4-pre-synthesis.md) | 6-item integrity check that runs before final synthesis. | [⚙️ module](../../modules/replication/m4-pre-synthesis.md) |

## Assumptions

_(Document any implicit assumptions about how this folder is used —
file-naming conventions, slot-fill mechanisms, depth ordering, etc.
This block exists to prevent workflow drift; future agents inherit
the rationale instead of re-deriving it. If no assumptions apply,
state that explicitly.)_

- _none recorded yet_

---

_See also:_ [../../AGENTS.md](../../AGENTS.md) · [../../../AGENTS.md](../../../AGENTS.md)
