---
tags: [codex, install, setup]
---

# Install And Sync

## Human steps

1. Copy `.codex/agents/*.toml` to `~/.codex/agents/`.
2. Copy `.agents/skills/*` to `~/.agents/skills/`.
3. Copy `.codex/config.toml` to `~/.codex/config.codex-helper.example.toml`.
4. Optionally append `templates/global-AGENTS.md` into `~/.codex/AGENTS.md`.

## Obsidian (no commands)

If someone downloads the ZIP and does not want to run commands:

1. Open the repo folder.
2. Copy the single `for_obsidian/` folder into their Obsidian vault.
3. Open `for_obsidian/00_Home.md` in Obsidian.

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

The exported folder includes full generated catalogs under `for_obsidian/catalog/`.

## Linked views

- [[00_Home]]
- [[08_Repo_Structure]]
- [[90_Markdown_Inventory]]
