# methods/

Concept docs for the 13 methods. One file per method, mirroring `modules/methods/`.

## What and why

Each concept doc explains where the method comes from (literature, prior art, in-house experiment), what it costs to execute, and what failure modes it has.

## Contents

| Concept doc | Purpose | Module file |
|-------------|---------|-------------|
| [m01-falsification.md](./m01-falsification.md) | Force the agent to actively try to disprove the current top hypothesis (Popper's disconfirmation principle). | [⚙️ module](../../modules/methods/m01-falsification.md) |
| [m02-steelmanning.md](./m02-steelmanning.md) | Build the strongest possible version of the opposing position before critiquing it. | [⚙️ module](../../modules/methods/m02-steelmanning.md) |
| [m03-pre-mortem.md](./m03-pre-mortem.md) | Imagine the research has already failed; reason backward to the most likely failure modes. | [⚙️ module](../../modules/methods/m03-pre-mortem.md) |
| [m04-contrast-classes.md](./m04-contrast-classes.md) | Sharpen claims by asking 'compared to what?' — surface the implicit reference class. | [⚙️ module](../../modules/methods/m04-contrast-classes.md) |
| [m05-bayesian-prior.md](./m05-bayesian-prior.md) | Make the prior belief explicit before evidence collection; track update direction & magnitude. | [⚙️ module](../../modules/methods/m05-bayesian-prior.md) |
| [m06-source-triangulation.md](./m06-source-triangulation.md) | Require ≥3 orthogonal source types per major claim before treating it as established. | [⚙️ module](../../modules/methods/m06-source-triangulation.md) |
| [m07-contradiction-log.md](./m07-contradiction-log.md) | Maintain an explicit log of contradictions surfaced; resolve before final synthesis. | [⚙️ module](../../modules/methods/m07-contradiction-log.md) |
| [m08-what-would-change-my-mind.md](./m08-what-would-change-my-mind.md) | Pre-commit to specific evidence thresholds that would force position-revision. | [⚙️ module](../../modules/methods/m08-what-would-change-my-mind.md) |
| [m09-red-team.md](./m09-red-team.md) | Adversarial pass: an imagined critic with the strongest case against the conclusion. | [⚙️ module](../../modules/methods/m09-red-team.md) |
| [m10-first-principles.md](./m10-first-principles.md) | Decompose to ground truths before re-composing; bypass borrowed assumptions. | [⚙️ module](../../modules/methods/m10-first-principles.md) |
| [m11-assumption-decay.md](./m11-assumption-decay.md) | Surface assumptions, classify by half-life, flag those near expiry for re-validation. | [⚙️ module](../../modules/methods/m11-assumption-decay.md) |
| [m12-base-rate.md](./m12-base-rate.md) | Anchor probability claims to the relevant reference-class base rate before adjusting. | [⚙️ module](../../modules/methods/m12-base-rate.md) |
| [m13-adversarial-query-expansion.md](./m13-adversarial-query-expansion.md) | Generate 4 axes of orthogonal query expansion (adjacent / opposing / abstraction / domain-shift). | [⚙️ module](../../modules/methods/m13-adversarial-query-expansion.md) |

## Assumptions

_(Document any implicit assumptions about how this folder is used —
file-naming conventions, slot-fill mechanisms, depth ordering, etc.
This block exists to prevent workflow drift; future agents inherit
the rationale instead of re-deriving it. If no assumptions apply,
state that explicitly.)_

- _none recorded yet_

---

_See also:_ [../../AGENTS.md](../../AGENTS.md) · [../../../AGENTS.md](../../../AGENTS.md)
