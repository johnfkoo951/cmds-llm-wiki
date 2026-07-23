# cmds-llm-wiki 셋업 가이드

| 항목 | 내용 |
|------|------|
| 대상 | `cmds-llm-wiki` v1.10.0+ |
| 작성 | 2026-06-27 · 갱신 2026-07-23 |
| 전제 | macOS · Obsidian 1.5+ · Claude Code (또는 Codex) · Git |

---

## 1. 이 키트는 무엇인가

Karpathy LLM Wiki 패턴을 그대로 실행 가능한 형태로 옮긴 **Obsidian 볼트 + Claude Code 프로젝트**. 외부 자료 (기사·논문·전사) 를 LLM 이 한 번 컴파일하여 복리로 자라는 persistent wiki 로 축적하는 시스템.

세 가지가 한 폴더에 들어있다.

**1. Obsidian 볼트 골격** — `00. Inbox`, `10. Raw Sources`, `20. Wiki`, `30. Queries`, `40. Paper Analyses`, `80. References`, `90. Settings` 7 폴더 + `index.md` / `log.md`.

**2. Claude Code + Codex 듀얼 harness** — `.claude/commands/` 의 11 슬래시 명령어 (`/ingest`, `/query`, `/lint`, `/inbox`, `/status`, `/reindex`, `/refresh-context`, `/onboard`, `/capture-tabs`, `/verify`, `/audit`) + `.claude/hooks/` 의 PostToolUse 훅 2개 (raw source verbatim 검증 + qmd 자동 재인덱스) + `.claude/settings.json`. Codex 사용자는 `.codex/commands/` (10, onboard 제외) + `.agents/skills/` (10) + `AGENTS.md` 미러를 그대로 사용.

**3. 사용자 맥락 템플릿** — `CLAUDE.md` (스키마), `Core Context.md` (사용자 정체성·재활용 축·철학 placeholder 노트), `90. Settings/Templates/` (노트 템플릿 11종 — raw source · wiki page · query result · MOC · AI research capture · research question · synthesis · paper hub · paper analysis note · atomization SPEC · scale page — + 12-Step Analysis Schemes 스킴 문서), `90. Settings/Sharing/clipper-*.json` 18 개 (Obsidian Web Clipper 사이트별 템플릿).

---

## 2. 자기 볼트로 쓸 수 있는가

**가능. 그게 권장 사용법.**

이 레포 자체가 "fork 해서 본인 볼트로 쓰는" 템플릿이다. 두 가지 운영 모드 중 하나를 선택한다.

### Mode A — Standalone (단독 운영)

별도 PKM 볼트 없이 이 키트 하나만 쓴다. 가장 단순하고 빠른 시작.

- 모든 수집·합성이 이 볼트 안에서 끝남
- `Core Context.md` §5 (Mothership 섹션) 는 비우거나 삭제
- placeholder 중 `{PATH_TO_YOUR_MOTHERSHIP_VAULT}`, `{your-mothership-vault-name}` 무시 가능

### Mode B — Satellite (모선 볼트 연계)

이미 운영 중인 PKM 볼트가 따로 있고, 이 키트를 LLM 전용 satellite 로 둔다. 두 볼트가 cross-reference 로 연결됨.

- `Core Context.md` §5 에 모선 볼트의 시스템 파일 경로 등록
- Raw Source frontmatter 에 `mainVaultRelated`, `mainVaultCmds` 자동 채워짐
- `obsidian://open?vault=...` URL 로 모선 노트 클릭 가능

`Mode A → Mode B` 전환은 언제든 가능 (`Core Context.md` §5 만 채우면 됨).

---

## 3. 셋업 절차

> 💡 **대화형으로 하려면**: Claude Code에서 **`/onboard`** 실행 (트리거: "온보딩해줘", "처음 시작할게"). 아래 Step 1·4·5(위치·placeholder 치환·Core Context)를 필수 질문 인터뷰로 자동 진행한다. 수동으로 하려면 아래 절차를 그대로 따른다.

### Step 1 — 위치 결정 및 이름 변경

`~/Downloads/cmds-llm-wiki/` 는 임시 위치. 영구 위치로 옮기면서 본인 볼트명으로 변경한다.

```bash
mv ~/Downloads/cmds-llm-wiki ~/DEV/my-llm-wiki
cd ~/DEV/my-llm-wiki
```

