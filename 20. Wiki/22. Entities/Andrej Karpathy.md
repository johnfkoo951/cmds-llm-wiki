---
type: wiki-page
aliases:
  - Karpathy
  - 카르파시
description: Andrej Karpathy — AI researcher, former Tesla AI Director, OpenAI founding member, creator of the LLM Wiki pattern. Known for making deep learning education accessible.
author:
  - Claude
date created: 2026-04-12T00:00
date modified: 2026-04-14T16:00
tags:
  - person
  - ai-researcher
  - educator
source:
  - "[[2026-04-02-Karpathy-LLM-Knowledge-Bases-X-Thread]]"
  - "[[2026-04-12-Karpathy-LLM-Wiki]]"
  - "[[2026-04-13-Changhyun-Ahn-Soverign-PKM]]"
related:
  - "[[LLM Wiki Pattern]]"
  - "[[Synthetic Data Generation for Wiki]]"
  - "[[kepano (Steph Ango)]]"
  - "[[qmd]]"
  - "[[Sovereign PKM]]"
  - "Changhyun Ahn"
  - "Yohan Koo"
confidence: high
layer: entities
status: active
---

# Andrej Karpathy

> [!tip] Key Insight
> AI 연구자이자 교육자. Tesla AI Director를 거쳐, 딥러닝의 대중화와 LLM 활용 패턴을 선도하고 있다.

---

## Overview

Andrej Karpathy는 슬로바키아 출신의 AI 연구자, 교육자, 엔지니어이다. Stanford에서 Fei-Fei Li 지도하에 박사 학위를 받았으며, OpenAI 창립 멤버, Tesla AI Director (Autopilot)를 역임했다. 딥러닝 교육 콘텐츠(YouTube 강의, 블로그, nanoGPT 등)로 널리 알려져 있다.

---

## Details

### 주요 이력

- **Stanford CS PhD**: Computer Vision, Fei-Fei Li 연구실
- **OpenAI**: 창립 멤버 (2015)
- **Tesla**: AI Director, Autopilot 리드 (2017-2022)
- **OpenAI 복귀**: 2023, 이후 퇴사
- **독립 활동**: 교육 콘텐츠, 오픈소스 프로젝트

### LLM Wiki와의 관계

2026년 4월, [[LLM Wiki Pattern]]을 두 단계로 공개:

| 시점 | 형태 | 비고 |
|------|------|------|
| **2026-04-02** | X 포스트 → [[2026-04-02-Karpathy-LLM-Knowledge-Bases-X-Thread]] | 825 words, 패턴의 최초 공개. kepano·YohanKoo·Beomsu 답글 획득 |
| **2026-04-06** | 공식 Gist → [[2026-04-12-Karpathy-LLM-Wiki]] | X 버전을 확장, "Optional CLI tools"에서 [[qmd]] 권장 추가 |

이 볼트({your-llm-wiki})가 그 패턴의 구현체이다.

**Karpathy의 실사용 방식**:
- LLM 에이전트를 한쪽에, Obsidian을 다른 쪽에 열어놓고 작업
- LLM이 대화 기반으로 wiki를 편집하면 Obsidian에서 실시간 탐색
- "Obsidian은 IDE, LLM은 프로그래머, Wiki는 코드베이스"
- **개인 deployment 규모**: ~100 articles / ~400K words (자가 공개, 2026-04-02)
- **확장 구상**: [[Synthetic Data Generation for Wiki|Wiki 기반 파인튜닝]]으로 지식을 가중치에 내장하는 방향

### 커뮤니티 반응

X 스레드에서 주목할 답글 3개:
- [[kepano (Steph Ango)]] (Obsidian CEO): [[Contamination Mitigation]] 개념 제시
- **YohanKoo** (Yohan Koo): 10,000+ 노트 CMDS 볼트가 동일 패턴에 독립 도달했다고 보고 (3년간)
- **Beomsu** (@BeromArtDev): [[qmd]] 실사용 확인

**한국 PKM 커뮤니티의 reframing** (2026-04-13):

Changhyun Ahn의 LinkedIn Pulse 에세이는 Karpathy의 LLM Wiki를 **"혁신의 출발점이 아니라, 이미 앞서 가던 흐름이 AI 본류의 입에서 재확인된 signal"** 로 해석. "Markdown Is All You Need"라는 슬로건 아래 더배러·Yohan Koo 등 한국 PKM 실천자들이 동일 방향에 먼저 도달해 있었다는 주장. Karpathy의 발화가 **도구의 정당성**보다 **구조적 정당성**의 확인으로 기능.

### 교육 기여

- **YouTube**: "Neural Networks: Zero to Hero" 시리즈
- **nanoGPT**: 교육용 미니멀 GPT 구현
- **micrograd**: 자동미분 교육 라이브러리
- **cs231n**: Stanford Computer Vision 강의 (조교 → 교수)

---

## Related

- [[LLM Wiki Pattern]] — Karpathy가 제안한 핵심 패턴
- [[Synthetic Data Generation for Wiki]] — Karpathy의 forward-looking 확장
- [[kepano (Steph Ango)]] — X 스레드 대화 상대, 주요 해석자
- [[qmd]] — Karpathy가 권장한 search tool
- [[Sovereign PKM]] — Karpathy 패턴을 Korean PKM 관점에서 reframe
- Changhyun Ahn — Sovereign PKM 관점의 에세이 저자
- Yohan Koo — 본 vault 소유자, X 스레드에서 회신

---

## Sources

- [[2026-04-02-Karpathy-LLM-Knowledge-Bases-X-Thread]] — 원조 X 스레드
- [[2026-04-12-Karpathy-LLM-Wiki]] — 확장된 Gist
- [[2026-04-13-Changhyun-Ahn-Soverign-PKM]] — Korean PKM 관점의 reframing

---

## Open Questions

> [!question] Open Question
> Karpathy 자신이 이 패턴을 어떤 도메인에서 실제로 사용하고 있는지, 그 결과물은 공개되어 있는지?
