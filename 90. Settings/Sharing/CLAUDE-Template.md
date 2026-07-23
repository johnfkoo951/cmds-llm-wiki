# CLAUDE.md — LLM Wiki Schema

This file is the **Schema Layer** of this LLM Wiki vault. It governs how LLMs (Claude Code, Cursor, etc.) read, write, and maintain this vault.

> **Architecture**: Karpathy LLM Wiki Pattern
> - Raw Sources = 원본 자료 (immutable)
> - Wiki = LLM이 관리하는 지식 페이지
> - Schema = 이 문서 (CLAUDE.md)

---

## CRITICAL RULES

### Indentation Rules
- **YAML frontmatter**: 2 SPACES (절대 탭 금지)
- **Markdown body**: TAB (절대 스페이스 금지)

### Wikilink Rules
- YAML 내 wikilinks는 반드시 큰따옴표: `"[[link]]"`
- Markdown body에서는 따옴표 없이: `[[link]]`

### Pre-Flight Checklist (Before Every Write/Edit)
- [ ] YAML frontmatter uses 2 SPACES
- [ ] Markdown body uses TAB
- [ ] Wikilinks in YAML are quoted: `"[[link]]"`
- [ ] Arrays use proper format: `- value`
- [ ] Dates use ISO 8601: `YYYY-MM-DD`
- [ ] `description` field present and in English
- [ ] File saved in correct layer folder

---

## Essential (Post-Compact)

> 컨텍스트 압축 후에도 반드시 기억:
> 1. **YAML: 2 SPACES** / **Body: TAB**
> 2. **Wikilinks in YAML: 큰따옴표** `"[[link]]"`
> 3. **3 Layers**: Raw Sources (immutable) → Wiki (LLM-maintained) → Schema (this file)
> 4. **Operations**: Ingest → Query → Lint
> 5. **필수 프로퍼티 7개**: type, aliases, description (English), author, date created, date modified, tags

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
├── 21. Concepts/     # 추상 개념
├── 22. Entities/     # 사람, 조직, 제품
├── 23. Guides/       # How-to, 튜토리얼
├── 24. Maps/         # MOC (Map of Content)
└── 25. Questions/    # Research Question 카드 (RQ-{slug}.md)
```

**규칙**:
- `21~24` 페이지는 `type: wiki-page`, `25. Questions` 카드는 `type: research-question` frontmatter 사용
- 관련 Raw Source를 `source` 프로퍼티로 역참조
- 모든 주장에 출처 명시 (Wiki 내 링크 또는 Raw Source 참조)
- Cross-reference: 관련 개념은 반드시 `[[wikilink]]`로 연결
- 모순 발견 시 `> [!warning] Contradiction` callout으로 플래그
- 미해결 항목은 `> [!question] Open Question` callout 사용

### Layer 3: Schema (이 파일)

**규칙층** — LLM의 행동을 제어하는 harness 문서.

---

## Operations

### 1. Ingest (새 자료 흡수)

새 source가 들어오면:

1. **분석**: source의 핵심 주제, 엔티티, 개념 추출
2. **저장**: `10. Raw Sources/{적절한 하위폴더}/`로 이동 (원본 보존)
3. **컴파일**: 관련 Wiki 페이지 10~15개를 incremental update
   - 기존 페이지가 있으면 → 새 정보 추가/업데이트
   - 새 개념이면 → 새 Wiki 페이지 생성
4. **연결**: cross-reference 링크 추가, MOC 업데이트
5. **로그**: `log.md`에 ingest 기록 추가
6. **인덱스**: `index.md` 업데이트

### 2. Query (지식 검색+합성)

질문을 받으면:

1. `index.md`에서 relevant pages 탐색
2. Wiki 페이지를 읽고 정보 종합
3. 답변 생성 (gap이나 모순 발견 시 Wiki에 피드백)
4. 필요시 `30. Queries/`에 합성 결과 저장

### 3. Lint / Health Check (자가 정화)

주기적으로:

- **Orphan 검사**: 어디에도 링크되지 않은 Wiki 페이지
- **Stale 검사**: 오래된 정보 플래그
- **모순 검사**: 페이지 간 상충하는 정보 → callout 추가
- **누락 링크**: `[[link]]`가 있지만 페이지가 없는 경우
- **인덱스 동기화**: `index.md`가 실제 구조와 일치하는지 확인

---

## Folder Structure

```
{vault-name}/
├── CLAUDE.md               # Schema (이 파일)
├── index.md                # 마스터 인덱스
├── log.md                  # 변경 이력
├── 00. Inbox/              # 새 자료 임시 저장 (Web Clipper 대상)
│   ├── 01. Articles/
│   ├── 02. Papers/
│   ├── 03. Transcripts/
│   └── 04. Clippings/
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
│   ├── 24. Maps/
│   └── 25. Questions/      # Research Question 카드
├── 30. Queries/            # 합성된 질의 결과 + synthesis
├── 40. Paper Analyses/     # 논문 12단 분석 ({citekey}/ 허브 S00 + 원자)
├── 80. References/         # 첨부 파일
│   └── Attachments/
└── 90. Settings/           # 템플릿
    └── Templates/
