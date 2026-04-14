---
description: Re-snapshot Core Context.md from (optional) mothership system files + key personal essays. Run when mothership files change, when new essays signal philosophy shift, or when snapshot is older than 30 days.
allowed-tools: Read, Edit, Glob, Grep, Bash, mcp__qmd__query
---

# /refresh-context — Core Context Re-Snapshot

[[Core Context]] 노트는 사용자의 **시점 snapshot** 이다. 사용자 생각이 발전하거나 (옵션) mothership 볼트가 변하면 이 snapshot 도 갱신해야 한다.

## When to Run

- `/lint` 또는 `/status` 가 "Core Context > 30 days old" 또는 "mothership drift" flag 했을 때
- (mothership 운영 시) 메인 볼트 시스템 파일 major version 변경
- 사용자가 새 에세이·manifesto 를 발행했을 때 — §4 철학 갱신 필요
- 7 재활용 축(§2) 이 바뀌었을 때 (예: 새 역할 추가, 기존 축 제거)
- 연속성 선언(§1) 이 업데이트 필요할 때

## Process

### Step 1: Load Current Core Context

Read [[Core Context]] frontmatter `snapshot_date` 및 현재 §1 (정체성), §2 (7 재활용 축), §3 (프레임워크), §4 (철학), §5 (mothership 참조).

### Step 2: (옵션) Re-Read Mothership System Files

[[Core Context]] §5 에 등록된 mothership 파일들을 읽는다. 예시 (본인 볼트 경로로 교체):

```
Read("{PATH_TO_YOUR_MOTHERSHIP}/CLAUDE.md")
Read("{PATH_TO_YOUR_MOTHERSHIP}/AGENTS.md")
# ... §5 에 등록된 만큼
```

For each file, capture:
- `version:` (frontmatter) — bumped?
- `date modified:` — newer than current snapshot?
- `changelog:` first entry — what changed?
- 섹션 변화가 Core Context §5 테이블에 영향을 주는가 (precedence, audience, focus, memory-type)

Mothership 이 등록되어 있지 않다면 이 단계 건너뜀.

### Step 3: (옵션) Re-Read Personal Essays

사용자가 `source:` 프로퍼티에 등록한 에세이들을 다시 읽는다. Core Context frontmatter 의 `source:` 리스트 확인.

```
# frontmatter source 에 있는 각 경로에 대해
Read("<essay path>")
```

Also scan for **new** essays (last 60 days) that may signal philosophy shift. 경로는 사용자 환경 따라 다름 — [[Core Context]] §5 와 같이 `{PATH_TO_YOUR_ESSAYS}` 형태로 등록해두고 사용:

```bash
find "{PATH_TO_YOUR_ESSAYS}" -name "*.md" -mtime -60 | head -10
```

### Step 4: Diff & Propose

사용자에게 side-by-side 로 보여줌:
- **Current Core Context** (§1~§4 핵심 섹션)
- **Proposed updates** based on mothership/essay state
- **New essays** discovered (한 줄 요약 — §4 철학으로 승격할지 물음)

Ask: **"이 diff 를 적용할까요? (전체 / 부분 / 거부)"**

### Step 5: Apply

If approved:
- Update [[Core Context]] 본문 섹션
- Update frontmatter: `snapshot_date: {today}`, `date modified: {today}`, bump `version` (§2/§4/§5 변경 시 minor, 구조 재편 시 major)
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
