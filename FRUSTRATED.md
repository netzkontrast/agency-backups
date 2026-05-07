# Agent Frustration & Friction Specification

To continuously improve prompts, tooling, and repository structure, we require agents to self-report friction and frustration encountered during any session.

Agents MUST use the following **Frustration Levels (FL)** when logging their experience in the designated `friction-log.md` (or equivalent session logs). **This log is MANDATORY for every session.**

## Why FL0 is mandatory (rationale)

An FL0 entry is a *falsifiable null-baseline declaration* — "I executed this run and observed no friction". Absent that declaration, the maintenance run cannot distinguish "no friction occurred" from "the agent forgot to log", which destroys the denominator for every friction-frequency metric. Empirical evidence: 38% of the 60 friction logs in the repo at 2026-05-07 are FL0; if FL0 were optional, half the population would silently disappear from longitudinal analysis. FL0 entries also carry semantic content (e.g. the "plan obsolesced cleanly" supersession pattern, observed in 6 of 23 FL0 entries). Logging FL0 is *cheap* — one line — and it is the cheapness that makes the discipline sustainable. The friction the rule causes for agents is acknowledged; the friction the rule prevents (silent corpus drift) is larger. See [`research/fl0-value-justification/output/SPEC.md`](./research/fl0-value-justification/output/SPEC.md) §3 for the full upstream-consumer enumeration.

## Frustration Levels Defined

### FL0 — Zero Friction
- **Definition:** The task proceeded exactly as expected. Instructions were clear, tools worked flawlessly, and no backtracking was required.
- **Action:** Briefly state that the execution was perfectly aligned with the prompt. **You must still write the log even if the status is FL0.**

### FL1 — Minor Annoyance
- **Definition:** The agent encountered minor ambiguities, syntax issues in the prompt, or had to execute repetitive tool calls to format data. The task was completed without needing to fundamentally alter the plan.
- **Action:** Document the specific ambiguity or repetitive task. Suggest a minor prompt or process tweak.
- **Example:** "Having to manually reconstruct a `session.log` from memory because an automatic script wasn't provided."

### FL2 — Significant Frustration
- **Definition:** The agent experienced conflicting instructions, had to significantly backtrack to retrofit work due to shifting constraints, or encountered tooling/dependency failures that required substantial diagnostic effort to bypass.
- **Action:** Clearly identify the exact conflicting instructions or tooling failures. Provide a concrete recommendation for how the initial prompt or environment must be restructured to prevent this.
- **Example:** "The initial prompt demanded a monolithic file, but a later prompt demanded a deep directory structure, forcing a tedious teardown and rebuild of the data."

### FL3 — Task Blocker / Extreme Frustration
- **Definition:** The agent is stuck in a loop, the instructions are fundamentally impossible to execute within the sandbox, or environmental errors prevent the completion of the core objective.
- **Action:** Halt normal execution. Log the FL3 status, document the exact point of failure, and request human intervention.

## Special Triggers
- **Structural Bloat / Micromanagement:** If a prompt demands deeply nested folder structures with less than 3 files per folder, or requires tedious administrative overhead (e.g., updating a `readme.md` for every single minor file change *instead of batching them at the pre-commit stage*), the agent MUST log this as FL2. This administrative burden distracts the LLM's context window from actual logic and code generation.

## When and How to Log (Mandatory)
1. **Research Tasks (FL.Log.1):** You MUST create or update `/reflection/friction-log.md` at the **end** of the session (during the pre-commit phase), explicitly declaring your highest FL experienced during the run at the top of the file (e.g., `Highest Frustration Level: FL2`).
2. **Standard Tasks (FL.Log.2):** You MUST include a section named `## Frustration Log` in your final PR description or submit message.

## Mechanical Enforcement

The FL declaration is mechanically validated by [`tools/check-fl-declaration.py`](./tools/check-fl-declaration.py). The linter accepts the canonical line `Highest Frustration Level: FL[0-3]` plus the documented variant forms in [`research/fl0-value-justification/output/SPEC.md`](./research/fl0-value-justification/output/SPEC.md) §2.2 (covering ~14 surface forms found in the historical corpus). It runs WARN-tier under `tools/check-governance.sh` by default; set `FM_FL_DECLARATION_STRICT=1` to gate the suite once the historical malformed logs (tasks 030, 033) are remediated. Diagnostic format: `<relpath>::ERROR:FR.B.4:<missing|malformed>:<details>`.

