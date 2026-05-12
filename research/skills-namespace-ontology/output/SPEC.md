---
type: research
status: completed
slug: skills-namespace-ontology
summary: "Ratified skill_* L2 namespace ontology: five skill_kind values, three skill_tier values, two-case reciprocity rule (broken target = error; missing complement = warning), 14-skill mapping table, deprecated metadata.* key map, and three-batch migration plan."
created: 2026-05-05
updated: 2026-05-05
research_phase: complete
research_executes_prompt: skills-namespace-ontology
research_friction_level: FL0
---

# `skill_*` L2 Namespace Ontology — Ratified Spec

**Status:** Ratified output. Consumed by [Task 009](../../../../tasks/009-author-skills-root-spec/) (SKILLS.md) and [Task 011](../../../../tasks/011-skills-frontmatter-schema-files/) (JSON Schema).

**RFC 2119:** The key words MUST, MUST NOT, REQUIRED, SHALL, SHALL NOT, SHOULD, SHOULD NOT, RECOMMENDED, MAY, and OPTIONAL in this document are to be interpreted as described in BCP 14 [RFC 2119] [RFC 8174].

**Scope:** This document ratifies the `skill_*` L2 namespace proposed in `research/skills-navigation-bootstrap/output/SPEC.md` §3.2 and Annex A §A.4–§A.6. It does NOT modify any `SKILL.md` body. Migration is planned here and executed by Task 009.

---

## 1. Ratified `skill_kind` Vocabulary

`skill_kind` MUST be one of the following five values. The vocabulary is closed; new values require a spec amendment.

| Value | RFC 2119 | Definition |
|---|---|---|
| `meta` | REQUIRED | A cross-cutting skill that intercepts or routes all agent interactions regardless of user-message domain. Activates before domain or tool skills. Currently: exactly one (`prompt-optimizer`). |
| `domain` | REQUIRED | A content-domain expertise skill. Holds deep knowledge of a specific subject (narrative theory, music production, creative writing). Activated by domain-relevant trigger phrases. |
| `tool` | REQUIRED | A utility or integration skill. Performs a discrete operation (file conversion, API interaction, artifact generation, spec authoring). Activated by task-type trigger phrases. |
| `bootstrap` | RESERVED | A system-management skill responsible for materialising or verifying the canonical skill set. Not host-activatable. Currently: `skills-skill-bootstrap/` (has no SKILL.md — not a skill body). Reserved for future system skills with SKILL.md. |
| `adapter` | RESERVED | A cross-agent portability shim. Translates the canonical SKILL.md format for agents that do not natively support it (e.g., Jules, gemini-cli). No current instances. |

**Mapping consistency check:** All 14 existing skills map to exactly one value. No conflicts found. See §3.

---

## 2. Ratified `skill_tier` Vocabulary

`skill_tier` MUST be one of the following three values, exactly as proposed in the source SPEC.md.

| Value | RFC 2119 | Definition | Manifest behaviour |
|---|---|---|---|
| `T1` | REQUIRED | Always-on skill. Activates for every agent interaction without an explicit user trigger. Body is summarised in the manifest; full body is pre-loaded before any user message is processed. | `"tier": "T1"` in manifest; agent pre-loads body at session start. |
| `T2` | REQUIRED | Standard on-trigger skill. Full body loaded when the host matches the user message against `skill_triggers` or the `description` field. Default tier. | `"tier": "T2"` in manifest; body loaded on match. |
| `T3` | REQUIRED | Reference-heavy skill. Body is primarily an index into a large `references/` corpus. Sections are queried lazily via `tools/skills-index.py get <slug> --section <name>` rather than loading the full body. | `"tier": "T3"` in manifest; body loaded on match; references queried on demand. |

**T3 threshold:** Per `research/skills-navigation-bootstrap/output/SPEC.md` §A.10.3, T3 is appropriate when `references/` content exceeds the body by an order of magnitude. Currently met by `dramatica-theory` (15 reference files) and `dramatica-vocabulary` (18 reference files).

---

