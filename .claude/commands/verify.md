---
description: Verify a single Wiki page against 3 knowledge-integrity criteria — eligibility, consistency, confirmability. Writes verificationStatus back to the page; flags conflicts as disputed rather than deleting them.
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, mcp__qmd__query
# Antigravity equivalents: view_file, replace_file_content, write_to_file, list_dir, grep_search, run_command
---

# /verify — Wiki Page Verification

Verify that one Wiki page meets quality requirements as an LLM Wiki knowledge unit. Follow CLAUDE.md rules strictly (YAML: 2 spaces, Body: TAB, wikilinks in YAML quoted).

> **🧭 Prerequisite**: Read [[Core Context]] once per session — needed for Phase 2.4 alignment against user's 7 reuse axes.

## Input

`$ARGUMENTS` (Claude Code) / `User Request` (Antigravity)

- Page name (e.g., "Agent Harness Design") — resolve via `Glob "20. Wiki/**/{name}*.md"`
- Or absolute path to a `.md` file
- Or `--latest` to verify the most recently modified Wiki page
- Optional `--no-write-back` flag — read-only verification, no frontmatter change
- Optional `--resolve` flag — for a page currently `disputed: true`, attempt resolution

## Conceptual Framework — 3 Quality Gates

### 1. 지식요건해당성 (Eligibility) — Does it meet formal requirements?

Every Wiki page must expose **Subject · Predicates · Objects · Source · Evidence Scope · Claim Type**:

- **Subject (주어)** — page title is a well-defined entity / concept / topic
- **Predicates (술어)** — H2 sections name what the subject *is, does, relates to*
- **Objects (객체)** — claims inside sections are specific assertions
- **Source (출처)** — claims trace to `source:` Raw Source(s) OR `mainVaultRelated` (user-original)
- **Evidence Scope (증거 범위)** — declarable as one of 5 levels (below)
- **Claim Type** — declarable as one of 6 types (below)

### 2. 정합성 (Consistency) — Does it conflict with the knowledge order?

Four reference frames:

- **vs source** — claims actually supported by cited Raw Source verbatim (anti-hallucination)
- **vs other Wiki pages** — no cross-page contradictions
- **vs CLAUDE.md policies** — layer / naming / frontmatter conventions
- **vs Core Context** — connected to ≥1 of the user's 7 reuse axes

> **Conflicts are flagged `disputed`, not deleted.** Both sides preserved with cross-link callouts until new evidence resolves the conflict. Deletion is a last resort reserved for verifiable factual errors (e.g., hallucinated number with no source support).

### 3. 확증가능성 (Confirmability) — How strong is the evidence?

Compute confidence **independently** of the declared `confidence:` field:

- Count sources, classify primary / secondary / user-original
- Search Wiki for counter-evidence
- Detect overclaim (high-confidence + single source) and underclaim (low-confidence + multiple primary sources)
- Generate Bias Check counter-arguments if missing

The output of this phase determines **how strongly /query may speak about this page's claims**.

### Claim Type Taxonomy (6 types)

| Type | Definition | Example |
|------|-----------|---------|
| `definition` | What X *is* | "Agent Harness is the scaffolding around an LLM" |
| `empirical` | Measurable fact | "Opus 4.6 BrowseComp = 61.6%" |
| `theoretical` | Framework, pattern, hypothesis | "Lance Martin's 3 design principles" |
| `historical` | Event, timeline, attribution | "2026-04-08 Anthropic launched Managed Agents" |
| `prescriptive` | How-to, recommendation, norm | "Always ask 'what can I stop doing?'" |
| `interpretive` | Synthesis, opinion, judgment | "Harness assumptions grow stale as models improve" |

Use `mixed` when ≥3 types present.

### Evidence Scope Levels (5)

| Scope | Meaning |
|-------|---------|
| `single-source` | One Raw Source backs the page |
| `multi-source-primary` | 2+ Raw Sources, all primary |
| `multi-source-mixed` | Primary + secondary (commentary, interpretation) |
| `synthesis-only` | Derived from other Wiki pages, no direct Raw Source |
| `user-original` | Sourced from `mainVaultRelated` (mothership essays / permanent notes) |

## Process

### Phase 1 — Eligibility (지식요건해당성)

**1.1 Frontmatter completeness**

Required 7 (CLAUDE.md): `type`, `aliases`, `description`, `author`, `date created`, `date modified`, `tags`.
Wiki-page layer: `source`, `related`, `confidence`, `layer`, `explored`.
v2/v4: `mainVaultRelated`, `mainVaultCmds` (if Step 0-a returned candidates during /ingest).
**v5 (this command writes)**: `claimType`, `evidenceScope`.

