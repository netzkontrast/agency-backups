---
type: task
status: active
slug: spec-subagent-subtask-prompt-format
summary: "Execute the agency-adr-governance-spec research prompt to produce a normative ADR-governance spec covering ADR lifecycle (proposed → accepted → superseded), token-efficient rule synthesis, and tooling acceptance criteria. The spec retroactively ratifies (or amends) the provisional conventions Task 026 used: subtask file format, sub-prompt format, /sc:agent dispatch, /sc:* command lifecycle, frustration-log meta-format. Findings from Task 026's planning-session friction log feed the research as primary input."
created: 2026-05-05
updated: 2026-05-05
task_id: "027"
task_status: open
task_owner: "unassigned"
task_priority: P1
task_uses_prompts:
  - agency-adr-governance-spec
task_spawns_research:
  - agency-adr-governance-spec
task_spawns_prompts: []
task_supersedes: []
task_superseded_by: []
task_blocked_by: []
task_affects_paths:
  - maintenance/
  - tasks/027-spec-subagent-subtask-prompt-format/
  - research/agency-adr-governance-spec/
---

# Task 027 — Author the Agency ADR-Governance Spec

## Goal

Execute [`/prompts/agency-adr-governance-spec/prompt.md`](../../prompts/agency-adr-governance-spec/prompt.md) (the renderer-emitted Category-B research prompt) to produce a single deliverable: `research/agency-adr-governance-spec/output/SPEC.md` conforming to the §0–§9 structure mandated by the prompt's Constraint Block 3.

