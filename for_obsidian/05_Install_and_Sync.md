---
tags: [codex, install, setup]
---

# Install And Sync

## Human steps

1. Copy `.codex/agents/*.toml` to `~/.codex/agents/`.
2. Copy `.agents/skills/*` to `~/.agents/skills/`.
3. Copy `.codex/config.toml` to `~/.codex/config.codex-helper.example.toml`.
4. Optionally append `templates/global-AGENTS.md` into `~/.codex/AGENTS.md`.

## Script steps

```bash
./scripts/install_codex_helper.sh
./scripts/install_codex_helper.sh --with-global-guidance
./scripts/install_codex_helper.sh --force
```

## Symlink mode

```bash
./scripts/link_codex_helper.sh
```

## Obsidian export

```bash
./scripts/export_obsidian_bundle.sh "/path/to/ObsidianVault"
./scripts/export_obsidian_bundle.sh --force "/path/to/ObsidianVault"
```

## Linked views

- [[00_Home]]
- [[08_Repo_Structure]]
- [[90_Markdown_Inventory]]
