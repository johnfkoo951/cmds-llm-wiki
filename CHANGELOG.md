# cmds-llm-wiki — Changelog

템플릿 버전 이력. (`cmds-system-files` 의 CHANGELOG 형식 참고)

---

## v1.10.0 — 2026-07-23 (Paper Ingest Mode — 12-step paper atomization)

**Source**: 운영 볼트 schema v6.2 의 Paper Ingest Mode 를 sanitize 하여 이식. v1.9.0 에서 "학술 전용 버티컬이라 의도적 제외" 했던 항목을 **사용자 결정으로 포함** — RQ 카드 (v1.9.0) 와 결합해 논문 → 질문 → 논증의 전체 파이프라인이 킷 안에서 완결된다.

### Added — Paper Ingest Mode (`/ingest` 자동 감지)

- **감지**: DOI/arXiv/저널 URL · Abstract+References 구조 PDF · `00. Inbox/02. Papers/` → Standard 대신 **논문-스코프 12단 분석** (1 Raw Source + 1 Paper Hub + 지식 원자 30~100+ + Wiki 승격). 질문 예산 2개 (P-0 목적/RQ, P-1 유형).
- **P-0 → P-7 파이프라인 리소스**: `.agents/skills/ingest/resources/paper-ingest.md` (progressive disclosure — 논문 감지 시에만 로드). scope guard 는 개인 도메인 레지스트리 대신 **Core Context 정렬**로 일반화, 모선 단계는 Mode B 옵션.
- **ingest 3-surface 포인터**: `.claude/commands/ingest.md` + `.codex/commands/ingest.md` (폴백 = 단일 실행 중요도순) + `.agents/skills/ingest/SKILL.md`.

### Added — 12-Step Analysis Schemes + 신규 타입 2종

- `90. Settings/Templates/12-Step Analysis Schemes.md` — 6유형 (quantitative / qualitative / theory-concept / mixed-methods / scale-development / meta-analysis) × 12 좌표 (S01 CITATION ~ S12 WRITING VALUE) 통합 스펙 + Coverage & Exposition Contract + 원자 분해 규칙 + Decomposition Heuristics.
- `type: paper-hub` (S00 허브 — paperType·citekey·doi·targetManuscript) + `type: paper-analysis` (지식 원자 — analysisStep 2~12·analysisStepName·paperHub). 원자는 `claimType`/`evidenceScope` 면제 — 검증은 p7 인용 충실도로 대체.
- 새 폴더 `40. Paper Analyses/{citekey}/`. Wiki Page `layer` 확장: `theory` / `method` / `scale`.

### Added — Templates ×4 (7 → 11) + 검증 스크립트

- `Template_Paper Hub` (Coverage Map·Step Map·Atom Catalog) / `Template_Paper Analysis Note` (Analysis Context + 쉬운 도입→정밀 해설→원문 근거 verbatim quote) / `Template_Atomization SPEC` (팬아웃 배포용 작업 명세) / `Template_Scale Page` (measuredConstruct·itemCount + Psychometrics 표 + 저작권 콜아웃).
- `90. Settings/Scripts/p7_verify.py` — P-7 기계 게이트: YAML·좌표·provenance·인용 전수 verbatim·Coverage·Atom Catalog↔파일 대조. ALL PASS 가 통과 조건 (서브에이전트 자체검증은 게이트 아님).

### Added — Paper Ingest Guide (사용자 매뉴얼)

- `90. Settings/Sharing/Paper Ingest Guide.md` — 12단계 (S01~S12) 공통 골격 + 6유형별 변형 + 산출물 구조 + 인용 규율 + RQ 연계 + 실행 전략 + Zotero 옵션 + FAQ 를 사람 독자용으로 해설.

### Changed

- 스키마 (CLAUDE.md ↔ AGENTS.md parity): type 목록 + provenance 대상 (×2곳) + Layer별 프로퍼티 (Paper Hub/Analysis 블록) + 폴더 트리 (40 + Scripts) + File Naming 3행 + Callout 2종 (Analysis Context·quote) + camelCase 키 8종 (`paperType`·`analysisStep`·`analysisStepName`·`paperHub`·`targetManuscript`·`doi`·`measuredConstruct`·`itemCount`) + Citation Standard 에 "Paper Mode 는 citekey 항상 사용" 명시.
- `/status` 3-surface 에 Paper Analyses 카운트, `index.md` 에 Paper Analyses (허브만) nav 섹션, qmd config 에 `paper_analyses` 컬렉션, README/Setup Guide/CLAUDE-Template/kit 내부 문서 트리·카운트 정합 (6→7 폴더, 7→11 템플릿).

### Kit adaptations (운영 볼트와 의도적으로 다른 점)

- P-0.1 도메인 가드: 운영 볼트의 9-도메인 레지스트리 → **Core Context §2 재활용 축 정렬 확인**으로 일반화.
- Zotero Tier-0 는 명시적 **옵션** (미사용자는 provisional citekey 경로 완결).
- 운영 실증 사례 참조 (특정 논문 허브 wikilink) 는 수치만 남기고 제거.

### Known gaps

- `/autoresearch` 는 여전히 운영 볼트 전용 (v2.0 후보). `/lint` 는 RQ/citation/paper 커버리지 리포팅 미지원 (후속 마이너 후보).

## v1.9.1 — 2026-07-23 (docs: RQ/Synthesis usage guide + onboarding next-steps)

Docs-only patch — no schema, template, or harness behavior changes.

### Added — Setup Guide 사용법 문서화

- FAQ 신설: "Research Question / Synthesis 카드는 언제 쓰나" — 두 카드의 용도 구분 (알게 된 것 vs 묻고 있는 것/주장하는 것), 승격 흐름 (`Open Question` 콜아웃 → RQ 카드, `sourceCallout` 역추적), status 생애 추적, "둘 다 필수 아님 — 산출물 단계에 도입" 가이드, Citation Standard 연계.
- "다음 단계" 성장 경로에 RQ 승격·Synthesis 작성 시점 2개 bullet 추가.
- 헤더 대상 버전 `v1.6.2+` → `v1.9.0+`, 갱신일 표기.

### Changed — /onboard wrap-up

- 온보딩 마무리 추천 단계에 "(성장 후) 반복 Open Question → RQ 카드 승격, 주장 방어 → Synthesis 카드" 항목 추가 (4→5단계).

