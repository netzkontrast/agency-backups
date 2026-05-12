---
type: note
status: active
slug: task-039-review
summary: "Peer review of PR #92 (Task 039 — maintenance-spec-integration). Confirms three open reviewer checklist items; surfaces one critical gap (M.B.7 Gherkin contract vs. fm/edit.py implementation) and two advisory findings."
created: 2026-05-08
updated: 2026-05-08
---

# Review — PR #92 — Task 039 `maintenance-spec-integration`

**Reviewer:** Claude Code (session `claude/brave-darwin-DFjEM`)
**Reviewed branch:** `claude/run-close-task-39-9IqUT` → `main`
**Head commit:** `b30e317`
**Review date:** 2026-05-08

---

## Part I — Reviewer Checklist (from PR body)

### ✅ Item 1: Three-way toolchain table has exactly three columns

Confirmed. MAINTENANCE.md §1.1.2 table rows:

| Column | Value |
|---|---|
| Legacy | `tools/legacy/{validate-frontmatter,lint-structure,lint-linkage}.py` |
| Flexible (canonical) | `tools/fm/validate.py --type-check` |
| ADR | `tools/adr/cli.py validate` |

The prose explicitly guards against growth: "the columns are exactly three and the matrix MUST NOT silently grow a fourth column for MCP servers." The MorphLLM-Fast-Apply footnote is informational only and does not constitute a fourth column. **Item 1 passes.**

---

### ✅ Item 2: `MAINT_STALE_DAYS` default = 7 matches SPEC contract

Confirmed. `tools/maintenance/staleness-audit.py:113`:

```python
DEFAULT_STALE_DAYS = 7
MAX_STALE_DAYS = 365  # SPEC §4.2 sanity bound.
```

The resolution function at line 180–182 returns `DEFAULT_STALE_DAYS` when the env var is absent. MAINTENANCE.md §3.4 prose says "default: 7 days, configurable via `MAINT_STALE_DAYS`" — matches. **Item 2 passes.**

---

### ✅ Item 3: AGGREGATOR output consumable by §3.2 friction-aggregation

Confirmed. `tools/maintenance/trust-audit.py` emits two output streams:

1. **Canonical diagnostic lines** (stderr / governance check capture): `<path>::WARN:MAINT.TRUST.FRICTION:FL1:<scores>:recommend-task` — visible in `tools/check-governance.sh` output and consumable by `tools/check-maintenance-bypass.py`.
2. **Markdown roll-up block** (stdout): `## Per-workspace summary … ## Roll-up totals` — the format cited in MAINTENANCE.md §3.2 as the dynamic-readme rewrite input.
3. **JSON mode** (`--json` flag): machine-consumable equivalent of the Markdown block.

The `PartitionGuard` test (18/58 in the test suite) asserts `DIAGNOSTIC_SCHEMA` is imported from the GATE and that no `_score_*` helpers are re-implemented. **Item 3 passes.**

---

## Part II — Critical Finding

### ❌ M.B.7 Gherkin Contract Not Implemented in `tools/fm/edit.py`

**Severity: MUST-level spec violation.**

MAINTENANCE.md §6 anchor M.B.7, Scenario 1:

```gherkin
When the agent attempts to apply the T1 repair via `tools/fm/edit.py`
Then `tools/fm/edit.py` MUST refuse with diagnostic
      `M.B.7:adr-accepted-immutable:cannot apply T1 to adr_status=Accepted`
```

This describes a specific refusal behaviour that `tools/fm/edit.py` is required to implement. **The implementation is missing.** A search of `tools/fm/edit.py` (304 lines) finds zero references to `adr`, `Accepted`, `decisions/`, `immutable`, or `M.B.7`. The file has no ADR-awareness whatsoever.

The actual enforcement delivered is different and weaker:
- `tools/maintenance/staleness-audit.py` **excludes** `decisions/` from its scan by construction — preventing the *staleness linter* from proposing a mutation, but not preventing a direct `tools/fm/edit.py` invocation.
- `tools/adr/cli.py validate` enforces ADR schema and supersession-DAG cycles, but does not gate `fm/edit.py` operations.

An agent following the M.B.7 Gherkin scenario literally — calling `tools/fm/edit.py decisions/0042-storage-path.md --bump-updated` on an `adr_status: Accepted` file — will **succeed silently**. The Gherkin contract as written is unexecutable against the shipped implementation.

