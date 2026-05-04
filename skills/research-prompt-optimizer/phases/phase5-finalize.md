# Phase 5 — Finalize (Detail Spec)

This is the lazy-loaded detail document for Phase 5. The thin
SKILL.md describes Phase 5 in summary; this file covers zip
semantics, Google Drive upload mechanics, and edge cases.

## Purpose

After Phase 3 (audit skipped) or after Phase 4 acceptance, every
artefact the pipeline produced for the current slug should be
trivially exportable as a single bundle. Two delivery modes:

1. **Local download** — every workspace artefact in one zip,
   surfaced via `present_files`.
2. **Google Drive upload** — same zip, copied into the user's
   Drive (root or chosen folder) so it survives outside the
   conversation sandbox.

Both modes are explicit user selections; nothing happens silently.

---

## Algorithm in Detail

### Step 1 — Build the workspace zip

Use the `zip_workspace` helper in `render/io_helpers.py`:

```python
from render.io_helpers import zip_workspace

zip_path = zip_workspace(
    output_dir="/mnt/user-data/outputs",
    slug=slug,                # same slug used by the rest of the pipeline
)
# → /mnt/user-data/outputs/workspace_<slug>.zip
```

`zip_workspace` auto-collects every file in `output_dir` whose
filename contains `slug`, except prior `workspace_*.zip` files
(no recursion). Pass an explicit `paths=[...]` list to override.

Atomic semantics: writes `workspace_<slug>.zip.tmp` then
`os.replace` to the final name. Re-running for the same slug
overwrites the prior zip.

### Step 2 — Present the zip

Standard `present_files` call on the absolute zip path. Keep the
chat message short — one sentence acknowledging the zip is ready
plus the export gate question. No file listing in chat (file-first
principle); the user can open the zip to see contents.

### Step 3 — Export gate

```python
ask_user_input_v0([{
    "question": "Workspace-Zip ist erstellt. Wie willst du sie nutzen?",
    "options": [
        "Nur Download (zip ist oben verlinkt)",
        "Zusätzlich nach Google Drive hochladen",
        "Nichts weiter — fertig",
    ],
}])
```

Behaviour by selection:

| Selection | Action |
|---|---|
| Nur Download | End pipeline. The presented zip is the deliverable. |
| Zusätzlich nach Google Drive hochladen | Continue with step 4. |
| Nichts weiter | End pipeline silently. |

### Step 4 — Google Drive upload (only if selected)

#### 4a. Load the Drive tool

```
tool_search(query="google drive create file")
```

Skill instructions list the Drive tools as deferred — they require
`tool_search` before invocation. Do not call `tool_search` in any
earlier phase; load on demand in step 4 only.

#### 4b. Folder selection

Default target is Drive root. If the user has previously named a
target folder in this conversation, prefer that. Otherwise, ask
once:

```python
ask_user_input_v0([{
    "question": "Drive-Ziel?",
    "options": [
        "Drive Root",
        "Bestehenden Ordner per Suche wählen",
        "Neuen Ordner anlegen (Name in nächster Antwort)",
    ],
}])
```

For "Bestehenden Ordner per Suche wählen": call
`Google Drive:search_files` with a query the user provides.

For "Neuen Ordner anlegen": after the user names it, call
`Google Drive:create_file` with `mimeType=application/vnd.google-apps.folder`.

#### 4c. Upload

Read the zip as bytes, base64-encode, then call
`Google Drive:create_file` with:

- `name`: `workspace_<slug>.zip`
- `mimeType`: `application/zip`
- `parents`: target folder ID (omit for Drive root)
- file content: base64-encoded zip bytes

Exact parameter names depend on the connector schema returned by
`tool_search`; do not guess. After `tool_search` returns the
schema, use the parameter names from the schema verbatim.

#### 4d. Confirm

Surface the Drive web link in chat (one line). End pipeline.

---

## Edge Cases

### Empty workspace

`zip_workspace` raises `FileNotFoundError` if no files match the
slug. Should never happen in normal flow (Phase 3 always writes the
rendered prompt). If it does happen — e.g. user invoked the skill
mid-conversation against a slug from a prior conversation that no
longer has files in `/mnt/user-data/outputs` — surface the error
plainly and skip the export gate. Do not synthesise an empty zip.

### Drive auth failure

If `Google Drive:create_file` returns an auth error after
`tool_search`, the connector is unauthenticated. Call
`suggest_connectors` with the Google Drive UUID so the user can
reconnect, then retry the upload. Do not silently fall back to
download-only — the user explicitly chose upload.

### Large zip

The `zip_workspace` helper uses `ZIP_DEFLATED`. Workspaces with
many revisions (`_v2.md`, `_v3.md`, ...) plus audit files plus
status views are still small (typically < 1 MB). If a workspace
ever exceeds ~25 MB and the Drive connector rejects the upload,
surface the size to the user and ask whether to split (not
expected in normal use).

### Re-running Phase 5

Idempotent for download (overwrites prior zip). For Drive: each
upload creates a *new* Drive file with the same name (Drive does
not deduplicate by name). Note this in the confirmation message
if you detect it (search Drive for `workspace_<slug>.zip` first).

### Slug collision across conversations

If the user runs the pipeline twice with the same slug in different
conversations, the second run's `zip_workspace` will pick up files
from both runs (auto-collect mode). To avoid this, pass an explicit
`paths=[...]` list of just the current run's artefacts.

---

## Hard Rules (recap)

- Phase 5 always runs (even when Phase 4 was skipped).
- Drive upload is opt-in — never silent.
- `tool_search` for Drive happens **inside** step 4, not earlier.
- The zip is idempotent per slug; the version trail lives inside
  it (`research-prompt_<slug>_v2.md` etc.), not on the zip itself.
- Never modify or repackage the rendered prompt during Phase 5 —
  zip what's on disk, nothing more.
