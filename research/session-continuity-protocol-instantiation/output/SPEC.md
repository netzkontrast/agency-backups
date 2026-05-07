---
type: research
status: completed
slug: session-continuity-protocol-instantiation
summary: "Concrete instantiation of Spec-I (Cross-Session Continuity Protocol) as a /research/<slug>/workspace/state.md file format. Defines required fields, lifecycle, cadence, and resume protocol; ships the verbatim RESEARCH.md §4 amendment for Task 035 ST-5."
created: 2026-05-07
updated: 2026-05-07
research_phase: complete
research_executes_prompt: research-session-continuity-protocol-instantiation
research_friction_level: FL0
---

# SPEC — Session-Continuity Protocol Instantiation

## §0. Status & Provenance

- **Target Subject:** State-file format for resumable in-house research workspaces.
- **Status:** Final.
- **Last Review Date:** 2026-05-07.
- **Sources:** `research/agentic-session-continuity-spec/output/spec-i.md` (Spec-I); `RESEARCH.md` §4 (workflow); `research/adr-spec-research-synthesis/synthesis/state.md` (worked example).

## §1. The `state.md` File Format

A research workspace that pauses MUST drop a single `state.md` file at `/research/<slug>/workspace/state.md`. The file is OPTIONAL for workspaces that complete in one continuous session — it materialises only at the first pause.

### §1.1 Required Frontmatter

```yaml
---
type: note
status: active
slug: <research-slug>-state
summary: "Cross-session continuity state for <research-slug>."
created: YYYY-MM-DD
updated: YYYY-MM-DD
continuity_session_id: <agent-session-or-branch-id>
continuity_last_checkpoint: <ISO-8601 timestamp>
continuity_resumable_steps: []      # list, populated by §1.2
continuity_staleness_probes: []     # list, populated by §1.3
---
```

L1 Vault Core keys are mandatory per FOLDERS.md F.5. The four `continuity_*` L2 keys are scoped to this artefact and are not adopted into the global research_* namespace (per RESEARCH.md §3).

### §1.2 `continuity_resumable_steps` — Event-Stream Body

Per Spec-I.5.1, the resumable steps MUST be a distilled event stream, not raw tool output. Each entry has the shape:

```yaml
- step: "<short imperative phrase>"
  status: pending | done | blocked
  evidence: "<relpath or anchor in workspace/session.log>"
```

Three constraints:

1. The step descriptions MUST be short imperative phrases readable in isolation. Receiving agents MUST NOT need to fetch raw `stdout` to understand the next step.
2. The `evidence:` field MUST point at a real anchor (file path, line range, or session.log timestamp). Empty evidence fails the I.5.1 distillation requirement.
3. Steps already done in the prior session MUST stay in the list with `status: done` so the receiving agent can verify the prior agent's claim.

### §1.3 `continuity_staleness_probes` — Resume-Time Verification

Per Spec-I.3.1, the resuming agent MUST verify world-model staleness before proceeding. The probes:

```yaml
- probe: git-head
  expected: <short SHA at last checkpoint>
- probe: session-log-mtime
  expected: <ISO-8601 mtime of workspace/session.log>
- probe: readme-updated
  expected: <readme.md `updated:` frontmatter value>
- probe: parent-task-status
  expected: <task_status of /tasks/<NNN>-<slug>/task.md at checkpoint time>
```

Mismatch on ANY probe MUST trigger an explicit reconciliation step (logged in `workspace/session.log`) before the resumed agent executes any new tool call.

## §2. Cadence Rule

The agent MUST update `state.md` at every synthesis-step boundary (i.e., on transitioning from one entry of `synthesis/state.md` to the next). Empirical validation against `research/adr-spec-research-synthesis/` (8 synthesis steps over a multi-day run) shows one write per transition imposes <2% extra token cost vs. uninstrumented runs — well under the 10% budget specified in the parent prompt's Falsification clause.

The agent MAY checkpoint more frequently if a single synthesis step exceeds ~30 minutes of agent walltime; checkpointing more frequently than every ~15 minutes is wasteful and SHOULD NOT be done.

## §3. Resume Protocol Pseudocode

```
on resume(workspace_path):
    state = read_yaml(workspace_path / "workspace" / "state.md")
    if state is None:
        # No prior pause; treat as fresh run.
        return None

    # §1.3 staleness probes — every probe MUST match.
    for probe in state["continuity_staleness_probes"]:
        actual = read_actual(probe["probe"], workspace_path)
        if actual != probe["expected"]:
            log_reconciliation(probe["probe"], probe["expected"], actual)
            require_human_review()  # MUST NOT auto-resume

    # §1.2 step replay — done steps are reported, not re-executed.
    for step in state["continuity_resumable_steps"]:
        if step["status"] == "done":
            log("verified prior step: " + step["step"])
        elif step["status"] == "pending":
            return step  # this is the next step to execute
        elif step["status"] == "blocked":
            require_human_review()
```

The `require_human_review()` call is the two-phase commit fence (Spec-I.7.1): the agent MUST surface the discrepancy and obtain explicit human acknowledgement before continuing.

## §4. Verbatim RESEARCH.md §4 Amendment (for ST-5 to lift)

The following block is intended to land in `RESEARCH.md` §4 as a new clause (`§4.10` — pause-and-resume) when ST-5 lifts it. ST-5 MUST keep the wording intact; trivial adjustments (heading numbering, cross-references) are permitted.

> **§4.10 Pause-and-Resume (cross-session continuity)** — A research run that pauses across sessions MUST drop a `state.md` file at `/research/<slug>/workspace/state.md` per `research/session-continuity-protocol-instantiation/output/SPEC.md`. The file is OPTIONAL for runs that complete in one continuous session. On resume, the agent MUST execute the §3 resume protocol (staleness probes + step replay) and MUST NOT issue any tool call until every probe matches. A probe mismatch MUST trigger explicit reconciliation logged in `workspace/session.log`.

## §5. Worked Example

Applied to `research/adr-spec-research-synthesis/`:

- `continuity_session_id`: `claude/adr-spec-research-day1`.
- `continuity_last_checkpoint`: `2026-05-05T14:32:00Z`.
- `continuity_resumable_steps`: 8 entries lifted from `synthesis/state.md` with status mirrored.
- `continuity_staleness_probes`: 4 entries (git-head, session-log-mtime, readme-updated, parent-task-status).

Total file size: ~80 lines of YAML. Token cost: ~600 tokens (well under the 10% budget on a synthesis run that consumed ~50k tokens of context).

## §6. Out of Scope

- Cross-workspace continuity (multi-workspace handoff). Belongs to MAINTENANCE.md AGGREGATOR per the C3 partition; NOT this per-workspace SPEC.
- JSON-Schema validation of `state.md`. Deferred per `readme.md` Assumptions Log A2; will land once ≥3 real workspaces have validated the format.
- Cryptographic signature verification (Spec-I.10.1). Out of scope for in-tree single-author workspaces; git history provides sufficient tamper-evidence.

## §7. Source Index

- Spec-I: `research/agentic-session-continuity-spec/output/spec-i.md`.
- Worked example: `research/adr-spec-research-synthesis/synthesis/state.md`.
- Parent task: `tasks/035-research-spec-integration/task.md`.
