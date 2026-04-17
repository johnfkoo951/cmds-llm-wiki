---
description: Scan `00. Inbox/` for unprocessed files and batch-ingest them, delegating per-file work to /ingest (which enforces the purpose gate).
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# /inbox — LLM Wiki Inbox Scanner

Scan `00. Inbox/` and its subfolders for unprocessed files and offer to ingest them.

> **🧭 Prerequisite**: [[Core Context]] once per session. Batch mode asks the purpose question once (single axis) or per-file based on the user's choice.

## Input

`$ARGUMENTS`

- If blank: scan ALL subfolders
- If a category name (e.g., `articles`, `papers`): scan only that subfolder
- If `count` or `status`: just show counts without detail

## Inbox Structure

```
00. Inbox/
├── 01. Articles/      ← 웹 기사, 블로그, 뉴스
├── 02. Papers/        ← 학술 논문, 기술 보고서
├── 03. Transcripts/   ← 강연, 팟캐스트, 영상 전사
├── 04. Clippings/     ← 짧은 스니펫, 트윗 스레드
└── (root)             ← 미분류 파일
```

Files in subfolders already have a category assigned (by Web Clipper template).
Files in the root `00. Inbox/` are uncategorized and need category assignment.

## Process

### Step 1: Scan

Scan all folders recursively. Skip `.gitkeep` files.
- `00. Inbox/01. Articles/*.md`
- `00. Inbox/02. Papers/*.md`
- `00. Inbox/03. Transcripts/*.md`
- `00. Inbox/04. Clippings/*.md`
- `00. Inbox/*.md` (root — uncategorized)

If empty everywhere, report "Inbox is empty. Nothing to ingest."

### Step 2: Preview

For each file found:
1. Read the content (first 100 lines if large)
2. Check frontmatter for Web Clipper metadata:
   - `category` → use as-is (already classified by Web Clipper)
   - `source` → original URL
   - `author` → original author
   - `date clipped` → when it was captured
3. If no frontmatter category: infer from subfolder name, or suggest one
4. Extract: title, source URL, language, approximate length, key topics (2-3)

### Step 3: Present

Show a grouped summary:

```
📥 Inbox Status
──────────────────────────
Articles:     {n} files
Papers:       {n} files
Transcripts:  {n} files
Clippings:    {n} files
Uncategorized: {n} files
──────────────────────────
Total: {n} files pending
```

Then a detail table:

| # | Category | File | Source | Topics |
|---|----------|------|--------|--------|
| 1 | Articles | ... | ... | ... |

### Step 4: Ask

Ask two questions in one turn:
1. **Scope**: "전부 / 카테고리만 / 선택만" — which files?
2. **Purpose mode** (미래의 나에게 보내는 편지, see [[Core Context]] §2):
   - **Single-axis bulk**: 모두 같은 목적 (예: "이번 주 강의 자료") → 한 번만 묻고 모든 파일에 같은 `collectionPurpose` 적용
   - **Per-file**: 파일마다 다른 목적 → /ingest 가 파일별로 질문
   - **Auto-infer**: "알아서 판단" → /ingest 가 소스 + Core Context 로 추론 + 추론 근거 명시

### Step 5: Ingest

For each file to ingest, run the full ingest pipeline:
1. The subfolder determines the Raw Source category:
   - `00. Inbox/01. Articles/` → `10. Raw Sources/11. Articles/`
   - `00. Inbox/02. Papers/` → `10. Raw Sources/12. Papers/`
   - `00. Inbox/03. Transcripts/` → `10. Raw Sources/14. Transcripts/`
   - `00. Inbox/04. Clippings/` → `10. Raw Sources/15. Clippings/`
   - `00. Inbox/` (root) → ask user or infer category
2. Preserve Web Clipper frontmatter (source URL, author, date) in the raw source
3. Create/update wiki pages (10~15 per source)
4. Update index.md and log.md

### Step 6: Cleanup

After successful ingest, ask user:
- "Inbox에서 처리된 파일 삭제할까요?" → delete originals from Inbox
- Or leave them (user can manually clean up)

## Notes

- Web Clipper files have `type: inbox` and `category` in frontmatter — use these as reliable category signals
- If a file has both frontmatter category AND is in a subfolder, frontmatter takes precedence
- For batch ingest (5+ files), process sequentially and show progress: `[3/7] Ingesting: article-title...`
