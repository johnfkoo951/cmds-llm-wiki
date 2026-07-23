# cmds-llm-wiki

> **LLM Wiki 볼트 템플릿** — Karpathy LLM Wiki pattern + 미래의 나에게 보내는 편지 + Claude Code · Codex 듀얼 harness.
>
> Obsidian 볼트이자 Claude Code / Codex 프로젝트. 외부 소스 (기사·논문·전사) 를 LLM 이 컴파일하여 복리로 성장하는 persistent wiki 로 축적합니다.

**🌐 Live Showcase**: **[llm-wiki.cmdspace.work](https://llm-wiki.cmdspace.work)** — 10 섹션 상세 페이지 (아키텍처 · 11 commands · 미래의 나에게 보내는 편지 · Quick Start)

**제작**: Yohan Koo ([@YohanKoo](https://x.com/YohanKoo)) · CMDSPACE 에서 운영 중인 satellite 볼트를 템플릿화

---

## 무엇인가

- **Karpathy LLM Wiki pattern** 의 실행 가능한 시작 킷
  - Raw Sources (불변) → Wiki (LLM 관리) → Schema (규칙) 3-layer
  - Ingest · Query · Lint 3 operations
  - `index.md` + `log.md` 두 개 핵심 파일
- **미래의 나에게 보내는 편지** — `/ingest` 시 "왜 수집?" 목적 질문을 강제하여 파편 축적 방지
- **Claude Code + Codex 듀얼 harness**
  - 11 slash commands (`/ingest`, `/query`, `/lint`, `/inbox`, `/status`, `/reindex`, `/refresh-context`, `/onboard`, `/capture-tabs`, `/verify`, `/audit`)
  - 2 PostToolUse hooks (raw source verbatim 검증 + qmd auto-reindex)
  - **Codex 미러**: `.codex/commands/` (10) + `.agents/skills/` (10) + `AGENTS.md` — 같은 operation 을 Codex·Cursor·Windsurf 등에서도 동일하게 실행
  - 18 Obsidian Web Clipper JSON 템플릿 (Article / YouTube / Substack / X / arXiv / Stibee 등)
  - 73개 Obsidian hotkey 바인딩 (`.obsidian/hotkeys.json`) — heading shortcuts, wikilink/callout 삽입, 사이드바 토글 등
- **선택적 mothership 볼트 연계** — 별도 PKM 볼트가 있다면 satellite 로 운영 가능

---

## 출처 및 참고

| 원천 | 링크 |
|---|---|
| **Andrej Karpathy — LLM Wiki Gist** | https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f |
| **Karpathy X thread** (2026-04-02) | https://x.com/karpathy/status/1... (본 레포 `10. Raw Sources/11. Articles/` 에 예시 포함) |
| **kepano (Steph Ango, Obsidian CEO)** — contamination mitigation | 에이전트 playground 와 personal vault 분리 개념 |
| **cmds-system-files** (mothership pattern 자매 레포) | https://github.com/johnfkoo951/cmds-system-files |

## 관련 레포

- **[cmds-system-files](https://github.com/johnfkoo951/cmds-system-files)** — CMDS mothership PKM 시스템 (100-900 카테고리 + Connect→Merge→Develop→Share). 본 레포가 optional mothership 으로 연결할 수 있는 사자매 시스템.

---

## 빠르게 시작하기

> **깊이있는 셋업 매뉴얼**: `90. Settings/Sharing/Setup Guide.md` — Mode A/B 구분, sed 일괄 치환 명령어, 검증용 grep, FAQ 7개 포함. 아래 5단계로 부족하다면 이 문서를 펼쳐놓고 작업.

### 1. 클론

```bash
cd ~/DEV
git clone https://github.com/johnfkoo951/cmds-llm-wiki.git my-llm-wiki
cd my-llm-wiki
```

### 2. Obsidian 볼트로 열기

Obsidian → Open folder as vault → `my-llm-wiki/` 선택.

### 3. placeholder 채우기

아래 placeholder 가 여러 파일에 흩어져 있습니다. 한 번에 바꾸세요:

| placeholder | 채울 값 (예시) |
|---|---|
| `{your-name}` | `[[홍길동]]` 같은 wikilink 친화 이름 |
| `{Your Name}` | `Jane Doe` 표시용 이름 |
| `{PATH_TO_YOUR_LLM_WIKI}` | `/Users/foo/DEV/my-llm-wiki` |
| `{PATH_TO_YOUR_MOTHERSHIP_VAULT}` | (옵션) 별도 PKM 볼트 경로 |
| `{your-mothership-vault-name}` | (옵션) mothership 폴더 이름 |

일괄 치환:
```bash
cd my-llm-wiki
LC_ALL=C find . -name "*.md" -o -name "*.sh" -o -name "*.yml" -o -name "*.json" | xargs sed -i '' \
  -e 's|{your-name}|홍길동|g' \
  -e 's|{Your Name}|Jane Doe|g' \
  -e 's|{PATH_TO_YOUR_LLM_WIKI}|/Users/foo/DEV/my-llm-wiki|g'
```

### 4. Core Context 채우기

`Core Context.md` 에서:
- §1 정체성 (이름·역할·전문 분야·연속성 선언)
- §2 재활용 축 5~9개 (당신의 지식은 어디에 쓰일 것인가)
- §3~§5 는 선택

### 5. qmd (선택, 권장) — 로컬 검색 엔진

```bash
# 설치 (brew 필요)
brew install qmd-search/qmd/qmd

# 설정 파일 복사
cp "90. Settings/qmd-config-template.yml" ~/.config/qmd/index.yml
# ~/.config/qmd/index.yml 의 {PATH_TO_YOUR_LLM_WIKI} 를 실제 경로로 수정

# 인덱싱
export QMD_EMBED_MODEL="hf:Qwen/Qwen3-Embedding-0.6B-GGUF/Qwen3-Embedding-0.6B-Q8_0.gguf"
qmd update && qmd embed
```

### 6. Obsidian Web Clipper (선택)

`90. Settings/Sharing/clipper-*.json` 18개 중 원하는 사이트 템플릿을 Web Clipper Settings → Templates → Import 에서 불러오기.

### 7. Claude Code 실행

```bash
cd my-llm-wiki
claude
```

첫 명령어 추천 순서:
1. `/status` — 현재 볼트 상태 확인
2. `/ingest <URL>` — 관심 기사 하나 ingest (목적 질문에 답해보기)
3. `/query <질문>` — 쌓인 wiki 로 첫 질의
4. `/lint` — 건강도 체크

---

## 구조

```
cmds-llm-wiki/
├── CLAUDE.md                    # Schema (Claude Code) — LLM 행동 규칙
├── AGENTS.md                    # Schema (Codex/Cursor/Windsurf) — CLAUDE.md 미러
├── Core Context.md              # 사용자 맥락 (채워서 사용)
├── index.md                     # 마스터 인덱스
├── log.md                       # 변경 이력 (append-only)
├── README.md                    # 이 파일
├── CHANGELOG.md                 # 템플릿 버전 이력
├── LLM-Wiki-Starter-Kit.md      # 간이 공유용 킷
├── .claude/
│   ├── commands/                # 11 slash commands
│   ├── hooks/                   # 2 PostToolUse hooks
│   └── settings.json
├── .codex/                      # Codex harness (Claude 미러)
│   ├── commands/                # 10 commands (onboard 제외)
│   ├── hooks/                   # 2 hooks
│   └── hooks.json
├── .agents/
│   └── skills/                  # 10 Codex reusable operation skills
├── .obsidian/
│   └── hotkeys.json             # 73개 Obsidian hotkey 바인딩 (선택 — 마음에 안 들면 삭제)
├── 00. Inbox/                   # Web Clipper 수신 (02~05 서브폴더)
├── 10. Raw Sources/             # 불변 원본 (11~15 서브폴더)
│   └── 11. Articles/            # Karpathy 예시 2개 포함
├── 20. Wiki/                    # LLM 관리 위키
│   ├── 21. Concepts/            # 예시 (LLM Wiki Pattern 등)
│   ├── 22. Entities/            # 예시 (Karpathy, Bush, Memex)
│   ├── 23. Guides/              # 예시 가이드
│   ├── 24. Maps/                # 예시 MOC
│   └── 25. Questions/           # Research Question 카드 (빈 폴더, RQ-{slug}.md)
├── 30. Queries/                 # 합성된 질의 결과 + synthesis (빈 폴더, /query 결과로 채워짐)
├── 80. References/Attachments/  # 모든 이미지 일원화
└── 90. Settings/
    ├── Templates/               # Obsidian 노트 템플릿 (7종)
    ├── Sharing/                 # 18 Web Clipper JSON + Setup Guide.md + CLAUDE-Template.md
    └── qmd-config-template.yml  # 로컬 검색 엔진 설정
```

---

## 핵심 규약

- **YAML 2 SPACES / Body TAB** (혼용 금지)
- **Wikilink in YAML quoted**: `"[[link]]"`
- **Mermaid 라벨 큰따옴표**: `A["label"]`
- **필수 7 프로퍼티**: `type`, `aliases`, `description` (English, LLM hint), `author`, `date created`, `date modified`, `tags`
- **ISO 8601 날짜**: `YYYY-MM-DD`
- **새 YAML 키는 camelCase**: `collectionPurpose`, `mainVaultRelated`, `mainVaultCmds`, `reusableFor`

자세한 내용은 `CLAUDE.md` 참조.

---

## 예시 컨텐츠 안내

`10. Raw Sources/` 와 `20. Wiki/` 에 Karpathy 의 LLM Wiki 원문을 ingest 한 결과 일부가 예시로 들어있습니다. 이는 **패턴이 어떻게 동작하는지 보여주기 위한** 샘플입니다:

- `10. Raw Sources/11. Articles/2026-04-12-Karpathy-LLM-Wiki.md`
- `10. Raw Sources/11. Articles/2026-04-02-Karpathy-LLM-Knowledge-Bases-X-Thread.md`
- `20. Wiki/` — 개념·엔티티·MOC 약 16개 (정확한 수는 `/lint` 가 재집계)

예시 wiki 페이지 일부에는 **orphan wikilinks** (존재하지 않는 페이지로의 링크) 가 포함되어 있습니다. 이는 의도된 것으로, `/ingest` 를 반복하면서 자연스럽게 채워지는 wiki 의 성장 방식을 보여줍니다.

완전히 빈 상태에서 시작하려면 `10. Raw Sources/11. Articles/*.md` 와 `20. Wiki/**/*.md` 를 삭제하세요.

---

## 라이선스 & 기여

- 본 레포는 **템플릿** 입니다. 자유롭게 fork·복제하여 본인 볼트로 사용하세요.
- 개선 PR 환영. 단 `Core Context.md`, `index.md`, `log.md` 같은 템플릿 파일은 placeholder 유지.

제작: [@YohanKoo](https://x.com/YohanKoo) · [CMDSPACE](https://litt.ly/cmds)
- Karpathy 의 LLM Wiki pattern
- kepano 의 contamination mitigation 개념
- cmds-system-files (자매 mothership pattern)
