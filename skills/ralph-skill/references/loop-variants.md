# Ralph Loop Script Variants — v1.1.0

All loop.sh variants for Ralph workflows.
**v1.1 additions**: Git worktrees workflow (from Spec-B B.5.2, R.2.9).

---

## Variant 1 — Base Loop (Minimal)

Geoff's original minimal form. Two lines.

```bash
#!/bin/bash
while :; do cat PROMPT.md | claude; done
```

Use for: rapid prototyping, understanding the concept. Not suitable for production.

---

## Variant 2 — Standard Loop (Recommended)

Plan/build mode selection, max-iterations, git push per iteration.

```bash
#!/bin/bash
# Usage: ./loop.sh [plan|build] [max_iterations]
# Examples:
#   ./loop.sh              # Build mode, unlimited
#   ./loop.sh 20           # Build mode, max 20 tasks
#   ./loop.sh build 20     # Build mode, max 20 tasks
#   ./loop.sh plan         # Plan mode, unlimited
#   ./loop.sh plan 5       # Plan mode, max 5 iterations

if [ "$1" = "plan" ]; then
    MODE="plan"; PROMPT_FILE="PROMPT_plan.md"; MAX_ITERATIONS=${2:-0}
elif [ "$1" = "build" ]; then
    MODE="build"; PROMPT_FILE="PROMPT_build.md"; MAX_ITERATIONS=${2:-0}
elif [[ "$1" =~ ^[0-9]+$ ]]; then
    MODE="build"; PROMPT_FILE="PROMPT_build.md"; MAX_ITERATIONS=$1
else
    MODE="build"; PROMPT_FILE="PROMPT_build.md"; MAX_ITERATIONS=0
fi

ITERATION=0
CURRENT_BRANCH=$(git branch --show-current)

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Mode:   $MODE"
echo "Prompt: $PROMPT_FILE"
echo "Branch: $CURRENT_BRANCH"
[ $MAX_ITERATIONS -gt 0 ] && echo "Max:    $MAX_ITERATIONS iterations"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ ! -f "$PROMPT_FILE" ]; then echo "Error: $PROMPT_FILE not found"; exit 1; fi

while true; do
    if [ $MAX_ITERATIONS -gt 0 ] && [ $ITERATION -ge $MAX_ITERATIONS ]; then
        echo "Reached max iterations: $MAX_ITERATIONS"; break
    fi

    cat "$PROMPT_FILE" | claude -p \
        --dangerously-skip-permissions \
        --output-format=stream-json \
        --model claude-opus-4-7 \
        --verbose

    git push origin "$CURRENT_BRANCH" || {
        echo "Failed to push. Creating remote branch..."
        git push -u origin "$CURRENT_BRANCH"
    }

    ITERATION=$((ITERATION + 1))
    echo -e "\n\n======================== LOOP $ITERATION ========================\n"
done
```

---

## Variant 3 — Extended Loop (All Enhancement Modes)

Adds: specs, reverse-engineer, plan-work, SLC planning.