## v1.9.0 — 2026-07-23 (Research Question + Synthesis cards · Citation Standard · CLAUDE.md Operations parity)

**Source**: 운영 볼트(CMDS_LLM_Wiki) schema v6.1 (2026-07-07) 의 "논문 산출층" 중 **일반화 가능한 절반**만 선별 이식 — 질문·논증의 1급 객체화. 학술 전용 버티컬(v6.2 Paper Ingest Mode, 12단 논문 분석)은 의도적으로 제외하고 운영 볼트 전용으로 유지한다.

### Added — Research Question 카드 (`type: research-question`, v6.1)

- 새 폴더 `20. Wiki/25. Questions/` + 파일명 `RQ-{slug}.md`. in-page `> [!question] Open Question` 콜아웃을 1급 카드로 승격 — 반복 등장하거나 산출물(논문·책·블로그 시리즈·제품 결정)로 이어질 질문을 first-class object 로 추적.
- 프로퍼티: `status`(open/investigating/answered/parked/superseded) · `questionType`(descriptive/causal/comparative/methodological/normative/design) · `feedsInto` · `hypotheses` · `evidenceFor`/`evidenceAgainst` · `cites`(권장) · `sourceCallout`(역추적) · `related`.
- RQ 는 claim 이 아니라 질문이므로 v5 `claimType`/`verificationStatus` 대신 `status` 를 쓴다.

### Added — Synthesis 카드 (`type: synthesis`, v6.1)

- `30. Queries/` 에 query-result 와 같은 폴더, `type` 으로만 구분 (YAGNI — flat 유지). Query 가 반응형 답변이면 Synthesis 는 능동 논증: `thesis` + 근거 claim + `counters` + gap + `targetVenue`.
- `/query` operation 에 Step 5 추가: 능동 논증이 필요하면 `type: synthesis` 카드로 저장.

### Added — Citation Standard (v6.1, 옵션)

- BetterBibTeX citekey (`authYearShorttitle`) + Pandoc/CSL `[@citekey]` inline + `cites:` frontmatter + `## References` + Raw Source `citekey` 이중 연결. **옵션 규약** — 채택하지 않아도 볼트 운영에 지장 없음.

### Added — Templates ×2 (5 → 7)

- `Template_Research Question.md` / `Template_Synthesis.md` — v6 provenance (`model`/`effort`) + quoted `description: ""` 포함, 생성 시점부터 스키마 만족.

### Fixed — kit CLAUDE.md Operations parity (v1.7.1 부터 이월된 부채)

- kit `CLAUDE.md` Operations 챕터에 §0 Capture Tabs / §5 Verify / §6 Audit 추가 — kit `AGENTS.md` 와의 비대칭 해소 (Claude-first entrypoint 표기로 적응).

### Fixed — CLAUDE.md ↔ AGENTS.md parity 복원 + AGENTS.md 일반화 (릴리스 전 적대적 검증에서 적발된 pre-1.9 drift)

- **Frontmatter Standards 7곳 동기화**: author 행 (`Claude` → `Claude`/`Codex`/`Grok`), effort 문구 중립화, CLAUDE.md category 에 `AI Research` 누락 보충, `mainVaultRelated` 문구 (URL_ENCODED_PATH 리터럴 예시 제거 → stat 검증 문구), `chapterPart` 예시, camelCase 헤딩의 mothership 내부 alias (`@CMDS-Guide`) 제거, Quality Control v4 의 운영볼트 이력 문장 제거 + Bias Check 콜아웃 표기.
- **Compatibility Matrix**: AGENTS.md 헤딩 `Codex Compatibility Matrix (v1.3)` → `Cross-Agent Compatibility Matrix` (stale v1.3 태그 제거), 정보량 없는 `Status` 열 제거.
- **AGENTS.md mothership 옵션화**: Vault Overview·Core Context·ingest Step 0-a·Cross-Vault Reference 를 CLAUDE.md 와 같은 `(옵션)` 프레이밍으로 — standalone Codex 사용자가 모순된 지시를 받지 않도록. 잔존하던 원저자 볼트 구조 예시 링크 2건을 generic placeholder 로 교체.
- **type 목록 완결**: 필수 프로퍼티 `type` 에 실제 사용 중이던 `documentation`·`inbox` 추가 (양 스키마).
- **부속 파일 정합**: `CLAUDE-Template.md` (규칙 문구 + RQ/Synthesis 최소 프로퍼티 블록 + naming 행), `index.md` (description 큰따옴표 + Questions 반영 + nav stub), `Setup Guide.md` (템플릿 7종 표기 + 잘못된 brace glob 정리 커맨드 수정), `Template_Synthesis` 의 미선언 `status` 키 제거.

### Changed

- Provenance Rule 대상 타입에 `research-question`·`synthesis` 추가 (양 스키마 ×2곳).
- 필수 프로퍼티 `type` 목록, Folder Structure 트리, File Naming 표 (`RQ-{slug}.md` 행), camelCase 키 목록 (+11 keys), Parity Contract 문구 (v6/v6.1 키 포함) 갱신.
- README 트리: `25. Questions/` 추가 + Templates 카운트 stale "4종" → "7종" 정정 (v1.7.1 부터 5종이었음).

### Kit adaptations (운영 볼트와 의도적으로 다른 점)

- `cites` 는 운영 볼트에서 필수지만 킷에서는 **권장** — Citation Standard 자체가 옵션이므로.
- `feedsInto`/`targetVenue` 예시를 중립화 (논문 / 책 챕터 / 블로그 시리즈 / 제품 결정).
- `localDev` (v6.1) 는 개인 로컬 경로 패턴이라 미이식.

### Known gaps

- `/autoresearch` 는 운영 볼트 전용 (Generator-Verifier loop — v2.0 후보).
- `/lint` 는 아직 RQ/synthesis/citation 커버리지를 리포팅하지 않는다 (후속 마이너 후보).

## v1.8.0 — 2026-07-23 (Description Rule + v6 Provenance schema)

**Source**: 운영 볼트(CMDS_LLM_Wiki) schema v6 (2026-07-05) 에서 검증된 두 규칙을 sanitize 하여 이식. Schema/template edits were staged in the canonical on 2026-07-07; this release publishes them.

