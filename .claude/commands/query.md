---
description: Search Wiki pages, synthesize a cited answer, optionally save to 30. Queries/, and feed gaps/contradictions back into the Wiki.
allowed-tools: Read, Write, Edit, Glob, Grep, mcp__qmd__query
---

# /query — LLM Wiki Query

Answer a question by searching the wiki, synthesizing information, and optionally saving the result.

> **🧭 Prerequisite**: [[Core Context]] once per session. Tailor answers to the user's 7 reuse axes (PhD / 학술 / 강의 / 컨설팅 / CMDS / 에세이 / 제품) — a good answer connects to at least one axis.

## Input

`$ARGUMENTS`

## Process

### Step 1: Search

Read `index.md` to identify relevant pages. Then read those pages in full.
If the question spans multiple topics, read pages from each relevant area.

### Step 2: Synthesize

Compose a comprehensive answer based on wiki content:
- Cite sources with `[[wikilinks]]` to specific wiki pages
- If information is from raw sources, reference via the wiki page that compiled it
- Note confidence level based on source quality

### Step 3: Identify Gaps

While answering, note:
- Questions the wiki **cannot** answer → flag as knowledge gaps
- Contradictions discovered between pages → add `> [!warning]` callouts
- Missing pages that would help → suggest for future ingest

### Step 4: Save (if substantial)

If the answer is substantial (comparison, analysis, multi-source synthesis), save it:
- File: `30. Queries/YYYY-MM-DD-Q-{question-summary}.md`
- Type: `query-result`
- Include referenced pages in `source` property

If it's a simple factual answer, just reply without saving.

### Step 5: Feedback

Update wiki pages if the query revealed:
- Missing cross-references → add them
- Outdated information → flag with `> [!note] Update`
- New connections between concepts → add to `related` properties

### Step 6: Connect to User's 7 Reuse Axes

Before finalizing, ask which of the user's 7 reuse axes the answer feeds — see [[Core Context]] §2:
- (1) PhD 연구 · (2) 학술 출판 · (3) 강의·강연 · (4) 컨설팅 · (5) CMDS 시스템 · (6) 에세이·브랜딩 · (7) 제품·플러그인

Add a closing line to the answer: **"이 답변은 ${axis}에 활용 가능합니다 — ${one-sentence why}."**

If saving as Query Result, set `reusableFor` frontmatter to the matched axis.

## Output

Answer the question, then briefly note:
- Pages consulted
- Whether result was saved
- Any gaps or contradictions found
- Reuse axis the answer connects to
