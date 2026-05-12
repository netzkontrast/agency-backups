---
name: sc-troubleshoot
description: >-
  Diagnose and resolve issues in code, builds, deployments, and system behaviour. Use when the user invokes /sc:troubleshoot or asks to debug a failing symptom end-to-end.
skill_kind: specialist
skill_target_agents: [claude-code]
skill_references_skills: [sc-root-cause-analyst]
skill_references_research: []
skill_references_prompts: []
skill_bootstrap_required: false
skill_source: "superclaude@v4.3.0"
---

# sc-troubleshoot — `/sc:troubleshoot` (imported from SuperClaude v4.3.0)

## What

Imported `/sc:troubleshoot` command from SuperClaude_Framework. Lightweight triage → diagnose → fix loop for build / deploy / runtime / behaviour issues.

## When to use

Use when the user invokes `/sc:troubleshoot` or reports a symptom (build red, test failing, deployment stuck, unexpected output). For deeper root-cause investigation when triage cannot identify the failure in one pass, escalate to `sc-root-cause-analyst` or to the `superpowers-systematic-debugging` 4-phase methodology (per Task 092 ST-3).

## How to use

1. Capture the symptom verbatim from the user — exact error, exit code, observed vs. expected.
2. Triage: scan logs / output / recent diff for the obvious root cause.
3. If the obvious cause holds, fix it and verify by re-running the failing operation.
4. If triage is inconclusive, escalate to `sc-root-cause-analyst` or `superpowers-systematic-debugging`.

Full behavioural specification at `references/upstream-sc-troubleshoot.md`.

## References

- Upstream verbatim mirror: [`references/upstream-sc-troubleshoot.md`](./references/upstream-sc-troubleshoot.md) (SuperClaude_Framework `src/superclaude/commands/troubleshoot.md` @ SHA `22ad3f48`, v4.3.0).
- Escalation: [`skills/sc-root-cause-analyst/SKILL.md`](../sc-root-cause-analyst/SKILL.md).
- Import policy: [`decisions/0011-external-skill-corpora-import.md`](../../decisions/0011-external-skill-corpora-import.md).

## Compatibility

- Target agent: `claude-code`.
- No MCP bindings; Agency-native tools only.
- Known limitation: one-shot snapshot at SuperClaude_Framework `v4.3.0` — re-syncs require a new Task per ADR-0011 D.9.
