---
name: "query"
description: "Search compiled LLM Wiki pages, synthesize a cited answer, save substantial results, and feed durable gaps back into the Wiki; also responds to /query and 위키 질의."
---

# query

Use this skill when the user asks `/query` or requests a substantial synthesis from the LLM Wiki.

## Command Template

Read `.codex/commands/query.md` and follow it as the runtime entrypoint. Always read [[Core Context]] first for substantial queries.

## Non-Negotiables

- Search compiled Wiki pages before raw sources.
- Read relevant pages in full before synthesis.
- Save substantial answers under `30. Queries/`.
- Add `reusableFor` when saving.
- Feed durable gaps, contradictions, and cross-links back into Wiki pages.
- Record quality-control gaps: missing `mainVaultRelated`, missing `explored`, or missing Bias Check.

## Related

- Codex command: `.codex/commands/query.md`
- Claude mirror: `.claude/commands/query.md`
