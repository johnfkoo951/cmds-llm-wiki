# Paper Ingest Guide — 논문 12단 분석 매뉴얼

| 항목 | 내용 |
|------|------|
| 대상 | `cmds-llm-wiki` v1.10.0+ |
| 작성 | 2026-07-23 |
| 전제 | `/ingest` 사용 경험 · (권장) Research Question 카드 이해 (`Setup Guide` FAQ 참고) |

---

## 1. Paper Ingest Mode 는 무엇이 다른가

Standard `/ingest` 는 소스를 **10~15개 주제 위키 페이지**로 쪼갠다 — 위키 전체의 관점에서 소스를 흡수하는 방식이다. **Paper Ingest Mode 는 논문 한 편을 논문-스코프로 완전 해부**한다:

```
1 Raw Source (원문 verbatim)
  → 1 Paper Hub (S00 — 분석 앵커)
  → N 지식 원자 (S02~S12 좌표를 가진 노트, 논문당 30~100+)
  → 소수 Wiki 승격 (재사용 개념·이론·척도)
```

**왜 이렇게까지 하나**: 12단 노트는 회상용 요약이 아니라 **집필 시 인용·팩트체크·paraphrase 대조의 대상**이다. 논문을 쓰다가 "그 논문에서 β 값이 뭐였지", "그 정의의 원문 표현이 뭐였지" 를 원문 PDF 를 다시 열지 않고 노트에서 verbatim 으로 꺼내는 것이 목표다.

**성공 기준 (Coverage & Exposition Contract)** — 두 겹:
- **(a) Coverage**: 이 노트들만 읽으면 원문을 두 번 다시 열지 않아도 된다.
- **(b) Exposition**: 원문보다 더 잘 이해된다 — 용어를 풀고, 개념 차이의 메커니즘을 밝히고, 예시를 든다.

## 2. 핵심 개념 3가지

**① 지식 원자 (knowledge atom)** — 노트의 단위는 원문 "섹션" 이 아니다. 개념 정의 하나, 독립 주장 하나, 개념 간 구분 하나, 작동 메커니즘 하나, 사례 하나 = 노트 하나. 판별 질문: *"이 노트는 정확히 하나의 질문에 답하는가?"* 두 개 이상이면 쪼갠다.

**② 12단 = 좌표계 (axis), 파일 수가 아니다** — S01~S12 는 "12개 파일을 만들라" 가 아니라 모든 원자가 갖는 **좌표**다. 밀도 높은 축(예: 양적논문의 S08 분석)에는 원자가 10개 이상 달릴 수 있고, 내용이 없는 축은 0개(허브에 `skipped (사유)` 명기)일 수 있다.

**③ 원저자 우선 + 왜곡 금지** — 정의·주장·통계치는 원자당 2~6개의 `> [!quote]` 콜아웃에 **verbatim** 으로 고정한다 (Raw Source 에서 grep 대조 가능해야 함). 분석자의 보충은 【분석자 주】 로 구분한다.

## 3. 언제 발동되나

`/ingest` 가 다음 중 하나를 감지하면 자동으로 Paper Mode 로 전환한다 (별도 확인 질문 없음):

- DOI · arXiv · 저널 URL
- Abstract + References 구조를 가진 PDF/변환 md
- `00. Inbox/02. Papers/` 의 파일
- 명시 요청: `/ingest --paper`, "논문 분석해줘"

**질문 예산은 정확히 2개** — 그 외에는 묻지 않고 진행한다:
1. **P-0**: 수집 목적 + 이 논문이 기여할 Research Question (`25. Questions/` 의 열린 RQ 를 동적 선택지로 제시)
2. **P-1**: 논문 유형 확인 (6유형 자동 분류 + confirm) 및 실행 전략

## 4. 파이프라인 한눈에 (P-0 → P-7)

| 단계 | 이름 | 하는 일 |
|------|------|---------|
| P-0 | Purpose + Scope Gate | Core Context 정렬 확인 → 수집 목적 + 타깃 RQ 질문 (질문 1) → 기존 RQ·draft 연결 탐색 |
| P-1 | Paper Type | 6유형 분류 + 실행 전략 확인 (질문 2) → `12-Step Analysis Schemes` 해당 스킴 로드 |
| P-2 | Save Raw Source | `10. Raw Sources/12. Papers/` 에 verbatim 보존 + citekey/doi 서지 기록 |
| P-3a | Decomposition Blueprint | 원문 전 섹션 → 지식 원자 분해 설계. 산출물 = 허브 초안 (Coverage Map + Step Map + Atom Catalog) |
| P-3b | Compile | SPEC 배포 → 원자 노트 작성 (병렬 fan-out 기본) → 허브 마무리 |
| P-4 | Wiki Promotion | 재사용 개념을 `21. Concepts/` 로 승격 (layer: theory/method/scale) |
| P-5 | RQ Sync | 타깃 RQ 의 `cites[]`·`evidenceFor/Against` 갱신 |
| P-6 | Index + Log | index 에 **허브만** 등록, log 기록 |
| P-7 | Review Gate | `p7_verify.py` 기계 검증 — **ALL PASS 가 통과 조건** |

