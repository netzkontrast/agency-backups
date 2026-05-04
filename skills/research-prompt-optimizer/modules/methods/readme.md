# methods/

The 13 critical-thinking methods (M01–M13) the rendered research prompt instructs the external agent to apply.

## What and why

Each method file is one block of executable instruction copy: what the method is, when to apply it during research, and what slots it exposes for Phase-2 fill-in. Four of these methods (M01, M03, M05, M07) are also self-applied during Phase 2 planning — see `catalog.yaml` → `self_applied_phase2_index`.

## Contents

| Module file | Purpose | Concept doc |
|-------------|---------|-------------|
| [m01-falsification.md](./m01-falsification.md) | Force the agent to actively try to disprove the current top hypothesis (Popper's disconfirmation principle). | [📖 concept](../../docs/methods/m01-falsification.md) |
| [m02-steelmanning.md](./m02-steelmanning.md) | Build the strongest possible version of the opposing position before critiquing it. | [📖 concept](../../docs/methods/m02-steelmanning.md) |
| [m03-pre-mortem.md](./m03-pre-mortem.md) | Imagine the research has already failed; reason backward to the most likely failure modes. | [📖 concept](../../docs/methods/m03-pre-mortem.md) |
| [m04-contrast-classes.md](./m04-contrast-classes.md) | Sharpen claims by asking 'compared to what?' — surface the implicit reference class. | [📖 concept](../../docs/methods/m04-contrast-classes.md) |
| [m05-bayesian-prior.md](./m05-bayesian-prior.md) | Make the prior belief explicit before evidence collection; track update direction & magnitude. | [📖 concept](../../docs/methods/m05-bayesian-prior.md) |
| [m06-source-triangulation.md](./m06-source-triangulation.md) | Require ≥3 orthogonal source types per major claim before treating it as established. | [📖 concept](../../docs/methods/m06-source-triangulation.md) |
| [m07-contradiction-log.md](./m07-contradiction-log.md) | Maintain an explicit log of contradictions surfaced; resolve before final synthesis. | [📖 concept](../../docs/methods/m07-contradiction-log.md) |
| [m08-what-would-change-my-mind.md](./m08-what-would-change-my-mind.md) | Pre-commit to specific evidence thresholds that would force position-revision. | [📖 concept](../../docs/methods/m08-what-would-change-my-mind.md) |
| [m09-red-team.md](./m09-red-team.md) | Adversarial pass: an imagined critic with the strongest case against the conclusion. | [📖 concept](../../docs/methods/m09-red-team.md) |
| [m10-first-principles.md](./m10-first-principles.md) | Decompose to ground truths before re-composing; bypass borrowed assumptions. | [📖 concept](../../docs/methods/m10-first-principles.md) |
| [m11-assumption-decay.md](./m11-assumption-decay.md) | Surface assumptions, classify by half-life, flag those near expiry for re-validation. | [📖 concept](../../docs/methods/m11-assumption-decay.md) |
| [m12-base-rate.md](./m12-base-rate.md) | Anchor probability claims to the relevant reference-class base rate before adjusting. | [📖 concept](../../docs/methods/m12-base-rate.md) |
| [m13-adversarial-query-expansion.md](./m13-adversarial-query-expansion.md) | Generate 4 axes of orthogonal query expansion (adjacent / opposing / abstraction / domain-shift). | [📖 concept](../../docs/methods/m13-adversarial-query-expansion.md) |

## Assumptions

_(Document any implicit assumptions about how this folder is used —
file-naming conventions, slot-fill mechanisms, depth ordering, etc.
This block exists to prevent workflow drift; future agents inherit
the rationale instead of re-deriving it. If no assumptions apply,
state that explicitly.)_

- _none recorded yet_

---

_See also:_ [../../AGENTS.md](../../AGENTS.md) · [../../../AGENTS.md](../../../AGENTS.md)
