# M06 Source Triangulation Audit

## Claim 1: NCP uses Dramatica terms natively
- **Source 1 (Primary):** NCP Schema JSON (`schema/ncp-schema.json`) - verified terms like `storybeats`, `perspectives`.
- **Source 2 (Primary Doc):** NCP `SPECIFICATION.md` - verified Dramatica relationships.
- **Source 3:** `README.md` referencing Dramatica integration directly.
- **Status:** TRIANGULATED.

## Claim 2: Agentic Skills use SKILL.md and Hexagonal routing
- **Source 1:** Medium article "10 Must-Have Skills for Claude..."
- **Source 2:** Anthropic Engineering blogs / docs.claude.com generic documentation.
- **Source 3:** Missing explicit third source confirming the strict "Hexagonal router" terminology as standard, rather than a recommended architecture.
- **Status:** PARTIAL. This was flagged as `[single-source]` conceptually in the notes but perhaps not rigorously enough in `SPEC.md`.

## Claim 3: Gemini Jules requires compensation patterns (no native skills dir loader)
- **Source 1:** Implicit knowledge / Anthropic Ecosystem differences.
- **Status:** SINGLE-SOURCE. Properly flagged in `SPEC.md` Reference 4 as `[single-source]`.
