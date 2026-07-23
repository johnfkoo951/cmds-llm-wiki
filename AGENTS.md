---
type: documentation
aliases:
  - LLM Wiki Schema
  - Wiki Harness
description: "Schema and harness document for the CMDS LLM Wiki vault. Defines the 3-layer architecture (Raw Sources / Wiki / Schema), ingest-query-lint operations, file conventions, and frontmatter standards. This is the single source of truth for LLM behavior in this vault."
author:
  - "[[{your-name}]]"
date created: 2026-04-10T21:30
date modified: 2026-07-23
tags:
  - system
  - schema
  - llm-wiki
status: active
version: "1.10.0"
---

# AGENTS.md — LLM Wiki Schema

This file is the **Schema Layer** of the CMDS LLM Wiki. It governs how LLMs (Codex, Cursor, etc.) read, write, and maintain this vault.

> **Architecture**: Karpathy LLM Wiki Pattern
> - Raw Sources = 소스코드 (immutable)
> - Wiki = 실행 파일 (LLM이 관리)
> - Schema = 이 문서 (AGENTS.md)

---

## ⚠️ CRITICAL RULES

### Indentation Rules
- **YAML frontmatter**: 2 SPACES (절대 탭 금지)
- **Markdown body**: TAB (절대 스페이스 금지)

### Wikilink Rules
- YAML 내 wikilinks는 반드시 큰따옴표: `"[[link]]"`
- Markdown body에서는 따옴표 없이: `[[link]]`

### Description Rule
- **`description` 값은 항상 큰따옴표**로 감쌀 것 — 값에 콜론(`: `)·엠대시(`—`)·괄호·`#`·wikilink 등이 들면 unquoted YAML 은 파싱 에러로 노트 전체가 렌더 실패한다.
	- ✅ `description: "RLHF: 인간 피드백 기반 정렬 (3단계)."`
	- ❌ `description: RLHF: 인간 피드백 기반 정렬 (3단계).`
- 값 안에 `"` 가 있으면 `\"` 이스케이프하거나 문장을 재작성. 빈 값도 `description: ""`.

### Provenance Rule (author + model + effort)
- 에이전트가 쓰는 모든 콘텐츠 페이지(raw-source·wiki-page·research-question·query-result·synthesis·moc·inbox·paper-hub·paper-analysis)는 `author` 바로 뒤에 **`model`·`effort` 를 항상 기록** — Claude Code·Codex·Grok 가 누가·어떤 모델·어떤 강도로 썼는지 교차 확인.
	- `model`: 상세 모델 id (`claude-opus-4-8`, `claude-sonnet-5`, `gpt-5.4-codex`, `grok-4` …). 복수 기여 시 list.
	- `effort`: 추론 강도/모드 (`low`/`medium`/`high`/`xhigh`/`max` 또는 타 에이전트 등가). 미상은 `default`.
	- harness 정의 파일(command/skill)의 자기 frontmatter 엔 넣지 않음 — Description Rule 만 적용.

### Mermaid Rules
- **모든 노드/엣지 라벨은 큰따옴표**로 감쌀 것 — 한글·특수문자 안정성
	- ✅ `A["시작"] --> B{"선택?"}`
	- ❌ `A[시작] --> B{선택?}`
- **`[/` 로 시작하는 라벨 금지** — trapezoid 도형 기호로 파싱됨 (lexical error)
	- ❌ `C[/query 스킬]`
	- ✅ `C["/query 스킬"]` 또는 `C["query 스킬"]`
- **엣지 라벨도 따옴표 권장**: `B -->|"한글 라벨"| C`
- 라벨 안에 마크다운(`**bold**`, `[[wikilink]]`) 금지 — 렌더 깨짐

### Pre-Flight Checklist (Before Every Write/Edit)
- [ ] YAML frontmatter uses 2 SPACES
- [ ] Markdown body uses TAB
- [ ] Wikilinks in YAML are quoted: `"[[link]]"`
- [ ] Mermaid node/edge labels are quoted: `A["label"]`
- [ ] Arrays use proper format: `- value`
- [ ] Dates use ISO 8601: `YYYY-MM-DD`
- [ ] `description` field present, in English, and **double-quoted** (`description: "..."`)
- [ ] Agent-written content pages carry provenance: `author` + `model` + `effort`
- [ ] File saved in correct layer folder

---

## Essential (Post-Compact)

> 컨텍스트 압축 후에도 반드시 기억:
> 1. **YAML: 2 SPACES** / **Body: TAB**
> 2. **Wikilinks in YAML: 큰따옴표** `"[[link]]"`
> 3. **Mermaid 라벨: 큰따옴표** `A["label"]` / `[/` 로 시작 금지
> 4. **3 Layers**: Raw Sources (immutable) → Wiki (LLM-maintained) → Schema (this file)
> 5. **Operations**: Capture Tabs → Inbox → Ingest → Query → Verify/Audit → Lint (+Status/Reindex/Refresh)
> 6. **필수 프로퍼티 7개**: type, aliases, description (English, **항상 큰따옴표**), author, date created, date modified, tags
> 7. **Core Context 먼저 읽기**: 모든 operation 전에 [[Core Context]] 로 사용자 목적·철학 정렬
> 8. **미래의 나에게 보내는 편지**: `/ingest` 는 반드시 수집 목적 1회 질문 → `collectionPurpose` 프로퍼티에 기록
> 9. **Provenance 항상 (v6)**: 에이전트 작성 페이지는 `author` + `model`(상세 모델 id) + `effort`(추론 강도) 기록 — Claude/Codex/Grok 교차 참조

---

## 🧭 Core Context (반드시 먼저 로드)

**모든 operation 전에 [[Core Context]] 를 먼저 읽는다.**

해당 노트는 (1) 사용자의 정체성·7 재활용 축·철학 + (2) **옵션**: 별도 mothership 볼트가 있다면 그 시스템 파일 snapshot 을 담는다. 이 맥락 없이는 LLM Wiki 의 모든 operation 이 "목적 없는 자동 정리" 로 전락한다. mothership 예시 구성은 아래 표 참조 — standalone 사용자는 건너뜀.

### (옵션) 메인 볼트 9 시스템 파일 — 원 저자 CMDSPACE 구성 예시 (precedence 순)

Mothership 볼트가 없는 standalone 사용자는 이 표를 건너뛰어도 됩니다. 원 저자 기준: 6개 공개 + 3개 비공개 (vendor·product 전용).

