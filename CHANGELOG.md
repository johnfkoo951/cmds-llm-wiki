# cmds-llm-wiki — Changelog

템플릿 버전 이력. (`cmds-system-files` 의 CHANGELOG 형식 참고)

---

## v1.6.1 — 2026-06-16 (3-Layer 개념층 vs 물리 폴더 정합 노트)

**Source**: 운영 볼트의 지식 레이어 재검증 과정에서, 템플릿이 `30. Queries/` 물리 폴더를 제공하면서도 3-Layer(Raw/Wiki/Schema) 개념과의 관계를 설명하지 않아 신규 사용자가 "30. Queries 는 4번째 레이어인가?" 혼동하던 지점 발견.

### Changed

- `3-Layer Architecture`: "이 볼트에서의 구현" 표 아래에 callout 추가 — `30. Queries/` 는 *4번째 구조 레이어가 아니라* Ingest-Query-Lint 의 Query 단계 산출 위치임을 명시 (구조 축 Raw/Wiki/Schema vs 운영 축 Ingest/Query/Lint 구분). 유저별 콘텐츠가 아닌 일반 개념 정합이라 템플릿에 반영.

---

## v1.6.0 — 2026-06-08 (Codex 호환 — dual-harness)

**Source**: 운영 볼트가 Claude Code + Codex 양 harness 로 정합화(같은 operation 이름을 `.claude/` · `.codex/` · `.agents/skills/` 에 1:1 유지)된 것을 공개 킷에도 반영. 이전 킷은 Claude 전용이었음.

### Added

- **`AGENTS.md`** — Codex / 타 에이전트용 schema mirror (CLAUDE.md 와 같은 규칙, audience 만 다름).
- **`.codex/`** — Codex operation harness: `commands/` 10개 (Claude commands 와 1:1 mirror) + `hooks/` (`validate-raw-source.sh`, `qmd-reindex.sh`) + `hooks.json`. 코덱스 hook 은 단순 payload shape (`tool_input.path` / `file_path` / `path`) 도 처리하고, Book Ingest `status: stub` chapter 는 body-length 검사에서 제외.
- **`.agents/skills/`** — Codex reusable operation skills 10개 (`{operation}/SKILL.md`).
- **`.claude/commands/`** 에 `capture-tabs`, `verify`, `audit` 3개 추가 (기존 8 → 11). Capture Tabs = AI research / 브라우저 탭 묶음 → Inbox pre-ingest layer. Verify = 단일 페이지 3-기준 검증. Audit = vault/MOC 전체 점검 + `/verify` 큐.

### Changed

- `CLAUDE.md`: Operations 섹션에 Agent Note + Cross-Agent Compatibility Matrix + Codex Compatibility Notes 추가, Folder Structure 에 `.codex/` · `.agents/` · `AGENTS.md` 반영, Essential operations 한 줄 갱신. version 1.5.0 → 1.6.0.

### Notes

- Codex hook 경로는 `{PATH_TO_YOUR_LLM_WIKI}` placeholder — 셋업 시 절대 경로로 치환 (또는 `/onboard` 가 처리). Claude hook 은 `$CLAUDE_PROJECT_DIR` 라 치환 불필요.

---

## v1.5.0 — 2026-06-01 (/onboard 인터뷰 셋업 커맨드)

**Source**: 온보딩이 수동 `Setup Guide.md`(sed)뿐이라, "온보딩해줘/처음 시작할게" 트리거로 필수 질문을 물으며 placeholder·Core Context를 자동으로 채우는 대화형 단계 신설.

### Added

- **`.claude/commands/onboard.md`** — 인터뷰 기반 first-run 셋업 커맨드. pre-flight 감지 → 필수 5문항(위치/이름 · Mode A·B · 모선 경로 · Core Context §1 정체성 · §2 재활용 축) + 옵션(§3·§4) → placeholder 일괄 치환 + Core Context 작성 + `status: active`. answer-1-of-many · resume · 음성 모드 · passive fallback 포함 (cmds-onboarding 철학 차용).

### Changed

- `Setup Guide.md`: 상단에 `/onboard` 대화형 경로 안내 추가, 대상 버전 v1.3.0 → v1.5.0+.

---

## v1.4.1 — 2026-05-31 (Doc Fixes · Live Showcase URL · Placeholder Count · Mothership Count Soften)

**Source**: `cmds-system-files` v4.9.0 audit surfaced three documentation bugs in this kit.

### Fixed

