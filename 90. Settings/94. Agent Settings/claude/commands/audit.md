---
description: Audit the whole Wiki vault against 3 knowledge-integrity criteria — eligibility coverage, MOC-cluster consistency, confidence calibration. Produces a vault health report and queues high-priority pages for /verify.
allowed-tools: Read, Write, Glob, Grep, Bash, mcp__qmd__query
# Antigravity equivalents: view_file, write_to_file, list_dir, grep_search, run_command
---

# /audit — Whole-Vault Knowledge Integrity Audit

Run a vault-wide audit against the same 3 criteria as `/verify`, but at scale via MOC-cluster strategy + prioritized sampling. Produces a structured health report and queues `/verify` actions for the highest-impact pages.

> **🧭 Prerequisite**: Read [[Core Context]] once per session — Phase B consistency check needs the user's 7 reuse axes for purpose-alignment scoring.

> **Relation to /verify**: `/audit` does NOT verify every page individually — that would take hundreds of LLM calls. It surfaces **drift patterns** and **prioritizes** the next `/verify` calls. Think of it as the planner; `/verify` is the worker.

## Input

`$ARGUMENTS` (Claude Code) / `User Request` (Antigravity)

- empty / `--full` — audit entire `20. Wiki/`
- `--moc {MOC name}` — audit one MOC cluster only (faster; useful for incremental audits)
- `--recent {N}` — only pages with `date modified` within last N days
- `--confidence high` — only `confidence: high` pages (highest-stakes audit)
- `--no-save` — print only, do not save report to `30. Queries/`
- `--compare {YYYY-MM-DD-Q-vault-audit-...}` — diff against a previous audit report

## Conceptual Framework — Same 3 Criteria as /verify

See `.claude/commands/verify.md` for full definitions of:
- 지식요건해당성 (Eligibility) — Subject · Predicates · Objects · Source · Evidence Scope · Claim Type
- 정합성 (Consistency) — vs source / cross-page / policy / Core Context (conflicts → `disputed`, not delete)
- 확증가능성 (Confirmability) — independent confidence calibration + Bias Check coverage
- Claim Type taxonomy (6 types) + Evidence Scope levels (5)

### Scaling Strategy

| Criterion | At single-page (verify) | At vault scale (audit) |
|-----------|--------------------------|------------------------|
| **Eligibility** | full per-claim check | deterministic Grep-based sweep — counts and gaps |
| **Consistency** | full cross-page search | MOC-cluster batched — each MOC = one semantic cluster |
| **Confirmability** | full calibration | prioritized sampling — all `high`, all stale `explored: false`, 10% random of rest |

## Process

### Phase 0 — Inventory

```bash
# Page inventory
find "20. Wiki" -name "*.md" -type f      # all wiki pages
find "20. Wiki/24. Maps" -name "MOC-*.md" # all MOCs
```

For each MOC: read body, parse `[[wikilinks]]`, build cluster membership map.

Compute:
- Total pages, MOC count
- Cluster coverage % (pages belonging to ≥1 MOC)
- **Audit-orphan pages** (in zero MOCs) — flagged as cluster gap; included in Phase A but skipped in Phase B

Print inventory before starting Phase A.

### Phase A — Eligibility Sweep (deterministic, vault-wide)

Pure Grep/find operations. Fast — should complete in seconds.

**A.1 Frontmatter coverage**

```bash
# Per-property coverage (% of pages with the key)
total=$(find "20. Wiki" -name "*.md" | wc -l)
for key in claimType evidenceScope confidence explored mainVaultRelated verificationStatus; do
    count=$(grep -lE "^${key}:" "20. Wiki"/**/*.md 2>/dev/null | wc -l)
    echo "${key}: ${count}/${total}"
done
```

**A.2 SPO structure**

```bash
# Pages missing H1
grep -L "^# " "20. Wiki"/**/*.md

# Pages missing Sources section
grep -L "^## Sources" "20. Wiki"/**/*.md

# Pages missing Related section
grep -L "^## Related" "20. Wiki"/**/*.md
```

**A.3 Source citation density**

For each page, count `[[wikilinks]]` pointing into `10. Raw Sources/` (proxy via source filenames). Pages with **0 source citations in body** flagged as `synthesis-only` (not a failure — but must declare `evidenceScope: synthesis-only`).

**A.4 Policy violations (CLAUDE.md)**

- YAML indent (tabs in YAML block)
- Body indent (spaces where TAB expected)
- Unquoted wikilinks in YAML (`- [[link]]` instead of `- "[[link]]"`)
- Unquoted Mermaid labels (`A[label]` instead of `A["label"]`)
- Layer mismatch (e.g., a concept in `22. Entities/`)

**Output for Phase A**:
- Coverage table per dimension
- Names of failing pages (cap at top 20 per dimension)
- Eligibility score (weighted % of pages passing all 4 sub-checks)

