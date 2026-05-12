---
type: task
status: completed
slug: adr-assumption-audit
summary: "Multi-subagent critical-thinking audit: surface hidden assumptions baked into the ADR governance spec, catalogue which architectural decisions are already implicitly in force in this repo, and enumerate the decisions that must still be made before implementation can begin."
created: 2026-05-05
updated: 2026-05-05
task_id: "029"
task_status: done
task_owner: "claude-code"
task_priority: P2
task_uses_prompts:
  - adr-assumption-audit
task_spawns_research:
  - adr-assumption-audit
task_spawns_prompts: []
task_supersedes: []
task_blocked_by:
  - "027"
task_affects_paths:
  - research/adr-assumption-audit/
  - prompts/adr-assumption-audit/
---

# Task 029 — ADR Assumption Audit (Critical-Thinking)

## Goal

Use **three parallel subagents** — each governed by a distinct critical-thinking method from the Research Prompt Optimizer (M06, M07, M13) — to produce an exhaustive audit of:

1. **Hidden assumptions** embedded in the Gemini ADR governance spec and the Task 027 synthesis, which, if violated, would silently break the governance model.
2. **Implicit ADRs already in force** — architectural decisions the repo has already made (in root specs, tooling, or branching conventions) that the ADR spec must acknowledge, formalize, or supersede.
3. **Pending decisions** that block implementation — explicit open questions that require a human architectural judgment call before tooling can be built.

The task is **done** when `research/adr-assumption-audit/output/REPORT.md` exists, is structured per the three deliverables above, and has been reviewed by the maintainer.

## Context

The Gemini research prompt (`research/gemini/agency-adr-governance-spec/research-prompt_agency-adr-governance-spec.md`) embedded five critical-thinking methods: M06 Source Triangulation, M07 Contradiction Log, M08 What Would Change My Mind, M12 Base-Rate Anchoring, and M13 Adversarial Query Expansion. These methods were applied during the *generation* of the spec but not against the *repo itself*. This task inverts that lens.

Key categories of hidden assumptions to surface:

- **Storage assumptions:** The spec mandates `docs/decisions/` but the repo uses `research/` for synthesis artefacts. Which wins, and under what rule?
- **Tooling assumptions:** The spec defines `agency-adr` as a standalone CLI but the repo has `tools/fm/` Python modules. Is co-location required? Is the dependency graph compatible?
- **Frontmatter assumptions:** The spec's JSON-Schema defines `id`, `title`, `status`, `date`, `supersedes`. The repo's L1/L2 Vault Core Ontology defines `type`, `status`, `slug`, `summary`, `created`, `updated`. Fields overlap (`status`), collide (`slug` vs `id`), or are absent on one side. Which ontology is authoritative?
- **AGENTS.md ownership assumptions:** The spec mandates the synthesis pipeline overwrites `AGENTS.md`. But `AGENTS.md` currently contains manually authored content. Who owns which sections?
- **Semantic fidelity assumptions:** The spec mandates ≥ 0.95 fidelity but does not define the measurement algorithm. This is an open implementation decision, not a resolved one.

## Plan

### Subagent A — M13 Adversarial Query Expansion: Hidden Assumption Extraction

Deploy a subagent running **[M13] Adversarial Query Expansion** across four axes against the ADR governance spec and existing root specs:

- **Adjacent:** What assumptions does the spec share with similar governance frameworks (OPA/Rego, RFC-style specs, legal codes)?
- **Opposing:** Where does the spec assume things will *not* happen that this repo *does* do (e.g., manual `AGENTS.md` edits, direct ADR status mutation)?
- **Abstraction:** What higher-level assumption is the entire spec resting on (e.g., "engineers will write ADRs proactively" — is this true for an agentic repo)?
- **Orthogonal:** What happens if the MDL compression pipeline is never built — does the governance spec degrade gracefully or collapse?

Output: `research/adr-assumption-audit/workspace/m13-hidden-assumptions.md` — a numbered list of assumptions, each with axis label, assumption text, and a falsifiability criterion.

### Subagent B — M07 Contradiction Log: Implicit ADR Inventory

Deploy a subagent running **[M07] Contradiction Log** to scan all root specs and tooling for decisions that are already architectural facts but not formally recorded:

Scan targets:
- `AGENTS.md` — agent routing rules, token budget conventions
- `TASK.md` — Frontmatter Ontology, lifecycle states, branching convention
- `PROMPT.md` — prompt structure, framework requirements
- `RESEARCH.md` — research workspace layout, immutability rules
- `FOLDERS.md` — directory topology decisions
- `PRE_COMMIT.md` — hook architecture decisions
- `MAINTENANCE.md` — drift-detection and repair tier decisions
- `tools/check-governance.sh`, `tools/fm/*.py` — tooling architecture decisions

