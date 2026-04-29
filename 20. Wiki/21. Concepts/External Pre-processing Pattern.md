---
type: wiki-page
aliases:
  - External Preprocessing
  - Pre-processing Pipeline
  - GPT-First LLM Wiki Pattern
description: Cost-optimization pattern for LLM Wiki workflows — heavy raw materials (long PDFs, video transcripts, web scraping, foreign-language content) are first processed in cheaper or free external platforms (GPT deep research, Google AI Studio, Whisper STT) and only the distilled output is fed into the LLM Wiki via /ingest. Reserves expensive Claude tokens for what only Claude does well in this stack (wiki compilation, lint, query).
author:
  - Claude
date created: 2026-04-29
date modified: 2026-04-29
tags:
  - concept
  - workflow
  - token-optimization
  - llm-wiki
  - hybrid-pipeline
  - cost-engineering
source: []
related:
  - "[[Cohort Token Economy]]"
  - "[[LLM Wiki Token Optimization Strategies]]"
  - "[[Ingest-Query-Lint Cycle]]"
confidence: high
layer: concepts
status: active
---

# External Pre-processing Pattern

> [!tip] Key Insight
> **"Claude 가 잘하는 것 만 Claude 에게 시킨다"**. PDF·영상·웹 크롤링 같은 **무거운 raw 변환** 은 GPT 심층 리서치·Google AI Studio·Whisper STT 같은 외부에서 먼저 처리, 정제된 결과만 LLM Wiki 의 `/ingest` 로 투입. 토큰 비용을 위키 컴파일·lint·query 같은 Claude 의 unique value 에 집중.

---

## Overview

**External Pre-processing Pattern** 은 [[Cohort Token Economy]] 의 가장 효과적 해결 전략. 핵심 통찰: 모든 작업을 Claude 에 맡기는 게 단순하지만 **비용 비효율**. 무거운 변환은 외부에 보내고, **wiki 컴파일과 query** 처럼 LLM Wiki 의 핵심 가치만 Claude 에 집중.

---

## 적용 가능한 외부 도구

| 무거운 입력 | 외부 처리 | 출력 (Claude 입력) |
|----------|---------|------------------|
| **장편 논문 (40+ pages)** | GPT 심층 리서치 (Deep Research) | 주제별 정제 레포트 |
| **외국어 영상** | Whisper STT + GPT/Gemini 번역 | 모국어 정제 스크립트 |
| **대용량 텍스트 처리** | Google AI Studio (long context) | 요약·재구성 |
| **웹 페이지 다수 클리핑** | 옵시디언 Web Clipper (자동 markdown 변환) | Inbox 에 standardized markdown |
| **공개 API 데이터** | 자체 스크립트 (Python) | 정형 jsonl/markdown |

→ Claude 의 입력은 **이미 정제된** 상태로만 투입.

---

## 워크플로 단계

### 1. 입력 분류
새 raw 자료 도착 시 즉시 판단:
- 짧고 정제된 텍스트 (e.g. 블로그 포스트, GitHub README) → 직접 LLM Wiki ingest
- 장편·다국어·멀티모달 → **외부 전처리** 우선

### 2. 외부 전처리 실행
적합한 외부 도구로 정제. 출력은 항상:
- Markdown 형식
- 구조화 (heading + bullet)
- 모국어 (또는 사용자 언어)
- 핵심 인사이트 highlight

### 3. LLM Wiki 진입
정제 결과를 `00. Inbox/` 에 저장 → `/ingest` 호출 → wiki 컴파일.

### 4. 비교·검증
가끔 외부 처리 결과를 **그대로 ingest** vs **Claude 가 처음부터 다시** 비교 — 어느 쪽 wiki 품질이 더 좋은지 모니터링.

---

## 트레이드오프

### 장점
- **토큰 절감**: 50-80% (cohort 사례 기반 추정)
- **속도**: 외부 long-context 플랫폼이 Claude 직접 처리보다 빠를 때 다수
- **분산 리스크**: 단일 vendor 의존도 감소
- **각 도구 강점 활용**: GPT (deep research), Gemini (대용량), Whisper (STT)

### 단점
- **워크플로 복잡도**: 도구 N 개 관리
- **결과 일관성 손상**: 외부 도구의 stylistic drift
- **자동화 어려움**: 다단계 → 사용자 수동 개입 많음
- **데이터 노출**: 민감 데이터를 여러 vendor 에 전달

### 잘 안 맞는 경우
- 인터랙티브 wiki query (외부 전처리 후 Claude 로 와도 → query 마다 토큰 소모)
- 빠른 1회성 자료 처리 (멀티 플랫폼 셋업이 오버헤드)
- 매우 민감한 데이터 (vendor 분산 자체가 risk)

---

## [[Ingest-Query-Lint Cycle]] 과의 관계

External Pre-processing 은 **Ingest 단계 앞에** 배치되는 **0 단계 (Pre-Ingest)**:

```
[Pre-Ingest: 외부]    [Ingest: Claude]    [Compile: Claude]    [Query/Lint: Claude]
GPT/AI Studio  →  /ingest  →  Wiki pages  →  지속 업데이트
(정제)           (구조화 저장)    (컴파일)         (운영)
```

→ Claude 의 토큰 budget 을 핵심 단계 (compile, query, lint) 로 집중.

---

## Related

- [[Cohort Token Economy]] — 본 패턴이 해결하는 상위 문제
- [[LLM Wiki Token Optimization Strategies]] — 종합 가이드
- [[Ingest-Query-Lint Cycle]] — 본 패턴이 확장하는 cycle

---

## Open Questions

> [!question] 자동 routing skill
> `/ingest` 가 입력 크기·언어·형식 보고 자동으로 "외부 전처리 권장" 출력하는 skill 확장 가치.

> [!question] 외부 전처리 결과 품질 보증
> GPT 심층 리서치 결과의 **정확성·hallucination** 검증 없이 Claude 에 투입하면 오류 누적. Lint 단계에서 외부 출처 자료의 인용 검증 자동화 가치.

> [!question] 비용 정확 비교
> 외부 전처리 후 Claude vs Claude 직접 — 실제 토큰·비용·시간 비교 데이터 수집 가치 (cohort 가 좋은 실험 환경).