- **README "Live Showcase" link** → `https://llm-wiki.cmdspace.work` (the prior `cmds-llm-wiki.vercel.app` returned HTTP 401; the branded apex is live 200).
- **CHANGELOG placeholder count** corrected from "10 files" to "13 files carry placeholder tokens" (live count).
- **`Core Context.md` mothership reference** softened from a hard "5 system files" count to durable "multiple audience-specific system files … + semver changelog" phrasing — the mothership is now 9 files / 6 public after the 2026-05-27 8→9 restructure, and an un-counted phrasing won't re-stale.

### Note

- No schema/structure changes. canonical ↔ DEV mirror ↔ ZIP regenerated together.

---

## v1.4.0 — 2026-05-27 (Missing Files Audit · Hotkeys · Empty Queries Folder · Stibee Clipper)

**Source**: User audit "왜 옵시디언 웹클리퍼 json 파일들이 빠져있지?" surfaced three template gaps that had silently drifted from the live operating vault. Same release also closes the 3-place sync loop documented at v1.3.0 by promoting the canonical (`_starter-kit/cmds-llm-wiki/`) as single source of truth.

### What's missing → now included

- **`.obsidian/hotkeys.json`** (9.2 KB · 73 bindings) — Korean PKM-friendly Obsidian hotkey set used in the operating vault. Heading shortcuts (`⌘1~4`), wikilink/callout inserters (`⌘[` / `⌘]`), sidebar toggles, etc. Optional — delete if your own keymap suits you.
- **`30. Queries/`** (empty folder + `.gitkeep`) — Was missing entirely from the v1.3.0 template even though `/query` writes results here and the README structure referenced it. `.gitkeep` ensures the folder ships through git/zip.
- **`clipper-stibee.json`** — Korean newsletter platform (Stibee) Web Clipper. Operating vault has had this since 2026-04-14; v1.3.0 sanitization excluded it. Re-included for Korean newsletter users. (Sanitization decision retained: `clipper-parkjoon-mdshare.json` stays excluded — it targets a personal domain.)

### Numbers

- Clipper JSON: 17 → **18**
- Folders shipped: was missing `30. Queries/` and `.obsidian/`; now complete
- No schema changes (CLAUDE.md still v1.4 over v1.3 structurally identical except frontmatter `version`/`date modified`)

### 3-place sync canonicalised (operational doc, not template content)

Documented in parent vault's `CMDS_LLM_Wiki/CLAUDE.md` "Starter Kit Distribution (3-Place Sync)" section:
1. Canonical: `_starter-kit/cmds-llm-wiki/` (this folder, unversioned)
2. DEV mirror: `/DEV/cmds-llm-wiki/` ↔ GitHub `johnfkoo951/cmds-llm-wiki`
3. ZIP archives: `_starter-kit/cmds-llm-wiki-{starter-kit,vX.Y.Z}.zip`

🚫 `~/Downloads/cmds-llm-wiki-*.zip` is no longer used as a distribution surface. External users obtain releases via GitHub Releases.

### Placeholder coverage

13 files carry placeholder tokens (~10 require user substitution before operation). Placeholder types: `{your-name}`, `{Your Name}`, `{PATH_TO_YOUR_LLM_WIKI}`, `{PATH_TO_YOUR_MOTHERSHIP_VAULT}`, `{your-mothership-vault-name}`, `{YYYY-MM-DD}`. Run the `sed` commands in `90. Settings/Sharing/Setup Guide.md` to replace all in one shot per Mode A (standalone) or Mode B (mothership-satellite).

### Files changed

- `.obsidian/hotkeys.json` (new)
- `30. Queries/.gitkeep` (new)
- `90. Settings/Sharing/clipper-stibee.json` (new)
- `CLAUDE.md` — frontmatter `version: "1.3"` → `"1.4"`, `date modified`
- `README.md` — clipper count 17→18 (with Stibee), hotkeys.json mention, structure section
- `CHANGELOG.md` — this entry

---

## v1.3.0 — 2026-05-04 (Quality Control v4 + Tool Outputs + Multi-Harness)

**Source**: Distilled from one month of operating the parent vault since v1.2.0. Three classes of upgrade: (1) a Book Ingest hook bug uncovered during real ingestion, (2) page-level quality-control properties that emerged from a self-audit ("we have 89 wiki pages but 0% are human-verified"), (3) generalised harness compatibility for non-Claude-Code agents.

### Bug fixes

