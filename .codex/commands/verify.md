---
description: Verify a single Wiki page against eligibility, consistency, and confirmability; writes verificationStatus and queues disputed claims without deleting evidence.
---

# /verify — Codex Wiki Page Verification

Follow [[AGENTS.md]] and read [[Core Context]] once per session. This is the Codex mirror of `.claude/commands/verify.md`.

## Input

- Page name, e.g. `Agent Harness Design`
- Absolute path to a `.md` file
- `--latest` for the most recently modified Wiki page
- `--no-write-back` for read-only verification
- `--resolve` for a page currently marked `disputed: true`

## Quality Gates

1. **Eligibility**: subject, predicates, objects, source, evidence scope, and claim type are identifiable.
2. **Consistency**: claims align with cited Raw Sources, related Wiki pages, AGENTS.md policy, and [[Core Context]].
3. **Confirmability**: declared `confidence` matches evidence strength and counter-evidence.

## Process

1. Resolve the target page with `rg --files "20. Wiki"`, exact path lookup, or recent modified time.
2. Read the target page, `index.md`, [[Core Context]], and cited Raw Sources.
3. Classify `claimType` and `evidenceScope`.
4. Check concrete claims against Raw Source text with `rg`.
5. Search related Wiki pages with `rg`, `qmd query`, or `qmd vsearch`.
6. Flag conflicts as `disputed: true` with `> [!warning] Disputed Claim` callouts. Do not delete either side.
7. Calibrate `confidence` independently.
8. Draft or update `> [!note] Bias Check` when needed.
9. Unless `--no-write-back`, update v5 frontmatter:

```yaml
verificationStatus: verified | partial | unverified | disputed
verifiedAt: YYYY-MM-DD
verifiedBy: agent | human | both
claimType: definition | empirical | theoretical | historical | prescriptive | interpretive | mixed
evidenceScope: single-source | multi-source-primary | multi-source-mixed | synthesis-only | user-original
disputed: true
```

10. Flip `explored: true` only when the user explicitly confirms that the verification should count as explored.
11. Append `log.md`.

## Output

Print a concise verification report with eligibility, consistency, confirmability, recommended `confidence`, write-back actions, and follow-up `/verify` targets.
