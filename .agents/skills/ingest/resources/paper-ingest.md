---
description: "Paper Ingest Mode (Academic Papers) — the full 12-step atomization pipeline for /ingest, loaded on demand when a paper is detected. Covers citekey naming, RQ linking, optional mothership draft surfacing, Zotero Tier-0, and the p7_verify gate."
---

# Paper Ingest Mode (Academic Papers) — 12-Step Scheme

> **로드 규칙 (progressive disclosure)**: 이 리소스는 `/ingest` 가 **논문을 감지했을 때만** 읽는다 — Standard/Book 경로는 이 파일을 로드하지 않는다. 논문이 아니면 `ingest.md` 의 Standard 로직으로 돌아간다.

> **Dual-runtime contract**: 먼저 `.claude/commands/ingest.md` shared behavioral contract 와 `.codex/commands/ingest.md` Codex adapter 를 모두 읽는다. Claude Code 는 `CLAUDE.md`, Codex/Fugu 는 `AGENTS.md` 를 적용하되 질문 예산, write gates, P-7 verification semantics 는 동일하다.

`/ingest` Standard 는 소스를 10~15 주제 위키로 쪼갠다. **Paper Mode 는 논문-스코프 12단 분석**을 컴파일한다 — 1 Raw Source + 1 Paper Hub + N 지식 원자 (`40. Paper Analyses/{citekey}/`) + 소수 Wiki 승격. 12단 노트가 집필 시 인용·팩트체크·paraphrase 대조의 대상이다.

> **12단은 파일 수가 아니라 좌표계 (axis)**. 노트 단위는 원문 섹션이 아니라 **지식 원자** (개념·주장·구분·메커니즘·사례 하나 = 노트 하나). 모든 원자가 `analysisStep` 좌표 + 자기완결 Analysis Context 를 갖는다. 논문당 원자 30~100+ 정상. 사용자용 해설은 `90. Settings/Sharing/Paper Ingest Guide.md` 참고. 성공 기준 두 겹: (a) 원문을 두 번 다시 안 열어도 되고 (coverage), (b) 원문보다 더 잘 이해된다 (exposition).

**Triggers** (any): 명시 요청 (`/ingest --paper`, "논문 분석") · `00. Inbox/02. Papers/` 또는 Category = Papers · DOI/arXiv/저널 URL · Abstract + References 구조의 변환 md. 자동 감지 시 "Paper Mode 로 할까요?" 별도 질문 없이 P-0 안에서 알린다. **질문 예산: 정확히 2개** (P-0 목적/RQ, P-1 유형/전략).

---

## Step P-0: Purpose + Scope Gate — MANDATORY

표준 Step 0 (미래의 나에게 보내는 편지) 를 확장. **먼저 볼트 루트 `Core Context.md` 를 로드** (재활용 축·도메인 정렬).

### P-0.1 스코프 가드 (scope guard)

Abstract 로 논문의 주제를 파악하고 **Core Context §2 재활용 축 및 기존 위키 도메인과의 정렬**을 확인한다. 명백히 볼트의 수집 범위 밖 주제이면 STOP — 원자화하지 말고 사용자에게 알린다:

> "이 논문은 현재 위키의 수집 범위 밖({분류})으로 보입니다. (a) 새 영역으로 수집 승인 / (b) 최근접 기존 영역({X})에 편입 / (c) 단순 수집만 — 어떻게 할까요?"

승인 없이 볼트의 도메인 범위를 조용히 확장하지 않는다 (contamination 방지).

### P-0.2 목적 + RQ 게이트

`20. Wiki/25. Questions/*.md` 를 읽어 (`type: research-question`, `status` ∉ {answered, superseded}) **동적 선택지**로 단일 질문:

> "Paper Mode 로 진행합니다. 이 논문을 **어느 Research Question/산출물에 쓰려고** ingest 하시나요?
> (1) {RQ-A} — {status} · (2) {RQ-B} — {status}
> (n+1) 새 RQ 등록 — 질문을 알려주시면 `25. Questions/` 에 만들고 계속
> (n+2) (Mode B) 모선 draft 에 — 검색된 모선 초안 제시 (`mainVaultRelated` 로만 연결)
> (n+3) 지금 없음 — 그래도 12단 분석 (`targetManuscript: none`)
> (n+4) 단순 수집 — Standard Ingest 로 전환
> + 수집 목적 한 줄도 함께 (편지)"

