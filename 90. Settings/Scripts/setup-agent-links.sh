#!/usr/bin/env bash
# setup-agent-links.sh — recreate the agent dotfolder symlinks for this vault.
#
# The canonical agent settings live in a normal (synced) folder:
#   90. Settings/94. Agent Settings/{claude,codex,agents}/
# and the dotfolders point at it with RELATIVE symlinks:
#   .claude/commands -> ../90. Settings/94. Agent Settings/claude/commands
#   .claude/hooks    -> ../90. Settings/94. Agent Settings/claude/hooks
#   .codex/commands  -> ../90. Settings/94. Agent Settings/codex/commands
#   .codex/hooks     -> ../90. Settings/94. Agent Settings/codex/hooks
#   .agents/skills   -> ../90. Settings/94. Agent Settings/agents/skills
#
# Run it once per machine, or again whenever the links are missing
# (ZIP downloads, Windows checkouts, Obsidian Sync copies can flatten them).
# Safe to re-run: correct links are left alone, stray copies are backed up.
#
# Usage:  bash "90. Settings/Scripts/setup-agent-links.sh" [--check]
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
VAULT="$(cd "$SCRIPT_DIR/../.." && pwd -P)"
cd "$VAULT"

CANON="90. Settings/94. Agent Settings"
CHECK_ONLY=0
[[ "${1:-}" == "--check" ]] && CHECK_ONLY=1

# "<link path>|<canonical path relative to vault root>"
LINKS=(
	".claude/commands|$CANON/claude/commands"
	".claude/hooks|$CANON/claude/hooks"
	".codex/commands|$CANON/codex/commands"
	".codex/hooks|$CANON/codex/hooks"
	".agents/skills|$CANON/agents/skills"
)

stamp="$(date +%Y%m%d-%H%M%S)"
problems=0

for entry in "${LINKS[@]}"; do
	link="${entry%%|*}"
	target="${entry#*|}"
	parent="$(dirname "$link")"
	rel="../$target"

	if [[ ! -d "$target" ]]; then
		if [[ -d "$link" && ! -L "$link" ]]; then
			# Old layout: real folder in the dotfolder, no canonical copy yet.
			if (( CHECK_ONLY )); then
				echo "MIGRATE  $link -> $target (canonical missing)"; problems=$((problems + 1)); continue
			fi
			mkdir -p "$(dirname "$target")"
			mv "$link" "$target"
			echo "moved    $link -> $target"
		else
			echo "MISSING  $target (canonical folder not found — did Sync/ZIP bring it?)" >&2
			problems=$((problems + 1)); continue
		fi
	fi

	if [[ -L "$link" && "$(readlink "$link")" == "$rel" ]]; then
		echo "ok       $link"
		continue
	fi

	if (( CHECK_ONLY )); then
		echo "FIX      $link (should link to $rel)"; problems=$((problems + 1)); continue
	fi

	mkdir -p "$parent"
	if [[ -L "$link" ]]; then
		rm "$link"
	elif [[ -d "$link" ]]; then
		if diff -rq -x .DS_Store "$link" "$target" >/dev/null 2>&1; then
			rm -rf "$link"
		else
			mv "$link" "${link}_backup-$stamp"
			echo "backup   $link -> ${link}_backup-$stamp (differs from canonical — merge by hand, then delete)"
		fi
	elif [[ -e "$link" ]]; then
		# A flattened symlink (plain text file holding the path).
		rm "$link"
	fi
	ln -s "$rel" "$link"
	echo "linked   $link -> $rel"
done

# Obsidian Sync and ZIP extraction can drop the executable bit.
if (( ! CHECK_ONLY )); then
	for hooks in "$CANON/claude/hooks" "$CANON/codex/hooks"; do
		[[ -d "$hooks" ]] && find "$hooks" -name '*.sh' -exec chmod +x {} +
	done
fi

for hooks in .claude/hooks .codex/hooks; do
	for f in "$hooks"/*.sh; do
		[[ -e "$f" ]] || continue
		[[ -x "$f" ]] || { echo "NOT EXEC $f" >&2; problems=$((problems + 1)); }
	done
done

if (( problems )); then
	echo "Done with $problems problem(s)." >&2
	exit 1
fi
echo "All agent links are in place."
