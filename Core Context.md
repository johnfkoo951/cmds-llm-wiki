---
type: core-context
aliases:
  - User Context
  - 핵심 맥락
description: The user's core context — identity, knowledge-collection purpose (reuse axes), and philosophy. LLM must read this BEFORE any ingest/query/lint so operations align with the user's purpose, not just structure. Fill in placeholders before using.
author:
  - "[[{your-name}]]"
date created: {YYYY-MM-DD}
date modified: {YYYY-MM-DD}
tags:
  - system
  - schema
  - core-context
source-vault: "{your-mothership-vault-name}"
source: []
version: "1.0"
snapshot_date: {YYYY-MM-DD}
status: template
---

# 🧭 Core Context — LLM Wiki 사용자 맥락

> **템플릿 노트**입니다. 아래 placeholder 를 본인 맥락으로 채운 뒤 `status: active` 로 바꾸세요.
> 이 노트는 LLM 이 ingest / query / lint 전에 **반드시 먼저 읽는** 사용자 맥락입니다.
> 채우는 방법 두 가지:
> 1. **직접 작성** — 자기소개, 목적, 철학을 아래 섹션에 직접 입력
> 2. **기존 기록에서 추출** — 이미 블로그·노트·에세이가 있다면, LLM 에게 읽고 이 노트를 채우도록 요청
> 3. **STT 인터뷰** — 마이크로 자기소개 녹음 → LLM 에게 정리 요청 (박준 가이드 Phase 1 방식)

---

## 1. Who — 사용자 정체성

### 기본 정체성

- **이름**: `{Your Name}` (예: 홍길동 / Jane Doe)
- **직함 / 역할**: `{your current role(s)}` (예: 연구자, 프리랜서 디자이너, 강사, PM...)
- **전문 분야**: `{your domain(s)}` (예: AI 교육, UX 리서치, 플라이트 엔지니어링...)
- **주 활동 영역**: `{your working domain}` (예: 대학·기업 교육, 소프트웨어 개발, 창작...)

### 연속성 선언 (Continuity Statement)

> "{현재 지식 관리 활동이 과거의 어떤 질문과 연결되는지 1~3 문장}"

**예시** (참고용):
> "나는 원래 A를 연구하던 사람이다. 지금 B를 말할 때도 내가 보는 것은 결국 A다. C 는 A 를 더 잘 다루기 위한 도구의 진화일 뿐이다."

이 선언은 LLM 이 "왜 이 사람이 이 주제를 수집하는가" 의 깊이를 이해하는 앵커가 된다.

---

## 2. Why — 지식을 수집하는 목적 (재활용 축)

**Gold In Gold Out 원칙**: "이 소스가 아래 어느 축에 재활용될지" 를 수집 시점에 명시하지 못하면 수집하지 않는다.

아래는 일반적 축 예시 — 본인 맞게 추가/삭제/재배열하세요.

1. **`{축 1}`**: (예) 학술 연구 / 논문 · 학위
2. **`{축 2}`**: (예) 저술 · 출판
3. **`{축 3}`**: (예) 강의 · 강연
4. **`{축 4}`**: (예) 컨설팅 · 자문
5. **`{축 5}`**: (예) 제품 · 소프트웨어 개발
6. **`{축 6}`**: (예) 개인 에세이 · 브랜딩
7. **`{축 7}`**: (예) 커뮤니티 · 교육 자료

> 축은 5~9개 권장. 너무 적으면 모든 수집이 같은 축으로 쏠리고, 너무 많으면 축 자체가 무의미해진다.

---

## 3. What — (옵션) 개인 지식 프레임워크

자체 지식 관리 프레임워크가 있다면 여기 기록. 없다면 이 섹션은 비워도 OK.

**예시 구조**:
- 지식 생애주기 단계 (예: Connect → Merge → Develop → Share)
- 카테고리 체계 (예: 100 Themes / 200 Literature / ... / 900 Divisions)
- 역할/포지션 구분

