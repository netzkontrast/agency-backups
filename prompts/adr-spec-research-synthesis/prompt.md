---
type: prompt
status: active
slug: adr-spec-research-synthesis
summary: "Drives Task 027: analyze root specs + tooling via /sc:analyze and /sc:brainstorm, then synthesize the repo-native ADR governance specification (§0–§9) that integrates the Gemini draft with this repo's actual governance conventions."
created: 2026-05-05
updated: 2026-05-05
prompt_kind: research-proposal
prompt_framework: RISEN+ReAct
prompt_target_agent: "Claude Code"
prompt_relates_to_task: adr-spec-research-synthesis
---

# ADR Spec Research Synthesis — Research-Proposal Prompt

## R — Role

You are the **Repository Governance Architect** for `netzkontrast/agency`. Your mission is to produce a single, authoritative ADR governance specification that is simultaneously:
- Theoretically sound (grounded in the Gemini draft's MDL, DAG, and Gherkin framework)
- Structurally compatible (honoring the repo's existing Frontmatter Ontology, tooling surface, and branching conventions)
- Immediately deployable (every normative statement has a mechanical enforcement path in this specific repo)

You are not permitted to copy the Gemini draft verbatim. Every §0–§9 section must be re-derived against the actual repo content you find during execution.

## I — Input

Primary sources (read in this order, per CONSTRAINT BLOCK 1 of the originating research prompt):

1. **Repo root specs:** `AGENTS.md`, `TASK.md`, `PROMPT.md`, `RESEARCH.md`, `FOLDERS.md`, `PRE_COMMIT.md`, `MAINTENANCE.md`, `FRUSTRATED.md`, `README.md`
2. **Tooling:** `tools/check-governance.sh`, `tools/fm/validate.py`, `tools/fm/extract.py`, `tools/fm/edit.py`, `tools/fm/query.py`
3. **Existing schemas:** `maintenance/schemas/header-ontology.json` (read if exists; log absence if not)
4. **Gemini ADR draft:** `research/gemini/agency-adr-governance-spec/adr-governance-spec.md` (theoretical reference only)
5. **Gemini research prompt:** `research/gemini/agency-adr-governance-spec/research-prompt_agency-adr-governance-spec.md` (for critical-thinking method definitions)

## S — Steps

### Step 0 — Research Workspace Initialisation

Create the workspace at `research/adr-spec-research-synthesis/` following `RESEARCH.md` §2 structure. Set all `readme.md` files with correct frontmatter. Do not proceed to Step 1 until the workspace is initialised.

### Step 1 — `/sc:analyze` Root Specs and Tooling

Invoke `/sc:analyze` with scope: all files listed under Input §1 and §2.

Record findings in `research/adr-spec-research-synthesis/workspace/analysis.md`. The analysis MUST answer:

1. Which architectural decisions are already implicitly in force in this repo (not formally documented as ADRs)?
2. Which structural conventions does any new ADR governance spec MUST honour (naming, paths, frontmatter schema, hook architecture)?
3. Where does the Gemini draft's assumed structure (e.g., `docs/decisions/`, standalone CLI) conflict with the existing repo topology?
4. Which existing tooling primitives (frontmatter parsing, validation, file traversal) can be reused by the synthesis pipeline?

Apply [M06] Source Triangulation: every finding MUST be confirmed in ≥ 2 source files before being recorded as a fact.

### Step 2 — `/sc:brainstorm` Integration Points

Invoke `/sc:brainstorm` using the analysis from Step 1 as context. Brainstorm answers to these five questions:

1. **Storage path:** Where do ADR files live? `docs/decisions/` conflicts with the `research/`-centric model. Justify the chosen path against `FOLDERS.md`.
2. **CLI integration:** How does `agency-adr` attach to `tools/` without duplicating `tools/fm/` primitives?
3. **Frontmatter composition:** How does the ADR schema (`id`, `title`, `status`, `date`, `supersedes`) compose with the L1/L2 Vault Core Ontology without collision?
4. **AGENTS.md ownership:** How is the synthesis pipeline's overwrite authority reconciled with the manually authored content currently in `AGENTS.md`?
5. **Migration path:** How are implicit architectural decisions (found in Step 1) bootstrapped as the first batch of formal ADRs?

Record output in `research/adr-spec-research-synthesis/workspace/brainstorm.md`. Every brainstorm conclusion MUST be labelled as either `[RESOLVED]`, `[OPEN — needs human decision]`, or `[DEFERRED to Task 029]`.

Apply [M07] Contradiction Log: when two brainstorm conclusions conflict, log both in `research/adr-spec-research-synthesis/reflection/M07-contradictions.md`.

### Step 3 — [M13] Adversarial Query Expansion

Before drafting the spec, invoke [M13] Adversarial Query Expansion along all four axes to stress-test the integrated model:

- **Adjacent:** What governance patterns in similar multi-agent repos (adr-tools, log4brains) contradict your current model?
- **Opposing:** What would cause the ADR governance spec to *fail* in this repo? (e.g., agents simply never author ADRs; synthesis pipeline silently produces wrong AGENTS.md)
- **Abstraction:** What higher-level principle does the entire spec rest on? Is that principle honoured by this repo's culture?
- **Orthogonal:** Apply the MDL lens: given the repo's current AGENTS.md is approximately N tokens, what is the maximum ADR corpus size that keeps the synthesized output under 2,000 tokens?

Record in `research/adr-spec-research-synthesis/reflection/M13-query-expansion.md`. Apply [M08] What Would Change My Mind for any conclusion that is high-stakes.

### Step 4 — Draft Repo-Native ADR Governance Spec

Draft `research/adr-spec-research-synthesis/output/SPEC.md` following the §0–§9 schema from the Gemini draft. Every section MUST be re-derived from Step 1–3 findings. Sections MUST NOT be copied from the Gemini draft.

Mandatory content per section:

- **§0 Status & Provenance:** Status IN-FORCE, direct repo file citations, world-change annotation addressing `llms.txt` emergence.
- **§1 Normative Conventions:** Reproduce RFC-2119 binding paragraph verbatim; Gherkin binding; style guide with stable `A.<Aspect>.<Stmt>` IDs.
- **§2 System-Level Conventions:** Resolved storage path, AGENTS.md ownership split (synthesized vs manually-authored sections), hook integration diagram.
- **§3–§7 Aspects (Explore/Plan/Implement/Review/Validate):** Each MUST contain §X.1 normative statements, §X.2 Gherkin acceptance criteria with `# anchor:` comments, §X.3 rationale in lowercase prose.
- **§7 Validate:** Complete JSON-Schema for ADR frontmatter composing with L1/L2 Vault Core; CLI command shape for `agency-adr validate` and `agency-adr synthesize`.
- **§8 Known Limitations:** Every `[OPEN]` and `[DEFERRED]` item from Step 2 appears here with an explicit owner and unblock condition.
- **§9 Knowledge Base Index:** All sources used in Steps 1–3; Contradiction Log summary; Query Expansion Log.

### Step 5 — Reflection and Verification

1. Write all five mandatory reflection checkpoints (CB0): Kickoff, Mid-run, Post-M13, Pre-synthesis, Post-synthesis.
2. Run `tools/check-governance.sh` against all new files; fix any failures.
3. Populate `research/adr-spec-research-synthesis/reflection/friction-log.md` with FL[0-3] declaration per `FRUSTRATED.md`.

### Step 6 — Closure

1. Mark `task_status: done` in `tasks/027-adr-spec-research-synthesis/task.md`.
2. Confirm `tasks/028-adr-tooling-impl-plan/task.md` and `tasks/029-adr-assumption-audit/task.md` exist and are set to `open`.

## E — Expectations

**Success criteria:**

- `research/adr-spec-research-synthesis/output/SPEC.md` exists with all §0–§9 sections populated.
- Every MUST statement has a Gherkin acceptance criterion with an `# anchor:` comment.
- Every `[OPEN]` item from Step 2 brainstorm is surfaced in §8.
- `tools/check-governance.sh` exits 0.
- Friction log declares FL[0-3].

**Non-goals (do not produce):**
- Working implementation code for `agency-adr` (that is Task 028's scope).
- Concrete ADR records (the spec governs HOW, not WHAT decisions to record).
- Changes to `AGENTS.md` content (the spec defines synthesis rules; execution is Task 028).

## N — Narrowing

- Output schema: locked to §0–§9 structure. No additional top-level sections.
- Source priority: repo files first, Gemini draft second (reference only), external sources for triangulation only.
- Temporal scope: 2011-01-01 through today. Pre-2022 sources on LLM/agent patterns are background only.
- BCP-14 keyword density: exactly one per normative sentence.
- `additionalProperties: true` in the JSON-Schema to allow future L2 namespace extension without breaking validation.
