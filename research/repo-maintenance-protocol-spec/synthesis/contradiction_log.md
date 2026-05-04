# Contradiction Log (M07)

## C1: Root Spec Updatability during Maintenance
- **Claim A:** Maintenance agents should automatically update Root Specs (like FOLDERS.md or RESEARCH.md) when they find a better pattern or when aggregating synthesized learnings.
- **Claim B:** Root Specs must be immutable by background maintenance tasks to prevent systemic collapse; changes require explicit human or architect-agent approval.
- **Hypothesized Cause:** The tension between autonomy (Claim A) and stability (Claim B). If a background script alters the core definitions, active agents might fail due to "protocol drift" midway through a task.
- **Evidence for Resolution:** M13 Opposing Query highlighted that allowing automated systems to overwrite core context leads to hallucinated context loss. Active agent workflows require stable, predictable root constraints during execution.
- **Interim Statement:** A background maintenance agent MUST NOT directly edit Root Specs (`AGENTS.md`, `FOLDERS.md`, `RESEARCH.md`, `MAINTENANCE.md`). Instead, if it detects a needed governance change, it MUST generate a proposal and place it in the `/todo/` pipeline for explicit human or architect-agent review.