### Phase B — Consistency Clusters (LLM-driven, batched)

Process MOC clusters in parallel — each MOC is independent.

For each MOC:

1. **Load cluster** — read MOC body + every linked Wiki page (typical cluster: 5-30 pages)
2. **Extract claims** — from each page, identify the 3-5 central claims (Subject + Predicate + Object)
3. **Cross-compare** — within the cluster, look for:
   - Same concept, **different definition** (most common drift mode)
   - **Contradicting empirical claims** (different numbers / dates / attributions for the same fact)
   - **Contradicting prescriptions** ("always X" in one page, "avoid X" in another)
   - **Same Raw Source, divergent interpretations**
4. **Report conflicts** — for each, name the two (or more) pages involved + the specific claim + proposed action

> **Conflict action default**: mark both pages `disputed: true` + add `> [!warning] Disputed Claim` cross-link callouts via `/verify --resolve`. `/audit` itself does NOT write to pages — it queues the actions.

**Concurrency**: spawn one sub-task per MOC cluster (independent). 10-15 MOCs → 10-15 parallel LLM calls. Use Workflow tool or parallel Agent invocations for this phase if Ultracode is on.

**Audit-orphan handling**: pages in zero MOCs cannot be cluster-checked. Two options:
- Per-tag pseudo-cluster (group by top-3 tags)
- Skip and flag as "uncluster-able" → recommend MOC assignment

**Output for Phase B**:
- Per-MOC conflict list
- Cross-MOC conflict list (rare; same claim contested in 2 different MOCs)
- Hallucination suspects (claims with numbers/dates not found in any cited Raw Source — sample only, full check in Phase C)
- Consistency score: `100 − (5 × MOC conflicts) − (10 × hallucination suspects) − (2 × policy violations)`, floored at 0

### Phase C — Confirmability Sampling (LLM-driven, prioritized)

Target population is the **union** of:

1. **All `confidence: high` pages** — strongest claims, must be audited fully
   ```bash
   grep -lE "^confidence: high" "20. Wiki"/**/*.md
   ```
2. **Stale unexplored backlog** — `explored: false` AND `date modified > 30 days ago`
3. **Disputed pages** — `disputed: true`, even if previously verified
4. **Random 10% stratified sample of remaining** — drift detection
   - Stratify by category (Concepts / Entities / Guides / MOCs) to avoid sample bias

For each target page, run an **abbreviated /verify Phase 3** (Confirmability only):

- Count primary / secondary / user-original sources
- Search Wiki for counter-evidence (Grep + `mcp__qmd__query` semantic search)
- Compute recommended `confidence` (same matrix as /verify Phase 3.3)
- Flag overclaim / underclaim
- Check Bias Check presence on high-confidence pages

**Concurrency**: partition target list into batches of ~20, each batch processed in parallel.

**Output for Phase C**:
- Confidence calibration table (page, declared, recommended, verdict)
- Overclaim list (high-confidence with single source)
- Underclaim list (low-confidence with strong evidence)
- Bias Check coverage % on high-confidence pages
- Confirmability score: weighted avg of (calibration alignment) + (high-conf Bias Check coverage)

### Phase D — Synthesis

Compute three scores 0-100 and the **composite Vault Health**:

| Score | Formula |
|-------|---------|
| **Eligibility** | weighted avg of frontmatter coverage + SPO presence + claim type assignability |
| **Consistency** | `100 − (5 × MOC conflicts) − (10 × hallucination suspects) − (2 × policy violations)` |
| **Confirmability** | weighted avg of calibration alignment + Bias Check coverage (high-conf only) |
| **Composite** | arithmetic mean of the three |

Identify **Top 10 actions**, ranked by impact:

Priority signals:
- Pages involved in **multiple conflicts** (Phase B)
- **Overclaim** pages with declared `confidence: high` (Phase C)
- Pages with **broken `source:`** wikilinks (Phase A)
- High-traffic pages (referenced from many `related:`) with low confirmability

Each action: `/verify [[Page]] — {reason}`.

### Phase E — Save report (unless `--no-save`)

Save to `30. Queries/YYYY-MM-DD-Q-vault-audit.md`:

```yaml
---
type: query-result
description: Vault-wide audit against the 3 knowledge-integrity criteria — eligibility, consistency, confirmability.
query: "Vault audit ({scope})"
aliases:
  - "Vault Audit {YYYY-MM-DD}"
author:
  - Claude
date created: YYYY-MM-DD
date modified: YYYY-MM-DD
tags:
  - audit
  - quality-control
  - vault-health
source:
  - "Wiki snapshot @ YYYY-MM-DD"
reusableFor: "(5) CMDS 시스템 — wiki self-maintenance"
---
```

