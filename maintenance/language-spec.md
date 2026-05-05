---
type: spec
status: active
slug: language-spec
summary: "Canonical, complete definitions of RFC 2119 normative keywords, Gherkin syntax binding, and the Frontmatter Ontology (L0–L3). This is the single source of truth for the spec language used across this repository."
created: 2026-05-04
updated: 2026-05-04
---

# Repository Language Specification

This document is the **single source of truth** for the formal language used in every specification, governance rule, and acceptance-criteria block in this repository. All agents and human contributors MUST conform to the rules here. Summaries in `AGENTS.md` and other files derive from this document; in case of conflict, this document wins.

## 1. Definitions (RFC 2119)

The keywords in §2 are to be interpreted as described in BCP 14 \[RFC 2119\] \[RFC 8174\] **when, and only when, they appear in all capitals** as shown in this document.

---

## 2. RFC 2119 Normative Keyword Reference

### 2.1 Keyword Semantics

| Keyword(s) | Obligation Level | Meaning |
|---|---|---|
| **MUST** / **REQUIRED** / **SHALL** | Absolute requirement | The definition is an absolute requirement. No compliant implementation may deviate. |
| **MUST NOT** / **SHALL NOT** | Absolute prohibition | The definition is an absolute prohibition. |
| **SHOULD** / **RECOMMENDED** | Strong default | There may exist valid reasons to ignore this item in particular circumstances, but full implications must be understood and carefully weighed before choosing a different course. |
| **SHOULD NOT** / **NOT RECOMMENDED** | Strong discouragement | There may exist valid reasons when the particular behavior is acceptable, but full implications must be understood and carefully weighed. |
| **MAY** / **OPTIONAL** | Permissive | The item is truly optional. A vendor may choose to include it if it enhances interoperability; another vendor may omit it. |

### 2.2 Usage Rules

- **U1.** Every normative statement MUST use exactly one RFC 2119 keyword per sentence. Sentences with two or more keywords are normatively ambiguous and MUST be split.
- **U2.** Rationale paragraphs, motivation text, background prose, and explanatory notes MUST NOT contain RFC 2119 keywords in all-caps. Lowercase forms ("should", "may", "must") in prose are permitted and do not carry normative weight.
- **U3.** Each normative statement SHOULD be addressable by a stable identifier of the form `<Spec-Letter>.<Section>.<Index>` (e.g., `A.3.2`, `T.6.1`). This enables audit logs and cross-references to cite exact clauses.
- **U4.** A `[Confidence: low (single-source)]` annotation SHOULD be appended to any normative statement derived from a single, unverified source. This signals to future agents that the clause warrants re-validation.

### 2.3 Mandatory Declaration Boilerplate

Every spec file that contains normative clauses MUST include the following verbatim block before its first normative statement (typically as §1 or §1.1):

```
The key words MUST, MUST NOT, REQUIRED, SHALL, SHALL NOT, SHOULD, SHOULD NOT,
RECOMMENDED, NOT RECOMMENDED, MAY, and OPTIONAL in this document are to be
interpreted as described in BCP 14 [RFC 2119] [RFC 8174] when, and only when,
they appear in all capitals as shown here.
```

---

## 3. Gherkin Syntax Binding

### 3.1 Purpose

Gherkin is the **mandatory notation** for all behavioural examples, agent-interaction scenarios, and hand-off specifications in this repository. Written acceptance criteria MUST use Gherkin; bullet-list assertions are not a compliant substitute.

### 3.2 Keyword Reference

| Keyword | Role | Constraints |
|---|---|---|
| `Feature:` | Names the capability under test. | Every Gherkin block MUST be nested inside a `Feature`. |
| `Background:` | Shared `Given` steps applied to every `Scenario` in the `Feature`. | OPTIONAL; RECOMMENDED when ≥ 3 scenarios share the same setup. |
| `Scenario:` | A single, named behavioural example. | MUST contain ≥ 1 `Given`, ≥ 1 `When`, ≥ 1 `Then`. |
| `Scenario Outline:` | Parametric scenario template. | MUST be paired with an `Examples:` table. RECOMMENDED when the same shape repeats with varying inputs. |
| `Examples:` | Data table for `Scenario Outline`. | MUST follow a `Scenario Outline` block; MUST NOT appear standalone. |
| `Given` | Establishes pre-conditions (world state before the action). | MUST appear at least once per `Scenario`. |
| `When` | Describes the triggering action or event. | MUST appear at least once per `Scenario`. |
| `Then` | States the expected observable outcome or assertion. | MUST appear at least once per `Scenario`. |
| `And` | Continuation of the immediately preceding keyword. | MUST NOT be the first step in a `Scenario` or `Background`. |
| `But` | Negative continuation of the immediately preceding keyword. | MUST NOT be the first step in a `Scenario` or `Background`. |

### 3.3 Validity Rules

