#!/bin/bash
# PostToolUse hook — validates that Raw Source files have a proper ## Original Content section.
#
# Triggered after Write / Edit / MultiEdit on files under `10. Raw Sources/`.
# Exits with code 2 (blocking error) if the raw source is missing verbatim content,
# forcing the active agent to fix it before proceeding.
#
# Rationale: 2026-04-14 session had 2/4 ingests fail to preserve verbatim content.
# Skill text + memory alone proved insufficient — harness enforcement required.

set -e

# Read tool input from stdin. Supports Claude Code-style PostToolUse payloads
# and simple Codex-style file path payloads.
INPUT=$(cat)

# Extract file_path from common tool payload shapes.
FILE_PATH=$(echo "$INPUT" | python3 -c "import sys, json; d = json.load(sys.stdin); ti = d.get('tool_input', {}) if isinstance(d, dict) else {}; print(ti.get('file_path') or ti.get('path') or d.get('file_path') or d.get('path') or '')" 2>/dev/null || echo "")

# Exit quietly if we can't parse or file_path is empty
[ -z "$FILE_PATH" ] && exit 0

# Only check files under `10. Raw Sources/`
if [[ "$FILE_PATH" != *"10. Raw Sources/"* ]]; then
  exit 0
fi

# Skip non-markdown files and .gitkeep
if [[ "$FILE_PATH" != *.md ]] || [[ "$FILE_PATH" == *".gitkeep" ]]; then
  exit 0
fi

# File must exist to validate
if [ ! -f "$FILE_PATH" ]; then
  exit 0
fi

# Check 1: presence of `## Original Content` section
if ! grep -q "^## Original Content" "$FILE_PATH"; then
  cat >&2 <<EOF
[validate-raw-source] BLOCKING: Raw Source is missing the \`## Original Content\` section.

File: $FILE_PATH

Rule (AGENTS.md / CLAUDE.md, /ingest): every Raw Source MUST contain a \`## Original Content\`
section with the verbatim article body — including embedded images (\`![alt](url)\`),
YouTube/video URLs, customer quotes, citations, and code blocks.

Summaries (Core Thesis / Key Takeaways / Key Arguments) belong in the upper sections,
not as a replacement. Raw Sources are the immutable source-of-truth layer.

Fix: append the verbatim article body under a new \`## Original Content\` heading.
If the inbox file is still available, use that. If deleted, retrieve from git:
  git log --all --oneline -- "00. Inbox/..."
  git show <commit>:"<inbox path>" > /tmp/body.md
Then copy the body (excluding Web Clipper frontmatter/preambles) into the raw source.

This hook exists because prior sessions slipped on this rule (2026-04-14: 2/4 ingests).
Memory note, if available, may live under the agent-specific project memory.
EOF
  exit 2
fi

# Book Ingest chapter stubs intentionally preserve TOC metadata before the
# chapter body is read. They still need the heading above, but the body may be
# a placeholder until promotion.
IS_STUB=$(awk 'NR==1 && $0=="---"{fm=1; next} fm && $0=="---"{exit} fm && $0 ~ /^status:[[:space:]]*stub([[:space:]]|$)/{print "yes"; exit}' "$FILE_PATH")
if [ "$IS_STUB" = "yes" ]; then
  exit 0
fi

# Check 2: Original Content section must have substantive body (>20 non-empty lines)
BODY_LINE_COUNT=$(awk '/^## Original Content/{found=1; next} /^## /{if(found) exit} found && NF>0 {count++} END{print count+0}' "$FILE_PATH")

if [ "$BODY_LINE_COUNT" -lt 20 ]; then
  cat >&2 <<EOF
[validate-raw-source] BLOCKING: \`## Original Content\` section has only $BODY_LINE_COUNT non-empty lines — likely just headers/placeholder.

File: $FILE_PATH

Rule: Original Content must be the verbatim article body, not a stub.
For normal articles, expect 50+ lines. For short clippings (X threads etc.), at least the full thread.

Fix: replace the stub with the actual verbatim body from the inbox clipper or WebFetch result.
EOF
  exit 2
fi

# Success
exit 0
