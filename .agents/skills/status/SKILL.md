---
name: "status"
description: "Show the LLM Wiki state at a glance: counts, recent activity, index drift, inbox backlog, collectionPurpose/mainVault/explored/verificationStatus coverage, and Core Context snapshot age; also responds to /status and 상태 점검."
---

# status

Use this skill when the user asks to run `status`, `/status`, "상태 점검", or a quick LLM Wiki status report.

## Command Template

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
   - `20. Wiki/25. Questions/*.md` → research question count
   - `30. Queries/*.md` → query count
   - `40. Paper Analyses/*/` → paper analysis count (citekey folders = hubs)
   - `00. Inbox/**/*` → pending inbox items (scan all subfolders)
4. Check for discrepancies between index.md counts and actual counts
5. **Coverage check**: grep `^collectionPurpose:` across `10. Raw Sources/**/*.md` → coverage % (미래의 나에게 보내는 편지)
6. **Cross-vault check**: grep `^mainVaultRelated:` across `20. Wiki/**/*.md` → coverage %
7. **Exploration Gate check**: grep `^explored:` across `20. Wiki/**/*.md` → coverage %
8. **Verification check**: grep `^verificationStatus:` across `20. Wiki/**/*.md` → coverage %
9. **Core Context age**: read `Core Context.md` frontmatter `snapshot_date` → days since snapshot

## Output

```
📊 LLM Wiki Status
──────────────────────────
Raw Sources:  {n}    (collectionPurpose coverage: {n/N} = {pct}%)
Wiki Pages:   {n} (Concepts: {n}, Entities: {n}, Guides: {n})
MOCs:         {n}
Queries:      {n}    (filed-back ratio: {queries}/{wiki} = {pct}%)
Inbox:        {n} pending
mainVault*:   {n/N} wiki pages = {pct}%
explored:     {n/N} wiki pages = {pct}%
verified:     {n/N} wiki pages have verificationStatus = {pct}%

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
- Exploration Gate missing: {count} wiki pages (run /lint for backlog)
- Verification fields missing: {count} wiki pages (run /audit or /verify for queue)
- Core Context > 30 days old: suggest /refresh-context
```
