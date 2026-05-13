# Agency Repo Refactoring Plan (Working Draft)

> **Status:** Iterative requirements capture — Round 7 closed. Round 8 pending. Not yet finalised.
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
- **Meta scope (revised in Round 7).** `meta/` is **maintenance-only** — NOT the Round-6 kitchen-sink. It carries per-aspect reasoning workspaces that analyse accumulated artefacts and may spawn new Tasks. Layout:
  ```
  meta/
  ├── tasks/      # cross-task pattern analysis, anti-patterns, improvement proposals
  ├── prompts/    # accumulated trace analysis (feeds prompt-optimizer skill)
  ├── research/   # synthesis-pattern audit, gap detection across closed workspaces
  └── runs/       # maintenance-run logs and digests
  ```
  Plans, friction logs, session traces, code reviews now live **adjacent to their owning artefact** (inside `tasks/<NNN>/`), not centralised under `meta/`. Only meta-initialized maintenance Tasks may write `meta/`.
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

### Subtasks — Tasks may have many (Round 7 answer)
- **Pure decomposition** is the basic shape. A parent Task (often a `task_kind: goal`) decomposes into **N subtasks**.
- Each Task/subtask has its own **Plan directory inside the Task folder** (`tasks/<NNN>/plan/`), NOT under `meta/`.
- `meta/` is reserved for maintenance Tasks that reason across many closed Tasks/Prompts/Research workspaces.

### Cardinality (Round 7 answer)
- **Main triple is paired 1:1:1:** one Task ↔ one Prompt ↔ one Research workspace at the canonical level. Main synthesis lives there and stays canonical.
- **Sub-numbered amendments** capture subtasks, prompt updates, and research re-syntheses. These are self-reflective loops that **feed back into the main triple** — they do not replace it.
- The audit graph: `task.md` ← amendment trail ← (sub)prompt updates ← (sub)research re-syntheses ← back into main synthesis.

### Audit-trail layout (Round 8 lock)
- **Amendment folders inside main:**
  ```
  tasks/042/
  ├── task.md                       # canonical mission
  ├── plan/                         # plan for this task
  ├── amendments/
  │   ├── 001-replan/               # plan revision
  │   ├── 002-subtask-validator/    # decomposed subtask
  │   └── 003-research-resynth/     # re-synthesis loop
  └── readme.md
  prompts/042/
  ├── prompt.md
  ├── brief.md
  ├── traces/                       # tool-call session traces (feeds prompt-optimizer)
  ├── amendments/
  │   └── 001-revised-instructions/
  └── readme.md
  research/042/
  ├── output/
  ├── synthesis/
  ├── reflection/
  ├── amendments/
  │   └── 001-resynth/              # tighter synthesis of same evidence
  └── readme.md
  ```
- Each amendment carries its own L1+L2 frontmatter (`type: amendment`, `amendment_kind`, `amendment_of`).

### Gate-tooling matrix (Round 7 answer)
For every Task's validation tooling, mandatory baseline + conditional layers:

| Layer | Mandatory? | When applied |
|---|---|---|
| **Gherkin scenarios** (acceptance criteria) | **Yes — always** | Every Task. Bar Research must clear. |
| **JSON Schema assertions** (artefact shape) | **Yes — always** | Every artefact (Task, Prompt, Research, amendment) validated against its schema. |
| **Custom validator scripts** | **No — only for meta-initialized maintenance Tasks** | Forbidden for regular Tasks. Available when meta spawns a tooling-update Task. |
| **Reviewer subagent (code-reviewer / prose reviewer)** | **No — conditional** | When output is code, prose, or otherwise mechanically ungateable. |