| # | Alias | 경로 | 역할 | 공개 |
|:-:|-------|------|------|:----:|
| 1 | `@CMDS-CLAUDE` | `{your-mothership-vault-name}/CLAUDE.md` | HOW — Claude Code 기술 규칙 | 공개 |
| 2 | `@CMDS-AGENTS` | `{your-mothership-vault-name}/AGENTS.md` | HOW — 타 AI 에이전트 규칙 (Codex, Cursor, Windsurf) | 공개 |
| 3 | `@CMDS-Antigravity` | `{your-mothership-vault-name}/ANTIGRAVITY.md` | HOW — Google Gemini / Antigravity IDE 전용 | 비공개 |
| 4 | `@CMDS-Context` | `{your-mothership-vault-name}/CMDS.md` | WHY/WHAT — 시스템 철학·사용자 프로필 | 공개 |
| 5 | `@CMDS-Guide` | `{your-mothership-vault-name}/🏛 CMDS Guide.md` | STANDARDS — 7 프로퍼티·템플릿·camelCase | 공개 |
| 6 | `@CMDS-HQ` | `{your-mothership-vault-name}/🏛 CMDS Head Quarter.md` | WHERE — 87 서브카테고리 네비게이션 | 공개 |
| 7 | `@CMDS-Brain` | `{your-mothership-vault-name}/BRAIN.md` | PERSONA — {your-name} brain profile (개인 제품 연동용) | 비공개 |
| 8 | `@CMDS-BrainPrompt` | `{your-mothership-vault-name}/BRAIN_PROMPT.md` | PERSONA — Agent Rules of Engagement | 비공개 |
| 9 | `@CMDS-DESIGN` | `{your-mothership-vault-name}/DESIGN.md` | VISUAL — v4.3 design constants · Anti-Slop · skill ↔ surface mapping | 공개 |

최신본 읽기: `Read("{PATH_TO_YOUR_MOTHERSHIP_VAULT}/{file}")` 또는 `mcp__qmd__query` (user-scope, cwd 무관).

[[Core Context]] 은 `snapshot_date` 기준. 30일 이상 오래되면 lint 가 flag → re-snapshot.

---

## Vault Overview

이 볼트는 **Karpathy LLM Wiki Pattern**을 구현한 LLM 전용 지식 베이스입니다.

- **목적**: LLM이 raw sources를 컴파일하여 persistent, structured wiki를 유지
- **철학**: RAG(매번 검색+합성)가 아닌, 한 번 컴파일된 위키가 compounding artifact로 성장
- **연결**: (옵션) mothership Obsidian 볼트의 satellite 로 운영 가능

### (옵션) Mothership 볼트 연결

별도 PKM 볼트가 있다면 본 LLM Wiki 를 satellite 로 두고 cross-reference.

| 항목 | 값 |
|------|-----|
| 메인 볼트 경로 | `{PATH_TO_YOUR_MOTHERSHIP_VAULT}` |
| 이 볼트 경로 | `{PATH_TO_YOUR_LLM_WIKI}` |
| Cross-reference | `source-vault` 프로퍼티로 메인 볼트 노트 참조 |

---

## 3-Layer Architecture

### Layer 1: Raw Sources (`10. Raw Sources/`)

**불변층** — 원본 자료를 그대로 보관. 절대 수정하지 않음.

```
10. Raw Sources/
├── 11. Articles/     # 웹 기사, 블로그 포스트
├── 12. Papers/       # 학술 논문, 기술 보고서
├── 13. Books/        # 도서 노트, 챕터 요약
├── 14. Transcripts/  # 강연, 팟캐스트, 영상 전사
├── 15. Clippings/    # 웹 클리핑, 스크랩
└── 16. AI Research/  # ChatGPT/Gemini/Grok/Claude/Perplexity 선행 조사 묶음
```

**규칙**:
- 원본 텍스트를 그대로 보존
- 수정이 필요하면 Wiki 페이지에서 재해석
- `type: raw-source` frontmatter 사용
- `date ingested` 프로퍼티로 인제스트 시점 기록

### Layer 2: The Wiki (`20. Wiki/`)

**LLM 관리층** — LLM이 직접 작성하고 업데이트하는 지식 페이지.

```
20. Wiki/
├── 21. Concepts/     # 추상 개념 (Attention, Transformer, RLHF, ...)
├── 22. Entities/     # 사람, 조직, 제품 (OpenAI, Karpathy, GPT-4, ...)
├── 23. Guides/       # How-to, 튜토리얼, 실전 가이드
├── 24. Maps/         # MOC (Map of Content), 주제별 인덱스
└── 25. Questions/    # Research Question — 1급 연구 질문 카드 (v6.1)
```

**규칙**:
- `21~24` 페이지는 `type: wiki-page`, `25. Questions` 카드는 `type: research-question` frontmatter 사용
- 관련 Raw Source를 `source` 프로퍼티로 역참조
- 모든 주장에 출처 명시 (Wiki 내 링크 또는 Raw Source 참조)
- Cross-reference: 관련 개념은 반드시 `[[wikilink]]`로 연결
- 모순 발견 시 `> [!warning] Contradiction` callout으로 플래그
- To-do/미해결 항목은 `> [!question] Open Question` callout 사용
- 반복 등장하거나 산출물로 이어질 질문은 Open Question 콜아웃에서 `25. Questions/` 의 Research Question 카드로 승격 (`sourceCallout` 으로 역추적)

### Layer 3: Schema (이 파일)

**규칙층** — LLM의 행동을 제어하는 harness 문서.

---

## Operations

> **🤖 Agent Note (Codex & Antigravity)**:
> Codex 의 operation entrypoint 는 `.codex/commands/{operation}.md` 이다. 재사용 가능한 Codex skills 는 `.agents/skills/{operation}/SKILL.md` 처럼 직관적인 operation 이름을 사용한다 (`ingest`, `query`, `capture-tabs`, `status` 등). Antigravity(Gemini) 등 타 에이전트 역시 해당 operation을 수행하기 전에 대응 command 파일을 읽고 그 절차를 엄격히 따라야 한다.
> Claude Code 전용 command 는 `.claude/commands/{operation}.md` 에 보존한다. 같은 operation 은 양쪽 harness 에 같은 이름으로 둔다. Codex 작업에서는 `AGENTS.md` + `.codex/commands/` + 필요한 `.agents/skills/{operation}/SKILL.md` 가 우선이다.

### Cross-Agent Compatibility Matrix

Codex 에서 가능한 작업은 아래 10개 operation 으로 표준화한다. 새 operation 을 추가할 때는 **반드시** `.codex/commands/{name}.md`, `.agents/skills/{name}/SKILL.md`, 필요 시 `.claude/commands/{name}.md` mirror 를 함께 맞춘다.

> [!warning] Parity Contract (CLAUDE.md ↔ AGENTS.md)
> 이 두 스키마는 같은 규칙의 미러다. 다음 섹션은 **양쪽이 동일해야** 하며 한쪽만 편집 금지: (1) Cross-Agent Compatibility Matrix, (2) Frontmatter Standards (7 필수 + v2/v3/v4/v5/v6/v6.1/v6.2 키), (3) Verification Properties (v5) 3 기준, (4) Callout Conventions. 편집 시 CLAUDE.md 와 AGENTS.md 를 함께 고치고 `/lint` + parity 체크리스트로 확인. `.codex/`·`.agents/` 는 untracked 라 diff 에 안 보이므로 수동 대조가 필요하다.

