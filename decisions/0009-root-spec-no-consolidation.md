---
type: adr
status: active
slug: 0009-root-spec-no-consolidation
summary: "11-spec root bundle stays as-is. Merging PRE_COMMIT/FRUSTRATED into AGENTS/MAINTENANCE saves ~1% tokens but costs 381 cross-ref rewrites + dilutes single-concern clarity. Deferred behind three falsifier triggers."
created: 2026-05-11
updated: 2026-05-11
adr_id: ADR-0009
adr_status: Proposed
adr_owner: agency-maintainer
adr_tags:
  - root-specs
  - bundle-size
  - token-cost
  - folder-topology
---

# ADR-0009 — Root-Spec Bundle Stays As-Is (No PRE_COMMIT / FRUSTRATED Merge)

## Context and Problem Statement

Every agent session reads a bundle of root governance specs at boot. [`README.md §10`](../README.md) describes the bundle as "9+ root specs"; the measured reality (2026-05-11) is **11 files** totalling **~70,676 tokens**:

| File | Lines | Tokens (~) |
|---|---:|---:|
| `AGENTS.md` | 517 | 10,274 |
| `TASK.md` | 458 | 9,909 |
| `PROMPT.md` | 245 | 4,255 |
| `RESEARCH.md` | 289 | 5,169 |
| `FOLDERS.md` | 194 | 4,027 |
| `PRE_COMMIT.md` | 257 | 5,455 |
| `FRUSTRATED.md` | 119 | 2,164 |
| `MAINTENANCE.md` | 471 | 12,022 |
| `SKILLS.md` | 276 | 4,853 |
| `README.md` | 343 | 8,830 |
| `maintenance/language-spec.md` | 317 | 3,713 |
| **Bundle total** | **3,486** | **~70,676** |

[Task 057](../tasks/057-root-spec-consolidation-adr/) (dispatched from [Task 053](../tasks/053-core-architecture-review-followups/) finding B.6) evaluates two specific consolidations to reduce this bundle:

- **M1.** Merge `PRE_COMMIT.md` (5,455 tokens) → `AGENTS.md` as a new `## Pre-Commit Gate` section.
- **M2.** Merge `FRUSTRATED.md` (2,164 tokens) → `MAINTENANCE.md` as a new `## Friction Logging` section.

The falsifiable outcome of Task 057 is a ratified ADR recording one of {both-merges, partial-merge, status-quo} with measured token-cost data backing the choice.

## Decision Drivers

### Measured token-cost saving from the proposed merges

The merge does **not** delete content; it relocates two sections into existing files. The realistic saving is:

| Source | Estimated saving | Mechanism |
|---|---:|---|
| Frontmatter / preamble dedup | ~100 tokens × 2 = ~200 tokens | Each merged file's L1 frontmatter + title + intro paragraph collapses into the parent's table-of-contents. |
| Cross-reference dedup | ~300–600 tokens | "See PRE_COMMIT.md" / "See FRUSTRATED.md" pointers inside other root specs become `#anchor` jumps. |
| Inline-pointer pruning | ~100–300 tokens | The merged-section can drop "as defined in this section" boilerplate that exists today as cross-file scaffolding. |
| **Optimistic total** | **~600–1,100 tokens** | **~0.85–1.55 % of the 70,676-token bundle** |

A 1 % reduction on session boot is not negligible across many sessions, but it is at the noise floor of the variation in spec-evolution churn (a single ADR ratification flips guarded-section content by hundreds of tokens). The measured benefit is **below the threshold the migration cost would justify**.

### Cross-reference rewrite cost

A `grep -rln` over `*.md`, `*.py`, `*.sh` returns:

- **`FRUSTRATED.md`**: 206 referencing files (200 md, 5 py, 1 sh).
- **`PRE_COMMIT.md`**: 175 referencing files.
- **Anchor links** (one each): `FRUSTRATED.md#when-and-how-to-log-mandatory`, `PRE_COMMIT.md#7-mechanical-governance-checks`.

**Total references to rewrite: 381 files.** The rewrite itself is mechanical (a `sed` pass), but each rewritten link MUST be re-verified against the new anchor target — and 100 % of `tasks/<NNN>-<slug>/`-internal `[FRUSTRATED.md](../../FRUSTRATED.md)` patterns become `[MAINTENANCE.md#friction-logging](../../MAINTENANCE.md#friction-logging)`, which is *longer* and slightly less readable.

