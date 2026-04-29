---
type: wiki-page
aliases:
  - Cohort Token Economy
  - Class Token Constraint
description: Predictable failure pattern observed in LLM Wiki cohorts — when a group of users (class, research lab, study group) relies on Claude Pro plan for sustained wiki/agent work, token limits become the primary bottleneck within 1-2 weeks. Distinct from individual hobbyist usage where Pro suffices. A cohort-runner concern, not just a per-user concern — informs curriculum and onboarding design.
author:
  - Claude
date created: 2026-04-29
date modified: 2026-04-29
tags:
  - concept
  - cohort
  - token-economy
  - curriculum-design
  - claude-pro
  - claude-max
  - operations
source: []
related:
  - "[[LLM Wiki Token Optimization Strategies]]"
  - "[[External Pre-processing Pattern]]"
  - "[[Ingest-Query-Lint Cycle]]"
confidence: high
layer: concepts
status: active
---

# Cohort Token Economy

> [!tip] Key Insight
> **개인 취미 = Pro 충분 / cohort 정규 사용 = Pro 한계**. 위키·에이전트·반복 개발 작업이 누적되면 cohort 의 80%+ 가 1-2주 내에 토큰 한계 도달. 이는 학습자 개인 부담의 문제가 아니라 **커리큘럼·운영 설계의 필수 변수** — 전처리·모델 선택·로컬 옵션을 onboarding 안에 포함시켜야 cohort 가 학습을 지속 가능.

---

## Overview

**Cohort Token Economy** 는 정규 강의·연구 그룹·스터디 cohort 가 LLM Wiki Starter Kit 을 도입했을 때 관측되는 일반적 패턴: **거의 전원이 Claude Pro 요금제 토큰 한계에 부딪힌다**.

핵심 차이:
- **개인 취미 사용**: 간헐적 ingest, 가끔 query → Pro 로 충분
- **Cohort 정규 사용**: 주별 과제 + 다양한 raw source 변환 + 위키 재컴파일 → Pro 한계 빠르게 도달

---

## 왜 정규 cohort 에서 더 심한가

### 1. 빈도
취미: 주 1-2 회 vs cohort: 매일 (과제 마감 압박)

### 2. 작업 종류
취미: 가벼운 query vs cohort: 본격 ingest + 위키 재컴파일 + lint + custom skill 추가

### 3. 학습 곡선
초기 학습자는 한 번에 성공 못 함 → **재시도** → 같은 raw source 를 여러 번 처리 → 토큰 N 배 소모

### 4. 실험 비용
학습자가 자기 도메인에 맞춤화하는 과정에서 **trial-and-error** → 결과만 나오는 게 아니라 잘못된 결과도 토큰 소비

---

## 해결 전략 (cohort-level)

### A. 외부 전처리 ([[External Pre-processing Pattern]])
- GPT 심층 리서치 → LLM Wiki Raw 자료
- 외부 long-context 플랫폼 → 정제본만 Claude 에 투입
- Whisper STT (음성/영상) → 텍스트 변환 후 ingest
→ **Claude 토큰을 wiki 컴파일·query 에만** 집중 소비.

### B. 모델 effort 조정
- `/effort` 명령으로 effort level 낮춤
- 단순 분류·정리 작업은 Haiku
- 복잡 analysis 만 Opus

### C. 로컬 모델 (선택적)
- Ollama + Qwen / Gemma 로컬 설치
- 클로드 코드 ↔ 로컬 모델 연결
- 한계: 컴퓨터 사양 (사양 부족 시 줌 발표·collaboration 곤란)

### D. 요금제 업그레이드 (서비스화 목표 시)
- Pro → Max 또는 Max+
- 비즈니스 적용 사례 (실제 회사 BI, 콘텐츠 제작 엔진) 는 투자로 정당화

### E. 멀티 플랫폼 분산
- ChatGPT (전처리·심층 리서치)
- Gemini (대용량 처리)
- Claude (위키 컴파일·에이전트 워크플로)
- 각자 강점에 맞춰 분담

---

## 커리큘럼·온보딩 설계 함의

Cohort 운영자가 LLM Wiki 를 도입할 때 권장:

1. **첫 주 token economy 명시** — Pro 한계 미리 경고 + 외부 전처리 패턴 시연
2. **3주차 외부 전처리 lab** — GPT/Gemini 전처리 → Claude 투입 워크플로 핸즈온
3. **5주차 모델 선택 가이드** — Haiku/Sonnet/Opus 별 적정 작업 매핑
4. **선택 lab — 로컬 모델 설치** — 사양 가능 학습자 대상 옵션 lab
5. **상시 도움말** — `/effort` · YOLO 모드 등 토큰 절감 팁 자료 상시 비치

---

## 정책 변동성 주의

LLM 플랫폼은 수시로 요금·접근 정책을 변경 — Claude Code 가 특정 요금제에서만 사용 가능하도록 시도된 적 있음. Cohort 운영 시 정책 변경 리스크를 커리큘럼 lock-in 회피 설계 (Claude Code 외 대안 lab 도 운영) 로 헷지.

---

## Related

- [[LLM Wiki Token Optimization Strategies]] — 실용 가이드
- [[External Pre-processing Pattern]] — 가장 효과적 전략
- [[Ingest-Query-Lint Cycle]] — 토큰 소비 발생 지점

---

## Open Questions

> [!question] 학습자당 적정 토큰 예산
> Cohort 1 인당 1 학기 동안 필요한 토큰 양 추정치는? Pro 의 N 배인가, Max 의 N 배인가. 학습자 부담 vs 기관 지원 vs vendor edu 라이선스 가능성.

> [!question] Token-aware ingest skill
> `/ingest` 가 자동으로 source 크기 보고 → "이 source 는 외부 전처리를 권장합니다" 식으로 routing 권고하는 skill 확장 가치.

> [!question] 무료 대안의 학습 effective 차이
> 학습자가 ChatGPT free + Gemini free 만으로 LLM Wiki 학습 가능한가? 가능한 부분과 막히는 부분의 경계 측정 가치.
