---
type: adr
status: active
slug: 0007-skill-bundles-tools-frontmatter
summary: "Introduces SKILL.md frontmatter key skill_bundles_tools so a skill MAY declare /tools/<slug>/ trees that sync.sh copies into <synced-skill>/scripts/_bundled/<slug>/ at sync time."
created: 2026-05-11
updated: 2026-05-11
adr_id: ADR-0007
adr_status: Accepted
adr_owner: agency-maintainer
adr_tags:
  - frontmatter
  - skills
  - sync
  - tooling
---

# ADR-0007 — `skill_bundles_tools` SKILL.md Frontmatter Key

## Context and Problem Statement

The canonical sync mechanism
[`skills/skills-skill-bootstrap/sync.sh`](../skills/skills-skill-bootstrap/sync.sh)
pulls only `SKILL.md` from `origin/main:skills/<name>/` into
`~/.claude/skills/<name>/`. Subdirectories (`scripts/`, `references/`,
`assets/`) are intentionally omitted (see
[skills-skill-bootstrap/readme.md §Assumptions Log](../skills/skills-skill-bootstrap/readme.md)).
Consequently, skills running inside Claude Code's user-skills sandbox at
`~/.claude/skills/<name>/` cannot reach the repo-resident toolchain at
`/home/user/agency/tools/`. Skills that need
[`tools/fm/`](../tools/fm/),
[`tools/adr/`](../tools/adr/), or
[`tools/dramatica-nav/`](../tools/dramatica-nav/) either re-implement
those helpers inline (token-bloat, drift) or rely on an `AGENCY_REPO`
path being present in the host environment (unreliable across
agents).