### Added — Description Rule (CLAUDE.md + AGENTS.md CRITICAL RULES)

- **`description` 값은 항상 큰따옴표** — 값에 콜론(`: `)·엠대시·괄호·`#`·wikilink 가 들면 unquoted YAML 은 파싱 에러로 노트 전체가 렌더 실패하는 실전 사고 클래스를 규칙화. 빈 값도 `description: ""`.
- Pre-Flight Checklist, Essential (Post-Compact) #6, 필수 프로퍼티 7개 표가 모두 double-quoted 요구사항을 반영하도록 갱신.
- 두 스키마 파일의 자기 frontmatter `description` 도 큰따옴표로 전환 (dogfooding).

### Added — Provenance Rule (v6): `model` + `effort`

- 에이전트가 쓰는 모든 콘텐츠 페이지(raw-source·wiki-page·query-result·moc·inbox)는 `author` 바로 뒤에 **`model`(상세 세션 모델 id) + `effort`(추론 강도)** 를 항상 기록 — Claude Code·Codex·Grok cross-agent provenance.
- 새 "Provenance 프로퍼티 (v6 신설)" 섹션 + Essential #9 + Pre-Flight 항목 추가. camelCase 허용 키 목록에 `model`, `effort` 추가.
- harness 정의 파일(`.claude/commands/*`, `.codex/commands/*`, `.agents/skills/*`)의 자기 frontmatter 는 provenance 면제 (슬래시 커맨드/스킬 파서 혼선 방지) — Description Rule 만 적용.

### Changed — Templates ×5 (schema alignment)

- `Template_Raw Source` / `Template_Wiki Page` / `Template_Query Result` / `Template_MOC` / `Template_AI Research Capture`: `description:` → `description: ""` (quoted empty) + `author` 뒤에 `model:` / `effort:` 키 추가 — 템플릿으로 생성되는 페이지가 생성 시점부터 v6 스키마를 만족.

### Known gaps (carried over from v1.7.1)

- Kit `CLAUDE.md` Operations chapter still lacks the Capture Tabs / Verify / Audit sections that kit `AGENTS.md` already has (asymmetry — port planned).
- `/autoresearch` remains operating-vault-only (Generator half of the Generator-Verifier loop).

## v1.7.1 — 2026-07-03 (hook runtime fixes + broken template dependency + sanitization)

Patch release driven by the 2026-07-03 full satellite system-files audit (multi-agent, adversarially verified). No schema or feature changes.

### Fixed — hooks (real runtime bugs, both `.claude/` and `.codex/` copies)

- **`qmd-reindex.sh` debounce was a no-op on macOS** — `date +%s -r FILE` is GNU argument order; BSD date fails silently (empty output), so the settle-wait loop never ran. Replaced with `date -r FILE +%s`.
- **Stale-lock permanent lockout** — a worker killed mid-run (or aborted by `set -e` on a qmd failure) left `.running` behind, silently disabling all future auto-reindexes. Added a 10-minute mtime expiry on the lock + `trap EXIT` cleanup in the worker.
- **`validate-raw-source.sh` Check 2 false positives** — the line counter stopped at the first `## ` heading after `## Original Content`, but verbatim bodies legitimately preserve the source article's own H2 headings, so long real bodies were counted as near-empty and would block the next edit. Counter now stops only at a trailing `## Metadata` section (or EOF).

### Fixed — broken dependency

- **`Template_AI Research Capture.md` now shipped** — `/capture-tabs` (distributed since v1.6.0) referenced this template as its required shape, but the kit never included it. Added (sanitized), so the kit's template count is now **5** (Raw Source / Wiki Page / Query Result / MOC / AI Research Capture).

### Fixed — templates vs schema drift

