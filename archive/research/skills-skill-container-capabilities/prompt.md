---
type: prompt
status: active
slug: skills-skill-container-capabilities
summary: "Research what tools and runtimes are available in the claude.ai session container, whether skills can execute shell commands, and whether the filesystem persists between sessions — resolving UNCERTAIN markers U1 and U2 from the skills-skill-architecture spec."
created: 2026-05-04
updated: 2026-05-04
prompt_kind: follow-up
prompt_framework: RISEN
prompt_target_agent: Claude Code
prompt_relates_to_task: ""
prompt_spawned_from_research: skills-skill-architecture
---

# Research: claude.ai Container Capabilities for skills-skill Bootstrap

## Role

You are a technical researcher with access to web search. Your task is to determine the execution environment available inside a claude.ai web session — specifically the tools, runtimes, and filesystem behaviour that a SKILL.md stub would encounter when it tries to bootstrap a git-backed skill loader.

## Information

The `skills-skill` architecture spec (`research/skills-skill-architecture/output/SPEC.md`) proposes a bootstrap sequence (Steps B1–B5) that relies on `git clone` / `git fetch` to pull skill bodies from a GitHub repository. This approach contains two CRITICAL UNCERTAIN markers:

- **U1 (Critical)**: Whether `git` is available as an executable in the claude.ai session container's `PATH`. If not, the entire B1–B5 clone sequence must be replaced with an HTTP-based alternative (GitHub REST API via `curl`, GitHub MCP server, Python `requests`, etc.).
- **U2 (High)**: Whether the claude.ai container's filesystem at `~/.claude/` persists across sessions. If ephemeral, every session incurs a full clone latency cost; the pull-if-exists optimisation is moot.

A Gemini Deep Research prompt exists at `research/skills-skill-architecture/output/gemini-prompt.md` (questions R1-Q1 and R7-Q1) but has not yet been executed. This research prompt is the Claude Code-executed counterpart, using web search to gather the same intelligence.

## Scope

Research the following questions in priority order:

### Q1 (Critical — resolves U1)

Is `git` available in the claude.ai session container?

- Search for Anthropic documentation, claude.ai changelog entries, and community reports (GitHub discussions, Reddit, Discord threads, developer blogs) that describe the shell environment available to claude.ai skills or Projects.
- If `git` is unavailable, identify the best-supported alternative for fetching content from a public GitHub repository: `curl`, `wget`, Python `requests`, the GitHub REST API, or the GitHub MCP server connector.
- Determine what shell utilities and runtimes are available: `bash`, `sh`, `python3`, `node`, `curl`, `wget`, `jq`, `gpg`, etc.
- Determine whether a SKILL.md body can trigger shell command execution at all, or whether it only injects text into the model's context (i.e., is there a tool-use or Bash tool available to skills in the claude.ai web interface?).

### Q2 (High — resolves U2)

Does the claude.ai session container's filesystem persist between sessions?

- Determine whether files written to `~/.claude/` (or any writable path outside `/mnt/skills/user/`) survive a session end and reappear in the next session for the same user.
- If ephemeral: estimate the latency of a shallow `git clone --depth 1` of a ~5 MB public GitHub repository from within a claude.ai session (or the equivalent HTTP fetch latency), based on any available reports.
- If persistent: document the persistence boundary (per user, per browser, per device) and any capacity or durability caveats Anthropic has mentioned.
- Identify any Anthropic-documented persistent storage mechanism available to skills beyond the read-only `/mnt/skills/user/` mount.

### Q3 (Medium — informs redesign if U1 is negative)

If `git` is definitively unavailable, what is the most practical bootstrap alternative?

- Evaluate the GitHub REST API (`/repos/{owner}/{repo}/contents/{path}`) via `curl`/`wget` or Python `requests`.
- Evaluate the GitHub MCP server connector (if it is registered by default in claude.ai sessions).
- Evaluate a pre-rendered static skill-index served from a GitHub Pages URL.
- For each alternative, note: availability in the container, authentication requirements for public repos, rate limits, and approximate latency.

## Necessary Steps

1. Search Anthropic's official documentation and changelog for any description of the claude.ai skill execution environment.
2. Search GitHub, Reddit (r/ClaudeAI), Discord (Anthropic), and developer blogs for first-hand reports of tool availability in claude.ai skills.
3. Search for any open-source SKILL.md examples that demonstrate shell command execution from within a claude.ai skill.
4. Check the Claude Code documentation for differences between the claude.ai web container and the Claude Code CLI environment (both use SKILL.md but may have different tool access).
5. Synthesise findings into normative RFC-2119 language suitable for patching the UNCERTAIN markers in `research/skills-skill-architecture/output/SPEC.md`.

## Expected Output

Produce `research/skills-skill-container-capabilities/output/SPEC.md` with:

1. A definitive (or best-evidence) answer to U1: is `git` available, yes/no, with evidence citations.
2. A definitive (or best-evidence) answer to U2: is the filesystem persistent, yes/no, with evidence citations.
3. If U1 = no: a ranked list of alternative bootstrap mechanisms with pros/cons.
4. Normative PATCH text ready to replace the `> **UNCERTAIN (U1)**` and `> **UNCERTAIN (U2)**` blocks in `research/skills-skill-architecture/output/SPEC.md`.
5. A friction log at `research/skills-skill-container-capabilities/reflection/friction-log.md` per `FRUSTRATED.md`.

## Reflection

After completing the research, apply the following critical-thinking method:

- **M13 — Evidence Quality**: For each finding, rate the evidence as: (a) Anthropic-official, (b) community-confirmed (multiple independent sources), (c) single-source anecdote, or (d) inference. Flag any finding rated (c) or (d) as requiring verification before the architecture spec is patched.
