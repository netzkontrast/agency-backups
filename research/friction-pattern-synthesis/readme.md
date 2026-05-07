---
type: research
status: active
slug: friction-pattern-synthesis
summary: "Cross-task friction taxonomy: aggregates every friction-log.md across tasks/ and research/ into FL distribution, root-cause taxonomy, per-spec attribution, and verbatim governance-spec amendments. Closes Task 033 ST-1."
created: 2026-05-07
updated: 2026-05-07
research_phase: complete
research_executes_prompt: research-friction-pattern-synthesis
research_friction_level: FL1
---

# Research — Friction Pattern Synthesis

## What this workspace is

Executes [`/prompts/research-friction-pattern-synthesis/prompt.md`](../../prompts/research-friction-pattern-synthesis/prompt.md). Aggregates every `friction-log.md` in `/tasks/<NNN>-<slug>/` and `/research/<slug>/reflection/` into a structured cross-task synthesis: (a) FL distribution histogram, (b) recurring root-cause taxonomy with frequency counts, (c) per-spec friction-attribution, (d) verbatim TASK.md / FRUSTRATED.md amendments grounded in evidence.

## Why now

Task 033 (`task-spec-integration`) ST-1 needs an evidence-grounded basis for amending `TASK.md` and `FRUSTRATED.md`. Without a cross-task synthesis, individual friction logs cannot inform spec amendments — patterns are only visible at aggregate. The work also feeds the parallel Task 038 ST-1 (FL0 justification audit) which reads the same corpus.

**Spawned by:** Task 033 ST-1 dispatch on `claude/run-close-task-spec-2sW2y`.

## Layout

- [`output/SPEC.md`](./output/SPEC.md) — final deliverable: FL histogram, taxonomy, per-spec attribution, verbatim amendment proposals.
- [`workspace/`](./workspace/) — corpus inventory, raw FL extraction, classification scratch.
- [`synthesis/`](./synthesis/) — root-cause clustering tracks.
- [`reflection/`](./reflection/) — `friction-log.md` (FL declaration) plus method notes.

## Open Questions Surfaced

- The four verbatim amendments in `output/SPEC.md §4` are evidence-anchored proposals; ratification is the parent Task 033's call (specifically ST-5: amend TASK.md / ST-6: amend FRUSTRATED.md per the chain's amendment phase).
- Aggregate suggested rules from Task 030 (FE-1..FE-10 and FE-EX-1..5) and the cross-task amendment routing table (Task 030 friction-log §Pattern routing) are absorbed here as evidence; whether they land verbatim in target specs is decided by Tasks 032-040 individually.

## Assumptions Log

- **A-1.** "Closed task" = any task folder under `/tasks/<NNN>-<slug>/` carrying a `friction-log.md`. The corpus survey enumerated 33 such logs (including `updated`-status closures), well above the ≥15 falsification threshold. *Invalidates if* a closure-status filter strips the count below 15; if so the SPEC documents the constrained corpus rather than failing silently.
- **A-2.** Research-side friction is read from `/research/<slug>/reflection/friction-log.md` only (not `synthesis/` or `workspace/`). 20 such logs found. *Invalidates if* future research workspaces relocate their FL declaration; rule already encoded in TASK.md §7.7 and `RESEARCH.md` §2.5 so the location is canonical.
- **A-3.** Pre-existing baseline ERRORs are deferred to their owning task per the precedent set by Task 032 (`agents-spec-integration`) friction log F1. Documented here, not fixed under this Task. After in-session repair of the 5 × `decisions/000{1..5}-*.md` `ADR.A.5.4` ERRORs by `pip install jsonschema` (per AGENTS.md SS.1) and after the in-flight branch state landed bullets for 045 and 046 in `tasks/readme.md`, the remaining baseline ERRORs at run-end are: (a) `tasks/046-github-workflow-research/task.md::F.4.2` missing required heading `## Todo` — owned by Task 046 itself; (b) `tasks/readme.md::T.7.11` Task 033 bullet status `done` vs `task.md task_status: open` — resolves automatically when the parent Task 033 closure flow flips `task_status: open` → `done` at merge time. The dispatch instruction explicitly says "Do NOT modify TASK.md or any other governance specs — the parent task handles that"; the 033 readme/task drift is exactly that hand-off.
- **A-4.** Task 030's `notes.md §3` already classified planning-time friction events FE-1..FE-10 by FL band. Those are absorbed as additional evidence into §2 of the SPEC but are not re-counted in §1's session-execution histogram (different lifecycle: planning-time vs execution-time).
- **A-5.** "Per-spec attribution" (§3) means: for each FL2+ entry, cite the root spec (TASK.md, FRUSTRATED.md, FOLDERS.md, etc.) whose ambiguity, gap, or contradiction caused the friction. Multiple specs can be implicated for the same entry. The table in §3 is intended as input to Tasks 032-039 amendment passes.
