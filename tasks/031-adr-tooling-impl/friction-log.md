---
type: note
status: active
slug: 031-adr-tooling-impl-friction-log
summary: "Closure friction log for Task 031 (TASK.md §7.7). Records the FL declaration and the three notable frictions encountered while implementing the agency-adr CLI suite. Finalised on PR #67 merge (commit bf90826)."
created: 2026-05-06
updated: 2026-05-06
---

# Task 031 Friction Log

**Highest Frustration Level: FL2**

## Outcome

`agency-adr` is in force on `main`. PR [#67](https://github.com/netzkontrast/agency/pull/67) merged as commit `bf90826`. Validate + synthesize sub-commands ship; 49 ADR-specific tests pass alongside the 153 pre-existing tests; `tools/check-governance.sh` PASSes 5/5 numbered steps plus the trust audit; `.github/workflows/adr-validate.yml` runs the same gate plus a dry-run diff against the committed `AGENTS.md` guarded section. The PR carried five commits: `97719e7` (initial implementation), `1643110` (compress-citation aggregation + ADR.A.1.4 enforcement + diagnostic-explanations registration), `01c8a96` (CI fix: AGENTS.md alignment + run-log schema), `6a30991` (PR #67 review findings T.1–T.4), and `81f5ee4` (this Task entry + the [adr-tooling-impl prompt](../../prompts/adr-tooling-impl/prompt.md), closing PR #67 review findings G.1 and G.2).

## FL Declaration

Three FL1–FL2 frictions encountered during implementation. The aggregate FL is **FL2** for the dual-imports diagnosis (Entry 1); no additional friction surfaced between local push and merge.

### Entry 1 — `tools/` is not a Python package; relative imports are forbidden (FL2)

**What happened.** My first cut of `tools/adr/*.py` used the existing `tools/fm/*.py` import idiom:

```python
if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from fm import _core
else:
    from ..fm import _core
```

The relative-import branch (`from ..fm import _core`) failed in pytest with `ImportError: attempted relative import beyond top-level package`. Cause: `tools/` has no `__init__.py`, so neither `fm` nor `adr` is part of a parent `tools` package — the `..fm` path has no anchor. The fm modules survive because they only ever execute the script-mode branch (`__package__ in (None, "")`); my modules were imported as `adr.body` etc., so the package branch ran and exploded.

**Resolution.** Dropped the dual-branch shim entirely; every module unconditionally puts both `tools/` and `tools/fm/` on `sys.path` and does `import _core` (not `from fm import _core`). The latter would have re-imported the `fm` *package* and shadowed `tools/fm/fm.py` (the dispatcher script the fm-wrapper tests rely on), breaking 6 fm tests at runtime.

**Suggested process tweak.** `tools/readme.md` SHOULD note that adding a sub-package under `tools/` requires the script-mode-only import idiom (or a top-level `tools/__init__.py`), since the existing fm shim is misleading.

**Cost.** ≈ 25 minutes of repeated fail-fix-fail before I traced the package-vs-script ambiguity.

### Entry 2 — Run-log schema mismatch only surfaced in CI (FL1–FL2)

**What happened.** `tools/adr/runlog.py` v1 emitted records with the fields documented inline in `maintenance/run-log.md`'s "How to Read This File" prose: `agent`, `mode`, `contributing_adr_ids`, `token_count`, `fidelity`, `fidelity_mode`. `tools/lint-runlog.py` enforces a different (richer) schema designed for Repo Coherence Checks: `start_commit`, `end_commit`, `baseline_commit`, `files_in_delta`, `files_scanned`, `t1_fixes`, `t2_fixes`, `t3_tasks_created`, `t4_skipped`, `issues_skipped`, `notes`. The mismatch wasn't caught locally because my early test runs didn't synthesise into the real `maintenance/run-log.md`; CI exercised the full pipeline and the run-log linter rejected the malformed record.

**Resolution.** Reshaped `runlog.append_run_record` to emit every coherence-check field (with `n/a` / `0` placeholders for fields that do not apply to synthesis runs) and parked ADR-specific metadata in `notes`. Added a test asserting every required field is present.

**Suggested process tweak.** `MAINTENANCE.md §2.3` documents the prose-shape of run-log records, but the binding contract is `tools/lint-runlog.py`'s `REQUIRED_FIELDS` constant. Either inline the constant into `MAINTENANCE.md`, or reference `tools/lint-runlog.py` as the authoritative shape, so future appenders cannot drift.

**Cost.** ≈ 10 minutes after the CI failure surfaced; would have been ≈ 1 minute if `MAINTENANCE.md` had cited the linter.

### Entry 3 — Diff gate vs. placeholder text in the committed AGENTS.md (FL1)

**What happened.** I seeded `AGENTS.md` with a human-readable placeholder inside the markers (`_(empty — /decisions/ carries no Accepted ADRs yet…)_`). The synthesizer with an empty corpus emits an empty body (`"\n"`). The CI diff gate compared committed bytes against dry-run output and correctly rejected the mismatch.

**Resolution.** Ran `python3 tools/adr/cli.py synthesize` so the committed bytes match the dry-run output for an empty corpus. The placeholder text was descriptively useful to a human reader but operationally wrong — the diff gate is the source of truth.

**Suggested process tweak.** When seeding markers, the safe pattern is to commit whatever the synthesizer would produce on the current corpus state. The author MUST run `synthesize` once before pushing, not just `validate`.

**Cost.** ≈ 5 minutes; the CI annotation was unambiguous about the remedy.

## Boundaries Honoured

- No edits to the immutable [`research/adr-spec-research-synthesis/output/SPEC.md`](../../research/adr-spec-research-synthesis/output/SPEC.md) (T4 immutability per `MAINTENANCE.md §1`).
- No edits to `.githooks/pre-commit` directly; the only gate edit was via `tools/check-governance.sh` per ADR.A.5.8.
- No new top-level dependencies; `agency-adr` reuses `tools/fm/_core.py` and the existing `jsonschema` requirement.

## Outstanding Items

- All PR #67 review findings are closed: G.1 (Task entry) and G.2 (prompt artifact) by this Task and the sibling [`prompts/adr-tooling-impl/prompt.md`](../../prompts/adr-tooling-impl/prompt.md); T.1–T.4 by commit `6a30991`. No items deferred to a successor Task.
- The first batch of authored ADRs (PD-005 in [`research/adr-assumption-audit/output/REPORT.md`](../../research/adr-assumption-audit/output/REPORT.md) §3) remains a separate Task — `agency-adr` is the *tooling*; the corpus seed is the next Task in the lineage.