## 3. Skill-by-Skill Mapping Table

All 14 existing skill bodies, with ratified `skill_kind`, `skill_tier`, `skill_uses`, `skill_complements`, `skill_triggers` source, and `skill_supersedes`.

| Skill slug | `skill_kind` | `skill_tier` | `skill_uses` | `skill_complements` | trigger source | `skill_supersedes` |
|---|---|---|---|---|---|---|
| `dramatica-theory` | `domain` | `T3` | `[]` | `[dramatica-vocabulary, ncp-author]` | prose in description | — |
| `dramatica-vocabulary` | `domain` | `T3` | `[]` | `[dramatica-theory, ncp-author]` | prose in description | — |
| `drive-markdown-converter` | `tool` | `T2` | `[]` | `[]` | `metadata.triggers` | — |
| `gdrive-notion-curator` | `tool` | `T2` | `[]` | `[]` | prose in description | — |
| `ncp-author` | `domain` | `T2` | `[dramatica-theory, dramatica-vocabulary]` | `[dramatica-theory, dramatica-vocabulary, novel-architect]` | `metadata.triggers` | — |
| `notebooklm-prompt-architect` | `tool` | `T2` | `[]` | `[]` | `metadata.triggers` | — |
| `novel-architect` | `domain` | `T2` | `[ncp-author, dramatica-theory, dramatica-vocabulary, research-prompt-optimizer, drive-markdown-converter]` | `[ncp-author]` | prose in description | — |
| `pdf-to-markdown` | `tool` | `T2` | `[]` | `[]` | prose in description | — |
| `prompt-optimizer` | `meta` | `T1` | `[]` | `[]` | `metadata.triggers` | — |
| `ralph-skill` | `tool` | `T2` | `[spec-skill]` | `[spec-skill]` | `metadata.triggers` | — |
| `research-prompt-optimizer` | `tool` | `T2` | `[]` | `[]` | `metadata.triggers` | — |
| `spec-skill` | `tool` | `T2` | `[]` | `[ralph-skill]` | prose in description | — |
| `suno-lyric-writer` | `domain` | `T2` | `[]` | `[the-agency-system-architect]` | `metadata.triggers` | — |
| `the-agency-system-architect` | `domain` | `T2` | `[suno-lyric-writer]` | `[suno-lyric-writer]` | prose in description | — |

**Notes on `skill_uses` derivation:**
- `novel-architect` → "routes Skill-Pipeline (dramatica-theory, dramatica-vocabulary, ncp-author, research-prompt-optimizer, doc-coauthoring, drive-markdown-converter)". `doc-coauthoring` and `memory-sync` are NOT present as skills in this repo; excluded.
- `ncp-author` → "Actively co-invokes dramatica-theory … and dramatica-vocabulary …".
- `ralph-skill` → "Uses **spec-skill** (apply mode) against `references/ralph-spec.md`".
- `the-agency-system-architect` → "Delegates lyric craft to the `suno-lyric-writer` skill".

**Notes on `skill_complements` derivation:**
- `skill_complements` is the symmetric counterpart of `skill_uses`. If A uses B, then B.skill_complements SHOULD list A.
- `ncp-author` also complements `novel-architect` (reverse of novel-architect uses ncp-author).
- `spec-skill` complements `ralph-skill` (reverse of ralph-skill uses spec-skill).
- `suno-lyric-writer` complements `the-agency-system-architect` (reverse of that skill using suno-lyric-writer).

---

## 4. Reciprocity Rule (Ratified)

The original draft specified one undifferentiated "warning" case. This spec ratifies a two-case rule with differentiated severity.

### Case 1 — Broken Dependency Target (ERROR)

> If `A.skill_uses` lists slug `B` and no `skills/B/SKILL.md` exists, the linter MUST exit non-zero and report the broken dependency.

**Rationale:** `skill_uses` is an operational dependency declaration. A cannot function without B. A missing target is a functional failure, not merely a navigational gap. This case MUST be treated as an error to prevent silent runtime failures.

