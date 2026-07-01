---
description: Ingest a URL, file, or inbox item into Raw Sources and compile durable Wiki pages with Codex-safe tool assumptions.
---

# /ingest — Codex LLM Wiki Ingest

Follow [[AGENTS.md]] first. Read [[Core Context]] once per session before ingest so the source is tied to the user's 7 reuse axes.

## Codex Tool Map

- Read/search files with `rg`, `sed`, and shell reads.
- Make file edits with `apply_patch`.
- Use `web.run` or a local fetch command for URLs when source content must be retrieved.
- Use `qmd query` / `qmd vsearch` from shell when the qmd MCP tool is unavailable.

## Process

### Step 0: Purpose Gate

Ask exactly one collection-purpose question before ingest:

> 미래의 내가 이 자료를 다시 볼 때 — 왜 수집했고, 어디에 쓸 예정인지 한 줄 남겨주세요. 재활용 축: (1) PhD (2) 학술 (3) 강의 (4) 컨설팅 (5) CMDS 시스템 (6) 에세이 (7) 제품.

If the user says to infer automatically, infer from the source plus [[Core Context]] and record the reasoning in `collectionPurpose`.

### Step 0-a: Mothership Links (mothership only)

Skip if no mothership vault is configured in [[Core Context]] §5. Otherwise search `{PATH_TO_YOUR_MOTHERSHIP_VAULT}` for 2-5 related notes. Prefer:

- `30. Permanent Notes/` essays
- MOCs or hub notes
- CMDS category pages
- Recent teaching/consulting notes when the purpose is 강의 or 컨설팅

**URL construction — MANDATORY validation** (do not hand-construct from memory):

1. Use the exact path `qmd`/`rg` returned — do not strip `.md` or add prefixes.
2. Percent-encode with a real encoder: `ENCODED=$(python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1], safe=''))" "<exact path>")` (`safe=''` encodes `/`, spaces, non-ASCII).
3. Stat before writing: `test -f "{PATH_TO_YOUR_MOTHERSHIP_VAULT}/<exact path>"` — if it fails, drop the candidate.
4. Construct `"[<label>](obsidian://open?vault={your-mothership-vault-name}&file=${ENCODED})"`.

**`mainVaultCmds` — authoritative list**: build the set with `find "{PATH_TO_YOUR_MOTHERSHIP_VAULT}" -maxdepth 3 -name "📚 [0-9][0-9][0-9] *.md" -type f` and pick an exact match. Leave empty rather than inventing a category.

Record the final, stat-verified links in `mainVaultRelated` and the best CMDS category in `mainVaultCmds`.

### Step 0.5: Format Conversion (binary → markdown)

If the source is a binary/non-markdown file (`.pdf`, `.pptx`, `.docx`, `.hwp`, `.epub`, `.html`, image, etc.), convert it to markdown first (an `omni-to-md` skill if available, or `markitdown`/`pandoc`/`hwp5txt`/`defuddle` directly). Move the original binary to `80. References/Attachments/` and carry `source-attachment`, `source-format`, `conversion-tool`, `conversion-date`, `conversion-fidelity` into the Raw Source. Audio (`.mp3`/`.wav`/`.m4a`) → an audio-transcription tool instead. The `## Original Content` section then holds the converted markdown.

### Step 1: Analyze

Extract key concepts, entities, guides, claims, contradictions, and related existing pages. Read `index.md` before creating pages and prefer updating existing pages.

### Step 2: Save Raw Source

Move inbox sources into the correct `10. Raw Sources/` subfolder. Preserve the original content verbatim under `## Original Content`.

Folder mapping:

- `00. Inbox/01. Articles/` -> `10. Raw Sources/11. Articles/`
- `00. Inbox/02. Papers/` -> `10. Raw Sources/12. Papers/`
- `00. Inbox/03. Transcripts/` -> `10. Raw Sources/14. Transcripts/`
- `00. Inbox/04. Clippings/` -> `10. Raw Sources/15. Clippings/`
- `00. Inbox/05. AI Research/` -> `10. Raw Sources/16. AI Research/`

Required raw-source fields:

```yaml
type: raw-source
aliases:
  - "{short name}"
description: "{English description}"
author:
  - "{author}"
date created: {today}
date modified: {today}
date ingested: {today}
tags:
  - raw-source
source: "{url-or-reference}"
category: "{Articles|Papers|Books|Transcripts|Clippings|AI Research}"
status: ingested
collectionPurpose: "{purpose}"
mainVaultRelated:
  - "[note](obsidian://open?vault={your-mothership-vault-name}&file=encoded-path)"
mainVaultCmds: "[[📚 NNN Category]]"
```

If the source came from `00. Inbox/`, delete the inbox original only after the raw source passes verbatim checks.

### Step 3: Compile Wiki Pages

Create or update 10-15 relevant Wiki pages when the source is substantial. New Wiki pages default to:

```yaml
explored: false
verificationStatus: unverified
```

Use `explored: true` only after a human or agent has completed the Exploration Gate check and documented it in the page body.

When possible, classify the page for later `/verify`:

```yaml
claimType: definition | empirical | theoretical | historical | prescriptive | interpretive | mixed
evidenceScope: single-source | multi-source-primary | multi-source-mixed | synthesis-only | user-original
```

For high-confidence or synthesis-heavy claims, add a bias check callout:

```markdown
> [!note] Bias Check
> Counter-argument: ...
> Data gap: ...
```

### Step 4: Connect

Add `[[wikilinks]]`, update relevant MOCs, and avoid orphan pages.

### Step 5: Update Index And Log

Update `index.md` stats and the Queries/Recent Ingests sections as needed. Append a `log.md` entry with source, purpose, pages created/updated, and mothership links.

### Step 6: Review

Verify `## Original Content`, inbox cleanup, wikilink targets, and qmd reindex status. Report open questions and any contradictions. Also run:

**Cross-vault link integrity (mothership only)** — mothership refs are invisible to Obsidian's graph. Stat-check every `obsidian://open?vault={your-mothership-vault-name}&file=...` URL in touched files against `{PATH_TO_YOUR_MOTHERSHIP_VAULT}`; fix or drop any broken path. Never leave a literal `URL_ENCODED_PATH` / `...`. Confirm each `mainVaultCmds` `[[📚 NNN ...]]` matches a live mothership category exactly (emoji included), and that no bare `[[mothership]]` wikilink appears in body text.

**Index sync verification** — for each new Wiki page, `rg -F "[[<newpage>]]" index.md` must find it in the Concepts/Entities/Guides/Maps section; Stats-table counts must match `find "20. Wiki/<subfolder>" -name "*.md" | wc -l`. Fix Step 5 before reporting done.

## Book Ingest Mode

For multi-page books/docs with 5+ chapters:

- Create one Book Index raw source.
- Create chapter stubs with `status: stub`, `bookIndex`, `chapterNumber`, `chapterPart`, `chapterPrev`, and `chapterNext`.
- Do not precompile chapter-specific Wiki pages.
- On later promotion, replace the stub `## Original Content`, set `status: completed`, compile chapter pages, and update the book progress table.
