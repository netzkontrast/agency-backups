# Agent Instructions

Welcome, agent. This repository manages development and deep research tasks.

**Before committing any work:** You MUST review and abide by the checks defined in [PRE_COMMIT.md](./PRE_COMMIT.md).

## Folder Management & Workflow Drift
You MUST abide by the rules defined in [FOLDERS.md](./FOLDERS.md).
**Preventing Workflow Drift:** To prevent this repository's protocols from slowly drifting out of sync with reality, you are required to document your assumptions. If you assumed a certain file should be JSON instead of Markdown, or if you assumed a specific subfolder was unnecessary, you MUST log that assumption in the relevant folder's `readme.md`. This ensures human operators and future agents understand *why* the repository looks the way it does.

## Mandatory Frustration Feedback
We rely on your honest feedback to improve these protocols. You MUST consult [FRUSTRATED.md](./FRUSTRATED.md) to accurately log the Frustration Level (FL) associated with your task. **This is a mandatory step for every session, even if everything went perfectly (FL0).**

## Research Tasks
If your initial request or prompt is a **Research Task**, you must consult the [RESEARCH.md](./RESEARCH.md) file located in the root of this repository before proceeding. `RESEARCH.md` details the strict directory structure, required artifact logging, and output expectations for all research-oriented tasks.
## Current State
- Output exists in `research/agent-prompt-specs-3-systems-sdd/output/SPEC.md`
- Needs audit against RISE-DX constraints.

## LOOP_LOG
<!-- Jules appends one record per iteration. Do not edit manually. -->

### Iteration 0 — 2026-05-02
- Status: Loop initialized
- Work artifact: research/agent-prompt-specs-3-systems-sdd/output/SPEC.md
- Verification command: `cat research/agent-prompt-specs-3-systems-sdd/output/SPEC.md | grep -E "(MUST|SHOULD|MAY)"`
- Max iterations: 5

### Iteration 1 — 2026-05-02
- Dimension targeted: Completeness
- What was wrong: Step S6.a (Schema-Gap Hypothesis) was not properly documented in the Cross-Pollination Log and Contradiction Log.
- What changed: Added explicit Schema-Gap Hypothesis for "Failure Recovery / Error Handling" to both logs.
- Verification: PASS
- Next candidate (if known): Multiple RFC 2119 keywords in single normative statements.

### Iteration 2 — 2026-05-02
- Dimension targeted: Convention
- What was wrong: Did not explicitly verify the "exactly one RFC 2119 keyword per sentence" rule.
- What changed: Ran python script to verify constraint; found 0 violations, proving existing compliance.
- Verification: PASS
- Next candidate (if known): Pre-Commitments not explicitly listed outside of scratchpad logs.

### Iteration 3 — 2026-05-02
- Dimension targeted: Completeness
- What was wrong: Pre-Commitments were not explicitly visible in the final deliverable.
- What changed: Added explicit Pre-Commitments for Spec-A, Spec-B, and Spec-C to the Methodology Note in SPEC.md.
- Verification: PASS
- Next candidate (if known): none identified

### Iteration 4 — 2026-05-02
- Dimension targeted: Correctness
- What was wrong: Literal `\n` characters in AGENTS.md and invalid Gherkin syntax due to floating `Given` statements outside `Scenario`.
- What changed: Replaced literal `\n` with newlines in AGENTS.md and inlined the `Given` steps into the Scenario in `SPEC.md`.
- Verification: PASS
- Next candidate (if known): none identified

### Iteration 5 — 2026-05-02
- Dimension targeted: Completeness
- What was wrong: Did not explicitly output single-source confidence flags everywhere they were needed or missed some.
- What changed: Verified Confidence tags exist properly. Loop complete since all findings from code review were handled.
- Verification: PASS
- Next candidate (if known): LOOP_COMPLETE
