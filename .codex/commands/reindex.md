---
description: Rebuild qmd BM25 and vector indexes for wiki, raw_sources, and queries collections.
---

# /reindex — Codex qmd Reindex

Use after direct Obsidian edits, bulk file moves, embedding model changes, or suspected index drift.

## Workflow

```bash
export QMD_EMBED_MODEL="hf:Qwen/Qwen3-Embedding-0.6B-GGUF/Qwen3-Embedding-0.6B-Q8_0.gguf"
qmd update
qmd embed
qmd status
```

Force rebuild:

```bash
qmd embed -f
```

## Scope

- `20. Wiki/**/*.md`
- `10. Raw Sources/**/*.md`
- `30. Queries/**/*.md`

Inbox is excluded until ingest.

## Related

- Auto hook: `.codex/hooks/qmd-reindex.sh`
- Config template: `90. Settings/qmd-config-template.yml`
