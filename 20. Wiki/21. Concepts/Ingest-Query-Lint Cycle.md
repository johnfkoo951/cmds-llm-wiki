---
type: wiki-page
aliases:
  - Wiki Operations
  - Ingest Query Lint
  - IQL Cycle
description: The three core operations of an LLM Wiki — Ingest (absorb new sources), Query (search and synthesize answers), and Lint (health-check for contradictions, orphans, and staleness).
author:
  - Claude
date created: 2026-04-12T00:00
date modified: 2026-04-14T15:00
tags:
  - llm-wiki
  - operations
  - workflow
source:
  - "[[2026-04-02-Karpathy-LLM-Knowledge-Bases-X-Thread]]"
  - "[[2026-04-12-Karpathy-LLM-Wiki]]"
  - "[[2026-04-02-Harnessing-Claudes-Intelligence-3-Patterns]]"
related:
  - "[[LLM Wiki Pattern]]"
  - "[[3-Layer Architecture]]"
  - "[[Persistent Knowledge Base]]"
  - "[[qmd]]"
  - "[[Agent Harness Design]]"
  - "[[Progressive Disclosure Pattern]]"
confidence: high
layer: concepts
status: active
---

# Ingest-Query-Lint Cycle

> [!tip] Key Insight
> Wiki를 살아있게 만드는 세 가지 작업: **Ingest**(새 지식 흡수), **Query**(검색+합성), **Lint**(자가 정화). 세 작업 모두 wiki를 더 풍부하게 만든다.

---

## Overview

[[LLM Wiki Pattern]]은 세 가지 핵심 operation으로 운영된다. 각 operation은 [[Persistent Knowledge Base|wiki를 성장시키는]] 방향으로 작동한다.

---

## Details

### 1. Ingest (새 자료 흡수)

새 source를 wiki에 통합하는 과정.

**워크플로**:
1. 새 source가 `00. Inbox/`에 도착
2. LLM이 source를 읽고 핵심 takeaway 추출
3. `10. Raw Sources/`에 원본 저장 (불변)
4. Wiki 페이지 10~15개를 incremental update:
	- 기존 페이지가 있으면 → 새 정보 추가/업데이트
	- 새 개념이면 → 새 페이지 생성
5. `index.md` 업데이트
6. `log.md`에 기록

**Karpathy의 선호**: source를 하나씩 ingest하면서 관여하기 (요약 확인, 방향 제시). 단, batch ingest도 가능.

### 2. Query (지식 검색+합성)

wiki에 대해 질문하고 답변을 받는 과정.

**워크플로**:
1. `index.md`에서 관련 페이지 탐색
2. 관련 Wiki 페이지 읽기
3. 정보 종합하여 답변 생성

**답변 형태**: markdown 페이지, 비교 표, 슬라이드 (Marp), 차트 (matplotlib), canvas 등.

**핵심 인사이트**: 좋은 답변은 wiki에 다시 저장할 수 있다. 비교 분석, 발견한 연결, 합성 결과 — 이것들은 chat history에서 사라지면 안 된다. Wiki에 저장하면 탐색도 source처럼 **compounding**된다.

### 3. Lint (자가 정화)

wiki의 건강 상태를 점검하는 과정.

**점검 항목**:
- **Contradictions**: 페이지 간 상충하는 정보
- **Stale claims**: 새 source로 대체된 오래된 주장
- **Orphan pages**: 어디에도 링크되지 않은 페이지
- **Missing pages**: 언급되었지만 아직 페이지가 없는 개념
- **Missing cross-references**: 연결되어야 할 링크 누락
- **Data gaps**: 웹 검색으로 채울 수 있는 정보 공백

> [!tip] "What can I stop doing?" — Wiki edition
> [[Lance Martin]]의 [[Agent Harness Design|agent harness 설계 원칙]]을 wiki에 적용: **Lint는 "무엇을 그만할 수 있을까?"의 문서 판본**. Wiki도 dead weight를 축적한다 — 한때 유효했으나 이제 모델이 발전해 필요 없어진 규칙, 중복 설명, 낡은 경고. 매 lint 사이클마다 "이것을 지워도 위키가 여전히 잘 작동하는가?"를 묻는 것이 건강한 규율.

### Indexing and Logging

두 가지 시스템 파일이 wiki 네비게이션을 지원한다:

| 파일 | 목적 | 특성 |
|------|------|------|
| `index.md` | 콘텐츠 카탈로그 | 페이지 목록 + 1줄 요약. Query 시 LLM이 먼저 읽음 |
| `log.md` | 시간순 이력 | Append-only. 무엇이 언제 일어났는지 기록 |

`index.md`는 ~100 sources, ~수백 pages 규모까지 embedding-based RAG 인프라 없이도 잘 작동한다.

> [!info] Scale Calibration
> Karpathy 본인 deployment (2026-04-02 X 공개): **~100 articles, ~400K words**까지 `index.md`만으로 충분. 이 규모를 넘어서면 [[qmd]] 같은 로컬 검색 엔진 도입이 자연스러워진다.

---

## Related

- [[LLM Wiki Pattern]] — 이 operations가 속한 전체 패턴
- [[3-Layer Architecture]] — operations가 작동하는 구조
- [[Persistent Knowledge Base]] — 세 operations가 wiki를 compounding하는 이유
- [[Agent Harness Design]] — Lint의 철학적 뿌리 ("what can I stop doing?")
- [[Progressive Disclosure Pattern]] — Query가 이 패턴으로 작동 (index.md → drill-down)

---

## Sources

- [[2026-04-02-Karpathy-LLM-Knowledge-Bases-X-Thread]]
- [[2026-04-12-Karpathy-LLM-Wiki]]
- [[2026-04-02-Harnessing-Claudes-Intelligence-3-Patterns]]
