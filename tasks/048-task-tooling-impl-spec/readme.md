---
type: index
status: active
slug: task-048-folder
summary: "Folder index for Task 048 — Task Tooling Implementation SPEC. Surveys /skills/ (especially research-prompt-optimizer and prompt-optimizer) for inspiration, inventories existing /tasks/ tooling and gaps, and produces an implementation-ready SPEC for the next generation of Task-orchestration tooling."
created: 2026-05-07
updated: 2026-05-07
---

# Task 048 Folder

## What

Operational folder for Task 048, which produces an implementation-ready SPEC at `research/task-tooling-impl-spec/output/SPEC.md` proposing ≥6 concrete tools for Task creation, state-transition, template scaffolding, audit-graph maintenance, and friction-log capture. Inspiration is drawn from the `/skills/` corpus — especially `research-prompt-optimizer/` (phase + module decomposition) and `prompt-optimizer/` (scenario-keyed decision tables) — which solve an analogous problem at the prompt layer with a structured decomposition the Task layer has never adopted.

## Files

- [`task.md`](./task.md) — Goal, Plan, Falsification, Todo.
- [`subtasks/`](./subtasks/) — 2 research + 1 spec synthesis (Phase A parallel; Phase B sequential).

## Assumptions Log

- The `/skills/research-prompt-optimizer/` body is the highest-yield inspiration source per the user's framing; ST-1 prioritises it but does not exclude the other 12 skill bodies.
- The proposed tools all sit under `tools/fm/` (frontmatter-toolchain successor) rather than spawning a new `tools/task/` namespace; this minimises directory bloat per `FOLDERS.md` §F.1.1 and consumes the existing `tools/fm/_core.py` shared library. The SPEC MAY revisit this assumption in §2 (architecture) and propose a new namespace if the inventory in ST-2 surfaces a clean separation boundary.
- The SPEC is the deliverable; implementation is explicitly out of scope. A follow-up Task implements per the §1–§7 build contract, parallel to how Task 031 implemented the spec produced by Task 028.
- Pre-existing baseline ERRORs (e.g. Task 046 missing `## Todo`) are deferred per the Task 032 / Task 033 precedent; the closing run documents them in `friction-log.md` rather than expanding scope to fix them.
