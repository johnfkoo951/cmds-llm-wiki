---
description: Ingest a source (URL/file/text) into Raw Sources + compile 10~15 Wiki pages, with mandatory user-purpose gate and mothership cross-linking.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebFetch, mcp__qmd__query
---

# /ingest — LLM Wiki Ingest

Ingest source material into the LLM Wiki. Follow CLAUDE.md rules strictly (YAML: 2 spaces, Body: TAB, wikilinks in YAML: quoted).

> **🧭 Prerequisite**: Read [[Core Context]] first (once per session). It establishes the user's 7 reuse axes and philosophy — ingest quality depends on it.

## Input

`$ARGUMENTS`

- If a **URL**: fetch the content with WebFetch, then process
- If a **file path** or **filename**: read that file from the vault (check `00. Inbox/` and its subfolders first)
- If **blank or "all"**: delegate to `/inbox` (scan all Inbox subfolders)
- If **raw text**: treat the argument itself as the source content

## Category Detection

Determine the Raw Source category in this priority order:
1. **Inbox subfolder** — file in `00. Inbox/01. Articles/` → category: Articles
2. **Web Clipper frontmatter** — `category` property in YAML → use as-is
3. **Content inference** — LLM analyzes content to determine best fit
4. **Default** — Articles (most common for web content)

Category → Path mapping:
| Category | Inbox Path | Raw Source Path |
|----------|------------|----------------|
| Articles | `00. Inbox/01. Articles/` | `10. Raw Sources/11. Articles/` |
| Papers | `00. Inbox/02. Papers/` | `10. Raw Sources/12. Papers/` |
| Books | — | `10. Raw Sources/13. Books/` |
| Transcripts | `00. Inbox/03. Transcripts/` | `10. Raw Sources/14. Transcripts/` |
| Clippings | `00. Inbox/04. Clippings/` | `10. Raw Sources/15. Clippings/` |

## Process (execute ALL steps in order)

### Step 0: Ask Collection Purpose (Gold In Gold Out) — MANDATORY

**Before doing anything else**, ask the user ONE consolidated question:

> "이 소스를 왜 수집하셨나요? 7 재활용 축 중 어디에 쓰일 예정인가요?
> (1) PhD 연구 · (2) 학술 출판 · (3) 강의·강연 · (4) 컨설팅 · (5) CMDS 시스템 · (6) 에세이·브랜딩 · (7) 제품·플러그인
> — 한 줄로 맥락을 덧붙여 주시면 됩니다. 예: '(3) 강의 — 4월 기업 임원 세미나 자료'"

Rules:
- Ask ONLY this question. Do not bombard the user with multiple questions.
- If the user explicitly says "알아서 판단해줘" or "자동으로" → infer the most likely axis from source content + [[Core Context]] §2 and state inference + reason explicitly. Still record in `collectionPurpose`.
- Save the user's answer verbatim into `collectionPurpose` (Raw Source frontmatter).
- **Batch mode** (`/ingest all`): ask once up front — "오늘 들어온 {N}개 소스, 전체를 하나의 목적으로 묶으시겠어요, 아니면 개별로 물을까요?". Respect user's choice.

### Step 0-a: Search Main Vault for Connections — MANDATORY when purpose given

Once the user provides purpose, search the (optional) mothership vault for related notes/concepts, as registered in [[Core Context]] §5. This becomes `mainVaultRelated`. Skip this step if no mothership is configured.

```
# Semantic search (preferred — user-scope qmd, cwd-independent)
mcp__qmd__query(
  searches=[
    {type: "vec", query: "<key concept 1 from source>"},
    {type: "vec", query: "<user's collectionPurpose keywords>"}
  ],
  intent="Find mothership notes related to this ingest for cross-vault linking"
)

# Keyword fallback
Grep(pattern="<key term>", path="{PATH_TO_YOUR_MOTHERSHIP_VAULT}", output_mode="files_with_matches", head_limit=20)
```

