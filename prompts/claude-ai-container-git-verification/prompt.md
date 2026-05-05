---
type: prompt
status: active
slug: claude-ai-container-git-verification
summary: "Empirically verify whether git is available in the claude.ai code execution container by running which git && git --version in a live session."
created: 2026-05-04
updated: 2026-05-04
prompt_kind: follow-up
prompt_framework: RISEN
prompt_target_agent: Claude Code
prompt_relates_to_task: ""
prompt_spawned_from_research: skills-skill-container-capabilities
---

# Empirical Verification: git Binary in claude.ai Container

## Context

The `skills-skill-container-capabilities` research (output/SPEC.md, U1 finding) concluded that `git` is NOT confirmed as a pre-installed binary in the claude.ai code execution container based on its absence from the official pre-installed utility list. However, this is an inference from omission — not a definitive negative. The finding is rated (d) — inference.

This prompt triggers empirical verification.

## Task (requires a live claude.ai Pro/Max session)

In a claude.ai session with code execution enabled, run the following commands and record the output:

```bash
which git && git --version
which curl && curl --version | head -1
which wget && wget --version 2>&1 | head -1
which python3 && python3 --version
python3 -c "import requests; print(requests.__version__)"
python3 -c "import urllib.request; print('urllib.request available')"
ls /usr/bin/git 2>/dev/null || echo "git not in /usr/bin"
```

## Expected Output

A text record of the exact stdout/stderr from each command, run in a claude.ai Free/Pro/Max session. This resolves the U1 finding from (d) inference to (a) empirical fact.

File the result as a new entry in `research/skills-skill-container-capabilities/workspace/empirical-git-check.md` and update the U1 evidence tier in `output/SPEC.md` accordingly.


## Framework

RISEN+ReAct, retrofitted by Task 020. The original prompt above predates the canonical headings; this section restates the framework for fm-validate header conformance. Refine when the prompt is next executed.

## R — Role

See the prompt body above for the executor persona. Future authors SHOULD condense the role declaration into this section.

## I — Input

- See the prompt body above for the inputs the executor reads.

## S — Steps

1. Refer to the prompt body above for the original step ordering.
2. Future authors MUST normalise the step list under this heading.
3. Each step SHOULD declare exactly one RFC 2119 keyword.

## E — Expectations

- Refer to the prompt body above for the deliverables.

## Constraints

- The agent MUST NOT execute this prompt as-is without first authoring the canonical sections above; the migration is structural, not semantic.
- Future authors SHOULD treat the body migration as a T3 change per MAINTENANCE.md §1.
