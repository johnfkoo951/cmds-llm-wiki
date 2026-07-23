---
type: wiki-page
aliases:
  - Three Layer Architecture
  - Raw Sources Wiki Schema
  - LLM Wiki Architecture
description: The 3-layer architecture of the LLM Wiki — Raw Sources (immutable truth), Wiki (LLM-maintained knowledge), and Schema (LLM behavior rules via CLAUDE.md/AGENTS.md).
author:
  - Claude
date created: 2026-04-12T00:00
date modified: 2026-04-14T14:00
tags:
  - llm-wiki
  - architecture
  - knowledge-management
source:
  - "[[2026-04-12-Karpathy-LLM-Wiki]]"
related:
  - "[[LLM Wiki Pattern]]"
  - "[[Ingest-Query-Lint Cycle]]"
  - "[[Persistent Knowledge Base]]"
  - "[[Contamination Mitigation]]"
confidence: high
layer: concepts
status: active
---

# 3-Layer Architecture

> [!tip] Key Insight
> Raw Sources(불변 원본) → Wiki(LLM 관리 지식) → Schema(행동 규칙). 세 층의 분리가 LLM Wiki의 구조적 핵심이다.

---

## Overview

[[LLM Wiki Pattern]]은 세 개의 명확히 분리된 층(layer)으로 구성된다. 각 층은 고유한 소유자와 규칙을 가진다.

---

## Details

### Layer 1: Raw Sources (원본층)

```
10. Raw Sources/
├── 11. Articles/     # 웹 기사, 블로그 포스트
├── 12. Papers/       # 학술 논문, 기술 보고서
├── 13. Books/        # 도서 노트, 챕터 요약
├── 14. Transcripts/  # 강연, 팟캐스트, 영상 전사
└── 15. Clippings/    # 웹 클리핑, 스크랩
```

- **소유자**: 인간이 큐레이션
- **규칙**: **불변(immutable)** — LLM은 읽기만 하고 절대 수정하지 않음
- **역할**: Source of truth. 모든 wiki 페이지의 근거
- **Frontmatter**: `type: raw-source`, `date ingested`, `category`

### Layer 2: The Wiki (지식층)

```
20. Wiki/
├── 21. Concepts/     # 추상 개념 (Attention, Transformer, RLHF, ...)
├── 22. Entities/     # 사람, 조직, 제품 (OpenAI, Karpathy, GPT-4, ...)
├── 23. Guides/       # How-to, 튜토리얼, 실전 가이드
├── 24. Maps/         # MOC (Map of Content), 주제별 인덱스
└── 25. Questions/    # Research Question — 1급 연구 질문 카드
```

- **소유자**: LLM이 전적으로 관리
- **규칙**: 인간은 읽고, LLM이 작성. 모든 주장에 출처 명시
- **역할**: Pre-synthesized, cross-referenced 지식 페이지
- **Frontmatter**: `type: wiki-page`, `source`, `related`, `confidence`

### Layer 3: The Schema (규칙층)

- **파일**: `CLAUDE.md` (Claude Code), `AGENTS.md` (Codex) 등
- **소유자**: 인간과 LLM이 공동 진화(co-evolve)
- **규칙**: LLM의 행동을 제어하는 핵심 설정 문서
- **역할**: Wiki의 구조, 컨벤션, 워크플로를 정의. 이것이 LLM을 "규율 있는 wiki 관리자"로 만드는 핵심

### 층 간 관계

```
Schema (CLAUDE.md)
    │ 제어
    ▼
Wiki ◀──── compile ──── Raw Sources
    │                        ▲
    └── reference ───────────┘
```

- Schema가 LLM의 행동을 **제어**
- Raw Sources를 LLM이 Wiki로 **컴파일**
- Wiki가 Raw Sources를 **역참조** (`source` 프로퍼티)
- Raw Sources는 절대 수정되지 않음

### 이 볼트에서의 구현

| Layer | 경로 | 구현 |
|-------|------|------|
| Raw Sources | `10. Raw Sources/` | 5개 하위 폴더 (11.Articles, 12.Papers, 13.Books, 14.Transcripts, 15.Clippings) |
| Wiki | `20. Wiki/` | 4개 하위 폴더 (21.Concepts, 22.Entities, 23.Guides, 24.Maps) |
| Schema | `CLAUDE.md` | Frontmatter 규격, 네이밍 컨벤션, Operations 정의 |

> [!note] 개념적 3층 vs 물리적 폴더
> 이 볼트에는 `30. Queries/` 물리 폴더도 있다 (Query 산출물 위치). 하지만 이는 *4번째 구조 레이어가 아니라* [[Ingest-Query-Lint Cycle]] 의 *Query 단계 산출물*이다. **구조 축**은 Raw/Wiki/Schema 3층이 정본이고, `30. Queries` 는 그 위에서 작동하는 **운영 축**의 결과물.

---

## Related

- [[LLM Wiki Pattern]] — 이 아키텍처를 사용하는 전체 패턴
- [[Ingest-Query-Lint Cycle]] — 이 아키텍처 위에서 작동하는 operations
- [[Persistent Knowledge Base]] — Wiki 층이 compounding artifact인 이유
- [[Contamination Mitigation]] — 한 단계 상위 분리 원리 (볼트 단위)

### 계층 분리의 스케일

| 단위 | 개념 |
|------|------|
| 볼트 간 | [[Contamination Mitigation]] — personal vs agent playground |
| 볼트 내 (이 문서) | 3-Layer — Raw / Wiki / Schema |
| 페이지 내 | frontmatter vs body, `source:` vs content |

세 수준 모두 "누가 쓸 수 있는가"의 경계 설정이다.

---

## Sources

- [[2026-04-12-Karpathy-LLM-Wiki]]