볼트 이름은 자유. 예: `johndoe-wiki`, `research-vault`, `LLM-Wiki`. **공백 없는 이름 권장** (Claude Code 경로 처리가 더 깔끔).

### Step 2 — Git 원격 분리

원본 템플릿과 본인 볼트의 git 이력을 분리한다. 본인 볼트로 운영할 거라면 fresh 시작이 깔끔.

```bash
rm -rf .git
git init
git add .
git commit -m "init: my llm wiki from cmds-llm-wiki template"
```

업스트림 템플릿 업데이트를 추적하고 싶다면 `git remote add upstream https://github.com/johnfkoo951/cmds-llm-wiki.git` 추가하고 가끔 `git fetch upstream` 으로 변경사항 확인.

### Step 3 — Obsidian 볼트로 열기

Obsidian → `Open folder as vault` → `~/DEV/my-llm-wiki/` 선택.

볼트 이름은 Obsidian 사이드바 상단에 폴더명으로 표시됨. 변경하려면 폴더 자체를 rename.

### Step 4 — Placeholder 일괄 치환

다음 placeholder 가 여러 파일에 흩어져 있다 (`.codex/` · `.agents/` 추가로 약 22 개 파일). 아래 sed glob 이 `*.md`/`*.json`/`*.yml`/`*.sh` 를 모두 훑으므로 정확한 파일 수는 신경 쓸 필요 없다. 한 번에 치환한다.

| Placeholder | 치환할 값 (예) | 비고 |
|---|---|---|
| `{your-name}` | `홍길동` | wikilink 친화 (한국어·핸들·실명 모두 가능). YAML 안에서 `"[[홍길동]]"` 형태로 들어감 |
| `{Your Name}` | `Jane Doe` 또는 `홍길동` | 표시용 이름 (Core Context §1) |
| `{PATH_TO_YOUR_LLM_WIKI}` | `/Users/foo/DEV/my-llm-wiki` | 절대경로. `pwd` 결과 그대로 |
| `{PATH_TO_YOUR_MOTHERSHIP_VAULT}` | `/Users/foo/Vaults/Main-PKM` | Mode B 전용. Mode A 면 무시 |
| `{PATH_TO_YOUR_MOTHERSHIP}` | (위와 동일) | 일부 파일에서 다른 키 이름 사용 |
| `{your-mothership-vault-name}` | `Main-PKM` | Mode B. 모선 폴더명만 (경로 X). `obsidian://open?vault=` URL 에 들어감 |
| `{YYYY-MM-DD}` | `2026-04-30` | Core Context 의 `date created`, `date modified`, `snapshot_date` |

#### 일괄 치환 명령어 (Mode A — 단독 운영)

```bash
cd ~/DEV/my-llm-wiki

LC_ALL=C find . -type f \( -name "*.md" -o -name "*.yml" -o -name "*.json" -o -name "*.sh" \) \
  -not -path "./.git/*" \
  -exec sed -i '' \
  -e 's|{your-name}|홍길동|g' \
  -e 's|{Your Name}|홍길동|g' \
  -e "s|{PATH_TO_YOUR_LLM_WIKI}|$PWD|g" \
  -e "s|{YYYY-MM-DD}|$(date +%Y-%m-%d)|g" \
  {} +
```

#### 일괄 치환 명령어 (Mode B — 모선 연계)

위에 더해서 모선 경로·이름도 함께 치환.

```bash
LC_ALL=C find . -type f \( -name "*.md" -o -name "*.yml" -o -name "*.json" -o -name "*.sh" \) \
  -not -path "./.git/*" \
  -exec sed -i '' \
  -e 's|{PATH_TO_YOUR_MOTHERSHIP_VAULT}|/Users/foo/Vaults/Main-PKM|g' \
  -e 's|{PATH_TO_YOUR_MOTHERSHIP}|/Users/foo/Vaults/Main-PKM|g' \
  -e 's|{your-mothership-vault-name}|Main-PKM|g' \
  {} +
```

#### 치환 검증

치환 후 남은 placeholder 가 있는지 확인.

```bash
grep -rn "{your-name}\|{Your Name}\|{PATH_TO\|{your-mothership\|{YYYY-MM-DD}" \
  --include="*.md" --include="*.json" --include="*.yml" --include="*.sh" \
  -l | grep -v ".git"
```

출력이 비어 있으면 통과. Mode A 라면 `{PATH_TO_YOUR_MOTHERSHIP*}` `{your-mothership-vault-name}` 만 남아 있어도 무해 (해당 섹션을 안 쓰므로).

