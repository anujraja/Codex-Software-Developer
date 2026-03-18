# Repository Layout

```text
Codex-Helper/
├── .agents/skills/                 # Repo-level skills (Codex discovery source in project)
├── .codex/agents/                  # Custom subagent definitions for ~/.codex/agents
├── docs/                           # Human + Codex-facing operations docs
├── for_obsidian/                   # Copy-ready Obsidian knowledge bundle
├── scripts/                        # Install/sync/export automation scripts
├── templates/                      # Reusable template snippets
├── AGENTS.md                       # Repo-level Codex routing instructions
└── README.md
```

## Design goal

Keep the repo portable and explicit:
- all runnable operations are script-backed
- all human flows are documented
- all knowledge-map views are Obsidian-ready
- install scripts auto-resolve user skill target:
  - `~/.codex/skills` when present
  - else `~/.agents/skills`
  - or explicit `SKILL_TARGET_DIR` override
