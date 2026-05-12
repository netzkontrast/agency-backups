---
type: note
status: active
slug: skills-skill-container-capabilities-m13
summary: "M13 Evidence Quality assessment for skills-skill-container-capabilities findings."
created: 2026-05-04
updated: 2026-05-04
---

# M13 — Evidence Quality Assessment

Evidence tiers:
- **(a) Anthropic-official** — Direct Anthropic documentation or announcement
- **(b) Community-confirmed** — Multiple independent sources converge
- **(c) Single-source anecdote** — One developer report or forum post
- **(d) Inference** — Logical deduction from related facts, no direct evidence

Findings rated (c) or (d) require verification before being used in normative architectural language.

## Findings Table

| Claim | Source | Tier | Action Required |
|---|---|---|---|
| Skills run via code execution tool with bash access | Anthropic Engineering Blog (Equipping agents for the real world) | (a) | None — use as normative |
| SKILL.md injects text; Claude executes bash via sub-tool | Anthropic Engineering Blog | (a) | None — use as normative |
| claude.ai Free/Pro/Max has "varying" network (GitHub reachable) | Agent Skills overview, "Runtime environment constraints" | (a) | None — use as normative |
| claude.ai Team/Enterprise network disabled by default | Agent Skills overview | (a) | None — use as normative |
| Claude API has no network access | Agent Skills overview | (a) | None — use as normative |
| Claude Code has full network access (host OS) | Agent Skills overview | (a) | None — use as normative |
| claude.ai Skills "can pull from GitHub repositories" | Agent Skills best-practices, "Package dependencies" | (a) | Ambiguous phrasing — see note |
| Pre-installed utilities list (unzip, rg, fd, sqlite…) — git absent | Code execution tool docs, pre-installed packages | (a) for list; (d) for git-absent inference | Verify empirically (file `claude-ai-container-git-verification`) |
| Container expires 30 days after creation | Code execution tool docs | (a) | None — use as normative |
| Container reuse requires explicit container ID | Code execution tool docs | (a) | None — use as normative |
| claude.ai web sessions do NOT auto-reuse containers | Inferred: no documented mechanism + GitHub issue #28307 closed as dup | (d) | Verify empirically or await Anthropic docs update |
| Python `requests` library is pre-installed | Pre-installed list includes standard data science stack; `requests` is a near-universal dep | (d) | Verify empirically; fall back to `urllib.request` (stdlib) |
| GitHub MCP server is NOT a default connector | No Anthropic doc lists it as default; requires manual setup | (b) community-confirmed | None |
| Container: 5 GiB RAM, 5 GiB storage, 1 CPU | Code execution tool docs | (a) | None — use as normative |
| Data retained up to 30 days | Code execution tool docs | (a) | None — use as normative |

## Notes on Ambiguous Findings

### "Can pull from GitHub repositories"

The best-practices page uses this phrase under "Package dependencies" in the context of package installation (npm, PyPI, GitHub). Most naturally read, it means `pip install git+https://github.com/…` (which works even without git if using the zip URL). It does NOT confirm git is a binary in PATH. **Do not use this phrase as evidence of git availability.**

### Python `requests` availability

The code execution tool docs list named packages: pandas, numpy, scipy, matplotlib, PIL, pdfplumber, etc. `requests` is not explicitly named but is a transitive dependency of many listed packages and is nearly universally present in data science environments. For maximum portability, SKILL.md implementations should fall back to `urllib.request` (stdlib, always available) if `requests` import fails.
