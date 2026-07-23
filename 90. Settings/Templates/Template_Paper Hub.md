---
type: paper-hub
aliases:
  - "{Surname} {Year} Hub"
description: "{English summary of the paper and the scope of its 12 step analysis.}"
author:
  - "{Agent}"
model: "{model-id}"
effort: "{effort-level}"
date created: "{{date}}T00:00"
date modified: "{{date}}T00:00"
tags:
  - paper-hub
  - "{paperType}"
  - "{topic}"
paperType: "{paperType}"
citekey: "{authYearShorttitle}"
doi: "{doi}"
targetManuscript: "[[RQ-{slug}]]"
collectionPurpose: "{user answer verbatim}"
source:
  - "[[{Raw Source}]]"
related:
  - "[[RQ-{slug}]]"
explored: false
verificationStatus: unverified
status: active
---

# {Surname} {Year} - S00 Hub

> [!info] Paper Hub
> **{저자} ({출판연도})**, *{논문 제목}* — 이 논문의 12단 분석 앵커. 지식 원자는 아래 Atom Catalog, 축별 요약은 Step Map 참조.
> **수집 맥락**: "{collectionPurpose 요지}" → [[RQ-{slug}]] (없으면 "단순 수집")

> [!warning] 변환 품질
> (조건부 — 원문이 PDF·HTML→md 변환이고 품질 이슈가 있을 때만 유지, 아니면 이 콜아웃 삭제)
> 변환 방식: {arXiv HTML / OCR / Zotero PDF 추출}. 확인 필요: {수식·표·각주 유실 등}. 페이지 locator: {Zotero PDF 있음 → p.N 복원 / 없음 → 섹션만}.

---

## S01 Citation

- **Full citation**: {APA 등 완전한 서지 — 원문 표기 그대로}
- **citekey**: {authYearShorttitle}
- **DOI**: {doi 또는 없음}
- **Zotero**: zotero://select/library/items/{itemKey}
- **Raw Source**: [[{YYYY-MM-DD-Paper-Title}]]

---

## Abstract 요약

{초록의 3~5줄 요약 — verbatim 이 아니라 압축. verbatim 초록은 Raw Source 에 있음.}

---

## Coverage Map (원문 섹션 → 지식 원자 전수 분해)

{컴파일 **전에** 설계한다 (atomization first). 원문의 모든 H2/H3 섹션이 빠짐없이 나타나고, 밀도 높은 섹션은 원자 여러 개로 분해되어야 한다 — 배정 안 된 섹션 = coverage hole, 원자 1개뿐인 밀도 섹션 = under-decomposition.}

| 원문 섹션 | 지식 원자 (노트) |
|-----------|-----------------|
| Abstract | (허브 Abstract 요약) |
| §1 {...} | [[{S02 원자}]] · [[{S03 원자}]] |
| §2.1 {...} | [[{S04 원자 A}]] · [[{S04 원자 B}]] · [[{S04 원자 C}]] |
| §{...} 모든 섹션 | ... 섹션당 원자 여러 개 ... |
| References | (Raw Source 보존) |

---

## Step Map (축별 요약)

{단계명은 paperType 에 따라 다르다 — [[12-Step Analysis Schemes]] 에서 해당 유형 스킴을 로드해 채운다. Step 1 CITATION 은 항상 허브(위 S01)가 보유.}

| S | Step name | Atoms | Status |
|---|-----------|-------|--------|
| 1 | CITATION | (허브 보유) | compiled |
| 2 | {단계명} | {N} | compiled |
| 3 | {단계명} | {N} | compiled |
| 4 | {단계명} | {N} | compiled |
| 5 | {단계명} | {N} | stub {M}건 |
| 6 | {단계명} | {N} | compiled |
| 7 | {단계명} | {N} | compiled |
| 8 | {단계명} | {N} | compiled |
| 9 | {단계명} | {N} | compiled |
| 10 | {단계명} | {N} | compiled |
| 11 | {단계명} | {N} | compiled |
| 12 | {단계명} | {N} | compiled |

> Status 값: `planned` (P-3a Blueprint 직후 초기값 — 원자 미작성) / `compiled` / `stub {M}건` (progressive 대기 — `/ingest {노트 경로}` 로 승격) / `skipped (사유)`. P-3b 허브 마무리에서 `planned` 를 전부 해소한다 — 잔존 시 `p7_verify.py` 가 FAIL.

---

## Atom Catalog (원자 카탈로그 — 축별 전체 색인)

### S02 — {단계명} ({N} atoms)

- [[{Surname} {Year} - S02 {원자 제목}]] — {1줄: 이 원자가 답하는 질문}

### S04 — {단계명} ({N} atoms)

- [[{Surname} {Year} - S04 {원자 A}]] — {1줄}
- [[{Surname} {Year} - S04 {원자 B}]] — {1줄}
	- [[{Surname} {Year} - S04 {원자 B 의 하위 원자}]] — {1줄, 들여쓰기(TAB)로 재귀 깊이 표현}

{... S12 까지 전 축 반복. 이 카탈로그가 허브의 본체 — 모든 원자 노트가 여기 나타나야 한다.}

---

## Target Manuscript

{RQ redirect — 이 볼트에는 별도 원고 파일이 없다. 기여 대상은 RQ 카드(`type: research-question`)다.}

- [[RQ-{slug}]] — {이 논문이 그 RQ 에 기여하는 지점 1줄: evidenceFor / evidenceAgainst / cites 중 무엇으로}
- 없으면: `targetManuscript: none` + "단순 수집 (12단 분석만)"

---

## Wiki Promotions

{재사용 개념은 `20. Wiki/21. Concepts/` 로 승격하고 `layer:` 로 구분한다 (별도 25/26/27 폴더 없음). 척도 페이지는 `measuredConstruct`·`itemCount` + Psychometrics 표 + 저작권 콜아웃.}

- 이론: [[{Theory Page}]] (21. Concepts · layer: theory)
- 방법: [[{Method Page}]] (21. Concepts · layer: method)
- 척도: [[{Scale Page}]] (21. Concepts · layer: scale)
- 개념: [[{Concept Page}]] (21. Concepts · layer: concepts)
- 저자·저널: [[{Entity Page}]] (22. Entities)

---

## Related

- {같은 targetManuscript RQ 를 공유하는 다른 Paper Hub, 같은 이론·척도를 쓰는 논문 등}

---

> [!note] Compile Plan
> (P-3a 임시 산출물 — P-3b 허브 마무리에서 **삭제**. 잔존 시 `p7_verify.py` FAIL.)
> **원자 채굴 지점**: {원문 섹션 → 원자 매핑 초안 (Coverage Map 근거)}
> **가로 링크 설계**: {원자 간 [[…]] 직접 연결 계획 — 허브 경유 아님}
> **팬아웃 배치**: {축별 5~9 원자/배치. 실행 전략 ① parallel fan-out (기본) / ② importance-order 단일 / ③ progressive stub (>15K 단어)}
