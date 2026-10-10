---
description: Scan 00. Inbox for pending sources and route selected files through the Codex ingest workflow.
---

# /inbox — Codex Inbox Scanner

Follow [[AGENTS.md]] and read [[Core Context]] once per session.

## Process

1. Scan `00. Inbox/` recursively, skipping `.gitkeep`.
2. Group files by folder: Articles, Papers, Transcripts, Clippings, AI Research, and uncategorized root files.
3. Preview title, source URL, author, category, language, approximate length, and 2-3 topics.
4. Ask the user for scope and purpose mode in one turn:
	- all files
	- one category
	- selected files
	- one shared `collectionPurpose`
	- per-file purpose
	- auto-infer purpose
5. Route each selected file through `.codex/commands/ingest.md`.
6. Delete inbox originals only after raw-source verbatim preservation passes.
7. Update `index.md`, `log.md`, and qmd indexes.

## Output

Show pending counts, selected ingest scope, completed raw sources, created/updated Wiki pages, and any files left in Inbox.
