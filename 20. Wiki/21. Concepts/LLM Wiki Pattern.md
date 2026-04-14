---
type: wiki-page
aliases:
  - LLM Wiki
  - Karpathy Wiki Pattern
  - LLM-Maintained Wiki
description: The LLM Wiki pattern proposed by Andrej Karpathy — LLMs incrementally build and maintain a persistent, structured markdown wiki from raw sources instead of using RAG for every query.
author:
  - Claude
date created: 2026-04-12T00:00
date modified: 2026-04-14T16:00
tags:
  - llm-wiki
  - knowledge-management
  - design-pattern
source:
  - "[[2026-04-02-Karpathy-LLM-Knowledge-Bases-X-Thread]]"
  - "[[2026-04-12-Karpathy-LLM-Wiki]]"
  - "[[2026-04-02-Harnessing-Claudes-Intelligence-3-Patterns]]"
  - "[[2026-04-13-Changhyun-Ahn-Soverign-PKM]]"
related:
  - "[[RAG vs Compiled Wiki]]"
  - "[[Persistent Knowledge Base]]"
  - "[[3-Layer Architecture]]"
  - "[[Ingest-Query-Lint Cycle]]"
  - "[[Andrej Karpathy]]"
  - "[[Memex]]"
  - "[[Contamination Mitigation]]"
  - "[[Synthetic Data Generation for Wiki]]"
  - "[[qmd]]"
  - "[[Progressive Disclosure Pattern]]"
  - "[[Context Engineering]]"
  - "[[Agent Harness Design]]"
  - "[[Sovereign PKM]]"
  - "[[Harness Literacy]]"
confidence: high
layer: concepts
status: active
---

# LLM Wiki Pattern

> [!tip] Key Insight
> LLM이 raw source를 읽고 persistent wiki를 직접 작성·관리한다. 매 질문마다 재검색하는 RAG가 아니라, 한 번 컴파일된 지식이 계속 성장하는 **compounding artifact**.

---

## Overview

**LLM Wiki Pattern**은 [[Andrej Karpathy]]가 2026년 4월 제안한 개인 지식 베이스 구축 패턴이다. 핵심 아이디어는 간단하다:

> LLM에게 raw source를 주면, LLM이 직접 structured markdown wiki를 작성하고 유지한다.

기존 [[RAG vs Compiled Wiki|RAG 방식]]에서는 질문할 때마다 문서를 검색하고 합성한다. LLM Wiki에서는 source를 **한 번 컴파일**하여 wiki 페이지로 만들고, 새 source가 들어올 때마다 기존 페이지를 **incremental update**한다. 결과물은 cross-reference가 이미 연결되어 있고, 모순이 이미 플래그되어 있으며, 모든 source의 종합이 이미 반영된 [[Persistent Knowledge Base|persistent knowledge base]]이다.

---

## Details

### 역할 분담

| 역할 | 담당 |
|------|------|
| Source 큐레이션 | 인간 |
| 질문, 방향 설정, 의미 해석 | 인간 |
| 요약, cross-referencing, 파일링, 북키핑 | LLM |
| Wiki 작성 및 유지보수 | LLM |

Karpathy의 비유: **Obsidian은 IDE, LLM은 프로그래머, Wiki는 코드베이스.**

### 적용 분야

- **Personal**: 목표, 건강, 자기계발 추적
- **Research**: 논문·기사를 읽으며 evolving thesis를 가진 comprehensive wiki 구축
- **Reading a Book**: 챕터별 캐릭터·테마·플롯 페이지 생성 (팬 위키처럼)
- **Business/Team**: Slack, 회의록, 프로젝트 문서를 LLM이 wiki로 유지
- **기타**: 경쟁 분석, 실사, 여행 계획, 코스 노트, 취미 deep-dive

### 핵심 특성

1. **Persistent**: 대화가 끝나도 wiki는 남는다
2. **Compounding**: source가 추가될수록 wiki가 더 풍부해진다
3. **Pre-synthesized**: cross-reference와 모순 플래그가 이미 완료되어 있다
4. **Human-readable**: Obsidian 등에서 직접 탐색 가능
5. **Version-controlled**: Git으로 모든 변경 이력을 추적

### 실증된 스케일

Karpathy 본인의 deployment (2026-04-02 X 공개): **~100 articles, ~400K words**. 이 규모에서:

- 전통적 RAG 인프라(embedding DB, retriever) 불필요
- `index.md` 기반 네비게이션만으로 충분
- LLM이 관련 페이지를 수동 drill-down으로 탐색 가능

이 수치는 "embedding search가 언제 필요해지는가"의 경계선을 암시한다 (→ [[Obsidian Tooling for LLM Wiki|qmd 도입 시점 논의]]).

### 확장 방향

- **[[Contamination Mitigation]]** ([[kepano (Steph Ango)|kepano]] 제안): agent playground vault와 personal vault 분리
- **[[Synthetic Data Generation for Wiki]]** (Karpathy 제안): wiki 콘텐츠로 파인튜닝 → 지식을 가중치에 내장
- **[[Sovereign PKM]]** (Changhyun Ahn 제안): 원본은 Markdown, 레거시 포맷(HWPX/DOCX/PPTX)은 출력 어댑터로 강등
- **[[Harness Literacy]]** (Changhyun Ahn 제안): 사용자가 맥락을 외부화·기계가독화·실행 연결하는 역량

