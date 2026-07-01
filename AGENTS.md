---
type: documentation
aliases:
  - LLM Wiki Schema
  - Wiki Harness
description: Schema and harness document for the CMDS LLM Wiki vault. Defines the 3-layer architecture (Raw Sources / Wiki / Schema), ingest-query-lint operations, file conventions, and frontmatter standards. This is the single source of truth for LLM behavior in this vault.
author:
  - "[[{your-name}]]"
date created: 2026-04-10T21:30
date modified: 2026-07-01
tags:
  - system
  - schema
  - llm-wiki
status: active
version: "1.7.0"
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
- [ ] `description` field present and in English
- [ ] File saved in correct layer folder

---

## Essential (Post-Compact)

> 컨텍스트 압축 후에도 반드시 기억:
> 1. **YAML: 2 SPACES** / **Body: TAB**
> 2. **Wikilinks in YAML: 큰따옴표** `"[[link]]"`
> 3. **Mermaid 라벨: 큰따옴표** `A["label"]` / `[/` 로 시작 금지
> 4. **3 Layers**: Raw Sources (immutable) → Wiki (LLM-maintained) → Schema (this file)
> 5. **Operations**: Capture Tabs → Inbox → Ingest → Query → Verify/Audit → Lint (+Status/Reindex/Refresh)
> 6. **필수 프로퍼티 7개**: type, aliases, description (English), author, date created, date modified, tags
> 7. **Core Context 먼저 읽기**: 모든 operation 전에 [[Core Context]] 로 사용자 목적·철학 정렬
> 8. **미래의 나에게 보내는 편지**: `/ingest` 는 반드시 수집 목적 1회 질문 → `collectionPurpose` 프로퍼티에 기록

---

## 🧭 Core Context (반드시 먼저 로드)

**모든 capture / inbox / ingest / query / lint 전에 [[Core Context]] 를 먼저 읽는다.**

해당 노트는 메인 볼트 `{your-mothership-vault-name}` 의 9 system files (precedence 1~9, 2026-05-22 기준 DESIGN.md 추가) + 핵심 에세이 5편에서 추출된 사용자 맥락 snapshot 이다. {your-name}의 정체성·철학·7 재활용 축·CMDS 9 categories 를 담고 있으며, 이 맥락 없이는 LLM Wiki 의 모든 operation 이 "목적 없는 자동 정리" 로 전락한다. 9 system files 전체 alias 표는 `CLAUDE.md` "Core Context" 섹션 또는 [[Core Context]] §8 참조.

### 메인 볼트 9 시스템 파일 (최신 원본 동적 참조, precedence 순)

6개 공개 (system.cmdspace.work 배포) + 3개 비공개 (vendor·product 전용).

| # | Alias | 경로 | 역할 | 공개 |
|:-:|-------|------|------|:----:|
| 1 | `@CMDS-CLAUDE` | `{your-mothership-vault-name}/CLAUDE.md` | HOW — Claude Code 기술 규칙 | 공개 |
| 2 | `@CMDS-AGENTS` | `{your-mothership-vault-name}/AGENTS.md` | HOW — 타 AI 에이전트 규칙 (Codex, Cursor, Windsurf) | 공개 |
| 3 | `@CMDS-Antigravity` | `{your-mothership-vault-name}/ANTIGRAVITY.md` | HOW — Google Gemini / Antigravity IDE 전용 | 비공개 |
| 4 | `@CMDS-Context` | `{your-mothership-vault-name}/CMDS.md` | WHY/WHAT — 시스템 철학·사용자 프로필 | 공개 |
| 5 | `@CMDS-Guide` | `{your-mothership-vault-name}/🏛 CMDS Guide.md` | STANDARDS — 7 프로퍼티·템플릿·camelCase | 공개 |
| 6 | `@CMDS-HQ` | `{your-mothership-vault-name}/🏛 CMDS Head Quarter.md` | WHERE — 91 카테고리 네비게이션 | 공개 |
| 7 | `@CMDS-Brain` | `{your-mothership-vault-name}/BRAIN.md` | PERSONA — {your-name} brain profile (Gobi 앱 entry) | 비공개 |
| 8 | `@CMDS-BrainPrompt` | `{your-mothership-vault-name}/BRAIN_PROMPT.md` | PERSONA — Agent Rules of Engagement | 비공개 |
| 9 | `@CMDS-DESIGN` | `{your-mothership-vault-name}/DESIGN.md` | VISUAL — v4.3 design constants · Anti-Slop · skill ↔ surface mapping | 공개 |