## 5. 12단계 (S01~S12) — 공통 골격

모든 논문 유형이 같은 12개 좌표를 쓴다. 좌표의 의미:

| S | 공통 단계명 | 이 좌표가 답하는 것 |
|---|------------|-------------------|
| **S01** | CITATION | 완전한 서지 — **항상 허브(S00)가 보유**, 별도 노트 없음 |
| **S02** | PURPOSE AND GENERAL RATIONALE | 연구의 큰 목적은 무엇이며, 저자는 그 일반적 중요성을 어떻게 정당화했는가 |
| **S03** | FIT AND SPECIFIC RATIONALE | 이 연구가 기존 문헌의 어디에 맞물리며, 그 계보가 어떤 구체적 근거가 되는가 |
| **S04** | PARTICIPANTS *(유형별 변형)* | 누구를/무엇을 연구했나 — 유형에 따라 표본·핵심 개념·논문 코퍼스로 변형 |
| **S05** | CONTEXT *(유형별 변형)* | 연구가 일어난 장소·상황, 이론의 적용 범위 |
| **S06** | STEPS IN SEQUENCE *(유형별 변형)* | 절차·논증·설계·개발·리뷰의 **순서** |
| **S07** | DATA *(유형별 변형)* | 무엇이 데이터였나 — 자료·문항·논증 재료·추출 항목 |
| **S08** | ANALYSIS *(유형별 변형)* | 어떤 분석·통합·개념 작업을 어떤 질문에 답하도록 설계했나 |
| **S09** | RESULTS *(유형별 변형)* | 주요 결과·산출물 — **통계치·효과크기는 원문 verbatim 필수** |
| **S10** | CONCLUSIONS | 결과가 S02 의 목적에 어떻게 응답했다고 저자가 주장하는가 |
| **S11** | CAUTIONS *(유형별 변형)* | 저자가 밝힌 한계 + 분석자의 유보 |
| **S12** | DISCUSSION / WRITING VALUE | **내 연구·글쓰기에 바로 가져갈 것** — 타깃 RQ 관점에서 재서술 |

읽는 순서로 보면: S02~S03 이 "왜 이 연구인가", S04~S07 이 "무엇을 어떻게 연구했나", S08~S09 가 "무엇을 발견했나", S10~S12 가 "그래서 어떤 의미인가" 를 담당한다. **S12 가 이 시스템의 출구** — 논문에서 내 산출물로 흘러가는 지점이다.

## 6. 유형별 변형 (6유형)

P-1 에서 확정된 유형에 따라 S04~S09·S11 의 질문이 달라진다. 전체 표는 `90. Settings/Templates/12-Step Analysis Schemes.md` 에 있고, 여기서는 각 유형의 **무엇이 특별한가**만 요약한다:

| 유형 | 핵심 변형 | 핵심 축 (progressive 시 우선) |
|------|----------|------------------------------|
| **A. Quantitative** (양적) | S07=변수·척도, S08=통계 기법, S09=가설별 결과 (β·p·CI verbatim) | S02·03·08·09·12 |
| **B. Qualitative** (질적) | S04 는 **연구자 자신의 특성부터** (저자-현장 관계), S09=주제(theme)별 발견, S11=신뢰성(trustworthiness) 강화 방법 | S02·04·08·09·12 |
| **C. Theory-Concept** (이론·개념) | S04=핵심 구성 개념 각각의 정의 (verbatim), S06=논증의 순서, S08=수행된 개념 작업(정의/통합/분리/유형화/명제), S09=산출물(틀·모형·유형표·명제) | S04·06·08·09·12 |
| **D. Mixed-Methods** (혼합) | S06 이 **핵심** — 설계 유형 판별 (explanatory/exploratory sequential·convergent·embedded), S08=양적·질적·**통합** 방식, S09=메타 추론 (둘이 만나서 무엇을 새로 만들었는가) | S06·08·09·12 |
| **E. Scale-Development** (척도개발) | S04=연구별 복수 표본 구분, S06=문항 생성→EFA→CFA→타당도 흐름, S07=문항 (**저작권 주의** — 공개 척도만 verbatim), S09=요인·문항 수·적합도 verbatim. **척도 Wiki 페이지 (layer: scale) 생성이 사실상 의무** | S06·07·08·09·12 |
| **F. Meta-Analysis** (메타·체계적 고찰) | S04=포함 논문 코퍼스, S06=PRISMA 흐름 (수치까지), S07=추출 항목 (효과크기·조절변수), S08=통합 방식 (이질성·출판편향), S12=분야 전체 지도 | S04·08·09·10·12 |

6유형 밖 논문(서평·에디토리얼·방법론 튜토리얼)은 **가장 가까운 유형을 적용**하고 허브에 편차를 기록한다 — 7번째 유형은 만들지 않는다.

## 7. 산출물 구조

