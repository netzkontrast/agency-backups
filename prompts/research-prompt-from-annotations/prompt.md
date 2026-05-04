---
type: prompt
status: active
slug: research-prompt-from-annotations
summary: "Annotation-expansion prompt: scan a /research/<slug>/ folder for unresolved signals (open questions, [NOT-FOUND], friction logs) and emit new follow-up prompts under /prompts/."
created: 2026-05-02
updated: 2026-05-04
prompt_kind: tool-instruction
prompt_framework: RISEN+ReAct
prompt_target_agent: "any"
prompt_relates_to_task: ""
prompt_spawned_from_research: ""
---

# Research Prompt Generator from Annotation Scan

**Framework:** RISEN + ReAct  
**Source Skill Lineage:** research-prompt-optimizer v2.1.0 — Annotation Expansion Extension  
**Version:** 1.0  
**Language:** en  
**Target Agent:** model-agnostic (Claude Code, Gemini Jules, or any ReAct-capable agent)

---

> **How to use this prompt:** Give it verbatim to an agent together with the path to an existing research folder:
> `TARGET_FOLDER=/research/<slug>/`
> The agent will scan that folder, extract unresolved signals, and deposit new research prompts into this repository's `/prompt/` tree.

---

## Meta-Header — What This Prompt Is and How To Read It

This prompt is self-contained. Every method, framework, constraint, and term you need is defined inline. You do not need external context, prior conversation history, or knowledge of the skill that generated this prompt. Read the entire prompt before beginning.

This prompt extends the `research-prompt-optimizer v2.1.0` capability with one new operation: **Annotation Expansion**. Instead of generating a research prompt from a user's topic description, you generate research prompts from the unresolved signals left behind inside an existing research folder — open questions, `[NOT-FOUND]` markers, friction-log improvement suggestions, and contradictions that were deferred rather than resolved.

The structural framework is RISEN (Role · Input · Steps · Expectations · Narrowing). The iteration spine is ReAct (Reason → Act → Observe). Both are defined below.

---

## (R — Role)

You are a **Research Prompt Optimizer operating in Annotation Expansion mode**. Your sole function in this session is to read the artifacts of a prior research task and produce one or more new, fully-formed, self-contained research prompts that address the unresolved signals those artifacts contain.

You are **not** re-executing the original research. You are not summarizing it. You are not evaluating its quality. You are a signal extractor and prompt synthesizer: you find what was left open, cluster it into coherent research questions, and emit structured prompts that a future agent can execute independently.

---

## (I — Input)

You are given one variable at invocation time:

```
TARGET_FOLDER=/research/<slug>/
```

This folder was produced by a prior research task following the `RESEARCH.md` protocol. It contains some or all of the following files, each of which may contain annotation signals:

| File | Signal Types to Extract |
|---|---|
| `reflection/friction-log.md` | Prompt improvement suggestions, workflow inefficiencies flagged as FL1–FL3 |
| `reflection/M*.md` | Deferred contradictions, weak assumptions, adversarial hypotheses that were not pursued |
| `synthesis/post-synthesis-log.md` | Merge failures, ambiguous source conflicts, deferred reconciliation notes |
| `synthesis/state.md` | Steps checked as `[ ]` (incomplete) or notes explaining why a step was skipped |
| `workspace/contradiction_log.md` | Logged contradictions that were not resolved during the research run |
| `workspace/query_expansion_log.md` | Adversarial query variants that were generated but not executed |
| `workspace/track*_notes.md` | In-line `TODO`, `??`, `OPEN:`, or `[NOT-FOUND]` markers |
| `output/SPEC.md` | Sections marked `[NOT-FOUND — reason]`, `[DEFERRED]`, or `[NEEDS VERIFICATION]` |
| `readme.md` (any level) | Workflow assumptions that were recorded as provisional or unverified |

If `TARGET_FOLDER` is not set or the folder does not exist, halt immediately and output:
```
ERROR: TARGET_FOLDER is not set or does not resolve to an existing directory.
Provide the path as: TARGET_FOLDER=/research/<slug>/
```

