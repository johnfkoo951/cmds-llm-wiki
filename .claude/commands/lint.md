---
description: Run comprehensive wiki health check — orphans, broken links, contradictions, stale pages, index sync, MOC coverage, v2/v4/v5 frontmatter coverage, Core Context freshness, and cross-vault link integrity (mainVaultRelated/mainVaultCmds).
allowed-tools: Read, Edit, Glob, Grep, Bash, mcp__qmd__query
# Antigravity equivalents: view_file, write_to_file, replace_file_content, list_dir, grep_search, run_command
---

# /lint — LLM Wiki Lint / Health Check

Run a comprehensive health check on the LLM Wiki. Follow CLAUDE.md rules strictly.

> **🧭 Prerequisite**: Read [[Core Context]] once per session — needed for snapshot staleness check (§8).

## Process

### Step 1: Inventory

Read `index.md` to get the current wiki catalog. Then scan actual files:
- Glob `20. Wiki/**/*.md` for all wiki pages (in 21-24 subfolders)
- Glob `10. Raw Sources/**/*.md` for all raw sources (in 11-16 subfolders)
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

### Step 8: v2/v4/v5 Frontmatter Coverage

Check the 미래의 나에게 보내는 편지 fields introduced with [[Core Context]]:
- **Raw Sources**: every file in `10. Raw Sources/` should have `collectionPurpose`, `mainVaultRelated`, `mainVaultCmds`
	- Missing `collectionPurpose` → flag as "pre-v2 raw source — consider backfill"
	- Report % coverage (e.g., "5/13 raw sources have collectionPurpose = 38%")
- **Wiki pages**: recent pages should have `mainVaultRelated` (if mothership configured)
- **Attachment location**: any `![...](...)` or `![[...]]` in Wiki pages pointing outside `80. References/Attachments/` → flag
- **Exploration Gate (v4)**: every Wiki page should have `explored: true|false`
	- Missing `explored` → flag as "pre-v4 page — add `explored: false` during next touch"
	- `explored: false` → count as review backlog, not an error
	- `explored: true` without `exploredBy` or `exploredDate` → flag as incomplete review metadata
- **Bias check (v4)**: high-confidence Wiki pages and synthesis-heavy guides should include `> [!note] Bias Check`
	- Missing bias check → flag as "quality-control gap"
	- Bias callout must include `Counter-argument:` and `Data gap:`
- **v5 verification fields**: every Wiki page should eventually have `claimType`, `evidenceScope`, `verificationStatus`
	- Missing fields → flag as "pre-v5 page — route through `/verify` when touched"
	- `verificationStatus: disputed` → include in high-priority `/verify --resolve` queue

### Step 9: Core Context Freshness

Read `Core Context.md` frontmatter `snapshot_date`. If §5 has mothership system files registered, compare `snapshot_date` with max `date modified` of those registered files.

If mothership files changed AFTER `snapshot_date` (or `snapshot_date` > 30 days old): suggest running `/refresh-context`.

### Step 10: Cross-Vault Link Check (mothership only)

> **Only runs if a mothership vault is configured** in Core Context §5. If you run this LLM Wiki standalone, skip this step.

