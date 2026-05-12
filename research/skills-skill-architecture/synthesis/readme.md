---
type: index
status: active
slug: skills-skill-architecture
summary: "Synthesis artifacts for the skills-skill-architecture research run."
created: 2026-05-04
updated: 2026-05-04
---

# /research/skills-skill-architecture/synthesis/

Structured synthesis artifacts for the skills-skill-architecture research run.

## Hard Results

1. **Claude Code skill format confirmed identical to claude.ai**: `~/.claude/skills/<name>/SKILL.md` — same SKILL.md format, no adapter needed.
2. **Read/write topology established**: `/mnt/skills/user/` is read-only ephemeral; repo is canonical; `~/.claude/skills/` is a consumer synced by Stage B's bootstrap tool.
3. **Routing model**: Two-tier (host activates stub; stub selects skill body). The stub complements the host's trigger mechanism, does not replace it.
4. **Progressive disclosure**: Three-tier content ladder (summary → full body → references).
5. **Jules and gemini-cli remain unknown**: Dedicated follow-up prompts filed. Adapter slots reserved in the architecture.
6. **Three UNCERTAIN markers** propagated into the spec (host trigger mechanism, git availability in container, container persistence across sessions).

## Linked Navigation

| File | Purpose |
|---|---|
| [methodology.md](./methodology.md) | Research methods applied (M01–M05) |
| [tracks.md](./tracks.md) | Per-track synthesis (A: R1+R5, B: R2+R7, C: R3+R4, D: R6) |
| [post-synthesis-log.md](./post-synthesis-log.md) | Merge sequence and contradiction check |
| [state.md](./state.md) | Synthesis checklist (all steps checked off) |

## Assumptions Log

- No web search was performed. All synthesis is based on direct environment inspection and analogical reasoning from the confirmed claude.ai and Claude Code skill formats. Gemini Deep Research is expected to fill the empirical gaps for Jules, gemini-cli, and the claude.ai trigger lifecycle.
