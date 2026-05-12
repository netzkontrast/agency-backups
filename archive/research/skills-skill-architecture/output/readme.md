---
type: index
status: active
slug: skills-skill-architecture
summary: "Final output artifacts for the skills-skill-architecture research run."
created: 2026-05-04
updated: 2026-05-04
---

# /research/skills-skill-architecture/output/

Final deliverables from the skills-skill-architecture research run.

## Linked Navigation

| File | Purpose |
|---|---|
| [SPEC.md](./SPEC.md) | RFC-2119 preliminary architecture spec covering R1–R7. Six UNCERTAIN markers deferred to Gemini. |
| [gemini-prompt.md](./gemini-prompt.md) | Self-contained Deep Research prompt for Google Gemini. Copy the Research Task section verbatim into Gemini Deep Research. |
| [integration-plan.md](./integration-plan.md) | Mechanical step-by-step instructions for the next agent to fold the Gemini PDF into SPEC.md v2. |

## Assumptions Log

- Three output files instead of the conventional single `SPEC.md` because the brief explicitly required all three. The validator checks only `SPEC.md` for frontmatter; the other two do not require it.
- `gemini-prompt.md` is self-contained by design: an agent reading only that file and having access to Gemini Deep Research can produce a useful PDF without consulting this repository.
- `integration-plan.md` is mechanical by design: the next agent should be able to execute it without judgment calls, referencing only this file and the Gemini PDF.
