# cmds-llm-wiki — Changelog

템플릿 버전 이력. (`cmds-system-files` 의 CHANGELOG 형식 참고)

---

## v1.1.0 — 2026-04-20 (Book Ingest Pattern)

**Addition**: `/ingest` operation gains a new variant — **Book Ingest Mode (Progressive Stubs)** — for multi-page books and documentation sites.

### What it solves

멀티 페이지 책 (mdBook, VitePress, GitBook, Docusaurus, ReadTheDocs, Nextra 등 TOC ≥5 챕터) 을 표준 `/ingest` 로 처리하면 두 가지 실패:

1. **한 파일에 전부** → 가독성 붕괴, `## Original Content` 비대화
2. **전체 동시 컴파일** → 읽지도 않은 내용이 Wiki 에 심어져 contamination (AI 요약이 human-curated knowledge 자리 차지)

### How it works

- **Scaffold**: 1 Book Index Raw Source (verbatim preface + TOC with wikilinks) + N chapter stubs (`status: stub`, placeholder `## Original Content`, navigable via `chapterPrev`/`chapterNext`)
- **Wiki seed**: book entity + author entity + preface-anchor concept (≤3 페이지). 장별 wiki 는 **미생성**.
- **Promote on read**: 사용자가 장을 읽을 때 해당 stub 파일에 `/ingest` 재호출 → URL 에서 verbatim fetch + `## Original Content` 채움 + 장 특화 Wiki 컴파일 + `status: stub → completed` + Book Index Progress Tracking 업데이트

Karpathy "지식은 스크랩이 아니라 독서 시점에 컴파일" 원칙의 구체화. [[Progressive Disclosure Pattern]] 의 ingest-layer 대응.

### New frontmatter keys (Raw Source, book stubs only)

- `status: stub | reading | completed` (기존 `ingested` 와 병존)
- `bookIndex` — 소속 Book Index wikilink
- `chapterNumber` — 정수
- `chapterPart` — 편/파트 이름 (원문 언어 보존)
- `chapterPrev` / `chapterNext` — 이전·다음 챕터 wikilink (null 가능)

### File naming

- Book Index: `YYYY-MM-DD-{authorSlug}-{bookSlug}-book-index.md`
- Chapter Stub: `YYYY-MM-DD-{authorSlug}-{bookSlug}-ch{NN}-{slug}.md`

### Files changed

- `.claude/commands/ingest.md` — "Book Ingest Mode (Multi-Page Sources)" 섹션 추가 (step B-1 ~ B-5 + promotion workflow + hook interaction + visual pattern)
- `CLAUDE.md` — Operations §1 Variants callout + Raw Source frontmatter 에 `status` enum 확장 + Book Ingest 전용 4 키 + 파일 네이밍 테이블 2 행 추가
- `20. Wiki/21. Concepts/Book Ingest Pattern.md` — 신규 self-documenting concept 페이지 (architecture, lifecycle, 적합성 매트릭스, hook interaction)

### Hook compatibility

`validate-raw-source.sh` 는 stubs 도 통과 — 모든 stub 이 `## Original Content` 섹션을 placeholder 와 함께 보유. Hook 이 본문 substantiveness 검사로 업그레이드될 경우 `status: stub` 예외 처리 필요 (document in Book Ingest Pattern concept).

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

### 미래의 나에게 보내는 편지 Policy (v2 frontmatter)

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
