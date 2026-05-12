---
type: index
status: active
slug: upstream-snapshot-index
summary: "Verbatim snapshot of SuperClaude_Framework v4.3.0 + Superpowers v4.0.3 skill corpora, staged for Phase 2 evaluation. Read-only mirror; re-syncs require a new Task per ADR-0011 D.9."
created: 2026-05-12
updated: 2026-05-12
---

# Upstream Snapshot — Phase 2 evaluation staging

**What:** Verbatim, read-only mirror of every file that constitutes a "skill corpus" in the two upstream repositories ratified by [ADR-0011](../../../../decisions/0011-external-skill-corpora-import.md). Provided to enable per-skill triage ("concept them one by one") ahead of Phase 2 import. **No transformation, no curation** — these are byte-identical mirrors of upstream content.

**Why here:** Phase 1 (ST-1 of Task 091) ported 14 specific skills. The remaining upstream corpus is Phase 2 / out-of-scope for ST-1 (per [`../full-plan-part-2.md` §5](../full-plan-part-2.md)) but the user wants the raw material staged in-tree so each skill can be evaluated, adapted, or rejected on its merits.

## Snapshot provenance

| Vendor | Upstream repo | Pinned SHA | Version tag | Snapshot date |
|---|---|---|---|---|
| `superclaude` | [`SuperClaude-Org/SuperClaude_Framework`](https://github.com/SuperClaude-Org/SuperClaude_Framework) | `22ad3f483a6fe6c626834e1c9a3573126644a058` | v4.3.0 | 2026-05-12 |
| `superpowers` | [`obra/superpowers`](https://github.com/obra/superpowers) | `b9e16498b9b6b06defa34cf0d6d345cd2c13ad31` | v4.0.3 | 2026-05-12 |

Both SHAs are mirrored on the `netzkontrast/*` org per the repo-scope policy in this session.

## Structure

This snapshot is the **complete working tree** of each upstream repo (excluding `.git/`, `__pycache__/`, `*.pyc`, `.pytest_cache/`, `.benchmarks/`). Per the user's directive ("every file from the corresponding repos"), all non-VCS, non-cache content is staged so the eventual Phase 2 triage can evaluate skills in their native context (docs/tests/plugins/manifests all intact).

### `superclaude_framework/` — 411 files (~3.8 MB)

```
superclaude_framework/
├── docs/        (126 files) — full upstream documentation tree
├── plugins/     (94 files)  — plugin packaging: plugins/superclaude/{commands,agents,modes,skills,…}
├── src/         (123 files) — Python source + skill corpora:
│                              src/superclaude/{agents,commands,modes,skills,pm_agent,cli,core,hooks,mcp,scripts}/
├── tests/       (16 files)  — upstream pytest suites
├── scripts/     (8 files)   — build / release / utility scripts
├── skills/      (2 files)   — root-level skills marker (confidence-check only)
├── *.md         (~24 files) — README, CHANGELOG, CLAUDE.md, AGENTS.md, TASK.md, planning docs
└── (root)       — LICENSE, Makefile, pyproject.toml, package.json, setup.py, VERSION, install.sh
```

Source: `/home/user/SuperClaude_Framework/` working tree at SHA `22ad3f48`.

### `superpowers/` — 104 files (~900 KB)

```
superpowers/
├── .claude-plugin/  (2 files)  — plugin manifest + plugin descriptor
├── .codex/          (3 files)  — Codex-flavoured plugin descriptor
├── .opencode/       (2 files)  — OpenCode-flavoured plugin descriptor
├── .github/         (1 file)   — GitHub workflows / config
├── agents/          (1 file)   — agent personas
├── commands/        (3 files)  — slash commands
├── docs/            (7 files)  — skill-architecture documentation
├── hooks/           (3 files)  — SessionStart / pre-tool-use hook scripts
├── lib/             (1 file)   — shared library
├── skills/          (35 files) — primary skill corpus (brainstorming, executing-plans, systematic-debugging, …)
├── tests/           (42 files) — upstream test suites
└── (root)           — LICENSE, README.md, RELEASE-NOTES.md, .gitignore
```

Source: `/home/user/superpowers/` working tree at SHA `b9e16498`.

## Phase 1 already imported (do not re-port)

The 14 skills below are already ported under [`skills/sc-*/`](../../../../skills/) per ST-1. Their snapshot copies remain here for diff-tracking; do not re-port them.

- From `superclaude_framework/commands/`: `createPR.md`, `implement.md`, `test.md`, `improve.md`, `research.md`.
- From `superclaude_framework/agents/`: `backend-architect.md`, `frontend-architect.md`, `refactoring-expert.md`, `performance-engineer.md`, `system-architect.md`, `security-engineer.md`, `quality-engineer.md`, `deep-research-agent.md`, `pm-agent.md`.
- From `superclaude_framework/modes/`: `MODE_Orchestration.md`, `MODE_DeepResearch.md` (bundled as `references/` inside `sc-implement` / `sc-research`).

## Triage workflow (suggested)

For each candidate skill in this snapshot, evaluate:

1. **Is the underlying capability missing from Agency's stack?** If covered (e.g. by an existing native skill or root spec), skip.
2. **Does it bind to an MCP server Agency does not ship?** If yes, adapt the body per ADR-0011 D.8 before porting.
3. **Is the upstream body ≤ 5 KB?** If not, the overflow must move to `references/` per ADR-0011 D.6.
4. **What is its audit-graph position?** Identify `skill_references_skills` edges (forward refs) to siblings already in `/skills/`.
5. **What is its tier (L1–L4)?** Determines landing order in the next batch's build DAG.

When ready to port: file a new Task (`tasks/<NNN>-port-<vendor>-phase-2-<batch>/`) citing ADR-0011 and following the §10 design recipe from this Epic.

## Governance carve-outs

Because these files are byte-identical upstream mirrors, Agency frontmatter and PC.1.1 script-hygiene cannot be imposed on them without violating ADR-0011 D.9 (no-edit on imports). Two carve-outs make `tools/check-governance.sh` exit 0 over the snapshot:

- [`tools/.frontmatter-waivers`](../../../../tools/.frontmatter-waivers) — `tasks/091-port-external-skill-corpora/references/upstream-snapshot/*` waived for rule `*`, expires `2026-08-12`. Tracks the Phase 2 triage deadline (90 days).
- [`tools/.script-allowlist`](../../../../tools/.script-allowlist) — same glob, exempts the ~80 `.py` / `.sh` files from PC.1.1.

When triage finishes (whether by porting or by deciding-not-to-port each skill), the snapshot directory should be **deleted in its entirety**, and the two waivers above should be removed. The 2026-08-12 expiry forces that conversation.

## Assumptions Log

- This snapshot is **read-only**. Touching any file under `superclaude_framework/` or `superpowers/` is a T4 violation — these are byte-identical upstream mirrors. To "edit" a file, port it to `/skills/<vendor>-<slug>/` and adapt there.
- The snapshot is a one-shot capture at 2026-05-12 per ADR-0011 D.9; subsequent upstream releases require a new Task to refresh.
- Files include non-Markdown artefacts (`__init__.py`, `pyproject.toml`, hook shell scripts) that are part of how upstream skills *run*, not what they *are*. Phase 2 ports must decide per-file whether to include the runtime scaffolding or just the SKILL.md-equivalent prose.