Concretely, the spec MUST cover (per the prompt's §3–§7 aspect template):

1. **§3 — ADR-Explore.** How agents discover existing ADRs in the agency repo (location, naming, audit graph). Includes the question of where ADRs live: `/maintenance/adrs/` or `/decisions/` or repurposed `/tasks/<NNN>-<slug>/decision.md`.
2. **§4 — ADR-Plan.** How an agent proposes a new ADR (brief shape, status flow, reciprocity with `/tasks/`). Specifically resolves whether a Task can spawn an ADR independently of spawning a research workspace.
3. **§5 — ADR-Implement.** Lifecycle states (proposed → accepted → superseded → archived). Reciprocity of `adr_supersedes` ↔ `adr_superseded_by`. Whether ADRs participate in the existing `task_supersedes` audit graph.
4. **§6 — ADR-Review.** Acceptance criteria for an ADR (Gherkin scenarios, source triangulation if external sources used). Mapping to existing `tools/check-governance.sh` gates.
5. **§7 — ADR-Validate.** Token-efficient rule synthesis: how the ADR corpus collapses into the rules-files an AI agent loads (compression ratio + semantic-fidelity bounds, both measurable). Tooling acceptance criteria expressed as Gherkin + JSON-Schema sketches + CLI shape (NO reference implementation source code per CB3).

In addition to the prompt's mandated §0–§9 structure, the spec MUST address — as concrete §X.1 normative statements with stable IDs — every "Suggested rule for Task 027 to ratify" item from [`tasks/026-cleanup-dramatica-skills-corpus/notes.md §3 (Planning-Session Frustration Log)`](../026-cleanup-dramatica-skills-corpus/notes.md). These are listed in §Inputs below.

The Task is `done` when:

- `research/agency-adr-governance-spec/output/SPEC.md` exists, conforms to the §0–§9 structure, passes the prompt's 11-item Self-Verification Checklist.
- Each "Suggested rule" item from Task 026's frustration log is either (a) ratified as a normative statement in the spec OR (b) explicitly REJECTED with a rationale paragraph in §8 (Known Limitations & Open Questions).
- The Cross-Pollination Log records both Phase-2b imports (Exploration Sanity Pass + World-Change Check) per the prompt's §Cross-Pollination Steps.
- A friction log lands per [`FRUSTRATED.md`](../../FRUSTRATED.md).

## Background — Why This Task Exists

[Task 026](../026-cleanup-dramatica-skills-corpus/) authored nine subtask files using a PROVISIONAL convention copied verbatim from [Task 019](../019-fm-toolchain-suite-integration/). The convention is uncodified: no spec under `/maintenance/` documents what a subtask file MUST contain, what a sub-prompt block MUST look like, what `/sc:agent` invocation syntax means, when worktree isolation applies, or how `/sc:improve --loop --iterations N` counts iterations.

Task 026's [`notes.md §3 — Planning-Session Frustration Log`](../026-cleanup-dramatica-skills-corpus/notes.md) records ten distinct friction events (FE-1 through FE-10) encountered while AUTHORING those subtasks. Most surface as "Suggested rule for Task 027 to ratify" items. Task 027 absorbs them.

The user explicitly framed this as a two-step pattern: (a) Task 026 builds with provisional conventions; (b) Task 027 ratifies those conventions via research-driven spec. The prompt was rendered upstream (slug `agency-adr-governance-spec` per `research-prompt-optimizer v3.2.0`) and saved verbatim by the Task-026 planning agent into `/prompts/agency-adr-governance-spec/`.

ADRs are the right mechanism for this ratification BECAUSE:

- The conventions in question span multiple existing specs (TASK.md, PROMPT.md, RESEARCH.md, AGENTS.md, FRUSTRATED.md). Inlining the rules into one of them privileges the wrong axis.
- The conventions evolve — `/sc:agent` semantics in 2026 may differ from 2027. ADRs handle supersession natively; the existing spec layer doesn't.
- Token-efficient rule synthesis is itself an open question (the spec's §7). ADRs that agents read on-demand are cheaper than fat specs an agent re-reads every session.

## Pre-Work — Critical-Thinking Hooks (per `skills/research-prompt-optimizer/`)

The prompt itself imposes M06 / M07 / M08 / M12 / M13 plus the cross-pollination Phase-2b modules. This Task adds two task-side hooks per repo discipline:

### Bayesian Prior (M05)

- **Prior:** A Category-B extraction with the prompt's CB1 (repo-first) discipline produces a spec whose §3–§7 normative statements achieve ≥80% reciprocity with the "Suggested rule" items from Task 026's frustration log. Confidence: medium-high.
- **What would change the prior:** if the ADR canon (Nygard, MADR, Y-Statements) genuinely doesn't address AI-coding-agent rule-file patterns (a real risk per CB1 step 4: "literature-thin" disclosure). Then the spec would land more "open question" items than ratified rules, and Task 028 (or another follow-up) would be needed to resolve the residue.

### Pre-Mortem (M03) — Top 3 Failure Modes

1. **Spec bloat.** The §3–§7 aspect template plus the 10 frustration items plus the orthogonal information-theoretic lens combines into a spec that exceeds ~3000 lines and stops being readable. *Mitigation:* the prompt's CB3 explicitly forbids reference implementation source code; the §X.1 statements MUST be one BCP-14 keyword per sentence, capping verbosity at the per-statement level. Spec body MUST stay under 800 lines (rough target).
2. **Missed orthogonal axis.** The prompt's pre-specified orthogonal lens is "information-theoretic / compression — frame the ADR-corpus → rules-file synthesis as a minimum-description-length compression with semantic-fidelity bounds". An executing agent that doesn't actually invoke that lens (per the prompt's M13 audit at the Pre-Synthesis Integrity Check) ships a spec with no measurable acceptance criteria for the synthesis tool. *Mitigation:* the prompt's §11-item self-verification checklist enforces M13 invocation. The Task's friction-log MUST surface a non-invocation as FL2.
3. **Ratification ambiguity.** The 10 frustration items aren't binary "ratify / reject" — most have nuance (e.g., FE-7 is asking for an exception rule, not a primary rule). The spec author needs to convert each into a falsifiable normative statement. *Mitigation:* this Task's §Inputs section lists every frustration item by FE-N anchor; the spec author MUST address each by anchor in §3–§7 or rebut in §8.

## Plan

The plan is two phases: research execution (Phase R) + spec landing (Phase S).

```
Phase R — Research execution (single agent run):
  R1  Read /prompts/agency-adr-governance-spec/prompt.md end-to-end before any file edit.
  R2  Restate the prompt's Role + Narrowing sections in own words (per RISEN first-action directive).
  R3  Run the prompt's BATCH PROCEDURE (5 iterations: Explore / Plan / Implement / Review / Validate).
  R4  Honour the prompt's Constraint Block 0 reflection schedule (5 reflection entries minimum).
  R5  Honour M13 Adversarial Query Expansion across all four axes; the orthogonal lens is the
      pre-specified information-theoretic / compression frame.
  R6  Run the Pre-Synthesis Integrity Check (M4) verbatim before drafting the synthesis.
  R7  Author research/agency-adr-governance-spec/output/SPEC.md with the §0–§9 structure.
  R8  Each "Suggested rule" item from Task 026 §notes.md §3 is addressed in §3–§7 or rebutted in §8.

Phase S — Spec landing:
  S1  Land SPEC.md as research/agency-adr-governance-spec/output/SPEC.md (per RESEARCH.md).
  S2  Cross-link from this Task's friction-log to the SPEC.
  S3  Update Task 026's task.md §Anti-Patterns to remove the "PROVISIONAL" qualifier on the
      ratified conventions (and KEEP it on the rejected ones with a pointer to the §8 rebuttal).
  S4  Optionally: file a follow-up mini-task to amend AGENTS.md / TASK.md / PROMPT.md per the
      ratifications. This is OPTIONAL because some ratifications may live as ADRs forever
      and never need cross-spec amendment.
```

### Heavy /sc:* command usage

This task uses:

- **`/sc:research`** — primary execution. The prompt's framework declarations (Layer 1 Category-B, Layer 2 ReAct, Layer 3 RISEN) suit `/sc:research`'s pipeline. Single invocation against the prompt file.
- **`/sc:test`** — runs `tools/check-governance.sh` after S1 lands the SPEC.
- **`/sc:createPR`** — final action per [`AGENTS.md § Closing Run Procedure`](../../AGENTS.md).

`/sc:agent` is NOT used here — Task 027 is a single-agent research execution, not a fan-out.

## Todo

- [ ] 1. Author this `task.md` (current step) — set `task_status: open`.
- [ ] 2. Verify the executing prompt exists at [`/prompts/agency-adr-governance-spec/prompt.md`](../../prompts/agency-adr-governance-spec/prompt.md) and is `status: active`.
- [ ] 3. Initialise the research workspace at [`/research/agency-adr-governance-spec/`](../../research/agency-adr-governance-spec/) per [`RESEARCH.md`](../../RESEARCH.md). Frontmatter sets `research_executes_prompt: agency-adr-governance-spec`, `research_phase: kickoff`.
- [ ] 4. Phase R steps R1–R8 — execute the prompt to produce `research/agency-adr-governance-spec/output/SPEC.md`. This is one agent run; the prompt's self-verification checklist gates closure.
- [ ] 5. Phase S step S1 — verify SPEC.md is at the documented path and passes its own gates.
- [ ] 6. Phase S step S2 — write `friction-log.md` for this Task per [`FRUSTRATED.md`](../../FRUSTRATED.md). Link to SPEC.md.
- [ ] 7. Phase S step S3 — amend [`tasks/026-cleanup-dramatica-skills-corpus/task.md §Anti-Patterns`](../026-cleanup-dramatica-skills-corpus/task.md) to reflect the ratification outcome.
- [ ] 8. Phase S step S4 (OPTIONAL) — file a follow-up mini-task for cross-spec amendments if any ratification requires it.
- [ ] 9. Set `task_status: done`. Run `tools/check-governance.sh`. If exit 0, invoke `/sc:createPR` per [`AGENTS.md § Closing Run Procedure`](../../AGENTS.md).

## Inputs (the 10 Frustration Items From Task 026)

The spec's §3–§7 normative statements MUST address each item below. Each is identified by its FE-N anchor in [`tasks/026-cleanup-dramatica-skills-corpus/notes.md §3`](../026-cleanup-dramatica-skills-corpus/notes.md). One-line summaries here; the executing agent reads the verbose context from notes.md.

| FE | One-line summary | Suggested ratification (from notes.md) |
|---|---|---|
| FE-1 | No canonical "subtask file" template | L2.1 frontmatter namespace `subtask_*`; subtasks live under `<parent-task-folder>/subtasks/<NN>-<slug>.md`. |
| FE-2 | `/sc:agent` invocation syntax undocumented | `/sc:agent` ≡ harness `Agent` tool; subtask "Agent Prompt" block IS the prompt parameter. |
| FE-3 | `task_status` drift between task.md and tasks/readme.md | `tasks/readme.md` regenerated, not hand-maintained. Pre-commit gate. |
| FE-4 | Renderer-emitted prompt has depth-2 YAML | Renderer-output exemption: depth-2 OK only inside fenced ```yaml block in body. |
| FE-5 | Prompt-spawn vs prompt-use semantics under-typed | Add `prompt_spawned_by_task` field; reciprocity rules. |
| FE-6 | `/sc:*` command lifecycle undocumented | New spec `maintenance/sc-command-spec.md` enumerating every `/sc:*` command. |
| FE-7 | Verbosity tension with anti-bloat rule | `@verbose-load-bearing` HTML-comment marker exempts intentional verbose sections. |
| FE-8 | No precedent for "task spawns research that ratifies parent's own conventions" | `task_provisional_conventions` field; advisory linter only. |
| FE-9 | `task_uses_prompts` vs `task_spawns_prompts` cardinality | Restate definitions explicitly: USES = executes, SPAWNS = authors-for-other-task. |
| FE-10 | New ontology-surface artefacts have no preview lifecycle | `status: preview` lifecycle for new ontology-surface artefacts; promotion via ADR. |

The spec MAY group multiple FE items under a single normative statement when they share an underlying invariant (e.g., FE-1 and FE-8 may collapse into "L2.1 subtask + provisional-conventions" cluster). The spec MUST NOT silently drop any FE; rejections go to §8.

## Anti-Patterns to Avoid

- **MUST NOT** modify the executing prompt at `/prompts/agency-adr-governance-spec/prompt.md`. The prompt is verbatim by user instruction; amendments are out of scope.
- **MUST NOT** reproduce concrete ADR records in the spec (per the prompt's CB3). The spec governs HOW ADRs are made, not their content.
- **MUST NOT** emit reference implementation source code (per CB3). Tooling acceptance criteria depth is BEHAVIOUR + INTERFACE only: Gherkin + JSON-Schema + CLI shape.
- **MUST NOT** ratify a subtask convention that conflicts with [Task 019's existing pattern](../019-fm-toolchain-suite-integration/subtasks/) without explicitly noting Task 019 as a "to-be-migrated predecessor" in the spec's §8.
- **SHOULD NOT** propose a new top-level operational directory beyond `/tasks/`, `/prompts/`, `/research/`, `/maintenance/`, `/skills/`, `/tools/`, `/templates/`, `/tests/`. ADRs SHOULD live under one of these (likely `/maintenance/adrs/` per the prompt's framing).

## Links

- Predecessor (non-blocking, supplies primary input): [`/tasks/026-cleanup-dramatica-skills-corpus/`](../026-cleanup-dramatica-skills-corpus/) — its planning-session frustration log is direct input to this Task's research.
- Executing prompt: [`/prompts/agency-adr-governance-spec/`](../../prompts/agency-adr-governance-spec/) — Category-B research-proposal prompt rendered by `research-prompt-optimizer v3.2.0`.
- Spawned research: [`/research/agency-adr-governance-spec/`](../../research/agency-adr-governance-spec/) — workspace initialised in step 3.
- Sibling pattern reference: [`/tasks/015-integrate-dramatica-ncp-skills/`](../015-integrate-dramatica-ncp-skills/) — the kickoff/synthesis research-execution pattern this task copies.
- Governing specs: [`AGENTS.md`](../../AGENTS.md), [`TASK.md`](../../TASK.md), [`PROMPT.md`](../../PROMPT.md), [`RESEARCH.md`](../../RESEARCH.md), [`FRUSTRATED.md`](../../FRUSTRATED.md), [`PRE_COMMIT.md`](../../PRE_COMMIT.md), [`MAINTENANCE.md`](../../MAINTENANCE.md).
- Critical-thinking source: [`research-prompt-optimizer`](../../skills/research-prompt-optimizer/) — methods M03, M05, M13 applied above; M06, M07, M08, M12 applied inside the prompt.
