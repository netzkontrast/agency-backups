---
type: adr
status: active
slug: 0011-codex-entrypoint-and-platform-note
summary: "Record Codex runtime onboarding via CODEX.md and Codex platform implementation note in AGENTS.md Closing Run Procedure section."
created: 2026-05-12
updated: 2026-05-12
adr_id: ADR-0011
adr_status: Proposed
adr_deciders:
  - codex
adr_consulted: []
adr_informed: []
adr_supersedes: []
---

# ADR-0011: Codex entrypoint and closing-procedure implementation note

## Context and Problem Statement

The repository added Codex runtime support by introducing `CODEX.md` and a Codex subsection under `AGENTS.md` platform implementation notes. Governance review identified missing ADR traceability for this architectural addition.

## Decision Drivers

- Cross-platform closing procedure consistency.
- Root-spec entrypoint parity for supported runtimes.
- Auditability of architecture-level governance changes.

## Considered Options

- Option 1: Keep Codex additions without ADR coverage.
- Option 2: Add a dedicated ADR documenting Codex entrypoint and platform note semantics.

## Decision Outcome

Chosen option: **Option 2**.

The repository keeps `CODEX.md` as a root runtime entrypoint and keeps a Codex platform implementation note in `AGENTS.md` that names the runtime PR primitive (`make_pr`) and CR.5/CR.6 obligations.

## Consequences

- Positive: architecture-level provenance is explicit and reviewable.
- Positive: Codex onboarding semantics become durable via ADR ledger.
- Neutral: future Codex behavior changes now require ADR update/supersession rather than ad-hoc edits.