기록: `collectionPurpose` (verbatim) + `targetManuscript` (`"[[RQ-…]]"` 또는 `none`). 옵션 (n+4) → Standard 파이프라인으로 전환하고 이 리소스 종료.

> **주의**: 이 볼트에는 로컬 원고 파일 폴더가 없다 — 기여 대상은 **RQ 카드**(`feedsInto` 축)와 (Mode B) **모선 draft**(cross-vault, 메타데이터로만)다. `targetManuscript` 값은 RQ wikilink 이지 로컬 manuscript 파일이 아니다.

### P-0.3 Step 0-a — Draft 연결 (3-tier)

논문 관련 미연결 RQ·아이디어·초안을 찾아 "이 논문을 기다리던 게 이미 있습니다" 를 노출. 입력: `title`, `citekey`, `doi`, 키워드 3~5.

- **Tier 1 — 결정적 citekey stem 매치** (무료·최고정밀): RQ 의 `cites[]`·`[@…]` 를 `{surname}{year}` **stem 으로 정규화 후 prefix-match** (string-equality 아님 — RQ 는 `authYearShorttitle`, 논문 키도 동일 형식이나 shorttitle 이 다를 수 있음):
	```bash
	cd "20. Wiki/25. Questions"    # 볼트 루트 기준
	grep -ril '{surname}{year}' *.md    # stem 매치 — block-style cites 리스트·inline [@…] 모두 포착
	```
	히트 = 이 논문을 근거로 기다리는 RQ.
- **Tier 2 — `wiki` 컬렉션 시맨틱** (qmd 설치 시 — vec/hyde 에서 하이픈 제거, `-` 는 negation 파싱):
	- Claude/qmd MCP path:
	```
	mcp__qmd__query(collections=["wiki"], limit=8, searches=[
	  {type:"lex",  query:"<키워드 3~5, 공백>"},
	  {type:"vec",  query:"<논문 핵심 질문, 평문, 하이픈 없이>"},
	  {type:"hyde", query:"<2문장 모의 초록, 하이픈 없이>"}])
	```
	- Codex/Fugu shell fallback:
	```bash
	qmd query "<논문 핵심 질문, 평문, 하이픈 없이>" -c wiki -n 8
	qmd vsearch "<키워드와 2문장 모의 초록, 하이픈 없이>" -c wiki -n 8
	```
	경로에 `25. Questions/`·`21. Concepts/` 포함 히트 유지. qmd 미설치면 `rg` 키워드 검색으로 대체.
- **Tier 3 — (Mode B) 모선 시맨틱** (surfacing-only): 모선 볼트를 인덱싱한 qmd 컬렉션이 있으면 같은 방식으로 검색해 진행 중 아이디어·미발행 draft 를 표면화한다. standalone (Mode A) 이면 이 tier 는 건너뜀.

**연결 배선:**
- **RQ ↔ 논문** (양방향·동일 볼트): RQ 노트에 논문 `citekey` 를 `cites[]` 에 + stance 를 `evidenceFor`/`evidenceAgainst` 에 (LLM 이 abstract 로 판정). 허브에 RQ 를 `related` + 콜아웃:
	```markdown
	> [!question] Feeds Open Questions
	> - [[RQ-{slug}]] — evidence **for** {가설} / 이 논문이 메우는 gap
	```
- **(Mode B) 모선 아이디어/draft → 논문** (단방향·메타데이터): `mainVaultRelated` 에 실재 확인된 `obsidian://open?vault={your-mothership-vault-name}&file=…` 2~5개. **모선에 기본 쓰기 금지 — 보고만.**

---

## Step P-1: Paper Type Confirmation — 1 question

변환 md 의 Abstract + 방법 섹션 헤더를 스캔해 6유형 중 하나로 분류하고 근거 1줄과 함께 확인:

| paperType | 신호 |
|-----------|------|
| `quantitative` | 가설·표본·통계 (회귀·SEM·ANOVA)·p-value |
| `qualitative` | 인터뷰·FGI·코딩·주제분석·trustworthiness |
| `theory-concept` | 실증 데이터 없음·개념 정의·명제·프레임워크 제안 |
| `mixed-methods` | 양적+질적 2 strand·integration |
| `scale-development` | 문항 개발·EFA/CFA·타당도가 목적 |
| `meta-analysis` | 체계적 검색·효과크기 통합·PRISMA |

