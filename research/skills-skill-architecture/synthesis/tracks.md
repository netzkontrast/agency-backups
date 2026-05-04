# Synthesis Tracks — skills-skill-architecture

## Track A: Bootstrap Mechanics & Trust (R1, R5)

**Goal**: Define how the minimal stub in `/mnt/skills/user/skills-skill/` activates and routes, and what invariants it must enforce.

**Findings**:

R1 — The stub's job is two-phase: (1) ensure the repo is available locally (clone or fetch), and (2) inject the requested skill body into the model context. The stub lives in the read-only host directory and is therefore immutable per session — it cannot be modified by repo content it loads.

The host's native skill-trigger fires based on user intent (claude.ai detects the user is asking for a skill and injects the SKILL.md body into context). The stub body must itself instruct the model to: detect which skill is requested, load that skill's body from the cloned repo, and re-inject it.

UNCERTAIN: How the host determines which skill to activate. If the host uses the SKILL.md description field as a routing hint, the stub's description must be broad enough to match all skill requests. If the host requires an exact match, routing must happen INSIDE the stub's body after activation.

R5 — The stub's immutability (read-only mount) IS the primary trust boundary. Repo content can inject arbitrary instructions when loaded, but only after the stub activates. Invariants the stub MUST enforce regardless of repo content:
1. The stub MUST specify a version reference (branch name or SHA) that it trusts.
2. The stub MUST NOT follow redirects that attempt to load from a different repository.
3. The stub MUST surface any git error to the user rather than silently failing.

UNCERTAIN: Whether git commit signing or tag signing is feasible inside the claude.ai container.

**Confidence**: Medium (R1 mechanism), Low (trust enforcement feasibility in container)

---

## Track B: Sync Direction & Version Pinning (R2, R7)

**Goal**: Define the full read/write topology and the freshness/reproducibility policy.

**Findings**:

R2 — Topology confirmed via direct inspection:
- `/mnt/skills/user/` → READ ONLY (ephemeral per session; only writable by Michael via the container management interface, NOT by the running model)
- Repo `/skills/` → CANONICAL; writes via PR only
- `~/.claude/skills/` → CONSUMER; synced FROM repo via skills-skill-bootstrap (Stage B)
- Jules → UNKNOWN
- gemini-cli → UNKNOWN

Conflict model: there are NO concurrent writes because `/mnt/skills/user/` is read-only and `~/.claude/skills/` is written only by the sync tool. The repo is the single mutable source. No conflict resolution algorithm is needed in the current topology.

R7 — Version strategy decision: **pull-if-exists (shallow)** as default.
- Clone on first use to `~/.claude/skills-skill/repo/` (persistent across sessions if the container persists; ephemeral if not).
- Fetch `origin/main` at session start.
- If fetch fails: use cached clone with a visible staleness warning.
- SHA pinning: supported via `SKILLS_SKILL_PIN=<sha>` environment variable. When set, the stub checks out the pinned SHA instead of HEAD.

UNCERTAIN: Whether the claude.ai container's filesystem persists across sessions. If ephemeral, every session starts with a fresh clone (high latency). If persistent, pull-if-exists wins.

**Confidence**: High (topology), Medium (version strategy), Low (container persistence)

---

## Track C: Runtime Routing & Progressive Disclosure (R3, R4)

**Goal**: Define how skills-skill selects the right skill and delivers content progressively.

**Findings**:

R3 — Routing model: **two-tier**.
1. Host tier: claude.ai's native skill-trigger activates `skills-skill` when it determines the user intent matches the stub's description.
2. Stub tier: after activation, the stub reads the user's current message, scans available skill descriptions in `origin/main:skills/*/SKILL.md` (the frontmatter `description` field), and selects the best match.

The stub tier does NOT replace the host's trigger mechanism — it COMPLEMENTS it. The host handles "should a skill activate at all?" and the stub handles "which skill body to load?".

UNCERTAIN: Whether the host provides the user's original message to the stub, or only a pre-processed intent signal. This determines how fine-grained the stub's routing can be.

R4 — Progressive disclosure: **three-tier content ladder**.
- Tier 1 (always loaded): The first 200 chars of SKILL.md body (the "trigger description"). Size: ~200 chars.
- Tier 2 (on activation): Full SKILL.md body. Typical size: 1–5 KB.
- Tier 3 (on explicit request): `references/` content. Size: unlimited but agent-controlled.

State is tracked in-context per session (no persistent state assumption). The stub includes instructions: "If the user asks for more detail, load references/."

UNCERTAIN: Whether context window constraints in claude.ai require stricter size budgets per tier.

**Confidence**: Medium (routing model), High (disclosure ladder structure), Low (context budget details)

---

## Track D: Cross-Agent Portability (R6)

**Goal**: Determine how close a single SKILL.md can get to being loadable by all agents.

**Findings**:

Confirmed:
- claude.ai: `/mnt/skills/user/<name>/SKILL.md` (native)
- Claude Code: `~/.claude/skills/<name>/SKILL.md` (native, confirmed by direct inspection)
- Same format, no adapter needed for either.

Unknown:
- Jules: No binary or config found. Skill-loading convention unknown.
- gemini-cli: No binary or config found. Skill-loading convention unknown.

Architecture decision: design the canonical `/skills/skills-skill/SKILL.md` to be fully loadable by claude.ai and Claude Code without adapters. For Jules and gemini-cli, reserve adapter directories at `/skills/skills-skill/adapters/jules/` and `/skills/skills-skill/adapters/gemini-cli/` — to be populated once R6 is resolved by the follow-up research prompts.

**Confidence**: High (claude.ai + Claude Code), None (Jules, gemini-cli)
