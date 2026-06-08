#!/usr/bin/env bash
# qmd auto-reindex hook for CMDS LLM Wiki
# Triggered by PostToolUse after Write/Edit in this vault.
# Runs qmd update + embed in background so the main session doesn't block.
# Debounced via lock file — burst writes collapse into one reindex.

set -euo pipefail

VAULT="{PATH_TO_YOUR_LLM_WIKI}"
LOCK="/tmp/qmd-reindex-cmds-llm-wiki.lock"
LOG="/tmp/qmd-reindex-cmds-llm-wiki.log"
DEBOUNCE_SEC=8

# Read agent hook payload from stdin. Supports Claude Code-style PostToolUse
# payloads and simple Codex-style file path payloads.
payload=$(cat 2>/dev/null || echo "{}")
file_path=$(echo "$payload" | /usr/bin/jq -r '.tool_input.file_path // .tool_input.path // .file_path // .path // empty' 2>/dev/null || echo "")

# Only reindex when a markdown file inside the vault was touched
case "$file_path" in
	"$VAULT"/*.md) ;;
	"$VAULT"/*/*.md) ;;
	*) exit 0 ;;
esac

# Skip Inbox changes (pre-ingest staging — not indexed)
case "$file_path" in
	*"/00. Inbox/"*) exit 0 ;;
esac

# Debounce: if a reindex worker is already queued, bump its timer
touch "$LOCK.request"

# Spawn background worker only if not already running
if [[ -f "$LOCK.running" ]]; then
	exit 0
fi

(
	touch "$LOCK.running"
	# Wait for burst of writes to settle
	last=""
	while [[ "$(date +%s -r "$LOCK.request" 2>/dev/null)" != "$last" ]]; do
		last="$(date +%s -r "$LOCK.request" 2>/dev/null)"
		sleep "$DEBOUNCE_SEC"
	done

	export QMD_EMBED_MODEL="hf:Qwen/Qwen3-Embedding-0.6B-GGUF/Qwen3-Embedding-0.6B-Q8_0.gguf"
	export PATH="$HOME/.bun/bin:/opt/homebrew/bin:/usr/bin:/bin"

	{
		echo "=== $(date -u +%FT%TZ) qmd auto-reindex ==="
		qmd update 2>&1
		qmd embed 2>&1
		echo "=== done ==="
	} >> "$LOG" 2>&1

	rm -f "$LOCK.running" "$LOCK.request"
) >/dev/null 2>&1 &

disown 2>/dev/null || true
exit 0