- **`validate-raw-source.sh` — skip `status: stub`**: Book Ingest chapter stubs intentionally have no `## Original Content` until the user reads them and re-invokes `/ingest` for promotion. The v1.1.0 release added Book Ingest but the verbatim-validation hook still blocked stubs as malformed Raw Sources. Hook now reads frontmatter and exits 0 for `status: stub` files.
- **`lint.md` indentation**: Step 8 sub-bullets used 2-space indent instead of TAB, violating the project's body-uses-TAB rule. Fixed.

### What's new

#### Exploration Gate (v4 frontmatter)

A page-level human-verification track on Wiki pages. Addresses the gap where `confidence: high` was being set by the LLM at compile time without any human read pass.

- New optional Wiki page properties: `explored: false|true`, `exploredBy: "[[Name]]"`, `exploredDate: YYYY-MM-DD`
- New `> [!note] Bias Check` callout pattern (Counter-argument + Data gap) for high-confidence and synthesis-heavy pages
- New `> [!check] Exploration Gate` callout for documenting verification status
- `/ingest` now emits new pages with `explored: false` by default and adds Bias Check on `confidence: high`
- `/lint` Step 8 reports `explored` coverage % and high-confidence pages without bias check
- `/status` reports `explored:` and `mainVault*:` coverage %
- `/query` flags missing `mainVaultRelated`, `explored`, or Bias Check during synthesis

#### `70. Outputs/` Tool Output Convention (optional)

A separate folder for external-tool side products (graphify, audio-transcriber, etc.) that should not pollute the Wiki layer. Generic pattern: `70. Outputs/{tool-name}/{YYYY-MM-DD}-{topic}/`. Outputs are exempt from the standard schema (frontmatter, naming) — they're the tool's format. Insights distilled from outputs go into `30. Queries/` or get absorbed into Wiki pages, so Wiki body never wikilinks into `70. Outputs/`. Skip this folder entirely if you don't run such tools.

#### CJK Person Naming Rule

Native script only for Korean / Chinese / Japanese person entities; English Romanization moves to `aliases`. Examples: `홍길동.md`, `张汉东.md` (not `홍길동 (Gildong Hong).md`). Latin handles + real-name combos (`kepano (Steph Ango).md`) keep their existing form. Reasons: file-name duplication adds wikilink friction, Romanization is transliteration not identity, Obsidian graph/search reads aliases.

#### Multi-harness comment headers

Every `.claude/commands/*.md` now carries a YAML-comment line listing the equivalent tool names on Antigravity (Gemini) and similar harnesses — `view_file`, `write_to_file`, `replace_file_content`, `list_dir`, `grep_search`, `run_command`, `read_url_content`. Helps users running these commands through non-Claude-Code agents identify the equivalent tool surface.

#### Genericised "7 reuse axes"

`/ingest` and `/query` previously hard-coded the parent vault's specific axes (PhD / 학술 / 강의 / 컨설팅 / CMDS 시스템 / 에세이 / 제품). Now both files reference [[Core Context]] §2 directly with neutral examples (학술 / 저술 / 강의 / 컨설팅 / 제품 / 에세이 / 커뮤니티). User-defined axes (5~9 recommended) remain the source of truth.

#### Setup Guide (deeper personalization manual)

New `90. Settings/Sharing/Setup Guide.md` — covers Mode A (standalone) vs Mode B (mothership-satellite) operation, single-pass `sed` replacement commands per mode, verification `grep`, 8-step setup procedure, and 7-item FAQ. Complements README.md (which stays as the GitHub-facing 5-step quick start). Convertible to PDF via the same `md-to-pdf` workflow used to produce the 2026-04-30 standalone PDF.

### Files changed

- `.claude/hooks/validate-raw-source.sh` — stub skip
- `.claude/commands/{ingest,inbox,lint,query,refresh-context,reindex,status}.md` — Antigravity equivalents header
- `.claude/commands/ingest.md` — Quality control v4 block + genericised axes
- `.claude/commands/lint.md` — Step 8 v2/v4 coverage + indent fix
- `.claude/commands/status.md` — explored + mainVault coverage lines
- `.claude/commands/query.md` — quality gap flagging + genericised axes
- `CLAUDE.md` — `70. Outputs/` section, Frontmatter Standards v4 block, CJK naming rule, Bias/Exploration callouts, version bump 1.0 → 1.3
- `90. Settings/Sharing/Setup Guide.md` — new
- `README.md` — pointer to Setup Guide above the 5-step quick start
- `CHANGELOG.md` — this entry

