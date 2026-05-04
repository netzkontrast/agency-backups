---
type: index
status: active
slug: skills-skill-bootstrap
summary: "On-demand sync tool that pulls skill bodies from origin/main:/skills/ into Claude Code's ~/.claude/skills/ directory."
created: 2026-05-04
updated: 2026-05-04
---

# /skills/skills-skill-bootstrap/

## What and Why

This folder is the **local maintenance sync mechanism** for keeping Claude Code's user-scoped skill capability aligned with the canonical skill bodies in this repository.

### Problem it solves

Claude Code loads user skills from `~/.claude/skills/<name>/SKILL.md`. Without a sync mechanism, these files diverge from the versioned content in `origin/main:/skills/` after every PR that updates a skill. A human or CI job must be able to re-align them reliably, without manual copying.

### What it does NOT do

- It does **not** implement the future `skills-skill` loader (`/skills/skills-skill/` is reserved for that).
- It does **not** modify anything inside the repository — it is strictly a one-way pull from repo → local filesystem.
- It does **not** touch `~/.claude/commands/` or `~/.claude/agents/` — only `~/.claude/skills/`.

## Linked Navigation

| File | Purpose |
|---|---|
| [sync.sh](./sync.sh) | Pull skills from `origin/main:/skills/` → `~/.claude/skills/` |
| [verify.sh](./verify.sh) | Verify sync state; exits non-zero if any skill is missing or diverged |
| [readme.md](./readme.md) | This file |

## Design Decisions (Justification Log)

### Sync direction: repo → local (one-way)

The repo is the canonical source of truth. `~/.claude/skills/` is an ephemeral consumer. Edits always flow through PRs to `main`, never from the local skill directory back to the repo. This prevents conflicting states.

### Target location: `~/.claude/skills/`

This is Claude Code's user-scoped skill directory, confirmed by inspecting the running installation at `/root/.claude/skills/`. It is the closest equivalent to claude.ai's `/mnt/skills/user/`. No dedicated "skill path" config key exists in `settings.json`; the location is a convention, not a setting.

**Key finding**: Claude Code's skill mechanism (`~/.claude/skills/<name>/SKILL.md`) is structurally identical to claude.ai's `/mnt/skills/user/<name>/SKILL.md`. The same `SKILL.md` bodies in `/skills/<name>/` sync to either platform without transformation.

### Non-destructive by default

Running `sync.sh` without `--clean` will not delete local skills that are absent from the repo (e.g., the `session-start-hook` skill). Use `--clean` to enforce exact parity.

### Idempotent

`sync.sh` is safe to run multiple times. It uses `cmp -s` (binary comparison) to skip skills already in sync. Re-running against an up-to-date state completes with `0 synced, 14 already-in-sync, 0 errors`.

### Skill discovery uses `-d --name-only`

`git ls-tree -d --name-only origin/main:skills/` returns only tree objects (directories), which naturally excludes flat files like `readme.md`. This is safer than filtering by name — it scales to any future non-skill file added at the skills/ root.

### Manual trigger, no cron

Invoked on demand. Expected trigger points:
1. After any PR to `main` that modifies `/skills/`.
2. At the start of a new Claude Code session (via SessionStart hook, optional — see below).

### Scheduling via SessionStart hook (optional)

To automate syncing at session start, add to `.claude/settings.json` (adjust the repo path):

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "$(git -C \"$CLAUDE_PROJECT_DIR\" rev-parse --show-toplevel)/skills/skills-skill-bootstrap/sync.sh"
          }
        ]
      }
    ]
  }
}
```

Or with a fixed path if you know the checkout location:

```json
"command": "/your/path/to/agency/skills/skills-skill-bootstrap/sync.sh"
```

This is **not** enabled by default.

## How to Use

### List available skills

```bash
skills/skills-skill-bootstrap/sync.sh --list
```

### Sync skills from origin/main

```bash
cd /path/to/agency
skills/skills-skill-bootstrap/sync.sh
```

### Verify sync state

```bash
skills/skills-skill-bootstrap/verify.sh
# exit 0 = all canonical skills in sync (LOCAL-only skills are reported but don't fail)
# exit 1 = missing or diverged skills; run sync.sh to fix
```

### Full clean sync (also removes local skills absent from repo)

```bash
skills/skills-skill-bootstrap/sync.sh --clean
```

### Custom target directory

```bash
skills/skills-skill-bootstrap/sync.sh --target /some/other/path
```

## Recovery Procedure

If sync produces an error or the local skill directory is corrupt:

1. Run `verify.sh` to identify which skills are affected.
2. Delete the offending skill folder: `rm -rf ~/.claude/skills/<name>/`
3. Re-run `sync.sh` to re-create it from the canonical source.
4. Re-run `verify.sh` to confirm recovery (exit 0).

## How a Human Verifies Sync State

```bash
skills/skills-skill-bootstrap/verify.sh && echo "All skills in sync"
```

`verify.sh` prints `OK`, `MISSING`, `DIVERGED`, or `LOCAL` for each skill. `LOCAL` entries (skills present locally but absent from the repo) are informational and do not cause a non-zero exit.

## Assumptions Log

- `~/.claude/skills/` is the correct target for Claude Code user skills. Confirmed by inspecting `/root/.claude/skills/` on the running installation. If Anthropic changes this path, update the default in `sync.sh` and this readme.
- `git ls-tree -d --name-only` is used to enumerate skill directories. Tested against the live repo with 14 skills plus a `readme.md` at the skills root — the `-d` flag correctly excludes the readme.
- Only `SKILL.md` is synced per skill. Skills with `references/`, `scripts/`, or `agents/` subdirectories have those managed separately (they remain in the repo but are not synced to `~/.claude/skills/`). Claude Code loads `SKILL.md` only; the deeper content is fetched by the skill itself at runtime. If this assumption changes, `sync.sh` will need a `--deep` mode.
- The `session-start-hook` skill in `~/.claude/skills/` is NOT in the repo and is correctly reported as `LOCAL` by `verify.sh`. It is intentionally not touched.
- This folder intentionally does NOT have `/skills/skills-skill/` as a neighbor — that path is reserved for the future loader implementation.