### Agent Harness로서의 Wiki — Lance Martin 3 Patterns 연결

[[Lance Martin]]의 [[Agent Harness Design|agent harness 설계 원칙]]을 LLM Wiki에 대입하면 구조적 동형성이 드러난다:

| Lance Martin Pattern | LLM Wiki 대응 |
|----------------------|---------------|
| Use what Claude knows | Markdown + bash/text editor — LLM이 잘 아는 파일 기반 저장 |
| Ask what you can stop doing | [[Ingest-Query-Lint Cycle\|Lint]] — wiki의 dead weight 제거 |
| Set boundaries carefully | `CLAUDE.md` schema — YAML 규칙, wikilink 규칙, 층 분리 |

[[Progressive Disclosure Pattern]]은 특히 직접 대응: Skill YAML frontmatter ↔ `index.md` 한 줄 요약, Skill body ↔ 개별 Wiki 페이지. Karpathy의 "~100 sources까지 index.md만으로 충분" 관찰은 progressive disclosure가 human-LLM 인터페이스에도 효과적임을 실증한다.

[[Context Engineering|5-레버 context 관리]] 중 **Externalize (memory folder)** 가 LLM Wiki의 본질 — Claude가 스스로 선택한 knowledge를 파일로 외부화하여 세션 경계를 넘어 축적.

### 왜 작동하는가

위키 유지의 어려운 부분은 읽기나 사고가 아니라 **북키핑**이다 — cross-reference 업데이트, 요약 최신화, 모순 감지, 일관성 유지. 인간은 이 부담에 지쳐 위키를 포기하지만, LLM은 지루함을 모르고 한 번에 15개 파일을 업데이트할 수 있다. 유지보수 비용이 거의 0이므로 wiki가 살아남는다.

---

## Historical Context

이 패턴은 정신적으로 [[Vannevar Bush]]의 [[Memex]] (1945)와 연결된다. Bush는 문서 간 associative trail을 가진 개인 지식 저장소를 구상했지만, 유지보수 문제를 해결하지 못했다. 80년 후, LLM이 그 역할을 맡는다.

### 한국 PKM 커뮤니티의 reframing

Changhyun Ahn의 [[2026-04-13-Changhyun-Ahn-Soverign-PKM|LinkedIn Pulse 에세이]] (2026-04-13):

> "Karpathy의 글은 혁신의 출발점이 아니라, 이미 앞서 가던 흐름이 이제 AI 본류의 입에서 다시 확인되었다는 signal에 가깝다."

"Markdown Is All You Need" 슬로건 아래 Yohan Koo·더배러 등 한국 PKM 실천자들이 동일한 방향에 먼저 도달해 있었다는 주장. 본 vault({your-llm-wiki})가 그 실증 사례이며, [[Sovereign PKM]] 관점에서 LLM Wiki는 **"원본 포맷 주권 + LLM 협업 자동화"** 의 교집합이다.

---

## Related

- [[RAG vs Compiled Wiki]] — 두 접근의 차이와 trade-off
- [[Persistent Knowledge Base]] — compounding artifact로서의 wiki
- [[3-Layer Architecture]] — Raw Sources / Wiki / Schema 구조
- [[Ingest-Query-Lint Cycle]] — wiki 운영의 세 가지 작업
- [[Obsidian Tooling for LLM Wiki]] — 실용 도구 가이드
- [[Contamination Mitigation]] — 에이전트 볼트 분리 (kepano)
- [[Synthetic Data Generation for Wiki]] — 파인튜닝 확장 경로
- [[qmd]] — 스케일업 시 권장 검색 도구
- [[Progressive Disclosure Pattern]] — index.md ↔ Skills frontmatter 구조적 동형
- [[Context Engineering]] — Wiki = "externalize" 레버의 구현
- [[Agent Harness Design]] — Wiki 스키마도 곧 harness
- [[Sovereign PKM]] — Korean PKM 관점의 원본 포맷 주권 확장
- [[Harness Literacy]] — LLM Wiki가 훈련 도구이자 산출물인 사용자 역량

---

## Sources

- [[2026-04-02-Karpathy-LLM-Knowledge-Bases-X-Thread]] — 원조 X 스레드 (2026-04-02)
- [[2026-04-12-Karpathy-LLM-Wiki]] — 확장된 Gist (2026-04-06)
- [[2026-04-02-Harnessing-Claudes-Intelligence-3-Patterns]] — Lance Martin의 agent harness 3 patterns
- [[2026-04-13-Changhyun-Ahn-Soverign-PKM]] — 안창현의 Sovereign PKM 에세이

---

## Open Questions

> [!question] Open Question
> 이 패턴이 수백 개 source, 수천 개 wiki 페이지 규모에서도 index.md 기반 네비게이션만으로 충분한가? 어느 시점에 embedding-based search가 필요해지는가?