### Step 5 — Core Context 채우기

`Core Context.md` 를 열어 본인 맥락으로 채운다. 이 노트는 LLM 이 모든 ingest / query / lint **전에** 먼저 읽는 사용자 맥락 앵커.

#### 필수 섹션

**§1 정체성** — 이름, 역할, 전문 분야, 주 활동 영역, 그리고 **연속성 선언** (현재 활동이 과거의 어떤 질문에서 출발했는지 1~3 문장).

**§2 재활용 축 5~9 개** — "이 소스가 어디에 쓰일 것인가" 의 축. 7 개 권장. 예: 학술 / 저술 / 강의 / 컨설팅 / 제품 / 에세이 / 커뮤니티. 너무 적으면 모든 수집이 같은 축으로 쏠리고, 너무 많으면 축 자체가 무의미.

#### 옵션 섹션

**§3 개인 프레임워크** — 자체 지식 관리 프레임워크가 있으면 기록.

**§4 철학 3~5 개** — LLM 이 ingest 시 "내 철학과 정렬되는가" 판단할 원칙.

**§5 모선 볼트** — Mode B 일 때만 채움. Mode A 면 섹션 통째로 삭제 권장.

#### 채우는 3 가지 방식

방식 1. **직접 작성** — 섹션별로 직접 입력.

방식 2. **기존 기록에서 추출** — 블로그·노트·에세이가 있으면 LLM 에게 "이 글들을 읽고 Core Context 를 채워줘" 라고 요청.

방식 3. **STT 인터뷰** — 마이크로 자기소개·목적·철학 녹음 → LLM 에게 정리 요청.

#### 마무리

- frontmatter `status: template` → `status: active` 로 변경
- frontmatter `snapshot_date` 오늘 날짜
- `version: "1.0"` 유지

### Step 6 — qmd 설치 (선택, 권장)

로컬 검색 엔진. BM25 + 의미 검색 + HyDE 모두 지원. Claude Code 의 MCP 도구로 wiki 검색 가능.

```bash
brew install qmd-search/qmd/qmd

mkdir -p ~/.config/qmd
cp "90. Settings/qmd-config-template.yml" ~/.config/qmd/index.yml

# index.yml 안의 {PATH_TO_YOUR_LLM_WIKI} 가 Step 4 에서 이미 치환됐는지 확인
grep "{PATH_TO" ~/.config/qmd/index.yml  # 출력 없어야 정상

# 임베딩 모델 (한국어 지원)
echo 'export QMD_EMBED_MODEL="hf:Qwen/Qwen3-Embedding-0.6B-GGUF/Qwen3-Embedding-0.6B-Q8_0.gguf"' >> ~/.zshrc
source ~/.zshrc

qmd update && qmd embed
```

설치 후 Claude Code 안에서 `mcp__qmd__query` 도구로 검색 가능. PostToolUse 훅 (`qmd-reindex.sh`) 이 wiki 편집 시 자동으로 인덱스 업데이트.

### Step 7 — Obsidian Web Clipper (선택)

`90. Settings/Sharing/clipper-*.json` 의 18 개 사이트별 템플릿 (Article / YouTube / Substack / X / arXiv / Hacker News / Naver Blog 등) 을 Obsidian Web Clipper 에서 import.

브라우저에서 Web Clipper 확장 설치 → Settings → Templates → Import → JSON 파일 선택.

자료를 클리핑하면 `00. Inbox/` 의 적절한 서브폴더로 자동 저장. 이후 `/inbox` 또는 `/ingest` 로 처리.

### Step 8 — Claude Code 첫 실행

```bash
cd ~/DEV/my-llm-wiki
claude
```

#### 첫 명령어 추천 순서

```text
/status
```

볼트 상태 점검. 카운트, Core Context snapshot 나이, inbox 백로그 표시.

```text
/ingest <URL>
```

관심 기사·논문 하나로 첫 ingest. **목적 질문이 뜨면 §2 재활용 축 중 하나 골라서 답변** — 이게 "미래의 나에게 보내는 편지" 의 핵심. Raw Source + 10~15 wiki 페이지가 생성됨.

```text
/query <질문>
```

방금 쌓은 wiki 로 첫 질의.

```text
/lint
```

건강도 체크 — orphan, broken link, contradiction, stale 페이지 점검.

---

## 4. 개인화 체크리스트

### 필수 항목

