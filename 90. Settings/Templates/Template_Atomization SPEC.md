---
type: template
aliases:
  - Template_Atomization SPEC
  - Atomization SPEC 템플릿
  - 컴파일 SPEC 템플릿
description: "Per-paper compile SPEC template for Paper Ingest step P-3b. Instantiated outside the vault in session scratchpad or the tool-state ingest fallback with the P-3a blueprint baked in, the single spec every writing unit reads first so format uniformity and lateral-link integrity hold across parallel fan-out agents. The section-1 quality-calibration block must be propagated verbatim."
author:
  - "{Agent}"
model: "{model-id}"
effort: "{effort-level}"
date created: 2026-07-09T00:00
date modified: 2026-07-12T00:00
tags:
  - template
  - system
  - paper-analysis
  - 12-step
status: template
---

# Template_Atomization SPEC

> [!info] 사용법 (P-3b Step 1 — 인스턴스 생성)
> 이 템플릿은 `/ingest` Paper Mode **P-3b** 에서 논문별 SPEC 인스턴스로 복사·치환된다. 인스턴스 위치는 **볼트 밖**: Claude Code 또는 ChatGPT/Codex 세션 scratchpad → 없으면 `70. Outputs/.tool-state/ingest/{citekey}-SPEC.md`. 볼트 레이어 (10/20/30/40) 에 두지 않는다 — 파일명 리스트 등 논문별 일회용 작업 파일이다.
> 치환 대상: `{...}` placeholder 전부. **§1 의 품질 캘리브레이션 예문 블록은 수정 금지** — verbatim 전파 자체가 목적이다.
> 모든 작성 단위 (팬아웃 서브에이전트, 또는 단일 실행의 각 배치) 는 이 SPEC 인스턴스를 **필독 1순위**, Raw Source 를 필독 2순위로 읽고 시작한다.

---

## 0. 작업 개요 (논문 메타 상수)

	- **논문**: {저자} ({연도}), *{제목}*
	- **citekey**: `{citekey}` · **paperType**: `{paperType}`
	- **targetManuscript**: {"[[RQ-…]]" 또는 none} · **collectionPurpose**: "{사용자 답변 verbatim}"
	- **conversion-fidelity**: {high|medium|low} → **locator 방침**: {페이지 우선 (p.N, §Section) | 섹션(§)만 — 페이지 번호 유실, 지어내기 금지}
	- **Raw Source 절대 경로**: `{.../10. Raw Sources/12. Papers/YYYY-MM-DD-{Title}.md}` — 인용은 이 파일의 `## Original Content` 에서만
	- **저장 폴더 절대 경로**: `{.../40. Paper Analyses/{citekey}/}`
	- **허브 파일**: `{Surname} {Year} - S00 Hub.md` — P-3a 에서 이미 생성됨. Coverage Map + Atom Catalog + 말미 `[!note] Compile Plan` 콜아웃이 분해 설계도다.

> [!info] Zotero Tier-0 (BBT 자동 메타 — 있으면 사용, 없으면 provisional)
> Better BibTeX 로컬 서버 `http://127.0.0.1:23119/better-bibtex/` 가 떠 있으면 citekey 하나로 논문 메타를 자동으로 끌어와 허브 frontmatter 를 채운다.
> - JSON-RPC `item.citationkey` 또는 citekey 로 metadata 조회 → title·authors·year·doi·abstract·pdfPath·zoteroSelectURI 자동 채움.
> - CAYW `http://127.0.0.1:23119/better-bibtex/cayw?format=pandoc` → 본문 인용 `[@citekey]` 삽입.
> - `[!quote]` locator 의 `zotero://open-pdf/library/items/{KEY}?page={N}` 로 페이지 점프. arXiv-HTML 인제스트도 저장된 PDF 에서 `p.N` 을 복구해 페이지 우선 locator 를 확보한다.
> - **Fallback (논문이 Zotero 에 없을 때)**: 로컬에서 `authYearShorttitle` provisional citekey 를 생성하고 `citekeyProvisional: true` + 경고 콜아웃을 남긴다. 나중에 Zotero 임포트 시 BBT 키를 이 값으로 **PIN** 한다 — 노트·폴더는 절대 rename 하지 않는다. provisional backlog 는 `/lint` 를 확장해 보고하게 할 수 있다 (기본 `/lint` 는 미포함).
> - BBT 서버가 안 떠 있으면 provisional citekey 로 진행하고 그 사실을 허브에 명기한다.

---

## 1. 품질 기준 (지배 원칙)

