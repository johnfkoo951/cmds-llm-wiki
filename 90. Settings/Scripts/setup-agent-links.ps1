# setup-agent-links.ps1 — Windows version of setup-agent-links.sh.
#
# Recreates the agent dotfolder links that point at the canonical folder
# "90. Settings\94. Agent Settings\{claude,codex,agents}\".
#
# Symbolic links on Windows need Developer Mode (Settings > System > For developers)
# or an elevated PowerShell. Without either, this script falls back to directory
# junctions, which work for folders without special rights (absolute paths only).
#
# Usage (from the vault root or anywhere):
#   powershell -ExecutionPolicy Bypass -File "90. Settings\Scripts\setup-agent-links.ps1"
$ErrorActionPreference = 'Stop'

$Vault = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
Set-Location $Vault
$Canon = '90. Settings\94. Agent Settings'

$Links = @(
	@('.claude\commands', "$Canon\claude\commands"),
	@('.claude\hooks',    "$Canon\claude\hooks"),
	@('.codex\commands',  "$Canon\codex\commands"),
	@('.codex\hooks',     "$Canon\codex\hooks"),
	@('.agents\skills',   "$Canon\agents\skills")
)
$Stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$Problems = 0

foreach ($pair in $Links) {
	$link = $pair[0]; $target = $pair[1]
	$targetAbs = Join-Path $Vault $target
	$linkAbs = Join-Path $Vault $link

	if (-not (Test-Path $targetAbs -PathType Container)) {
		Write-Warning "MISSING  $target (canonical folder not found)"
		$Problems++; continue
	}

	$item = Get-Item $linkAbs -Force -ErrorAction SilentlyContinue
	if ($item -and $item.LinkType) {
		$resolved = [System.IO.Path]::GetFullPath((Join-Path (Split-Path $linkAbs) $item.Target))
		if ($resolved.TrimEnd('\') -eq $targetAbs.TrimEnd('\')) { Write-Host "ok       $link"; continue }
		$item.Delete()
	} elseif ($item -and $item.PSIsContainer) {
		Rename-Item $linkAbs "$(Split-Path $link -Leaf)_backup-$Stamp"
		Write-Host "backup   $link -> ${link}_backup-$Stamp (compare with canonical, then delete)"
	} elseif ($item) {
		# git with core.symlinks=false checks symlinks out as small text files
		Remove-Item $linkAbs -Force
	}

	New-Item -ItemType Directory -Force -Path (Split-Path $linkAbs) | Out-Null
	$relative = '..\' + $target
	try {
		New-Item -ItemType SymbolicLink -Path $linkAbs -Target $relative | Out-Null
		Write-Host "linked   $link -> $relative"
	} catch {
		New-Item -ItemType Junction -Path $linkAbs -Target $targetAbs | Out-Null
		Write-Host "junction $link -> $targetAbs (no symlink rights; junction is fine for folders)"
	}
}

if ($Problems) { Write-Error "Done with $Problems problem(s)."; exit 1 }
Write-Host 'All agent links are in place.'
Write-Host 'Hooks are bash scripts: on Windows run them through Git Bash or WSL.'
