---
type: adr
status: active
slug: 0011-archive-move-default
summary: "Set move-based archival as default and define canonical /archive/* destinations for closed task/prompt/research artifacts."
created: 2026-05-12
updated: 2026-05-12
adr_id: ADR-0011
adr_status: Proposed
adr_owner: agency-maintainer
adr_tags:
  - archive
  - governance
  - lifecycle
  - maintenance
---

# ADR-0011 — Move-Based Archival Default

## Context and Problem Statement

The repository owner wants closed artifacts to disappear from active work roots (`/tasks`, `/prompts`, `/research`) so those surfaces stay operationally clean. The prior index-only archival approach left closed artifacts in-place and did not satisfy that operational intent.

## Decision Drivers

- Keep active directories focused on current work.
- Preserve full Git provenance.
- Provide canonical archive destinations for deterministic automation.

## Considered Options

### Option 1 — Index-only archival

Mark files as archived in frontmatter while keeping folders in-place.

### Option 2 — Move-based archival (chosen)

Move closed artifact folders into `/archive/tasks`, `/archive/prompts`, and `/archive/research`.

## Decision Outcome

Choose **Option 2**. Closed artifacts are archived via `git mv` into canonical archive paths.

## Consequences

- Active roots are cleaner and signal in-progress work.
- Links and cross-references may require follow-up normalization where absolute relative paths assumed old roots.
- Tooling that scans only active roots naturally excludes archived corpus.