> [!warning] 품질 기준점 (실증 캘리브레이션 — 이 블록은 인스턴스에서 수정 금지)
> 다음 밀도가 원자 해설의 **최소선**이다 — "이 논문은, 미디어 리터러시 연구들이 'AI 리터러시'와 미디어 리터러시를 동의어로 간주하지만, 미디어 리터러시의 '비판적 사고능력'은 AI 의 하네스를 이해한 리터러시와 개념이 매우 다른데도 '비판적'이라는 추상어만으로 하네스 이해가 자동으로 된다고 여기는 문제가 있다 — 는 점을 날카롭게 지적한다" 급.
> 즉 **용어를 풀고, 개념 차이의 메커니즘을 밝히고, 왜 날카로운 지적인지까지 해설한다 — 그리고 이것도 그나마 최소한이다.** 요약·압축은 실패다. 토큰을 아끼지 말 것 (원자당 본문 700~1,500 단어 기준). 추상 지침 ("처음 보는 독자를 이해 상태로") 만 전파했던 v1 (요약 카드)·v2 (섹션 압축) 는 실패했고, 구체 예문을 전파한 v3 (7K 단어 이론 논문 → 원자 78개 실증) 가 처음 통과했다.

**5대 요구** (전 원자 공통):

	1. **미해설 용어 금지** — 노트에 등장하는 모든 전문용어는 그 자리에서 풀거나 하위 원자로 분리해 링크한다. "대학원 1년차가 이 노트만 읽고 이해할 수 있는가" 가 테스트.
	2. **메커니즘 명시** — 개념 간 차이·주장·효과는 "왜 그런가" 의 작동 방식까지 서술한다 ("A 만으로 B 가 되지 않는 이유는 ...").
	3. **논증 내 역할** — 이 원자가 논문 전체 논증에서 하는 일을 명시한다 (이 원자가 없으면 어떤 주장이 무너지는가).
	4. **토큰 아끼지 않기** — 분량 압박으로 원자를 합치거나 해설을 줄이지 않는다. 원문에 충실 = 논지의 보존이지 난이도의 보존이 아니다.
	5. **원저자 우선 + 【분석자 주】** — 정의·주장·예시는 원저자 것을 verbatim 인용으로 고정하고, 분석자 보충 (예시·비유·재기술) 은 반드시 【분석자 주】 로 구분한다.

---

## 2. 파일명·frontmatter 규격

**파일명**: `{Surname} {Year} - S{NN} {원자 제목}.md` — 반드시 **§6 리스트의 파일명 그대로** (한 글자도 바꾸지 않는다 — 다른 원자의 가로 링크가 이 이름을 가리키고 있다).

**완성 frontmatter 예시** (YAML 2-space 들여쓰기 · free-text 값 큰따옴표 · 값 내부 큰따옴표 금지):

```yaml
---
type: paper-analysis
aliases:
  - "{Surname} {Year} - S{NN} {원자 제목}"
description: "{English 1-2 sentences — what this atom explains and why it matters in the paper}"
author:
  - "{Agent}"
model: "{model-id}"
effort: "{effort-level}"
date created: "{YYYY-MM-DDTHH:mm}"
date modified: "{YYYY-MM-DDTHH:mm}"
tags:
  - paper-analysis
  - "{paperType}"
  - "{topic-tag}"
paperType: "{paperType}"
analysisStep: 0 # replace 0 with integer N (2-12)
analysisStepName: "{§3 표의 해당 축 정식 단계명 verbatim}"
paperHub: "[[{Surname} {Year} - S00 Hub]]"
source:
  - "[[{Raw Source 파일명 (.md 제외)}]]"
related:
  - "[[{인접 원자}]]"
  - "[[{관련 Wiki 페이지}]]"
status: completed
explored: false
verificationStatus: unverified
---
```

**v6.1 규칙 요약**: YAML 2 스페이스 (탭 금지) / Markdown body 는 TAB (스페이스 금지) / YAML 내 wikilink 는 큰따옴표 `"[[...]]"` / `description` 등 free-text 값은 큰따옴표로 감싸고 내부에 큰따옴표·`: ` (콜론+공백) 금지 — 인용은 작은따옴표로.

---

## 3. analysisStepName 표 ({paperType})

{P-3b 인스턴스 생성 시 `90. Settings/Templates/12-Step Analysis Schemes.md` 의 해당 유형 표에서 복사 — 작성 단위가 Schemes 파일을 따로 열지 않아도 되게 한다. `analysisStepName` 은 이 표의 단계명 verbatim.}

| S | 단계명 |
|---|--------|
| 2 | {단계명} |
| 3 | {단계명} |
| 4 | {단계명} |
| 5 | {단계명} |
| 6 | {단계명} |
| 7 | {단계명} |
| 8 | {단계명} |
| 9 | {단계명} |
| 10 | {단계명} |
| 11 | {단계명} |
| 12 | {단계명} |

