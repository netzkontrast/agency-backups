---
type: note
status: active
slug: review-pr-29
summary: "Structured critique of PR #29 (tasks 009–011, skills governance). Findings are categorised Critical / Structural / Minor with file:line references."
created: 2026-05-04
updated: 2026-05-04
---

# PR #29 Code Review — Skills Governance (Tasks 009 / 010 / 011)

**Reviewer:** claude-sonnet-4-6  
**PR:** [#29 — task(009-011): skills-governance task workflow + research proposals](https://github.com/netzkontrast/agency/pull/29)  
**Head SHA:** `82d8fcf11f9d01a536bdbd324adf0cfcefd6a7f7`  
**Branch:** `claude/analyze-skills-tools-BF0wL → main`  
**Review date:** 2026-05-04  

---

## Summary

PR #29 is a well-motivated, authoring-only contribution that fills the long-standing
governance gap around `/skills/`. The separation of concerns across three Tasks
(spec → index → schema) is architecturally sound, the RFC-2119 usage is consistent
throughout, and the RISEN-framework declarations in prompts 010 and 011 are
correctly matched to their task shapes.

Two findings rise to **Critical** because they will actively mislead or block the
agent that picks up Task 009. Five **Structural** findings could cause issues during
execution (concurrent writes, pre-declared research, underspecified benchmarks).
Four **Minor** findings are cosmetic or low-risk but worth correcting before an
agent picks up the work.

---

## Critical Findings

### C-1 — Section-count mismatch in `prompts/author-skills-root-spec/prompt.md`

**File:** `prompts/author-skills-root-spec/prompt.md`, Step 1 (§ S — Steps)

The prompt text reads:

> "The executor MUST produce `SKILLS.md` with exactly the following
> **nine** top-level sections"

… but the ordered list that immediately follows enumerates **eleven** sections
(§1 Definitions through §11 Anti-Patterns). This is a factual error that will
confuse the executing agent: it will either stop after nine sections (missing
§10 Edge Cases and §11 Anti-Patterns) or assume the count is a typo and produce
eleven, but with diminished confidence in the spec's precision.

**Fix:** Change "nine" to "eleven" in that sentence, or collapse §10 and §11 into
§9 if the nine-section target is intentional and §10–§11 are meant to be
subsections.

---

### C-2 — Framework mismatch: RISEN declared, tool-execution required (Task 009 prompt)

**File:** `prompts/author-skills-root-spec/prompt.md`, frontmatter + Step 8

Frontmatter declares:

```yaml
prompt_framework: RISEN
```

Yet Step 8 ("Pre-commit verification") instructs the executor to run:

```bash
bash tools/check-governance.sh
python3 tools/validate-frontmatter.py
```

`RISEN` is the repo's convention for **structured one-shot authoring** (compare
`PROMPT.md §4` — "structured one-shot output tasks"). Steps that require
observe-act-verify loops (run linter → interpret exit code → fix → re-run) are
the defining use case of **RISEN+ReAct** or **RISE-DX**, as correctly declared in
`prompts/skills-frontmatter-index-suite/prompt.md` (which also has a build phase).

Executing agents that enforce framework semantics (cf. `AGENTS.md §Gherkin`) may
either refuse the tool-execution step or proceed without the expected ReAct loop,
producing an un-verified deliverable.

**Fix:** Change `prompt_framework: RISEN` to `prompt_framework: RISEN+ReAct` and
add a minimal ReAct loop description around Step 8 (Thought → Act → Observe for
each linter run).

---

## Structural Findings

### S-1 — `task_spawns_research` pre-populated in Task 010 before research exists

**File:** `tasks/010-skills-frontmatter-index-suite/task.md`, frontmatter

```yaml
task_spawns_research:
  - skills-frontmatter-index-suite
```

`TASK.md §6` (Gherkin scenario "Spawning research from a Task") states:

> "When the agent finishes the research run, the research slug MUST appear in
> `task_spawns_research`."

The operative word is *finishes*: the slug is added upon closure, not at task
creation. There is currently no `/research/skills-frontmatter-index-suite/`
directory. While the linter waives §7.3 (Research Linkage) for non-`done` tasks,
any agent that reads `task_spawns_research` to discover *existing* research
workspaces will find a dangling reference and may either create a duplicate
workspace or error-out.

