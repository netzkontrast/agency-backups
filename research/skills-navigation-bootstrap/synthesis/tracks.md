---
type: note
status: active
slug: skills-navigation-bootstrap-tracks
summary: "Per-track work breakdown for the skills-navigation-bootstrap synthesis."
created: 2026-05-04
updated: 2026-05-04
---

# Tracks

The work was decomposed into four parallel tracks. Each maps to one section of `output/SPEC.md`.

## T-NAV — Inter-skill Navigation

**Question:** How can one `SKILL.md` reference another token-efficiently and unambiguously?

**Findings:**

- Body-level Markdown links are insufficient because they are not machine-readable without parsing each file.
- `FOLDERS.md` §6 already establishes that *frontmatter is the source of truth* for cross-directory linkage. The same rule SHOULD apply inside `/skills/`.
- Propose an L2 `skill_*` namespace mirroring the existing `task_*`, `prompt_*`, `research_*` patterns:
  - `skill_kind` — one of `meta`, `domain`, `tool`, `bootstrap`, `adapter`.
  - `skill_uses` — list of slugs this skill loads at T2/T3 disclosure time.
  - `skill_complements` — list of slugs the model SHOULD consider activating *together*.
  - `skill_supersedes` — slug this skill replaces (drives deprecation messaging).
  - `skill_triggers` — flat list of trigger phrases (already present as a free-text `description` paragraph; this lifts them into structured form).
  - `skill_tier` — `T1` (always-on, summary only), `T2` (full body on activation), `T3` (references on demand) — matching the disclosure ladder from `research/skills-skill-architecture/` §5.

**Out of scope here:** the exact value vocabulary, reciprocity rules, and migration path for the 14 existing skills. Filed as follow-up prompt `skills-namespace-ontology`.

## T-BOOT — Per-Agent Bootstrap

**Question:** How does each agent (Claude Code, claude.ai, Jules, gemini-cli) materialise the skill set into its runtime?

**Findings:**

- Claude Code is **already covered** by `skills/skills-skill-bootstrap/sync.sh` (one-way pull from `origin/main:/skills/` to `~/.claude/skills/`).
- claude.ai bootstrap is **deferred** — preliminary architecture exists at `research/skills-skill-architecture/output/SPEC.md`; six UNCERTAIN markers (U1-U6) await Gemini Deep Research before implementation.
- Jules and gemini-cli have **open follow-up prompts** filed by the architecture run (`skills-skill-jules-portability`, `skills-skill-gemini-cli-portability`). Their bootstrap is unknowable until those answer.
- The agent-neutral bootstrap **contract** is therefore the only durable abstraction here: `(materialise canonical bodies → emit/read manifest → register with host)`. Section §5 of the output SPEC writes this as Gherkin.

## T-INDEX — Markdown Indexing Tool Suite

**Question:** What is the minimum tool surface that makes 14 (and growing) skills navigable in token-efficient form?

**Findings:**

- A single emitter is sufficient: `tools/skills-index.py emit` reads each `SKILL.md` frontmatter and writes a flat `~/.claude/skills/.index.json` (≈ 8 KB for 14 skills today; grows linearly).
- A single query helper is sufficient: `tools/skills-index.py get <slug> [--section <name>]` extracts either the manifest record or one named section of the body. The `--section` flag is how the three-tier disclosure model is operationalised: T1 = manifest record, T2 = full body, T3 = a named `## Section` from `references/`.
- A header schema is required for `--section` to be deterministic: `tools/schemas/skill-headers.schema.json` enumerates the canonical `## Section` headings (`## What`, `## When to use`, `## Triggers`, `## Workflow`, `## Anti-patterns`, `## References`). Implementation deferred to Task 010/011.
- `verify` (already exists alongside `sync.sh`) covers integrity of the materialised tree; no new tool needed for that.

## T-SPEC — Root `SKILLS.md` Draft

**Question:** What is the minimum normative content that closes the governance gap acknowledged in `skills/readme.md`?

**Findings:**

- The other root specs (`TASK.md` 258 lines, `PROMPT.md` similar, `RESEARCH.md` similar) are the right size envelope.
- The draft (Annex A of `output/SPEC.md`) follows their structure: Definitions → Directory Structure → Frontmatter (L1 + new `skill_*` L2) → Workflow → Required Sections → Gherkin scenarios → Pre-commit checks → Edge cases → Anti-patterns.
- Two scopes are deliberately deferred to Task 009: (a) ratifying the exact `skill_*` key set; (b) folding `SKILLS.md` into `AGENTS.md`'s task-routing table. This research drafts the spec; it does not merge it.
