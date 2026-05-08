---
type: adr
status: active
slug: 0006-agency-system-prototype-exemption
summary: "/Agency-System/ is a frontend-prototype folder consumed by skills/the-agency-system-architect/; this ADR formalises its exemption from FOLDERS.md §1 operational-folder rules and the §7 audit graph."
created: 2026-05-08
updated: 2026-05-08
adr_id: ADR-0006
adr_status: Accepted
adr_owner: agency-maintainer
adr_tags:
  - folder-topology
  - exemption
  - prototype
  - skills
---

# ADR-0006 — `/Agency-System/` Frontend-Prototype Exemption

## Context and Problem Statement

The repository's [FOLDERS.md §1](../FOLDERS.md) enforces a strict
operational-folder rule: only `/tasks/`, `/prompts/`, and `/research/`
hold orchestration / instruction / evidence content; every other
top-level folder is either a governance fixture (`/tools/`,
`/maintenance/`, `/templates/`, `/decisions/`) or an explicit
exemption recorded in §8.

`/Agency-System/` is a frontend-prototype storage folder containing
HTML / JSX / SVG sources for the "Agency System triptychon" UI. The
folder is consumed by [`skills/the-agency-system-architect/`](../skills/the-agency-system-architect/)
as a design-system reference; nothing else in the repo loads from
it. Without an ADR backing the exemption, a future maintenance agent
would correctly read FOLDERS.md §8 line 192 ("authoring ADR pending")
and either (a) file a Task to delete the folder or (b) try to wedge
it into the operational ontology — both wrong outcomes.

The README §4 topology tree at `94-95` lists `/Agency-System/`
alongside the other exempt non-operational directories; FOLDERS.md
§8 enumerates it but flags the ADR as pending. This ADR closes that
loop.

## Decision Drivers

- **Skill-asset opacity.** Frontend prototype assets (HTML, JSX, SVG)
  are not Markdown and carry no frontmatter; forcing them through
  `tools/fm/validate.py` would either require an exemption every
  time fm-validate is extended, or produce constant noise.
- **One-skill consumer.** `/Agency-System/` is referenced from
  exactly one skill (`skills/the-agency-system-architect/`); moving
  the assets into `/skills/the-agency-system-architect/assets/`
  would inflate every load of that skill with multi-megabyte
  artefacts a non-narrative session must not pay for.
- **Mechanical-enforcement clarity.** The audit graph
  (`tools/check-audit-graph-consistency.py`) walks frontmatter
  edges; a folder with no operational frontmatter is invisible to
  it. Recording the carve-out in an Accepted ADR makes the
  invisibility intentional rather than incidental.

## Considered Options

1. **Move assets into `skills/the-agency-system-architect/assets/`**
   (no exemption needed). Rejected: each skill load would pull in
   the prototype assets (≈ 1.5 MB at branch-time); session-token
   regression on every session that mentions the skill.
2. **Treat `/Agency-System/` as an operational folder** (require
   frontmatter, audit-graph linkage). Rejected: HTML / JSX / SVG do
   not carry the L1 + L2 ontology; producing a synthetic frontmatter
   layer for every prototype file is over-engineering with no
   downstream consumer.
3. **Carve-out exemption recorded in this ADR (chosen).** The folder
   is treated as opaque storage; only its `readme.md` is required to
   carry L1 frontmatter (per FOLDERS.md F.5); inbound references
   from skills travel via plain Markdown links rather than
   frontmatter audit edges.
4. **Delete the prototype.** Rejected: the design-system mock is the
   intended starting surface for human-led UI iteration; deleting it
   loses authored work.

## Decision Outcome

`/Agency-System/` is a top-level folder exempt from the FOLDERS.md §1
operational-folder rule and from the §7 audit-graph linkage rule.
The folder's contents (HTML / JSX / SVG / JS) are opaque to
`tools/fm/validate.py` and to the linkage linter. The folder MUST
carry a `readme.md` declaring its purpose, its consuming skill, and
its lifecycle (per FOLDERS.md F.5). Inbound references from
`skills/the-agency-system-architect/` MUST travel as plain Markdown
links inside `SKILL.md` (or its references), not as frontmatter
audit edges.

The README §4 topology tree and FOLDERS.md §8 entry already record
the exemption; this ADR is the binding authority FOLDERS.md §8 was
waiting for. Once `Accepted`, FOLDERS.md §8 SHOULD drop the
"authoring ADR pending" parenthetical via a follow-up T1 / T2 edit.

## Consequences

- **Positive.** The carve-out is discoverable as an ADR rather than
  a buried table cell; future maintenance agents see the rationale
  in seconds. The frontend prototype stays editable without
  collateral governance work; skill consumers pay zero
  asset-load cost on non-narrative sessions.
- **Negative.** One more "exempt" surface to remember. The
  exemption is targeted (one folder, one consuming skill); growing
  the exempt set further would require reconsidering whether the
  operational-folder rule itself is doing the right work.
- **Neutral.** The narrative skills (`skills/novel-architect/`,
  `skills/suno-lyric-writer/`) follow a parallel pattern — they ship
  large reference corpora that consumers MUST NOT autoload (NO.5).
  This ADR does not formalise that pattern; that decision lives in
  Task 056 (narrative-skills-extraction-adr).
