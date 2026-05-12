# Friction Log — Task 007 (Reconcile Closed-Task Linkage Drift)

Highest Friction Level: FL1

## Summary

Task execution went smoothly: the four problem clusters were unambiguous, the
strategy menu in `task.md` (A/B/C/D) named the trade-offs cleanly, and the
governance suite gave a deterministic green/red signal at every step.

The only friction was **strategy disambiguation for `prompt_relates_to_task`
reciprocity**. The original schema overloaded that field as both "task that
uses this prompt" (reciprocity required) and "task this prompt was spawned
from" (no reciprocity, just lineage). Strategies B and A both work; choosing
A required updating PROMPT.md §6.6 to state the *uses* semantics explicitly,
which felt heavier than a pure data fix. Spec writes for clarification took
roughly the same effort as Strategy B's schema extension would have, but
preserve a flatter L2 namespace.

## Recommendation (Governance)

Future "linkage drift" coherence findings should default to clarifying spec
semantics over extending the L2 namespace. The Layered Schema guideline in
TASK.md §3 implicitly favours flat, fewer-key designs; reflexively reaching
for new keys when reciprocity breaks would erode that.

## Provenance

Authored 2026-05-04 by `claude-code` on branch `claude/analyze-code-PfoLl` as
part of PR #27. The same PR delivered the fix.
