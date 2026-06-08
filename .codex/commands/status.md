---
description: Show the current state of the Wiki: counts, backlog, Core Context freshness, and major coverage signals.
---

# /status — Codex LLM Wiki Status

## Process

1. Read `index.md` stats.
2. Read the last 5 relevant entries from `log.md`.
3. Count actual files in Raw Sources, Wiki subfolders, Maps, Queries, and Inbox.
4. Check `collectionPurpose` coverage in Raw Sources.
5. Check `mainVaultRelated` coverage in Wiki pages.
6. Check `explored` coverage in Wiki pages.
7. Check `verificationStatus` coverage in Wiki pages.
8. Read `Core Context.md` `snapshot_date`.
9. Report index drift if actual counts differ from `index.md`.

## Output

```text
LLM Wiki Status
Raw Sources: {n}
Wiki Pages: {n}
Queries: {n}
Inbox: {n}
collectionPurpose: {n}/{N}
mainVaultRelated: {n}/{N}
explored: {n}/{N}
verificationStatus: {n}/{N}
Core Context: snapshot {date} ({days} days ago)
Issues: ...
```
