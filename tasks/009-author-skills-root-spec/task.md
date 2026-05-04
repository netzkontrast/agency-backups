---
type: task
status: active
slug: author-skills-root-spec
summary: "Author SKILLS.md — the missing root governance spec for /skills/ — wire cross-references between skills, formalize the skill-bootstrap protocol, and harmonize AGENTS.md / PROMPT.md / RESEARCH.md to acknowledge skills as a fourth top-level concern."
created: 2026-05-04
updated: 2026-05-04
task_id: "009"
task_owner: "unassigned"
task_status: open
task_priority: P1
task_uses_prompts:
  - author-skills-root-spec
task_spawns_research: []
task_spawns_prompts: []
task_affects_paths:
  - SKILLS.md
  - AGENTS.md
  - PROMPT.md
  - RESEARCH.md
  - TASK.md
  - FOLDERS.md
  - skills/readme.md
  - skills/skills-skill-bootstrap/readme.md
  - templates/skill.md
---

# Task 009 — Author the Root `SKILLS.md` Specification

## Goal

The repository has four top-level operational concerns — `/tasks/`, `/prompts/`, `/research/`, and `/skills/` — but only the first three are governed by a root specification (`TASK.md`, `PROMPT.md`, `RESEARCH.md`). `/skills/` is governed implicitly by `skills/readme.md` and a single research SPEC (`research/skills-skill-architecture/output/SPEC.md`). This task is `done` when:

1. A new file `SKILLS.md` exists at the repository root, mirroring the structural shape of `TASK.md` / `PROMPT.md` / `RESEARCH.md`.
2. `SKILLS.md` is normative (RFC-2119), self-contained, and binds all agents (Claude Code, Jules, Gemini) on what `/skills/` may and MUST NOT contain.
3. Cross-references between skills are mechanically resolvable (skill-to-skill linkage rules added to `FOLDERS.md §6` and the linter).
4. The skill-bootstrap protocol (pull latest skill bodies into the active workspace, then expose token-efficient navigation tools) is canonically described in `SKILLS.md` rather than scattered across `skills/skills-skill-bootstrap/readme.md` and `research/skills-skill-architecture/`.
5. `AGENTS.md` lists `SKILLS.md` in its task-type routing table and references the new spec from § Frontmatter Ontology.
6. `templates/skill.md` exists and emits a SKILL.md skeleton with the canonical L1 frontmatter plus the new `skill_*` L2 namespace defined in `SKILLS.md`.

The Task is **author-only**: no code changes to existing skill bodies, no rebuild of the bootstrap script. Tasks 010 and 011 implement the tools and schemas that `SKILLS.md` will mandate.

## Background — Why This Task Exists

The 2026-05-04 surface-skills-architecture coherence run (Task 006) flagged that `skills-skill-architecture` research findings have not been promoted to root governance. Compounding evidence:

1. **`/skills/` has no root spec.** `AGENTS.md § Task Type Routing` only mentions `/tasks/`, `/prompts/`, `/research/`. An agent that wants to author or modify a skill has nowhere normative to read first.
2. **No skill-to-skill linkage convention exists.** `the-agency-system-architect` orchestrates `suno-lyric-writer` and `dramatica-theory` implicitly; `ralph-skill` mentions `research-prompt-optimizer` in prose. None of these are mechanically resolvable, and nothing prevents a renamed skill from silently breaking a referencing skill.
3. **Skill frontmatter is non-standard.** Existing skills use Anthropic's `name` / `description` keys (and ad-hoc `metadata:` blocks) that are *not* the L1 Vault Core schema. Skills are therefore invisible to `tools/validate-frontmatter.py` and to any future repo-wide query tool.
4. **Bootstrap protocol is implicit.** `skills/skills-skill-bootstrap/readme.md` documents `sync.sh` operationally, but the *protocol* (when to bootstrap, what guarantees the bootstrap provides to consuming agents, how the bootstrap interacts with the not-yet-built `skills-skill` loader) lives only in research output. It is not binding.
5. **Cross-agent portability is asserted, not normative.** `skills-skill-architecture/output/SPEC.md §7` reserves adapter directories for Jules and gemini-cli without a root rule that says other-agent compatibility is REQUIRED. Without a root statement, follow-up tasks for Jules portability cannot fail-closed.

