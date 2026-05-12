---
type: task
status: archived
slug: flexible-frontmatter-toolchain
summary: "Implement the four-tool stateless toolchain (fm-validate, fm-extract, fm-edit, fm-query) and the per-type required-keys + required-headings contract specified in research/flexible-frontmatter-toolchain/output/SPEC.md."
created: 2026-05-05
updated: 2026-05-12
task_id: "016"
task_status: archived
task_owner: "claude-code"
task_priority: P1
task_uses_prompts:
  - build-flexible-frontmatter-toolchain
task_spawns_research: []
task_spawns_prompts: []
task_affects_paths:
  - tools/fm/
  - tools/fm/_core.py
  - tools/fm/validate.py
  - tools/fm/extract.py
  - tools/fm/edit.py
  - tools/fm/query.py
  - tools/check-governance.sh
  - maintenance/schemas/header-ontology.json
  - tests/fm/
---

# Task 016 — Build the Flexible Frontmatter Toolchain

## Goal

Ship the four CLI tools (`fm-validate`, `fm-extract`, `fm-edit`, `fm-query`) plus the shared `tools/fm/_core.py` library so that, on the staged tree, every Gherkin scenario in [`research/flexible-frontmatter-toolchain/output/SPEC.md §6`](../../research/flexible-frontmatter-toolchain/output/SPEC.md) passes and `tools/check-governance.sh` has been re-pointed at `fm-validate` *behind a feature flag* (the legacy validator stays in CI for one release; the cutover is Task 017's responsibility).

## Plan

1. **Scaffold `tools/fm/`.** Create the package directory with `__init__.py`, `_core.py`, `validate.py`, `extract.py`, `edit.py`, `query.py`. Move `tools/_frontmatter.py` into `tools/fm/_core.py` and add a thin re-export shim at the old path (per SPEC §5.5).
2. **`fm-validate` (SPEC §5.1).** Implement per-`type:` classification, the L1+L2 required-key check (§3.1–3.3), the typo-detection rule (§3.4), and the required-heading walk (§4). Diagnostic shape MUST match SPEC §5.1 verbatim. Exit codes: 0 (clean), 1 (any ERROR), with `--strict` promoting WARNs.
3. **`fm-extract` (SPEC §5.2).** Implement `--section`, `--frontmatter [<key>]`, `--whole-file`. Honour the 4 KB / 2 KB caps (§5.2). Preserve case-insensitive heading match with em-dash + colon stripping.
4. **`fm-edit` (SPEC §5.3).** Implement `--set / --unset / --append-list / --remove-from-list / --bump-updated`. Take an OS file lock around the read-modify-write. Verify byte-identical body bytes pre/post (§5.3).
5. **`fm-query` (SPEC §5.4).** Implement the selectors listed in §5.4. Statelessness: zero filesystem writes outside the explicit `--output` path; zero reads of `.agent_cache/`. Default scope = the operational roots.
6. **Header ontology JSON.** Author `maintenance/schemas/header-ontology.json` per SPEC §4.3. Mirror the §4.1 table verbatim. The ontology becomes the canonical machine-readable source; `fm-validate` MUST load from JSON, not hardcode.
7. **Tests.** Write `tests/fm/` covering every Gherkin scenario in SPEC §6 plus the M01 falsification cases (M01-falsification.md §P1–P5). Use the standard library `unittest` only (no pytest dependency, per the no-extra-deps principle).
8. **CI integration (feature-flagged).** Add a step to `tools/check-governance.sh` that runs `fm-validate` *and* the legacy validator side-by-side, gated by `FM_TOOLCHAIN=1`. Default state: legacy validator decides exit code; fm-validate logs only. Task 017 flips the gate.
9. **Friction log + run-log entry.** On task close, declare an FL[0–3] in `friction-log.md` and append a short note to `maintenance/run-log.md` describing the new tools' availability.

## Todo

- [x] 1. Scaffold `tools/fm/` package + re-export shim.
- [x] 2. Implement `fm-validate` with §3 + §4 checks.
- [x] 3. Implement `fm-extract` with token caps.
- [x] 4. Implement `fm-edit` with file lock + body-byte invariant.
- [x] 5. Implement `fm-query` with stateless filesystem scan.
- [x] 6. Author `maintenance/schemas/header-ontology.json`.
- [x] 7. Write `tests/fm/` covering every Gherkin scenario + M01 attacks.
- [x] 8. Wire `fm-validate` into `tools/check-governance.sh` behind `FM_TOOLCHAIN=1`.
- [x] 9. Resolve SPEC §10 Q1 (submodule/sparse-checkout interaction) in `notes.md`.
- [x] 10. Resolve SPEC §10 Q2 (fm-edit `--batch` mode default-no decision) in `notes.md`.
- [x] 11. Run `tools/check-governance.sh` clean.
- [x] 12. Set `task_status: done`, `updated:`; write `friction-log.md`; append `maintenance/run-log.md`.

## Links

- Source SPEC: [`/research/flexible-frontmatter-toolchain/output/SPEC.md`](../../research/flexible-frontmatter-toolchain/output/SPEC.md)
- Executing prompt: [`/prompts/build-flexible-frontmatter-toolchain/prompt.md`](../../prompts/build-flexible-frontmatter-toolchain/prompt.md)
- Hand-off (next): [`/tasks/017-migrate-repo-to-flexible-toolchain/`](../017-migrate-repo-to-flexible-toolchain/)
- Adjacent open work (scope narrowed by SPEC §C1): [`/tasks/010-skills-frontmatter-index-suite/`](../010-skills-frontmatter-index-suite/), [`/tasks/011-skills-frontmatter-schema-files/`](../011-skills-frontmatter-schema-files/)
- Prior art: [`/tools/dramatica-nav/`](../../tools/dramatica-nav/), [`/skills/skill-creator/`](../../skills/skill-creator/)
- Governing specs: [`TASK.md`](../../TASK.md), [`MAINTENANCE.md`](../../MAINTENANCE.md), [`PRE_COMMIT.md`](../../PRE_COMMIT.md)
