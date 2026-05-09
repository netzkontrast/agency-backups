---
type: note
status: active
slug: maintenance-spec-session-insights-2026-05-09-brief
summary: "Human-readable orientation for the prompt that rolls 2026-05-09 maintenance-run insights into MAINTENANCE.md."
created: 2026-05-09
updated: 2026-05-09
---

# Brief — Roll 2026-05-09 maintenance-run session insights into MAINTENANCE.md

## What this prompt asks an agent to do

Amend `MAINTENANCE.md` so the next agent that runs both the Coherence Check (§2) and the Nightly Maintenance Run (§3) in a single session does not hit the five ambiguities recorded by the 2026-05-09 session:

1. **Delta vs. aggregator scope** — the Coherence Check is delta-only, but `tools/maintenance/trust-audit.py` always scans every research workspace. The spec doesn't say how the agent reconciles "scan the delta only" with "report aggregator findings".
2. **WARN-tier dedup policy** — the trust-audit aggregator emitted 13 `recommend-task` lines on 2026-05-09 for FL≥1 workspaces that were already covered. The spec doesn't tell the agent how to skip pre-existing coverage.
3. **MAINT_STALE_DAYS gate-skipped reporting** — the staleness audit silently treats "every Task is too young to audit" as "0 flagged", which conflates "no drift" with "audit-window-skip".
4. **`/sc:*` skill bindings** — `/sc:analyze`, `/sc:reflect`, `/sc:improve`, `/sc:review`, `/sc:createPR` are useful around the maintenance routines but are not referenced from the spec or the prompt.
5. **Root-spec frontmatter exemption** — `README.md` has no L1 frontmatter; the gate accepts this silently. The spec must say whether root files are exempt, and if not, the linter must emit a diagnostic.

## Why it matters

The 2026-05-09 session was the first time both routines ran together with `/sc:*` skills as bookends. Each gap above forced the executing agent to make a judgement call without spec backing. Without these amendments the next combined run will reproduce the same friction.

## What success looks like

- `MAINTENANCE.md` carries five new normative paragraphs (one per gap) and five paired Gherkin scenarios under `M.B.8` through `M.B.12`.
- `tools/maintenance/staleness-audit.py` emits the gate-skipped count as a canonical diagnostic.
- `tools/check-governance.sh` exits 0 against the amended state.
- The closing run-log entry uses `routine_type: task-implementation` and references this Task's slug.

## Out of scope

- Introducing new aggregator linters (the scope is documenting what already exists).
- Mutating any `decisions/<NNNN>-<slug>.md` file with `adr_status: Accepted`.
- Refactoring `prompts/repo-coherence-check/prompt.md` beyond a one-line cross-reference to the amended spec sections.
