-- ===================================================================
-- gdrive-notion-curator v0.3.0 — DDL für die 3 Notion-DBs
-- Copy-Paste-fähig für notion-create-database (parameter "schema")
-- ===================================================================

-- ===================================================================
-- DB 1 — Claude Drive Files
-- ===================================================================
-- Zweck: Eine Page pro Drive-File, mit Original- und Curated-IDs
--        getrennt, Klassifikation, Workflow-Status.

CREATE TABLE (
  "Filename"               TITLE       COMMENT 'Aktueller Drive-Filename des Originals.',
  "Original Drive ID"      RICH_TEXT   COMMENT 'Drive-fileId des Source-Originals. Stabiler Identifier.',
  "Curated Drive ID"       RICH_TEXT   COMMENT 'Drive-fileId der Kopie in /Claude/curated/. Leer wenn noch nicht kopiert oder Duplikat.',
  "Original Drive Link"    URL         COMMENT 'webViewLink zum Original.',
  "Curated Drive Link"     URL         COMMENT 'webViewLink zur Kopie in /curated/.',
  "MIME"                   SELECT('Doc':blue, 'Sheet':green, 'Slide':orange, 'PDF':red, 'Image':purple, 'Audio':pink, 'Video':yellow, 'Folder':gray, 'Other':default) COMMENT 'Drive mimeType-Kategorie.',
  "Created"                DATE        COMMENT 'Drive createdTime des Originals (RFC-3339).',
  "Modified"               DATE        COMMENT 'Drive modifiedTime des Originals.',
  "MD5 Checksum"           RICH_TEXT   COMMENT 'Nur bei Binary-Files (PDF, Image, etc). Google Docs haben kein md5.',
  "Language"               SELECT('de':blue, 'en':green, 'mixed':yellow, 'unknown':gray) COMMENT 'Erkannte Sprache.',
  "Topic"                  SELECT('kohaerenz-protokoll':blue, 'dramatica-theory':purple, 'agency-system-design':pink, 'agentic-architecture':orange, 'llm-wiki-agent':yellow, 'research-prompt-optimizer':green, 'music-production':red, 'trauma-dis-material':brown, 'dkt-physik':default, 'visual-design':gray, 'misc':default) COMMENT 'Primary Topic-Slug.',
  "Suggested Topics"       MULTI_SELECT('kohaerenz-protokoll':blue, 'dramatica-theory':purple, 'agency-system-design':pink, 'agentic-architecture':orange, 'llm-wiki-agent':yellow, 'research-prompt-optimizer':green, 'music-production':red, 'trauma-dis-material':brown, 'dkt-physik':default, 'visual-design':gray, 'misc':default) COMMENT 'Bei Multi-Match: alle Kandidaten.',
  "Confidence"             SELECT('high':green, 'medium':yellow, 'low':orange, 'none':gray, 'manual':blue) COMMENT 'Klassifikations-Sicherheit.',
  "Match Reason"           RICH_TEXT   COMMENT 'Audit-Trail: matched keyword(s), score, reason.',
  "Sort Status"            STATUS('pending':default, 'copied':blue, 'indexed':green, 'in-inbox':yellow, 'duplicate':gray, 'archived':gray, 'pinned':purple) COMMENT 'Lifecycle-Phase.',
  "Run ID"                 RICH_TEXT   COMMENT 'Welcher Skill-Run (Format: run-YYYYMMDD-HHMMSS).',
  "Sub-Page Link"          URL         COMMENT 'Direktlink zur Sub-Page in Topics-DB falls indexed.',
  "Inbox Page Link"        URL         COMMENT 'Direktlink zum Inbox-Eintrag falls in-inbox.',
  "Sensitive"              CHECKBOX    COMMENT 'trauma-relevant — kein Content-Read, kein indexierter Inhalt.',
  "Pinned"                 CHECKBOX    COMMENT 'Skill rührt nicht mehr an, auch nicht bei Repair.',
  "Notes"                  RICH_TEXT   COMMENT 'Frei-Annotationen User. Wird von Claude NICHT überschrieben.'
)


-- ===================================================================
-- DB 2 — Claude Topics
-- ===================================================================
-- Zweck: Eine Page pro Topic. Sub-Pages dieser Page = File-Inhalte.
-- Hinweis: KEINE RELATION zur Files-DB in v0.3.0 (siehe notion-schema.md
--          für Begründung — Cross-Lookup erfolgt via Topic-Slug-Match).

CREATE TABLE (
  "Topic Name"      TITLE,
  "Slug"            RICH_TEXT,
  "Sensitive"       CHECKBOX,
  "Keywords"        RICH_TEXT,
  "File Count"      NUMBER,
  "Description"     RICH_TEXT
)


-- ===================================================================
-- DB 3 — Claude Topic Inbox
-- ===================================================================
-- Zweck: Eine Page pro Vorschlag für neuen Topic. Awaits askuser-Approve.

CREATE TABLE (
  "Vorschlag"           TITLE,
  "Suggested Slug"      RICH_TEXT,
  "Sample File IDs"     RICH_TEXT,
  "Sample File Count"   NUMBER,
  "Suggested Keywords"  RICH_TEXT,
  "Status"              STATUS('pending-review':yellow, 'approved':green, 'rejected':red, 'merged':gray),
  "Decision Notes"      RICH_TEXT,
  "Merged Into"         RICH_TEXT,
  "Created"             CREATED_TIME
)
