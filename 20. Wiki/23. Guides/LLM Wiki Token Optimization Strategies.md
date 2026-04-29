---
type: wiki-page
aliases:
  - Token Optimization Guide
  - LLM Wiki 토큰 절감
  - Cohort Token Survival Guide
description: Practical guide for sustaining heavy LLM Wiki workloads on token-constrained budgets. Covers external preprocessing, model selection per task, /effort throttling, multi-platform distribution, and conditional local-model fallback. Designed as the curriculum companion when introducing LLM Wiki to a class, research lab, or study cohort.
author:
  - Claude
date created: 2026-04-29
date modified: 2026-04-29
tags:
  - guide
  - token-optimization
  - cohort
  - claude-code
  - llm-wiki
  - cost-engineering
source: []
related:
  - "[[Cohort Token Economy]]"
  - "[[External Pre-processing Pattern]]"
  - "[[Obsidian Tooling for LLM Wiki]]"
confidence: high
layer: guides
status: active
---

# LLM Wiki Token Optimization Strategies

> [!tip] Key Insight
> **"Pro 가 한계인 건 정상이다, 시스템이 잘못된 게 아니다"**. Cohort 작업량은 Pro 한계를 넘는 게 자연스러움. 해결책은 4 단계: (1) 외부 전처리로 무거운 변환 분리, (2) 모델 선택으로 작업별 적정화, (3) `/effort` 로 단가 낮추기, (4) 필요하면 요금제 업그레이드 또는 로컬 모델. 가이드 본문은 각 단계의 적용 시점·방법·주의사항.

---

## Overview

본 가이드는 [[Cohort Token Economy]] 문제를 해결하기 위해 정리. 정규 강의·연구 cohort 가 LLM Wiki 를 지속적으로 사용할 때 적용 가능한 토큰 최적화 전략을 단계별로 설명.

대상: 정규 강의 cohort, 연구실 그룹, 학습자 본인.

---

## 단계 1 — 작업 분해 (가장 큰 효과)

### 1-1. 외부 전처리 도입
무거운 변환은 외부 도구로. → 상세: [[External Pre-processing Pattern]].

| 무거운 입력 | 외부 도구 | 결과 |
|----------|---------|------|
| 장편 논문 (40+ pages) | GPT 심층 리서치 (Deep Research) | 정제된 markdown 리포트 |
| 외국어 영상·강의 | Whisper STT + GPT/Gemini 번역 | 모국어 정제 스크립트 |
| 대용량 텍스트 다수 | Google AI Studio (long context) | 요약·재구성 |
| 웹 페이지 다수 | 옵시디언 Web Clipper | Inbox 의 standardized markdown |

→ Claude 의 토큰을 **wiki 컴파일·query·lint** 에만 집중.

---

## 단계 2 — 모델 선택 (작업별 적정화)

### 2-1. 모델 - 작업 매핑

| 작업 | 권장 모델 | 이유 |
|-----|---------|------|
| 단순 분류·태깅·요약 | **Haiku** | 충분 + 토큰 저렴 |
| 표준 wiki 컴파일 | **Sonnet** | 균형 |
| 복잡 분석·창의 발산 | **Opus** | 차이 큼 |
| Vision 작업 (디자인·이미지) | Opus (vision-capable) | vision 특화 |
| 일상 chat | Pro · Free Sonnet | 별도 |

### 2-2. Subagent 분할
복잡 작업을 [[Orchestrator-Subagent Pattern]] 으로 분할 → 각 subagent 가 자기 작업에 적정 모델 사용.

---

## 단계 3 — Effort throttling

### 3-1. `/effort` 명령
터미널에서:

```
/effort minimal   # 단순 작업
/effort medium    # 표준
/effort high      # 복잡 분석
```

→ Effort level 낮출수록 토큰 소모·응답 시간 감소.

### 3-2. 적용 가이드라인
- 1차 ingest (정형화된 자료) → **minimal**
- 표준 wiki 컴파일 → **medium**
- 모순 검출 lint, 복잡 query → **high**

### 3-3. YOLO 모드
반복 승인이 필요 없는 batch 작업:

```
claude --dangerously-skip-permissions
```

승인 마찰 제거 → 시간 절감 (직접 토큰은 아니지만 사용자 시간 = 토큰 효율).

