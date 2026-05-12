---
type: index
status: active
slug: retire-novel-architect-legacy
summary: "Directory index for Task 084 — placeholder retirement Task for skills/novel-architect-legacy. Blocked by Task 083 plus productive-session evidence. Filed now (not at-need) so the retirement contract is discoverable."
created: 2026-05-12
updated: 2026-05-12
---

# Task 084 — Retire novel-architect-legacy

**What:** Placeholder Task that retires the legacy v0.3.3-archived skill once Task 070's three preconditions all hold. Currently `task_status: blocked`; criterion (c) already mechanically satisfied.

**Why here:** A future agent doing a "cleanup unused skills" sweep would notice `skills/novel-architect-legacy/` is `status: archived` and might propose deletion without knowing the retirement criteria. This Task makes those criteria machine-discoverable (search `tasks/` for `retire-novel-architect-legacy`) and gates the actual deletion behind verifiable evidence (≥3 productive sessions + NCP-validation).

## Navigation

- [`task.md`](./task.md) — Task spec: Goal, Retirement Preconditions (verification commands for a/b/c), Plan, Todo, Links.

## Assumptions Log

- Criterion (c) is mechanically satisfied at filing time; the verification command in task.md returns 0 hits against the repo at `2a85657`. Re-verification at unblock time is mandatory.
- The migrated Kohärenz Protokoll workspace lives at `/home/claude/novel-projects/kohaerenz-protokoll/` on the host where productive sessions run. The dev-shell that filed this Task cannot validate (a) or (b) — they require the runtime host.
- The legacy skill is preserved in git history; removal at retirement is `git rm`, not file deletion, so the snapshot remains recoverable if the criteria turn out to be wrong.