```bash
#!/bin/bash
set -euo pipefail

# Usage:
#   ./loop.sh [plan|build|specs|reverse|slc] [max_iterations]
#   ./loop.sh plan-work "work description" [max_iterations]

MODE="build"; PROMPT_FILE="PROMPT_build.md"; MAX_ITERATIONS=0; WORK_DESCRIPTION=""

if [ "${1:-}" = "plan" ]; then
    MODE="plan"; PROMPT_FILE="PROMPT_plan.md"; MAX_ITERATIONS=${2:-0}
elif [ "${1:-}" = "build" ]; then
    MAX_ITERATIONS=${2:-0}
elif [ "${1:-}" = "specs" ]; then
    MODE="specs"; PROMPT_FILE="PROMPT_specs.md"; MAX_ITERATIONS=${2:-0}
elif [ "${1:-}" = "reverse" ]; then
    MODE="reverse"; PROMPT_FILE="PROMPT_reverse_engineer_specs.md"; MAX_ITERATIONS=${2:-0}
elif [ "${1:-}" = "slc" ]; then
    MODE="slc"; PROMPT_FILE="PROMPT_plan_slc.md"; MAX_ITERATIONS=${2:-0}
elif [ "${1:-}" = "plan-work" ]; then
    if [ -z "${2:-}" ]; then echo "Error: plan-work requires a work description"; exit 1; fi
    MODE="plan-work"; WORK_DESCRIPTION="$2"; PROMPT_FILE="PROMPT_plan_work.md"; MAX_ITERATIONS=${3:-5}
elif [[ "${1:-}" =~ ^[0-9]+$ ]]; then
    MAX_ITERATIONS=$1
fi

ITERATION=0
CURRENT_BRANCH=$(git branch --show-current)

if [ "$MODE" = "plan-work" ]; then
    if [ "$CURRENT_BRANCH" = "main" ] || [ "$CURRENT_BRANCH" = "master" ]; then
        echo "Error: plan-work should be run on a work branch, not main/master"
        echo "Create a work branch first: git checkout -b ralph/your-work"; exit 1
    fi
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Mode:   $MODE"
echo "Prompt: $PROMPT_FILE"
echo "Branch: $CURRENT_BRANCH"
[ -n "$WORK_DESCRIPTION" ] && echo "Work:   $WORK_DESCRIPTION"
[ $MAX_ITERATIONS -gt 0 ] && echo "Max:    $MAX_ITERATIONS iterations"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ ! -f "$PROMPT_FILE" ]; then echo "Error: $PROMPT_FILE not found"; exit 1; fi

while true; do
    if [ $MAX_ITERATIONS -gt 0 ] && [ $ITERATION -ge $MAX_ITERATIONS ]; then
        echo "Reached max iterations: $MAX_ITERATIONS"; break
    fi

    if [ "$MODE" = "plan-work" ]; then
        export WORK_SCOPE="$WORK_DESCRIPTION"
        envsubst < "$PROMPT_FILE" | claude -p \
            --dangerously-skip-permissions \
            --output-format=stream-json \
            --model claude-opus-4-7 \
            --verbose
    else
        cat "$PROMPT_FILE" | claude -p \
            --dangerously-skip-permissions \
            --output-format=stream-json \
            --model claude-opus-4-7 \
            --verbose
    fi

    CURRENT_BRANCH=$(git branch --show-current)
    git push origin "$CURRENT_BRANCH" || git push -u origin "$CURRENT_BRANCH"

    ITERATION=$((ITERATION + 1))
    echo -e "\n\n======================== LOOP $ITERATION ========================\n"
done
```

---

## Variant 4 — Streamed Output Loop

Pipes Claude's JSON output through parse_stream.js for readable color-coded terminal display.
Requires `parse_stream.js` in the same directory.

```bash
#!/bin/bash
set -o pipefail

if [ "$1" = "plan" ]; then
    MODE="plan"; PROMPT_FILE="PROMPT_plan.md"; MAX_ITERATIONS=${2:-0}
elif [ "$1" = "build" ]; then
    MODE="build"; PROMPT_FILE="PROMPT_build.md"; MAX_ITERATIONS=${2:-0}
elif [[ "$1" =~ ^[0-9]+$ ]]; then
    MODE="build"; PROMPT_FILE="PROMPT_build.md"; MAX_ITERATIONS=$1
else
    MODE="build"; PROMPT_FILE="PROMPT_build.md"; MAX_ITERATIONS=0
fi

ITERATION=0
CURRENT_BRANCH=$(git branch --show-current)

if [ ! -f "$PROMPT_FILE" ]; then echo "Error: $PROMPT_FILE not found"; exit 1; fi

while true; do
    if [ $MAX_ITERATIONS -gt 0 ] && [ $ITERATION -ge $MAX_ITERATIONS ]; then
        echo "Reached max iterations: $MAX_ITERATIONS"; break
    fi

    FULL_PROMPT="$(cat "$PROMPT_FILE")

Execute the instructions above."

    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    claude -p "$FULL_PROMPT" \
        --dangerously-skip-permissions \
        --model claude-opus-4-7 \
        --verbose \
        --output-format stream-json \
        --include-partial-messages | node "$SCRIPT_DIR/parse_stream.js"

    git push origin "$CURRENT_BRANCH" || git push -u origin "$CURRENT_BRANCH"

    ITERATION=$((ITERATION + 1))
    echo -e "\n\n======================== LOOP $ITERATION ========================\n"
done
```