## Plan

1. **Read the source material.** Open `research/skills-skill-architecture/output/SPEC.md`, `skills/readme.md`, `skills/skills-skill-bootstrap/readme.md`, and the existing `TASK.md` / `PROMPT.md` / `RESEARCH.md` to extract the shared structural shape (Definitions → Directory Structure → Frontmatter Ontology → Workflow → Pre-Commit Checks → Edge Cases → Anti-Patterns).
2. **Draft `SKILLS.md` skeleton.** Produce the section skeleton in the prompt at `/prompts/author-skills-root-spec/prompt.md`. The skeleton MUST mirror `TASK.md`'s nine-section template so that agents who already know one root spec can read this one without re-orientation.
3. **Define the L2 `skill_*` frontmatter namespace.** Required keys (proposed, subject to research-proposal review):
   - `skill_kind` — One of: `domain` (e.g. dramatica-theory), `tool` (e.g. pdf-to-markdown), `orchestrator` (e.g. the-agency-system-architect), `meta` (e.g. skills-skill-bootstrap).
   - `skill_target_agents` — List of agents the skill is verified-portable to: `claude-ai`, `claude-code`, `jules`, `gemini-cli`.
   - `skill_references_skills` — List of slugs of other skills this skill invokes or composes. Reciprocal (A → B implies B is `skill_referenced_by` A; the linter resolves both directions).
   - `skill_references_research` — List of `/research/<slug>/` workspaces that grounded the skill's normative claims.
   - `skill_references_prompts` — List of `/prompts/<slug>/` instruction sets the skill embeds or extends.
   - `skill_bootstrap_required` — Boolean; true if the skill cannot run without the bootstrap clone in the active workspace (most skills); false if the skill is self-contained (e.g. `skills-skill-bootstrap` itself).
4. **Define the skill-bootstrap protocol.** Section 7 of `SKILLS.md` MUST normatively bind:
   - **B.1** Every agent (Claude Code, Jules, Gemini) MUST run the bootstrap before touching `/skills/` or executing a skill.
   - **B.2** The bootstrap MUST clone or fast-forward `origin/main` into the active workspace at a known path; the path is stored in environment variable `AGENCY_SKILLS_ROOT`.
   - **B.3** The bootstrap MUST emit a manifest of all skill slugs and their `skill_kind` to `$AGENCY_SKILLS_ROOT/.skills-manifest.json` so that downstream tools can route without re-walking the tree.
   - **B.4** The bootstrap MUST surface a non-zero exit on staleness > 24h to force a sync at the cost of a per-day prompt to the human; the agent MAY override with `AGENCY_SKILLS_ALLOW_STALE=1` for offline work.
   - **B.5** Token-efficient navigation rule: *agents MUST query the manifest and the frontmatter index (Task 010) before opening any SKILL.md body.* This is the single token-saving lever that makes a 14-skill repo cheap to consult.
