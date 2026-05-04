---
type: prompt
status: active
slug: author-skills-root-spec
summary: "Author SKILLS.md — the root governance spec for /skills/ — mirroring TASK.md / PROMPT.md / RESEARCH.md, defining the skill_* L2 namespace, the skill-bootstrap protocol, and the cross-agent portability contract."
created: 2026-05-04
updated: 2026-05-04
prompt_kind: task-spec
prompt_framework: RISEN
prompt_target_agent: "Claude Code"
prompt_relates_to_task: author-skills-root-spec
prompt_spawned_from_research: skills-skill-architecture
---

# Author the Root SKILLS.md Specification

## Framework

**RISEN.** This is a structured one-shot authoring task: a new spec file written end-to-end against a fixed schema, plus a small set of mechanical edits to existing root specs. ReAct loops are not required — the inputs are stable repository artifacts, not external evidence.

---

## § RFC 2119

The key words MUST, MUST NOT, REQUIRED, SHALL, SHALL NOT, SHOULD, SHOULD NOT, RECOMMENDED, NOT RECOMMENDED, MAY, and OPTIONAL in this document are to be interpreted as described in BCP 14 [RFC 2119] [RFC 8174] when, and only when, they appear in all capitals as shown here.

---

## R — Role

You are a governance-spec author in a multi-agent repository. You write specs that are read by *other* agents — Claude Code, Jules, and Gemini — who depend on the spec's normativity (RFC-2119) and structure (Gherkin) to fail closed against ambiguous instructions. You do not implement; you specify.

## I — Input

The executor MUST read the following files before writing a single normative statement:

1. `/TASK.md` — the canonical shape of a root spec (nine sections: §1 Definitions → §9 Anti-Patterns).
2. `/PROMPT.md` — the parallel root spec for `/prompts/`, used to validate that section parity is preserved.
3. `/RESEARCH.md` — the parallel root spec for `/research/`.
4. `/AGENTS.md` — specifically the § Task Type Routing table (which `SKILLS.md` extends), the § Frontmatter Ontology Summary, and the § Closing Run Procedure.
5. `/FOLDERS.md` — the existing audit graph (Task → Prompt → Research) that `SKILLS.md` extends with skill-to-skill linkage.
6. `/skills/readme.md` — the current de-facto skills index.
7. `/skills/skills-skill-bootstrap/readme.md` and `/skills/skills-skill-bootstrap/sync.sh` — the existing bootstrap implementation.
8. `/research/skills-skill-architecture/output/SPEC.md` — the preliminary architecture spec (R1–R7) that `SKILLS.md` ratifies.
9. `/maintenance/language-spec.md` — the canonical RFC-2119 + Gherkin grammar `SKILLS.md` MUST adhere to.
10. The `task.md` for this prompt's task: `/tasks/009-author-skills-root-spec/task.md`. Its §Plan is the binding outline; this prompt is the execution layer for that plan.

## S — Steps

### Step 1 — Confirm structural parity with sibling root specs

The executor MUST produce `SKILLS.md` with exactly the following nine top-level sections:

```
§1. Definitions (RFC 2119)
§2. Directory Structure
§3. Frontmatter Ontology (skill_* namespace)
§4. Workflow (Skill Lifecycle)
§5. SKILL.md Required Sections
§6. Skill-to-Skill Cross-References
§7. Bootstrap Protocol
§8. Cross-Agent Portability
§9. Mandatory Pre-Commit Checks
§10. Edge Cases & Open Questions
§11. Anti-Patterns
```

Sections §1–§5 mirror `TASK.md`'s §1–§5 by purpose (allowing readers to navigate by analogy). Sections §6–§8 are skills-specific and are the substantive new contribution. Sections §9–§11 mirror `TASK.md` §7–§9.

### Step 2 — Define the L2 `skill_*` namespace

The executor MUST define the following keys, each with a single-sentence purpose, in §3.3:

| Key | Type | Purpose |
|---|---|---|
| `skill_kind` | string | One of: `domain`, `tool`, `orchestrator`, `meta`. Drives index routing. |
| `skill_target_agents` | list | Agents the skill is verified-portable to. Members from: `claude-ai`, `claude-code`, `jules`, `gemini-cli`. |
| `skill_references_skills` | list | Slugs of other skills this skill invokes or composes. Reciprocity is computed by the linter. |
| `skill_references_research` | list | Slugs of `/research/<slug>/` workspaces grounding the skill's claims. |
| `skill_references_prompts` | list | Slugs of `/prompts/<slug>/` instruction sets the skill embeds or extends. |
| `skill_bootstrap_required` | boolean | True if the skill cannot run without the bootstrap clone. |

The executor MUST NOT introduce additional keys without adding a Rationale paragraph in §3.3 justifying each one.

### Step 3 — Author §6 (Skill-to-Skill Cross-References)

§6 MUST contain four normative clauses (X.1 – X.4), exactly as scoped by §Plan step 5 of `tasks/009-author-skills-root-spec/task.md`. Each clause MUST be paired with a Gherkin scenario in the same section that demonstrates the rule on a concrete pair of existing skills (suggested: `the-agency-system-architect` referencing `suno-lyric-writer` for invocation; `dramatica-vocabulary` referencing `dramatica-theory` for composition).

### Step 4 — Author §7 (Bootstrap Protocol)

§7 MUST contain five normative clauses (B.1 – B.5) that lift `task.md` §Plan step 4 from "proposed" to "binding". Each clause MUST be paired with at least one Gherkin scenario. The protocol MUST cover:

- **B.1** Mandatory bootstrap-before-skill-use for every agent.
- **B.2** Canonical clone path `$AGENCY_SKILLS_ROOT`.
- **B.3** Manifest emission to `$AGENCY_SKILLS_ROOT/.skills-manifest.json`.
- **B.4** Staleness gate (24 h soft limit, override via `AGENCY_SKILLS_ALLOW_STALE`).
- **B.5** Token-efficient navigation — the agent MUST query the manifest and the frontmatter index before opening any SKILL.md body.

The executor MUST cite `research/skills-skill-architecture/output/SPEC.md` §2 (R1) and §8 (R7) as the source of these clauses, since that research SPEC is the evidence base. The executor MUST resolve UNCERTAIN markers from the source SPEC by either (a) restating them as B-clauses, with explicit citation; or (b) deferring them in §10 as Open Questions.

### Step 5 — Author §8 (Cross-Agent Portability)

§8 MUST contain three normative clauses (P.1 – P.3) that bind multi-agent compatibility:

- **P.1** Every skill SHOULD declare `skill_target_agents`. Single-agent skills are valid but flagged.
- **P.2** Multi-agent skills MUST keep canonical `SKILL.md` agent-neutral; agent-specific behavior MUST live in `skills/<slug>/adapters/<agent>/`.
- **P.3** A skill MUST NOT silently change behavior across agents.

The executor MUST cite the open follow-up prompts `/prompts/skills-skill-jules-portability/` and `/prompts/skills-skill-gemini-cli-portability/` and reserve adapter directory paths consistent with `skills-skill-architecture/output/SPEC.md` §7.2.

### Step 6 — Author §9 (Pre-Commit Checks) by analogy to TASK.md §7

The executor MUST define seven mechanical checks mapped to existing or planned tools. The mapping table follows the format of `TASK.md §7.0`:

| Check | Tool | Failure mode |
|---|---|---|
| §9.1 Frontmatter Integrity | `tools/validate-frontmatter.py` | Missing L1/L2 keys, YAML depth > 1 |
| §9.2 Skill-Reference Resolution | `tools/lint-linkage.py` (extended in Task 010) | `skill_references_*` slug doesn't resolve |
| §9.3 Bootstrap Manifest Freshness | `tools/skills-manifest.py` (Task 010) | Manifest out of sync with `/skills/` |
| §9.4 Header Conformance | `tools/lint-structure.py` + header-ontology schema (Task 011) | SKILL.md missing REQUIRED `##` section |
| §9.5 Cross-Agent Adapter Parity | human review for now; future linter | Adapter directory referenced but missing |
| §9.6 Readme Audit | `tools/lint-structure.py` | Missing `readme.md` in skill folder |
| §9.7 Bootstrap-Required Self-Honesty | `tools/lint-linkage.py` | `skill_bootstrap_required: false` skill that imports from `references/` |

The executor MUST mark §9.5 as a "human review for now" check; it depends on Task 010's index for mechanization.

