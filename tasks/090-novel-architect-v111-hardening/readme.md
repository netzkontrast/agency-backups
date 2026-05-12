---
type: index
status: active
slug: novel-architect-v111-hardening
summary: "Directory index for Task 090 — v1.1.1-hardening of the novel-architect skill family. Carries the executable workflow plan (workflow.md) produced by /sc:analyze → /sc:brainstorm → /sc:design → /sc:workflow."
created: 2026-05-12
updated: 2026-05-12
---

# Task 090 — novel-architect@1.1.1-hardening

**What:** Convert v1.1.0's metadata-only sub-module declaration into a runtime two-layer delegation contract. Rewrites 12 orchestrator files (5 phases + 7 commands); grows the 4 sub-modules with 14 new method files; graduates scene from stub; ships 3 of 4 deferred CLI linters.

**Why here:** Closes the H1/H2/M1/M2/M3/M4 findings from the post-v1.1.0 `/sc:analyze` audit. The friction-log of [Task 070](../070-novel-architect-v110-epic/task.md) (FL2) explicitly identified the "lean but real" depth-for-breadth trade and the 4 deferred linters; v1.1.1 is the planned remediation.

## Navigation

- [`task.md`](./task.md) — Task spec: Goal, Context, Plan, Todo, Acceptance Criteria, Spawned Tasks, Links.
- [`workflow.md`](./workflow.md) — Executable implementation plan produced by `/sc:workflow`: 19 commits across 4 clusters (A: prose rewrite, B: scene graduation, C: linter triple, D: small fixes + retirement-placeholder verify), with file manifests, verification plan, risk register, and FL pre-brief.
- [`friction-log.md`](./friction-log.md) — Closing friction log with `Highest Frustration Level: FL[0-3]` declaration (written at Task close).

## Assumptions Log

- The `/home/user/Dual-Kernel/` checkout is the canonical pattern source per Task 071's references; v1.1.1's two-layer contract derives the "Architect = single entry point per domain, delegates but doesn't execute" invariant from `skill-audit/ecosystem-analysis.md:10@9fdf16f`.
- The 4 sub-modules from v1.1.0 (`novel-architect-{character,structure,world,scene}`) are the canonical destination set. The /sc:design review explicitly rejected 3 additional sub-modules (`-story`, `-bootstrap`, `-integration`) proposed by the line-level cartographer; bootstrap and reflection stay in the orchestrator as dispatcher/meta surfaces; drafting folds into scene.
- The legacy skill (`skills/novel-architect-legacy/`) stays on disk through v1.1.1 per Task 070's retirement criterion; criterion (c) is mechanically satisfied (zero `task_blocked_by` legacy refs), criteria (a)+(b) require productive Kohärenz-Protokoll sessions on v1.1.1+ (Task 091 placeholder gates this).
- No external consumers reference the migrated `skills/novel-architect/methods/{character,structure,research}/` paths — verified via `grep` against the full repo at audit time. Therefore D2: clean rewrite, no compat symlinks.
