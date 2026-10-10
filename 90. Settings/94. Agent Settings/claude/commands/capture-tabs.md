---
description: Capture a Chrome research tab group or AI-chat research session into LLM Wiki Inbox markdown, then optionally route it through /inbox or /ingest.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
# Antigravity equivalents: view_file, write_to_file, replace_file_content, list_dir, grep_search, run_command
---

# /capture-tabs — Claude AI Research Capture

Follow [[CLAUDE.md]] and read [[Core Context]] once per session. This command is the Claude mirror of `.codex/commands/capture-tabs.md`; it is a pre-ingest capture layer for research gathered through ChatGPT, Gemini, Grok, Claude, Perplexity, and adjacent source tabs.

## Purpose

Use this command when the user has a Chrome tab group or browser session containing AI-assisted preliminary research and wants it preserved as Markdown in `00. Inbox/` before full `/ingest`.

The default output is one research-bundle note:

`00. Inbox/05. AI Research/YYYY-MM-DD-ai-research-{topic-slug}.md`

Use `00. Inbox/04. Clippings/` only for short excerpts, social posts, or a manifest-only capture without substantial conversation text.

## Capture Principles

1. Preserve evidence before synthesis.
2. Keep raw copied transcript under `## Original Content`.
3. Put Claude interpretation under `## Agent Capture Notes`, never inside `## Original Content`.
4. Treat existing `## Codex Capture Notes` sections as legacy-compatible agent notes.
5. Record source URLs, platform names, visible model names, capture method, and capture limitations.
6. Do not create public share links, post messages, upload files, or change account settings unless the user explicitly asks and confirms at action time.

## Tool Choice

Prefer the least lossy available path:

1. Existing Chrome tab group:
	- If Claude Code can read browser metadata non-destructively, first collect tab titles and URLs.
	- If a browser/computer-use surface is available, use it only for reading, selecting, copying, scrolling, or exporting visible content.
	- If account-bound ChatGPT/Gemini/Grok/Claude tabs cannot be controlled, ask the user to paste or export the conversation text.
2. Normal URL or local file:
	- Use available URL/file reading tools when the target can be opened independently without the user's live Chrome session.
3. Fallback:
	- Ask the user to copy conversation text or export/download a conversation, then capture the pasted/local file content into the Inbox template.

## Process

### Step 0: Scope

Resolve these fields from the user's prompt or the visible browser session:

- `topic`: the research topic or tab-group name
- `platforms`: ChatGPT, Gemini, Grok, Claude, Perplexity, and any source sites
- `captureMode`: `transcript`, `manifest-only`, `curated-excerpts`, or `mixed`
- `nextStep`: `inbox-only`, `run-inbox`, or `ingest-now`
- `collectionPurpose`: one of the 7 reuse axes, if already known

If the topic or target tab group is ambiguous, ask one concise question before operating Chrome.

### Step 1: Read Tab Metadata

Capture a manifest table with:

- platform
- title
- URL
- visible model/account/workspace if relevant
- role in research, such as "question answering", "counterpoint", "source evidence", or "follow-up"

### Step 2: Extract Conversation Or Page Text

For each selected tab:

1. Prefer built-in copy/export controls when they produce local text without creating a public link.
2. If allowed and available, use browser/Chrome text extraction for page text.
3. If UI extraction is the only path, select/copy visible conversation text without sending new messages.
4. Record gaps, truncation, hidden collapsed answers, failed extraction, or paywalled/auth-only content.

### Step 3: Create Inbox Note

Use `90. Settings/Templates/Template_AI Research Capture.md` as the shape.

Required frontmatter fields for generated capture notes:

```yaml
type: "inbox"
category:
  - "AI Research"
clip_type: "ai-research-tab-group"
source_url:
  - "{primary-url-or-conversation-url}"
platforms:
  - "ChatGPT"
capture_method: "browser-ui-or-manual-export"
capture_status: "captured"
captureMode: "mixed"
description: "English one-sentence description of the captured research bundle."
author:
  - "[[{your-name}]]"
  - Claude
date created: YYYY-MM-DD
date modified: YYYY-MM-DD
date_clipped: YYYY-MM-DD
tags:
  - inbox
  - agent-capture
  - ai-research
```

### Step 4: Add Capture Notes

Under `## Agent Capture Notes`, add:

- one-paragraph topic summary
- key claims by platform
- source URLs mentioned by the models
- disagreements between platforms
- missing evidence or follow-up questions
- suggested Wiki pages to create/update during `/ingest`

### Step 5: Route

- `inbox-only`: stop after writing the Inbox note and report the file path.
- `run-inbox`: run `.claude/commands/inbox.md` on the new file.
- `ingest-now`: run `.claude/commands/ingest.md` after the collection-purpose gate and mothership link search.

## Verification

Before reporting success:

1. Confirm the generated `.md` file exists under `00. Inbox/05. AI Research/` or `00. Inbox/04. Clippings/`.
2. Confirm it has a non-empty `## Original Content` section or is explicitly marked `captureMode: manifest-only`.
3. Confirm source URLs are present.
4. Confirm agent synthesis is separated from raw content.
5. If the next step is ingest, confirm `/ingest` preserved the raw source before deleting any Inbox original.
