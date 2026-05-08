# M07 — Contradiction Sweep

Critical-thinking pass over the inputs to surface silent contradictions before they land in `output/SPEC.md`.

## Candidate contradictions evaluated

### C-1. "Migration is `done` when fm-validate gates" vs. "Legacy advisory still runs in `[1/6]`"

- **Input A** ([`research/flexible-frontmatter-toolchain/output/SPEC.md`](../../../research/flexible-frontmatter-toolchain/output/SPEC.md) §8.2): "Migration is `done` when … the four legacy linters under `tools/legacy/` are removed in a final cleanup commit".
- **Input B** ([`MAINTENANCE.md`](../../../MAINTENANCE.md) §1.1): "**Legacy** (advisory shim, one release window) … scheduled for removal once the structural rules in `lint-structure.py` and `lint-linkage.py` are folded into `fm/validate.py` / a successor `fm-graph`."
- **Resolution.** No live contradiction — Input A names the *terminal* state; Input B names the *current* state. The `output/SPEC.md` flip checklist captures the ordering: criteria 1–6 confirm `tools/legacy/` is no longer load-bearing; criterion 7 enforces *zero live consumer* before the procedure deletes the directory.

### C-2. ADR validator step number inside `tools/check-governance.sh`

- The hook-line in `tools/check-governance.sh` reads `[5/6]` today (Step `[5/6] ADR governance validator`), and `tools/lint-runlog.py` runs as `[4/6]`. PRE_COMMIT.md §7 mentions step `[5/5]` and §7.C anchors `[5/6]`.
- **Resolution.** The `5/6` numbering reflects the legacy-runner placeholder occupying step `[3/6]` ("Cross-reference linkage (folded into fm-validate --type-check)" — the printed banner is preserved as a no-op). Once the legacy advisory is removed (post-flip §3 cleanup), the banner re-numbers to `[N/5]`. Captured in `output/SPEC.md` §3 as a sequencing note.

### C-3. `FM_TOOLCHAIN=0` is "documented escape hatch" vs. "MUST NOT be used in CI"

- MAINTENANCE.md §1.1 calls `FM_TOOLCHAIN=0` "a documented escape hatch … but is NOT the supported configuration; it exists only to unblock a contested migration step and SHOULD NOT be used in CI."
- **Resolution.** Not a contradiction; the escape hatch is for *human* unblocking only. Post-flip, the env var is removed entirely (the codepath in `tools/check-governance.sh` lines 27–47 collapses to a single fm-validate gate). Captured in `output/SPEC.md` §2 as a file change.

### C-4. Trust-audit behavioral threshold (0.80 vs. 0.90)

- `tools/check-trust-audit.py` `DIAGNOSTIC_SCHEMA["thresholds"]["behavioral"] = 0.80` with a comment to "raise back to 0.90 once Task 039 ST-5 (AGGREGATOR) lands AND RESEARCH.md §5 normatively requires methodology.md".
- The task assignment says: "Spec-J/K/L thresholds: schema ≥80%, behavioral ≥90%, governance ≥95%".
- **Resolution.** Apparent — not real — contradiction. The task instruction quotes the *post-flip* (Spec-J/K/L canonical) thresholds. The runtime tool is at the *migration-window* relaxed value. The flip criteria SPEC therefore lists "behavioral threshold raised to 0.90" as an explicit §3 WARN→ERROR-style promotion that follows the toolchain flip.

## No live contradictions

No candidate above produced a live contradiction in the input corpus. The flip-criteria SPEC therefore needs no caveats; it can speak in unambiguous MUST clauses.
