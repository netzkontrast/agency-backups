---
type: note
status: active
slug: skills-query-v2-fulfilment
summary: "v2 fulfilment of Task 010's ten canonical questions via the stateless skills-query wrapper. Documentation lives Task-side because the upstream research SPEC is T4-immutable (research_phase: complete)."
created: 2026-05-11
updated: 2026-05-11
---

# Task-010 v2 Fulfilment Note

## Why this lives in the Task folder

Task 022's original plan said *"Update SPEC §C with the v2 fulfilment note."* The referenced
spec is [`research/flexible-frontmatter-toolchain/output/SPEC.md`](../../research/flexible-frontmatter-toolchain/output/SPEC.md),
whose frontmatter sets `research_phase: complete`. Per `MAINTENANCE.md §1`, that body is
**T4-immutable**; the closed-research repair allowance ([Task 059](../059-closed-research-repair-allowance/))
permits T1 (`updated:` bumps) and T2 (broken-link repair) only — adding a `## §C` section
would be a T3 structural edit, which is forbidden. The v2 fulfilment note therefore lives
here, under Task 022's folder, and is *cited* by the SPEC via `task_uses_prompts` reciprocity
(predecessor Task 010 → successor Task 022 in the supersession graph) rather than embedded
in the SPEC body.

## Supersession statement

The persistent-index strategy proposed in [`tasks/010-skills-frontmatter-index-suite/`](../010-skills-frontmatter-index-suite/task.md)
is superseded by the stateless toolchain defined in
[`research/flexible-frontmatter-toolchain/output/SPEC.md`](../../research/flexible-frontmatter-toolchain/output/SPEC.md) §2
(*"supersedes the persistent-index strategy proposed in tasks/010-skills-frontmatter-index-suite/"*).
The ten canonical questions enumerated in Task 010's §Plan step 3 remain valuable —
they are the common access patterns that drove the original index design.

Task 022 ships [`tools/fm/skills_query.py`](../../tools/fm/skills_query.py) as a
**thin convenience wrapper** that answers each of those ten questions by composing the
stateless tools (`fm-query`, `fm-extract`, `fm-graph`). No persistent index is built; every
invocation walks the live filesystem through the canonical tools. The wrapper exists for
human + agent ergonomics, NOT as a second source of truth.

## Question → composition map

| Q   | Task-010 wording                       | skills-query invocation                                     | Underlying composition |
|-----|----------------------------------------|-------------------------------------------------------------|------------------------|
| Q1  | `query summary <slug>`                 | `skills-query summary <slug>`                               | `fm-query slug=<X>` → `fm-extract --frontmatter summary` |
| Q2  | `query skills --kind tool`             | `skills-query skills --kind tool`                           | `fm-query has-key=skill_kind --scope skills`, post-filter |
| Q3  | `query skills --target-agent jules`    | `skills-query skills --target-agent jules`                  | `fm-query has-key=skill_target_agents --scope skills`, post-filter |
| Q4  | `query references <slug>`              | `skills-query references <slug>`                            | `fm-query refers-to=<X>` ∪ `fm-query referenced-by=<X>` |
| Q5  | `query orphans`                        | `skills-query orphans`                                      | `fm-graph --detect orphans,dangling` |
| Q6  | `query stale --since 30d`              | `skills-query stale --since 30d`                            | `fm-query stale-since=30d` |
| Q7  | `query path <slug>`                    | `skills-query path <slug>`                                  | `fm-query slug=<X> --format paths` |
| Q8  | `query header <slug> <header>`         | `skills-query header <slug> <heading>`                      | `fm-query slug=<X>` → `fm-extract --section <heading>` |
| Q9  | `query graph --type task --status open`| `skills-query graph --type task --status open`              | `fm-query type=<T>` → post-filter `task_status` |
| Q10 | `query manifest`                       | `skills-query manifest`                                     | `fm-query has-key=name --scope skills` (rendered as JSON) |

## Invariants

- **No persistent index.** The wrapper MUST NOT cache results and MUST NOT write any
  file under `.agent_cache/`.
- **1 KB output cap.** Every subcommand caps stdout at 1 024 bytes, inherited from
  `fm-query`'s `OUTPUT_CAP_BYTES` (per the §5.4 stateless contract).
- **Read-only.** No subcommand mutates filesystem state. `tools/check-governance.sh` step
  `[5c]` invokes two read-only smoke commands (`manifest`, `path`) to verify the wrapper
  composes the underlying tools without error.
- **Single source of truth preserved.** The wrapper consumes `header-ontology.json` indirectly
  through the underlying `fm-*` tools; it does NOT re-encode any matrix.

## Token-cost record (measured 2026-05-11)

Sizes are bytes of returned stdout (multiply by ≈ 0.25 for an approximate token count).
"Body baseline" = the file size or section size a naive agent would read instead.

| Q   | Invocation                                          | stdout bytes | Body baseline | Reduction |
|-----|-----------------------------------------------------|-------------:|--------------:|----------:|
| Q1  | `summary surface-skills-architecture`               |          277 |       ≥ 1 200 |     ≥ 4×  |
| Q7  | `path flexible-frontmatter-toolchain`               |          217 |  ≥ 5 KB folder|    ≥ 23×  |
| Q8  | `header surface-skills-architecture Goal`           |          324 |     ≥ 1 200   |     ≥ 4×  |
| Q9  | `graph --type task --status open`                   |     1 KB cap | 100 KB tree   |   ≥ 100×  |
| Q10 | `manifest`                                          |     1 KB cap |  ≥ 200 KB skills bodies | ≥ 200× |

**Reading.** Point lookups (Q1/Q7/Q8) clear the Task-010 §Plan-step-7 threshold (≥ 8×) by a
comfortable margin. Matrix queries (Q5/Q9/Q10) bottom-out at the cap, where the comparison
flips: the *body baseline* there represents the full scan an agent would otherwise need.
The wrapper exposes `--limit` (via `fm-query`) for callers that want tighter scope.

## References

- Predecessor Task: [`../010-skills-frontmatter-index-suite/task.md`](../010-skills-frontmatter-index-suite/task.md)
- Upstream SPEC: [`../../research/flexible-frontmatter-toolchain/output/SPEC.md`](../../research/flexible-frontmatter-toolchain/output/SPEC.md) §2, §5
- Closed-research T1/T2 allowance: [`../059-closed-research-repair-allowance/task.md`](../059-closed-research-repair-allowance/task.md)
- Wrapper source: [`../../tools/fm/skills_query.py`](../../tools/fm/skills_query.py)
- Tests: [`../../tools/tests/fm/test_skills_query.py`](../../tools/tests/fm/test_skills_query.py)
