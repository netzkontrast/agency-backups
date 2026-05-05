---
type: note
status: active
slug: 027-adr-spec-research-synthesis-friction-log
summary: "Mandatory closure friction log for Task 027 (TASK.md §7.7). Mirrors the run-level friction log in research/adr-spec-research-synthesis/reflection/friction-log.md."
created: 2026-05-05
updated: 2026-05-05
---

# Task 027 Friction Log

**Highest Frustration Level: FL1**

## Summary

The full friction record from the Research run lives in [`research/adr-spec-research-synthesis/reflection/friction-log.md`](../../research/adr-spec-research-synthesis/reflection/friction-log.md). This file is the required Task-level mirror per `TASK.md §7.7`.

## FL Declaration

The task closed cleanly. The two FL1 frictions encountered are:

1. **`/sc:` skill invocation ambiguity** — the prompt names `/sc:analyze` and `/sc:brainstorm` as commands; their semantics were applied directly rather than spawning sub-agent runs that would shadow the same artefacts. ≈ 5 min context-switching cost.
2. **Two-toolchain transition state** — the spec had to declare which validator chain (`tools/validate-frontmatter.py` legacy vs `tools/fm/validate.py` flexible) it composes with. Resolved by composing with the *currently default* legacy chain and documenting the future re-registration in §7.3 rationale. ≈ 3 min cost.

Neither friction blocked the work. Both are recorded in the run's friction log with suggested process tweaks for future research-proposal prompts.

## Outcome

`research/adr-spec-research-synthesis/output/SPEC.md` is in force. `tools/check-governance.sh` exits 0. Tasks 028 and 029 remain `open`, both `task_blocked_by: ["027"]` — they unblock with this commit.