## Acceptance Scenarios (Gherkin)

```gherkin
# anchor: FR.B.1 — closing-run FL declaration
Feature: Every closed task carries an FL declaration in canonical format
Scenario: Task transitions to done with a parseable FL declaration
  Given a task folder `tasks/<NNN>-<slug>/` whose `task.md` carries `task_status: done`
  And `tasks/<NNN>-<slug>/friction-log.md` exists with a parseable declaration line
        matching one of the variant forms in SPEC §2.2
  When `tools/check-fl-declaration.py tasks/<NNN>-<slug>/` runs
  Then the linter MUST exit 0
  And no diagnostic is emitted
```

```gherkin
# anchor: FR.B.2 — Special-trigger bloat
Feature: Per-file readme spam triggers FL2
Scenario: Agent encounters per-file readme update demand
  Given the prompt asks the agent to update `readme.md` for every single file change
        rather than batching the readme audit at the pre-commit stage
  And the agent observes the resulting administrative overhead
  When the agent authors the closing friction-log
  Then the friction-log MUST declare `Highest Frustration Level: FL2`
  And the log body MUST cite the per-file vs batch distinction (FRUSTRATED.md §28)
  And the log body MUST recommend a concrete restructuring of the originating prompt
```

```gherkin
# anchor: FR.B.3 — FL.Log surface routing
Feature: Research runs vs standard tasks log to different surfaces
Scenario Outline: Surface routing by run type
  Given a session of type <run_type>
  When the agent reaches the closing-run phase
  Then the FL declaration MUST land at <surface>
  And `tools/check-fl-declaration.py` MUST accept that surface

  Examples:
    | run_type        | surface                                              |
    | research        | /research/<slug>/reflection/friction-log.md          |
    | standard task   | tasks/<NNN>-<slug>/friction-log.md                   |
    | standard task   | the PR description's `## Frustration Log` section    |
```

```gherkin
# anchor: FR.B.4 — missing-log rejection (default WARN-tier)
Feature: FL-declaration linter surfaces malformed/missing closures
Scenario: Default invocation emits an advisory diagnostic, no commit block
  Given a Task transitions `task_status: in_progress` → `task_status: done`
  And the staged commit modifies `tasks/<NNN>-<slug>/task.md` accordingly
  And neither `tasks/<NNN>-<slug>/friction-log.md` carries a parseable declaration
        nor the PR description contains a `## Frustration Log` section with one
  And the environment does NOT export `FM_FL_DECLARATION_STRICT=1`
  When `tools/check-fl-declaration.py` runs as part of `tools/check-governance.sh`
  Then the linter MUST emit `<relpath>::ERROR:FR.B.4:missing:<details>` to stderr
  And `tools/check-governance.sh` MUST still exit 0 (the diagnostic is advisory)
  And the maintainer MAY land the commit with the diagnostic visible
```

```gherkin
# anchor: FR.B.4.STRICT — missing-log rejection (gating mode)
Feature: Strict-mode promotes the FL declaration check to a gate
Scenario: Strict-mode invocation blocks the commit
  Given the same closing-run conditions as FR.B.4
  And the environment exports `FM_FL_DECLARATION_STRICT=1`
  When `tools/check-fl-declaration.py` runs as part of `tools/check-governance.sh`
  Then the linter MUST exit 1 with diagnostic `<relpath>::ERROR:FR.B.4:missing:<details>`
  And `tools/check-governance.sh` MUST exit non-zero
  And the commit MUST be blocked until an FL declaration is added
  And the strict-mode flip is gated on remediation of historical malformed logs
        (tasks 030, 033 — see `tasks/062-frustrated-spec-followup-ac1-ac5/task.md`)
```

## Frustration Log

**Highest Frustration Level: FL0**

This spec carries an example FL declaration so the file itself satisfies the
canonical form for self-test purposes.
