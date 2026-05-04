# Friction Log — skills-skill-architecture

**Highest Frustration Level: FL1**

---

## FL1 — Claude Code skill directory is undocumented

**What happened**: The mission instructs Stage B to "discover" where Claude Code's skill capability lives and design the sync against it. There is no public documentation, CLAUDE.md entry, or settings key that identifies `~/.claude/skills/` as the user-scoped skill directory for Claude Code. It was discovered by directly listing `/root/.claude/` and finding a `skills/` subdirectory with a `SKILL.md` file inside it.

**Impact**: Low — the directory was found quickly. But a future agent starting fresh would have no documented path to this discovery. If Anthropic renames the directory, all sync scripts break silently.

**Recommendation**: Add a note to the project's CLAUDE.md (or a new `docs/claude-code-paths.md`) documenting confirmed Claude Code filesystem conventions: skill dir, commands dir, agents dir, settings file. This prevents every new agent from spending discovery cycles on infrastructure archaeology.

---

## FL1 — claude.ai SKILL.md trigger lifecycle is opaque

**What happened**: R1 and R3 both require understanding of how claude.ai's native skill-trigger works — specifically: (a) how the host decides which skill to activate for a given user message, and (b) whether the stub receives the raw user message or a pre-processed intent signal.

This information is not documented in any governance spec, README, or published Anthropic documentation accessible during this run. The spec had to mark these as UNCERTAIN and defer to Gemini Deep Research.

**Impact**: Medium — the UNCERTAIN markers are correctly placed, but they represent real implementation blockers. An agent trying to implement `skills-skill` from this spec alone would have to guess at the trigger mechanism.

**Recommendation**: Michael should include the trigger lifecycle details in the follow-up prompt or in a brief.md addendum. If he knows how claude.ai selects which skill to inject, that information should pre-empt the Gemini research for R1 and R3.

---

## FL1 — Jules and gemini-cli have no discoverable skill-loading conventions

**What happened**: R6 asks how close the canonical `SKILL.md` can get to being loadable by all four agents. Jules and gemini-cli were not installed in the local environment, and no documentation about their skill-loading conventions was found.

**Impact**: Medium — two of four agents are completely unknown for R6. The spec correctly reserves adapter slots rather than guessing.

**Recommendation**: The Gemini Deep Research prompt explicitly asks for Jules and gemini-cli skill conventions. If Gemini can't answer those either, Michael should open dedicated research tasks with access to the relevant agent documentation or codebases.

---

## FL0 — Governance was clear and well-structured

The governance documents (AGENTS.md, FOLDERS.md, PRE_COMMIT.md, RESEARCH.md, PROMPT.md, FRUSTRATED.md) were well-written and unambiguous. The workflow from "create prompt → create research workspace → produce output → file follow-up prompts" was clean to execute. No contradictions between specs were encountered.