### Schema overflow channel (Round 8 lock)
- Every schema carries a top-level **`overflow:` frontmatter key** — a free-form mapping for information that doesn't fit the canonical schema yet.
- Meta-runs grep non-empty `overflow:` blocks across artefacts → cluster patterns → propose schema upgrades (and may spawn schema-evolution Tasks).
- Linter behaviour: non-empty `overflow:` is permitted (it's the whole point) but **WARNs after N days** to ensure overflow doesn't become a permanent dumping ground.
- Schema-evolution flow: overflow accumulates → meta notices → meta asks user → user confirms → schema gains canonical key → meta spawns migration Task → overflow keys drain.

---

## Working layer model (post-Round 8)

```
Global ID dispenser (MCP service)
        │
        ▼
  ┌─────────────┐  task_uses_prompts ┌──────────────┐ executed-by ┌────────────────┐
  │   Task <NNN>│ ─────────────────► │ Prompt <NNN> │ ──────────► │ Research <NNN> │
  │ • goal      │   (1:1 pairing)    │ • body       │  (1:1)      │ • output       │
  │ • Gherkin   │                    │ • brief      │             │ • synthesis    │
  │ • Schema    │                    │ • traces ────┼──► prompt-  │ • reflection   │
  │ • plan/     │                    │ • amendments │   optimizer │ • amendments   │
  │ • amendments│ ◄──── gate ──────────────────────────────────── │                │
  └─────┬───────┘  (PASS / replan / re-synth / spawn-followup)    └────────────────┘
        │
        │  PASS  → research becomes T4-immutable
        │  FAIL  → amendment loop (replan | re-synth | new-followup Task)
        │
        ▼
   meta/{tasks,prompts,research,runs}/  (maintenance-only; reasons across closed artefacts)
```

Every artefact's frontmatter carries an `overflow:` channel that meta-runs harvest to propose schema upgrades.

---

## Closed questions

**Round 7:**
1. Cardinality → **1 Task : 1 Prompt : 1 Research at main level; sub-numbered amendments loop back to main.**
2. Subtask shape → **Pure decomposition; meta/ is maintenance-only.**
3. Gate tooling → **Gherkin + JSON Schema mandatory; custom validators only for meta-init Tasks; reviewer subagent for code/prose.**

**Round 8:**
4. Audit-trail layout → **Amendment folders inside main artefact** (`<NNN>/amendments/<NNN>-<slug>/`).
5. Overflow channel → **Top-level `overflow:` frontmatter key**, machine-harvestable by meta.
6. Layer-name renames (tasks→missions etc.) → **Deferred** until after meta/ refactor lands.

## Open questions for Round 9

1. **MCP numbering server design** — single global counter vs. per-kind counters (`task_id`, `prompt_id`, `research_id`) vs. hierarchical (`042.amendments.003`). Sequence reservation semantics for parallel branches.
2. **Bootstrap budget mechanism** — how is the agent mechanically held to <8K tokens before deferring? Candidate: a `bootstrap.md` as the only mandatory read, with all other specs lazy-loaded via a manifest.
3. **Migration mechanics** — what happens to the 96 existing tasks / 77 prompts / 30 research workspaces? Re-numbered through the MCP dispenser, or grandfathered at current numbers with new artefacts starting from a fresh high-water mark?
4. **Initial goal seeding** — which existing top-level concerns become the seed `task_kind: goal` parents under the new layout? (Candidate list will need user nomination.)

---

## Held items (still unresolved, deferred past Round 9)

- **Skill corpus fate.** 76 skills currently in `skills/`. Keep all, prune, restructure under the new four-layer model?
- **Pre-commit / hook re-wiring.** `tools/check-governance.sh`, `tools/check-hooks.py`, and the five D.7-compliant hooks need to be aware of the new layout (amendment folders, `overflow:` keys, MCP-dispensed IDs).
- **Layer renames** (deferred — revisit after meta/ refactor lands).

---

## Verification (will be filled in once the plan is final)

*Placeholder — verification steps depend on the unresolved questions above. Will include:*
- Dry-run migration of the existing 96 tasks through the MCP dispenser.
- `tools/check-governance.sh` passes against the new layout.
- A round-trip test: create a goal-task → spawn subtasks → execute prompts → close research → gate fires → demonstrate a PASS path and a FAIL-with-resynth path.
- Skill-tool invocation telemetry (`skill-invocation-log.md`) continues to land in the right place under the new `meta/` structure.

---

*This file is the **only** file being edited during plan-mode iteration. All other repository state remains untouched until the user explicitly approves the final plan via ExitPlanMode.*
