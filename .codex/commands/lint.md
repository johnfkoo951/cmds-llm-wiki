---
description: Run Codex-compatible health checks for the LLM Wiki, including schema, links, cross-vault fields, Exploration Gate, v5 verification fields, and Core Context freshness.
---

# /lint — Codex LLM Wiki Health Check

Follow [[AGENTS.md]] and read [[Core Context]] first. The local skill `.agents/skills/lint/SKILL.md` is the detailed companion spec; this command is the Codex entrypoint.

## Checks

1. Inventory `10. Raw Sources/**/*.md`, `20. Wiki/**/*.md`, `30. Queries/**/*.md`, `index.md`, and `log.md`.
2. Compare actual counts with `index.md`.
3. Find orphan Wiki pages by collecting inbound `[[wikilinks]]`.
4. Find broken wikilinks.
5. List `> [!warning] Contradiction` callouts.
6. Flag low-confidence pages not updated in 30+ days.
7. Check MOC coverage.
8. Check raw-source `collectionPurpose`, `mainVaultRelated`, and `mainVaultCmds`.
9. Check Wiki-page `mainVaultRelated` and `mainVaultCmds`.
10. Check `explored` coverage and list pages missing the property.
11. Check v5 verification coverage: `claimType`, `evidenceScope`, `verificationStatus`, `verifiedAt`, `verifiedBy`, `disputed`.
12. Check bias coverage for high-confidence pages and synthesis-heavy guides.
13. Check cross-vault links: `mainVaultRelated` Obsidian URLs and `mainVaultCmds` format.
14. Check attachment paths against `80. References/Attachments/`.
15. Check `Core Context.md` `snapshot_date` against current date and the 9 mothership system files: `CLAUDE.md`, `AGENTS.md`, `ANTIGRAVITY.md`, `CMDS.md`, `🏛 CMDS Guide.md`, `🏛 CMDS Head Quarter.md`, `BRAIN.md`, `BRAIN_PROMPT.md`, `DESIGN.md`.

## Output

Report:

- Stats
- Orphans
- Broken links
- Contradictions
- Stale pages
- Index issues
- v2 field coverage
- Exploration Gate coverage
- v5 verification coverage
- Bias-check coverage
- Cross-vault link integrity
- Core Context freshness
- Recommended fixes, ordered by impact and effort