```
40. Paper Analyses/wu2024longMemEval/          ← citekey 폴더
├── Wu 2024 - S00 Hub.md                       ← 허브 (앵커)
├── Wu 2024 - S02 벤치마크 목적과 정당화.md      ← 지식 원자들…
├── Wu 2024 - S04 평가 대상 시스템.md
├── Wu 2024 - S08 평가 지표 분석.md
├── Wu 2024 - S09 모델별 결과.md
└── … (원자 30~100+)
```

**허브 (S00) 의 4요소** — 논문 전체의 지도:
1. **S01 Citation** — 완전한 서지 + citekey + DOI
2. **Coverage Map** — 원문 모든 섹션 → 어느 원자가 담당하는지 전수 매핑 (구멍 = coverage hole)
3. **Step Map** — 축별 원자 수와 상태 (`compiled` / `stub N건` / `skipped (사유)`)
4. **Atom Catalog** — 모든 원자의 축별 색인 (허브가 원자의 유일한 전체 목록)

**원자 노트의 섹션 구조** (순서 고정): `Analysis Context` 콜아웃 (이 원자가 논문 어디의 무엇인지 4행 자기소개) → `쉬운 도입` → `정밀 해설` → `예시` → `원문 근거` (verbatim quote 2~6개) → `개념 관계` (형제 원자와 직접 링크) → 선택: `내 원고 맥락` / `Open Questions`.

`index.md` 에는 **허브만** 등록한다 — 원자를 index 에 노출하면 index 가 비대해진다.

## 8. Research Question 연계

Paper Mode 의 P-0 은 "이 논문을 **어느 RQ 에 쓰려고** ingest 하나" 를 묻는다 (v1.9.0 의 Research Question 카드와 연동):

- 타깃 RQ 지정 → 허브 `targetManuscript: "[[RQ-…]]"` + P-5 에서 RQ 의 `cites[]`·`evidenceFor`/`evidenceAgainst` 자동 갱신
- 타깃 없음 → `targetManuscript: none` (12단 분석 자체는 진행)
- 새 질문 발견 → 그 자리에서 `25. Questions/` 에 RQ 신규 등록 가능

## 9. 실행 전략 (3옵션)

| 전략 | 언제 |
|------|------|
| **① Full 원자화 (기본)** | 통상 논문. 서브에이전트 병렬 fan-out (Claude Code) |
| **② 단일 실행 중요도순** | 서브에이전트 없는 harness (Codex CLI 등) 폴백 |
| **③ Progressive stub** | 장문(>~15K 단어) 또는 "핵심만" 요청 — 유형별 핵심 축만 full, 나머지는 stub. 나중에 `/ingest {원자 경로}` 로 개별 승격 |

## 10. Zotero 연동 (옵션)

Zotero + Better BibTeX 사용자는 citekey 자동 조회·서지 자동 채움·PDF 페이지 점프(`zotero://open-pdf/...?page=N`)를 쓸 수 있다. **미사용자도 문제 없다** — provisional citekey 를 로컬 생성하고 (`citekeyProvisional: true`), 나중에 Zotero 에 등록할 때 BBT 키를 그 값으로 PIN 하면 노트·폴더·인용 변경이 0 이다. 상세: `paper-ingest.md` §Zotero.

## 11. 검증 — P-7 게이트

분석이 끝나면 볼트 루트에서:

```bash
python3 "90. Settings/Scripts/p7_verify.py" "40. Paper Analyses/{citekey}"
```

YAML 파싱 · v6.2 키·좌표 · provenance · 필수 섹션 · 가로 링크 · **인용 전수 verbatim 대조** · Atom Catalog↔실제 파일 · Coverage 전수 · index 허브-단독을 기계 검사한다. **ALL PASS 가 통과 조건** — 컴파일한 에이전트의 "자체 검증 OK" 는 게이트가 아니다.

## 12. FAQ

**Q. 원자가 30~100개라니 너무 많지 않나?**
목적이 다르다 — 요약(회상)이 아니라 집필 시 대조다. 가볍게 훑을 논문이면 Paper Mode 대신 P-0 의 "(n+4) 단순 수집" 을 골라 Standard Ingest 로 처리하면 된다. 중간 강도는 ③ progressive stub (핵심 축만 full).

**Q. 12개 축을 다 채워야 하나?**
아니다. 내용이 없는 축은 원자 0개 — 단 허브 Step Map 에 `skipped (사유)` 를 명기한다 (조용한 생략 금지). S01 은 항상 허브가 보유하므로 원자를 만들지 않는다.

**Q. Zotero 가 없으면?**
provisional citekey 로 전부 동작한다 (§10). 인용 locator 는 페이지 대신 §섹션을 쓴다.

**Q. Mode A (standalone) 여도 되나?**
된다. 모선 관련 단계 (P-0.3 Tier 3, P-5 모선 보고) 만 자동 생략된다.

---

## 참고

- 스킴 전문 (유형별 12단 표): `90. Settings/Templates/12-Step Analysis Schemes.md`
- 파이프라인 상세 (에이전트용): `.agents/skills/ingest/resources/paper-ingest.md`
- 템플릿: `Template_Paper Hub` · `Template_Paper Analysis Note` · `Template_Atomization SPEC` · `Template_Scale Page`
- 셋업 전반: `90. Settings/Sharing/Setup Guide.md`
