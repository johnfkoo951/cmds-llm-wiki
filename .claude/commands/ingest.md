---
description: Ingest a source (URL/file/text) into Raw Sources + compile 10~15 Wiki pages, with mandatory user-purpose gate and mothership cross-linking.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebFetch, mcp__qmd__query
# Antigravity equivalents: view_file, write_to_file, replace_file_content, list_dir, grep_search, run_command, read_url_content
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
- If an **academic paper** (DOI/arXiv/journal URL, PDF with Abstract+References, or a file from `00. Inbox/02. Papers/`): **use Paper Ingest Mode** — read `.agents/skills/ingest/resources/paper-ingest.md` for the full 12-step pipeline (do NOT inline it here — progressive disclosure keeps this command lean).
- If a **multi-page book/docs site** (mdBook, VitePress, GitBook, Docusaurus, ReadTheDocs, Nextra with 5+ chapters in sidebar/TOC): **use Book Ingest Mode** — see dedicated section below.
- If a **binary/non-markdown file** (`.pdf`, `.pptx`, `.docx`, `.xlsx`, `.hwp`, `.hwpx`, `.epub`, `.html`, image, etc.): **run Step 0.5 (Format Conversion)** before any other processing.

## Step 0.5: Format Conversion (binary → markdown)

Detect by extension:

```bash
ext="${input##*.}"; ext="${ext:l}"
```

If `ext` is in `{md, markdown, txt}` → skip this step.

If `ext` is in `{mp3, wav, m4a}` → **delegate to an audio-transcription tool** (e.g., an `audio-transcriber` skill or Whisper), not a document converter.

Otherwise → **invoke a binary-to-markdown converter** — an `omni-to-md` skill if you have one, or run `markitdown` / `pandoc` / `hwp5txt` / `defuddle` directly on the file.

The converter should:
1. Convert the binary to markdown using the right tool for the format
2. Move the original binary to `80. References/Attachments/<original-filename>`
3. Produce a converted `.md` file (placed in the same Inbox subfolder, same basename)
4. Add these conversion frontmatter fields, which must be carried over to the Raw Source in Step 2:
   - `source-attachment: "[[<original-filename>]]"`
   - `source-format: pdf|pptx|docx|hwp|hwpx|...`
   - `conversion-tool: markitdown|pandoc|hwp5txt|defuddle|hwpx-xml`
   - `conversion-date: YYYY-MM-DD`
   - `conversion-fidelity: high|medium|low`

After conversion, **proceed to Step 0 (purpose gate) using the converted `.md` as the source**. The `## Original Content` verbatim section in Step 2 holds the *converted markdown* (not the original binary) — the original binary is preserved as an attachment, satisfying the immutable-source principle by reference.

If conversion fails (missing tool, unsupported format, empty output) → halt and tell the user how to install the missing tool, or ask them to convert manually.

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
| AI Research | `00. Inbox/05. AI Research/` | `10. Raw Sources/16. AI Research/` |

## Process (execute ALL steps in order)

### Step 0: Ask Collection Purpose (미래의 나에게 보내는 편지) — MANDATORY

**Before doing anything else**, ask the user ONE consolidated question — 미래의 나에게 보내는 편지:

> "미래의 내가 이 자료를 다시 볼 때 — 왜 수집했고, 어디에 쓸 예정인지 한 줄 남겨주세요.
> 재활용 축 참고: 사용자가 [[Core Context]] §2 에 정의한 5~9 개 축 (예: 학술 / 저술 / 강의 / 컨설팅 / 제품 / 에세이 / 커뮤니티)
> 예: '(3) 강의 — 4월 기업 임원 세미나 자료'"

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

**URL construction — MANDATORY validation** (prevents cross-vault link rot):

For each candidate, do NOT hand-construct the URL from memory. Instead:

1. **Use the actual file path returned by qmd/Grep**, not a reconstructed one. If qmd returned `30. Permanent Notes/33. Essay/foo.md`, use that exact string — do not strip `.md`, do not add prefixes.
2. **Percent-encode with a real encoder**, not the LLM's string manipulation:
   ```bash
   ENCODED=$(python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1], safe=''))" "<exact path from qmd>")
   ```
   `safe=''` ensures `/`, spaces, non-ASCII (Korean, emoji) all get encoded — Obsidian's URL parser expects this.
