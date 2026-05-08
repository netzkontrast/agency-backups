---
type: index
status: active
slug: tools-maintenance
summary: "Linters and helpers that mechanise MAINTENANCE.md routines: stale-task audit (§3.4 — shipped), dynamic-readme partition (§3.2 — shipped), trust-audit aggregator (§3.2 / §3.3 — shipped). Each emits diagnostics in the `<path>::<level>:<code>:<msg>` format consumed by `tools/check-governance.sh` and `tools/adr/runlog.py`."
created: 2026-05-08
updated: 2026-05-08
---

# `tools/maintenance/` — Maintenance-Routine Linters

This folder houses the mechanised counterparts of the prose maintenance routines defined in [`MAINTENANCE.md`](../../MAINTENANCE.md). Each script in this folder is a pure-stdlib (+ optional PyYAML) reader that applies one §-bound algorithm to the task / research corpus and emits diagnostics in the canonical `<path>::<level>:<code>:<msg>` format that `tools/check-governance.sh` aggregates.

## What and Why

The Nightly Maintenance Run and Repo Coherence Check (per `MAINTENANCE.md §2` and §3) used to be human-only routines. Three subtasks of [Task 039 — MAINTENANCE.md Spec Integration](../../tasks/039-maintenance-spec-integration/task.md) lift the deterministic parts of those routines into linters that can run inside `tools/check-governance.sh`:

| Linter | Anchors | Spec source | Status |
|---|---|---|---|
| [`staleness-audit.py`](./staleness-audit.py) | `MAINT.STALE.*` | [`MAINTENANCE.md §3.4`](../../MAINTENANCE.md) + [`research/spec-staleness-decision-formalization/output/SPEC.md §1`](../../research/spec-staleness-decision-formalization/output/SPEC.md) | Shipped (Task 039 ST-3). |
| [`dynamic-readme-partition.py`](./dynamic-readme-partition.py) | `M.B.6:*` | [`MAINTENANCE.md §3.2`](../../MAINTENANCE.md) + [`research/repo-maintenance-protocol-spec/output/SPEC.md §3.1`](../../research/repo-maintenance-protocol-spec/output/SPEC.md) | Shipped (Task 039 ST-4). |
| [`trust-audit.py`](./trust-audit.py) | `MAINT.TRUST.*` (incl. `MAINT.TRUST.FRICTION`) | [`MAINTENANCE.md §3.2 / §3.3`](../../MAINTENANCE.md) + [`research/agentic-eval-trust-improvement-spec/output/SPEC.md`](../../research/agentic-eval-trust-improvement-spec/output/SPEC.md) (Spec-J/K/L) | Shipped (Task 039 ST-5). Cross-research AGGREGATOR; imports the per-workspace GATE shipped by Task 035 ST-4 (`tools/check-trust-audit.py`) — never re-implements its scoring logic (C3 partition). |

All three linters run **advisory-tier** in `tools/check-governance.sh` (WARN-only, never gate). Promotion to gating requires a follow-up Task that resolves any pre-existing repo drift the linter flags.

## Linked Navigation

- [`staleness-audit.py`](./staleness-audit.py) — classifies each open Task into one of the four §3.4 lifecycle buckets per the deterministic decision tree in the staleness SPEC.
- [`dynamic-readme-partition.py`](./dynamic-readme-partition.py) — verifies the static/dynamic boundary marker pair (`<!-- BEGIN DYNAMIC -->` / `<!-- END DYNAMIC -->`) and section placement in every operational `readme.md` under `tasks/`, `research/`, `prompts/`. WARN-tier per the falsification mitigation in the Task 039 ST-4 brief: readmes lacking markers emit a single `missing-marker` advisory rather than an ERROR.
- [`trust-audit.py`](./trust-audit.py) — cross-research AGGREGATOR (C3 partition) for the per-workspace trust-audit GATE. Iterates every `research/<slug>/` workspace at `research_phase: complete`, invokes the GATE's `audit()` callable by import (not subprocess), and rolls findings into a single MAINTENANCE.md §3.2 / §3.3 friction-aggregation report. FL≥1 trust failures emit a `MAINT.TRUST.FRICTION` recommendation for Task creation (delegated, never auto-created). Surface: `python3 tools/maintenance/trust-audit.py [--threshold-mode strict|advisory] [--format text|json] [--write-runlog]`.
- [`../tests/maintenance/`](../tests/maintenance/) — pytest suites for the linters in this folder.

## How a Linter in this Folder Behaves

1. Reads `MAINTENANCE.md`-relevant configuration from environment variables (e.g. `MAINT_STALE_DAYS`).
2. Walks `tasks/` (or `research/`) using `tools/fm/_core.py` for frontmatter parsing — never duplicates the YAML reader.
3. Applies the SPEC algorithm and emits one diagnostic line per finding to stdout in the form:

    ```
    <path>::<level>:<code>:<message>
    ```

   compatible with `tools/check-maintenance-bypass.py` consumption.
4. Writes one summary line to stderr.
5. Exits `0` on no findings, `2` on advisory findings (WARN), `1` on usage error. The shell wrapper in `check-governance.sh` swallows exit code 2 with `|| true` so the suite stays green during the migration window.

## Assumptions Log

- The audit-time signal extraction in `staleness-audit.py` is purely a function of `HEAD` (filesystem + frontmatter) — it does NOT shell out to `git grep`. The SPEC §2 S4/S5 recipes were translated into in-process readers to avoid forking `git` from inside `check-governance.sh`. Equivalence with the SPEC's `git grep`-based recipes is preserved by walking the same files (the eight root specs for S4; every `tasks/*/task.md` for S5).
- The linter MAY skip closed Tasks (`task_status` ∈ {`done`, `archived`, `abandoned`, `superseded`}) entirely; only `task_status: open` and `in_progress` participate in the §3.4 audit per the SPEC's "active task corpus" framing.
- The §3.4 audit is **observational** — it never mutates Task files. Bucket *remediation* is a separate workflow governed by `MAINTENANCE.md §3.4` (T3 in most cases) and is outside this linter's scope.
- The trust-audit AGGREGATOR is **schema-locked** to the per-workspace GATE: it imports `DIAGNOSTIC_SCHEMA` and the `audit()` callable from `tools/check-trust-audit.py` rather than re-implementing Spec-J/K/L. A regression test in `tools/tests/maintenance/test_trust_audit_aggregator.py::SchemaLockStep` asserts identity of the schema object so any future threshold change in the GATE flows through to the AGGREGATOR automatically. The `PartitionGuard` test additionally asserts the AGGREGATOR module exposes no `_score_*` helpers — surfacing C3-partition violations at test time.
- The AGGREGATOR's selection criterion (`research_phase: complete` line scan) intentionally mirrors the shell glob in `tools/check-governance.sh`'s per-workspace step, so the GATE and the AGGREGATOR see identical workspace sets. A workspace newly closed between the two steps will be picked up by the AGGREGATOR but not the GATE in that single run; the next run reconciles.
