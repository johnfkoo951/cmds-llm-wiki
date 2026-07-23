---
type: moc
aliases:
  - Wiki Index
  - Master Index
description: "Master index of the LLM Wiki. Central navigation hub listing all Wiki pages organized by category (Concepts, Entities, Guides, Maps, Questions). Updated automatically on every ingest operation."
author:
  - "[[{your-name}]]"
date created: {YYYY-MM-DD}
date modified: {YYYY-MM-DD}
tags:
  - index
  - moc
  - system
status: active
---

# 📖 LLM Wiki — Master Index

> **Architecture**: Karpathy LLM Wiki Pattern
> Raw Sources → **LLM Compiler** → This Wiki

이 볼트는 LLM 이 직접 작성하고 관리하는 **persistent knowledge wiki** 입니다.
매번 query 마다 재합성하지 않고, 한 번 컴파일된 지식이 계속 성장합니다.

---

## 📊 Stats

| Metric | Count |
|--------|-------|
| Raw Sources | 2 (예시) |
| Wiki Pages | 16 (예시) |
| Concepts | 9 |
| Entities | 3 |
| Guides | 2 |
| MOCs | 2 |
| Queries | 0 |

> *Stats 는 `/ingest` 실행 시 자동 갱신됩니다. 본인 컨텐츠를 채워나가면서 업데이트.*

---

## 🗂 Wiki Pages (예시)

아래는 Karpathy 의 LLM Wiki 원문을 ingest 한 결과로 만들어진 **예시 wiki 페이지** 입니다. 새 소스를 ingest 할 때마다 이 목록이 자라납니다.

### Concepts

> 추상 개념, 기술, 방법론

- [[LLM Wiki Pattern]] — LLM 이 raw source 를 컴파일하여 persistent wiki 를 관리하는 패턴
- [[RAG vs Compiled Wiki]] — RAG(매번 재검색) vs Compiled Wiki(한 번 컴파일)의 비교
- [[3-Layer Architecture]] — Raw Sources / Wiki / Schema 3층 구조
- [[Ingest-Query-Lint Cycle]] — Wiki 운영의 세 가지 핵심 작업 (Ingest, Query, Lint)

### Entities

> 사람, 조직, 제품, 모델

- [[Andrej Karpathy]] — AI 연구자, LLM Wiki 패턴 제안자
- [[Vannevar Bush]] — Memex 개념 제안자 (1945)
- [[Memex]] — 문서 간 associative trail 을 가진 개인 지식 저장소 구상

### Guides

> How-to, 튜토리얼, 실전 가이드

- [[Obsidian Tooling for LLM Wiki]] — Web Clipper, Dataview, qmd 등 실용 도구 가이드

### Maps (MOC)

> 주제별 Map of Content

- [[MOC-Knowledge Management]] — 지식 관리 개념, 패턴, 역사 종합
- [[MOC-LLM Wiki Guide]] — 이 볼트 사용 온보딩 가이드

### Questions (RQ)

> 1급 연구 질문 카드 (`RQ-{slug}.md`) — Open Question 콜아웃의 승격 대상

(첫 Research Question 카드를 만들면 여기에 기록됩니다.)

---

## 🔎 Queries (Synthesized Answers)

> 질의 결과가 wiki 에 역피드백된 합성 페이지. [[Ingest-Query-Lint Cycle|Karpathy 원문 권장]]: "good answers can be filed back into the wiki as new pages."

(첫 `/query` 를 실행하면 여기에 기록됩니다.)

---

## 📄 Paper Analyses (허브만)

> 논문 12단 분석 — `40. Paper Analyses/{citekey}/` 의 허브(S00)만 여기 등록한다 (원자는 허브의 Atom Catalog 참조).

(첫 Paper Ingest 를 실행하면 여기에 기록됩니다.)

---

## 📥 Recent Ingests

| Date | Source | Pages Touched |
|------|--------|---------------|
| 2026-04-12 | [[2026-04-12-Karpathy-LLM-Wiki\|Karpathy LLM Wiki Gist]] | 10 pages (예시) |

→ [[log]] 참조

---

## 🔗 Quick Links

- [[log]] — 전체 변경 이력
- [[CLAUDE]] — Schema (볼트 규칙서)
- [[Core Context]] — 사용자 맥락 (채워서 사용)

---

## 🚀 시작하기

1. [[Core Context]] 에 본인 정체성·목적·철학 채우기
2. Obsidian Web Clipper 로 관심 소스를 `00. Inbox/` 에 저장
3. `/ingest` — 목적 질문에 답하면 Raw Sources + Wiki 페이지 자동 생성
4. `/query` — 쌓인 Wiki 를 바탕으로 질문 답변
5. `/lint` — 주기적으로 건강도 체크

자세한 가이드는 [[LLM-Wiki-Starter-Kit]] 참조.
