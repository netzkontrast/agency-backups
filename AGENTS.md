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

## LOOP_LOG
<!-- Jules appends one record per iteration. Do not edit manually. -->

### Iteration 0 — 2026-05-02
- Status: Loop initialized
- Work artifact: research/obsidian-frontmatter-agentic-spec/output/SPEC.md
- Verification command: python3 test_spec.py
- Max iterations: 5

### Iteration 1 — 2026-05-02
- Dimension targeted: Completeness
- What was wrong: The SPEC.md output contained pseudocode instead of the explicitly requested ASCII diagram for the Expansion-Pattern decision tree.
- What changed: Replaced the pseudocode script logic section with a fully formatted ASCII flowchart.
- Verification: PASS
- Next candidate: Missing "Abstraction Axis" in the Adversarial Query Expansion passes (M13).
