---
type: index
status: active
slug: decisions-root
summary: "Architectural Decision Records (ADRs) — repo-native MADR 4.0.0 ledger validated by tools/adr/cli.py."
created: 2026-05-06
updated: 2026-05-06
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

_(empty — no ADRs authored yet. The first batch is sequenced by `tasks/029-adr-assumption-audit/` PD-005 and the implementation Task that succeeds Task 028.)_