최신본 읽기: `Read("{PATH_TO_YOUR_MOTHERSHIP_VAULT}/{file}")` 또는 `mcp__qmd__query` (user-scope, cwd 무관).

[[Core Context]] 은 `snapshot_date` 기준. 30일 이상 오래되면 lint 가 flag → re-snapshot.

---

## Vault Overview

이 볼트는 **Karpathy LLM Wiki Pattern**을 구현한 LLM 전용 지식 베이스입니다.

- **목적**: LLM이 raw sources를 컴파일하여 persistent, structured wiki를 유지
- **철학**: RAG(매번 검색+합성)가 아닌, 한 번 컴파일된 위키가 compounding artifact로 성장
- **연결**: CMDSPACE 메인 볼트(`{your-mothership-vault-name}`)의 satellite vault

### 메인 볼트 연결

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
└── 24. Maps/         # MOC (Map of Content), 주제별 인덱스
```

**규칙**:
- 모든 페이지는 `type: wiki-page` frontmatter 사용
- 관련 Raw Source를 `source` 프로퍼티로 역참조
- 모든 주장에 출처 명시 (Wiki 내 링크 또는 Raw Source 참조)
- Cross-reference: 관련 개념은 반드시 `[[wikilink]]`로 연결
- 모순 발견 시 `> [!warning] Contradiction` callout으로 플래그
- To-do/미해결 항목은 `> [!question] Open Question` callout 사용

### Layer 3: Schema (이 파일)

**규칙층** — LLM의 행동을 제어하는 harness 문서.

---

## Operations

> **🤖 Agent Note (Codex & Antigravity)**:
> Codex 의 operation entrypoint 는 `.codex/commands/{operation}.md` 이다. 재사용 가능한 Codex skills 는 `.agents/skills/{operation}/SKILL.md` 처럼 직관적인 operation 이름을 사용한다 (`ingest`, `query`, `capture-tabs`, `status` 등). Antigravity(Gemini) 등 타 에이전트 역시 해당 operation을 수행하기 전에 대응 command 파일을 읽고 그 절차를 엄격히 따라야 한다.
> Claude Code 전용 command 는 `.claude/commands/{operation}.md` 에 보존한다. 같은 operation 은 양쪽 harness 에 같은 이름으로 둔다. Codex 작업에서는 `AGENTS.md` + `.codex/commands/` + 필요한 `.agents/skills/{operation}/SKILL.md` 가 우선이다.

### Codex Compatibility Matrix (v1.3)

Codex 에서 가능한 작업은 아래 10개 operation 으로 표준화한다. 새 operation 을 추가할 때는 **반드시** `.codex/commands/{name}.md`, `.agents/skills/{name}/SKILL.md`, 필요 시 `.claude/commands/{name}.md` mirror 를 함께 맞춘다.

> [!warning] Parity Contract (CLAUDE.md ↔ AGENTS.md)
> 이 두 스키마는 같은 규칙의 미러다. 다음 섹션은 **양쪽이 동일해야** 하며 한쪽만 편집 금지: (1) Cross-Agent Compatibility Matrix, (2) Frontmatter Standards (7 필수 + v2/v3/v4/v5 키), (3) Verification Properties (v5) 3 기준, (4) Callout Conventions. 편집 시 CLAUDE.md 와 AGENTS.md 를 함께 고치고 `/lint` + parity 체크리스트로 확인. `.codex/`·`.agents/` 는 untracked 라 diff 에 안 보이므로 수동 대조가 필요하다.

| Operation | Codex command | Codex skill | Claude mirror | Status | Notes |
|-----------|---------------|-------------|---------------|--------|-------|
| Capture Tabs | `.codex/commands/capture-tabs.md` | `.agents/skills/capture-tabs/SKILL.md` | `.claude/commands/capture-tabs.md` | Active | AI research / browser tab bundle → Inbox |
| Inbox | `.codex/commands/inbox.md` | `.agents/skills/inbox/SKILL.md` | `.claude/commands/inbox.md` | Active | pending source preview + ingest routing |
| Ingest | `.codex/commands/ingest.md` | `.agents/skills/ingest/SKILL.md` | `.claude/commands/ingest.md` | Active | purpose gate + Raw Source + Wiki compile |
| Query | `.codex/commands/query.md` | `.agents/skills/query/SKILL.md` | `.claude/commands/query.md` | Active | compiled Wiki synthesis + Query Result |
| Lint | `.codex/commands/lint.md` | `.agents/skills/lint/SKILL.md` | `.claude/commands/lint.md` | Active | health check + frontmatter coverage |
| Status | `.codex/commands/status.md` | `.agents/skills/status/SKILL.md` | `.claude/commands/status.md` | Active | counts + coverage snapshot |
| Reindex | `.codex/commands/reindex.md` | `.agents/skills/reindex/SKILL.md` | `.claude/commands/reindex.md` | Active | qmd update/embed/status |
| Refresh Context | `.codex/commands/refresh-context.md` | `.agents/skills/refresh-context/SKILL.md` | `.claude/commands/refresh-context.md` | Active | Core Context from mothership system files |
| Verify | `.codex/commands/verify.md` | `.agents/skills/verify/SKILL.md` | `.claude/commands/verify.md` | Active | single-page verification |
| Audit | `.codex/commands/audit.md` | `.agents/skills/audit/SKILL.md` | `.claude/commands/audit.md` | Active | vault/MOC audit + `/verify` queue |

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

새 source가 `00. Inbox/`에 들어오면:

0. **🎯 목적 질문 (미래의 나에게 보내는 편지)**: LLM은 사용자에게 **단일 질문** 을 던진다 — "이 소스를 왜 수집했나요? (7 재활용 축: PhD / 학술 / 강의 / 컨설팅 / CMDS 시스템 / 에세이 / 제품 중 어디에 쓰일 예정인가요?)". 답변 없이 ingest 하지 않음. 답변은 `collectionPurpose` 프로퍼티에 기록.
0-a. **🔗 메인 볼트 연결 검색**: 사용자 답변을 받으면 **메인 볼트에서 유사 노트·개념을 검색** 한다 (`mcp__qmd__query` vec/hyde + `Grep` path=`/Users/.../{your-mothership-vault-name}`). 2~5개 후보를 `mainVaultRelated` 프로퍼티에 기록하고 사용자에게 확인.
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
│   └── 24. Maps/
├── 30. Queries/            # 합성된 질의 결과
├── 70. Outputs/            # 외부 도구 산출물 (Layer 4: tool outputs)
│   ├── graphify/           # /graphify 결과 — YYYY-MM-DD-{topic}/ 단위
│   ├── …/                  # 향후 다른 도구도 같은 패턴
│   └── .tool-state/        # cross-run 캐시·manifest (gitignore 가능)
├── 80. References/         # 첨부 파일
│   └── Attachments/
└── 90. Settings/           # 템플릿, 설정
    └── Templates/
```

