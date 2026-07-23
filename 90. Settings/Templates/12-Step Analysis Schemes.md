---
type: documentation
aliases:
  - 12-Step Analysis Schemes
  - 12단 분석 스킴
  - Paper Analysis Schemes
description: "Unified specification of the 12-step paper analysis scheme across six social-science paper types including quantitative, qualitative, theory-concept, mixed-methods, scale-development, and meta-analysis. Loaded by Paper Ingest Mode at step P-1 to drive hub and step-note compilation."
author:
  - Claude
date created: 2026-07-09T00:00
date modified: 2026-07-09T00:00
tags:
  - system
  - template
  - paper-analysis
  - 12-step
status: active
---

# 12-Step Analysis Schemes

**`/ingest` Paper Ingest Mode 의 단일 스펙 파일.** P-1 에서 논문 유형이 확정되면 이 파일의 해당 유형 섹션을 로드해 허브 + 단계 노트를 컴파일한다.

> [!info] Source
> 원형은 quantitative/qualitative 12-step 템플릿 (대학원 연구방법론 교재 부록의 "12 Steps to Understanding a Research Report") 이며, theory-concept / mixed-methods / scale-development / meta-analysis 변형은 킷 사용자가 사회과학 커뮤니케이션 논문 전반을 커버하도록 확장한 것이다. 원본의 "한 장 회상용 기록" 철학은 LLM 컴파일에서 "상세 분석 + 원문 verbatim 인용" 으로 대체된다 — 사람의 회상이 아니라 집필·팩트체크·paraphrasing 대조가 목적이기 때문.

---

## 공통 골격 (모든 유형 동일한 12 좌표)

| S | 공통 단계명 | 좌표의 의미 |
|---|------------|------------|
| 1 | CITATION | 완전한 서지 — **항상 허브 (S00 Hub) 가 보유**, 단계 노트 없음 |
| 2 | PURPOSE AND GENERAL RATIONALE | 연구의 큰 목적과 일반적 중요성 근거 |
| 3 | FIT AND SPECIFIC RATIONALE | 기존 문헌 속 위치와 구체적 정당화 |
| 4 | PARTICIPANTS (유형별 변형) | 누구를/무엇을 연구했나 — 유형에 따라 표본/개념/코퍼스 |
| 5 | CONTEXT (유형별 변형) | 연구가 일어난 장소·상황·적용 범위 |
| 6 | STEPS IN SEQUENCE (유형별 변형) | 절차·논증·설계·개발·리뷰의 순서 |
| 7 | DATA (유형별 변형) | 데이터·문항·논증 재료·추출 항목 |
| 8 | ANALYSIS (유형별 변형) | 분석·통합·개념 작업·종합 방식 |
| 9 | RESULTS (유형별 변형) | 주요 결과·산출물·메타 추론 |
| 10 | CONCLUSIONS | 결과가 S02 의 목적에 어떻게 응답했는가 |
| 11 | CAUTIONS (유형별 변형) | 저자의 경고 + 분석자의 유보 |
| 12 | DISCUSSION / WRITING VALUE | 내 연구·글쓰기에 바로 가져갈 것 |

**12단은 파일 수가 아니라 좌표계 (axis) 다.** 노트의 단위는 원문 섹션이 아니라 **지식 원자 (knowledge atom)** — 개념·주장·구분·메커니즘·사례 하나 = 노트 하나 — 이고, 모든 원자 노트가 정확히 하나의 `analysisStep` 좌표를 가진다. 축당 원자 수는 무제한 (논문 하나 = 원자 30~100+ 정상). 병합 노트 (S08+S09 겸용) 금지.

