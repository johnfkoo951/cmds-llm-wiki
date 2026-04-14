---
type: documentation
aliases:
  - LLM Wiki Schema
  - Wiki Harness
description: Schema and harness document for the CMDS LLM Wiki vault. Defines the 3-layer architecture (Raw Sources / Wiki / Schema), ingest-query-lint operations, file conventions, and frontmatter standards. This is the single source of truth for LLM behavior in this vault.
author:
  - "[[{your-name}]]"
date created: 2026-04-10T21:30
date modified: 2026-04-10T21:30
tags:
  - system
  - schema
  - llm-wiki
status: active
version: "1.0"
---

# CLAUDE.md — LLM Wiki Schema

This file is the **Schema Layer** of the CMDS LLM Wiki. It governs how LLMs (Claude Code, Cursor, etc.) read, write, and maintain this vault.

> **Architecture**: Karpathy LLM Wiki Pattern
> - Raw Sources = 소스코드 (immutable)
> - Wiki = 실행 파일 (LLM이 관리)
> - Schema = 이 문서 (CLAUDE.md)

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
> 5. **Operations**: Ingest → Query → Lint
> 6. **필수 프로퍼티 7개**: type, aliases, description (English), author, date created, date modified, tags
> 7. **Core Context 먼저 읽기**: 모든 operation 전에 [[Core Context]] 로 사용자 목적·철학 정렬
> 8. **Gold In Gold Out**: `/ingest` 는 반드시 수집 목적 1회 질문 → `collectionPurpose` 프로퍼티에 기록

---

## 🧭 Core Context (반드시 먼저 로드)

**모든 ingest / query / lint 전에 [[Core Context]] 를 먼저 읽는다.**

해당 노트는 (1) 사용자의 정체성·7 재활용 축·철학 + (2) **옵션**: 별도 mothership 볼트가 있다면 그 시스템 파일 snapshot 을 담는다. 이 맥락 없이는 LLM Wiki 의 모든 operation 이 "목적 없는 자동 정리" 로 전락한다.

### (옵션) Mothership 볼트가 있는 경우