---

## 단계 4 — 인프라 결정 (필요 시)

### 4-1. Claude 요금제 업그레이드 (서비스 출시 목표 시)

| 요금제 | 적정 사용자 |
|------|-----------|
| Pro | 개인 학습, 가벼운 cohort 사용 |
| Max | 정규 cohort, 활발한 wiki 작업 |
| Max+ | 본격 서비스 출시, 비즈니스 적용 |

비즈니스 적용 사례 (BI, 콘텐츠 엔진) 는 Max 이상 투자 정당화 가능.

### 4-2. 로컬 모델 도입 (선택적)

| 모델 | 사양 | 비고 |
|------|-----|------|
| Qwen 3.6 (32B) | 일반 노트북 가능 | 권장 |
| Gemma (31B) | 일반 노트북 가능 | 다수 환경 정상 작동 |
| 대형 (35B+, MoE) | 고사양 GPU 필요 | high-spec only |

설치: Ollama → 모델 pull → 클로드 코드 ↔ 로컬 연결.

**경고**: 컴퓨터 사양 부족 시 줌 발표·collaboration 곤란할 정도로 느린 사례 있음 — 사양 가능 학습자 한정.

### 4-3. 멀티 플랫폼 분산
한 vendor 에 모두 의존 안 함:

| 플랫폼 | 강점 |
|-------|------|
| **OpenAI ChatGPT** | 심층 리서치, 자유 form chat |
| **Anthropic Claude** | 코드·wiki·에이전트 |
| **Google AI Studio (Gemini)** | 대용량 컨텍스트 (1M+) |
| **로컬 (Ollama)** | 민감 데이터, 무한 ingest |

→ 각 플랫폼의 강점 시점 인식해 작업 배분.

---

## 커리큘럼 설계 권장 (Cohort 운영자용)

Cohort 가 LLM Wiki 를 본격 도입할 때 권장:

1. **1주차**: Token economy 명시 + Pro 한계 사전 경고 + 외부 전처리 패턴 시연
2. **3주차**: 외부 전처리 핸즈온 lab — GPT 심층 리서치 → Claude
3. **5주차**: 모델 선택 가이드 + `/effort` 실습
4. **선택 lab**: Ollama 로컬 모델 설치 (사양 가능 학습자)
5. **상시 도움말**: YOLO 모드, multi-platform 팁 자료에 상시 비치

---

## 정책 변동 대비

LLM 플랫폼은 수시로 요금·접근 정책 변경. Cohort 운영 시 정책 변경 리스크 헷지:
- 클로드 외 대안 lab (GPT, Gemini) 도 운영
- 학습자가 1 vendor 에 lock-in 되지 않도록 multi-platform 워크플로 강제
- 대체재 동향 매주 cohort 와 공유

---

## 의사결정 흐름 (요약)

```
새 작업 도착
  ↓
무거운 변환 필요? — Yes → [단계 1] 외부 전처리
  ↓ No
적정 모델 결정 — [단계 2] Haiku/Sonnet/Opus
  ↓
복잡도? — High → /effort high / Low → /effort minimal — [단계 3]
  ↓
실행
  ↓
토큰 한계 도달? — Yes → [단계 4] 요금제 업그레이드 OR 로컬 모델
                  ↓ No
                  계속
```

---

## Related

- [[Cohort Token Economy]] — 본 가이드가 해결하는 문제
- [[External Pre-processing Pattern]] — 단계 1 의 핵심
- [[Obsidian Tooling for LLM Wiki]] — 인프라 측 가이드

---

## Open Questions

> [!question] Edu 라이선스 가능성
> Anthropic edu license · Cursor edu plan 등 학생 대상 할인 프로그램 여부 추적. 단체 신청 가능한 옵션이 있다면 token economy 문제 근본 해결.

> [!question] Token-aware 자동 routing
> `/ingest` 가 입력 크기 보고 "이 source 는 외부 전처리 권장" 자동 출력하는 skill 확장. Cohort 가 실험할 수 있는 학습 과제로도 좋음.

> [!question] Cohort 토큰 통계 수집
> 학습자들이 자기 토큰 소비를 자발적 공유하면 cohort 평균·중앙·최대 통계 작성 가능 → 신입 cohort 에게 정확한 사전 안내.
