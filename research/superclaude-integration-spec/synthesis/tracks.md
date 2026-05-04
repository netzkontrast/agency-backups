---
type: note
status: active
slug: superclaude-integration-spec
summary: "Per-track work breakdown for the SC integration spec research run."
created: 2026-05-04
updated: 2026-05-04
---

# Tracks

## Track A — SC Inventory

**Goal**: Full catalog of commands, agents, skills.
**Sources**: Filesystem listings + individual command files + SuperClaude CLAUDE.md.
**Output**: SPEC.md §1 Catalog (3 tables).
**Status**: Complete. 30 commands, 20 agents, 2 skills.

## Track B — Agency Phase Analysis

**Goal**: Map each Agency workflow phase to SC tools.
**Sources**: TASK.md §4, RESEARCH.md §4, PROMPT.md §4, MAINTENANCE.md §1–4.
**Output**: SPEC.md §2 Phase Mapping (10-row table).
**Status**: Complete.

## Track C — Integration Pattern Design

**Goal**: Concrete executable examples per phase.
**Sources**: SC command behavioral flows (research.md, implement.md, spawn.md, analyze.md), KNOWLEDGE.md §Core Insights.
**Output**: SPEC.md §3 Integration Patterns (9 patterns).
**Status**: Complete.

## Track D — Template Design

**Goal**: Canonical SuperClaude Integration Block for future specs.
**Sources**: TASK.md §3.2 (frontmatter pattern), RESEARCH.md §2 (output structure).
**Output**: SPEC.md §4 New Spec Template.
**Status**: Complete. Includes mandatory, SHOULD, and minimal variants.

## Track E — Root Spec Link Analysis

**Goal**: Identify exactly where existing root specs should cross-link to this spec.
**Sources**: AGENTS.md, RESEARCH.md, TASK.md, PROMPT.md, MAINTENANCE.md structure.
**Output**: SPEC.md §5 Root Spec Link Recommendations (5-row table).
**Status**: Complete.

## Track F — Maintenance Extension

**Goal**: Extend MAINTENANCE.md with SC Integration Scan protocol.
**Sources**: MAINTENANCE.md §1–4, FOLDERS.md §7 (contradiction identified).
**Output**: Updated MAINTENANCE.md with new §5 (6 subsections).
**Status**: Complete. Note: /todo/ → /prompts/ correction applied in MAINTENANCE.md §3.