### Migration notes

No breaking changes. Existing v1.2.0 vaults adopt v1.3.0 by:
1. Pulling the updated hook (`validate-raw-source.sh`) — required if you use Book Ingest
2. Pulling updated commands and CLAUDE.md — adds optional fields, doesn't break existing pages
3. (Optional) backfilling `explored: false` on existing Wiki pages via `/lint` flag list

---

## v1.2.0 — 2026-04-29 (Cohort Learnings)

**Source**: Distilled from a real classroom cohort that adopted LLM Wiki Starter Kit as the practical backbone of a regular university course (10 students, 10 distinct domains — systematic review, healthcare AI, anti-aging content, silver-care market analysis, sports analytics, biomedical research, embryology AI, etc.). All cohort-specific names, organizations, and personal contexts have been anonymized — only the generalizable patterns and operational learnings ship in this template.

### What's new

#### `/ingest` skill — Inbox cleanup discipline (operational fix)

Previously possible failure mode: writing the Raw Source but forgetting to delete the Inbox original → next `/inbox` scan re-ingests the same source → duplicate Raw Sources. Now explicit:

- **Step 2 renamed** to "Save Raw Source (Move, not Copy)" with prominent warning callout
- **Inbox cleanup section** added — when source originated from `00. Inbox/`, the Inbox file MUST be deleted after pre-flight checklist passes (with source-origin matrix specifying when delete applies)
- **Step 7 verification** — explicit Inbox cleanup check (`ls "00. Inbox/{subfolder}/"` should not show consumed file)
- **Failure modes** section restructured: (1) summarization-instead-of-verbatim, (2) Inbox residue

Edge case documented: delete only AFTER all pre-flight checks pass, otherwise verbatim failure could lose the only copy.

#### New Concepts (4)

- **`Cohort Token Economy`** — Predictable failure pattern when 80%+ of a cohort relies on Pro plan. Distinguishes cohort runs from individual hobbyist usage. Informs curriculum/onboarding design (token economy must be in week 1, not discovered in week 4).
- **`External Pre-processing Pattern`** — "Claude 가 잘하는 것 만 Claude 에게 시킨다." Heavy raw conversion (long PDFs, video transcripts, large web scrapes, foreign-language content) goes to GPT Deep Research / Google AI Studio / Whisper STT first; only the distilled output enters LLM Wiki via `/ingest`. Cohort estimates: 50-80% token savings.
- **`Track Classification and Research Gap Detection`** — Custom command pattern for typology-driven domains. Splits ingested papers into thematic tracks during ingest, computes per-track coverage %, surfaces lowest-coverage track as research gap. Generalizable across systematic review · market analysis · content planning · learning path design. Includes `/track` skill proposal.
- **`Idea Generation Pipeline`** — Each new raw source triggers automatic idea generation tied to a domain seed context. Distinguishes LLM Wiki from passive learning tools (NotebookLM-style) by treating each new input as a divergence prompt, not just a record. Includes `/idea` skill proposal.

#### New Guide (1)

- **`LLM Wiki Token Optimization Strategies`** — 4-step practical guide (1: external preprocessing → 2: model selection → 3: `/effort` throttling → 4: infrastructure decisions). Designed as a curriculum companion when introducing LLM Wiki to a class, lab, or study cohort. Includes decision-flow diagram, week-by-week curriculum recommendation, and policy-change hedge advice (don't lock cohorts into a single vendor).

### Files changed

- `.claude/commands/ingest.md` — Step 2 title + Inbox cleanup section + Step 7 verification + Failure modes restructure
- `20. Wiki/21. Concepts/Cohort Token Economy.md` — new
- `20. Wiki/21. Concepts/External Pre-processing Pattern.md` — new
- `20. Wiki/21. Concepts/Track Classification and Research Gap Detection.md` — new
- `20. Wiki/21. Concepts/Idea Generation Pipeline.md` — new
- `20. Wiki/23. Guides/LLM Wiki Token Optimization Strategies.md` — new
- `CHANGELOG.md` — this entry

### Migration notes

No breaking changes. Existing v1.1.0 vaults can adopt v1.2.0 by:
1. Pulling the updated `.claude/commands/ingest.md`
2. Copying the 4 new concept pages and 1 new guide page (or letting `/ingest` auto-generate them as wikilinks resolve)
3. Reviewing `Cohort Token Economy` if running a cohort

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