| Operation | Codex command | Codex skill | Claude mirror | Notes |
|-----------|---------------|-------------|---------------|-------|
| Capture Tabs | `.codex/commands/capture-tabs.md` | `.agents/skills/capture-tabs/SKILL.md` | `.claude/commands/capture-tabs.md` | AI research / browser tab bundle → Inbox |
| Inbox | `.codex/commands/inbox.md` | `.agents/skills/inbox/SKILL.md` | `.claude/commands/inbox.md` | pending source preview + ingest routing |
| Ingest | `.codex/commands/ingest.md` | `.agents/skills/ingest/SKILL.md` | `.claude/commands/ingest.md` | purpose gate + Raw Source + Wiki compile |
| Query | `.codex/commands/query.md` | `.agents/skills/query/SKILL.md` | `.claude/commands/query.md` | compiled Wiki synthesis + Query Result |
| Lint | `.codex/commands/lint.md` | `.agents/skills/lint/SKILL.md` | `.claude/commands/lint.md` | health check + frontmatter coverage |
| Status | `.codex/commands/status.md` | `.agents/skills/status/SKILL.md` | `.claude/commands/status.md` | counts + coverage snapshot |
| Reindex | `.codex/commands/reindex.md` | `.agents/skills/reindex/SKILL.md` | `.claude/commands/reindex.md` | qmd update/embed/status |
| Refresh Context | `.codex/commands/refresh-context.md` | `.agents/skills/refresh-context/SKILL.md` | `.claude/commands/refresh-context.md` | Core Context from mothership system files |
| Verify | `.codex/commands/verify.md` | `.agents/skills/verify/SKILL.md` | `.claude/commands/verify.md` | single-page verification |
| Audit | `.codex/commands/audit.md` | `.agents/skills/audit/SKILL.md` | `.claude/commands/audit.md` | vault/MOC audit + `/verify` queue |

> `/onboard` 는 Claude 전용 first-run 셋업 인터뷰로 Codex mirror 가 없다 (Claude commands 11 = 위 10 + onboard). Codex 사용자는 `90. Settings/Sharing/Setup Guide.md` 의 sed 경로를 따른다.

### Codex Tool Compatibility Rules

| Task Type | Codex path | Rule |
|-----------|------------|------|
| File search | `rg`, `rg --files`, `find` | Use shell search first; avoid slow broad scans when qmd can scope collections. |
| File edit | `apply_patch` | Manual edits must use patch-style changes; keep Raw Sources immutable except ingest/update policy. |
| Wiki search | `qmd query`, `qmd vsearch`, `rg` | Prefer compiled Wiki first, then Raw Sources, then mothership. |
| Main-vault search | qmd collections + `rg "/Users/.../{your-mothership-vault-name}"` | Record useful cross-vault links in `mainVaultRelated`. |
| Browser capture | Browser/Computer Use when available, otherwise user export/paste | Never create public share links or modify accounts without action-time confirmation. |
| Hook validation | `.codex/hooks/validate-raw-source.sh` | Raw Sources need `## Original Content`; `status: stub` chapter stubs are exempt from body-length check. |
| Auto reindex | `.codex/hooks/qmd-reindex.sh` or `/reindex` | Inbox is excluded until ingest; `qmd status` verifies freshness. |
| Quality verification | `/verify` and `/audit` | Conflicts become `disputed`; do not delete evidence to force consistency. |

### 0. Capture Tabs / AI Research Capture (선행 조사 보존)

`/capture-tabs` 는 ChatGPT, Gemini, Grok, Claude, Perplexity, 일반 source tab 으로 만든 Chrome 탭 그룹을 `00. Inbox/05. AI Research/` 에 Markdown research bundle 로 저장하는 **pre-ingest capture layer** 다.

**Entrypoints**:
- Codex command: `.codex/commands/capture-tabs.md`
- Codex skill trigger: `.agents/skills/capture-tabs/SKILL.md`
- Claude mirror: `.claude/commands/capture-tabs.md`
- Template: `90. Settings/Templates/Template_AI Research Capture.md`

**규칙**:
- 원문·복사본·export 는 `## Original Content` 아래에 보존한다.
- 에이전트의 요약·불일치·Wiki 제안은 `## Agent Capture Notes` 아래에 둔다. 기존 `## Codex Capture Notes` 파일은 레거시 호환으로 인정한다.
- 기본 저장 위치는 `00. Inbox/05. AI Research/YYYY-MM-DD-ai-research-{topic-slug}.md` 이다.
- source URL, platform, visible model/account/workspace, capture method, capture limitation 을 기록한다.
- 공개 share link 생성, 계정 설정 변경, 대화창 전송, 파일 업로드는 사용자 action-time confirmation 없이 금지한다.
- `inbox-only`, `run-inbox`, `ingest-now` 중 다음 단계를 명시하고, `ingest-now` 는 `/ingest` 의 목적 질문과 메인 볼트 연결 검색을 그대로 따른다.

### 1. Ingest (새 자료 흡수)

> [!info] Variants
> - **Standard Ingest** (기본): 단일 URL/파일/텍스트 → 1 Raw Source + 10~15 Wiki pages
> - **Book Ingest (Progressive Stubs)**: 멀티 페이지 책·문서 사이트 (mdBook/VitePress/GitBook/Docusaurus/ReadTheDocs, TOC 에 5+ 챕터) → 1 Book Index + N chapter stubs + 소수 Wiki (책·저자·앵커 개념). 사용자가 장을 읽을 때 해당 stub 을 "promote" (verbatim 삽입 + Wiki 컴파일 + `status: stub` → `completed`). 상세: [[Book Ingest Pattern]] + `.codex/commands/ingest.md` "Book Ingest Mode" 섹션.
> - **Paper Ingest Mode (Academic Papers, v6.2)**: 논문(PDF/DOI/arXiv/Abstract+References) 자동 감지 → `.agents/skills/ingest/resources/paper-ingest.md` 리소스 로드 (12단 원자화, citekey 네이밍, RQ 연결, `p7_verify.py` 게이트). Standard/Book 와 공존, `/ingest` 단일 진입점. 사용자 매뉴얼: `90. Settings/Sharing/Paper Ingest Guide.md`.

새 source가 `00. Inbox/`에 들어오면:

0. **🎯 목적 질문 (미래의 나에게 보내는 편지)**: LLM은 사용자에게 **단일 질문** 을 던진다 — "이 소스를 왜 수집했나요? (7 재활용 축: PhD / 학술 / 강의 / 컨설팅 / CMDS 시스템 / 에세이 / 제품 중 어디에 쓰일 예정인가요?)". 답변 없이 ingest 하지 않음. 답변은 `collectionPurpose` 프로퍼티에 기록.
0-a. **🔗 메인 볼트 연결 검색 (옵션, mothership 운영 시만)**: 사용자 답변을 받으면 **메인 볼트에서 유사 노트·개념을 검색** 한다 (`mcp__qmd__query` vec/hyde + `Grep` path=`{PATH_TO_YOUR_MOTHERSHIP_VAULT}`). 2~5개 후보를 `mainVaultRelated` 프로퍼티에 기록하고 사용자에게 확인. mothership 이 없다면 이 단계는 건너뜀.
1. **분석**: source의 핵심 주제, 엔티티, 개념 추출
2. **저장**: `10. Raw Sources/{적절한 하위폴더}/`로 이동 (원본 보존). Raw Source frontmatter에 `collectionPurpose`, `mainVaultRelated`, `mainVaultCmds` 추가.
3. **컴파일**: 관련 Wiki 페이지 10~15개를 incremental update
   - 기존 페이지가 있으면 → 새 정보 추가/업데이트
   - 새 개념이면 → 새 Wiki 페이지 생성