별도의 mothership Obsidian 볼트를 운영하고 있다면 (예: CMDSPACE 같은 개인 PKM 볼트), 그 시스템 파일들을 Core Context 의 "동적 참조" 섹션에 등록한다. mothership pattern 예시는 [cmds-system-files](https://github.com/johnfkoo951/cmds-system-files) 참고.

mothership 이 없다면 이 LLM Wiki 단독으로 운영한다 — Core Context §5 는 비워두거나 삭제.

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

Mothership pattern 예시: [cmds-system-files](https://github.com/johnfkoo951/cmds-system-files) (Karpathy Wiki pattern 과 분리된 PKM harness).

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
└── 15. Clippings/    # 웹 클리핑, 스크랩
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

### 1. Ingest (새 자료 흡수)

새 source가 `00. Inbox/`에 들어오면:

0. **🎯 목적 질문 (Gold In Gold Out)**: LLM은 사용자에게 **단일 질문** 을 던진다 — "이 소스를 왜 수집했나요? (7 재활용 축: PhD / 학술 / 강의 / 컨설팅 / CMDS 시스템 / 에세이 / 제품 중 어디에 쓰일 예정인가요?)". 답변 없이 ingest 하지 않음. 답변은 `collectionPurpose` 프로퍼티에 기록.
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

---

## Folder Structure

```
CMDS_LLM_Wiki/
├── .obsidian/              # Obsidian 설정
├── CLAUDE.md               # Schema (이 파일)
├── index.md                # 마스터 인덱스
├── log.md                  # 변경 이력
├── 00. Inbox/              # 새 자료 임시 저장 (Web Clipper 대상)
│   ├── 01. Articles/       # 웹 기사, 블로그
│   ├── 02. Papers/         # 학술 논문, 기술 보고서
│   ├── 03. Transcripts/    # 강연, 팟캐스트, 영상 전사
│   └── 04. Clippings/      # 짧은 스니펫, 발췌
├── 10. Raw Sources/        # Layer 1: 불변 원본
│   ├── 11. Articles/
│   ├── 12. Papers/
│   ├── 13. Books/
│   ├── 14. Transcripts/
│   └── 15. Clippings/
├── 20. Wiki/               # Layer 2: LLM 관리 위키
│   ├── 21. Concepts/
│   ├── 22. Entities/
│   ├── 23. Guides/
│   └── 24. Maps/
├── 30. Queries/            # 합성된 질의 결과
├── 80. References/         # 첨부 파일
│   └── Attachments/
└── 90. Settings/           # 템플릿, 설정
    └── Templates/
```

---

## Frontmatter Standards

### 필수 프로퍼티 (7개)

모든 .md 파일에 반드시 포함:

| Property | Type | Description |
|----------|------|-------------|
| `type` | text | 노트 유형: `raw-source`, `wiki-page`, `query-result`, `moc`, `log` |
| `aliases` | list | 대체 이름 |
| `description` | text | English, 1-2 sentences for LLMs |
| `author` | list | 작성자 (LLM인 경우 `Claude`) |
| `date created` | datetime | ISO 8601 |
| `date modified` | datetime | ISO 8601 |
| `tags` | list | 관련 태그 |

### Layer별 추가 프로퍼티

**Raw Source** (`type: raw-source`):
- `source`: 원본 URL 또는 참조
- `date ingested`: 인제스트 일시
- `category`: Articles / Papers / Books / Transcripts / Clippings
- `collectionPurpose`: **(필수, v2 신설)** 사용자가 명시한 수집 목적 — Gold In Gold Out. 7 재활용 축 중 하나 이상. 예: `"PhD 연구 — AI readiness 측정 도구"`, `"컨설팅 deliverable — LG AX 임원교육 사례"`
- `mainVaultRelated`: **(v2 신설)** ingest 시 메인 볼트에서 검색된 유사 노트 2~5개 — `→ CMDSPACE: {path}` 텍스트 참조 형태의 리스트
- `mainVaultCmds`: **(v2 신설)** 관련 CMDS 카테고리 — `"[[📚 601 Knowledge Management]]"` quoted wikilink (메인 볼트 기준이므로 이 볼트에서는 resolve 안 되지만 메타데이터로 보존)

**Wiki Page** (`type: wiki-page`):
- `source`: 참조한 Raw Source 링크 목록
- `related`: 관련 Wiki 페이지 링크
- `confidence`: high / medium / low (정보 신뢰도)
- `layer`: concepts / entities / guides
- `mainVaultRelated`: **(v2 신설)** 메인 볼트의 관련 에세이·MOC — `→ CMDSPACE: {path}` 리스트
- `mainVaultCmds`: **(v2 신설)** 연결될 CMDS 카테고리

**Query Result** (`type: query-result`):
- `query`: 원래 질문
- `source`: 참조한 Wiki 페이지
- `reusableFor`: **(v2 신설, 선택)** 7 재활용 축 중 어디에 쓰일지

**MOC** (`type: moc`):
- `topic`: 주제 영역
- `related`: 하위 MOC 또는 관련 MOC

### 새 YAML 키는 camelCase (`@CMDS-Guide` 준수)

- ✅ `collectionPurpose`, `mainVaultRelated`, `mainVaultCmds`, `reusableFor`
- ❌ `collection_purpose`, `main-vault-related` — 메인 볼트의 camelCase 네이밍 컨벤션 위반

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
| Wiki Page | `{Topic Name}.md` | `Transformer.md`, `Andrej Karpathy.md` |
| Query Result | `YYYY-MM-DD-Q-{question}.md` | `2026-04-10-Q-How-does-RLHF-work.md` |
| MOC | `MOC-{Topic}.md` | `MOC-Large Language Models.md` |
| Log | `log.md` (단일 파일) | — |

---

## Callout Conventions

```markdown
> [!info] Source
> 출처 또는 참조 정보

> [!warning] Contradiction
> 모순되는 정보 플래그

> [!question] Open Question
> 아직 해결되지 않은 질문

> [!tip] Key Insight
> 핵심 인사이트 강조

> [!note] Update
> 최근 업데이트 내용
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
→ CMDSPACE: 00. Inbox/03. AI Agent/03-1. Claude Code (MBP)/2026-04-06-llm-wiki-karpathy.md
→ CMDSPACE: 30. Permanent Notes/33. Essay/📜 Schema는 Harness다...
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
