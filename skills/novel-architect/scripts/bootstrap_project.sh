#!/bin/bash
# bootstrap_project.sh — Set up a project workspace for novel-architect
#
# Usage:
#   bash bootstrap_project.sh <slug>
#   bash bootstrap_project.sh kohaerenz-protokoll   # special: migrate from legacy
#
# Creates /home/claude/novel-projects/<slug>/ with template files.
# Special case: if <slug> is "kohaerenz-protokoll" and novel-architect-legacy/
# exists, migrate its data to the workspace.

set -euo pipefail

SLUG="${1:-}"
if [ -z "$SLUG" ]; then
    echo "Usage: bash bootstrap_project.sh <slug>" >&2
    echo "Example: bash bootstrap_project.sh my-sf-novel" >&2
    echo "Migration: bash bootstrap_project.sh kohaerenz-protokoll" >&2
    exit 1
fi

# Determine paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_ROOT="$(dirname "$SCRIPT_DIR")"
LEGACY_SKILL="$(dirname "$SKILL_ROOT")/novel-architect-legacy"
WORKSPACE="/home/claude/novel-projects/$SLUG"

# Create workspace
echo "Creating workspace: $WORKSPACE"
mkdir -p "$WORKSPACE/canon"
mkdir -p "$WORKSPACE/research/briefs"
mkdir -p "$WORKSPACE/research/findings"
mkdir -p "$WORKSPACE/drafts"

# Check for legacy migration
if [ "$SLUG" = "kohaerenz-protokoll" ] && [ -d "$LEGACY_SKILL/references/canon" ]; then
    echo "Detected legacy migration for kohaerenz-protokoll"
    echo "Copying legacy data..."
    cp "$LEGACY_SKILL/references/canon/kohaerenz-protokoll.ncp.json" \
       "$WORKSPACE/canon/kohaerenz-protokoll.ncp.json"
    cp "$LEGACY_SKILL/references/canon/README.md" \
       "$WORKSPACE/canon/README.md"
    cp "$LEGACY_SKILL/references/canon-meta.md" \
       "$WORKSPACE/canon-meta.md"
    cp "$LEGACY_SKILL/references/progress.md" \
       "$WORKSPACE/progress.md"
    cp "$LEGACY_SKILL/references/open-questions.md" \
       "$WORKSPACE/open-questions.md"
    # learnings.md: take from legacy if not present
    if [ ! -f "$WORKSPACE/learnings.md" ]; then
        cp "$LEGACY_SKILL/references/learnings.md" \
           "$WORKSPACE/learnings.md"
    fi
    # Generate project-config.yaml for the legacy project
    cat > "$WORKSPACE/project-config.yaml" <<EOF
project:
  slug: kohaerenz-protokoll
  name: "Kohärenz Protokoll"
  language: de
  genre: hard_sf
  workspace_root: /home/claude/novel-projects/kohaerenz-protokoll/
  is_demo: false

narrative:
  storyform_count: dual
  chapter_count_target: 39
  structure_template: 40-chapter-matrix

methods_enabled:
  character:
    - tsdp-ifs
    - jung-archetypes
  structure:
    - 40-chapter-matrix
    - dramatica-quad
  conflict:
    - philosophy-as-engine
    - science-as-engine
    - dual-storyform
  research:
    - domain-mapping
    - deep-research-briefs

ncp:
  schema_version: "1.3.0"
  file: canon/kohaerenz-protokoll.ncp.json

canon:
  meta_file: canon-meta.md

state:
  progress_file: progress.md
  open_questions_file: open-questions.md
  learnings_file: learnings.md
  intent_file: intent.yaml
  architecture_file: architecture.yaml
  character_architecture_file: character-architecture.yaml
  scene_matrix_file: scene-matrix.md

integration:
  philosophy_level: engine
  science_level: engine

provenance:
  created_by: novel-architect@1.0.0 (migrated from novel-architect-legacy@0.3.3)
  created_at: $(date -u +"%Y-%m-%dT%H:%M:%SZ")
  predecessor: "novel-architect-legacy@0.3.3"
EOF
    echo "Legacy migration complete: $WORKSPACE"
    echo "Recommended next step: run audit-mode (/novel-reflect → audit)"
    exit 0
fi

# Standard new-project setup
echo "Setting up new project: $SLUG"

# Copy templates
cp "$SKILL_ROOT/assets/project-config-template.yaml" "$WORKSPACE/project-config.yaml"
cp "$SKILL_ROOT/assets/project-progress-template.md" "$WORKSPACE/progress.md"

# Create empty NCP (from ncp-author template if available)
NCP_TEMPLATE="$(dirname "$SKILL_ROOT")/ncp-author/assets/template-empty.json"
if [ -f "$NCP_TEMPLATE" ]; then
    cp "$NCP_TEMPLATE" "$WORKSPACE/canon/$SLUG.ncp.json"
else
    echo "WARN: ncp-author template not found at $NCP_TEMPLATE" >&2
    echo "{}" > "$WORKSPACE/canon/$SLUG.ncp.json"
fi

# Create empty state files
touch "$WORKSPACE/intent.yaml"
touch "$WORKSPACE/canon-meta.md"
touch "$WORKSPACE/open-questions.md"
touch "$WORKSPACE/learnings.md"

# Adjust project-config.yaml placeholders
sed -i "s|<PLACEHOLDER-kebab-case>|$SLUG|g" "$WORKSPACE/project-config.yaml"
sed -i "s|<PLACEHOLDER-slug>|$SLUG|g" "$WORKSPACE/project-config.yaml"
sed -i "s|<PLACEHOLDER human-readable>|$SLUG|g" "$WORKSPACE/project-config.yaml"

echo "Workspace ready: $WORKSPACE"
echo ""
echo "Next steps:"
echo "1. Edit $WORKSPACE/project-config.yaml (fill placeholders)"
echo "2. Trigger /novel-start to begin Phase 1 (Intent Capture)"
