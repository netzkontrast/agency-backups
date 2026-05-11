---
type: note
status: active
slug: dramatica-scenarios-foundation-brief
summary: "Captured user intent for the foundational research prompt that will drive the dramatica-scenarios Epic — content-template system + build-time line indexing + scenario-taxonomy gap analysis."
created: 2026-05-11
updated: 2026-05-11
---

# Brief — `dramatica-scenarios-foundation`

> **Optimizer Phase 1 capture (intent.yaml-equivalent).** This file records the
> user's raw request and the answers gathered through four AskUserQuestion
> rounds before drafting the prompt. Immutable by convention — to revise the
> prompt's intent, append a new Brief Revision section, do not edit the captured
> answers.

## Raw user request (paraphrased)

> "With your findings on the dramatica-theory and dramatica-vocabulary skills,
> please write a detailed new Task for an improvement. The dramatica-nav tool
> should not return a filename, but the actual content. There needs to be
> content created for all the different scenarios — so a lot of subtasks,
> instructions to ingest the theory completely, and to think ultra about every
> step in the scenario pipeline. The goal is to get real instructions based on
> the theory for every possible and defined scenario which might be of use in
> the novel-architect skill. Create a detailed plan for this. Prior to creating
> the Task, use /research-prompt-optimizer to create an initial Research Task
> that uses the askuser tool intensively so that the resulting plan is solid."

## Findings that triggered the request (from the Task 072 self-audit)

- The Task 072 worked example originally claimed `Crucial Element: SELF-INTEREST`
  with partner `MORALITY` — but `nav.py by-id var.self-interest` confirms both
  are **Variations**, not **Elements**, living in `quad.approach-var-physics`
  under **Physics** class. That violates source rules H5 (Element-level required)
  and H6 (must live in OS = Mind). The example would have failed validation if
  any agent tried to execute it.
- Root cause class: `nav.py by-id` returns ontology metadata + a `term_file`
  pointer (e.g. `skills/dramatica-vocabulary/references/elements.md#faith`).
  The agent must follow the pointer, open the markdown, find the heading, and
  read the prose. Practical experience: agents skip the dereferencing step,
  reason from the metadata fields alone, and confabulate operational
  instructions that look right but don't pass the H1–H12 hard rules.
- Scenario tags exist in the ontology (`scenarios:`-list per entry; 11 distinct
  values) but there is **no operational corpus** behind them — the tags are
  signals without content. Agents see `novel.crucial-element-audit` on
  `el.faith` and have no instruction for what to do with that knowledge.

## Captured intent (4 askuser rounds, 14 total questions)

### Round 1 — scope + nav.py shape + authoring + location

| Question | Answer |
|---|---|
| Which scenarios should this Task cover? | **Expand the scenario taxonomy first, then author.** Discovery sub-task identifies missing scenarios (e.g. `novel.signpost-encoding`, `novel.gate-3-validation-failure`, `novel.crucial-element-encoding`). Then author. |
| What should `nav.py` return instead of `term_file`? | **New command: `nav.py instruct <entry> <scenario>`** for scenario instructions. The existing `by-id` keeps its current pointer-only contract; the new sub-command is where embedded content lives. |
| How should per-scenario instructions be authored? | **Store line-numbers with filename for each entry so they can be found easily. Create a content-template SYSTEM that needs to be researched first within the first sub-task, then populated by the agent per scenario (this should be a lot of tasks — use the decomposition steps of the research optimizer).** |
| Where should the new content live? | **`skills/dramatica-theory/scenarios/<scenario_id>.md`.** |

### Round 2 — Epic shape + line-index implementation + worksheet axis + research scope

| Question | Answer |
|---|---|
| Decomposition shape? | **Umbrella Epic Task + many child Tasks** (Task 070 pattern). |
| Line-index implementation? | **Build-time pre-compile: line numbers stored in `ontology.json`** (new `term_file_line:` field). |
| Should every scenario use Task 72's 8-step Worksheet skeleton, or have its own pipeline shape? | **Each scenario's pipeline is bespoke** (audit vs arc-design vs slot-fill differ). The content-template system must support multiple pipeline-archetypes. |
| How many research prompts as Phase-1 inputs? | **One foundational research prompt** covering content-template + indexing + discovery. |

### Round 3 — done bar + index scope + bilingual + reader-test

| Question | Answer |
|---|---|
| What's the "done" bar per scenario document? | **Pipeline + heuristics + anti-patterns + Gherkin acceptance scenarios + ontology cross-refs + nav.py test + per-scenario end-to-end worked example.** Highest depth-bar. |
| Build-time line-index — which files? | **Vocabulary refs + dramatica-theory chunks + the new `scenarios/*.md`** (self-indexing as scenario docs land incrementally). |
| Bilingual contract for `scenarios/<id>.md`? | **EN throughout** — match `dramatica-theory`'s contract (theory chunks are EN-only). |
| Phase 4 reader-test on the research prompt? | **Yes — enabled.** This research output drives an Epic of 12-15 child Tasks; one fresh-frame audit pass is high-leverage. |