### `70. Outputs/` 규칙 (Tool Output Convention)

외부 도구 (graphify, markdown-formatter 등) 가 생성하는 부산물은 Wiki 본체와 격리되어야 한다. Karpathy 패턴에서 Wiki 는 *컴파일 결과물* 이지만, 도구 산출물은 *분석 결과* — 둘은 라이프사이클이 다르다.

**경로 패턴**: `70. Outputs/{tool-name}/{YYYY-MM-DD}-{topic-slug}/`
- 예: `70. Outputs/graphify/2026-04-30-cmds-multivault/`
- 예: `70. Outputs/audio-transcriber/2026-05-12-meeting-notes/`

**규칙**:
- 한 번의 실행 = 한 개의 dated 폴더 (덮어쓰지 않음, 비교 가능)
- 입력 스냅샷이 있으면 `_corpus/` 또는 `_input/` 서브폴더로 보존 (재현성)
- Cross-run 상태 (캐시, manifest) 는 `70. Outputs/.tool-state/{tool-name}/` 로 분리
- 결과물에서 발견한 인사이트는 `30. Queries/` 에 별도 노트로 정제 (output != insight)
- Wiki 본체 (10/20/30/80) 에서 outputs 를 직접 wikilink 하지 않음 — 발견을 정제해 Wiki 페이지로 흡수하거나, Query 결과로 인용
- Outputs 자체는 LLM 의 schema 규칙 (필수 7 프로퍼티, naming convention) 적용 면제 — 도구가 자기 형식으로 생성

