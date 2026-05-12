---
type: index
status: archived
slug: spec-staleness-decision-formalization
summary: "Research workspace for the deterministic staleness-decision algorithm — produces output/SPEC.md (consumed by tools/fm/check-task-lifecycle-classification.py per Task 033 ST-4 / Task 039 ST-4)."
created: 2026-05-07
updated: 2026-05-12
research_phase: archived
research_executes_prompt: research-spec-staleness-decision-formalization
research_friction_level: FL0
---

# Spec — Staleness Decision Formalization

This folder contains the execution workspace for the [`research-spec-staleness-decision-formalization`](../../prompts/research-spec-staleness-decision-formalization/prompt.md) prompt. The prompt is shared between [Task 033 ST-2](../../tasks/033-task-spec-integration/subtasks/02-research-spec-staleness-decision-formalization.md) and Task 039 ST-2 (cross-Task input).

## Why this exists

`MAINTENANCE.md §3.4` declares a four-bucket staleness audit but specifies it in prose. The downstream helper `tools/fm/check-task-lifecycle-classification.py` (Task 033 ST-4 / Task 039 ST-4) needs a deterministic algorithm — same inputs, same bucket — that a Python script can implement directly. This workspace produces that algorithm.

## Contents

- [`output/SPEC.md`](./output/SPEC.md) — the deterministic decision tree (§1), five signal extraction recipes (§2), four open-Task walkthroughs (§3), `MAINT_STALE_DAYS` configuration declaration (§4), independent-agent-agreement argument (§5), and ST-4 implementation notes (§6).
- [`reflection/friction-log.md`](./reflection/friction-log.md) — FL declaration for the run.

## Open Questions Surfaced

None. The four-bucket contract is fully specified by `TASK.md §4.7` + `MAINTENANCE.md §3.4`; the SPEC just renders it as a deterministic mapping.

## Consumed by

- [`tools/fm/check-task-lifecycle-classification.py`](../../tools/fm/) — implements §1's pseudocode.
- [`MAINTENANCE.md §3.4`](../../MAINTENANCE.md) — references this SPEC as the executable spec for the staleness audit (parent task handles that edit; not in scope here).

## Assumptions Log

- The four §4.7 buckets are stable and exhaustive — no fifth bucket is needed (assumption inherited from `TASK.md §4.7`; if a fifth bucket emerges, this SPEC is superseded, not amended).
- `MAINT_STALE_DAYS` defaults to 7 days per current `MAINTENANCE.md §3.4`; if that default changes, only the §4.1 table needs updating, not the §1 algorithm.
- `tools/fm/_core.py` and `tools/fm/query.py` are the canonical frontmatter-parsing and search surfaces for the ST-4 implementation (per Task 016 / 019 toolchain landing).
- Worked examples (Tasks 022/023/024/025) are evaluated against `HEAD` on 2026-05-07; on a different baseline the bucket assignments may shift mechanically, which is the point of the deterministic algorithm.
