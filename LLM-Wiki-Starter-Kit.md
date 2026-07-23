# LLM Wiki Starter Kit

> Andrej Karpathy의 LLM Wiki 패턴을 Obsidian + Claude Code로 구현하는 스타터 킷.

---

## What is LLM Wiki?

RAG는 질문할 때마다 문서를 검색하고 합성합니다. **LLM Wiki**는 다릅니다:

- LLM이 자료를 **한 번 읽고** structured wiki 페이지로 컴파일
- 새 자료가 들어올 때마다 기존 페이지를 **incremental update**
- Cross-reference, 모순 감지, 인덱싱을 **LLM이 자동** 유지
- 결과물: 점점 더 풍부해지는 **compounding knowledge base**

> Obsidian은 IDE, LLM은 프로그래머, Wiki는 코드베이스. — Andrej Karpathy

원본: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f

---

## Quick Start (5분)

### Step 1: 새 Obsidian Vault 생성

Obsidian에서 새 vault를 만듭니다. 이름은 자유 (예: `My-LLM-Wiki`).

### Step 2: CLAUDE.md 복사

아래 파일의 내용을 **vault 루트**에 `CLAUDE.md`로 저장합니다:

> **CLAUDE.md 템플릿**: `90. Settings/Sharing/CLAUDE-Template.md`

이 파일이 vault 이름과 같은 수준에 있어야 합니다:
```
My-LLM-Wiki/
├── CLAUDE.md    ← 여기
├── ...
```

### Step 3: Claude Code로 초기화

터미널에서 vault 폴더로 이동 후 Claude Code를 실행합니다:

```bash
cd /path/to/My-LLM-Wiki
claude
```

그리고 이렇게 말합니다:

> "이 볼트를 LLM Wiki로 초기화해줘. CLAUDE.md에 정의된 폴더 구조, 템플릿, index.md, log.md를 생성해줘."

Claude Code가 CLAUDE.md를 읽고 모든 구조를 자동 생성합니다.

### Step 4: 첫 번째 자료 Ingest

자료(URL, 텍스트, PDF 등)를 Claude Code에게 전달합니다:

> "이 자료를 wiki로 ingest 해줘: [URL 또는 텍스트]"

LLM이 자동으로:
1. Raw Source 저장 (원본 보존)
2. Wiki 페이지 10~15개 생성/업데이트
3. index.md, log.md 갱신

### Step 5: 사용 & 성장

| 작업 | 명령 | 효과 |
|------|------|------|
| **Ingest** | "이 자료 ingest 해줘" | wiki에 새 지식 추가 |
| **Query** | "~에 대해 설명해줘" | wiki에서 합성 답변 |
| **Lint** | "wiki health check 해줘" | orphan, 모순, 누락 검사 |

핵심 3개 외에 `/inbox` · `/status` · `/reindex` · `/refresh-context` · `/onboard` · `/capture-tabs` · `/verify` · `/audit` 까지 총 11개 명령이 있다 (전체 목록·설명은 `README.md` / `CLAUDE.md`). 자료를 추가할수록 wiki가 성장합니다.

---

## 구조 미리보기

초기화 후 vault는 이런 구조가 됩니다:

```
My-LLM-Wiki/
├── CLAUDE.md               # Schema (LLM 행동 규칙)
├── index.md                # 마스터 인덱스
├── log.md                  # 변경 이력
├── 00. Inbox/              # 새 자료 임시 저장
├── 10. Raw Sources/        # 불변 원본
│   ├── 11. Articles/
│   ├── 12. Papers/
│   ├── 13. Books/
│   ├── 14. Transcripts/
│   └── 15. Clippings/
├── 20. Wiki/               # LLM이 관리하는 위키
│   ├── 21. Concepts/       # 개념
│   ├── 22. Entities/       # 인물, 조직, 제품
│   ├── 23. Guides/         # 가이드
│   ├── 24. Maps/           # MOC (주제별 인덱스)
│   └── 25. Questions/      # Research Question 카드 (RQ-{slug}.md)
├── 30. Queries/            # 질의 결과 저장
└── 80. References/         # 첨부 파일
    └── Attachments/
```

---

## 핵심 원리

### 3-Layer Architecture

| Layer | 폴더 | 소유자 | 규칙 |
|-------|------|--------|------|
| **Raw Sources** | `10. Raw Sources/` | 인간이 수집 | 불변 — 절대 수정 안 함 |
| **Wiki** | `20. Wiki/` | LLM이 관리 | 인간은 읽기, LLM이 쓰기 |
| **Schema** | `CLAUDE.md` | 인간+LLM 공동 | LLM의 행동 규칙 정의 |

### RAG vs LLM Wiki

| | RAG | LLM Wiki |
|---|-----|----------|
| **언제** | 질문할 때마다 검색 | 자료 추가 시 한 번 컴파일 |
| **축적** | 없음 | 있음 (compounding) |
| **Cross-ref** | 매번 재구성 | 사전 구축 |
| **탐색** | LLM 통해서만 | Obsidian에서 직접 |
| **인프라** | Embedding DB 필요 | Markdown 파일만 |

---

## 추천 도구

| 도구 | 용도 | 필수? |
|------|------|-------|
| **Obsidian** | wiki 탐색, Graph View | 필수 |
| **Claude Code** | wiki 관리 LLM | 필수 |
| **Obsidian Web Clipper** | 웹 기사 → markdown 변환 | 권장 |
| **Dataview** (plugin) | frontmatter 기반 동적 테이블 | 선택 |
| **Git** | wiki 버전 관리 | 권장 |

---

## FAQ

**Q: 어떤 LLM 에이전트를 써야 하나요?**
Claude Code 권장 (CLAUDE.md 네이티브 지원). **Codex 도 1급 지원** — `.codex/commands/` (10) + `.agents/skills/` (10) + `AGENTS.md` 미러가 함께 포함되어 같은 operation 을 그대로 실행. Cursor, Windsurf 등은 `AGENTS.md` 를 schema 로 참조. 현재 command set 은 `CLAUDE.md` / `README.md` 참조.

**Q: 어떤 주제에 쓸 수 있나요?**
아무 주제나 — AI 연구, 독서 노트, 경쟁 분석, 수업 정리, 취미 deep-dive 등.

**Q: Git은 필수인가요?**
아닙니다. 선택사항이지만 권장. `git init` 후 ingest마다 commit하면 wiki 진화 과정 추적 가능.

**Q: 기존 Obsidian vault에 추가할 수 있나요?**
가능하지만 별도 vault 권장. LLM 관리 영역과 직접 관리 영역이 섞이면 혼란.

---

## 파일 목록

이 스타터 킷에 포함된 공유용 파일:

| 파일 | 설명 |
|------|------|
| `LLM-Wiki-Starter-Kit.md` | 이 가이드 (지금 읽고 있는 파일) |
| `90. Settings/Sharing/CLAUDE-Template.md` | CLAUDE.md 템플릿 (vault 루트에 복사) |

---

*Based on Andrej Karpathy's LLM Wiki pattern (April 2026)*
