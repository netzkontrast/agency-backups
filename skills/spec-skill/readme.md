# spec-skill

## What
"Authoring, applying, and auditing normative specifications for autonomous AI agents and long-horizon agentic workflows — using RFC-2119 keywords, Gherkin acceptance criteria, and a fixed five-aspect schema (Explore, Plan, Implement, Review, Validate). Use this skill whenever the user wants to write a spec or specification for an agent, codify best practices for a coding/research/orchestration agent, draft normative MUST/SHOULD/MAY statements, derive prompts or workflows from an existing spec, validate a spec for schema-conformance and BCP-14 compliance, or convert vague requirements into a structured Markdown agent-specification document. Triggers on terms like spec, specification, RFC-2119, BCP-14, normative statement, MUST/SHOULD/MAY, Gherkin, acceptance criteria, agent best practices, agentic workflow spec, codify conventions, spec-driven, prompt spec, agent governance, long-horizon agent, autonomous agent prompt, write a spec, audit a spec, derive prompts from spec."

## Why here
Snapshot of the user-skill `/mnt/skills/user/spec-skill/` from a Claude.ai
session (taken 2026-05-04). Version-controlled here so that other agents
(Claude Code, Jules, gemini-cli) can read, audit, and propose changes via PR.
The session-side copy under `/mnt/skills/user/` remains the live runtime
"upstream" until a sync-back protocol is defined.

## Top-level navigation
- [SKILL.md](./SKILL.md)
- [references/](./references/)

## Assumptions Log
- Skill-internal subfolders (e.g. `references/`, `scripts/`, `agents/`) are
  NOT given their own `readme.md`. Rationale: skills are governed by `SKILL.md`
  and Anthropic's skill-creator conventions; adding per-subfolder readmes would
  trigger "Structural Bloat" per `FRUSTRATED.md` (FL2 special-trigger). This
  drift is logged once here and once globally in the PR Frustration Log.
- The `name` and `description` shown above are extracted verbatim from
  `SKILL.md` YAML frontmatter; if the skill is updated in `/mnt/skills/user/`,
  this readme drifts until the next snapshot run.