---

## 4. 본문 구조 (순서 고정)

H1 (= 파일명과 동일) 직후 **Analysis Context 콜아웃 4행** — 완성 예시:

```markdown
# {Surname} {Year} - S{NN} {원자 제목}

> [!info] Analysis Context
> **Paper**: {저자} ({연도}), *{제목}* — [[{Surname} {Year} - S00 Hub|허브]] · [[{Raw Source 파일명}|원문]]
> **수집 맥락**: "{collectionPurpose 요지}" → [[{targetManuscript}]] (없으면 "단순 수집")
> **위치**: Step {N} / 12 — {단계명} ({paperType}) · 원문 §{담당 섹션} · 상위 원자: [[{...}]] (하위 원자일 때만)
> **이 원자**: {이 노트가 답하는 하나의 질문}. 인접 원자: [[{...}]] · [[{...}]]
```

이어지는 섹션 순서 (H2, 고정):

	1. `## 쉬운 도입` — 모르는 독자에게 1~2문단, 일상 언어
	2. `## 정밀 해설` — 원저자의 정의·논지·전개, 차이의 메커니즘까지
	3. `## 예시` — 원문 예시 전부 + 분석자 예시는 【분석자 주】
	4. `## 원문 근거` — `[!quote]` verbatim 2~6개
	5. `## 개념 관계` — 논증 내 역할 + **비-허브 원자 직접 링크 ≥ 1** (§7 설계 반영)
	6. `## 내 원고 맥락` (선택) — targetManuscript 관점
	7. `## Open Questions` (선택)

**S12 예외**: WRITING VALUE 원자는 자유 구조 허용 (예: `## 바로 쓸 수 있는 것` / `## 인용 시 주의`) — 단 `## 개념 관계` 와 verbatim 인용 규율은 유지.

---

## 5. 인용 규율 (위반 = 전체 실패)

	- `> [!quote] 원문 ({locator})` 콜아웃 본문은 Raw Source `## Original Content` 에서 **verbatim** — grep 으로 찾을 수 있어야 한다. 원자당 통상 2~6개 (기준은 개수가 아니라 원자-인용 밀착도).
	- **locator**: §0 의 방침을 따른다. 페이지 번호를 지어내지 않는다.
	- **요약을 quote 콜아웃 안에 넣지 않는다** — 요약·재기술은 콜아웃 밖 본문에.
	- 통계치 (β, p, CI, 적합도 지수) 는 항상 verbatim.
	- 분석자 보충이 원저자 논지처럼 섞이면 재인용 오염 — 반드시 【분석자 주】.
	- P-7 에서 `p7_verify.py` 가 인용을 **전수 대조**한다 — 한 건이라도 fabrication 이면 해당 배치 전체를 재검토한다.

---

## 6. 전체 원자 파일명 리스트 (P-3a 확정본 — 수정 금지)

{P-3a Blueprint 의 파일명 전량을 축별로 붙여넣는다. 모든 작성 단위가 자기 담당 밖의 원자로도 가로 링크를 걸어야 하므로 전체 리스트가 필요하다 — 리스트에 있는 이름이면 **아직 미생성이어도 정확한 링크**다. 리스트 밖 파일명 즉흥 생성 금지.}

### S02 — {단계명} ({N} atoms)

	- `{Surname} {Year} - S02 {원자 제목}.md` — {답하는 질문 1줄}

### S03 — {단계명} ({N} atoms)

	- `{...}.md` — {...}

{... S12 까지 전 축 반복 ...}

---

## 7. 축 간 가로 링크 설계 (Blueprint 관계 힌트)

{P-3a 에서 확정한 원자 간 인접 관계를 붙여넣는다 — 각 원자의 `## 개념 관계` 와 Analysis Context "인접 원자" 행이 이 설계를 따른다. 축 내 관계 + **축 간 (S04↔S07, S06↔S09 등) 교차 관계** 를 모두 포함할 것 — 위계 (허브 경유) 만 있고 가로 그물이 없으면 P-7 실패.}

	- [[{원자 A}]] ↔ [[{원자 B}]]: {구분점 또는 연결 메커니즘 1줄}
	- [[{원자 C}]] → [[{원자 D}]]: {선행 개념 관계}

---