같은 질문에서 **실행 전략** 확인: 기본 = **full 원자화 (학술 논문)** / "핵심만" = progressive stub / 장문(>~15K 단어) = 자동 progressive. 6유형 밖 논문(서평·튜토리얼)은 최근접 유형 + 허브에 편차 기록 (7번째 유형 신설 금지). 확정 후 `90. Settings/Templates/12-Step Analysis Schemes.md` 의 해당 유형 스킴 로드.

---

## Step P-2: Save Raw Source

표준 Step 0.5 (binary→md; `conversion-fidelity` 기록 — 인용 규율에 영향) + 표준 Step 2 재사용:
- `10. Raw Sources/12. Papers/YYYY-MM-DD-{Title}.md` (ingest 날짜), verbatim `## Original Content`, `validate-raw-source.sh` hook 통과.
- 서지 frontmatter 추가: `citekey`, `doi`, `targetManuscript` (허브와 동일값).
- **Zotero Tier-0 (아래 §Zotero, 옵션)**: BBT 로 metadata 자동 채움. Zotero 미사용/미등록이면 provisional citekey.

---

## Step P-3: Hub + Atomic Notes — THE CORE

> **지배 원칙 (Coverage & Exposition Contract)**: "이 노트들만 읽으면 원문을 두 번 다시 안 열어도 되고, 원문보다 더 잘 이해된다." 노트 단위 = 지식 원자. 12단 = 좌표계. 축당 원자 무제한. 원저자 정의·주장은 verbatim `[!quote]` 로 고정, 분석자 보충은 【분석자 주】.

### P-3a: Decomposition Blueprint (분해 설계) — 산출물 = 허브 초안

원자 노트 작성 전에:
1. 변환 md 의 H2/H3 섹션 전수 나열.
2. 섹션별 지식 원자 분해 — 원자마다 4필드 확정: ① 파일명 `{Surname} {Year} - S{NN} {제목}` (**전량 확정**) ② 답하는 하나의 질문 ③ 원문 채굴 지점(§+문단) ④ 인접 원자·Wiki 링크.
3. 산출물 = **허브 초안** `{Surname} {Year} - S00 Hub.md` (`Template_Paper Hub`): S01 Citation + Coverage Map (2단, 미생성 원자 가리켜도 정상) + Step Map (전 축 `planned`) + Atom Catalog (축별 색인) + 말미 임시 `> [!note] Compile Plan`.
4. 규모 점검: `12-Step Analysis Schemes` "Decomposition Heuristics" 와 대조. 밀도 섹션 원자 1개 = under-decomposition 재검토. 논문당 30~100+ 정상.
5. 사용자 확인 불필요 (Blueprint 는 LLM 산출물, 질문 예산 유지).

폴더: `40. Paper Analyses/{citekey}/` — **citekey 폴더** (ASCII·Zotero 정렬·BBT 유일). 생성 전 동일 citekey 폴더 스캔.

### P-3b: Compile (SPEC 배포 + 원자 작성)

1. `Template_Atomization SPEC` 인스턴스를 **볼트 밖**(세션 scratchpad, 없으면 `70. Outputs/.tool-state/ingest/{citekey}-SPEC.md`) 에 생성 — 논문 메타 상수(citekey·paperType·targetManuscript·collectionPurpose) · Raw Source 경로 · **품질 기준 예문(수정 금지)** · frontmatter 예시(provenance model/effort 포함) · 전체 원자 파일명 리스트(P-3a 확정본) · 가로 링크 설계 · 자체 검증 스니펫.
2. **실행 전략** (아래 §Execution) 에 따라 원자 작성 — 기본 ① Parallel Fan-out (축별 5~9 원자/배치).
3. **허브 마무리**: Step Map `planned` → `compiled`(/`stub {M}건`/`skipped (사유)`), Compile Plan 콜아웃 삭제, Wiki Promotions 확정.

**원자 본문 계약** (`Template_Paper Analysis Note`, 순서 고정): H1 → `[!info] Analysis Context` 4행 → `## 쉬운 도입` → `## 정밀 해설` → `## 예시` → `## 원문 근거` (`[!quote]` verbatim 2~6) → `## 개념 관계` (비-허브 형제 원자 링크 ≥1) → 선택 `## 내 원고 맥락` / `## Open Questions`. 원자당 본문 700~1,500 단어. provenance(model/effort) 필수.

