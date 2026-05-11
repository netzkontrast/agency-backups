---
type: index
status: active
slug: novel-architect-mif-learnings-sessionhook
summary: "Directory index for Task 077 — adopt MIF Level 3 schema for learnings.md AND ship a lean SessionStart-Hook in novel-architect."
created: 2026-05-11
updated: 2026-05-11
---

# Task 077 — MIF Level 3 learnings + SessionStart-Hook (lean)

**What:** Couples two Dual-Kernel patterns: structured memory traces (MIF Level 3 subset) for learnings.md, plus a lean SessionStart-Hook script that loads project-config and surfaces recent learnings at session-start.

**Why here:** v1.0.0's append-only learnings.md has no decay, no classification, no derivation chain. MIF Level 3 (subset) adds structure without the over-engineering of full ML-trace schemas. The SessionStart-Hook makes the learnings actually surface — they're useless if no agent reads them at session-start.

## Navigation

- [task.md](./task.md) — Task spec covering both schema + hook.

## Assumptions Log

- Full mnemonic system integration (semantic/episodic/procedural namespaces, /mnemonic:capture command) is **explicitly out-of-scope** for v1.1.0 — deferred to v1.2.0+. This task ships the *schema* and a *lean hook* only.