> [!warning] Coverage & Exposition Contract (v3) — 모든 유형에 우선 적용
> 12단 분석의 존재 이유: **"이 노트들만 읽으면 원문을 두 번 다시 열지 않아도 되고, 원문보다 더 잘 이해된다."**
> 1. **원자화 (atomization)**: 컴파일 전에 원문 섹션 → 지식 원자 분해를 설계한다 (허브 Coverage Map, 2단). 밀도 높은 섹션 하나 = 원자 3~10개가 정상. 원자 판별 질문: *"이 노트는 정확히 하나의 질문에 답하는가?"* 하위 개념이 문단 이상의 해설을 요구하면 하위 원자로 **재귀 분해**. "내 연구에 필요한 부분만" 선별은 정보 손실.
> 2. **해설 의무 (exposition)**: 각 원자는 그 개념을 처음 보는 독자를 이해 상태로 데려간다 — 아래 표들의 질문에 "원문 표현 재배열" 로 답하면 실패. 용어를 풀고, 개념 간 차이의 메커니즘을 밝히고, 예시를 든다. 원문에 충실 = 논지의 보존이지 난이도의 보존이 아니다.
> 3. **원저자 우선 + 왜곡 금지**: 정의·주장·예시는 verbatim 인용으로 고정 (원자당 2~6개 `[!quote]`), 분석자 보충은 【분석자 주】 구분. 재인용·표절 체크가 이 노트 위에서 이루어진다.
> 4. **내 맥락 = 레이어**: 완전한 원자 분해 + 해설 위에 얹는다. 필터가 아니다.
> 5. **분량·토큰 제한 없음**: 아래 표들의 질문은 각 축이 다뤄야 할 **최소** 범위다. 원본 수작업 템플릿의 "한 장 회상용" 지침은 LLM 컴파일에 적용하지 않는다.

---

## Type A — Quantitative (양적연구)

| S | 단계명 | LLM 컴파일 지침 |
|---|--------|----------------|
| 1 | CITATION | 완전한 reference citation 을 허브에 기록 (APA 등 원문 표기 그대로 + DOI) |
| 2 | PURPOSE AND GENERAL RATIONALE | 연구의 폭넓은 목적은 무엇이며, 저자는 그 일반적 중요성을 어떻게 정당화했는가 |
| 3 | FIT AND SPECIFIC RATIONALE | 이 주제가 기존 연구 문헌에 어떻게 맞물리며, 그 계보가 이 연구의 구체적 근거로 어떻게 사용되는가 |
| 4 | PARTICIPANTS | 누가 연구되었나 — 수와 특성, 선정·표집 방식 |
| 5 | CONTEXT | 연구가 이루어진 장소와 그곳의 중요한 특성 |
| 6 | STEPS IN SEQUENCE | 수행 순서대로 주요 절차 단계 — 순서와 단계 간 관계를 기술 (필요 시 Mermaid flowchart, 라벨은 큰따옴표) |
| 7 | DATA | 무엇이 데이터였나 (검사 점수, 설문 응답, 빈도 등), 수집 방식, 수집 과정에서 연구자의 역할 |
| 8 | ANALYSIS | 어떤 분석을 썼고 어떤 질문에 답하도록 설계됐나 — 통계 기법·소프트웨어 명시 |
| 9 | RESULTS | 저자가 제시한 1차 결과 — 통계치는 원문 verbatim 인용 필수 (β, p, CI 등) |
| 10 | CONCLUSIONS | 결과가 S02 의 목적에 어떻게 응답한다고 저자가 주장했는가 |
| 11 | CAUTIONS | 저자가 밝힌 한계 + 분석자의 유보 (설계·표본·해석) |
| 12 | DISCUSSION / WRITING VALUE | 결과·설계·참고문헌·도구·이론·영감 등 가치 있는 모든 것 — targetManuscript 관점에서 재서술 |

**핵심 단계 (progressive 기본값)**: S02 · S03 · S08 · S09 · S12

## Type B — Qualitative (질적연구)