Report missing fields. For `claimType` / `evidenceScope`, propose values from content analysis instead of just flagging.

**1.2 SPO structure**

- `# {Page Name}` H1 present and matches frontmatter subject
- ≥2 H2 sections (predicates)
- `## Sources` section listing Raw Source wikilinks
- `## Related` section with cross-references

**1.3 Per-claim metadata**

Extract up to **10 major claims** from page body (sentences asserting fact / definition / prescription). For each:

- Is the claim attributed (inline `[[wikilink]]` or implicit via `## Sources`)?
- Is the claim type classifiable (one of 6)?
- Can the evidence be located in a cited source?

**Verdict**: `eligible` (all pass) / `partial` (1-2 gaps) / `ineligible` (≥3 gaps or missing Subject).

### Phase 2 — Consistency (정합성)

**2.1 Source fidelity (anti-hallucination)**

For the **top 5 most concrete claims** (numbers, dates, attributions, quotes):

1. Read each cited Raw Source from `source:` frontmatter
2. Grep the Raw Source body for keywords / numbers / quotes from the claim
3. If a specific number / date / quote is **not present** in the source → flag `HALLUCINATION SUSPECTED`

Actions per unsupported claim: (a) find correct source, (b) downgrade to `interpretive` claim type + soften wording, (c) mark `disputed`.

**2.2 Cross-page consistency**

For each major claim, search related Wiki pages via:
- `related:` frontmatter on this page
- `mcp__qmd__query` semantic search over `wiki` collection
- `Grep` for the same key term across `20. Wiki/`

Detect four conflict shapes:
- Same concept, **different definition**
- **Contradicting empirical claims** (different numbers / dates / attributions)
- **Contradicting prescriptions** ("always X" vs "avoid X")
- **Same source, divergent interpretations**

For each conflict:
- Add `> [!warning] Disputed Claim` callout in **both** pages with cross-link
- Set `disputed: true` in **both** pages' frontmatter
- Do NOT auto-delete either side

**2.3 Policy consistency (CLAUDE.md)**

- Correct layer folder (Concepts / Entities / Guides / Maps)?
- Filename convention (CJK person → native script, Latin → original spelling)?
- YAML 2-space indent, body TAB indent?
- Wikilinks in YAML quoted (`"[[link]]"`)?
- Mermaid labels quoted (`A["label"]`)?
- `description` in English (1-2 sentences)?

**2.4 Core Context alignment**

Check page's `mainVaultCmds` + `tags` for connection to ≥1 of the 7 reuse axes (PhD / 학술 / 강의 / 컨설팅 / CMDS / 에세이 / 제품). If none → soft flag "orphaned from user purpose" (not a hard fail, but lowers confirmability).

**Verdict**: list of conflicts grouped by reference frame, each with proposed action (`disputed` / fix / accept).

### Phase 3 — Confirmability (확증가능성)

**3.1 Source count and type**

Count sources in `source:` frontmatter. Classify:
- **Primary** — Raw Source in `10. Raw Sources/`
- **Secondary** — commentary, derived synthesis
- **User-original** — `mainVaultRelated` mothership essay link

**3.2 Counter-evidence search**

For the page's central claim, search Wiki for:
- Pages explicitly contradicting (already found in 2.2)
- Pages presenting alternative frameworks
- `> [!warning]` callouts naming this page

**3.3 Confidence calibration**

Compute recommended confidence **independently**:

| Conditions | Recommended `confidence` |
|------------|--------------------------|
| 3+ primary sources, no counter-evidence, age > 30 days, no unresolved Phase 2 conflicts | `high` |
| 1-2 primary sources, no counter-evidence | `medium` |
| Single source OR `synthesis-only` OR created < 7 days ago | `low` |
| Counter-evidence present and unresolved | `disputed` |

Compare to declared `confidence:`:
- Declared > Recommended → **OVERCLAIM**. Suggest downgrade or add sources.
- Declared < Recommended → **UNDERCLAIM**. Suggest upgrade.

**3.4 Bias Check generation**

If page is `confidence: high` (declared or recommended) and `> [!note] Bias Check` callout is missing:
- Draft a counter-argument **specific to this page's central claim** (no generic stubs)
- Identify a data gap (missing primary source, longitudinal data, cross-validation, contrary case)
- Propose insertion near page bottom (after Sources, before Open Questions if present)

**3.5 `explored` gate decision**

