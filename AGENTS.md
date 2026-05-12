---
type: spec
status: active
slug: agents-spec
summary: "Entry-point governance spec for all agents operating in this repository. Defines task routing, folder rules, spec language (RFC 2119 + Gherkin), and the Frontmatter Ontology every agent must apply."
created: 2026-05-02
updated: 2026-05-12
---

# Agent Instructions

Welcome, agent. This repository manages development and deep research tasks.

**First action of every session:** Run `./install.sh` from the repo root *before* reading, editing, or validating any file. This installs the Python tooling (`PyYAML`, `jsonschema`, `pytest`) the rest of this spec assumes is present. See [§ Session Setup](#session-setup) below — rules **SS.1–SS.3** are binding.

**Before committing any work:** You MUST review and abide by the checks defined in [PRE_COMMIT.md](./PRE_COMMIT.md).

**Last step of every session (all agents):** After your final commit and push succeed, you MUST satisfy the platform-agnostic closing checklist defined in [§ Closing Run Procedure](#closing-run-procedure) below. Claude Code implements step 4 via `/sc:createPR`; Jules and Gemini implement it via their platform-native PR primitives — the checklist is the binding contract, not any single implementation.

## Theoretical Foundations

The MDL-compression / supersession-DAG paradigm encoded in this repository's ADR governance pipeline (`tools/adr/{compress,graph,synthesize}.py`, the `<!-- BEGIN/END AGENCY-ADR SYNTHESIS -->` guarded section below) traces to the external Gemini research run at [`research/gemini/agency-adr-governance-spec/`](./research/gemini/agency-adr-governance-spec/). That artefact is the theoretical anchor for the §0–§9 ADR governance contract synthesised in [`research/adr-spec-research-synthesis/output/SPEC.md`](./research/adr-spec-research-synthesis/output/SPEC.md) and implemented by Task 028/031. Citing it here closes the provenance gap between the deployed pipeline and its theoretical premise per Task 032 ST-5 acceptance criterion (a). Subsequent re-derivations of this paradigm MUST go through the supersession DAG defined in the ADR SPEC §6, not informal amendment.

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

## Closing Run Procedure

This section binds the *final* step of every session, regardless of platform. The four-step checklist below is the contract; each agent platform satisfies it through whichever primitive is native to its runtime. Claude Code MUST satisfy step 4 via `/sc:createPR`; Jules and Gemini MUST satisfy it via their respective platform-native PR mechanisms. **No platform may skip any step.**

### Platform-Agnostic Checklist

Every agent session MUST satisfy these four steps, in order, before declaring the session complete:

1. **Friction log written and committed.** The session's `friction-log.md` MUST exist with a parseable `Highest Frustration Level: FL[0-3]` declaration in the body (per [FRUSTRATED.md §FL.Log](./FRUSTRATED.md)). Standard sessions MAY substitute a `## Frustration Log` section in the PR body or commit message; research runs MUST write `/research/<slug>/reflection/friction-log.md`. **FL0 is mandatory even on perfect runs — absence of a log is itself a defect.**
2. **`tasks/readme.md` index synced.** If any Task changed status (`open` → `done`, `done` → `updated`, …) in this session, the corresponding bullet under [`/tasks/readme.md`](./tasks/readme.md) MUST be updated in the same commit set. The `tools/fm/index_diff.py` gate (PRE_COMMIT.md §7.11) blocks drift mechanically.
3. **Pre-commit gate green.** [`tools/check-governance.sh`](./tools/check-governance.sh) MUST exit 0 on the final commit. A failing or unverified working tree MUST NOT be promoted to a pull request. Agents MUST NOT bypass with `--no-verify`, `--no-gpg-sign`, or equivalent.
4. **Pull request opened (or confirmed as already covering the pushed commits).** The agent MUST open a draft pull request via the platform's PR-creation primitive against the configured upstream branch, or confirm an existing PR already covers the pushed commits. The PR body MUST cite (a) the closed Task slug(s) under `/tasks/` if any, and (b) the FL declaration from the friction log.

Step 4 MUST be idempotent: re-invocation on a branch that already has an open pull request MUST be a no-op. Agents MUST NOT create duplicate PRs to "force-update" an existing one — pushing additional commits to the same branch updates the open PR automatically.

### Normative Rules

- **CR.1** Every agent (any platform) MUST satisfy the four-step checklist before declaring a session complete; the steps MUST be performed in order.
- **CR.2** An agent MUST NOT consider a session complete until step 4 has either (a) opened a new pull request, or (b) confirmed an existing PR already covers the pushed commits.
- **CR.3** An agent MUST NOT advance past step 3 if pre-commit checks (per [PRE_COMMIT.md](./PRE_COMMIT.md)) failed or were skipped. A failing working tree MUST NOT be promoted to a PR.
- **CR.4** If the platform's PR-creation primitive errors out, the agent MUST NOT silently exit — the error MUST be reported to the user with the exact command output, and the session MUST remain in `in_progress` for the operator to triage.
- **CR.5** The PR body opened in step 4 MUST reference (a) the closed Task slug(s) under `/tasks/` if any, and (b) the FL declaration from the friction log per [FRUSTRATED.md](./FRUSTRATED.md).
- **CR.6** Step 4 invocations on a branch with an open pull request MUST be a no-op. Agents MUST NOT create duplicate PRs.
- **CR.7** Each platform implementation note below specifies how step 4 is satisfied on that platform. Adding a new platform to this repo MUST be accompanied by a new implementation note in this section, not by a new normative rule.

### Platform Implementation Notes

#### Claude Code

Step 4 is satisfied by invoking the `/sc:createPR` slash-command immediately after a successful `git push`. The command is provided by the **SuperClaude Framework** at [`src/superclaude/commands/createPR.md`](https://github.com/netzkontrast/SuperClaude_Framework/blob/main/src/superclaude/commands/createPR.md); it is installed automatically alongside the rest of the `/sc:*` command set. The skill re-runs `tools/check-governance.sh` before opening the PR (defence-in-depth on CR.3) and assembles the citation block CR.5 requires.

If the cloud-hosted GitHub MCP integration is the agent's only path to GitHub (no local `gh` CLI), the agent MUST use the `mcp__github__create_pull_request` tool with the same body conventions; the four-step checklist applies unchanged.

#### Jules

Jules sessions satisfy step 4 by opening a draft pull request through the Jules-native PR primitive (Jules ships GitHub integration; the agent calls into it as part of the session-close routine). The PR body MUST carry the same Task-slug + FL citations CR.5 requires. There is no `/sc:createPR` equivalent on Jules; the implementation note for Jules is "use the platform's GitHub primitive directly, with the body shape this section mandates."

#### Gemini

Gemini Deep Research sessions execute against an external research surface, not a Git working tree; step 4 on Gemini is satisfied by writing the research output back into this repo via a follow-on integration Task (RESEARCH.md §6.5) that then opens its own PR per the Claude Code / Jules path. **Gemini sessions therefore satisfy steps 1–3 in the source environment, and step 4 is satisfied by the integration Task's agent (Claude or Jules) once the artefacts land in this repo.** The integration Task MUST cite the originating Gemini research slug in its PR body.

#### Adding a new platform

A new agent platform (e.g., Devin, Codex, future SDK harness) MAY be added to this section. The PR introducing it MUST add a new "Platform Implementation Notes" subsection that names the platform's PR primitive and confirms steps 1–3 are achievable in the platform's runtime. If any step is not achievable, the PR MUST also propose either a delegation pattern (like Gemini's above) or an amendment to the checklist itself.

### Gherkin Scenarios

```gherkin
Feature: Every agent closes every run with the four-step checklist

  # anchor: CR.1.1
  Scenario: Claude Code session closes with /sc:createPR
    Given a Claude Code session has finished its work
    And the agent has committed and pushed all changes
    And tools/check-governance.sh exited 0 on the final commit
    And the friction-log.md carries a "Highest Frustration Level: FL[0-3]" line
    And tasks/readme.md reflects the new task_status frontmatter
    When the agent reaches the end of the session
    Then the agent MUST invoke /sc:createPR before declaring the session complete
    And the resulting pull request body MUST cite the closed Task slug(s) and the FL declaration

  # anchor: CR.1.2
  Scenario: Pre-commit failure blocks step 4 on any platform
    Given any agent (Claude / Jules / future) is finishing a session
    And tools/check-governance.sh exited non-zero on the most recent commit attempt
    When the agent considers advancing to step 4
    Then the agent MUST NOT open a pull request
    And the agent MUST report the linter diagnostics to the user
    And the session MUST remain open for triage

  # anchor: CR.1.3
  Scenario: Jules session closes via platform-native PR primitive
    Given a Jules session has finished its work
    And the agent has committed and pushed all changes
    And tools/check-governance.sh exited 0 on the final commit
    When the agent reaches step 4
    Then the agent MUST open a draft pull request via the Jules-native GitHub primitive
    And the PR body MUST cite the closed Task slug(s) and the FL declaration

  # anchor: CR.1.4
  Scenario: Gemini session delegates step 4 to an integration Task
    Given a Gemini Deep Research session has produced an output artefact
    And the artefact is destined for this repo
    When the Gemini session ends
    Then steps 1-3 MUST have been satisfied in Gemini's source environment
    And step 4 MUST be deferred to a follow-on integration Task agent
    And the integration Task's PR body MUST cite the originating Gemini research slug

  # anchor: CR.1.5
  Scenario: Re-invocation on an open PR is a no-op
    Given any agent has already opened a pull request for the current branch
    When the agent re-invokes step 4 (for any reason)
    Then the primitive MUST detect the existing PR
    And the primitive MUST NOT create a duplicate PR
    And subsequent commits pushed to the same branch MUST update the existing PR automatically
```

## Task Type Routing

Three top-level governance specs partition the work this repository performs. Pick the one that matches your request *before* writing any file:

| If the request is… | Consult | Operational directory |
|---|---|---|
| Coordination/orchestration with a goal, plan, and todo | [TASK.md](./TASK.md) | [/tasks/](./tasks/) |
| Authoring an executable instruction set (research proposal, follow-up, tool instruction, task-spec) | [PROMPT.md](./PROMPT.md) | [/prompts/](./prompts/) |
| Executing a prompt to produce evidence, synthesis, reflection, output | [RESEARCH.md](./RESEARCH.md) | [/research/](./research/) |
| Authoring or modifying a skill | [SKILLS.md](./SKILLS.md) | [/skills/](./skills/) |
| Archivierung/Stilllegung von Artefakten inkl. Trigger und Ablauf | [ARCHIVE.md](./ARCHIVE.md) | [/tasks/](./tasks/), [/prompts/](./prompts/), [/research/](./research/) |

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

> **Polarity-inversion advisory (Task 032 ST-3).** Polarity inversion — silently stripping a `MUST NOT` qualifier so a clause inverts to a permissive `MUST` — is undetectable by deterministic compression-fidelity checks alone. See [`research/adr-assumption-audit/output/REPORT.md`](./research/adr-assumption-audit/output/REPORT.md) §1 ASM-001 for the worked example. With Task 031's ADR synthesis pipeline live, an ASM-001 inversion in any `decisions/<NNNN>-<slug>.md` would silently invert governance language inside the [`Synthesised ADR Constraints`](#synthesised-adr-constraints) guarded section on the next `tools/adr/cli.py synthesize` run. The advisory linter [`tools/check-rfc2119-polarity.py`](./tools/check-rfc2119-polarity.py) is the missing guard rail; it runs WARN-tier in [`tools/check-governance.sh`](./tools/check-governance.sh) over all 8 root specs, every `research/<slug>/output/SPEC.md`, and every `decisions/<NNNN>-<slug>.md`. Reviewers MUST treat any `WARN:RFC2119.POLARITY` diagnostic as a manual-review candidate before merging.

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
| **L2** — Domain Namespace | `task_*`, `prompt_*`, `research_*`, `skill_*` keys | MUST be present inside the directory that owns the namespace. |
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
- **NO.5.** An agent doing **non-narrative work** (governance refactors, frontmatter linters, build tooling, anything not under the four narrative skills) MUST NOT load the Narrative Ontology files. Loading wastes tokens on data the work does not need. The Frontmatter Ontology governs that work; this ontology does not. NO.5 is mechanically enforced by [`tools/check-narrative-ontology-load.py`](./tools/check-narrative-ontology-load.py) (Task 032 ST-2), which runs WARN-tier inside [`tools/check-governance.sh`](./tools/check-governance.sh) and emits `WARN:NO.5:<msg>` against any task whose `task_affects_paths` does NOT include `skills/dramatica-*` / `skills/ncp-*` / `skills/novel-*` yet references `maintenance/schemas/narrative-ontology/`.
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

## Skills Architecture — Container Capabilities and Citation Protocol

The skills loader and any skill that fetches its own dependencies MUST honour the operational constraints resolved by [`research/skills-skill-container-capabilities/output/SPEC.md`](./research/skills-skill-container-capabilities/output/SPEC.md). Two previously-`UNCERTAIN` markers (U1, U2) are now `RESOLVED`:

- **U1 — `git` is NOT a pre-installed binary on the claude.ai code-execution container.** The official utility list (`unzip`, `unrar`, `7zip`, `bc`, `rg`, `fd`, `sqlite`) excludes git. Skills targeting claude.ai (Free/Pro/Max) MUST NOT assume `git clone` is available; they MUST use the GitHub REST API as the primary fetch mechanism (`requests` over `https://api.github.com/repos/<owner>/<repo>/contents/<path>`). Skills MAY attempt `git` first with graceful REST-API fallback. Claude API code-execution has no network access; git clone MUST NOT be used there. Claude Code on a host system has full git access. See SPEC §2.4.
- **U2 — Container filesystem persistence between independent web conversations is NOT guaranteed.** The web UI exposes no container-ID reuse mechanism; each new claude.ai conversation MUST be treated as starting with a fresh container. The "pull-if-exists" optimisation MUST NOT be relied upon in the claude.ai web surface. All bootstrap sequences MUST re-fetch required files on each invocation. Workspace storage is 5 GiB; RAM 5 GiB. See SPEC §3.4.

The skills-skill stub itself (the bootstrap layer that routes requests to skill bodies on `origin/main`) is governed by a separate spec, [`research/skills-skill-architecture/output/SPEC.md`](./research/skills-skill-architecture/output/SPEC.md). The four operational invariants ratified from that spec — **B.6 repository lock, B.7 version-reference declaration, B.8 error surfacing, B.9 scope containment** (trust boundary R5) — plus the **three-tier T1/T2/T3 content ladder** (R4) and the **`SKILLS_SKILL_PIN` / `SKILLS_SKILL_OFFLINE`** version-pinning vocabulary (R7) live in [`SKILLS.md §7.2 / §7.3 / §7.4`](./SKILLS.md#72-trust-boundary-invariants-r5). The remaining `UNCERTAIN` markers (`U3` host activation mechanism, `U4` Jules portability, `U5` raw-message availability, `U6` git signing) remain deferred to Gemini Deep Research per the `skills-skill-architecture` workspace's §9 open-questions table.

### Citation Reproducibility Protocol

When a skill (or any agent producing audit-traceable output) cites a file region, the citation MUST use the form `path/to/file.ext:Lstart-Lend@<sha>` per [`research/ncp-novel-co-authoring-spec/output/SPEC.md`](./research/ncp-novel-co-authoring-spec/output/SPEC.md) §"Inline citations". The `@<sha>` suffix pins the citation to a commit so subsequent re-derivations remain reproducible. Skills SHOULD prefer this form over bare `path:Lstart-Lend` references in narrative-ontology and novel-co-authoring contexts. Non-narrative agents MAY use bare `path:Lstart-Lend` when commit-pinning is not material to audit recovery.

### Acceptance Scenarios (Normative)

```gherkin
Feature: Skills honour container capability constraints and the citation protocol

  # anchor: AG.SK.1
  Scenario: Skill targeting claude.ai web surface MUST NOT assume git
    Given a Skill bootstrap sequence runs inside the claude.ai code-execution container
    When the Skill needs to fetch a file from a public GitHub repository
    Then the Skill MUST NOT execute `git clone` as the primary mechanism
    And the Skill MUST use the GitHub REST API (or HTTP archive download) instead
    And the Skill MAY attempt `git` first only if it gracefully falls back to the REST API on `command not found`

  # anchor: AG.SK.2
  Scenario: Each claude.ai conversation starts with a fresh container
    Given an agent begins a new claude.ai web conversation
    When the agent runs a skill that previously cached files in `/workspace`
    Then the agent MUST re-fetch every required file
    And the agent MUST NOT branch on the presence of a prior local clone

  # anchor: AG.SK.3
  Scenario: Narrative-ontology citation pins to a commit sha
    Given an agent produces an audit citation referencing a narrative-ontology entry
    When the citation appears inside an NCP, novel-architect, or dramatica artefact
    Then the citation MUST take the form `path/to/file.ext:Lstart-Lend@<sha>`
    And the agent MUST resolve `<sha>` to the commit that owns the cited line range

  # anchor: AG.NO5.1
  Scenario: Non-narrative agent loads narrative ontology — WARN
    Given an agent runs a Task whose `task_affects_paths` does NOT include any of `skills/dramatica-*`, `skills/ncp-*`, `skills/novel-*`
    And the staged frontmatter or diff shows a read against `maintenance/schemas/narrative-ontology/ontology.json`
    When `tools/check-narrative-ontology-load.py` runs at pre-commit
    Then the linter MUST emit a WARN (exit 2) citing the offending path
    And `tools/check-governance.sh` MUST NOT block the commit (advisory only)
```

---

## Assumption-Log Substance — Mechanical Validation

AGENTS.md §"Folder Management & Workflow Drift" requires every operational folder's `readme.md` to log its assumptions; FOLDERS.md F.3 binds the section heading. Both rules are now mechanically enforced by [`tools/check-assumption-log.py`](./tools/check-assumption-log.py) (Task 032 ST-4), which runs WARN-tier in `tools/check-governance.sh` over `tasks/<NNN>-<slug>/readme.md` and `research/<slug>/readme.md`.

The linter emits three diagnostic codes:

- `ASSUMPTION.LOG.MISSING` — required `## Assumptions Log` section absent.
- `ASSUMPTION.LOG.EMPTY` — section present but body has no substance and no explicit `(none)` declaration.
- `ASSUMPTION.LOG.STALE` — readme `updated:` predates sibling `task.md` `updated:`; assumptions MUST be reconfirmed or refreshed.

An empty section with the literal line `(none)` (case-insensitive) is permitted as an explicit declaration of no assumptions; the linter does NOT flag it. New operational folders SHOULD include the section at creation time so the WARN tier stays clean.

```gherkin
Feature: Operational folder readme carries an Assumptions Log

  # anchor: AG.AL.1
  Scenario: New operational folder ships with an Assumptions Log
    Given an agent creates `tasks/<NNN>-<slug>/readme.md`
    When the agent writes the file
    Then the file MUST contain a level-2 heading `## Assumptions Log`
    And the section MUST contain at least one substantive entry OR the literal line `(none)`

  # anchor: AG.AL.2
  Scenario: Stale readme triggers refresh advisory
    Given a `tasks/<NNN>-<slug>/readme.md` carries an `## Assumptions Log` section
    And the sibling `task.md` `updated:` is more recent than the readme `updated:`
    When `tools/check-assumption-log.py` runs at pre-commit
    Then the linter MUST emit `WARN:ASSUMPTION.LOG.STALE`
    And the agent SHOULD reconfirm the assumptions and bump the readme `updated:` field
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
### MUST
- The folder MUST carry a `readme. [ADR-0006]
- Inbound references from `skills/the-agency-system-architect/` MUST travel as plain Markdown links inside `SKILL. [ADR-0006]

### SHOULD
- md §8 SHOULD drop the "authoring ADR pending" parenthetical via a follow-up T1 / T2 edit. [ADR-0006]

### MUST NOT
- ** The narrative skills (`skills/novel-architect/`, `skills/suno-lyric-writer/`) follow a parallel pattern — they ship large reference corpora that consumers MUST NOT autoload (NO. [ADR-0006]

**Contributing ADRs:** ADR-0006.
<!-- END AGENCY-ADR SYNTHESIS -->

---

## Current State

- Output exists in `research/agent-prompt-specs-3-systems-sdd/output/SPEC.md`
- Needs audit against RISE-DX constraints.

## Session Logs

Jules per-iteration runtime state lives in
[`maintenance/session-logs/jules-loop-log.md`](./maintenance/session-logs/jules-loop-log.md).
Append new iteration records there, never here — `R.19` forbids
runtime-state sections in root governance specs, and
`tools/check-spec-runtime-state.py` (Task 055) flags them at
pre-commit.
