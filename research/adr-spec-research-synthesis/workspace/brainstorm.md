---
type: note
status: active
slug: adr-spec-research-synthesis-brainstorm
summary: "/sc:brainstorm output: five integration questions answered. Each conclusion labelled [RESOLVED] / [OPEN — needs human decision] / [DEFERRED to Task 029]."
created: 2026-05-05
updated: 2026-05-05
---

# Step 2 — `/sc:brainstorm` Integration Points

Inputs: [`analysis.md`](./analysis.md). Method: every conclusion below is labelled `[RESOLVED]`, `[OPEN — needs human decision]`, or `[DEFERRED to Task 029]`. Conflicting conclusions are recorded in [`../reflection/M07-contradictions.md`](../reflection/M07-contradictions.md).

## Q1. Storage Path: Where Do ADR Files Live?

**Candidates considered:**

1. `docs/decisions/` — Gemini's default; aligned with industry adr-tools convention.
2. `decisions/` (no `docs/` parent) — repo-native: avoids introducing a `docs/` top-level (which `FOLDERS.md §1` does not authorise).
3. `research/adr/` — co-located with synthesis artefacts; reuses an existing top-level.
4. `tasks/<NNN>-adr-<slug>/` — model each ADR as a Task. Rejected immediately: ADRs are immutable, Tasks are not.

**Trade-off matrix:**

| Criterion | `docs/decisions/` | `decisions/` | `research/adr/` |
|---|---|---|---|
| Honours `FOLDERS.md §1` (3 operational folders) | adds new top-level | adds new top-level | reuses existing |
| Industry recognition for AI agents (`AGENTS.md`-readers, `adr-tools`) | high | medium | low |
| Cleanly separates "decision" (immutable) from "research" (immutable-after-complete) | yes | yes | NO — collides with `research_phase` semantics |
| Migration-path simplicity | medium | medium | low (would require renaming `research/` schema) |

**Conclusion: `[RESOLVED]` — the canonical path is `decisions/` at the repo root.**

Rationale: introducing a `docs/` parent would smuggle in a third level (`docs/decisions/X.md` is a 3-segment path) for negligible benefit; flattening to `decisions/` honours `FOLDERS.md §4 "Prefer Flat Structures"`. The `FOLDERS.md §8` exemption table is extended (a T3 Task — see Task 028) to add `decisions/` as a fifth non-operational storage folder. `research/adr/` is rejected because `research_phase: complete` immutability + ADR `Superseded` lifecycle would create two mutually exclusive lifecycle vocabularies in one folder.

## Q2. CLI Integration: How Does `agency-adr` Attach Without Duplicating `tools/fm/`?

**Conclusion: `[RESOLVED]` — `agency-adr` lives at `tools/adr/cli.py` and reuses `tools/fm/_core.py`.**

Concrete shape:

```text
tools/adr/
├── cli.py        # argparse entry; sub-commands: validate, synthesize
├── schema.py     # JSON-Schema for adr_* L2 namespace; imports tools/fm/_core
├── graph.py      # Build supersession DAG; Kahn cycle-detection
├── extract.py    # Pull "Decision Outcome" + "Consequences" sections (uses fm/extract.py heading machinery)
├── compress.py   # MDL synthesis: token-counting + rule deduplication
├── synthesize.py # Orchestrator: extract → compress → write guarded AGENTS.md section
└── readme.md
```

The CLI is invoked from `tools/check-governance.sh` as a new `[N/N] ADR governance validator` step (placed before the trust audit). Direct `.githooks/pre-commit` modification is prohibited per the legacy convention.

`agency-adr` is NOT installed as a Python entry-point in `setup.py`; it is invoked as `python3 tools/adr/cli.py`. This matches every other tool in `tools/`. A symlink `tools/adr/agency-adr` MAY be added later for ergonomics; that is a Task 028 implementation detail.

## Q3. Frontmatter Composition: ADR Schema vs L1/L2 Vault Core

**Collision points (from `analysis.md §C2`):**

