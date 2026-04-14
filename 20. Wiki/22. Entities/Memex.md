---
type: wiki-page
aliases:
  - Memory Extender
  - 메멕스
description: Memex — Vannevar Bush's 1945 conceptual device for storing and linking personal knowledge with associative trails. Spiritual ancestor of hypertext, the web, and the LLM Wiki pattern.
author:
  - Claude
date created: 2026-04-12T00:00
date modified: 2026-04-12T00:00
tags:
  - concept
  - knowledge-management
  - historical
source:
  - "[[2026-04-12-Karpathy-LLM-Wiki]]"
related:
  - "[[Vannevar Bush]]"
  - "[[LLM Wiki Pattern]]"
  - "[[Persistent Knowledge Base]]"
confidence: high
layer: entities
status: active
---

# Memex

> [!tip] Key Insight
> 1945년 구상된 "개인 기억 확장 장치". 문서 간 associative trail(연상적 연결)을 핵심으로 했으며, 하이퍼텍스트와 LLM Wiki의 사상적 선조.

---

## Overview

**Memex** (Memory Extender)는 [[Vannevar Bush]]가 1945년 에세이 "As We May Think" (The Atlantic)에서 제안한 개념적 장치이다. 마이크로필름에 저장된 책, 기록, 통신 자료를 담고, 사용자가 **associative trail** — 문서 간 연상적 연결 — 을 만들어 탐색하는 시스템이었다.

---

## Details

### 핵심 특성

- **개인적(Private)**: 개인이 소유하고 큐레이션하는 지식 저장소
- **연상적 연결(Associative Trails)**: 인덱스가 아닌, 문서 간 의미적 연결로 탐색
- **능동적 큐레이션**: 사용자가 trail을 만들고 유지
- **축적적**: 사용할수록 trail이 풍부해짐

### Memex와 LLM Wiki의 비교

| 차원 | Memex (1945) | LLM Wiki (2026) |
|------|-------------|-----------------|
| 저장 매체 | 마이크로필름 | Markdown 파일 |
| 연결 방식 | Associative trail | Wikilinks + cross-reference |
| 큐레이션 | 인간 수동 | LLM 자동 |
| 유지보수 | 인간 (미해결) | LLM (해결) |
| 탐색 | 기계적 | Obsidian Graph View |
| 실현 여부 | 미구현 개념 | 구현 가능 |

### 미해결 과제

Bush의 Memex에서 가장 큰 약점은 **유지보수**였다. Trail을 만드는 것은 가능했지만, 새 정보가 들어올 때 기존 trail을 업데이트하고, 모순을 감지하고, 일관성을 유지하는 것은 인간에게 너무 큰 부담이었다. [[LLM Wiki Pattern]]이 LLM을 통해 이 문제를 해결한다.

---

## Related

- [[Vannevar Bush]] — Memex의 제안자
- [[LLM Wiki Pattern]] — Memex 비전의 현대적 구현
- [[Persistent Knowledge Base]] — Memex의 "축적" 아이디어의 발전

---

## Sources

- [[2026-04-12-Karpathy-LLM-Wiki]]
