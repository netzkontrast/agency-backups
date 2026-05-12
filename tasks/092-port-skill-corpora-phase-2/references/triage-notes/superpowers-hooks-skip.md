---
type: note
status: active
slug: triage-note-superpowers-hooks-skip
summary: "Combined triage note for the three Superpowers hook artefacts (hooks.json, session-start.sh, run-hook.cmd). All three SKIP per ADR-0011 D.7 — SessionStart injection is prohibited. Documented to forestall any ST-3 attempt to port them."
created: 2026-05-12
updated: 2026-05-12
---

# Triage note — Superpowers hooks (all SKIP under D.7)

ADR-0011 D.7 explicitly prohibits SessionStart-injection. The three hook files in the Superpowers snapshot exist solely to implement that pattern and MUST NOT be ported. This note exists so a future maintainer reading just the matrix does not mistake these `skip` rows for low-priority candidates.

## Files

| Snapshot path | What it does | Why D.7 prohibits |
|---|---|---|
| `superpowers/hooks/hooks.json` | Registers `session-start.sh` as a Claude Code SessionStart handler. | Hook config is the **mechanism** D.7 forbids. |
| `superpowers/hooks/session-start.sh` | Injects `using-superpowers` SKILL.md content into the agent's prompt at session bootstrap. | This is the **literal anti-pattern** D.7 names — auto-loading skill content without user invocation. |
| `superpowers/hooks/run-hook.cmd` | Windows shim that runs the .sh hook via WSL/cygwin. | Same anti-pattern, platform variant. |

## Why D.7 forbids this

Three reasons (ADR-0011 §6, summarised):

1. **Context-pollution risk:** auto-injected skill prose competes with user task content for the agent's attention.
2. **Reproducibility:** hooks make the agent's behaviour depend on external state the user cannot inspect; Agency mandates explicit Skill-tool invocation so every behaviour is in the transcript.
3. **Session-start no-injection rule (SS.1–SS.3, AGENTS.md):** the bootstrap procedure is the ONLY thing that may run before the user's first prompt; skill injection is not part of bootstrap.

## What ST-3 ports instead

The **content** that `session-start.sh` was injecting is `superpowers/skills/using-superpowers/SKILL.md` (matrix row 65, decision `adapt`). ST-3 ports that skill as `skills/superpowers-using-superpowers/SKILL.md`, where it becomes user-invocable via the Skill tool — preserving the value of the upstream content without the SessionStart mechanism. See [`superpowers-using-superpowers.md`](./superpowers-using-superpowers.md) for the rewrite plan.

## Audit-graph linkage

None — these files do not land in `/skills/`.

## ST-4 cleanup

When ST-4 deletes the snapshot directory, these three files are removed alongside everything else. No special handling required.