**RFC 2119 level:** MUST (linter error, blocks commit).

### Case 2 — Missing Complement (WARNING)

> If `A.skill_uses` lists `B`, and `B.skill_complements` does not list `A`, the linter SHOULD emit a warning (not error) citing this rule.

**Rationale:** `skill_complements` is a symmetric navigation hint — it tells the agent which other skills to consider activating together. Missing reciprocity reduces discoverability but does not break any operational function. An agent that activates A without knowing B complements it will still execute A correctly; it simply may not suggest B.

**RFC 2119 level:** SHOULD (linter warning, does not block commit).

### Case 3 — Asymmetric Complement (WARNING)

> If `A.skill_complements` lists `B` and `B.skill_complements` does not list `A`, the linter SHOULD emit a warning (not error).

**Rationale:** Same as Case 2. Pure navigational gap; no functional impact.

**RFC 2119 level:** SHOULD (linter warning, does not block commit).

### Summary Table

| Case | Condition | Severity | Blocks commit? |
|---|---|---|---|
| 1 | `A.skill_uses: [B]` and `B` does not exist | ERROR | Yes |
| 2 | `A.skill_uses: [B]` and `B.skill_complements` omits A | WARNING | No |
| 3 | `A.skill_complements: [B]` and `B.skill_complements` omits A | WARNING | No |

---

## 5. Deprecated `metadata.*` Keys

The following `metadata.*` sub-keys are deprecated by `skill_*` equivalents. They MUST be removed during migration (planned, not executed here).

| `metadata.*` key | Deprecated by | Skills affected | Migration action |
|---|---|---|---|
| `metadata.always_on` | `skill_tier: T1` | `prompt-optimizer` | Replace with `skill_tier: T1` in frontmatter; remove `metadata.always_on`. |
| `metadata.category` | `skill_kind` | `drive-markdown-converter`, `ncp-author`, `notebooklm-prompt-architect`, `novel-architect`, `prompt-optimizer`, `ralph-skill`, `research-prompt-optimizer`, `suno-lyric-writer` | Map category value to `skill_kind` per §1; add `skill_kind` key; remove `metadata.category`. |
| `metadata.triggers` | `skill_triggers` | `drive-markdown-converter`, `ncp-author`, `notebooklm-prompt-architect`, `prompt-optimizer`, `ralph-skill`, `research-prompt-optimizer`, `suno-lyric-writer` | Copy value into `skill_triggers` as YAML list (split on `, `); remove `metadata.triggers`. |

### `metadata.*` Keys to Retain

The following keys are NOT deprecated. They have no `skill_*` equivalent and serve distinct purposes.

| `metadata.*` key | Retain reason |
|---|---|
| `metadata.version` | Versioning — no skill_* equivalent; used by manifest for staleness detection. |
| `metadata.status` | Operational lifecycle (mvp, stable, deprecated) — distinct from skill_tier. |
| `metadata.source` | Attribution/provenance — informational, not functional. |
| `metadata.date_added` | Provenance chronology. |
| `metadata.research_sources` | Evidence trail for skill body claims (ralph-skill). |
| `metadata.upstream_pin` | Version-pinned external dependency (ncp-author). |
| `metadata.upstream_repo` | External repo reference (ncp-author). |
| `metadata.project` | Project assignment (novel-architect) — runtime scoping context. |
| `metadata.granularity` | Project-specific config (ncp-author). |
| `metadata.language` | Language scope (ncp-author). |
| `metadata.category` for non-deprecated categories | See above — only deprecated when a matching skill_kind value exists. |

### Category → skill_kind Mapping

| `metadata.category` value | `skill_kind` value |
|---|---|
| `meta` | `meta` |
| `agentic-workflow` | `tool` |
| `prompt-engineering` | `tool` |
| `tool-integration` | `tool` |
| `narrative-systems` | `domain` |
| `creative-writing` | `domain` |
| `creative` | `domain` |

---

## 6. Migration Plan

