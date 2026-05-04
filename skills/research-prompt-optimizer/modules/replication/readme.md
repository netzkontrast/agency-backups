# replication/

The 5 replication mechanisms (M0 Reflection, M1 Constraint Blocks, M2 Restatement Checkpoint, M3 Batch, M4 Pre-Synthesis).

## What and why

These structural mechanisms appear in every rendered research prompt regardless of category. M3 Batch is conditional — included only when Phase 2 detects batchable items. M0 and M4 are also self-applied during Phase 2 planning.

## Contents

| Module file | Purpose | Concept doc |
|-------------|---------|-------------|
| [m0-reflection.md](./m0-reflection.md) | Mid-loop reflection mechanism — 5-question full or 2-question mini variant. | [📖 concept](../../docs/replication/m0-reflection.md) |
| [m1-constraint-blocks.md](./m1-constraint-blocks.md) | Explicit constraint blocks (Source Priority, Temporal, Output Exclusions, etc.) governing the whole prompt. | [📖 concept](../../docs/replication/m1-constraint-blocks.md) |
| [m2-restatement-checkpoint.md](./m2-restatement-checkpoint.md) | Forces the agent to restate the research question in its own words before proceeding. | [📖 concept](../../docs/replication/m2-restatement-checkpoint.md) |
| [m3-batch.md](./m3-batch.md) | Batch-iteration mechanism — present when Phase 2 detects batchable items. | [📖 concept](../../docs/replication/m3-batch.md) |
| [m4-pre-synthesis.md](./m4-pre-synthesis.md) | 6-item integrity check that runs before final synthesis. | [📖 concept](../../docs/replication/m4-pre-synthesis.md) |

## Assumptions

_(Document any implicit assumptions about how this folder is used —
file-naming conventions, slot-fill mechanisms, depth ordering, etc.
This block exists to prevent workflow drift; future agents inherit
the rationale instead of re-deriving it. If no assumptions apply,
state that explicitly.)_

- _none recorded yet_

---

_See also:_ [../../AGENTS.md](../../AGENTS.md) · [../../../AGENTS.md](../../../AGENTS.md)