## Implications for the prompt design

1. The deep-research executor MUST traverse THREE interleaved corpora:
   (a) the 9 dramatica-theory chunks (~900 KB source-book derivative),
   (b) the 265 vocabulary entries across reference files (elements / variations /
       types / classes / archetypes / dynamic-pairs / domains / encoding-patterns /
       dramatica-fundamentals / character-dynamics / element-quads),
   (c) the existing ontology `entries[]` array in
       `maintenance/schemas/narrative-ontology/ontology.json`.

2. The output SPEC.md MUST be directly actionable for writing the Epic Task body
   AND its child-Task list — the user said: *"I will know the research succeeded
   when I can take the SPEC.md and write the Epic Task body + child-Task list
   directly from it."*

3. The three coupled design problems are NOT independent — content-template shape
   constrains line-indexing requirements (do scenarios want line-cited theory
   excerpts? if so, line-index must cover theory chunks, which is what the user
   chose). Line-indexing precompile cadence affects scenario-authoring workflow
   (does each scenario merge trigger a re-index? yes per the self-indexing
   choice). Scenario taxonomy gap analysis depends on knowing the
   pipeline-archetypes that exist (so taxonomy expansion is the LAST sub-question,
   gated on (1) and (2)'s outputs).

4. The Epic's child-Task list must respect dependencies:
   - **Foundation first:** content-template system + line-index tooling + nav.py
     `instruct` command — all three before any scenario authoring starts.
   - **Discovery before authoring:** scenario taxonomy expansion must produce
     the final scenario_id list before per-scenario authoring child-Tasks can be
     created.
   - **Per-scenario tasks parallelizable:** once template + tooling + taxonomy
     land, each scenario authoring task is independent.
   - **Validation last:** integration test that wires `nav.py instruct` into
     novel-architect Phase 2 / 3 / 5 / 7 closes the Epic.

## Out of scope for this research

- Authoring the actual scenario content (that's the per-scenario child Tasks).
- Implementing the line-index precompile (that's a child Task — design only here).
- Implementing the `nav.py instruct` subcommand (also a child Task — design only).
- The `lyric.*` scenarios (suno-lyric-writer's domain; deferred).
- Replacing or modifying the existing `nav.py by-id` contract (additive change only).

## Target audience

- **Primary:** Claude Code agents who will execute the Epic and child Tasks.
- **Secondary:** the human reviewer (= user) who approves the Epic plan before
  child Tasks are spawned.

## Selected framework + agent

- **Framework:** RISEN+ReAct.
  - RISEN gives the executor declared structured outputs (R/I/S/E/N) so the
    SPEC.md sections are committed at prompt-author time, not improvised.
  - ReAct allows iterative tool use (read → reason → cross-cite → re-plan)
    across the three corpora. The executor MUST trace its claims to specific
    file:line citations — ReAct's observation step is where the line numbers
    get captured.
- **Target agent:** Gemini Deep Research (primary) / Claude Research (fallback) /
  Perplexity Pro (last resort, may struggle with the cross-corpus traversal).

## Acceptance criteria for the rendered prompt

The rendered prompt is acceptable when it:

1. Carries the captured intent slots verbatim in its `## I — Input` section so
   the executor doesn't need to re-discover them.
2. Decomposes the work into ≥ 3 explicitly-numbered investigative steps that
   map 1:1 onto the SPEC.md output sections.
3. Names the three corpora with absolute or repo-relative paths the executor
   can resolve.
4. Carries a "must cite" rule: every recommendation in SPEC.md MUST cite at
   least one (file, line) tuple from the corpora — no theory-free assertions.
5. Specifies the output SPEC.md skeleton (sections + body schema) so the
   executor doesn't invent its own structure.
6. Passes a fresh-frame reader-test audit (Phase 4) for: ambiguity-free
   instructions, complete corpus enumeration, no implicit context.

## Phase-by-phase status

- **Phase 1 (Intent):** ✅ Complete — captured above; 14 askuser answers.
- **Phase 2 (Planning):** Implicit — captured intent supplied the building blocks
  (3 investigative steps, RISEN+ReAct framework, output SPEC.md skeleton).
  No formal `meta-prompt.yaml` produced; the planning output is encoded directly
  in the rendered `prompt.md`.
- **Phase 3 (Render):** Done in this same session — see `prompt.md`.
- **Phase 4 (Reader Test):** Done by spawning a fresh subagent that read the
  prompt cold and audited it; findings folded into the prompt before Phase 5.
- **Phase 5 (Finalize):** This three-file scaffold is the workspace; no zip
  produced (the workspace lives in the agency repo, not in a tmpdir).

## Frustration log seed

If this prompt + Epic land cleanly: FL0. If the executor surfaces blind spots
the Phase-4 audit missed: bump to FL1 and capture the blind-spot pattern in the
follow-up Task spawned by the research run.
