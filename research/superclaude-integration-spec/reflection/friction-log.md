---
type: note
status: active
slug: superclaude-integration-spec
summary: "Friction log: FL1 for /todo/ vs /tasks/ structural contradiction."
created: 2026-05-04
updated: 2026-05-04
---

# Friction Log

**Highest Frustration Level: FL1**

## FL1 — Minor: /todo/ vs /tasks/ Contradiction in MAINTENANCE.md

**Observed**: `MAINTENANCE.md §3` instructs maintenance agents to place delegation prompts in `/todo/` (e.g., `/todo/fix-api-rate-limits/prompt.md`). However, `FOLDERS.md §7` explicitly states: "MUST NOT create operational folders outside `/tasks/`, `/prompts/`, `/research/`."

**Impact**: A maintenance agent following MAINTENANCE.md literally would violate FOLDERS.md.

**Resolution taken**: Updated MAINTENANCE.md §3 to reference `/prompts/` as the delegation target, aligning with FOLDERS.md §7. Filed follow-up prompt `maintenance-todo-audit` to ratify this change.

**Recommendation**: A formal audit SHOULD be conducted to confirm no other /todo/ references exist and to ratify the MAINTENANCE.md §3 correction.

## FL0 — General Execution

All Agency governance specs were clear, well-structured, and mutually consistent (modulo the /todo/ issue). SuperClaude CLAUDE.md and KNOWLEDGE.md provided explicit gap analysis which made the integration mapping straightforward. No backtracking required.
