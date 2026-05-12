Track: 1
Headline finding: The NCP repository defines a standard JSON schema for transporting authorial intent with three distinct layers: `ideation`, `subtext` (perspectives, players, dynamics, storypoints, storybeats), and `storytelling` (overviews, moments). The schema natively uses Dramatica terms. It relies on `status` inside the `narrative` object as the state machine (`candidate`, `draft`, `complete`). There are no native 'scene' or 'chapter' entities, only `storybeats` (with scopes `signpost`, `progression`, `event`) and `moments` under storytelling.
Primary sources cited: `schema/ncp-schema.json:L83@0b9ab1223d3822a49eddc139bcdf2669aa067734`, `README.md:L1-L50@0b9ab1223d3822a49eddc139bcdf2669aa067734`, `SPECIFICATION.md:L1-L50@0b9ab1223d3822a49eddc139bcdf2669aa067734`
Confirmation source 1: `schema/ncp-schema.json`
Confirmation source 2: `README.md`
Contradictions encountered: None yet.
Query expansions triggered (M13): None yet.
Confidence: HIGH
Open questions for Track 6 synthesis: What specific gaps exist for novel authoring, as NCP has 'moments' but maybe not 'chapters' or 'scenes' explicitly formatted for a novel? We need to bridge this with Dramatica elements or an additional context.
