---
type: log
aliases:
  - Change Log
  - Wiki Log
  - Ingest Log
description: Chronological log of all wiki operations — ingests, queries, lint fixes, and structural changes. Append-only; entries use `## [YYYY-MM-DD] operation | title` prefix for grep-based parsing.
author:
  - "[[{your-name}]]"
date created: {YYYY-MM-DD}
date modified: {YYYY-MM-DD}
tags:
  - system
  - log
status: active
---

# 📝 LLM Wiki — Change Log

> 모든 wiki 변경사항을 시간순으로 기록합니다. **Append-only** — 기존 항목을 수정하지 마세요.
>
> **Entry format (Karpathy-style)**: `## [YYYY-MM-DD] operation | title`
>
> **Quick scan**:
>
> ```bash
> grep "^## \[" log.md | tail -10   # 최근 10개 operation
> grep "^## \[.*\] ingest" log.md   # ingest만 필터
> ```
>
> **Operations**: `ingest`, `update`, `create`, `lint`, `query`, `restructure`, `cleanup`

---

## [2026-04-12] ingest | Karpathy LLM Wiki Gist (example)

- Source: [[2026-04-12-Karpathy-LLM-Wiki]]
- Origin: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
- Raw Source 저장: `10. Raw Sources/11. Articles/`
- Wiki 페이지 생성 (10):
	- Concepts (4): [[LLM Wiki Pattern]], [[RAG vs Compiled Wiki]], [[3-Layer Architecture]], [[Ingest-Query-Lint Cycle]]
	- Entities (3): [[Andrej Karpathy]], [[Vannevar Bush]], [[Memex]]
	- Guides (1): [[Obsidian Tooling for LLM Wiki]]
	- Maps (2): [[MOC-Knowledge Management]], [[MOC-LLM Wiki Guide]]
- **예시 ingest** — 이 볼트가 어떻게 성장하는지 보여주기 위한 샘플. 본인 소스 ingest 시작 시 이 entry 아래에 append.

## [{YYYY-MM-DD}] create | Vault initialized

- Cloned from [cmds-llm-wiki template](https://github.com/johnfkoo951/cmds-llm-wiki)
- Core Context 채움 완료 (§1 정체성, §2 재활용 축, ...)
- 첫 ingest 진행 예정
