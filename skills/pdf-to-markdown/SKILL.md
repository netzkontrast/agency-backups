---
name: pdf-to-markdown
description: Convert a PDF to Markdown using PyMuPDF4LLM. Works on locally uploaded PDFs (/mnt/user-data/uploads) and on PDFs in Google Drive (download → convert → optional Drive upload of the .md). Default mode is context-safe — the .md is written to /mnt/user-data/outputs and presented to the user without ever loading PDF or Markdown content into the main conversation context, so large or sensitive documents do not pollute the thread. The user can opt into direct mode per call to load the result into context for downstream summarize/analyze/quote tasks. Trigger phrases include — pdf to markdown, pdf2md, convert pdf, extract markdown from pdf, pymupdf4llm, structured pdf extraction, pdf for LLM ingestion, RAG-ready pdf, prepare pdf for embedding. Use this rather than plain text extraction whenever Markdown structure (headers, tables, lists, multi-column layouts) matters for downstream LLM use.
---

# PDF to Markdown (PyMuPDF4LLM)

Convert a PDF to Markdown with PyMuPDF4LLM, keeping content out of the main context window unless the user explicitly opts in.

## Why this skill exists

Plain text extraction loses structure that LLMs rely on: heading hierarchy, list nesting, table cell relationships, multi-column reading order. PyMuPDF4LLM preserves all of that as Markdown, which is what downstream RAG / summarization / agent pipelines actually want.

This skill is also the **context-safe path** for handling PDFs. The PDF bytes and the resulting Markdown stay on disk; they only enter the conversation if the user asks for it. That matters for two reasons: large PDFs would otherwise blow the context budget, and sensitive PDFs (medical records, contracts, internal docs) shouldn't be sitting in conversation history when they don't need to be.

## Decision the user makes per call

**Mode = context-safe** (default): convert → write `.md` → `present_files` → stop. Do **not** read the .md back. The user sees the file, downloads it, that's the deliverable.

**Mode = direct**: convert → write `.md` → `view` it back into context → continue with the user's downstream task (summarize, extract X, quote a section).

If the user's request is just "convert this PDF", default to context-safe. If the request implies wanting to *do something with* the content in the same turn ("summarize this PDF", "extract the methodology section", "what does the contract say about termination"), default to direct. When ambiguous, pick context-safe and offer: *"Want me to load the markdown back into context so we can work with it?"*

## Source: local vs Drive

### Local source

Path: `/mnt/user-data/uploads/<filename>.pdf`. Output to `/mnt/user-data/outputs/<filename>.md`.

```bash
python /path/to/skill/scripts/convert.py <input.pdf> <output.md>
```

The script handles install-on-demand, runs `pymupdf4llm.to_markdown()` with library defaults, writes the result, and prints a one-line stats summary on success.

### Drive source

Requires the Google Drive MCP. Flow:

1. **Resolve file ID.** If the user gave a name or partial path, use `Google Drive:search_files` (mimeType filter `application/pdf`). If they gave a Drive URL or ID, extract the ID directly.
2. **Download bytes.** Use `Google Drive:download_file_content` — returns base64. Decode and write to `/tmp/<filename>.pdf`.
3. **Convert.** Same script as local source: `python scripts/convert.py /tmp/<filename>.pdf /mnt/user-data/outputs/<filename>.md`.
4. **Optional Drive upload.** If the user asked for the .md to land back in Drive, use `Google Drive:create_file` with the markdown content and an appropriate parent folder. Do **not** upload by default — only when asked.
5. **Present.** `present_files` the local .md path so the user has an immediate download link even when also uploading to Drive.
6. **Clean up** `/tmp/<filename>.pdf`.

> Honest caveat: the Drive download step briefly passes PDF bytes through the MCP tool response. The skill cannot avoid that for Drive sources. The conversion itself, and any subsequent .md content, still stay out of context unless direct mode is chosen.

## Step-by-step (the normal path)

1. **Identify the PDF.** Local path or Drive reference.
2. **Decide the mode.** Context-safe by default; direct only if the user's request implies in-turn use of the content.
3. **(Drive only)** Download to `/tmp/`.
4. **Run the converter script.** Single command, single .md output.
5. **(Drive + user asked)** Upload .md back to Drive.
6. **`present_files`** with the .md path.
7. **Mode-dependent finish:**
   - context-safe → stop. State briefly that the file is ready, mention page/char count if useful, optionally offer to load it on request.
   - direct → `view` the .md, then proceed with the downstream task using its content.
8. **(Drive only)** Remove the temp PDF.

## Defaults that matter

- **One .md per PDF.** No chunking, no page-range slicing, no image extraction. PyMuPDF4LLM supports all of those (`page_chunks=True`, `pages=[...]`, `write_images=True`); they are intentionally not exposed here. If a user asks for them, edit `scripts/convert.py` to add the flag — don't reach for a different skill.
- **Output naming.** Same stem as input, `.md` extension, written to `/mnt/user-data/outputs/`.
- **No silent fallback.** If `pymupdf4llm` import fails after the install attempt, surface the error directly. Do not silently fall back to PyMuPDF text extraction or another library — the user picked this skill because they wanted PyMuPDF4LLM's structural output.
- **Empty output is informative.** If the .md comes out empty or near-empty (< ~200 chars for a multi-page PDF), the PDF likely has no text layer (scanned image). Tell the user directly and point them to the `pdf-reading` skill's OCR workflow.

## What this skill is NOT for

- **Google Docs in Drive** → `drive-markdown-converter` (different extraction path; Docs are exported via the Drive API, not parsed as PDFs).
- **OCR on scanned PDFs** → `pdf-reading` skill (PyMuPDF4LLM only reads existing text layers).
- **Form filling, merging, splitting, watermarking, encryption** → `pdf` skill.
- **Reading a PDF that's already in the conversation as a viewable document block** → just use the visible content; you don't need to re-extract it.

## Reference

`scripts/convert.py` is the single entry point. It is small (~30 lines) and intentionally so — modify it directly if you need to expose more PyMuPDF4LLM options for a specific job.
