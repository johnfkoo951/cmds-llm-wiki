---
type: documentation
aliases:
  - Web Clipper 설정
  - Clipper Templates
  - 웹 클리퍼 가이드
description: Obsidian Web Clipper JSON template collection (14 templates) for routing clipped content into the LLM Wiki Inbox by category. Covers web articles, papers, videos, podcasts, social media, newsletters, news, discussions, and pure-selection clips. Includes a variable reference appendix extracted from real Web Clipper variable dumps.
author:
  - Claude
date created: 2026-04-13T00:00
date modified: 2026-04-14T13:00
tags:
  - system
  - web-clipper
  - tooling
  - templates
status: active
---

# Web Clipper Templates

> Obsidian Web Clipper에서 클리핑할 때 카테고리별로 자동 분류되도록 JSON 템플릿을 등록합니다.  
> 모든 템플릿은 `90. Settings/Sharing/clipper-*.json`에 저장되어 있으며, Web Clipper → Settings → Templates → Import JSON 으로 일괄 등록합니다.

---

## Inbox 라우팅 구조

```
00. Inbox/
├── 01. Articles/      ← 웹 기사, 블로그, 뉴스, 뉴스레터, 기술 문서
├── 02. Papers/        ← 학술 논문, arXiv, 기술 보고서
├── 03. Transcripts/   ← YouTube, 팟캐스트, 강연 녹취
└── 04. Clippings/     ← 짧은 발췌, 소셜, 디스커션, 하이라이트
```

---

## 📋 17 Templates Overview

| 템플릿 | 파일 | 대상 | Inbox 경로 | 트리거 도메인 |
|--------|------|------|-----------|-----------|
| **Web Article** | `clipper-web-article.json` | 일반 웹 기사 (기본값) | `01. Articles` | (any) |
| **arXiv / Paper** | `clipper-arxiv-paper.json` | 학술 논문, 기술 보고서 | `02. Papers` | arxiv.org, papers.ssrn.com, ... |
| **Tech Docs** | `clipper-tech-docs.json` | 공식 문서·API 레퍼런스 (reference) | `01. Articles` | docs.anthropic.com, platform.openai.com, MDN, 등 |
| **Tech Blog** 🆕 | `clipper-tech-blog.json` | AI 랩·빅테크 엔지니어링 블로그 | `01. Articles` | openai.com/index/, anthropic.com/news/, deepmind, hf/blog, vercel, github blog 등 |
| **GitHub** | `clipper-github.json` | GitHub 저장소·Gist | `01. Articles` | github.com |
| **YouTube** ✨ | `clipper-youtube.json` | YouTube 영상 + 자막 | `03. Transcripts` | youtube.com, youtu.be |
| **Podcast** 🆕 | `clipper-podcast.json` | Apple/Spotify/Overcast 팟캐스트 | `03. Transcripts` | podcasts.apple.com, open.spotify.com, pca.st |
| **News** 🆕 | `clipper-news.json` | 뉴스 매체 (NYT, WSJ, 조선·한겨레 등) | `01. Articles` | 주요 뉴스 도메인 |
| **Substack / Newsletter** 🆕 | `clipper-substack.json` | Substack, Beehiiv, Medium, Ghost | `01. Articles` | substack.com, medium.com, beehiiv, ghost |
| **Reddit** 🆕 | `clipper-reddit.json` | Reddit 스레드 + 댓글 | `04. Clippings` | reddit.com |
| **Hacker News** 🆕 | `clipper-hackernews.json` | HN 스토리 + 전문가 댓글 | `04. Clippings` | news.ycombinator.com |
| **X (Twitter)** 🆕 | `clipper-x.json` | X 포스트·스레드·Articles·quote tweet | `04. Clippings` | x.com, twitter.com, mobile.twitter.com |
| **Threads** | `clipper-threads.json` | Meta Threads 포스트 | `04. Clippings` | threads.net |
| **LinkedIn Post** | `clipper-linkedin.json` | LinkedIn 단문 포스트·피드 | `01. Articles` | linkedin.com/feed/, /posts/, /in/ |
| **LinkedIn Pulse** 🆕 | `clipper-linkedin-pulse.json` | LinkedIn Pulse 장문 아티클 | `01. Articles` | linkedin.com/pulse/ |
| **Instagram** | `clipper-instagram.json` | Instagram 포스트 | `04. Clippings` | instagram.com |
| **Selection** 🆕 | `clipper-selection.json` | 페이지 내 **하이라이트 발췌만** | `04. Clippings` | (모든 사이트, 선택 영역) |

