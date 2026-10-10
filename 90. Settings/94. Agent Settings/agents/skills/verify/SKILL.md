---
name: "verify"
description: "Verify one LLM Wiki page against eligibility, consistency, and confirmability; also responds to /verify, 페이지 검증, and 단일 페이지 검증."
---

# verify

Use this skill when the user asks to verify a Wiki page, run `/verify`, resolve a disputed page, or check whether a page's confidence is justified.

## Command Template

Read `.codex/commands/verify.md` and follow it as the runtime entrypoint. Always read [[Core Context]] first.

## Non-Negotiables

- Conflicts are flagged as `disputed`, not deleted.
- Check concrete claims against Raw Source text when possible.
- Calibrate `confidence` independently from declared frontmatter.
- Add or update `> [!note] Bias Check` for high-confidence pages when missing.
- Do not flip `explored: true` without explicit user confirmation.

## Related

- Codex command: `.codex/commands/verify.md`
- Claude mirror: `.claude/commands/verify.md`
- Audit command: `.codex/commands/audit.md`