The need is selective: only skills with explicit toolchain
dependencies should pull tools into their sandboxed sibling tree. A
catch-all "always copy `/tools/` into every skill" approach is
rejected as over-broad. A repo-wide literal-copy approach (committing
duplicates of every tool under each consuming skill's `scripts/`) is
rejected as a DRY violation that guarantees drift.

## Decision Drivers

- **Sandbox isolation.** Skills loaded under `~/.claude/skills/` have
  no access to repo-relative paths; they need a sibling copy of any
  helper they shell out to.
- **Single source of truth.** Tools MUST live exactly once in
  `/tools/<slug>/` and be edited there; bundled copies are
  derived artefacts, not authored content.
- **Sync-time atomicity.** Materialising bundles during the existing
  sync pass keeps the operation idempotent and gives `verify.sh` a
  single drift-detection surface.
- **Opt-in.** Domain skills with no tool dependency
  (`suno-lyric-writer`, `prompt-optimizer`) MUST NOT pay any bundling
  cost.
- **Alignment with `tools/fm/` toolchain.** Frontmatter parsing inside
  `sync.sh` MUST go through `tools/fm/extract.py`
  ([CLAUDE.md §4](../CLAUDE.md)), not ad-hoc `sed`/`awk`.

## Considered Options

1. **Status quo — re-implement helpers inline in SKILL.md bodies.**
   Rejected: every change to `tools/fm/_core.py` silently breaks
   skills; token-bloat in every SKILL.md that recreates a YAML
   parser.
2. **Literal copies under `skills/<name>/scripts/<slug>/` committed
   to the repo.** Rejected: DRY violation; drift inevitable; the
   pre-commit hook would need a same-content cross-check between
   `skills/*/scripts/<slug>/` and `tools/<slug>/`, which is a
   different (and harder) maintenance burden than what this ADR
   adopts.
3. **Frontmatter-declared, sync-time materialised copy
   into `_bundled/` namespace (CHOSEN).** A new SKILL.md frontmatter
   key `skill_bundles_tools: [tools/<slug>, …]` declares the
   dependency; `sync.sh` rsyncs `/tools/<slug>/` into
   `<synced-skill>/scripts/_bundled/<slug>/` at sync time;
   `verify.sh` enforces parity. Tools stay in `/tools/`. The
   `_bundled/` directory is `.gitignore`d so the materialisation
   never re-enters the repo.
4. **Git submodules.** Rejected: hostile to the existing single-repo
   clone protocol; introduces a second `.git` surface that the
   bootstrap protocol would need to know about.

## Decision Outcome

Adopt option 3. A new top-level SKILL.md frontmatter key
`skill_bundles_tools` (list of strings) declares which
repo-relative `tools/<slug>` trees are to be materialised into the
synced skill's `scripts/_bundled/<basename>/`. The key is
OPTIONAL; absent or empty means "no bundles". Each list entry MUST
start with `tools/`, MUST resolve to an existing directory under
the repo root, and MUST contain no `..` segments.

### Frontmatter shape

The `skill` type in
[`maintenance/schemas/header-ontology.json`](../maintenance/schemas/header-ontology.json)
adds `skill_bundles_tools` to its `recommended_keys`. SKILL.md files
continue to use the Anthropic flat-frontmatter convention (`name`,
`description`); `skill_bundles_tools` is a sibling key at the same
level. Example:

```yaml
---
name: skill-creator
description: …
skill_bundles_tools:
  - tools/fm
  - tools/adr
---
```

### Pre-commit enforcement

`tools/fm/validate.py` gains a new check `_check_skill_bundles`
emitting diagnostics:

- **F.B.5** — entry is not a string, does not start with `tools/`,
  contains `..`, is duplicated, or does not resolve to an existing
  directory.
- **F.B.6** — declared bundle's transitive dependency missing. The
  static dependency map `BUNDLE_DEPS` in `tools/fm/_core.py`
  encodes which tools require which siblings; today
  `tools/adr` requires `tools/fm`.

### Sync-time materialisation

`skills/skills-skill-bootstrap/sync.sh` is rewritten so each
per-skill loop iteration:

1. Stages the entire `skills/<name>/` tree from `origin/main` via
   `git archive` and atomically rsync-swaps it into the
   target — preserving `scripts/_bundled/` across the swap.
2. Reads `skill_bundles_tools` via `tools/fm/extract.py` and rsyncs
   each declared `tools/<slug>` source into
   `<target>/scripts/_bundled/<basename>/` with `--checksum` for
   idempotency.
3. Writes a `.bundle.sha256` sidecar containing sorted hashes of
   the source files so `verify.sh` can detect drift independent
   of mtimes.

Companion changes: `verify.sh` enforces subtree presence and
bundle parity; the `_bundled/` namespace is added to `.gitignore`
to keep materialisation out of the repo.

### Tier classification

This is a **T3 structural change** to the SKILL.md schema, the
sync protocol, and the pre-commit gate — therefore it lands as
ADR-0007 in the same PR that ships the implementation, per
[CLAUDE.md §6](../CLAUDE.md).

## Consequences

### Positive

- Portable skills: any skill needing repo tooling declares it and
  receives a working copy at sync time.
- Single source of truth: tools live once in `/tools/`; the bundle
  is a derived artefact that never re-enters git.
- Drift detectable: `verify.sh` reports `BUNDLE-DRIFT` when the
  source moved without a re-sync, surfacing toolchain churn
  immediately.
- Auditable: every dependency is named in the SKILL.md
  frontmatter, lintable, and grep-able.

### Negative

- Tool-API churn (e.g. a rename inside `tools/fm/_core.py`)
  silently breaks every skill that bundles `tools/fm` until the
  next `sync.sh` run. Mitigated by (a) `verify.sh` exit code 1 on
  next bootstrap, (b) sync.sh idempotency (re-running is free),
  and (c) a recommended Nightly Maintenance verify pass.
- Not every tool is bundle-safe. Tools that read repo-relative
  paths (`tools/check-*.py` scanning `tasks/`, `prompts/`,
  `research/`) MUST NOT be declared — they cannot function in
  the sandbox. The validator does not enforce portability; that
  remains a reviewer concern. See §"Authorised Bundle Set" below.

### Neutral

- This ADR introduces the first SKILL.md frontmatter key whose
  value is a repo path, not a slug. `validate.py` therefore needs
  a path resolver in addition to its existing slug resolver. The
  added code path is local to `_check_skill_bundles` and does not
  affect any other diagnostic.

## Authorised Bundle Set (initial)

The following six skills receive `skill_bundles_tools` declarations
in the same PR (selective per tool-demand, justified per row):

| Skill | Bundles | Rationale |
|---|---|---|
| `skill-creator` | `tools/fm` | Authors SKILL.md; needs `fm/edit.py`/`fm/new.py` to honour YAML depth-1 rule. |
| `the-agency-system-architect` | `tools/fm`, `tools/adr` | Touches root specs and the ADR ledger; both validators required. |
| `spec-skill` | `tools/fm` | Writes `type: spec` artefacts. |
| `dramatica-theory` | `tools/dramatica-nav` | Ontology lookups via `nav.py` (NO.5 channel). |
| `ncp-author` | `tools/dramatica-nav` | NCP authoring depends on Dramatica term resolution. |
| `novel-architect` | `tools/dramatica-nav` | Narrative-ontology gateway. |

The selection deliberately excludes governance checkers and
maintenance scripts that depend on repo-relative directory walks
(`tasks/`, `research/`, `prompts/`, `decisions/`) — they would
not function in the sandbox.

## References

- [skills/skills-skill-bootstrap/sync.sh](../skills/skills-skill-bootstrap/sync.sh)
- [skills/skills-skill-bootstrap/verify.sh](../skills/skills-skill-bootstrap/verify.sh)
- [SKILLS.md §3.3](../SKILLS.md), §7 (Bootstrap Protocol), §9
- [maintenance/schemas/header-ontology.json](../maintenance/schemas/header-ontology.json)
- [tools/fm/validate.py](../tools/fm/validate.py),
  [tools/fm/_core.py](../tools/fm/_core.py),
  [tools/fm/extract.py](../tools/fm/extract.py)
- [CLAUDE.md §4 (Frontmatter rule)](../CLAUDE.md),
  [§6 (ADR governance)](../CLAUDE.md)
