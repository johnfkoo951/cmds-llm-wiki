# cmds-llm-wiki — Changelog

템플릿 버전 이력. (`cmds-system-files` 의 CHANGELOG 형식 참고)

---

## v1.0.0 — 2026-04-14 (Initial Template Release)

**Source**: Extracted and sanitized from Yohan Koo's personal LLM Wiki satellite vault, active since 2026-04-10.

### Architecture

- **3-Layer**: Raw Sources (immutable) / Wiki (LLM-managed) / Schema (CLAUDE.md)
- **Operations**: Ingest · Query · Lint · Refresh-Context
- **Core files**: `index.md`, `log.md`, `CLAUDE.md`, `Core Context.md`

### Claude Code Harness

- **7 slash commands** in `.claude/commands/`:
  - `/ingest` — purpose-gated source ingestion with mothership cross-link search
  - `/inbox` — batch scan of `00. Inbox/` with single-axis / per-file / auto-infer modes
  - `/query` — wiki-grounded Q&A with 7-axis reuse tagging
  - `/lint` — health check (orphans, broken links, contradictions, v2 coverage, Core Context freshness)
  - `/status` — at-a-glance stats + coverage metrics
  - `/reindex` — manual qmd index rebuild
  - `/refresh-context` — re-snapshot Core Context when mothership drifts
- **2 PostToolUse hooks** in `.claude/hooks/`:
  - `validate-raw-source.sh` — enforces `## Original Content` verbatim preservation
  - `qmd-reindex.sh` — debounced auto-reindex on Write/Edit

### Schema Standards

- **YAML 2 spaces / Body TAB** indentation
- **7 required properties**: `type`, `aliases`, `description` (English), `author`, `date created`, `date modified`, `tags`
- **Wikilinks in YAML must be quoted**: `"[[link]]"`
- **Mermaid labels in quotes**: `A["label"]`
- **camelCase for new YAML keys**: `collectionPurpose`, `mainVaultRelated`, `mainVaultCmds`, `reusableFor`

### Gold In Gold Out Policy (v2 frontmatter)

- **`collectionPurpose`** — mandatory user answer to "왜 수집?" at ingest time
- **`mainVaultRelated`** — 2~5 related notes from (optional) mothership vault, found via qmd
- **`mainVaultCmds`** — mothership CMDS category (if applicable)
- **`reusableFor`** — which of the 7 reuse axes a query answer feeds

### Collection Infrastructure

- **18 Obsidian Web Clipper templates** in `90. Settings/Sharing/`:
  - Articles (web, tech-blog, news, substack), Social (X, threads, linkedin, reddit, instagram, hackernews)
  - Video (youtube, podcast), Technical (github, arxiv, tech-docs, linkedin-pulse)
  - Selection clipper for ad-hoc highlights
- **qmd config template** in `90. Settings/qmd-config-template.yml` — BM25 + vector hybrid search

### Example Content

- 2 Raw Sources (Karpathy LLM Wiki gist + X thread)
- 4 Concept wiki pages (LLM Wiki Pattern, RAG vs Compiled Wiki, 3-Layer Architecture, Ingest-Query-Lint Cycle)
- 3 Entity pages (Karpathy, Vannevar Bush, Memex)
- 1 Guide (Obsidian Tooling for LLM Wiki)
- 2 MOCs (Knowledge Management, LLM Wiki Guide)

### Notes

- Template uses `{your-name}`, `{Your Name}`, `{PATH_TO_YOUR_LLM_WIKI}`, `{PATH_TO_YOUR_MOTHERSHIP_VAULT}`, `{your-mothership-vault-name}` placeholders per the `cmds-system-files` convention.
- Mothership integration is **optional** — this wiki operates standalone or as satellite to any Obsidian PKM vault.