✨ = 이번 세션에서 개선 / 🆕 = 이번 세션에서 신규

---

## 🆕 이번 세션 추가/개선 상세

### ✨ YouTube 템플릿 개선 (`clipper-youtube.json`)

**변경 전 문제**:
- `{{content}}` (description + transcript가 섞임)
- `{{selector:span.ytp-time-duration}}` — DOM 스크래핑으로 불안정
- `{{language}}`를 LLM 프롬프트로 추측 (불필요)

**변경 후**:
- `{{transcript}}` 전용 변수로 자막 분리 저장
- `{{description}}` 별도 섹션
- `{{schema:@VideoObject:thumbnailUrl}}` 사용 (schema.org)
- `{{language}}`, `{{words}}` 클리퍼 변수 직접 사용
- "Topics Mentioned" 섹션 추가 (자막 기반 엔티티 추출)

### 🆕 Selection (`clipper-selection.json`)

> 페이지 전체가 아닌 **하이라이트한 부분만** 저장. 인용문 수집에 최적.

- `{{selection}}` / `{{highlights}}` 변수 사용
- 원문 인용은 보존, LLM은 "왜 중요한가"를 맥락화
- "Connected Concepts"로 Wiki 연결 힌트

### 🆕 Podcast (`clipper-podcast.json`)

> Apple Podcasts, Spotify, Overcast, Pocket Casts, Castro

- 쇼 노트 + 플랫폼 메타 수집
- 전체 transcript는 페이지에 없음 → 필요 시 `audio-transcriber` 스킬로 별도 추출 후 append 안내

### 🆕 Reddit (`clipper-reddit.json`)

- OP + 주요 댓글 구조 유지
- "Signal vs Noise" 섹션 — meme/저품질 vs 인사이트 분리
- Subreddit 메타 capture

### 🆕 Substack / Newsletter (`clipper-substack.json`)

> Substack, Beehiiv, Medium, Ghost, Buttondown

- 에세이의 **thesis 추출** 우선
- "Key Claims & Evidence" 쌍 구조
- "Counterpoints" — 회의적 반박 강제 (bias 감지)

### 🆕 News (`clipper-news.json`)

> NYT, WSJ, Reuters, Bloomberg, BBC, 주요 국내 매체 (조선/한겨레/중앙/네이버 뉴스)

- 5W1H 요약 기본
- **Facts vs Framing** 섹션 — 사실과 프레이밍 분리 (중요)
- 교차 검증 필요 항목 리스트

### 🆕 Hacker News (`clipper-hackernews.json`)

- `news.ycombinator.com/item` 트리거
- "Top Insights" + "Contrarian Takes" 구분
- 댓글에서 외부 참조 URL 자동 수집

### 🆕 X / Twitter (`clipper-x.json`)

> 주의: Meta Threads와 **분리된** 템플릿. X는 `x.com` + `twitter.com` + mobile 서브도메인.

- 포스트 타입 자동 분류: single tweet / thread / quote tweet / X Article / reply
- **Thread Reconstruction** — 다중 포스트를 `1/`, `2/`, `3/` 순서로 재조립
- **Claims & Evidence** — X 특성상 "주장 vs 근거" 구분이 유독 중요 (인용 없이 단언 많음)
- Community Notes + quoted context 캡처
- 2026년 기준 X Articles(장문) 지원 — 다른 플랫폼처럼 1,000+ 단어 글도 가능

---

## 🚀 등록 절차

### 1. 일괄 등록

```bash
open "{PATH_TO_YOUR_LLM_WIKI}/90. Settings/Sharing/"
```