Body sections:
- `## Vault Health` — composite + 3 sub-scores
- `## Phase A — Eligibility Sweep` — coverage tables
- `## Phase B — MOC-Cluster Consistency` — conflict list grouped by MOC
- `## Phase C — Confirmability Calibration` — overclaim / underclaim tables
- `## Top 10 Recommended Actions` — ordered `/verify` queue
- `## Drift Since Last Audit` — diff vs previous audit (if `--compare` or prior audit found)

Append to `log.md`:

```markdown
## [YYYY-MM-DD] audit | {scope}

- Health: {composite}/100 (E:{eligibility} C:{consistency} K:{confirmability})
- Conflicts: {N} | Overclaim: {N} | Coverage gaps: {N}
- Report: [[YYYY-MM-DD-Q-vault-audit]]
```

## Output

Print summary to terminal:

```
🔍 Vault Audit — YYYY-MM-DD  ({scope})
──────────────────────────────────────
Vault Health: {composite}/100

1. Eligibility (지식요건해당성):    {score}/100
   Frontmatter coverage:
     claimType        {pct}%  evidenceScope    {pct}%
     verificationStatus {pct}%  explored      {pct}%
     mainVaultRelated {pct}%
   SPO structure:                  {pct}% complete
   Policy violations:              {N}
   Failing pages:                  {N} → see report

2. Consistency (정합성):           {score}/100
   MOC clusters audited:           {N}
   Cross-page conflicts:           {N}  (queued for disputed: {N})
   Hallucination suspects:         {N}
   Audit-orphan pages (no MOC):    {N}

3. Confirmability (확증가능성):     {score}/100
   High-confidence audited:        {N}
   Overclaim suspects:             {N}
   Underclaim suspects:            {N}
   Bias Check on high-conf:        {pct}%

🎯 Top 10 Actions (run as /verify)
   1. /verify [[Page A]] — 3 conflicts in {MOC}
   2. /verify [[Page B]] — overclaim suspect (1 source, high conf)
   ...

📁 Report saved: 30. Queries/YYYY-MM-DD-Q-vault-audit.md
   Drift vs last audit: {scores delta}
```

## Failure Modes

1. **MOC out of sync** — page links to MOC but MOC doesn't link back (or vice versa). Don't include in cluster; flag separately as MOC-sync gap and recommend `/lint` to fix.

2. **Oversized cluster** — one MOC has 50+ linked pages. Subdivide by tag intersection (e.g., MOC-AI Agents → sub-cluster by `agent-harness` tag vs `agent-skills` tag). Audit each sub-cluster separately.

3. **Sample bias** — random 10% sample disproportionately hits one category. Always stratify by Concepts / Entities / Guides; never plain random.

4. **Audit storm** — every `/audit` flags the same pages without resolution. Read previous audit report first; pages flagged in **2 consecutive audits without `/verify` action** escalate to `STALE FLAG` priority (top of action list).

5. **Concurrency safety** — multiple LLM calls within audit could race on file reads if any phase wrote intermediate state. Audit is **read-only on Wiki pages** — all writes (report file, log.md) happen in Phase E, serialized. Pages are mutated only via subsequent `/verify` calls the user initiates.

6. **Confirmability vs source ground truth** — `/audit` Phase C cannot fully read every cited Raw Source for every claim. It samples. For the **definitive** source-fidelity check on a flagged page, the user runs `/verify` on that page.

7. **Action list explosion** — if Top 10 grows to Top 50, cap output at 10 and note "30+ more actions queued — see report Top {N} table". Don't dump 50 actions in terminal output.

## Integration

- `/audit` consumes v5 keys (`claimType`, `evidenceScope`, `verificationStatus`, `disputed`) written by `/verify`. First audit after introducing v5 will show low coverage — that's the backfill baseline.
- `/lint` and `/audit` are complementary: `/lint` = mechanical health (orphans, broken links, frontmatter presence), `/audit` = epistemic health (claim integrity, evidence strength). Run `/lint` weekly, `/audit` monthly.
- The Top 10 Actions list feeds `/verify` — the user can pipe `/audit` output to a follow-up `/verify {top action}` loop.
- For incremental audits, `/audit --moc {MOC name}` after every major `/ingest` keeps drift bounded to the changed cluster.

## Scheduling Suggestion

| Cadence | Command | Why |
|---------|---------|-----|
| Per-ingest | `/lint` (auto-style) | Catch mechanical drift immediately |
| Weekly | `/lint` (full) | Frontmatter / link health |
| Monthly | `/audit --full` | Vault-wide epistemic health |
| After major ingest | `/audit --moc {affected MOC}` | Cluster-scoped consistency check |
| Per-page on creation | `/verify` (recommended) | Establish baseline `verificationStatus: verified` at birth |