- `Template_Wiki Page.md` — added `explored: false` (v4 mandatory) and `verificationStatus: unverified` (v5 default); pages created from the template no longer violate the schema on creation.
- `Template_Raw Source.md` — added v2 keys `collectionPurpose` / `source-vault` / `mainVaultRelated` / `mainVaultCmds` (the ingest command already required them).
- `Template_Query Result.md` — added `reusableFor` (the query command's Step 6 already set it).

### Fixed — sanitization / genericization leftovers

- `CLAUDE.md` / `AGENTS.md` Cross-Vault Reference: hard-coded author paths (`CMDSPACE/40. Docs/...`, `03-1. Claude Code (MBP)/...`) → `{your-mothership-vault-name}` placeholders; entry-point note phrased as optional.
- `AGENTS.md` Core Context: removed dangling reference to a CLAUDE.md alias table that no longer exists in the kit; the 9-system-files table is now framed as an **optional author example** (standalone users can skip); stale "91 categories" → 87.

### Known gaps (deferred to a future minor)

- Kit `CLAUDE.md` Operations chapter still lacks the Capture Tabs / Verify / Audit sections that kit `AGENTS.md` already has (asymmetry — port planned).
- `/autoresearch` remains operating-vault-only (Generator half of the Generator-Verifier loop).

## v1.7.0 — 2026-07-01 (v5 Verification schema completion + ingest/lint cross-vault hardening)

**Source**: 운영 볼트(CMDS_LLM_Wiki)에서 검증·안정화된 v5 검증 스키마와 cross-vault 링크 하드닝을 sanitize 하여 킷으로 이식. schema 는 킷이 아직 v4 수준이었고, ingest/lint 는 링크 rot 방지 로직이 빠져 있던 갭을 메움.

### Added — v5 Verification schema completion (CLAUDE.md + AGENTS.md 양쪽)

- **Verification Properties (v5) 3 기준 블록** (지식요건해당성·정합성·확증가능성 + 운영 규칙) 을 Quality Control (v4) 다음에 추가. CLAUDE.md 는 "vs CLAUDE.md policy", AGENTS.md 는 "vs AGENTS.md policy" 로 각자 자기 스키마 참조.
- **Wiki Page 6 v5 키**: `claimType`, `evidenceScope`, `verificationStatus`, `verifiedAt`, `verifiedBy`, `disputed` 추가.
- **camelCase 목록 v5 엔트리 8개**: ✅ 6개(위 키) + ❌ 2개(`claim_type`, `verification-status`).
- **`> [!warning] Disputed Claim` 콜아웃** 을 Callout Conventions 에 추가 (Contradiction 과 별개 — `/verify --resolve` 로만 해소).
- **Parity Contract 콜아웃** (CLAUDE.md ↔ AGENTS.md) — 두 스키마 미러가 반드시 동일해야 하는 섹션(Cross-Agent Matrix · Frontmatter Standards · v5 3기준 · Callout Conventions) 을 명문화.

### Added — lint v5 coverage reporting

- `.claude/commands/lint.md`: Step 8 헤더 `v2/v4` → `v2/v4/v5`, v5 검증 필드(`claimType`/`evidenceScope`/`verificationStatus`) 커버리지 체크 + `disputed` → `/verify --resolve` 큐 추가. Output 에 "v5 Verification Coverage" 항목 추가.
- `.codex/commands/lint.md`: 이미 v5 verification + cross-vault integrity 항목 보유(변경 불필요).

### Added — ingest/lint cross-vault hardening (sanitized)

- **Step 0.5 Format Conversion** (binary → markdown): `.pdf`/`.pptx`/`.docx`/`.hwp`/`.epub`/image 등을 변환 후 ingest, 원본은 `80. References/Attachments/` 로 보존 (`.claude` + `.codex` ingest 양쪽).
- **`mainVaultRelated` URL percent-encoding 필수 검증**: qmd 반환 실제 경로 사용 → `urllib.parse.quote(safe='')` 인코딩 → `test -f` stat 검증 → `obsidian://open?vault=...&file=` 구성. 손으로 URL 추측 금지.
- **`mainVaultCmds` authoritative 목록**: `find ... -name "📚 [0-9][0-9][0-9] *.md"` 로 실제 카테고리 집합을 만든 뒤 정확 매칭. 추측 금지.
- **Cross-vault link integrity 검사** (ingest Step 6/7 + lint Step 10): touched 파일의 `obsidian://` URL 과 `mainVaultCmds` 를 모선 파일시스템에 stat 대조, 깨진 링크·리터럴 placeholder 적발.
- **Index-sync 검증** 강화: 신규 Wiki 페이지가 index.md 섹션에 실제로 나타나는지 `grep -F`, Stats 카운트를 `find | wc -l` 로 대조.
- **CLAUDE.md `mainVaultRelated` 설명** 을 AGENTS.md 와 정합하도록 `obsidian://` 클릭 링크 형식으로 통일 (Parity Contract 준수).

### Sanitization

- 모든 이식분에서 실제 경로/볼트명 제거 → `{PATH_TO_YOUR_MOTHERSHIP_VAULT}` · `{your-mothership-vault-name}` placeholder. cross-vault 단계는 "mothership only" 로 표기 — 모선 없이 단독 운영 시 skip.

### No breaking changes

기존 v1.6.x 볼트는 갱신 파일만 pull. v5 키는 전부 추가형(신규 페이지 기본 `verificationStatus: unverified`), 기존 페이지는 `/verify`/`/lint` 접촉 시 점진 backfill.

---

## v1.6.2 — 2026-06-27 (정합성 audit — sanitization sync + doc accuracy + folder scaffold)

**Source**: 배포 전 8-차원 정합성 audit (version·inventory·cross-harness·placeholder-PII·frontmatter·doc·zip·hooks), 각 finding 을 적대적으로 검증. blocker 0, confirmed 20 (major 5 / minor 5 / nit 8 + 1 dismissed). 모두 반영.

### Fixed — Sanitization sync (Codex 미러가 Claude gold 와 어긋나 있던 부분)

- **`.agents/skills/refresh-context/SKILL.md`** — 하드코딩돼 있던 5개 실제 개인 에세이 제목을 generic 패턴 (`Read("<essay path>")` + `{PATH_TO_YOUR_ESSAYS}`) 으로 교체. Claude command 는 이미 genericize 돼 있었으나 Codex skill 만 누락됐던 단일 spot.
- **`AGENTS.md` CJK Person Naming 예시** — 실명(`Yohan Koo`)·핸들(`johnfkoo951`)·제3자(`안창현/Changhyun Ahn`, `Andy Suh`)·실제 저자(`zhanghandong`) 를 CLAUDE.md gold (`홍길동`/`Gildong Hong`/`johndoe`) 로 동기화.
- **`collectionPurpose` 예시의 실제 클라이언트명** → `기업 임원교육 사례` 로 generic 화 (CLAUDE.md + AGENTS.md 양쪽).

### Fixed — Doc accuracy (제품과 어긋난 사용자 문서)

- **"7 commands" → "11 commands"**: README (×3) + Setup Guide. onboard/capture-tabs/verify/audit 누락분 추가.
- **README 가 v1.6.0 Codex 듀얼-harness 를 누락** → `.codex/` · `.agents/skills/` · `AGENTS.md` 를 구조도·파일목록·소개 bullet 에 반영.
- **Setup Guide 의 죽은 vercel 쇼케이스 URL** (`cmds-llm-wiki.vercel.app`, SSO 벽) → `llm-wiki.cmdspace.work`.
- 예시 wiki 카운트 `10개` → `16` (README·Setup Guide·index.md). index.md Stats 표 자체모순(헤더 8 vs 합계 10) 을 실제 디스크 수치(16: Concepts 9·Entities 3·Guides 2·MOC 2)로 정정.
- Setup Guide placeholder 파일 수 `12개` → "약 22개 (sed glob 이 전부 커버)". LLM-Wiki-Starter-Kit.md 의 "Codex는 이름만 변경" FAQ + 3-operations 설명을 듀얼-harness/11-command 현실로 갱신.
- AGENTS.md Codex Compatibility Matrix Notes 칼럼을 CLAUDE.md genericized 표현으로 정렬 (`v2/v4/v5`, 하드코딩 `9` 제거) + onboard Claude-전용 안내 추가.

### Added — Folder scaffold (문서가 참조하나 미생성이던 카테고리)

- `00. Inbox/01. Articles/`, `00. Inbox/05. AI Research/` (/capture-tabs 기본 저장 위치), `10. Raw Sources/12. Papers/`, `10. Raw Sources/16. AI Research/` 에 `.gitkeep` 추가 — 표준 카테고리 세트 완성. CLAUDE.md 폴더 다이어그램도 05/16 AI Research 포함하도록 AGENTS.md 와 정합.

### Housekeeping

- CHANGELOG v1.0.0 의 "18 Web Clipper" 표기를 17 로 정정 (당시 실제 17개, Stibee 는 v1.4.0 에서 18 로). 
- 정렬: canonical .DS_Store 4개 제거, `archives/cmds-llm-wiki-starter-kit.zip` (구 v1.3.0 가리키던 stale alias) 삭제 — archives/ 는 versioned ZIP 만 보관.

### Deliberately NOT changed

- `.codex/hooks/validate-raw-source.sh` 의 stub-skip 순서 (Check 1 뒤) 는 Claude 와 다르지만 **의도적·문서화된 설계** (stub 도 heading 은 필요). 양 harness 모두 well-formed stub 을 정상 통과하므로 유지.
- Karpathy X-thread 데모 wiki 페이지의 실제 공개 인물명 (Karpathy·kepano·Changhyun Ahn·Yohan Koo) 은 의도된 예시 출처라 유지 (sanitization 대상 아님).

### No schema/structure breaking changes

기존 v1.6.x 볼트는 갱신된 파일만 pull 하면 됨. 폴더 추가는 비파괴적 (.gitkeep).

---

## v1.6.1 — 2026-06-16 (3-Layer 개념층 vs 물리 폴더 정합 노트)

**Source**: 운영 볼트의 지식 레이어 재검증 과정에서, 템플릿이 `30. Queries/` 물리 폴더를 제공하면서도 3-Layer(Raw/Wiki/Schema) 개념과의 관계를 설명하지 않아 신규 사용자가 "30. Queries 는 4번째 레이어인가?" 혼동하던 지점 발견.

### Changed

- `3-Layer Architecture`: "이 볼트에서의 구현" 표 아래에 callout 추가 — `30. Queries/` 는 *4번째 구조 레이어가 아니라* Ingest-Query-Lint 의 Query 단계 산출 위치임을 명시 (구조 축 Raw/Wiki/Schema vs 운영 축 Ingest/Query/Lint 구분). 유저별 콘텐츠가 아닌 일반 개념 정합이라 템플릿에 반영.

---

## v1.6.0 — 2026-06-08 (Codex 호환 — dual-harness)

**Source**: 운영 볼트가 Claude Code + Codex 양 harness 로 정합화(같은 operation 이름을 `.claude/` · `.codex/` · `.agents/skills/` 에 1:1 유지)된 것을 공개 킷에도 반영. 이전 킷은 Claude 전용이었음.

### Added

- **`AGENTS.md`** — Codex / 타 에이전트용 schema mirror (CLAUDE.md 와 같은 규칙, audience 만 다름).
- **`.codex/`** — Codex operation harness: `commands/` 10개 (Claude commands 와 1:1 mirror) + `hooks/` (`validate-raw-source.sh`, `qmd-reindex.sh`) + `hooks.json`. 코덱스 hook 은 단순 payload shape (`tool_input.path` / `file_path` / `path`) 도 처리하고, Book Ingest `status: stub` chapter 는 body-length 검사에서 제외.
- **`.agents/skills/`** — Codex reusable operation skills 10개 (`{operation}/SKILL.md`).
- **`.claude/commands/`** 에 `capture-tabs`, `verify`, `audit` 3개 추가 (기존 8 → 11). Capture Tabs = AI research / 브라우저 탭 묶음 → Inbox pre-ingest layer. Verify = 단일 페이지 3-기준 검증. Audit = vault/MOC 전체 점검 + `/verify` 큐.

### Changed

- `CLAUDE.md`: Operations 섹션에 Agent Note + Cross-Agent Compatibility Matrix + Codex Compatibility Notes 추가, Folder Structure 에 `.codex/` · `.agents/` · `AGENTS.md` 반영, Essential operations 한 줄 갱신. version 1.5.0 → 1.6.0.

### Notes

- Codex hook 경로는 `{PATH_TO_YOUR_LLM_WIKI}` placeholder — 셋업 시 절대 경로로 치환 (또는 `/onboard` 가 처리). Claude hook 은 `$CLAUDE_PROJECT_DIR` 라 치환 불필요.

---

## v1.5.0 — 2026-06-01 (/onboard 인터뷰 셋업 커맨드)

**Source**: 온보딩이 수동 `Setup Guide.md`(sed)뿐이라, "온보딩해줘/처음 시작할게" 트리거로 필수 질문을 물으며 placeholder·Core Context를 자동으로 채우는 대화형 단계 신설.

### Added

- **`.claude/commands/onboard.md`** — 인터뷰 기반 first-run 셋업 커맨드. pre-flight 감지 → 필수 5문항(위치/이름 · Mode A·B · 모선 경로 · Core Context §1 정체성 · §2 재활용 축) + 옵션(§3·§4) → placeholder 일괄 치환 + Core Context 작성 + `status: active`. answer-1-of-many · resume · 음성 모드 · passive fallback 포함 (cmds-onboarding 철학 차용).

### Changed

- `Setup Guide.md`: 상단에 `/onboard` 대화형 경로 안내 추가, 대상 버전 v1.3.0 → v1.5.0+.

---

## v1.4.1 — 2026-05-31 (Doc Fixes · Live Showcase URL · Placeholder Count · Mothership Count Soften)

**Source**: `cmds-system-files` v4.9.0 audit surfaced three documentation bugs in this kit.

### Fixed

- **README "Live Showcase" link** → `https://llm-wiki.cmdspace.work` (the prior `cmds-llm-wiki.vercel.app` returned HTTP 401; the branded apex is live 200).
- **CHANGELOG placeholder count** corrected from "10 files" to "13 files carry placeholder tokens" (live count).
- **`Core Context.md` mothership reference** softened from a hard "5 system files" count to durable "multiple audience-specific system files … + semver changelog" phrasing — the mothership is now 9 files / 6 public after the 2026-05-27 8→9 restructure, and an un-counted phrasing won't re-stale.

### Note

- No schema/structure changes. canonical ↔ DEV mirror ↔ ZIP regenerated together.

---

## v1.4.0 — 2026-05-27 (Missing Files Audit · Hotkeys · Empty Queries Folder · Stibee Clipper)

**Source**: User audit "왜 옵시디언 웹클리퍼 json 파일들이 빠져있지?" surfaced three template gaps that had silently drifted from the live operating vault. Same release also closes the 3-place sync loop documented at v1.3.0 by promoting the canonical (`_starter-kit/cmds-llm-wiki/`) as single source of truth.

### What's missing → now included

- **`.obsidian/hotkeys.json`** (9.2 KB · 73 bindings) — Korean PKM-friendly Obsidian hotkey set used in the operating vault. Heading shortcuts (`⌘1~4`), wikilink/callout inserters (`⌘[` / `⌘]`), sidebar toggles, etc. Optional — delete if your own keymap suits you.
- **`30. Queries/`** (empty folder + `.gitkeep`) — Was missing entirely from the v1.3.0 template even though `/query` writes results here and the README structure referenced it. `.gitkeep` ensures the folder ships through git/zip.
- **`clipper-stibee.json`** — Korean newsletter platform (Stibee) Web Clipper. Operating vault has had this since 2026-04-14; v1.3.0 sanitization excluded it. Re-included for Korean newsletter users. (Sanitization decision retained: `clipper-parkjoon-mdshare.json` stays excluded — it targets a personal domain.)

### Numbers

- Clipper JSON: 17 → **18**
- Folders shipped: was missing `30. Queries/` and `.obsidian/`; now complete
- No schema changes (CLAUDE.md still v1.4 over v1.3 structurally identical except frontmatter `version`/`date modified`)

### 3-place sync canonicalised (operational doc, not template content)

Documented in parent vault's `CMDS_LLM_Wiki/CLAUDE.md` "Starter Kit Distribution (3-Place Sync)" section:
1. Canonical: `_starter-kit/cmds-llm-wiki/` (this folder, unversioned)
2. DEV mirror: `/DEV/cmds-llm-wiki/` ↔ GitHub `johnfkoo951/cmds-llm-wiki`
3. ZIP archives: `_starter-kit/cmds-llm-wiki-{starter-kit,vX.Y.Z}.zip`

🚫 `~/Downloads/cmds-llm-wiki-*.zip` is no longer used as a distribution surface. External users obtain releases via GitHub Releases.

### Placeholder coverage

13 files carry placeholder tokens (~10 require user substitution before operation). Placeholder types: `{your-name}`, `{Your Name}`, `{PATH_TO_YOUR_LLM_WIKI}`, `{PATH_TO_YOUR_MOTHERSHIP_VAULT}`, `{your-mothership-vault-name}`, `{YYYY-MM-DD}`. Run the `sed` commands in `90. Settings/Sharing/Setup Guide.md` to replace all in one shot per Mode A (standalone) or Mode B (mothership-satellite).

### Files changed

- `.obsidian/hotkeys.json` (new)
- `30. Queries/.gitkeep` (new)
- `90. Settings/Sharing/clipper-stibee.json` (new)
- `CLAUDE.md` — frontmatter `version: "1.3"` → `"1.4"`, `date modified`
- `README.md` — clipper count 17→18 (with Stibee), hotkeys.json mention, structure section
- `CHANGELOG.md` — this entry

---

## v1.3.0 — 2026-05-04 (Quality Control v4 + Tool Outputs + Multi-Harness)

**Source**: Distilled from one month of operating the parent vault since v1.2.0. Three classes of upgrade: (1) a Book Ingest hook bug uncovered during real ingestion, (2) page-level quality-control properties that emerged from a self-audit ("we have 89 wiki pages but 0% are human-verified"), (3) generalised harness compatibility for non-Claude-Code agents.

### Bug fixes

- **`validate-raw-source.sh` — skip `status: stub`**: Book Ingest chapter stubs intentionally have no `## Original Content` until the user reads them and re-invokes `/ingest` for promotion. The v1.1.0 release added Book Ingest but the verbatim-validation hook still blocked stubs as malformed Raw Sources. Hook now reads frontmatter and exits 0 for `status: stub` files.
- **`lint.md` indentation**: Step 8 sub-bullets used 2-space indent instead of TAB, violating the project's body-uses-TAB rule. Fixed.

### What's new

#### Exploration Gate (v4 frontmatter)

A page-level human-verification track on Wiki pages. Addresses the gap where `confidence: high` was being set by the LLM at compile time without any human read pass.

- New optional Wiki page properties: `explored: false|true`, `exploredBy: "[[Name]]"`, `exploredDate: YYYY-MM-DD`
- New `> [!note] Bias Check` callout pattern (Counter-argument + Data gap) for high-confidence and synthesis-heavy pages
- New `> [!check] Exploration Gate` callout for documenting verification status
- `/ingest` now emits new pages with `explored: false` by default and adds Bias Check on `confidence: high`
- `/lint` Step 8 reports `explored` coverage % and high-confidence pages without bias check
- `/status` reports `explored:` and `mainVault*:` coverage %
- `/query` flags missing `mainVaultRelated`, `explored`, or Bias Check during synthesis

#### `70. Outputs/` Tool Output Convention (optional)

A separate folder for external-tool side products (graphify, audio-transcriber, etc.) that should not pollute the Wiki layer. Generic pattern: `70. Outputs/{tool-name}/{YYYY-MM-DD}-{topic}/`. Outputs are exempt from the standard schema (frontmatter, naming) — they're the tool's format. Insights distilled from outputs go into `30. Queries/` or get absorbed into Wiki pages, so Wiki body never wikilinks into `70. Outputs/`. Skip this folder entirely if you don't run such tools.

#### CJK Person Naming Rule

Native script only for Korean / Chinese / Japanese person entities; English Romanization moves to `aliases`. Examples: `홍길동.md`, `张汉东.md` (not `홍길동 (Gildong Hong).md`). Latin handles + real-name combos (`kepano (Steph Ango).md`) keep their existing form. Reasons: file-name duplication adds wikilink friction, Romanization is transliteration not identity, Obsidian graph/search reads aliases.

#### Multi-harness comment headers

Every `.claude/commands/*.md` now carries a YAML-comment line listing the equivalent tool names on Antigravity (Gemini) and similar harnesses — `view_file`, `write_to_file`, `replace_file_content`, `list_dir`, `grep_search`, `run_command`, `read_url_content`. Helps users running these commands through non-Claude-Code agents identify the equivalent tool surface.

#### Genericised "7 reuse axes"

`/ingest` and `/query` previously hard-coded the parent vault's specific axes (PhD / 학술 / 강의 / 컨설팅 / CMDS 시스템 / 에세이 / 제품). Now both files reference [[Core Context]] §2 directly with neutral examples (학술 / 저술 / 강의 / 컨설팅 / 제품 / 에세이 / 커뮤니티). User-defined axes (5~9 recommended) remain the source of truth.

#### Setup Guide (deeper personalization manual)

New `90. Settings/Sharing/Setup Guide.md` — covers Mode A (standalone) vs Mode B (mothership-satellite) operation, single-pass `sed` replacement commands per mode, verification `grep`, 8-step setup procedure, and 7-item FAQ. Complements README.md (which stays as the GitHub-facing 5-step quick start). Convertible to PDF via the same `md-to-pdf` workflow used to produce the 2026-04-30 standalone PDF.

### Files changed

- `.claude/hooks/validate-raw-source.sh` — stub skip
- `.claude/commands/{ingest,inbox,lint,query,refresh-context,reindex,status}.md` — Antigravity equivalents header
- `.claude/commands/ingest.md` — Quality control v4 block + genericised axes
- `.claude/commands/lint.md` — Step 8 v2/v4 coverage + indent fix
- `.claude/commands/status.md` — explored + mainVault coverage lines
- `.claude/commands/query.md` — quality gap flagging + genericised axes
- `CLAUDE.md` — `70. Outputs/` section, Frontmatter Standards v4 block, CJK naming rule, Bias/Exploration callouts, version bump 1.0 → 1.3
- `90. Settings/Sharing/Setup Guide.md` — new
- `README.md` — pointer to Setup Guide above the 5-step quick start
- `CHANGELOG.md` — this entry

### Migration notes

No breaking changes. Existing v1.2.0 vaults adopt v1.3.0 by:
1. Pulling the updated hook (`validate-raw-source.sh`) — required if you use Book Ingest
2. Pulling updated commands and CLAUDE.md — adds optional fields, doesn't break existing pages
3. (Optional) backfilling `explored: false` on existing Wiki pages via `/lint` flag list

---

## v1.2.0 — 2026-04-29 (Cohort Learnings)

**Source**: Distilled from a real classroom cohort that adopted LLM Wiki Starter Kit as the practical backbone of a regular university course (10 students, 10 distinct domains — systematic review, healthcare AI, anti-aging content, silver-care market analysis, sports analytics, biomedical research, embryology AI, etc.). All cohort-specific names, organizations, and personal contexts have been anonymized — only the generalizable patterns and operational learnings ship in this template.

### What's new

#### `/ingest` skill — Inbox cleanup discipline (operational fix)

Previously possible failure mode: writing the Raw Source but forgetting to delete the Inbox original → next `/inbox` scan re-ingests the same source → duplicate Raw Sources. Now explicit:

- **Step 2 renamed** to "Save Raw Source (Move, not Copy)" with prominent warning callout
- **Inbox cleanup section** added — when source originated from `00. Inbox/`, the Inbox file MUST be deleted after pre-flight checklist passes (with source-origin matrix specifying when delete applies)
- **Step 7 verification** — explicit Inbox cleanup check (`ls "00. Inbox/{subfolder}/"` should not show consumed file)
- **Failure modes** section restructured: (1) summarization-instead-of-verbatim, (2) Inbox residue

Edge case documented: delete only AFTER all pre-flight checks pass, otherwise verbatim failure could lose the only copy.

#### New Concepts (4)

- **`Cohort Token Economy`** — Predictable failure pattern when 80%+ of a cohort relies on Pro plan. Distinguishes cohort runs from individual hobbyist usage. Informs curriculum/onboarding design (token economy must be in week 1, not discovered in week 4).
- **`External Pre-processing Pattern`** — "Claude 가 잘하는 것 만 Claude 에게 시킨다." Heavy raw conversion (long PDFs, video transcripts, large web scrapes, foreign-language content) goes to GPT Deep Research / Google AI Studio / Whisper STT first; only the distilled output enters LLM Wiki via `/ingest`. Cohort estimates: 50-80% token savings.
- **`Track Classification and Research Gap Detection`** — Custom command pattern for typology-driven domains. Splits ingested papers into thematic tracks during ingest, computes per-track coverage %, surfaces lowest-coverage track as research gap. Generalizable across systematic review · market analysis · content planning · learning path design. Includes `/track` skill proposal.
- **`Idea Generation Pipeline`** — Each new raw source triggers automatic idea generation tied to a domain seed context. Distinguishes LLM Wiki from passive learning tools (NotebookLM-style) by treating each new input as a divergence prompt, not just a record. Includes `/idea` skill proposal.

#### New Guide (1)

- **`LLM Wiki Token Optimization Strategies`** — 4-step practical guide (1: external preprocessing → 2: model selection → 3: `/effort` throttling → 4: infrastructure decisions). Designed as a curriculum companion when introducing LLM Wiki to a class, lab, or study cohort. Includes decision-flow diagram, week-by-week curriculum recommendation, and policy-change hedge advice (don't lock cohorts into a single vendor).

### Files changed

- `.claude/commands/ingest.md` — Step 2 title + Inbox cleanup section + Step 7 verification + Failure modes restructure
- `20. Wiki/21. Concepts/Cohort Token Economy.md` — new
- `20. Wiki/21. Concepts/External Pre-processing Pattern.md` — new
- `20. Wiki/21. Concepts/Track Classification and Research Gap Detection.md` — new
- `20. Wiki/21. Concepts/Idea Generation Pipeline.md` — new
- `20. Wiki/23. Guides/LLM Wiki Token Optimization Strategies.md` — new
- `CHANGELOG.md` — this entry

### Migration notes

No breaking changes. Existing v1.1.0 vaults can adopt v1.2.0 by:
1. Pulling the updated `.claude/commands/ingest.md`
2. Copying the 4 new concept pages and 1 new guide page (or letting `/ingest` auto-generate them as wikilinks resolve)
3. Reviewing `Cohort Token Economy` if running a cohort

---

## v1.1.0 — 2026-04-20 (Book Ingest Pattern)

**Addition**: `/ingest` operation gains a new variant — **Book Ingest Mode (Progressive Stubs)** — for multi-page books and documentation sites.

### What it solves

멀티 페이지 책 (mdBook, VitePress, GitBook, Docusaurus, ReadTheDocs, Nextra 등 TOC ≥5 챕터) 을 표준 `/ingest` 로 처리하면 두 가지 실패:

1. **한 파일에 전부** → 가독성 붕괴, `## Original Content` 비대화
2. **전체 동시 컴파일** → 읽지도 않은 내용이 Wiki 에 심어져 contamination (AI 요약이 human-curated knowledge 자리 차지)

### How it works

- **Scaffold**: 1 Book Index Raw Source (verbatim preface + TOC with wikilinks) + N chapter stubs (`status: stub`, placeholder `## Original Content`, navigable via `chapterPrev`/`chapterNext`)
- **Wiki seed**: book entity + author entity + preface-anchor concept (≤3 페이지). 장별 wiki 는 **미생성**.
- **Promote on read**: 사용자가 장을 읽을 때 해당 stub 파일에 `/ingest` 재호출 → URL 에서 verbatim fetch + `## Original Content` 채움 + 장 특화 Wiki 컴파일 + `status: stub → completed` + Book Index Progress Tracking 업데이트

Karpathy "지식은 스크랩이 아니라 독서 시점에 컴파일" 원칙의 구체화. [[Progressive Disclosure Pattern]] 의 ingest-layer 대응.

### New frontmatter keys (Raw Source, book stubs only)

- `status: stub | reading | completed` (기존 `ingested` 와 병존)
- `bookIndex` — 소속 Book Index wikilink
- `chapterNumber` — 정수
- `chapterPart` — 편/파트 이름 (원문 언어 보존)
- `chapterPrev` / `chapterNext` — 이전·다음 챕터 wikilink (null 가능)

### File naming

- Book Index: `YYYY-MM-DD-{authorSlug}-{bookSlug}-book-index.md`
- Chapter Stub: `YYYY-MM-DD-{authorSlug}-{bookSlug}-ch{NN}-{slug}.md`

### Files changed

- `.claude/commands/ingest.md` — "Book Ingest Mode (Multi-Page Sources)" 섹션 추가 (step B-1 ~ B-5 + promotion workflow + hook interaction + visual pattern)
- `CLAUDE.md` — Operations §1 Variants callout + Raw Source frontmatter 에 `status` enum 확장 + Book Ingest 전용 4 키 + 파일 네이밍 테이블 2 행 추가
- `20. Wiki/21. Concepts/Book Ingest Pattern.md` — 신규 self-documenting concept 페이지 (architecture, lifecycle, 적합성 매트릭스, hook interaction)

### Hook compatibility

`validate-raw-source.sh` 는 stubs 도 통과 — 모든 stub 이 `## Original Content` 섹션을 placeholder 와 함께 보유. Hook 이 본문 substantiveness 검사로 업그레이드될 경우 `status: stub` 예외 처리 필요 (document in Book Ingest Pattern concept).

---

## v1.0.0 — 2026-04-14 (Initial Template Release)

**Source**: Extracted and sanitized from Yohan Koo's personal LLM Wiki satellite vault, active since 2026-04-10.

### Architecture

- **3-Layer**: Raw Sources (immutable) / Wiki (LLM-managed) / Schema (CLAUDE.md)
- **Operations**: Ingest · Query · Lint · Refresh-Context
- **Core files**: `index.md`, `log.md`, `CLAUDE.md`, `Core Context.md`

### Claude Code Harness

- **7 slash commands** in `.claude/commands/`:
  - `/ingest` — purpose-gated source ingestion with mothership cross-link search
  - `/inbox` — batch scan of `00. Inbox/` with single-axis / per-file / auto-infer modes
  - `/query` — wiki-grounded Q&A with 7-axis reuse tagging
  - `/lint` — health check (orphans, broken links, contradictions, v2 coverage, Core Context freshness)
  - `/status` — at-a-glance stats + coverage metrics
  - `/reindex` — manual qmd index rebuild
  - `/refresh-context` — re-snapshot Core Context when mothership drifts
- **2 PostToolUse hooks** in `.claude/hooks/`:
  - `validate-raw-source.sh` — enforces `## Original Content` verbatim preservation
  - `qmd-reindex.sh` — debounced auto-reindex on Write/Edit

### Schema Standards

- **YAML 2 spaces / Body TAB** indentation
- **7 required properties**: `type`, `aliases`, `description` (English), `author`, `date created`, `date modified`, `tags`
- **Wikilinks in YAML must be quoted**: `"[[link]]"`
- **Mermaid labels in quotes**: `A["label"]`
- **camelCase for new YAML keys**: `collectionPurpose`, `mainVaultRelated`, `mainVaultCmds`, `reusableFor`

### 미래의 나에게 보내는 편지 Policy (v2 frontmatter)

- **`collectionPurpose`** — mandatory user answer to "왜 수집?" at ingest time
- **`mainVaultRelated`** — 2~5 related notes from (optional) mothership vault, found via qmd
- **`mainVaultCmds`** — mothership CMDS category (if applicable)
- **`reusableFor`** — which of the 7 reuse axes a query answer feeds

### Collection Infrastructure

- **17 Obsidian Web Clipper templates** in `90. Settings/Sharing/` (Stibee added in v1.4.0 → 18):
  - Articles (web, tech-blog, news, substack), Social (X, threads, linkedin, reddit, instagram, hackernews)
  - Video (youtube, podcast), Technical (github, arxiv, tech-docs, linkedin-pulse)
  - Selection clipper for ad-hoc highlights
- **qmd config template** in `90. Settings/qmd-config-template.yml` — BM25 + vector hybrid search

### Example Content

- 2 Raw Sources (Karpathy LLM Wiki gist + X thread)
- 4 Concept wiki pages (LLM Wiki Pattern, RAG vs Compiled Wiki, 3-Layer Architecture, Ingest-Query-Lint Cycle)
- 3 Entity pages (Karpathy, Vannevar Bush, Memex)
- 1 Guide (Obsidian Tooling for LLM Wiki)
- 2 MOCs (Knowledge Management, LLM Wiki Guide)

### Notes

- Template uses `{your-name}`, `{Your Name}`, `{PATH_TO_YOUR_LLM_WIKI}`, `{PATH_TO_YOUR_MOTHERSHIP_VAULT}`, `{your-mothership-vault-name}` placeholders per the `cmds-system-files` convention.
- Mothership integration is **optional** — this wiki operates standalone or as satellite to any Obsidian PKM vault.
