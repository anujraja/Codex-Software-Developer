# Codex Helper

One-repo setup to make a Codex install production-ready quickly.

This repository gives you:
- reusable custom agents (`.codex/agents/*.toml`)
- reusable custom skills (`.agents/skills/*/SKILL.md`)
- safe install/sync scripts
- copy-ready Obsidian knowledge graph notes (`for_obsidian/`)
- routing docs for when to use which agent or skill

## Quick start

```bash
# 1) Clone
git clone <your-new-repo-url> Codex-Helper
cd Codex-Helper

# 2) Install assets into your local Codex home
./scripts/install_codex_helper.sh

# 3) (Optional) append global guidance into ~/.codex/AGENTS.md
./scripts/install_codex_helper.sh --with-global-guidance

# 4) (Optional) update existing installs from repo versions
./scripts/install_codex_helper.sh --force
```

## What gets installed

| Asset | Source in repo | Installed location |
|---|---|---|
| Custom agents | `.codex/agents/*.toml` | `~/.codex/agents/` |
| Custom skills | `.agents/skills/*` | `~/.agents/skills/` |
| Config template | `.codex/config.toml` | `~/.codex/config.codex-helper.example.toml` |
| Global AGENTS guidance (optional) | `templates/global-AGENTS.md` | appended to `~/.codex/AGENTS.md` |

## Obsidian bundle

`for_obsidian/` is designed to be copied as a single folder into an Obsidian vault.

```bash
./scripts/export_obsidian_bundle.sh "/path/to/YourObsidianVault"
# overwrite existing exported folder if needed
./scripts/export_obsidian_bundle.sh --force "/path/to/YourObsidianVault"
```

This creates `YourObsidianVault/Codex-Helper/` with linked notes, tables, and diagrams.

## Human setup steps (no scripts)

1. Copy `.codex/agents/*.toml` to `~/.codex/agents/`.
2. Copy `.agents/skills/*` to `~/.agents/skills/`.
3. Copy `.codex/config.toml` to `~/.codex/config.codex-helper.example.toml` and merge what you need into `~/.codex/config.toml`.
4. Optionally append `templates/global-AGENTS.md` guidance into `~/.codex/AGENTS.md`.

Detailed instructions: `docs/getting-all-assets-locally.md`.

## Decision docs

- Codex routing playbook: `docs/routing-playbook.md`
- Repo structure: `docs/repo-layout.md`
- Official Codex alignment notes (verified 2026-03-18): `docs/latest-openai-codex-notes-2026-03-18.md`

## Current official docs alignment (verified 2026-03-18)

This repo was cross-checked against current OpenAI Codex docs:
- Codex docs hub: <https://developers.openai.com/codex>
- CLI docs: <https://developers.openai.com/codex/cli>
- Config basics: <https://developers.openai.com/codex/config-basic>
- AGENTS.md docs: <https://developers.openai.com/codex/agents-md>
- Skills docs: <https://developers.openai.com/codex/skills>
- Subagents docs: <https://developers.openai.com/codex/subagents>
- Codex models docs: <https://developers.openai.com/codex/models>
- Open-source Codex repo: <https://github.com/openai/codex>