Migration MUST NOT modify the `name:` or `description:` fields of any SKILL.md. Those fields are read by the host runtime and changing them breaks activation. The `skill_*` keys are additive and coexist with the Anthropic schema.

### Batch 1 — Add-Only (no existing metadata changes)

**Skills:** `dramatica-theory`, `dramatica-vocabulary`, `drive-markdown-converter`, `gdrive-notion-curator`, `pdf-to-markdown`, `spec-skill`, `the-agency-system-architect`

**Change:** Add `skill_kind`, `skill_tier`, `skill_uses`, `skill_complements`, `skill_triggers` keys. No keys removed.

**Risk:** Low. Pure addition; host behavior unchanged.

**PR scope:** One PR per 2–3 skills for reviewable diff size.

### Batch 2 — Add skill_* and Deprecate `metadata.category` + `metadata.triggers`

**Skills:** `drive-markdown-converter` (move from Batch 1 if metadata present), `ncp-author`, `notebooklm-prompt-architect`, `novel-architect`, `ralph-skill`, `research-prompt-optimizer`, `suno-lyric-writer`

**Change:** Add `skill_*` keys AND remove `metadata.category` and `metadata.triggers`. For `metadata.triggers`, lift the comma-separated value into a YAML list under `skill_triggers`.

**Risk:** Medium. Removes metadata keys; other tooling or agents reading `metadata.triggers` will no longer find it. Verify no tool currently consumes `metadata.triggers` before executing. (Current check: `tools/validate-frontmatter.py` does not validate `metadata.*` keys. Risk is low but non-zero.)

**PR scope:** One PR per skill to keep diffs focused.

### Batch 3 — prompt-optimizer (Highest Risk)

**Skills:** `prompt-optimizer` only.

**Change:** Add `skill_tier: T1`, `skill_kind: meta`, `skill_triggers: [...]`. Remove `metadata.always_on`, `metadata.category`, `metadata.triggers`.

**Risk:** High. `prompt-optimizer` is the only always-on skill. Removing `metadata.always_on` changes its activation semantics if the host currently reads that field. Prerequisite: confirm whether the claude.ai host reads `metadata.always_on` or the `description` field for always-on behavior before removing it. If host reads `metadata.always_on`, retain it alongside `skill_tier: T1` until the host is updated.

**PR scope:** Dedicated single-skill PR with explicit test steps.

### Trigger Lifting Guide

For skills where triggers are embedded prose in `description:` (not in `metadata.triggers`), the executing agent MUST extract the trigger phrase list manually. Patterns to look for:

| Pattern | Skills |
|---|---|
| `"Trigger phrases include — ..."` followed by comma-separated list | `dramatica-theory`, `pdf-to-markdown` |
| `"Trigger explizit bei ..."` followed by comma-separated list | `dramatica-vocabulary` |
| `"Trigger bei ..."` followed by comma-separated list | `gdrive-notion-curator` |
| `"Trigger — ..."` followed by comma-separated list | `novel-architect` |
| `"Triggers on: ..."` followed by comma-separated list | `the-agency-system-architect` |
| `"Triggers on terms like ..."` followed by comma-separated list | `spec-skill` |

The extracted trigger list MUST be stored as a flat YAML list (no nesting):

```yaml
skill_triggers:
  - dramatica
  - story mind
  - storyform
```

---

## 7. Open Questions Surfaced

No open questions were surfaced that require new follow-up prompts. All decisions in this run are self-contained and justified from on-disk evidence.

The following pre-existing follow-up prompts remain unexecuted and are NOT addressed by this run:

- `prompts/skills-manifest-emission-tool/` — manifest emitter contract (error codes, exit codes, full JSON Schema). Pre-condition for Task 010.
- `prompts/skills-skill-trigger-lifecycle/` — claude.ai trigger lifecycle (UNCERTAIN U3). Requires Gemini PDF.
- `prompts/claude-ai-container-git-verification/` — empirical verification of git binary.

These are tracked per `research/skills-navigation-bootstrap/output/SPEC.md` §7 (Open Questions Summary) and remain routed to their respective follow-up prompts.