- [ ] 폴더 이름 본인 볼트명으로 변경 (`my-llm-wiki` 등)
- [ ] `git init` 으로 git 이력 fresh start
- [ ] Placeholder 7 종 치환 (`{your-name}`, `{Your Name}`, `{PATH_TO_YOUR_LLM_WIKI}`, `{YYYY-MM-DD}` 4 종 + Mode B 면 모선 3 종)
- [ ] `grep -rn "{your-name}\|{PATH_TO" ...` 로 치환 누락 검증
- [ ] `Core Context.md` §1 정체성 작성
- [ ] `Core Context.md` §2 재활용 축 5~9 개 정의
- [ ] `Core Context.md` frontmatter `status: active` + `snapshot_date` 오늘 날짜
- [ ] `index.md` 의 카운트 (현재 예시 wiki 약 16 개) 가 본인 볼트 실제 카운트로 업데이트되도록 첫 `/lint` 실행
- [ ] `.claude/hooks/*.sh` 실행권한 확인 (`chmod +x .claude/hooks/*.sh`)

### 권장 항목

- [ ] qmd 설치 + 첫 인덱싱
- [ ] Obsidian Web Clipper 템플릿 import (자주 쓰는 사이트만)
- [ ] `Core Context.md` §4 철학 3~5 개 작성
- [ ] `.gitignore` 점검 — 기본값에 `.claude/sessions/`, `.qmd/`, `.obsidian/workspace*` 등 제외 설정됨

### 옵션 항목 (Mode B 만)

- [ ] `Core Context.md` §5 에 모선 볼트 시스템 파일 경로 등록
- [ ] `CLAUDE.md` 의 "메인 볼트 연결" 표 채우기
- [ ] 모선 볼트의 진입점 노트 만들기 (모선 → 위성 wikilink)

### 정리 항목

- [ ] 예시 콘텐츠 처리 결정 — Karpathy 예시 raw source 2 개 + wiki 약 16 개를 (a) 그대로 둘지 (b) 삭제하고 빈 상태로 시작할지. 패턴 학습 목적이면 (a), 처음부터 본인 자료만 원하면 (b).
- [ ] (b) 선택 시: `rm "10. Raw Sources/11. Articles/2026-04-"*.md "20. Wiki"/*/*.md` (21~25 하위 예시 wiki 전체) 삭제 후 `index.md` 재생성 (`/lint`)

---

## 5. 자주 묻는 질문

### Q. 볼트명은 어디서 정의되나

Obsidian 은 **폴더명을 볼트명으로 사용**. 별도 설정 파일 없음. 폴더를 rename 하면 자동 반영.

`obsidian://open?vault=...` URL 의 `vault=` 값은 Obsidian 의 vault ID (= 폴더명). Mode B 의 모선 볼트 참조에서 이 값을 사용.

### Q. 폴더 이름의 숫자 prefix (`10.`, `20.`) 를 바꿔도 되나

가능. 단 `CLAUDE.md` 의 "Folder Structure" 섹션과 `.claude/commands/*.md` 안의 경로 참조도 같이 수정해야 함. 권장하지 않음 (Karpathy / cmds 컨벤션을 깨뜨려서 다른 사람 자료와 호환성 떨어짐).

### Q. Mode A 로 시작했다가 나중에 Mode B 로 전환하려면

`Core Context.md` §5 만 채우면 됨. 기존 raw source 의 frontmatter 에 `mainVaultRelated` 가 비어있는 건 그대로 두거나, `/lint` 실행 시 LLM 에게 "기존 raw source 들의 mainVaultRelated 를 backfill 해달라" 고 요청.

### Q. CLAUDE.md 를 내 입맛대로 수정해도 되나

권장. CLAUDE.md 는 LLM 의 행동 규칙. 본인 워크플로우에 맞게 추가/삭제/수정. 단 다음 4 가지는 유지 권장.

- YAML 2 SPACES / Body TAB 규칙
- Wikilink in YAML quoted (`"[[link]]"`)
- 필수 7 프로퍼티 (`type`, `aliases`, `description`, `author`, `date created`, `date modified`, `tags`)
- 3-Layer 아키텍처 (Raw Sources / Wiki / Schema)

이건 Karpathy 패턴의 골격이라 깨뜨리면 다른 슬래시 명령어들이 망가짐.

### Q. `description` 필드를 한국어로 써도 되나

