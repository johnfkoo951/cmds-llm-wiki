---
type: moc
aliases:
  - LLM Wiki 사용 가이드
  - Getting Started
description: Onboarding guide for the CMDS LLM Wiki vault. Explains the 3-layer architecture, how to ingest sources, query knowledge, and maintain wiki health. Start here if you are new to this vault.
author:
  - Claude
date created: 2026-04-10T21:30
date modified: 2026-10-21T19:15
tags:
  - moc
  - guide
  - onboarding
topic:
  - llm-wiki
  - knowledge-management
related:
  - "[[index]]"
  - "[[CLAUDE]]"
  - "[[log]]"
  - "[[MOC-Knowledge Management]]"
  - "[[LLM Wiki Pattern]]"
status: active
source-vault: {your-mothership-vault-name}
---

# MOC-LLM Wiki Guide

> 이 볼트는 **Andrej Karpathy의 LLM Wiki 패턴**을 구현한 지식 베이스입니다.
> LLM이 raw source를 컴파일하여 persistent wiki를 직접 관리합니다.

---

## 🏗 Architecture

```
┌─────────────────────────────────────────────┐
│                Schema Layer                  │
│            CLAUDE.md (규칙서)                 │
├─────────────────────────────────────────────┤
│              Wiki Layer                      │
│   20. Wiki/ (LLM이 관리하는 지식 페이지)       │
│   ┌──────────┬──────────┬────────┬────────┐ │
│   │ Concepts │ Entities │ Guides │  Maps  │ │
│   └──────────┴──────────┴────────┴────────┘ │
├─────────────────────────────────────────────┤
│           Raw Sources Layer                  │
│   10. Raw Sources/ (불변 원본 자료)            │
│   ┌──────────┬────────┬───────┬───────────┐ │
│   │ Articles │ Papers │ Books │Transcripts│ │
│   └──────────┴────────┴───────┴───────────┘ │
└─────────────────────────────────────────────┘
```

---

## 📥 How to Ingest

1. 새 자료를 `00. Inbox/`에 드롭
2. Claude Code에게 ingest 요청: *"이 자료를 Wiki에 인제스트해줘"*
3. LLM이 자동으로:
	- Raw Source를 `10. Raw Sources/`로 이동 (원본 보존)
	- 관련 Wiki 페이지 10~15개 incremental update
	- `[[log]]`에 기록, `[[index]]` 업데이트

---

## 🔍 How to Query

- Wiki 페이지를 직접 탐색하거나
- Claude Code에게 질문: *"Transformer의 attention 메커니즘을 설명해줘"*
- LLM이 Wiki에서 관련 페이지를 검색하여 합성 답변 생성
- 결과는 `30. Queries/`에 저장 가능

---

## 🔧 How to Maintain (Lint)

주기적으로 Claude Code에게 요청:
- *"Wiki health check 해줘"* — orphan, stale, contradiction 검사
- *"인덱스 동기화해줘"* — `[[index]]`와 실제 구조 일치 확인
- *"broken links 찾아줘"* — 누락된 링크 자동 생성/플래그

---

## 📊 Explored 학습 보드

[[Explored 학습 보드.base|Explored 학습 보드]]는 `explored` 메타데이터로 읽은 카드와 아직 안 읽은 카드를 모아 보여 주는 Obsidian Bases 보드다 (v1.13.0). Obsidian 1.9 이상의 Bases 코어 플러그인이 필요하다.

| 뷰 | 용도 |
|---|---|
| 📖 주제별 대기열 | MOC 영역별로 아직 읽지 않은 카드. 연결이 많은 허브 카드부터 |
| 🗂️ 유형별 대기열 | 개념 → 가이드 → 엔티티 → 연구 질문 순 |
| 🎯 먼저 읽을 것 | `confidence: high` 또는 `disputed` 인데 아직 사람이 읽지 않은 카드 |
| 🆕 최근 2주 유입 | 새로 들어온 카드 |
| ✅ 읽은 것 | 읽은 날 순 |
| 📊 영역별 진행률 | 영역마다 읽은 개수와 % (MOC 제외) |
| ❓ 연구 질문 · 📄 논문 12단 분석 | RQ 카드, 논문 허브와 원자 |
| 🧭 이어 읽기 | 노트에 임베드하면 그 노트가 링크한 카드만 보여 준다 |
| 🗺️ 지도 검토 | MOC 마다 지도 검토 여부와 그 지도 속 카드의 읽음 진도 |
| 🃏 카드로 훑어보기 | 요약 위주 카드 뷰 |

- **읽음 표시**: 표의 `읽음` 체크박스를 누르면 그 노트에 `explored: true` 가 기록된다. 사람이 직접 읽은 것도 Exploration Gate 완료로 인정된다. `exploredDate` 도 함께 채우면 좋다.
- **주제 영역 계산**: "이 카드를 링크하는 MOC" 를 MOC 쪽에서 확인한다. 여러 MOC 에 걸친 카드는 보드의 `domains` 공식 목록에서 먼저 나오는 MOC 가 대표 영역이 된다.
- **MOC 를 새로 만들면**: 보드 파일의 `domains` 공식 목록에 `MOC-` 를 뺀 이름을 추가한다 (예: `"Agent Memory"`). 구체적인 MOC 를 앞에, 포괄적인 MOC 를 뒤에 두면 겹치는 카드가 더 구체적인 영역으로 간다.
- **MOC 의 `explored`**: claim 카드가 아니라 **지도 검토** 표시다. 진행률 분모에 들어가지 않는다.
- **MOC 에 임베드**: `![[Explored 학습 보드.base#🧭 이어 읽기]]`

## 🔗 CMDSPACE 메인 볼트 연결

이 볼트는 `{your-mothership-vault-name}` 볼트의 satellite입니다.

| 용도 | 볼트 |
|------|------|
| 전체 PKM (일상·업무·학습) | {your-mothership-vault-name} |
| LLM 전용 지식 컴파일 | {your-llm-wiki} (여기) |

### Cross-Reference 방법

메인 볼트의 노트를 참조할 때:
- `source-vault: {your-mothership-vault-name}` 프로퍼티 사용
- Body에서: `→ CMDSPACE: 카테고리/노트명` 형식으로 텍스트 참조
- 관련 원본: → CMDSPACE: `00. Inbox/2026-04-08-Karpathy LLM Wiki.md`

### 메인 볼트에서 이 볼트 참조

메인 볼트에서 이 Wiki를 참조하려면:
- `→ LLM Wiki: 페이지명` 형식 사용
- 또는 `source-vault: {your-llm-wiki}` 프로퍼티 활용
