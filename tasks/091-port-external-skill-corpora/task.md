---
type: task
status: active
slug: port-external-skill-corpora
summary: "Epic: Port SuperClaude v4.3.0 + Superpowers v4.0.3 skill corpora into /skills/ under vendor-prefixed namespaces per ADR-0011. Phase 1 (14 skills + validator + root-spec hookup) ships in two subtasks ST-1 + ST-2."
created: 2026-05-12
updated: 2026-05-12
task_id: "091"
task_status: open
task_owner: "claude-opus-4-7"
task_priority: P1
task_uses_prompts: []
task_spawns_research: []
task_spawns_prompts: []
task_affects_paths:
  - tools/fm/validate.py
  - tools/tests/test_validate_skill_source.py
  - skills/sc-createPR/
  - skills/sc-implement/
  - skills/sc-test/
  - skills/sc-improve/
  - skills/sc-research/
  - skills/sc-system-architect/
  - skills/sc-backend-architect/
  - skills/sc-frontend-architect/
  - skills/sc-security-engineer/
  - skills/sc-quality-engineer/
  - skills/sc-refactoring-expert/
  - skills/sc-performance-engineer/
  - skills/sc-deep-research-agent/
  - skills/sc-pm-agent/
  - skills/readme.md
  - AGENTS.md
  - RESEARCH.md
---

# Task 091 — Port External Skill Corpora (Epic)

## Goal

Execute the Phase 1 batch ratified by [ADR-0011](../../decisions/0011-external-skill-corpora-import.md) (`adr_status: Accepted` 2026-05-12). Port the **five dangling `/sc:*` skill references** cited in [`CLAUDE.md §13`](../../CLAUDE.md) (`sc:createPR`, `sc:implement`, `sc:test`, `sc:improve`, `sc:research`) plus **nine supporting agent-skills** required by their `skill_references_skills` audit-graph edges (per the per-skill tier table in [`references/full-plan-part-4.md` §10.3](./references/full-plan-part-4.md)).

