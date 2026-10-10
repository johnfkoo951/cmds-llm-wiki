---
description: Interview-based first-run setup for this LLM Wiki kit. Asks the essential questions (vault location/name, Mode A/B, mothership path, Core Context identity + reuse axes), then fills every placeholder and writes Core Context so the wiki knows you from day one. Activate when the user says "온보딩해줘", "처음 시작할게", "처음 시작", "온보딩", "setup", "set up my wiki", "getting started", "fill my wiki", or opens a freshly-cloned kit and asks "어떻게 시작하지" / "where do I start". The interactive equivalent of `90. Settings/Sharing/Setup Guide.md`.
allowed-tools: Read, Edit, Glob, Grep, Bash
# Antigravity equivalents: view_file, replace_file_content, list_dir, grep_search, run_command. AskUserQuestion → ask plain-text questions if the tool is unavailable.
---

# /onboard — LLM Wiki Setup (Interview)

Turn a freshly-cloned `cmds-llm-wiki` into *your* wiki in ~10 minutes by interviewing you and filling everything in. This is the interactive driver for `90. Settings/Sharing/Setup Guide.md` — read that for full detail/rationale.

## Philosophy (from cmds-onboarding)
1. **Context-first** — fill *who you are* (Core Context) before ingesting; without it every `/ingest` and `/query` is generic.
2. **Answer-1-of-many** — ask a handful per turn; the user answers only what's relevant. Context accumulates across turns.
3. **Agent-does-the-typing** — user describes in natural language; the agent writes frontmatter, placeholders, Core Context.
4. **Resume-safe** — re-running detects what's done and continues from the first unfinished step.

## Pre-flight (detect whether onboarding is needed)
```bash
echo "PWD: $(pwd)"
echo "남은 placeholder 파일 수: $(grep -rl '{your-name}\|{PATH_TO_YOUR_LLM_WIKI}\|{your-mothership-vault-name}' --include='*.md' --include='*.yml' --include='*.json' . 2>/dev/null | grep -v '/.git/' | wc -l | tr -d ' ')"
echo "Core Context status: $(grep -m1 '^status:' 'Core Context.md' 2>/dev/null)"
```
- placeholder 파일 0개 + `status: active` → 이미 온보딩됨. 사용자에게 알리고 재실행 여부 확인.
- 그 외 → 인터뷰 시작.

## Interview — 필수 5 + 옵션 2 (answer-1-of-many)

> 음성 모드면 한 번에 1문항, 텍스트면 배치로. 각 답 후 1–2문장 요약 confirm.

**Q1 — 위치 & 이름**
- 볼트 절대경로는 `pwd` 로 자동 확보(= `{PATH_TO_YOUR_LLM_WIKI}`).
- 물어볼 것: "이 위키에서 쓸 이름은? (실명·핸들·한국어 다 가능 — wikilink로 들어감)" → `{your-name}` / `{Your Name}`.

**Q2 — 운영 모드** *(AskUserQuestion 권장, 없으면 평문)*
- **Mode A (단독)**: 별도 PKM 볼트 없이 이 키트만. 모선 placeholder 무시.
- **Mode B (모선 연계)**: 기존 PKM 볼트를 모선으로 두고 satellite 운영.

**Q3 — (Mode B만) 모선 경로·이름**
- `{PATH_TO_YOUR_MOTHERSHIP_VAULT}` / `{PATH_TO_YOUR_MOTHERSHIP}` = 모선 절대경로
- `{your-mothership-vault-name}` = 모선 폴더명(경로 X, `obsidian://open?vault=` 용)

**Q4 — Core Context §1 정체성 (핵심)**
- 이름·역할·전문 분야·주 활동 + **연속성 선언**(지금 활동이 과거 어떤 질문에서 출발했는지 1–3문장).

**Q5 — Core Context §2 재활용 축 5–9개 (핵심)**
- "이 소스가 어디 쓰일까"의 축. 7개 권장 (예: 학술/저술/강의/컨설팅/제품/에세이/커뮤니티). 너무 적으면 쏠리고 너무 많으면 무의미.

**옵션 — §3 개인 프레임워크 / §4 철학 3–5개**
- 있으면 채우고, 없으면 건너뜀(나중에 `/refresh-context`로 보강 가능).

> 막힐 때(failure mode): 답이 안 나오면 *passive 모드* — 기존 블로그/노트/에세이 경로를 받아 "이 글들 읽고 §1·§2 추론해줘"로 전환.

## Fill — placeholder 치환 + Core Context 작성

**Step F1 — placeholder 일괄 치환** (값 confirm 후 실행). 날짜는 KST 오늘.
```bash
# Mode A (단독)
LC_ALL=C find . -type f \( -name "*.md" -o -name "*.yml" -o -name "*.json" -o -name "*.sh" \) \
  -not -path "./.git/*" -exec sed -i '' \
  -e 's|{your-name}|<NAME>|g' -e 's|{Your Name}|<NAME>|g' \
  -e "s|{PATH_TO_YOUR_LLM_WIKI}|$PWD|g" \
  -e "s|{YYYY-MM-DD}|$(date +%Y-%m-%d)|g" {} +

# Mode B — 위에 더해 모선 경로·이름도
LC_ALL=C find . -type f \( -name "*.md" -o -name "*.yml" -o -name "*.json" -o -name "*.sh" \) \
  -not -path "./.git/*" -exec sed -i '' \
  -e 's|{PATH_TO_YOUR_MOTHERSHIP_VAULT}|<MOTHERSHIP_PATH>|g' \
  -e 's|{PATH_TO_YOUR_MOTHERSHIP}|<MOTHERSHIP_PATH>|g' \
  -e 's|{your-mothership-vault-name}|<MOTHERSHIP_NAME>|g' {} +
```

**Step F2 — Core Context.md 작성**: §1 정체성 + §2 재활용 축(+옵션 §3·§4)을 인터뷰 답으로 채움. 작성 전 draft를 보여주고 confirm. 그다음:
- frontmatter `status: template` → `active`
- `snapshot_date` → 오늘(KST), `version: "1.0"` 유지
- Mode A면 §5 Mothership 섹션 삭제.

**Step F3 — 치환 검증**
```bash
grep -rn "{your-name}\|{Your Name}\|{PATH_TO\|{your-mothership" --include="*.md" --include="*.json" --include="*.yml" --include="*.sh" -l 2>/dev/null | grep -v ".git"
```
- 출력 없으면 통과. Mode A면 `{PATH_TO_YOUR_MOTHERSHIP*}`·`{your-mothership-vault-name}`만 남아도 무해(섹션 미사용).

## Resume logic
재실행 시 pre-flight grep으로 단계 판정 → 첫 미완료부터. (placeholder 남음 → F1 / Core Context `status: template` → F2.)

## Wrap-up + 다음 단계
완료 요약 후 추천:
1. `/status` — 볼트 상태 점검
2. `/ingest <URL>` — 첫 수집. **목적 질문이 뜨면 §2 재활용 축 중 하나로 답** ("미래의 나에게 보내는 편지")
3. `/query <질문>` — 첫 질의
4. (성장 후) 반복되는 Open Question 은 `20. Wiki/25. Questions/` 의 Research Question 카드로 승격, 주장을 방어할 땐 Synthesis 카드 (v1.9.0+) — Setup Guide FAQ 참고
5. (선택) qmd 설치·Web Clipper import → Setup Guide §6·§7

> 깊은 인터뷰·도메인별 질문 풀이 필요하면 모선 키트(cmds-vault)의 `cmds-onboarding` 스킬 참고. 이 `/onboard`는 LLM Wiki 단독 셋업에 최적화된 경량 버전.
