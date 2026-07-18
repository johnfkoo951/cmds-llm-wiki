**English** · [한국어](README.ko.md)

# cmds-llm-wiki

> **An LLM Wiki vault template** — Karpathy's LLM Wiki pattern + a letter to your future self + a dual Claude Code · Codex harness.
>
> It's both an Obsidian vault and a Claude Code / Codex project. An LLM compiles external sources (articles, papers, transcripts) into a persistent wiki that compounds over time.

**🌐 Live Showcase**: **[llm-wiki.cmdspace.work](https://llm-wiki.cmdspace.work)** — a 10-section deep-dive page (architecture · 11 commands · letter to your future self · Quick Start)

**Built by**: Yohan Koo ([@YohanKoo](https://x.com/YohanKoo)) · templatized from a satellite vault running in production at CMDSPACE

---

## Try it in 5 minutes

Want to see the pattern work before committing to a full setup? The repo ships with example content (Karpathy's LLM Wiki, ingested), so you can explore immediately:

```bash
cd ~/DEV
git clone https://github.com/johnfkoo951/cmds-llm-wiki.git my-llm-wiki
cd my-llm-wiki
claude
```

Then run these commands in order:

1. `/status` — check the current state of the vault
2. `/ingest <URL>` — ingest an article you care about (answer the "why am I collecting this?" prompt)
3. `/query <question>` — ask your first question against the accumulated wiki
4. `/lint` — run a health check

Filling in placeholders, Core Context, and installing qmd (the local search engine) are all part of the full setup below — they make the vault *yours*, but you don't need them just to see how ingest → query → lint feels.

---

## What it is

- **A runnable starter kit for Karpathy's LLM Wiki pattern**
  - 3-layer flow: Raw Sources (immutable) → Wiki (LLM-maintained) → Schema (rules)
  - 3 operations: Ingest · Query · Lint
  - Two core files: `index.md` + `log.md`
- **A letter to your future self** — `/ingest` forces the "why am I collecting this?" purpose question up front, so you accumulate intent instead of fragments
- **A dual Claude Code + Codex harness**
  - 11 slash commands (`/ingest`, `/query`, `/lint`, `/inbox`, `/status`, `/reindex`, `/refresh-context`, `/onboard`, `/capture-tabs`, `/verify`, `/audit`)
  - 2 PostToolUse hooks (raw-source verbatim verification + qmd auto-reindex)
  - **Codex mirror**: `.codex/commands/` (10) + `.agents/skills/` (10) + `AGENTS.md` — run the same operations identically from Codex, Cursor, Windsurf, and other agents
  - 18 Obsidian Web Clipper JSON templates (Article / YouTube / Substack / X / arXiv / Stibee, and more)
  - 73 Obsidian hotkey bindings (`.obsidian/hotkeys.json`) — heading shortcuts, wikilink/callout insertion, sidebar toggles, and so on
- **Optional mothership vault integration** — if you already have a separate PKM vault, you can run this as a satellite of it

---

## Sources & credits

| Source | Link |
|---|---|
| **Andrej Karpathy — LLM Wiki Gist** | https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f |
| **Karpathy X thread** (2026-04-02) | https://x.com/karpathy/status/1... (an example is included under `10. Raw Sources/11. Articles/` in this repo) |
| **kepano (Steph Ango, Obsidian CEO)** — contamination mitigation | the idea of separating the agent playground from your personal vault |
| **cmds-system-files** (the sibling repo for the mothership pattern) | https://github.com/johnfkoo951/cmds-system-files |

## Related repos

- **[cmds-system-files](https://github.com/johnfkoo951/cmds-system-files)** — the CMDS mothership PKM system (100–900 categories + Connect→Merge→Develop→Share). The sibling system that this repo can optionally connect to as its mothership.

---

## Getting started

> **In-depth setup manual**: `90. Settings/Sharing/Setup Guide.md` — covers Mode A/B, one-shot `sed` replacement commands, verification greps, and 7 FAQs. If the 5 steps below aren't enough, keep that document open while you work.

### 1. Clone

```bash
cd ~/DEV
git clone https://github.com/johnfkoo951/cmds-llm-wiki.git my-llm-wiki
cd my-llm-wiki
```

### 2. Open as an Obsidian vault

Obsidian → Open folder as vault → select `my-llm-wiki/`.

### 3. Fill in the placeholders

The placeholders below are scattered across several files. Replace them all at once:

| Placeholder | Value to fill in (example) |
|---|---|
| `{your-name}` | a wikilink-friendly name like `[[Jane Doe]]` |
| `{Your Name}` | `Jane Doe`, a display name |
| `{PATH_TO_YOUR_LLM_WIKI}` | `/Users/foo/DEV/my-llm-wiki` |
| `{PATH_TO_YOUR_MOTHERSHIP_VAULT}` | (optional) path to a separate PKM vault |
| `{your-mothership-vault-name}` | (optional) the mothership folder name |

Bulk replace:
```bash
cd my-llm-wiki
LC_ALL=C find . -name "*.md" -o -name "*.sh" -o -name "*.yml" -o -name "*.json" | xargs sed -i '' \
  -e 's|{your-name}|Jane Doe|g' \
  -e 's|{Your Name}|Jane Doe|g' \
  -e 's|{PATH_TO_YOUR_LLM_WIKI}|/Users/foo/DEV/my-llm-wiki|g'
```

### 4. Fill in Core Context

In `Core Context.md`:
- §1 Identity (name · role · areas of expertise · continuity declaration)
- §2 5–9 reuse axes (where will your knowledge be used?)
- §3–§5 are optional

### 5. qmd (optional, recommended) — the local search engine

```bash
# Install (requires brew)
brew install qmd-search/qmd/qmd

# Copy the config file
cp "90. Settings/qmd-config-template.yml" ~/.config/qmd/index.yml
# Edit {PATH_TO_YOUR_LLM_WIKI} in ~/.config/qmd/index.yml to the real path

# Index
export QMD_EMBED_MODEL="hf:Qwen/Qwen3-Embedding-0.6B-GGUF/Qwen3-Embedding-0.6B-Q8_0.gguf"
qmd update && qmd embed
```

### 6. Obsidian Web Clipper (optional)

Among the 18 `90. Settings/Sharing/clipper-*.json` files, import the site templates you want via Web Clipper Settings → Templates → Import.

### 7. Run Claude Code

```bash
cd my-llm-wiki
claude
```

Recommended order for your first commands:
1. `/status` — check the current state of the vault
2. `/ingest <URL>` — ingest an article you care about (try answering the purpose question)
3. `/query <question>` — run your first query against the accumulated wiki
4. `/lint` — run a health check

---

## Structure

```
cmds-llm-wiki/
├── CLAUDE.md                    # Schema (Claude Code) — LLM behavior rules
├── AGENTS.md                    # Schema (Codex/Cursor/Windsurf) — mirror of CLAUDE.md
├── Core Context.md              # User context (fill in before use)
├── index.md                     # Master index
├── log.md                       # Change history (append-only)
├── README.md                    # This file
├── CHANGELOG.md                 # Template version history
├── LLM-Wiki-Starter-Kit.md      # Lightweight kit for sharing
├── .claude/
│   ├── commands/                # 11 slash commands
│   ├── hooks/                   # 2 PostToolUse hooks
│   └── settings.json
├── .codex/                      # Codex harness (mirror of Claude)
│   ├── commands/                # 10 commands (onboard excluded)
│   ├── hooks/                   # 2 hooks
│   └── hooks.json
├── .agents/
│   └── skills/                  # 10 reusable Codex operation skills
├── .obsidian/
│   └── hotkeys.json             # 73 Obsidian hotkey bindings (optional — delete if not to your taste)
├── 00. Inbox/                   # Web Clipper inbox (subfolders 02–05)
├── 10. Raw Sources/             # Immutable originals (subfolders 11–15)
│   └── 11. Articles/            # includes 2 Karpathy examples
├── 20. Wiki/                    # LLM-maintained wiki
│   ├── 21. Concepts/            # examples (LLM Wiki Pattern, etc.)
│   ├── 22. Entities/            # examples (Karpathy, Bush, Memex)
│   ├── 23. Guides/              # example guides
│   └── 24. Maps/                # example MOCs
├── 30. Queries/                 # synthesized query results (empty folder, filled by /query)
├── 80. References/Attachments/  # all images centralized here
└── 90. Settings/
    ├── Templates/               # Obsidian note templates (4 types)
    ├── Sharing/                 # 18 Web Clipper JSONs + Setup Guide.md + CLAUDE-Template.md
    └── qmd-config-template.yml  # local search engine config
```

---

## Core conventions

- **YAML 2 SPACES / Body TAB** (never mix the two)
- **Wikilinks in YAML are quoted**: `"[[link]]"`
- **Mermaid labels are double-quoted**: `A["label"]`
- **7 required properties**: `type`, `aliases`, `description` (English, an LLM hint), `author`, `date created`, `date modified`, `tags`
- **ISO 8601 dates**: `YYYY-MM-DD`
- **New YAML keys use camelCase**: `collectionPurpose`, `mainVaultRelated`, `mainVaultCmds`, `reusableFor`

See `CLAUDE.md` for the details.

---

## A note on the example content

`10. Raw Sources/` and `20. Wiki/` contain part of the result of ingesting Karpathy's original LLM Wiki writing, included as an example. These are samples meant **to show how the pattern works**:

- `10. Raw Sources/11. Articles/2026-04-12-Karpathy-LLM-Wiki.md`
- `10. Raw Sources/11. Articles/2026-04-02-Karpathy-LLM-Knowledge-Bases-X-Thread.md`
- `20. Wiki/` — roughly 16 concepts, entities, and MOCs (run `/lint` for the exact count)

Some of the example wiki pages contain **orphan wikilinks** (links to pages that don't exist yet). This is intentional — it demonstrates how the wiki grows and naturally fills in as you repeat `/ingest`.

To start completely empty, delete `10. Raw Sources/11. Articles/*.md` and `20. Wiki/**/*.md`.

---

## License & contributing

- This repo is a **template**. Fork or clone it freely and use it as your own vault.
- Improvement PRs are welcome. Just keep the placeholders intact in template files like `Core Context.md`, `index.md`, and `log.md`.

Built by: [@YohanKoo](https://x.com/YohanKoo) · [CMDSPACE](https://litt.ly/cmds)
- Karpathy's LLM Wiki pattern
- kepano's contamination mitigation idea
- cmds-system-files (the sibling mothership pattern)