**Root cause:** The M.B.7 enforcement is correct at the coherence-run *dispatch* level (agents are told not to mutate `decisions/`), but the contract was specified at the *tool* level without implementing the tool-level guard.

**Required action:** Either:

Option A — Implement the guard in `tools/fm/edit.py`:
```python
# Before any mutation, reject adr_status: Accepted files
if fm.get("adr_status") == "Accepted":
    sys.exit(
        "M.B.7:adr-accepted-immutable:cannot apply T1 to adr_status=Accepted"
    )
```

Option B — Downgrade the Gherkin to match actual enforcement scope (replace `tools/fm/edit.py MUST refuse` with `the coherence run MUST NOT invoke tools/fm/edit.py on`).

Option A is strongly preferred — it makes the contract enforceable mechanically and closes the gap between spec and code.

**This finding warrants a follow-up Task before the PR is merged, or an inline fix.**

---

## Part III — Advisory Findings

### ⚠️ Finding A: Dynamic-readme partition corpus debt (170 non-compliant readmes)

`tools/maintenance/dynamic-readme-partition.py` ships at WARN-tier (advisory) because all 170 existing operational `readme.md` files lack the `<!-- BEGIN/END DYNAMIC -->` marker pair. The friction-log correctly notes "WARN-tier `M.B.6:missing-marker` does not gate."

However, MAINTENANCE.md §3.2 now says the dynamic section's content "MUST be sourced from the per-workspace trust-audit GATE output." This is a MUST-level obligation on every research `readme.md` — but the enforcement is advisory. The spec is ahead of the corpus. No follow-up Task has been filed to remediate the 170 missing markers.

**Recommendation:** File a Task for progressive corpus remediation (e.g., `tasks/NNN-dynamic-readme-corpus-remediation/`) before promoting the linter to gating tier. The Toolchain Flip SPEC §3.2 WARN→ERROR ladder requires the corpus to be clean before promotion; this Task would close that prerequisite.

---

### ⚠️ Finding B: ST-2 audit-graph ambiguity

`task.md` lists `research-staleness-decision-formalization` in `task_uses_prompts`. However, the friction-log correctly notes that ST-2 was "already complete on disk before dispatch — authored as the joint deliverable of Task 033 ST-2." The prompt was not executed by this Task's agent.

The audit-graph link (`task_uses_prompts: research-staleness-decision-formalization`) implies the prompt was *executed by this task*, which it was not. The correct relationship is `task_depends_on_research: spec-staleness-decision-formalization` or similar cross-task reference, but that frontmatter key does not exist in the current schema.

**Recommendation:** Add a `task_note` or prose comment in `task.md` clarifying the cross-Task consumption pattern. The frontmatter schema gap (no `task_depends_on_research` key) is a T3 change that warrants its own ADR or follow-up Task, not an inline fix.

---

## Part IV — Commendations

- **15 Gherkin scenarios** delivered across M.B.1–M.B.7 (≥7 required). The distribution (M.B.2×3, M.B.3×2, M.B.4×2, M.B.5×2, M.B.6×2, M.B.7×2) addresses the highest-complexity areas with multiple scenarios.
- **58/58 tests pass** (`pytest tools/tests/maintenance/ -q`).
- **`tools/check-governance.sh` exits 0** on the committed tree.
- **`PartitionGuard` test** is an exemplary pattern: enforcing schema-content equality between GATE and AGGREGATOR at test time prevents silent schema drift.
- **Falsification clause self-verification** in the friction-log is thorough and correctly traces every clause.
- **Footnote discipline on MorphLLM-Fast-Apply** correctly navigates the Task 040 §C constraint without silently including it as a dependency.
- **FL0 across the full 6-subtask chain** with an honest account of the shared-file additive merge coordination challenge.

---

## Summary

| Item | Status |
|---|---|
| Reviewer checklist item 1 (three-column table) | ✅ PASS |
| Reviewer checklist item 2 (MAINT_STALE_DAYS default) | ✅ PASS |
| Reviewer checklist item 3 (AGGREGATOR consumable) | ✅ PASS |
| M.B.7 tool-level enforcement in `fm/edit.py` | ❌ MUST-level gap |
| Dynamic-readme corpus remediation Task | ⚠️ Advisory |
| ST-2 audit-graph linkage accuracy | ⚠️ Advisory |

The critical finding (M.B.7) should be resolved — via inline fix or filed Task — before merging. The advisory findings are below the FL1 threshold and can be deferred.