5. **Define skill-to-skill cross-reference rules.** Section 6 of `SKILLS.md` MUST normatively bind:
   - **X.1** A skill MAY reference other skills *only* through the `skill_references_skills` frontmatter list. Inline mentions in prose are non-normative and MUST NOT be relied on by consumers.
   - **X.2** Every reference MUST resolve at lint time. A broken reference is a pre-commit failure.
   - **X.3** Reciprocity is computed by the linter, not authored. Authors do not write `skill_referenced_by`; the index tool generates it.
   - **X.4** Composition vs. invocation is signalled by reference shape: a list element of bare `<slug>` is *invocation* (skill A calls skill B as a tool); a list element of the form `<slug>:embed` is *composition* (skill A inlines skill B's body — RECOMMENDED only between skills with the same `skill_kind`).
6. **Define cross-agent portability requirements.** Section 8 of `SKILLS.md` MUST bind:
   - **P.1** Every skill SHOULD declare every agent it has been verified-portable to in `skill_target_agents`. Skills with `claude-ai` only are not failures, but they are flagged by the index as single-agent.
   - **P.2** Multi-agent skills MUST live in `skills/<slug>/SKILL.md` with optional adapter overlays at `skills/<slug>/adapters/<agent>/` (per `skills-skill-architecture/output/SPEC.md §7.2`).
   - **P.3** A skill MUST NOT silently change behavior across agents. Any agent-specific divergence MUST be encoded in an adapter overlay; the canonical `SKILL.md` MUST be agent-neutral.
7. **Update AGENTS.md routing table.** Add a fourth row pointing skill-authoring requests to `SKILLS.md` and `/skills/`. Update the Frontmatter Ontology Summary to include the L2 `skill_*` namespace.
8. **Update FOLDERS.md.** Add `/skills/` as a fourth top-level operational directory (currently treated as content-only). Document the skill-to-skill audit graph alongside the existing Task → Prompt → Research graph.
9. **Update PROMPT.md and RESEARCH.md.** Add a one-line cross-reference: prompts/research that target a skill MUST set the appropriate L2 reverse-link (`prompt_relates_to_skill`, `research_documents_skill`) — these are introduced by Task 011's schema work but called out here.
10. **Author `templates/skill.md`.** A SKILL.md skeleton with placeholder L1 + `skill_*` frontmatter, the canonical body sections (`## What`, `## When to use`, `## How to use`, `## References`, `## Compatibility`), and `REPLACE` markers compatible with `tools/validate-frontmatter.py`.
11. **Pre-commit verification.** Run `tools/check-governance.sh`. Fix any failure. Confirm the new files pass `validate-frontmatter.py`. Do NOT modify existing skill bodies in this task — `SKILLS.md` declares the spec; conformance migrations are downstream tasks.

## Todo

- [ ] 1. Read TASK.md / PROMPT.md / RESEARCH.md and extract the shared section skeleton.
- [ ] 2. Read the skills-skill-architecture SPEC and skills-skill-bootstrap readme; extract every normative claim.
- [ ] 3. Author `SKILLS.md` at the repository root following the nine-section template.
- [ ] 4. Author `templates/skill.md` matching the new `skill_*` L2 namespace.
- [ ] 5. Update `AGENTS.md` routing table to include `SKILLS.md`.
- [ ] 6. Update `FOLDERS.md §1, §6` to include `/skills/` and the skill-audit graph.
- [ ] 7. Update `PROMPT.md` and `RESEARCH.md` with the cross-reference one-liners.
- [ ] 8. Update `skills/readme.md` to reference `SKILLS.md` as the governing spec.
- [ ] 9. Run `tools/check-governance.sh`; fix any failures.
- [ ] 10. Set `task_status: done`, write `friction-log.md`, update `updated` field.

## Links

- Executing prompt: [`/prompts/author-skills-root-spec/prompt.md`](../../prompts/author-skills-root-spec/prompt.md)
- Source research: [`/research/skills-skill-architecture/output/SPEC.md`](../../research/skills-skill-architecture/output/SPEC.md)
- Sibling Tasks: [`010-skills-frontmatter-index-suite/`](../010-skills-frontmatter-index-suite/), [`011-skills-frontmatter-schema-files/`](../011-skills-frontmatter-schema-files/)
- Predecessor: [`006-surface-skills-architecture/`](../006-surface-skills-architecture/) — surfaces *findings*; this task ratifies them as a *spec*.
- Governing specs: [`TASK.md`](../../TASK.md), [`PROMPT.md`](../../PROMPT.md), [`RESEARCH.md`](../../RESEARCH.md), [`FOLDERS.md`](../../FOLDERS.md)
