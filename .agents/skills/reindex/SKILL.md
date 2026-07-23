---
name: "reindex"
description: "Manually re-run qmd indexing and embeddings for wiki, raw_sources, and queries after Obsidian edits, bulk moves, or embedding-model changes; also responds to /reindex and 재색인."
---

# reindex

Use this skill when the user asks to run `reindex`, `/reindex`, or rebuild qmd indexes.

## Command Template

# /reindex — qmd 인덱스 재구축

qmd 인덱스를 수동으로 재구축합니다. 보통은 PostToolUse hook이 자동으로 처리하지만, 다음 경우에 수동 실행이 필요합니다:

- Obsidian에서 직접 파일 편집했을 때 (hook 미발화)
- 외부 도구로 대량 파일 변경 후
- 임베딩 모델 교체 후 (`qmd embed -f`로 강제 재임베드)
- `qmd status`에서 vector 수가 문서 수와 어긋날 때

## Workflow

```bash
export QMD_EMBED_MODEL="hf:Qwen/Qwen3-Embedding-0.6B-GGUF/Qwen3-Embedding-0.6B-Q8_0.gguf"
qmd update    # BM25 인덱스 갱신 (변경된 파일만)
qmd embed     # 벡터 임베딩 생성 (새/변경된 청크만)
qmd status    # 상태 확인
```

강제 재임베드 (예: 모델 교체 후):

```bash
qmd embed -f
```

## Check results

쿼리 테스트:

```bash
qmd vsearch "테스트 쿼리" -n 3
qmd query "LLM Wiki Pattern" -n 3   # hybrid + reranking
```

## Scope

이 커맨드는 다음 3개 collection을 갱신:

- **wiki**: `20. Wiki/**/*.md` (Concepts, Entities, Guides, MOCs)
- **raw_sources**: `10. Raw Sources/**/*.md` (불변 원본)
- **queries**: `30. Queries/**/*.md` (합성된 쿼리 결과)

Inbox는 스코프 제외 (아직 ingest 전 staging).

## Related

- Auto-reindex hook: `.codex/hooks/qmd-reindex.sh` (PostToolUse, debounced 8초)
- Config: `~/.config/qmd/index.yml` (template: `90. Settings/qmd-config-template.yml`)
- Guide: → qmd README — https://github.com/tobi/qmd
