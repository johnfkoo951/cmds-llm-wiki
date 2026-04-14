---
type: moc
aliases:
  - LLM Wiki 사용 가이드
  - Getting Started
description: Onboarding guide for the CMDS LLM Wiki vault. Explains the 3-layer architecture, how to ingest sources, query knowledge, and maintain wiki health. Start here if you are new to this vault.
author:
  - Claude
date created: 2026-04-10T21:30
date modified: 2026-04-12T00:00
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
