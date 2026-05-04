---
type: research
status: active
slug: skills-navigation-bootstrap
summary: "Preliminary RFC-2119 architecture for skill-to-skill navigation, per-agent bootstrap, and a token-efficient markdown indexing tool suite, plus a draft of the root SKILLS.md governance spec (Annex A)."
created: 2026-05-04
updated: 2026-05-04
research_phase: complete
research_executes_prompt: skills-navigation-bootstrap
research_friction_level: FL1
---

# Preliminary Architecture Spec — Skills Navigation, Bootstrap & Indexing

**Status:** Preliminary v1 — research-only output. Implementation is deferred to Tasks [009](../../../tasks/009-author-skills-root-spec/), [010](../../../tasks/010-skills-frontmatter-index-suite/), and [011](../../../tasks/011-skills-frontmatter-schema-files/).

**RFC 2119:** The key words MUST, MUST NOT, REQUIRED, SHALL, SHALL NOT, SHOULD, SHOULD NOT, RECOMMENDED, MAY, and OPTIONAL in this document are to be interpreted as described in BCP 14 \[RFC 2119\] \[RFC 8174\].

---

## 1. Purpose & Scope

This document specifies the architecture by which:

1. A skill body in `/skills/<name>/SKILL.md` cross-references another skill *token-efficiently*.
2. An agent (Claude Code, claude.ai, Jules, gemini-cli) materialises the canonical skill set into its runtime — the **bootstrap** — without each agent reinventing the protocol.
3. The repository emits a single, small, machine-readable manifest that drives navigation across all agents.
4. The `/skills/` directory acquires the root governance file it currently lacks (Annex A — draft `SKILLS.md`).

**In scope:** the `skill_*` L2 namespace; the agent-neutral bootstrap contract; the manifest schema + tool suite contract; the draft `SKILLS.md`.

**Out of scope:** any implementation, any modification of root governance files, any modification of `research_phase: complete` workspaces (in particular `research/skills-skill-architecture/`). These are explicitly Task 009/010/011 territory.

---

## 2. Inventory of Existing Primitives

The repository already provides nine of the ten primitives needed; only the root governance file itself is missing.

| Primitive | Location | Status |
|---|---|---|
| 14 canonical skill bodies | `/skills/<name>/SKILL.md` | Present. |
| Repo→Claude-Code sync tool | `skills/skills-skill-bootstrap/sync.sh` | Present, tested end-to-end. |
| Repo→Claude-Code sync verifier | `skills/skills-skill-bootstrap/verify.sh` | Present. |
| L1 Vault Core frontmatter ontology | `TASK.md` §3 | Present. |
| L2 namespacing pattern (`task_*`, `prompt_*`, `research_*`) | `TASK.md` §3.3 | Present. Adds the missing `skill_*` namespace in §3 below. |
| Per-skill `SKILL.md` frontmatter (Anthropic schema) | each `skills/<name>/SKILL.md` | Present (`name`, `description`, optional `metadata`). Augmented by `skill_*` here. |
| Pre-commit linters | `tools/{validate-frontmatter,lint-structure,lint-linkage,check-trust}.py` | Present. Need a small extension for `/skills/` (Task 010). |
| claude.ai loader architecture (preliminary) | `research/skills-skill-architecture/output/SPEC.md` | Complete; six U-markers deferred to Gemini Deep Research. |
| Token-efficient frontmatter cheatsheet | `research/obsidian-frontmatter-agentic-spec/output/SPEC.md` | Present. |
| **Root governance spec for `/skills/`** | none | **Missing — drafted as Annex A.** |

The existing `skills/readme.md` body explicitly acknowledges the gap and points to Tasks 009/010/011 to close it. This research run produces the input those tasks consume.

---

## 3. Skill-to-Skill Navigation Surface

### 3.1 Design Principle

Navigation between skills MUST ride on YAML frontmatter, not body-level Markdown links. Rationale: `FOLDERS.md` §6 already declares frontmatter as the source of truth for cross-directory linkage; consistency lowers cognitive load for both agents and humans, and is mechanically enforceable by the existing linkage linter with a small extension.

