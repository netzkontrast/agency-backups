---
type: index
status: active
slug: task-092-subtasks
summary: "Subtask index for Task 092 (Phase 2 skill-corpora port). Four strictly-sequential subtasks: triage → SuperClaude Phase 2 → Superpowers full corpus → snapshot cleanup."
created: 2026-05-12
updated: 2026-05-12
---

# Task 092 — Subtasks

Four sequential subtasks. The ordering is not arbitrary: each one needs its predecessor's output. ST-2 and ST-3 MAY proceed in parallel **only** if ST-1's triage matrix explicitly partitions their work and ST-1 is `done` first.

## Sequencing DAG

```
ST-1 (triage)
   └─► [triage-matrix.md produced; reviewed; closed]
         │
         ├─► ST-2 (SuperClaude Phase 2)   ─┐
         │                                  │  (MAY parallelise if ST-1 partitions
         └─► ST-3 (Superpowers full corpus) ─┘   the work non-overlappingly)
                              │
                              └─► ST-4 (cleanup)
                                    └─► [snapshot deleted; waivers removed]
```

## Subtasks

- [`01-triage.md`](./01-triage.md) — **ST-1 (read-only).** Read every snapshot artefact via `/sc:research` and `/sc:analyze` *(local-only — see Task 092 Note)*; produce a decision matrix at `../references/triage-matrix.md`. Output: matrix + per-skill notes; no `/skills/` writes.
- [`02-superclaude-phase-2.md`](./02-superclaude-phase-2.md) — **ST-2.** Port the SuperClaude keep-list from the matrix into `skills/sc-<slug>/`. Bundle the 5 remaining MODE files. Apply ADR-0011 D.8 body adaptation where the upstream binds to a non-Agency MCP.
- [`03-superpowers-port.md`](./03-superpowers-port.md) — **ST-3.** Port the Superpowers keep-list into `skills/superpowers-<slug>/`. Vendor-prefix already accepted by `tools/fm/validate.py::_check_skill_source` per Task 091 forward-compat test.
- [`04-cleanup.md`](./04-cleanup.md) — **ST-4.** Delete `tasks/091-…/references/upstream-snapshot/`, strip the two waiver entries, bump `skills/readme.md`. Final governance.

## Assumptions Log

- "Keep-list" is the union of ST-1 matrix rows where `decision ∈ {port, adapt}`. Items marked `skip` carry rationale only — no port.
- The 2026-08-12 waiver expiry is the hard deadline for ST-4. If ST-1 + ST-2 + ST-3 cannot land before then, the alternative is filing a waiver-extension Task (low-merit; prefer accelerating the porting).
- ST-2 and ST-3 each get their own PR — never a combined "all-Phase-2" PR. Per the Phase 1 split-into-2 precedent (`tasks/091-…/references/full-plan-part-3.md §9.7 OQ1`), keeping subtask PRs scope-narrow accelerates review.
