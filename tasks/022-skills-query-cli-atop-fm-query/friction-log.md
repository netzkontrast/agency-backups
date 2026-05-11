---
type: note
status: active
slug: friction-log-022
summary: "Friction log for Task 022 — skills-query wrapper ships clean; one FL1 deviation from the original plan (upstream SPEC is T4-immutable)."
created: 2026-05-11
updated: 2026-05-11
---

# Friction Log — Task 022

Highest Frustration Level: FL1

## Summary

Shipped [`tools/fm/skills_query.py`](../../tools/fm/skills_query.py): a thin convenience wrapper that answers Task 010's ten canonical questions by composing the stateless `fm-query`, `fm-extract`, and `fm-graph` CLIs. No persistent index file; no `.agent_cache/` writes; every subcommand caps stdout at 1 KB. Smoke-wired into `tools/check-governance.sh` step `[5c]`. 15 tests in `tools/tests/fm/test_skills_query.py`, all green; full governance suite exits 0.

## FL1 — Deviation from Task 022 plan step 4

The Task plan said *"Add a section to `research/flexible-frontmatter-toolchain/output/SPEC.md` §C — keep the supersession note explicit; record the wrapper's existence as the v2 fulfilment of Task 010."*

That spec has `research_phase: complete`. Per `MAINTENANCE.md §1`, a `complete` research workspace is T4-immutable for body content; the closed-research repair allowance ([Task 059](../059-closed-research-repair-allowance/)) explicitly permits T1 (`updated:` bumps) and T2 (broken-link repair) only. Appending a new `## §C` heading is a T3 structural change and would violate the immutability rule.

Resolution: the v2 fulfilment note now lives Task-side at [`./v2-fulfilment.md`](./v2-fulfilment.md), with the rationale, the full Q→composition map, the invariants, and the token-cost record. The upstream SPEC's existing supersession statement in §2 already declares the v1 strategy retired; the Task-side note is the v2 *fulfilment* artefact (downstream evidence, not normative spec content).

This deviation was logged FL1 because it required a small re-think mid-Task and a follow-up reflexion. No code lost.

## Observations

- `fm-graph --detect orphans,dangling` exits non-zero whenever it surfaces WARN findings — that is intended behaviour, not an error. The wrapper's `_run_tool` carries an `allow_nonzero=True` flag for diagnostic subcommands so the wrapper still returns the report instead of propagating the exit code.
- Slug resolution is ambiguous in the live tree (the same slug commonly appears in `readme.md`, `task.md`, and the spawning `prompt.md`). The wrapper applies a file-priority order (`task.md` > `SKILL.md` > `output/SPEC.md` > `prompt.md` > `readme.md`) to pick the right body for `header`/`summary` queries. Documented in [`./v2-fulfilment.md`](./v2-fulfilment.md) §Invariants.
- The 1 KB cap dominates matrix queries (`graph`, `manifest`). Callers can pass `--limit` upstream via `fm-query` for tighter scope; the wrapper doesn't re-expose `--limit` to keep the surface minimal.

## Trust dimensions (Spec-J/K/L)

- **Schema integrity:** PASS — wrapper consumes the canonical `header-ontology.json` indirectly through `fm-*`; no second source of truth.
- **Behavioural integrity:** PASS — 15/15 tests green; full check-governance.sh suite passes; smoke `[5c]` succeeds.
- **Governance integrity:** PASS — original SPEC body untouched (T4 preserved); supersession statement preserved; Task 010's questions answerable in O(walk).

No follow-up Task warranted.
