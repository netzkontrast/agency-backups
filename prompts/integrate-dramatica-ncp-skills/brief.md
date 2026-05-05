# Brief — Integrate Dramatica Skills With NCP and Novel-Architect

## Raw user request

> /sc:analyze and /sc:research Both of the dramatica skills and Integration them
> deeply with the ncp skill … the goal is, that you further Improve and tightly
> Integrate those skills with the novel-architect — also Read the Research
> optimizer, especially the critical thinking methods … and use them
> intensively for this Task … try to follow the /research-prompt-optimizer as
> much as you can for this Task … After your analyze step, but before the
> Research step … the goal is, to First Write an extensive Task (Task.md) —
> Detailing enhanced Structure and tooling for the dramatica skills …
> (enhanced in a way that you have spec driven (follow the repo Rules for spec
> Development), Scenarios of the novel Author, and Organist vocabulary and
> theory based on those usage Scenarios — and … extend the vocabulary
> extensively — so, that when loading a specific Term, you get an Overview
> over the Scenarios in which the Term can be Applied … additionally — think
> hard, and Ultra about how to use Python tooling, and frontmatter, to
> navigate and extract Data Token efficient (Beispiel: du hast n Fall das das
> Vokabular nach storyform und Szenario validation gesucht wird … dann sollte
> ein frontmatter navigator Skript helfen können die richtige Stelle
> extrahieren zu können … darüber hinaus … auch wichtig — klar Schemata
> entwickeln für das Vokabular und für the Theorie skills … und auch eine
> ontologie — die über alle skills hinweg genutzt werden kann.

## Target audience

The agent (Claude Code primary; Jules viable) that picks up Task 015 from `/tasks/015-integrate-dramatica-ncp-skills/`. The downstream beneficiaries are the Novel Author persona (working through `novel-architect`) and the Organist / Lyric Architect persona (working through `the-agency-system-architect` + `suno-lyric-writer`).

## Intended model / agent

Claude Code is the natural fit: the work is repo-local, mixes JSON-Schema authoring with Python tooling and per-term frontmatter edits, and benefits from the SuperClaude commands available in this environment (`/sc:research`, `/sc:test`, `/sc:createPR`).

## Use-case context

Today, `dramatica-theory` and `dramatica-vocabulary` carry strong narrative theory but no machine-readable structure beyond Markdown chapters; `ncp-author` ships a JSON-Schema enum but defers theory to those skills via prose-only delegation; `novel-architect` orchestrates the chain but cannot index it. Per-query token cost grows linearly with session length, and the user's two real personas (novel author and organist) are not visible in any of the existing skill files. This prompt drives the work that closes those gaps: a shared Narrative Ontology, per-term frontmatter, scenario tagging, and a small Python navigator suite — all gated by the spec-driven discipline already established in Tasks 009–011.

## Constraints carried forward

- The Dramatica source corpus is © Screenplay Systems and not redistributable; new artefacts MUST NOT extract or paraphrase >1 line of source prose into ontology entries.
- NCP enums are owned upstream; the ontology MUST map to them, never coin new ones.
- YAML frontmatter MUST NOT nest beyond depth 1 (repo-wide rule, [`AGENTS.md`](../../AGENTS.md)).
- Skill prose must remain human-readable in Obsidian after frontmatter is added.
