---
type: note
status: active
slug: 069-operationalise-adr-falsifier-triggers-friction-log
summary: "Friction log for Task 069. Audit-tool composition of bundle-size-snapshot landed cleanly; the audit itself surfaced two genuine ADR-0008 fires (F1 narrative-skill count, F2 bundle-token growth) which is the correct outcome — the brief's assumption of a clean baseline was already stale."
created: 2026-05-13
updated: 2026-05-13
---

# Task 069 — Friction Log

Highest Frustration Level: FL1

## Entries

### FL1 — Brief's "no trigger fires" baseline was already stale

The task brief asserted the audit should fire no trigger when run against HEAD ("ADR-0009 F1 should be ~70,676 tokens / 11 specs per the existing snapshot"). The audit ran honestly and surfaced two genuine ADR-0008 fires:

1. F1 (narrative-skill count > 10) — ADR-0008's prose claims "today: 6" but the on-disk count is 11 because the `novel-architect` corpus split into 5 sub-skills.
2. F2 (bundle > 60 K tokens) — the live bundle is ~77,859 tokens; ADR-0008's "~50 K" baseline predates Task 056/057/060 ratification work.

The friction is not in the audit — the audit did its job. The friction is in the brief / ADR drift: a measurement spec written 2 days ago is already outdated relative to its own thresholds. The audit's value proposition (a cheap, deterministic re-measurement) is reinforced by this exact behaviour, not undermined by it.

**Disposition:** maintainer reviews the ADR-0008 fires post-Task and decides between (a) successor ADR per the protocol, or (b) revising ADR-0008's thresholds (a T3 amendment requiring its own Task). Out of scope for Task 069.

### FL0 — Composition path worked cleanly

`adr-trigger-audit.py` composes `bundle-size-snapshot.py` via `importlib.util` (the dashed filename forbids `from … import …`). One small wrinkle: tests against a `tmp_path` repo would have failed to find the bundle script — fixed by having the audit's loader prefer the script colocated with itself before falling back to `<repo_root>/tools/maintenance/`. No friction beyond the initial test failure that exposed the issue.

### FL0 — F4 heuristic needed precision

First-pass F4 implementation grepped the whole task.md body for non-neutral root specs, which triggered a false positive on Task 088 (prose mention of `MAINTENANCE.md §1.0.1` in the summary, not in `task_affects_paths`). Tightened the scan to the `task_affects_paths:` YAML block via a one-line regex. No further drama.

## Patterns worth carrying forward

- ADR falsifier triggers benefit from a cheap re-measurement cadence: the moment the audit ran, two stale assumptions in the brief surfaced. This is exactly the pattern ADR-0008 / ADR-0009 ratified.
- Compose-over-duplicate paid off: the audit script is ~330 lines including formatters; the bundle-size logic remained in one place; the test that asserts `audit.run_audit(...).bundle_tokens == bss.measure_bundle(...).total_tokens` enforces the composition contract permanently.
