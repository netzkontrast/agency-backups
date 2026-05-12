# Integration Plan: Folding the Gemini PDF into `SPEC.md`

This document is the instruction set for the agent that receives the Gemini Deep Research PDF and integrates it into the preliminary spec at `research/skills-skill-architecture/output/SPEC.md`.

---

## 1. Where the PDF Lives

Michael uploads the PDF to Google Drive and places it in the repository at:

```
research/skills-skill-architecture/workspace/gemini-deep-research.pdf
```

This path is the canonical input for the integration agent. The integration agent MUST NOT proceed until this file exists at that path.

---

## 2. Prerequisites

Before starting integration, the agent MUST confirm:

1. `research/skills-skill-architecture/workspace/gemini-deep-research.pdf` exists and is non-empty.
2. `research/skills-skill-architecture/output/SPEC.md` exists (this preliminary spec).
3. The current branch is a new branch created from `main` after Stage A has merged (the 14 skills must be in `origin/main:skills/` for the architecture to be grounded in real skill bodies).

Branch naming convention: `claude/skills-skill-spec-v2`.

---

## 3. Extraction Step

The agent MUST extract the Gemini PDF's findings using the `pdf-to-markdown` skill (available in `skills/pdf-to-markdown/` after Stage A merges). Save the extracted Markdown to:

```
research/skills-skill-architecture/workspace/gemini-findings.md
```

---

## 4. Comparison Matrix

For each UNCERTAIN marker in `SPEC.md`, compare the preliminary spec's assumption against Gemini's finding. Fill in this table as the first artifact of the integration work:

| ID | SPEC.md assumption | Gemini finding | Action |
|---|---|---|---|
| U1 | git available in container | [Gemini answer] | Replace B1–B3 if git unavailable |
| U2 | Container may be ephemeral | [Gemini answer] | Update R7 latency guarantees |
| U3 | Description-match or explicit-name trigger | [Gemini answer] | Fix routing model if wrong |
| U4 | Jules unknown | [Gemini answer] | Populate adapter spec or confirm none needed |
| U5 | Host may or may not pass raw message | [Gemini answer] | Fix R3 routing algorithm |
| U6 | Signing feasibility unknown | [Gemini answer] | Update R5 trust model |

Save this table to: `research/skills-skill-architecture/workspace/comparison-matrix.md`

---

## 5. SPEC.md Update Rules

Apply the following rules mechanically:

### 5a. Resolve UNCERTAIN markers

For each `> **UNCERTAIN (Ux)**` block in `SPEC.md`:
- If Gemini resolves the uncertainty definitively: **replace** the UNCERTAIN block with a normative statement using RFC-2119 keywords.
- If Gemini partially resolves it: **update** the UNCERTAIN block to narrow the remaining uncertainty. Keep the `> **UNCERTAIN**` prefix but update the body.
- If Gemini could not resolve it: **leave** the UNCERTAIN block unchanged and add a note: `> Gemini Deep Research (2026-MM-DD) could not resolve this. See open-questions.md.`

### 5b. Bootstrap sequence (U1)

If Gemini confirms `git` is available: the B1–B3 sequence stands unchanged.

If Gemini says `git` is NOT available: **replace** the B1–B3 sequence in Section 2.1 with the Gemini-recommended alternative (likely GitHub API via `curl` or `requests`). Preserve the overall bootstrap structure (clone/fetch → route → inject).

### 5c. Routing model (U3, U5)

If Gemini clarifies the host trigger mechanism: update Section 4.1 (Two-Tier Routing Model) to reflect the actual mechanism. If the description-match model is wrong, rewrite the Tier-1 description. If the host does NOT pass the raw message: update step 2 in Section 4.1.

### 5d. Cross-agent adapters (U4)

For Jules and gemini-cli: if Gemini provides their skill-loading conventions, create stub adapter specs as new files:
- `research/skills-skill-architecture/output/adapter-jules.md`
- `research/skills-skill-architecture/output/adapter-gemini-cli.md`

These are not new research tasks — they are appendices to the spec.

### 5e. Trust model (U6)

If Gemini recommends a specific signing approach: replace Section 6.2 with normative language specifying the signing/verification procedure.

If Gemini confirms signing is infeasible: add a note that SHA-comparison against a hardcoded stub value is the fallback.

---

## 6. Frontmatter Update

After applying all changes, update `SPEC.md`'s frontmatter:

```yaml
status: active          # keep active until spec is accepted by Michael
research_phase: complete
updated: <today's date>
```

Add a new field to track the Gemini integration:
```yaml
research_gemini_integrated: YYYY-MM-DD
```

---

## 7. What Gets a New PR vs. What Gets Appended

| Artifact | Destination | PR or append? |
|---|---|---|
| Updated `SPEC.md` (UNCERTAIN resolved) | Same file, same location | New PR: `claude/skills-skill-spec-v2` |
| `workspace/gemini-findings.md` | Workspace file | Same PR (workspace artifact) |
| `workspace/comparison-matrix.md` | Workspace file | Same PR (workspace artifact) |
| `output/adapter-jules.md` (if Gemini answers R2-Q1) | Output file | Same PR |
| `output/adapter-gemini-cli.md` (if Gemini answers R2-Q2) | Output file | Same PR |
| Remaining unresolved uncertainties → new follow-up prompts | `/prompts/<new-slug>/` | Separate PR or same PR |
| `/specs/skills-skill/` (the final implementable spec folder) | New top-level folder per brief | **New PR after v2 is merged**: `claude/skills-skill-spec-final` |

**IMPORTANT**: The `research/skills-skill-architecture/` workspace is NOT the final spec location. The brief requires the final spec at `/specs/skills-skill/` (containing `spec.md`, `architecture.md`, `tooling.md`, `open-questions.md`, `readme.md`). The integration agent MUST produce `/specs/skills-skill/` as a second PR AFTER the v2 SPEC.md is accepted.

---

## 8. Triggering the Integration Step (Copy-Pasteable Instructions for Michael)

Once Michael has the Gemini PDF:

```
1. Upload the PDF to Google Drive
2. Start a new Claude Code session in the netzkontrast/agency repository
3. Say:
   "I have the Gemini Deep Research PDF for the skills-skill architecture.
   It's in Google Drive. Please follow the integration plan at
   research/skills-skill-architecture/output/integration-plan.md and
   produce a v2 spec PR."
4. Claude Code will:
   - Download the PDF from Drive
   - Extract it to research/skills-skill-architecture/workspace/gemini-deep-research.pdf
   - Fill the comparison matrix
   - Update SPEC.md (resolve UNCERTAIN markers)
   - Create branch claude/skills-skill-spec-v2
   - Open a PR against main
5. Review the PR. Merge when satisfied.
6. After v2 merges, ask Claude Code to produce /specs/skills-skill/ as a separate PR.
```

---

## 9. Definition of Done for the Integration Agent

The integration is complete when:
- [ ] All UNCERTAIN markers in `SPEC.md` are either resolved or explicitly forwarded to new follow-up prompts.
- [ ] `workspace/comparison-matrix.md` exists and all rows are filled.
- [ ] `SPEC.md` frontmatter includes `research_gemini_integrated: <date>`.
- [ ] Any new adapter specs (Jules, gemini-cli) exist in `output/` if Gemini answered R2-Q1 and R2-Q2.
- [ ] PR `claude/skills-skill-spec-v2` is open against main.
- [ ] A second PR is ready (or queued) for `/specs/skills-skill/` containing the five-file final spec per the research brief.