If all 3 phases pass **AND** the user confirms verification in the same turn:
- Propose flipping `explored: false` → `true`
- Set `exploredBy: agent` (or `human` if the user performed the read)
- Set `exploredDate: YYYY-MM-DD`

> **Never auto-flip `explored` without explicit user OK** — the gate's value is the human/audited attestation; silent auto-flip destroys it.

**Verdict**: per-claim verifiability scores, recommended `confidence`, Bias Check draft.

### Phase 4 — Write-back (unless `--no-write-back`)

Update the page frontmatter (v5 keys):

```yaml
verificationStatus: verified | partial | unverified | disputed
verifiedAt: YYYY-MM-DD
verifiedBy: agent | human | both
claimType: <classified>
evidenceScope: <classified>
confidence: <recommended, only if user confirms change>
disputed: <true if any unresolved Phase 2 conflict>
explored: <true ONLY if user confirms in same turn>
exploredBy: agent | human
exploredDate: YYYY-MM-DD
```

If Bias Check was generated → insert callout in body.
If Disputed Claim callouts were generated → insert in body AND in each conflicting page's body.

Append a log entry to `log.md`:

```markdown
## [YYYY-MM-DD] verify | {page name}

- Status: {verified|partial|unverified|disputed}
- Eligibility: {pass|partial|fail}
- Consistency: {N conflicts found, M marked disputed}
- Confirmability: declared {X} → recommended {Y}
- Actions: {short list — Bias Check added, conflicts flagged, etc.}
```

## Output

Print a structured verification report:

```
# Verification Report — {Page Name}
File: {path}
Verified: {YYYY-MM-DD} by {agent|human|both}

## 1. Eligibility — {PASS | PARTIAL | FAIL}
Subject:        {subject identified or AMBIGUOUS}
Predicates:     {N H2 sections}
Objects:        {N major claims extracted}
Frontmatter:    {complete | missing: [list]}
Claim type:     {classified}
Evidence scope: {classified}

## 2. Consistency — {N conflicts}
Source fidelity:    {N/M concrete claims supported}
   HALLUCINATION SUSPECTED:
   - claim "..." not in source [[source-name]]
Cross-page:         {N} conflicts
   - vs [[Other Page]]: conflict on {claim} → proposed `disputed`
Policy violations:  {N} (CLAUDE.md rules)
Core Context:       connects to axes [{1,3,5}] | no axis match

## 3. Confirmability
Sources:            {N primary} + {M secondary} + {P user-original}
Counter-evidence:   {N pieces found}
Confidence:         declared {X} → recommended {Y}   [{OVERCLAIM|UNDERCLAIM|MATCH}]
Bias Check:         {present | generated | missing}

## Verdict
{VERIFIED | NEEDS REVISION | DISPUTED}
Actions taken:      [...]
Remaining gaps:     [...]
explored gate:      {flipped to true | pending user confirmation | stays false}
```

## Failure Modes

1. **Source file missing** — `source:` wikilink resolves to a deleted Raw Source. Skip Phase 2.1 for that source; flag `source:` as broken link; recommend re-ingest.

2. **Claim too vague to verify** — generic statements like "LLMs are powerful". Skip in Phase 2.1; mark in report as "non-verifiable interpretive claim"; recommend tightening wording.

3. **Counter-evidence itself unverified** — found a contradicting page, but it is `confidence: low` and `explored: false`. Do NOT auto-mark current page `disputed`. Instead recommend `/verify` on the counter-page first.

4. **Auto-flip `explored`** — never set `explored: true` without explicit user OK in the same turn. Same rule for `verificationStatus: verified`.

5. **Disputed cascade** — one conflict triggers `disputed: true` on many pages. Cap at **5 pages** per /verify call; queue the rest as recommended follow-up.

6. **Resolution mode (`--resolve`)** — only allowed when user provides new evidence (new source, new reasoning) in the same turn. Resolution can result in: keep both as disputed, remove `disputed` from one side, or downgrade the losing side's `confidence`.

## Integration

- New frontmatter keys (`claimType`, `evidenceScope`, `verificationStatus`, `verifiedAt`, `verifiedBy`, `disputed`) are **v5 additions** — documented in CLAUDE.md "Quality Control Properties" section.
- `/audit` consumes these keys to compute vault-wide health scores.
- `/query` SHOULD read `verificationStatus` + `confidence` of cited pages and hedge answer strength accordingly (e.g., "according to [[Page]] (verified, high confidence)..." vs "[[Page]] suggests, though unverified...").
- `/lint` SHOULD report coverage of v5 keys (% pages with `claimType`, `evidenceScope`, `verificationStatus`).
