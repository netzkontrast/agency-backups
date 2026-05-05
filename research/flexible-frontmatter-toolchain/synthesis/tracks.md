# Tracks

Per-track work breakdown for the synthesis. Each track terminates in one or more sections of `output/SPEC.md`.

## Track A — Required-Only Validation Semantics

Goal: define a minimal, per-`type:` check matrix that fails on missing required keys or required headings, never on extras.

Output: `SPEC.md §3 (Required Keys)`, `§4 (Required Headings)`, `§6.1` Gherkin scenarios.

## Track B — Stateless Toolchain CLI Surface

Goal: replace dramatica-nav + the proposed task-010 index with a four-tool surface (`fm-validate`, `fm-extract`, `fm-edit`, `fm-query`) that performs every operation by walking the filesystem fresh.

Output: `SPEC.md §5 (Toolchain)`, `§6.2/§6.3` Gherkin scenarios.

## Track C — Pre-Commit & Maintenance Wiring

Goal: bind the new tools into `tools/check-governance.sh`, `.githooks/pre-commit`, and the Coherence-Check protocol without breaking the existing T1/T2/T3/T4 ladder.

Output: `SPEC.md §7 (Integration)`, `§6.4` Gherkin scenarios.

## Track D — Migration Path

Goal: define the additive migration that brings every operational file under the new contract without breaking pre-existing diagnostics.

Output: `SPEC.md §8 (Migration)`, hand-off to `/tasks/017-migrate-repo-to-flexible-toolchain/`.
