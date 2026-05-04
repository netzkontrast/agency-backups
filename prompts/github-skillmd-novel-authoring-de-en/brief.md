---
type: note
status: completed
slug: github-skillmd-novel-authoring-de-en
summary: "Brief for the external Gemini research run on SKILL.md-conformant novel-authoring GitHub repos (DE/EN)."
created: 2026-05-04
updated: 2026-05-04
---

# Brief — GitHub SKILL.md Novel-Authoring Repositories (DE/EN)

**Requester:** Repository maintainer  
**Target agent:** Google Gemini (external execution)  
**Use case:** Populate the agency's knowledge base with real-world examples of SKILL.md-conformant novel-authoring repositories to inform the design of the `skills-skill` architecture.

## Raw Request

Extract GitHub repositories implementing the SKILL.md standard for novel-authoring and fiction writing. Filter for bilingual applicability (English and German). Classify by conformance grade (Klasse A / Klasse B) and apply a quality signal rubric (stars, recency, README quality, license, CI). Document key architectural patterns.

## Context

- The agency uses SKILL.md as a specification for agentic skill definitions.
- Prior research (`skills-skill-architecture`) defined the skill architecture but lacked real-world repository examples.
- This external research run was triggered as part of `tasks/003-analyze-skillmd-novel-authoring`.

## Intended Model / Agent

Google Gemini Deep Research (external). Result ingested per `RESEARCH.md` §6 (External Research Ingestion).
