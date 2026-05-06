# Task 030 — Notes

> Running scratchpad. Three sections, in this order:
> 1. **Assumption Log** — every choice the planner made that a downstream agent could reasonably challenge, plus the rationale.
> 2. **Inventory of corruption** — the concrete numbers behind §Goal #1 of the task; this is the baseline `cleanup.py --check` is graded against.
> 3. **Planning-Session Frustration Log (verbose, per user request)** — the meta-friction encountered while AUTHORING this task. Not the same as `friction-log.md`, which records the friction of EXECUTING it. The user explicitly asked for verbosity here so Task 027's research can extract pattern requirements.

---

## 1. Assumption Log

Format: `**A-N.** Assumption.` followed by *Rationale.* + *What would invalidate.*

### A-1. The dramatica corpus corruption is mostly OCR / PDF-extract residue, not author-introduced semantic drift.

*Rationale.* Spot-checks across `character-dynamics.md`, `elements.md`, `dramatica-terms.md` show consistent pattern: copyright-footer + page-number lines exactly where a PDF page would have broken, double-apostrophe escapes (`one''s`) exactly where a CLI quote-escape would have run, leading `>` characters on bullet entries that match a Phillips/Huntley dictionary's bullet style. Task 015's `notes.md §Plan Step 5` explicitly describes the source as "OCR-bereinigt" — meaning a partial cleanup happened upstream but did not finish.

*What would invalidate.* Finding a corruption that maps to an author choice (e.g., a deliberately-empty entry referenced by a working SKILL.md path). ST-2 and ST-4 carry that audit explicitly; if either subtask reports the corruption is intentional, the task's §Goal #1 contracts to "structural artefacts only".

### A-2. The 17 partial-quad-membership warnings from Task 015 are NOT in scope here.

*Rationale.* Task 015's friction log marked them as "documented v0.1 limitation; resolution OQ-X requires a `quad_ids: array` schema bump that breaks existing tooling." A schema bump is a Task-027-class decision (ADR-governance scope), not a clean-up-the-data-we-have decision.

*What would invalidate.* If `tools/dramatica-nav/cleanup.py` cannot be authored without resolving the quad question (e.g., because `cleanup.py` walks the ontology and trips over partial quads). ST-6's brief says "warnings, not errors", which sidesteps this. If the author finds otherwise, ST-6 emits a friction event and Task 027 fast-tracks OQ-X.

### A-3. New tooling lives under `tools/dramatica-nav/`, not `tools/fm/`.

*Rationale.* `tools/fm/` is the Frontmatter Ontology toolchain (Tasks 016–023). `tools/dramatica-nav/` is the Narrative Ontology toolchain (Task 015). [AGENTS.md § Narrative Ontology rule NO.5](../../AGENTS.md) explicitly forbids cross-loading. Putting alias-loading or term-editing into `tools/fm/` would either break NO.5 (tool loads narrative ontology in non-narrative work) or duplicate `tools/fm/_core.py` helpers.

*What would invalidate.* If a Task-027 ADR ratifies a "single canonical CLI" pattern (`fm` wrapper is already in flight per Task 019). Then `tools/dramatica-nav/` should expose its commands as a sub-namespace under `fm` (e.g., `fm dn term …`) rather than as a standalone CLI. ST-5/ST-6/ST-7 keep their scripts importable, so this refactor is mechanical.

### A-4. `/sc:agent` is the right dispatcher for these subtasks.

*Rationale.* Task 019 establishes the precedent — nine subtasks dispatched via `/sc:agent` in two phases, with `isolation: "worktree"` for code-touching subtasks and main-tree for markdown-touching ones. The same shape fits this task's nine subtasks.

*What would invalidate.* If Task 027 surfaces evidence that `/sc:agent` worktree-mode is unstable (orphaned branches, merge conflicts, …) at high concurrency. Mitigation: Phase A only fans out 4 subtasks in parallel; Phase B fans out 3; Phase C is sequential. No phase exceeds the concurrency Task 019 demonstrated successfully.

### A-5. The provisional subtask format follows Task 019's convention.

*Rationale.* No canonical "subtask spec" exists in the repo (this is part of why Task 027 exists). Task 019's `subtasks/<NN>-<name>.md` layout — frontmatter + Goal + Falsification + Inputs + Acceptance + Dependencies + Agent Prompt — is the most-recent and most-load-bearing precedent. Copying it preserves the audit graph.

*What would invalidate.* Task 029's audit output could ratify a different shape (e.g., requiring a Pre-Mortem section, or a different agent-prompt embedding format, or a normative statement on whether `# anchor:`-style stable IDs apply at the subtask level). The task body explicitly flags subtask format as PROVISIONAL.

### A-6. Sub-prompt format = subtask file's "Agent Prompt" code block, copy-pasted into `/sc:agent`.

*Rationale.* Same source as A-5: Task 019 uses this pattern. The agent-prompt block is verbatim copy-pasteable; subagents do not see this conversation, so the prompt must be self-contained per [PROMPT.md §5](../../PROMPT.md).

*What would invalidate.* The renderer pattern from `research-prompt-optimizer v3.2.0` (visible in [`/prompts/agency-adr-governance-spec/prompt.md`](../../prompts/agency-adr-governance-spec/prompt.md)) is a more rigorous self-containedness contract — with constraint blocks, methods, and reflection checkpoints. Subtask agent-prompts are LIGHTER than that because they're code-implementation tasks, not research extractions. Task 027's output should explicitly state when the heavier rendering is required and when the lighter Task-019 pattern suffices.

### A-7. The 106 "unmapped headings" are NOT all candidates for ontology entries.

*Rationale.* `validate.py`'s `unmapped-heading` warning is mechanical: a `## ` heading exists in source but no ontology entry's `term_file` points to its slug. Task 015's `notes.md §Plan Step 5` already partitioned them roughly: ~50 are intro/explainer sub-headings, ~30 are throughline-specific slot specialisations ("Female Mental Sex", "Impact Character Concern"), ~25 are mismatched anchors. Only the third bucket needs ontology IDs. The first bucket is structural prose (legitimate `## ` headings inside `essential-questions.md`, `encoding-patterns.md`, etc.). The second bucket is exactly what kind: concept is for. ST-3 reproduces this partition.

*What would invalidate.* If the partition turns out to need a fourth bucket — e.g., terms that ARE canonical Dramatica entries but were missed during Task 015's bootstrap (similar to the 5-missing-canonical-entities fix Task 015 §Plan Step 4 made). ST-3's brief asks the subagent to flag any such terms explicitly so the schema bump cost is visible.

### A-8. Precompiled persona-scenario JSONs are an additive layer, not a replacement.