가능하지만 권장하지 않음. `description` 은 **LLM 에게 주는 hint** 라서 영어가 토큰 효율 + 모델 이해도 모두 나음. 본인이 읽을 설명은 본문에 한국어로 쓰면 됨.

### Q. Research Question / Synthesis 카드는 언제 쓰나

(v1.9.0+) 일반 wiki 페이지가 "알게 된 것" 이라면 두 카드는 "묻고 있는 것 / 주장하는 것" 이다.

- **Research Question** (`20. Wiki/25. Questions/RQ-{slug}.md`, `Template_Research Question`) — 여러 페이지에서 반복 등장하거나 실제 산출물 (논문·책·블로그 시리즈·제품 결정) 로 이어질 질문. `> [!question] Open Question` 콜아웃에서 승격하고 `sourceCallout` 으로 역추적. `status` (open → investigating → answered / parked) 로 질문의 생애를, `feedsInto` 로 어느 산출물로 흘러가는지 추적.
- **Synthesis** (`30. Queries/`, `Template_Synthesis`) — `/query` 가 반응형 답변이라면 synthesis 는 능동 논증: `thesis` 한 문장을 근거와 함께 방어. 반론은 지우지 않고 `counters` + `> [!warning]` 콜아웃으로 보존.
- 둘 다 **필수 아님**. 위키가 축적 단계일 때는 없어도 되고, 산출물 단계로 넘어갈 때 도입하면 된다. 엄밀한 인용이 필요한 산출물 (논문·책) 이 목표면 `CLAUDE.md` 의 "Citation Standard (옵션)" 섹션 (BetterBibTeX citekey + `[@citekey]`) 을 함께 채택.

### Q. 논문 (paper) 은 어떻게 ingest 하나

(v1.10.0+) `/ingest` 에 DOI·arXiv·저널 URL 또는 논문 PDF 를 주면 **Paper Ingest Mode** 가 자동 발동한다 — Standard 의 10~15 위키 페이지 대신, 논문 한 편을 `40. Paper Analyses/{citekey}/` 아래 **12단 분석** (허브 S00 + 지식 원자 30~100+) 으로 해부한다. 집필 시 인용·팩트체크·paraphrase 대조가 목적. 질문은 2개만 (수집 목적/타깃 RQ + 논문 유형). 전체 방법은 **`90. Settings/Sharing/Paper Ingest Guide.md`** (12단계 설명 포함) 참고. 가볍게 수집만 하려면 P-0 질문에서 "단순 수집" 을 고르면 Standard 로 전환된다.

### Q. PostToolUse 훅이 동작 안 한다

```bash
ls -la .claude/hooks/
chmod +x .claude/hooks/*.sh
cat .claude/settings.json  # PostToolUse 블록 확인
```

훅이 실패해도 ingest 자체는 진행됨. `validate-raw-source.sh` 는 Raw Source 의 `## Original Content` 섹션 누락을 막는 verbatim 검증이라 깨졌으면 디버깅 권장.

---

## 6. 다음 단계

- 첫 `/ingest` 후 wiki 가 어떻게 자라는지 관찰
- 10~20 회 ingest 누적되면 `/query` 의 답변 품질이 눈에 띄게 좋아짐
- 같은 질문이 여러 페이지에서 반복되면 Open Question 콜아웃을 `20. Wiki/25. Questions/` 의 **Research Question 카드**로 승격 — 답이 아니라 질문 자체를 추적 (v1.9.0+, 위 FAQ 참고)
- 하나의 주장을 방어할 단계가 되면 `30. Queries/` 에 **Synthesis 카드** — thesis + 근거 + 반론 + gap (v1.9.0+)
- 논문을 본격적으로 파야 하면 **Paper Ingest Mode** — `/ingest` 에 DOI/arXiv/PDF 를 주면 12단 분석 (허브 + 지식 원자) 으로 해부 (v1.10.0+, `Paper Ingest Guide` 참고)
- 한 달 후 `/refresh-context` 로 Core Context 재스냅샷 (philosophy drift 반영)
- 100+ 페이지 도달하면 qmd 의 의미 검색 (`mcp__qmd__query` vec/hyde) 진가가 드러남

---

## 7. 참고

- 원본 Karpathy LLM Wiki Gist: `https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f`
- 템플릿 레포: `https://github.com/johnfkoo951/cmds-llm-wiki`
- 자매 레포 (모선 패턴): `https://github.com/johnfkoo951/cmds-system-files`
- 라이브 쇼케이스: `https://llm-wiki.cmdspace.work`
