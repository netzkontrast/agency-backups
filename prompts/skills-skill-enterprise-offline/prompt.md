---
type: prompt
status: active
slug: skills-skill-enterprise-offline
summary: "Define the Files API pre-upload workflow for skills-skill in Team/Enterprise deployments where network access is disabled by default."
created: 2026-05-04
updated: 2026-05-04
prompt_kind: follow-up
prompt_framework: RISEN
prompt_target_agent: Claude Code
prompt_relates_to_task: ""
prompt_spawned_from_research: skills-skill-container-capabilities
---

# Research: skills-skill Enterprise Offline Bootstrap

## Context

The `skills-skill-container-capabilities` research (output/SPEC.md) found that claude.ai Team and Enterprise plans disable network access by default. This means the REST API bootstrap approach (recommended for Free/Pro/Max) fails for enterprise deployments. The architecture must define an offline fallback using the Anthropic Files API.

## Research Questions

1. What is the Anthropic Files API? What file types and sizes does it support?
2. How does a skill body get pre-uploaded before a session starts? What is the upload workflow?
3. How does a SKILL.md reference a pre-uploaded file by ID so Claude can load it without network access?
4. What is the maintenance burden for keeping pre-uploaded skill files current when the repo changes?
5. Can the upload step be automated (e.g., a GitHub Actions workflow that uploads on each merge to main)?
6. What are the file ID durability guarantees — do IDs change on re-upload?

## Expected Output

Produce a specification for the enterprise offline bootstrap pattern:
- Files API upload workflow (manual + automated via GitHub Actions)
- SKILL.md stub variant for offline/enterprise deployment
- Maintenance runbook: how to detect stale uploads and trigger re-upload
- RFC-2119 language ready to add as §2.5 "Enterprise Offline Deployment" to `research/skills-skill-architecture/output/SPEC.md`
