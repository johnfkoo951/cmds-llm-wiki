---
description: Refresh Core Context.md from the 9 mothership system files and key essays when snapshot drift is detected.
---

# /refresh-context — Codex Core Context Refresh

Use when `/lint` or `/status` flags Core Context age or mothership drift.

## Process

1. Read current [[Core Context]] frontmatter and sections for identity, reuse axes, system files, and philosophy.
2. Re-read mothership system files:
	- `{PATH_TO_YOUR_MOTHERSHIP_VAULT}/CLAUDE.md`
	- `{PATH_TO_YOUR_MOTHERSHIP_VAULT}/AGENTS.md`
	- `{PATH_TO_YOUR_MOTHERSHIP_VAULT}/ANTIGRAVITY.md`
	- `{PATH_TO_YOUR_MOTHERSHIP_VAULT}/CMDS.md`
	- `{PATH_TO_YOUR_MOTHERSHIP_VAULT}/🏛 CMDS Guide.md`
	- `{PATH_TO_YOUR_MOTHERSHIP_VAULT}/🏛 CMDS Head Quarter.md`
	- `{PATH_TO_YOUR_MOTHERSHIP_VAULT}/BRAIN.md`
	- `{PATH_TO_YOUR_MOTHERSHIP_VAULT}/BRAIN_PROMPT.md`
	- `{PATH_TO_YOUR_MOTHERSHIP_VAULT}/DESIGN.md`
3. Re-read the key essays listed in [[Core Context]] `source`.
4. Scan recent Permanent Notes for major philosophy drift.
5. Propose a concise diff before applying major semantic changes.
6. If approved or explicitly requested, update [[Core Context]], bump `snapshot_date`, update `date modified`, and append `log.md`.

## Output

Report snapshot age, drift sources, sections changed, essays added, and version bump.
