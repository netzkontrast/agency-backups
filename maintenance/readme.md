---
type: index
status: active
slug: maintenance
summary: "Central maintenance and governance support folder. Holds canonical definitions that all agents and specs in this repository depend on."
created: 2026-05-04
updated: 2026-05-04
---

# Maintenance

**What:** This folder is the governance support centre for the repository. It holds canonical, complete definitions that are referenced by root governance specs (`AGENTS.md`, `TASK.md`, `PROMPT.md`, `RESEARCH.md`) but are too detailed to inline without bloating those files.

**Why:** Keeping canonical definitions in one place prevents divergence. When a rule in a governance spec conflicts with a definition here, this folder wins — the root files are summaries and shortcuts, not sources of truth.

## Navigation

- [language-spec.md](./language-spec.md) — **Canonical** RFC 2119 keyword definitions, Gherkin syntax binding, and the complete Frontmatter Ontology (L0–L3). Every agent in this repo MUST conform to this document.

## Relationship to Root Governance Specs

| Root spec | Summarises from here |
|---|---|
| `AGENTS.md §Spec Language Reference` | `language-spec.md §2–§3` (RFC 2119 + Gherkin) |
| `AGENTS.md §Frontmatter Ontology` | `language-spec.md §4` (Layered Schema) |
| `TASK.md §3` | `language-spec.md §4.4` (L2 namespaces) |

## Assumptions Log

- The `maintenance/` folder is intentionally outside the three operational directories (`/tasks/`, `/prompts/`, `/research/`). It is a governance support folder, not a work-execution folder. This matches the FOLDERS.md §7 intent that operational and governance concerns stay separated.
- The `MAINTENANCE.md` file at the repository root governs the *process* of maintenance runs; this folder holds the *content* (canonical definitions) that those runs depend on.
