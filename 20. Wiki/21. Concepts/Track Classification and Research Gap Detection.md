---
type: wiki-page
aliases:
  - Track Classification
  - Research Gap Detection
description: Custom command pattern for systematic-review-style LLM Wiki workflows — splits ingested papers/articles into thematic tracks during analysis, then computes per-track coverage percentages to surface research gaps (lowest-coverage track = highest-priority gap to fill). Generalizable across any domain that benefits from typology-driven literature mapping.
author:
  - Claude
date created: 2026-04-29
date modified: 2026-04-29
tags:
  - concept
  - command-pattern
  - skill-extension
  - research
  - systematic-review
source: []
related:
  - "[[Ingest-Query-Lint Cycle]]"
  - "[[Idea Generation Pipeline]]"
confidence: medium
layer: concepts
status: active
---

# Track Classification and Research Gap Detection

> [!tip] Key Insight
> **"내 도메인의 어디가 비어있는가"** 를 wiki 가 자동 발견. 표준 `/ingest` 가 단순 ingest 만 한다면, 본 패턴은 **2 개 보조 명령어** 로 확장: (1) thematic track 분류, (2) 트랙별 비중 비교 → 가장 빈 곳 = 연구 갭. Systematic review · 시장 분석 · 콘텐츠 기획 등 **typology-driven** 도메인에 일반 적용.

---

## Overview

**Track Classification and Research Gap Detection** 은 LLM Wiki 의 표준 `/ingest` 를 확장하는 **2 개 보조 명령어 패턴**:

1. **트랙 분류 명령어** — 논문·자료 ingest 시 미리 정의된 thematic track 으로 분류
2. **리서치 갭 판단 명령어** — 트랙별 비중 (%) 비교 → 가장 낮은 트랙 = research gap 식별

학습자가 자기 도메인에 맞춰 **자체 추가** 한 cohort-level skill contribution 의 일반화.

---

## 작동 원리

### Step 1: Track 정의
사용자가 도메인의 thematic track 을 사전 정의:

```
예시 — 어떤 헬스케어 도메인의 5 트랙:
- 인지 자극 (cognitive stimulation)
- 신체 활동 (physical activity)
- 사회적 상호작용 (social engagement)
- 영양 개선 (nutrition)
- 기술 보조 (assistive technology)
```

### Step 2: Ingest 시 분류
`/ingest` 호출 시 Claude 가 raw source 의 본문을 읽고 어느 트랙에 해당하는지 자동 분류 → frontmatter `track` 필드에 기록.

### Step 3: 그래프 적재
트랙별 wiki 페이지 (혹은 MOC) 에 backlink 생성. 트랙 노드에서 그 트랙에 속한 모든 raw source 가 한눈에 보임.

### Step 4: Gap 분석
별도 명령으로 트랙별 raw source 비중 (%) 집계 → 비중 최저 트랙 보고:

```
트랙 A: 45%
트랙 B: 30%
트랙 C: 12%   ← Research Gap
트랙 D: 8%    ← Research Gap
트랙 E: 5%    ← Research Gap (최우선)
```

→ "트랙 E 분야는 5% — 이 분야의 논문·자료를 수집할 때 우선순위" 식으로 연구 방향 자동 권고.

---

## 구현 권장 사항

### Backlink as primary signal
트랙 분류가 단순 frontmatter 필드만 채우는 게 아니라, **트랙별 개념 노트에 해당 트랙 정보가 멘션 (backlink)** 으로 기록되어야 그래프 쿼리 분석이 가능. Frontmatter 만으로는 옵시디언 그래프 뷰가 연결 인식 안 함.

### Ingest 통합 vs 별도 명령
- 옵션 A: `/ingest` 자체에 분류 통합 (단순)
- 옵션 B: `/track classify <file>` 별도 명령 (재처리 가능)
- 권장: 둘 다 — 처음 ingest 시 자동 분류, 나중에 트랙 정의 변경되면 재분류 가능

### Track 정의 자동 추천
사용자가 직접 트랙 정의 어려우면 LLM 에 도메인 ("치매 예방" · "안티에이징") 만 입력 → 적절한 트랙 5-7 개 자동 추천 받기.

---

## 적용 가능 도메인

| 도메인 | Track 예시 |
|------|----------|
| Systematic Review | PRISMA stage (identification·screening·eligibility·inclusion) |
| 헬스케어 mechanism | 분자·세포·조직·시스템·임상 |
| 시장 분석 | 지역 (Korea·Japan·China) × 차원 (특허·매출·인력) |
| 콘텐츠 기획 | 사용자 segment × 채널 × 주제 |
| 학습 분야 | 입문·중급·고급·전문가 단계 |

→ **typology 가 명확한** 모든 도메인.

---

## Systematic Review 와의 정렬

이 패턴은 본질적으로 **systematic review 의 PRISMA flow** 의 자동화. PRISMA 의 inclusion/exclusion 자동 판정도 같은 메커니즘.

→ Starter Kit 에 **systematic review 모드** 로 묶어 배포 가능 (PRISMA 단계 분류 + 단계별 비중 시각화).

---

## 제안 — `/track` skill (예시)

```
/track init [domain]      # 새 도메인의 트랙 정의 wizard
/track classify <raw>      # 단일 raw source 트랙 분류
/track gap                # 트랙별 비중 + research gap 보고
/track migrate             # 기존 raw sources 트랙 일괄 분류 (마이그레이션)
```

→ 본 concept 을 정식 skill 로 구현하면 cohort 전원이 동일 어법으로 사용 가능.

---

## Related

- [[Ingest-Query-Lint Cycle]] — 확장 대상
- [[Idea Generation Pipeline]] — 보완 패턴 (수집 vs 발산)
- [[LLM Wiki Pattern]]

---

## Open Questions

> [!question] 트랙 정의의 자동화
> Domain 만 입력 (예: "치매 예방") 하면 LLM 이 적절한 트랙 5-7 개를 추천하는 메타 skill 가능?

> [!question] 멀티 트랙 Source
> 한 논문이 여러 트랙에 속할 때 어떻게 비중 계산? 0.5 씩 분배 vs 우선순위 1 트랙만 vs 모든 트랙에 1.0.

> [!question] Cohort 표준화
> Cohort 학습자 전원이 자기 도메인의 트랙 5-7 개를 정의하고 LLM Wiki 에 등록하면, **도메인 간 비교** 가 가능 — 트랙 구조 자체가 학습 outcome.
