# Post-Synthesis Merge Log — skills-skill-architecture

## Merge Sequence

### Step 1 — Environment inspection findings → Track B (R2) and Track D (R6)
Merged the direct Claude Code inspection results (skills dir = `~/.claude/skills/`, format = SKILL.md) into Track B's topology table and Track D's portability analysis. Elevated confidence on the Claude Code portion of R2 and R6 from "assumed" to "confirmed".

### Step 2 — Gap analysis results → Track D (R6) and open questions
The absence of Jules and gemini-cli binaries/configs in the environment confirmed that R6 for those agents cannot be resolved from local inspection alone. These findings were transferred from Track D into three follow-up prompts:
- `/prompts/skills-skill-jules-portability/`
- `/prompts/skills-skill-gemini-cli-portability/`
- `/prompts/skills-skill-trigger-lifecycle/`

### Step 3 — Track A (R1) findings → SPEC.md R1 section + UNCERTAIN markers
The host trigger mechanism for claude.ai remains opaque. Merged Track A's findings into the spec with explicit UNCERTAIN markers on: (a) how the host determines which skill to fire, (b) whether git is available in the container, (c) whether the stub receives the user's raw message or a pre-processed intent signal.

### Step 4 — Track B (R7) decision → SPEC.md R7 section
The "pull-if-exists (shallow)" strategy decision was merged into the spec's R7 section with its rationale. The UNCERTAIN tag on container persistence was propagated.

### Step 5 — Track C (R3, R4) routing model → SPEC.md + Gherkin scenarios
The two-tier routing model and three-tier disclosure ladder were formalized into RFC-2119 MUST/SHOULD statements with corresponding Gherkin scenarios.

### Step 6 — Contradiction check
No contradictions found between tracks. The topology in Track B (repo is canonical, /mnt/skills/user/ is read-only) is consistent with Track A's trust analysis (stub immutability as primary security boundary) and Track D's portability assumption (same SKILL.md format, no concurrent writes).

### Step 7 — Gemini prompt assembled from open questions
The three UNCERTAIN markers and two unknown agents (Jules, gemini-cli) were used to construct the Gemini Deep Research prompt. Each UNCERTAIN maps to a discrete Gemini research question.

### Step 8 — Integration plan written
The integration plan describes mechanical steps for folding the Gemini PDF into SPEC.md v2. Each UNCERTAIN marker in SPEC.md has a corresponding integration step.
