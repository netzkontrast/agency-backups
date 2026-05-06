---
type: spec
status: active
slug: agents-spec
summary: "Entry-point governance spec for all agents operating in this repository. Defines task routing, folder rules, spec language (RFC 2119 + Gherkin), and the Frontmatter Ontology every agent must apply."
created: 2026-05-02
updated: 2026-05-05
---

# Agent Instructions

Welcome, agent. This repository manages development and deep research tasks.

**Before committing any work:** You MUST review and abide by the checks defined in [PRE_COMMIT.md](./PRE_COMMIT.md).

**Last step of every Claude Code run:** After your final commit and push succeed, you MUST invoke `/sc:createPR` to open a pull request for review. See [§ Closing Run Procedure (Claude Code)](#closing-run-procedure-claude-code) below for the binding rule.

## Session Setup

Before doing any other work, you MUST verify that all tooling dependencies are installed. Run the bootstrap script from the repository root:

```bash
./install.sh
```

This installs the packages declared in [`tools/requirements.txt`](./tools/requirements.txt) (`PyYAML`, `jsonschema`, `pytest`) and prints a per-package confirmation. The script is idempotent — rerunning it on an already-configured environment is safe and fast.

After `install.sh` exits 0, you MUST confirm the full tooling stack is operational:

```bash
tools/check-governance.sh
```

If `check-governance.sh` exits non-zero, you MUST resolve all reported errors before proceeding. A failing governance check indicates a broken environment or uncommitted drift; starting work on top of it will compound the problem.

### Normative Rules

- **SS.1** An agent MUST run `./install.sh` at the start of every session before reading or writing any repository file.
- **SS.2** An agent MUST run `tools/check-governance.sh` immediately after `install.sh` completes and MUST NOT proceed if it exits non-zero.
- **SS.3** An agent MUST NOT skip setup on the assumption that dependencies are already installed — the script is idempotent and the cost of skipping is a silent broken environment.

```gherkin
Feature: Agent bootstraps tooling before session work

  # anchor: SS.1.1
  Scenario: Fresh session installs dependencies first
    Given an agent has just started a new session in this repository
    When the agent is about to read or write any file
    Then the agent MUST run ./install.sh before any other action
    And the agent MUST confirm install.sh exited 0

  # anchor: SS.2.1
  Scenario: Governance check gates all further work
    Given ./install.sh has exited 0
    When the agent runs tools/check-governance.sh
    Then if it exits non-zero the agent MUST stop and report all errors to the user
    And the agent MUST NOT create, edit, or commit any file until the check passes
```

## Folder Management & Workflow Drift

You MUST abide by the rules defined in [FOLDERS.md](./FOLDERS.md).

**Preventing Workflow Drift:** To prevent this repository's protocols from slowly drifting out of sync with reality, you are required to document your assumptions. If you assumed a certain file should be JSON instead of Markdown, or if you assumed a specific subfolder was unnecessary, you MUST log that assumption in the relevant folder's `readme.md`. This ensures human operators and future agents understand *why* the repository looks the way it does.

## Mandatory Frustration Feedback

We rely on your honest feedback to improve these protocols. You MUST consult [FRUSTRATED.md](./FRUSTRATED.md) to accurately log the Frustration Level (FL) associated with your task. **This is a mandatory step for every session, even if everything went perfectly (FL0).**

## Closing Run Procedure (Claude Code)

This section binds the *final* step of every Claude Code session. It applies to Claude Code only; Jules and Gemini agents follow their own platform conventions.

### Skill Provenance

The `/sc:createPR` slash-command is provided by the **SuperClaude Framework** at [`src/superclaude/commands/createPR.md`](https://github.com/netzkontrast/SuperClaude_Framework/blob/main/src/superclaude/commands/createPR.md). It is installed automatically alongside the rest of the `/sc:*` command set; no per-repository setup is required beyond having SuperClaude available in the session.

### Normative Rules

- **CR.1** A Claude Code agent MUST invoke `/sc:createPR` as the final action of every session, immediately after a successful `git push`.
- **CR.2** The agent MUST NOT consider a session complete until `/sc:createPR` has either (a) opened a new pull request, or (b) returned an explicit no-op confirmation that an existing PR already covers the pushed commits.
- **CR.3** The agent MUST NOT invoke `/sc:createPR` if pre-commit checks (per [PRE_COMMIT.md](./PRE_COMMIT.md)) failed or were skipped. A failing or unverified working tree MUST NOT be promoted to a PR. The `/sc:createPR` skill itself enforces this gate by re-running `tools/check-governance.sh` before opening the PR.
- **CR.4** If `/sc:createPR` errors out, the agent MUST NOT silently exit — the error MUST be reported to the user with the exact command output, and the session MUST remain in `in_progress` for the operator to triage.
- **CR.5** The PR body created by `/sc:createPR` MUST reference (a) the closed Task slug(s) under `/tasks/` if any, and (b) the FL declaration from the friction log per [FRUSTRATED.md](./FRUSTRATED.md).
- **CR.6** Re-invocation of `/sc:createPR` on a branch that already has an open pull request MUST be a no-op (the skill is idempotent). Agents MUST NOT create duplicate PRs to "force-update" an existing one — pushing additional commits to the same branch updates the open PR automatically.

### Gherkin Scenario

```gherkin
Feature: Claude Code closes every run with /sc:createPR

  # anchor: CR.1.1
  Scenario: Successful run ends with PR creation
    Given a Claude Code session has finished its work
    And the agent has committed and pushed all changes
    And tools/check-governance.sh exited 0 on the final commit
    When the agent reaches the end of the session
    Then the agent MUST invoke /sc:createPR before declaring the session complete
    And the resulting pull request body MUST cite the closed Task slug(s) and the FL declaration

  # anchor: CR.1.2
  Scenario: Pre-commit failure blocks PR creation
    Given a Claude Code session is finishing
    And tools/check-governance.sh exited non-zero on the most recent commit attempt
    When the agent considers invoking /sc:createPR
    Then the agent MUST NOT invoke /sc:createPR
    And the agent MUST report the linter diagnostics to the user
    And the session MUST remain open for triage
```

## Task Type Routing

Three top-level governance specs partition the work this repository performs. Pick the one that matches your request *before* writing any file:

| If the request is… | Consult | Operational directory |
|---|---|---|
| Coordination/orchestration with a goal, plan, and todo | [TASK.md](./TASK.md) | [/tasks/](./tasks/) |
| Authoring an executable instruction set (research proposal, follow-up, tool instruction, task-spec) | [PROMPT.md](./PROMPT.md) | [/prompts/](./prompts/) |
| Executing a prompt to produce evidence, synthesis, reflection, output | [RESEARCH.md](./RESEARCH.md) | [/research/](./research/) |

**Separation of concerns is hard:** a Task MUST link to its prompt (never inline it); research MUST NOT contain prompt drafts; follow-up questions discovered during research MUST be filed as new prompts in `/prompts/`. The full audit-graph rules and Frontmatter Ontology (Layered Schema with Namespacing) live in [TASK.md §3](./TASK.md).

---

## Spec Language Reference

Every agent in this repository MUST speak a shared formal language when writing normative specifications, acceptance criteria, or governance rules. This section defines that language. The **canonical, complete definitions** live in [`/maintenance/language-spec.md`](./maintenance/language-spec.md). The rules below are the authoritative binding summary every agent must internalize before writing any spec.

### RFC 2119 Normative Keywords

The key words **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHALL NOT**, **SHOULD**, **SHOULD NOT**, **RECOMMENDED**, **NOT RECOMMENDED**, **MAY**, and **OPTIONAL** in this repository are to be interpreted as described in BCP 14 \[RFC 2119\] \[RFC 8174\] **when, and only when, they appear in all capitals**.

#### Quick Reference

| Keyword | Strength | Meaning |
|---|---|---|
| MUST / REQUIRED / SHALL | Absolute | No deviation permitted under any circumstances. |
| MUST NOT / SHALL NOT | Absolute prohibition | The behaviour is never allowed. |
| SHOULD / RECOMMENDED | Strong default | Deviation allowed only with documented justification. |
| SHOULD NOT / NOT RECOMMENDED | Strong discouragement | Deviation allowed only with documented justification. |
| MAY / OPTIONAL | Permissive | Fully at the implementer's discretion. |

#### Usage Rules

- **R1.** Every normative statement MUST use exactly one RFC 2119 keyword per sentence.
- **R2.** Rationale paragraphs, motivation text, and prose explanations MUST NOT contain RFC 2119 keywords in uppercase. Lowercase "should" or "may" in prose is permitted.
- **R3.** Each normative statement SHOULD be addressable by a stable identifier of the form `<Spec-Letter>.<Section>.<Index>` (e.g., `A.3.2`), so that cross-references and audit logs can pin-point the exact clause.
- **R4.** A spec file MUST include a verbatim `§ RFC 2119` declaration section before its first normative clause (see `/maintenance/language-spec.md` for the canonical boilerplate).

### Gherkin Syntax Binding

Every behavioural example, agent-interaction scenario, or hand-off specification in every produced spec MUST use standard Gherkin syntax and MUST be self-contained and executable.

#### Keywords

| Keyword | Role |
|---|---|
| `Feature:` | Names the capability under test. Every Gherkin block must be nested inside a Feature. |
| `Background:` | Shared setup steps applied to every Scenario in the Feature. OPTIONAL; RECOMMENDED when ≥ 3 scenarios share the same Given setup. |
| `Scenario:` | A single, named behavioural example. |
| `Scenario Outline:` | A parametric scenario template. MUST be paired with an `Examples:` table. RECOMMENDED when the same behavioural shape repeats with varying inputs. |
| `Given` | Establishes pre-conditions. At least one Given MUST appear in every Scenario. |
| `When` | Describes the triggering action or event. At least one When MUST appear in every Scenario. |
| `Then` | States the expected observable outcome. At least one Then MUST appear in every Scenario. |
| `And` / `But` | Continuation of the immediately preceding `Given`, `When`, or `Then`. MUST NOT be used as the first step in a Scenario. |

#### Validity Rules

- **G1.** Every `Scenario` block MUST contain at least one `Given`, at least one `When`, and at least one `Then`.
- **G2.** `And` and `But` MUST follow a `Given`, `When`, or `Then` — never open a scenario.
- **G3.** A scenario MUST be **self-contained**: it MUST NOT reference external context that is not also defined within the same spec file.
- **G4.** A scenario MUST be **executable**: a human or agent reading it MUST be able to enact every step without additional clarification.
- **G5.** Each `Scenario` SHOULD carry an anchor comment on the line immediately above it: `# anchor: <stable-id>`. This enables cross-referencing from prose.
- **G6.** Acceptance criteria in this repository MUST be written as Gherkin scenarios, not as bullet-list assertions.

#### Minimal Valid Example

```gherkin
Feature: Agent picks up an open Task

  # anchor: T.6.1
  Scenario: Agent claims a task before writing
    Given a file "/tasks/003-example/task.md" exists
    And its frontmatter field "task_status" is "open"
    When an agent decides to work on the task
    Then the agent MUST set "task_status" to "in_progress" before any other write
    And the agent MUST set "task_owner" to its own identifier
    And the agent MUST update "updated" to today's ISO-8601 date
```

---

## Frontmatter Ontology (Summary)

Every Markdown file in this repository SHOULD carry frontmatter. Files inside operational directories (`/tasks/`, `/prompts/`, `/research/`) MUST carry frontmatter. The schema is a **Layered Schema with Namespacing** derived from `research/obsidian-frontmatter-agentic-spec/output/SPEC.md` and canonically defined in [TASK.md §3](./TASK.md).

### Layer Overview

| Layer | Scope | Mandate |
|---|---|---|
| **L0** — Obsidian Reserved | `tags`, `aliases`, `cssclasses` | Optional; preserved if present. |
| **L1** — Vault Core | `type`, `status`, `slug`, `summary`, `created`, `updated` | MUST be present on all operational files. |
| **L2** — Domain Namespace | `task_*`, `prompt_*`, `research_*` keys | MUST be present inside the directory that owns the namespace. |
| **L3** — Agent-Only | Vector embeddings, graph scores, token matrices | MUST NOT appear in YAML. Lives in `/.agent_cache/<file>.meta.json`. |

### L1 Field Semantics

| Key | Type | Agent Guidance |
|---|---|---|
| `type` | string | One of: `task`, `prompt`, `research`, `spec`, `readme`, `note`, `index`. Drives parser routing — read this first. |
| `status` | string | One of: `draft`, `active`, `blocked`, `completed`, `archived`. Archived files MAY be skipped by the agent to save tokens. |
| `slug` | string | Kebab-case; MUST match the enclosing folder name where applicable. |
| `summary` | string | Token-cheap tl;dr. The agent should read `summary` before opening the body. This is the primary token-saving lever in the repo. |
| `created` | date | ISO-8601 (`YYYY-MM-DD`). Set once at creation; never update. |
| `updated` | date | ISO-8601 (`YYYY-MM-DD`). MUST be updated on every substantive change. |

### YAML Depth Rule

YAML frontmatter MUST NOT nest beyond one level. Lists MUST contain scalars or short strings only. This is a hard constraint to prevent LLM YAML-parsing hallucinations.

The complete ontology with all L2 namespaces and worked examples lives in [TASK.md §3](./TASK.md). The Obsidian-native reasoning behind this design is in [`research/obsidian-frontmatter-agentic-spec/output/SPEC.md`](./research/obsidian-frontmatter-agentic-spec/output/SPEC.md).

---

## Narrative Ontology — Dramatica × NCP × Novel-Architect Bridge

This is a separate ontology from the Frontmatter Ontology. The Frontmatter Ontology governs **every operational file**; the Narrative Ontology governs **only narrative-craft work** (Dramatica theory, NCP storyforms, Kohärenz-Protokoll novel-architect, Suno-lyric / Agency-System triptychon work). Most repository tasks do not touch it. Loading the schemas inside a non-narrative session is a token-budget mistake.

### Authoritative Location

| File | Purpose |
|---|---|
| [`maintenance/schemas/narrative-ontology/ontology.schema.json`](./maintenance/schemas/narrative-ontology/ontology.schema.json) | One ontology entry contract (kind, aliases, dynamic-pair links, NCP mapping, provenance, scenarios). |
| [`maintenance/schemas/narrative-ontology/scenarios.schema.json`](./maintenance/schemas/narrative-ontology/scenarios.schema.json) | Persona-scenario entry contract (`novel.*` / `lyric.*` IDs). |
| [`maintenance/schemas/narrative-ontology/term-frontmatter.schema.json`](./maintenance/schemas/narrative-ontology/term-frontmatter.schema.json) | Per-term YAML block contract for `skills/dramatica-vocabulary/references/*.md`. |
| [`maintenance/schemas/narrative-ontology/theory-chunk.schema.json`](./maintenance/schemas/narrative-ontology/theory-chunk.schema.json) | Theory-chapter frontmatter contract for `skills/dramatica-theory/references/*.md`. |
| [`maintenance/schemas/narrative-ontology/ontology.json`](./maintenance/schemas/narrative-ontology/ontology.json) | Canonical entry table (~215 entries). The single source of truth for all narrative IDs. |
| [`maintenance/schemas/narrative-ontology/scenarios.json`](./maintenance/schemas/narrative-ontology/scenarios.json) | The eleven persona scenarios (six Novel Author, five Organist / Lyric Architect). |
| [`maintenance/schemas/narrative-ontology/readme.md`](./maintenance/schemas/narrative-ontology/readme.md) | Reader's guide; statement of OQ-A/B/C resolutions; provenance rule. |

The query surface over the ontology is [`tools/dramatica-nav/nav.py`](./tools/dramatica-nav/nav.py). Agents SHOULD prefer `nav.py` over loading the JSON files directly; it returns one record + a pointer rather than the whole table.

> **Status note.** The schemas, ontology, and navigator are produced by [Task 015](./tasks/015-integrate-dramatica-ncp-skills/task.md) executing [the integrate-dramatica-ncp-skills prompt](./prompts/integrate-dramatica-ncp-skills/prompt.md). Until that task closes, paths above MAY resolve to placeholders or 404. The load triggers below remain binding the moment the files exist — agents MUST NOT pre-load before existence-check, and MUST start using them once they do exist.

### When to Load (RFC 2119)

- **NO.1.** An agent working on **Dramatica theory or vocabulary** (`skills/dramatica-theory/`, `skills/dramatica-vocabulary/`) MUST consult `nav.py` before reading the prose chapters when the question is structural ("what's the dynamic pair of Trust?", "which Quad does Logic sit in?", "which scenarios does Crucial Element appear in?"). Prose loading is RECOMMENDED only when the question is conceptual ("explain the Story Mind premise", "why does MC Resolve matter?") and the navigator's pointer directs to a chapter.
- **NO.2.** An agent authoring or auditing an **NCP** document (`*.ncp.json`, `skills/ncp-author/`) MUST resolve every Dramatica-flavored slot through the ontology. The mapping rule is one-way: ontology IDs map to NCP enum strings; NCP enum strings are owned upstream and MUST NOT be coined from the Dramatica side. Use `nav.py by-ncp <enum-string>` to find the ontology ID, or `nav.py by-id <ontology-id>` to find the NCP string.
- **NO.3.** An agent working on the **`novel-architect` Kohärenz Protokoll** (any file under `skills/novel-architect/references/canon/`) MUST consult the ontology before changing a structural canon entry, so the change references a canonical ID rather than a free-text label. Direct prose canon (DKT-Physik, Prosa-Regeln, Mandate in `canon-meta.md`) does not trigger this rule.
- **NO.4.** An agent doing **Agency-System triptychon / Suno-lyric** work (`skills/the-agency-system-architect/`, `skills/suno-lyric-writer/`) SHOULD consult the ontology when a track, verse, or arc encodes a Dramatica concept. Tag the concept with its `lyric.*` scenario ID where applicable so the cross-skill audit graph stays intact.
- **NO.5.** An agent doing **non-narrative work** (governance refactors, frontmatter linters, build tooling, anything not under the four narrative skills) MUST NOT load the Narrative Ontology files. Loading wastes tokens on data the work does not need. The Frontmatter Ontology governs that work; this ontology does not.
- **NO.6.** When the navigator and the prose disagree, the **navigator is authoritative for IDs and relationships**; the **prose is authoritative for meaning**. The skills' own SKILL.md files document this precedence rule under their `## Navigator` sections.

### What the Schemas Bind

- **Canonical IDs.** The fourth throughline is `throughline.relationship` (`canonical_label: "Relationship Story"`). Aliases `Subjective Story`, `SS`, `Relationship`, `RS` are recorded but MUST NOT be used as IDs in machine-readable contexts. Same pattern: `throughline.influence` (canonical `Influence Character`; alias `Impact Character` / `IC`) and `character-dynamic.problem-solving-style` (canonical `Problem-solving Style`; alias `Mental Sex`; deprecated `Male/Female problem-solving`).
- **Kind discrimination.** `kind: element` is one of the canonical 64; `kind: concept` is a meta-entry *about* a structural slot (Crucial Element, Symptom, Focus, Direction). Likewise `kind: type` (16 canonical) vs `kind: concept`. Agents MUST NOT silently merge these.
- **Locale aliases.** Aliases are stored as flattened depth-1 keys: `aliases_en: [...]`, `aliases_de: [...]`, `deprecated_aliases_<locale>: [...]`. Per the YAML Depth Rule, no nested-map form is permitted.
- **Dynamic-pair representation.** Every `kind: element | variation` MAY carry a `dynamic_pair_id` pointing at its partner. Each of the 75 reciprocal pairs ALSO has a standalone `kind: dynamic-pair` entry with `pair_member_a` + `pair_member_b`. The reciprocity invariant is enforced by `tools/dramatica-nav/validate.py`.
- **NCP closure.** `ncp_appreciation` is OPTIONAL. Approximately 60% of entries carry it as partial (`ncp_appreciation_partial: true`), 30% omit it (archetypes, quads, dynamic-pairs, concepts — NCP has no native enum target), 10% carry it cleanly (throughlines, story-level appreciations). Validators MUST treat absence-with-reason as legal.

### Gherkin Scenarios (Normative)

```gherkin
Feature: Agent uses the Narrative Ontology when narrative work is in scope

  # anchor: NO.1.1
  Scenario: Structural lookup uses the navigator before prose
    Given an agent is asked the dynamic pair of a Dramatica term
    And tools/dramatica-nav/nav.py exists
    When the agent answers the question
    Then the agent MUST invoke nav.py by-id (or by-alias) before opening any chapter file
    And the agent SHOULD open a chapter only if nav.py's term_file pointer indicates the answer requires prose

  # anchor: NO.2.1
  Scenario: NCP document fills slots through the ontology
    Given an agent is authoring or auditing a *.ncp.json document
    When the agent fills a Dramatica-flavored slot (appreciation, narrative_function, throughline)
    Then the agent MUST resolve the canonical ontology ID first
    And the agent MUST NOT coin a new NCP enum value
    And if the slot has no clean NCP target the agent MUST use the parallel custom_* field with its *_namespace companion

  # anchor: NO.5.1
  Scenario: Non-narrative work does not load the ontology
    Given an agent is working on governance, lint tooling, or non-narrative skills
    When the agent considers loading maintenance/schemas/narrative-ontology/ontology.json
    Then the agent MUST NOT load it
    And the agent SHOULD log "narrative ontology skipped — non-narrative scope" if narrative content is mentioned only in passing
```

---

## Gherkin Scenarios (Normative) — Agent Behaviour

```gherkin
Feature: Agent reads a file before acting

  Background:
    Given the agent is operating inside this repository
    And the repository root contains AGENTS.md, TASK.md, PROMPT.md, RESEARCH.md

  # anchor: AG.1.1
  Scenario: Agent reads summary before body
    Given a Markdown file exists with a non-empty "summary" frontmatter field
    When the agent needs to understand that file's purpose
    Then the agent MUST read the "summary" field first
    And the agent SHOULD open the file body only if the summary is insufficient

  # anchor: AG.1.2
  Scenario: Agent skips archived files
    Given a Markdown file has frontmatter "status: archived"
    When the agent is scanning the repository for actionable work
    Then the agent MAY skip reading the body of that file
    And the agent MUST NOT modify an archived file without first updating its status

  # anchor: AG.2.1
  Scenario: Agent selects task type before writing
    Given the agent has received a work request
    When the agent determines the request type
    Then if it is coordination work the agent MUST consult TASK.md before creating any file
    And if it is instruction-set authoring the agent MUST consult PROMPT.md before creating any file
    And if it is evidence-gathering the agent MUST consult RESEARCH.md before creating any file

  # anchor: AG.3.1
  Scenario: Agent adds frontmatter to every new operational file
    Given the agent is creating a new file inside /tasks/, /prompts/, or /research/
    When the agent writes the file
    Then the agent MUST include L1 Vault Core frontmatter
    And the agent MUST include the L2 namespace appropriate to the directory
    And the YAML MUST NOT nest deeper than one level
```

---

## Synthesised ADR Constraints

The block below is rewritten by [`tools/adr/cli.py synthesize`](./tools/adr/cli.py) from the [`/decisions/`](./decisions/) corpus. Manual edits inside the markers will be overwritten on the next synthesis run; author or supersede an ADR instead. The bounding markers are byte-exact and required (anchor `ADR.A.3.5`).

<!-- BEGIN AGENCY-ADR SYNTHESIS -->
<!-- AGENT-WRITTEN. DO NOT EDIT BY HAND. Edits will be overwritten by tools/adr/cli.py synthesize. -->
_(empty — `/decisions/` carries no Accepted ADRs yet; run `python3 tools/adr/cli.py synthesize` after the first Accepted ADR lands.)_
<!-- END AGENCY-ADR SYNTHESIS -->

---

## Current State

- Output exists in `research/agent-prompt-specs-3-systems-sdd/output/SPEC.md`
- Needs audit against RISE-DX constraints.

## LOOP_LOG
<!-- Jules appends one record per iteration. Do not edit manually. -->

### Iteration 0 — 2026-05-02
- Status: Loop initialized
- Work artifact: research/agent-prompt-specs-3-systems-sdd/output/SPEC.md
- Verification command: `cat research/agent-prompt-specs-3-systems-sdd/output/SPEC.md | grep -E "(MUST|SHOULD|MAY)"`
- Work artifact: research/obsidian-frontmatter-agentic-spec/output/SPEC.md
- Verification command: python3 test_spec.py
- Max iterations: 5

### Iteration 1 — 2026-05-02
- Dimension targeted: Completeness
- What was wrong: Step S6.a (Schema-Gap Hypothesis) was not properly documented in the Cross-Pollination Log and Contradiction Log.
- What changed: Added explicit Schema-Gap Hypothesis for "Failure Recovery / Error Handling" to both logs.
- Verification: PASS
- Next candidate (if known): Multiple RFC 2119 keywords in single normative statements.

### Iteration 2 — 2026-05-02
- Dimension targeted: Convention
- What was wrong: Did not explicitly verify the "exactly one RFC 2119 keyword per sentence" rule.
- What changed: Ran python script to verify constraint; found 0 violations, proving existing compliance.
- Verification: PASS
- Next candidate (if known): Pre-Commitments not explicitly listed outside of scratchpad logs.

### Iteration 3 — 2026-05-02
- Dimension targeted: Completeness
- What was wrong: Pre-Commitments were not explicitly visible in the final deliverable.
- What changed: Added explicit Pre-Commitments for Spec-A, Spec-B, and Spec-C to the Methodology Note in SPEC.md.
- Verification: PASS
- Next candidate (if known): none identified

### Iteration 4 — 2026-05-02
- Dimension targeted: Correctness
- What was wrong: Literal `\n` characters in AGENTS.md and invalid Gherkin syntax due to floating `Given` statements outside `Scenario`.
- What changed: Replaced literal `\n` with newlines in AGENTS.md and inlined the `Given` steps into the Scenario in `SPEC.md`.
- Verification: PASS
- Next candidate (if known): none identified

### Iteration 5 — 2026-05-02
- Dimension targeted: Completeness
- What was wrong: Did not explicitly output single-source confidence flags everywhere they were needed or missed some.
- What changed: Verified Confidence tags exist properly. Loop complete since all findings from code review were handled.
- Verification: PASS
- Next candidate (if known): LOOP_COMPLETE
- What was wrong: The SPEC.md output contained pseudocode instead of the explicitly requested ASCII diagram for the Expansion-Pattern decision tree.
- What changed: Replaced the pseudocode script logic section with a fully formatted ASCII flowchart.
- Verification: PASS
- Next candidate: Missing "Abstraction Axis" in the Adversarial Query Expansion passes (M13).

### Iteration 2 — 2026-05-02
- Dimension targeted: Completeness
- What was wrong: The M13 Query Expansion passes missed the "Abstraction Axis", meaning only 3 of the 4 explicitly mandated axes were executed.
- What changed: Added the Abstraction Axis query expansion to methodology.md and to the Query Expansion Log in SPEC.md.
- Verification: PASS
- Next candidate: none identified

### Iteration 3 — 2026-05-02
- Dimension targeted: Completeness
- What was wrong: The Python pseudocode block was accidentally removed from SPEC.md when the ASCII diagram was added in Iteration 1.
- What changed: Restored the Python pseudocode block to sit alongside the ASCII diagram in SPEC.md.
- Verification: PASS
- Next candidate: none identified
