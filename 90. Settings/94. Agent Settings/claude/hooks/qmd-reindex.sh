#!/usr/bin/env bash
# qmd auto-reindex hook for CMDS LLM Wiki
# Triggered by PostToolUse after Write/Edit in this vault.
# Runs qmd update + embed in background so the main session doesn't block.
# Debounced via lock file — burst writes collapse into one reindex.

set -euo pipefail

VAULT="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "$0")/../.." && pwd)}"
LOCK="/tmp/qmd-reindex-cmds-llm-wiki.lock"
LOG="/tmp/qmd-reindex-cmds-llm-wiki.log"
DEBOUNCE_SEC=8

# Read Claude Code hook payload from stdin
payload=$(cat 2>/dev/null || echo "{}")
file_path=$(echo "$payload" | /usr/bin/jq -r '.tool_input.file_path // empty' 2>/dev/null || echo "")

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

# Spawn background worker only if not already running.
# Stale-lock guard: a worker killed mid-run (reboot, kill, qmd failure under set -e)
# leaves .running behind — treat locks older than 10 min as dead and reclaim.
if [[ -f "$LOCK.running" ]]; then
	if [[ -n "$(find "$LOCK.running" -mmin +10 2>/dev/null)" ]]; then
		rm -f "$LOCK.running"
	else
		exit 0
	fi
fi

(
	touch "$LOCK.running"
	# Ensure lock cleanup on any exit path (incl. qmd failure aborting via set -e)
	trap 'rm -f "$LOCK.running" "$LOCK.request"' EXIT
	# Wait for burst of writes to settle.
	# NOTE: BSD/macOS syntax — options before the format operand
	# (`date +%s -r FILE` is GNU order and silently fails on macOS).
	last=""
	while [[ "$(date -r "$LOCK.request" +%s 2>/dev/null)" != "$last" ]]; do
		last="$(date -r "$LOCK.request" +%s 2>/dev/null)"
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
	# trap EXIT handles lock cleanup (covers qmd failure paths too)
) >/dev/null 2>&1 &

disown 2>/dev/null || true
exit 0