**Fix:** Clear `task_spawns_research` to `[]` at authoring time. The executing
agent will populate it when research is spawned, per the lifecycle.

---

### S-2 — Concurrent write risk on `SKILLS.md` (Tasks 009 and 011)

**Files:** `tasks/009-author-skills-root-spec/task.md`,
`tasks/011-skills-frontmatter-schema-files/task.md`

Both tasks list `SKILLS.md` in `task_affects_paths`:

- Task 009 authors `SKILLS.md` from scratch.
- Task 011 §Plan step 7 updates prose sections of `SKILLS.md` to reference the
  canonical JSON schemas by link.

If two agents run concurrently — which is a supported pattern in this repo (cf.
Jules / Claude Code parallelism) — the second write will silently clobber the
first, or produce a merge conflict that blocks both tasks.

**Fix:** Add a sequencing constraint to Task 011's `task.md` under a new
`## Sequencing` section: "Task 011 MUST NOT begin until Task 009 `task_status`
is `done`." Alternatively, encode this as a `task_blocked_by: [author-skills-root-spec]`
frontmatter key (which Task 008 §5 has already proposed adding).

---

### S-3 — Token-efficiency benchmark (≥8x) lacks measurement methodology

**File:** `tasks/010-skills-frontmatter-index-suite/task.md`, §Plan step 7

The acceptance criterion reads:

> "Average speedup ≥ 8x; if a question is < 4x, redesign the index entry shape."

"Speedup" is not defined. Possible interpretations:
- Bytes read from disk (file body vs. index entry)
- Tokens consumed by the LLM (prompt tokens needed to answer the question)
- Wall-clock latency
- Number of tool calls

Without a definition, the executor cannot produce a reproducible benchmark, and
a reviewer cannot verify the ≥8x claim.

**Fix:** Add a one-paragraph `## Benchmark Methodology` note in `task.md` (or
delegate to the prompt, which already uses the four-stage architecture framing)
defining "speedup" as: `(tokens-to-answer-via-body-read) / (tokens-to-answer-via-index)`,
where token counts are estimated by `tiktoken` or a repo-local counter.

---

### S-4 — Skill count discrepancy (14 stated, 15 present)

**Files:** `tasks/010-skills-frontmatter-index-suite/task.md` §Background,
PR body

Both the task and the PR body refer to "14 skills in `/skills/`". An `ls`
of the current `skills/` directory yields 15 entries:

```
dramatica-theory       dramatica-vocabulary    drive-markdown-converter
gdrive-notion-curator  ncp-author              notebooklm-prompt-architect
novel-architect        pdf-to-markdown         prompt-optimizer
ralph-skill            research-prompt-optimizer  skills-skill-bootstrap
spec-skill             suno-lyric-writer       the-agency-system-architect
```

The discrepancy is minor in isolation but will cause the token-efficiency
benchmark to compute the baseline wrong (incorrect "280 KB total" claim).

**Fix:** Update the count to 15 in Task 010 §Background. Re-measure the total
byte size if the 280 KB figure is load-bearing.

---

### S-5 — `prompt_target_agent: "Claude Code"` mismatches multi-agent scope

**Files:** `prompts/author-skills-root-spec/prompt.md`,
`prompts/skills-frontmatter-schema-files/prompt.md` (frontmatter)

All three new prompts declare `prompt_target_agent: "Claude Code"`, yet:

- Task 009's §Brief and `task.md` explicitly state: "Whichever agent (Claude Code,
  Jules, or Gemini) picks up Task 009".
- The entire skills-portability architecture (P.1–P.3, adapter overlays, Jules /
  Gemini portability prompts) is motivated by *multi-agent* execution.

An agent routing layer that reads `prompt_target_agent` (e.g. the index from
Task 010, or a future Jules dispatcher) will see "Claude Code" and decline to
route these prompts to Jules or Gemini, undermining the very portability the PR
is meant to establish.

**Fix:** Change `prompt_target_agent` in all three prompts to `"any"` (per the
allowed values in `TASK.md §3.3`).

---

## Minor Findings

### M-1 — No `notes.md` in any task folder

**Files:** `tasks/009-*/`, `tasks/010-*/`, `tasks/011-*/`