Filter to **2~5 highest-relevance notes**. Prefer:
1. Essays in `30. Permanent Notes/` (user's original thinking)
2. MOCs or 🏛 hub notes
3. CMDS category pages (`📚 N0N ...`)
4. Recent meeting/consulting notes if the purpose is teaching/consulting

Format each as: `"→ {your-mothership-vault-name}: {relative path from vault root}"`.

Show the user the candidate list, ask: **"이 중 연결할 노트를 골라주시거나, 추가로 생각나는 것 있으면 알려주세요. (그대로 진행하려면 'ok')"**

Record the final list in `mainVaultRelated` (Raw Source + relevant Wiki pages). Also identify the best-fit CMDS category (`📚 NNN ...`) and record as `mainVaultCmds`.

### Step 1: Analyze

Read the source content thoroughly. Extract:
- **Key topics/concepts** (3~8): abstract ideas worth a Concept page
- **Entities** (1~5): people, organizations, products, models
- **Practical guidance** (0~3): how-to content worth a Guide page
- **Key claims**: assertions that should be fact-tracked
- **Connections**: concepts that link to existing wiki pages

Before creating pages, read `index.md` to check what pages already exist. Prioritize **updating** existing pages over creating new ones.

### Step 2: Save Raw Source

Create the raw source file in `10. Raw Sources/{NN. category}/`:
- Filename: `YYYY-MM-DD-{Title}.md` (today's date)
- Category: Articles (web), Papers (academic), Books, Transcripts, Clippings
- **MANDATORY — Preserve original content verbatim in `## Original Content` section.** No exceptions, no summaries, no "redacted for brevity." Including embedded image URLs, YouTube links, customer quote blocks, citation lists. If the source is extremely long (e.g., >10K words), still preserve it — this is the immutable layer of the 3-Layer Architecture.
	- If the Inbox clipper already wraps the article body in `## Original Content`, copy that section verbatim.
	- If the source is a URL (WebFetch), preserve the fetched content.
	- Deduplicate only obvious clipper artifacts (e.g., customer-quote block repeated 3x due to clipper bug) and note the dedup in `## Ingest Notes`.
	- Images: keep the markdown `![alt](url)` lines even if CDN-hosted — the URL is part of the record.
- If from Web Clipper: carry over frontmatter (`source` URL, `author`, `date clipped`) into the raw source file
- Use the Category Detection rules above to determine the target subfolder

**Pre-flight checklist before moving on**:
- [ ] `## Original Content` section present
- [ ] Article body lines > 50 (or > 80% of Inbox body length for normal articles)
- [ ] Embedded images (`![...](...)`) preserved
- [ ] Embedded videos / media URLs preserved
- [ ] Customer quotes, citations, code blocks preserved verbatim
- [ ] Frontmatter has 7 required properties (type, aliases, description, author, date created, date modified, tags)

Frontmatter template:
```yaml
---
type: raw-source
aliases:
  - {short name}
description: {English, 1-2 sentences}
author:
  - {original author}
date created: {today ISO 8601}
date modified: {today ISO 8601}
date ingested: {today ISO 8601}
tags:
  - raw-source
  - {topic tags}
source: {URL or reference}
category: {Articles|Papers|Books|Transcripts|Clippings}
status: ingested
source-vault: "{your-mothership-vault-name}"
collectionPurpose: {user's answer from Step 0 — verbatim}
mainVaultRelated:
  - "→ {your-mothership-vault-name}: {path to related note 1}"
  - "→ {your-mothership-vault-name}: {path to related note 2}"
mainVaultCmds: "[[📚 NNN {Category Name}]]"
---
```

**YAML 준수 체크**: `collectionPurpose`, `mainVaultRelated`, `mainVaultCmds` 는 CMDS camelCase 네이밍 (v2 신설 키). snake_case 금지.

### Step 3: Compile Wiki Pages

For each extracted topic/entity/guide, either **update** an existing page or **create** a new one:

**Concepts** (`20. Wiki/21. Concepts/`):
- Abstract ideas, techniques, methodologies, patterns
- Include: Overview, Details, Related links, Sources, Open Questions
- `confidence`: high (well-sourced) / medium (partial) / low (speculative)

**Entities** (`20. Wiki/22. Entities/`):
- People, organizations, products, models, tools
- Include: Overview, Details, key contributions/features, Related

**Guides** (`20. Wiki/23. Guides/`):
- How-to content, practical tutorials, tooling guides
- Include: step-by-step instructions, prerequisites, tips

**When updating existing pages**:
- Add new information under relevant sections
- Add new source to the `source` property list
- Add new cross-references to `related` property
- If new info contradicts existing: add `> [!warning] Contradiction` callout
- Update `date modified`

**Target: 10~15 wiki pages touched per ingest.**

### Step 4: Connect

- Add `[[wikilinks]]` between all related pages
- Create or update relevant MOC in `20. Wiki/24. Maps/`
- Ensure no orphan pages (every new page linked from at least one other page)

### Step 5: Update index.md

- Add new pages to the appropriate category section (Concepts/Entities/Guides/Maps)
- Each entry: `- [[Page Name]] — one-line description`
- Update Stats table (counts)
- Add entry to Recent Ingests table

### Step 6: Update log.md

Append a new log entry (Karpathy-style prefix `## [YYYY-MM-DD] ingest | title`):
```markdown
## [{YYYY-MM-DD}] ingest | {source title}

- Source: [[{raw source filename}]]
- **Purpose**: {collectionPurpose verbatim}
- Mothership links: {mainVaultRelated count} — {top 1-2 paths}
- Pages created: [[page1]], [[page2]], ...
- Pages updated: [[page3]], [[page4]], ...
```

### Step 7: Review

After all writes are complete, do a quick health check:
- **Raw Source verbatim preservation check**: grep the new raw source for `^## Original Content` — must be present AND followed by substantive body (not just 1-2 lines). If source was from Inbox, compare line count to inbox file body to confirm no accidental summarization.
- Verify all new `[[wikilinks]]` point to existing pages
- Check that no duplicate pages were created
- Confirm index.md reflects the current state
- Report any open questions or knowledge gaps discovered

**Failure mode to watch for**: summarizing the original content into "Key Takeaways" / "Core Thesis" sections INSTEAD OF preserving verbatim body. Summaries belong in Wiki pages, not Raw Sources. Raw Sources are the immutable source-of-truth layer — if verbatim content is missing, the Raw Source is corrupt regardless of how rich the summary is.

## Output

Summarize the ingest result:
1. Source: what was ingested (title, URL if applicable)
2. Raw Source: where saved
3. Pages created: list with one-line descriptions
4. Pages updated: list with what changed
5. Connections: key cross-references added
6. Open questions: gaps or contradictions discovered
