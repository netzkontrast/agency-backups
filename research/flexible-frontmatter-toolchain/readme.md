---
type: research
status: completed
slug: flexible-frontmatter-toolchain
summary: "Synthesis run distilling 6 in-house specs + Anthropic skill-creator into a flexible maintenance contract (required-only) plus a stateless validate/edit/extract/query toolchain that supersedes count-based linters and stored indexes."
created: 2026-05-05
updated: 2026-05-05
research_phase: complete
research_executes_prompt: flexible-frontmatter-toolchain
research_friction_level: FL1
---

# /research/flexible-frontmatter-toolchain/

**What is this folder?** Execution workspace for the prompt at [`/prompts/flexible-frontmatter-toolchain/`](../../prompts/flexible-frontmatter-toolchain/). It synthesises prior in-house research and Anthropic's `skill-creator` pattern into a flexible-frontmatter-toolchain SPEC.

**Why is it here?** Per `RESEARCH.md`, every research run lives in `/research/<slug>/` where the slug equals the executing prompt's slug. This run is **synthesis-only** — no new external Deep Research was issued.

## Linked Navigation

| Resource | Purpose |
|---|---|
| [prompt.md](./prompt.md) | Immutable snapshot of the executing prompt at run-start. |
| [workspace/](./workspace/) | Session log + scratch notes. |
| [synthesis/](./synthesis/) | Methodology, tracks, state, post-synthesis log. |
| [reflection/](./reflection/) | Critical-thinking artefacts: contradiction log, falsification, friction. |
| [output/SPEC.md](./output/SPEC.md) | The deliverable — Flexible Frontmatter Toolchain SPEC. |

## Downstream Tasks

- [`/tasks/016-flexible-frontmatter-toolchain/`](../../tasks/016-flexible-frontmatter-toolchain/) — build the `fm-validate / fm-extract / fm-edit / fm-query` tool suite.
- [`/tasks/017-migrate-repo-to-flexible-toolchain/`](../../tasks/017-migrate-repo-to-flexible-toolchain/) — migrate the existing repo onto the new tools and retire the count-based linters.

## Open Questions Surfaced

None blocking; the spec lists three deferred design questions in §Open Questions. Two of them are tracked as Todo items inside Task 016, one inside Task 017. No new follow-up prompts were filed.

## Workflow Assumptions

- This run reuses the `research_phase: complete` lifecycle in one shot because every input was a repo-local artefact already produced by an earlier `complete` workspace. There is no kickoff/synthesis/reflection split spread across sessions.
- The synthesis explicitly **reverses** part of `tasks/010-skills-frontmatter-index-suite/` (the persisted-index strategy) and explains the reversal in [`reflection/M07-contradiction-log.md`](./reflection/M07-contradiction-log.md). Task 010 remains open; its scope is narrowed by Task 016 to the *query CLI surface only*.
