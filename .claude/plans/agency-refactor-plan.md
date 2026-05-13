# Agency Repo Refactoring Plan (Working Draft)

> **Status:** Iterative requirements capture — Round 7. Still gathering. Not yet finalised.
> **Branch:** `claude/repo-refactoring-plan-CfLY5`
> **Scope:** Restructure the `agency` repo per the four-layer model the user is incrementally specifying across rounds.

---

## Context

The current `agency` repository (96 tasks, 77 prompts, 30 research workspaces, 76 skills, 16 ADRs, 10+ root specs) has accumulated friction in three areas the user wants to address:

1. **Bootstrap cost.** Every session is required to read `AGENTS.md` plus several layer specs before any work — the user has signalled they want a `<8K`-token bootstrap budget with the rest deferred / on-demand.
2. **Parallel-work renumbering.** Filesystem-derived `NNN` numbering (`tasks/096-…`) collides when multiple agents create artifacts on parallel branches. Numbers must come from a **global authoritative dispenser**, not from `ls | wc -l`.
3. **Layer-content drift.** The Task / Prompt / Research / Skill separation in CLAUDE.md is correct in spirit, but the *contents* of each layer have drifted (prompts contain task framing, tasks contain prompt body, research workspaces accumulate follow-up prompts). Round 7 re-pins what each layer actually carries.

---

## Locked decisions (Rounds 1 – 6)

These are not re-litigated in Round 7 unless the user explicitly reopens them.

- **Spec language.** Primary normative surface is **JSON Schema** (machine-validated). `AGENTS.md` and layer specs become thin prose envelopes pointing at the schemas. Gherkin remains for acceptance criteria.
- **ADRs.** Authored as `decision.yaml`; the `decision.md` MADR rendering is **auto-generated** (CLI: `tools/adr/cli.py render`). Accepted ADRs remain T4-immutable; supersede via successor.
- **Meta scope expansion.** A new top-level `meta/` directory absorbs friction logs, session traces, plans, reviews, and runbooks. Layout:
  ```
  meta/
  ├── friction/       # FL declarations + nightly maintenance digest
  ├── sessions/       # session-trace exports
  ├── plans/          # plan documents (referenced by tasks)
  ├── reviews/        # code-review subagent outputs
  ├── runbooks/       # operational procedures
  └── workspace/<NNN>/  # per-plan scratch space, NNN mirrors the plan number
  ```
- **Goals.** Not a new top-level folder. Implemented as a `task_kind: goal` subtype within `tasks/`. Goals are long-horizon parent tasks that decompose into subtasks.
- **MCP numbering server.** A small MCP service dispenses globally unique, monotonically increasing IDs to remove `ls`-based numbering. Eliminates parallel-branch renumbering. (Design details: Round 7 Q2.)

---

## Round 7 additions — layer contents pinned

The user re-specified what each layer carries:

### Prompts — *session traces + tool-calling artefacts*
- Captures the **executable instruction set** AND the **realised execution trace** (tool calls, intermediate outputs, hook telemetry).
- Primary downstream consumer: the **`prompt-optimizer` skill**, which learns from accumulated traces to improve future prompts.
- Implication: prompts are not just authored text; they are append-only execution records bound to the prompt body.

### Research — *results + reflection*
- Carries the **artefacts produced by executing a prompt** (`output/`, `synthesis/`, `workspace/`) PLUS a **reflection-on-task** entry (what worked, what failed against the Task's acceptance criteria).
- Reflection feeds the gate decision (below).

### Tasks — *goal + criteria + gate-tooling*
A Task carries three things:
1. **Goal definition** (what done looks like).
2. **Acceptance criteria** (Gherkin scenarios; the bar Research must clear).
3. **Validation tooling** that can mechanically gate the Research result. The tooling may be **built by subtasks** (a Task that produces a validator is itself a subtask of the parent goal-task).

### Gating loop — feedback flow
When a Research workspace closes, the parent Task runs its gate-tooling against the result:
- **PASS** → Task closes, research workspace marked immutable (T4).
- **FAIL** → one or more of:
  1. Update the Plan (revise approach).
  2. Re-synthesise the current Research workspace (no new workspace; same prompt, sharper synthesis).
  3. Spawn a **follow-up Task** (new goal, new criteria, new prompt — never appended to closed research).

### Subtasks — Tasks may have many
- A parent Task (often a `task_kind: goal`) decomposes into **N subtasks**.
- Each Task/subtask has its own **Plan directory** under `meta/plans/<NNN>/` with the corresponding workspace at `meta/workspace/<NNN>/`.
- **Cardinality of Plan → Prompt → Research:** *open question, sentence cut off in Round 7 — see Open Questions below.*

---

## Working layer model (post-Round 7, pending Q1/Q3/Q4 answers)

```
Global ID dispenser (MCP service)
        │
        ▼
  ┌─────────────┐  task_uses_prompts ┌──────────────┐ executed-by ┌────────────────┐
  │   Task      │ ─────────────────► │   Prompt     │ ──────────► │   Research     │
  │ (incl. goal)│                    │ (traces +    │             │ (results +     │
  │ • criteria  │                    │  tool calls) │             │  reflection)   │
  │ • gate-tool │ ◄──── gate ───────────────────────────────────  │                │
  │ • subtasks  │  (PASS / replan / re-synth / spawn followup)    │                │
  └─────┬───────┘                                                 └────────────────┘
        │
        ├─► meta/plans/<NNN>/        (plan document for this task/subtask)
        └─► meta/workspace/<NNN>/    (scratch space mirroring the plan number)
```

---

## Open questions for Round 7 (asked via AskUserQuestion)

1. The cut-off sentence — *"each [Plan] can have one, but…"* — cardinality of Plan ↔ Prompt ↔ Research.
2. Subtask shape — pure decomposition vs. typed (work-subtask / tooling-subtask).
3. Validation-tooling form — Gherkin-runner, custom script, JSON-Schema assertion, or reviewer-subagent.
4. (Held for later round) MCP-numbering server: global vs. per-kind vs. hierarchical ID space.

---

## Not-yet-resolved (will be folded in later rounds)

- **Bootstrap budget mechanism.** How the agent is mechanically held to `<8K` tokens before deferring further reads. Candidate: a `bootstrap.md` that is the *only* required read, with all other specs lazy-loaded via a manifest.
- **Migration mechanics.** What happens to the 96 existing tasks / 77 prompts / 30 research workspaces — re-numbered through the MCP dispenser, or left at their current numbers with new artefacts starting from a fresh high-water mark?
- **Skill corpus fate.** 76 skills currently in `skills/`. Keep all, prune, restructure under the new four-layer model?
- **Initial goal seeding.** Which existing top-level concerns become the seed `task_kind: goal` parents?
- **Pre-commit / hook re-wiring.** `tools/check-governance.sh`, `tools/check-hooks.py`, and the five D.7-compliant hooks all need to be aware of the new layout (especially `meta/` and the MCP-dispensed IDs).

---

## Verification (will be filled in once the plan is final)

*Placeholder — verification steps depend on the unresolved questions above. Will include:*
- Dry-run migration of the existing 96 tasks through the MCP dispenser.
- `tools/check-governance.sh` passes against the new layout.
- A round-trip test: create a goal-task → spawn subtasks → execute prompts → close research → gate fires → demonstrate a PASS path and a FAIL-with-resynth path.
- Skill-tool invocation telemetry (`skill-invocation-log.md`) continues to land in the right place under the new `meta/` structure.

---

*This file is the **only** file being edited during plan-mode iteration. All other repository state remains untouched until the user explicitly approves the final plan via ExitPlanMode.*
