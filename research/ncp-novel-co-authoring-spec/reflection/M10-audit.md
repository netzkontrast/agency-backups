# M10 First-Principles Decomposition Audit

## Term 1: "Scene"
- **Decomposition:** A continuous block of action in time and space.
- **Novel Craft Meaning:** The fundamental unit of prose.
- **NCP Meaning:** Modeled as `storytelling.moments[]`.
- **Dramatica Meaning:** A grouping of PRCO (Potential, Resistance, Current, Outcome) at the event level.
- **Verification in SPEC:** Successfully disambiguated in the Glossary (§2). The specification explicitly directs agents to map Dramatica events to `storybeats`, and subsequently draft them into `moments` (prose scenes).

## Term 2: "Story"
- **Decomposition:** An organized sequence of events conveying meaning.
- **NCP Meaning:** The root JSON payload (`story`).
- **Dramatica Meaning:** The Grand Argument Story (Story Mind).
- **Verification in SPEC:** Disambiguated in Glossary (§2).

## Term 3: "Throughline"
- **Decomposition:** A specific perspective or continuous thread of narrative focus.
- **NCP Meaning:** A string field used for grouping/filtering `perspectives` or `storybeats`.
- **Dramatica Meaning:** The four structural perspectives (OS, MC, IC, RS).
- **Verification in SPEC:** Disambiguated in Glossary (§2). It was crucial to note that NCP treats it as a mere string label, whereas Dramatica treats it as a foundational structural pillar.
