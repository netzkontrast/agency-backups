# Methodology — skills-skill-architecture

## Methods Applied

### M01 — Direct Environment Inspection

Inspected the live Claude Code installation at `/root/.claude/`:
- Discovered `~/.claude/skills/<name>/SKILL.md` as the user-scoped skill convention.
- Confirmed `SKILL.md` format identical to the claude.ai convention.
- Confirmed no `skills_path` config key in `settings.json` — the directory is conventional, not configurable.
- Identified pre-existing skill: `session-start-hook/SKILL.md`.

**Result**: Claude Code and claude.ai share the same SKILL.md format. No adapter needed for skill bodies.

### M02 — Governance Document Analysis

Read all root governance specs to extract constraints applicable to the architecture:
- `FOLDERS.md §7`: `/skills/` is content, not operational — exempt from the task/prompt/research restriction.
- `MAINTENANCE.md §2`: Static/dynamic readme partition — relevant to how `skills-skill` might update readme inventory on sync.
- `PRE_COMMIT.md §7`: validate-frontmatter.py is the mechanical gate.
- `RESEARCH.md §4.9`: Open questions must exit to `/prompts/`, not accumulate in the workspace.

### M03 — Analogical Reasoning (claude.ai → Claude Code)

Mapped the two skill ecosystems side by side:

| Property | claude.ai | Claude Code |
|---|---|---|
| Skill dir | `/mnt/skills/user/<name>/` | `~/.claude/skills/<name>/` |
| Format | `SKILL.md` | `SKILL.md` |
| Writability | Read-only per session | Read-write |
| Persistence | Ephemeral (per session) | Persistent |
| Commands | Separate (not examined) | `~/.claude/commands/<ns>/<cmd>.md` |
| Agents | Separate (not examined) | `~/.claude/agents/<name>.md` |

Both use the same canonical SKILL.md format. The difference is persistence and writability, not format.

### M04 — Gap Analysis (Jules, gemini-cli)

Attempted to find Jules and gemini-cli skill-loading documentation:
- No `jules` binary or config found in the live environment.
- No `gemini-cli` binary or config found in the live environment.
- No mention of skill-loading conventions for either agent in the governance docs.

**Result**: Jules and gemini-cli are genuinely unknown. Three follow-up prompts filed.

### M05 — Failure Mode Enumeration (R1, R7)

Enumerated failure scenarios for the bootstrap stub:
1. Network unreachable at session start → use cached clone if available, else degrade gracefully.
2. Repo missing `/skills/` directory (pre-Stage A) → warn, no skills available.
3. Corrupt local clone → detect via `git fsck`, re-clone.
4. Requested skill not in repo → return "skill not found" message, list available skills.
5. Clone latency too high → configurable timeout; fall back to cached.