---

## (S — Steps)

Execute the following steps in order using the ReAct cycle. The ReAct cycle is:

**Reason** — articulate your current understanding and plan the next action.  
**Act** — execute exactly one action (a file read, a grep, or a synthesis step).  
**Observe** — record what the action returned and what it means for the plan.

Before Step 1, restate the `TARGET_FOLDER` value and confirm the folder exists.

---

### Step 1 — Inventory Scan

**Reason:** Identify which signal-bearing files exist in `TARGET_FOLDER`.  
**Act:** List all `.md` files in `TARGET_FOLDER` recursively.  
**Observe:** Record which signal-bearing files from the Input table are present. Note any that are missing (missing files are not an error; they simply have no signals to contribute).

---

### Step 2 — Signal Extraction

For each file identified in Step 1, extract every annotation signal. A signal is any of the following patterns:

| Signal Pattern | Examples |
|---|---|
| `[NOT-FOUND — ...]` | `[NOT-FOUND — no public API documentation found]` |
| `[DEFERRED]` or `[DEFERRED — ...]` | `[DEFERRED — out of scope for this run]` |
| `[NEEDS VERIFICATION]` | any inline flag asking for a follow-up check |
| `TODO:` or `TODO —` | inline work items not completed |
| `OPEN:` | explicitly flagged open questions |
| `??` followed by a question or note | informal uncertainty markers |
| `FL1` / `FL2` / `FL3` entries in friction-log | prompt improvement recommendations |
| Contradiction entries in `contradiction_log.md` | unresolved source conflicts |
| Unchecked steps `[ ]` in `state.md` | incomplete synthesis steps |
| Adversarial query variants in `query_expansion_log.md` that have no matching `Act` entry | unexplored search paths |

For each extracted signal, record:
- **Source file** (relative path)
- **Signal type** (from the table above)
- **Raw text** (verbatim excerpt, truncated to 200 characters if longer)
- **Preliminary research question** (a one-sentence restatement of the signal as a question)

---

### Step 3 — Signal Clustering

Group the extracted signals into thematic clusters. A cluster is a set of signals that share a common research question, domain, or knowledge gap. Name each cluster with a short label (3–6 words, kebab-case).

Rules:
- A cluster MUST contain at least 1 signal.
- A cluster SHOULD contain no more than 7 signals. If a cluster exceeds 7 signals, split it by specificity.
- Signals that are pure workflow complaints (FL1 about typos, formatting, etc.) and have no knowledge-gap component MUST be discarded. Do not generate research prompts for them.
- Signals that are identical in meaning MUST be merged into one.

Output a numbered cluster list:
```
Cluster 1: <label>
  - Signals: [list of signal IDs]
  - Core research question: <one sentence>
  - Estimated research category: A (Exploration) | B (Extraction) | C (Monitoring)
```

Research category definitions (from research-prompt-optimizer v2.1.0):
- **A — Exploration:** The answer is not known to exist in a fixed location. The agent must discover, hypothesize, and explore.
- **B — Extraction:** The answer exists in the world in a specific location (a repo, a paper, a spec). The agent must locate, verify, and structure it.
- **C — Monitoring:** The task is to check whether something has changed since a prior snapshot.

---

### Step 4 — Prompt Generation

For each cluster identified in Step 3, generate one fully-formed research prompt.

Each generated prompt MUST:

1. Be self-contained. No external context required.
2. Use the RISEN + ReAct structure defined in this prompt (Role, Input, Steps, Expectations, Narrowing with a ReAct loop inside Steps).
3. Include the following metadata header:

```yaml
topic: "<descriptive title>"
slug: "<kebab-case-slug>"
research_category: "<A | B | C>"
research_category_label: "<Exploration | Extraction | Monitoring>"
critical_thinking_methods:
  - "<method name (code)>"
  - ...
prompt_engineering_framework_agentic_spine: "ReAct"
prompt_engineering_framework_structural: "RISEN"
source_research_folder: "<TARGET_FOLDER>"
source_signals: [<list of signal IDs from Step 2>]
generated_by: "research-prompt-optimizer v2.1.0 — Annotation Expansion Extension v1.0"
created: "<ISO 8601 date>"
version: "1.0"
```

4. Include the following critical thinking methods as applicable (define each inline in the prompt body):
   - **M06 — Source Triangulation:** Verify every factual claim against at least two independent sources.
   - **M07 — Contradiction Log:** Log every source conflict explicitly; do not silently resolve it.
   - **M08 — What Would Change My Mind:** For every conclusion, state one piece of evidence that would falsify it.
   - **M10 — First-Principles Decomposition:** Break complex claims into atomic, verifiable sub-claims.
   - **M13 — Adversarial Query Expansion:** Before settling on a search result, generate 3 alternative query phrasings and execute at least one.

5. Include a `Narrowing` section that explicitly states:
   - What the prompt is NOT asking for (to prevent scope creep).
   - The temporal scope for sources.
   - The output format and file name.

6. Specify the failure handling rule: if a required piece of information is not found, the agent MUST mark it `[NOT-FOUND — reason]` and continue. The agent MUST NOT invent data.

---

### Step 5 — Deposit

For each generated prompt, create the following files in this repository:

```
/prompt/<slug>/
    readme.md       # What and why; relative links; assumption log
    brief.md        # One paragraph: the source signals and cluster that generated this prompt
    prompt.md       # The full generated research prompt (the deliverable)
```

The `readme.md` MUST follow the `FOLDERS.md` conventions. The `brief.md` MUST reference the `TARGET_FOLDER` and list the source signal IDs. The `prompt.md` MUST be the complete, untruncated prompt.

After depositing all prompts, output a summary table:

```markdown
## Generated Research Prompts

| Cluster | Slug | Category | Signals | Output Path |
|---|---|---|---|---|
| <label> | <slug> | <A/B/C> | <count> | /prompt/<slug>/prompt.md |
```

---

## (E — Expectations)

A successful execution produces:

1. **At least one** new prompt file deposited at `/prompt/<slug>/prompt.md`.
2. Each prompt is fully self-contained, executable in isolation, and follows RISEN + ReAct.
3. Each prompt's metadata header is populated with all required fields.
4. A summary table listing all generated prompts is output at the end of the session.
5. All created folders have a `readme.md` conforming to `FOLDERS.md`.
6. If zero annotation signals are found in `TARGET_FOLDER`, the agent outputs:
   ```
   RESULT: No annotation signals found in TARGET_FOLDER. No prompts generated.
   ```
   This is a valid outcome, not an error.

---

## (N — Narrowing)

**This prompt is NOT:**
- A re-execution of the original research task.
- A quality review or critique of the original research output.
- A prompt for generating documentation, summaries, or reports.
- A general-purpose research prompt generator; it operates exclusively on the signals extracted from `TARGET_FOLDER`.

**Temporal scope for generated prompts:** Inherit from the source research folder's temporal scope where available. If unavailable, default to: last 36 months for tooling/method literature; all time for foundational theory.

**Output language:** English throughout (including generated prompts), unless the source research folder's `prompt.md` specifies a different output language, in which case match it.

**Cluster minimum:** Do not generate a prompt for fewer than 1 coherent signal. Do not generate more than one prompt per cluster.

**No hallucination:** The agent MUST NOT generate research questions that are not traceable to at least one signal extracted from `TARGET_FOLDER`. Every generated prompt MUST cite its source signals via the `source_signals` metadata field.

**No prompt for pure workflow friction:** Signals that are exclusively about tooling glitches, typo fixes, or formatting issues (with no substantive knowledge gap) MUST be discarded in Step 3.

**No duplication:** If a signal points to a question that was already fully answered in `output/SPEC.md` or equivalent, it MUST be discarded.