Obsidian Web Clipper → **Settings** → **Templates** → **Import** → 14개 JSON 각각 선택.

### 2. Vault 설정

- Web Clipper **Vault** 드롭다운 → 본인 LLM Wiki 볼트 선택
- 기본 템플릿(fallback) → `LLM Wiki — Web Article`

### 3. 확인

브라우저에서 `github.com/tobi/qmd` 방문 → Web Clipper 아이콘 클릭 → 드롭다운에 `LLM Wiki — GitHub` 자동 선택되면 OK.

---

## 🔁 라우팅 우선순위

복수 트리거가 매칭되면 **구체적 > 일반**. 예시 충돌:

| URL | 매칭 후보 | 선택 |
|-----|-----------|------|
| `substack.com/article/...` | Web Article, Substack | **Substack** (도메인 지정) |
| `youtube.com/watch?v=...` | Web Article, YouTube | **YouTube** (도메인 지정) |
| `news.ycombinator.com/item?id=...` | Web Article, Hacker News | **Hacker News** |

수동 override가 필요하면 Web Clipper 팝업에서 드롭다운으로 다른 템플릿 선택.

---

## 🧠 프롬프팅 전략 (템플릿 간 공통 패턴)

모든 템플릿은 아래 3단계 패턴:

1. **자동 필드 (클리퍼 변수)**: `{{title}}`, `{{url}}`, `{{author}}`, `{{published}}` 등은 클리퍼가 자동 수집
2. **원문 보존 영역**: `{{content}}` / `{{transcript}}` / `{{selection}}` — LLM이 수정 금지
3. **LLM 분석 영역**: `{{"프롬프트"}}` 구문 — 클리핑 시 LLM이 요약/추출 수행

각 템플릿의 LLM 분석 영역은 **콘텐츠 타입별 차별화**:

| 타입 | 강조하는 것 |
|------|------------|
| Article | 3줄 요약 |
| Paper | 기여·방법론·관련성 |
| YouTube | Takeaways + 언급 토픽 |
| Podcast | 액션 아이템 |
| News | 5W1H + 사실/프레이밍 분리 |
| Substack | Thesis + 반박 |
| Reddit | Signal vs Noise |
| HN | Insight + Contrarian |
| Selection | 왜 중요한가 + 연결 개념 |

---

## 📚 Appendix: Web Clipper 변수 레퍼런스

실제 YouTube 페이지 클리핑 시 Web Clipper가 노출하는 변수 덤프를 기준으로 정리.

### 기본 변수

| 변수 | 설명 | 예시 값 |
|------|------|---------|
| `{{title}}` | 페이지 타이틀 | "클로드 코드를..." |
| `{{url}}` | 현재 페이지 URL | `https://...` |
| `{{author}}` | 작성자/채널 | `@seulkiji1151` |
| `{{description}}` | 메타 설명 | "AI 시대 단순..." |
| `{{site}}` | 사이트 이름 | `YouTube` |
| `{{domain}}` | 도메인 | `youtube.com` |
| `{{favicon}}` | 파비콘 URL | `https://.../favicon.png` |
| `{{image}}` | OG image / 썸네일 | `https://i.ytimg.com/vi/.../maxresdefault.jpg` |
| `{{content}}` | 본문 전체 (마크다운 변환) | — |
| `{{date}}` | 클리핑 시각 | `2026-04-14T16:31:38+09:00` |
| `{{time}}` | 클리핑 시각 (동일) | — |
| `{{published}}` | 원본 게시 시각 | `2026-04-12T06:02:27-07:00` |
| `{{language}}` | 감지된 언어 | `ko` |
| `{{words}}` | 단어 수 | `14260` |
| `{{noteName}}` | 생성될 노트 제목 | — |

### 컨텍스트 특화 변수

| 변수 | 대상 | 설명 |
|------|------|------|
| `{{transcript}}` | YouTube | 영상 자막 (섹션 헤더 + 타임스탬프 포함) |
| `{{selection}}` | 전체 | 사용자가 하이라이트한 plain text |
| `{{selectionHtml}}` | 전체 | 하이라이트 부분의 HTML |
| `{{highlights}}` | 전체 | 구조화된 하이라이트 데이터 |

