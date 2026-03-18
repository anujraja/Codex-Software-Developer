---
tags: [codex, structure]
---

# Repo Structure

```text
Codex-Helper/
├── AGENTS.md
├── README.md
├── .codex/
│   ├── config.toml
│   └── agents/
├── .agents/
│   └── skills/
├── docs/
├── scripts/
├── templates/
└── for_obsidian/
    ├── catalog/
    └── graph/
```

## Why this structure

- `scripts/` keeps installation repeatable.
- `.codex/agents` and `.agents/skills` keep reusable runtime assets versioned.
- `for_obsidian/` keeps a copy-ready knowledge map in one folder.
- `for_obsidian/catalog/` contains full generated catalogs (agents, subagents, skills, prompts, capability matrix).
- `for_obsidian/graph/` contains highly connected graph nodes (agents, skills, prompts, roles, systems, languages, playbooks).
