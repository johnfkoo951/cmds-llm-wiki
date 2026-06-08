---
name: "lint"
description: "Run the LLM Wiki health check: orphans, broken links, contradictions, stale pages, index sync, MOC coverage, frontmatter fields, Exploration Gate, v5 verification fields, Bias Check, cross-vault links, and Core Context freshness; also responds to /lint and 위키 점검."
---

# lint

Use this skill when the user asks to run `lint`, `/lint`, "위키 점검", or a comprehensive LLM Wiki health check.

## Command Template

# /lint — LLM Wiki Lint / Health Check

Run a comprehensive health check on the LLM Wiki. Follow AGENTS.md rules strictly.

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

### Step 8: v2/v4 Frontmatter Coverage (2026-04-14+ / 2026-05-04+)

Check the 미래의 나에게 보내는 편지 fields introduced with [[Core Context]]:
- **Raw Sources**: every file in `10. Raw Sources/` should have `collectionPurpose`, `mainVaultRelated`, `mainVaultCmds`
	- Missing `collectionPurpose` → flag as "pre-v2 raw source — consider backfill"
	- Report % coverage (e.g., "5/13 raw sources have collectionPurpose = 38%")
- **Wiki pages**: recent pages (post 2026-04-14) should have `mainVaultRelated`
- **Attachment location**: any `![...](...)` or `![[...]]` in Wiki pages pointing outside `80. References/Attachments/` → flag
- **Exploration Gate**: every Wiki page should have `explored: true|false`
	- Missing `explored` → flag as "pre-v4 page — add `explored: false` during next touch"
	- `explored: false` → count as review backlog, not an error
	- `explored: true` without `exploredBy` or `exploredDate` → flag as incomplete review metadata
- **v5 verification fields**: every Wiki page should eventually have `claimType`, `evidenceScope`, `verificationStatus`
	- Missing fields → flag as "pre-v5 page — route through `/verify` when touched"
	- `verificationStatus: disputed` → include in high-priority `/verify --resolve` queue
- **Bias check**: high-confidence Wiki pages and synthesis-heavy guides should include `> [!note] Bias Check`
	- Missing bias check → flag as "quality-control gap"
	- Bias callout must include `Counter-argument:` and `Data gap:`

### Step 9: Core Context Freshness

Read `Core Context.md` frontmatter `snapshot_date`. Compare with max `date modified` of mothership 9 system files:
- `{your-mothership-vault-name}/CLAUDE.md`, `AGENTS.md`, `ANTIGRAVITY.md`, `CMDS.md`, `🏛 CMDS Guide.md`, `🏛 CMDS Head Quarter.md`, `BRAIN.md`, `BRAIN_PROMPT.md`, `DESIGN.md`

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
8. **v4 Quality Coverage**: `explored` / Bias Check coverage %
9. **v5 Verification Coverage**: `claimType` / `evidenceScope` / `verificationStatus` coverage %
10. **Cross-Vault Links**: `mainVaultRelated` URL and `mainVaultCmds` format issues
11. **Core Context**: snapshot age + mothership drift
12. **Recommendations**: suggested improvements