4. **연결**: cross-reference 링크 추가, MOC 업데이트. Wiki 페이지에도 `mainVaultRelated` 프로퍼티로 모선 링크 유지.
5. **로그**: `log.md`에 ingest 기록 추가 — `collectionPurpose` 한 줄 포함.
6. **인덱스**: `index.md` 업데이트 (필요 시)

### 2. Query (지식 검색+합성)

질문을 받으면:

1. Wiki에서 relevant pages 검색
2. 정보 종합하여 답변 생성
3. 답변 과정에서 발견한 gap이나 모순은 Wiki에 피드백
4. 필요시 `30. Queries/`에 합성 결과 저장
5. 반응형 답변을 넘어 능동적 논증 구성(thesis + 근거 + 반론)이 필요하면 같은 폴더에 `type: synthesis` 카드로 저장 (v6.1)

### 3. Lint / Health Check (자가 정화)

주기적으로 수행:

- **Orphan 검사**: 어디에도 링크되지 않은 Wiki 페이지 찾기
- **Stale 검사**: 오래된 정보 플래그
- **모순 검사**: 페이지 간 상충하는 정보 발견 → callout 추가
- **누락 링크**: `[[link]]`가 있지만 페이지가 없는 경우 → 생성 또는 플래그
- **인덱스 동기화**: `index.md`가 실제 Wiki 구조와 일치하는지 확인

### 4. Source Update (기존 자료 업데이트)

이미 ingest된 Raw Source의 원본이 변경된 경우 (웹 기사 수정, 스레드 추가 등).

> ⚠️ **중요**: Source Update가 감지되면, 반드시 사용자에게 의견을 묻고 진행 방식을 확인받을 것.

**시나리오별 처리**:

| 시나리오 | Raw Source 처리 | Wiki 처리 | 커밋 메시지 |
|----------|----------------|-----------|-------------|
| **Minor** (오타, 문법) | 기존 파일 유지 | Lint에서 수정 | `lint: minor correction from {source}` |
| **Major** (새 정보, 수정된 주장) | 새 버전 파일 생성 (suffix `-v2`) | Re-ingest: 영향받는 Wiki 페이지 업데이트 | `ingest: {source} v2 — {변경 요약}` |
| **Contradiction** (기존 내용과 모순) | 모든 버전 보존 | `> [!warning]` callout 추가 | `update: {page} — contradiction flagged` |

**규칙**:
- Raw Source v1은 **절대 삭제하지 않음** (불변 원칙 유지)
- Major update 시 새 파일: `YYYY-MM-DD-{title}-v2.md`
- 새 파일의 frontmatter에 `supersedes: "[[원본 파일]]"` 프로퍼티 추가
- 원본 파일의 frontmatter에 `superseded-by: "[[새 파일]]"` 프로퍼티 추가
- Wiki 페이지의 `source` 프로퍼티에 최신 버전 추가 (기존 참조도 유지)

### 5. Verify (단일 페이지 검증, v5)

`/verify {page}` — 한 Wiki 페이지를 3 기준 (지식요건해당성·정합성·확증가능성) 에 대해 검증.

**Entrypoints**:
- Codex command: `.codex/commands/verify.md`
- Codex skill trigger: `.agents/skills/verify/SKILL.md`
- Claude mirror: `.claude/commands/verify.md`

**규칙**:
- `verificationStatus`, `verifiedAt`, `verifiedBy`, `claimType`, `evidenceScope`, `disputed` 를 기록한다.
- source-backed 검증 없이 `explored: true` 로 바꾸지 않는다. 사용자의 명시 확인이 필요하다.
- 충돌은 삭제하지 않고 `disputed: true` + `> [!warning] Disputed Claim` 으로 보존한다.
- `confidence` 는 source count, source type, counter-evidence 를 기준으로 독립 재산정한다.

### 6. Audit (전체 볼트 검증, v5)

`/audit` — vault 전체를 3 기준으로 점검. 모든 페이지 개별 검증이 아니라 **drift pattern 발견 + 우선순위 큐 생성** 이 목표.

**Entrypoints**:
- Codex command: `.codex/commands/audit.md`
- Codex skill trigger: `.agents/skills/audit/SKILL.md`
- Claude mirror: `.claude/commands/audit.md`

**규칙**:
- `/audit` 은 Wiki page 를 직접 수정하지 않는 read-only planning operation 이다.
- MOC cluster 단위 consistency, high-confidence / stale unexplored / disputed page sampling 을 수행한다.
- 결과가 substantial 하면 `30. Queries/YYYY-MM-DD-Q-vault-audit.md` 로 저장하고 `log.md` 에 기록한다.
- Top 10 `/verify` queue 를 출력한다.

---

## Folder Structure

```
CMDS_LLM_Wiki/
├── .obsidian/              # Obsidian 설정
├── .codex/                 # Codex command + hook harness
│   ├── commands/           # Codex operation entrypoints
│   └── hooks/              # Raw Source validation + qmd reindex hooks
├── .agents/skills/         # Codex reusable operation skills
├── .claude/                # Claude Code commands/hooks mirror
├── AGENTS.md               # Schema (이 파일)
├── index.md                # 마스터 인덱스
├── log.md                  # 변경 이력
├── 00. Inbox/              # 새 자료 임시 저장 (Web Clipper 대상)
│   ├── 01. Articles/       # 웹 기사, 블로그
│   ├── 02. Papers/         # 학술 논문, 기술 보고서
│   ├── 03. Transcripts/    # 강연, 팟캐스트, 영상 전사
│   ├── 04. Clippings/      # 짧은 스니펫, 발췌
│   └── 05. AI Research/    # ChatGPT/Gemini/Grok/Claude/Perplexity 선행 조사 묶음
├── 10. Raw Sources/        # Layer 1: 불변 원본
│   ├── 11. Articles/
│   ├── 12. Papers/
│   ├── 13. Books/
│   ├── 14. Transcripts/
│   ├── 15. Clippings/
│   └── 16. AI Research/
├── 20. Wiki/               # Layer 2: LLM 관리 위키
│   ├── 21. Concepts/
│   ├── 22. Entities/
│   ├── 23. Guides/
│   ├── 24. Maps/
│   └── 25. Questions/      # Research Question 카드 (RQ-{slug}.md)
├── 30. Queries/            # 합성된 질의 결과 (+ synthesis)
├── 40. Paper Analyses/     # 논문별 12단 분석 (folder = {citekey}/) — 허브 S00 + 원자 S02~S12 (v6.2)
├── 70. Outputs/            # (옵션) 외부 도구 산출물 (Layer 4: tool outputs)
│   ├── graphify/           # /graphify 결과 — YYYY-MM-DD-{topic}/ 단위
│   ├── …/                  # 향후 다른 도구도 같은 패턴
│   └── .tool-state/        # cross-run 캐시·manifest (gitignore 가능)
├── 80. References/         # 첨부 파일
│   └── Attachments/
└── 90. Settings/           # 템플릿, 설정, 스크립트
    ├── Templates/          # 노트 템플릿 11종 + 12-Step Analysis Schemes
    └── Scripts/            # p7_verify.py (Paper Mode P-7 게이트)
```