`TASK.md §2` marks `notes.md` as `OPTIONAL`, but all three tasks carry complex
interdependencies, open questions (Task 009 §Plan step 3 proposes five `skill_*`
keys "subject to research-proposal review"), and an explicit §10 placeholder
for unresolved UNCERTAIN markers from `skills-skill-architecture`. Without a
`notes.md`, the next agent has no place to accumulate working assumptions without
polluting `task.md`.

**Recommendation:** Author a minimal `notes.md` in each task folder with an
"Open Questions" header and the UNCERTAIN items extracted from the architecture
research.

---

### M-2 — `AGENCY_SKILLS_ALLOW_STALE=1` override unconstrained

**File:** `prompts/author-skills-root-spec/prompt.md`, §B.4

The override variable is defined as: "the agent MAY override with
`AGENCY_SKILLS_ALLOW_STALE=1` for offline work." There is no constraint on who
may set this variable (agent vs. human), no mention of audit logging when the
override is used, and no maximum staleness cap beyond which even the override is
refused. In a multi-agent environment where Jules runs autonomously, this creates
an unmonitored bypass path.

**Recommendation:** Add a normative clause: "An agent MUST log a warning to its
friction log when `AGENCY_SKILLS_ALLOW_STALE=1` is detected. The staleness gate
MUST NOT be bypassed for more than 72 h (the 24 h soft limit × 3 tolerance
factor)."

---

### M-3 — `templates/skill.md` listed as deliverable but no template directory scan

**File:** `prompts/author-skills-root-spec/prompt.md`, §E Expectations table

The prompt mandates `/templates/skill.md` as a deliverable. The existing
`templates/` directory likely already contains `task.md` and `prompt.md`
skeletons — the prompt should instruct the executor to read these first to
ensure structural parity (same `REPLACE` token convention, same validator
skip-rule). As written, the executor may invent a different token format.

**Fix:** Add to §I (Input): "8. `/templates/task.md` and `/templates/prompt.md` —
read these to confirm the `REPLACE` token and validator-skip convention before
authoring `templates/skill.md`."

---

### M-4 — `task_status: open` vs `status: active` semantic tension

**Files:** All three new `task.md` files (frontmatter)

Every new `task.md` carries:

```yaml
status: active       # L1 Vault Core
task_status: open    # L2 Task namespace
```

`status: active` is used in the repo for spec files and prompt files meaning
"this file is the live, current version" — cf. `AGENTS.md`, `TASK.md`,
`PROMPT.md` all have `status: active`. For a *task* file, `status: draft` or
`status: active` carries the same "not yet closed" connotation. The two fields
coexist but the semantics differ: `status` tracks the file lifecycle,
`task_status` tracks the work lifecycle. This is correct per `TASK.md §3.2`
but could confuse a future parser that conflates the two.

**Recommendation:** Document this distinction explicitly in `SKILLS.md §1` (or
`TASK.md §3.2`) so the next Task that introduces a new L2 namespace does not
accidentally collapse the two fields.

---

## What is Good

- **Interdependency architecture is excellent.** Task 009 → 010 → 011 forms a
  clear DAG with no hidden coupling (except S-2 above). Each task's §Links
  section fully cross-references siblings.
- **RFC-2119 normativity is consistent.** Every normative sentence in all three
  prompts uses exactly one keyword in all-caps. No violations found.
- **RISEN+ReAct is correctly applied to Task 010's prompt.** The two-phase
  structure (OSS survey → build) maps cleanly to the framework.
- **Prompt self-containedness is strong.** Each prompt restates the §RFC 2119
  boilerplate, defines its Role, and specifies its Deliverable Lock (§E table).
  A fresh agent reading the prompt without any repo context can follow it.
- **Pre-commit bypass is transparently disclosed.** The PR body lists all 15
  pre-existing errors, names the tasks tracking them, and provides a
  per-file `validate-frontmatter.py` verification showing zero new errors.
  This is the right level of disclosure.
- **Cross-link reciprocity is complete.** Every `task_uses_prompts` resolves,
  every `prompt_relates_to_task` is reciprocated, `prompt_spawned_from_research`
  points to existing research workspaces.

---

## Verdict

**Request changes** on C-1 (section count) and C-2 (framework declaration)
before this is merged; both are in `prompts/author-skills-root-spec/prompt.md`
and are a two-line fix. S-1 through S-5 are strongly recommended fixes but
could be resolved by the picking-up agent in a follow-up commit to the same
branch. M-1 through M-4 are at reviewer discretion.
