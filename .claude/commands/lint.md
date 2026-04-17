---
description: Run comprehensive wiki health check — orphans, broken links, contradictions, stale pages, index sync, MOC coverage, v2 frontmatter fields, and Core Context freshness.
allowed-tools: Read, Edit, Glob, Grep, Bash
---

# /lint — LLM Wiki Lint / Health Check

Run a comprehensive health check on the LLM Wiki. Follow CLAUDE.md rules strictly.

> **🧭 Prerequisite**: Read [[Core Context]] once per session — needed for snapshot staleness check (§8).

## Process

### Step 1: Inventory

Read `index.md` to get the current wiki catalog. Then scan actual files:
- Glob `20. Wiki/**/*.md` for all wiki pages (in 21-24 subfolders)
- Glob `10. Raw Sources/**/*.md` for all raw sources (in 11-15 subfolders)
- Compare index.md entries with actual files

### Step 2: Orphan Check

Find wiki pages that have **no inbound links** from any other wiki page or MOC.
- Read each wiki page and collect all `[[wikilinks]]`
- Pages with zero inbound links = orphans
- Suggest: link from relevant MOC or related page

### Step 3: Broken Link Check

Find `[[wikilinks]]` that point to **non-existent pages**.
- For each: decide whether to create the page or remove/fix the link

### Step 4: Contradiction Check

Scan wiki pages for `> [!warning] Contradiction` callouts.
- List all existing contradictions
- Check if any have been resolved by newer sources

### Step 5: Staleness Check

Check `date modified` on all wiki pages.
- Pages not updated in 30+ days with `confidence: low` → flag as potentially stale

### Step 6: Index Sync

Verify `index.md` matches actual wiki structure:
- Missing entries → add
- Entries for deleted pages → remove
- Stats table accurate → update counts

### Step 7: MOC Coverage

Check that every wiki page belongs to at least one MOC.
- Pages without MOC coverage → suggest which MOC to add them to

### Step 8: v2 Frontmatter Coverage (2026-04-14+)

Check the 미래의 나에게 보내는 편지 fields introduced with [[Core Context]]:
- **Raw Sources**: every file in `10. Raw Sources/` should have `collectionPurpose`, `mainVaultRelated`, `mainVaultCmds`
  - Missing `collectionPurpose` → flag as "pre-v2 raw source — consider backfill"
  - Report % coverage (e.g., "5/13 raw sources have collectionPurpose = 38%")
- **Wiki pages**: recent pages (post 2026-04-14) should have `mainVaultRelated`
- **Attachment location**: any `![...](...)` or `![[...]]` in Wiki pages pointing outside `80. References/Attachments/` → flag

### Step 9: Core Context Freshness

Read `Core Context.md` frontmatter `snapshot_date`. If §5 has mothership system files registered, compare `snapshot_date` with max `date modified` of those registered files.

If mothership files changed AFTER `snapshot_date` (or `snapshot_date` > 30 days old): suggest running `/refresh-context`.

## Output

Report in this format:
1. **Stats**: total pages, sources, MOCs
2. **Orphans**: pages with no inbound links
3. **Broken Links**: wikilinks pointing to nothing
4. **Contradictions**: flagged conflicts
5. **Stale Pages**: potentially outdated content
6. **Index Issues**: sync problems found and fixed
7. **v2 Coverage**: `collectionPurpose` / `mainVaultRelated` coverage %
8. **Core Context**: snapshot age + mothership drift
9. **Recommendations**: suggested improvements
