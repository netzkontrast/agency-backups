---
type: research
status: archived
slug: skills-navigation-bootstrap
summary: "Research workspace executing /prompts/skills-navigation-bootstrap/. Designs the inter-skill navigation surface, the bootstrap process, a token-efficient markdown indexing tool suite, and drafts a normative SKILLS.md root spec."
created: 2026-05-04
updated: 2026-05-12
research_phase: archived
research_executes_prompt: skills-navigation-bootstrap
research_friction_level: FL1
---

# /research/skills-navigation-bootstrap/

**What is this folder?** Execution workspace for the prompt at [`/prompts/skills-navigation-bootstrap/`](../../prompts/skills-navigation-bootstrap/). It produces a preliminary architecture for skill-to-skill navigation, a per-agent bootstrap protocol, schemas for token-efficient markdown indexing, and a draft `SKILLS.md` (the missing root governance spec for `/skills/`).

**Why is it here?** Per `RESEARCH.md`, every research run lives in `/research/<slug>/` where the slug equals the executing prompt's slug.

## Linked Navigation

| Path | Purpose |
|---|---|
| [prompt.md](./prompt.md) | Immutable run-start snapshot of the executing prompt. |
| [workspace/](./workspace/) | Session log + scratch notes from the research run. |
| [synthesis/](./synthesis/) | Methodology, tracks, state, post-synthesis log. |
| [reflection/](./reflection/) | Friction-log (FL1). |
| [output/](./output/) | Deliverable: `SPEC.md` (architecture + draft root `SKILLS.md`). |

## Key Findings

1. **Three concerns are conflated in the prompt and MUST be separated downstream:** (a) the `/skills/` root governance spec — a new sibling of `TASK.md`/`PROMPT.md`/`RESEARCH.md`; (b) a per-skill *navigation surface* that lets one skill cross-reference another token-efficiently; (c) an agent-side *bootstrap* protocol that materialises that surface in each agent runtime (Claude Code, claude.ai, Jules, gemini-cli). The output spec routes each concern to its own downstream Task (009/010/011).
2. **The repository already has nine of the ten necessary primitives.** Frontmatter ontology (TASK.md §3), runtime sync (`skills-skill-bootstrap/sync.sh`), and a draft loader architecture (`research/skills-skill-architecture/`) all exist. The only missing primitive is the `skills/` root governance file itself. Recommend that the spec be named `SKILLS.md` for symmetry with the other root specs.
3. **Skill→skill navigation should ride on existing frontmatter, not a new graph format.** Add an L2 `skill_*` namespace (`skill_uses`, `skill_complements`, `skill_supersedes`, `skill_kind`, `skill_triggers`, `skill_tier`) to each `SKILL.md`. Edges become first-class for tooling without a separate index file.
4. **Token-efficient indexing collapses to a single small JSON manifest emitted from frontmatter.** `tools/skills-index.py emit` writes `~/.claude/skills/.index.json` (≤ 8 KB for 14 skills) carrying name, description (truncated to 200 chars), L2 keys, and SHA. Every agent reads the manifest first; it opens a body only on demand. This is the T1 layer of the three-tier disclosure model from `research/skills-skill-architecture/`.
5. **Bootstrap is per-agent and MUST NOT assume a single binary.** The bootstrap contract is `(materialise canonical skill bodies → emit manifest → register with host)`. Claude Code uses `sync.sh`; claude.ai uses the future `skills-skill` stub; Jules and gemini-cli are deferred per follow-up prompts already filed by `skills-skill-architecture`.
6. **Header semantics MUST be schema'd, not narrative.** A `headers.schema.json` enumerates the canonical `## Sections` an agent may extract (`## What`, `## When to use`, `## Triggers`, `## Workflow`, `## Anti-patterns`, `## References`). The query CLI then supports `--section` to extract just the requested block, cutting the typical skill-load token cost by ~70 %.

## Open Questions Surfaced

Per `RESEARCH.md` §4.9, every unresolved question MUST be filed as a follow-up prompt under `/prompts/`. This run filed:

| Slug | Question |
|---|---|
| [`skills-namespace-ontology`](../../prompts/skills-namespace-ontology/) | What is the exact `skill_*` L2 key set, value vocabularies, and reciprocity rule for skill-to-skill edges? Pre-condition for Tasks 009/011. |
| [`skills-manifest-emission-tool`](../../prompts/skills-manifest-emission-tool/) | What are the contract, output schema, and invocation semantics of `tools/skills-index.py emit`? Pre-condition for Task 010. |

The three pre-existing follow-ups from `skills-skill-architecture` (Jules, gemini-cli, trigger-lifecycle) remain valid and are *not* re-filed here.

## Workflow Assumptions

- The prompt's "draft a `skill.md` root spec" instruction is interpreted as **draft `SKILLS.md`** (uppercase, plural). Rationale: the existing root specs (`TASK.md`, `PROMPT.md`, `RESEARCH.md`) all use the plural form because they govern a directory whose name is the same plural form (`/tasks/`, `/prompts/`, `/research/`). The directory under audit is `/skills/`, not `/skill/`. This assumption is logged in `synthesis/state.md` and forwarded to Task 009.
- The research is preliminary and explicitly *delegates* implementation to Tasks 009/010/011 (already filed). The spec MUST NOT be merged to repo root from this research workspace; that ratification belongs to Task 009. This is a Narrowing constraint of the executing prompt.
- No web search was performed. All synthesis is from direct repository inspection and prior research in `research/skills-skill-architecture/` and `research/obsidian-frontmatter-agentic-spec/`.
- Pre-existing structural lint errors in `prompts/claude-ai-container-git-verification/`, `prompts/skills-skill-container-capabilities/`, and `prompts/skills-skill-enterprise-offline/` (missing `brief.md` / `readme.md`) are *out of scope* for this task and intentionally not repaired here. They are surfaced in `reflection/friction-log.md` and SHOULD be folded into Task 008 (coherence-baseline hardening).
