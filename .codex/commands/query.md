---
description: Search the compiled Wiki, synthesize an answer, optionally save it under 30. Queries, and feed gaps back into the Wiki.
---

# /query — Codex LLM Wiki Query

Follow [[AGENTS.md]]. Read [[Core Context]] once per session before substantial query work.

## Process

### Step 1: Search

Read `index.md`, then search relevant Wiki pages with `rg`, `qmd query`, or `qmd vsearch`. Read the most relevant pages in full before answering.

### Step 2: Synthesize

Answer from compiled Wiki pages first, not raw-source sprawl. Cite with `[[wikilinks]]` in saved notes and mention source pages in the chat response.

### Step 3: Detect Gaps

Track:

- Missing pages that should exist
- Contradictions between pages
- Claims that need source strengthening
- Pages that need `mainVaultRelated`
- Pages that need `explored` or bias-check coverage
- Pages that are `verificationStatus: disputed` or overclaiming their `confidence`

### Step 4: Save When Substantial

Save substantial analysis as:

`30. Queries/YYYY-MM-DD-Q-{question-summary}.md`

Use `type: query-result`, English `description`, `source`, `reusableFor`, and `confidence`.

### Step 5: Feedback Into Wiki

When the query reveals durable improvements, update the relevant Wiki pages, MOCs, `index.md`, and `log.md`.

When citing Wiki pages in an answer, read `verificationStatus` and `confidence` together:

- `verified` + `high`: answer directly
- `partial` or `medium`: answer with appropriate hedging
- `unverified` or `low`: present as tentative
- `disputed`: name both sides and avoid collapsing the conflict

### Step 6: Reuse Axis

Close saved query notes with the most likely reuse axis:

`이 답변은 {axis}에 활용 가능합니다 — {one-sentence why}.`
