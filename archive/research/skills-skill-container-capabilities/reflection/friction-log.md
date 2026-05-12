---
type: note
status: active
slug: skills-skill-container-capabilities-friction-log
summary: "Friction log for skills-skill-container-capabilities research run. Highest friction: FL1."
created: 2026-05-04
updated: 2026-05-04
---

# Friction Log

**Highest friction level experienced: FL1**

## FL1 — Non-Trivial Friction

The research encountered one significant epistemic gap: the official Anthropic documentation does not explicitly state whether `git` is present or absent as a pre-installed binary in the claude.ai code execution container. The pre-installed utility list (from the code execution tool docs) enumerates specific tools (unzip, rg, fd, sqlite, etc.) and **omits git** — but does not say "git is not installed." This creates an absence-of-evidence situation.

### Friction Detail

**Friction point**: U1 (git availability) cannot be definitively confirmed as absent — only inferred from omission in the official list. The phrase "can pull from GitHub repositories" in the best-practices page is ambiguous: it could mean git-based pull, pip-from-GitHub, or REST API fetching.

**Resolution**: Rated as evidence level (d) — inference from official list omission. The architectural decision (use REST API, do not rely on git) is the conservative correct choice regardless of the truth. The follow-up question `claude-ai-container-git-verification` has been filed to resolve this empirically.

**No blockers**: The research was completable. All findings are grounded in official Anthropic documentation. The REST API alternative is well-specified and production-ready.

## FL0 Items (no friction)

- U2 (filesystem persistence) was well-documented: container lifetime (30 days), no auto-reuse in web UI, confirmed by GitHub issue evidence.
- Network access model (by plan) was documented precisely in the official Skills overview.
- Alternative bootstrap mechanisms (REST API, ZIP download) are standard and well-understood patterns.
