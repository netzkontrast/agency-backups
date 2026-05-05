# Brief: Empirical `git` Verification in claude.ai Container

## Source

Follow-up question from `research/skills-skill-container-capabilities/output/SPEC.md`. Sub-question of U1 (is `git` available in the claude.ai container?) — the prior research inferred *no* from omission in the official pre-installed utility list, but did not run a live probe.

## Question

Run `which git && git --version` inside a live claude.ai code execution session. Report the actual exit code, stdout, and stderr.

## Why it's blocked

This requires an interactive claude.ai session. The local environment cannot execute the probe.