### `70. Outputs/` 규칙 (Tool Output Convention, 옵션)

외부 도구 (graphify, audio-transcriber 등) 가 생성하는 부산물은 Wiki 본체와 격리되어야 한다. Karpathy 패턴에서 Wiki 는 *컴파일 결과물* 이지만, 도구 산출물은 *분석 결과* — 둘은 라이프사이클이 다르다. 해당 도구를 쓰지 않으면 이 폴더 자체를 만들지 않아도 됨.

**경로 패턴**: `70. Outputs/{tool-name}/{YYYY-MM-DD}-{topic-slug}/`
- 예: `70. Outputs/graphify/2026-04-30-knowledge-graph/`
- 예: `70. Outputs/audio-transcriber/2026-05-12-meeting-notes/`

**규칙**:
- 한 번의 실행 = 한 개의 dated 폴더 (덮어쓰지 않음, 비교 가능)
- 입력 스냅샷이 있으면 `_corpus/` 또는 `_input/` 서브폴더로 보존 (재현성)
- Cross-run 상태 (캐시, manifest) 는 `70. Outputs/.tool-state/{tool-name}/` 로 분리
- 결과물에서 발견한 인사이트는 `30. Queries/` 에 별도 노트로 정제 (output != insight)
- Wiki 본체 (10/20/30/80) 에서 outputs 를 직접 wikilink 하지 않음 — 발견을 정제해 Wiki 페이지로 흡수하거나, Query 결과로 인용
- Outputs 자체는 LLM 의 schema 규칙 (필수 7 프로퍼티, naming convention) 적용 면제 — 도구가 자기 형식으로 생성

---

## Frontmatter Standards

### 필수 프로퍼티 (7개)

모든 .md 파일에 반드시 포함:

| Property | Type | Description |
|----------|------|-------------|
| `type` | text | 노트 유형: `documentation`, `raw-source`, `wiki-page`, `research-question` (v6.1), `query-result`, `synthesis` (v6.1), `moc`, `inbox` (capture 단계 pre-ingest), `paper-hub` (v6.2 — 논문 허브), `paper-analysis` (v6.2 — 논문 원자), `log` |
| `aliases` | list | 대체 이름 |
| `description` | text | English, 1-2 sentences for LLMs — **값은 항상 큰따옴표** (`description: "..."`) |
| `author` | list | 작성자 (LLM인 경우 `Claude` / `Codex` / `Grok`) |
| `date created` | datetime | ISO 8601 |
| `date modified` | datetime | ISO 8601 |
| `tags` | list | 관련 태그 |

### Provenance 프로퍼티 (v6 신설 — 항상 기록)

에이전트가 생성·갱신하는 모든 콘텐츠 페이지(raw-source·wiki-page·research-question·query-result·synthesis·moc·inbox·paper-hub·paper-analysis) frontmatter 는 `author` 바로 뒤에 아래 2 키를 **항상** 포함한다. 목적: Claude Code·Codex·Grok 어떤 에이전트가 읽어도 "누가(role) · 어떤 모델(id) · 어떤 강도(effort)로 썼는가" 를 즉시 확인 — cross-agent provenance.

- `author`: **(기존 필수)** 역할/작성자 — `Claude` / `Codex` / `Grok` / `"[[{your-name}]]"` (사람).
- `model`: **(v6 신설)** 상세 모델 id. 예: `claude-opus-4-8`, `claude-sonnet-5`, `gpt-5.4-codex` (Codex), `grok-4` (Grok). 여러 모델 기여 시 list.
- `effort`: **(v6 신설)** 작성 시점의 추론 강도·모드. `low` / `medium` / `high` / `xhigh` / `max` 또는 타 에이전트 등가. 미상은 `default`.

```yaml
author:
  - Claude
model: claude-opus-4-8
effort: high
```

harness 정의 파일(`.claude/commands/*`, `.codex/commands/*`, `.agents/skills/*`)의 **자기 frontmatter 에는 provenance 를 넣지 않는다** (슬래시 커맨드/스킬 파서 혼선 방지) — Description Rule(큰따옴표)만 적용.

### Layer별 추가 프로퍼티

**Raw Source** (`type: raw-source`):
- `source`: 원본 URL 또는 참조
- `date ingested`: 인제스트 일시 (Book Ingest stub 의 경우 scaffold 날짜)
- `category`: Articles / Papers / Books / Transcripts / Clippings / AI Research
- `status`: **(v2 신설)** `ingested` (기본) / `stub` (Book Ingest 미독서) / `reading` (독서 중) / `completed` (독서 완료 + Wiki 컴파일 완료). 표준 ingest 는 `ingested` 만 사용.
- `collectionPurpose`: **(필수, v2 신설)** 사용자가 명시한 수집 목적 — 미래의 나에게 보내는 편지. 7 재활용 축 중 하나 이상. 예: `"PhD 연구 — AI readiness 측정 도구"`, `"컨설팅 deliverable — 기업 임원교육 사례"`
- `mainVaultRelated`: **(v2 신설)** ingest 시 메인 볼트에서 검색된 유사 노트 2~5개 — `[노트명](obsidian://open?vault=...)` 클릭 가능 링크 (ingest Step 0-a 에서 stat 검증한 값만 사용)
- `mainVaultCmds`: **(v2 신설)** 관련 CMDS 카테고리 — `"[[📚 601 Knowledge Management]]"` quoted wikilink (메인 볼트 기준이므로 이 볼트에서는 resolve 안 되지만 메타데이터로 보존)

**Book Ingest 전용 키** (Raw Source chapter stub, `status: stub`):
- `bookIndex`: **(v3 신설)** 소속 책의 Book Index — `"[[YYYY-MM-DD-{authorSlug}-{bookSlug}-book-index]]"` quoted wikilink
- `chapterNumber`: **(v3 신설)** 챕터 번호 (정수, TOC 기준)
- `chapterPart`: **(v3 신설)** 챕터가 속한 편/파트 이름 — 원문 언어 보존 (예: `"Part I"`, `"第一篇"`)
- `chapterPrev`, `chapterNext`: **(v3 신설)** 이전·다음 챕터 wikilink, null 가능

