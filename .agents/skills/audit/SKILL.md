---
name: "audit"
description: "Audit the whole LLM Wiki or one MOC cluster for eligibility, consistency, and confirmability; also responds to /audit, 전체 검증, and 볼트 감사."
---

# audit

Use this skill when the user asks for a whole-vault audit, MOC-level audit, confidence audit, or `/audit`.

## Command Template

Read `.codex/commands/audit.md` and follow it as the runtime entrypoint. Always read [[Core Context]] first.

## Non-Negotiables

- Audit is read-only on Wiki pages; page mutations happen through later `/verify`.
- Use MOC clusters for consistency checks.
- Prioritize high-confidence, stale unexplored, disputed, and sampled pages.
- Save substantial audit reports to `30. Queries/` unless the user asks for `--no-save`.
- Output a Top 10 `/verify` queue.

## Related

- Codex command: `.codex/commands/audit.md`
- Claude mirror: `.claude/commands/audit.md`
- Verify command: `.codex/commands/verify.md`
