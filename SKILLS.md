---
type: spec
status: active
slug: skills-spec
summary: "Root specification governing the /skills/ capability directory, the skill-bootstrap protocol, and the cross-agent portability contract."
created: 2026-05-05
updated: 2026-05-11
---

# Skill Architecture Specification

> **Mechanical Enforcement Notice:** This spec is mechanically enforced by `tools/check-governance.sh`. Before editing any file under `/skills/`, install the pre-commit hook once with `tools/install-hooks.sh`. See [§9 Mandatory Pre-Commit Checks](#9-mandatory-pre-commit-checks) for the per-clause linter mapping.

When the agent is asked to author or modify a capability, the agent MUST treat it as a **Skill** and apply the rules in this document. A Skill represents *what the agent knows how to do*.

## 1. Definitions (RFC 2119)

The keywords MUST, MUST NOT, REQUIRED, SHALL, SHALL NOT, SHOULD, SHOULD NOT, RECOMMENDED, NOT RECOMMENDED, MAY, and OPTIONAL in this document are to be interpreted as described in BCP 14 [RFC 2119] [RFC 8174] when, and only when, they appear in all capitals as shown here.

- **Skill** — A version-controlled capability stored in `/skills/<slug>/SKILL.md`. It provides actionable instructions, tools, or domain knowledge that agents can load into their context to solve tasks.
- **Bootstrap Protocol** — The mandatory process of cloning `origin/main` skills into the local agent's context path.

## 2. Directory Structure

Every Skill MUST live in a dedicated subfolder under `/skills/`. The folder name MUST be `<slug>` in kebab-case.

```text
/skills
└── /<slug>
    ├── readme.md        # Directory index.
    ├── SKILL.md         # The main capability body. MUST exist.
    ├── adapters/        # OPTIONAL agent-specific overrides.
    └── references/      # OPTIONAL local context files the skill requires.
```

## 3. Frontmatter Ontology (skill_* namespace)

`SKILL.md` files MUST carry the L1 Vault Core keys plus the L2 `skill_*` namespace defined here. YAML MUST NOT nest deeper than one level.

### 3.1 Layer Overview

| Layer | Scope | Mandate |
|---|---|---|
| **L0** — Obsidian Reserved | `tags`, `aliases`, `cssclasses` | Optional; preserved if present. |
| **L1** — Vault Core | `type`, `status`, `slug`, `summary`, `created`, `updated` | MUST be present on all operational files. |
| **L2** — Domain Namespace | `skill_*` keys | MUST be present inside `/skills/`. |
| **L3** — Agent-Only | Vector embeddings, graph scores, token matrices | MUST NOT appear in YAML. Lives in `/.agent_cache/<file>.meta.json`. |

Full semantics: [TASK.md §3](./TASK.md).

### 3.2 L1 — Vault Core

Every `SKILL.md` MUST carry these six L1 keys (full semantics in [TASK.md §3.2](./TASK.md)):

| Key | Type | Constraint for SKILL.md |
|---|---|---|
| `type` | string | MUST be `spec`. (`skill` is not a valid L1 type value; valid values: `task \| prompt \| research \| spec \| readme \| note \| index`.) |
| `status` | string | One of: `active`, `draft`, `deprecated`, `archived`. |
| `slug` | string | Kebab-case; MUST match the parent folder name. |
| `summary` | string | One-line description; MUST be ≤ 120 characters. |
| `created` | date | ISO 8601 (`YYYY-MM-DD`). Set at creation; never changed. |
| `updated` | date | ISO 8601 (`YYYY-MM-DD`). MUST be updated on every normative change. |

### 3.3 L2 — `skill_*` Namespace

| Key | Type | Purpose |
|---|---|---|
| `skill_kind` | string | One of: `domain` (e.g. dramatica-theory), `tool` (e.g. pdf-to-markdown), `orchestrator` (e.g. the-agency-system-architect), `meta` (e.g. skills-skill-bootstrap). Drives index routing. |
| `skill_target_agents` | list | Agents the skill is verified-portable to. Members from: `claude-ai`, `claude-code`, `jules`, `gemini-cli`. |
| `skill_references_skills` | list | Slugs of other skills this skill invokes or composes. Reciprocity is computed by the linter. |
| `skill_references_research` | list | Slugs of `/research/<slug>/` workspaces grounding the skill's claims. |
| `skill_references_prompts` | list | Slugs of `/prompts/<slug>/` instruction sets the skill embeds or extends. |
| `skill_bootstrap_required` | boolean | True if the skill cannot run without the bootstrap clone in the active workspace. |
| `skill_bundles_tools` | list[str] | OPTIONAL. Repo-relative `tools/<slug>` paths that `skills/skills-skill-bootstrap/sync.sh` materialises into `<synced-skill>/scripts/_bundled/<basename>/` at sync time. Each entry MUST start with `tools/`, MUST resolve to an existing directory, and MUST contain no `..` segments. Introduced by [ADR-0007](./decisions/0007-skill-bundles-tools-frontmatter.md). |

## 4. Workflow (Skill Lifecycle)

The lifecycle states are: `draft` → `active` → `deprecated` → `archived`.

- A skill MAY be created directly as `active` if it is immediately ready for use; `draft` is OPTIONAL for specs still under review.
- `active` means: in force; agents MAY invoke the skill freely.
- `deprecated` means: agents MUST NOT invoke the skill for new work; the skill is preserved for historical reference and read-only consumption.
- `archived` means: historical record only; agents SHOULD NOT open the body without an explicit reason. `archived` is a terminal state.
- Valid transitions: `draft → active`, `active → deprecated`, `deprecated → archived`. Direct `active → archived` is permitted only when the skill was never invoked in production.

The normative authoring flow is:

1. A task determines that a new capability is needed.
2. The agent executes research or writes a prompt to design the capability.
3. The agent implements the `SKILL.md` following the template.
4. The agent commits and pushes the new skill.
5. Other agents pull the new skill using the bootstrap protocol.

### 4.1 Gherkin Scenarios

```gherkin
Feature: Skill Lifecycle

  # anchor: LC.1.1
  Scenario: Author creates a new skill
    Given an agent identifies a reusable capability that requires version control
    When the agent follows the bootstrap protocol and implements SKILL.md using `templates/skill.md`
    Then the skill MUST be committed to `/skills/<slug>/SKILL.md` with `status: active`
    And the skills manifest MUST be regenerated before the commit is finalised

  # anchor: LC.2.1
  Scenario: Maintainer deprecates an existing skill
    Given a skill is superseded or no longer safe to use
    When the maintainer sets `status: deprecated` in the skill's SKILL.md frontmatter
    Then agents MUST NOT invoke that skill for new work
    And the `updated` date MUST be set to the date of the deprecation commit
```

## 5. SKILL.md Required Sections

Every `SKILL.md` MUST include the following H2 (`##`) sections, as defined in `templates/skill.md`:

- `## What` — The purpose and scope of the skill.
- `## When to use` — The triggers and conditions for activation.
- `## How to use` — Actionable instructions, steps, or code.
- `## References` — Links to research, prompts, or domain context.
- `## Compatibility` — Agent portability and known limitations.

## 6. Skill-to-Skill Cross-References

- **X.1** A skill MAY reference other skills *only* through the `skill_references_skills` frontmatter list. Inline mentions in prose are non-normative and MUST NOT be relied on by consumers.
- **X.2** Every reference MUST resolve at lint time. A broken reference is a pre-commit failure.
- **X.3** Reciprocity is computed by the linter, not authored. Authors do not write `skill_referenced_by`; the index tool generates it.
- **X.4** Composition vs. invocation is signalled by reference shape: a list element of bare `<slug>` is *invocation* (skill A calls skill B as a tool); a list element of the form `<slug>:embed` is *composition* (skill A inlines skill B's body — RECOMMENDED only between skills with the same `skill_kind`).
- **X.5** `skill_bundles_tools` entries are not skill-to-skill references; they declare repo-relative `tools/<slug>` paths that `sync.sh` materialises at sync time. Adding or removing an entry is a **T2 additive repair** via `tools/fm/edit.py --append-list skill_bundles_tools tools/<slug>`. Validation lives in `tools/fm/validate.py` (diagnostics `F.B.5`, `F.B.6`); governance authority is [ADR-0007](./decisions/0007-skill-bundles-tools-frontmatter.md).

### 6.1 Gherkin Scenarios

```gherkin
Feature: Skill-to-Skill Linkage

  # anchor: X.1.1
  Scenario: Skill invocation
    Given a skill "the-agency-system-architect" needs to invoke "suno-lyric-writer"
    When the author defines the linkage
    Then "the-agency-system-architect/SKILL.md" MUST contain "suno-lyric-writer" in its "skill_references_skills" list

  # anchor: X.2.1
  Scenario: Broken skill reference fails pre-commit
    Given a skill "the-agency-system-architect/SKILL.md" lists "nonexistent-skill" in "skill_references_skills"
    When the agent runs tools/lint-linkage.py
    Then the linter MUST exit with a non-zero code
    And the agent MUST NOT commit until the broken reference is removed or the referenced skill exists

  # anchor: X.3.1
  Scenario: Linter computes reciprocity without author involvement
    Given skill A lists skill B in "skill_references_skills"
    When the linter generates the skills manifest
    Then the manifest MUST include B's reverse-reference to A under a computed "skill_referenced_by" field
    And the author of skill A MUST NOT manually write "skill_referenced_by" in any SKILL.md frontmatter

  # anchor: X.4.1
  Scenario: Skill composition
    Given a skill "dramatica-vocabulary" composes "dramatica-theory"
    When the author defines the linkage
    Then "dramatica-vocabulary/SKILL.md" MUST contain "dramatica-theory:embed" in its "skill_references_skills" list
```

## 7. Bootstrap Protocol

This section ratifies preliminary research from `research/skills-skill-architecture/output/SPEC.md` (§2 R1, §8 R7).

The canonical shell implementation of this protocol is [`skills/skills-skill-bootstrap/sync.sh`](./skills/skills-skill-bootstrap/sync.sh). New agents SHOULD read this implementation before authoring their own bootstrap logic.

- **B.1** Mandatory bootstrap-before-skill-use for every agent. Every agent (`claude-code`, `jules`, `gemini-cli`, `claude-ai`) MUST run the bootstrap before touching `/skills/` or executing a skill. (`claude-ai` host-routing semantics are deferred to §10 U3.)
- **B.2** Canonical clone path `$AGENCY_SKILLS_ROOT`. The bootstrap MUST clone or fast-forward `origin/main` into the active workspace at a known path; the path is stored in environment variable `AGENCY_SKILLS_ROOT`.
- **B.3** Manifest emission to `$AGENCY_SKILLS_ROOT/.skills-manifest.json`. The bootstrap MUST emit a manifest of all skill slugs and their `skill_kind` to this path so that downstream tools can route without re-walking the tree. The manifest SHOULD also carry the `skill_bundles_tools` list per skill so consumers can locate the materialised `scripts/_bundled/<slug>/` paths without re-parsing every SKILL.md (per [ADR-0007](./decisions/0007-skill-bundles-tools-frontmatter.md)).
- **B.4** Staleness gate. The bootstrap MUST surface a non-zero exit on staleness > 24h to force a sync at the cost of a per-day prompt to the human; the agent MAY override with `AGENCY_SKILLS_ALLOW_STALE=1` for offline work.
- **B.5** Token-efficient navigation. Agents MUST query the manifest and the frontmatter index before opening any SKILL.md body. This is the single token-saving lever that makes a multi-skill repo cheap to consult.

### 7.1 Gherkin Scenarios

```gherkin
Feature: Agent Bootstrap

  # anchor: B.1.1
  Scenario: Agent encounters a skill request
    Given an agent is asked to load a skill
    When the agent starts the task
    Then the agent MUST execute the bootstrap protocol before opening any SKILL.md

  # anchor: B.2.1
  Scenario: Bootstrap clones into the canonical path
    Given an agent starts the bootstrap protocol
    When the bootstrap step completes
    Then the skills directory MUST be accessible at the path stored in `$AGENCY_SKILLS_ROOT`
    And `$AGENCY_SKILLS_ROOT` MUST reflect an up-to-date clone of `origin/main`

  # anchor: B.3.1
  Scenario: Bootstrap emits the skills manifest
    Given an agent has completed the clone step
    When the bootstrap finalises
    Then `$AGENCY_SKILLS_ROOT/.skills-manifest.json` MUST exist and be valid JSON
    And the manifest MUST list every skill slug and its `skill_kind` present in `/skills/`

  # anchor: B.4.1
  Scenario: Staleness gate blocks a stale workspace
    Given the last bootstrap ran more than 24 hours ago
    When an agent attempts to use a skill
    Then the bootstrap MUST exit with a non-zero code
    And the agent MAY override the gate by setting `AGENCY_SKILLS_ALLOW_STALE=1`

  # anchor: B.5.1
  Scenario: Agent consults manifest before opening SKILL.md body
    Given an agent needs to locate or invoke a skill
    When the agent starts its skill-lookup
    Then the agent MUST query `.skills-manifest.json` and the frontmatter index first
    And the agent MUST NOT open any `SKILL.md` body without first consulting the manifest
```

## 8. Cross-Agent Portability

This section resolves adapter architecture (R7.2) and reserved portability tracking (see follow-up prompts `/prompts/skills-skill-jules-portability/` and `/prompts/skills-skill-gemini-cli-portability/`).

- **P.1** Every skill SHOULD declare every agent it has been verified-portable to in `skill_target_agents`. Skills with `claude-ai` only are not failures, but they are flagged by the index as single-agent.
- **P.2** Multi-agent skills MUST live in `skills/<slug>/SKILL.md` with optional adapter overlays at `skills/<slug>/adapters/<agent>/`.
- **P.3** A skill MUST NOT silently change behavior across agents. Any agent-specific divergence MUST be encoded in an adapter overlay; the canonical `SKILL.md` MUST be agent-neutral.

## 9. Mandatory Pre-Commit Checks

| Check | Tool | Failure mode |
|---|---|---|
| §9.1 Frontmatter Integrity | `tools/validate-frontmatter.py` | Missing L1/L2 keys, YAML depth > 1 |
| §9.2 Skill-Reference Resolution | `tools/lint-linkage.py` (extended in Task 010) | `skill_references_*` slug doesn't resolve |
| §9.3 Bootstrap Manifest Freshness | `tools/skills-manifest.py` (Task 010) | Manifest out of sync with `/skills/` |
| §9.4 Header Conformance | `tools/lint-structure.py` + header-ontology schema (Task 011) | SKILL.md missing REQUIRED `##` section |
| §9.5 Cross-Agent Adapter Parity | human review for now; future linter | Adapter directory referenced but missing |
| §9.6 Readme Audit | `tools/lint-structure.py` | Missing `readme.md` in skill folder |
| §9.7 Bootstrap-Required Self-Honesty | `tools/lint-linkage.py` | `skill_bootstrap_required: false` skill that imports from `references/` |
| §9.8 Bundle-Path Resolution | `tools/fm/validate.py` (`_check_skill_bundles`) | `skill_bundles_tools` entry malformed, contains `..`, duplicated, or does not resolve to an existing `tools/<slug>/` directory (diagnostic `F.B.5`). Transitive dependency missing per `BUNDLE_DEPS` (diagnostic `F.B.6`). Authority: [ADR-0007](./decisions/0007-skill-bundles-tools-frontmatter.md). |

## 10. Edge Cases & Open Questions

- **U1 / U2 (from R1, R7)**: Whether `git` is available inside the container and whether the filesystem persists across sessions. Deferred to Gemini Deep Research.
- **U3**: How claude.ai's host selects which skill to activate. Deferred to Gemini Deep Research.

## 11. Anti-Patterns

- **A.1** Defining multi-level YAML frontmatter in a `SKILL.md`.
- **A.2** Changing canonical skill behavior for a specific agent without an adapter overlay.
- **A.3** Opening a `SKILL.md` without querying the manifest or index first.