### 3.2 Proposed L2 Namespace — `skill_*`

The following L2 keys SHOULD be added to every `/skills/<name>/SKILL.md`. The keys are flat (no nesting beyond depth 1), per `TASK.md` §3.3.

| Key | Type | Purpose |
|---|---|---|
| `skill_kind` | string | One of: `meta`, `domain`, `tool`, `bootstrap`, `adapter`. Drives the agent's "should I activate this?" gate. |
| `skill_tier` | string | One of: `T1`, `T2`, `T3`. Maps to the disclosure ladder defined in `research/skills-skill-architecture/` §5. `T1` = always-on (summary only); `T2` = full body on activation; `T3` = references on demand. |
| `skill_uses` | list | Slugs of other skills this skill loads or hands off to. |
| `skill_complements` | list | Slugs the agent SHOULD consider activating *together* with this one. |
| `skill_supersedes` | string | OPTIONAL. Slug this skill replaces; the bootstrap CLI surfaces a deprecation warning when both are installed. |
| `skill_triggers` | list | Trigger phrases. Today these are encoded prose-style in the `description` paragraph; lifting them into a flat list makes them machine-extractable for the manifest. |

**Reciprocity rule:** if `A.skill_uses` lists `B`, the linker emits a warning (not error) when `B.skill_complements` does not list `A`. Reciprocity is encouraged but not mandated, because `uses` is directional whereas `complements` is symmetric.

### 3.3 Compatibility with the Existing Anthropic Schema

The existing `name:` and `description:` keys in each `SKILL.md` MUST remain unchanged — they are read by the host (claude.ai, Claude Code) and changing them breaks activation. The `skill_*` keys are *additive*; they coexist with `name`/`description`/`metadata`. The current `metadata.always_on` flag in `prompt-optimizer/SKILL.md` becomes redundant once `skill_tier: T1` is adopted; migration is a Task 009 concern.

### 3.4 Gherkin Scenarios — §3

```gherkin
Feature: Skill-to-skill navigation rides on frontmatter

  # anchor: SN.3.1
  Scenario: Adding skill_uses creates a manifest edge
    Given skills/dramatica-theory/SKILL.md exists
    And the file's frontmatter sets "skill_uses: [dramatica-vocabulary]"
    When tools/skills-index.py emit runs
    Then the manifest record for dramatica-theory MUST contain "uses: [dramatica-vocabulary]"
    And the manifest record for dramatica-vocabulary MUST be reachable via reverse-lookup

  # anchor: SN.3.2
  Scenario: Reciprocity warning, not error
    Given skills/A/SKILL.md sets "skill_uses: [B]"
    And skills/B/SKILL.md does not set "skill_complements: [A]"
    When the linkage linter runs
    Then the linter MUST emit a WARNING citing SN.3.2
    And the linter MUST NOT exit non-zero solely on this warning
```

---

## 4. Per-Agent Bootstrap Status Matrix

| Agent | Materialisation path | Status | Mechanism |
|---|---|---|---|
| Claude Code | `~/.claude/skills/<name>/SKILL.md` | **Live** | `skills/skills-skill-bootstrap/sync.sh` (one-way pull). |
| claude.ai | `/mnt/skills/user/<name>/SKILL.md` (read-only) plus `~/.claude/skills-skill/repo/` (clone) | **Preliminary** | Future `skills-skill` stub per `research/skills-skill-architecture/` — six U-markers deferred. |
| Jules | unknown | **Open** | Filed as `prompts/skills-skill-jules-portability/`. |
| gemini-cli | unknown | **Open** | Filed as `prompts/skills-skill-gemini-cli-portability/`. |

This run does NOT fill the open cells. It sets the contract those agents MUST honour (§5 below) so that whichever follow-up research lands first can plug in.

---

## 5. Agent-Neutral Bootstrap Contract

### 5.1 Contract

Every agent runtime MUST satisfy three steps in order:

1. **Materialise** — Make every canonical `/skills/<name>/SKILL.md` body readable by the host. The implementation MAY be a clone, a sync, a virtual filesystem mount, or a runtime fetch; the contract is solely that the body becomes readable at a stable path before the next step.
2. **Emit Manifest** — Run the manifest emitter (§6) once per session-start to produce `<runtime-skills-dir>/.index.json`. The manifest is the agent's primary navigation surface.
3. **Register with Host** — Tell the host runtime which skills are now available. Implementation is host-specific (claude.ai uses native triggers; Claude Code reads `~/.claude/skills/`; Jules and gemini-cli unknown).

### 5.2 Failure-Mode Surface

| Failure | Required behaviour |
|---|---|
| Materialisation fails (network, permission, disk) | The agent MUST surface a visible error and refuse to silently fall back to a stale or partial set. |
| Manifest emission fails | The agent MUST fall back to scanning each `SKILL.md` directly and MUST log a warning citing the failure. |
| Manifest is stale (SHA mismatch) | The agent MUST re-emit before reading. |
| Host registration partial | The agent MUST log which slugs failed to register and MUST NOT silently advertise them as available. |

### 5.3 Gherkin Scenarios — §5

```gherkin
Feature: Agent-neutral bootstrap contract

  # anchor: SN.5.1
  Scenario: Successful bootstrap
    Given an agent supports the bootstrap contract
    And the network is available
    When the agent starts a session
    Then the agent MUST materialise canonical skill bodies
    And the agent MUST emit the manifest at <runtime-skills-dir>/.index.json
    And the agent MUST register the materialised slugs with its host

  # anchor: SN.5.2
  Scenario: Manifest emitter unavailable, fallback to body scan
    Given materialisation succeeded
    And tools/skills-index.py is not present in the runtime
    When the agent attempts to emit the manifest
    Then the agent MUST log a warning citing SN.5.2
    And the agent MUST proceed by scanning each SKILL.md directly
    And the agent MUST NOT mark the bootstrap as failed
```

---

## 6. Markdown Indexing Tool Suite

### 6.1 Goal

A single token-efficient navigation surface that every agent reads first. Concrete target: a typical "what skills are available?" query MUST be answerable from ≤ 8 KB of JSON for the current 14 skills, and SHOULD be answerable from ≤ 40 KB for any plausible near-term growth (≤ 100 skills).

### 6.2 Tool Surface

| Tool | Contract |
|---|---|
| `tools/skills-index.py emit [--target DIR]` | Reads every `/skills/*/SKILL.md`, writes `<DIR>/.index.json`. Default `<DIR>` is `~/.claude/skills/`. Idempotent. |
| `tools/skills-index.py get <slug> [--section <name>]` | Reads `<DIR>/.index.json`. Without `--section`, returns the manifest record for `<slug>`. With `--section`, extracts the named `## Section` block from `<slug>/SKILL.md`. |
| `tools/skills-index.py verify` | Recomputes the manifest in memory and exits non-zero if `<DIR>/.index.json` differs. Used by `verify.sh`. |

The CLI is intentionally three verbs deep. No subcommand graph. Every option is positional or a `--flag VALUE` pair so completion is trivial across shells.

### 6.3 Manifest Schema (Sketch)

```json
{
  "schema_version": "1.0",
  "generated_at": "<ISO-8601>",
  "repo_sha": "<short SHA of HEAD>",
  "skills": [
    {
      "slug": "<name>",
      "kind": "<skill_kind>",
      "tier": "<skill_tier>",
      "summary": "<first 200 chars of description>",
      "triggers": ["..."],
      "uses": ["..."],
      "complements": ["..."],
      "supersedes": "",
      "sha": "<sha256 of SKILL.md body>"
    }
  ]
}
```

The full JSON Schema and validation rules are deferred to **Task 011** (`skills-frontmatter-schema-files`). This document specifies only the contract.

### 6.4 Failure Modes

| Mode | Behaviour |
|---|---|
| Manifest absent | Tool MUST emit a one-line warning and proceed by scanning bodies. |
| Manifest corrupt (invalid JSON) | Tool MUST surface the error and refuse to use the file. |
| Manifest schema mismatch | Tool MUST refuse to read; user MUST regenerate. |
| `--section <name>` not present in body | Tool MUST exit non-zero with a list of `## Sections` actually present in that body. |