## 8. 관련 Wiki 페이지 (링크 선허용 규칙)

	- **기존 갱신 대상**: {[[페이지]] — 어느 원자와 연결되는지}
	- **신규 승격 예정 (P-4 에서 생성)**: {[[페이지]] — 어느 원자에서 승격되는지}
	- **링크 선허용 규칙**: 위 목록의 Wiki 페이지는 아직 존재하지 않아도 원자 노트에서 링크할 수 있다 (P-4 가 생성 예정이므로). 단 **목록 밖 Wiki 링크를 즉흥으로 만들지 않는다** — 깨진 링크 표류 방지.
	- **링크는 반드시 최종 파일명으로 (v1.10.1)**: Obsidian 은 bare `[[alias]]` 를 해석하지 않고 `/` 를 폴더 경로로 파싱한다. slash·특수문자가 든 개념은 이 목록에서 **최종 파일명을 확정**하고 (예: `Harm-care.md`), 링크는 `[[Harm-care|Harm/care]]` 파이프 형태로만 건다. `[[Harm/care]]` 처럼 alias 로 직접 링크 금지 — 클릭 시 새 폴더+새 노트가 생긴다 (파일럿 분석에서 123곳 실증·수정됨).

---

## 9. 저장 전 체크리스트 + 자체 검증 의무

**각 원자 저장 전** (작성 단위별):

	- [ ] YAML 2 스페이스 · body TAB · YAML wikilink 큰따옴표 · free-text 값 큰따옴표
	- [ ] 파일명 = §6 리스트와 정확히 일치
	- [ ] Analysis Context 콜아웃 4행 (H1 직후)
	- [ ] 섹션 순서 = §4 (S12 예외 규칙 포함)
	- [ ] `[!quote]` 2~6개, verbatim + locator 방침 준수
	- [ ] `## 개념 관계` 에 비-허브 원자 링크 ≥ 1 (§7 설계 반영)
	- [ ] 분석자 보충 전부 【분석자 주】 구분
	- [ ] 밀도가 §1 Kim 예문 기준선 이상 (본문 700~1,500 단어)

**자체 검증 의무 (배치 완료 시 — 보고 필수)**: 각 작성 단위는 자기 산출물 전체에 대해 (1) YAML 실파서 파싱, (2) 인용 전수 verbatim 대조를 수행하고 결과를 보고한다. 아래 스니펫을 그대로 실행하면 된다 (인자 = 자기가 작성한 원자 파일 경로들):

```bash
python - "{원자1 절대경로}" "{원자2 절대경로}" <<'PY'
import io, re, sys, unicodedata, yaml
RAW = r"{Raw Source 절대 경로 — §0 값으로 치환}"
# 유니코드 구두점 변이 (curly quote·dash·ellipsis) 정규화 — p7_verify.py 와 동일 규칙 (v1.10.1).
# LLM 은 원문의 ’ “ ” — 를 ' " - 로 옮겨쓰는 경향이 있어 이를 흡수한다. 단어·숫자는 보존 — fabrication 은 여전히 검출.
_PT = {0x2018: "'", 0x2019: "'", 0x201C: '"', 0x201D: '"', 0x2013: "-", 0x2014: "-", 0x2015: "-",
       0x2026: "...", 0x00A0: " ", 0x2032: "'", 0x2033: '"'}
def norm(s): return re.sub(r"\s+", " ", unicodedata.normalize("NFC", s).translate(_PT)).strip()
src = norm(io.open(RAW, encoding="utf-8").read().split("## Original Content", 1)[1])
bad = 0
for f in sys.argv[1:]:
    t = io.open(f, encoding="utf-8").read()
    try:
        yaml.safe_load(t[3:t.find("\n---", 3)])
    except Exception as e:
        print("YAML FAIL:", f, "->", str(e).split("\n")[0]); bad += 1; continue
    for m in re.finditer(r"^> *\[!quote\][^\n]*\n((?:>.*\n?)+)", t, re.M):
        body = re.sub(r"^> ?", "", m.group(1), flags=re.M)
        q = norm(body).strip("\"'“”‘’")
        if q in src: continue
        lines = [norm(l).strip("\"'“”‘’") for l in body.split("\n")]
        lines = [l for l in lines if len(l) >= 12]
        if lines and all(l in src for l in lines): continue
        print("QUOTE FAIL:", f, "->", q[:60]); bad += 1
print("SELF-CHECK", "OK" if not bad else "FAIL(%d)" % bad, "-", len(sys.argv) - 1, "files")
PY
```

**보고 형식** (작성 단위 → 오케스트레이터): `"원자 {n}개 작성 완료 · YAML {n}/{n} OK · 인용 {m}/{m} verbatim OK · 특이사항: {없음 | 내용}"`. SELF-CHECK FAIL 상태로 완료 보고 금지 — 수정 후 재검증.

오케스트레이터는 전 배치 완료 후 통합 검증을 실행한다: `python "90. Settings/Scripts/p7_verify.py" "{저장 폴더}"` → **ALL PASS 가 P-7 통과 조건**.