**현재 사용처**:
- `/graphify` → 자동으로 `70. Outputs/graphify/{date}-{topic}/` 에 저장 (skill 이 ensure)

---

## Frontmatter Standards

### 필수 프로퍼티 (7개)

모든 .md 파일에 반드시 포함:

| Property | Type | Description |
|----------|------|-------------|
| `type` | text | 노트 유형: `raw-source`, `wiki-page`, `query-result`, `moc`, `log` |
| `aliases` | list | 대체 이름 |
| `description` | text | English, 1-2 sentences for LLMs |
| `author` | list | 작성자 (LLM인 경우 `Codex`) |
| `date created` | datetime | ISO 8601 |
| `date modified` | datetime | ISO 8601 |
| `tags` | list | 관련 태그 |

### Layer별 추가 프로퍼티

**Raw Source** (`type: raw-source`):
- `source`: 원본 URL 또는 참조
- `date ingested`: 인제스트 일시 (Book Ingest stub 의 경우 scaffold 날짜)
- `category`: Articles / Papers / Books / Transcripts / Clippings / AI Research
- `status`: **(v2 신설)** `ingested` (기본) / `stub` (Book Ingest 미독서) / `reading` (독서 중) / `completed` (독서 완료 + Wiki 컴파일 완료). 표준 ingest 는 `ingested` 만 사용.
- `collectionPurpose`: **(필수, v2 신설)** 사용자가 명시한 수집 목적 — 미래의 나에게 보내는 편지. 7 재활용 축 중 하나 이상. 예: `"PhD 연구 — AI readiness 측정 도구"`, `"컨설팅 deliverable — 기업 임원교육 사례"`
- `mainVaultRelated`: **(v2 신설)** ingest 시 메인 볼트에서 검색된 유사 노트 2~5개 — `[노트명](obsidian://open?vault={your-mothership-vault-name}&file=URL_ENCODED_PATH)` 클릭 가능 링크
- `mainVaultCmds`: **(v2 신설)** 관련 CMDS 카테고리 — `"[[📚 601 Knowledge Management]]"` quoted wikilink (메인 볼트 기준이므로 이 볼트에서는 resolve 안 되지만 메타데이터로 보존)

**Book Ingest 전용 키** (Raw Source chapter stub, `status: stub`):
- `bookIndex`: **(v3 신설)** 소속 책의 Book Index — `"[[YYYY-MM-DD-{authorSlug}-{bookSlug}-book-index]]"` quoted wikilink
- `chapterNumber`: **(v3 신설)** 챕터 번호 (정수, TOC 기준)
- `chapterPart`: **(v3 신설)** 챕터가 속한 편/파트 이름 — 원문 언어 보존 (예: `"第一篇: 架构"`, `"Part II: Context Management"`)
- `chapterPrev`, `chapterNext`: **(v3 신설)** 이전·다음 챕터 wikilink, null 가능

