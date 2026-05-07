---
type: adr
status: draft
slug: 0002-operational-folder-topology
summary: "Top-level tree partitions into operational quartet (/tasks/, /prompts/, /research/, /skills/) plus a named exemption set (/tools/, /maintenance/, /decisions/, /templates/, /Agency-System/). New top-level folders MUST land via FOLDERS.md §8."
created: 2026-05-07
updated: 2026-05-07
adr_id: ADR-0002
adr_status: Proposed
adr_owner: agency-maintainer
adr_tags:
  - folder-topology
  - separation-of-concerns
  - audit-graph
---

# ADR-0002 — Operational Folder Topology and Exemption Protocol

## Context and Problem Statement

Without a hard partition between orchestration (`/tasks/`), instruction (`/prompts/`), evidence (`/research/`), and capability (`/skills/`), folders mix kinds and the audit graph becomes unwalkable. Non-operational stores (`/tools/`, `/maintenance/`, `/decisions/`, `/templates/`, `/Agency-System/`) need first-class status without polluting the operational partition; otherwise mechanical lints either over-walk (false positives in tooling code) or under-walk (missing legitimate orchestration content).

The rule is currently declared at [`FOLDERS.md:18-23`](../FOLDERS.md) (top-level table) and [`FOLDERS.md:105-122`](../FOLDERS.md) (anti-pattern list + §8 exemption table) but has never been ratified as an ADR. This ADR formalises the partition so additions land via the supersession DAG.

## Decision Drivers

- **Mechanical enforcement.** Closed-list path globs in `tools/lint-structure.py` and `tools/lint-linkage.py` need a stable, declarative partition.
- **Audit-graph traversal.** The Task → Prompt → Research → Prompt edge graph only walks if the operational quartet is the closed traversal universe.
- **First-class non-operational stores.** Storage classes like ADRs and skills need a sanctioned home that is *not* swept by orchestration lints.

## Considered Options

1. **Free-form folders + per-file frontmatter routing.** Rejected: no static ground truth; lints would have to walk the entire tree and infer scope from frontmatter, doubling cost.
2. **Closed operational partition + named exemptions (chosen).** Four operational folders are the universe; all other top-level folders must appear in `FOLDERS.md §8` with explicit exemption scope.
3. **Single monolithic `/repo/` tree.** Rejected: regresses to undifferentiated content; loses the audit-graph entirely.

## Decision Outcome

The repository's top-level tree is partitioned into the operational quartet (`/tasks/`, `/prompts/`, `/research/`, `/skills/`) and a named exemption set (`/tools/`, `/maintenance/`, `/decisions/`, `/templates/`, `/Agency-System/`); any new top-level folder MUST land via amendment to `FOLDERS.md §8` declaring its exemption scope, and `tools/validate-frontmatter.py` enforces the partition mechanically.

## Consequences

- **Positive.** Lint tooling can hard-code path globs without walking the entire tree. Audit-graph traversal is closed. Non-operational stores are unambiguous about what discipline applies.
- **Negative.** Every new storage class requires a documentation edit to `FOLDERS.md §8`. The list grows monotonically, and pruning a class (deprecation) is a T3 change that demands a successor ADR.
- **Neutral.** This is the structural backbone every other ADR in this corpus composes against; ADR-0010 (`/decisions/` storage path, declared in the ratified SPEC §2.1) inherits its exemption-table row from this ADR.
