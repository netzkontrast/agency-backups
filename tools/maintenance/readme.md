---
type: index
status: active
slug: tools-maintenance
summary: "Linters and helpers that mechanise MAINTENANCE.md routines: stale-task audit (§3.4 — shipped), dynamic-readme partition (§3.2 — shipped), trust-audit aggregator (§5 — pending). Each emits diagnostics in the `<path>::<level>:<code>:<msg>` format consumed by `tools/check-governance.sh` and `tools/adr/runlog.py`."
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
| `trust-audit.py` | `MAINT.TRUST.*` | `MAINTENANCE.md §5` + `research/agentic-eval-trust-improvement-spec/output/SPEC.md` | Pending (Task 039 ST-5). |

All three linters run **advisory-tier** in `tools/check-governance.sh` (WARN-only, never gate). Promotion to gating requires a follow-up Task that resolves any pre-existing repo drift the linter flags.

## Linked Navigation

- [`staleness-audit.py`](./staleness-audit.py) — classifies each open Task into one of the four §3.4 lifecycle buckets per the deterministic decision tree in the staleness SPEC.
- [`dynamic-readme-partition.py`](./dynamic-readme-partition.py) — verifies the static/dynamic boundary marker pair (`<!-- BEGIN DYNAMIC -->` / `<!-- END DYNAMIC -->`) and section placement in every operational `readme.md` under `tasks/`, `research/`, `prompts/`. WARN-tier per the falsification mitigation in the Task 039 ST-4 brief: readmes lacking markers emit a single `missing-marker` advisory rather than an ERROR.
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
