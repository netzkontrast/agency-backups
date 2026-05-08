# Methodology — Toolchain Flip Criteria

## M06 — Source Triangulation

The flip criteria are derived by triangulating four authoritative repo-local sources. No external web fetches were performed because every source needed to enumerate the gating surface is checked into the repository.

| Source | Read for |
|---|---|
| [`MAINTENANCE.md`](../../../MAINTENANCE.md) §1.1 | Current Toolchain Surface table (dual Legacy/Flexible) and the FM_TOOLCHAIN escape-hatch semantics. |
| [`PRE_COMMIT.md`](../../../PRE_COMMIT.md) §7 / §7.A / §7.B / §7.C | Three-way precedence matrix, per-rule waiver burn protocol, ADR validator step `[5/6]`. |
| [`research/flexible-frontmatter-toolchain/output/SPEC.md`](../../../research/flexible-frontmatter-toolchain/output/SPEC.md) §8 | "Migration is `done` when …" — the original Task-017 era criteria; we lift these and harden them with mechanical commands. |
| [`research/governance-specs-update-research/output/SPEC.md`](../../../research/governance-specs-update-research/output/SPEC.md) §2 | The orphaned ask that the spec MUST document the parallel existence of the two toolchains and their bypass interactions. |
| [`tools/check-governance.sh`](../../../tools/check-governance.sh) | Live pipeline shape: which step gates and which is advisory; `[1/6]` toggles on `FM_TOOLCHAIN`. |
| [`tools/.frontmatter-waivers`](../../../tools/.frontmatter-waivers) | The actual waiver corpus (header-only, no live rows at run-time). |

## M08 — What Would Change My Mind

Pre-commitment: I assume the legacy toolchain has no remaining live consumer because (a) `tools/check-governance.sh` step `[1/6]` already gates on `tools/fm/validate.py --type-check` by default, and (b) the legacy shim runs with `FM_LEGACY_QUIET=1` silencing its output.

What would change my mind:

- A live caller of `tools/legacy/{validate-frontmatter,lint-structure,lint-linkage}.py` outside `tools/check-governance.sh` (none found via `grep -RIn "tools/legacy/" docs prompts research tasks`).
- A workflow under `.github/workflows/` that pins `FM_TOOLCHAIN=0` (none found; only `adr-validate.yml` uses the ADR column).
- A documented dependency on `FM_TOOLCHAIN=0` in any closed Task's notes (none found in Tasks 016/017/019, all `done`).

If any of the above surfaced, the flip checklist would have to add a deprecation-window item before retiring `tools/legacy/`.

## M07 — Contradiction Sweep

See [`../reflection/M07-contradictions.md`](../reflection/M07-contradictions.md).

## M13 — Adversarial Query Expansion

Counter-questions surfaced and resolved in the SPEC:

- *"Does the ADR column ever need to flip?"* — No. ADR runs unconditionally; the only "flip" affecting it is the change in step numbering after the legacy advisory runner is removed (`[5/6]` → `[5/5]`). Captured as a §3 cleanup line item.
- *"Is `FM_TOOLCHAIN=0` the same as 'pre-flip'?"* — No. `FM_TOOLCHAIN=0` inverts which column of the dual gate emits the ERROR; both columns continue to run. Post-flip, `FM_TOOLCHAIN` is removed entirely. Captured as §1 criterion.
- *"What about per-rule waivers carrying legacy diagnostic codes?"* — `tools/.frontmatter-waivers` is header-only at run time; if any TSV row carries a `tools/legacy/`-emitted rule-id, it MUST be re-expressed against an `tools/fm/validate.py` code or burned. Captured as §1 / §3.