| Gemini key | L1 collision | Resolution |
|---|---|---|
| `id: ADR-NNNN` | `slug` (kebab-case) | Promote `slug` to canonical (e.g. `slug: 0001-record-architecture-decisions`); add `adr_id: "ADR-0001"` as a secondary identifier. |
| `title` | none, but body's `# <Title>` already encodes the human-readable title | Drop `title` from frontmatter; the body H1 is the title. `summary` (L1) carries the token-cheap tl;dr. |
| `status: enum{Proposed, Accepted, Superseded, Deprecated}` | L1 `status: enum{draft, active, blocked, completed, archived}` | Use `adr_status` for the four ADR lifecycle states; keep L1 `status: active` for Proposed/Accepted ADRs and `status: archived` for Superseded/Deprecated. |
| `date` | L1 `created` + `updated` | Drop `date`; use L1 `created` (the ADR's authorship date) and `updated` (last status change). |
| `supersedes: list[ADR-NNNN]` | none | Adopt as `adr_supersedes` (L2 namespace). Reciprocal `adr_superseded_by` mirrors `task_superseded_by`. |
| `tags: list` | L0 `tags` (Obsidian) | Reuse L0 `tags` for graph/search; do NOT introduce a parallel `adr_tags`. |

**Conclusion: `[RESOLVED]` — the ADR namespace is `adr_*` (L2), composes additively with L0+L1, and the canonical JSON-Schema lives in `maintenance/schemas/header-ontology.json` under `types.adr`.**

The schema sets `additionalProperties: true` per the prompt's narrowing, so future L2 keys (`adr_owner`, `adr_blast_radius`, …) can be added without breaking existing files.

## Q4. AGENTS.md Ownership: Synthesis Overwrite vs Manual Content

**The conflict (from `analysis.md §C3`):** Gemini mandates wholesale overwrite (idempotent, deterministic). The repo's `AGENTS.md` contains:

- Hand-authored normative prose (Session Setup, Folder Management, Mandatory Frustration Feedback, Closing Run Procedure, Spec Language Reference, Frontmatter Ontology, Narrative Ontology).
- Append-only `LOOP_LOG` written by Jules.
- A "Current State" pointer to research artefacts.

Wholesale overwrite would destroy all of this.

**Conclusion: `[RESOLVED]` — the synthesis pipeline writes a *guarded section*, never the full file.**

Markers:

```markdown
<!-- BEGIN AGENCY-ADR SYNTHESIS -->
... synthesised normative summary derived from Accepted ADRs ...
<!-- END AGENCY-ADR SYNTHESIS -->
```

Hard rules:

1. The pipeline MUST refuse to write if both markers are not present (prevents accidental destructive overwrite of a fresh `AGENTS.md`).
2. The pipeline MUST overwrite ONLY the bytes between the markers; everything else is preserved verbatim.
3. The pipeline MUST be deterministic: the same Accepted ADR corpus produces the same byte sequence between markers.
4. Manual edits inside the markers are LOST on the next synthesis run; this MUST be documented at the top of the guarded section as `<!-- AGENT-WRITTEN. DO NOT EDIT BY HAND. Edits will be overwritten by tools/adr/cli.py synthesize. -->`.
5. The guarded section MUST cite each contributing ADR by `adr_id` in a footer block so the human/agent can trace any synthesised rule back to its source.

**Where to insert markers in the existing `AGENTS.md`:** the Task 028 implementation plan (not this spec) decides the exact location. A reasonable default is between `## Frontmatter Ontology (Summary)` and `## Narrative Ontology — Dramatica × NCP × Novel-Architect Bridge`. This is `[DEFERRED to Task 028]`.

## Q5. Migration Path: How Are Implicit Decisions Bootstrapped as Formal ADRs?

The 14 implicit decisions catalogued in `analysis.md §A` are the natural ADR-0001 corpus. Two strategies:

**Strategy A — One ADR per implicit decision (14 ADRs).** Maximum granularity. Each ADR is small, self-contained, and individually superseded if a future decision changes course. Implementation cost: 14× the per-ADR work.

**Strategy B — Cluster by surface (≈ 5 ADRs).** ADR-0001 "Frontmatter Ontology" (covers I1, I2, I11), ADR-0002 "Folder Topology" (I3, I4, I14), ADR-0003 "Repair Tier Model" (I7, I8), ADR-0004 "Tooling Composition" (I9, I10), ADR-0005 "Closure Protocol" (I6, I12, I13). Lower per-ADR cost, but supersession granularity is coarser.

**Conclusion: `[OPEN — needs human decision]` — Task 029 (assumption audit) MUST recommend A or B before the first ADR is authored.**

The ADR governance spec itself does NOT take a position on the migration cardinality; it MUST work for both strategies. The `adr_supersedes` graph is a list, so a single successor MAY supersede multiple predecessors regardless of which strategy seeded the corpus.

## Open Items Roll-Up (For §8 of `output/SPEC.md`)

| Item | Label | Owner | Unblock condition |
|---|---|---|---|
| Storage path final ratification (`decisions/` accepted via this spec) | `[RESOLVED]` | — | — |
| CLI co-location at `tools/adr/` | `[RESOLVED]` | — | — |
| Frontmatter `adr_*` L2 namespace shape | `[RESOLVED]` | — | — |
| AGENTS.md guarded-section markers placement (exact line range) | `[DEFERRED to Task 028]` | Task 028 | Implementation plan finalises insertion point. |
| Migration cardinality (Strategy A vs B) | `[OPEN — needs human decision]` | Maintainer | Task 029 audit recommendation. |
| Fidelity-metric algorithm (`bcp14-keyword` vs `adr-id-anchor` vs `llm-pass`) | `[OPEN — needs human decision]` | Maintainer | Task 029 audit + Task 028 prototype benchmarks. |
| `tools/.frontmatter-waivers` interaction (does it cover `decisions/`?) | `[OPEN — needs human decision]` | Maintainer | Burn-down protocol decision; spec leans NO. |
| Token-limit empirical floor (current `AGENTS.md` ≈ 4.8 KT; 2,000 KT is aspirational) | `[OPEN — needs human decision]` | Maintainer | Once first synthesis run reports actual size. |
| Whether `adr_status: Proposed` ADRs participate in synthesis | `[DEFERRED to Task 028]` | Task 028 | Default: NO; only Accepted contributes to guarded section. |

Five `[OPEN]` items + two `[DEFERRED]` items + four `[RESOLVED]` items = 11 conclusions tracked. Every `[OPEN]` and `[DEFERRED]` item is surfaced in §8 of [`../output/SPEC.md`](../output/SPEC.md).

## Cross-Pollination With `analysis.md`

Brainstorm conclusions that *feed back* into the analysis:

- **Q3** confirmed B1–B3 are sufficient: no new L1 keys are needed for ADRs.
- **Q4** introduces a *new convention* — guarded-section markers — that is not yet in any root spec. The ADR governance spec MUST therefore mandate it (it becomes a normative statement, not an implementation choice).
- **Q5** confirms the implicit-ADR list in §A of `analysis.md` is the seed corpus. The cardinality question is genuinely open.
