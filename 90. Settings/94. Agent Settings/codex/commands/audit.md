---
description: Audit the whole Wiki vault against eligibility, consistency, and confirmability; saves a vault health report and queues high-priority /verify targets.
---

# /audit — Codex Whole-Vault Knowledge Integrity Audit

Follow [[AGENTS.md]] and read [[Core Context]] once per session. This is the Codex mirror of `.claude/commands/audit.md`.

## Input

- empty or `--full`: audit all `20. Wiki/`
- `--moc {MOC name}`: audit one MOC cluster
- `--recent {N}`: pages modified within N days
- `--confidence high`: high-confidence pages only
- `--no-save`: report only
- `--compare {query-result}`: compare against previous audit

## Process

### Phase 0 — Inventory

Count Wiki pages, MOCs, Raw Sources, Queries, and MOC membership. Identify audit-orphan pages outside every MOC.

### Phase A — Eligibility Sweep

Use deterministic shell checks for:

- `claimType`
- `evidenceScope`
- `confidence`
- `explored`
- `mainVaultRelated`
- `verificationStatus`
- H1 / Sources / Related sections
- AGENTS.md policy violations

### Phase B — MOC-Cluster Consistency

For each MOC cluster, read linked pages and compare central claims. Queue conflicts for `/verify --resolve`; do not mutate Wiki pages during audit.

### Phase C — Confirmability Sampling

Prioritize all `confidence: high`, stale `explored: false`, `disputed: true`, and a stratified sample of remaining pages. Calibrate confidence and Bias Check coverage.

### Phase D — Synthesis

Compute:

- Eligibility score
- Consistency score
- Confirmability score
- Composite Vault Health
- Top 10 `/verify` actions

### Phase E — Save

Unless `--no-save`, save:

`30. Queries/YYYY-MM-DD-Q-vault-audit.md`

Append `log.md` with health score, conflict count, overclaim count, and report link.

## Output

Print the vault health summary and the Top 10 `/verify` queue.
