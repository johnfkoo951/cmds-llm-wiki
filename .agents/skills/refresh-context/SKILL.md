---
name: "refresh-context"
description: "Re-snapshot Core Context.md from the 9 mothership system files and key essays when the mothership changes or the snapshot is older than 30 days; also responds to /refresh-context and 코어 컨텍스트 갱신."
---

# refresh-context

Use this skill when the user asks to run `refresh-context`, `/refresh-context`, or refresh the LLM Wiki Core Context snapshot.

## Command Template

# /refresh-context — Core Context Re-Snapshot

[[Core Context]] 노트는 메인 볼트 (`{your-mothership-vault-name}`) 9 시스템 파일과 핵심 에세이 5편의 **시점 snapshot** 이다. 메인 볼트가 변하면 이 snapshot 도 갱신해야 한다.

## When to Run

- `/lint` 또는 `/status` 가 "Core Context > 30 days old" 또는 "mothership drift" flag 했을 때
- 메인 볼트 9 시스템 파일 (`CLAUDE.md`, `AGENTS.md`, `ANTIGRAVITY.md`, `CMDS.md`, `🏛 CMDS Guide.md`, `🏛 CMDS Head Quarter.md`, `BRAIN.md`, `BRAIN_PROMPT.md`, `DESIGN.md`) 의 major version 이 변경되었을 때
- 사용자가 새 에세이를 발행했을 때 (Permanent Notes)
- 7 재활용 축이 변경되었을 때 (예: 새 사업부 추가, 기존 축 제거)

## Process

### Step 1: Load Current Core Context

Read [[Core Context]] frontmatter `snapshot_date` and current §2 (7 재활용 축), §4 (철학 4축), §5 (5 시스템 파일 요약).

### Step 2: Re-Read Mothership System Files

```
# Codex: Read(...)
# Antigravity: view_file(...)
Read("{PATH_TO_YOUR_MOTHERSHIP_VAULT}/CLAUDE.md")
Read("{PATH_TO_YOUR_MOTHERSHIP_VAULT}/AGENTS.md")
Read("{PATH_TO_YOUR_MOTHERSHIP_VAULT}/ANTIGRAVITY.md")
Read("{PATH_TO_YOUR_MOTHERSHIP_VAULT}/CMDS.md")
Read("{PATH_TO_YOUR_MOTHERSHIP_VAULT}/🏛 CMDS Guide.md")
Read("{PATH_TO_YOUR_MOTHERSHIP_VAULT}/🏛 CMDS Head Quarter.md")
Read("{PATH_TO_YOUR_MOTHERSHIP_VAULT}/BRAIN.md")
Read("{PATH_TO_YOUR_MOTHERSHIP_VAULT}/BRAIN_PROMPT.md")
Read("{PATH_TO_YOUR_MOTHERSHIP_VAULT}/DESIGN.md")
```

For each file, capture:
- `version:` (frontmatter) — has it bumped?
- `date modified:` — newer than current snapshot?
- `changelog:` first entry — what changed?
- Sections that affect Core Context §5 table (precedence, audience, focus, memory-type)

### Step 3: (옵션) Re-Read Personal Essays

사용자가 Core Context 의 `source:` 프로퍼티에 등록한 에세이들을 다시 읽는다. 경로는 사용자 환경마다 다르므로 `{PATH_TO_YOUR_ESSAYS}` placeholder 로 등록해두고 사용.

```
# Codex: Read(...)  /  Antigravity: view_file(...)
# Core Context frontmatter 의 source 리스트에 있는 각 경로에 대해
Read("<essay path>")
```

Also scan for **new** essays (last 60 days) that may signal philosophy shift:

```bash
find "{PATH_TO_YOUR_ESSAYS}" -name "*.md" -mtime -60 | head -10
```

### Step 4: Diff & Propose

Show the user a side-by-side:
- **Current Core Context** (key sections — 7 axes, 5 files table, 4 philosophies)
- **Proposed updates** based on mothership state
- **New essays** discovered (with one-line summary each — ask if any deserve §4 promotion)

Ask: **"이 diff 를 적용할까요? (전체 / 부분 / 거부)"**

### Step 5: Apply

If approved:
- Update [[Core Context]] body sections
- Update frontmatter: `snapshot_date: {today}`, `date modified: {today}`, bump `version` if §2/§4/§5 changed (semver-ish: 1.0 → 1.1 for additions, 2.0 for restructure)
- Update `source:` list if new essays added

### Step 6: Log

Append to `log.md`:
```markdown
## [{YYYY-MM-DD}] update | Core Context refreshed (v{old} → v{new})

- Mothership drift: {which files changed since last snapshot}
- New essays incorporated: {list}
- Updated sections: {§2 / §4 / §5 / etc}
- Why: {one-line reason}
```

## Output

Report:
1. **Snapshot age**: was {N} days old, now 0
2. **Changes applied**: bullet list of section updates
3. **New essays added to source list**: count + titles
4. **Version bump**: old → new
