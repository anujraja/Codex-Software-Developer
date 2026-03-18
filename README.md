# Codex-Software-Developer

Canonical, English-first, reproducible knowledge base for Codex agents, subagents, skills, roles, jobs, systems, prompts, and workflows, plus an install-ready Codex helper toolkit.

## What This Repo Does

- Aggregates multiple public agent/skill repositories into one canonical index.
- Deduplicates agent names and generates one merged canonical definition per name.
- Preserves detailed provenance for canonical output files.
- Builds Obsidian-friendly docs and relationship maps.
- Provides portable local install assets (custom agents/skills/scripts) for Codex users.

## Source Repositories

- `am-will/codex-skills` (`main`)
- `proflead/codex-skills-library` (`master`)
- `VoltAgent/awesome-codex-subagents` (`main`)
- `Dimillian/Skills` (`main`)
- `ComposioHQ/awesome-codex-skills` (`master`)
- `msitarzewski/agency-agents` (`main`)

## Current Snapshot

- Indexed source files: **1280**
- Indexed binary assets: **57** (indexed only, not copied)
- Canonical agents: **627**
- Canonical skills: **130**
- Canonical prompts: **20**
- Cross-repo duplicate agent names merged: **51**

## Repository Layout

```text
config/                 # source definitions
scripts/                # reproducible build/index/validate pipeline + helper install scripts
catalog/                # machine-readable manifests and normalized contracts
knowledge/agents/       # canonical merged agent TOMLs
knowledge/skills/       # canonical skill markdown
knowledge/prompts/      # canonical prompt markdown
docs/                   # source map, merge policy, matrix, install/routing guides
Obsidian-Helper.md      # vault-first relationship guide
for_obsidian/           # copy-ready Codex helper bundle for Obsidian
.codex/agents/          # installable custom Codex agents
.agents/skills/         # installable custom Codex skills
```

## Canonical Pipeline Quickstart

```bash
python3 scripts/fetch_sources.py
python3 scripts/index_files.py
python3 scripts/extract_entities.py
python3 scripts/build_canonical.py
python3 scripts/build_docs.py
python3 scripts/validate_repo.py
```

## Codex Helper Toolkit Quickstart

```bash
# Install local Codex assets from this repo
./scripts/install_codex_helper.sh

# Optional: append reusable global guidance into ~/.codex/AGENTS.md
./scripts/install_codex_helper.sh --with-global-guidance

# Optional: force overwrite matching assets (with backup)
./scripts/install_codex_helper.sh --force

# Export copy-ready Obsidian bundle
./scripts/export_obsidian_bundle.sh "/path/to/YourObsidianVault"
```

## Human Setup (No Scripts)

1. Copy `.codex/agents/*.toml` to `~/.codex/agents/`.
2. Copy `.agents/skills/*` to `~/.agents/skills/`.
3. Copy `.codex/config.toml` to `~/.codex/config.codex-helper.example.toml`.
4. Optionally append `templates/global-AGENTS.md` into `~/.codex/AGENTS.md`.

## Routing And Decision Docs

- Local install and sync: `docs/getting-all-assets-locally.md`
- End-to-end setup and demo how-to: `docs/how-to-codex-helper-end-to-end.md`
- Skill/agent routing playbook: `docs/routing-playbook.md`
- Repo structure notes: `docs/repo-layout.md`
- Codex official docs alignment (verified 2026-03-18): `docs/latest-openai-codex-notes-2026-03-18.md`

## Official Codex References (Verified 2026-03-18)

- <https://developers.openai.com/codex>
- <https://developers.openai.com/codex/cli>
- <https://developers.openai.com/codex/config-basic>
- <https://developers.openai.com/codex/agents-md>
- <https://developers.openai.com/codex/skills>
- <https://developers.openai.com/codex/subagents>
- <https://developers.openai.com/codex/models>
- <https://github.com/openai/codex>
