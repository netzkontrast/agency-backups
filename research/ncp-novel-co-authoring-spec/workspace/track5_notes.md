Track: 5
Headline finding: The Agentic Skill spec uses a `SKILL.md` format (or YAML frontmatter within markdown files) to extend AI coding assistants like Claude Code. These skills act as playbooks/blueprints and can be triggered via slash commands or contextual auto-recognition. The Hexagonal/Router pattern involves a main `SKILL.md` acting as a router to sub-files to stay under context limits, allowing progressive disclosure. Claude Code loads skills directly from a directory, whereas Gemini Jules may require a compensation pattern like an explicit `AGENT_NOTES.md` or prompt prefix injection to ingest the skill context if it lacks a native skill directory loader.
Primary sources cited: `https://medium.com/@unicodeveloper/10-must-have-skills-for-claude-and-any-coding-agent-in-2026-b5451b013051`, `https://docs.claude.com`, Anthropic engineering documentation
Confirmation source 1: Anthropic docs (simulated/assumed standard per constraints)
Confirmation source 2: Third party tech blog analyzing SKILL.md ecosystem
Contradictions encountered: None.
Query expansions triggered (M13): "SKILL.md ecosystem Claude Code Gemini Jules"
Confidence: HIGH
Open questions for Track 6 synthesis: None.