Cross-vault references — `mainVaultRelated` (obsidian:// URLs) and `mainVaultCmds` (`"[[📚 NNN ...]]"` quoted wikilinks) — point into the mothership vault and cannot be validated by Obsidian's graph or by the Step 3 wikilink check. This step stat-checks them against the mothership filesystem. Set `MOTHERSHIP` / vault name to your own values before running.

**10.1 Broken `mainVaultRelated` URLs**

Scan all `.md` files in `10. Raw Sources/` + `20. Wiki/`. For each `mainVaultRelated:` entry:

```python
# python3 inline (macOS has python3 by default)
import os, re, urllib.parse, glob

MOTHERSHIP = "{PATH_TO_YOUR_MOTHERSHIP_VAULT}"
VAULT_NAME = "{your-mothership-vault-name}"
URL_RE = re.compile(r'obsidian://open\?vault=' + re.escape(VAULT_NAME) + r'&file=([^)"\s]+)')

broken = []
for f in glob.glob("20. Wiki/**/*.md", recursive=True) + \
         glob.glob("10. Raw Sources/**/*.md", recursive=True):
    with open(f, encoding="utf-8") as fh:
        text = fh.read()
    text = re.sub(r'```.*?```', '', text, flags=re.S)  # exclude fenced code blocks
    text = re.sub(r'`[^`\n]*`', '', text)              # and inline code spans — doc examples (e.g. file=URL_ENCODED_PATH) are not real links
    for m in URL_RE.finditer(text):
        encoded = m.group(1)
        decoded = urllib.parse.unquote(encoded)
        # Try with and without .md suffix; mothership paths sometimes include it
        candidates = [
            os.path.join(MOTHERSHIP, decoded),
            os.path.join(MOTHERSHIP, decoded + ".md"),
            os.path.join(MOTHERSHIP, decoded.rstrip(".md") + ".md"),
        ]
        if not any(os.path.isfile(c) for c in candidates):
            broken.append((f, decoded))

for src, target in broken:
    print(f"BROKEN  {src}  →  {target}")
```

Output rows: source file (in this vault), broken target path (in mothership).

**10.2 Broken `mainVaultCmds` categories**

Build the authoritative mothership category set, then check each Wiki/Raw Source `mainVaultCmds` against it. **Must strip pipe-aliases** (`[[📚 501 Obsidian|Obsidian]]` → check `📚 501 Obsidian`) before lookup.

```python
import os, re, glob
MOTHERSHIP = "{PATH_TO_YOUR_MOTHERSHIP_VAULT}"

# Authoritative mothership category set (folder note files named "📚 NNN ...")
auth = set()
for root, dirs, files in os.walk(MOTHERSHIP):
    depth = root[len(MOTHERSHIP):].count(os.sep)
    if depth > 3: dirs[:] = []; continue
    for fn in files:
        if fn.startswith("📚 ") and fn.endswith(".md"):
            auth.add(fn[:-3])

# Extract refs, stripping pipe aliases
CMDS_RE = re.compile(r'\[\[(📚 [0-9]{3}[^|\]]+)(?:\|[^\]]+)?\]\]')
broken = {}
for f in glob.glob("20. Wiki/**/*.md", recursive=True) + \
         glob.glob("10. Raw Sources/**/*.md", recursive=True):
    with open(f, encoding="utf-8") as fh:
        for m in CMDS_RE.finditer(fh.read()):
            ref = m.group(1).rstrip()
            if ref not in auth:
                broken.setdefault(ref, []).append(f)

# Suggest renames via prefix match (📚 NNN ...)
for ref in broken:
    prefix = ref[:7]  # "📚 NNN "
    candidates = [a for a in auth if a.startswith(prefix)]
    # report ref + occurrences + top candidate
```

Output: list of broken category refs + occurrence count + suggested rename (top prefix match if any). Pipe-alias-stripped before lookup.

**10.3 Auto-fix suggestion (READ-ONLY by default)**

For each broken link found in 10.1 / 10.2:

1. Run `mcp__qmd__query` against mothership with the decoded label / category name to find renamed equivalents
2. Present 1-3 suggested replacements per broken link
3. **Do NOT auto-patch** — print the proposed Edit commands for the user to confirm

Auto-apply mode (`/lint --fix-crossvault`):
- Apply the top-1 suggestion ONLY when the user explicitly invokes the flag
- Even then, the LLM emits a diff preview and requires "ok" before each batch of 10 edits

## Output

Report in this format:
1. **Stats**: total pages, sources, MOCs
2. **Orphans**: pages with no inbound links
3. **Broken Links**: wikilinks pointing to nothing (same-vault)
4. **Contradictions**: flagged conflicts
5. **Stale Pages**: potentially outdated content
6. **Index Issues**: sync problems found and fixed
7. **v2 Coverage**: `collectionPurpose` / `mainVaultRelated` coverage %
8. **v4 Quality Coverage**: `explored` / Bias Check coverage %
9. **v5 Verification Coverage**: `claimType` / `evidenceScope` / `verificationStatus` coverage %
10. **Core Context**: snapshot age + mothership drift
11. **Cross-Vault Integrity**: broken `mainVaultRelated` URLs (count + sample), broken `mainVaultCmds` categories (count + sample), suggested fixes per broken link (mothership only)
12. **Recommendations**: suggested improvements (top 10 actions)