3. **Stat the file BEFORE writing the URL**:
   ```bash
   test -f "{PATH_TO_YOUR_MOTHERSHIP_VAULT}/<exact path from qmd>"
   ```
   If stat fails → DO NOT include this candidate in `mainVaultRelated`. Print: "qmd returned non-existent path: {path} — skipping".
4. Construct: `"[<label>](obsidian://open?vault={your-mothership-vault-name}&file=${ENCODED})"` where `<label>` is the filename without `.md`.

**`mainVaultCmds` construction — authoritative category list**:

Do NOT guess CMDS category names from memory. Build the authoritative set from the mothership filesystem first:

```bash
find "{PATH_TO_YOUR_MOTHERSHIP_VAULT}" -maxdepth 3 -name "📚 [0-9][0-9][0-9] *.md" -type f
```

Pick from this exact list. Format as `"[[📚 NNN {Name from file}]]"` (quoted wikilink — won't resolve in this satellite vault, but preserved as metadata). If the best-fit category file does not exist, leave `mainVaultCmds` empty rather than inventing one.

Show the user the candidate list (with validation results), ask: **"이 중 연결할 노트를 골라주시거나, 추가로 생각나는 것 있으면 알려주세요. (그대로 진행하려면 'ok')"**

Record the final, **stat-verified** list in `mainVaultRelated` (Raw Source + relevant Wiki pages) and `mainVaultCmds`.

**Failure mode this prevents**: LLM hand-constructed URLs with wrong encoding (missing percent-encoding for non-ASCII, wrong path depth, stale filename from memory). Result was broken `obsidian://` clicks that look valid in YAML but resolve to 404 in Obsidian. `/lint` Step 10 (Cross-Vault Link Check) catches drift after the fact, but ingest-time validation is the upstream fix — cheaper to prevent than to clean up.

### Step 1: Analyze

Read the source content thoroughly. Extract:
- **Key topics/concepts** (3~8): abstract ideas worth a Concept page
- **Entities** (1~5): people, organizations, products, models
- **Practical guidance** (0~3): how-to content worth a Guide page
- **Key claims**: assertions that should be fact-tracked
- **Connections**: concepts that link to existing wiki pages

Before creating pages, read `index.md` to check what pages already exist. Prioritize **updating** existing pages over creating new ones.

### Step 2: Save Raw Source (Move, not Copy)

> [!warning] This is a **MOVE** operation, not a copy
> If the source originated from `00. Inbox/`, the Raw Source write is **step 1 of 2**. Step 2 is **deleting the Inbox original** after verbatim-preservation is verified. Skipping the delete leaves the file visible to `/inbox` and re-ingested next scan — observed failure mode.

Create the raw source file in `10. Raw Sources/{NN. category}/`:
- Filename: `YYYY-MM-DD-{Title}.md` (today's date)
- Category: Articles (web), Papers (academic), Books, Transcripts, Clippings, AI Research
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

**Inbox cleanup (MANDATORY when source came from Inbox)**:

After the Raw Source file is written AND pre-flight checklist passes:

```bash
# Source determination rule
# Delete the Inbox file ONLY when the source originated from 00. Inbox/
# Do NOT delete when the source was a URL (WebFetch), external file path, or raw text — nothing to clean up.

rm "{vault-root}/00. Inbox/{subfolder}/{original-file.md}"
```

Matrix of source origin → cleanup action:
| Source origin | Action after Raw Source write |
|---------------|-------------------------------|
| `00. Inbox/NN. {category}/{file}.md` | **Delete** Inbox file |
| URL (WebFetch) | No file to delete |
| Absolute path outside Inbox | No delete — user-provided file |
| Raw text (prompt argument) | No file to delete |

**Edge cases**:
- If verbatim preservation check in Step 7 fails AFTER Inbox delete: the Inbox file is lost. Therefore, **delete only after all pre-flight checks pass**.
- If multiple Inbox files were batched into one Raw Source (rare): delete all consumed Inbox files. Document in `## Ingest Notes`.

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
category: {Articles|Papers|Books|Transcripts|Clippings|AI Research}
status: ingested
source-vault: "{your-mothership-vault-name}"
collectionPurpose: {user's answer from Step 0 — verbatim}
mainVaultRelated:
  - "[노트명1](obsidian://open?vault={your-mothership-vault-name}&file=URL_ENCODED_PATH_1)"
  - "[노트명2](obsidian://open?vault={your-mothership-vault-name}&file=URL_ENCODED_PATH_2)"
mainVaultCmds: "[[📚 NNN {Category Name}]]"
---
```

**YAML 준수 체크**: `collectionPurpose`, `mainVaultRelated`, `mainVaultCmds` 는 CMDS camelCase 네이밍 (v2 신설 키). snake_case 금지.

> [!warning] Cross-vault 링크 정확성 (mothership 운영 시)
> 위 템플릿의 `URL_ENCODED_PATH_*` 와 `📚 NNN {Category Name}` 는 **반드시 실제 값으로 치환**한다. 리터럴 placeholder 를 그대로 커밋 금지.
> - `mainVaultRelated` URL 의 `file=` 경로는 **모선 실제 파일명을 percent-encode** 한 값 — slug 추측(`03-ai-agent` 같은 lowercase-hyphen) 금지. 실제 폴더는 `03. AI Agent` 처럼 다를 수 있다. Step 0-a 에서 stat 검증한 값만 사용한다.
> - `mainVaultCmds` 는 **현재 모선 taxonomy 의 정확한 카테고리명**(`📚`/`📖` 이모지 포함)과 일치해야 한다. 리네임된 옛 이름은 조용히 깨진다. 최신 목록: `find "{PATH_TO_YOUR_MOTHERSHIP_VAULT}" -maxdepth 4 \( -name "📚 *.md" -o -name "📖 *.md" \)`.

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

**Quality control (v4)**:
- New Wiki pages default to `explored: false`
- Set `explored: true` only after a human or source-backed review loop has verified the page
- For `confidence: high` or synthesis-heavy pages, add:
	```markdown
	> [!note] Bias Check
	> Counter-argument: ...
	> Data gap: ...
	```

### Step 4: Connect

- Add `[[wikilinks]]` between all related pages
- Create or update relevant MOC in `20. Wiki/24. Maps/`
- Ensure no orphan pages (every new page linked from at least one other page)

### Step 5: Update index.md — MANDATORY full sync

This step is the #1 source of index drift. Every ingest sweep that leaves 10+ files unlinked failed here. Do all four:

- **Each new Wiki page → corresponding category section** (Concepts/Entities/Guides/Maps). Entry format: `- [[Page Name]] — one-line description`. Do NOT skip pages because the section "looks long enough."
- **Stats table** — recount and update Raw Sources / Wiki Pages / Concepts / Entities / Guides / MOCs / Queries. Run `find "20. Wiki/21. Concepts" -name "*.md" | wc -l` etc. to verify, do not increment-by-guess.
- **Recent Ingests table** — add one row at the top (most recent first).
- **`date modified` in index.md frontmatter** — update to today's date.

After writing, re-read index.md and verify all newly-created page names appear in the appropriate section list.

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
- **Raw Source verbatim preservation check**: grep the new raw source for `^## Original Content` — must be present AND followed by substantive body (not just 1-2 lines). If source was from Inbox, compare line count to inbox file body BEFORE the Inbox delete in Step 2, to confirm no accidental summarization.
- **Inbox cleanup check (MANDATORY if source came from Inbox)**: verify the original Inbox file has been deleted. Run `ls "00. Inbox/{subfolder}/"` — the consumed file should NOT appear. If it still exists, delete it now (Step 2 requirement).
- Verify all new `[[wikilinks]]` point to existing pages
- Check that no duplicate pages were created

**v4 schema compliance** — for every new Wiki page created in this ingest, verify:

- **`explored: false` set** — `grep -L "^explored:" <newpage>.md` should return empty
- **Bias Check present on high-confidence pages** — for every page with `confidence: high`, the body must contain `> [!note] Bias Check` AND lines starting with `> Counter-argument:` and `> Data gap:`
- **`mainVaultRelated` populated** — if Step 0-a returned mothership candidates, frontmatter has them as `obsidian://open?vault=...` URLs

**Cross-vault link integrity (mothership only)** — mothership refs are invisible to Obsidian's graph. Verify them against the mothership filesystem BEFORE reporting done:

```bash
python3 - <<'PY'
import os, re, urllib.parse, glob
M = "{PATH_TO_YOUR_MOTHERSHIP_VAULT}"
VAULT = "{your-mothership-vault-name}"
U = re.compile(r'obsidian://open\?vault=' + re.escape(VAULT) + r'&file=([^)"\s]+)')
for f in glob.glob("20. Wiki/**/*.md", recursive=True) + glob.glob("10. Raw Sources/**/*.md", recursive=True):
    t = re.sub(r'```.*?```', '', open(f, encoding="utf-8").read(), flags=re.S)  # skip fenced code
    t = re.sub(r'`[^`\n]*`', '', t)  # and inline code (doc examples)
    for m in U.finditer(t):
        d = urllib.parse.unquote(m.group(1))
        if d in ("URL_ENCODED_PATH", "...") or not any(os.path.isfile(os.path.join(M, c)) for c in (d, d+".md", (d[:-3] if d.endswith(".md") else d)+".md")):
            print("BROKEN", f, "->", d)
PY
```

Any `BROKEN` row from a file you touched → fix the `file=` path with the REAL mothership filename (or remove the entry). Never leave a literal `URL_ENCODED_PATH` / `...`.

- **`mainVaultCmds` resolves to a live category** — `[[📚 NNN ...]]` / `[[📖 NNN ...]]` must equal an existing mothership category exactly (emoji included). Renamed names break silently.
- **No bare `[[mothership]]` in body** — mothership files cited in Wiki/Raw BODY must be `[label](obsidian://open?vault=...)` or plain text, NEVER bare `[[...]]`. The `mainVaultCmds` frontmatter quoted-wikilink is the ONLY allowed non-resolving `[[📚 ...]]`.

**Index sync verification** — the #1 ingest failure mode:

- `grep -F "[[<newpage>]]" index.md` — every new page name must appear in index.md's Concepts/Entities/Guides/Maps section
- If missing, return to Step 5 and fix before reporting done
- Stats table counts must match `find "20. Wiki/<subfolder>" -name "*.md" | wc -l` for each category

Report any open questions or knowledge gaps discovered.

**Failure modes to watch for**:

1. **Summarization instead of verbatim**: summarizing the original content into "Key Takeaways" / "Core Thesis" sections INSTEAD OF preserving verbatim body. Summaries belong in Wiki pages, not Raw Sources. Raw Sources are the immutable source-of-truth layer — if verbatim content is missing, the Raw Source is corrupt regardless of how rich the summary is.

2. **Inbox residue**: writing the Raw Source but forgetting to delete the Inbox original. Symptom — next `/inbox` scan treats the same source as unprocessed and re-ingests it, creating duplicate Raw Sources. Mitigation — Step 2 Inbox cleanup is MANDATORY and Step 7 verifies it.

3. **v4 schema drift**: writing Wiki pages without `explored: false` or without Bias Check on high-confidence pages. Symptom — `/lint` Step 8 reports growing gaps. Mitigation — Step 3 quality control + Step 7 v4 schema compliance check. Run the grep one-liners; do not assume.

4. **Index drift**: creating Wiki pages but skipping Step 5 sync. Symptom — `index.md` Stats table out of date and pages missing from the Concepts/Entities sections, even though the Recent Ingests row was added. Mitigation — Step 5 four-part checklist must complete, Step 7 verifies via `grep -F "[[<page>]]" index.md`.

## Output

Summarize the ingest result:
1. Source: what was ingested (title, URL if applicable)
2. Raw Source: where saved
3. Pages created: list with one-line descriptions
4. Pages updated: list with what changed
5. Connections: key cross-references added
6. Open questions: gaps or contradictions discovered

---

## Paper Ingest Mode (Academic Papers) — pointer

- **Auto-detect**: DOI/arXiv/journal URL, a PDF whose body has an Abstract + References structure, or a file from `00. Inbox/02. Papers/`. Atomizes the paper into a 12-step analysis (hub S00 + knowledge atoms) under `40. Paper Analyses/{citekey}/`.
- **Read the resource file** `.agents/skills/ingest/resources/paper-ingest.md` for the full P-0 → P-7 pipeline (12-step schemes, citekey naming, RQ linking, `p7_verify.py` gate). Do NOT inline it here — progressive disclosure keeps this command lean.
- **2-question budget**: P-0 (collection purpose + which RQ this feeds — reads `20. Wiki/25. Questions/` RQ cards) and P-1 (paper type — 6-type classify + confirm). No other blocking questions.
- **Shared with Standard**: Step 0 (purpose gate) and Step 0-a (mothership search, Mode B only) are identical — Paper Mode extends them, it does not replace them.
- **User manual**: `90. Settings/Sharing/Paper Ingest Guide.md` — the 12 steps explained for humans.

---

## Book Ingest Mode (Multi-Page Sources) — Progressive Stubs

Activate this mode when the source is a **structured multi-page book or documentation site** (typical signals: a sidebar/TOC with ≥5 chapters, mdBook/VitePress/GitBook/Docusaurus/ReadTheDocs/Nextra frontends, or an explicit `book`/`docs` URL pattern). Standard `/ingest` dumps everything into one Raw Source; Book Mode creates a **navigable scaffold** — one Book Index file + N chapter stubs — and fills chapters progressively as the user reads them.

> **Why this is different**: Karpathy's LLM Wiki philosophy = "knowledge is compiled when read, not when scraped." Pre-ingesting 30 unread chapters = hoarding. Pre-creating 30 **stubs** = navigable future-compile targets, linked from the Index. Compile (fill verbatim + Wiki pages) only when the user actually reads each chapter.

### Step 0 + 0-a: same as standard (Purpose + Mothership search)

Still mandatory. Get one purpose answer covering the whole book.

### Step B-1: Fetch TOC + derive chapter URL pattern

```
WebFetch(url=<preface/readme/index URL>, prompt="Extract full TOC with chapter titles in their original order, preserve part groupings (Part/Section), return as JSON: [{part, ch, title, slug_hint}]")
```

Test URL pattern by fetching **2 chapter URLs** directly. Common patterns:
- mdBook: `/ch01-00-foo.html`, `/ch01-01-bar.html` or `/part1/ch01.html`
- VitePress/Docusaurus: `/ch01-foo/`, `/en/ch01-foo`
- GitBook: `/book/chapter-1/section-1`

Confirm the pattern matches reality before committing to naming.

### Step B-2: Create Book Index (1 Raw Source)

`10. Raw Sources/11. Articles/YYYY-MM-DD-{authorSlug}-{bookSlug}-book-index.md`

Contains:
- Full frontmatter (see stub frontmatter below but with `status: ingested` and **no `chapterNumber`**)
- **Verbatim** preface content in `## Original Content`
- `## TOC` — every chapter as `- [ ] [[stub filename]] — {TOC one-liner}` grouped by Part
- `## Reading Paths` — if author provides (e.g., role-based paths), preserve verbatim
- `## Progress Tracking` — table: `| Ch | Title | Status | Read on |`

### Step B-3: Create chapter stubs (N files)

For each chapter, create `10. Raw Sources/11. Articles/YYYY-MM-DD-{authorSlug}-{bookSlug}-ch{NN}-{slug}.md`:

```yaml
---
type: raw-source
status: stub                                # ← new status value
aliases:
  - "ch{NN} {English title}"
description: "Chapter {N} of {book} — {TOC one-liner}. Stub until read."
author:
  - "{book author}"
date created: {today}
date modified: {today}
date ingested: {today}                      # for stubs, = date scaffolded, not date read
tags:
  - raw-source
  - stub
  - {book-slug}
  - {topic tags from TOC}
source: "{direct chapter URL}"
category: Articles
bookIndex: "[[YYYY-MM-DD-{...}-book-index]]"   # ← new key
chapterPart: "{Part I / 第一篇 / etc.}"        # ← new key, preserve original language
chapterNumber: {N}                             # ← new key, integer
chapterPrev: "[[...ch{N-1}...]]"              # may be null for ch01
chapterNext: "[[...ch{N+1}...]]"              # may be null for last ch
collectionPurpose: "{inherited from book-level purpose}"
---

# {Ch{NN}: Full chapter title from TOC}

> [!info] Reading Status: Stub
> This chapter has not been read yet. Only the TOC one-liner is preserved. On reading, re-invoke `/ingest {this file path}` → verbatim body fill + Wiki page compile + `status: stub` → `completed` promotion.

## Source

- Original URL: {direct chapter URL}
- Book: [[YYYY-MM-DD-{...}-book-index]]
- Previous: [[...ch{N-1}...]] · Next: [[...ch{N+1}...]]

## TOC Preview

{the one-line summary from TOC, verbatim}

## Original Content

<!-- STUB: pending verbatim fill. Placeholder intentionally non-empty to satisfy validate-raw-source hook. -->

_This chapter body is empty while `status: stub`. Re-invoking `/ingest` on this file will fetch from the original URL and fill this section verbatim._

## Reading Notes

<!-- Notes, questions, wiki-promotion candidates added while reading -->
```

Pre-flight per stub:
- [ ] `## Original Content` section present (even as placeholder — required for hook)
- [ ] `status: stub` in frontmatter
- [ ] `source` = direct chapter URL (verified resolvable)
- [ ] `chapterNumber`, `chapterPart`, `bookIndex` set
- [ ] `chapterPrev` / `chapterNext` wikilinks point to existing stub files (or null for endpoints)
- [ ] No Wiki pages compiled yet for this chapter (that happens on promotion)

### Step B-4: Book-level Wiki pages (small set)

Compile only what's derivable from TOC + preface:

- **Entity**: `{Book Title (native)}` — the book itself
- **Entity**: `{Author Name}` — author
- **Entity** (optional): companion sites (e.g., visualization, discussion)
- **Concept(s)** (1~3): concepts the author names in the preface that are **anchor** to the whole book (e.g., "Agent Loop" as the book's anchor chapter)
- **Guide** (optional, 0~1): if preface itself contains a reusable methodology (e.g., reading paths)
- **MOC update**: link book index to relevant MOC

**Do NOT** pre-compile chapter-specific Wiki pages. Those appear at promotion time.

### Step B-5: Index + Log

- index.md Recent Ingests: `{N chapters scaffolded, M wiki pages}` format
- log.md: single entry documenting whole book scaffold + noting progressive compile plan

### Promotion Workflow (when user reads ch N)

Trigger: user runs `/ingest 2026-XX-XX-...-chNN-slug.md` OR describes the chapter in chat with intent to compile.

Steps:
1. Fetch chapter URL → verbatim body into `## Original Content` (replacing stub placeholder)
2. Flip `status: stub` → `status: completed` (or `reading` if partial)
3. Update `date modified`
4. Compile Wiki pages specific to this chapter (concepts/entities/updates to existing pages)
5. Update book index's Progress Tracking table: `- [ ]` → `- [x]`
6. Append log.md: `## [YYYY-MM-DD] promote | {book} ch{NN}`

### Frontmatter Keys Added by Book Ingest Mode

Keys introduced by this mode (camelCase per schema conventions):
- `bookIndex` — wikilink to the book index Raw Source
- `chapterNumber` — integer
- `chapterPart` — string, preserve source language
- `chapterPrev`, `chapterNext` — wikilinks, may be null
- `status: stub` — new enumerated value alongside `ingested`, `reading`, `completed`

### Hook Interaction

The `validate-raw-source.sh` PostToolUse hook enforces `## Original Content` presence. Book stubs **satisfy this by design** (placeholder block is non-empty). If the hook is upgraded to also check body substantiveness, it should exempt `status: stub`. Document this expectation here so future hook edits stay aware.

### Visual Pattern

```mermaid
flowchart TB
	User["User: multi-page book URL"]
	Detect["Book Mode detection"]
	Fetch["Fetch TOC + URL pattern"]
	Index["Create Book Index (verbatim preface)"]
	Stubs["Create N chapter stubs"]
	BookWiki["Book / author / anchor concept Wiki pages"]

	User --> Detect --> Fetch --> Index
	Index --> Stubs
	Index --> BookWiki

	Read["User reads ch3"]
	Promote["/ingest {ch3 stub}"]
	Compile["Fill body + compile Wiki + update Progress"]

	Stubs -.progressive.-> Read --> Promote --> Compile
```