### 메타 태그 접근

| 패턴 | 설명 |
|------|------|
| `{{meta:name:title}}` | `<meta name="title">` |
| `{{meta:name:description}}` | `<meta name="description">` |
| `{{meta:name:keywords}}` | `<meta name="keywords">` |
| `{{meta:property:og:image}}` | `<meta property="og:image">` |
| `{{meta:property:og:video:url}}` | OG 비디오 URL |
| `{{meta:name:twitter:card}}` | Twitter card 타입 |

### Schema.org 접근

| 패턴 | 설명 |
|------|------|
| `{{schema:@VideoObject:thumbnailUrl}}` | VideoObject의 썸네일 |
| `{{schema:@VideoObject:uploadDate}}` | VideoObject 업로드 일자 |
| `{{schema:@Article:headline}}` | NewsArticle/BlogPosting 헤드라인 |
| `{{schema:@Person:name}}` | Person 엔티티 이름 |

### 유틸리티 필터

| 필터 | 용도 | 예시 |
|------|------|------|
| `|truncate:80` | 길이 제한 | `{{title|truncate:80}}` |
| `|date:"YYYY-MM-DD"` | 날짜 포맷 | `{{date|date:"YYYY-MM-DD"}}` |
| `|fallback:image` | 다른 변수로 대체 | `{{schema:@VideoObject:thumbnailUrl|fallback:image}}` |
| `|callout:("type","title",false)` | 콜아웃 래핑 | `{{"요약"|callout:("summary","3줄 요약",false)}}` |

### DOM 셀렉터 (불안정, 최후의 수단)

```
{{selector:span.class-name}}
{{selector:[data-testid="subreddit-name"]}}
```

DOM 구조가 바뀌면 파손. schema/meta 변수를 우선 사용.

### LLM 추론 영역

```
{{"프롬프트 내용. 한국어로 답변.}}
{{"프롬프트 내용"|callout:("summary","요약",false)}}
```

클리핑 시점에 LLM이 호출되어 결과를 삽입. 복잡한 분석 가능하지만 토큰 비용 고려.

---

## 🔄 Workflow

1. 브라우저에서 자료 발견
2. Web Clipper 아이콘 클릭 (또는 단축키 `Cmd+Shift+O`)
3. 도메인에 따라 템플릿 자동 선택, 필요시 수동 변경
4. Save → `00. Inbox/{카테고리}/`에 저장
5. Claude Code에서 `/inbox` 실행 → 미처리 목록 확인
6. `/ingest` 로 Wiki 컴파일 → qmd 자동 재인덱싱

---

## 🛠 Troubleshooting

### 트리거가 작동 안 함

- Web Clipper → Settings → Templates → 해당 템플릿 → Triggers 필드 확인
- 와일드카드 형식 확인: `https://*.substack.com/` (슬래시 끝 포함)

### `{{transcript}}`가 비어있음

- YouTube가 자막을 제공하지 않는 영상인 경우 fallback `{{content}}` 사용됨 (템플릿에 `|fallback:content` 이미 설정)
- 자동 자막이 있는지 먼저 확인 (YouTube 플레이어 하단 CC 버튼)

### LLM 호출 실패

- Web Clipper Settings → Interpreter → API key 확인
- 한국어 프롬프트 사용 시 일부 모델에서 응답 품질 저하 → 기본 모델을 Claude/GPT-4 계열로

### 중복 템플릿 선택

- 복수 템플릿의 트리거가 겹치면 설정 상단 템플릿이 우선
- Web Clipper Settings → Templates → 드래그로 순서 조정

---

## Related

- [[CLAUDE]] — 볼트 스키마 (frontmatter 규칙)
- `.claude/commands/inbox.md` — `/inbox` 명령
- `.claude/commands/ingest.md` — `/ingest` 명령
- `90. Settings/Sharing/` — 14 JSON 템플릿 저장소
