---
type: note
status: active
slug: triage-note-superpowers-orchestration-cluster
summary: "Combined triage note for the Superpowers orchestration cluster: dispatching-parallel-agents, subagent-driven-development, requesting-code-review, executing-plans, writing-plans, code-reviewer agent. All adapt (D.1 + sometimes D.6); deconflict with Agency's Agent tool semantics."
created: 2026-05-12
updated: 2026-05-12
---

# Triage note — Superpowers "orchestration" cluster

Six Superpowers artefacts encode **multi-agent orchestration patterns**. Agency already exposes:

- The `Agent` tool (with `subagent_type` selector) — covers most "dispatch a subagent" patterns natively.
- Built-in `code-reviewer` agent type — covers most "request a review" patterns natively.
- The Task layer (`tasks/<NNN>-*/task.md`) — covers plan-write + plan-execute patterns natively.

Therefore each Superpowers artefact in this cluster `adapts` to **document the upstream pattern** in Agency-native vocabulary, rather than introducing a parallel orchestration framework.

## Files

| Snapshot path | KB | Landing slug | Adaptation hint |
|---|---|---|---|
| `skills/dispatching-parallel-agents/SKILL.md` | 5.2 | `superpowers-dispatching-parallel-agents` | Cite Agency's `Agent` tool with parallel tool-use; references/ examples ≤ 3 KB. |
| `skills/subagent-driven-development/SKILL.md` | 9.8 | `superpowers-subagent-driven-development` | Body ≤ 4 KB; two-stage review checklist → `references/two-stage-review.md`. |
| `skills/requesting-code-review/SKILL.md` | 2.6 | `superpowers-requesting-code-review` | Wrap Agency built-in `code-reviewer` invocation; no references/. |
| `skills/executing-plans/SKILL.md` | 1.9 | `superpowers-executing-plans` | Map to Agency Task layer's `## Plan` / `## Todo` sections. |
| `skills/writing-plans/SKILL.md` | 2.2 | `superpowers-writing-plans` | Map to Agency `sc-workflow` + Task `## Plan` template. Deconflict explicitly. |
| `agents/code-reviewer.md` | 1.8 | `superpowers-code-reviewer` | Document relation to Agency built-in `code-reviewer` agent type. |

## Adaptation plan (ST-3)

1. **Replace upstream "dispatch a fresh Claude session" language** with Agency's `Agent` tool + `subagent_type` parameter pattern.
2. **Replace upstream Task-Management vocabulary** with Agency's Task layer (`tasks/<NNN>-*/task.md` + `## Plan` + `## Todo` + frontmatter `task_status`).
3. **For `superpowers-code-reviewer`:** the SKILL.md MUST cite that Agency already exposes a `code-reviewer` agent type (see top of system prompt) and explain that this Superpowers variant is the **prompt template** for that built-in, not a competing implementation.
4. **For `superpowers-requesting-code-review`:** body MUST cite Agency's `Agent({subagent_type: "code-reviewer", ...})` invocation pattern.
5. **Slug deconfliction** (matrix rows 59, 64): `superpowers-brainstorming` ↔ `sc-brainstorm` and `superpowers-writing-plans` ↔ `sc-workflow`. Each SKILL.md MUST carry a `## Relation to Agency native skills` section.

## Audit-graph linkage

- All carry `skill_source: "superpowers@v4.0.3"`.
- Cross-edges:
  - `superpowers-dispatching-parallel-agents` → `[sc-task, sc-spawn-equivalent]` (note `sc-spawn` is `skip` so no edge there)
  - `superpowers-subagent-driven-development` → `[superpowers-code-reviewer, sc-task]`
  - `superpowers-requesting-code-review` → `[superpowers-receiving-code-review]`
  - `superpowers-executing-plans` → `[sc-task, sc-implement]`
  - `superpowers-writing-plans` → `[sc-workflow, sc-task]`
  - `superpowers-code-reviewer` → `[superpowers-requesting-code-review]` (built-in `code-reviewer` is referenced in body, not in graph).

## Tier assignment

- L2: `superpowers-requesting-code-review`, `superpowers-executing-plans`, `superpowers-writing-plans`, `superpowers-code-reviewer`.
- L3: `superpowers-dispatching-parallel-agents`, `superpowers-subagent-driven-development` (orchestrate over L2 cluster).
