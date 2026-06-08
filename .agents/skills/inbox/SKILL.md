---
name: "inbox"
description: "Scan the LLM Wiki 00. Inbox, preview pending files, choose scope/purpose mode, and route selected material through ingest; also responds to /inbox and 인박스 점검."
---

# inbox

Use this skill when the user asks `/inbox`, asks what is waiting in Inbox, or asks to ingest pending Inbox material.

## Command Template

Read `.codex/commands/inbox.md` and follow it as the runtime entrypoint. Always read [[Core Context]] first.

## Non-Negotiables

- Scan all `00. Inbox/` subfolders unless the user narrows scope.
- Present counts and a compact preview.
- Ask scope and purpose mode in one turn.
- Route selected files through `/ingest`.
- Delete processed Inbox originals only after raw-source preservation checks pass.

## Related

- Codex command: `.codex/commands/inbox.md`
- Claude mirror: `.claude/commands/inbox.md`
