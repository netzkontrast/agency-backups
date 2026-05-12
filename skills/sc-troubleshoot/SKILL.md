---
name: sc-troubleshoot
description: >-
  Diagnose and resolve issues in code, builds, deployments, and system behavior. Use when the user invokes /sc:troubleshoot or asks to debug a bug, build failure, performance regression, or deployment problem. Diagnose-first; fixes require explicit --fix.
skill_kind: analysis
skill_target_agents: [claude-code]
skill_references_skills: [sc-root-cause-analyst]
skill_references_research: []
skill_references_prompts: []
skill_bootstrap_required: false
skill_source: "superclaude@v4.3.0"
---

# sc-troubleshoot — `/sc:troubleshoot` (imported from SuperClaude v4.3.0)

## What

Imported `/sc:troubleshoot` command from SuperClaude_Framework. Performs systematic, evidence-driven issue diagnosis across code defects, build failures, performance regressions, and deployment problems. **Diagnosis-first**: fixes require the explicit `--fix` flag and user confirmation.

## When to use

Use when the user invokes `/sc:troubleshoot` or asks to debug a runtime error, build failure, performance regression, or deployment problem. For deep root-cause investigation, delegate to `sc-root-cause-analyst`.

## How to use

1. **Analyze** the issue description and gather relevant system state.
2. **Investigate** root causes systematically via pattern analysis and hypothesis formation.
3. **Debug** using structured procedures — log/state examination, error pattern detection.
4. **Propose** ranked solution options with risk and impact assessment.
5. **Stop and present findings** by default. Apply fixes only with the `--fix` flag and explicit user approval, then verify with tests.

Full behavioural specification (including the critical "DIAGNOSE FIRST" boundary) at `references/upstream-sc-troubleshoot.md`.

## References

- Upstream: [`src/superclaude/commands/troubleshoot.md@22ad3f4`](https://github.com/SuperClaude-Org/SuperClaude_Framework/blob/22ad3f483a6fe6c626834e1c9a3573126644a058/src/superclaude/commands/troubleshoot.md) — verbatim mirror at [`references/upstream-sc-troubleshoot.md`](./references/upstream-sc-troubleshoot.md) (ADR-0011 D.3).
- Agency anchor: CLAUDE.md §13 — `/sc:*` skill invocation policy.
- Import policy: [`decisions/0011-external-skill-corpora-import.md`](../../decisions/0011-external-skill-corpora-import.md).

## Compatibility

- Target agent: `claude-code` (this repo's primary surface)
- Known limitation: one-shot snapshot at v4.3.0 — re-syncs require a new Task per ADR-0011 D.9.