**Wiki Page** (`type: wiki-page`):
- `source`: 참조한 Raw Source 링크 목록
- `related`: 관련 Wiki 페이지 링크
- `confidence`: high / medium / low (정보 신뢰도)
- `layer`: concepts / entities / guides / theory / method / scale (theory/method/scale = v6.2, 논문 승격 재사용 단위 — `21. Concepts` 내 layer 태그로 구분, 별도 폴더 없음. scale 페이지는 `measuredConstruct`·`itemCount` + `Template_Scale Page`)
- `mainVaultRelated`: **(v2 신설)** 메인 볼트의 관련 에세이·MOC — `[노트명](obsidian://open?vault=...)` 클릭 가능 링크
- `mainVaultCmds`: **(v2 신설)** 연결될 CMDS 카테고리
- `explored`: **(v4 신설)** Exploration Gate 상태. 새 Wiki 페이지 기본값은 `false`. 사용자가 직접 읽었거나 에이전트가 별도 검증 루프를 수행한 뒤에만 `true`.
- `exploredBy`: **(v4 선택)** `explored: true` 로 바꾼 사람 또는 에이전트 이름
- `exploredDate`: **(v4 선택)** Exploration Gate 완료일 (`YYYY-MM-DD`)
- `claimType`: **(v5 신설)** 페이지의 지배적 claim 유형 — `definition` / `empirical` / `theoretical` / `historical` / `prescriptive` / `interpretive` / `mixed`. `/verify` 가 분류·기록.
- `evidenceScope`: **(v5 신설)** 증거 범위 — `single-source` / `multi-source-primary` / `multi-source-mixed` / `synthesis-only` / `user-original`. `/verify` 가 분류·기록.
- `verificationStatus`: **(v5 신설)** 검증 상태 — `verified` (3 기준 모두 통과) / `partial` (일부 통과) / `unverified` (미검증, 기본값) / `disputed` (충돌 미해결). `/verify` 가 기록.
- `verifiedAt`: **(v5 선택)** 최종 `/verify` 실행일 (`YYYY-MM-DD`)
- `verifiedBy`: **(v5 선택)** `agent` / `human` / `both`
- `disputed`: **(v5 선택)** `true` 일 때 충돌하는 다른 Wiki 페이지와 양방향 `> [!warning] Disputed Claim` callout 으로 연결. `/verify` Phase 2.2 또는 `/audit` Phase B 가 기록. 삭제 대신 disputed 처리하는 것이 원칙.

**Query Result** (`type: query-result`):
- `query`: 원래 질문
- `source`: 참조한 Wiki 페이지
- `reusableFor`: **(v2 신설, 선택)** 7 재활용 축 중 어디에 쓰일지

**Synthesis** (`type: synthesis`, v6.1 신설 — 능동 논증층):
- `30. Queries/` 에 query-result 와 **같은 폴더**, `type` 으로만 구분 (폴더 분할 안 함 — 결정 근거 아래). Query 가 *반응형 답변* 이면 Synthesis 는 *능동적 논증 구성*: thesis statement + 근거 claim(각 인용) + 반론 + gap + 타깃 산출물.
- `thesis`: **(필수)** 이 합성이 방어하는 한 문장 주장
- `targetVenue`: 타깃 산출물·채널 (예: `"논문"`, `"책 챕터"`, `"블로그 시리즈"`, `"제품 결정 문서"`)
- `supports`: 근거가 되는 Wiki 페이지·Research Question `[[link]]` 목록
- `counters`: 반론·경쟁 가설 (본문 `> [!warning]` 로도 보존)
- `cites`: **(권장)** 인용 문헌 citekey 목록 — Citation Standard(옵션) 채택 시 `## References` 의 원천
- `reusableFor`: 7 재활용 축
- 공통 7 필수 + `## Thesis` / `## Argument` (claim + 근거) / `## Counter-arguments` / `## Gap` / (`## References`) 섹션.

> [!info] 폴더 결정 — `30. Queries/` 를 쪼개지 않는다
> Query 와 Synthesis 는 둘 다 "compiled wiki 를 발화한 산출물"(Karpathy: 좋은 답을 위키로 역피드백)의 두 flavor 다 — `type` 필드로 깔끔히 구분된다. Synthesis 가 대량 축적되면 그때 하위폴더로 분리 (파일명 기반 wikilink 라 이동은 저렴). **YAGNI — 지금은 flat + `type: synthesis`.**

**MOC** (`type: moc`):
- `topic`: 주제 영역
- `related`: 하위 MOC 또는 관련 MOC

**Research Question** (`type: research-question`, v6.1 신설 — 질문의 1급 객체화):
- 볼트의 5번째 Wiki 카드 타입. `20. Wiki/25. Questions/` 에 저장. 파일명 `RQ-{slug}.md`. in-page `> [!question] Open Question` 콜아웃을 **1급 카드로 승격** — 반복 등장하거나 산출물(논문·책·블로그 시리즈·제품 결정)로 이어질 질문을 first-class object 로 다뤄 답이 아니라 질문 자체를 추적한다.
- `status`: **(필수)** `open` / `investigating` / `answered` / `parked` / `superseded`
- `questionType`: **(필수)** `descriptive` / `causal` / `comparative` / `methodological` / `normative` / `design`
- `feedsInto`: **(필수)** 어느 산출물로 흘러가나 (예: `"논문 2장"`, `"블로그 시리즈 — AI 도입 가이드"`, `"제품 로드맵 결정"`)
- `evidenceFor` / `evidenceAgainst`: 지지·반대 증거 — `[[wiki page]]` (+ Citation Standard 채택 시 `[@citekey]`) 혼합
- `hypotheses`: 후보 답변 목록
- `cites`: **(권장)** 인용 문헌 citekey 목록 (Citation Standard 채택 시)
- `sourceCallout`: 이 질문이 승격돼 나온 원본 wiki 페이지 `[[link]]` (역추적)
- `related`: 관련 RQ·concept
- 공통 7 필수 + `explored`(기본 false). RQ 는 claim 이 아니라 질문이므로 v5 `claimType`/`verificationStatus` 대신 위 `status` 를 쓴다.

**Paper Hub** (`type: paper-hub`, v6.2 신설 — 논문 12단 분석 앵커):
- `paperType`: **(필수)** quantitative / qualitative / theory-concept / mixed-methods / scale-development / meta-analysis
- `citekey`: **(필수)** BetterBibTeX `authYearShorttitle` (Citation Standard). Raw Source·허브·원자 동일 토큰. Zotero 미사용 시 provisional citekey.
- `doi`: (선택) DOI 문자열
- `targetManuscript`: **(필수)** 이 논문이 기여할 Research Question — `"[[RQ-…]]"` quoted wikilink 또는 `none`
- `source`: 논문 Raw Source `"[[…]]"` · `collectionPurpose`: (v2 재사용) · `explored`/`verificationStatus`: v4/v5 그대로
- provenance(`model`/`effort`) 필수 (에이전트 작성 콘텐츠)