---

## Git Worktrees Workflow

**Source**: Spec-B B.5.2 (Claude Code parallel implementation), R.2.9

Use when the project has two or more independent features that can be developed simultaneously without sharing in-progress state in `src/lib/`. Git worktrees give each feature branch its own working directory and `IMPLEMENTATION_PLAN.md`, eliminating context bleed between parallel Ralph loops.

### Setup

```bash
# From main project root
git worktree add ../my-project-feature-a feature/feature-a
git worktree add ../my-project-feature-b feature/feature-b

# Copy loop infrastructure to each worktree
cp loop.sh PROMPT_build.md PROMPT_plan.md AGENTS.md ../my-project-feature-a/
cp loop.sh PROMPT_build.md PROMPT_plan.md AGENTS.md ../my-project-feature-b/
```

### Create scoped plans per worktree

```bash
# In each worktree, run plan-work to create a focused plan
cd ../my-project-feature-a
./loop.sh plan-work "user authentication with OAuth and session management"

cd ../my-project-feature-b
./loop.sh plan-work "REST API for product catalog with search and filtering"
```

### Build independently

```bash
# Sequential (safe, simpler)
cd ../my-project-feature-a && ./loop.sh 20
cd ../my-project-feature-b && ./loop.sh 20

# Parallel (faster, requires separate terminals or tmux panes)
# Terminal 1:
cd ../my-project-feature-a && ./loop.sh 20

# Terminal 2:
cd ../my-project-feature-b && ./loop.sh 20
```

### Merge and clean up

```bash
# After both features are complete and PRs merged
git worktree remove ../my-project-feature-a
git worktree remove ../my-project-feature-b
```

### Known trade-off (R.2.9 §8 Known Limitations)

If feature-a and feature-b both modify `src/lib/`, changes will conflict at merge time. Coordinate shared library changes manually, or ensure the features don't touch the same `src/lib/` modules. Consider using `plan-work` scope descriptions that explicitly exclude `src/lib/` changes if this is a concern.

---

## Model String Reference

As of May 2026 (Claude Code v2.1.123), use these model strings in `--model` flag:

| Model tier | String | Notes |
|-----------|--------|-------|
| Opus (primary orchestrator) | `claude-opus-4-7` | Released April 16, 2026. 1M token context on Max/Team/Enterprise; ~150K usable in practice before auto-compaction (Issue #50888). Adaptive reasoning (low/medium/high/xhigh). |
| Sonnet (subagents, reads) | `claude-sonnet-4-6` | CLI default. Near-Opus coding quality at ~1.67× lower cost. |
| Haiku (fast/cheap checks) | `claude-haiku-4-5-20251001` | Fast, cheapest tier. |

**Model alias behaviour**: `--model opus` resolves to `claude-opus-4-7` on Anthropic API, but only `claude-opus-4-6` on Bedrock/Vertex/Foundry. Pin the full string for reproducible loops via `ANTHROPIC_MODEL` env var or `--model claude-opus-4-7`.

**In subagent references within prompts**, use tier labels: "Opus subagent", "Sonnet subagent".
**In guardrail 99999999999999**, the literal string is `Opus 4.7 subagent` — update when generating fresh Ralph files.

**Cost threshold** (April 2026 rate card): Opus 4.7 at $5/$25 per MTok is ~1.67× Sonnet 4.6 at $3/$15 per MTok. Factoring in Opus 4.7's new tokenizer (+35% token inflation), effective cost difference is ~2.25×. Switch Sonnet → Opus when the loop "spins" (same files edited/reverted across iterations without forward progress); switch back when it stabilises.

Update model strings whenever generating new Ralph files. They drift as Anthropic releases new models.

---

## Permission Mode & Sandbox

### Choosing a permission mode

Two options for unattended loop execution:

| Mode | Flag | When to use |
|------|------|-------------|
| **YOLO** | `--dangerously-skip-permissions` | Air-gapped sandbox, no credentials reachable, maximum speed |
| **Auto mode** | `--auto` (Team-plan research preview, launched March 24, 2026) | Credentials/SSH keys reachable; Sonnet 4.6 classifier approves safe tool calls, blocks dangerous ones. Terminates after 3 consecutive denials or 20 total. |

**Auto mode caveat**: Adds classifier latency per tool call. Classifier accuracy degrades near the 200K token compaction boundary. For overnight production runs with credentials in scope, prefer auto mode over YOLO + trusting the sandbox alone.

**YOLO caveat** (Huntley's own framing): "It's not if it gets popped, it's when. What is the blast radius?" Always pair with OS-level isolation.

### Sandbox options

Always run Ralph inside an isolated environment regardless of permission mode:

| Option | Best for |
|--------|----------|
| Docker local (`docker sandbox run claude`) | Local development, prototyping |
| E2B | Production, CI/CD, multi-tenant |
| Fly Sprites | Long-running persistent agents (no timeout) |
| Modal | Python/ML-heavy projects |

Minimum viable access: only the API keys and deploy keys needed for the task. No access to private data beyond requirements. Restrict network connectivity where possible.

### Subagent MCP Limitation

**Important**: Subagents do NOT inherit MCP tools (Issue #34935). Only 8 built-in tools are available to subagents:
`Read`, `Write`, `Edit`, `Bash`, `Grep`, `Glob`, `WebSearch`, `WebFetch`

MCP tools (Slack, Google Drive, Asana, etc.) are only usable in the main agent context. Design specs and PROMPT files accordingly — never instruct a subagent to use an MCP tool.

---

## File Permissions

Always remind the user to make loop.sh executable after creation:

```bash
chmod +x loop.sh
chmod +x loop_streamed.sh  # if generated
```

---

## Project File Tree

```
project-root/
├── loop.sh                                   # Ralph loop script (chmod +x)
├── loop_streamed.sh                          # Optional: streamed output variant
├── parse_stream.js                           # Required by loop_streamed.sh
├── PROMPT_build.md                           # Build mode
├── PROMPT_plan.md                            # Plan mode
├── PROMPT_specs.md                           # Specs audit mode (optional)
├── PROMPT_reverse_engineer_specs.md          # Brownfield specs (optional)
├── PROMPT_plan_work.md                       # Work-branch planning (optional)
├── PROMPT_plan_slc.md                        # SLC release planning (optional)
├── AUDIENCE_JTBD.md                          # Required by SLC mode
├── AGENTS.md                                 # Operational only — build/run/validate
├── IMPLEMENTATION_PLAN.md                    # Prioritized task list (Ralph-managed)
├── specs/                                    # One file per topic of concern
│   ├── 01-[topic].md
│   └── 02-[topic].md
├── src/                                      # Application source code
└── src/lib/                                  # Shared utilities & components
    ├── llm-review.ts                         # Optional: non-deterministic backpressure
    └── llm-review.test.ts                    # Optional: usage examples for Ralph

# Git worktrees (when using Variant 3 git-worktrees extension):
../project-feature-a/                         # Separate working directory
├── IMPLEMENTATION_PLAN.md                    # Feature-scoped plan
└── [same loop files as above]
../project-feature-b/
├── IMPLEMENTATION_PLAN.md
└── [same loop files as above]
```
