---
type: research
status: archived
slug: pre-commit-readme-update-cadence
summary: "Token-cost analysis of three readme-update cadence options (per-touch / batched-at-precommit / hybrid) on the existing corpus; ratifies batched-at-precommit and produces drop-in wording for PRE_COMMIT.md §2 and FRUSTRATED.md §28 (joint subtask consumed by Task 037 ST-4 and Task 062 B-1)."
created: 2026-05-07
updated: 2026-05-12
research_phase: archived
research_executes_prompt: research-pre-commit-readme-update-cadence
research_friction_level: FL0
---

# Research — Pre-Commit Readme-Update Cadence

**What is this folder?** Execution workspace for the prompt at [`/prompts/research-pre-commit-readme-update-cadence/`](../../prompts/research-pre-commit-readme-update-cadence/).

**Why is it here?** Per `RESEARCH.md`, every research run lives in `/research/<slug>/` where the slug equals the executing prompt's slug. This run resolves the load-bearing contradiction between PRE_COMMIT.md §2 (read by some agents as "update on touch") and FRUSTRATED.md §28 (treats per-file readme spam as FL2).

## Contents

- [`prompt.md`](./prompt.md) — Immutable run-start snapshot of the executing prompt.
- [`workspace/`](./workspace/) — Scratch notes and `session.log`.
- [`synthesis/`](./synthesis/) — `state.md`, `methodology.md`, `post-synthesis-log.md`.
- [`reflection/`](./reflection/) — `friction-log.md` and method notes.
- [`output/`](./output/) — `SPEC.md` (the deliverable: cadence rule + drop-in wording).

## Open Questions Surfaced

None. The cadence rule resolves cleanly; the byte-identical wording dependency is tracked by Task 062 B-1 (which consumes this SPEC's §3).

## Workflow Assumptions

- Token-cost evidence draws on the existing corpus (closed PRs and commits on `main`); no synthetic benchmarking.
- The "hybrid" option is included for completeness but is shown to dominate neither the per-touch nor the batched-at-precommit option on token cost or human comprehension.
