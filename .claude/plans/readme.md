# `.claude/plans/` — Agency Repo Refactor Plan

> Working area for the long-running brainstorm to refactor the `agency` repository. This is **not** the executed refactor — that becomes Tasks under `tasks/` once the plan is locked. Everything in `.claude/` is brainstorm-state, kept out of `tasks/`/`prompts/`/`research/` so it does not pollute the canonical governance layers.

---

## State of the plan (2026-05-13)

**Round 10 closed. Round 11 paused for synthesis review before resuming.**

Iteration so far:

- **Rounds 1–6** captured the original goal and the first wave of architectural decisions (four-layer model, JSON Schema as primary spec language, ADRs as `decision.yaml`, MCP numbering server, `task_kind: goal` subtype).
- **Round 7** re-pinned layer contents (prompts = traces, research = results + reflection, gate-tooling matrix) and reopened `meta/` scope.
- **Round 8** explored audit-trail layouts and overflow channels; both decisions were superseded in Round 9.
- **Round 9** locked SemVer-versioned amendment folders and a reserved `notes:` field. Theatrical rename direction (Actor enacts → Space witnesses) was locked in *direction only*; execution deferred.
- **Round 10** opened the goal-only Task workflow: 4-phase `task_phase` lifecycle, deferred Gherkin, no-decomp direct promotion, dual MCP-ID + parent-SemVer subtask addressing, explicit `task_depends_on` DAG. Four locks (A/B/C/D).
- **`/sc:reflect` after Round 10** surfaced **drift**: 30 sub-decisions across 10 rounds, zero mechanically connected to the original Round-1 budget target (~50K → ≤ 8K tokens). FL1 declared.
- **Two Gemini Deep Research briefs** commissioned and returned (2026-05-13). Brief #1 audits the 14 architectural decisions; brief #2 surveys context-engineering patterns implementable with what was locked.
- **Synthesis + rethink overview** written reading both briefs against the *original* Round-1 goal (not against existing locks). Headline: ~60 % of the plan survives; 4 locks need REPLACE, 4 need REVISE, 1 major addition (the bootstrap-budget machinery the plan never had).

**Next:** the user reviews the rethink overview, then Round 11+ resumes with the question inventory in `plan-rethink-overview.md §7`.

---

## File navigation

### Plans (`.claude/plans/`)

| File | What it is | When to read |
|---|---|---|
| [`agency-refactor-plan.md`](./agency-refactor-plan.md) | The canonical iterative plan. Locks from Rounds 1–10, open questions for Round 11+, `/sc:reflect` drift analysis and FL1 friction log appended at the bottom. | Start here for the full history. |
| [`round-10-additions.md`](./round-10-additions.md) | Detailed write-up of the four Round-10 locks (A/B/C/D — Gherkin deferred-write, no-decomp direct promotion, dual subtask addressing, DAG ordering). Sibling to the main plan. | When you need the goal-only Task / deferred-Gherkin / DAG-ordering rationale in depth. |
| [`synthesis-gemini-1-2.md`](./synthesis-gemini-1-2.md) | Synthesis of the two Gemini Deep Research briefs, read against the **original** Round-1 goal — not against accumulated locks. Convergent thesis, divergent findings, top-5 external precedents, top-5 warnings, synthesis-level open questions. | Read BEFORE the rethink overview to understand the literature's verdict. |
| [`plan-rethink-overview.md`](./plan-rethink-overview.md) | Maps synthesis findings onto the existing plan. What survives, what to REPLACE, what to REVISE, what to ADD (bootstrap Tiers 1/2/3), what remains open. Includes proposed Round-11+ AskUser sequencing. | Read AFTER the synthesis. This is the input to the next round of user-dialogue. |
| [`readme.md`](./readme.md) | This file. Navigation + state-of-plan summary. | Right now. |

### Research prompts (`.claude/research-prompts/`)

