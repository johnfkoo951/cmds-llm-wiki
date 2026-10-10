---
name: "capture-tabs"
description: "Capture Chrome tab groups, browser research bundles, or ChatGPT/Gemini/Grok/Claude/Perplexity sessions into LLM Wiki Inbox markdown; also responds to 탭 캡처, 리서치 캡처, Deep Research 캡처, and /capture-tabs."
---

# capture-tabs

Use this skill when the user asks to collect browser tabs, Chrome tab groups, ChatGPT/Gemini/Grok/Claude/Perplexity conversations, or AI research sessions into the LLM Wiki Inbox.

## Command Template

Read `.codex/commands/capture-tabs.md` and follow it as the runtime entrypoint. Always read [[Core Context]] first.

## Tool Trigger

- This skill does not invoke Computer Use by name; it triggers from the user intent and metadata (`Chrome tab groups`, `browser research bundles`, `ChatGPT/Gemini/Grok/Perplexity sessions`).
- After the skill loads, `.codex/commands/capture-tabs.md` decides the tool path: use Computer Use for visible, account-bound Chrome tabs; use AppleScript or browser extraction when available; fall back to user-provided exports when UI extraction is blocked. Claude Code uses the mirrored `.claude/commands/capture-tabs.md` entrypoint.

## Non-Negotiables

- Preserve raw copied text under `## Original Content`.
- Put agent summaries, disagreements, and Wiki suggestions under `## Agent Capture Notes`; treat existing `## Codex Capture Notes` as legacy-compatible.
- Prefer one research-bundle note per topic or tab group.
- Record platform, URL, model/account/workspace when visible, capture method, and capture limitations.
- Do not create public share links, upload files, post messages, or modify account settings unless the user explicitly confirms at action time.
- Route substantial captures through `/inbox` or `/ingest` only after the collection-purpose gate.

## Related

- Codex command: `.codex/commands/capture-tabs.md`
- Claude command: `.claude/commands/capture-tabs.md`
- Inbox command: `.codex/commands/inbox.md`
- Ingest command: `.codex/commands/ingest.md`
- Claude inbox command: `.claude/commands/inbox.md`
- Claude ingest command: `.claude/commands/ingest.md`
- Template: `90. Settings/Templates/Template_AI Research Capture.md`
