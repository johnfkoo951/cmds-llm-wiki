#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""p7_verify.py — Paper Ingest Mode P-7 기계 검증 (v6.2 schema)

Usage:
    python p7_verify.py "<40. Paper Analyses/{citekey} 폴더 절대/상대 경로>" [--vault "<볼트 루트>"]

의존성: Python 3.8+, PyYAML

동작:
    - 폴더명 = citekey (예: `wu2024longMemEval`); 허브는 폴더에서 자동 발견
    - 허브 (`* - S00 Hub.md`) 를 폴더에서 자동 발견
    - Raw Source 는 허브 frontmatter `source` wikilink 를 `10. Raw Sources/**` 에서 glob 해석
    - 단계명 스킴은 허브 `paperType` → `90. Settings/Templates/12-Step Analysis Schemes.md` 파싱 (6유형 전부)

검사 항목 (ingest.md P-7 의 스크립트 대체 범위):
    [1] YAML 실파서 전수 (yaml.safe_load)
    [2] v6 필수 키 (citekey 등) + analysisStep ↔ 파일명 S{NN} 일치 + analysisStepName ↔ 유형 스킴 일치
        + paperType ↔ 허브 일치 + paperHub ↔ 허브 일치
    [3] Analysis Context 콜아웃 + 필수 섹션 (쉬운 도입 / 정밀 해설 / 예시 / 원문 근거 / 개념 관계)
        — S12 완화: `## 개념 관계` 만 필수 (Writing Value 원자는 자유 구조)
        — `status: stub` 원자는 [3]~[5] 완화: Analysis Context 만 필수
    [4] 가로 연결: `## 개념 관계` 에 비-허브 형제 원자 wikilink ≥ 1
    [5] 인용 **전수** verbatim 대조 — 공백 정규화 substring, 실패 시 줄 단위 폴백 (PDF 개행 분절 대응)
    [6] Atom Catalog ↔ 실제 파일 양방향 + Coverage Map 원자 ⊆ Catalog
        + Step Map Atoms 수 ↔ 실제 파일 수 + `planned` 잔존 + Compile Plan 콜아웃 잔존
    [7] Coverage Map 에 원문 leaf 섹션 전수 등장 (Raw Source `## Original Content` 헤딩 추출 대조)
    [8] index.md 허브-단독 등재 (허브 있음 · 원자 노출 없음)
    [9] provenance: 허브 + 전 원자 frontmatter 에 model + effort 존재
        (v6 요건 — 에이전트 작성 콘텐츠는 model+effort 필수)

