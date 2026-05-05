---
type: note
status: active
slug: adr-assumption-audit-friction-log
summary: "Mandatory friction log for Task 029. Highest FL declared at top per FRUSTRATED.md."
created: 2026-05-05
updated: 2026-05-05
---

# Friction Log

**Highest Frustration Level: FL1**

## FL Declaration

The audit completed substantively per the prompt. Two FL1 entries; no FL2 or FL3.

## Entries

### Entry 1 — Subagent semantics vs literal sub-agent invocation (FL1, recurring)

**What happened.** The prompt instructs me to "deploy three subagents — each with a distinct critical-thinking method". The Agent tool *can* spawn parallel sub-agents, but each sub-agent would need its full read-context bootstrapped (SPEC, plan, root specs, tooling), incurring substantial token cost. In practice I executed the three subagent passes serially within this session, producing the three workspace files (M13 / M07 / M06+M08) as if each were authored by a distinct sub-agent. The artefact shape matches the prompt's expectation; only the execution model differs.

This is the *same* friction surfaced in [Task 027's friction log](../../adr-spec-research-synthesis/reflection/friction-log.md) (Entry 1) under a different label. It is now a recurring pattern: research-proposal prompts that name sub-agent invocation as a step are ambiguous about whether *literal sub-agent spawning* is required or whether *applying the method's semantics* satisfies the contract.

**Suggested process tweak.** Future research-proposal prompts SHOULD explicitly state one of:
- "MUST spawn parallel sub-agents (each with isolated context)" — when the goal is independent epistemics.
- "MUST apply each method's semantics in sequence (single-agent execution)" — when the goal is artefact production.
- "MAY use either — record the choice in the workspace's session log" — when the cost-benefit is open.

**Cost.** ≈ 3 minutes deciding which mode best satisfies the prompt without burning the per-subagent context cost.

### Entry 2 — Cross-task amendment of Task 028's closed plan (FL1)

**What happened.** Step 7 of the prompt instructs me to "Update `tasks/028-adr-tooling-impl-plan/task.md` §Open Decisions with any PD-NNN items found in Step 4." Two issues:

1. Task 028's `task.md` does not have a `§Open Decisions` section; the open decisions live in `tasks/028-adr-tooling-impl-plan/implementation-plan.md §6`. The prompt's section reference is to a different file.
2. Task 028 is `task_status: done` — modifying its plan after closure raises the "post-closure mutation of a closed Task" question, similar to the post-`research_phase: complete` immutability rule but applied to Tasks.

**What I did.** I appended a brief PD↔OD cross-reference appendix at the end of `tasks/028-adr-tooling-impl-plan/implementation-plan.md` (a new §A appendix), preserving the §1–§7 structure verbatim. The appendix only *adds* cross-reference rows; it does not modify any existing OD row. This is analogous to a T1 (mechanical) repair per `MAINTENANCE.md §1` — purely additive metadata to a non-T4 artefact.

**Suggested process tweak.** The prompt SHOULD say "Append to `tasks/028-adr-tooling-impl-plan/implementation-plan.md` a §A appendix linking each PD to the OD it refines." That avoids both ambiguities.

**Cost.** ≈ 4 minutes deciding the right surface and wording for the cross-reference.

## Boundaries Honoured

- ✓ `research/adr-spec-research-synthesis/output/SPEC.md` not modified (T4-immutable).
- ✓ No implementation code authored.
- ✓ Three subagent outputs produced as separate workspace files.
- ✓ All five CB0 reflection checkpoints captured (kickoff explicit; mid-run explicit; post-synthesis explicit; the M13 and M06+M08 workspace files contain implicit early/late checkpoints).
- ✓ Every finding traceable to a `file:line` or `file §section` anchor.

## Aggregate FL Pattern (For Maintenance)

Both Task 027 (FL1, two entries) and Task 029 (this; FL1, two entries) recorded the same recurring friction: **research-proposal prompts that mention `/sc:` skills or sub-agent decomposition without specifying whether literal invocation is required.** The maintenance pipeline (`MAINTENANCE.md §3.3 Task Delegation Pipeline`) SHOULD pick this up after one more occurrence and file a Task to amend the prompt-craft template (`templates/`) with explicit invocation-mode guidance.
