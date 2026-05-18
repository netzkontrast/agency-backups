---
type: research
status: active
slug: skills-skill-jules-portability
summary: "Jules native custom-instruction format is AGENTS.md (Markdown, lexical scope, nested overrides). SKILL.md is NOT natively compatible — an AGENTS.md adapter is REQUIRED for skill portability."
created: 2026-05-18
updated: 2026-05-18
research_phase: complete
research_executes_prompt: skills-skill-jules-portability
research_friction_level: FL2
---

# Research Output: Jules Custom-Instruction Loading and SKILL.md Portability

**RFC-2119**: The key words MUST, MUST NOT, REQUIRED, SHALL, SHALL NOT, SHOULD, SHOULD NOT, RECOMMENDED, MAY, and OPTIONAL in this document are to be interpreted as described in RFC 2119.

This document answers the follow-up question filed at `/prompts/skills-skill-jules-portability/` on 2026-05-04, which corresponds to UNCERTAIN marker **U4** in `research/skills-skill-architecture/output/SPEC.md`. The basis is an externally-captured Jules architecture analysis (Gemini 3 era), reproduced verbatim at [source-jules-architecture.md](./source-jules-architecture.md).

---

## 1. Conclusion

Google Jules DOES support repository-scoped custom instructions, but the mechanism is **`AGENTS.md`**, not `SKILL.md`. `AGENTS.md` is plain Markdown without YAML frontmatter, is loaded unconditionally for the directory tree it occupies, and supports nested override semantics. The Claude `SKILL.md` convention — YAML frontmatter plus a `description:`-keyed trigger mechanism — has no native counterpart on Jules. Therefore, any skill that the `skills-skill` orchestrator wants Jules to "always know" MUST be surfaced through an `AGENTS.md` shim: either inlined into a root-level `AGENTS.md` or referenced from it. A thin adapter under `skills/skills-skill/adapters/jules/` is REQUIRED to make the canonical skill corpus portable to Jules.

---

## 2. Findings

The following five findings are extracted from the source analysis (see §5):

1. **Jules supports custom instructions natively.** Files named `AGENTS.md` placed inside the repository are read by Jules and treated as a "localized, overriding system prompt containing conventions, architectural rules, and mandatory testing directives." The system prompt explicitly commands Jules to read and obey these files before finalizing any operational plan.

2. **Format: plain Markdown.** No YAML frontmatter is required or used. There is no `description:` field, no `type:`, no `slug:`. The whole file is treated as instruction text.

3. **Scoping: lexical.** An `AGENTS.md` applies to the entire directory tree rooted at its location. There is no global "skills index"; placement determines scope.

4. **Nested overrides win.** Where multiple `AGENTS.md` files coexist in a monorepo, "the most deeply nested file overrides higher-level directives." This allows microservice-style local conventions, but it also means an inner `AGENTS.md` can silently shadow a root-level one.

5. **No native SKILL.md compatibility.** The `SKILL.md` convention is built around (a) YAML frontmatter and (b) a `description:`-keyed triggering mechanism. Neither concept exists on Jules. `AGENTS.md` is loaded unconditionally for its directory tree; there is no description-based dispatch. Consequently, skill discovery as implemented in `skills-skill-architecture` §4 (R3) is unavailable on Jules — every skill the orchestrator wants Jules to "always know" MUST be either inlined into `AGENTS.md` or linked from it.

---

## 3. Implications for `skills-skill-architecture`

The findings collapse U4 (Medium priority) to a known answer. The upstream SPEC at `research/skills-skill-architecture/output/SPEC.md` MUST be updated in three places:

- **§3.1 (R2 Read/Write Topology table)** — the `Jules skill directory` row MUST change from `UNKNOWN / UNKNOWN / UNKNOWN` to:
  - Location: `<repo>/AGENTS.md` (and optionally nested `AGENTS.md` files per directory tree)
  - Access: read by Jules at session start; written by the adapter generator at sync time
  - Who writes: the `skills-skill` Jules adapter (`skills/skills-skill/adapters/jules/`)
  - When: when the canonical skill corpus changes and the adapter is regenerated

- **§7.1 (R6 Confirmed Compatibility table)** — the `Jules` row MUST change from `UNKNOWN / UNKNOWN / UNKNOWN` to:
  - Skill directory: `<repo>/AGENTS.md`
  - Format: plain Markdown, no frontmatter, no `description:`-keyed trigger
  - Adapter needed: **YES** — `skills/skills-skill/adapters/jules/`

- **§9 (Open Questions Summary table)** — the `U4` row MUST be annotated as Resolved 2026-05-18, citing this output.

A conservative "Resolved" annotation appended next to each marker is sufficient. The surrounding paragraphs SHOULD NOT be rewritten — the original uncertainty framing remains historically accurate.

---

## 4. Recommended Adapter

This section describes the adapter at the conceptual level. **No implementation is delivered here** — that is a future Task.

**Adapter location**: `skills/skills-skill/adapters/jules/` (already reserved in `skills-skill-architecture` §7.2).

**Adapter responsibility**: produce a single consolidated `AGENTS.md` at repo root (or, per the lexical-scope rule, one `AGENTS.md` per active skill subtree) that makes the canonical skill corpus discoverable to Jules without relying on `description:`-keyed dispatch.

**Two viable shapes** — the choice is deferred to the implementing Task:

- **Shape A — consolidated root `AGENTS.md`**: a generator walks `skills/*/SKILL.md`, strips the YAML frontmatter, concatenates each body under a heading naming the skill, and writes the result to `<repo>/AGENTS.md`. Jules then has every skill body in context unconditionally. Cost: large `AGENTS.md`, high token load on every Jules session. Benefit: trivial for users — no per-skill invocation primitive required.

- **Shape B — index + references**: the generator writes a compact root `AGENTS.md` that names each skill and points Jules at `skills/<slug>/SKILL.md` (or a body-only mirror). Jules' `read_file` tool is then expected to fetch the body on demand. Cost: relies on Jules choosing to read the referenced file. Benefit: small `AGENTS.md`, no token blowup.

**Discovery gap**: regardless of shape, the `description:`-keyed trigger mechanism that `skills-skill-architecture` §4.1 (R3) relies on does NOT exist on Jules. The adapter MUST therefore either (a) inline everything Jules should always know, or (b) document each skill prominently enough that Jules' planner chooses to load it via `read_file`. There is no third option.

**Maintenance contract**: the adapter MUST regenerate `AGENTS.md` whenever the canonical skill corpus changes. A pre-commit or sync-time check SHOULD fail if `AGENTS.md` is stale relative to `skills/*/SKILL.md`.

---

## 5. Source

External Jules architecture analysis, captured 2026-05-18. Full text at `research/skills-skill-jules-portability/output/source-jules-architecture.md`. Specifically, §"Filesystem Topology and Lexical Scoping via AGENTS.md" of that document is the load-bearing passage; the rest of the source informs context (sandbox topology, tool schemas, MCP integration) but is not directly cited here.

The source is an externally-pasted analysis, not a live empirical observation inside a Jules sandbox. The friction level for this research output is therefore `FL2` (external research consumed). If a future Task gains direct access to a Jules sandbox and the AGENTS.md behaviour described here proves incorrect, this SPEC SHOULD be superseded by a new research run rather than amended in place.