### Step 7 — Mechanical edits to root specs

After `SKILLS.md` is written, the executor MUST apply these mechanical edits exactly once:

1. `AGENTS.md § Task Type Routing` table: add a fourth row.

   ```
   | Authoring or modifying a skill | [SKILLS.md](./SKILLS.md) | [/skills/](./skills/) |
   ```

2. `AGENTS.md § Frontmatter Ontology Summary`: add `skill_*` to the L2 namespace list.

3. `AGENTS.md § Closing Run Procedure` is unchanged; SKILLS.md does NOT alter PR-creation rules.

4. `FOLDERS.md §1 Top-Level Topology` table: add a fourth row.

   ```
   | `/skills/` | `SKILLS.md` | Capability: *what the agent knows how to do* | Skill folders `<slug>/` with `SKILL.md`. |
   ```

5. `FOLDERS.md §6 Cross-Directory Linking`: add the skill audit graph. The new lines MUST be:

   ```
   - Skill → Skill: `skill_references_skills: [<slug>, ...]`
   - Skill → Research: `skill_references_research: [<slug>, ...]`
   - Skill → Prompt: `skill_references_prompts: [<slug>, ...]`
   ```

6. `PROMPT.md §3` and `RESEARCH.md §3`: add a one-line note that prompts/research targeting a skill MAY set `prompt_relates_to_skill` / `research_documents_skill` once Task 011 ratifies the schemas.

7. `templates/skill.md`: create the file. It MUST include L1 frontmatter with `REPLACE` markers identical to `templates/task.md`, the proposed L2 `skill_*` namespace with placeholder values, and the canonical body sections (`## What`, `## When to use`, `## How to use`, `## References`, `## Compatibility`).

8. `skills/readme.md`: replace the "Open Blockers" line about Jules/Gemini portability with a link to `SKILLS.md §8`.

### Step 8 — Pre-commit verification

The executor MUST run:

```
bash tools/check-governance.sh
python3 tools/validate-frontmatter.py
```

Both MUST exit 0. The executor MUST NOT commit if either fails.

## E — Expectations (Deliverable Lock)

On completion, the following files MUST exist and be staged:

| Path | Content shape |
|---|---|
| `/SKILLS.md` | The new root spec, eleven sections, RFC-2119 throughout, ≥ 1 Gherkin scenario per normative section. |
| `/templates/skill.md` | New SKILL.md skeleton. |
| `/AGENTS.md` | Three small edits (routing, ontology, no closing-procedure change). |
| `/FOLDERS.md` | Two small edits (§1 topology, §6 audit graph). |
| `/PROMPT.md` | One-line cross-reference note. |
| `/RESEARCH.md` | One-line cross-reference note. |
| `/skills/readme.md` | One-line replacement of the Open Blockers entry. |
| `/tasks/009-author-skills-root-spec/task.md` | All Todo boxes ticked; `task_status: done`; `updated` field today. |
| `/tasks/009-author-skills-root-spec/friction-log.md` | Per `FRUSTRATED.md`; FL declaration mandatory. |

The executor MUST NOT modify existing skill bodies (`/skills/<slug>/SKILL.md` for slugs other than `skills-skill-bootstrap`) in this run. Conformance migration is a downstream task.

## Constraints

1. **MUST NOT** introduce a new top-level directory. `/skills/` already exists.
2. **MUST NOT** ratify any UNCERTAIN marker from `research/skills-skill-architecture/output/SPEC.md` as a normative statement without explicit citation. Unresolved uncertainties MUST be deferred to §10 Open Questions.
3. **MUST NOT** define `skill_*` keys that nest deeper than one level. The YAML depth rule is non-negotiable (per `TASK.md §3.4`).
4. **MUST** keep `SKILLS.md` self-contained: every term, framework, or convention referenced MUST be either defined in §1 or linked to its canonical source.
5. **MUST** preserve idempotency: re-running the executor against the post-edit tree MUST be a no-op (no changes detected by `git diff`).
6. **SHOULD** keep `SKILLS.md` under 600 lines; if longer, factor into `SKILLS.md` + `maintenance/skills-spec-extras.md`.
7. **MUST** declare an FL value (FL0 inclusive) in the friction log per `FRUSTRATED.md`.
