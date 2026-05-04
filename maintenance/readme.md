---
type: index
status: active
slug: maintenance
summary: "Central maintenance and governance support folder. Holds canonical definitions, the run log for the Repo Coherence Check routine, and references to the routines that keep this repo coherent."
created: 2026-05-04
updated: 2026-05-04
---

# Maintenance

**What:** This folder is the governance support centre for the repository. It holds two things:

1. **Canonical definitions** — the language spec and frontmatter ontology that all agents and specs depend on, too detailed to inline in root governance files without bloating them.
2. **Execution state** — the run log for the Repo Coherence Check routine, which records the git-commit baseline for each run so the next run knows where to start.

**Why:** Keeping canonical definitions and routine state in one place prevents divergence. When a rule in a governance spec conflicts with a definition here, **this folder wins** — the root files are summaries and shortcuts, not sources of truth.

---

## Navigation

- [language-spec.md](./language-spec.md) — **Canonical** RFC 2119 keyword definitions, Gherkin syntax binding, and the complete Frontmatter Ontology (L0–L3). Every agent MUST conform to this document. All other specs summarise from here.
- [run-log.md](./run-log.md) — Chronological log of every Repo Coherence Check and Nightly Maintenance run. **The agent MUST read the last `end_commit` entry before beginning any coherence-check run.**

---

## The Repo Coherence Check Routine

The coherence-check prompt lives at [`/prompts/repo-coherence-check/prompt.md`](../prompts/repo-coherence-check/prompt.md). It is a **recurring self-improvement routine**, not a one-shot research task:

- Reads `run-log.md` to find its starting commit.
- Scans only files changed since that commit (delta-aware).
- Applies T1/T2 repairs immediately; writes Tasks for T3 findings.
- Appends a new record to `run-log.md` before committing.

It SHOULD be wired as a Claude Code `SessionStart` hook or run manually before opening any new Task. See `prompt.md §Wiring as a Claude Code Routine`.

---

## Relationship to Root Governance Specs

| Root spec | Summarises from here |
|---|---|
| `AGENTS.md §Spec Language Reference` | `language-spec.md §2–§3` (RFC 2119 + Gherkin) |
| `AGENTS.md §Frontmatter Ontology` | `language-spec.md §4` (Layered Schema) |
| `TASK.md §3` | `language-spec.md §4.4` (L2 namespaces) |
| `MAINTENANCE.md §2` | `run-log.md` (execution state) |

---

## Assumptions Log

- The `maintenance/` folder is intentionally outside the three operational directories (`/tasks/`, `/prompts/`, `/research/`). It is a governance support folder, not a work-execution folder, consistent with `FOLDERS.md §7`.
- The `MAINTENANCE.md` file at the repository root governs the *process* (repair tiers, routine scope, delegation rules); this folder holds the *content* (canonical definitions) and *state* (run log) that those processes depend on.
- `run-log.md` was bootstrapped on 2026-05-04 at commit `f620b6d`. All future coherence checks use that as their minimum baseline.
