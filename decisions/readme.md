---
type: index
status: active
slug: decisions-root
summary: "Architectural Decision Records (ADRs) — repo-native MADR 4.0.0 ledger validated by tools/adr/cli.py."
created: 2026-05-06
updated: 2026-05-07
---

# Decisions

**What is this folder?** The append-only ledger of Architectural Decision Records that bind every agent in this repo. The governance contract lives at [`../research/adr-spec-research-synthesis/output/SPEC.md`](../research/adr-spec-research-synthesis/output/SPEC.md); the validator and synthesis pipeline live at [`../tools/adr/`](../tools/adr/).

**Why is it here?** ADRs are the only mechanism for changing repo-level architectural conventions (storage paths, frontmatter schemas, hook integration, branching). Every accepted ADR contributes to the synthesised guarded section of [`../AGENTS.md`](../AGENTS.md) on the next `python3 tools/adr/cli.py synthesize` run.

## Authoring an ADR

1. Pick the next zero-padded integer (`0001`, `0002`, …) by inspecting filenames here.
2. Author `decisions/<NNNN>-<slug>.md` with the canonical MADR sections (`Context and Problem Statement`, `Decision Drivers`, `Considered Options`, `Decision Outcome`, `Consequences`).
3. Frontmatter MUST carry `type: adr`, `adr_id: ADR-<NNNN>`, `adr_status: Proposed | Accepted | Superseded | Deprecated`, plus standard L1 keys.
4. Run `python3 tools/adr/cli.py validate` and fix any diagnostics.
5. When the ADR's status flips to `Accepted`, run `python3 tools/adr/cli.py synthesize` so the AGENTS.md guarded section reflects it.
6. Commit and open a PR via `/sc:createPR`.

## Lifecycle

- **Proposed** — drafted but not yet binding; excluded from synthesis.
- **Accepted** — binding; contributes to synthesis. T4-immutable per [`../MAINTENANCE.md`](../MAINTENANCE.md) §1; alterations land via a successor ADR that names this `adr_id` in `adr_supersedes`.
- **Superseded** — replaced by a successor; excluded from synthesis.
- **Deprecated** — withdrawn without a direct successor; excluded from synthesis.

## Index

The first batch landed via [Task 032 ST-1](../tasks/032-agents-spec-integration/subtasks/01-research-adr-corpus-extraction.md) — the 5 P1 IADRs from [`research/adr-corpus-extraction-from-governance-specs/output/SPEC.md`](../research/adr-corpus-extraction-from-governance-specs/output/SPEC.md). All five are at `adr_status: Proposed` and are therefore excluded from the AGENTS.md synthesis block until a maintainer flips them to `Accepted`.

- [`0001-mandatory-session-bootstrap.md`](./0001-mandatory-session-bootstrap.md) — Session bootstrap and governance gate (AGENTS.md `SS.1`–`SS.3`). `adr_status: Proposed`.
- [`0002-operational-folder-topology.md`](./0002-operational-folder-topology.md) — Top-level folder partition and `/decisions/` exemption protocol (FOLDERS.md §1, §8). `adr_status: Proposed`.
- [`0003-frontmatter-source-of-truth.md`](./0003-frontmatter-source-of-truth.md) — Frontmatter as the single source of truth for the audit graph (FOLDERS.md §3; TASK.md §3). `adr_status: Proposed`.
- [`0004-yaml-depth-one-constraint.md`](./0004-yaml-depth-one-constraint.md) — YAML nesting depth ≤ 1 anti-hallucination rule (AGENTS.md §"YAML Depth Rule"; `tools/fm/_core.py`). `adr_status: Proposed`.
- [`0005-repair-authority-tiers.md`](./0005-repair-authority-tiers.md) — Repair authority tiers and mutation surface boundaries (MAINTENANCE.md §1). `adr_status: Proposed`.
