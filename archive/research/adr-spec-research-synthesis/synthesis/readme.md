---
type: index
status: active
slug: adr-spec-research-synthesis-synthesis
summary: "Synthesis index for Task 027's research run. Hard results are surfaced here; mechanics live in the per-file logs below."
created: 2026-05-05
updated: 2026-05-05
---

# Synthesis

## Hard Results

1. **Canonical ADR storage path:** `decisions/` at the repo root (per `output/SPEC.md §2`).
2. **CLI surface:** `tools/adr/cli.py validate | synthesize`, composing `tools/fm/_core.py` for parsing.
3. **Frontmatter contract:** new L2 namespace `adr_*`, registered in `maintenance/schemas/header-ontology.json` under `types.adr`.
4. **AGENTS.md ownership split:** the synthesis pipeline writes a guarded section between `<!-- BEGIN AGENCY-ADR SYNTHESIS -->` and `<!-- END AGENCY-ADR SYNTHESIS -->`; bytes outside the markers are preserved.
5. **Validation gate:** `agency-adr validate` is invoked from `tools/check-governance.sh` as a new step; failure exits 1.
6. **Supersession graph:** modelled as a DAG via `adr_supersedes` / `adr_superseded_by`, reciprocity enforced, cycles rejected at validate-time.
7. **Migration corpus:** 14 implicit decisions in `workspace/analysis.md §A` are the candidate seed; cardinality (Strategy A vs B) is `[OPEN]` for Task 029.
8. **Fidelity floor:** declared MUST ≥ 0.95; algorithm parameterised via `--fidelity-mode`; default is `bcp14-keyword` (deterministic, no LLM).

## Files

- [`methodology.md`](./methodology.md) — Methods applied (M06, M07, M08, M13, [M12] base-rate anchoring on prior ADR practice).
- [`tracks.md`](./tracks.md) — Per-track work breakdown (analyze, brainstorm, draft, verify).
- [`post-synthesis-log.md`](./post-synthesis-log.md) — Chronological merge log into `output/SPEC.md`.
- [`state.md`](./state.md) — Step-by-step checklist; every step `[x]` before commit.

## Open Loops

The five `[OPEN — needs human decision]` items from `workspace/brainstorm.md` flow into `output/SPEC.md §8`. They are also routed into [Task 029](../../../tasks/029-adr-assumption-audit/task.md) for the assumption audit.
