---
type: note
status: active
slug: task-092-st1-triage
summary: "ST-1 (Task 092 Epic): triage every snapshot artefact under tasks/091-…/references/upstream-snapshot/ via /sc:research + /sc:analyze (local-only) and produce a port/adapt/skip decision matrix at references/triage-matrix.md."
created: 2026-05-12
updated: 2026-05-12
---

# ST-1 — Triage

**Executor:** main-agent invoking [`/sc:research`](../../../skills/sc-research/SKILL.md) and `/sc:analyze` over local paths. **No external GitHub fetches** — see [Task 092 Note](../task.md#note--internal-research-only).

**Parallelism:** Sequential — ST-2 and ST-3 depend on this matrix. ST-1 itself MAY parallelise its per-skill reads using subagents, but the final matrix is a single artifact.

**Depends on:** Task 091 ST-1 ([PR #115](https://github.com/netzkontrast/agency/pull/115)) merged to `main` so the snapshot path is on `main`; no other dependencies.

## Scope

- **Inventory.** Enumerate every `*.md` (and notable non-md skill scaffolding: `SKILL.md`-equivalents inside skill subdirs, MODE files, plugin manifests) under [`tasks/091-…/references/upstream-snapshot/`](../../091-port-external-skill-corpora/references/upstream-snapshot/). Expected count: **~75 candidate skills** + supporting modes/hooks/lib/docs/manifest files. Exclude items already ported by Task 091 ST-1 (the 14 sc-* skills + MODE_Orchestration + MODE_DeepResearch).
- **Triage per artefact.** For each candidate, decide one of three outcomes:
  1. **`port`** — verbatim or near-verbatim mirror is suitable; body fits 5 KB; no MCP-binding adaptation needed.
  2. **`adapt`** — body requires ADR-0011 D.8 rewrite (binds to Tavily / Serena / Morphllm / Magic / Chrome-DevTools / etc), or D.6 overflow (> 5 KB body) requires references/ extraction, or a SessionStart-injection clause needs stripping (D.7).
  3. **`skip`** — capability already covered by an Agency-native skill, a root spec, or another in-flight Task; or upstream skill's value-add is marginal; or licensing/scope concerns.
- **Decision matrix.** Single canonical artifact at [`../references/triage-matrix.md`](../references/triage-matrix.md). One row per candidate. Schema:

  ```markdown
  | # | Snapshot path (relative to snapshot root) | Proposed Agency slug | Tier (L1–L4) | Decision | ADR-0011 clauses | Rationale (≤ 1 line) |
  ```

  Order rows by vendor (SuperClaude first, then Superpowers), then by tier (L1 leaves first, then up).

- **Per-skill research notes.** When a `port` or `adapt` row needs more than one line of rationale, append a per-skill note under [`../references/triage-notes/<vendor>-<slug>.md`](../references/) (subfolder auto-created). Keep each note ≤ 1 KB.

## Out of scope

- Any `/skills/` write. ST-1 is purely a reading + decision-recording exercise.
- Re-evaluating Task 091 ST-1's already-ported 14 skills — those are settled.
- Porting decisions for **future upstream releases**; ADR-0011 D.9 pins the snapshot.

## How to use `/sc:research` (local-only)

1. Set the target explicitly: `/sc:research --target tasks/091-port-external-skill-corpora/references/upstream-snapshot/<vendor>/<subtree>/`.
2. The agency-adapted body of `/sc:research` ([`skills/sc-research/SKILL.md`](../../../skills/sc-research/SKILL.md)) defaults to WebSearch + WebFetch; for this Epic, override that step — do NOT invoke either tool. Use `Read` / `Glob` / `Grep` directly against the snapshot path.
3. Deliverable for each researched skill: a single `## Findings` paragraph in the triage matrix row (or a longer note under `triage-notes/` if needed).

## How to use `/sc:analyze` (local-only)

1. `/sc:analyze tasks/091-…/references/upstream-snapshot/<vendor>/<subtree>/<file> --focus quality|security|performance|architecture --depth quick|deep`.
2. Use to score the *adaptability* of a candidate — quality + architecture analyses are most useful for porting decisions.

## Acceptance Criteria (Gherkin)

```gherkin
Feature: ST-1 produces a complete, locally-sourced triage matrix

  # anchor: T092.1.1
  Scenario: Every snapshot candidate has a matrix row
    Given ST-1 is complete
    When a reader greps the triage matrix
    Then every *.md file under tasks/091-…/references/upstream-snapshot/ MUST have a row
        (excluding files already ported by Task 091 ST-1)
    And every row MUST carry a decision ∈ {port, adapt, skip}

  # anchor: T092.1.2
  Scenario: ADR-0011 D.8 cases flagged
    Given a row's "Decision" column = "adapt"
    When the reader inspects the row's "ADR-0011 clauses" column
    Then it MUST cite at least one of D.6 (body cap), D.7 (no SessionStart), D.8 (MCP-free)

  # anchor: T092.1.3
  Scenario: No external citations
    Given the triage matrix is committed
    When a reader greps the matrix and any triage-notes/ file for "https://github.com"
    Then the grep MUST return zero matches
        (research was local-only per Task 092 Note)

  # anchor: T092.1.4
  Scenario: Matrix sums to the expected candidate count
    Given ST-1 is complete
    When the reader counts {port + adapt + skip} rows
    Then the sum MUST be ≥ 75 (the inventory floor; matches snapshot inventory)
        And the count of "port"+"adapt" rows MUST be ≥ 1 (this Epic's existence requires it)
```

## Branch + PR shape

Author on a fresh branch derived from `main` post-merge of Task 091 ST-1. PR title MUST cite this subtask, e.g. `Task 092 ST-1: Phase 2 triage matrix (75 candidates)`. PR body MUST include:

- The matrix file rendered (or linked + summary table of counts: `port=N, adapt=M, skip=K`).
- Confirmation grep output for T092.1.3 (zero `https://github.com` citations in matrix or notes).
- Friction-log declaration (FL0–FL3) per `FRUSTRATED.md`.