### 6.5 Future Generalisation

The same emitter pattern generalises to `/prompts/` and `/research/`. This is *acknowledged* but **out of scope** here. Routing to a future task is at the discretion of Task 010's owner.

### 6.6 Header Schema (drives `--section`)

`tools/schemas/skill-headers.schema.json` SHOULD enumerate the canonical `## Section` headings every well-formed `SKILL.md` MAY use:

| Section | Purpose | Recommended length |
|---|---|---|
| `## What this skill is for` / `## What` | One-paragraph orientation. | ≤ 200 words. |
| `## When to use` / `## When NOT to use` | Activation gates. | ≤ 200 words each. |
| `## Triggers` | Bulleted phrases (machine-extractable). | ≤ 30 phrases. |
| `## Workflow` | The numbered execution protocol. | ≤ 1 KB. |
| `## Anti-patterns` | What NOT to do. | ≤ 500 words. |
| `## References` | Pointers into `references/`. | flat list. |

Existing skill bodies use a near-superset of these headings; Task 011 reconciles divergences. This document specifies only the schema *contract*, not the migration plan.

---

## 7. Open Questions Summary

| ID | Question | Routes To |
|---|---|---|
| Q1 | Exact `skill_*` value vocabularies, reciprocity rules, migration path. | New follow-up: `skills-namespace-ontology`. Pre-condition for Task 009/011. |
| Q2 | Manifest emitter contract: error codes, exit codes, full JSON Schema. | New follow-up: `skills-manifest-emission-tool`. Pre-condition for Task 010. |
| Q3 | claude.ai trigger lifecycle (U3 in `skills-skill-architecture`). | Existing follow-up: `skills-skill-trigger-lifecycle`. |
| Q4 | Jules skill-loading conventions. | Existing follow-up: `skills-skill-jules-portability`. |
| Q5 | gemini-cli skill-loading conventions. | Existing follow-up: `skills-skill-gemini-cli-portability`. |

---

## Annex A — Draft `SKILLS.md` (Root Governance)

> **Status:** Draft for ratification by [Task 009 — Author Skills Root Spec](../../../tasks/009-author-skills-root-spec/). MUST NOT be merged to repo root from this research workspace. Section IDs are local to this annex.

```markdown
---
type: spec
status: draft
slug: skills-spec
summary: "Root specification governing the /skills/ directory: SKILL.md format, the skill_* L2 namespace, the bootstrap contract, the indexing tool suite, and pre-commit checks."
created: 2026-05-04
updated: 2026-05-04
---

# Skills Specification

> **Mechanical Enforcement Notice:** Skills are mechanically validated by `tools/check-governance.sh` after Task 011 lands. Until then, frontmatter compliance is human-reviewed.

The `/skills/` directory holds the canonical, versioned bodies of all Claude skills. This file governs their format, navigation, bootstrap, and pre-commit checks. It is the missing sibling of `TASK.md`, `PROMPT.md`, and `RESEARCH.md`.

## A.1 Definitions (RFC 2119)

The keywords MUST, MUST NOT, SHOULD, SHOULD NOT, MAY, REQUIRED, RECOMMENDED, OPTIONAL are interpreted per BCP 14.

- **Skill** — A self-contained instructable capability stored in `/skills/<slug>/SKILL.md`, conformant to Anthropic's skill-creator schema (`name`, `description`, optional `metadata`).
- **Bootstrap** — The agent-side process of materialising the canonical skill set into the host runtime.
- **Manifest** — The machine-readable index of all skills, emitted by `tools/skills-index.py emit`.

## A.2 Directory Structure

Every skill MUST live in a dedicated subfolder under `/skills/`. The folder name MUST equal the `name:` field of its `SKILL.md`.

```text
/skills
└── /<slug>
    ├── SKILL.md             # MANDATORY. Anthropic schema + skill_* L2 namespace.
    ├── readme.md            # OPTIONAL human index; auto-generated from SKILL.md frontmatter.
    ├── references/          # OPTIONAL T3 disclosure content.
    ├── scripts/             # OPTIONAL executable helpers.
    └── assets/              # OPTIONAL static files referenced by the skill body.
