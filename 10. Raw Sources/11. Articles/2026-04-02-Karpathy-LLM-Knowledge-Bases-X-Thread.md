---
type: raw-source
aliases:
  - Karpathy LLM Knowledge Bases
  - LLM Knowledge Bases Tweet
  - Karpathy X Thread 2026-04-02
description: Andrej Karpathy's original X (Twitter) thread from 2026-04-02 introducing the LLM Knowledge Bases pattern. Predates the longer Gist version (2026-04-06) by four days. Includes notable replies from Yohan Koo (CMDS), kepano (Obsidian CEO — contamination mitigation framing), and Beomsu (qmd user confirmation).
author:
  - Andrej Karpathy
  - Yohan Koo
  - kepano
  - Beomsu
date created: 2026-04-14T14:00
date modified: 2026-04-14T14:00
date ingested: 2026-04-14T14:00
tags:
  - raw-source
  - llm-wiki
  - karpathy
  - knowledge-management
  - x-twitter
  - contamination-mitigation
  - qmd
source: "https://x.com/karpathy/status/2039805659525644595"
category: Articles
status: ingested
---

# Karpathy — LLM Knowledge Bases (X Thread)

> [!info] Origin
> This is the **original X post** (2026-04-02) where Karpathy first shared the LLM Knowledge Bases pattern. The [[2026-04-12-Karpathy-LLM-Wiki|longer Gist version]] was published four days later (2026-04-06) with the same core ideas expanded.

> [!note] Category Override
> Auto-routed to `04. Clippings` by Web Clipper (X/Twitter trigger), but re-categorized to **Articles** because the 825-word thread is structurally a long-form essay companion to the existing Karpathy gist.

---

## Metadata

| Field | Value |
|-------|-------|
| Author | Andrej Karpathy (@karpathy) |
| Authority | Stanford, 2.2M followers, joined 2009, Tesla AI Director / OpenAI founding |
| Posted | 2026-04-02T20:42:21Z |
| Word Count | 825 |
| Replies Captured | Yohan Koo, kepano (Steph Ango), Beomsu |
| URL | https://x.com/karpathy/status/2039805659525644595 |

---

## Original Content

### @karpathy (2026-04-02) — Root Post

LLM Knowledge Bases

Something I'm finding very useful recently: using LLMs to build personal knowledge bases for various topics of research interest. In this way, a large fraction of my recent token throughput is going less into manipulating code, and more into manipulating knowledge (stored as markdown and images). The latest LLMs are quite good at it.

**Data ingest**:
I index source documents (articles, papers, repos, datasets, images, etc.) into a `raw/` directory, then I use an LLM to incrementally "compile" a wiki, which is just a collection of .md files in a directory structure. The wiki includes summaries of all the data in `raw/`, backlinks, and then it categorizes data into concepts, writes articles for them, and links them all. To convert web articles into .md files I like to use the Obsidian Web Clipper extension, and then I also use a hotkey to download all the related images to local so that my LLM can easily reference them.

**IDE**:
I use Obsidian as the IDE "frontend" where I can view the raw data, the compiled wiki, and the derived visualizations. Important to note that the LLM writes and maintains all of the data of the wiki, I rarely touch it directly. I've played with a few Obsidian plugins to render and view data in other ways (e.g. Marp for slides).

**Q&A**:
Where things get interesting is that once your wiki is big enough (e.g. mine on some recent research is **~100 articles and ~400K words**), you can ask your LLM agent all kinds of complex questions against the wiki, and it will go off, research the answers, etc. I thought I had to reach for fancy RAG, but the LLM has been pretty good about auto-maintaining index files and brief summaries of all the documents and it reads all the important related data fairly easily at this ~small scale.

**Output**:
Instead of getting answers in text/terminal, I like to have it render markdown files for me, or slide shows (Marp format), or matplotlib images, all of which I then view again in Obsidian. You can imagine many other visual output formats depending on the query. Often, I end up "filing" the outputs back into the wiki to enhance it for further queries. So my own explorations and queries always "add up" in the knowledge base.

**Linting**:
I've run some LLM "health checks" over the wiki to e.g. find inconsistent data, impute missing data (with web searchers), find interesting connections for new article candidates, etc., to incrementally clean up the wiki and enhance its overall data integrity. The LLMs are quite good at suggesting further questions to ask and look into.

**Extra tools**:
I find myself developing additional tools to process the data, e.g. I vibe coded a small and naive search engine over the wiki, which I both use directly (in a web UI), but more often I want to hand it off to an LLM via CLI as a tool for larger queries.

**Further explorations**:
As the repo grows, the natural desire is to also think about **synthetic data generation + finetuning** to have your LLM "know" the data in its weights instead of just context windows.

**TLDR**: raw data from a given number of sources is collected, then compiled by an LLM into a .md wiki, then operated on by various CLIs by the LLM to do Q&A and to incrementally enhance the wiki, and all of it viewable in Obsidian. You rarely ever write or edit the wiki manually, it's the domain of the LLM. I think there is room here for an incredible new product instead of a hacky collection of scripts.

---

### @YohanKoo (2026-04-02) — Self-verification Reply

This resonates deeply. I've been running a 10,000+ note Obsidian vault (CMDS) with Claude Code for 3 years, and arrived at nearly identical patterns:

- Your `raw/` → wiki compilation = my Connect → Merge → Develop → Share process
- Your `AGENTS.md` schema = my 5 system files

---

### @kepano (Steph Ango, Obsidian CEO) (2026-04-02) — Contamination Mitigation

I like this approach because it mitigates the contamination risks of agent-generated content in your primary vault... the agents need a playground too!

> I like @karpathy's Obsidian setup as a way to mitigate contamination risks. Keep your personal vault clean and create a messy vault for your agents.
>
> I prefer my personal Obsidian vault to be high signal:noise, and for all the content to have known origins.
>
> Keeping a separation.

---

### @BeromArtDev (Beomsu, 2026-04-03) — qmd Adoption Signal

Yeah, recently I've been using Claude Code with Obsidian — collaborating with my past self. I also use @tobi's QMD for exploration. It's been surprisingly impactful. Sometimes I discover ideas that directly help with my current tasks. The more context we accumulate, the more [signal].

---

## Compilation Notes

Key new insights vs. the 2026-04-12 Gist (already ingested):

1. **Timeline**: X post preceded gist by 4 days. The pattern was first crowd-tested on X.
2. **Scale data point**: `~100 articles / ~400K words` — Karpathy's own deployment size.
3. **Synthetic data generation + finetuning**: Forward-looking extension not fully explored in the gist.
4. **kepano's contamination mitigation framing**: Agents contaminate primary vaults; solution is separate "messy" playground vault. This is the philosophical justification for satellite vault patterns.
5. **qmd real-world usage**: Beomsu's reply confirms qmd adoption beyond Karpathy's endorsement.