**Paper Analysis** (`type: paper-analysis`, v6.2 신설 — 12단 좌표를 가진 지식 원자):
- `paperType`: (필수) 허브와 동일값 (자기완결 + "모든 양적논문 S08" 필터)
- `analysisStep`: **(필수)** 정수 2~12 (S01 CITATION 은 항상 허브가 보유)
- `analysisStepName`: **(필수)** 유형별 정식 단계명 (`12-Step Analysis Schemes` verbatim)
- `paperHub`: **(필수)** `"[[{Surname} {Year} - S00 Hub]]"` quoted wikilink
- `citekey`: (필수) 허브와 동일 · `source`: Raw Source wikilink · `status`: completed / stub
- `claimType`/`evidenceScope` **면제** (단일 논문 요약은 퇴화) — 검증은 `p7_verify.py` 인용 충실도 검사로 대체
- provenance(`model`/`effort`) 필수

### 새 YAML 키는 camelCase

- ✅ `collectionPurpose`, `mainVaultRelated`, `mainVaultCmds`, `reusableFor`, `bookIndex`, `chapterNumber`, `chapterPart`, `chapterPrev`, `chapterNext`, `explored`, `exploredBy`, `exploredDate`, `claimType`, `evidenceScope`, `verificationStatus`, `verifiedAt`, `verifiedBy`, `disputed`, `model`, `effort`, `citekey`, `cites`, `questionType`, `feedsInto`, `evidenceFor`, `evidenceAgainst`, `sourceCallout`, `thesis`, `targetVenue`, `supports`, `counters`, `paperType`, `analysisStep`, `analysisStepName`, `paperHub`, `targetManuscript`, `doi`, `measuredConstruct`, `itemCount`
- ❌ `collection_purpose`, `main-vault-related`, `book_index`, `chapter-number`, `explored_by`, `claim_type`, `verification-status`, `cite_key`, `feeds_into` — camelCase 네이밍 컨벤션 위반

### Citation Standard (v6.1 — 옵션, Zotero-ready 인용 규약)

논문·책·리포트처럼 **엄밀한 인용이 필요한 산출물**을 목표로 하는 사용자를 위한 옵션 규약이다. 채택하지 않아도 볼트 운영에는 지장 없다 — Research Question / Synthesis 의 `cites` 는 이 규약 채택 시에만 채운다. 단, **Paper Ingest Mode (v6.2) 는 citekey 를 항상 사용**한다 — Zotero 미사용 시에도 provisional citekey 를 로컬 생성. 진리 원천은 **Zotero (BetterBibTeX)** 이며, Wiki 는 citekey 만 참조 → 나중에 Zotero `.bib` export 가 Pandoc/Obsidian 에서 formatted reference 로 자동 렌더.

- **Citekey 규약**: BetterBibTeX 표준 `authYearShorttitle` (예: `yang2024sweAgent`, `wu2024longMemEval`).
- **Inline citation**: **Pandoc/CSL 스타일 `[@citekey]`** (필요 시 `[@citekey, p. 12]`) — Zotero·Pandoc 네이티브라 export 시 자동 변환.
- **두 링크의 분리**: 내부 지식 참조는 `[[wikilink]]` ("우리가 컴파일한 X 지식 참조"), 외부 문헌 인용은 `[@citekey]` ("문헌 X 가 확립함"). 둘은 공존한다. 벤더/2차 소스가 아니라 **primary work** 를 citekey 로 가리킨다.
- **`cites:` frontmatter**: 카드가 인용한 citekey 목록. `## References` 의 원천.
- **`## References` 섹션**: 인용 문헌을 나열. Zotero 연동 전에는 수기 full citation (`- [@yang2024sweAgent] Yang et al. (2024). SWE-agent... NeurIPS 2024. arXiv:2405.15793`), 연동 후 Pandoc 이 자동 생성.
- **`citekey:` on Raw Source**: 어떤 raw source 가 특정 primary work 의 ingested 사본이면 그 raw source frontmatter 에 `citekey` 를 달아 `[[raw source]]`(읽은 사본) ↔ `[@citekey]`(정식 인용)를 이중 연결.

### Quality Control Properties (v4)

새 Wiki 페이지와 대형 업데이트는 다음 규칙을 따른다:

- 새 `type: wiki-page` 는 반드시 `explored: false` 를 갖는다.
- `explored: true` 는 사람이 읽었거나, 별도 검증 루프에서 source-backed review 를 끝낸 뒤에만 사용한다.
- `confidence: high` 로 올리는 페이지는 반대해석 또는 데이터 공백을 최소 1 줄 기록한다 (Bias Check 콜아웃).
- `/lint` 는 `explored` 누락, `explored: false` backlog, high-confidence 페이지의 bias check 누락을 보고한다.

### Verification Properties (v5)

v4 Exploration Gate 가 "누가 읽었나"만 추적하던 한계를 보완 — claim 단위 정합성·확증가능성을 형식화. 다음 3 기준으로 모든 Wiki 페이지가 평가될 수 있어야 한다:

1. **지식요건해당성 (Eligibility)** — 주어·술어·객체·출처·증거 범위·Claim type 의 6 요소를 갖춘 형식적 지식 단위인가? `claimType` + `evidenceScope` 가 분류 가능해야 함.
2. **정합성 (Consistency)** — vs source / vs other Wiki pages / vs AGENTS.md policy / vs Core Context 4 frame 모두에서 충돌이 없는가? 충돌 시 양쪽 페이지에 `disputed: true` + `> [!warning] Disputed Claim` callout 으로 보존 — 삭제 금지.
3. **확증가능성 (Confirmability)** — 출처 수·종류·반대증거를 종합해 독립적으로 산출한 confidence 가 declared `confidence:` 와 일치하는가? Overclaim (high-conf + single source) / Underclaim (low-conf + multi-source) 모두 flag.

운영 규칙:

- 신규 `type: wiki-page` 의 기본값: `verificationStatus: unverified`, `claimType`/`evidenceScope` 분류 시도, `disputed: false` (또는 키 생략).
- `/verify {page}` 가 단일 페이지 3 기준 통과 후 `verificationStatus: verified` + `verifiedAt`/`verifiedBy` 기록.
- `/audit` 가 MOC cluster 단위 consistency + sampling 기반 confirmability 로 vault 전체 점수 산출 → Top 10 `/verify` 큐 생성.
- 충돌은 항상 disputed 처리. `/verify --resolve` 만이 disputed → verified 또는 한쪽 confidence 강등 가능.
- `/query` 는 인용 시 `verificationStatus` + `confidence` 를 함께 읽고, `verified` + `high` 면 단언, `partial` 또는 `medium` 이하면 hedge, `disputed` 면 양쪽 명시 후 답변.

---

## Images & Attachments Policy

**모든 이미지·첨부파일은 `80. References/Attachments/` 로 일원화**. Raw Sources · Wiki · Queries 하위에 이미지 폴더를 만들지 않음.

