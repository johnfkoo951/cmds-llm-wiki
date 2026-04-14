---
type: wiki-page
aliases:
  - RAG vs Wiki
  - RAG vs LLM Wiki
  - Retrieval vs Compilation
description: Comparison between RAG (retrieval-augmented generation) and the compiled wiki approach. RAG re-derives answers per query; the wiki pre-compiles knowledge into persistent, cross-referenced pages.
author:
  - Claude
date created: 2026-04-12T00:00
date modified: 2026-04-12T00:00
tags:
  - rag
  - llm-wiki
  - knowledge-management
  - comparison
source:
  - "[[2026-04-12-Karpathy-LLM-Wiki]]"
related:
  - "[[LLM Wiki Pattern]]"
  - "[[Persistent Knowledge Base]]"
confidence: high
layer: concepts
status: active
---

# RAG vs Compiled Wiki

> [!tip] Key Insight
> RAG는 매 질문마다 지식을 재발견한다. Compiled Wiki는 지식을 한 번 컴파일하고 계속 업데이트한다. 축적(accumulation)의 유무가 핵심 차이.

---

## Overview

[[LLM Wiki Pattern]]의 출발점은 기존 RAG(Retrieval-Augmented Generation) 방식의 한계 인식이다. 두 접근은 LLM과 문서의 관계를 근본적으로 다르게 설정한다.

---

## Details

### RAG 방식

1. 문서 컬렉션을 chunk로 분할하여 인덱싱
2. 질문이 들어오면 관련 chunk를 검색
3. LLM이 검색된 chunk를 바탕으로 답변 생성
4. 답변 후 — 아무것도 남지 않음

**한계**: LLM이 매번 처음부터 지식을 재발견(rediscover)한다. 5개 문서를 종합해야 하는 미묘한 질문에는 매번 조각을 찾아 맞춰야 한다. **축적(accumulation)이 없다.**

대표 시스템: NotebookLM, ChatGPT file uploads, 대부분의 RAG 시스템.

### Compiled Wiki 방식

1. 새 source가 들어오면 LLM이 읽고 wiki에 통합
2. 기존 entity/concept 페이지를 업데이트, 모순 플래그, cross-reference 추가
3. 질문이 오면 이미 컴파일된 wiki에서 답변
4. 좋은 답변은 다시 wiki에 저장 — **지식이 축적**

**장점**: cross-reference가 이미 완성되어 있고, 모순이 이미 감지되어 있으며, 종합이 모든 source를 반영한다. Source를 추가할수록, 질문을 할수록 wiki는 더 풍부해진다.

### 비교 표

| 차원 | RAG | Compiled Wiki |
|------|-----|---------------|
| 지식 처리 시점 | Query time (매번) | Ingest time (한 번) |
| 축적 | 없음 | 있음 (compounding) |
| Cross-reference | 매번 재구성 | 사전 구축 |
| 모순 감지 | 우연적 | 체계적 (lint) |
| 인프라 | Embedding DB, retriever | Markdown 파일 + Git |
| 탐색 가능성 | LLM 통해서만 | 직접 탐색 가능 (Obsidian) |
| 확장성 | 대규모에 강점 | 중규모까지 index.md로 충분 |

---

## Trade-offs

> [!warning] Contradiction
> RAG가 항상 열등한 것은 아니다. 대규모(수천 source)에서는 index.md 기반 네비게이션이 한계에 도달하며, embedding-based search가 필요해진다. 두 접근은 상호 보완적일 수 있다 — wiki 위에 RAG를 얹는 하이브리드 구조.

---

## Related

- [[LLM Wiki Pattern]] — compiled wiki의 전체 패턴
- [[Persistent Knowledge Base]] — 왜 축적이 중요한가

---

## Sources

- [[2026-04-12-Karpathy-LLM-Wiki]]