**인용 규율**: `[!quote] 원문 (p.{N}, §{Section})` 본문은 Raw Source `## Original Content` 에서 **verbatim** (grep 대조). **페이지 우선 locator** — Zotero PDF 있으면 `p.N` 복원(§Zotero), 없으면 §섹션. 통계치(β·p·CI·적합도) 항상 verbatim. 요약을 quote 안에 넣지 않음.

---

## Step P-4: Wiki Promotion (상한 없음, 하한 10~15)

재사용 개념을 `20. Wiki/21. Concepts/` 로 승격하고 `layer:` 로 구분 (**별도 폴더 없음** — 클러스터 형성 시 하위폴더 승격 고려):

| 재료 | layer |
|------|-------|
| 이론·프레임워크 + 구성 개념 각각 | `theory` |
| 연구방법·분석기법 | `method` |
| 측정도구·척도 (`Template_Scale Page`, `measuredConstruct`·`itemCount` + Psychometrics 표 + 저작권 콜아웃) | `scale` |
| 일반 개념 | `concepts` |
| 저자·저널·데이터셋 | `22. Entities/` |

update-over-create · v4 quality (`explored: false`, high-confidence 는 Bias Check) · 양방향 링크 (Wiki "Paper Analyses" 섹션 ↔ 원자 `related`+`개념 관계`) · provenance 필수.

---

## Step P-5: RQ Sync

`targetManuscript` ≠ `none` 이면:
- **RQ 카드**: 논문 `citekey` 를 RQ 의 `cites[]` 에 추가 + S12(Writing Value) 요지를 `evidenceFor`/`evidenceAgainst` 에 + RQ 본문에 한 줄.
- **(Mode B) 모선 draft**: `mainVaultRelated` 로만 보고 (모선 쓰기 금지).

---

## Step P-6: Index + Log

- **허브 마무리 확인**: Step Map `planned` 잔존 없음 + Compile Plan 콜아웃 삭제됨.
- `index.md`: Paper Analyses 섹션에 **허브만** 추가 (12×N 원자 금지 — index 비대), Stats 갱신.
- `log.md`: `## [YYYY-MM-DD] ingest-paper | {Surname} {Year} — {title}` (Purpose·targetManuscript·원자 수·Wiki 승격·p7 요약).

---

## Step P-7: Review — 게이트

**`90. Settings/Scripts/p7_verify.py` 를 오케스트레이터가 직접 실행** (볼트 루트에서, 인자 = 분석 폴더):
```bash
python3 "90. Settings/Scripts/p7_verify.py" "40. Paper Analyses/{citekey}"
```
검사: YAML 실파서 · v6.2 키+좌표 · **provenance(model/effort)** · Analysis Context+필수섹션 · 가로연결 · **인용 전수 verbatim** · Atom Catalog↔파일 · Coverage 섹션 전수 · index 허브-단독. **ALL PASS 가 통과 조건.**

> [!warning] 자체 검증 ≠ 게이트
> 팬아웃 서브에이전트의 "SELF-CHECK OK" 는 참고용이다 (거짓 양성 실증됨). 통과 판정은 오직 오케스트레이터의 `p7_verify.py` ALL PASS.

LLM 정성 검사(스크립트 비대체): decomposition(긴 섹션 2개 정독) · exposition(축마다 원자 1개, S09~S12 포함) · 인용 충실도 spot-check.

---

## Zotero Tier-0 (옵션 — 플러그인 없이)

Zotero + Better BibTeX(BBT) 사용자는 BBT 로컬 서버 `http://127.0.0.1:23119/better-bibtex/` 를 curl 로 활용할 수 있다. 미사용자는 이 절 전체를 건너뛰고 provisional citekey 경로를 쓴다.

- **metadata by citekey** (JSON-RPC) → 허브 frontmatter 자동 채움 (title·authors·year·doi·abstract·pdfPath). 예:
	```bash
	curl -s -H 'Content-Type: application/json' \
	  -d '{"jsonrpc":"2.0","method":"item.search","params":["{citekey}"],"id":1}' \
	  http://127.0.0.1:23119/better-bibtex/json-rpc
	```