The rewrite is also **destructive to git blame**: every file that today cites `FRUSTRATED.md` or `PRE_COMMIT.md` carries a blame line pointing at the spec author's commit. Mass-rewriting those references replaces the blame trail with a single bulk-edit commit by the consolidation agent. This is recoverable via `git blame --follow` but adds friction for any future maintenance archaeology.

### Single-concern clarity is a feature, not just boilerplate

`PRE_COMMIT.md` and `FRUSTRATED.md` are the two **shortest** root specs (257 and 119 lines respectively). Their brevity is the point: an agent triaging a pre-commit failure opens `PRE_COMMIT.md` and reads ≤ 5 KB before knowing which linter row to consult. Merging them into `AGENTS.md` (already 517 lines) and `MAINTENANCE.md` (already 471 lines) buries that content inside longer files where the agent must `grep` to a specific anchor.

The current topology rewards **lookup latency** at the cost of **bundle size**. Consolidation trades the cost vector backwards.

### In-flight Tasks depend on the current topology

- [Task 037](../tasks/037-pre-commit-spec-integration/) — Pre-commit spec integration — landed at `done` on the current topology. Its anchors (PC.B.1–PC.B.4) live in `PRE_COMMIT.md §7.A`. Merge would invalidate every external citation of those anchors.
- [Task 038](../tasks/038-frustrated-spec-integration/) — FRUSTRATED.md integration — landed at `updated` (superseded by Task 062), but its FR.B.1–FR.B.4 anchors are cited from `tools/check-fl-declaration.py` and from the AGENTS.md guarded synthesis block.
- [Task 044](../tasks/044-improve-maintenance-spec-may-07-2026/), [Task 064](../tasks/064-improve-maintenance-spec-may-08-2026/) — both target FRUSTRATED.md among their `task_affects_paths`.
- [Task 062](../tasks/062-frustrated-spec-followup-ac1-ac5/) — explicitly references `FRUSTRATED.md §28` and `PRE_COMMIT.md §2` byte-identicality. Merging both files away would either invalidate the byte-identicality contract or require rewriting it as a same-file-cross-section contract.

A consolidation today would either block these Tasks or force a coordinated multi-Task rewrite.

### Adoption signal: zero recurrence of the friction

The Task 053 review identified bundle size as *one* concern among ten. It has not recurred in subsequent Nightly Maintenance Runs (FRUSTRATED.md FL1+ aggregations) as a friction pattern. The measured ~1 % saving is the *theoretical* upside; the *observed* friction is zero.

## Considered Options

### Option 1 — Both merges (PRE_COMMIT → AGENTS, FRUSTRATED → MAINTENANCE)

Land both M1 and M2 in a single coordinated commit. Rewrite all 381 cross-references; coordinate with Tasks 037 / 038 / 044 / 064 / 062.

- **Positives.** Bundle drops by ~1 % (~600–1,100 tokens); two spec filenames retired; README §4 + §10 catalogue shrinks; new agents face 9 spec filenames instead of 11.
- **Negatives.** 381 cross-references to rewrite; git-blame churn; 5 in-flight Tasks blocked or forced to retarget anchors; AGENTS.md grows from 10,274 → ~15,500 tokens (the single largest spec); MAINTENANCE.md grows from 12,022 → ~14,200 tokens; lookup-latency for pre-commit and friction-log discipline degrades.
- **Cost.** Medium (mechanical rewrite + Task coordination + downstream-Task retargeting).

### Option 2 — Partial merge (only M2: FRUSTRATED → MAINTENANCE)

Land M2 but defer M1. Rationale: FRUSTRATED.md is the shortest spec (119 lines) and its content is most thematically aligned with MAINTENANCE.md (friction → nightly maintenance run).

- **Positives.** Half the cross-reference rewrites (~206 files); preserves PRE_COMMIT.md's lookup-latency advantage; eliminates the smallest spec which is the lowest-value standalone file.
- **Negatives.** Saves only ~0.4 % of bundle; still disrupts Tasks 038 / 044 / 062 / 064; introduces asymmetry (why FRUSTRATED but not PRE_COMMIT?).
- **Cost.** Low–medium.

### Option 3 — Status quo (chosen)

Keep the 11-spec bundle as-is. Bundle stays at ~70,676 tokens; the single-concern clarity of PRE_COMMIT.md and FRUSTRATED.md is preserved; in-flight Tasks proceed without disruption.