- Obsidian 설정: `Settings → Files & Links → Default location for new attachments` = `80. References/Attachments/`
- Web Clipper 가 이미지를 CDN URL 로 남겨도 OK — URL 은 원본의 일부이므로 Raw Source body 에서 그대로 보존 (`validate-raw-source.sh` hook 이 verbatim 강제)
- 로컬로 저장해야 하는 이미지 (스크린샷, 사용자 업로드) 는 모두 `80. References/Attachments/YYYY-MM-DD-{description}.{ext}` 포맷
- Wiki 페이지에서 임베드: `![[{filename}]]` (Obsidian 단축 경로)

---

## File Naming Convention

| Layer | Pattern | Example |
|-------|---------|---------|
| Raw Source | `YYYY-MM-DD-{title}.md` | `2026-04-10-Attention-Is-All-You-Need.md` |
| Raw Source — Book Index | `YYYY-MM-DD-{authorSlug}-{bookSlug}-book-index.md` | `2026-04-20-author-slug-book-slug-book-index.md` |
| Raw Source — Book Chapter Stub | `YYYY-MM-DD-{authorSlug}-{bookSlug}-ch{NN}-{slug}.md` | `2026-04-20-author-slug-book-slug-ch03-agent-loop.md` |
| Wiki Page | `{Topic Name}.md` | `Transformer.md`, `Andrej Karpathy.md` |
| **Wiki Page — CJK Person Entity** | **네이티브 스크립트만 (한글·한자·일본어)** · 영문 이름은 aliases | `홍길동.md` (alias: `Gildong Hong`), `张汉东.md` (alias: `Zhang Handong`) |
| Wiki Page — Latin Person / Handle | 원어 표기 그대로 | `Andrej Karpathy.md`, `kepano (Steph Ango).md` (핸들 + 실명) |
| Query Result | `YYYY-MM-DD-Q-{question}.md` | `2026-04-10-Q-How-does-RLHF-work.md` |
| MOC | `MOC-{Topic}.md` | `MOC-Large Language Models.md` |
| Research Question | `RQ-{slug}.md` (`20. Wiki/25. Questions/`) | `RQ-agent-memory-architecture.md` |
| Paper Analysis 폴더 | `40. Paper Analyses/{citekey}/` | `40. Paper Analyses/wu2024longMemEval/` |
| Paper Hub | `{Surname} {Year} - S00 Hub.md` | `Wu 2024 - S00 Hub.md` |
| Paper 원자 | `{Surname} {Year} - S{NN} {세부주제}.md` | `Wu 2024 - S08 평가 지표 분석.md` |
| Log | `log.md` (단일 파일) | — |

### CJK Person Naming Rule

한국어·중국어·일본어 이름의 인물 entity 는 **네이티브 스크립트로만** 파일명을 짓고, 영문 로마자 표기는 `aliases` 프로퍼티에 둔다:

```yaml
# 20. Wiki/22. Entities/홍길동.md
---
type: wiki-page
aliases:
  - Gildong Hong
  - 홍길동
  - johndoe   # 핸들도 alias
---
```

**이유**: (1) 파일명 중복 (`홍길동 (Gildong Hong)`) 은 wikilink 작성 시 인지 부담 증가, (2) 영문 표기는 transliteration 일 뿐 고유 이름이 아니므로 aliases 위치가 맞다, (3) Obsidian graph/검색은 aliases 를 인식하므로 접근성에 손실 없음.

**적용 대상**: 한국인·중국인·일본인 등 CJK 이름을 가진 person entity. **제외**: 영문 핸들 + 실명 조합 (`kepano (Steph Ango)`), 책·제품 등 non-person entity.

---

## Callout Conventions

```markdown
> [!info] Source
> 출처 또는 참조 정보

> [!warning] Contradiction
> 모순되는 정보 플래그

> [!warning] Disputed Claim
> (v5) 다른 Wiki 페이지와 충돌하는 claim. 양쪽 페이지에 `disputed: true` + 상호 링크로 보존 (삭제 금지). `/verify --resolve` 만이 해소.

> [!question] Open Question
> 아직 해결되지 않은 질문

> [!tip] Key Insight
> 핵심 인사이트 강조

> [!note] Update
> 최근 업데이트 내용

> [!note] Bias Check
> Counter-argument: 가능한 반대해석 또는 과잉일반화 위험
> Data gap: 추가 source, 실제 사용 사례, 수치 검증 등 아직 비어 있는 근거

> [!check] Exploration Gate
> Status: explored / unexplored / needs-review
> Evidence: 사용자가 읽은 근거 또는 에이전트 검증 요약

> [!info] Analysis Context
> (v6.2) Paper Analysis 원자의 자기완결 계약 — H1 직후 4행 (Paper / 수집맥락 / 위치 Step N/12 / 이 원자+인접).

> [!quote] 원문 (p.12, §4.2)
> (v6.2) Paper Analysis 인용 규율 — Raw Source `## Original Content` 에서 verbatim (grep 대조). 페이지 우선 locator (Zotero PDF 로 복구), 없으면 §섹션. 요약을 quote 안에 넣지 않음.
```

---

## Cross-Vault Reference

(옵션) 이 볼트를 별도 mothership PKM 볼트의 **satellite** 로 운영할 수 있다. 그럴 경우 양방향 참조 규약:

### Vault Registry (채워서 사용)

| 역할 | 볼트 | 경로 |
|------|------|------|
| Mothership | `{your-mothership-vault-name}` | `{PATH_TO_YOUR_MOTHERSHIP_VAULT}` |
| Satellite (this) | `{your-llm-wiki}` | `{PATH_TO_YOUR_LLM_WIKI}` |

### 메인 볼트 참조하기 (위성 → 모선)

Obsidian은 볼트 간 직접 wikilink 불가. 다음 조합 사용:

**Frontmatter**:

```yaml
source-vault: {your-mothership-vault-name}
```

**Markdown body**:

```markdown
→ {your-mothership-vault-name}: 00. Inbox/{capture-lane}/2026-04-06-llm-wiki-karpathy.md
→ {your-mothership-vault-name}: 30. Permanent Notes/{essay-folder}/📜 예시 에세이...
```

### 메인 볼트에서 이 볼트 참조하기 (모선 → 위성)

메인 볼트에 **진입점 노트**를 만들어 두면 편리합니다 (예시 경로):

- `{your-mothership-vault-name}/40. Docs/🛰 CMDS_LLM_Wiki Satellite Vault.md`

메인 볼트 노트는 이 진입점을 `[[🛰 CMDS_LLM_Wiki Satellite Vault]]`로 wikilink하고, 구체적 page는 텍스트 참조:

```markdown
→ LLM Wiki: LLM Wiki Pattern (Concepts)
→ LLM Wiki: MOC-Knowledge Management
```

### Graph view 한계

Obsidian Graph view는 볼트 내부만 시각화. Cross-vault 연결은 frontmatter property로만 인식 가능하며, 사람이 눈으로 읽는 메타데이터로 기능합니다.

---

## Git Integration

이 볼트는 Git으로 버전 관리합니다:

- 모든 Wiki 변경사항은 commit으로 추적
- Ingest 시 commit message: `ingest: {source title}`
- Wiki 업데이트 시: `update: {page name} — {변경 요약}`
- Lint 수정 시: `lint: {수정 내용}`
