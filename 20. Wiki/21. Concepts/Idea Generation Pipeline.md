---
type: wiki-page
aliases:
  - Idea Generation Pipeline
  - Source-to-Idea Trigger
description: Workflow pattern that turns each new raw source ingest into an automatic creativity trigger tied to the user's research domain. New source + domain seed context → LLM-generated novel ideas (3 sources can yield 7+ distinct ideas in practice). Distinguishes LLM Wiki from passive learning tools (NotebookLM-style) by treating each new input as a divergence prompt, not just a record. Generalizable as a Starter Kit skill for research-driven users.
author:
  - Claude
date created: 2026-04-29
date modified: 2026-04-29
tags:
  - concept
  - workflow
  - idea-generation
  - creativity
  - research
  - llm-wiki
source: []
related:
  - "[[Ingest-Query-Lint Cycle]]"
  - "[[Track Classification and Research Gap Detection]]"
  - "[[LLM Wiki Pattern]]"
confidence: medium
layer: concepts
status: active
---

# Idea Generation Pipeline

> [!tip] Key Insight
> **"새 자료 = 새 아이디어 trigger"**. raw source 가 추가될 때마다 도메인 컨텍스트와 결합하여 새 아이디어를 자동 생성. 3 source → 7 ideas 정도가 cohort 실측. NotebookLM 같은 학습 도구와의 차별점 — **수동 흡수 vs 능동 발산**.

---

## Overview

**Idea Generation Pipeline** 은 단순한 자료 정리·요약 (NotebookLM 식) 을 넘어, **소스 추가가 곧 새 아이디어 도출의 트리거** 가 되는 LLM Wiki 워크플로 패턴. 학습자가 자기 도메인에 맞게 자체 설계한 cohort-level contribution 의 일반화.

특징: 단순 wiki 페이지 컴파일이 아니라 **창의적 발산** 단계가 ingest 와 통합.

---

## 작동 원리

### Step 1: 도메인 시드 (seed) 컨텍스트 정의
사용자가 자기 연구 도메인의 핵심 framework·문제·관심을 wiki 에 미리 등록 (concept 페이지 들로).

```
예시 — 의학 연구 시드:
- 분야 기초 개념
- 현재 기술 현황
- 핵심 문제·한계
```

### Step 2: 새 raw source ingest
표준 `/ingest` 흐름 + 추가 단계: 시드 컨텍스트와 cross-pollinate.

### Step 3: 아이디어 생성 trigger
ingest 완료 시 Claude 에게 명시적 prompt:

```
"이 새 raw source 가 [도메인 시드] 와 결합하면 어떤 새 아이디어가 가능한가?
- 기존에 없던 application
- 기존 문제의 새 해결 angle
- 기존 framework 의 확장
이미 wiki 에 있는 아이디어와 중복 없이 1-3 개 제시."
```

### Step 4: 아이디어 노트 생성
출력된 아이디어를 `30. Queries/` 또는 `20. Wiki/Ideas/` 에 페이지로 저장 → backlink 망에 편입.

### Step 5: 누적 효과
시간이 흐를수록 시드 자체가 두꺼워짐 → 새 source 마다 더 풍부한 cross-reference → 아이디어 품질 상승.

---

## NotebookLM·일반 RAG 와의 차이

| 축 | NotebookLM | RAG | LLM Wiki Idea Generation |
|---|----------|-----|------------------------|
| 입력 자료 다루는 법 | 학습용 흡수 | 검색 인덱스 | **창의 trigger** |
| 출력 | 요약·Q&A | 답변 | **새 아이디어 + wiki 노드** |
| 누적 효과 | 없음 | 인덱스만 큼 | **시드 풍부화 → 아이디어 품질 상승** |
| 사용 시점 | 학습 시 | query 시 | **자료 도착 즉시** |

→ "노트북 LM이 단순 학습 도구라면, LLM 위키는 더 깊은 사고와 응용 방안을 탐색하는 데 적합".

---

## 적용 가능 도메인

| 도메인 | 시드 | 아이디어 형태 |
|------|-----|----------|
| 헬스케어 | 메커니즘 · 임상 | 새 콘텐츠 앵글, 신서비스 |
| 비즈니스 | 회사 강점·약점·시장 | 신제품 idea, 경쟁 우위 발견 |
| 스포츠 | 종목·전술 | 새 분석 방법 |
| 학술 | 논문 분야 | 연구 갭 + 신가설 |
| 창업·창작 | 도메인 + 페르소나 | 콘텐츠 기획, 스토리 idea |

---

## 제안 — `/idea` skill (예시)

```
/idea seed [domain]        # 시드 컨텍스트 정의
/idea trigger <raw>         # 새 raw source 로부터 아이디어 도출
/idea list                  # 누적 아이디어 보기
/idea promote <id>          # 아이디어 → 정식 wiki concept 로 승격
```

[[Track Classification and Research Gap Detection]] 와 보완:
- Track Classification: **수집 방향** 안내 (어디가 비어있나)
- Idea Generation Pipeline: **창의 발산** 안내 (지금 자료로 무엇을 새로 할 수 있나)

---

## 위험·한계

1. **Hallucination 위험** — "새 아이디어" 가 사실은 기존 idea 의 표현 변경일 뿐일 수 있음. 중복 검사 + lint 필요.
2. **품질 변동** — 시드 컨텍스트 빈약하면 아이디어도 빈약. 초기 학습자에겐 어려움.
3. **Query 토큰 추가** — ingest 마다 idea generation prompt 추가 → [[Cohort Token Economy]] 압박. 옵션으로 제공 + on-demand 호출 권장.

---

## Related

- [[Ingest-Query-Lint Cycle]] — 본 패턴이 확장하는 cycle
- [[Track Classification and Research Gap Detection]] — 보완 skill
- [[LLM Wiki Pattern]]
- [[Cohort Token Economy]] — 비용 trade-off

---

## Open Questions

> [!question] 아이디어 노드의 wiki 적재 방식
> Ideas 가 별도 폴더 (`20. Wiki/Ideas/`) 에 들어가야 하나, 아니면 기존 concept 와 동일 layer 인가? Vault 구조 영향.

> [!question] 시드 풍부화 모니터링
> 시드 컨텍스트가 시간에 따라 두꺼워지는 정도를 측정 가능한 지표 — concept page 수, 백링크 밀도, embedding cluster size 등.

> [!question] 아이디어 검증 통합
> 생성된 아이디어를 그대로 두지 말고 외부 검색 (학술 DB, 특허 DB) 과 cross-check 해 "이미 누가 했는지" 확인하는 후속 skill.