For each implicit ADR found, record: (a) the decision, (b) where it is embedded, (c) whether it conflicts with the Gemini spec, (d) whether it needs to be formalized as an ADR-0001-style record.

Output: `research/adr-assumption-audit/workspace/m07-implicit-adrs.md` — structured as a table: `Decision | Source Location | Conflicts With Spec? | Needs Formalization?`

### Subagent C — M06 Source Triangulation + M08 What Would Change My Mind: Pending Decisions

Deploy a subagent running **[M06] Source Triangulation** and **[M08] What Would Change My Mind** to identify every open architectural question that the spec deferred or left underspecified:

For each open question, apply M08: write the concrete observable evidence that would resolve it in each direction. Format:

> **Question:** [Precise question]
> **Option A:** [Choice] — confirmed by [evidence type needed]
> **Option B:** [Choice] — confirmed by [evidence type needed]
> **Current lean:** [Which way the spec implicitly leans and why]
> **Blocking:** [Which Task 028 module cannot be built until this is resolved]

Examples of known open questions:
- Storage path: `docs/decisions/` vs `research/adr/` vs `decisions/`
- Fidelity metric: cosine similarity vs AST-diff vs secondary LLM call
- AGENTS.md ownership: full synthesis overwrite vs guarded sections vs separate `AGENTS-adr.md`
- Supersession DAG storage: in YAML frontmatter vs external graph file
- Migration path: how existing implicit ADRs are bootstrapped as ADR-0001..N

Output: `research/adr-assumption-audit/workspace/m06-m08-pending-decisions.md`

### Synthesis — REPORT.md

Merge the three subagent outputs into `research/adr-assumption-audit/output/REPORT.md` structured as:

1. **§1 Hidden Assumptions** — from Subagent A (ranked by blast radius if assumption is violated)
2. **§2 Implicit ADRs in Force** — from Subagent B (table format, recommended formalization priority)
3. **§3 Pending Decisions** — from Subagent C (sorted by blocking dependency on Task 028)
4. **§4 Recommended Actions** — concrete next steps for each category, mapped to Task 027/028 or new tasks

## Todo

- [x] 1. Confirm Task 027 is `done` and `research/adr-spec-research-synthesis/output/SPEC.md` exists.
- [x] 2. Launch Subagent A (M13) — produce `m13-hidden-assumptions.md` (9 ASMs across 4 axes).
- [x] 3. Launch Subagent B (M07) — produce `m07-implicit-adrs.md` (11 IADRs; 5 P1, 4 P2, 2 P3).
- [x] 4. Launch Subagent C (M06+M08) — produce `m06-m08-pending-decisions.md` (7 PDs incl. 2 novel).
- [x] 5. Merge into `research/adr-assumption-audit/output/REPORT.md` §1–§4.
- [x] 6. Map pending decisions to Task 028 modules — appended PD↔OD cross-reference as `tasks/028-adr-tooling-impl-plan/implementation-plan.md §B`.
- [x] 7. Run `tools/check-governance.sh`; fix failures.
- [x] 8. Set `task_status: done`.

## Links

- Output report: [`research/adr-assumption-audit/output/REPORT.md`](../../research/adr-assumption-audit/output/REPORT.md) — §1–§4 (9 ASMs, 11 IADRs, 7 PDs, 5 Recommended Actions).
- PD↔OD cross-reference appendix: [`../028-adr-tooling-impl-plan/implementation-plan.md §B`](../028-adr-tooling-impl-plan/implementation-plan.md).
- Closure friction log: [`./friction-log.md`](./friction-log.md) — FL1.
- Blocked by (resolved): [`027-adr-spec-research-synthesis/task.md`](../027-adr-spec-research-synthesis/task.md) (`task_status: done`).
- Sibling: [`028-adr-tooling-impl-plan/task.md`](../028-adr-tooling-impl-plan/task.md) (`task_status: done`).
- Executing prompt: [`prompts/adr-assumption-audit/prompt.md`](../../prompts/adr-assumption-audit/prompt.md)
- Critical-thinking source: [`research/gemini/agency-adr-governance-spec/research-prompt_agency-adr-governance-spec.md`](../../research/gemini/agency-adr-governance-spec/research-prompt_agency-adr-governance-spec.md)
- Governing specs: [`TASK.md`](../../TASK.md), [`RESEARCH.md`](../../RESEARCH.md), [`FRUSTRATED.md`](../../FRUSTRATED.md)