Extend [`tools/fm/validate.py`](../../tools/fm/validate.py) to accept the new `skill_source` L2 frontmatter key (ADR-0011 D.2) with two new diagnostic codes (`F.B.7`, `F.B.8`). Rewrite [`AGENTS.md` Closing Run Procedure](../../AGENTS.md#closing-run-procedure) to cite the local `skills/sc-createPR/SKILL.md` (closing the remote `https://github.com/.../createPR.md` URL) and add `RESEARCH.md §7` citing the local `skills/sc-research/SKILL.md`.

The Epic is **done** when both subtasks close `done`:

- **ST-1 (corpus)** — [`subtasks/01-phase-1-corpus.md`](./subtasks/01-phase-1-corpus.md): validator extension + 14 skill folders under `skills/sc-*/` per ADR-0011 D.1–D.9.
- **ST-2 (hookup)** — [`subtasks/02-phase-1-hookup.md`](./subtasks/02-phase-1-hookup.md): AGENTS.md citation rewrite + RESEARCH.md §7 addition.

ST-2 MAY only commence after ST-1 closes `done` and merges to `main` (per `references/full-plan-part-3.md` §9.7 OQ1 resolution — split-into-2 Task shape).

## Context

This Epic operationalises the design output of the `/sc:brainstorm` → `/sc:design` → `/sc:implement` cycle captured in [`references/readme.md`](./references/readme.md) (the four-part plan index). The five dangling `/sc:*` references in `CLAUDE.md §13` and the remote-URL citation in `AGENTS.md` Closing Run Procedure CR.7 (Claude Code implementation note) are aspirational today — no `skills/sc-*/SKILL.md` exists in this repository. The Epic resolves them.

Two upstream corpora are sourced:

- **SuperClaude_Framework v4.3.0** — five `/sc:*` commands + five engineer/architect/expert/research agent personas + four sibling agent skills + one pm agent. 14 items total for Phase 1.
- **Superpowers v4.0.3** — out of scope for Phase 1 (sequenced for Phase 2 per `references/full-plan-part-2.md` §5).

Per ADR-0011, imported skills land at `skills/sc-<bare-slug>/` with the new L2 frontmatter key `skill_source: "superclaude@v4.3.0"` and SHA-pinned upstream citations in `## References`. The `sc:research` SKILL.md body is materially rewritten per D.8 (WebSearch + WebFetch primary; Tavily MCP marked OPTIONAL in `## Compatibility`); the verbatim upstream body is archived at `skills/sc-research/references/upstream-sc-research.md`.

The 14-item batch + per-skill tier table + canonical SKILL.md shape + frontmatter values + `skill_bundles_tools` entries + root-spec citation diffs are fully specified in [`references/full-plan-part-4.md` §10.3–§10.5](./references/full-plan-part-4.md). The implementing agent SHOULD treat that document as the executable specification.

## Plan

The complete plan is at [`references/full-plan-part-4.md`](./references/full-plan-part-4.md) §10 (Design specifications). The Epic-level summary is:

1. **ST-1 prep.** Verify ADR-0011 is `Accepted` (`python3 tools/adr/cli.py validate decisions/0011-external-skill-corpora-import.md` exits 0). Read [`references/full-plan-part-1.md`](./references/full-plan-part-1.md) — [`references/full-plan-part-4.md`](./references/full-plan-part-4.md) end-to-end so the implementer has the full design in context (~83 KB of planning record).
2. **ST-1 execute.** Run the 11-step plan from `references/full-plan-part-4.md` §10.5 "Task A". Close `task_status: done` with friction log.
3. **ST-1 verify.** Run the verification recipe from `references/full-plan-part-4.md` §10.7. All 9 steps MUST pass.
4. **ST-2 execute.** Run the 7-step plan from `references/full-plan-part-4.md` §10.5 "Task B" (after ST-1 merges to `main`). Close `task_status: done` with friction log.
5. **ST-2 verify.** Re-run the verification recipe — particularly the `grep -n "src/superclaude/commands/createPR.md" AGENTS.md` test (BR.9.2) MUST return zero matches.
6. **Epic close.** Once both subtasks merge, flip this Task to `task_status: done`. Update [`../readme.md`](../readme.md) Status: `open` → `done`.

## Todo

- [ ] 1. ST-1 (corpus) opened, executed, closed `done` per [`subtasks/01-phase-1-corpus.md`](./subtasks/01-phase-1-corpus.md)
- [ ] 2. ST-1 PR merged to `main`
- [ ] 3. ST-2 (hookup) opened, executed, closed `done` per [`subtasks/02-phase-1-hookup.md`](./subtasks/02-phase-1-hookup.md)
- [ ] 4. ST-2 PR merged to `main`
- [ ] 5. End-to-end verification recipe from `references/full-plan-part-4.md` §10.7 passes
- [ ] 6. `tasks/readme.md` entry flipped `Status: open` → `done`
- [ ] 7. Friction log authored (this Epic's `friction-log.md`)
- [ ] 8. `task_status: done` set

## Acceptance Criteria

The Epic-level acceptance criteria are inherited from the design's `BR.9.*` Gherkin scenarios in [`references/full-plan-part-3.md` §9.6](./references/full-plan-part-3.md):

- **BR.9.1** — five dangling references resolve to local skill bodies
- **BR.9.2** — AGENTS.md no longer cites the remote SuperClaude URL
- **BR.9.3** — sc:research is Agency-adapted, not Tavily-mandatory
- **BR.9.4** — audit graph reciprocity computed for new skills
- **BR.9.5** — T2 body cap enforced (≤ 5 KB); overflow in `references/`

Per-subtask AC live inside each subtask file (`TA.1.*` for ST-1, `TB.1.*` for ST-2).

## Links

- ADR: [`decisions/0011-external-skill-corpora-import.md`](../../decisions/0011-external-skill-corpora-import.md) (`adr_status: Accepted`)
- Subtask index: [`subtasks/readme.md`](./subtasks/readme.md)
- Subtask ST-1 (corpus): [`subtasks/01-phase-1-corpus.md`](./subtasks/01-phase-1-corpus.md)
- Subtask ST-2 (hookup): [`subtasks/02-phase-1-hookup.md`](./subtasks/02-phase-1-hookup.md)
- Complete planning record (4 parts): [`references/readme.md`](./references/readme.md)
- Governing root specs: [`AGENTS.md`](../../AGENTS.md), [`CLAUDE.md §13`](../../CLAUDE.md), [`SKILLS.md`](../../SKILLS.md), [`RESEARCH.md`](../../RESEARCH.md)
- Sibling ADRs cited: [ADR-0003](../../decisions/0003-frontmatter-source-of-truth.md) (frontmatter source of truth), [ADR-0006](../../decisions/0006-agency-system-prototype-exemption.md) (precedent: imported content stays in repo), [ADR-0007](../../decisions/0007-skill-bundles-tools-frontmatter.md) (precedent: L2 additive key via ADR)
- Upstream: [SuperClaude_Framework v4.3.0](https://github.com/netzkontrast/SuperClaude_Framework), [Superpowers v4.0.3](https://github.com/netzkontrast/superpowers)