```

---

## Frontmatter Standards

### 필수 프로퍼티 (7개)

모든 .md 파일에 반드시 포함:

| Property | Type | Description |
|----------|------|-------------|
| `type` | text | `raw-source`, `wiki-page`, `research-question`, `query-result`, `synthesis`, `moc`, `paper-hub`, `paper-analysis`, `log` |
| `aliases` | list | 대체 이름 |
| `description` | text | English, 1-2 sentences |
| `author` | list | 작성자 (LLM인 경우 `Claude`) |
| `date created` | datetime | ISO 8601 |
| `date modified` | datetime | ISO 8601 |
| `tags` | list | 관련 태그 |

### Layer별 추가 프로퍼티

**Raw Source** (`type: raw-source`):
- `source`: 원본 URL 또는 참조
- `date ingested`: 인제스트 일시
- `category`: Articles / Papers / Books / Transcripts / Clippings

**Wiki Page** (`type: wiki-page`):
- `source`: 참조한 Raw Source 링크 목록
- `related`: 관련 Wiki 페이지 링크
- `confidence`: high / medium / low
- `layer`: concepts / entities / guides

**Query Result** (`type: query-result`):
- `query`: 원래 질문
- `source`: 참조한 Wiki 페이지

**MOC** (`type: moc`):
- `topic`: 주제 영역
- `related`: 하위 MOC 또는 관련 MOC

**Synthesis** (`type: synthesis`, `30. Queries/` 에 query-result 와 동거):
- `thesis`: 이 합성이 방어하는 한 문장 주장 (필수)
- `targetVenue`: 타깃 산출물·채널 (논문 / 책 챕터 / 블로그 시리즈 / 제품 결정)
- `supports`: 근거 Wiki 페이지·RQ `[[link]]` 목록
- `counters`: 반론·경쟁 가설

**Research Question** (`type: research-question`, `20. Wiki/25. Questions/`):
- `status`: open / investigating / answered / parked / superseded (필수)
- `questionType`: descriptive / causal / comparative / methodological / normative / design (필수)
- `feedsInto`: 어느 산출물로 흘러가나 (필수)
- `sourceCallout`: 승격돼 나온 원본 wiki 페이지 `[[link]]`
- `explored`: 기본 false

**Paper Hub / Paper Analysis** (`type: paper-hub` / `paper-analysis`, `40. Paper Analyses/{citekey}/`):
- 허브: `paperType` (6유형) · `citekey` · `targetManuscript` (`"[[RQ-…]]"` 또는 none) 필수
- 원자: `analysisStep` (2~12) · `analysisStepName` · `paperHub` wikilink · `citekey` 필수
- 상세는 메인 스키마 + `Paper Ingest Guide` 참고

---

## File Naming Convention

| Layer | Pattern | Example |
|-------|---------|---------|
| Raw Source | `YYYY-MM-DD-{title}.md` | `2026-04-13-Attention-Is-All-You-Need.md` |
| Wiki Page | `{Topic Name}.md` | `Transformer.md`, `OpenAI.md` |
| Query Result | `YYYY-MM-DD-Q-{question}.md` | `2026-04-13-Q-How-does-RLHF-work.md` |
| MOC | `MOC-{Topic}.md` | `MOC-Large Language Models.md` |
| Research Question | `RQ-{slug}.md` (`20. Wiki/25. Questions/`) | `RQ-agent-memory-architecture.md` |
| Paper Hub / 원자 | `{Surname} {Year} - S{NN} {제목}.md` (`40. Paper Analyses/{citekey}/`) | `Wu 2024 - S00 Hub.md` |

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

## Bootstrap

이 vault를 처음 세팅할 때, LLM에게 다음을 요청하세요:

> "이 볼트를 LLM Wiki로 초기화해줘. CLAUDE.md에 정의된 폴더 구조, 템플릿, index.md, log.md를 생성해줘."

---

## Git Integration (선택사항)

이 볼트를 Git으로 버전 관리하면 변경 이력을 추적할 수 있습니다:

- Ingest 시: `ingest: {source title}`
- Wiki 업데이트 시: `update: {page name} — {변경 요약}`
- Lint 수정 시: `lint: {수정 내용}`
