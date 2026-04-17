---
description: Show wiki state at a glance — counts, recent activity, index drift, inbox backlog, collectionPurpose coverage, Core Context snapshot age.
allowed-tools: Read, Glob, Grep, Bash
---

# /status — LLM Wiki Status

Show the current state of the wiki at a glance.

## Process

1. Read `index.md` for the Stats table and page catalog
2. Read `log.md` for the last 5 operations
3. Count actual files:
   - `10. Raw Sources/**/*.md` → raw source count
   - `20. Wiki/21. Concepts/*.md` → concept count
   - `20. Wiki/22. Entities/*.md` → entity count
   - `20. Wiki/23. Guides/*.md` → guide count
   - `20. Wiki/24. Maps/*.md` → MOC count
   - `30. Queries/*.md` → query count
   - `00. Inbox/**/*` → pending inbox items (scan all subfolders)
4. Check for discrepancies between index.md counts and actual counts
5. **Coverage check**: grep `^collectionPurpose:` across `10. Raw Sources/**/*.md` → coverage % (미래의 나에게 보내는 편지)
6. **Core Context age**: read `Core Context.md` frontmatter `snapshot_date` → days since snapshot

## Output

```
📊 LLM Wiki Status
──────────────────────────
Raw Sources:  {n}    (collectionPurpose coverage: {n/N} = {pct}%)
Wiki Pages:   {n} (Concepts: {n}, Entities: {n}, Guides: {n})
MOCs:         {n}
Queries:      {n}    (filed-back ratio: {queries}/{wiki} = {pct}%)
Inbox:        {n} pending

🧭 Core Context: snapshot {snapshot_date} ({n} days ago)
──────────────────────────
📥 Recent Activity (last 5)
- {date} [{operation}] {description}
- ...
──────────────────────────
⚠️  Issues (if any)
- Index out of sync: {details}
- Orphan pages: {count}
- Inbox items waiting: {count}
- collectionPurpose missing: {count} raw sources (run /lint for details)
- Core Context > 30 days old: suggest /refresh-context
```
