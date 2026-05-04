# pdf-to-markdown

## What
Convert a PDF to Markdown using PyMuPDF4LLM. Works on locally uploaded PDFs (/mnt/user-data/uploads) and on PDFs in Google Drive (download → convert → optional Drive upload of the .md). Default mode is context-safe — the .md is written to /mnt/user-data/outputs and presented to the user without ever loading PDF or Markdown content into the main conversation context, so large or sensitive documents do not pollute the thread. The user can opt into direct mode per call to load the result into context for downstream summarize/analyze/quote tasks. Trigger phrases include — pdf to markdown, pdf2md, convert pdf, extract markdown from pdf, pymupdf4llm, structured pdf extraction, pdf for LLM ingestion, RAG-ready pdf, prepare pdf for embedding. Use this rather than plain text extraction whenever Markdown structure (headers, tables, lists, multi-column layouts) matters for downstream LLM use.

## Why here
Snapshot of the user-skill `/mnt/skills/user/pdf-to-markdown/` from a Claude.ai
session (taken 2026-05-04). Version-controlled here so that other agents
(Claude Code, Jules, gemini-cli) can read, audit, and propose changes via PR.
The session-side copy under `/mnt/skills/user/` remains the live runtime
"upstream" until a sync-back protocol is defined.

## Top-level navigation
- [SKILL.md](./SKILL.md)
- [scripts/](./scripts/)

## Assumptions Log
- Skill-internal subfolders (e.g. `references/`, `scripts/`, `agents/`) are
  NOT given their own `readme.md`. Rationale: skills are governed by `SKILL.md`
  and Anthropic's skill-creator conventions; adding per-subfolder readmes would
  trigger "Structural Bloat" per `FRUSTRATED.md` (FL2 special-trigger). This
  drift is logged once here and once globally in the PR Frustration Log.
- The `name` and `description` shown above are extracted verbatim from
  `SKILL.md` YAML frontmatter; if the skill is updated in `/mnt/skills/user/`,
  this readme drifts until the next snapshot run.
