# Round 10 additions — Goal-only initial Task, decomposition workflow

> **Status:** Locks A/B/C/D ratified. One open question (decompose-goal SKILL) carries into Round 11. Round 11 is paused pending Gemini Deep Research output — see [`../research-prompts/gemini-deep-research-agency-refactor.md`](../research-prompts/gemini-deep-research-agency-refactor.md) and [`../research-prompts/gemini-deep-research-bootstrap-context-engineering.md`](../research-prompts/gemini-deep-research-bootstrap-context-engineering.md).
> **Parent plan:** [`agency-refactor-plan.md`](./agency-refactor-plan.md).

---

## The insight (Round 10)

A new initial Task may carry **only a goal** — no acceptance criteria, no gate-tooling. The decomposition itself becomes the first wave of work:

1. **Task[goal-only]** — frontmatter: `task_kind: goal`, `task_phase: undecomposed`. Body contains just the goal statement, no Gherkin scenarios yet.
2. **First Prompt[decompose]** — its job is to read the goal and propose a decomposition into N candidate subtasks. Frontmatter: `prompt_kind: decomposition`.
3. **Research[explore decomposition]** — runs the prompt; `output/` carries candidate subtask drafts; `reflection/` notes alternatives considered.
4. **Synthesis step → spawns subtasks.** The synthesis pass crystallises candidate subtasks into proper Task artefacts, each with their own goal + criteria + gate-tooling.
5. **Parent Task evolves.** Once subtasks exist, the parent transitions `task_phase: decomposed` and gains derived acceptance criteria: *"all subtasks PASS their gates"*.

---

## Layer-model deltas

| Layer | New field | Values |
|---|---|---|
| Task | `task_phase` | `undecomposed`, `decomposed`, `ready-to-execute`, `closed` |
| Task | `task_depends_on` | list of Task IDs (DAG, no cycles) — declares sibling-subtask ordering |
| Prompt | `prompt_kind` | `decomposition`, `execution` |
| Research | `research_mode` | `decomposition-synthesis`, `execution-synthesis` |

### Lock A — Gherkin for goal-only Tasks (deferred-write)
- A Task in `task_phase: undecomposed` has **NO Gherkin** at creation time. The Gherkin field is absent (not empty `(none)`, not a placeholder — genuinely not present).
- The **decomposition-synthesis step writes the parent's Gherkin** after subtasks have been spawned. Default written form: `Given <goal>, When all subtasks PASS their gates, Then the goal is achieved.` Synthesis may write richer scenarios when the decomposition produces structure worth gating.
- Linter enforces a phase-conditional rule: `Gherkin REQUIRED iff task_phase ∈ {decomposed, ready-to-execute}`. While `undecomposed`, the linter accepts absence.

### Lock B — No-decomposition-needed (direct promotion)
- If decomposition concludes the goal IS a single concrete unit, the parent Task transitions **directly to `task_phase: ready-to-execute`** (skipping `decomposed`).
- Decomposition-synthesis writes the Gherkin + gate-tooling for the goal itself. No trivial subtask is spawned. Same Task, no ceremonial duplication.
- This is why `task_phase` has 4 values, not 3: `undecomposed` → `decomposed` (spawned ≥1 subtask) **OR** `ready-to-execute` (synthesis upgraded in place) → `closed`.

### Lock C — Subtask IDs (full MCP + parent-relative SemVer)
- Each subtask gets its own **MCP-dispensed Task ID** (e.g. parent is Task 042, subtask is Task 087, fully independent address).
- Each subtask ALSO carries a **parent-relative SemVer coordinate** in frontmatter: `task_parent_semver: 042/1.1.0`.
- Both addressing schemes are queryable: cross-Task tooling uses MCP IDs; parent's amendment-trail rendering uses the SemVer coordinate.
- Frontmatter on a subtask: `task_parent: 042`, `task_parent_semver: 042/1.1.0`, `task_kind: execution` (or further `goal` for recursive decomposition).

### Lock D — Subtask ordering (explicit DAG)
- Each subtask declares dependencies via `task_depends_on: [<MCP-id>, ...]` in frontmatter.
- Decomposition-synthesis records the DAG when it spawns subtasks. Empty list = independent.
- Gate-tooling evaluates **partial PASS in topological order**: a subtask's gate runs only after all its dependencies have PASSed.
- Schema invariant: `task_depends_on` MUST NOT contain cycles. Linter walks the graph; cycles fail at pre-commit.

---

## SemVer interaction

Composes cleanly with the Round 9 SemVer scheme:

- **Initial goal-only Task** = `1.0.0`
- **First decomposition pass produces subtasks** — each subtask is a **MINOR** bump on the parent: `1.1.0`, `1.2.0`, `1.3.0`, …
- **Each subtask is itself a Task** with its own SemVer namespace. Subtask `1.1.0-validator` (parent's view) is internally `validator/1.0.0`, may evolve to `validator/1.0.1`, `validator/1.1.0`, etc.
- **Major bump on parent** (`2.0.0`) = original goal got fundamentally redesigned, invalidating the prior decomposition.

Folder layout (extending Round 9):
```
tasks/042/
├── task.md                                  # goal-only, semver: 1.0.0, task_phase: undecomposed
├── plan/                                    # initial plan: "decompose"
├── amendments/
│   ├── 1.1.0-subtask-validator/             # first subtask spawned by decomposition synthesis
│   │   ├── task.md                          # full Task: goal + criteria + gate-tooling
│   │   └── amendments/                      # subtask has its own amendment trail
│   │       └── 1.0.1-replan/
│   ├── 1.2.0-subtask-migration-runner/      # second subtask
│   └── 1.0.1-goal-clarified/                # patch: parent's goal statement tightened
└── readme.md
```

---

## Question status (Round 10)

**Closed (4 locks):**
| ID | Question | Lock |
|---|---|---|
| A | Gherkin for goal-only Tasks | Deferred-write by synthesis step; phase-conditional linter rule |
| B | No-decomposition-needed case | Direct promotion to `ready-to-execute`; no trivial subtask spawned |
| C | MCP ID semantics for subtasks | Full MCP ID + parent-relative SemVer; both addressable |
| D | Cross-subtask ordering | Explicit DAG via `task_depends_on`; topological gate evaluation |

**Still open (carries into Round 11, currently paused):**
- **Decomposition prompts as a first-class SKILL.** Candidate: `decompose-goal` skill that defines (a) the decomposition prompt template, (b) the JSON Schema for decomposition output (must list candidate subtasks with `name`, `parent_relative_semver`, `depends_on`), (c) rules for when to recurse (when does a spawned subtask itself become a goal-only Task that needs its own decomposition?), and (d) the no-decomposition-needed escape hatch.