출력: 항목별 카운트 + 오류 리스트 + ALL PASS / FAIL + log.md 붙여넣기용 요약 블록.
종료 코드: ALL PASS = 0, FAIL = 1, 실행 불가 (허브/Raw Source/스킴 미해석) = 2.
"""

import argparse
import glob as globmod
import io
import os
import re
import sys
import unicodedata

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML 이 필요합니다 — pip install pyyaml")
    sys.exit(2)

# cp949 콘솔 (Windows) 대응 — UTF-8 출력 강제
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

TYPE_LETTER = {
    "quantitative": "A",
    "qualitative": "B",
    "theory-concept": "C",
    "mixed-methods": "D",
    "scale-development": "E",
    "meta-analysis": "F",
}

REQUIRED_SECTIONS = ["쉬운 도입", "정밀 해설", "예시", "원문 근거", "개념 관계"]
S12_REQUIRED_SECTIONS = ["개념 관계"]  # S12 (WRITING VALUE) 완화 규칙
# Raw Source 에서 ingest 가 덧붙이는 헤딩 — 논문 섹션이 아니므로 coverage 대상 제외
EXEMPT_HEADINGS = {"metadata", "ingest notes", "original content"}

WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]")
FENCE_RE = re.compile(r"```.*?```", re.S)
QUOTE_HEAD_RE = re.compile(r"^>\s*\[!quote\]", re.I)
HEADING_RE = re.compile(r"^(#{1,3})\s+(.+?)\s*$", re.M)
STEP_IN_NAME_RE = re.compile(r" - S(\d{2}) ")


def read_text(path):
    return io.open(path, encoding="utf-8").read()


def parse_frontmatter(text):
    """(frontmatter dict | None, 오류 문자열 | None) 반환. frontmatter 없음 = (None, 'frontmatter 없음')."""
    if not text.startswith("---"):
        return None, "frontmatter 없음"
    end = text.find("\n---", 3)
    if end == -1:
        return None, "frontmatter 종결 '---' 없음"
    try:
        fm = yaml.safe_load(text[3:end])
    except Exception as e:
        return None, "YAML 파싱 실패: " + str(e).split("\n")[0][:120]
    if not isinstance(fm, dict):
        return None, "frontmatter 가 매핑이 아님"
    return fm, None


def body_of(text):
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            return text[end + 4:]
    return text


def nfc(s):
    return unicodedata.normalize("NFC", s)


# 의미 동일·표기만 다른 유니코드 구두점 변이 → ASCII 정규화.
# LLM 은 원문의 curly quote·em dash 를 straight/hyphen 으로 옮겨쓰는 경향이 있어
# (grep 상 불일치지만 fabrication 은 아님) 이를 흡수한다. 단어·숫자는 건드리지 않으므로
# 내용 조작은 여전히 검출된다.
_PUNCT_TRANS = {
    0x2018: "'", 0x2019: "'", 0x201A: "'", 0x201B: "'",   # single quotes
    0x201C: '"', 0x201D: '"', 0x201E: '"', 0x201F: '"',   # double quotes
    0x2032: "'", 0x2033: '"',                              # primes
    0x2013: "-", 0x2014: "-", 0x2015: "-", 0x2212: "-",   # en/em dash, minus
    0x2026: "...",                                         # ellipsis
    0x00A0: " ", 0x2009: " ", 0x202F: " ",                # nbsp, thin/narrow spaces
}

def norm_ws(s):
    """NFC + 유니코드 구두점 변이 정규화 (curly quote·dash·ellipsis) + 공백 단일화 — verbatim 대조용."""
    return re.sub(r"\s+", " ", nfc(s).translate(_PUNCT_TRANS)).strip()


def norm_heading(s):
    """헤딩/커버리지 매칭용 정규화 — 선행 번호 제거, 소문자, 구두점 → 공백."""
    s = nfc(s).strip()
    s = re.sub(r"[*_`]", "", s)                       # markdown 강조 제거
    s = re.sub(r"^[§\s]*[\dIVX]+(?:\.\d+)*[.)\s]*", "", s)  # 선행 번호 (1. / 2.1 / IV.)
    s = s.lower()
    s = re.sub(r"[—–\-‑:：·+&/(),'\"“”‘’]", " ", s)
    s = re.sub(r"[^\w\s가-힣]", " ", s, flags=re.UNICODE)
    return re.sub(r"\s+", " ", s).strip()


def strip_quote_marks(s):
    return s.strip().strip("\"'“”‘’「」『』《》").strip()


def wikilink_targets(text):
    return [nfc(m.group(1).strip()) for m in WIKILINK_RE.finditer(text)]


def h2_sections(body):
    """[(제목, 본문)] — fenced code 제거 후 H2 단위 분할."""
    clean = FENCE_RE.sub("", body)
    parts = re.split(r"^##\s+", clean, flags=re.M)
    out = []
    for part in parts[1:]:
        lines = part.split("\n", 1)
        title = lines[0].strip()
        content = lines[1] if len(lines) > 1 else ""
        # 다음 H1 이 나오면 잘라냄 (H2 split 이라 H1 은 content 에 남을 수 있음)
        content = re.split(r"^#\s+", content, flags=re.M)[0]
        out.append((title, content))
    return out


def section_content(body, prefix):
    for title, content in h2_sections(body):
        if title.startswith(prefix):
            return content
    return None


def extract_quotes(body):
    """[(첫 줄 번호, [body 줄들])] — fenced code 제거 후 [!quote] 콜아웃 전수 추출."""
    clean = FENCE_RE.sub("", body)
    lines = clean.split("\n")
    quotes = []
    i = 0
    while i < len(lines):
        if QUOTE_HEAD_RE.match(lines[i]):
            qlines = []
            j = i + 1
            while j < len(lines) and lines[j].startswith(">"):
                qlines.append(re.sub(r"^>\s?", "", lines[j]))
                j += 1
            quotes.append((i + 1, qlines))
            i = j
        else:
            i += 1
    return quotes


def parse_scheme(schemes_path, paper_type):
    """{step:int → 단계명} — Schemes 파일의 `## Type {L} — ` 표 파싱."""
    letter = TYPE_LETTER.get(paper_type)
    if letter is None:
        return None, "paperType '%s' 은 6유형이 아님" % paper_type
    text = read_text(schemes_path)
    m = re.search(r"^## Type %s — .*?$(.*?)(?=^## |\Z)" % re.escape(letter), text, re.M | re.S)
    if not m:
        return None, "Schemes 에서 'Type %s' 섹션을 찾지 못함" % letter
    steps = {}
    for row in re.finditer(r"^\|\s*(\d{1,2})\s*\|([^|]+)\|", m.group(1), re.M):
        try:
            steps[int(row.group(1))] = row.group(2).strip()
        except ValueError:
            continue
    if len(steps) < 12:
        return None, "Type %s 표에서 12단을 다 읽지 못함 (%d개)" % (letter, len(steps))
    return steps, None


def norm_stepname(s):
    return re.sub(r"\s+", " ", nfc(str(s)).strip().upper())


def main():
    ap = argparse.ArgumentParser(description="Paper Ingest P-7 기계 검증")
    ap.add_argument("folder", help="40. Paper Analyses/{citekey} 폴더 경로")
    ap.add_argument("--vault", default=None, help="볼트 루트 (기본: 폴더의 2단계 상위)")
    args = ap.parse_args()

    folder = os.path.abspath(args.folder)
    if not os.path.isdir(folder):
        print("ERROR: 폴더가 없음 — %s" % folder)
        sys.exit(2)
    vault = os.path.abspath(args.vault) if args.vault else os.path.dirname(os.path.dirname(folder))
    schemes_path = os.path.join(vault, "90. Settings", "Templates", "12-Step Analysis Schemes.md")
    index_path = os.path.join(vault, "index.md")
    if not os.path.isfile(schemes_path):
        print("ERROR: Schemes 파일을 찾지 못함 — %s (--vault 로 볼트 루트 지정)" % schemes_path)
        sys.exit(2)

    md_files = sorted(f for f in os.listdir(folder) if f.endswith(".md"))
    hubs = [f for f in md_files if f.endswith(" - S00 Hub.md")]
    if len(hubs) != 1:
        print("ERROR: 허브 (`* - S00 Hub.md`) 가 %d개 — 정확히 1개여야 함" % len(hubs))
        sys.exit(2)
    hub_file = hubs[0]
    hub_stem = nfc(hub_file[:-3])
    hub_prefix = nfc(hub_file[: -len(" - S00 Hub.md")])  # "{Surname} {Year}"
    atom_files = [f for f in md_files if f != hub_file]
    atom_stems = {nfc(f[:-3]) for f in atom_files}

    errors = []   # (검사 번호, 메시지)
    def err(check, msg):
        errors.append((check, msg))

    # ---------- [1] YAML 실파서 전수 ----------
    fms, bodies = {}, {}
    yaml_ok = 0
    for f in md_files:
        text = read_text(os.path.join(folder, f))
        fm, e = parse_frontmatter(text)
        if e:
            err(1, "%s — %s" % (f, e))
        else:
            yaml_ok += 1
        fms[f] = fm or {}
        bodies[f] = body_of(text)

    hub_fm = fms[hub_file]
    paper_type = str(hub_fm.get("paperType", "")).strip()

    # ---------- 스킴 로드 ----------
    steps, e = parse_scheme(schemes_path, paper_type)
    if e:
        print("ERROR: %s" % e)
        sys.exit(2)

    # ---------- Raw Source 해석 ----------
    src_val = hub_fm.get("source")
    src_names = wikilink_targets(" ".join(src_val)) if isinstance(src_val, list) else wikilink_targets(str(src_val or ""))
    raw_path = None
    for name in src_names:
        hits = globmod.glob(os.path.join(vault, "10. Raw Sources", "**", name + ".md"), recursive=True)
        if hits:
            raw_path = hits[0]
            break
    if raw_path is None:
        print("ERROR: 허브 source 의 Raw Source 를 `10. Raw Sources/**` 에서 찾지 못함 — %s" % src_names)
        sys.exit(2)
    raw_text = read_text(raw_path)
    oc_match = re.search(r"^## Original Content\s*$", raw_text, re.M)
    if not oc_match:
        print("ERROR: Raw Source 에 `## Original Content` 섹션이 없음 — %s" % raw_path)
        sys.exit(2)
    original = raw_text[oc_match.end():]
    original_norm = norm_ws(original)

    # ---------- [2] v6 키 + 좌표 ----------
    n_stub = 0
    v6_ok = 0
    if str(hub_fm.get("type", "")) != "paper-hub":
        err(2, "%s — type 이 paper-hub 가 아님" % hub_file)
    if not hub_fm.get("citekey"):
        err(2, "%s — citekey 없음" % hub_file)
    if "targetManuscript" not in hub_fm:
        err(2, "%s — targetManuscript 없음 (none 이라도 명시)" % hub_file)
    for f in atom_files:
        fm = fms[f]
        ok = True
        if str(fm.get("type", "")) != "paper-analysis":
            err(2, "%s — type 이 paper-analysis 가 아님" % f); ok = False
        if str(fm.get("paperType", "")).strip() != paper_type:
            err(2, "%s — paperType 이 허브(%s)와 불일치" % (f, paper_type)); ok = False
        m = STEP_IN_NAME_RE.search(f)
        fname_step = int(m.group(1)) if m else None
        if fname_step is None:
            err(2, "%s — 파일명에 ' - S{NN} ' 좌표 없음" % f); ok = False
        try:
            fm_step = int(fm.get("analysisStep"))
        except (TypeError, ValueError):
            err(2, "%s — analysisStep 이 정수가 아님: %r" % (f, fm.get("analysisStep"))); ok = False
            fm_step = None
        if fm_step is not None:
            if not (2 <= fm_step <= 12):
                err(2, "%s — analysisStep %d 은 2~12 밖" % (f, fm_step)); ok = False
            if fname_step is not None and fm_step != fname_step:
                err(2, "%s — analysisStep %s ≠ 파일명 S%02d" % (f, fm_step, fname_step)); ok = False
            expected = steps.get(fm_step)
            if expected and norm_stepname(fm.get("analysisStepName", "")) != norm_stepname(expected):
                err(2, "%s — analysisStepName %r ≠ 스킴 %r" % (f, fm.get("analysisStepName"), expected)); ok = False
        hub_links = wikilink_targets(str(fm.get("paperHub", "")))
        if hub_stem not in hub_links:
            err(2, "%s — paperHub 가 허브를 가리키지 않음: %r" % (f, fm.get("paperHub"))); ok = False
        if not fm.get("source"):
            err(2, "%s — source 없음" % f); ok = False
        status = str(fm.get("status", "")).strip()
        if status not in ("completed", "stub"):
            err(2, "%s — status 는 completed/stub 여야 함: %r" % (f, status)); ok = False
        if status == "stub":
            n_stub += 1
        if ok:
            v6_ok += 1

    # ---------- [3] Analysis Context + 필수 섹션 / [4] 가로 연결 / [5] 인용 ----------
    ctx_ok = sec_ok = lat_ok = 0
    n_completed = 0
    q_total = q_pass = q_linemode = 0
    for f in atom_files:
        body = bodies[f]
        fm = fms[f]
        is_stub = str(fm.get("status", "")).strip() == "stub"
        try:
            step = int(fm.get("analysisStep"))
        except (TypeError, ValueError):
            step = None

        # [3a] Analysis Context — stub 포함 전 원자 필수
        if re.search(r"\[!info\]\s*Analysis Context", body):
            ctx_ok += 1
        else:
            err(3, "%s — Analysis Context 콜아웃 없음" % f)

        if is_stub:
            continue  # [9] stub 완화: [3b]~[5] 면제
        n_completed += 1

        # [3b] 필수 섹션 (S12 완화)
        titles = [t for t, _ in h2_sections(body)]
        required = S12_REQUIRED_SECTIONS if step == 12 else REQUIRED_SECTIONS
        missing = [p for p in required if not any(t.startswith(p) for t in titles)]
        if missing:
            err(3, "%s — 필수 섹션 누락: %s" % (f, ", ".join(missing)))
        else:
            sec_ok += 1

        # [4] 가로 연결 — 개념 관계 섹션에 비-허브 형제 원자 링크 ≥1
        rel = section_content(body, "개념 관계")
        siblings = [t for t in wikilink_targets(rel or "") if t in atom_stems and t != nfc(f[:-3])]
        if rel is None:
            err(4, "%s — `## 개념 관계` 섹션 없음" % f)
        elif not siblings:
            err(4, "%s — 개념 관계에 비-허브 원자 링크 0개 (가로 연결 실패)" % f)
        else:
            lat_ok += 1

        # [5] 인용 전수 verbatim
        for lineno, qlines in extract_quotes(body):
            q_total += 1
            joined = strip_quote_marks("\n".join(qlines))
            if not joined:
                err(5, "%s:%d — 빈 quote 콜아웃" % (f, lineno))
                continue
            if norm_ws(joined) in original_norm:
                q_pass += 1
                continue
            # 줄 단위 폴백 (PDF 개행 분절 대응)
            checked, failed = 0, None
            for ln in qlines:
                lnorm = norm_ws(strip_quote_marks(ln))
                if len(lnorm) < 12:
                    continue
                checked += 1
                if lnorm not in original_norm:
                    failed = lnorm
                    break
            if checked and failed is None:
                q_pass += 1
                q_linemode += 1
            else:
                snippet = (failed or norm_ws(joined))[:70]
                err(5, "%s:%d — verbatim 불일치: “%s…”" % (f, lineno, snippet))

    # ---------- [6] Catalog ↔ files + Step Map + 잔존물 ----------
    hub_body = bodies[hub_file]
    catalog = section_content(hub_body, "Atom Catalog")
    coverage = section_content(hub_body, "Coverage Map")
    stepmap = section_content(hub_body, "Step Map")
    if catalog is None:
        err(6, "허브에 `## Atom Catalog` 섹션 없음")
    if coverage is None:
        err(7, "허브에 `## Coverage Map` 섹션 없음")

    cat_links = {t for t in wikilink_targets(catalog or "") if t.startswith(hub_prefix + " - S")}
    for stem in sorted(atom_stems - cat_links):
        err(6, "파일이 Atom Catalog 에 없음 — %s" % stem)
    for link in sorted(cat_links - atom_stems):
        err(6, "Atom Catalog 링크가 실제 파일에 없음 — %s" % link)
    cov_links = {t for t in wikilink_targets(coverage or "") if t.startswith(hub_prefix + " - S")}
    for link in sorted(cov_links - cat_links):
        err(6, "Coverage Map 원자가 Atom Catalog 에 없음 — %s" % link)
    for link in sorted(cov_links - atom_stems):
        err(6, "Coverage Map 링크가 실제 파일에 없음 — %s" % link)

    per_step = {}
    for f in atom_files:
        m = STEP_IN_NAME_RE.search(f)
        if m:
            per_step[int(m.group(1))] = per_step.get(int(m.group(1)), 0) + 1
    if stepmap:
        for row in re.finditer(r"^\|\s*(\d{1,2})\s*\|[^|]*\|([^|]*)\|([^|]*)\|", stepmap, re.M):
            s = int(row.group(1))
            atoms_cell, status_cell = row.group(2).strip(), row.group(3).strip()
            if "planned" in status_cell:
                err(6, "Step Map S%02d 가 아직 `planned` — 컴파일 미완 (P-3b/P-6 미실행)" % s)
            if s >= 2 and re.fullmatch(r"\d+", atoms_cell):
                actual = per_step.get(s, 0)
                if int(atoms_cell) != actual:
                    err(6, "Step Map S%02d Atoms %s ≠ 실제 파일 %d" % (s, atoms_cell, actual))
    if re.search(r"\[!note\]\s*Compile Plan", hub_body):
        err(6, "허브에 임시 `[!note] Compile Plan` 콜아웃 잔존 — P-6 에서 삭제해야 함")

    # ---------- [7] Coverage Map 원문 섹션 전수 ----------
    headings = [(len(m.group(1)), m.group(2).strip()) for m in HEADING_RE.finditer(original)]
    numbered = {}
    for _, t in headings:
        m = re.match(r"^(\d+(?:\.\d+)*)[.)\s]", t)
        if m:
            numbered[m.group(1).rstrip(".")] = t
    parents = {num for num in numbered if any(o != num and o.startswith(num + ".") for o in numbered)}
    title_norm = norm_heading(headings[0][1]) if headings and headings[0][0] == 1 else None
    coverage_norm = norm_heading(coverage or "")

    def covered(tn):
        """전체 일치 우선, 실패 시 접두사 (≥2단어·≥8자) — 허브의 긴 섹션명 축약 표기 허용."""
        if tn in coverage_norm:
            return "full"
        words = tn.split()
        for k in range(len(words) - 1, 1, -1):
            prefix = " ".join(words[:k])
            if len(prefix) >= 8 and prefix in coverage_norm:
                return "prefix"
        return None

    cov_required = cov_found = cov_prefix = 0
    for level, t in headings:
        tn = norm_heading(t)
        if not tn or tn in EXEMPT_HEADINGS:
            continue
        if title_norm and tn == title_norm:
            continue  # 변환된 논문 제목 헤딩
        m = re.match(r"^(\d+(?:\.\d+)*)[.)\s]", t)
        if m and m.group(1).rstrip(".") in parents:
            continue  # 부모 섹션 — 자식이 대신 등장하면 됨
        cov_required += 1
        mode = covered(tn)
        if mode:
            cov_found += 1
            if mode == "prefix":
                cov_prefix += 1
        else:
            err(7, "원문 섹션이 Coverage Map 에 없음 — “%s”" % t)

    # ---------- [8] index.md 허브-단독 등재 ----------
    idx_ok = True
    if os.path.isfile(index_path):
        idx = nfc(read_text(index_path))
        if hub_stem not in idx:
            err(8, "index.md 에 허브 [[%s]] 미등재" % hub_stem)
            idx_ok = False
        leaked = sorted(s for s in atom_stems if s in idx)
        for s in leaked:
            err(8, "index.md 에 원자 노트 노출 (허브-단독 규칙 위반) — %s" % s)
            idx_ok = False
    else:
        err(8, "index.md 를 찾지 못함 — %s" % index_path)
        idx_ok = False

    # ---------- [9] provenance (model + effort) — 허브 + 전 원자 ----------
    prov_ok = 0
    for f in md_files:
        fm = fms[f]
        missing = [k for k in ("model", "effort") if not str(fm.get(k, "")).strip()]
        if missing:
            err(9, "%s — provenance 누락: %s (v6 요건: 에이전트 작성 콘텐츠는 model+effort 필수)"
                % (f, ", ".join(missing)))
        else:
            prov_ok += 1

    # ---------- 리포트 ----------
    n_atoms = len(atom_files)
    print("=== P-7 VERIFY: %s ===" % os.path.basename(folder))
    print("Hub: %s · paperType: %s · citekey: %s" % (hub_file, paper_type, hub_fm.get("citekey")))
    print("Raw Source: %s" % os.path.relpath(raw_path, vault))
    print("Atoms: %d (completed %d / stub %d)" % (n_atoms, n_atoms - n_stub, n_stub))
    print()
    print("[1] YAML 실파서      : %d/%d OK" % (yaml_ok, len(md_files)))
    print("[2] v6 키 + 좌표     : %d/%d OK" % (v6_ok, n_atoms))
    print("[3] Analysis Context : %d/%d OK · 필수 섹션 %d/%d OK (S12 완화·stub 면제)"
          % (ctx_ok, n_atoms, sec_ok, n_completed))
    print("[4] 가로 연결        : %d/%d OK" % (lat_ok, n_completed))
    print("[5] 인용 verbatim    : %d/%d OK (전수%s)"
          % (q_pass, q_total, " · 줄-폴백 %d" % q_linemode if q_linemode else ""))
    print("[6] Catalog ↔ files : catalog %d · files %d · coverage-원자 %d" % (len(cat_links), n_atoms, len(cov_links)))
    print("[7] Coverage 섹션    : %d/%d OK%s"
          % (cov_found, cov_required, " · 접두사-매칭 %d" % cov_prefix if cov_prefix else ""))
    print("[8] index.md         : %s" % ("hub-단독 등재 OK" if idx_ok else "위반"))
    print("[9] provenance       : %d/%d OK (model+effort)" % (prov_ok, len(md_files)))
    print()
    if errors:
        print("---- 오류 %d건 ----" % len(errors))
        for check, msg in errors:
            print("  [%d] %s" % (check, msg))
        print()
        print("RESULT: FAIL (%d errors)" % len(errors))
    else:
        print("RESULT: ALL PASS")
    print()
    print("--- log.md 요약 블록 ---")
    print("p7_verify: %s — atoms %d (stub %d) · quotes %d/%d verbatim · provenance %d/%d · catalog↔files %s · coverage %d/%d · index %s"
          % ("ALL PASS" if not errors else "FAIL(%d)" % len(errors),
             n_atoms, n_stub, q_pass, q_total,
             prov_ok, len(md_files),
             "일치" if not any(c == 6 for c, _ in errors) else "불일치",
             cov_found, cov_required,
             "hub-only" if idx_ok else "위반"))
    sys.exit(0 if not errors else 1)


if __name__ == "__main__":
    main()