- **CAYW** `http://127.0.0.1:23119/better-bibtex/cayw?format=pandoc` → `[@citekey]` 삽입.
- **페이지 점프**: `[!quote]` locator 에 `zotero://open-pdf/library/items/{itemKey}?page={N}` — arXiv-HTML 인용의 유실된 `p.N` 을 Zotero 저장 PDF 로 복구.
- **Fallback (Zotero 미사용/미등록/BBT 미도달)**: `authYearShorttitle` 를 로컬 생성 + `citekeyProvisional: true` + 경고 콜아웃:
	```markdown
	> [!warning] Provisional citekey
	> `{citekey}` 는 로컬 생성 — Zotero 미등록. 등록 시 BBT 키를 이 값으로 **PIN**(고정), 노트/폴더 재명명 금지.
	```
	Zotero 등록 시 **PIN**(재명명 아님) → 노트/폴더/`[@citekey]` 변경 0. provisional 백로그는 `/lint` 를 확장해 보고하게 할 수 있다 (기본 `/lint` 는 미포함).

---

## Execution Strategy (3-옵션)

| 전략 | 내용 | 적용 |
|------|------|------|
| **① Parallel Fan-out (기본)** | Blueprint 축·계열 경계로 원자 5~9개/배치를 서브에이전트 병렬. 각 프롬프트 필수 5종: SPEC 경로(필독1) · Raw Source(필독2) · 담당 원자 표 · 특이사항 · 자체검증 의무 | 서브에이전트 harness (Claude Code 등) + 통상 논문. **학술 논문 full 원자화 기본** |
| **② 단일 실행 중요도순** | 허브 초안 → 핵심 축 → 나머지 → Wiki 승격 | 서브에이전트 없는 harness (Codex CLI 등) 폴백 |
| **③ Progressive stub** | 핵심 축만 full, 나머지 `status: stub` (Analysis Context + 질문 1줄). 승격 = `/ingest {원자 경로}` | 장문(>~15K 단어) 또는 P-1 "핵심만" |

유형별 핵심 축 (progressive 기본값): quant S02·03·08·09·12 / qual S02·04·08·09·12 / theory S04·06·08·09·12 / mixed S06·08·09·12 / scale S06·07·08·09·12 / meta S04·08·09·10·12. 원자 30 미만이면 배치 수 비례 축소.

---

## Failure Modes (Paper Mode)

1. **요약 카드화 / 섹션 요약화** (#1, 실증 재발 클래스) — 노트가 회상 카드·섹션 압축으로 퇴화. Defense: 원자 단위 + Exposition Contract + p7 decomposition/exposition.
2. **Under-decomposition** — 밀도 섹션이 원자 1~2개로 뭉침. Defense: atomization-first + p7.
3. **Coverage hole** — 원문 섹션이 어느 원자에도 미배정. Defense: Coverage Map 전수 + p7.
4. **Citation fabrication** — 없는 페이지·구절 조작. Defense: grep-able verbatim + p7 전수 대조.
5. **Provenance 누락** — hub·원자에 model/effort 없음 (v6 필수). Defense: 템플릿 placeholder + p7 provenance 검사.
6. **citekey ≠ 토큰 동일** — 논문 키가 RQ `cites[]` 와 불일치 → 링크·References 깨짐. Defense: BBT/provisional 통일 + Tier-1 stem 매치.
7. **범위 밖 조용한 확장** — 볼트 수집 범위 밖 논문을 무단 ingest. Defense: P-0.1 scope guard STOP.
8. **(Mode B) 모선 오염** — 모선에 쓰기. Defense: 모선은 surfacing-only, `mainVaultRelated` 로만.
9. **RQ 미연동** — targetManuscript RQ 인데 `cites[]`/`evidenceFor` 미갱신 (P-5 누락).
10. **Index 비대** — 원자를 index 에 노출. Defense: 허브만.
11. **Blueprint 생략 (즉흥 분해)** — 파일명·링크를 작성 중 즉흥 → 표류. Defense: P-3a 허브 초안 없이 P-3b 금지.

---

## File Naming (요약)

- Raw Source: `10. Raw Sources/12. Papers/YYYY-MM-DD-{Title}.md`
- 분석 폴더: `40. Paper Analyses/{citekey}/`
- 허브: `{Surname} {Year} - S00 Hub.md` · 원자: `{Surname} {Year} - S{NN} {제목}.md`
- Wiki 승격: `20. Wiki/21. Concepts/{Name}.md` (+ `layer:` theory/method/scale)