| S | 단계명 | LLM 컴파일 지침 |
|---|--------|----------------|
| 1 | CITATION | 완전한 서지 (허브) |
| 2 | PURPOSE AND GENERAL RATIONALE | Type A 와 동일 |
| 3 | FIT AND SPECIFIC RATIONALE | Type A 와 동일 |
| 4 | PARTICIPANTS | **연구자 자신의 특성부터** — 저자는 누구이며 목적·참여자·현장과 어떤 관계인가. 이어서 참여자 수·특성·선정 방식 |
| 5 | CONTEXT | 연구 현장과 중요한 특성 |
| 6 | STEPS IN SEQUENCE | 절차 단계 — 순서 + **소요 시간** + 단계 간 관계 |
| 7 | DATA | 무엇이 데이터였나 (필드노트, 인터뷰 전사, 사진, 일기 등), 수집 방식, 연구자의 역할 |
| 8 | ANALYSIS | 어떤 분석이며 무엇을 드러내도록 설계됐나 — 사용 소프트웨어 (있다면) |
| 9 | RESULTS | 1차 발견 — 일반적으로 "그 현장에서 무엇이 일어나고 있었는가". 핵심 인용문은 원문 verbatim |
| 10 | CONCLUSIONS | Type A 와 동일 |
| 11 | CAUTIONS | 저자의 경고 + 분석자의 유보 — **특히 신뢰성 (trustworthiness·believability) 강화 방법 관련** |
| 12 | DISCUSSION / WRITING VALUE | Type A 와 동일 |

**핵심 단계 (progressive 기본값)**: S02 · S04 · S08 · S09 · S12

## Type C — Theory & Concept Paper (이론·개념 논문)

| S | 단계명 | LLM 컴파일 지침 |
|---|--------|----------------|
| 1 | CITATION | 완전한 서지 (허브) |
| 2 | PURPOSE AND GENERAL RATIONALE | 이 논문이 풀려는 큰 문제는 무엇인가 |
| 3 | FIT AND SPECIFIC RATIONALE | 기존 이론·개념 논의의 어떤 빈칸, 충돌, 모호함을 겨냥하는가 |
| 4 | CORE CONSTRUCTS / KEY CONCEPTS | 핵심 개념은 무엇인가 — 각 개념의 정의 (원문 verbatim 인용), 비슷한 개념과의 구분 |
| 5 | SCOPE CONDITIONS / INTELLECTUAL CONTEXT | 이 이론은 어디까지 적용되는가 — 어떤 상황·수준·조건에서만 맞는가 |
| 6 | ARGUMENT IN SEQUENCE | 논리 흐름을 순서대로 — 예: 문제 제기 → 기존 이론 비판 → 개념 재정의 → 작동 방식 제시 → 명제 (propositions) 제안 |
| 7 | BUILDING BLOCKS / EVIDENTIARY BASE | 무엇을 재료로 논리를 세우는가 — 기존 연구, 철학자, 고전 이론, 사례 예시 |
| 8 | CONCEPTUAL WORK DONE | 실제로 수행한 개념 작업 — 정의 재정리 / 개념 통합 / 개념 분리 / 유형화 / 작동 방식 제시 / 명제 제안 중 무엇 |
| 9 | MAIN OUTPUTS | 최종 산출물 — 새 틀 (framework), 모형 (model), 유형표 (typology), 명제, 개념 지도 |
| 10 | CONCLUSIONS | 이 논문이 결국 새롭게 보게 만든 것 |
| 11 | CAUTIONS / BOUNDARY CONDITIONS | 검증 안 된 주장인가, 너무 넓거나 모호한가, 실증 연구로 이어지기 어려운가 |
| 12 | DISCUSSION / WRITING VALUE | 바로 쓸 수 있는 것 — 정의 문장, 인용할 문장, 이론 틀 그림, 가설로 바꿀 명제, 개념 구분 방식 |

**핵심 단계 (progressive 기본값)**: S04 · S06 · S08 · S09 · S12
**특히 유용한 시점**: 서론 개념 정리 / literature review 의 개념 싸움 정리 / "내 연구의 이론적 위치" 설정

## Type D — Mixed Methods (혼합방법연구)

