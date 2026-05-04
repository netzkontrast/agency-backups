# Brief: Enterprise Offline Bootstrap for `skills-skill`

## Source

Follow-up question from `research/skills-skill-container-capabilities/output/SPEC.md`. The container-capabilities research concluded that claude.ai Team/Enterprise plans disable network access by default, breaking the REST-API bootstrap path recommended for Free/Pro/Max.

## Question

What is the offline fallback bootstrap workflow for `skills-skill` in Team/Enterprise deployments? Specifically, how does the Anthropic Files API replace the network-dependent fetch step?

## Why it's blocked

The `skills-skill` architecture has no story for enterprise deployments without this answer.
