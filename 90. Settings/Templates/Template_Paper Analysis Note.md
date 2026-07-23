---
type: paper-analysis
aliases:
  - "{Surname} {Year} S{NN}"
description: "{English one line on the single question this atom answers.}"
author:
  - "{Agent}"
model: "{model-id}"
effort: "{effort-level}"
date created: "{{date}}T00:00"
date modified: "{{date}}T00:00"
tags:
  - paper-analysis
  - "{paperType}"
paperType: "{paperType}"
citekey: "{authYearShorttitle}"
analysisStep: 0 # ← 2~12 로 교체
analysisStepName: "{step name verbatim from 12-Step Analysis Schemes}"
paperHub: "[[{Surname} {Year} - S00 Hub]]"
source:
  - "[[{Raw Source}]]"
related:
  - "[[{sibling atom}]]"
status: completed
explored: false
verificationStatus: unverified
---

# {Surname} {Year} - S{NN} {제목}

> [!info] Analysis Context
> **Paper**: {저자} ({연도}), *{논문 제목}* — [[{Surname} {Year} - S00 Hub|허브]] · [[{YYYY-MM-DD-Paper-Title}|원문]]
> **수집 맥락**: "{collectionPurpose 요지}" → [[RQ-{slug}]] (없으면 "단순 수집")
> **위치**: Step {N} / 12 — {단계명} ({paperType}) · 원문 §{담당 섹션}
> **이 원자**: {이 노트가 답하는 하나의 질문 — 예: "background relation 이란 무엇이고 왜 이 논증에 결정적인가"}. 인접 원자: [[{...}]] · [[{...}]]

> [!note] Exposition Contract
> 이 노트는 지식 원자 1개 — 정확히 하나의 질문에 답한다. 이 노트만 읽으면 (a) 담당 원문 대목을 다시 열 필요가 없고, (b) 이 개념을 몰랐던 독자가 이해하게 되어야 한다. 하위 개념이 문단 이상 필요해지면 하위 원자로 분리하라.

---

## 쉬운 도입

{이 개념·주장을 **모르는 독자**에게 1~2문단, 일상 언어로: 무엇인지, 논문에 왜 등장하는지. 고맥락 용어 사용 금지 — 쓰려면 즉시 풀 것.}

---

## 정밀 해설

{원저자의 정의·논지·전개를 정확하게. 개념 간 차이의 **메커니즘**까지 명시 ("A 만으로 B 가 되지 않는 이유는 ..."). 하위 개념이 커지면 → [[하위 원자]] 분리 + 링크. 중첩 리스트 들여쓰기는 TAB.}

- {논점 — 원저자의 전개 순서 존중}
	- {하위 논점}

---

## 예시

{원문 예시 전부 보존 (아래 원문 근거의 quote 와 연동). 이해에 필요한 분석자 예시는 반드시 구분:}

- {원문의 예시}
- 【분석자 주】 {이해를 돕기 위한 보충 예시·비유 — 원저자의 것이 아님을 명시}

---

## 원문 근거

{이 원자의 핵심 문장마다 quote 콜아웃 (통상 2~6개). verbatim — Raw Source `## Original Content` 에서 grep 대조 가능해야 함. locator 는 페이지 우선 (Zotero PDF 있으면 `p.N` 복원), 유실 시 섹션만.}

> [!quote] 원문 (p.{페이지}, §{섹션})
> "{Raw Source ## Original Content 에서 verbatim}"

---

## 개념 관계

{이 원자가 논문 전체 논증에서 하는 역할 + 인접 원자·Wiki 개념과의 구분·연결. **가로 wikilink 의무** — 허브 경유가 아닌 형제 원자로 직접 연결 (최소 1개).}

- 논증 내 역할: {이 원자가 없으면 논문의 어떤 주장이 무너지는가}
- [[{인접 원자}]] 와의 관계: {구분점 또는 연결 메커니즘}
- Wiki: [[{승격된 개념 페이지}]]

---

## 내 원고 맥락

{선택 — targetManuscript RQ 관점의 해석·활용·주의. 이 섹션이 없어도 위 섹션들은 자립적으로 완전해야 한다.}

- 인용 예정: "{초안 문장 후보}" — 위 quote 와 대조
- 주의: {한계·조건 — 관련 S11 원자 링크}

---

## Open Questions

> [!question] Open Question
> {원문 재확인 필요 지점, 불명확한 부분}
