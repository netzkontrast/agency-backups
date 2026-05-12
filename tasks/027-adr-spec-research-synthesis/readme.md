---
type: index
status: active
slug: adr-spec-research-synthesis-readme
summary: "Index for Task 027 — analyze root specs via /sc:analyze + /sc:brainstorm, then execute a Research run producing the repo-native ADR governance spec."
created: 2026-05-05
updated: 2026-05-05
---

# Task 027 — ADR Spec Research Synthesis

- [`task.md`](./task.md) — Goal, Plan, Todo, Links.
- [`friction-log.md`](./friction-log.md) — Closure friction log (FL1 declared).

## State

`task_status: done`. Tasks 028 and 029 unblock with this closure (both list `task_blocked_by: ["027"]`).

## Artefacts

| Artefact | Status | Path |
|----------|--------|------|
| Analysis report | done | [`research/adr-spec-research-synthesis/workspace/analysis.md`](../../research/adr-spec-research-synthesis/workspace/analysis.md) |
| Brainstorm output | done | [`research/adr-spec-research-synthesis/workspace/brainstorm.md`](../../research/adr-spec-research-synthesis/workspace/brainstorm.md) |
| Output spec | done | [`research/adr-spec-research-synthesis/output/SPEC.md`](../../research/adr-spec-research-synthesis/output/SPEC.md) |
| Friction log (research) | done | [`research/adr-spec-research-synthesis/reflection/friction-log.md`](../../research/adr-spec-research-synthesis/reflection/friction-log.md) |
| Friction log (task closure) | done | [`./friction-log.md`](./friction-log.md) |

## Relationship to Gemini Draft

The Gemini draft at `research/gemini/agency-adr-governance-spec/adr-governance-spec.md` is the theoretical foundation. This task's research run grounds it against the repo's actual governance conventions and resolves all structural mismatches. The Gemini draft is input; the SPEC.md produced here is the authoritative output.
