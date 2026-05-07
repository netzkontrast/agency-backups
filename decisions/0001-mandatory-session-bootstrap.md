---
type: adr
status: draft
slug: 0001-mandatory-session-bootstrap
summary: "Every agent session MUST begin with ./install.sh then tools/check-governance.sh; non-zero exit halts the session before any read or write. Formalises AGENTS.md SS.1-SS.3."
created: 2026-05-07
updated: 2026-05-07
adr_id: ADR-0001
adr_status: Proposed
adr_owner: agency-maintainer
adr_tags:
  - bootstrap
  - governance-gate
  - session-lifecycle
---

# ADR-0001 — Mandatory Session Bootstrap and Governance Gate

## Context and Problem Statement

An agent that begins a session in a half-installed environment will silently produce broken artefacts: missing `PyYAML` makes the validators no-op, stale schemas mask drift, and an unrun `tools/check-governance.sh` lets pre-existing errors compound across the session's commits. The repository declares the bootstrap and governance-gate rule in [`AGENTS.md:38-42`](../AGENTS.md) as SS.1, SS.2, and SS.3, but the rule has never been ratified as an ADR — it lives only as a clause in a root spec and inherits no `adr_supersedes` lineage, so successor decisions have no formal predecessor to cite.

This ADR formalises that long-standing practice as a binding architectural decision so future amendments land via the supersession DAG rather than as silent edits to `AGENTS.md`.

## Decision Drivers

- **Idempotency cost vs broken-tooling cost.** Rerunning `install.sh` adds ≈ 1–2 s to a fresh shell; debugging a session that produced bad artefacts because tooling was missing costs hours.
- **Compound drift.** A failing `check-governance.sh` indicates pre-existing errors; starting work on top of them entangles the new work with the old defect, making the eventual fix more expensive.
- **Anchor for future ADRs.** Every ADR that depends on `tools/check-governance.sh` (the ADR validator itself, the narrative-ontology check, the trust audit) needs a stable predecessor declaring "the gate exists and runs first".

## Considered Options

1. **Bootstrap-on-demand (lazy).** Each tool installs its own dependencies the first time it runs. Rejected: leaves windows where reads precede installs; produces non-deterministic timing for friction logs.
2. **Mandatory `install.sh` + `tools/check-governance.sh` at session start (chosen).** A hard, idempotent, documented two-step that every agent runs before reading or writing any file.
3. **CI-only enforcement.** Move the gate entirely into a GitHub Action. Rejected: agents act outside CI (interactive sessions, web edits, sandboxed runs); CI catches the failure too late to prevent in-session drift.

## Decision Outcome

Every agent MUST run `./install.sh` and then `tools/check-governance.sh` as the first two actions of every session, before reading or writing any repository file; a non-zero exit from either MUST halt the session and be reported to the user, with no further file mutations until the gate passes.

## Consequences

- **Positive.** Tooling-environment defects surface in seconds, not after broken commits. The gate is the canonical anchor for every downstream governance check (frontmatter validators, narrative ontology, ADR validator). Idempotency means the cost is bounded.
- **Negative.** Adds ≈ 1–2 s to every fresh shell; agents using one-shot invocations must remember the rule even for "trivial" reads.
- **Neutral.** This is the bootstrap baseline every other ADR in this corpus may assume. Successor ADRs that change the gate composition (e.g. adding a new numbered step in `tools/check-governance.sh`) MUST cite ADR-0001 in `adr_supersedes` only if the change *removes* SS.1–SS.3; additive changes (new numbered steps) compose without supersession.
