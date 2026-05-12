# Post-Synthesis Merge Log

Chronological record of how the four tracks were merged into a single SPEC.

1. **Track A → SPEC §3 + §4.** Lifted `L1_REQUIRED` from `tools/validate-frontmatter.py:38`. Added a `REQUIRED_HEADINGS` table keyed by `type:` (sourced from `templates/task.md`, `templates/prompt.md`, `RESEARCH.md §2`, and the proposed skill template).
2. **Track B → SPEC §5.** Dramatica-nav's split (extract / validate / nav) maps cleanly to (`fm-extract` / `fm-validate` / `fm-query`). The fourth tool (`fm-edit`) is new — it replaces hand-rolled YAML edits with idempotent `--set` / `--unset` / `--append-list` operations.
3. **Track C → SPEC §7.** `check-governance.sh` invokes the new tools instead of the four legacy linters. The legacy linters are retained for one release as `tools/legacy/` to allow the migration in task 017.
4. **Track D → SPEC §8.** Migration is **additive-only**: existing files get an `updated:` bump; no L2 keys are renamed; new required-headings are emitted only on files that already have them or have `REPLACE` markers. Files that fail the new validator after migration become T2 fixes for the next coherence run.

## Deferrals

- **Reciprocity hardening** is mentioned in `§9 Anti-Patterns` but its full implementation lives in task 010 (renamed scope: "query CLI on top of the stateless toolchain") and task 011 (schema files).
- **Token-budget telemetry** (counting actual tokens vs. estimated) is descoped to a follow-up; the SPEC mandates the budget but does not mandate measurement.