| S | 단계명 | LLM 컴파일 지침 |
|---|--------|----------------|
| 1 | CITATION | 완전한 서지 (허브) |
| 2 | PURPOSE AND GENERAL RATIONALE | 왜 혼합방법이 필요했는가 — 양적만으로 부족했던 점, 질적만으로 부족했던 점 |
| 3 | FIT AND SPECIFIC RATIONALE | 이 주제가 기존 연구에서 어떻게 다뤄졌고, 왜 혼합이 필요한가 |
| 4 | PARTICIPANTS / DATA SOURCES FOR BOTH STRANDS | 양적 표본은 누구, 질적 참여자는 누구 — 같은 집단인가 다른 집단인가 |
| 5 | CONTEXT | 두 자료가 나온 맥락이 같은가 다른가 |
| 6 | DESIGN IN SEQUENCE | **핵심.** 설계 유형 판별 — explanatory sequential (양적 후 질적 설명) / exploratory sequential (질적 후 양적 확장) / convergent (동시 수렴) / embedded (내장) |
| 7 | DATA | 양적 자료 / 질적 자료를 나눠 기술 + **둘이 어디서 만나는지** |
| 8 | ANALYSIS AND INTEGRATION | 양적 분석 · 질적 분석 · 통합 방식 — merging / connecting / building / joint display |
| 9 | RESULTS / META-INFERENCES | 양적 결과와 질적 결과가 서로 확인하는가 / 충돌하는가 / 보완하는가 / 새 해석을 만드는가 |
| 10 | CONCLUSIONS | 혼합 덕분에 무엇을 더 잘 이해하게 되었는가 |
| 11 | CAUTIONS | 양적/질적 중 한쪽이 약한가 · 나란히만 놓고 진짜 통합은 안 했는가 · 이름만 mixed 인 분리된 두 연구인가 |
| 12 | DISCUSSION / WRITING VALUE | 혼합 설계 방식, joint display 아이디어, 후속 연구 설계 힌트 |

**핵심 단계 (progressive 기본값)**: S06 · S08 · S09 · S12
**핵심 판별 질문**: "양적이 맞았는가", "질적이 풍부한가" 보다 — **"둘이 만나서 무엇을 새로 만들었는가"**

## Type E — Measurement & Scale Development (척도개발연구)

| S | 단계명 | LLM 컴파일 지침 |
|---|--------|----------------|
| 1 | CITATION | 완전한 서지 (허브) |
| 2 | PURPOSE | 무엇을 측정하려고 하는가, 왜 새 척도가 필요한가 |
| 3 | FIT AND RATIONALE | 기존 척도의 한계, 비슷한 구성개념과의 구분 |
| 4 | SAMPLES / PARTICIPANTS ACROSS STUDIES | 파일럿 · 탐색 · 확인 · 재검증 등 **여러 표본을 연구별로 구분해서** 기록 |
| 5 | CONTEXT OF USE | 어떤 집단, 문화, 언어, 상황에서 쓰는 척도인가 |
| 6 | DEVELOPMENT PROCESS IN SEQUENCE | 문항 생성 → 전문가 검토 → 예비조사 → EFA → CFA → 타당도 검증 → invariance 검토 흐름 |
| 7 | DATA / ITEMS | 몇 문항 · 응답 척도 · 하위요인 · 역문항 · 삭제된 문항 — **문항 전문 verbatim 수록은 저작권 주의** (공개 척도만, 아니면 요약+출처) |
| 8 | ANALYSIS | EFA/CFA · 신뢰도 (alpha, omega) · 수렴/판별 타당도 · 준거 타당도 · 측정동일성 (invariance) · 번역/역번역 여부 |
| 9 | RESULTS | 최종 요인 수·문항 수, 적합도 지수 (원문 verbatim), 실용성 |
| 10 | CONCLUSIONS | 이 척도가 연구자에게 열어 주는 것 |
| 11 | CAUTIONS | 특정 집단에서만 검증 · 문화 번역 문제 · 짧은 척도의 얕음 · 자기보고 편향 |
| 12 | DISCUSSION / WRITING VALUE | 가져다 쓸 수 있는 문항, 번역 시 주의점, 비슷한 척도와의 차이, 조작적 정의 |

