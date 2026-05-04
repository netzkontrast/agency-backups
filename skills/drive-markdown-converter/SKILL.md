---
name: drive-markdown-converter
description: >-
  Use when the user wants to convert Google Docs or PDFs in a Google Drive
  folder to Markdown and upload the results to another Drive folder — without
  letting file contents land in the main context window. Supports two execution
  modes: Artifact-Generator (interactive React UI) and Subagent-Prompt (isolated
  API call for pipeline integration). Triggers on: drive to markdown, convert
  drive files, google docs to markdown, pdf to markdown drive, drive conversion,
  drive batch convert, context-safe drive, drive markdown pipeline.
metadata:
  category: tool-integration
  triggers: >-
    drive to markdown, convert drive files, google docs to markdown, pdf to
    markdown drive, drive conversion, drive batch convert, context-safe drive,
    drive markdown pipeline, drive ordner konvertieren, drive zu markdown
---

# Drive → Markdown Converter

Converts Google Docs and PDFs in a source Drive folder to Markdown and uploads
results to a target folder. **Core constraint: raw file content NEVER lands in
the calling context.** All I/O runs inside an isolated artifact or subagent.

---

## Input Parameters

Collect these before choosing a mode:

| Parameter | Required | Description |
|-----------|----------|-------------|
| `source_folder_id` | ✅ | Google Drive folder ID to read from |
| `target_folder_id` | ✅ | Google Drive folder ID to write to |
| `file_types` | optional | `docs`, `pdfs`, or `both` (default: `both`) |
| `naming_convention` | optional | e.g. `{original_name}.md` (default) |
| `dry_run` | optional | List files without converting (default: false) |

Folder IDs are the alphanumeric string in the Drive URL after `/folders/`.

---

## Mode Selection

```
User wants interactive UI / one-off run?  →  MODE A: Artifact-Generator
User wants pipeline integration / JANUS?  →  MODE C: Subagent-Prompt
No preference stated?                     →  Ask with ask_user_input_v0
```

---

## MODE A — Artifact-Generator

→ Read [references/artifact-mode.md](references/artifact-mode.md)

Generates a React artifact that:
1. Accepts folder IDs as input
2. Calls Anthropic API with Google Drive MCP (`https://drivemcp.googleapis.com/mcp/v1`)
3. Subagent reads, converts, uploads — content stays in subagent context
4. Artifact displays only progress + result summary (file names, byte counts, errors)

**When to use:** User runs this manually, wants to see progress, single conversion job.

---

## MODE C — Subagent-Prompt

→ Read [references/subagent-mode.md](references/subagent-mode.md)

Generates a complete Anthropic API call payload (system prompt + user message)
that can be embedded in a pipeline, cron job, or JANUS Executor node.

**When to use:** Automated pipeline, llm-wiki-agent ingest, JANUS orchestration,
repeated scheduled runs.

---

## Content Isolation Guarantee

Both modes enforce this contract:

```
Caller context  ←  {status, file_list, error_summary}  only
Isolated layer  ←  raw file content, conversion, upload
```

Never return raw Markdown content to the caller. If the user explicitly asks
to see a converted file's content, that is a separate deliberate action outside
this skill's default behaviour.

---

## Conversion Strategy by File Type

| Type | Drive MIME | Export Method | Markdown Quality |
|------|-----------|---------------|-----------------|
| Google Doc | `application/vnd.google-apps.document` | Drive export as `text/plain` + post-process headers | High |
| PDF (text-based) | `application/pdf` | Download → extract text via pdfminer | Medium-High |
| PDF (scanned) | `application/pdf` | Download → OCR note + raw text fallback | Low (flag to user) |

Google Docs export via the Drive API `export` endpoint preserves heading
structure better than downloading as DOCX first.

---

## Pre-Deploy Checklist

- [ ] Both reference files present in `references/`
- [ ] User has Google Drive MCP connected (check claude.ai connectors)
- [ ] Source and target folder IDs confirmed before generating output
- [ ] Mode selected (A or C)