```

`/skills/skills-skill-bootstrap/` is the **management layer**, not a domain skill: it ships the sync tool that materialises `/skills/` into Claude Code's `~/.claude/skills/`.

## A.3 Frontmatter

`SKILL.md` MUST carry the Anthropic schema (`name`, `description`, optional `metadata`). It SHOULD additionally carry the L2 `skill_*` namespace defined in §A.4.

`/skills/` is exempt from L1 Vault Core frontmatter (per `FOLDERS.md` §8) — the Anthropic schema is the source of truth for the host runtime, and dual-keying breaks activation.

## A.4 The `skill_*` L2 Namespace

| Key | Type | Purpose |
|---|---|---|
| `skill_kind` | string | `meta` \| `domain` \| `tool` \| `bootstrap` \| `adapter` |
| `skill_tier` | string | `T1` \| `T2` \| `T3` |
| `skill_uses` | list | Slugs this skill loads or hands off to. |
| `skill_complements` | list | Slugs the agent SHOULD consider activating together. |
| `skill_supersedes` | string | OPTIONAL. Slug this skill replaces. |
| `skill_triggers` | list | Trigger phrases (machine-extractable). |

YAML MUST NOT nest beyond one level (consistency with `TASK.md` §3.4).

## A.5 Workflow

1. **Author** — Draft `SKILL.md` per Anthropic's skill-creator. Slug = folder name = `name:` field.
2. **Wire** — Add `skill_*` keys per §A.4. Reciprocity (§A.6) emits warnings, not errors.
3. **Validate** — Run `tools/skills-index.py verify`. Pre-commit hook blocks if exit non-zero.
4. **Sync** — `skills/skills-skill-bootstrap/sync.sh` materialises bodies into `~/.claude/skills/`.
5. **Use** — Host activates the skill per its native trigger mechanism. The manifest is the agent's primary navigation surface.

## A.6 Reciprocity Rule

If `A.skill_uses` lists `B`, the linkage linter SHOULD emit a warning (not error) when `B.skill_complements` does not list `A`.

## A.7 Required Sections in `SKILL.md` Body

Every `SKILL.md` body SHOULD use the canonical `## Section` headings enumerated in §6.6 of this spec (the skill-headers schema). Divergences are tolerated; agents extracting via `tools/skills-index.py get <slug> --section <name>` simply error with the list of present sections.

## A.8 Pre-Commit Checks (deferred wiring)

After Task 010/011 land, `tools/check-governance.sh` SHALL include:

- `skills-index.py verify` — manifest is current.
- `lint-linkage.py --skills` — `skill_uses` and `skill_supersedes` slugs resolve.
- `validate-frontmatter.py --skills` — `skill_*` keys conform to `skills-frontmatter.schema.json`.

Until those tools exist, this section is informational.

## A.9 Anti-Patterns

- MUST NOT inline another skill's body inside `SKILL.md`. Use `skill_uses` and the manifest.
- MUST NOT modify `name:` or `description:` for stylistic reasons after a skill is published — the host caches them.
- MUST NOT add nested YAML keys.
- MUST NOT create new top-level skill folders for management tools; those belong in `/tools/`.

## A.10 Edge Cases

### A.10.1 Skill Renaming

Renaming MUST be done via a new slug + `skill_supersedes: <old-slug>`. The deprecated body remains for one release cycle; the manifest emits a deprecation flag.

### A.10.2 Cross-Agent Drift

A skill body that depends on a host capability not present in every agent (e.g., MCP tools) SHOULD declare this in its `## When NOT to use` section. There is no machine check for this today.

### A.10.3 References Larger Than the Body

When `references/` content exceeds the body by an order of magnitude, the body SHOULD push that content out and load it lazily via `skills-index.py get <slug> --section References`. This preserves the T2 size budget.
```

---

*End of SPEC.md. Annex A draft is ratification-ready for Task 009.*