**Wiki Page** (`type: wiki-page`):
- `source`: 참조한 Raw Source 링크 목록
- `related`: 관련 Wiki 페이지 링크
- `confidence`: high / medium / low (정보 신뢰도)
- `layer`: concepts / entities / guides
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

**MOC** (`type: moc`):
- `topic`: 주제 영역
- `related`: 하위 MOC 또는 관련 MOC

### 새 YAML 키는 camelCase (`@CMDS-Guide` 준수)

- ✅ `collectionPurpose`, `mainVaultRelated`, `mainVaultCmds`, `reusableFor`, `bookIndex`, `chapterNumber`, `chapterPart`, `chapterPrev`, `chapterNext`, `explored`, `exploredBy`, `exploredDate`, `claimType`, `evidenceScope`, `verificationStatus`, `verifiedAt`, `verifiedBy`, `disputed`
- ❌ `collection_purpose`, `main-vault-related`, `book_index`, `chapter-number`, `explored_by`, `claim_type`, `verification-status` — 메인 볼트의 camelCase 네이밍 컨벤션 위반

### Quality Control Properties (v4)

`2026-05-04` self-audit 에서 확인된 가장 큰 품질 갭은 Exploration Gate 0% 와 bias check 부재다. 따라서 새 Wiki 페이지와 대형 업데이트는 다음 규칙을 따른다:

- 새 `type: wiki-page` 는 반드시 `explored: false` 를 갖는다.
- `explored: true` 는 사람이 읽었거나, 별도 검증 루프에서 source-backed review 를 끝낸 뒤에만 사용한다.
- `confidence: high` 로 올리는 페이지는 반대해석 또는 데이터 공백을 최소 1 줄 기록한다.
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
```

---

## Cross-Vault Reference

이 볼트는 **{your-mothership-vault-name}의 satellite**입니다. 양방향 참조 규약을 명시합니다.

### Vault Registry

| 역할 | 볼트 | 경로 |
|------|------|------|
| Mothership | `{your-mothership-vault-name}` | `{PATH_TO_YOUR_MOTHERSHIP_VAULT}` |
| Satellite (this) | `CMDS_LLM_Wiki` | `{PATH_TO_YOUR_LLM_WIKI}` |

### 메인 볼트 참조하기 (위성 → 모선)

Obsidian은 볼트 간 직접 wikilink 불가. 다음 조합 사용:

**Frontmatter**:

```yaml
source-vault: {your-mothership-vault-name}
```

**Markdown body**:

```markdown
[2026-04-06-llm-wiki-karpathy](obsidian://open?vault={your-mothership-vault-name}&file=00.%20Inbox%2F03.%20AI%20Agent%2F03-1.%20Claude%20Code%20%28MBP%29%2F2026-04-06-llm-wiki-karpathy)
[📜 Schema는 Harness다 - Karpathy LLM Wiki와 CMDS의 구조적 동치에 관한 보고서](obsidian://open?vault={your-mothership-vault-name}&file=30.%20Permanent%20Notes/33.%20Essay/%F0%9F%93%9C%20Schema%EB%8A%94%20Harness%EB%8B%A4%20-%20Karpathy%20LLM%20Wiki%EC%99%80%20CMDS%EC%9D%98%20%EA%B5%AC%EC%A1%B0%EC%A0%81%20%EB%8F%99%EC%B9%98%EC%97%90%20%EA%B4%80%ED%95%9C%20%EB%B3%B4%EA%B3%A0%EC%84%9C)
```

### 메인 볼트에서 이 볼트 참조하기 (모선 → 위성)

메인 볼트에 **진입점 노트**가 있습니다:

- `CMDSPACE/40. Docs/47. CMDS Docs/🛰 CMDS_LLM_Wiki Satellite Vault.md`

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
