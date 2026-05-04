# skills/

## What
Version-controlled snapshots of user-installed Claude skills from
`/mnt/skills/user/`. Each subfolder is one skill, structured per Anthropic's
skill-creator convention (a `SKILL.md` plus optional `references/`, `scripts/`,
`assets/`, `agents/`).

## Why here
Skills evolve continuously across Claude.ai sessions. Hosting them here gives
us version history, a multi-agent collaboration surface (Claude Code, Jules,
gemini-cli can all read and propose changes via PR), and a recoverable
upstream when a session container is reset.

The runtime "live" location is still `/mnt/skills/user/` inside each
Claude.ai session. This folder is the durable mirror.

## Skill index (14 skills)
- [dramatica-theory/](./dramatica-theory/) — Apply Dramatica narrative theory (Phillips & Huntley, *Dramatica*, 4th ed., 2001) to story analysis, storyforming, drafting, and draft diagnosis.
- [dramatica-vocabulary/](./dramatica-vocabulary/) — Aktive Dramatica-Theorie für Storyform-Aufbau, Encoding und Storyweaving — kein passives Dictionary, sondern Werkzeug.
- [drive-markdown-converter/](./drive-markdown-converter/) — >- Use when the user wants to convert Google Docs or PDFs in a Google Drive folder to Markdown and upload the results to another Drive folder — without letting file contents land in the main contex...
- [gdrive-notion-curator/](./gdrive-notion-curator/) — >- MCP-driven Drive-zu-Notion Curator.
- [ncp-author/](./ncp-author/) — >- Schema cheatsheet, canonical vocabulary (463 appreciations + 144 narrative_functions), validation rules, 10-stage authoring workflow, and runnable schema validator for NCP (ncp-schema.json v1.3.0).
- [notebooklm-prompt-architect/](./notebooklm-prompt-architect/) — >- Use when designing custom-instruction prompts, source-pack governance, or full production specs for NotebookLM Audio Overviews / Deep Dive podcasts — especially "pitch podcast" use cases that de...
- [novel-architect/](./novel-architect/) — >- Orchestrator für den deutschsprachigen Roman „Kohärenz Protokoll" (Hard-SF / Philosophical Horror, Dual-Storyform, 39 Kapitel, 13 Alters).
- [pdf-to-markdown/](./pdf-to-markdown/) — Convert a PDF to Markdown using PyMuPDF4LLM.
- [prompt-optimizer/](./prompt-optimizer/) — >- Use at the START of EVERY conversation, before processing any user request.
- [ralph-skill/](./ralph-skill/) — "Use when generating Ralph agentic-loop files (loop.sh, PROMPT_build.md, PROMPT_plan.md, AGENTS.md, IMPLEMENTATION_PLAN.md), customizing or extending an existing Ralph workflow, auditing a Ralph se...
- [research-prompt-optimizer/](./research-prompt-optimizer/) — >- Use whenever a user wants to generate, optimize, audit, version, or architect a Deep Research prompt for any autonomous research system (Gemini Deep Research, Perplexity, Claude Research, GPT De...
- [spec-skill/](./spec-skill/) — "Authoring, applying, and auditing normative specifications for autonomous AI agents and long-horizon agentic workflows — using RFC-2119 keywords, Gherkin acceptance criteria, and a fixed five-aspe...
- [suno-lyric-writer/](./suno-lyric-writer/) — >- Use when writing, reviewing, or revising song lyrics for Suno AI generation.
- [the-agency-system-architect/](./the-agency-system-architect/) — >- Orchestrates the full concept-album production pipeline for "The Agency System" (Michael Schimmer's darkwave/industrial triptych — Album 1 "Together We Confide", Album 2 "Moment der Klarheit", A...

## Management layer
- [skills-skill-bootstrap/](./skills-skill-bootstrap/) — Sync tool: pulls skill bodies from `origin/main:skills/` into Claude Code's `~/.claude/skills/`.

## Current State

- **14 skills** in repo, all synced to `~/.claude/skills/` as of 2026-05-04.
- `skills-skill-bootstrap/` sync mechanism is live and tested end-to-end.
- Architecture spec for the future `skills-skill` loader is in progress at `research/skills-skill-architecture/` — awaiting Gemini Deep Research PDF to finalize.
- `/skills/skills-skill/` path reserved; do not create until spec is accepted.

## Latest Synthesized Learnings

- Claude Code `~/.claude/skills/` and claude.ai `/mnt/skills/user/` use the **same `SKILL.md` format** — no adapter needed between the two platforms.
- `git ls-tree -d --name-only` is the correct enumeration method for skill directories; `--name-only` without `-d` incorrectly includes flat files (like this readme).
- The sync mechanism should use `cmp -s` (binary comparison via temp file) rather than command-substitution string comparison for correctness on large or whitespace-sensitive files.

## Open Blockers

- Gemini Deep Research PDF pending (required to resolve 6 UNCERTAIN markers in the architecture spec before `skills-skill` implementation can begin).
- Jules and gemini-cli skill-loading conventions unknown — their portability to the `SKILL.md` format is unverified.

## Governance In Flight

`/skills/` does not yet have a root governance file. Three open tasks will close that gap:

- [`/tasks/009-author-skills-root-spec/`](../tasks/009-author-skills-root-spec/) — author `SKILLS.md` (the missing sibling of `TASK.md` / `PROMPT.md` / `RESEARCH.md`); ratify the `skill_*` L2 namespace and the bootstrap protocol.
- [`/tasks/010-skills-frontmatter-index-suite/`](../tasks/010-skills-frontmatter-index-suite/) — build the token-efficient frontmatter index + query CLI + manifest emitter so Claude Code, Jules, and Gemini share one cheap navigation surface.
- [`/tasks/011-skills-frontmatter-schema-files/`](../tasks/011-skills-frontmatter-schema-files/) — author JSON Schemas for L1/L2 frontmatter and the canonical header ontology.

## Assumptions Log
- Initial import: snapshot taken 2026-05-04 from a single Claude.ai
  session. No sync-back protocol (`/mnt/skills/user/` ← `skills/`) is defined
  yet — that is a follow-up task (will likely live as a "agency bootstrap"
  skill that clones this repo into the session workspace).
- Per-skill `readme.md` files are auto-generated from each `SKILL.md`'s YAML
  frontmatter. If the frontmatter format changes, regeneration is needed.
- Skill-internal subfolders are intentionally NOT given individual readmes
  (see per-skill Assumptions Log for rationale).
- **FOLDERS.md §7 tension**: `skills/` is content storage, not a workflow
  orchestration folder, and is therefore exempt from the task/prompt/research
  restriction. This interpretation is logged here to prevent future agents from
  deleting `skills/` to satisfy a strict reading of §7.
