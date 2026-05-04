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

**IMPORTANT FINDING**: Claude Code's skill mechanism (`~/.claude/skills/<name>/SKILL.md`) is structurally identical to what the mission describes for `claude.ai`. A skill is a folder containing `SKILL.md`. The same file format works in both systems. This means the same `SKILL.md` bodies in `/skills/<name>/` can be synced to either platform without transformation.

### Non-destructive by default

Running `sync.sh` without `--clean` will not delete local skills that are absent from the repo (e.g., the pre-existing `session-start-hook` skill). Use `--clean` to enforce exact parity. This prevents accidental deletion of skills installed by other means.

### Idempotent

`sync.sh` is safe to run multiple times. It overwrites existing `SKILL.md` files only when their content differs from the canonical remote. The `verify.sh` script confirms the no-op state after a clean sync.

### Manual trigger, no cron

The sync is invoked on demand by a human or another script. No systemd timer or cron job is created here — those would be fragile in a sandboxed container environment. The expected trigger points are:
1. After any PR to `main` that modifies `/skills/`.
2. At the start of a new Claude Code session (can be added to a `SessionStart` hook in `.claude/settings.json`).

### Scheduling via SessionStart hook (optional)

To automate syncing at session start, add this to `.claude/settings.json`:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "/home/user/agency/skills/skills-skill-bootstrap/sync.sh"
          }
        ]
      }
    ]
  }
}
```

This is **not** enabled by default. The path is absolute and assumes the repository is checked out at `/home/user/agency`. Adjust for your environment.

## How to Use

### Sync skills from origin/main

```bash
cd /path/to/agency
skills/skills-skill-bootstrap/sync.sh
```

### Verify sync state (check if up-to-date)

```bash
skills/skills-skill-bootstrap/verify.sh
# exit 0 = all skills in sync
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
4. Re-run `verify.sh` to confirm recovery.

If `origin/main:skills/` is missing entirely (before Stage A merges), `sync.sh` exits 0 with a warning. This is expected pre-Stage A.

## How a Human Verifies Sync State

```bash
skills/skills-skill-bootstrap/verify.sh && echo "All skills in sync"
```

Non-zero exit means at least one skill is missing or diverged. The script prints which ones.

## Assumptions Log

- `~/.claude/skills/` is the correct target for Claude Code user skills. This was confirmed by inspecting `/root/.claude/skills/` on the running installation. If Anthropic changes this path, update the default in `sync.sh`.
- `git show origin/main:skills/<name>/SKILL.md` is sufficient to extract skill content. If skills gain binary assets, this approach needs revision.
- The `session-start-hook` skill currently in `~/.claude/skills/` is NOT in the repo's `/skills/` and will NOT be touched by a non-`--clean` sync. It was installed by other means and is treated as an external resource.
- This folder intentionally does NOT have `/skills/skills-skill/` as a neighbor yet — that path is reserved for the future `skills-skill` loader implementation and must not be created until the architecture spec is finalized.