*Rationale.* The Task 015 navigator (`nav.py by-scenario`) already supports scenario-keyed lookup. The precompiled JSONs are a denormalised projection — same data, structured for the consumer's convenience. Token cost should be measurably lower; if it isn't, the layer is redundant (covered by ST-9's falsification clause).

*What would invalidate.* If the consumer (`novel-architect`, `ncp-author`) prefers calling `nav.py by-scenario` programmatically instead of loading a JSON file (e.g., because the JSON file forces a load of all 11 scenarios when only one is needed). ST-9's brief calls for ONE JSON per scenario specifically to avoid this — agents load only the scenario they're working on.

### A-9. German aliases are seeded for top-50 high-frequency terms only, not exhaustively.

*Rationale.* Task 015's friction log called DE-locale coverage "currently EN-only; DE substitution used for NO.1.2", implying a partial DE coverage was intentional v0.1 scope. The `dramatica-vocabulary` SKILL.md is in German, so SOME DE aliases are critical (Hauptfigur, Vertrauen, Wandel, Wendepunkt, Akt, Charakter, Element, Klasse, Variation), but exhaustive translation of 304 entries is a Translation-Task scope, not a Cleanup-Task scope.

*What would invalidate.* If the German-speaking persona (Anna in Task 015) actually queries by terms beyond the top-50 in real sessions. Lacking that evidence, ST-7 ships the top-50 starter set; the rest grow on demand via `tools/dramatica-nav/aliases.py add`.

### A-10. The Frustration Log in `notes.md` is verbose by design and stays verbose.

*Rationale.* The user's literal request: *"please… be verbose in your Frustration log"*. This is the planning-session friction; trimming it would lose the pattern data Task 027 needs.

*What would invalidate.* If `tools/check-governance.sh` rejects the file size or breadth. The frontmatter-validator pattern doesn't rate-limit body content, and the file is <40K, so this should be safe — but if a future linter does, the resolution is to FILE A FRICTION EVENT in Task 027's research, not to trim this log.

---

### A-11. Task 028 dependency is encoded per-subtask, NOT as `task_blocked_by` on the parent task.

*Rationale.* Per [PR #55 review C1](https://github.com/netzkontrast/agency/pull/55), only ST-5 and ST-6 actually need `agency-adr` from Task 028; ST-1…ST-4 + ST-7…ST-9 are independent. Setting `task_blocked_by: ["028"]` at the parent level would serialise all nine subtasks behind the ADR work for no benefit, blocking Phase A's low-risk high-value cleanup. Instead, ST-5 and ST-6 carry a **Pre-dispatch Gate** clause in their `## Dependencies` section that the dispatching agent MUST honour.

*What would invalidate.* If a future audit-graph linter requires `task_blocked_by` to be populated whenever ANY subtask declares an inter-task dependency, this convention would need to flip back to task-level. Mitigation: A-11 is a candidate input to main's [Task 029 assumption audit](../../029-adr-assumption-audit/) — that task's spec output decides whether per-subtask gating is the canonical pattern or whether task-level is mandated.

## 2. Inventory of Corruption (Baseline for §Goal #1)

These numbers are the baseline `tools/dramatica-nav/cleanup.py --check` (delivered by ST-6) is graded against. Measured by direct grep over `skills/dramatica-{theory,vocabulary}/references/*.md` during the planning session.

### 2.1 PDF page-break footers — `Copyright (c) 2001 Screenplay Systems Inc.`

| Path | Hits |
|---|---:|
| `skills/dramatica-vocabulary/references/character-dynamics.md` | 3 |
| `skills/dramatica-vocabulary/references/dramatica-terms.md` | 2 |
| `skills/dramatica-vocabulary/references/elements.md` | 8 |
| `skills/dramatica-vocabulary/references/types.md` | 3 |
| `skills/dramatica-vocabulary/references/variations.md` | 5 |
| `skills/dramatica-vocabulary/references/plot-dynamics.md` | 6 |
| `skills/dramatica-vocabulary/references/overview-appreciations.md` | 6 |
| `skills/dramatica-vocabulary/references/structural-terms.md` | 2 |
| `skills/dramatica-vocabulary/references/archetypes.md` | 1 |
| `skills/dramatica-vocabulary/references/domains.md` | 1 |
| `skills/dramatica-vocabulary/references/plot-structures.md` | 1 |
| **Vocabulary subtotal** | **38** |
| `skills/dramatica-theory/references/*.md` | 0 |
| **Total** | **38** |

### 2.2 Page-number-only lines — `^[0-9]+\.\s*$`

| Path | Hits |
|---|---:|
| `skills/dramatica-theory/references/01-foundations.md` | 6 |
| `skills/dramatica-theory/references/02-characters.md` | 51 |
| `skills/dramatica-theory/references/03-deep-theory.md` | 11 |
| `skills/dramatica-theory/references/04-theme.md` | 36 |
| `skills/dramatica-theory/references/05-plot-genre.md` | 25 |
| `skills/dramatica-theory/references/06-storyforming.md` | 45 |
| `skills/dramatica-theory/references/07-storyencoding.md` | 33 |
| `skills/dramatica-theory/references/08-storyweaving-reception.md` | 39 |
| `skills/dramatica-theory/references/09-reference.md` | 78 |
| **Theory subtotal** | **324** |
| `skills/dramatica-vocabulary/references/*.md` | mixed in with §2.1 footers (≈38 paired) |

### 2.3 Double-apostrophe escapes — `''`

```
domains.md:1, character-dynamics.md:1, plot-dynamics.md:1
types.md:2, elements.md:2, variations.md:1
```

Total: **8**. These are CLI quote-escape artefacts; one for one each maps to an `'s` possessive that should not have been double-quoted.

### 2.4 Broken-parenthesis headings

```
skills/dramatica-vocabulary/references/character-dynamics.md:392:## Sex)
```

**1 occurrence.** Originated from `## Mental Sex` or `## (Mental Sex)`-style header that lost its prefix during a bulk edit; ST-2 repairs to either `## Mental Sex` (canonical) or deletes if `## Mental Sex` already exists elsewhere in the file.

### 2.5 "See X" empty redirect entries

```
character-dynamics.md:## Female Mental Sex / body: "See Intuitive Problem Solving Style"
character-dynamics.md:## Male Mental Sex   / body: "See Logical Problem Solving Style"
character-dynamics.md:## Sex)              / body (truncated, see §2.4)
elements.md (line 22):- [Direction (Overall Story Throughline)](#direction-overall-story-throughline) — See
elements.md (line 31):- [Focus](#focus) — See Symptom
```

**5 occurrences total.** ST-4's brief partitions them into "delete + alias on canonical" vs. "reify with substantive prose" decisions per case. The first two are textbook redirect-only entries (the canonical exists at `character-dynamic.problem-solving-style`). The last two are bullet-list cross-references (TOC entries) and resolve when the body of `## Direction` and `## Focus` is corrected.

### 2.6 Mis-attributed YAML — frontmatter on the wrong heading

```
character-dynamics.md (line 21–30):
  ## Approach
  <!-- nav-ontology … -->
  ```yaml
  id: character-dynamic.growth      ← Growth, not Approach
  canonical_label: Growth
  ```
```

**1 known occurrence.** The Approach heading carries Growth's frontmatter; Growth has no heading of its own. Both ontology entries (`character-dynamic.approach` AND `character-dynamic.growth`) already exist and BOTH currently have `term_file` pointing at the same `character-dynamics.md#approach` anchor. `validate.py` doesn't surface this as `term_file-anchor-mismatch` because the anchor DOES exist (the lint can't detect that a YAML block sits under the wrong heading).

ST-2's brief covers this; the fix is splitting `## Approach` into `## Approach` (with its own correct YAML for `character-dynamic.approach`) and a new `## Growth` heading carrying the `character-dynamic.growth` YAML. ST-3 then updates `character-dynamic.growth.term_file` from `...#approach` to `...#growth` so the ontology table tracks the new anchor.

### 2.7 `term_file` anchor mismatches (8 from `validate.py`)

```
concept.archetype       → archetypes.md#contents          (anchor exists but is a TOC, not a term)
el.ability              → elements.md#ability             (heading not found — Ability missing as ## entry)
el.change               → elements.md#change              (heading not found)
el.non-acceptance       → elements.md#non-acceptance      (heading not found)
el.non-accurate         → elements.md#non-accurate        (heading not found)
type.subconscious       → types.md#subconscious           (heading not found)
var.self-interest       → variations.md#self-interest     (heading not found)
var.work                → variations.md#work              (heading not found)
```

ST-3 partitions: missing canonical entries are real (Ability, Change, Non-acceptance, Non-accurate — all referenced in Task 015's Plan Step 4 merge fix #3). The fix is minting the headings AND moving / renaming when canonical name differs. `concept.archetype → archetypes.md#contents` is a special case — the entry's intent was "the meta-concept of an Archetype" but it landed on the Table of Contents heading.

### 2.8 Unmapped headings (106 from `validate.py`)

Partition (rough, from Task 015 §Plan Step 5):
- ~50 explainer sub-headings inside extension files (`Why Quads matter for Encoding`, `The KTAD Pattern — every Quad is the same fractal`, `Phase 1 — Throughline Class assignments`, etc.) — these are NOT terms; they're chapter sections inside extension prose.
- ~30 throughline-specific slot specialisations (`Female Mental Sex`, `Impact Character Concern`, `Dividend (Overall Story Throughline)`) — kind: concept candidates.
- ~25 anchor-format mismatches that resolve when ST-3 fixes §2.7's eight + the natural renaming in §2.6.

ST-3's deliverable is the partition table itself, not a 106-row index.

### 2.9 Alias coverage gap

```
Total entries:                     304
Entries with any aliases:            9 (3.0%)
Entries with aliases_en:             9 (3.0%)
Entries with aliases_de:             0 (0.0%)
Total alias strings:                14
```

ST-7 closes the EN gap from `_synonym-lookup.md` (~512 alias rows). DE starter set per A-9. Target after ST-7: ≥250 entries with aliases_en, ≥50 with aliases_de.

### 2.10 Scenario coverage gap

```
Total entries:                     304
Entries with ≥1 scenario:           85 (27.9%)
Entries with no scenarios:         219 (72.1%)
Median scenarios per tagged term:    1
Mean scenarios per tagged term:      1.59
```

ST-8 brings coverage up; target ≥250 entries with ≥1 scenario, median ≤4, max ≤8 (schema cap).

---

## 3. Planning-Session Frustration Log (Verbose, Per User Request)

> **Scope clarifier.** This log records friction encountered while AUTHORING this task. The file `friction-log.md` (currently absent) records friction encountered while EXECUTING it. The user explicitly asked for *verbose* meta-friction here so a downstream Task 027 reader can extract pattern requirements. Verbosity is the point.

**Highest Frustration Level reached during planning: FL2** (Significant Frustration — see FE-3 + FE-7 below). Net plan stable; no FL3 blockers.

### FE-1 (FL1, Minor) — No canonical "subtask file" template exists.

**What happened.** When breaking the cleanup work into nine subtasks, I needed a per-subtask file template covering: briefing for an out-of-context subagent, inputs (file paths + line numbers), acceptance criteria, falsification clause, dependencies, recommended subagent type, and agent-prompt block ready for `/sc:agent` consumption. The repo has no such template under `/templates/` and no SPEC under `/research/` or `/maintenance/`.

**Workaround.** Reverse-engineered Task 019's `subtasks/<NN>-<name>.md` files; they collectively encode an implicit format. Copied the structure verbatim.

**Risk this incurs.** If Task 027 ratifies a different layout, every subtask file under `tasks/030-cleanup-dramatica-skills-corpus/subtasks/` re-renders. That is an entirely mechanical edit but it WILL produce a noisy commit. Better outcome: ratify Task 019's pattern AS the canonical template before Task 030 dispatches; freeze it.

**Pattern this exposes.** The repo has L1+L2 frontmatter ontologies for tasks/prompts/research but NOT for subtasks. A subtask is not a Task (no own task_id), not a Prompt (it doesn't live in `/prompts/`), and not a Research artefact. Where does it sit? Task 027 needs to answer this.

**Suggested rule for Task 029 to ratify.** Subtasks are L2.1 artefacts under their parent Task. They MUST carry an L2.1 namespace (`subtask_id`, `subtask_status`, `subtask_recommended_agent`, `subtask_phase`, `subtask_depends_on`, `subtask_falsification`). They MUST live under `<parent-task-folder>/subtasks/<NN>-<slug>.md` and MUST NOT have their own folder.

### FE-2 (FL1, Minor) — `/sc:agent` invocation syntax is undocumented in the repo.

**What happened.** Task 019 references `/sc:agent` extensively but doesn't say how to invoke it. Is it a literal CLI command (`/sc:agent --type python-expert <prompt-file>`)? A SuperClaude slash-command typed into the agent UI? A prompt-side directive the agent recognises? The repo's PRE_COMMIT.md / AGENTS.md mention `/sc:createPR` as a slash-command invoked at session close, suggesting `/sc:agent` is the same shape — but there's no normative statement.

**Workaround.** Wrote the cleanup task's Plan section assuming `/sc:agent` is the same shape as the harness's `Agent` tool (with `description` / `subagent_type` / `prompt` / optional `isolation`). Copied Task 019's parallel-spawn recipe verbatim.

**Risk this incurs.** If `/sc:agent` is actually a different surface (e.g., it triggers a remote SuperClaude container with different worktree semantics), the task's Phase A "single message containing four Agent calls" is wrong.

**Pattern this exposes.** The repo treats `/sc:*` commands as opaque magic — they appear in task plans and friction logs but no spec describes them. Task 027 needs to either ratify `/sc:agent` as semantically equivalent to the harness `Agent` tool OR define it as a separate entity with its own contract.

**Suggested rule for Task 029 to ratify.** `/sc:agent` is the canonical dispatcher for subtasks. Its invocation surface MUST match the harness `Agent` tool's parameters (description / subagent_type / prompt / isolation / model). The subtask file's "Agent Prompt" block MUST be copy-pasteable into `/sc:agent`'s prompt parameter.

### FE-3 (FL2, Significant) — `task_status` mismatch between Task 015's `task.md` and `tasks/readme.md`.

**What happened.** Task 015's task.md frontmatter says `task_status: done`. But [tasks/readme.md line 43](../readme.md) says "Status: `in_progress`". This is a 2026-05-05 staleness window. When I tried to figure out whether to mark Task 030 as `task_blocked_by: ["015"]`, I had to read both, plus the friction log, plus Task 015's notes.md, to confirm: 015 IS done. The readme is stale.

**Workaround.** Trusted task.md (canonical per [TASK.md §3.1](../../TASK.md)). Marked Task 030 as `task_blocked_by: []` (Task 015's deliverables exist; no real blocker).

**Risk this incurs.** Other agents reading `tasks/readme.md` first will conclude 015 is `in_progress` and might pile work onto its branch instead of opening 026. Mitigation: this task's `links` section names 015 as predecessor and explicitly notes "Task 015's deliverables landed".

**Pattern this exposes.** Two-source-of-truth drift between an L0 frontmatter field and its denormalised mention in a parent index file. This is the EXACT failure mode Task 015 §Pre-Mortem item 1 ("Schema bloat") was supposed to prevent at the schema layer; it has reappeared at the readme-index layer. The repo needs a "tasks/readme.md is regenerated, not hand-maintained" linter (Task 023's mirror-divergence gate is the right precedent).

**Suggested rule for Task 029 to ratify.** `tasks/readme.md` MUST be regenerated from each `task.md`'s frontmatter at pre-commit (similar to `tools/fm/gen_schema_mirror.py` per Task 023). Manual edits to status fields in the readme are forbidden.

### FE-4 (FL1, Minor) — Renderer-emitted prompt has depth-2 YAML, breaking repo rule.

**What happened.** The user asked me to save a research prompt that was rendered upstream by `research-prompt-optimizer v3.2.0`. The renderer emits TWO YAML blocks at the top of the file: one with `provenance.{created,skill_version,…}` (depth-2 nesting), one with `cross_pollination[].{source_category,module,title}` (depth-2 list-of-objects). Both violate [AGENTS.md § YAML Depth Rule](../../AGENTS.md) (depth ≤ 1).

**Workaround.** Wrapped both renderer-emitted YAML blocks inside a fenced ```yaml code block in the body of `prompt.md` (preserving the renderer's verbatim output for traceability), and authored a fresh top-level YAML frontmatter that conforms to the repo's L1 + `prompt_*` namespace.

**Risk this incurs.** A future re-render produces a new renderer-emitted file; an agent that diffs the new render against this file's body will see the wrap-in-fenced-block as drift. The mitigation is brittle (manual re-wrap per render).

**Pattern this exposes.** The renderer's output schema is incompatible with the repo's frontmatter rule. Either the renderer needs to flatten its provenance metadata, OR the repo's rule needs an exception for renderer-produced documents (e.g., "renderer output is a Body Concern, not a Frontmatter Concern; the executing agent extracts what it needs at run-time").

**Suggested rule for Task 029 to ratify.** Renderer-produced prompts (any artefact bearing a `schema:` field naming a renderer schema) are exempt from the YAML-depth-1 rule for the renderer's metadata blocks ONLY when those blocks are wrapped inside a fenced code block in the body. The top-level frontmatter MUST still conform to the repo rule. This formalises the workaround above.

### FE-5 (FL1, Minor) — No clear contract for "task spawns prompts that are CONSUMED by ANOTHER task".

**What happened.** At planning time, Task 030 (then numbered 026) authored the `agency-adr-governance-spec` prompt as a follow-up deliverable for a then-also-planned Task 027 (`spec-subagent-subtask-prompt-format`). The TASK.md §3.3 description of `task_spawns_prompts` says: "Slugs of follow-up prompts generated by this Task". This raised the question of whether to mark the prompt as both "spawned by Task 030" AND "used by Task 027" — and noted no reciprocal field exists on the prompt itself for the spawner edge.

**Workaround (revised — see "Final decision" below).** The original draft set `task_spawns_prompts: ["agency-adr-governance-spec"]` on Task 030 to claim the spawn edge. **Final decision (post-merge with `origin/main`):** the prompt is now owned by main (a stub pointing at the externally executed Gemini run at `research/gemini/agency-adr-governance-spec/`), not authored on this branch. Task 030's `task_spawns_prompts` is therefore `[]`, and the FE-5 schema question — *how do we express "Task A spawns a prompt that Task B consumes" cleanly?* — remains open and is recorded for main's [Task 029 assumption audit](../../029-adr-assumption-audit/) to ratify. Per [PR #55 review S2](https://github.com/netzkontrast/agency/pull/55).

**Risk this incurs.** Audit-graph queries that walk "Task A spawned prompts → those prompts' consumers" cannot trace this branch's planning-time intent without reading FE-5's history here. The intent is preserved as documentation; the machine-readable graph reflects only the post-merge state.

**Pattern this exposes.** The audit-graph supports "Task uses Prompt" and "Task spawns Prompt" but treats them as orthogonal. In practice, "Task A spawns a Prompt that Task B uses" is a common pattern (this exact flow). The schema needs a `prompt_spawned_by_task` field to capture the third edge.

**Suggested rule for Task 029 to ratify.** Prompts SHOULD carry a `prompt_spawned_by_task` field when they were authored as a deliverable of a different Task than the one that consumes them. Reciprocity rules: if `prompt.prompt_spawned_by_task == X`, then `tasks/X/task.md` MUST list this prompt in `task_spawns_prompts`. If `prompt.prompt_relates_to_task == Y`, then `tasks/Y/task.md` MUST list this prompt in `task_uses_prompts` (existing reciprocity).

### FE-6 (FL1, Minor) — No spec for /sc: command lifecycle / which command does what.

**What happened.** Searching the repo for `/sc:` references surfaces them in 9 files but no central document. Task 015 used `/sc:improve --loop --iterations 3` for scenario tagging. Task 019 uses `/sc:agent` for subtask dispatch. AGENTS.md mentions `/sc:createPR` as the closing-run command. The README of agency-adr-governance-spec mentions the prompt is destined for `/sc:research` execution. No file says: "here is the full /sc: command set, here is what each does, here is when to invoke each".

**Workaround.** Inferred the command set from usage context: `/sc:agent` (subtask dispatch), `/sc:research` (research-prompt execution), `/sc:improve --loop` (iterative refinement), `/sc:test` (test runner), `/sc:cleanup` (lint/cleanup), `/sc:createPR` (closing). Each invocation in the cleanup task's Plan is justified inline.

**Risk this incurs.** If a `/sc:*` command works differently than expected, the task's plan misroutes work. Concrete unknown: does `/sc:improve --loop --iterations 3` count its iterations including the initial pass or only after-the-first? Task 015 used 3 iterations and produced 85 tagged terms; Task 030's ST-8 expects ~250 — does that mean 6 iterations? 9? Unknown until a Task-027 ADR settles it.

**Pattern this exposes.** `/sc:*` commands are part of the repo's working surface but not part of any spec under `/maintenance/` or `/AGENTS.md`. The closest thing to documentation is the SuperClaude Framework upstream URL in [AGENTS.md § Skill Provenance](../../AGENTS.md), but that points at one command (`createPR`) and not the rest.

**Suggested rule for Task 029 to ratify.** A new spec `maintenance/sc-command-spec.md` MUST enumerate every `/sc:*` command used in repo task plans, give each a one-paragraph description, list its expected parameters, list its expected outputs, and list which Task lifecycle phases SHOULD invoke it. This is the same shape `language-spec.md` takes for normative keywords.

### FE-7 (FL2, Significant) — Tension between user's "be verbose in your Frustration log" and the repo's general anti-verbosity discipline.

**What happened.** [FRUSTRATED.md § Special Triggers](../../FRUSTRATED.md) warns against "Structural Bloat / Micromanagement: deeply nested folder structures with less than 3 files per folder, or … tedious administrative overhead (e.g., updating a `readme.md` for every single minor file change *instead of batching them at the pre-commit stage*)". This frustration log is 200+ lines of meta-meta-friction. It's almost-by-definition the kind of overhead the repo wants to avoid.

But the user's literal request was *"please… be verbose in your Frustration log"*. And the user clarified upfront they want this exact verbose log to feed Task 027's research as raw material. So the verbosity IS the deliverable, not bloat.

**Workaround.** Honour the user's explicit instruction. Mark this section's verbosity as load-bearing in the task's `readme.md §Workflow Assumptions`. Note explicitly in [A-10](#a-10-the-frustration-log-in-notesmd-is-verbose-by-design-and-stays-verbose) that future coherence-pass agents must NOT trim it without consent.

**Risk this incurs.** A future linter may flag `notes.md` as "exceeds size budget" or "structural bloat". Mitigation: A-10 documents the consent.

**Pattern this exposes.** The repo's anti-bloat rule [FRUSTRATED.md § Special Triggers] does not have an exception for "intentional verbose record per user request". It would benefit from one.

**Suggested rule for Task 029 to ratify.** "Verbose-by-design" sections MUST be marked with a `@verbose-load-bearing` HTML comment at the top of the section, with a `since: <date>` and `requested-by: <user|agent>` attribute. Linters MUST NOT flag content inside such marks as bloat. (Or: the rule already doesn't apply to `notes.md` body content; the repo's existing tooling never flagged it; this entire sub-frustration is a paranoia event. A Task-027 ADR could state the rule explicitly to remove the paranoia.)

### FE-8 (FL1, Minor) — No clear precedent for "task that spawns a research-task that produces a spec that ratifies the parent task's own conventions".

**What happened.** Task 030 uses provisional conventions (subtask format / sub-prompt format / `/sc:*` usage) and explicitly ASKS Task 029 to ratify them. The repo has the `task_supersedes` / `task_superseded_by` pattern (Task 015 § friction log §Action Items references its three OQs as "can be standalone follow-up tasks") but the supersession pattern is for *Tasks* superseding *Tasks*. Here we have a *Task* spawning a *prompt* that drives a *research* whose output is a *spec* that retroactively binds the *Task*. Five layers, no canonical name.

**Workaround.** Authored both Task 030 and Task 027 in the same session. Task 030's `task.md §Anti-Patterns` says explicitly "MUST NOT treat the subtask format / sub-prompt format / /sc:* usage in this task as a precedent. They are PROVISIONAL pending Task 029's audit output." This pushes the "ratification" pattern into prose rather than into the audit graph.

**Risk this incurs.** A subagent reading Task 030's subtasks might assume the provisional conventions are normative because they LOOK like the rest of the repo's conventions. The Anti-Patterns line is one human-readable sentence; not a machine-checkable invariant.

**Pattern this exposes.** The repo doesn't have a way to mark a Task as "depends on a future spec that the current task itself surfaces the need for". This is exactly the M03 Pre-Mortem item Task 015 raised about "Cross-skill ontology drift" — but at a meta level (cross-task convention drift).

**Suggested rule for Task 029 to ratify.** A Task MAY declare `task_provisional_conventions: [list-of-convention-names]` in frontmatter. Each entry resolves to a section in [`maintenance/`](../../maintenance/) or to a future Task that will ratify the convention. While the convention is provisional, a linter MAY emit an advisory but MUST NOT fail.

### FE-9 (FL1, Minor) — Unclear cardinality on `task_spawns_prompts` reciprocity.

**What happened.** Task 015's frontmatter has `task_spawns_prompts: []` (empty). But it spawned the `integrate-dramatica-ncp-skills` prompt. Task 015's `task.md §Plan Step 13` calls for authoring the prompt; the prompt exists; both `task_uses_prompts` and `prompt_relates_to_task` are populated reciprocally. Yet `task_spawns_prompts` is `[]`. So `task_spawns_prompts` apparently does NOT include prompts the Task ITSELF authors as part of its own deliverables — only prompts the Task spawns for OTHER Tasks to consume.

This is the convention I had to infer to avoid double-counting. Setting Task 030's `task_spawns_prompts: ["agency-adr-governance-spec"]` IS correct under this convention because Task 030 authored the prompt for Task 027 to consume.

**Workaround.** Trust the convention from Task 015's example. Set Task 030's `task_uses_prompts: []` (it uses no prompts) and `task_spawns_prompts: ["agency-adr-governance-spec"]` (it spawns one for Task 027).

**Risk this incurs.** TASK.md §3.3 doesn't make the "uses vs. spawns" distinction explicit. A future agent could plausibly read either interpretation.

**Pattern this exposes.** Same as FE-5 — the audit graph's edges are under-typed.

**Suggested rule for Task 029 to ratify.** Restate TASK.md §3.3's definitions of `task_uses_prompts` vs. `task_spawns_prompts` to make explicit:
- `task_uses_prompts`: prompts this Task EXECUTES.
- `task_spawns_prompts`: prompts this Task AUTHORS for another Task to execute.
- A Task can list a prompt in BOTH if it both authored and executed the prompt within the same Task.

### FE-10 (FL1, Minor) — Persona scenarios have no schema-level contract for new precompiled artefacts.

**What happened.** Task 030 §Goal #4 introduces a NEW directory structure: `maintenance/schemas/narrative-ontology/precompiled/<scenario-id>.json` plus a `precompiled.schema.json`. Doing so:

1. Implicitly extends the Narrative Ontology surface ([AGENTS.md § Authoritative Location](../../AGENTS.md) lists 7 files; this adds an 8th category).
2. Implicitly extends the load-trigger rule ([AGENTS.md § NO.5](../../AGENTS.md) MUST be amended to forbid loading `precompiled/*.json` in non-narrative work).

Both are SCHEMA-CHANGING decisions, and §Anti-Patterns explicitly says schema bumps are out of scope for Task 030 and require a Task-027 ADR.

**Workaround.** Scoped Task 030 §Goal #4 to "produce JSON files passing a schema in this folder; do NOT amend [AGENTS.md § Narrative Ontology] yet". The amendment lands in Task 027 (or a new mini-task spawned from 027) once the ADR-governance pattern decides whether `precompiled/` is part of the Narrative Ontology canonical surface or a separate "denormalised projection layer".

**Risk this incurs.** ST-9 ships a `precompiled.schema.json` whose status is "not yet ratified by [AGENTS.md § Narrative Ontology]". An agent following the rule literally won't load it; an agent ignoring the rule will. The status quo is worse than the schema being clearly absent.

**Pattern this exposes.** New ontology-surface artefacts need a "preview" lifecycle that's not the same as "schema bump" or "regular file". This is exactly the architectural-decision-record use case Task 027's ADR-governance spec is meant to address — full-circle.

**Suggested rule for Task 029 to ratify.** New ontology-surface artefacts get a `status: preview` lifecycle. A `preview` artefact is loaded under a separate trigger rule; agents that don't explicitly handle `preview` artefacts treat them as `status: archived`. Promoting `preview` → `active` requires an ADR.

---

## 4. Pre-Action Sanity Check Notes

(Empty until Phase A dispatches. Populated during execution.)

## 5. Unmapped-heading partition (ST-3)

Snapshot: `validate.py` post-ST-3 reports `unmapped-heading: 105` (was 107 at ST-3 start; -2 net = +5 minted canonical headings now mapped, +5 brand-new headings now mapped via the ST-3 mints, -7 net via ontology pointer changes / pre-existing mappings; see commit body for full delta).

Bucket legend
-------------

- **A — anchor-format mismatch.** Heading IS canonical in source but the slug-from-heading does not match the slug-in-ontology, OR the canonical entry's `term_file` points at a different file/anchor. ST-3's deliverable #1 resolves the eight known cases; residual A entries are file-coordination calls that should resolve mechanically once duplicate headings are reconciled.
- **B — kind-concept slot specialisations.** Throughline-/MC-/IC-prefixed headings (`Female Mental Sex`, `Impact Character Approach`, `Overall (Objective) Story <X>`) and "See X" redirect entries. Per task §Anti-Pattern, these are alias-on-canonical or `kind: concept` candidates and are owned by ST-4 (alias resolution) and a follow-up task; ST-3 does NOT add aliases here.
- **C — structural prose.** Workflow chapters / explainer sub-headings inside extension-derived files (`element-quads.md`, `encoding-patterns.md`, `essential-questions.md`, `storyform-mechanics.md`, `dramatica-fundamentals.md`, `main-vs-impact-character.md`, `dynamic-pairs-index.md`). NOT ontology candidates by design — they are chapter sections, not term entries. Documented unmapped legitimately.
- **D — disputed.** Heading looks like it COULD be canonical (matches a Dramatica term name) but no ontology entry exists, AND minting would require either (a) a new ontology kind (forbidden here) or (b) a schema decision (e.g., enum-of-values for character-dynamic). Surfaced for Task 027 / a future task to ratify.

Partition table
---------------

| File | Heading | Bucket | Resolution / rationale |
|---|---|---|---|
| character-appreciations.md | Blind Spot | C | extension explainer of MC's Blind Spot relationship; not a canonical term |
| character-appreciations.md | Change Character | C | extension cross-ref to MC.resolve=Change; not a canonical term |
| character-dynamics.md | Change | D | enum-value of character-dynamic.resolve (Change vs. Steadfast); minting needs enum-schema decision |
| character-dynamics.md | Female Mental Sex | B | alias for character-dynamic.problem-solving-style — coordinate with ST-4 |
| character-dynamics.md | Impact Character Approach | B | IC-throughline specialisation of character-dynamic.approach — alias-on-canonical (ST-4) |
| character-dynamics.md | Impact Character Problem Solving Style | B | IC-throughline specialisation of character-dynamic.problem-solving-style — alias (ST-4) |
| character-dynamics.md | Male Mental Sex | B | alias for character-dynamic.problem-solving-style — coordinate with ST-4 |
| character-dynamics.md | Resolve | A | character-dynamic.resolve term_file points at dramatica-fundamentals.md#resolve-substantive-definition; the canonical body lives here. Pointer should arguably move to character-dynamics.md#resolve. Deferred — fundamentals.md anchor is also legitimate (substantive definition lives there). File-coordination ratification needed |
| character-dynamics.md | Intuitive | D | enum-value of character-dynamic.problem-solving-style (Intuitive/Holistic vs. Logical/Linear); ST-2 repaired the heading; minting needs enum-schema decision |
| character-dynamics.md | Start | D | enum-value of character-dynamic.growth (Start vs. Stop); minting needs enum-schema decision |
| character-dynamics.md | Steadfast | D | enum-value of character-dynamic.resolve (paired with Change); minting needs enum-schema decision |
| classes.md | Overall (Objective) Story Domain | B | OS-throughline specialisation of class-as-domain — alias (ST-4) |
| domains.md | Impact Character Throughline | B | throughline specialisation; the throughline.impact-character ontology entry already exists — alias-on-canonical (ST-4) |
| dramatica-definitions.md | Character | C | extension definition file overview heading |
| dramatica-definitions.md | Character Dynamics | C | extension definition file overview heading |
| dramatica-definitions.md | Dramatica Terms | C | extension definition file overview heading |
| dramatica-fundamentals.md | Mental Sex / Problem-Solving Style — `Linear` and `Holistic` | C | extension explainer chapter; canonical entry is character-dynamic.problem-solving-style |
| dramatica-fundamentals.md | Quick reference — the four MC Character Dynamics | C | extension chapter overview |
| dramatica-terms.md | Argument | D | candidate canonical term ("Argument" is a Dramatica concept); not yet in ontology — disputed mint |
| dramatica-terms.md | Grand Argument Story (GAS) | D | candidate canonical term — disputed mint |
| dramatica-terms.md | Storyform | D | candidate canonical term (referenced extensively in scenarios.json) — disputed mint |
| dramatica-terms.md | Theme | D | candidate canonical term — disputed mint |
| dramatica-terms.md | Vocabulary Item | C | meta-term about the dictionary, not a Dramatica concept |
| dynamic-terms.md | Charge | C | physics-metaphor explainer of Element/Variation dynamics |
| dynamic-terms.md | Current | C | physics-metaphor explainer |
| dynamic-terms.md | Potential | C | physics-metaphor explainer (cf. el.potentiality which IS canonical) |
| dynamic-terms.md | Power (Outcome) | C | physics-metaphor explainer |
| dynamic-terms.md | Resistance | C | physics-metaphor explainer |
| dynamic-terms.md | Z Pattern | C | structural diagram explainer |
| element-quads.md | Why Quads matter for Encoding | C | structural prose chapter |
| element-quads.md | The KTAD Pattern — every Quad is the same fractal | C | structural prose chapter |
| element-quads.md | The 16 Element Quads — Variation/Issue level | C | structural prose chapter |
| element-quads.md | The 16 Element Quads — Element/Problem level | C | structural prose chapter |
| element-quads.md | How to use the Quads in Encoding | C | structural prose chapter |
| encoding-patterns.md | The Encoding Discipline | C | structural prose chapter |
| encoding-patterns.md | Worked Example 1 — *Casablanca* (1942) | C | worked example, not a term |
| encoding-patterns.md | Worked Example 2 — *Star Wars: A New Hope* (1977) | C | worked example, not a term |
| encoding-patterns.md | Common Encoding Patterns by Slot | C | structural prose chapter |
| encoding-patterns.md | Encoding heuristics for non-narrative work | C | structural prose chapter |
| encoding-patterns.md | Anti-patterns to watch for | C | structural prose chapter |
| essential-questions.md | Why these questions | C | workflow-chapter intro |
| essential-questions.md | Phase 1 — Throughline Class assignments | C | workflow-chapter step |
| essential-questions.md | Phase 2 — Within each Throughline: Concern, Issue, Problem | C | workflow-chapter step |
| essential-questions.md | Phase 3 — Main Character Dynamics | C | workflow-chapter step |
| essential-questions.md | Phase 4 — Plot Dynamics | C | workflow-chapter step |
| essential-questions.md | What gets derived automatically | C | workflow-chapter step |
| essential-questions.md | When you don't know — leave it open | C | workflow-chapter step |
| essential-questions.md | Worked walkthrough: applying this to *Casablanca* | C | worked example, not a term |
| overview-appreciations.md | Actual Dilemma | B | OS-throughline storypoint specialisation — alias / kind:concept (ST-4) |
| overview-appreciations.md | Actual Work | B | OS-throughline storypoint specialisation — alias / kind:concept (ST-4) |
| overview-appreciations.md | Apparent Dilemma | B | storypoint specialisation — alias / kind:concept (ST-4) |
| overview-appreciations.md | Apparent Work | B | storypoint specialisation — alias / kind:concept (ST-4) |
| overview-appreciations.md | Both | D | enum-value of character-appreciation field; minting needs enum-schema decision |
| overview-appreciations.md | Essence | D | candidate canonical (story-essence concept); disputed mint |
| overview-appreciations.md | Female | D | enum-value of MC mental-sex axis; minting needs enum-schema decision |
| overview-appreciations.md | Male | D | enum-value of MC mental-sex axis; minting needs enum-schema decision |
| overview-appreciations.md | Nature | D | candidate canonical (story-nature concept); disputed mint |
| overview-appreciations.md | Negative Feel | D | enum-value of MC.feel axis; minting needs enum-schema decision |
| overview-appreciations.md | Neither | D | enum-value of character-appreciation field; minting needs enum-schema decision |
| overview-appreciations.md | Positive Feel | D | enum-value of MC.feel axis; minting needs enum-schema decision |
| overview-appreciations.md | Reach | D | candidate canonical; disputed mint |
| overview-appreciations.md | Sympathy | D | candidate canonical; disputed mint |
| overview-appreciations.md | Tendency | D | candidate canonical; disputed mint |
| overview-appreciations.md | Unwilling | D | enum-value of MC.attitude axis; minting needs enum-schema decision |
| overview-appreciations.md | Willing | D | enum-value of MC.attitude axis; minting needs enum-schema decision |
| plot-dynamics.md | Bad | D | enum-value of plot-dynamic.judgment (Good/Bad); minting needs enum-schema decision |
| plot-dynamics.md | Decision | D | enum-value of plot-dynamic.driver (Action/Decision); minting needs enum-schema decision |
| plot-dynamics.md | Failure | D | enum-value of plot-dynamic.outcome (Success/Failure); minting needs enum-schema decision |
| plot-dynamics.md | Good | D | enum-value of plot-dynamic.judgment; minting needs enum-schema decision |
| plot-dynamics.md | Optionlock | D | enum-value of plot-dynamic.limit (Optionlock/Timelock); minting needs enum-schema decision |
| plot-dynamics.md | Success | D | enum-value of plot-dynamic.outcome; minting needs enum-schema decision |
| plot-dynamics.md | Timelock | D | enum-value of plot-dynamic.limit; minting needs enum-schema decision |
| plot-structures.md | Domain Act Order | C | structural prose chapter |
| plot-structures.md | Overall (Objective) Story Type Order | C | structural prose chapter |
| storyform-mechanics.md | The Four Throughlines and their Class Distribution | C | structural prose chapter |
| storyform-mechanics.md | The Type Sequences — Acts as a Class's Type-Tour | C | structural prose chapter |
| storyform-mechanics.md | How a Storyform is Built — The Cascade | C | structural prose chapter |
| storyform-mechanics.md | The Eight Archetypal Characters — Element Pair Assignments | C | structural prose chapter |
| storyform-mechanics.md | Encoding consistency — quick checks | C | structural prose chapter |
| storytelling.md | Backstory | D | candidate canonical (storytelling-layer term); disputed mint |
| storytelling.md | Chapter | D | candidate canonical (storytelling-layer term); disputed mint |
| storytelling.md | Flashbacks and Flashforwards | C | storytelling-layer technique explainer |
| storytelling.md | Storytelling | C | extension definition file overview heading |
| storytelling.md | Subplot | D | candidate canonical (storytelling-layer term); disputed mint |
| structural-terms.md | Class | D | meta-term naming the kind (kind=class); minting requires meta-concept-of-kind ratification |
| structural-terms.md | Companion Pair | D | candidate canonical (kind=dynamic-pair sub-type); disputed mint |
| structural-terms.md | Dependent Pair | D | candidate canonical (kind=dynamic-pair sub-type); disputed mint |
| structural-terms.md | Dynamic Pair | D | meta-term naming the kind (kind=dynamic-pair); minting requires meta-concept-of-kind ratification |
| structural-terms.md | Element | D | meta-term naming the kind (kind=element); ratification needed |
| structural-terms.md | Family | D | candidate canonical (structural-relation term); disputed mint |
| structural-terms.md | Inverse | D | candidate canonical (structural-relation term); disputed mint |
| structural-terms.md | Level | D | meta-term (Class/Type/Variation/Element levels); ratification needed |
| structural-terms.md | Type | D | meta-term naming the kind (kind=type); ratification needed |
| structural-terms.md | Variation | D | meta-term naming the kind (kind=variation); ratification needed |
| types.md | Benchmark | A | concept.benchmark? No ontology entry — but `## Benchmark` is a canonical Type appreciation. Missing canonical mint candidate (similar to the 5 ST-3 minted) — flagged for ST-3 follow-up if budget allows; left as A residual |
| types.md | Goal | A | similar to Benchmark — missing canonical mint candidate (concept.story-goal exists at #overall-objective-story-goal but `## Goal` itself unmapped); residual A |
| types.md | Overall (Objective) Story Benchmark | B | OS-throughline storypoint specialisation — alias / kind:concept (ST-4) |
| types.md | Overall (Objective) Story Concern | B | OS-throughline storypoint specialisation — alias (ST-4) |
| types.md | Overall (Objective) Story Consequence | B | OS-throughline storypoint specialisation — alias (ST-4) |
| types.md | Overall (Objective) Story Costs | B | OS-throughline storypoint specialisation — alias (ST-4) |
| types.md | Overall (Objective) Story Dividends | B | OS-throughline storypoint specialisation — alias (ST-4) |
| types.md | Overall (Objective) Story Preconditions | B | OS-throughline storypoint specialisation — alias (ST-4) |
| types.md | Overall (Objective) Story Prerequisites | B | OS-throughline storypoint specialisation — alias (ST-4) |
| types.md | Overall (Objective) Story Requirements | B | OS-throughline storypoint specialisation — alias (ST-4) |
| types.md | Stipulation | A | heading exists, no ontology entry; canonical Type appreciation. Residual A — missing canonical mint candidate (similar shape to the 5 ST-3 minted) |

Row counts
----------

| Bucket | Count |
|---|---:|
| A | 4 |
| B | 18 |
| C | 42 |
| D | 41 |
| **Total** | **105** |

Note: post-ST-3 unmapped count is 105 (was 106-107 pre-ST-3 depending on snapshot timing). The eight anchor-mismatch fixes from §Goal deliverable #1 are not row-counted here because they no longer appear as unmapped after ST-3's mints; the partition table catalogues only the residual unmapped headings.

Bucket D summary (disputed terms requiring future ratification)
---------------------------------------------------------------

The 41 D-bucket entries split into three semantic clusters:

1. **Enum-value-of-character-dynamic / -plot-dynamic** (16 rows): Change, Steadfast, Start, Stop (implicit), Intuitive, Logical (implicit), Both, Female, Male, Negative Feel, Neither, Positive Feel, Unwilling, Willing, Bad, Decision, Failure, Good, Optionlock, Success, Timelock. These are values of an enumerated property of an existing canonical (character-dynamic.resolve, .growth, .problem-solving-style, plot-dynamic.judgment, .driver, .outcome, .limit). Minting an ontology entry per value would require a `kind: enum-value` schema bump or an `enum_values: [...]` field on the parent — both Task 027 ADR-class decisions.

2. **Candidate canonical Dramatica concepts not in ontology** (15 rows): Argument, Grand Argument Story, Storyform, Theme, Essence, Nature, Reach, Sympathy, Tendency, Backstory, Chapter, Subplot, Goal (`types.md`), Benchmark (`types.md`), Stipulation (`types.md`). These ARE Dramatica terms in Phillips/Huntley but were not bootstrapped in Task 015. Minting them is mechanical (similar to the 5 ST-3 minted) but the per-term decision (provenance, scenarios, NCP mapping) is non-trivial and best handled in a focused mint pass.

3. **Meta-terms naming the ontology kinds themselves** (10 rows): Class, Companion Pair, Dependent Pair, Dynamic Pair, Element, Family, Inverse, Level, Type, Variation. These are the words for the *categories* the ontology is built from (kind=class, kind=dynamic-pair, kind=element, kind=type, kind=variation). Minting them as `kind: concept` (e.g., `concept.element-meta`) would create a meta-self-reference that the schema currently neither encourages nor forbids; ratification needed.

Bucket A residuals (4 rows): `character-dynamics.md#resolve`, `types.md#benchmark`, `types.md#goal`, `types.md#stipulation`. The first is a file-coordination call; the other three are missing-canonical-mint candidates analogous to the 5 ST-3 minted under §Goal deliverable #1 but were not in the original 8-mismatch list and therefore deferred to a future pass. ST-3 surfaces them rather than silently bucketing.

Coordination notes for ST-4
---------------------------

ST-4's brief covers the empty-redirect-resolution work that overlaps with this partition's Bucket B. ST-3 has NOT added any aliases (per task constraint); the 18 B-bucket entries are passed to ST-4 as candidates for either:
- `deprecated_aliases_en` on the canonical entry (preferred for "See X" historic entries like `## Female Mental Sex` / `## Male Mental Sex`), or
- new `kind: concept` ontology entries with `term_file` pointing at the throughline-prefixed heading (preferred for entries with substantive unique body content, such as the `## Overall (Objective) Story <X>` family in types.md/elements.md if the body differs from the bare-canonical entry).

ST-4 makes the per-row decision; ST-3's bucketing is the input.



## 6. /sc:* Invocation Log

(Will be populated as each `/sc:agent`, `/sc:improve`, `/sc:test`, `/sc:createPR` invocation fires. Format: timestamp / command / parameters / observed-vs-expected outcome.)

## 7. ReAct Trace

(Will be populated during execution. Format from Task 015 §ReAct Trace: `**R:** what I'm about to do and why. **A:** what I did. **O:** what came back / what I learned.`)

## 8. ST-7 Alias Conflict Report

Captured from `python3 tools/dramatica-nav/aliases.py conflict-report` against `skills/dramatica-vocabulary/references/_synonym-lookup.md` after the EN bulk load. **Disposition for every row in this section: deferred — NOT auto-projected; left for human / Task 027 ADR review.** The loader runs the conflict pass first and refuses to write any of these aliases into the ontology.

**Summary**

- Rows parsed: 486
- Aliases projected (EN, conflict-free subset): 395 across 131 ontology IDs
- Blocking conflicts (no projection at all): 21
- Partial-resolution rows (one OK target, others unknown — projected via the OK target only, surfaced for transparency): 6
- Unknowns (canonical label not in the ontology — these labels are mostly file-only headings like `Bad`, `Be-er`, `Mental Sex`, etc.; out of scope for ST-7 — see ST-3 unmapped-heading partition for context): 70

**Conflict classes**

1. **alias-uniqueness** — the alias would project to ≥ 2 distinct ontology IDs (the synonym-lookup row carries multiple `**Label** (in `<file>`)` targets that all resolve cleanly to different entries). Auto-resolution is forbidden; the loader skips the row.

2. **reserved-alias-collision** — the alias string is already claimed (as the canonical label or an existing alias) by a different ontology entry. Adding it as an alias on the requested target would silently introduce an alias-uniqueness violation that `validate.py` would flag downstream.

**Blocking conflicts (21)**

- `ability to consider` — alias-uniqueness: would project to {`arc.contagonist`, `el.conscience`}
- `advancing` — alias-uniqueness: would project to {`el.production`, `var.hope`}
- `anticipation` — alias-uniqueness: would project to {`el.projection`, `var.prediction`}
- `cognizant` — alias-uniqueness: would project to {`arc.contagonist`, `el.conscience`}
- `concern` — alias-uniqueness: would project to {`concept.concern`, `var.worry`}
- `considerations` — alias-uniqueness: would project to {`arc.contagonist`, `el.conscience`}
- `examination` — alias-uniqueness: would project to {`el.evaluation`, `el.test`, `var.analysis`}
- `flowing` — alias-uniqueness: would project to {`el.production`, `var.hope`}
- `proceeding` — alias-uniqueness: would project to {`el.production`, `var.hope`}
- `retard` — alias-uniqueness: would project to {`el.hinder`, `var.delay`}
- `sensibilities` — alias-uniqueness: would project to {`arc.contagonist`, `el.conscience`}
- `subjective` — alias-uniqueness: would project to {`var.need`, `var.worth`}
- `analysis` — reserved-alias-collision: target `el.evaluation` blocked, already claimed by `var.analysis`
- `appraisal` — reserved-alias-collision: target `el.evaluation` blocked, already claimed by `var.appraisal`
- `consideration` — reserved-alias-collision: target `el.thought` blocked, already claimed by `quad.consideration-var`
- `determination` — reserved-alias-collision: target `var.choice` blocked, already claimed by `el.determination`
- `evaluation` — reserved-alias-collision: target `var.analysis` blocked, already claimed by `el.evaluation`
- `reappraisal` — reserved-alias-collision: target `el.reevaluation` blocked, already claimed by `var.reappraisal`
- `support` — reserved-alias-collision: target `el.help` blocked, already claimed by `el.support`
- `suspicion` — reserved-alias-collision: target `el.hunch` blocked, already claimed by `var.suspicion`
- `unique ability` — reserved-alias-collision: target `var.unique-ability` blocked, already claimed by `concept.unique-ability`

**Recommended follow-up.** A Task-027-style ADR per Bucket-D (per ST-7's falsification clause) needs to choose one ontology ID per blocking row. Most of these are genuinely ambiguous English shorthand (e.g. `analysis` could mean either the canonical `var.analysis` Variation OR `el.evaluation` element-as-prose-synonym). Until then, `nav.py by-alias` will return the canonical-label match (the entry that actually owns the string), which is the conservative behaviour.

## 9. ST-8 Scenario-Tag Measurement Table

(Reserved for ST-8's per-iteration measurement output. Format: iteration | tagged-count | median | mean | max | orphan-count | over-tagged-count | gate-status.)

## 10. ST-9 Token-Cost Benchmark

(Reserved for ST-9's `precompile.py benchmark` output. Format: scenario-id | prose-path-bytes | precompiled-path-bytes | reduction-% | gate-status.)