- **G1.** Every `Scenario` MUST contain at least one `Given`, at least one `When`, and at least one `Then`, in that relative order.
- **G2.** `And` and `But` MUST NOT open a scenario; they are always continuations.
- **G3.** Every scenario MUST be **self-contained**: it MUST NOT depend on state established in a previous `Scenario` block. Use `Background` for shared setup.
- **G4.** Every scenario MUST be **executable**: a human or agent reading it MUST be able to enact every step without consulting external documents not named in the same spec file.
- **G5.** Each `Scenario` SHOULD carry an anchor comment on the line immediately above its header, in the form: `# anchor: <stable-id>`. Example: `# anchor: B.5.1`.
- **G6.** `Scenario Outline` tables SHOULD use descriptive column headers, not positional ones (e.g., `| input_type | expected_status |` not `| col1 | col2 |`).

### 3.4 Scenario Outline Example

```gherkin
Feature: Frontmatter validation

  Scenario Outline: L1 key presence check
    Given a Markdown file at "<path>"
    When the frontmatter linter runs
    Then the linter MUST report an error if "<required_key>" is absent
    And the linter MUST NOT modify the file

    Examples:
      | path                              | required_key |
      | tasks/001-example/task.md         | slug         |
      | prompts/my-prompt/prompt.md       | type         |
      | research/my-research/readme.md    | summary      |
```

### 3.5 Full-Feature Template

```gherkin
Feature: <capability name>

  Background:
    Given <shared precondition 1>
    And <shared precondition 2>

  # anchor: <Spec>.<Section>.<Index>
  Scenario: <scenario title — action + outcome>
    Given <specific precondition beyond Background>
    When <triggering action>
    Then <primary observable outcome>
    And <secondary outcome>
    But <negative outcome that must not occur>
```

---

## 4. Frontmatter Ontology (Layered Schema with Namespacing)

This section is the **canonical definition** of the YAML frontmatter schema for all Markdown files in this repository. The design follows the "Layered Schema with Namespacing" model derived from `research/obsidian-frontmatter-agentic-spec/output/SPEC.md`. `TASK.md §3` reproduces the operational subset for convenience; this file is the source of record.

### 4.1 Design Principles

- **Flat YAML only:** YAML MUST NOT nest deeper than one level. This prevents LLM YAML-parsing hallucinations documented in the Obsidian frontmatter research.
- **Prefix-based namespacing:** Domain-specific keys use `<domain>_<key>` to simulate layers without nesting.
- **Agent token budget:** The `summary` field exists specifically so agents can route decisions from frontmatter alone, skipping the file body when the summary is sufficient.
- **Human readability preserved:** L0 and L1 fields are human-meaningful. L3 machine metadata is externalised to sidecar files.

### 4.2 L0 — Obsidian Reserved

These keys are owned by Obsidian. Agents MUST preserve them if present; agents MAY omit them if Obsidian is not in use.

| Key | Type | Obsidian Behaviour |
|---|---|---|
| `tags` | list of strings | Native Obsidian graph-view and search integration. |
| `aliases` | list of strings | Alternate wikilink targets for this note. |
| `cssclasses` | list of strings | Modifies the Obsidian UI rendering for this note. |

### 4.3 L1 — Vault Core (Mandatory for Operational Files)

Every file inside `/tasks/`, `/prompts/`, `/research/` MUST carry all six L1 keys. Files at the repository root SHOULD carry them.

| Key | Type | Allowed Values | Agent Guidance |
|---|---|---|---|
| `type` | string | `task`, `prompt`, `research`, `spec`, `readme`, `note`, `index` | Primary routing key. Read this before the body. |
| `status` | string | `draft`, `active`, `blocked`, `completed`, `archived` | `archived` files MAY be skipped to save tokens. |
| `slug` | string | kebab-case, max 5 tokens | MUST match the enclosing folder name where applicable. Stable across renaming. |
| `summary` | string | free-form, concise | Token-cheap tl;dr. The agent SHOULD prefer reading this before opening the body. Keep ≤ 40 words. |
| `created` | date | ISO-8601 `YYYY-MM-DD` | Set once at creation. Never update. |
| `updated` | date | ISO-8601 `YYYY-MM-DD` | MUST be updated on every substantive write. |

### 4.4 L2 — Domain Namespaces (Mandatory Inside Their Directory)

Convention: `<domain>_<key>`. Keys MUST be flat. Lists MUST contain scalars or short strings.

#### Task Namespace (`/tasks/<NNN>-<slug>/task.md`)

| Key | Type | Allowed Values |
|---|---|---|
| `task_id` | string | Zero-padded sequence: `"001"`, `"017"`. |
| `task_status` | string | `open`, `in_progress`, `blocked`, `done`, `abandoned` |
| `task_owner` | string | Agent name or human identifier. |
| `task_priority` | string | `P0`, `P1`, `P2`, `P3` |
| `task_uses_prompts` | list | Slugs of prompts this Task executes. MAY be empty. |
| `task_spawns_research` | list | Slugs of research workspaces produced. MAY be empty. |
| `task_spawns_prompts` | list | Slugs of follow-up prompts generated by this Task. MAY be empty. |
| `task_affects_paths` | list | Relative paths the Task is allowed to modify. |

