---
type: wiki-page
aliases:
  - LLM Wiki Tools
  - Obsidian LLM Wiki Setup
description: Practical guide to Obsidian plugins, extensions, and CLI tools recommended for running an LLM Wiki — Web Clipper, Dataview, Marp, qmd search, image handling, and graph view.
author:
  - Claude
date created: 2026-04-12T00:00
date modified: 2026-04-14T14:00
tags:
  - guide
  - obsidian
  - tooling
  - llm-wiki
source:
  - "[[2026-04-02-Karpathy-LLM-Knowledge-Bases-X-Thread]]"
  - "[[2026-04-12-Karpathy-LLM-Wiki]]"
related:
  - "[[LLM Wiki Pattern]]"
  - "[[3-Layer Architecture]]"
  - "[[Ingest-Query-Lint Cycle]]"
  - "[[qmd]]"
confidence: high
layer: guides
status: active
---

# Obsidian Tooling for LLM Wiki

> [!tip] Key Insight
> LLM Wiki는 도구 없이도 작동하지만, 적절한 Obsidian 도구를 활용하면 source 수집, 탐색, 시각화가 훨씬 효율적이다.

---

## Overview

[[LLM Wiki Pattern]]은 기본적으로 markdown 파일과 LLM만으로 작동한다. 하지만 [[Andrej Karpathy]]가 소개한 실용 도구들을 활용하면 워크플로가 크게 개선된다.

---

## Source 수집

### Obsidian Web Clipper

- **용도**: 웹 기사를 markdown으로 변환하여 Raw Sources에 추가
- **설치**: Obsidian Community Plugins → "Web Clipper" 또는 브라우저 확장
- **워크플로**: 브라우저에서 기사 발견 → 클리핑 → `00. Inbox/`에 저장 → LLM에게 ingest 요청

### 이미지 로컬 다운로드

클리핑한 기사의 이미지를 로컬에 보관하면 URL 깨짐을 방지할 수 있다.

**설정 방법**:
1. Obsidian Settings → Files and links → "Attachment folder path" → 고정 디렉토리 지정 (예: `80. References/Attachments/`)
2. Settings → Hotkeys → "Download attachments for current file" → 단축키 지정 (예: `Ctrl+Shift+D`)
3. 기사 클리핑 후 단축키로 이미지 일괄 다운로드

> [!note] Update
> LLM은 markdown 내 inline 이미지를 한 번에 읽지 못한다. 텍스트를 먼저 읽고, 참조된 이미지를 별도로 확인하는 2단계 접근이 필요하다.

---

## 탐색 및 시각화

### Graph View

- **용도**: wiki의 형태를 시각적으로 파악 — 허브, 고립 노드, 클러스터
- **활용**: Lint 작업 시 orphan 페이지 식별에 유용
- Obsidian 기본 기능 (플러그인 불필요)

### Dataview

- **용도**: frontmatter를 기반으로 동적 테이블/리스트 생성
- **활용 예**: 모든 wiki 페이지를 confidence별로 정렬, 최근 ingest 목록, tag별 그룹핑
- **전제**: LLM이 YAML frontmatter를 체계적으로 작성해야 함 (이 볼트에서는 필수 7개 프로퍼티로 보장)

---

## 검색

### index.md (기본)

- ~100 sources, ~수백 pages까지는 `index.md` 기반 탐색으로 충분
- LLM이 query 시 index를 먼저 읽고 관련 페이지로 drill down
- Embedding-based RAG 인프라가 불필요

### qmd (확장)

→ 상세: [[qmd]] (별도 엔티티 페이지)

- **용도**: markdown 파일 전용 로컬 검색 엔진
- **특징**: Hybrid BM25/vector search + LLM re-ranking, 모두 온디바이스. **Ollama 불사용** — node-llama-cpp + GGUF 직접 임베드
- **인터페이스**: CLI (LLM이 shell out 가능) + MCP server (LLM native tool)
- **시점**: wiki가 ~100 articles / ~400K words (Karpathy 본인 기준)를 넘어 index만으로 부족해질 때 도입
- **이 볼트에서**: 2026-04-14부터 3 collections(wiki/raw_sources/queries) 인덱싱, Qwen3-Embedding-0.6B(CJK) 사용, PostToolUse hook 자동 재인덱싱
- **실사용자**: [[Andrej Karpathy|Karpathy]], Beomsu (@BeromArtDev, 2026-04-03 X에서 공개 확인)

---

## 출력 형식

### Marp

- **용도**: markdown 기반 슬라이드 생성
- **활용**: wiki 콘텐츠에서 직접 프레젠테이션 생성
- Obsidian Marp 플러그인 사용 가능

---

## Related

- [[LLM Wiki Pattern]] — 이 도구들이 지원하는 패턴
- [[3-Layer Architecture]] — 도구가 각 층과 어떻게 연결되는지
- [[Ingest-Query-Lint Cycle]] — 도구가 각 operation을 어떻게 개선하는지

---

## Sources

- [[2026-04-02-Karpathy-LLM-Knowledge-Bases-X-Thread]]
- [[2026-04-12-Karpathy-LLM-Wiki]]