| File | What it is |
|---|---|
| [`gemini-deep-research-agency-refactor.md`](../research-prompts/gemini-deep-research-agency-refactor.md) | Brief #1 — sent to Gemini Deep Research. Stress-tests the 14 architectural decisions against the 2023–2026 literature. Per-decision verdict table, named precedents, falsification frames. |
| [`gemini-deep-research-bootstrap-context-engineering.md`](../research-prompts/gemini-deep-research-bootstrap-context-engineering.md) | Brief #2 — companion brief targeting the ~50K → ≤ 8K bootstrap-budget drift surfaced by `/sc:reflect`. Asks for ≥ 20 named patterns, compatibility matrix against the 14 locks, cheapest-first implementation roadmap with token budgets. |

### Research results (`.claude/research-results/`)

| File | What it is |
|---|---|
| [`gemini-1-architecture-audit.md`](../research-results/gemini-1-architecture-audit.md) | Brief #1 result — *Stress-testing the architectural decisions of the agency repository*. 292 lines, 84 citations. Per-decision KEEP/REVISE/REPLACE verdicts; Memos A–J on per-investigation-area patterns; recency-stratified bibliography. |
| [`gemini-2-bootstrap-context-engineering.md`](../research-results/gemini-2-bootstrap-context-engineering.md) | Brief #2 result — *Bootstrap-budget reduction & context-engineering patterns for the agency substrate*. 326 lines, 51 citations. Catalogue of 22 named patterns; compatibility matrix against the 14 locks; three-tier implementation roadmap with token-budget targets. |

---

## Read order

If you are coming into this brainstorm fresh, in order:

1. [`agency-refactor-plan.md`](./agency-refactor-plan.md) — what was decided in Rounds 1–10 and why.
2. [`round-10-additions.md`](./round-10-additions.md) — the Round-10 locks in detail (skip on a quick pass).
3. [`gemini-deep-research-agency-refactor.md`](../research-prompts/gemini-deep-research-agency-refactor.md) → [`gemini-1-architecture-audit.md`](../research-results/gemini-1-architecture-audit.md) — brief #1 prompt + result, for the per-decision audit.
4. [`gemini-deep-research-bootstrap-context-engineering.md`](../research-prompts/gemini-deep-research-bootstrap-context-engineering.md) → [`gemini-2-bootstrap-context-engineering.md`](../research-results/gemini-2-bootstrap-context-engineering.md) — brief #2 prompt + result, for the bootstrap-budget patterns.
5. [`synthesis-gemini-1-2.md`](./synthesis-gemini-1-2.md) — both results read together, against the original goal.
6. [`plan-rethink-overview.md`](./plan-rethink-overview.md) — what the synthesis means for the existing plan; the live Round-11+ question inventory.

---

## Why a working area under `.claude/` and not under `tasks/`?

The repository's canonical governance layers (`tasks/`, `prompts/`, `research/`, `skills/`) are subject to the pre-commit gate, frontmatter linters, and the assumption that artefacts they contain are decided / executing / executed work. The brainstorm is **none of those** — it is iterative dialogue producing decisions that *become* Tasks once locked.

Per the `CLAUDE.md` separation-of-concerns rules: do not pollute `tasks/` with planning chatter. Once the plan is locked (after Rounds 11–15 close), the executed refactor will be decomposed into Tasks under `tasks/` and the bootstrap machinery (Tier 1/2/3 from brief #2) will ship through that normal pipeline.

The `.claude/` directory is the right home for brainstorm-state because it is already the shared working area for Claude Code session-specific scratch (plans, drafts, harness config) that does not belong in the canonical layers.

---

## Friction log

`FL1` declared at end of Round 10 (`/sc:reflect` drift). See `agency-refactor-plan.md` § Frustration Log. The drift was self-corrected by commissioning the two Gemini briefs before resuming dialogue. Subsequent commits have closed that drift by re-grounding the plan in external literature.