**핵심 단계 (progressive 기본값)**: S06 · S07 · S08 · S09 · S12
**Wiki 승격**: 이 유형은 척도 자체가 산출물 — `21. Concepts/` (layer: scale) 페이지 (Template_Scale Page) 생성이 사실상 의무

## Type F — Meta-analysis & Systematic Review (메타분석·체계적 문헌고찰)

| S | 단계명 | LLM 컴파일 지침 |
|---|--------|----------------|
| 1 | CITATION | 완전한 서지 (허브) |
| 2 | PURPOSE AND REVIEW QUESTION | 이 리뷰가 답하려는 질문 |
| 3 | FIT AND RATIONALE | 왜 지금 이 리뷰가 필요한가, 기존 리뷰의 한계 |
| 4 | CORPUS / STUDY SET | 포함 논문 수, 검색 기간·데이터베이스, 포함/제외 기준 |
| 5 | CONTEXT OF THE REVIEWED FIELD | 어떤 분야·대상·나라·상황의 연구들을 묶었는가 |
| 6 | REVIEW PROCESS IN SEQUENCE | 검색 → 중복 제거 → 초록 확인 → 본문 심사 → 최종 포함 → 코딩 → 종합 (PRISMA 흐름이면 수치까지) |
| 7 | DATA EXTRACTED FROM STUDIES | 각 논문에서 추출한 것 — 효과크기 · 표본 정보 · 변수 · 조절변수 · 중재변수 · 연구 설계 · 측정 방식 |
| 8 | ANALYSIS / SYNTHESIS | 체계적 고찰: 주제별 묶음 · 질 평가 · 서술 종합 / 메타분석: 효과크기 계산 · 랜덤/고정 효과 · 이질성 · 출판 편향 · 메타회귀 — **둘은 S08·S09 에서만 분기** |
| 9 | RESULTS | 전반 효과 · 일관된 패턴 · 조절효과 · 중재효과 · 연구 부족 지점 (효과크기는 원문 verbatim) |
| 10 | CONCLUSIONS | 이 분야에서 지금 비교적 확실한 것 / 아직 불확실한 것 |
| 11 | CAUTIONS | 포함 연구의 질 · 나라/표본 편중 · 출판 편향 · 과도한 이질성 (사과와 오렌지) |
| 12 | DISCUSSION / WRITING VALUE | 분야 전체 지도, 대표 고전/핵심 연구, 자주 쓰인 변수, 빠진 대상/맥락, 후속 연구 제안 문장 |

**핵심 단계 (progressive 기본값)**: S04 · S08 · S09 · S10 · S12

---

## 원자 분해·생략 규칙 (모든 유형 공통, v3)

- **기본 단위 = 지식 원자.** 개념 정의 / 독립 주장 / 개념 간 구분 / 작동 메커니즘 / 사례 / 방법 요소 / 수치 결과 각각이 원자 후보. 원자 판별 질문: *"이 노트는 정확히 하나의 질문에 답하는가?"* — 두 개 이상의 질문에 답하면 쪼갠다.
- **재귀 분해**: 해설 중 등장한 하위 개념이 문단 이상의 해설을 요구하면 하위 원자로 분리 + 상호 링크. 이론 → 구성 개념 → 하위 개념 → 작동 조건, 어느 깊이든. (예: 기술 매개 이론 → Ihde 4관계 → background relation 각각이 별도 원자가 될 수 있다.)
- **과소 분해 경보**: 밀도 높은 원문 섹션이 원자 1~2개로 뭉치면 under-decomposition — 재검토.
- **생략 조건**: 해당 유형에서 내용이 실질적으로 없는 축은 원자 0개 허용 — 단, 허브 Step Map 에 `skipped (사유)` 명기. 조용한 생략 금지.
- **병합 금지**: 모든 원자는 단일 `analysisStep` 좌표. "S08+S09 통합 노트" 는 만들지 않는다.
- **S01 은 항상 허브가 보유** — CITATION 원자를 따로 만들지 않는다.
- **자리가 애매한 원문 섹션** (case studies, 부록, 방법론적 여담 등) 도 원자로 분해해 가장 가까운 축에 배정 — 사례는 통상 S07 (BUILDING BLOCKS — 사례는 논증의 재료). Coverage Map 에 구멍을 남기는 것보다 근사 배정이 낫다.

