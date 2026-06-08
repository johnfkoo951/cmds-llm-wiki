---
name: "ingest"
description: "Ingest a URL, file, raw text, or Inbox item into the LLM Wiki with the purpose gate, mothership link search, raw-source preservation, Wiki compilation, index/log update, and review; also responds to /ingest and 인제스트."
---

# ingest

Use this skill when the user asks to run `/ingest` or to ingest a URL, file, raw text, or Inbox item into the LLM Wiki.

## Command Template

Read `.codex/commands/ingest.md` and follow it as the runtime entrypoint. Always read [[Core Context]] first.

## Non-Negotiables

- Ask the collection-purpose question unless the user explicitly asked you to infer it.
- Search the mothership vault for 2-5 `mainVaultRelated` candidates.
- Preserve raw source body verbatim under `## Original Content`.
- Move Inbox files only after preservation checks pass.
- New Wiki pages get `explored: false`.
- High-confidence or synthesis-heavy pages get a `> [!note] Bias Check` callout.
- Update `index.md` and `log.md`.

## Related

- Codex command: `.codex/commands/ingest.md`
- Claude mirror: `.claude/commands/ingest.md`
- Hooks: `.codex/hooks/validate-raw-source.sh`, `.codex/hooks/qmd-reindex.sh`