- **Positives.** Zero migration cost. Zero in-flight Task disruption. Lookup latency preserved (an agent triaging a pre-commit failure opens a 5 KB file, not a 35 KB anchor-target). Single-concern partition continues to reward small-amendment economics (a 1-line FRUSTRATED.md edit doesn't touch AGENTS.md).
- **Negatives.** Bundle stays at ~70,676 tokens; the 11-file count grows the README §10 catalogue cost; new readers must learn 11 spec names.
- **Cost.** Zero migration; ongoing cost is whatever the current topology already imposes.

## Decision Outcome

**Option 3 (status quo) is chosen, recorded as `adr_status: Proposed`.** The 11-spec root bundle remains intact. PRE_COMMIT.md and FRUSTRATED.md retain their independent file identities.

### Falsifier triggers — re-open this ADR when any of the following hold

- **F1.** The measured bundle-token cost exceeds **100,000 tokens** (today: ~70,676). At that point the ~1 % saving from M1 + M2 is **~1,000 tokens** in absolute terms, which is large enough to justify the migration cost.
- **F2.** Either `PRE_COMMIT.md` or `FRUSTRATED.md` shrinks below **1,000 tokens** *and* its dependent-file count drops below **50**. A spec that small with limited inbound coupling is no longer paying for its own file.
- **F3.** Sustained FL1+ friction in the Nightly Maintenance Run cites root-spec count as cause across **three or more** sessions in a 14-day window. The bundle size is workable; sustained friction means it is not.

When any falsifier triggers, a successor ADR MUST be authored that re-evaluates Options 1 and 2 against the then-current evidence and supersedes this one via `adr_supersedes: [ADR-0009]`.

### Status note on `adr_status: Proposed`

This ADR ships at `adr_status: Proposed` rather than `Accepted` because the falsifier triggers above have not been observed yet, and ratification to `Accepted` would prematurely lock the topology against the very evidence the triggers are designed to surface. A maintainer flipping to `Accepted` SHOULD do so only after either (a) the triggers go un-fired for a sustained period (≥ 90 days) or (b) explicit operator confirmation that the 11-spec topology is the long-term commitment.

## Consequences

### Positive

- Zero migration cost; no in-flight Task disruption.
- Single-concern clarity preserved: PRE_COMMIT.md and FRUSTRATED.md remain the canonical lookup targets for their respective concerns.
- The README §10 catalogue continues to act as a self-documenting bundle-size meter; future agents can re-measure trivially.
- Tasks 037 / 038 / 044 / 062 / 064 audit-graph integrity preserved.

### Negative

- The 11-spec bundle's ~70,676-token boot cost is paid every session; sessions that need neither pre-commit guidance nor frustration-logging detail still load both files.
- The README §10 catalogue lists 11 entries; new contributors face a higher entry-cost than they would after consolidation.
- The "merge looks easy" optical bias remains: every future architecture review will likely re-surface the question. The five falsifier triggers above are the structured answer to that recurrence; without them, the question would re-litigate from scratch each time.

### Neutral

- This ADR is the *sibling* decision to [ADR-0008](./0008-narrative-skills-status-quo.md) (narrative skills stay in-repo) — both apply the "measure the friction, then act" pattern to topology-amendment questions. Together they establish a precedent: substrate-level topology amendments require falsifier-trigger evidence, not just architectural-elegance arguments.
- No follow-on implementation Task is created. If a falsifier fires, the successor ADR will spawn the consolidation Task at that time.
- The README §10 boot-bundle catalogue should be amended in a separate T1/T2 edit (not part of this ADR) to reflect the measured **11** specs instead of the prose "9+" — that is a documentation-accuracy fix, not a decision.

## Cross-references

- [Task 057 — Root-Spec Consolidation (ADR)](../tasks/057-root-spec-consolidation-adr/task.md) — this ADR's parent task.
- [Task 053 — Core Architecture Review Follow-ups](../tasks/053-core-architecture-review-followups/) finding B.6 — the dispatch.
- [ADR-0008 — Narrative Skills Status Quo](./0008-narrative-skills-status-quo.md) — sibling decision applying the same pattern.
- [`README.md §10`](../README.md) — the bundle catalogue ("9+" → measured 11; T1/T2 edit pending).
- [`PRE_COMMIT.md`](../PRE_COMMIT.md), [`FRUSTRATED.md`](../FRUSTRATED.md) — the two specs that would have been merged.
- [`AGENTS.md`](../AGENTS.md), [`MAINTENANCE.md`](../MAINTENANCE.md) — the two specs that would have grown.
- [`research/adr-spec-research-synthesis/output/SPEC.md`](../research/adr-spec-research-synthesis/output/SPEC.md) — ADR authoring contract.
