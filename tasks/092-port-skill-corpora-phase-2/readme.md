---
type: index
status: active
slug: port-skill-corpora-phase-2
summary: "Directory index for Task 092 — complete the upstream skill-corpora port (Phase 2 of ADR-0011). Four sequential subtasks (triage → sc Phase 2 → superpowers → cleanup) operating on the Task 091 snapshot."
created: 2026-05-12
updated: 2026-05-12
---

# Task 092 — Port Skill Corpora (Phase 2 / Epic)

**What:** Epic umbrella for the Phase 2 execution of [ADR-0011](../../decisions/0011-external-skill-corpora-import.md). Triages every snapshot artefact under [`tasks/091-…/references/upstream-snapshot/`](../091-port-external-skill-corpora/references/upstream-snapshot/), ports the keep-list under `skills/sc-*/` and `skills/superpowers-*/`, then retires the snapshot before its 2026-08-12 waiver expiry. Contains no code diffs itself — diffs land via four sequential subtasks.

**Why here:** Task 091 ST-1 closed the dangling-reference fix (14 sc-* skills); the remaining upstream corpus (~75 candidates across SuperClaude + Superpowers) was staged for triage rather than mass-ported, so each skill can be evaluated on merit. Splitting Phase 2 into triage + two port-batches + cleanup keeps each PR independently reviewable and gives the eventual snapshot deletion an explicit owner.

**Note — internal research only:** see [`task.md` Note section](./task.md#note--internal-research-only). All triage research MUST source the local snapshot; external GitHub fetches are an anti-pattern for this Epic (SHA drift, network dependency).

## Navigation

- [`task.md`](./task.md) — Epic spec: internal-research Note, Goal, Context, Plan, Todo, Acceptance (BR.92.1–BR.92.4), Out-of-Scope, Links.
- [`subtasks/`](./subtasks/) — Four sequential subtasks (ST-1 → ST-4).
  - [`subtasks/readme.md`](./subtasks/readme.md) — subtask index with sequencing + parallelism notes.
  - [`subtasks/01-triage.md`](./subtasks/01-triage.md) — Read snapshot via `/sc:research` and `/sc:analyze`; produce `references/triage-matrix.md`.
  - [`subtasks/02-superclaude-phase-2.md`](./subtasks/02-superclaude-phase-2.md) — Port `superclaude` keep-list (~25 commands + ~11 agents + 5 modes).
  - [`subtasks/03-superpowers-port.md`](./subtasks/03-superpowers-port.md) — Port full Superpowers corpus into `skills/superpowers-*/`.
  - [`subtasks/04-cleanup.md`](./subtasks/04-cleanup.md) — Delete snapshot, remove waivers, final governance.
- [`references/`](./references/) — Triage matrix + supporting per-skill notes (populated during ST-1).

## Assumptions Log

- Snapshot is **byte-pinned** at SuperClaude_Framework `22ad3f48` (v4.3.0) and Superpowers `b9e16498` (v4.0.3). ADR-0011 D.9 forbids re-syncing within this Epic; if upstream ships a newer release, file a separate Task.
- The two waivers added by Task 091 (`tools/.frontmatter-waivers` + `tools/.script-allowlist`) **expire 2026-08-12**. The 90-day window is the natural hard deadline for the Epic; ST-4 cleanup MUST land before then to avoid stale-waiver friction.
- The Phase-1 ST-2 hookup Task (AGENTS.md citation + RESEARCH.md §7) is a sibling, NOT a dependency of this Epic. Phase 2 only depends on Phase 1 ST-1 merging.
- The `F.B.7` → `F.B.8`/`F.B.9` renumber recorded in [Task 091 friction-log FL1.1](../091-port-external-skill-corpora/friction-log.md) should be ratified by a new ADR (`decisions/0012-skill-source-validator-diagnostic-codes.md`) before this Epic mass-ports. The Todo item 2 tracks this carry-over.
- Triage decisions (`port` / `adapt` / `skip`) are advisory until ST-1 is closed; ST-2 and ST-3 implementers MAY revise the matrix with rationale, but MUST NOT silently deviate.
