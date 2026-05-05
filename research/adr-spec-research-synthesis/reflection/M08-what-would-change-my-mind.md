---
type: note
status: active
slug: adr-spec-research-synthesis-m08
summary: "M08 What Would Change My Mind: explicit falsifiers for the four high-stakes design choices in output/SPEC.md."
created: 2026-05-05
updated: 2026-05-05
---

# [M08] What Would Change My Mind

For each high-stakes claim in `output/SPEC.md`, what concrete observable evidence would force a rewrite?

## Claim 1 — Storage Path Is `decisions/` (Not `docs/decisions/` or `research/adr/`)

**My current confidence:** high (0.85).

**Falsifier:** the maintainer documents an explicit preference for the `docs/` parent (e.g., to align with an existing static-site generator pipeline that expects `docs/`), or `FOLDERS.md §8` is amended *before* Task 028 ships to add a `docs/` exemption.

**Why this would change my mind:** the only argument for `docs/decisions/` is industry-convention compatibility. If the repo is integrated with a tool that requires the `docs/` parent (Sphinx, MkDocs, Docusaurus, log4brains static-site mode), the convention argument becomes a constraint. The repo currently ships none of these.

**Action if falsified:** rewrite `output/SPEC.md §2.1` and §7.1 ADR.A.5.4; update `FOLDERS.md §8` exemption to `docs/decisions/`; do NOT change `output/SPEC.md §2.3` (guarded-section markers) or §7 (CLI shape); the rest of the spec is path-agnostic.

## Claim 2 — Synthesis Pipeline Writes a Guarded Section, Not the Whole `AGENTS.md`

**My current confidence:** high (0.95).

**Falsifier:** the maintainer commits to the constraint that `AGENTS.md` content MUST be 100% derivable from ADRs (i.e., no hand-authored normative prose survives). This would require migrating the existing hand-authored content (Session Setup, Closing Run Procedure, Spec Language Reference, Frontmatter Ontology, Narrative Ontology) into the ADR corpus first.

**Why this would change my mind:** the guarded-section mechanism exists because the repo has non-ADR content in `AGENTS.md`. If the repo commits to the all-ADR model, the guarded section becomes the whole file and the markers can be dropped.

**Action if falsified:** rewrite `output/SPEC.md §2.3` and §5.1 ADR.A.3.5 to remove the marker requirement; introduce a migration Task to move Section Setup / Closing Run Procedure / etc. into ADRs first; the rest of the spec is unchanged.

## Claim 3 — `tools/adr/cli.py` Is the Right CLI Co-location (Not `tools/fm/adr.py` or a Top-Level `agency-adr` Binary)

**My current confidence:** high (0.90).

**Falsifier:** the existing `tools/fm/` toolchain absorbs ADR concerns (Task 019's "fm-toolchain-suite-integration" decides to extend `tools/fm/` rather than spawn `tools/adr/`); or the maintainer chooses a top-level `agency-adr` Python entry-point (via `setup.py` or `pyproject.toml`) for ergonomics.

**Why this would change my mind:** the `tools/fm/` toolchain is purposefully *generic frontmatter operations* — validate, extract, edit, query. ADR-specific logic (DAG cycle detection, MDL compression, guarded-section writing) is a different concern surface and would dilute `tools/fm/`'s purpose. But Task 019 has explicit authority to redraw this boundary.

**Action if falsified:** rewrite `output/SPEC.md §7.1` to swap `tools/adr/` → `tools/fm/adr/`; the public CLI shape (`agency-adr validate | synthesize`) is preserved either way; the rest of the spec is unchanged.

## Claim 4 — Token-Limit 2,000 Is Aspirational, Not Empirical, Against Current `AGENTS.md`

**My current confidence:** medium (0.65).

**Falsifier:** an empirical token-count of `AGENTS.md` produced by an actual tokeniser (Anthropic's `cl100k`-equivalent) shows ≤ 2,000 tokens in the *non-guarded* portion alone, leaving >0 budget for the guarded section under a 2,000-token total.

**Why this would change my mind:** my `wc -w × 1.33` heuristic is a lower bound. A real tokeniser may show that ≈ 70% of `AGENTS.md` is whitespace + Markdown punctuation, in which case the actual token count is much lower than estimated.

**Action if falsified:** strengthen `output/SPEC.md §5.1 ADR.A.3.3` from "applies to the synthesised guarded section only" to "applies to the entire `AGENTS.md`"; remove the `[OPEN]` item in §8 about empirical token-limit; everything else stays.

## Mid-Confidence Claims (Not Yet Surfaced as `[OPEN]`)

The following four claims have medium confidence (0.50–0.75) but are NOT routed as `[OPEN]` items because their falsification would not require a spec rewrite, only an implementation tweak (Task 028's responsibility):

1. The `bcp14-keyword` fidelity mode is "deterministic enough" for v0. Falsifier: a Task 028 implementation benchmark shows < 0.95 on a synthetic ADR corpus.
2. Kahn's algorithm is sufficient for cycle detection. Falsifier: ADR corpora exceed 10K nodes (we expect ~50).
3. The MADR 4.0.0 template is the right body schema. Falsifier: the maintainer prefers Y-Statements as the canonical body.
4. `--strict` promotes WARN to non-zero. Falsifier: the repo decides WARN-level diagnostics should never gate a commit.

These are flagged here for completeness; they do not block `output/SPEC.md` ratification.
