---
type: index
status: active
slug: decisions-root
summary: "Architectural Decision Records (ADRs) — repo-native MADR 4.0.0 ledger validated by tools/adr/cli.py."
created: 2026-05-06
updated: 2026-05-12
---

# Decisions

**What is this folder?** The append-only ledger of Architectural Decision Records that bind every agent in this repo. The governance contract lives at [`../research/adr-spec-research-synthesis/output/SPEC.md`](../research/adr-spec-research-synthesis/output/SPEC.md); the validator and synthesis pipeline live at [`../tools/adr/`](../tools/adr/).

**Why is it here?** ADRs are the only mechanism for changing repo-level architectural conventions (storage paths, frontmatter schemas, hook integration, branching). Every accepted ADR contributes to the synthesised guarded section of [`../AGENTS.md`](../AGENTS.md) on the next `python3 tools/adr/cli.py synthesize` run.

## Authoring an ADR

1. Pick the next zero-padded integer (`0001`, `0002`, …) by inspecting filenames here.
2. Author `decisions/<NNNN>-<slug>.md` with the canonical MADR sections (`Context and Problem Statement`, `Decision Drivers`, `Considered Options`, `Decision Outcome`, `Consequences`).
3. Frontmatter MUST carry `type: adr`, `adr_id: ADR-<NNNN>`, `adr_status: Proposed | Accepted | Superseded | Deprecated`, plus standard L1 keys. The `summary` field is capped at **240 characters** (per [`maintenance/schemas/l2-adr.schema.json`](../maintenance/schemas/l2-adr.schema.json)) — keep it short or `tools/adr/cli.py validate` will reject it with `ERROR:ADR.A.2.2`.
4. Run `python3 tools/adr/cli.py validate` and fix any diagnostics.
5. When the ADR's status flips to `Accepted`, run `python3 tools/adr/cli.py synthesize` so the AGENTS.md guarded section reflects it.
6. Commit and open a PR per the four-step closing procedure in [AGENTS.md § Closing Run Procedure](../AGENTS.md#closing-run-procedure) (Claude Code: `/sc:createPR`; Jules: native primitive; Gemini: deferred to integration Task).

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
- [`0006-agency-system-prototype-exemption.md`](./0006-agency-system-prototype-exemption.md) — `/Agency-System/` frontend-prototype exemption from FOLDERS.md §1 operational-folder rules and §7 audit graph. `adr_status: Accepted`.
- [`0007-skill-bundles-tools-frontmatter.md`](./0007-skill-bundles-tools-frontmatter.md) — `skill_bundles_tools` frontmatter key for skills that sync repo tools into `~/.claude/skills/`. `adr_status: Accepted`.
- [`0008-narrative-skills-status-quo.md`](./0008-narrative-skills-status-quo.md) — Narrative skills (6 folders + ontology + dramatica-nav) stay in this repo; the NO.5 don't-load rule + WARN linter remain the partition mechanism. `adr_status: Proposed`. Ships with five falsifier triggers (skill count > 10, bundle token cost > 60K, sustained NO.5-cited friction, narrative T3 amendment of non-AGENTS root spec, third-party-adopter blocker).
- [`0009-root-spec-no-consolidation.md`](./0009-root-spec-no-consolidation.md) — Measured 11-spec bootstrap bundle (~70,676 tokens) stays intact; PRE_COMMIT.md does not merge into AGENTS.md, FRUSTRATED.md does not merge into MAINTENANCE.md. Saving (~1%) below migration threshold (381 cross-references; in-flight Task disruption). `adr_status: Proposed`. Ships with three falsifier triggers (bundle > 100K tokens, either spec < 1000 tokens + < 50 dependents, sustained bundle-size-cited friction).
- [`0010-external-skill-corpora-import.md`](./0010-external-skill-corpora-import.md) — External skill corpora (SuperClaude v4.3.0, Superpowers v4.0.3) import under vendor-prefixed namespaces (`sc-*`, `superpowers-*`) with new L2 frontmatter key `skill_source`. Closes the five dangling `/sc:*` references in CLAUDE.md §13 and AGENTS.md Closing Run Procedure once the follow-up corpus Task lands. `adr_status: Proposed`. Ships with three falsifier triggers (third corpus, force-push tag drift, native↔import name collision).