**참고 사례**: [cmds-system-files](https://github.com/johnfkoo951/cmds-system-files) (Connect→Merge→Develop→Share + 100-900 9 categories)

---

## 4. How — (옵션) 지식 시스템 철학

LLM 이 정리 과정에서 따라야 할 사용자의 원칙·manifesto. 본인 에세이/블로그에서 뽑아 핵심 3~5개로 요약.

**예시 (참고용 — 본인 철학으로 교체)**:
- 스키마가 문서보다 먼저다 — Retrieval 은 구조 위에서 작동한다
- Harness 설계가 경쟁력이다 — 모델보다 harness 에 투자
- 암묵지 외재화가 AI-Ready 볼트의 본질이다 — 정리 도구가 아닌 창조 인프라
- 행동 의도를 설계하는 시스템이 정보 구조보다 오래 간다

각 원칙은 LLM 이 ingest 시 "이 수집이 내 철학과 어떻게 정렬되는가" 를 판단하는 기준이다.

---

## 5. (옵션) Mothership 볼트 시스템 파일

별도의 mothership Obsidian 볼트가 있고, 그 볼트의 system files (CLAUDE.md 등) 를 본 LLM Wiki 가 참고해야 한다면 여기 등록. 없다면 이 섹션 전체 삭제.

### Dynamic References (@mention)

| Alias | 경로 | 역할 |
|-------|------|------|
| `@MS-CLAUDE` | `{PATH_TO_MOTHERSHIP}/CLAUDE.md` | (설명) |
| `@MS-AGENTS` | `{PATH_TO_MOTHERSHIP}/AGENTS.md` | (설명) |
| ... | ... | ... |

최신본 읽기: `Read("{PATH_TO_MOTHERSHIP}/{file}")` 또는 `mcp__qmd__query`.

**Mothership pattern 참고**: [cmds-system-files](https://github.com/johnfkoo951/cmds-system-files) — 5 system files (CLAUDE/AGENTS/CMDS/CMDS Guide/CMDS HQ) 구조와 semver changelog.

---

## 6. Operational Directives (LLM 행동 규칙)

### Ingest 시

1. `/ingest` 는 반드시 "왜 수집했는가?" 를 1회 묻는다 (Gold In Gold Out, §2 축 참조).
2. 사용자 답변을 받으면 (mothership 이 있다면) 유사 노트 검색하여 `mainVaultRelated` 기록.
3. Raw Source frontmatter 에 `collectionPurpose`, `mainVaultRelated`, `mainVaultCmds` 기록.

### Query 시

1. 답변이 §2 7 재활용 축 중 어느 축에 연결되는지 명시.
2. (mothership 있다면) `→ {your-mothership}:` 참조 포함.

### Lint 시

- Raw Source 에 `collectionPurpose` 없으면 flag.
- Core Context `snapshot_date` 가 30 일 이상 오래되면 `/refresh-context` 추천.

### 이미지 저장

- 모든 이미지·첨부: `80. References/Attachments/` 일원화.

---

## 7. 채우고 나서

- [ ] §1 정체성 채움
- [ ] §2 재활용 축 5~9개 정의
- [ ] (옵션) §3 개인 프레임워크
- [ ] (옵션) §4 철학 3~5개
- [ ] (옵션) §5 mothership 볼트 등록
- [ ] frontmatter `status: template` → `status: active`
- [ ] frontmatter `snapshot_date` 오늘 날짜
- [ ] frontmatter `source:` 에 본인이 참고한 에세이·노트 경로 추가

완료 후 첫 `/ingest` 를 실행해보세요. Core Context 가 작동하면 LLM 이 §2 축을 언급하며 목적 질문을 던집니다.

---

## 8. Related

- [[CLAUDE]] — LLM Wiki Schema
- [[index]] — Master Index
- [[log]] — Change Log
- [[LLM-Wiki-Starter-Kit]] — 외부 공유용 간이 킷

---

*템플릿 v1.0 — Karpathy LLM Wiki pattern + 박준 Gold In Gold Out 가이드 기반*