#### Prompt Namespace (`/prompts/<slug>/prompt.md`)

| Key | Type | Allowed Values |
|---|---|---|
| `prompt_kind` | string | `research-proposal`, `follow-up`, `tool-instruction`, `task-spec`, `general` |
| `prompt_framework` | string | `RISEN`, `RISE-DX`, `ReAct`, `RISEN+ReAct`, `CoT` |
| `prompt_target_agent` | string | e.g. `Claude Code`, `Gemini`, `any` |
| `prompt_relates_to_task` | string | Task slug, or empty string if standalone. |
| `prompt_spawned_from_research` | string | Research slug that motivated this prompt, or empty string. |

#### Research Namespace (`/research/<slug>/output/SPEC.md` and `readme.md`)

| Key | Type | Allowed Values |
|---|---|---|
| `research_phase` | string | `kickoff`, `synthesis`, `reflection`, `complete` |
| `research_executes_prompt` | string | Slug of the prompt that triggered this run. MUST resolve to `/prompts/<slug>/`. |
| `research_friction_level` | string | `FL0`, `FL1`, `FL2`, `FL3` |

### 4.5 L3 — Agent-Only (Sidecar, Not in Markdown)

L3 fields (vector embeddings, graph scores, token matrices, dependency scores) MUST NOT appear in YAML frontmatter. They MUST live in a sidecar file: `/.agent_cache/<filename>.meta.json`. Placing L3 data inline would break Obsidian's Properties UI and exceed token limits during bulk parsing.

Suggested L3 sidecar keys (informative only — not normative):

```json
{
  "agent_token_estimate": 1200,
  "agent_depends_on": ["tasks/001-refactor-governance-from-specs/task.md"],
  "agent_embedding_vector": "...",
  "agent_graph_score": 0.87
}
```

### 4.6 Worked Examples

#### Minimal L1-only file (e.g., a readme.md)

```yaml
---
type: index
status: active
slug: research-obsidian-frontmatter
summary: "Directory index for the obsidian-frontmatter-agentic-spec research workspace."
created: 2026-05-02
updated: 2026-05-04
---
```

#### Full Task file

```yaml
---
type: task
status: active
slug: refactor-governance-from-specs
summary: "Encode rules from Spec A/B/C, G/H/I, J/K/L into linters, hooks, and templates."
created: 2026-05-04
updated: 2026-05-04
task_id: "001"
task_status: open
task_owner: "claude-code"
task_priority: P1
task_uses_prompts:
  - refactor-governance-from-specs
task_spawns_research: []
task_affects_paths:
  - PRE_COMMIT.md
  - .githooks/
  - tools/
---
```

#### Full Prompt file

```yaml
---
type: prompt
status: active
slug: token-efficiency-tool-suite
summary: "Research prompt: survey public GitHub repos tackling token efficiency via mandatory tool calling; produce a tool-suite spec for this repo."
created: 2026-05-04
updated: 2026-05-04
prompt_kind: research-proposal
prompt_framework: RISEN+ReAct
prompt_target_agent: "Claude Code"
prompt_relates_to_task: "token-efficiency-tool-suite"
prompt_spawned_from_research: ""
---
```

#### Full Research readme

```yaml
---
type: research
status: active
slug: token-efficiency-tool-suite
summary: "Execution workspace for the token-efficiency-tool-suite research proposal."
created: 2026-05-04
updated: 2026-05-04
research_phase: kickoff
research_executes_prompt: token-efficiency-tool-suite
research_friction_level: FL0
---
```

---

## 5. Navigation Decision Tree (ASCII)

How an agent navigates a repository file using frontmatter alone:

```text
               [Open file frontmatter]
                        |
          +-------------+-------------+
          |                           |
  [status == 'archived'?]    [type == 'index'?]
       /       \                  /      \
    [Yes]     [No]             [Yes]    [No]
      |          |               |        |
  [SKIP body]   |      [Read folder      |
                |       children]        |
                |                        |
                +------------------------+
                            |
                  [Read 'summary' field]
                            |
                   [Summary sufficient?]
                      /         \
                  [Yes]         [No]
                    |             |
              [Act on        [Open body
               summary]       for detail]
```

---

## 6. Anti-Patterns

- **MUST NOT** use two RFC 2119 keywords in a single normative sentence.
- **MUST NOT** use all-caps keywords (`MUST`, `SHOULD`, `MAY`) in prose rationale sections.
- **MUST NOT** nest YAML beyond one level in any frontmatter block.
- **MUST NOT** omit the `summary` field from operational files; agents depend on it for token-efficient navigation.
- **MUST NOT** write acceptance criteria as bullet-list assertions instead of Gherkin scenarios.
- **MUST NOT** place L3 agent metadata (embeddings, vectors, scores) inside YAML frontmatter.
- **SHOULD NOT** write `Scenario` blocks without `# anchor:` comments in normative spec files; anchors enable stable cross-references.
