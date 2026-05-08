---
type: index
status: completed
slug: task-039-maintenance-spec-integration
summary: "Folder index for Task 039 — MAINTENANCE.md spec integration. Closed: lifted three orphaned research outputs (agentic-eval-trust-improvement-spec, repo-maintenance-protocol-spec, governance-specs-update-research §2) into MAINTENANCE.md §1.1.2 / §2.3 / §3.2 / §3.4 / §3.5; shipped tools/maintenance/{staleness-audit,dynamic-readme-partition,trust-audit}.py + research/toolchain-flip-criteria/output/SPEC.md; 15 Gherkin scenarios across M.B.1–M.B.7."
created: 2026-05-06
updated: 2026-05-08
---

# Task 039 Folder

## What

Operational folder for Task 039. Largest payload in the 031–038 chain — six subtasks, three of which lift orphaned research into normative scope. Closed 2026-05-08.

## Files

- [`task.md`](./task.md)
- [`subtasks/`](./subtasks/) — 2 research, 3 tooling, 1 spec amendment.
- [`friction-log.md`](./friction-log.md) — FL0; chain-level reflection.

## Assumptions Log

- ~~The §3.4 staleness algorithm formalization is shared with Task 033~~ — **Resolved.** Task 033 ST-2 landed the canonical SPEC at [`research/spec-staleness-decision-formalization/output/SPEC.md`](../../research/spec-staleness-decision-formalization/output/SPEC.md); this Task's ST-2 consumed it verbatim and ST-3 implemented it as `tools/maintenance/staleness-audit.py`.
- ~~The §3.5 duplicate-task_id circular dependency resolution is contingent on Task 033's subtask 03~~ — **Resolved.** MAINTENANCE.md §3.5 now closes the discovery loop: coherence run files the dedup Task on first encounter; subsequent encounters surface the existing Task without re-discovery; the ADR validator step `[5/6]` is unaffected because the renumber excludes `decisions/`.