## Decomposition Heuristics (유형별 분해 휴리스틱, v1.10)

P-3a Blueprint 의 **규모 가늠용** — blank 세션이 "이 유형은 어느 축이 팽창하고, 무엇이 원자 1개가 되는가" 를 즉시 캘리브레이션하기 위한 표. 원자 판별 질문 (*"정확히 하나의 질문에 답하는가"*) 이 항상 우선하고, 이 휴리스틱은 그 다음이다.

| 유형 | 팽창 축 (원자 다수 예상) | 전형적 원자 유형 | 교차 분해 패턴 |
|------|------------------------|-----------------|---------------|
| A quantitative | S07 (변수·척도 각각) · S08 (분석 단위: 측정모형/구조모형/직접효과/매개/조절 각각) · S09 (가설 각각의 결과) | 가설 1개 = 원자 1개 · 통계 모형 1개 = 원자 1개 · 척도 1개 = 원자 1개 | 가설 × 결과, 변수 × 측정 |
| B qualitative | S08 (코딩 절차 단계) · S09 (주제 theme 각각) | theme 1개 = 원자 1개 (하위 코드는 하위 원자) · 인용 발췌 뭉치는 theme 원자에 귀속 | theme × 근거 발췌 |
| C theory-concept | S04 (구성 개념 + 하위 개념 재귀) · S09 (명제·원칙 각각) · S07 (사례 × 분석 조건) | 개념 정의 1 = 원자 1 · 개념 간 구분 1 = 원자 1 · 명제/원칙 1 = 원자 1 | **사례 × 조건 교차** (예: 사례 2개 × 분석 조건 3개 = 원자 6개) |
| D mixed-methods | S06 (설계 유형·시퀀스) · S08 (양적 분석/질적 분석/통합 각각) · S09 (메타 추론 각각) | strand 별 결과 = 각 원자 + 통합 지점 = 별도 원자 | strand × 만남 지점 |
| E scale-development | S07 (문항 pool·차원 각각) · S08 (EFA/CFA/신뢰도/타당도 단계 각각) | 타당도 증거 유형 1개 = 원자 1개 | 차원 × 검증 단계 |
| F meta-analysis | S04 (포함 연구군 특성) · S08 (효과크기 통합·이질성·출판편향 각각) · S09 (조절변수 분석 각각) | 효과크기 1 클러스터 = 원자 1개 | 조절변수 × 효과 |

**공통 규칙**: 원자 판별 질문이 항상 휴리스틱에 우선한다. 휴리스틱은 규모 가늠용 — 7K 단어 이론 논문 ≈ 원자 70~80개가 실증 기준점이되, **단어 수 대비 원자 수를 기계적으로 비례시키지 말 것** — 기준은 밀도다. 밀도 높은 섹션이 원자 1~2개로 뭉치면 under-decomposition (재검토), 원자 수가 30 미만이면 팬아웃 배치 수를 비례 축소 (Execution Strategy 참조).

## 6유형 밖 논문 (서평 · 에디토리얼 · 방법론 튜토리얼 등)

가장 가까운 유형을 적용하고 허브에 편차를 기록한다 (예: 방법론 튜토리얼 → Type A 적용 + 허브에 "S04/S05 skipped — 튜토리얼이라 표본 없음"). **7번째 유형을 신설하지 않는다** — scheme 안정성이 우선.
