---
type: task
status: active
slug: narrative-skills-extraction-adr
summary: "Decision-class Task: produce an ADR evaluating extraction of the narrative skills (novel-architect, the-agency-system-architect, suno-lyric-writer, Dramatica corpus) into a sibling repo or governance-isolated namespace, instead of relying on the AGENTS.md NO.5 don't-load workaround."
created: 2026-05-07
updated: 2026-05-07
task_id: "056"
task_status: open
task_owner: "unassigned"
task_priority: P3
task_uses_prompts: []
task_spawns_research: []
task_spawns_prompts: []
task_blocked_by: []
task_supersedes: []
task_superseded_by: []
task_affects_paths:
  - decisions/
  - tasks/056-narrative-skills-extraction-adr/
---

# Task 056 — Narrative Skills Extraction (ADR)

## Goal

Decide whether the four narrative-skill subtrees (`skills/novel-architect/`, `skills/the-agency-system-architect/`, `skills/suno-lyric-writer/`, plus the Dramatica corpus + `tools/dramatica-nav/`) belong in this governance-substrate repository at all. The current state is a workaround: `AGENTS.md` `NO.5` instructs agents *not to load* the narrative ontology for non-narrative work because it is large, off-domain, and bootstrap-cost expensive. The single falsifiable outcome of this Task: a new ADR under `decisions/<NNNN>-narrative-skills-extraction.md` is ratified (`adr_status: Accepted` or `Proposed` with a follow-up implementation Task), recording one of {extract-to-sibling-repo, isolate-as-`skills/narrative/` namespace with own root spec, status-quo with rationale}.

## Plan

1. **Inventory** the narrative-skill footprint: file count, total token budget under default `AGENTS.md` load, cross-references into governance specs vs. self-contained content, and the actual cost imposed by `NO.5` on a typical non-narrative agent session.
2. **Draft** three options with comparable tradeoff axes (governance coupling, agent boot cost, contributor onboarding cost, cross-repo CI burden, existing-Task disruption).
3. **Select** an option; author `decisions/<NNNN>-narrative-skills-extraction.md` per the ADR template and `research/adr-spec-research-synthesis/output/SPEC.md`.
4. **Open** an implementation successor Task if the chosen option requires migration work (extract or isolate); otherwise close with rationale.

## Todo

- [ ] Inventory narrative-skill footprint (write to `notes.md`).
- [ ] Draft three options + tradeoff matrix.
- [ ] Author ADR at `decisions/<NNNN>-narrative-skills-extraction.md`.
- [ ] If ADR status is Accepted with migration: open implementation Task and link it via `task_spawns_prompts`.
- [ ] Write `friction-log.md` with FL[0–3] declaration on closure.

## Links

- Parent dispatch: [Task 053](../053-core-architecture-review-followups/) finding B.5.
- Existing rules at branch-time: [`AGENTS.md` `NO.3`–`NO.6`](../../AGENTS.md) — the workaround being evaluated.
- Governance: [`research/adr-spec-research-synthesis/output/SPEC.md`](../../research/adr-spec-research-synthesis/output/SPEC.md) — ADR authoring contract.
