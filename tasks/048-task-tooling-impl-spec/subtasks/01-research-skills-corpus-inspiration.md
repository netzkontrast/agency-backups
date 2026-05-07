---
type: note
status: draft
slug: task-048-st1-research-skills-corpus-inspiration
summary: "ST-1 (research head): survey the /skills/ corpus — especially research-prompt-optimizer (phases / modules / render / AGENTS.md) and prompt-optimizer (scenario-keyed decision tables) — and extract ≥6 patterns that transfer to /tasks/-side tooling. Output feeds ST-3 SPEC synthesis."
created: 2026-05-07
updated: 2026-05-07
---

# ST-1: Research — `/skills/` Corpus Inspiration Survey

**Executor:** main-agent or deep-research subagent.

**Parallelism:** Phase A (parallel) — runs concurrently with ST-2. No inter-dependencies.

## Goal

Produce a structured inventory of patterns in the `/skills/` corpus that transfer to `/tasks/`-side tooling, prioritised by transferability score. The output is consumed by ST-3 as the inspiration column of every proposed tool's §3 entry.

## Inputs

- `/home/user/agency/skills/research-prompt-optimizer/` — full body. Notable artefacts: `phases/`, `modules/`, `render/`, `examples/`, `AGENTS.md`, `catalog.yaml`, `meta-prompt-spec.md`, `phase2-design-plan.md`, `CHANGELOG.md`, `docs/`.
- `/home/user/agency/skills/prompt-optimizer/` — `selection.md`, `intent-framework-map.md`, `framework-components.md`, `templates.md`, `output-format.md`, `clarification-questions.md`, `anti-patterns.md`, `examples.md`.
- `/home/user/agency/skills/spec-skill/` — apply-mode pattern (potential transfer to `task-apply` template scaffolder).
- `/home/user/agency/skills/the-agency-system-architect/` — meta-system orchestration framing.
- `/home/user/agency/skills/skill-creator/` — meta-pattern for authoring new skills (potential transfer to `task-creator` flow).
- `/home/user/agency/skills/ralph-skill/` — uses spec-skill apply-mode against `references/ralph-spec.md` (transferable interaction pattern).
- The other 7 skill bodies are read-on-demand if the floor (≥4 transfers from research-prompt-optimizer alone) is at risk.

## Acceptance Criteria

1. Output at `research/task-tooling-impl-spec/workspace/01-skills-inspiration.md` (work-in-progress; the final SPEC at `output/SPEC.md` is ST-3's deliverable).
2. **≥6** distinct patterns identified, each with: source slug, source artefact (file path + anchor), one-paragraph description, and a *transferability score* (`HIGH` / `MEDIUM` / `LOW`) with one-sentence rationale.
3. **≥4** of the patterns originate from `research-prompt-optimizer/` (the user-flagged primary inspiration source).
4. Each pattern names a candidate `/tasks/`-side tool surface that the pattern would inform (e.g. "phase decomposition → `tools/fm/task-phases.py` for Plan/Todo phase tagging").
5. Anti-patterns explicitly listed: at least 2 patterns from `prompt-optimizer/anti-patterns.md` re-cast as `/tasks/`-side anti-patterns the SPEC SHOULD prohibit.

## Falsification

Wrong cut **iff** fewer than 6 transferable patterns surface OR fewer than 4 originate from `research-prompt-optimizer/`. Mitigation: that skill has 7+ surface artefacts plus the AGENTS.md interaction contract; a four-pattern minimum is well-cleared at floor.

## Dependencies

None. Phase A.

## Estimated Effort

Medium (~2–3 hours; reading + thematic coding).
